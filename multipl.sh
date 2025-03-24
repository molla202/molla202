#!/bin/bash

# Başlık gösterimi
sleep 1
echo -e '\e[0;32m'
echo " ▄████████  ▄██████▄     ▄████████    ▄████████     ███▄▄▄▄    ▄██████▄  ████████▄     ▄████████ ";
echo "███    ███ ███    ███   ███    ███   ███    ███     ███▀▀▀██▄ ███    ███ ███   ▀███   ███    ███ ";
echo "███    █▀  ███    ███   ███    ███   ███    █▀      ███   ███ ███    ███ ███    ███   ███    █▀  ";
echo "███        ███    ███  ▄███▄▄▄▄██▀  ▄███▄▄▄         ███   ███ ███    ███ ███    ███  ▄███▄▄▄     ";
echo "███        ███    ███ ▀▀███▀▀▀▀▀   ▀▀███▀▀▀         ███   ███ ███    ███ ███    ███ ▀▀███▀▀▀     ";
echo "███    █▄  ███    ███ ▀███████████   ███    █▄      ███   ███ ███    ███ ███    ███   ███    █▄  ";
echo "███    ███ ███    ███   ███    ███   ███    ███     ███   ███ ███    ███ ███   ▄███   ███    ███ ";
echo "████████▀   ▀██████▀    ███    ███   ██████████      ▀█   █▀   ▀██████▀  ████████▀    ██████████ ";
echo "                        ███    ███                                                               ";
echo ""
echo -e '\e[0m'
sleep 3

# Dosyaları indirin ve klasörü oluşturun
echo "Dosyaları indiriliyor ve klasör oluşturuluyor..."
mkdir -p $HOME/selfcore
cd $HOME/selfcore
wget https://github.com/molla202/molla202/raw/main/cw20_base.wasm
echo "Dosyalar başarıyla indirildi ve klasör oluşturuldu."

# Kullanıcıdan gerekli bilgileri alın
read -p "Lütfen cüzdan adınızı girin: " KEY_NAME
read -p "Lütfen token adını girin: " TOKEN_NAME
read -p "Lütfen token sembolünü girin: " TOKEN_SYMBOL
read -p "Lütfen cüzdan adresinizi girin: " WALLET_ADDRESS

# Adresleri alın ve uyarıyı gösterin
echo "Lütfen göndermek istediğiniz adresleri virgülle ayırarak girin (örn: adres1,adres2):"
read -p "Adresler: " ADDRESSES_INPUT

# Adresleri diziye çevirin
IFS=',' read -r -a ADDRESSES <<< "$ADDRESSES_INPUT"

# Contract dosyasının yolunu tanımlayın
CONTRACT_WASM="$HOME/selfcore/cw20_base.wasm"

# INIT değişkenini oluşturun
INIT=$(jq -n \
  --arg name "$TOKEN_NAME" \
  --arg symbol "$TOKEN_SYMBOL" \
  --arg address "$WALLET_ADDRESS" \
  '{name: $name, symbol: $symbol, decimals: 6, initial_balances: [{address: $address, amount: "5000000"}], mint: {minter: $address}, marketing: {}}')

# Contract'ı deploy edin
echo "Contract deploy ediliyor..."
TX_HASH=$(selfchaind tx wasm store $CONTRACT_WASM --from $KEY_NAME --gas auto --gas-adjustment 1.4 --gas-prices="0.005uslf" -y --output json | jq -r '.txhash')
echo "Contract başarıyla deploy edildi. TxHash: $TX_HASH"

# Son işlemi alın
LATEST_TX=$(selfchaind q txs --events "message.action='store_code'" --page 1 --limit 1 --output json | jq -r '.txs[0].txhash')

# Code ID'yi alın
CODE_ID=$(selfchaind q tx $LATEST_TX --output json | jq -r '.logs[0].events[] | select(.type == "store_code") | .attributes[] | select(.key == "code_id") | .value')

# Token'ı oluşturun
echo "Token oluşturuluyor..."
selfchaind tx wasm instantiate $CODE_ID "$INIT" --from $KEY_NAME --label "test" --gas auto --gas-adjustment 1.4 --gas-prices="0.005uslf" --no-admin -y
echo "Token başarıyla oluşturuldu."

# Contract adresini alın
CONTRACT=$(selfchaind query wasm list-contract-by-code $CODE_ID --output json | jq -r '.contracts[-1]')

# Her adrese token gönderin
echo "Token gönderimi başlıyor..."
for ADDRESS in "${ADDRESSES[@]}"; do
  TRANSFER=$(jq -n --arg recipient "$ADDRESS" '{"transfer":{"recipient":$recipient,"amount":"100"}}')
  TX_HASH=$(selfchaind tx wasm execute $CONTRACT "$TRANSFER" --gas auto --gas-adjustment 1.4 --gas-prices="0.005uslf" --from $KEY_NAME -y --output json | jq -r '.txhash')
  echo "Token başarıyla gönderildi. TxHash: $TX_HASH"
done

echo "İşlemler başarıyla tamamlandı."
