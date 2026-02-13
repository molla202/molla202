# Evrensel Cosmos Auto-Compound Script Kullanım Kılavuzu

Tüm Cosmos SDK tabanlı blockchain'ler için otomatik ödül toplama ve stake scripti.


```bash
wget https://raw.githubusercontent.com/molla202/molla202/refs/heads/main/cosmos_auto_compound.py
```

<img width="879" height="1175" alt="image" src="https://github.com/user-attachments/assets/ec625d47-39c4-4f76-88f0-094a170be47e" />


## 🌟 Özellikler

- ✅ **Evrensel Destek**: Tüm Cosmos SDK tabanlı projeler için çalışır
- ✅ **Akıllı Yapılandırma**: İlk çalıştırmada ayarları sorar ve kaydeder
- ✅ **RPC Desteği**: Custom port ve remote RPC desteği
- ✅ **Gas Fee Optimizasyonu**: Otomatik gas buffer hesaplaması
- ✅ **Güvenli**: Şifreler hiçbir yere kaydedilmez
- ✅ **Esnek Decimal Desteği**: 6, 18 veya herhangi bir decimal sistemi
- ✅ **Detaylı Loglama**: Her işlem adımı kayıt altına alınır
- ✅ **İki Çalışma Modu**: Tek seferlik veya sürekli

## 📋 Desteklenen Projeler

- Warden Protocol
- Cosmos Hub (ATOM)
- Osmosis
- Celestia
- Juno
- Stargaze
- Injective
- Akash
- **Ve diğer tüm Cosmos SDK tabanlı projeler**

## 🚀 Hızlı Başlangıç

### 1. Script'i İndirin
```bash
# Script dosyasını çalıştırılabilir yapın
chmod +x cosmos_auto_compound.py
```

### 2. İlk Çalıştırma
```bash
python3 cosmos_auto_compound.py
```

Script sizden şu bilgileri isteyecek:

```
Proje adı (örn: Warden, Celestia): Warden
Binary adı [wardend]: wardend
Chain ID (örn: warden_8765-1): warden_8765-1
Base denom (örn: award, uatom, uosmo): award
Display denom [WARD]: WARD
Decimal sayısı [18]: 18
Validator adresi: wardenvaloper1abc...
Cüzdan adı: wallet
Cüzdan adresi: warden1xyz...
Reserve miktarı [1.0 WARD]: 2.0
Gas fees [250000000000000award]: 
RPC adresi [http://localhost:26657]: 
Kontrol aralığı (saat) [1]: 6
```

Bu bilgiler `cosmos_config.json` dosyasına kaydedilir.

### 3. Sonraki Kullanımlar

```bash
python3 cosmos_auto_compound.py
```

Mevcut yapılandırmanız gösterilir:
```
Mevcut yapılandırmayı kullanmak istiyor musunuz? (E/h) [E]:
```

- **E** (Enter): Mevcut ayarlarla devam eder
- **h**: Yeni ayarlar girmenizi sağlar

## 🎯 Çalıştırma Modları

### Tek Seferlik Çalıştırma
```bash
python3 cosmos_auto_compound.py --once
```
Sadece bir kez compound yapar ve durur.

### Sürekli Çalıştırma (Daemon)
```bash
python3 cosmos_auto_compound.py
```
Belirtilen saat aralıklarında otomatik olarak çalışır.

### Arka Planda Çalıştırma
```bash
# nohup ile
nohup python3 cosmos_auto_compound.py > cosmos.log 2>&1 &

# screen ile
screen -S cosmos
python3 cosmos_auto_compound.py
# Ctrl+A+D ile detach

# Tekrar bağlanmak için
screen -r cosmos
```

## 📊 Örnek Yapılandırmalar

### Warden Protocol (18 Decimals)
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
    "gas_fees": "250000000000000award",
    "gas_adjustment": "1.6",
    "check_interval_hours": 6.0
}
```

### Cosmos Hub (6 Decimals)
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
    "reserve_amount_display": 0.1,
    "reserve_amount": 100000,
    "gas_fees": "5000uatom",
    "gas_adjustment": "1.6",
    "check_interval_hours": 1.0
}
```

### Osmosis (6 Decimals)
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
    "gas_fees": "5000uosmo"
}
```

### Celestia (6 Decimals)
```json
{
    "project_name": "Celestia",
    "binary": "celestia-appd",
    "chain_id": "celestia",
    "base_denom": "utia",
    "display_denom": "TIA",
    "decimals": 6,
    "rpc_address": "http://localhost:26657",
    "reserve_amount_display": 0.5,
    "gas_fees": "5000utia"
}
```

## 🔧 Yapılandırma Detayları

### RPC Adresi
Script tüm işlemler için RPC bağlantısı kullanır:

```bash
# Localhost (default port)
http://localhost:26657

# Custom port
http://localhost:26658

# Remote RPC
https://rpc.cosmos.network:443

# Custom domain
http://my-node.example.com:26657
```

### Gas Fees
Decimal sayısına göre önerilen değerler:

| Decimals | Örnek Gas Fee | Açıklama |
|----------|---------------|----------|
| 18 | 250000000000000award | Warden gibi projeler |
| 6 | 5000uatom | Cosmos Hub, Osmosis vb. |
| Diğer | 250000{denom} | Genel öneri |

### Reserve Amount
Cüzdanda kalacak minimum miktar:
- Gas fee'leri ödemek için gerekli
- Script otomatik 5x gas buffer ekler
- Önerilen: 1-2 token (ağ yoğunluğuna göre)

### Kontrol Aralığı
Ödüllerin kontrol edilme sıklığı:
- **Yüksek ödül**: 1-6 saat
- **Düşük ödül**: 12-24 saat
- **Çok düşük ödül**: 24-48 saat

## 📝 Log Dosyaları

Script iki tür log tutar:

### 1. cosmos_auto_compound.log
Detaylı işlem logları:
```bash
tail -f cosmos_auto_compound.log
```

### 2. Ekran Çıktısı
Anlık durum bilgisi:
```
======================================================================
Warden Otomatik Compound - 2026-02-13 19:30:00
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
   Gas Buffer (5x): 1.250000 WARD
   ─────────────────────────────────────
   Stake Edilecek: 144.257024 WARD

Stake ediliyor: 144.257024 WARD (144257024100166243845 award)
Stake işlemi başarılı

İşlem Sonrası Bakiye:
   Son Bakiye: 3.250000 WARD

Bir sonraki kontrol: 6.0 saat sonra
======================================================================
```

## 🐛 Sorun Giderme

### Problem: "connection refused" veya "dial tcp" hatası
**Neden:** RPC bağlantı sorunu

**Çözüm:**
```bash
# Node durumunu kontrol edin
systemctl status wardend  # veya ilgili servis

# RPC portunu kontrol edin
netstat -tulpn | grep 26657

# Config.toml'de RPC ayarlarını kontrol edin
cat ~/.warden/config/config.toml | grep laddr

# RPC test scripti çalıştırın
./test_rpc.sh

# Farklı port kullanıyorsanız config'i güncelleyin
nano cosmos_config.json
# "rpc_address": "http://localhost:26658"
```

### Problem: "insufficient funds" hatası
**Neden:** Stake işlemi için yeterli bakiye yok

**Çözüm:**
```bash
# Reserve miktarını düşürün veya gas fee'yi düşürün
nano cosmos_config.json

# "reserve_amount_display": 1.0  # 2.0'dan 1.0'a düşür
# "gas_fees": "200000000000000award"  # Düşük yoğunlukta
```

### Problem: "Binary bulunamadı"
**Neden:** Binary PATH'de değil

**Çözüm:**
```bash
# Binary yolunu bulun
which wardend

# PATH'e ekleyin (geçici)
export PATH=$PATH:/usr/local/bin

# PATH'e ekleyin (kalıcı)
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

### Problem: "Permission denied"
**Neden:** Script çalıştırma yetkisi yok

**Çözüm:**
```bash
chmod +x cosmos_auto_compound.py
```

### Problem: "Config yüklenemedi"
**Neden:** JSON dosyası bozuk

**Çözüm:**
```bash
# Config dosyasını silin ve yeniden oluşturun
rm cosmos_config.json
python3 cosmos_auto_compound.py
```

### Problem: UTF-8 Encoding Hatası
**Neden:** Önceki script versiyonu encoding sorunu

**Çözüm:**
```bash
# Yeni script versiyonunu kullanın
# Script başında # -*- coding: utf-8 -*- olmalı
head -n 2 cosmos_auto_compound.py
```

## 🔒 Güvenlik

### Şifre Güvenliği
- ✅ Cüzdan şifresi **asla** dosyaya kaydedilmez
- ✅ Her çalıştırmada manuel girilir
- ✅ Şifre bellek dışına yazılmaz

### Config Dosyası
- ✅ Sadece genel bilgiler içerir
- ✅ Private key'ler ele alınmaz
- ✅ Dosya izinlerini kontrol edin: `chmod 600 cosmos_config.json`

### Öneriler
- ⚠️ Script'i güvenli bir sunucuda çalıştırın
- ⚠️ Düzenli olarak log dosyalarını kontrol edin
- ⚠️ Firewall ile RPC portunu koruyun
- ⚠️ SSH key authentication kullanın

## ⚙️ Systemd Servisi (Opsiyonel)

Script'i sistem servisi olarak çalıştırmak için:

### 1. Servis Dosyası Oluşturun
```bash
sudo nano /etc/systemd/system/cosmos-autocompound.service
```

### 2. İçerik
```ini
[Unit]
Description=Cosmos Auto Compound Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/usr/bin/python3 /home/ubuntu/cosmos_auto_compound.py
Restart=always
RestartSec=60
StandardOutput=append:/home/ubuntu/cosmos_service.log
StandardError=append:/home/ubuntu/cosmos_service_error.log

[Install]
WantedBy=multi-user.target
```

**Not:** Servis modunda şifre kullanılamaz! Şifresiz cüzdan gerekir.

### 3. Servisi Etkinleştirin
```bash
sudo systemctl daemon-reload
sudo systemctl enable cosmos-autocompound
sudo systemctl start cosmos-autocompound
```

### 4. Durumu Kontrol Edin
```bash
sudo systemctl status cosmos-autocompound

# Log'ları izleyin
sudo journalctl -u cosmos-autocompound -f
```

## 🧪 Test

### RPC Bağlantı Testi
```bash
./test_rpc.sh
```

Bu script kontrol eder:
- ✅ HTTP bağlantısı
- ✅ Node durumu
- ✅ CLI komutu
- ✅ Bakiye sorgusu

### Tek Seferlik Test
```bash
python3 cosmos_auto_compound.py --once
```

Her şey yolundaysa:
- Komisyon çekilir
- Ödüller çekilir
- Bakiye kontrol edilir
- Stake yapılır
- Son bakiye gösterilir

## 📊 Gas Buffer Hesaplaması

Script güvenli stake için otomatik gas buffer ekler:

```
Toplam Bakiye:    147.507 WARD
Reserve:          -2.000 WARD
Gas Buffer (5x):  -1.250 WARD  ← Otomatik hesaplanır
─────────────────────────────
Stake Edilecek:   144.257 WARD
```

**Gas Buffer = Gas Fee × 5**

Neden 5x?
1. Komisyon çekme: 1x gas ✅ (yapıldı)
2. Ödül çekme: 1x gas ✅ (yapıldı)
3. Stake işlemi: 1x gas ⏳ (yapılacak)
4. Ekstra güvenlik: 2x gas 🛡️ (ağ yoğunluğu için)

## 🎁 İpuçları

### 1. Test Önce
İlk kullanımda `--once` parametresi ile test edin:
```bash
python3 cosmos_auto_compound.py --once
```

### 2. Reserve Ayarı
Gas fee'leri karşılayacak kadar reserve bırakın:
- **18 decimals**: Minimum 2 token
- **6 decimals**: Minimum 0.1-0.5 token

### 3. Kontrol Aralığı
Ödüllerin birikmesine göre ayarlayın:
- **Validatör**: 6-12 saat
- **Delegator**: 12-24 saat

### 4. Log İzleme
Sürekli çalıştırmada log'ları takip edin:
```bash
tail -f cosmos_auto_compound.log
```

### 5. Düzenli Kontrol
Haftada bir script'in çalışıp çalışmadığını kontrol edin:
```bash
# Screen için
screen -ls

# Process için
ps aux | grep cosmos_auto_compound

# Systemd için
sudo systemctl status cosmos-autocompound
```

## 🔄 Güncelleme

Yeni bir proje eklemek için:
```bash
python3 cosmos_auto_compound.py
# Mevcut yapılandırmayı kullanmak istiyor musunuz? -> h
# Yeni bilgileri girin
```

Config dosyasını manuel düzenlemek için:
```bash
nano cosmos_config.json
# Değişiklikleri yapın ve kaydedin
```

## 📞 Destek

### Log Kontrolü
Sorun yaşarsanız log dosyasını kontrol edin:
```bash
cat cosmos_auto_compound.log
```

### Debug Modu
Detaylı log için:
```python
# Script başında logging.basicConfig içinde
level=logging.DEBUG  # INFO yerine DEBUG
```

### Manuel Test
Komutları manuel test edin:
```bash
# Bakiye kontrolü
wardend query bank balances warden1... --node http://localhost:26657

# Ödül kontrolü
wardend query distribution rewards warden1... --node http://localhost:26657
```

## 📚 Ek Kaynaklar

- [Cosmos SDK Dökümanları](https://docs.cosmos.network/)
- [Warden Protocol](https://wardenprotocol.org/)
- [Systemd Servisleri](https://www.freedesktop.org/software/systemd/man/systemd.service.html)

## 📄 Lisans

Bu script açık kaynaklıdır ve özgürce kullanılabilir.

## ⚠️ Feragatname

Bu script "olduğu gibi" sağlanmaktadır. Kullanımdan doğabilecek herhangi bir kayıptan script yazarı sorumlu değildir. Kullanmadan önce test edin ve riskleri anlayın.

---

**Son Güncelleme:** 2026-02-13  
**Versiyon:** 2.1 (UTF-8 Fix + RPC Support)  
**Durum:** ✅ Production Ready

Mutlu Staking! 🚀
