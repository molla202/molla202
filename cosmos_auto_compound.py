#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
        logging.FileHandler('cosmos_auto_compound.log', encoding='utf-8'),
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
                with open(self.config_file, 'r', encoding='utf-8') as f:
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
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=4, ensure_ascii=False)
            logging.info(f"Yapılandırma kaydedildi: {self.config_file}")
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
        print(f"RPC Address:         {self.config.get('rpc_address', 'N/A')}")
        print(f"Reserve Amount:      {self.config.get('reserve_amount_display', 'N/A')} {self.config.get('display_denom', '')}")
        
        if self.config.get('use_gas_prices'):
            print(f"Gas Prices:          {self.config.get('gas_prices', 'N/A')}")
        else:
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
        
        # Gas fees veya gas prices
        print("\nGas Ayarları:")
        print("  İki seçenek var:")
        print("    1. Gas Prices (önerilen): Birim fiyat, otomatik hesaplanır")
        print("    2. Fixed Fees: Sabit ücret")
        print("\nÖrnekler:")
        print("  Gas Prices:")
        print("    - Warden (18 decimals): 1000000000arai")
        print("    - Cosmos (6 decimals):  0.025uatom")
        print("  Fixed Fees:")
        print("    - Warden: 250000000000000award")
        print("    - Cosmos: 5000uatom")
        
        fee_choice = input("\nGas prices kullanmak ister misiniz? (E/h) [E]: ").strip().lower()
        
        if fee_choice in ['', 'e', 'evet', 'y', 'yes']:
            config['use_gas_prices'] = True
            
            # Decimal sayısına göre önerilen gas price
            if config['decimals'] == 18:
                suggested = f"1000000000{config['base_denom']}"
            elif config['decimals'] == 6:
                suggested = f"0.025{config['base_denom']}"
            else:
                suggested = f"1000{config['base_denom']}"
            
            gas_input = input(f"Gas prices [{suggested}]: ").strip()
            config['gas_prices'] = gas_input if gas_input else suggested
            config['gas_fees'] = None  # Fees kullanılmayacak
        else:
            config['use_gas_prices'] = False
            
            # Decimal sayısına göre önerilen gas fee
            if config['decimals'] == 18:
                suggested_gas = f"250000000000000{config['base_denom']}"
            elif config['decimals'] == 6:
                suggested_gas = f"5000{config['base_denom']}"
            else:
                suggested_gas = f"250000{config['base_denom']}"
            
            gas_input = input(f"Gas fees [{suggested_gas}]: ").strip()
            config['gas_fees'] = gas_input if gas_input else suggested_gas
            config['gas_prices'] = None  # Prices kullanılmayacak
        
        # Gas adjustment
        config['gas_adjustment'] = "1.6"
        
        # RPC adresi
        print("\nRPC Adresi:")
        print("  Örnekler:")
        print("    - Localhost: http://localhost:26657")
        print("    - Custom port: http://localhost:26658")
        print("    - Remote: https://rpc.example.com:443")
        default_rpc = "http://localhost:26657"
        rpc_input = input(f"RPC adresi [{default_rpc}]: ").strip()
        config['rpc_address'] = rpc_input if rpc_input else default_rpc
        
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
        self.gas_fees = config.get('gas_fees')
        self.gas_prices = config.get('gas_prices')
        self.use_gas_prices = config.get('use_gas_prices', False)
        self.gas_adjustment = config.get('gas_adjustment', '1.6')
        self.wallet_password = wallet_password
        self.project_name = config.get('project_name', 'Cosmos')
        self.rpc_address = config.get('rpc_address', 'http://localhost:26657')
        
        # Gas fee miktarını parse et (buffer hesaplaması için)
        if self.use_gas_prices and self.gas_prices:
            self.gas_fee_amount = self._parse_gas_fee(self.gas_prices)
        elif self.gas_fees:
            self.gas_fee_amount = self._parse_gas_fee(self.gas_fees)
        else:
            self.gas_fee_amount = 0
    
    def _parse_gas_fee(self, gas_fees_string):
        """
        Gas fee string'inden sayısal değeri çıkar
        
        Desteklenen formatlar:
        - "250000000000000arai"  -> 250000000000000
        - "0.00025rai"          -> 250000000000000 (18 decimal)
        - "5000uatom"           -> 5000
        - "auto"                -> Manuel ayar gerekli (varsayılan kullanılır)
        """
        import re
        
        try:
            gas_fees_string = str(gas_fees_string).strip()
            
            # "auto" kontrolü
            if gas_fees_string.lower() == "auto":
                logging.warning("Gas fee 'auto' olarak ayarlanmış, manuel değer önerilir!")
                # Varsayılan değer kullan (decimal'e göre)
                if self.decimals == 18:
                    default_gas = 250000000000000
                elif self.decimals == 6:
                    default_gas = 5000
                else:
                    default_gas = 250000
                logging.info(f"Varsayılan gas fee kullanılıyor: {default_gas} {self.base_denom}")
                return default_gas
            
            # Decimal format kontrolü (örn: "0.00025rai")
            decimal_match = re.match(r'^([\d.]+)([a-zA-Z]+)$', gas_fees_string)
            if decimal_match and '.' in decimal_match.group(1):
                decimal_value = float(decimal_match.group(1))
                denom = decimal_match.group(2)
                
                # Bu proje için decimal sayısını kullan
                multiplier = 10 ** self.decimals
                result = int(decimal_value * multiplier)
                
                logging.debug(f"Decimal format parse edildi: {decimal_value} {denom} = {result} base units")
                return result
            
            # Normal format kontrolü (örn: "250000000000000arai")
            amount_str = ''.join([c for c in gas_fees_string if c.isdigit()])
            if amount_str:
                result = int(amount_str)
                logging.debug(f"Normal format parse edildi: {result}")
                return result
            
            logging.warning(f"Gas fee parse edilemedi: '{gas_fees_string}'")
            return 0
            
        except Exception as e:
            logging.warning(f"Gas fee parse edilemedi: {e}, varsayılan 0 kullanılıyor")
            return 0
        
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
            logging.info("Bu cüzdan bir validatör değil, komisyon çekme atlanıyor")
            return True
        
        # Gas parametrelerini belirle
        if self.use_gas_prices and self.gas_prices:
            gas_params = f"--gas auto --gas-adjustment {self.gas_adjustment} --gas-prices {self.gas_prices}"
        else:
            gas_params = f"--gas auto --gas-adjustment {self.gas_adjustment} --fees {self.gas_fees}"
        
        cmd = f"{self.binary} tx distribution withdraw-rewards {val_output.strip()} --from {self.wallet_name} --commission --chain-id {self.chain_id} --node {self.rpc_address} {gas_params} -y"
        
        logging.info("Komisyon ödülleri çekiliyor...")
        output, error, code = self.run_command(cmd, self.wallet_password)
        
        if code == 0:
            logging.info("Komisyon çekme işlemi başarılı")
            time.sleep(8)
            return True
        else:
            logging.warning(f"Komisyon çekme hatası (normal olabilir): {error}")
            return False
    
    def withdraw_all_rewards(self):
        """Tüm ödülleri çek"""
        # Gas parametrelerini belirle
        if self.use_gas_prices and self.gas_prices:
            gas_params = f"--gas auto --gas-adjustment {self.gas_adjustment} --gas-prices {self.gas_prices}"
        else:
            gas_params = f"--gas auto --gas-adjustment {self.gas_adjustment} --fees {self.gas_fees}"
        
        cmd = f"{self.binary} tx distribution withdraw-all-rewards --from {self.wallet_name} --chain-id {self.chain_id} --node {self.rpc_address} {gas_params} -y"
        
        logging.info("Tüm ödüller çekiliyor...")
        output, error, code = self.run_command(cmd, self.wallet_password)
        
        if code == 0:
            logging.info("Ödül çekme işlemi başarılı")
            time.sleep(8)
            return True
        else:
            logging.error(f"Ödül çekme hatası: {error}")
            return False
    
    def get_balance(self, silent=False):
        """Cüzdan bakiyesini kontrol et"""
        cmd = f"{self.binary} query bank balances {self.wallet_address} --node {self.rpc_address} --output json"
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
                        if not silent:
                            logging.info(f"Cüzdan bakiyesi: {display_amount:.6f} {self.display_denom} ({amount} {self.base_denom})")
                        return amount
                
                if not silent:
                    logging.warning(f"Cüzdanda '{self.base_denom}' token bulunamadı")
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
        
        if not silent:
            logging.warning("Bakiye okunamadı")
        return 0
    
    def delegate_tokens(self, amount):
        """Token'ları stake et"""
        if amount <= 0:
            logging.warning("Stake edilecek miktar yok")
            return False
        
        # Gas parametrelerini belirle
        if self.use_gas_prices and self.gas_prices:
            gas_params = f"--gas auto --gas-adjustment {self.gas_adjustment} --gas-prices {self.gas_prices}"
        else:
            gas_params = f"--gas auto --gas-adjustment {self.gas_adjustment} --fees {self.gas_fees}"
            
        cmd = f"{self.binary} tx staking delegate {self.validator_address} {amount}{self.base_denom} --from {self.wallet_name} --chain-id {self.chain_id} --node {self.rpc_address} {gas_params} -y"
        
        display_amount = self.format_amount(amount)
        logging.info(f"Stake ediliyor: {display_amount:.6f} {self.display_denom} ({amount} {self.base_denom})")
        output, error, code = self.run_command(cmd, self.wallet_password)
        
        if code == 0:
            logging.info("Stake işlemi başarılı")
            return True
        else:
            logging.error(f"Stake hatası: {error}")
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
            logging.warning("Bakiye bulunamadı")
            return False
        
        # 4. Gas fee için buffer hesapla
        # Gas prices kullanıyorsak, ortalama bir transaction için tahmini gas miktarı
        if self.use_gas_prices:
            # Ortalama bir tx ~200,000 gas kullanır
            # gas_price * estimated_gas * 5 (güvenlik için)
            estimated_gas = 200000
            gas_buffer = self.gas_fee_amount * estimated_gas * 5
            
            if gas_buffer == 0:
                # Eğer parse edilememiş ise, default değer kullan
                if self.decimals == 18:
                    gas_buffer = 1000000000000000000  # 1 token
                else:
                    gas_buffer = 1000000  # 1 token (6 decimals)
                logging.warning(f"Gas prices parse edilemedi, varsayılan buffer kullanılıyor")
        else:
            # Fixed fees kullanıyorsak
            gas_buffer = self.gas_fee_amount * 5
        
        minimum_required = self.reserve_amount + gas_buffer
        
        # 5. Bakiye kontrolü
        if balance <= minimum_required:
            reserve_display = self.format_amount(self.reserve_amount)
            balance_display = self.format_amount(balance)
            gas_display = self.format_amount(gas_buffer)
            logging.warning(f"Bakiye yetersiz")
            logging.info(f"   Bakiye: {balance_display:.6f} {self.display_denom}")
            logging.info(f"   Reserve: {reserve_display:.6f} {self.display_denom}")
            logging.info(f"   Gas Buffer (5x): {gas_display:.6f} {self.display_denom}")
            logging.info(f"   Minimum Gerekli: {self.format_amount(minimum_required):.6f} {self.display_denom}")
            return False
        
        # 6. Stake edilecek miktarı hesapla (bakiye - reserve - gas buffer)
        stake_amount = balance - minimum_required
        reserve_display = self.format_amount(self.reserve_amount)
        stake_display = self.format_amount(stake_amount)
        balance_display = self.format_amount(balance)
        gas_display = self.format_amount(gas_buffer)
        
        logging.info(f"")
        logging.info(f"Hesaplamalar:")
        logging.info(f"   Toplam Bakiye: {balance_display:.6f} {self.display_denom}")
        logging.info(f"   Reserve (Kalacak): {reserve_display:.6f} {self.display_denom}")
        logging.info(f"   Gas Buffer (5x): {gas_display:.6f} {self.display_denom}")
        logging.info(f"   ─────────────────────────────────────")
        logging.info(f"   Stake Edilecek: {stake_display:.6f} {self.display_denom}")
        logging.info(f"")
        
        # 7. Stake et
        if stake_amount > 0:
            success = self.delegate_tokens(stake_amount)
            
            # 8. Başarılıysa son bakiyeyi göster
            if success:
                time.sleep(5)
                logging.info("")
                logging.info("İşlem Sonrası Bakiye:")
                final_balance = self.get_balance(silent=True)
                final_display = self.format_amount(final_balance)
                logging.info(f"   Son Bakiye: {final_display:.6f} {self.display_denom}")
                logging.info("")
            
            return success
        else:
            logging.warning("Stake edilecek miktar yok (negatif veya sıfır)")
        
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
            logging.info("Mevcut yapılandırma kullanılıyor")
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
    logging.info(f"RPC: {config.get('rpc_address', 'N/A')}")
    logging.info(f"Reserve: {config['reserve_amount_display']} {config['display_denom']}")
    logging.info(f"Kontrol Aralığı: {config.get('check_interval_hours', 1)} saat")
    logging.info("=" * 70)
    
    # Tek seferlik çalıştırma için '--once' parametresi kontrol et
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        logging.info("Tek seferlik çalıştırma modu")
        auto_compound.auto_compound()
        logging.info("İşlem tamamlandı")
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
            logging.info("\nScript kullanıcı tarafından durduruldu")
            break
        except Exception as e:
            logging.error(f"Beklenmeyen hata: {e}")
            logging.info("60 saniye sonra tekrar denenecek...")
            time.sleep(60)


if __name__ == "__main__":
    main()
