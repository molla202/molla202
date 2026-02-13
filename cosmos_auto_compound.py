#!/usr/bin/env python3
"""
Evrensel Cosmos Auto-Compound Scripti
Tüm Cosmos SDK tabanlı blockchain'ler için ödül çekme ve stake scripti
"""

import subprocess
import json
import time
import logging
import os
import sys
from datetime import datetime
from getpass import getpass

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cosmos_auto_compound.log'),
        logging.StreamHandler()
    ]
)

class ConfigManager:
    """Yapılandırma yöneticisi"""
    
    def __init__(self, config_file='cosmos_config.json'):
        self.config_file = config_file
        self.config = {}
    
    def load_config(self):
        """Kaydedilmiş yapılandırmayı yükle"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
                return True
            except Exception as e:
                logging.error(f"Config yükleme hatası: {e}")
                return False
        return False
    
    def save_config(self, config):
        """Yapılandırmayı kaydet"""
        try:
            # Şifreyi kaydetme (güvenlik)
            config_to_save = config.copy()
            if 'wallet_password' in config_to_save:
                del config_to_save['wallet_password']
            
            with open(self.config_file, 'w') as f:
                json.dump(config_to_save, f, indent=4)
            logging.info(f"✅ Yapılandırma kaydedildi: {self.config_file}")
            return True
        except Exception as e:
            logging.error(f"Config kaydetme hatası: {e}")
            return False
    
    def display_config(self):
        """Mevcut yapılandırmayı göster"""
        if not self.config:
            return
        
        print("\n" + "=" * 70)
        print("MEVCUT YAPILANDIRMA")
        print("=" * 70)
        print(f"Proje Adı:           {self.config.get('project_name', 'N/A')}")
        print(f"Chain ID:            {self.config.get('chain_id', 'N/A')}")
        print(f"Binary:              {self.config.get('binary', 'N/A')}")
        print(f"Base Denom:          {self.config.get('base_denom', 'N/A')}")
        print(f"Display Denom:       {self.config.get('display_denom', 'N/A')}")
        print(f"Decimals:            {self.config.get('decimals', 'N/A')}")
        print(f"Validator Address:   {self.config.get('validator_address', 'N/A')}")
        print(f"Wallet Name:         {self.config.get('wallet_name', 'N/A')}")
        print(f"Wallet Address:      {self.config.get('wallet_address', 'N/A')}")
        print(f"Reserve Amount:      {self.config.get('reserve_amount_display', 'N/A')} {self.config.get('display_denom', '')}")
        print(f"Gas Fees:            {self.config.get('gas_fees', 'N/A')}")
        print("=" * 70 + "\n")
    
    def prompt_for_config(self):
        """Kullanıcıdan yapılandırma bilgilerini al"""
        print("\n" + "=" * 70)
        print("COSMOS AUTO-COMPOUND YAPILANDIRMA")
        print("=" * 70 + "\n")
        
        config = {}
        
        # Proje adı
        config['project_name'] = input("Proje adı (örn: Warden, Celestia): ").strip()
        
        # Binary adı
        default_binary = config['project_name'].lower() + "d"
        binary_input = input(f"Binary adı [{default_binary}]: ").strip()
        config['binary'] = binary_input if binary_input else default_binary
        
        # Chain ID
        config['chain_id'] = input("Chain ID (örn: warden_8765-1): ").strip()
        
        # Base denom (ödeme için kullanılan)
        config['base_denom'] = input("Base denom (örn: award, uatom, uosmo): ").strip()
        
        # Display denom (gösterim için)
        default_display = config['base_denom'].replace('u', '').replace('a', '').upper()
        display_input = input(f"Display denom [{default_display}]: ").strip()
        config['display_denom'] = display_input if display_input else default_display
        
        # Decimals
        print("\nÖrnekler:")
        print("  - 18 decimals: 1 token = 1,000,000,000,000,000,000 base")
        print("  - 6 decimals:  1 token = 1,000,000 base")
        decimals_input = input("Decimal sayısı [18]: ").strip()
        config['decimals'] = int(decimals_input) if decimals_input else 18
        
        # Validator adresi
        config['validator_address'] = input("Validator adresi (örn: wardenvaloper1...): ").strip()
        
        # Cüzdan adı
        config['wallet_name'] = input("Cüzdan adı (örn: wallet): ").strip()
        
        # Cüzdan adresi
        config['wallet_address'] = input("Cüzdan adresi (örn: warden1...): ").strip()
        
        # Reserve amount (display cinsinden)
        default_reserve = "1.0"
        reserve_input = input(f"Reserve miktarı (cüzdanda kalacak) [{default_reserve} {config['display_denom']}]: ").strip()
        reserve_display = float(reserve_input) if reserve_input else float(default_reserve)
        config['reserve_amount_display'] = reserve_display
        config['reserve_amount'] = int(reserve_display * (10 ** config['decimals']))
        
        # Gas fees
        default_gas = f"250000{config['base_denom']}"
        gas_input = input(f"Gas fees [{default_gas}]: ").strip()
        config['gas_fees'] = gas_input if gas_input else default_gas
        
        # Gas adjustment
        config['gas_adjustment'] = "1.6"
        
        # Kontrol aralığı
        default_interval = "1"
        interval_input = input(f"Kontrol aralığı (saat) [{default_interval}]: ").strip()
        config['check_interval_hours'] = float(interval_input) if interval_input else float(default_interval)
        
        print("\n" + "=" * 70)
        
        return config


class CosmosAutoCompound:
    """Evrensel Cosmos Auto-Compound Sınıfı"""
    
    def __init__(self, config, wallet_password=None):
        """
        config: Yapılandırma dictionary'si
        wallet_password: Cüzdan şifresi (opsiyonel)
        """
        self.validator_address = config['validator_address']
        self.wallet_name = config['wallet_name']
        self.wallet_address = config['wallet_address']
        self.chain_id = config['chain_id']
        self.binary = config['binary']
        self.base_denom = config['base_denom']
        self.display_denom = config['display_denom']
        self.decimals = config['decimals']
        self.reserve_amount = config['reserve_amount']
        self.gas_fees = config['gas_fees']
        self.gas_adjustment = config.get('gas_adjustment', '1.6')
        self.wallet_password = wallet_password
        self.project_name = config.get('project_name', 'Cosmos')
        
    def run_command(self, cmd, stdin_input=None):
        """Komut çalıştır ve sonucu döndür"""
        try:
            logging.debug(f"Komut: {cmd}")
            
            if stdin_input:
                # Şifre girişi gerekiyorsa
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    input=stdin_input,
                    timeout=60
                )
            else:
                result = subprocess.run(
                    cmd, 
                    shell=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=60
                )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            logging.error(f"Komut zaman aşımına uğradı: {cmd}")
            return "", "Timeout", 1
        except Exception as e:
            logging.error(f"Komut hatası: {e}")
            return "", str(e), 1
    
    def format_amount(self, base_amount):
        """Base miktarı display formatına çevir"""
        return base_amount / (10 ** self.decimals)
    
    def withdraw_commission(self):
        """Validatör komisyonunu çek"""
        # Önce validator adresini kontrol et
        val_check_cmd = f"{self.binary} keys show {self.wallet_name} --bech val -a"
        val_output, val_error, val_code = self.run_command(val_check_cmd, self.wallet_password)
        
        if val_code != 0 or not val_output:
            logging.info("ℹ️  Bu cüzdan bir validatör değil, komisyon çekme atlanıyor")
            return True
        
        cmd = f"{self.binary} tx distribution withdraw-rewards {val_output.strip()} --from {self.wallet_name} --commission --chain-id {self.chain_id} --gas auto --gas-adjustment {self.gas_adjustment} --fees {self.gas_fees} -y"
        
        logging.info("Komisyon ödülleri çekiliyor...")
        output, error, code = self.run_command(cmd, self.wallet_password)
        
        if code == 0:
            logging.info("✅ Komisyon çekme işlemi başarılı")
            time.sleep(8)
            return True
        else:
            logging.warning(f"⚠️  Komisyon çekme hatası (normal olabilir): {error}")
            return False
    
    def withdraw_all_rewards(self):
        """Tüm ödülleri çek"""
        cmd = f"{self.binary} tx distribution withdraw-all-rewards --from {self.wallet_name} --chain-id {self.chain_id} --gas auto --gas-adjustment {self.gas_adjustment} --fees {self.gas_fees} -y"
        
        logging.info("Tüm ödüller çekiliyor...")
        output, error, code = self.run_command(cmd, self.wallet_password)
        
        if code == 0:
            logging.info("✅ Ödül çekme işlemi başarılı")
            time.sleep(8)
            return True
        else:
            logging.error(f"❌ Ödül çekme hatası: {error}")
            return False
    
    def get_balance(self):
        """Cüzdan bakiyesini kontrol et"""
        cmd = f"{self.binary} query bank balances {self.wallet_address} --output json"
        output, error, code = self.run_command(cmd)
        
        if code == 0 and output:
            try:
                data = json.loads(output)
                balances = data.get('balances', [])
                
                for balance in balances:
                    denom = balance.get('denom', '')
                    if denom == self.base_denom:
                        amount = int(balance.get('amount', '0'))
                        display_amount = self.format_amount(amount)
                        logging.info(f"Cüzdan bakiyesi: {display_amount:.6f} {self.display_denom} ({amount} {self.base_denom})")
                        return amount
                
                logging.warning(f"⚠️  Cüzdanda '{self.base_denom}' token bulunamadı")
                logging.info(f"Mevcut tokenler: {[b.get('denom') for b in balances]}")
                return 0
                
            except json.JSONDecodeError as e:
                logging.error(f"JSON parse hatası: {e}")
                logging.info(f"Ham çıktı: {output}")
            except Exception as e:
                logging.error(f"Bakiye parse hatası: {e}")
                logging.info(f"Output: {output}")
        else:
            logging.error(f"Bakiye sorgusu başarısız: {error}")
        
        logging.warning("⚠️  Bakiye okunamadı")
        return 0
    
    def delegate_tokens(self, amount):
        """Token'ları stake et"""
        if amount <= 0:
            logging.warning("⚠️  Stake edilecek miktar yok")
            return False
            
        cmd = f"{self.binary} tx staking delegate {self.validator_address} {amount}{self.base_denom} --from {self.wallet_name} --chain-id {self.chain_id} --gas auto --gas-adjustment {self.gas_adjustment} --fees {self.gas_fees} -y"
        
        display_amount = self.format_amount(amount)
        logging.info(f"Stake ediliyor: {display_amount:.6f} {self.display_denom} ({amount} {self.base_denom})")
        output, error, code = self.run_command(cmd, self.wallet_password)
        
        if code == 0:
            logging.info("✅ Stake işlemi başarılı")
            return True
        else:
            logging.error(f"❌ Stake hatası: {error}")
            return False
    
    def auto_compound(self):
        """Otomatik compound işlemi"""
        logging.info("=" * 70)
        logging.info(f"{self.project_name} Otomatik Compound - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info("=" * 70)
        
        # 1. Komisyon çek (validatör ise)
        self.withdraw_commission()
        
        # 2. Tüm ödülleri çek
        if not self.withdraw_all_rewards():
            logging.error("Ödül çekme başarısız, işlem iptal edildi")
            return False
        
        # İşlemin blockchain'e yazılmasını bekle
        logging.info("İşlemin tamamlanması bekleniyor...")
        time.sleep(10)
        
        # 3. Bakiyeyi kontrol et
        balance = self.get_balance()
        if balance == 0:
            logging.warning("⚠️  Bakiye bulunamadı")
            return False
        
        # 4. Stake edilecek miktarı hesapla (bakiye - reserve)
        if balance <= self.reserve_amount:
            reserve_display = self.format_amount(self.reserve_amount)
            balance_display = self.format_amount(balance)
            logging.warning(f"Bakiye reserve miktarından az veya eşit")
            logging.info(f"   Bakiye: {balance_display:.6f} {self.display_denom}")
            logging.info(f"   Reserve: {reserve_display:.6f} {self.display_denom}")
            return False
        
        stake_amount = balance - self.reserve_amount
        reserve_display = self.format_amount(self.reserve_amount)
        stake_display = self.format_amount(stake_amount)
        balance_display = self.format_amount(balance)
        
        logging.info(f"Hesaplamalar:")
        logging.info(f"   Toplam Bakiye: {balance_display:.6f} {self.display_denom}")
        logging.info(f"   Reserve (Kalacak): {reserve_display:.6f} {self.display_denom}")
        logging.info(f"   Stake Edilecek: {stake_display:.6f} {self.display_denom}")
        
        # 5. Stake et
        if stake_amount > 0:
            return self.delegate_tokens(stake_amount)
        
        return False


def main():
    """Ana fonksiyon"""
    
    config_manager = ConfigManager()
    
    # Mevcut config var mı kontrol et
    config_exists = config_manager.load_config()
    
    if config_exists:
        config_manager.display_config()
        
        # Kullanıcıya sor: mevcut config'i kullan mı?
        choice = input("Mevcut yapılandırmayı kullanmak istiyor musunuz? (E/h) [E]: ").strip().lower()
        
        if choice in ['h', 'hayır', 'n', 'no']:
            # Yeni config iste
            config = config_manager.prompt_for_config()
            config_manager.save_config(config)
        else:
            # Mevcut config'i kullan
            config = config_manager.config
            logging.info("✅ Mevcut yapılandırma kullanılıyor")
    else:
        # Config yok, yeni oluştur
        print("Yapılandırma dosyası bulunamadı. Yeni yapılandırma oluşturuluyor...\n")
        config = config_manager.prompt_for_config()
        config_manager.save_config(config)
    
    # Cüzdan şifresi (her çalıştırmada sor - güvenlik)
    print("\n" + "=" * 70)
    use_password = input("Cüzdan şifresi kullanıyor musunuz? (e/H) [H]: ").strip().lower()
    wallet_password = None
    
    if use_password in ['e', 'evet', 'y', 'yes']:
        wallet_password = getpass("Cüzdan şifresi: ")
        if wallet_password:
            wallet_password = wallet_password + "\n"  # Newline ekle
    
    print("=" * 70 + "\n")
    
    # Auto-compound instance oluştur
    auto_compound = CosmosAutoCompound(config, wallet_password)
    
    logging.info(f"{config.get('project_name', 'Cosmos')} Otomatik Compound Scripti")
    logging.info(f"Validatör: {config['validator_address']}")
    logging.info(f"Cüzdan: {config['wallet_address']}")
    logging.info(f"Reserve: {config['reserve_amount_display']} {config['display_denom']}")
    logging.info(f"Kontrol Aralığı: {config.get('check_interval_hours', 1)} saat")
    logging.info("=" * 70)
    
    # Tek seferlik çalıştırma için '--once' parametresi kontrol et
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        logging.info("Tek seferlik çalıştırma modu")
        auto_compound.auto_compound()
        logging.info("✅ İşlem tamamlandı")
        return
    
    # Sürekli çalıştırma modu
    check_interval = int(config.get('check_interval_hours', 1) * 3600)
    logging.info("Sürekli çalıştırma modu (Durdurmak için Ctrl+C)")
    
    while True:
        try:
            auto_compound.auto_compound()
            logging.info(f"Bir sonraki kontrol: {config.get('check_interval_hours', 1)} saat sonra")
            logging.info("=" * 70 + "\n")
            time.sleep(check_interval)
        except KeyboardInterrupt:
            logging.info("\n✅ Script kullanıcı tarafından durduruldu")
            break
        except Exception as e:
            logging.error(f"❌ Beklenmeyen hata: {e}")
            logging.info("60 saniye sonra tekrar denenecek...")
            time.sleep(60)


if __name__ == "__main__":
    main()
