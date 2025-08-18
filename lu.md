<h1 align="center"> Lumera




![image](https://github.com/user-attachments/assets/291dc80d-e97a-4941-b9be-ac0c39d2278c)

</h1>

 * [Topluluk kanalımız](https://t.me/corenodechat)<br>
 * [Topluluk Twitter](https://twitter.com/corenodeHQ)<br>


### Public RPC



### Explorer

### Faucet

https://faucet.testnet.lumera.io/

## 💻 Sistem Gereksinimleri
| Bileşenler | Minimum Gereksinimler | 
| ------------ | ------------ |
| CPU |	4|
| RAM	| 8+ GB |
| Storage	| 400 GB SSD |




### 🚧Gerekli kurulumlar
```
sudo apt update && sudo apt upgrade -y
sudo apt install curl git wget htop tmux build-essential jq make lz4 gcc unzip -y
```

### 🚧Go kurulumu
```
ver="1.22.5"
wget "https://golang.org/dl/go$ver.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go$ver.linux-amd64.tar.gz"
rm "go$ver.linux-amd64.tar.gz"
echo "export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin" >> ~/.bash_profile
source ~/.bash_profile
go version
```
### 🚧Dosyaları çekelim
```
cd $HOME
mkdir -p $HOME/lume
cd lume
wget https://github.com/LumeraProtocol/lumera/releases/download/v1.6.1/lumera_v1.6.1_linux_amd64.tar.gz
tar xzvf lumera_v1.6.1_linux_amd64.tar.gz
chmod +x lumerad
```
```
cd
mkdir -p $HOME/.lumera/cosmovisor/genesis/bin
mv $HOME/lume/lumerad $HOME/.lumera/cosmovisor/genesis/bin
mv $HOME/lume/libwasmvm.x86_64.so $HOME/.lumera/


```
```
echo 'export LD_LIBRARY_PATH=$HOME/.lumera:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```
```
sudo ln -s $HOME/.lumera/cosmovisor/genesis $HOME/.lumera/cosmovisor/current -f
sudo ln -s $HOME/.lumera/cosmovisor/current/bin/lumerad /usr/local/bin/lumerad -f
```
### 🚧Cosmovisor kuralım
```
go install cosmossdk.io/tools/cosmovisor/cmd/cosmovisor@v1.5.0
```
### 🚧Servis oluşturalım
```
sudo tee /etc/systemd/system/lumerad.service > /dev/null << EOF
[Unit]
Description=lumerad node service
After=network-online.target

[Service]
User=$USER
ExecStart=$(which cosmovisor) run start
Restart=on-failure
RestartSec=10
LimitNOFILE=65535
Environment="DAEMON_HOME=$HOME/.lumera"
Environment="DAEMON_NAME=lumerad"
Environment="UNSAFE_SKIP_BACKUP=true"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$HOME/.lumera/cosmovisor/current/bin"
Environment="LD_LIBRARY_PATH=$HOME/.lumera"

[Install]
WantedBy=multi-user.target
EOF
```
### 🚧Etkinleştirelim
```
sudo systemctl daemon-reload
sudo systemctl enable lumerad
```
### 🚧İnit
```
lumerad init "MONIKER" --chain-id lumera-mainnet-1
```
### 🚧Genesis ve addrbook
```
curl -L https://raw.githubusercontent.com/LumeraProtocol/lumera-networks/refs/heads/master/mainnet/claims.csv > $HOME/.lumera/config/claims.csv
curl -L https://raw.githubusercontent.com/LumeraProtocol/lumera-networks/refs/heads/master/mainnet/genesis.json > $HOME/.lumera/config/genesis.json
```
### 🚧Port
```
echo "export LUM_PORT="21"" >> $HOME/.bash_profile
source $HOME/.bash_profile
```
```
sed -i.bak -e "s%:1317%:${LUM_PORT}317%g;
s%:8080%:${LUM_PORT}080%g;
s%:9090%:${LUM_PORT}090%g;
s%:9091%:${LUM_PORT}091%g;
s%:8545%:${LUM_PORT}545%g;
s%:8546%:${LUM_PORT}546%g;
s%:6065%:${LUM_PORT}065%g" $HOME/.lumera/config/app.toml
```
### Port
```
sed -i.bak -e "s%:26658%:${LUM_PORT}658%g;
s%:26657%:${LUM_PORT}657%g;
s%:6060%:${LUM_PORT}060%g;
s%:26656%:${LUM_PORT}656%g;
s%^external_address = \"\"%external_address = \"$(wget -qO- eth0.me):${LUM_PORT}656\"%;
s%:26660%:${LUM_PORT}660%g" $HOME/.lumera/config/config.toml
```
### 🚧Seed ve Peer
```
SEEDS=""
PEERS="277773c00a7f7029775deba6e28532c40b670d16@lumera-mainnet-rpc.shazoes.xyz:30356,e1cedc37b9871332098d0a3ca2736813c92cedff@168.119.143.51:13656,e2c647e88db4deb2453cdbf2f08f98a1718e9e16@65.21.135.111:13656,ddd091cecab267b467f9f6167e9268391fc0ec1f@57.128.98.34:20001,385612fc40ace419dfb637e4f6e01ace4eb6897c@23.129.20.122:30756,faf9bc564f4d200d741da088731b6b3ba02192aa@65.108.232.93:30756,1636695e77723187f9d9bd6df3faae092712ca13@65.109.61.125:30756,8a6051b510f8adc802aece2e29976eabf3208eb5@96.230.25.243:26656,5b8d4baa4e4c86b94322d452dc66c4bf218cfc95@184.107.244.74:12300,1ef18bb3ed8efee9fb150151cbcdfca438fa9db4@64.185.227.242:30756,54361f222e87b7dd1cb90973079c44e7e31c03e5@15.235.42.134:12300,b7d5153841be7a3f1196767f55aa4817bb3cead0@148.113.162.70:12300,ab5b0bafe670543d6f25dea19a264c7da1e50672@65.108.201.240:30756"
sed -i -e "s/^seeds *=.*/seeds = \"$SEEDS\"/; s/^persistent_peers *=.*/persistent_peers = \"$PEERS\"/" $HOME/.lumera/config/config.toml

```

### 🚧Pruning
```
sed -i -e "s/^pruning *=.*/pruning = \"nothing\"/" $HOME/.lumera/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"100\"/" $HOME/.lumera/config/app.toml
sed -i 's|^indexer *=.*|indexer = "null"|' $HOME/.lumera/config/config.toml
```
### 🚧Gas ve index ayarı
```
sed -i.bak -e "s/^minimum-gas-prices *=.*/minimum-gas-prices = \"0.025ulume\"/" $HOME/.lumera/config/app.toml
```
### Snap 
YAPMA YAPMA YAPMAAAAA
```
lumerad tendermint unsafe-reset-all --home $HOME/.lumera
curl -L http://37.120.189.81/lumera_testnet/lumera_snap.tar.lz4 | tar -I lz4 -xf - -C $HOME/.lumera
```
### 🚧Başlatalım
NOT: buraya geldiysen dur önce gentx işlemlerini yap en alttan. başlatma da sonra sakın
```
sudo systemctl daemon-reload && sudo systemctl start lumerad && sudo journalctl -u lumerad -f --no-hostname -o cat
```
### Log
```
sudo journalctl -u lumerad -f --no-hostname -o cat
```
### Cüzdan olusturma
```
lumerad keys add cüzdan-adi-yaz
```
### Cüzdan import
```
lumerad keys add cüzdan-adi-yaz --recover
```
### Validator oluştur
```
cd $HOME
```
```
echo "{\"pubkey\":{\"@type\":\"/cosmos.crypto.ed25519.PubKey\",\"key\":\"$(lumerad comet show-validator | grep -Po '\"key\":\s*\"\K[^"]*')\"},
    \"amount\": \"1000000ulume\",
    \"moniker\": \"test\",
    \"identity\": \"AAA\",
    \"website\": \"AAA\",
    \"security\": \"AAA\",
    \"details\": \"AAA\",
    \"commission-rate\": \"0.1\",
    \"commission-max-rate\": \"0.2\",
    \"commission-max-change-rate\": \"0.01\",
    \"min-self-delegation\": \"1\"
}" > validatorlu.json
```

```
lumerad tx staking create-validator $HOME/.lumera/validatorlu.json \
--from wallet \
--chain-id lumera-mainnet-1 \
--gas-prices=0.025ulume \
--gas-adjustment=1.5 \
--gas=auto 
```

### unjail
```
lumerad tx slashing unjail --from wallet --chain-id lumera-mainnet-1 --gas-prices=0.025ulume --gas-adjustment=1.5 --gas=auto
```
### kendine stake
```
lumerad tx staking delegate $(lumerad keys show wallet --bech val -a) 1000000ulume --from wallet --chain-id lumera-mainnet-1 --gas-prices=0.025ulume --gas-adjustment=1.5 --gas=auto
```

### Delete node
```
sudo systemctl stop lumerad
sudo systemctl disable lumerad
sudo rm /etc/systemd/system/lumerad.service
sudo systemctl daemon-reload
rm -f $(which lumerad)
rm -rf .lumera
```
### Gentx

NOT: forklayacağınız ve gentxisini koyacağız yol https://github.com/LumeraProtocol/lumera-networks/tree/master/mainnet/gentx

NOT: alttakileri değiştir sonra kopyala yapıstır.
```
CHAIN_ID="lumera-mainnet-1"
MONIKER="---"
KEYNAME="---"
AMOUNT="1000000ulume"
VAL_DETAILS="---"
VAL_IDENTITY="---"
VAL_SECURITY_CONTACT="---"
VAL_WEBSITE="---"
VAL_COMMISSION_RATE="0.10"
VAL_COMMISSION_MAX_RATE="0.25"
VAL_COMMISSION_MAX_CHANGE_RATE="0.05"
MIN_SELF_DELEGATION="1"
```
```
lumerad genesis validate
```

NOT: eğer testeki cüzdanı kullanıcaksan aşağıdaki kodun sonuna --recover ekle
```
lumerad keys add $KEYNAME --keyring-backend file
```
```
VALIDATOR_ADDRESS=$(lumerad keys show $KEYNAME -a --keyring-backend file)
echo "Validator Address: $VALIDATOR_ADDRESS"
```
```
lumerad genesis add-genesis-account $VALIDATOR_ADDRESS $AMOUNT --keyring-backend file
```
```
lumerad genesis gentx $KEYNAME $AMOUNT \
	--chain-id=$CHAIN_ID \
	--moniker=$MONIKER \
	--commission-rate=$VAL_COMMISSION_RATE \
	--commission-max-rate=$VAL_COMMISSION_MAX_RATE \
	--commission-max-change-rate=$VAL_COMMISSION_MAX_CHANGE_RATE \
	--min-self-delegation=$MIN_SELF_DELEGATION \
	--details="$VAL_DETAILS" \
	--identity="$VAL_IDENTITY" \
	--security-contact="$VAL_SECURITY_CONTACT" \
	--website="$VAL_WEBSITE" \
	--keyring-backend=file
```
```
lumerad genesis validate
```

### pr atarken açıklama aşağıdakini moniker kısmını yazıp öle atın
```
##### Validator Information
Moniker: corenode

## Checklist
- [ ] I have backed up my validator keys securely
- [ ] I have stored my mnemonic phrase safely
- [ ] I have verified new genesis file is valid (I ran `lumerad genesis validate`)
- [ ] I have verified my gentx file is valid
- [ ] I will be available during the network launch
```

