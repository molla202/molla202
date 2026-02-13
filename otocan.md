# Evrensel Cosmos Auto-Compound Script Kullanım Kılavuzu

## 🌟 Özellikler

Bu script tüm Cosmos SDK tabanlı blockchain'ler için kullanılabilir:
- ✅ Warden Protocol
- ✅ Cosmos Hub (ATOM)
- ✅ Osmosis
- ✅ Celestia
- ✅ Juno
- ✅ Stargaze
- ✅ Ve diğer tüm Cosmos SDK tabanlı projeler

## 📋 İlk Kurulum

### 1. Script'i İndirin
```bash
chmod +x cosmos_auto_compound.py
```

### 2. İlk Çalıştırma
```bash
python3 cosmos_auto_compound.py
```

İlk çalıştırmada sizden şu bilgiler istenecek:

```
Proje adı (örn: Warden, Celestia): Warden
Binary adı [wardend]: wardend
Chain ID (örn: warden_8765-1): warden_8765-1
Base denom (örn: award, uatom, uosmo): award
Display denom [WARD]: WARD
Decimal sayısı [18]: 18
Validator adresi (örn: wardenvaloper1...): wardenvaloper1abc...
Cüzdan adı (örn: wallet): wallet
Cüzdan adresi (örn: warden1...): warden1xyz...
Reserve miktarı (cüzdanda kalacak) [1.0 WARD]: 2.0
Gas fees [250000award]: 250000award
Kontrol aralığı (saat) [1]: 1
```

Bu bilgiler `cosmos_config.json` dosyasına kaydedilir.

## 🔄 Sonraki Kullanımlar

Script'i tekrar çalıştırdığınızda:
```bash
python3 cosmos_auto_compound.py
```

Mevcut yapılandırmanız gösterilir ve sorulur:
```
Mevcut yapılandırmayı kullanmak istiyor musunuz? (E/h) [E]:
```

- **E** (Enter): Mevcut ayarlarla devam eder
- **h**: Yeni ayarlar girmenizi sağlar

## 🔐 Cüzdan Şifresi

Her çalıştırmada güvenlik için şifre sorulur:
```
Cüzdan şifresi kullanıyor musunuz? (e/H) [H]: e
Cüzdan şifresi: ********
```

**Not:** Şifre güvenlik nedeniyle config dosyasına kaydedilmez.

## 🎯 Çalıştırma Modları

### Sürekli Çalıştırma (Daemon Mode)
```bash
python3 cosmos_auto_compound.py
```
Belirtilen saat aralıklarında otomatik olarak çalışır.

### Tek Seferlik Çalıştırma
```bash
python3 cosmos_auto_compound.py --once
```
Sadece bir kez compound yapar ve durur.

### Arka Planda Çalıştırma (nohup)
```bash
nohup python3 cosmos_auto_compound.py > cosmos_auto.log 2>&1 &
```

### Screen ile Çalıştırma
```bash
screen -S cosmos-auto
python3 cosmos_auto_compound.py
# Ctrl+A+D ile detach
```

## 📊 Örnek Yapılandırmalar

### Warden Protocol
```
Proje adı: Warden
Binary: wardend
Chain ID: warden_8765-1
Base denom: award
Display denom: WARD
Decimals: 18
Reserve: 2.0 WARD
```

### Cosmos Hub
```
Proje adı: Cosmos
Binary: gaiad
Chain ID: cosmoshub-4
Base denom: uatom
Display denom: ATOM
Decimals: 6
Reserve: 0.1 ATOM
```

### Osmosis
```
Proje adı: Osmosis
Binary: osmosisd
Chain ID: osmosis-1
Base denom: uosmo
Display denom: OSMO
Decimals: 6
Reserve: 1.0 OSMO
```

### Celestia
```
Proje adı: Celestia
Binary: celestia-appd
Chain ID: celestia
Base denom: utia
Display denom: TIA
Decimals: 6
Reserve: 0.5 TIA
```

## 📝 Log Dosyaları

Script iki tür log tutar:

1. **cosmos_auto_compound.log**: Detaylı işlem logları
2. **Ekran çıktısı**: Anlık durum bilgisi

Log'ları takip etmek için:
```bash
tail -f cosmos_auto_compound.log
```

## 🔧 Yapılandırma Dosyası

`cosmos_config.json` dosyası elle de düzenlenebilir:
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
    "reserve_amount_display": 2.0,
    "reserve_amount": 2000000000000000000,
    "gas_fees": "250000award",
    "gas_adjustment": "1.6",
    "check_interval_hours": 1.0
}
```

## ⚙️ Sistemd Servisi (Opsiyonel)

Scripti sistem servisi olarak çalıştırmak için:

1. Servis dosyası oluşturun:
```bash
sudo nano /etc/systemd/system/cosmos-autocompound.service
```

2. İçeriği:
```ini
[Unit]
Description=Cosmos Auto Compound Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/script
ExecStart=/usr/bin/python3 /path/to/cosmos_auto_compound.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

3. Servisi etkinleştirin:
```bash
sudo systemctl daemon-reload
sudo systemctl enable cosmos-autocompound
sudo systemctl start cosmos-autocompound
```

4. Durumu kontrol edin:
```bash
sudo systemctl status cosmos-autocompound
```

## 🛡️ Güvenlik Notları

- ✅ Cüzdan şifresi asla dosyaya kaydedilmez
- ✅ Config dosyası yalnızca genel bilgileri içerir
- ✅ Private key'ler script tarafından ele alınmaz
- ⚠️ Script'i güvenli bir sunucuda çalıştırın
- ⚠️ Düzenli olarak log dosyalarını kontrol edin

## 🐛 Sorun Giderme

### Problem: "Binary bulunamadı"
```bash
which wardend  # Binary'nin yolunu kontrol edin
export PATH=$PATH:/path/to/binary
```

### Problem: "Permission denied"
```bash
chmod +x cosmos_auto_compound.py
```

### Problem: "Config yüklenemedi"
Config dosyasını silin ve yeniden oluşturun:
```bash
rm cosmos_config.json
python3 cosmos_auto_compound.py
```

## 📞 Destek

Sorun yaşarsanız log dosyasını kontrol edin:
```bash
cat cosmos_auto_compound.log
```

## 🎉 İpuçları

1. **Test Modu**: İlk kullanımda `--once` parametresi ile test edin
2. **Reserve Miktarı**: Gas fee'leri karşılayacak kadar reserve bırakın
3. **Kontrol Aralığı**: Ödüllerin birikmesine göre ayarlayın (önerilen: 6-24 saat)
4. **Gas Fees**: Network durumuna göre ayarlayın

## 🔄 Güncelleme

Yeni bir proje eklemek için:
```bash
python3 cosmos_auto_compound.py
# Mevcut yapılandırmayı kullanmak istiyor musunuz? -> h
# Yeni bilgileri girin
```

## ⚡ Hızlı Başlangıç

```bash
# 1. Script'i hazırlayın
chmod +x cosmos_auto_compound.py

# 2. Tek seferlik test yapın
python3 cosmos_auto_compound.py --once

# 3. Her şey yolundaysa sürekli çalıştırın
screen -S cosmos
python3 cosmos_auto_compound.py
# Ctrl+A+D ile detach
```

---

**Not:** Bu script tüm Cosmos SDK tabanlı blockchain'ler için evrenseldir. Sadece doğru parametreleri girmeniz yeterlidir!
