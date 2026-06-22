# 🟢 GenLayer Validator Node — Tam Kurulum Rehberi

> Kopyala-yapıştır ile çalışan, adım adım Türkçe manuel kurulum rehberi.  
> Kaynak: [docs.genlayer.com/validators/setup-guide](https://docs.genlayer.com/validators/setup-guide)

---

## 📋 İçindekiler

1. [Sistem Gereksinimleri](#1-sistem-gereksinimleri)
2. [Sunucu Hazırlığı — Gerekli Yazılımları Kur](#2-sunucu-hazırlığı--gerekli-yazılımları-kur)
3. [GenLayer CLI Kurulumu ve Validator Cüzdanı Oluşturma](#3-genlayer-cli-kurulumu-ve-validator-cüzdanı-oluşturma)
4. [Node Yazılımını İndir ve Kur](#4-node-yazılımını-indir-ve-kur)
5. [Konfigürasyon Dosyasını Oluştur](#5-konfigürasyon-dosyasını-oluştur)
6. [Operator Key'i İçe Aktar](#6-operator-keyi-i̇çe-aktar)
7. [LLM Sağlayıcısını Ayarla](#7-llm-sağlayıcısını-ayarla)
8. [Node'u Başlat](#8-nodeu-başlat)
9. [Node'u Arka Planda Çalıştır (screen)](#9-nodeu-arka-planda-çalıştır-screen)
10. [Faydalı Komutlar](#10-faydalı-komutlar)
11. [Sık Yapılan Hatalar](#11-sık-yapılan-hatalar)

---

## 1. Sistem Gereksinimleri

| Kaynak | Gereksinim |
|--------|-----------|
| **RAM** | 16 GB |
| **CPU** | 8 çekirdek — **AMD64 (x86_64) zorunlu!** ARM çalışmaz. |
| **Disk** | 128 GB SSD/NVMe |
| **Ağ** | 100 Mbps |
| **İşletim Sistemi** | 64-bit Linux (Ubuntu 20.04+ önerilir) |
| **Yazılım** | Docker, Docker Compose, Python 3, Node.js v18+, npm |

> ⚠️ **ÖNEMLİ:** Apple M serisi, Raspberry Pi veya herhangi bir ARM işlemcili sunucu **çalışmaz**. Mutlaka AMD64/x86_64 mimarili sunucu kullan.

> 💰 **Token Gereksinimi:** Minimum **42.000 GEN token** stake etmen gerekiyor.

---

## 2. Sunucu Hazırlığı — Gerekli Yazılımları Kur

Sunucuna SSH ile bağlandıktan sonra sırasıyla aşağıdaki adımları uygula.

### 2.1 Sistem Güncellemesi

```bash
sudo apt update && sudo apt upgrade -y
```

### 2.2 Temel Araçları Kur

```bash
sudo apt install -y curl wget git build-essential screen python3 python3-pip python3-venv
```

### 2.3 Docker Kurulumu

```bash
# Eski Docker sürümlerini kaldır (varsa)
sudo apt remove -y docker docker-engine docker.io containerd runc

# Docker resmi GPG anahtarını ekle
sudo apt install -y ca-certificates gnupg lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Docker reposunu ekle
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Docker'ı kur
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Docker'ı sudo'suz kullanmak için kullanıcını gruba ekle
sudo usermod -aG docker $USER

# Grubu aktif et (yeniden login gerekmez)
newgrp docker

# Docker çalışıyor mu kontrol et
docker --version
docker compose version
```

### 2.4 Node.js v18+ Kurulumu

```bash
# NodeSource reposunu ekle (Node.js 18 LTS)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# Node.js'i kur
sudo apt install -y nodejs

# Versiyonu kontrol et (18.x veya üzeri olmalı)
node --version
npm --version
```

### 2.5 Kurulumları Doğrula

```bash
echo "--- Versiyon Kontrolleri ---"
docker --version
docker compose version
node --version
npm --version
python3 --version
echo "--- Mimari Kontrolü (amd64 olmalı) ---"
uname -m
```

> Çıktıda `x86_64` görmelisin. Başka bir şey görüyorsan bu sunucu **çalışmaz**.

---

## 3. GenLayer CLI Kurulumu ve Validator Cüzdanı Oluşturma

> ⚠️ Bu adım **kendi bilgisayarında** (local makinende) veya ayrı güvenli bir ortamda yapılmalıdır. Owner (sahip) adresin soğuk cüzdanda tutulmalıdır.

### 3.1 GenLayer CLI'yi Kur

```bash
npm install -g genlayer
```

```bash
# Kurulumu doğrula
genlayer --version
```

### 3.2 Staking Wizard'ı Çalıştır

```bash
genlayer staking wizard
```

Wizard sana şu adımları soracak:

1. **Hesap kurulumu** — Yeni owner hesabı oluştur veya mevcut cüzdanı seç
2. **Ağ seçimi** — `testnet-asimov` seç
3. **Bakiye kontrolü** — En az 42.000 GEN token olduğunu doğrular
4. **Operator kurulumu** — Sunucunda kullanmak üzere operator keystore dosyası oluşturur ve export eder
5. **Stake miktarı** — Kaç GEN stake etmek istediğini gir (min: 42.000)
6. **Validator oluşturma** — Staking transaction'ı gönderir
7. **Kimlik ayarı** — Moniker (isim), website vb. bilgilerini gir

### 3.3 ÖNEMLİ: Şu Bilgileri Not Al!

Wizard tamamlandığında sana **3 adres** verecek. Bunları bir yere kaydet:

```
Owner Adresi    : 0x...  ← Stake'i çekme yetkisi, SOĞUK CÜZDANDA TUT
Operator Adresi : 0x...  ← Sunucunun blok imzalama adresi (node config'inde lazım)
Validator Wallet: 0x...  ← Akıllı kontrat adresi (node config'inde lazım)
```

### 3.4 Operator Keystore Dosyasını Sunucuya Kopyala

Wizard sana bir `operator-keystore.json` dosyası oluşturur. Bu dosyayı sunucuna kopyala:

```bash
# Kendi makinenden sunucuya kopyala (IP adresini değiştir)
scp /path/to/operator-keystore.json kullanici@SUNUCU_IP:/home/kullanici/operator-keystore.json
```

### 3.5 Validator Durumunu Doğrula

```bash
genlayer staking validator-info --validator 0xVALIDATOR_WALLET_ADRESİN
```

---

## 4. Node Yazılımını İndir ve Kur

> Bu adımdan itibaren **sunucunda** çalışıyorsun.

### 4.1 Mevcut Versiyonları Listele

```bash
curl -s "https://storage.googleapis.com/storage/v1/b/gh-af/o?prefix=genlayer-node/bin/amd64" | \
  grep -o '"name": *"[^"]*"' | \
  sed -n 's/.*\/\(v[^/]*\)\/.*/\1/p' | \
  sort -ru | grep -v "rc" | head -n 5
```

Şuna benzer bir çıktı görmelisin:

```
v0.5.12
v0.5.11
v0.5.10
v0.5.9
v0.5.8
```

### 4.2 Node Yazılımını İndir

```bash
# İstediğin versiyonu belirle (genellikle en yenisi)
export VERSION=v0.5.12

# İndir
wget https://storage.googleapis.com/gh-af/genlayer-node/bin/amd64/${VERSION}/genlayer-node-linux-amd64-${VERSION}.tar.gz
```

### 4.3 Dosyayı Çıkart ve Dizine Gir

```bash
# Klasör oluştur ve çıkart
mkdir -p ${VERSION}
tar -xzvf genlayer-node-linux-amd64-${VERSION}.tar.gz -C ./${VERSION}

# O klasöre gir
cd ./${VERSION}

# Şu an neredeyiz kontrol et
pwd
# Çıktı örneği: /home/kullanici/v0.5.12
```

### 4.4 GenVM Kurulumunu Çalıştır

Bu adım eksik runner'ları indirir, hash'leri doğrular ve binary'leri hazırlar.

```bash
python3 ./third_party/genvm/bin/setup.py
```

> Bu işlem birkaç dakika sürebilir, sabırla bekle.

---

## 5. Konfigürasyon Dosyasını Oluştur

Hâlâ `${VERSION}` klasörünün içindeyiz. Konfigürasyon dosyası `configs/node/config.yaml` konumunda olmalı.

### 5.1 Klasörü Oluştur

```bash
mkdir -p configs/node
```

### 5.2 config.yaml Dosyasını Oluştur

> Aşağıdaki komutta `TODO` ile başlayan değerleri **kendi bilgilerinle** doldur.

```bash
cat > configs/node/config.yaml << 'EOF'
# rollup configuration
rollup:
  genlayerchainrpcurl: "BURAYA_ZKSYNC_HTTP_RPC_URL_YAZ"        # ZKSync HTTP RPC URL
  genlayerchainwebsocketurl: "BURAYA_ZKSYNC_WEBSOCKET_URL_YAZ" # ZKSync WebSocket URL
  provider: "BURAYA_PROVIDER_ADI_YAZ"                           # Örnek: "heurist" veya "ionet"

# Testnet Asimov için consensus ayarları
consensus:
  consensusaddress: "0xe66B434bc83805f380509642429eC8e43AE9874a"
  genesis: 17326

# data dizini
datadir: "./data/node"

# logging configuration
logging:
  level: "INFO"
  json: false
  file:
    enabled: true
    level: "DEBUG"
    folder: logs
    maxsize: 10
    maxage: 7
    maxbackups: 100
    localtime: false
    compress: true

# node configuration
node:
  mode: "validator"
  validatorWalletAddress: "BURAYA_VALIDATOR_WALLET_ADRESİNİ_YAZ"  # 0x... wizard'dan aldın
  operatorAddress: "BURAYA_OPERATOR_ADRESİNİ_YAZ"                 # 0x... wizard'dan aldın
  admin:
    port: 9155
  rpc:
    port: 9151
    endpoints:
      groups:
        genlayer: true
        genlayer_debug: true
        ethereum: true
        zksync: true
  ops:
    port: 9153
    endpoints:
      metrics: true
      health: true
      balance: true

# genvm configuration
genvm:
  root_dir: ./third_party/genvm
  start_manager: true
  manager_url: http://127.0.0.1:3999
  permits: 8

# Advanced configuration
merkleforest:
  maxdepth: 16
  dbpath: "./data/node/merkle/forest/data.db"
  indexdbpath: "./data/node/merkle/index.db"
merkletree:
  maxdepth: 16
  dbpath: "./data/node/merkle/tree/"

# metrics configuration
metrics:
  interval: "15s"
  collectors:
    node:
      enabled: true
    genvm:
      enabled: true
    webdriver:
      enabled: true
EOF
```

### 5.3 Dosyayı Kontrol Et

```bash
cat configs/node/config.yaml
```

> ⚠️ `validatorWalletAddress` ve `operatorAddress` alanlarını doldurmayı **unutma**! Bu olmadan node validator olarak değil, full node olarak çalışır.

---

### 5.4 ZKSync RPC URL Nereden Bulunur?

Her validator, GenLayer chain'e bağlı bir ZKSync Full Node'a ihtiyaç duyar.

**Seçenek 1 — Kendi ZKSync node'unu çalıştır:**  
[ZKSync External Node dokümantasyonu](https://docs.zksync.io/zksync-era/tooling/external-node)

**Seçenek 2 — Ortak node kullan:**  
Birden fazla validator aynı ZKSync node'u paylaşabilir. GenLayer Discord/Telegram topluluğunda mevcut public node URL'lerini sorabilirsin.

---

## 6. Operator Key'i İçe Aktar

Hâlâ `${VERSION}` klasörünün içindeyiz.

### 6.1 Keystore Dosyasını İçe Aktar

```bash
./bin/genlayernode account import \
  --password "BURAYA_NODE_ŞIFRENI_YAZ" \
  --passphrase "BURAYA_WIZARD_EXPORT_ŞIFRESINI_YAZ" \
  --path "/home/kullanici/operator-keystore.json" \
  -c $(pwd)/configs/node/config.yaml \
  --setup
```

Başarılı olursa şuna benzer bir çıktı görürsün:

```
Account imported:
  Address: 0xA0b12Fd2f3F7e86fEC458D114A5E7a6f571160a8
  Account setup as a validator
```

> Görünen adresin wizard'dan aldığın **Operator Adresi** ile eşleştiğini kontrol et!

### 6.2 (Alternatif) Sunucuda Yeni Operator Key Oluştur

Eğer wizard'dan export etmediysen, doğrudan sunucuda oluşturabilirsin:

```bash
./bin/genlayernode account new \
  -c $(pwd)/configs/node/config.yaml \
  --setup \
  --password "BURAYA_NODE_ŞIFRENI_YAZ"
```

Bu komutu kullandıysan, üretilen adresi wizard'ı çalıştırırken operator olarak belirtmen gerekir.

### 6.3 Operator Key Yedeği Al

```bash
./bin/genlayernode account export \
  --password "NODE_ŞİFREN" \
  --address "0xOPERATOR_ADRESİN" \
  --passphrase "YEDEK_ŞİFREN" \
  --path "/home/kullanici/operator-backup.key" \
  -c $(pwd)/configs/node/config.yaml
```

> 🔒 Bu yedek dosyayı güvenli bir yerde sakla! Kaybedersen yeni operator kurman gerekir.

---

## 7. LLM Sağlayıcısını Ayarla

Her validator, Intelligent Contract'ları çalıştırmak için bir LLM'e erişim sağlamalıdır.

### Ücretsiz Kredi Alabileceğin Ortaklar

| Sağlayıcı | Ücretsiz Kredi | Link |
|-----------|---------------|------|
| **Heurist** | Evet — referans kodu: `genlayer` | [dev-api-form.heurist.ai](https://dev-api-form.heurist.ai) |
| **Comput3** | Evet | [genlayer.comput3.ai](https://genlayer.comput3.ai/) |
| **io.net** | Evet — form doldur | [form.typeform.com](https://form.typeform.com/to/pDmCCViV) |
| **Chutes** | Evet | [chutes.ai](https://chutes.ai) |
| **Morpheus** | Evet | [mor.org](https://mor.org/) |

### API Key'ini Environment Variable Olarak Ayarla

Kullandığın sağlayıcıya göre aşağıdaki satırlardan birini çalıştır:

```bash
# Heurist için
export HEURISTKEY='buraya_api_keyin'

# Comput3 için
export COMPUT3KEY='buraya_api_keyin'

# io.net için
export IOINTELLIGENCE_API_KEY='buraya_api_keyin'

# Chutes için
export CHUTES_API_KEY='buraya_api_keyin'

# Morpheus için
export MORPHEUS_API_KEY='buraya_api_keyin'

# OpenAI için
export OPENAIKEY='buraya_api_keyin'
```

> 💡 Sunucu yeniden başladığında key'in kaybolmaması için `~/.bashrc` veya `~/.profile` dosyasına ekleyebilirsin:
> ```bash
> echo "export HEURISTKEY='buraya_api_keyin'" >> ~/.bashrc
> source ~/.bashrc
> ```

---

## 8. Node'u Başlat

Hâlâ `${VERSION}` klasörünün içindeyiz.

### 8.1 WebDriver Container'ı Başlat

GenVM'in web modülü için gerekli:

```bash
docker compose up -d
```

Kontrol et:

```bash
docker ps
# "genlayer-node-webdriver" adlı container çalışıyor olmalı
```

### 8.2 Konfigürasyonu Doğrula

Node'u başlatmadan önce her şeyin doğru olup olmadığını kontrol et:

```bash
./bin/genlayernode doctor
```

Bu komut şunları kontrol eder:
- Consensus kontrat konfigürasyonu
- GenVM bağlantısı
- LLM sağlayıcısı bağlantısı ve API key
- ZKSync node erişimi

> Hata görüyorsan bir sonraki adıma geçme, önce sorunu çöz.

### 8.3 Node'u Çalıştır

```bash
./bin/genlayernode run \
  -c $(pwd)/configs/node/config.yaml \
  --password "NODE_ŞİFREN"
```

Başarılı başlangıçta şuna benzer loglar görürsün:

```
INFO  Node started
INFO  Syncing blocks...
INFO  Connected to consensus contract
```

---

## 9. Node'u Arka Planda Çalıştır (screen)

SSH bağlantısı koptuğunda node durmasın diye `screen` kullan.

### 9.1 Yeni screen Oturumu Başlat

```bash
screen -S genlayer
```

### 9.2 Node'u Bu Oturumda Çalıştır

```bash
# Önce doğru klasörde olduğundan emin ol
cd ~/v0.5.12   # VERSION klasörüne gir

# LLM key'ini ayarla
export HEURISTKEY='buraya_api_keyin'

# WebDriver başlat (ilk kurulumda yaptıysan atla)
docker compose up -d

# Node'u çalıştır
./bin/genlayernode run \
  -c $(pwd)/configs/node/config.yaml \
  --password "NODE_ŞİFREN"
```

### 9.3 Oturumu Arka Plana Al

Klavyede `Ctrl + A`, ardından `D` tuşlarına bas.

Node arka planda çalışmaya devam eder, SSH bağlantısını güvenle kapatabilirsin.

### 9.4 Oturuma Geri Dön

```bash
screen -r genlayer
```

### 9.5 Tüm screen Oturumlarını Listele

```bash
screen -ls
```

---

## 10. Faydalı Komutlar

### Node Durumu

```bash
# Health check
curl http://localhost:9153/health

# Metrics
curl http://localhost:9153/metrics

# Node balance
curl http://localhost:9153/balance
```

### Validator Yönetimi

```bash
# Validator bilgilerini görüntüle
genlayer staking validator-info --validator 0xVALIDATOR_WALLET_ADRESİN

# Aktif validator'ları listele
genlayer staking active-validators

# Daha fazla stake ekle
genlayer staking validator-deposit --amount 1000gen

# Validator'dan çıkış (7-epoch unbonding süreci başlar)
genlayer staking validator-exit --shares 100

# Unbonding sonrası fonları çek
genlayer staking validator-claim

# Kimlik bilgilerini güncelle
genlayer staking set-identity --validator 0x... --moniker "YeniIsim"
```

### Account Komutları

```bash
# Kayıtlı hesapları listele
./bin/genlayernode account list -c $(pwd)/configs/node/config.yaml

# Hesap bilgilerini göster
./bin/genlayernode account show \
  --address 0xOPERATOR_ADRESİN \
  -c $(pwd)/configs/node/config.yaml
```

---

## 11. Sık Yapılan Hatalar

### ❌ "exec format error" veya node başlamıyor

**Sebep:** Sunucu ARM mimarisi kullanıyor.  
**Çözüm:** AMD64 (x86_64) mimarili sunucuya geçiş yap. `uname -m` komutuyla kontrol et.

---

### ❌ "NO_PROVIDER_FOR_PROMPT"

**Sebep:** Hiçbir LLM sağlayıcısı aktif değil ya da API key ayarlanmamış.  
**Çözüm:** API key environment variable'ını ayarla ve node'u yeniden başlat.

```bash
export HEURISTKEY='api_keyin'
```

---

### ❌ Node validator olarak değil full node olarak çalışıyor

**Sebep:** `validatorWalletAddress` veya `operatorAddress` config'de boş bırakılmış.  
**Çözüm:** `configs/node/config.yaml` dosyasını düzenle ve wizard'dan aldığın adresleri ekle.

---

### ❌ Docker permission denied

**Sebep:** Kullanıcı docker grubunda değil.  
**Çözüm:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

### ❌ WebDriver container başlamıyor

**Çözüm:**
```bash
docker compose down
docker compose up -d
docker ps  # container çalışıyor mu?
docker logs genlayer-node-webdriver  # hata loglarını gör
```

---

### ❌ SSH bağlantısı kopunca node duruyor

**Çözüm:** [Adım 9](#9-nodeu-arka-planda-çalıştır-screen)'daki `screen` talimatlarını takip et.

---

## 📚 Kaynaklar

- [Resmi Dokümantasyon](https://docs.genlayer.com/validators/setup-guide)
- [GenVM Konfigürasyonu](https://docs.genlayer.com/validators/genvm-configuration)
- [Sistem Gereksinimleri](https://docs.genlayer.com/validators/system-requirements)
- [Upgrade Rehberi](https://docs.genlayer.com/validators/upgrade)
- [Discord](https://discord.gg/8Jm4v89VAu)
- [Telegram](https://t.me/genlayer)

---

> ✅ Bu rehberi takip ederek node'unu sorunsuz kurabilirsin. Herhangi bir adımda sorun yaşarsan GenLayer Discord'unda `#validators` kanalına sorabilirsin.
