# Evrensel Cosmos Auto-Compound Script Kullanım Kılavuzu

Tüm Cosmos SDK tabanlı blockchain'ler için otomatik ödül toplama ve stake scripti.


```bash
wget https://raw.githubusercontent.com/molla202/molla202/refs/heads/main/cosmos_auto_compound.py
```

<img width="879" height="1175" alt="image" src="https://github.com/user-attachments/assets/ec625d47-39c4-4f76-88f0-094a170be47e" />


## 🌟 Özellikler

- ✅ **Evrensel Destek**: Tüm Cosmos SDK tabanlı projeler (Warden, Cosmos Hub, Osmosis, Celestia, vb.)
- ✅ **Akıllı Yapılandırma**: İlk çalıştırmada ayarları sorar, kaydeder ve hatırlar
- ✅ **Esnek Gas Sistemi**: Hem `--gas-prices` hem `--fees` desteği
- ✅ **Custom RPC**: Farklı port ve remote RPC desteği
- ✅ **Otomatik Gas Buffer**: "Insufficient funds" hatasını önler
- ✅ **Güvenli**: Şifreler hiçbir yere kaydedilmez
- ✅ **Esnek Decimal**: 6, 18 veya herhangi bir decimal sistemi
- ✅ **Detaylı Log**: Her işlem adımı kayıt altına alınır
- ✅ **UTF-8 Uyumlu**: Türkçe karakter ve emoji desteği
- ✅ **İki Mod**: Tek seferlik veya sürekli çalışma

## 📋 Desteklenen Projeler

| Proje | Chain ID | Decimals | Test Durumu |
|-------|----------|----------|-------------|
| Warden Protocol | warden_8765-1 | 18 | ✅ Test Edildi |
| Cosmos Hub | cosmoshub-4 | 6 | ✅ Uyumlu |
| Osmosis | osmosis-1 | 6 | ✅ Uyumlu |
| Celestia | celestia | 6 | ✅ Uyumlu |
| Juno | juno-1 | 6 | ✅ Uyumlu |
| Stargaze | stargaze-1 | 6 | ✅ Uyumlu |
| Akash | akashnet-2 | 6 | ✅ Uyumlu |
| **Tüm Cosmos SDK projeler** | - | - | ✅ Uyumlu |

## 🚀 Hızlı Başlangıç

### Gereksinimler

```bash
# Python 3.6+
python3 --version

# Node binary (örnek: wardend, gaiad, osmosisd)
wardend version

# Node çalışıyor olmalı
systemctl status wardend  # veya ilgili servis
```

### 1. Script'i Hazırlayın

```bash
# Çalıştırılabilir yapın
chmod +x cosmos_auto_compound.py
```

### 2. İlk Çalıştırma

```bash
python3 cosmos_auto_compound.py
```

Script size adım adım şu bilgileri soracak:

#### 2.1 Temel Bilgiler
```
Proje adı (örn: Warden, Celestia): Warden
Binary adı [wardend]: wardend
Chain ID (örn: warden_8765-1): warden_8765-1
```

#### 2.2 Token Bilgileri
```
Base denom (örn: award, uatom, uosmo): award
Display denom [WARD]: WARD

Örnekler:
  - 18 decimals: 1 token = 1,000,000,000,000,000,000 base
  - 6 decimals:  1 token = 1,000,000 base
Decimal sayısı [18]: 18
```

#### 2.3 Cüzdan Bilgileri
```
Validator adresi (örn: wardenvaloper1...): wardenvaloper1abc...
Cüzdan adı (örn: wallet): wallet
Cüzdan adresi (örn: warden1...): warden1xyz...
Reserve miktarı (cüzdanda kalacak) [1.0 WARD]: 2.0
```

#### 2.4 Gas Ayarları (ÖNEMLİ!)
```
Gas Ayarları:
  İki seçenek var:
    1. Gas Prices (önerilen): Birim fiyat, otomatik hesaplanır
    2. Fixed Fees: Sabit ücret

Gas prices kullanmak ister misiniz? (E/h) [E]: E

Örnekler:
  - Warden (18 decimals): 1000000000arai
  - Cosmos (6 decimals):  0.025uatom

Gas prices [1000000000award]: 1000000000award
```

**Gas Prices vs Fixed Fees Farkı:**
- **Gas Prices** (Önerilen): `--gas-prices=1000000000award` → Daha esnek, otomatik hesaplama
- **Fixed Fees**: `--fees=250000000000000award` → Sabit ücret

#### 2.5 RPC ve Diğer Ayarlar
```
RPC Adresi:
  Örnekler:
    - Localhost: http://localhost:26657
    - Custom port: http://localhost:26658
    - Remote: https://rpc.example.com:443
RPC adresi [http://localhost:26657]: http://localhost:38657

Kontrol aralığı (saat) [1]: 6
```

### 3. Cüzdan Şifresi

Her çalıştırmada güvenlik için şifre sorulur:

```
Cüzdan şifresi kullanıyor musunuz? (e/H) [H]: h
# Şifre kullanmıyorsanız Enter
# Kullanıyorsanız 'e' yazın
```

### 4. İlk Test

```bash
# Tek seferlik test
python3 cosmos_auto_compound.py --once
```

Başarılı olursa şunu göreceksiniz:
```
======================================================================
Warden Otomatik Compound - 2026-02-13 19:00:00
======================================================================
Komisyon ödülleri çekiliyor...
Komisyon çekme işlemi başarılı
Tüm ödüller çekiliyor...
Ödül çekme işlemi başarılı
İşlemin tamamlanması bekleniyor...
Cüzdan bakiyesi: 147.507024 WARD (147507024100166243845 award)

Hesaplamalar:
   Toplam Bakiye: 147.507024 WARD
   Reserve (Kalacak): 2.000000 WARD
   Gas Buffer (5x): 1.000000 WARD
   ─────────────────────────────────────
   Stake Edilecek: 144.507024 WARD

Stake ediliyor: 144.507024 WARD (144507024100166243845 award)
Stake işlemi başarılı

İşlem Sonrası Bakiye:
   Son Bakiye: 3.000000 WARD

İşlem tamamlandı
```

## 🎯 Çalıştırma Modları

### Tek Seferlik Çalıştırma
```bash
python3 cosmos_auto_compound.py --once
```
- Sadece bir kez compound yapar
- Test için idealdir
- Sonuç hemen görülür

### Sürekli Çalıştırma (Daemon)
```bash
python3 cosmos_auto_compound.py
```
- Belirtilen saat aralıklarında otomatik çalışır
- Ctrl+C ile durur
- Production kullanımı için

### Arka Planda Çalıştırma

#### nohup ile
```bash
nohup python3 cosmos_auto_compound.py > cosmos.log 2>&1 &

# Process ID'yi öğrenin
echo $!

# Durdurmak için
kill <PID>
```

#### screen ile
```bash
# Yeni screen oturumu
screen -S cosmos

# Script'i çalıştırın
python3 cosmos_auto_compound.py

# Detach (Ctrl+A sonra D)
# Tekrar bağlanmak için
screen -r cosmos

# Tüm screen'leri görmek
screen -ls
```

#### tmux ile
```bash
# Yeni tmux oturumu
tmux new -s cosmos

# Script'i çalıştırın
python3 cosmos_auto_compound.py

# Detach (Ctrl+B sonra D)
# Tekrar bağlanmak için
tmux attach -t cosmos
```

## 📊 Yapılandırma Örnekleri

### Warden Protocol (18 Decimals + Gas Prices)
```json
{
    "project_name": "Warden",
    "binary": "wardend",
    "chain_id": "warden_8765-1",
    "base_denom": "award",
    "display_denom": "WARD",
    "decimals": 18,
    "validator_address": "wardenvaloper1...",
    "wallet_name": "wallet",
    "wallet_address": "warden1...",
    "rpc_address": "http://localhost:26657",
    "reserve_amount_display": 2.0,
    "reserve_amount": 2000000000000000000,
    "use_gas_prices": true,
    "gas_prices": "1000000000award",
    "gas_fees": null,
    "gas_adjustment": "1.6",
    "check_interval_hours": 6.0
}
```

### Cosmos Hub (6 Decimals + Fixed Fees)
```json
{
    "project_name": "Cosmos",
    "binary": "gaiad",
    "chain_id": "cosmoshub-4",
    "base_denom": "uatom",
    "display_denom": "ATOM",
    "decimals": 6,
    "validator_address": "cosmosvaloper1...",
    "wallet_name": "wallet",
    "wallet_address": "cosmos1...",
    "rpc_address": "http://localhost:26657",
    "reserve_amount_display": 0.5,
    "reserve_amount": 500000,
    "use_gas_prices": false,
    "gas_prices": null,
    "gas_fees": "5000uatom",
    "gas_adjustment": "1.6",
    "check_interval_hours": 12.0
}
```

### Osmosis (6 Decimals + Gas Prices)
```json
{
    "project_name": "Osmosis",
    "binary": "osmosisd",
    "chain_id": "osmosis-1",
    "base_denom": "uosmo",
    "display_denom": "OSMO",
    "decimals": 6,
    "rpc_address": "http://localhost:26657",
    "reserve_amount_display": 1.0,
    "reserve_amount": 1000000,
    "use_gas_prices": true,
    "gas_prices": "0.025uosmo",
    "gas_fees": null
}
```

## 🔧 Gas Ayarları Detayı

### Gas Prices (Önerilen)

**Avantajlar:**
- ✅ Daha esnek
- ✅ Otomatik hesaplama
- ✅ Network yoğunluğuna adapte
- ✅ Çoğu Cosmos chain için standart

**Önerilen Değerler:**

| Decimals | Base Denom | Önerilen Gas Price | Örnek Komut |
|----------|------------|-------------------|-------------|
| 18 | award | 1000000000 | `--gas-prices=1000000000award` |
| 18 | arai | 1000000000 | `--gas-prices=1000000000arai` |
| 6 | uatom | 0.025 | `--gas-prices=0.025uatom` |
| 6 | uosmo | 0.025 | `--gas-prices=0.025uosmo` |

### Fixed Fees

**Avantajlar:**
- ✅ Öngörülebilir
- ✅ Basit

**Önerilen Değerler:**

| Decimals | Önerilen Fee |
|----------|--------------|
| 18 | 250000000000000award |
| 6 | 5000uatom |

## 📝 Sonraki Kullanımlar

### Mevcut Config ile Çalıştırma

```bash
python3 cosmos_auto_compound.py

# Gösterecek:
MEVCUT YAPILANDIRMA
======================================================================
Proje Adı:           Warden
Chain ID:            warden_8765-1
...
======================================================================

Mevcut yapılandırmayı kullanmak istiyor musunuz? (E/h) [E]: 
```

- **E** veya **Enter**: Mevcut ayarlarla devam
- **h**: Yeni yapılandırma oluştur

### Config Güncelleme

```bash
# Yeni config oluştur
python3 cosmos_auto_compound.py
# Sorulduğunda 'h' yazın

# Veya manuel düzenle
nano cosmos_config.json
```

## 📁 Dosya Yapısı

```
cosmos_auto_compound.py      # Ana script
cosmos_config.json           # Yapılandırma (otomatik oluşur)
cosmos_auto_compound.log     # İşlem logları (otomatik oluşur)
check_gas_fee.py            # Gas fee kontrol aracı (opsiyonel)
test_rpc.sh                 # RPC test aracı (opsiyonel)
```

## 🔍 Log İzleme

### Canlı Log Takibi
```bash
# Log dosyasını canlı izle
tail -f cosmos_auto_compound.log

# Son 50 satırı göster
tail -n 50 cosmos_auto_compound.log

# Sadece hataları göster
grep "ERROR" cosmos_auto_compound.log

# Başarılı stake işlemlerini göster
grep "Stake işlemi başarılı" cosmos_auto_compound.log
```

### Log Formatı
```
2026-02-13 18:40:02,673 - INFO - Hesaplamalar:
2026-02-13 18:40:02,673 - INFO -    Toplam Bakiye: 52.249021 rai
2026-02-13 18:40:02,673 - INFO -    Reserve (Kalacak): 1.000000 rai
2026-02-13 18:40:02,673 - INFO -    Gas Buffer (5x): 1.000000 rai
2026-02-13 18:40:02,673 - INFO -    Stake Edilecek: 50.249021 rai
```

## 🐛 Sorun Giderme

### 1. Gas Buffer = 0.000000

**Belirti:**
```
Gas Buffer (5x): 0.000000 WARD
```

**Sebep:** Gas ayarları parse edilemiyor

**Çözüm:**
```bash
# Config kontrol scripti
python3 check_gas_fee.py

# Manuel düzeltme
nano cosmos_config.json

# Gas prices kullanıyorsanız:
"use_gas_prices": true,
"gas_prices": "1000000000award",
"gas_fees": null

# Fixed fees kullanıyorsanız:
"use_gas_prices": false,
"gas_prices": null,
"gas_fees": "250000000000000award"
```

### 2. RPC Bağlantı Hatası

**Belirti:**
```
connection refused
dial tcp: connect: connection refused
```

**Çözüm:**
```bash
# Node durumunu kontrol
systemctl status wardend

# RPC portunu kontrol
netstat -tulpn | grep 26657

# Config.toml kontrol
cat ~/.warden/config/config.toml | grep laddr

# RPC test
curl http://localhost:26657/status

# Script ile test
./test_rpc.sh
```

### 3. Insufficient Funds

**Belirti:**
```
insufficient funds
```

**Sebep:** Reserve + Gas buffer'dan fazla stake edilmeye çalışılıyor

**Çözüm:**
```bash
# Reserve'i düşür veya gas'ı düşür
nano cosmos_config.json

# Reserve azalt
"reserve_amount_display": 1.0,  # 2.0'dan 1.0'a

# Veya gas düşür (düşük yoğunlukta)
"gas_prices": "500000000award",  # 1000000000'dan 500000000'a
```

### 4. Binary Bulunamadı

**Belirti:**
```
wardend: command not found
```

**Çözüm:**
```bash
# Binary yolunu bul
which wardend

# PATH'e ekle (geçici)
export PATH=$PATH:/usr/local/bin

# PATH'e ekle (kalıcı)
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc

# Kontrol
wardend version
```

### 5. Permission Denied

**Belirti:**
```
Permission denied: 'cosmos_auto_compound.py'
```

**Çözüm:**
```bash
chmod +x cosmos_auto_compound.py
```

### 6. UTF-8 Encoding Hatası

**Belirti:**
```
'utf-8' codec can't decode byte
```

**Çözüm:**
```bash
# Script başında # -*- coding: utf-8 -*- olmalı
head -n 2 cosmos_auto_compound.py

# Güncel scripti kullanın
# Eski script varsa silin ve yeni indirin
```

### 7. JSON Config Bozuk

**Belirti:**
```
Config yükleme hatası
JSON parse hatası
```

**Çözüm:**
```bash
# Config'i sil ve yeniden oluştur
rm cosmos_config.json
python3 cosmos_auto_compound.py

# Veya JSON syntax kontrol
cat cosmos_config.json | python3 -m json.tool
```

### 8. Son Bakiye Değişmiyor

**Belirti:**
```
İşlem Sonrası Bakiye:
   Son Bakiye: 52.249021 rai  # Aynı kaldı
```

**Sebep:** Gas buffer sıfır olabilir veya işlem başarısız

**Çözüm:**
```bash
# Gas buffer kontrolü
python3 check_gas_fee.py

# Manuel bakiye kontrolü
wardend query bank balances <cüzdan-adresi>

# Log'ları kontrol
grep "ERROR" cosmos_auto_compound.log
```

## 🔒 Güvenlik

### Şifre Güvenliği
- ✅ Şifreler **asla** dosyaya kaydedilmez
- ✅ Her çalıştırmada manuel girilir
- ✅ Bellek dışına yazılmaz

### Config Dosyası Güvenliği
```bash
# Config dosyasını sadece sahibi okuyabilir
chmod 600 cosmos_config.json

# İçeriği kontrol
cat cosmos_config.json
```

**Config'de saklanan bilgiler:**
- ✅ Public bilgiler (chain ID, validator adresi)
- ✅ Yapılandırma ayarları (gas, reserve)
- ❌ Private key (saklanmaz)
- ❌ Şifre (saklanmaz)

### Öneriler
- ⚠️ Script'i güvenli bir sunucuda çalıştırın
- ⚠️ SSH key authentication kullanın
- ⚠️ Firewall kurallarını ayarlayın
- ⚠️ Log dosyalarını düzenli kontrol edin
- ⚠️ Şifresiz cüzdan kullanıyorsanız systemd kullanmayın

## ⚙️ Systemd Servisi

**UYARI:** Systemd servisi modunda şifre kullanılamaz!

### 1. Servis Dosyası Oluştur
```bash
sudo nano /etc/systemd/system/cosmos-autocompound.service
```

### 2. İçerik
```ini
[Unit]
Description=Cosmos Auto Compound Service
After=network.target wardend.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/usr/bin/python3 /home/ubuntu/cosmos_auto_compound.py
Restart=always
RestartSec=60
StandardOutput=append:/home/ubuntu/cosmos_service.log
StandardError=append:/home/ubuntu/cosmos_service_error.log

# Environment (gerekirse)
Environment="PATH=/usr/local/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target
```

### 3. Servisi Etkinleştir
```bash
sudo systemctl daemon-reload
sudo systemctl enable cosmos-autocompound
sudo systemctl start cosmos-autocompound
```

### 4. Kontrol
```bash
# Durum
sudo systemctl status cosmos-autocompound

# Log'lar
sudo journalctl -u cosmos-autocompound -f

# Son 100 satır
sudo journalctl -u cosmos-autocompound -n 100

# Durdur
sudo systemctl stop cosmos-autocompound

# Yeniden başlat
sudo systemctl restart cosmos-autocompound
```

## 🧪 Test Araçları

### RPC Bağlantı Testi
```bash
./test_rpc.sh
```

**Test eder:**
- ✅ HTTP bağlantısı
- ✅ Node durumu ve sync
- ✅ CLI komutu
- ✅ Bakiye sorgusu

### Gas Fee Kontrolü
```bash
python3 check_gas_fee.py
```

**Kontrol eder:**
- ✅ Gas ayarları parse ediliyor mu
- ✅ Önerilen değerler
- ✅ Otomatik düzeltme

### Manuel Test Komutları
```bash
# Bakiye
wardend query bank balances warden1... --node http://localhost:26657

# Ödüller
wardend query distribution rewards warden1... --node http://localhost:26657

# Validator info
wardend query staking validator wardenvaloper1... --node http://localhost:26657
```

## 💡 İpuçları ve En İyi Pratikler

### 1. İlk Kullanım
```bash
# 1. Test modunda başlayın
python3 cosmos_auto_compound.py --once

# 2. Birkaç kez test edin
python3 cosmos_auto_compound.py --once

# 3. Sürekli mod başlatın
screen -S cosmos
python3 cosmos_auto_compound.py
```

### 2. Reserve Ayarı
**Çok düşük reserve:**
- ❌ Insufficient funds hatası
- ❌ İşlemler başarısız

**Çok yüksek reserve:**
- ❌ Compound verimsiz
- ❌ Ödüller stake edilemiyor

**Önerilen:**
- ✅ 18 decimals: 1-2 token
- ✅ 6 decimals: 0.1-0.5 token

### 3. Kontrol Aralığı
**Validatör:**
- ✅ 6-12 saat (ödüller hızlı birikir)

**Delegator:**
- ✅ 12-24 saat (ödüller yavaş birikir)

**Test:**
- ✅ 1 saat (ilk günler için)

### 4. Gas Ayarı
**Yüksek yoğunluk:**
```json
"gas_prices": "2000000000award"  # 2x artır
```

**Düşük yoğunluk:**
```json
"gas_prices": "500000000award"  # Yarı yap
```

### 5. Log Yönetimi
```bash
# Eski log'ları temizle (30 günden eski)
find . -name "*.log" -mtime +30 -delete

# Log boyutunu kontrol
du -h cosmos_auto_compound.log

# Log rotate
mv cosmos_auto_compound.log cosmos_auto_compound.log.old
```

### 6. Düzenli Kontrol
**Günlük:**
- ✅ Script çalışıyor mu? (`screen -ls`)
- ✅ Son işlem başarılı mı? (`tail cosmos_auto_compound.log`)

**Haftalık:**
- ✅ Total stake arttı mı?
- ✅ Ödüller düzgün toplanıyor mu?

**Aylık:**
- ✅ Config güncellemesi gerekiyor mu?
- ✅ Script güncellemesi var mı?

## 📊 Gas Buffer Hesaplama

### Gas Prices Kullanımı
```
Gas Buffer = Gas Price × Estimated Gas × 5

Örnek (18 decimals):
  Gas Price:     1,000,000,000 award (0.000000001 WARD)
  Estimated Gas: 200,000
  ─────────────────────────────
  Single TX:     200,000,000,000,000 award (0.0002 WARD)
  Buffer (5x):   1,000,000,000,000,000 award (0.001 WARD)
```

### Fixed Fees Kullanımı
```
Gas Buffer = Gas Fee × 5

Örnek (18 decimals):
  Gas Fee:       250,000,000,000,000 award (0.00025 WARD)
  Buffer (5x):   1,250,000,000,000,000 award (0.00125 WARD)
```

### Neden 5x?
1. Komisyon çekme: 1x ✅ (yapıldı)
2. Ödül çekme: 1x ✅ (yapıldı)
3. Stake işlemi: 1x ⏳ (yapılacak)
4. Extra güvenlik: 2x 🛡️ (ağ yoğunluğu)

## 🔄 Güncelleme ve Bakım

### Script Güncelleme
```bash
# Yedek al
cp cosmos_auto_compound.py cosmos_auto_compound.py.backup

# Yeni scripti indir
# ...

# Config'i koru (otomatik)
# cosmos_config.json değişmez
```

### Config Güncelleme
```bash
# Yeni proje ekle
python3 cosmos_auto_compound.py
# 'h' seç → Yeni bilgileri gir

# Veya manuel
nano cosmos_config.json
```

### Log Temizleme
```bash
# Log'u yedekle ve temizle
mv cosmos_auto_compound.log cosmos_auto_compound.log.$(date +%Y%m%d)
touch cosmos_auto_compound.log

# Eski log'ları sıkıştır
gzip cosmos_auto_compound.log.*

# 30 günden eski log'ları sil
find . -name "cosmos_auto_compound.log.*.gz" -mtime +30 -delete
```

## 📞 Destek ve Yardım

### Debug Modu
```python
# Script başında (satır 17-24)
logging.basicConfig(
    level=logging.DEBUG,  # INFO yerine DEBUG
    ...
)
```

### Verbose Output
```bash
# Detaylı çıktı için
python3 -v cosmos_auto_compound.py --once
```

### Manuel Komut Testi
```bash
# Ödül kontrolü
wardend query distribution rewards \
  warden1... \
  --node http://localhost:26657

# Komisyon kontrolü
wardend query distribution commission \
  wardenvaloper1... \
  --node http://localhost:26657

# Bakiye
wardend query bank balances \
  warden1... \
  --node http://localhost:26657
```

## 📚 Ek Kaynaklar

- [Cosmos SDK Docs](https://docs.cosmos.network/)
- [Cosmos Hub](https://hub.cosmos.network/)
- [Warden Protocol](https://wardenprotocol.org/)
- [Systemd Service Tutorial](https://www.freedesktop.org/software/systemd/man/systemd.service.html)

## ⚠️ Feragatname

Bu script "olduğu gibi" sağlanmaktadır. Kullanımdan doğabilecek herhangi bir kayıptan script yazarı sorumlu değildir. 

**Öneriler:**
- ✅ Küçük miktarlarla test edin
- ✅ Log'ları düzenli kontrol edin
- ✅ Yedek alın
- ✅ Riskleri anlayın

## 📄 Lisans

MIT License - Özgürce kullanabilirsiniz

---

**Versiyon:** 2.2 (Gas Prices + RPC + UTF-8)  
**Son Güncelleme:** 2026-02-13  
**Durum:** ✅ Production Ready

**Özellikler:**
- ✅ Gas Prices desteği
- ✅ Fixed Fees desteği
- ✅ Custom RPC desteği
- ✅ UTF-8 encoding
- ✅ Gelişmiş gas parser
- ✅ Otomatik gas buffer
- ✅ Detaylı hata yönetimi

Mutlu Staking! 🚀
