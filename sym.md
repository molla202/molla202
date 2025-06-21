








<h1 align="center"> Symphony </h1>


![image](https://github.com/user-attachments/assets/64839830-41f3-4dd7-b45a-2a52a4cd2641)







 * [Topluluk kanalımız](https://t.me/corenodechat)<br>
 * [Topluluk Twitter](https://twitter.com/corenodeHQ)<br>
 * [Symphony Website](https://orchestralabs.org/)<br>
 * [Blockchain Explorer](https://testnet.ping.pub/symphony)<br>
 * [Discord](https://discord.gg/qEBPwncrSV)<br>
 * [Twitter](https://twitter.com/orchestra_labs)<br>
 * [Faucet](https://testnet.ping.pub/symphony/faucet)<br>

## Pulic RPC

https://symphony-testnet-rpc.corenode.info

https://symphony-testnet-api.corenode.info


## 💻 Sistem Gereksinimleri
| Bileşenler | Minimum Gereksinimler | 
| ------------ | ------------ |
| CPU |	4|
| RAM	| 8+ GB |
| Storage	| 160+ GB SSD |

### 🚧Gerekli kurulumlar
```
sudo apt update && sudo apt upgrade -y
sudo apt install curl git wget htop tmux build-essential jq make lz4 gcc unzip -y
```

### ➡️ Go Installation
```
cd $HOME
VER="1.22.3"
wget "https://golang.org/dl/go$VER.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go$VER.linux-amd64.tar.gz"
rm "go$VER.linux-amd64.tar.gz"
[ ! -f ~/.bash_profile ] && touch ~/.bash_profile
echo "export PATH=$PATH:/usr/local/go/bin:~/go/bin" >> ~/.bash_profile
source $HOME/.bash_profile
[ ! -d ~/go/bin ] && mkdir -p ~/go/bin
```
### 2️⃣ Install node
```
echo "export SYMPHONY_PORT="38"" >> $HOME/.bash_profile
source $HOME/.bash_profile
```
```
cd $HOME
rm -rf symphony
git clone https://github.com/Orchestra-Labs/symphony
cd symphony
git checkout v1.0.0
make build
```
```
mkdir -p $HOME/.symphonyd/cosmovisor/genesis/bin
mv $HOME/symphony/build/symphonyd $HOME/.symphonyd/cosmovisor/genesis/bin/
```
```
sudo ln -s $HOME/.symphonyd/cosmovisor/genesis $HOME/.symphonyd/cosmovisor/current -f
sudo ln -s $HOME/.symphonyd/cosmovisor/current/bin/symphonyd /usr/local/bin/symphonyd -f
```
```
go install cosmossdk.io/tools/cosmovisor/cmd/cosmovisor@v1.6.0
cd
```
### ➡️ Create a service
```
sudo tee /etc/systemd/system/symphonyd.service > /dev/null << EOF
[Unit]
Description=symphony node service
After=network-online.target

[Service]
User=$USER
ExecStart=$(which cosmovisor) run start --home $HOME/.symphonyd
Restart=on-failure
RestartSec=10
LimitNOFILE=65535
Environment="DAEMON_HOME=${HOME}/.symphonyd"
Environment="DAEMON_NAME=symphonyd"
Environment="UNSAFE_SKIP_BACKUP=true"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:~/.symphonyd/cosmovisor/current/bin"

[Install]
WantedBy=multi-user.target
EOF
```
### ➡️ Let's activate it
```
sudo systemctl daemon-reload
sudo systemctl enable symphonyd
```
### ➡️ Initialize the node
```
symphonyd init "NODE-NAME" --chain-id symphony-1
symphonyd config set client chain-id symphony-1
symphonyd config set client keyring-backend os
symphonyd config set client node tcp://localhost:${SYMPHONY_PORT}657
```
### ➡️ Genesis addrbook
```
curl https://raw.githubusercontent.com/Orchestra-Labs/symphony/refs/heads/main/networks/symphony-1/genesis.json -o ~/.symphonyd/config/genesis.json

```
### ➡️ Port
```
sed -i.bak -e "s%:1317%:${SYMPHONY_PORT}317%g;
s%:8080%:${SYMPHONY_PORT}080%g;
s%:9090%:${SYMPHONY_PORT}090%g;
s%:9091%:${SYMPHONY_PORT}091%g;
s%:8545%:${SYMPHONY_PORT}545%g;
s%:8546%:${SYMPHONY_PORT}546%g;
s%:6065%:${SYMPHONY_PORT}065%g" $HOME/.symphonyd/config/app.toml
```
```
sed -i.bak -e "s%:26658%:${SYMPHONY_PORT}658%g;
s%:26657%:${SYMPHONY_PORT}657%g;
s%:6060%:${SYMPHONY_PORT}060%g;
s%:26656%:${SYMPHONY_PORT}656%g;
s%^external_address = \"\"%external_address = \"$(wget -qO- eth0.me):${SYMPHONY_PORT}656\"%;
s%:26660%:${SYMPHONY_PORT}660%g" $HOME/.symphonyd/config/config.toml
```
### ➡️ Peers and Seeds
```
SEEDS=""
PEERS=""
sed -i -e "s/^seeds *=.*/seeds = \"$SEEDS\"/; s/^persistent_peers *=.*/persistent_peers = \"$PEERS\"/" $HOME/.symphonyd/config/config.toml
```
### ➡️ Pruning
```
sed -i -e "s/^pruning *=.*/pruning = \"custom\"/" $HOME/.symphonyd/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"100\"/" $HOME/.symphonyd/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"10\"/" $HOME/.symphonyd/config/app.toml
```
### ➡️ Gas Settings
```
sed -i 's|minimum-gas-prices =.*|minimum-gas-prices = "0note"|g' $HOME/.symphonyd/config/app.toml
```
### ➡️ Prometheus & Indexer
```
sed -i 's|^prometheus *=.*|prometheus = true|' $HOME/.symphonyd/config/config.toml
sed -i -e 's|^indexer *=.*|indexer = "null"|' $HOME/.symphonyd/config/config.toml
```
### ➡️ Starter Snap (soon)
```


```
### ➡️ Let's get started
NOT: BAŞLATMAYIN GENTXCİLER
```
sudo systemctl start symphonyd && sudo journalctl -u symphonyd -f -o cat
```
### ➡️ Log Command
```
journalctl -u symphonyd -f -o cat
```
### ➡️ Create wallet
```
symphonyd keys add wallet-name
```
### ➡️ Import wallet
```
symphonyd keys add wallet-name --recover
```
NOT: CÜZDANDA OLUŞTURDUNUZ MUMKUNSE TESTEKİNİ İMPORT ETTİNİZ. ALTTAKİ VALİ OLUSTURMA YOK GENTXDEN DEVAM
### ➡️ Create Validator
❗️100000note = 0.1 MLD❗️
NOT: pubkey alıp json içindekine yazıcaz düzenlemelerinizi yapın.
```
cd $HOME
```
```
symphonyd tendermint show-validator
```
```
rm -rf /root/validator.json
```
```
nano /root/validator.json
```
```
{
  "pubkey": {"@type":"/cosmos.crypto.ed25519.PubKey.......},
  "amount": "1000000note",
  "moniker": "",
  "identity": "",
  "website": "",
  "security": "",
  "details": "",
  "commission-rate": "0.1",
  "commission-max-rate": "0.2",
  "commission-max-change-rate": "0.01",
  "min-self-delegation": "1"
}
```
```
symphonyd tx staking create-validator $HOME/validator.json \
--from=wallet-name \
--chain-id=symphony-1 \
--gas-adjustment 1.5 \
--gas-prices 0.025note \
--gas auto
-y
```
### ➡️ Delegate to Yourself
```
symphonyd tx staking delegate $(symphonyd keys show wallet-name --bech val -a) amount0000note \
--chain-id symphony-1 \
--from "wallet-name" \
--fees "800note" \
--node=http://localhost:${SYMPHONY_PORT}657 \
-y
```
### ➡️ Edit Validator
```
symphonyd tx staking edit-validator \
--chain-id symphony-1 \
--commission-rate 0.05 \
--new-moniker "validator-name" \
--identity "" \
--details "" \
--website "" \
--security-contact "" \
--from "wallet-name" \
--node http://localhost:${SYMPHONY_PORT}657 \
--fees "800note" \
-y
```
### ➡️ Complete deletion
```
cd $HOME
sudo systemctl stop symphonyd
sudo systemctl disable symphonyd
sudo rm -rf /etc/systemd/system/symphonyd.service
sudo systemctl daemon-reload
sudo rm -f /usr/local/bin/symphonyd
sudo rm -f $(which symphonyd)
sudo rm -rf $HOME/.symphonyd $HOME/symphony
sed -i "/SYMPHONY_/d" $HOME/.bash_profile
```


### GENTX
Not : wallet adınızı farklı yaptıysanız ona göre ayarlayın. kendi genesislerinde zaten test cüzdanalrımız 2 bakiye ile eklenmiş 1 bakiye ile olusturucaz.
```
symphonyd gentx wallet 1000000note --chain-id symphony-1 \
  --moniker "" \
  --identity="" \
  --website="" \
  --details="" \
  --security-contact="" \
  --commission-rate "0.10" \
  --commission-max-rate "0.20" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1" \
  --pubkey "$(symphonyd tendermint show-validator)"
```

### PR atma

https://github.com/Orchestra-Labs/symphony

- forklayın ve gentx dosyanızı networks/symphony-1/gentxs/   içersine atın kendi forkunuzdaki sizdegentxs dosyası yoktur. 

![image](https://github.com/user-attachments/assets/98df5738-bfb5-4d0d-9927-1af6b7d89beb)


- create new file deyin dosya yoluna gentxs/adınız.json ekleyip gentx içeriğinizi içine kopyalayıp kaydedin. zaten / koyunca adınız.json girince anlayacaksınız gerisi next next.

![image](https://github.com/user-attachments/assets/46d7df00-6758-4572-861e-2750fd97fa75)
