# Safrochain Mainnet Node Rehberi

<img width="709" height="127" alt="image" src="https://github.com/user-attachments/assets/c6ec0398-afc0-4508-b5c7-9f5e5f74ba9f" />


> **Hazırlayan:** OshVanK  
> **Chain:** `safrochain-1` | **Versiyon:** `v0.2.2` | **Go:** `1.25.8`  
> **Genesis zamanı:** `2026-06-25T10:00:00Z`

---

## İçindekiler

1. [Hızlı Başlangıç — Otomatik Kurulum](#1-hızlı-başlangıç--otomatik-kurulum)
2. [Manuel Kurulum](#2-manuel-kurulum)
3. [Cüzdan İşlemleri](#3-cüzdan-i̇şlemleri)
4. [Validator İşlemleri](#4-validator-i̇şlemleri)
5. [Senkronizasyon Kontrolü](#5-senkronizasyon-kontrolü)
6. [Faydalı Komutlar](#6-faydalı-komutlar)
7. [Node'u Silme](#7-nodeu-silme)
8. [Ağ Bilgileri](#8-ağ-bilgileri)

---

## 1. Hızlı Başlangıç — Otomatik Kurulum

Kurulum scriptini indirin ve çalıştırın:

```bash
wget -O safrochain_mainnet.sh https://raw.githubusercontent.com/Edsny1/SafroChain-Mainnet/refs/heads/Edsny/safrochain_mainnet.sh
chmod +x safrochain_mainnet.sh
./safrochain_mainnet.sh
```

Script sizden şunları isteyecektir:
- **MONIKER** — node adınız
- **Port prefix** — varsayılan `26` (başka node'larınız varsayılan portları kullanıyorsa değiştirin)
- **Cüzdan adı** — varsayılan `wallet`

> **Aynı sunucuda birden fazla node çalışıyorsa:** Script yalnızca `/usr/local/go` dizinini günceller. `~/go/bin` içindeki mevcut binary'ler (lumerad, gnoland, atomoned vb.) önceden derlenmiş dosyalardır, Go'ya çalışma zamanında ihtiyaç duymazlar ve etkilenmezler.

---

## 2. Manuel Kurulum

### 2.1 Sistem Bağımlılıkları

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git wget htop tmux build-essential jq make lz4 gcc unzip
```

### 2.2 Go 1.25.8 Kurulumu

```bash
cd $HOME
wget https://go.dev/dl/go1.25.8.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.25.8.linux-amd64.tar.gz
rm go1.25.8.linux-amd64.tar.gz

echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> ~/.bashrc
source ~/.bashrc

go version
# Beklenen: go version go1.25.8 linux/amd64
```

### 2.3 safrochaind v0.2.2 Derleme

```bash
cd $HOME
git clone https://github.com/Safrochain-Org/safrochain-node ~/safrochain-node
cd ~/safrochain-node
git fetch --tags
git checkout v0.2.2
make build
```

<img width="745" height="448" alt="image" src="https://github.com/user-attachments/assets/980d4c51-c21c-47dc-aef3-7e1df98ca415" />


### 2.4 Cosmovisor Kurulumu

```bash
go install cosmossdk.io/tools/cosmovisor/cmd/cosmovisor@latest
```
```bash
mkdir -p $HOME/.safrochain/cosmovisor/genesis/bin
mkdir -p $HOME/.safrochain/cosmovisor/upgrades
mv $HOME/safrochain-node/bin/safrochaind $HOME/.safrochain/cosmovisor/genesis/bin/safrochaind
```
```bash
sudo ln -s $HOME/.safrochain/cosmovisor/genesis $HOME/.safrochain/cosmovisor/current -f
sudo ln -s $HOME/.safrochain/cosmovisor/current/bin/safrochaind /usr/local/bin/safrochaind -f
```
### 2.5 Node'u Başlat (Init)

```bash
safrochaind init "MONIKER_ADINIZ" --chain-id safrochain-1 --home $HOME/.safrochain
```

### 2.6 Genesis İndir ve Doğrula

```bash
curl -L https://raw.githubusercontent.com/Safrochain-Org/mainnet-genesis/main/genesis.json \
    -o $HOME/.safrochain/config/genesis.json
```

### 2.7 Peer Yapılandırması (config.toml)

```bash
SEEDS="bc772fdc9749e6dfd200a9428f07d86fe4fd34ec@seed.safrochain.network:26666,d323d296ba55e89fb6ce1a724f8da1740bd8cbb0@seed2.safrochain.network:26670"

sed -i -e "s|^seeds *=.*|seeds = \"$SEEDS\"|" $HOME/.safrochain/config/config.toml
```

### 2.8 

- ➡️ Pruning
```
sed -i -e "s/^pruning *=.*/pruning = \"custom\"/" $HOME/.safrochain/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"100\"/" $HOME/.safrochain/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"10\"/" $HOME/.safrochain/config/app.toml
```
- ➡️ Gas Settings
```
sed -i 's|minimum-gas-prices =.*|minimum-gas-prices = "0.05usaf"|g' $HOME/.safrochain/config/app.toml
```
- ➡️ Prometheus & Indexer
```
sed -i 's|^prometheus *=.*|prometheus = true|' $HOME/.safrochain/config/config.toml
sed -i -e 's|^indexer *=.*|indexer = "null"|' $HOME/.safrochain/config/config.toml
```
### 2.9 Systemd Servis Oluşturma

```bash
sudo tee /etc/systemd/system/safrochaind.service > /dev/null << 'EOF'
[Unit]
Description=Safrochain Mainnet Node (Cosmovisor)
After=network-online.target

[Service]
Type=simple
User=root
ExecStart=/root/go/bin/cosmovisor run start --home /root/.safrochain
Restart=on-failure
RestartSec=5s
LimitNOFILE=1048576
TimeoutStopSec=30s
Environment="DAEMON_HOME=/root/.safrochain"
Environment="DAEMON_NAME=safrochaind"
Environment="DAEMON_RESTART_AFTER_UPGRADE=true"
Environment="DAEMON_ALLOW_DOWNLOAD_BINARIES=false"
Environment="UNSAFE_SKIP_BACKUP=true"

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable safrochaind
sudo systemctl start safrochaind
```

---

## 3. Cüzdan İşlemleri

### Cüzdan Oluşturma

```bash
safrochaind keys add wallet
```

> **ÖNEMLİ:** Mnemonic phrase'inizi (24 kelime) güvenli bir yere kaydedin. Kaybolursa kurtarılamaz.

### Cüzdan Kurtarma

```bash
safrochaind keys add wallet --recover
# İstenildiğinde 24 kelimelik mnemonic'inizi girin
```

### Cüzdanları Listeleme

```bash
safrochaind keys list
```

### Cüzdan Adresini Göster

```bash
safrochaind keys show wallet -a
```

### Bakiye Sorgulama

```bash
safrochaind query bank balances \
    $(safrochaind keys show wallet -a) \
    --node https://rpc.safrochain.network:443
```

---

## 4. Validator İşlemleri

### Validator Oluşturma

Validator oluşturmadan önce node'unuzun tamamen senkronize olduğundan emin olun.

```bash
# Validator pubkey'i kontrol et
safrochaind tendermint show-validator

# validator.json dosyası oluştur
cat > $HOME/.safrochain/validator.json << EOF
{
  "pubkey": $(safrochaind tendermint show-validator),
  "amount": "1000000usaf",
  "moniker": "MONIKER_ADINIZ",
  "identity": "",
  "website": "",
  "security": "",
  "details": "Safrochain Mainnet Validator",
  "commission-rate": "0.10",
  "commission-max-rate": "0.20",
  "commission-max-change-rate": "0.01",
  "min-self-delegation": "1"
}
EOF

# Validator oluşturma TX'i gönder
safrochaind tx staking create-validator $HOME/.safrochain/validator.json \
    --from wallet \
    --chain-id safrochain-1 \
    --gas auto \
    --gas-adjustment 1.4 \
    --fees 300usaf \
    -y
```

### Token Stake Etme (Delegate)

```bash
# Validator adresinizi alın
VAL_ADDR=$(safrochaind keys show wallet --bech val -a)

safrochaind tx staking delegate "$VAL_ADDR" 1000000usaf \
    --from wallet \
    --chain-id safrochain-1 \
    --gas auto \
    --gas-adjustment 1.5 \
    --gas-prices 0.05usaf \
    -y
```

### Ödülleri Çekme

```bash
VAL_ADDR=$(safrochaind keys show wallet --bech val -a --home ~/.safrochain)

safrochaind tx distribution withdraw-rewards "$VAL_ADDR" \
    --commission \
    --from wallet \
    --chain-id safrochain-1 \
    --gas auto \
    --gas-adjustment 1.5 \
    --gas-prices 0.05usaf \
    -y
```

### Token Gönderme

```bash
safrochaind tx bank send \
    $(safrochaind keys show wallet -a) \
    ALICI_ADRESI \
    1000000usaf \
    --chain-id safrochain-1 \
    --gas auto \
    --gas-adjustment 1.5 \
    --gas-prices 0.05usaf \
    -y
```

### Validator Durumunu Sorgulama

```bash
# Validator adresiniz
safrochaind keys show wallet --bech val -a

# Validator detayları
safrochaind query staking validator \
    $(safrochaind keys show wallet --bech val -a) \
    --node https://rpc.safrochain.network:443
```

---

## 5. Senkronizasyon Kontrolü

```bash
# Tek seferlik kontrol
curl -s http://localhost:26657/status | jq '.result.sync_info | {latest_block_height, catching_up}'

# Ağ ile karşılaştırma
LOCAL=$(curl -s http://localhost:26657/status | jq -r '.result.sync_info.latest_block_height')
NETWORK=$(curl -s https://rpc.safrochain.network/status | jq -r '.result.sync_info.latest_block_height')
echo "Yerel: $LOCAL | Ağ: $NETWORK | Fark: $((NETWORK - LOCAL)) blok"
```

> Kurulumda özel port prefix kullandıysanız (örn. `53`), `26657` yerine `53657` yazın.

---

## 6. Faydalı Komutlar

### Servis Yönetimi

```bash
# Başlat / Durdur / Yeniden Başlat
sudo systemctl start safrochaind
sudo systemctl stop safrochaind
sudo systemctl restart safrochaind

# Durum kontrolü
sudo systemctl status safrochaind

# Canlı loglar
sudo journalctl -fu safrochaind -o cat
```

### Node Bilgileri

```bash
# Node ID (peer bağlantısı için paylaşın)
safrochaind tendermint show-node-id

# Mevcut blok yüksekliği
safrochaind status --home ~/.safrochain | jq '.SyncInfo.latest_block_height'

# Bağlı peer sayısı
curl -s localhost:26657/net_info | jq '.result.n_peers'
```

### Validator'ı Unjail Etme

Slashing sonrası validator'ı serbest bırakmak için:

```bash
safrochaind tx slashing unjail \
    --from wallet \
    --chain-id safrochain-1 \
    --gas auto \
    --gas-adjustment 1.5 \
    --gas-prices 0.05usaf \
    -y
```

---

## 7. Node'u Silme

> **Uyarı:** Bu işlem geri alınamaz. Önce key dosyalarınızı yedekleyin.

```bash
# Önce keyring'i yedekle
cp -r $HOME/.safrochain/keyring-file $HOME/safrochain_keyring_backup

# Servisi durdur ve devre dışı bırak
sudo systemctl stop safrochaind
sudo systemctl disable safrochaind
sudo rm -f /etc/systemd/system/safrochaind.service
sudo systemctl daemon-reload

# Node verilerini ve kaynak kodunu sil
rm -rf $HOME/.safrochain
rm -rf $HOME/safrochain-node
```

---

## 8. Ağ Bilgileri

| Parametre | Değer |
|-----------|-------|
| Chain ID | `safrochain-1` |
| Binary versiyonu | `v0.2.2` |
| Go versiyonu | `1.25.8` |
| Denom | `usaf` (1 SAF = 1.000.000 usaf) |
| Min gas ücreti | `0.05usaf` |
| Genesis zamanı | `2026-06-25T10:00:00Z` |
| RPC | `https://rpc.safrochain.network` |
| REST (API) | `https://api.safrochain.network` |
| gRPC | `https://grpc.safrochain.network` |
| Durum | `https://status.safrochain.network` |
| Seed 1 | `bc772fdc9749e6dfd200a9428f07d86fe4fd34ec@seed.safrochain.network:26666` |
| Seed 2 | `d323d296ba55e89fb6ce1a724f8da1740bd8cbb0@seed2.safrochain.network:26670` |
| Genesis hash | `c05ac5aec1918df9edb257e8e0eea184d73edc51370eb4aa9f0b4f0aad615c4d` |

---

*Hazırlayan: OshVanK*
*Düzenleyen: Gökhan Molla* 
