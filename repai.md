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
mkdir -p $HOME/.republicd/cosmovisor/genesis/bin
curl -L "https://media.githubusercontent.com/media/RepublicAI/networks/main/testnet/releases/v0.1.0/republicd-linux-amd64" -o $HOME/.republicd/cosmovisor/genesis/bin/republicd
chmod +x $HOME/.republicd/cosmovisor/genesis/bin/republicd
```
```
sudo ln -s $HOME/.republicd/cosmovisor/genesis $HOME/.republicd/cosmovisor/current -f
sudo ln -s $HOME/.republicd/cosmovisor/current/bin/republicd /usr/local/bin/republicd -f
```
### 🚧Cosmovisor kuralım
```
go install cosmossdk.io/tools/cosmovisor/cmd/cosmovisor@v1.5.0
```
### 🚧Servis oluşturalım
```
sudo tee /etc/systemd/system/republicd.service > /dev/null << EOF
[Unit]
Description=lumerad node service
After=network-online.target

[Service]
User=$USER
ExecStart=$(which cosmovisor) run start
Restart=on-failure
RestartSec=10
LimitNOFILE=65535
Environment="DAEMON_HOME=$HOME/.republicd"
Environment="DAEMON_NAME=republicd"
Environment="UNSAFE_SKIP_BACKUP=true"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$HOME/.lumera/cosmovisor/current/bin"

[Install]
WantedBy=multi-user.target
EOF
```
### 🚧Etkinleştirelim
```
sudo systemctl daemon-reload
sudo systemctl enable republicd
```
### 🚧İnit
```
republicd init "MONIKER" --chain-id raitestnet_77701-2
```
### 🚧Genesis ve addrbook
```
curl -L https://raw.githubusercontent.com/RepublicAI/networks/main/testnet/genesis.json > $HOME/.republicd/config/genesis.json
```
```
sed -i.bak -e "s/^minimum-gas-prices *=.*/minimum-gas-prices = \"250000000arai\"/" $HOME/.republicd/config/app.toml
```
### 🚧Port
```
echo "export REP_PORT="38"" >> $HOME/.bash_profile
source $HOME/.bash_profile
```
```
sed -i.bak -e "s%:1317%:${REP_PORT}317%g;
s%:8080%:${REP_PORT}080%g;
s%:9090%:${REP_PORT}090%g;
s%:9091%:${REP_PORT}091%g;
s%:8545%:${REP_PORT}545%g;
s%:8546%:${REP_PORT}546%g;
s%:6065%:${REP_PORT}065%g" $HOME/.republicd/config/app.toml
```
### Port
```
sed -i.bak -e "s%:26658%:${REP_PORT}658%g;
s%:26657%:${REP_PORT}657%g;
s%:6060%:${REP_PORT}060%g;
s%:26656%:${REP_PORT}656%g;
s%^external_address = \"\"%external_address = \"$(wget -qO- eth0.me):${REP_PORT}656\"%;
s%:26660%:${REP_PORT}660%g" $HOME/.republicd/config/config.toml
```
### 🚧Seed ve Peer
```
PEERS="517759f225c44c64fdc2fd5f4576778da4810fa5@44.199.194.212:26656,655b4c80d267633a6609d7030517a4043ffc419b@54.152.212.109:26656"
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"$PEERS\"/" "$HOME/.republicd/config/config.toml"
```

### 🚧Pruning
```
sed -i -e "s/^pruning *=.*/pruning = \"nothing\"/" $HOME/.republicd/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"100\"/" $HOME/.republicd/config/app.toml
sed -i 's|^indexer *=.*|indexer = "null"|' $HOME/.republicd/config/config.toml
```
### Snap 
YAPMA YAPMA YAPMAAAAA
```
hahhah zaten yok ki :D
```
### 🚧Başlatalım
```
sudo systemctl daemon-reload && sudo systemctl start republicd && sudo journalctl -u republicd -f --no-hostname -o cat
```
### Log
```
sudo journalctl -u republicd -f --no-hostname -o cat
```
### Cüzdan olusturma
```
republicd keys add cüzdan-adi-yaz
```
### Cüzdan import
```
republicd keys add cüzdan-adi-yaz --recover
```
### Validator oluştur
```
cd $HOME
```
```
republicd tx staking create-validator \
  --amount=1000000000000000000000arai \
  --pubkey=$(republicd comet show-validator) \
  --moniker="<your-moniker>" \
  --chain-id=raitestnet_77701-2 \
  --commission-rate="0.10" \
  --commission-max-rate="0.20" \
  --commission-max-change-rate="0.01" \
  --min-self-delegation="1" \
  --gas=auto \
  --gas-adjustment=1.5 \
  --gas-prices="250000000arai" \
  --from=<key-name>
```

### unjail
```
republicd tx slashing unjail --from wallet --chain-id raitestnet_77701-2 -gas=auto --gas-adjustment=1.5 --gas-prices=250000000arai
```
### kendine stake
```
republicd tx staking delegate $(republicd keys show wallet --bech val -a) 1000000arai --from wallet --chain-id raitestnet_77701-2 --gas=auto --gas-adjustment=1.5 --gas-prices=250000000arai
```

### Delete node
```
sudo systemctl stop republicd
sudo systemctl disable republicd
sudo rm /etc/systemd/system/republicd.service
sudo systemctl daemon-reload
rm -f $(which republicd)
rm -rf .republicd
```
