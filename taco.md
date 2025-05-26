



🔥 [CoreNode Telegram](https://t.me/corenode)

🔥 [CoreNode Twitter](https://twitter.com/corenodehq)

💬 [Gökhan Molla Twitter](https://twitter.com/gokhan_molla)

💬 [Gökhan Molla Telegram](https://t.me/gokhan_molla)

💬 Sorularınız için yukarıdaki adreslerden ulaşabilirsiniz.


Faucet: https://spb.faucet.tac.build/


 ## 💻 Sistem Gereksinimleri
| Bileşenler | Minimum Gereksinimler | 
| ------------ | ------------ |
| ✔️ CPU |	8+ |
| ✔️ RAM	| 16+ GB |
| ✔️ Storage	| 500GB+ SSD |


### 🚧Update
```
sudo apt -q update
sudo apt -qy install curl git jq lz4 build-essential
sudo apt -qy upgrade
```
### 🚧Go
```
go :D
```




### 🚧Dosyaları çekıyoruz
```
cd $HOME
git clone https://github.com/TacBuild/tacchain.git
cd tacchain
git checkout v0.0.8
```
```
make build
```
### 🚧Cosmovisor ayarlıyoruz
```
mkdir -p $HOME/.tacchaind/cosmovisor/genesis/bin
mv bin/sourced $HOME/.tacchaind/cosmovisor/genesis/bin/
rm -rf build
```
### 🚧Sistem kısayolları
```
sudo ln -s $HOME/.tacchaind/cosmovisor/genesis $HOME/.tacchaind/cosmovisor/current -f
sudo ln -s $HOME/.tacchaind/cosmovisor/current/bin/tacchaind /usr/local/bin/tacchaind -f
```

### 🚧Cosmovisor kuruyoruz
```
go install cosmossdk.io/tools/cosmovisor/cmd/cosmovisor@v1.5.0
```
### 🚧Servis olusturuyoruz
```
sudo tee /etc/systemd/system/tacchaind.service > /dev/null << EOF
[Unit]
Description=tacchaind node service
After=network-online.target

[Service]
User=$USER
ExecStart=$(which cosmovisor) run start
Restart=on-failure
RestartSec=10
LimitNOFILE=65535
Environment="DAEMON_HOME=$HOME/.tacchaind"
Environment="DAEMON_NAME=tacchaind"
Environment="UNSAFE_SKIP_BACKUP=true"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$HOME/.tacchaind/cosmovisor/current/bin"

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable tacchaind.service
```

### 🚧Node ayarları
```
tacchaind config chain-id source-1
tacchaind config keyring-backend file
tacchaind config node tcp://localhost:12857
```
### 🚧Node kuruyoruz
```
tacchaind init node-adınız --chain-id tacchain_2391-1
```
### 🚧indiriyoruz genesis ved addrbook
```
curl -Ls https://raw.githubusercontent.com/TacBuild/tacchain/refs/heads/main/networks/tacchain_2391-1/genesis.json > $HOME/.tacchaind/config/genesis.json
```
### 🚧Seed gas puring ayarları
```
SEEDS=""
PEERS="9c32b3b959a2427bd2aa064f8c9a8efebdad4c23@206.217.210.164:45130,04a2152eed9f73dc44779387a870ea6480c41fe7@206.217.210.164:45140,5aaaf8140262d7416ac53abe4e0bd13b0f582168@23.92.177.41:45110,ddb3e8b8f4d051e914686302dafc2a73adf9b0d2@23.92.177.41:45120"
sed -i -e "/^\[p2p\]/,/^\[/{s/^[[:space:]]*seeds *=.*/seeds = \"$SEEDS\"/}" \
       -e "/^\[p2p\]/,/^\[/{s/^[[:space:]]*persistent_peers *=.*/persistent_peers = \"$PEERS\"/}" $HOME/.tacchaind/config/config.toml


sed -i \
  -e 's|^pruning *=.*|pruning = "custom"|' \
  -e 's|^pruning-keep-recent *=.*|pruning-keep-recent = "100"|' \
  -e 's|^pruning-keep-every *=.*|pruning-keep-every = "0"|' \
  -e 's|^pruning-interval *=.*|pruning-interval = "19"|' \
  $HOME/.tacchaind/config/app.toml
```
### 🚧Port değiştiriyoruz
```
echo "export TAC_PORT="59"" >> $HOME/.bash_profile
source $HOME/.bash_profile

sed -i.bak -e "s%:1317%:${TAC_PORT}317%g;
s%:8080%:${TAC_PORT}080%g;
s%:9090%:${TAC_PORT}090%g;
s%:9091%:${TAC_PORT}091%g;
s%:8545%:${TAC_PORT}545%g;
s%:8546%:${TAC_PORT}546%g;
s%:6065%:${TAC_PORT}065%g" $HOME/.tacchaind/config/app.toml

sed -i.bak -e "s%:26658%:${TAC_PORT}658%g;
s%:26657%:${TAC_PORT}657%g;
s%:6060%:${TAC_PORT}060%g;
s%:26656%:${TAC_PORT}656%g;
s%^external_address = \"\"%external_address = \"$(wget -qO- eth0.me):${TAC_PORT}656\"%;
s%:26660%:${TAC_PORT}660%g" $HOME/.tacchaind/config/config.toml
```
### 🚧Snap
```
soon
```
### 🚧Başlatıyoruz...
```
sudo systemctl restart tacchaind.service && sudo journalctl -u tacchaind.service -f --no-hostname -o cat
```
