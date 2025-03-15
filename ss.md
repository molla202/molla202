
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
mkdir -p $HOME/.junctiond/cosmovisor/genesis/bin
mv $HOME/junctiond-linux-amd64 $HOME/.junctiond/cosmovisor/genesis/bin/junctiond
```
```
sudo ln -s $HOME/.junctiond/cosmovisor/genesis $HOME/.junctiond/cosmovisor/current -f
sudo ln -s $HOME/.junctiond/cosmovisor/current/bin/junctiond /usr/local/bin/junctiond -f
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
Environment="DAEMON_HOME=$HOME/.junctiond"
Environment="DAEMON_NAME=junctiond"
Environment="UNSAFE_SKIP_BACKUP=true"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$HOME/.junctiond/cosmovisor/current/bin"

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
NOT: node adını yaz
```
junctiond init node-adi-yaz --chain-id varanasi-1
```
### 🚧Genesis ve addrbook
NOT: gensissen yapma sonra 
```
curl -L /main/addrbook.json > $HOME/.junctiond/config/addrbook.json
curl -L /main/genesis.json > $HOME/.junctiond/config/genesis.json
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
s%:6065%:${J_PORT}065%g" $HOME/.junctiond/config/app.toml
```
### Port
```
sed -i.bak -e "s%:26658%:${J_PORT}658%g;
s%:26657%:${J_PORT}657%g;
s%:6060%:${J_PORT}060%g;
s%:26656%:${J_PORT}656%g;
s%^external_address = \"\"%external_address = \"$(wget -qO- eth0.me):${J_PORT}656\"%;
s%:26660%:${J_PORT}660%g" $HOME/.junctiond/config/config.toml
```
### 🚧Seed ve Peer
NOT: genesissen yapma
```
peers=""
sed -i 's|^persistent_peers *=.*|persistent_peers = "'$PEERS'"|' $HOME/.junctiond/config/config.toml
sed -i.bak -e "s/^persistent_peers *=.*/persistent_peers = \"$peers\"/" $HOME/.junctiond/config/config.toml
seeds=""
sed -i.bak -e "s/^seeds =.*/seeds = \"$seeds\"/" $HOME/.junctiond/config/config.toml

```

### 🚧Pruning
```
sed -i -e "s/^pruning *=.*/pruning = \"custom\"/" $HOME/.junctiond/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"100\"/" $HOME/.junctiond/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"50\"/" $HOME/.junctiond/config/app.toml
```
### 🚧Gas ve index ayarı
```
sed -i 's|minimum-gas-prices =.*|minimum-gas-prices = "0.025umaf"|g' $HOME/.junctiond/config/app.toml
sed -i -e "s/prometheus = false/prometheus = true/" $HOME/.junctiond/config/config.toml
sed -i -e "s/^indexer *=.*/indexer = \"null\"/" $HOME/.junctiond/config/config.toml
```
### Snap 
NOT: genesis sen yapma
```
junctiond tendermint unsafe-reset-all --home $HOME/.junctiond
curl -L http://37.120.189.81/airchain_testnet/airv_snap.tar.lz4 | tar -I lz4 -xf - -C $HOME/.junctiond
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
junctiond keys add wallet --keyring-backend os
```
### Cüzdan import
```
junctiond keys add wallet --keyring-backend os --recover
```
### Gentx oluşturma
NOT: genesis seçildiyseniz bunuda yapacanız başka yok başlatma ve genesis ekleme falan sonra olacak. yane bunuda yaptıktan sonra en alttaki ayrı kısımda pr atılışı yazıyor.
```
junctiond genesis add-genesis-account wallet 100000000000umaf  
junctiond genesis gentx wallet 100000000000umaf \  
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



### Genesis PR

- gentx işlemini yapınca dosya yolunu zaten gösteriyor ordan alıp pcnize çekin

![image](https://github.com/user-attachments/assets/c721bbb9-69e1-4d71-8530-5ee1bc11c78b)

- sonra forklayalım bu repoyu https://github.com/Core-Node-Team/junction-resources/tree/main

- sonra klasöre girelim ve upload seçip gentx dosyamızı atalım

![image](https://github.com/user-attachments/assets/db48a747-3e75-4221-82c1-904ec69ef428)

![image](https://github.com/user-attachments/assets/9230bcc6-b2c0-4fac-8b10-579e551b40a7)

![image](https://github.com/user-attachments/assets/4592221d-638b-4ef0-8506-ca0e923cf5c3)

- tut çerçeve içine gentx dosyasını at commit de yuklesin

![image](https://github.com/user-attachments/assets/1dcac528-095a-4e30-9cd1-fa5f275274ac)

- pull request diyelim.

![image](https://github.com/user-attachments/assets/77b8642b-f78b-4ebe-b039-d146ade6c87c)

![image](https://github.com/user-attachments/assets/63bd025f-450a-4117-b64d-ba2fd9951a49)

![image](https://github.com/user-attachments/assets/f7e72ad3-79f5-4294-be3c-c00372f5fc5e)

![image](https://github.com/user-attachments/assets/090d84a4-2e02-499d-a66e-efb4d6728d29)

![image](https://github.com/user-attachments/assets/c591bde4-5e42-4415-a193-091982e8f359)

![image](https://github.com/user-attachments/assets/42435785-ad1b-40eb-9694-d4aa653948ed)

- tamasın hayırlısı olsun. bundan sonra yayınlanacak genesis dosyasını ekleyip başlatmak kalıyor. hersey hazır olsun diye kurulum şeklide yaptık. zira öbür türlü kurmaklada uğraşmayalım kafa karışmasın.

























  
