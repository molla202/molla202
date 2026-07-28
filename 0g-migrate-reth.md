# 🔄 Corenode Altyapısı: Canlı Düğümden Geth'den Reth'e Geçiş (Migration) Rehberi

Bu döküman, sunucunuzda halihazırda çalışan ve altyapı standartlarımıza göre kurulu olan `0gchaind` ve `geth` servislerini koruyarak yürütme katmanını Reth katmanına taşır.

---

## 1️⃣ Servisleri Durdurma ve Güvenlik Yedeği

> ⚠️ **Önemli Değişiklik:** Blok numarasını servisleri durdurmadan önce değil, **durdurduktan sonra** alıyoruz. Bu sayede geth'in DB'sindeki gerçek son blok yakalanır; canlıyken alınan numara o sırada işlenmekte olan birkaç bloğu atlar.

### Servisleri durdur

```bash
sudo systemctl stop 0gchaind geth
```

### Geth DB'sinden son blok numarasını oku (kesin yöntem)

```bash
export CHAIN_HEAD=$($HOME/go/bin/geth \
  --datadir $HOME/.0gchaind/0g-home/geth-home \
  console --exec "eth.blockNumber" 2>/dev/null)

echo "Yakalanan Son Blok Yüksekliği (CHAIN_HEAD): $CHAIN_HEAD"
```

> Bu değeri not edin. Geth kapalıyken DB değişmez — alınan numara export ile birebir eşleşir.

### Yedek klasörü oluşturma

```bash
BACKUP_DIR="$HOME/.0gchaind/backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p $BACKUP_DIR
```

### Sadece Consensus verisini yedekliyoruz

```bash
cp -r $HOME/.0gchaind/0g-home/0gchaind-home $BACKUP_DIR/0gchaind-home
```

---

## 2️⃣ Aristotle v1.0.6 Paketi ve Klasör Düzeni

```bash
cd $HOME
wget -O aristotle.tar.gz https://github.com/0gfoundation/0gchain-Aristotle/releases/download/v1.0.6/aristotle-v1.0.6.tar.gz
tar -xzvf aristotle.tar.gz -C $HOME
rm -rf aristotle.tar.gz
```

### Klasör ismini Corenode standardına çeviriyoruz

```bash
mv $HOME/Aristotle-v1.0.6 $HOME/aristotle-used
```

### Binary yetkilerini verip go/bin altına taşıyoruz

```bash
sudo chmod 777 $HOME/aristotle-used/bin/*
cp $HOME/aristotle-used/bin/reth $HOME/go/bin/reth
cp $HOME/aristotle-used/bin/0gchaind $HOME/go/bin/0gchaind
```

### Yeni reth veritabanı klasörünü açıyoruz

```bash
mkdir -p $HOME/.0gchaind/0g-home/reth-home
```

### Gerekli JWT ve KZG dosyalarını kopyalıyoruz

```bash
cp $HOME/aristotle-used/jwt.hex $HOME/.0gchaind/0g-home/
cp $HOME/aristotle-used/kzg-trusted-setup.json $HOME/.0gchaind/0g-home/
```

---

## 3️⃣ Geth Verilerini İhraç Etme (Export RLP)

> ⏳ **Bu işlem disk hızına bağlı olarak uzun süreceği için `tmux` veya `screen` oturumunda çalıştırın!**

```bash
$HOME/go/bin/geth export \
  --datadir $HOME/.0gchaind/0g-home/geth-home \
  $HOME/.0gchaind/0g-home/chain-export.rlp \
  1 $CHAIN_HEAD
```

---

## 4️⃣ Reth İlklendirme ve RLP Filtreleme (Trim)

### Reth'i genesis dosyası ile ilklendir

```bash
reth init \
  --chain $HOME/aristotle-used/geth-genesis.json \
  --datadir $HOME/.0gchaind/0g-home/reth-home
```

### Trim scriptini oluştur

```bash
sudo tee $HOME/.0gchaind/0g-home/trim_export.py > /dev/null <<EOF
import sys

input_file = "$HOME/.0gchaind/0g-home/chain-export.rlp"
output_file = "$HOME/.0gchaind/0g-home/chain-export-from-{start}.rlp"

start_block = int(sys.argv[1]) if len(sys.argv) > 1 else 1
output_file = output_file.format(start=start_block)

print(f"Trimming blocks before {start_block}, output: {output_file}")

def read_rlp_length(f):
    first = f.read(1)
    if not first:
        return None, 0
    b = first[0]
    if b < 0xc0:
        return None, 0
    elif b <= 0xf7:
        return first, b - 0xc0
    else:
        len_bytes_count = b - 0xf7
        len_bytes = f.read(len_bytes_count)
        return first + len_bytes, int.from_bytes(len_bytes, 'big')

def get_block_number(block_data):
    offset = 0
    b = block_data[offset]
    offset += 1 if b <= 0xf7 else 1 + (b - 0xf7)
    b = block_data[offset]
    offset += 1 if b <= 0xf7 else 1 + (b - 0xf7)
    for _ in range(8):
        b = block_data[offset]
        if b <= 0x80:
            offset += 1
        elif b <= 0xb7:
            offset += 1 + (b - 0x80)
        elif b <= 0xbf:
            n = b - 0xb7
            offset += 1 + n + int.from_bytes(block_data[offset+1:offset+1+n], 'big')
        elif b <= 0xf7:
            offset += 1 + (b - 0xc0)
        else:
            n = b - 0xf7
            offset += 1 + n + int.from_bytes(block_data[offset+1:offset+1+n], 'big')
    b = block_data[offset]
    if b == 0x80: return 0
    if b < 0x80: return b
    length = b - 0x80
    return int.from_bytes(block_data[offset+1:offset+1+length], 'big')

block_count = 0
skipped = 0

with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
    while True:
        header_bytes, length = read_rlp_length(fin)
        if header_bytes is None:
            break
        block_body = fin.read(length)
        if len(block_body) < length:
            break
        full_block = header_bytes + block_body
        try:
            block_number = get_block_number(full_block)
        except Exception as e:
            print(f"Warning: could not parse block at index {block_count + skipped}, writing anyway: {e}")
            fout.write(full_block)
            block_count += 1
            continue
        if block_number < start_block:
            skipped += 1
            if skipped % 100000 == 0:
                print(f"Skipped {skipped} blocks (current: {block_number})...")
        else:
            fout.write(full_block)
            block_count += 1
            if block_count % 100000 == 0:
                print(f"Written {block_count} blocks (current: {block_number})...")

print(f"Done. Skipped {skipped}, wrote {block_count} blocks to {output_file}")
EOF
```

### Ayıklama işlemini başlat

```bash
python3 $HOME/.0gchaind/0g-home/trim_export.py 1
```

---

## 5️⃣ Blok Verilerini Reth İçine İthal Etme (Import)

```bash
nohup $HOME/go/bin/reth import \
  --chain $HOME/aristotle-used/geth-genesis.json \
  --datadir $HOME/.0gchaind/0g-home/reth-home \
  $HOME/.0gchaind/0g-home/chain-export-from-1.rlp \
  >> $HOME/.0gchaind/0g-home/reth-import.log 2>&1 &
```

### İthalat durumunu izle

```bash
tail -f $HOME/.0gchaind/0g-home/reth-import.log
```

> ⛔ **KRİTİK:** `reth-import.log` dosyasındaki işlemler tamamen bitmeden ve reth ağ yüksekliğine ulaşmadan asla bir sonraki adıma geçip servisleri başlatmayın. Aksi takdirde sistem `-38002 Invalid forkchoice state` hatası verir.

---

## 6️⃣ Konfigürasyon Güncellemesi ve Yeni Servis Dosyaları

### app.toml engine bağlantısını güncelle

```bash
sed -i "s|^rpc-dial-url *=.*|rpc-dial-url = \"http://localhost:${OG_PORT}551\"|" \
  $HOME/.0gchaind/0g-home/0gchaind-home/config/app.toml
```

### Eski servisleri temizle

```bash
sudo systemctl disable geth
sudo rm -f /etc/systemd/system/geth.service
```

### Yeni reth.service dosyasını oluştur

```bash
sudo tee /etc/systemd/system/reth.service > /dev/null <<EOF
[Unit]
Description=0G Labs Reth Execution Client
After=network.target

[Service]
User=$USER
Type=simple
WorkingDirectory=$HOME/aristotle-used
ExecStart=$HOME/go/bin/reth node \\
  --chain $HOME/aristotle-used/geth-genesis.json \\
  --http \\
  --http.addr 0.0.0.0 \\
  --http.port ${OG_PORT}545 \\
  --http.api eth,net,admin \\
  --authrpc.addr 0.0.0.0 \\
  --authrpc.port ${OG_PORT}551 \\
  --authrpc.jwtsecret $HOME/.0gchaind/0g-home/jwt.hex \\
  --datadir $HOME/.0gchaind/0g-home/reth-home \\
  --ipcpath $HOME/.0gchaind/0g-home/reth-home/eth-engine.ipc \\
  --engine.persistence-threshold 0 \\
  --engine.memory-block-buffer-target 0 \\
  --bootnodes="enode://2bf74c837a98c94ad0fa8f5c58a428237d2040f9269fe622c3dbe4fef68141c28e2097d7af6ebaa041194257543dc112514238361a6498f9a38f70fd56493f96@8.221.140.134:30303" \\
  --port ${OG_PORT}303 \\
  --nat extip:\$(curl -s http://ipv4.icanhazip.com)
Restart=always
RestartSec=3
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF
```

### Güncellenmiş 0gchaind.service dosyasını oluştur

```bash
sudo tee /etc/systemd/system/0gchaind.service > /dev/null <<EOF
[Unit]
Description=0GChainD Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$HOME/aristotle-used
ExecStart=$HOME/go/bin/0gchaind start \\
  --rpc.laddr tcp://0.0.0.0:${OG_PORT}657 \\
  --chaincfg.chain-spec mainnet \\
  --chaincfg.kzg.trusted-setup-path=$HOME/.0gchaind/0g-home/kzg-trusted-setup.json \\
  --chaincfg.engine.jwt-secret-path=$HOME/.0gchaind/0g-home/jwt.hex \\
  --chaincfg.block-store-service.enabled \\
  --chaincfg.node-api.enabled \\
  --chaincfg.node-api.address 0.0.0.0:${OG_PORT}500 \\
  --chaincfg.engine.rpc-dial-url=http://localhost:${OG_PORT}551 \\
  --pruning=nothing \\
  --chaincfg.restaking.enabled \\
  --chaincfg.restaking.symbiotic-rpc-dial-url $ETH_RPC_URL \\
  --chaincfg.restaking.symbiotic-get-logs-block-range 1 \\
  --home=$HOME/.0gchaind/0g-home/0gchaind-home \\
  --p2p.external_address=\$(curl -s http://ipv4.icanhazip.com):${OG_PORT}656
Restart=always
RestartSec=5
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF
```

---

## 7️⃣ Yeni Servisleri Devreye Alma

```bash
sudo systemctl daemon-reload
sudo systemctl enable reth 0gchaind
```

### Önce Reth katmanını başlat

```bash
sudo systemctl start reth
```

### Engine API portunun dinlemede olduğunu teyit et

```bash
ss -tlnp | grep ${OG_PORT}551
```

### Doğrulama tamamsa Consensus katmanını başlat

```bash
sudo systemctl start 0gchaind
```

---

## 📊 Canlı Log Takibi

```bash
# Reth izleme
sudo journalctl -u reth -f -o cat

# 0gchaind izleme
sudo journalctl -u 0gchaind -f -o cat
```

---

## ⚡ OTO MİGRATE (Tek Komutla)

### 1. Bağımlılık kontrolü

```bash
sudo apt update && sudo apt install curl -y
```

### 2. Scripti indir ve yetkilendir

```bash
curl -o $HOME/migrate.sh https://raw.githubusercontent.com/Core-Node-Team/0G-Mainnet/refs/heads/main/migrate.sh
chmod +x $HOME/migrate.sh
```

### 3. Scripti başlat

```bash
source $HOME/.bash_profile
$HOME/migrate.sh
```

### ⚙️ Script Çalışırken Dikkat Edilmesi Gerekenler

- **Blok Yakalama:** Script önce servisleri durdurur, ardından geth DB'sinden kesin son blok numarasını alır.
- **İthalat Aşaması (Adım 5):** Script `Corenode_Reth_Import` adında yeni bir Screen oturumu açıp ithalatı orada başlatır ve işlem bitene kadar ana ekranda bekler.
- **Canlı İthalat Loglarını İzleme:** Yeni bir terminal sekmesinde:

```bash
screen -r Corenode_Reth_Import
```

> Screen'den çıkmak için: `Ctrl + A` → `D`

- İthalat bittiğinde script otomatik olarak uyanır, konfigürasyonları günceller ve servisleri başlatır.
