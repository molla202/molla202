<div align="center">

# 🌐 Gnoland Test13 Full Node & Validator Kurulum Rehberi

<img width="1200" height="630" alt="og-gnoland" src="https://github.com/user-attachments/assets/a7d172d8-dea4-4cfa-88ed-edddc107f9a7" />

[![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04+-E95420?style=flat-square&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![Gnoland](https://img.shields.io/badge/Gnoland-Test13-A259FF?style=flat-square)](https://gno.land)
[![Branch](https://img.shields.io/badge/Branch-chain%2Ftest13-brightgreen?style=flat-square)](https://github.com/gnolang/gno)
[![Chain ID](https://img.shields.io/badge/Chain%20ID-test--13-blue?style=flat-square)](https://docs.gno.land)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

## İçindekiler

- [Donanım Gereksinimleri](#donanım-gereksinimleri)
- [Ağ Bilgileri](#ağ-bilgileri)
- [Adım 1 — Sistem Doğrulama](#adım-1--sistem-doğrulama)
- [Adım 2 — Sistem Güncellemesi ve Bağımlılıklar](#adım-2--sistem-güncellemesi-ve-bağımlılıklar)
- [Adım 3 — Go Kurulumu](#adım-3--go-kurulumu)
- [Adım 4 — Değişkenleri Ayarlama](#adım-4--değişkenleri-ayarlama)
- [Adım 5 — Binary Derleme](#adım-5--binary-derleme)
- [Adım 6 — Node Yapılandırması](#adım-6--node-yapılandırması)
- [Adım 7 — Genesis ve Veri Dizini](#adım-7--genesis-ve-veri-dizini)
- [Adım 8 — Systemd Servis Oluşturma](#adım-8--systemd-servis-oluşturma)
- [Adım 9 — Node'u Başlatma](#adım-9--nodeu-başlatma)
- [Adım 10 — Cüzdan Oluşturma](#adım-10--cüzdan-oluşturma)
- [Adım 11 — Validator Kaydı](#adım-11--validator-kaydı)
- [Faydalı Komutlar](#faydalı-komutlar)
- [Güncel Kalmak](#güncel-kalmak)

---

## Donanım Gereksinimleri

| Bileşen | Minimum | Önerilen |
|---|---|---|
| İşletim Sistemi | Ubuntu 22.04+ | Ubuntu 24.04 |
| CPU | 4 çekirdek | 8 çekirdek |
| RAM | 8 GB | 16 GB |
| Disk | 200 GB SSD | 500 GB NVMe SSD |
| Ağ | 100 Mbps | 1 Gbps |

> ℹ️ Gnoland bir testnet'tir — donanım gereksinimleri üretim zincirlerine kıyasla daha düşüktür.

---

## Ağ Bilgileri

| Tür | Endpoint |
|---|---|
| RPC | https://rpc.test13.testnets.gno.land |
| Explorer | https://test13.testnets.gno.land |
| Faucet | https://test13.testnets.gno.land/faucet |
| Valopers | https://test13.testnets.gno.land/r/gnops/valopers |
| Aktif Validatorlar | https://test13.testnets.gno.land/r/sys/validators/v3 |
| Resmi Dokümantasyon | https://docs.gno.land |
| GitHub | https://github.com/gnolang/gno |

---

## Adım 1 — Sistem Doğrulama

Sunucuya SSH bağlantısı sağladıktan sonra sistem gereksinimlerini doğrulayın:

```bash
lsb_release -a
uname -r
lscpu | grep -E "Model name|CPU\(s\)|Thread|Socket|Core"
free -h
df -h
```

---

## Adım 2 — Sistem Güncellemesi ve Bağımlılıklar

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git wget htop tmux build-essential jq make lz4 gcc unzip \
  screen btop iotop nethogs hdparm cmake perl automake autoconf libtool libssl-dev zstd pv
```

---

## Adım 3 — Go Kurulumu

Gnoland **Go 1.22+** gerektirir. Bu adım Go 1.23'ü kurar ve PATH ayarlarını yapılandırır:

```bash
cd $HOME
VER="1.23.0"
wget "https://golang.org/dl/go$VER.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go$VER.linux-amd64.tar.gz"
rm "go$VER.linux-amd64.tar.gz"

[ ! -f ~/.bash_profile ] && touch ~/.bash_profile
echo 'export PATH=/usr/local/go/bin:$HOME/go/bin:$PATH' >> ~/.bash_profile
echo 'export GNOROOT=$HOME/gno' >> ~/.bash_profile
source $HOME/.bash_profile
[ ! -d ~/go/bin ] && mkdir -p ~/go/bin
export PATH="$HOME/go/bin:$PATH"
```

Kurulumu doğrulayın:

```bash
go version
```

Beklenen çıktı:
```
go version go1.23.0 linux/amd64
```

---

## Adım 4 — Değişkenleri Ayarlama

Aşağıdaki değişkenleri kendi bilgilerinizle güncelleyip çalıştırın:

```bash
echo "export WALLET="wallet"" >> $HOME/.bash_profile
echo "export MONIKER="node-adiniz"" >> $HOME/.bash_profile
echo "export GNOLAND_CHAIN_ID="test13"" >> $HOME/.bash_profile
echo "export GNOLAND_PORT="54"" >> $HOME/.bash_profile
source $HOME/.bash_profile
```

> ℹ️ `GNOLAND_PORT` aynı sunucuda birden fazla node çalıştırıyorsanız port çakışmasını önler. Varsayılan `26` yerine `54` kullanılmaktadır (RPC: `54657`, P2P: `54656`).

---

## Adım 5 — Binary Derleme

Resmi gno deposunu klonlayın ve test13 branch'ine geçin:

```bash
cd $HOME
rm -rf gno
git clone https://github.com/gnolang/gno.git
cd gno
git checkout chain/test13
```

Binary'leri derleyin ve kurun:

```bash
make -C gno.land install.gnoland install.gnokey
```

Kurulumu doğrulayın:

```bash
gnoland version
gnokey version
```

---

## Adım 6 — Node Yapılandırması

Config ve secrets dosyalarını oluşturun:

```bash
cd $HOME/gno
gnoland config init
gnoland secrets init -data-dir $HOME/gno/gnoland-data/secrets/
```

Tüm gerekli yapılandırma ayarlarını uygulayın:

```bash
gnoland config set rpc.laddr tcp://0.0.0.0:${GNOLAND_PORT}657
gnoland config set p2p.laddr tcp://0.0.0.0:${GNOLAND_PORT}656
gnoland config set proxy_app tcp://127.0.0.1:${GNOLAND_PORT}658
gnoland config set moniker $MONIKER
gnoland config set application.prune_strategy syncable
gnoland config set consensus.timeout_commit 3s
gnoland config set consensus.peer_gossip_sleep_duration 10ms
gnoland config set p2p.flush_throttle_timeout 10ms
gnoland config set mempool.size 10000
gnoland config set p2p.external_address "$(wget -qO- eth0.me):${GNOLAND_PORT}656"
gnoland config set p2p.max_num_outbound_peers 40
gnoland config set p2p.persistent_peers \
  "g142k7zc2qym3c0u6jmkf6rv26llgr2f4nakmlmt@sentry-1.test13.testnets.gno.land:26656,g1lxkf9gn7kddrr26c640ww5wg3ezsm22we8cjpc@sentry-2.test13.testnets.gno.land:26656"
```

---

## Adım 7 — Genesis ve Veri Dizini

Veri dizinini ana dizine taşıyın ve genesis dosyasını indirin:

```bash
mv $HOME/gno/gnoland-data $HOME/gnoland-data
cd $HOME/gnoland-data/config
wget -O genesis.json https://github.com/gnolang/gno/releases/download/chain/test13/genesis.json
```

Genesis hash'ini doğrulayın — **hash tam olarak eşleşmelidir**:

```bash
shasum -a 256 genesis.json
```

Beklenen çıktı:
```
56f56e135174feff9f93283d5ec7e4ec955cd5155108aff5009d4fd51c5adaf2  genesis.json
```

> ⚠️ Hash eşleşmiyorsa devam etmeyin. Genesis dosyasını tekrar indirin.

---

## Adım 8 — Systemd Servis Oluşturma

Node'u yönetilen bir arka plan süreci olarak çalıştırmak için systemd servis dosyasını oluşturun:

```bash
sudo tee /etc/systemd/system/gnoland.service > /dev/null <<EOF
[Unit]
Description=Gnoland node
After=network-online.target

[Service]
User=$USER
WorkingDirectory=$HOME
Environment=HOME=$HOME
Environment=GNOROOT=$HOME/gno
ExecStart=$(which gnoland) start \
  --chainid test-13 \
  --genesis $HOME/gnoland-data/config/genesis.json \
  --data-dir $HOME/gnoland-data/ \
  --skip-genesis-sig-verification
Restart=on-failure
RestartSec=5
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable gnoland
```

---

## Adım 9 — Node'u Başlatma

Servisi başlatın ve logları takip edin:

```bash
sudo systemctl restart gnoland && sudo journalctl -u gnoland -f
```

Servis durumunu doğrulayın:

```bash
sudo systemctl status gnoland --no-pager
```

Beklenen çıktı:
```
● gnoland.service - Gnoland node
     Active: active (running) since ...
```

Senkronizasyon durumunu kontrol edin:

```bash
curl -s http://localhost:${GNOLAND_PORT}657/status | jq .result.sync_info
```

Tam senkronize olunduğunda beklenen çıktı:
```json
{
  "latest_block_height": "XXXXXX",
  "catching_up": false
}
```

> ⚠️ `catching_up` değeri `false` olana kadar validator kaydına geçmeyin.

---

## Adım 10 — Cüzdan Oluşturma

Yeni cüzdan oluşturun:

```bash
gnokey add $WALLET
```

> ⚠️ **KRİTİK:** Mnemonic phrase gösterilecektir. Hemen güvenli bir yere kaydedin. Kaybolursa cüzdanınızı kurtaramazsınız.

Mevcut bir cüzdanı mnemonic ile kurtarmak için:

```bash
gnokey add $WALLET --recover
```

Cüzdanlarınızı listeleyin ve `g1...` adresinizi alın:

```bash
gnokey list
```

Test GNOT almak için faucet'i kullanın: **https://test13.testnets.gno.land/faucet**

Bakiyenizi doğrulayın:

```bash
gnokey query \
  -remote "https://rpc.test13.testnets.gno.land" \
  auth/accounts/$(gnokey list | grep "^*" | awk '{print $3}')
```

---

## Adım 11 — Validator Kaydı

> ⚠️ Gnoland **GovDAO tabanlı validator kayıt** sistemi kullanır. Kayıt bir realm (akıllı sözleşme) çağrısıyla yapılır. Validator setine dahil olmak için GovDAO yönetişim önerisinin kabul edilmesi gerekir — kayıt tek başına yeterli değildir.

### Validator Public Key'ini Alın

```bash
cd $HOME/gnoland-data && gnoland secrets get validator_key
```

Beklenen çıktı:
```json
{
  "address": "g1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "pub_key": "gpub1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

> ⚠️ Kayıt için yalnızca `pub_key` kullanılır. Buradaki `address` consensus key adresidir — operator adresi olarak **kullanmayın**. Operator adresi olarak `gnokey list` çıktısındaki cüzdan adresinizi kullanın.

### Validator Kaydını Gönderin

Çalıştırmadan önce `VAL_PUBKEY` değerini yukarıdaki çıktıdan alın:

```bash
gnokey maketx call \
  --pkgpath gno.land/r/gnops/valopers \
  --func Register \
  --args "$MONIKER" \
  --args "ACIKLAMA" \
  --args "data-center" \
  --args "$(gnokey list | grep "^*" | awk '{print $3}')" \
  --args "VAL_PUBKEY" \
  --gas-fee 1000000ugnot \
  --gas-wanted 50000000 \
  --chainid test-13 \
  --remote https://rpc.test13.testnets.gno.land \
  --broadcast \
  $WALLET
```
### Alternatif validator olma

 - siteye gidin pubkey yazın bilgilerinizi doldurun işlemi yollayın `https://gno.satai.0xgen.online/register`
 
| Parametre | Açıklama |
|---|---|
| `$MONIKER` | `.bash_profile`'dan otomatik gelir |
| `ACIKLAMA` | Validator hakkında kısa açıklama (elle girin) |
| `data-center` | Altyapı konumunuz |
| `VAL_PUBKEY` | `gnoland secrets get validator_key` çıktısındaki `pub_key` |
| `$WALLET` | `.bash_profile`'dan otomatik gelir |

> ℹ️ Başarılı işlem sonrası profilinizi şu adreste görüntüleyebilirsiniz:  
> https://test13.testnets.gno.land/r/gnops/valopers

### Açıklama Güncelleme (Opsiyonel)

Açıklama limiti **2048 karakterdir**. Kayıt sonrası güncellemek için:

```bash
gnokey maketx call \
  --pkgpath gno.land/r/gnops/valopers \
  --func UpdateDescription \
  --args "$(gnokey list | grep "^*" | awk '{print $3}')" \
  --args "YENI-ACIKLAMANIZ" \
  --gas-fee 1000000ugnot \
  --gas-wanted 50000000 \
  --chainid test-13 \
  --remote https://rpc.test13.testnets.gno.land \
  --broadcast \
  $WALLET
```

---

## Faydalı Komutlar

### Servis Yönetimi

```bash
sudo systemctl start gnoland
sudo systemctl stop gnoland
sudo systemctl restart gnoland
sudo systemctl status gnoland
```

### Loglar ve Senkronizasyon

```bash
# Canlı loglar
sudo journalctl -u gnoland -f --no-hostname -o cat

# Son bir saatin logları
sudo journalctl -u gnoland --since "1 hour ago"

# Senkronizasyon durumu
curl -s http://localhost:${GNOLAND_PORT}657/status | jq .result.sync_info

# Bağlı peer sayısı
curl -s http://localhost:${GNOLAND_PORT}657/net_info | jq .result.n_peers
```

### Node Bilgileri

```bash
# Node ID
cd $HOME/gnoland-data && gnoland secrets get node_id

# Validator key
cd $HOME/gnoland-data && gnoland secrets get validator_key

# Tüm secrets
cd $HOME/gnoland-data && gnoland secrets get
```

### Cüzdan ve Bakiye

```bash
# Cüzdanları listele
gnokey list

# Bakiye sorgula
gnokey query \
  -remote "https://rpc.test13.testnets.gno.land" \
  auth/accounts/G1-ADRESINIZ
```

### Token Gönderme

```bash
gnokey maketx send \
  -send "1000000ugnot" \
  -to "ALICI_ADRESI" \
  -gas-fee 1000000ugnot \
  -gas-wanted 10000000 \
  -broadcast \
  -chainid "test-13" \
  -remote "https://rpc.test13.testnets.gno.land" \
  $WALLET
```

---

## Güvenlik Duvarı

```bash
# P2P — herkese açık olmalıdır
sudo ufw allow ${GNOLAND_PORT}656/tcp comment "gnoland P2P"

# RPC — sadece public endpoint sunuyorsanız açın
sudo ufw allow ${GNOLAND_PORT}657/tcp comment "gnoland RPC"
```

---

## Güncel Kalmak

- Discord: [Gnoland Discord](https://discord.com/invite/S8nKUqwkPn)
- GitHub: [gnolang/gno](https://github.com/gnolang/gno)
- Resmi Dokümantasyon: [docs.gno.land](https://docs.gno.land)
- Explorer: [test13.testnets.gno.land](https://test13.testnets.gno.land)

### Yeni Versiyona Güncelleme

```bash
sudo systemctl stop gnoland

cd $HOME/gno
git fetch --all --tags
git checkout chain/test14
make -C gno.land install.gnoland install.gnokey

sudo systemctl restart gnoland
sudo journalctl -u gnoland -f --no-hostname -o cat
```

---
