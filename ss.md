
<h1 align="center"> Airchain </h1>


![image](https://github.com/molla202/Airchain/assets/91562185/64b9e7f3-4739-4774-b421-635e224dcd4f)




 * [Topluluk kanalımız](https://t.me/corenodechat)<br>
 * [Topluluk Twitter](https://twitter.com/corenodeHQ)<br>
 * [Airchain Website](https://www.airchains.io)<br>
 * [Blockchain Explorer](https://testnet.airchains.io)<br>
 * [Discord](https://discord.gg/jsy8ZqrD)<br>
 * [Twitter](https://twitter.com/airchains_io)<br>

### Public RPC

RPC : https://airchains-testnet-rpc.corenode.info/

API : https://airchains-testnet-api.corenode.info/

GRPC : https://airchains-testnet-grpc.corenode.info/

### Explorer

https://explorer.corenodehq.com/Airchains-Testnet.

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
cd $HOME
VER="1.22.2"
wget "https://golang.org/dl/go$VER.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go$VER.linux-amd64.tar.gz"
rm "go$VER.linux-amd64.tar.gz"
[ ! -f ~/.bash_profile ] && touch ~/.bash_profile
echo "export PATH=$PATH:/usr/local/go/bin:~/go/bin" >> ~/.bash_profile
source $HOME/.bash_profile
[ ! -d ~/go/bin ] && mkdir -p ~/go/bin
```
### 🚧Dosyaları çekelim
```
wget https://github.com/airchains-network/junction/releases/download/v0.3.1/junctiond-linux-amd64 
chmod +x junctiond-linux-amd64 
```
```
mkdir -p $HOME/.junction/cosmovisor/genesis/bin
mv $HOME/junctiond-linux-amd64 $HOME/.junction/cosmovisor/genesis/bin/junctiond
```
```
sudo ln -s $HOME/.junction/cosmovisor/genesis $HOME/.junction/cosmovisor/current -f
sudo ln -s $HOME/.junction/cosmovisor/current/bin/junctiond /usr/local/bin/junctiond -f
```
### 🚧Cosmovisor kuralım
```
go install cosmossdk.io/tools/cosmovisor/cmd/cosmovisor@v1.5.0
```
### 🚧Servis oluşturalım
```
sudo tee /etc/systemd/system/junctiond.service > /dev/null << EOF
[Unit]
Description=junction node service
After=network-online.target

[Service]
User=$USER
ExecStart=$(which cosmovisor) run start
Restart=on-failure
RestartSec=10
LimitNOFILE=65535
Environment="DAEMON_HOME=$HOME/.junction"
Environment="DAEMON_NAME=junctiond"
Environment="UNSAFE_SKIP_BACKUP=true"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$HOME/.junction/cosmovisor/current/bin"

[Install]
WantedBy=multi-user.target
EOF
```
### 🚧Etkinleştirelim
```
sudo systemctl daemon-reload
sudo systemctl enable junctiond
```
### 🚧İnit
```
junctiond init node-adi-yaz --chain-id varanasi-1
```
### 🚧Genesis ve addrbook
NOT: gensissen yapma sonra 
```
curl -L /main/addrbook.json > $HOME/.junction/config/addrbook.json
curl -L /main/genesis.json > $HOME/.junction/config/genesis.json
```
### 🚧Port
```
echo "export J_PORT="63"" >> $HOME/.bash_profile
source $HOME/.bash_profile
```
```
sed -i.bak -e "s%:1317%:${J_PORT}317%g;
s%:8080%:${J_PORT}080%g;
s%:9090%:${J_PORT}090%g;
s%:9091%:${J_PORT}091%g;
s%:8545%:${J_PORT}545%g;
s%:8546%:${J_PORT}546%g;
s%:6065%:${J_PORT}065%g" $HOME/.junction/config/app.toml
```
### Port
```
sed -i.bak -e "s%:26658%:${J_PORT}658%g;
s%:26657%:${J_PORT}657%g;
s%:6060%:${J_PORT}060%g;
s%:26656%:${J_PORT}656%g;
s%^external_address = \"\"%external_address = \"$(wget -qO- eth0.me):${J_PORT}656\"%;
s%:26660%:${J_PORT}660%g" $HOME/.junction/config/config.toml
```
### 🚧Seed ve Peer
```
peers=""
sed -i 's|^persistent_peers *=.*|persistent_peers = "'$PEERS'"|' $HOME/.junction/config/config.toml
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"$peers\"/" $HOME/.junction/config/config.toml
seeds="2d1ea4833843cc1433e3c44e69e297f357d2d8bd@5.78.118.106:26656"
sed -i.bak -e "s/^seeds =.*/seeds = \"$seeds\"/" $HOME/.junction/config/config.toml

```

### 🚧Pruning
```
sed -i -e "s/^pruning *=.*/pruning = \"custom\"/" $HOME/.junction/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"100\"/" $HOME/.junction/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"50\"/" $HOME/.junction/config/app.toml
```
### 🚧Gas ve index ayarı
```
sed -i 's|minimum-gas-prices =.*|minimum-gas-prices = "0.025amf"|g' $HOME/.junction/config/app.toml
sed -i -e "s/prometheus = false/prometheus = true/" $HOME/.junction/config/config.toml
sed -i -e "s/^indexer *=.*/indexer = \"null\"/" $HOME/.junction/config/config.toml
```
### Snap 
NOT: genesis sen yapma
```
junctiond tendermint unsafe-reset-all --home $HOME/.junction
curl -L http://37.120.189.81/airchain_testnet/airv_snap.tar.lz4 | tar -I lz4 -xf - -C $HOME/.junction
```
### 🚧Başlatalım
NOT: gensissen yapma
```
sudo systemctl daemon-reload && sudo systemctl start junctiond && sudo journalctl -u junctiond -f --no-hostname -o cat
```
### Log
```
sudo journalctl -u junctiond -f --no-hostname -o cat
```
### Cüzdan olusturma
```
junctiond keys add cüzdan-adi-yaz --keyring-backend os
```
### Cüzdan import
```
junctiond keys add cüzdan-adi-yaz --keyring-backend os --recover
```
### Gentx oluşturma
NOT: genesis seçildiyseniz bunuda yapacanız başka yok başlatma ve genesis ekleme falan sonra olacak.
```
junctiond genesis add-genesis-account <key-name> 100000000000umaf  
junctiond genesis gentx <key-name> 100000000000umaf \  
  --chain-id varanasi-1 \  
  --moniker "" \
  --identity="" \
  --website="" \
  --details="" \
  --security-contact="" \ 
  --commission-rate "0.10" \  
  --commission-max-rate "0.20" \  
  --commission-max-change-rate "0.01" \  
  --min-self-delegation "1" \  
  --pubkey "$(junctiond tendermint show-validator)" \  
  --keyring-backend os 
```
### Validator oluştur
Not: pubkey alalım
```
junctiond comet show-validator
```

```
nano $HOME/validator.json
```
Not: alttaki kodu düzenleyin sonra üsteki kodu yazıp düzenlediğinizi içine yapıstırın. eğer vali kurarken hata alırsanız. size önerdiği kodu tekrar içine yapıstırıp düzenleyin tabi eskilerini silerek :D
```
{
	"pubkey": <validator-pub-key>,
	"amount": "1000000amf",
	"moniker": "<validator-name>",
	"identity": "optional identity signature (ex. UPort or Keybase)",
	"website": "validator's (optional) website",
	"security": "validator's (optional) security contact email",
	"details": "validator's (optional) details",
	"commission-rate": "0.1",
	"commission-max-rate": "0.2",
	"commission-max-change-rate": "0.01",
	"min-self-delegation": "1"
}
```
```
junctiond tx staking create-validator $HOME/validator.json --from cüzdan-adi --chain-id varanasi-1 --fees 5000amf --node http://localhost:63657
```
### Kendinize stake
```
junctiond tx staking delegate $(junctiond keys show cüzdan-adi-yaz --bech val -a) 1000000amf --from cüzdan-adi-yaz --chain-id varanasi-1 --fees 5000amf --node=http://localhost:63657 -y
```
### Jailden çıkma
```
junctiond tx slashing unjail --from cüzdan-adi-yaz --chain-id varanasi-1 --fees 5000amf --node=http://localhost:63657 -y
```







  
