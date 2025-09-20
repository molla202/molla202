


  

<h1 align="center"> Warden Protocol </h1>


![image](https://github.com/molla202/Warden-Protocol/assets/91562185/32f62d0a-d2b1-4dfa-9b6a-60395461025f)



> Unlock the Potential of Intent-Based, Secure Cross-Chain Interactions



 * [Topluluk kanalımız](https://t.me/corenodechat)<br>
 * [Topluluk Twitter](https://twitter.com/corenodeHQ)<br>
 * [Warden Website](https://wardenprotocol.org/)<br>
 * [Blockchain Explorer](https://explorer.corenodehq.com/Warden%20Testnet)<br>
 * [Discord](https://discord.gg/7rzkxXRK)<br>
 * [Twitter](https://twitter.com/wardenprotocol)<br>

## 💻 Sistem Gereksinimleri
| Bileşenler | Minimum Gereksinimler | 
| ------------ | ------------ |
| CPU |	6|
| RAM	| 16+ GB |
| Storage	| 400 GB SSD |

### 🚧Gerekli kurulumlar
```
sudo apt update && sudo apt upgrade -y
sudo apt install curl git wget htop tmux build-essential jq make lz4 gcc unzip -y
```

### 🚧 Go kurulumu
```
cd $HOME
VER="1.23.0"
wget "https://golang.org/dl/go$VER.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go$VER.linux-amd64.tar.gz"
rm "go$VER.linux-amd64.tar.gz"
[ ! -f ~/.bash_profile ] && touch ~/.bash_profile
echo "export PATH=$PATH:/usr/local/go/bin:~/go/bin" >> ~/.bash_profile
source $HOME/.bash_profile
[ ! -d ~/go/bin ] && mkdir -p ~/go/bin
```

### 🚧 Dosyaları çekelim ve kuralım

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```
```
cargo install just
```
```
git clone https://github.com/warden-protocol/wardenprotocol.git
cd wardenprotocol
git checkout v0.7.0-rc3
```
```
just wardend
```
```
mkdir -p $HOME/.warden/cosmovisor/genesis/bin/
mv $HOME/wardenprotocol/build/wardend $HOME/.warden/cosmovisor/genesis/bin/
```
```
sudo ln -s $HOME/.warden/cosmovisor/genesis $HOME/.warden/cosmovisor/current -f
sudo ln -s $HOME/.warden/cosmovisor/current/bin/wardend /usr/local/bin/wardend -f
```
```
go install cosmossdk.io/tools/cosmovisor/cmd/cosmovisor@v1.6.0
```
### 🚧 Servis oluşturalım
```
sudo tee /etc/systemd/system/wardend.service > /dev/null << EOF
[Unit]
Description=warden node service
After=network-online.target

[Service]
User=$USER
ExecStart=$(which cosmovisor) run start
Restart=on-failure
RestartSec=10
LimitNOFILE=65535
Environment="DAEMON_HOME=$HOME/.warden"
Environment="DAEMON_NAME=wardend"
Environment="UNSAFE_SKIP_BACKUP=true"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$HOME/.warden/cosmovisor/current/bin"

[Install]
WantedBy=multi-user.target
EOF
```
```
sudo systemctl daemon-reload
sudo systemctl enable wardend
```
### 🚧 İnit
```
wardend init "isim-yaz" --chain-id mainnet
```
### 🚧 Genesis addrbook
```
wget -O $HOME/.warden/config/genesis.json "https://raw.githubusercontent.com/warden-protocol/networks/main/testnets/barra/genesis.json"
```
### Ayarlar.
```
sed -i.bak 's|^\s*evm-chain-id\s*=.*|evm-chain-id = 9191|' $HOME/.warden/config/app.toml
sed -i.bak 's|^\s*chain-id\s*=.*|chain-id = "barra_9191-1"|' $HOME/.warden/config/client.toml
sed -i.bak 's|^\s*seeds\s*=.*|seeds = "c489c003b7c72298840bd4411ffc98ce13e07c27@54.194.136.183:26656,4564c91423a923eaba7982e69e33aec6185d362f@54.72.5.234:26656"|' $HOME/.warden/config/config.toml
sed -i.bak 's|^\s*timeout_propose\s*=.*|timeout_propose = "1s"|' $HOME/.warden/config/config.toml
sed -i.bak 's|^\s*timeout_propose_delta\s*=.*|timeout_propose_delta = "200ms"|' $HOME/.warden/config/config.toml
sed -i.bak 's|^\s*timeout_prevote\s*=.*|timeout_prevote = "500ms"|' $HOME/.warden/config/config.toml
sed -i.bak 's|^\s*timeout_prevote_delta\s*=.*|timeout_prevote_delta = "200ms"|' $HOME/.warden/config/config.toml
sed -i.bak 's|^\s*timeout_precommit\s*=.*|timeout_precommit = "500ms"|' $HOME/.warden/config/config.toml
sed -i.bak 's|^\s*timeout_precommit_delta\s*=.*|timeout_precommit_delta = "200ms"|' $HOME/.warden/config/config.toml
sed -i.bak 's|^\s*timeout_commit\s*=.*|timeout_commit = "2s"|' $HOME/.warden/config/config.toml
sed -i.bak 's|^\s*create_empty_blocks\s*=.*|create_empty_blocks = true|' $HOME/.warden/config/config.toml
```
### 🚧 Gas ayarı
```
sed -i 's|minimum-gas-prices =.*|minimum-gas-prices = "10award"|g' $HOME/.warden/config/app.toml
```
### 🚧 Peer
```
SEEDS="c489c003b7c72298840bd4411ffc98ce13e07c27@54.194.136.183:26656,4564c91423a923eaba7982e69e33aec6185d362f@54.72.5.234:26656"
PEERS="6ac41e45f21c43edc92f836be96cae60438f6960@136.243.74.81:18656,d301d25b48ebebd1257d4944e31c3a9f11835f39@152.53.137.213:29656,a416f0a5a925a3cd40ceb166aeab43e71748c1dc@95.217.109.206:11956,baf98d88fdb1f6e8df1455fa04179aecdef7223a@23.88.5.169:10056,ea1aff097b9078b4b4d343b65dadd4eac6c57dc6@152.53.33.174:26656,30b1384f9f4ae8a1644dabb92ad4715a8b155404@51.79.78.121:26656,abd2849ba845fa044bf4756e6f03c55699f41e13@65.109.111.234:18656,7345881034f09a7b6e621bed6f803168139a9a62@167.235.14.83:13656,0d3f078c6bdf2c4791a844df2fa5b932cd83c1c7@65.109.69.119:18656,da8ea8a131db1c9ade0b9e1089adfd9330e3246f@65.109.78.246:22656,92bf4175907fe1348820595c2c01db411304ec62@135.181.59.112:12756,837d8748b4d5f6bd21f58a87fb5c5bcf9d60d0c7@65.108.121.227:13556,ff37394693e96769342c1710c46704293c109c61@46.4.91.76:32056,26998b58d8d411ddd3476787463d40ef0d4d8c2f@65.21.135.111:11656,9dd2caead4b41af780256da0c2282a0c84c8d7fa@193.26.157.178:18656,4564c91423a923eaba7982e69e33aec6185d362f@3.252.37.24:26656,cd51069eec220d84765b2c18ca08c463b503e607@152.53.104.182:22656,3184c3a25d51a249bebd1b837e05a223c90b65b7@65.109.117.219:18656,84376de171068c766d55f4cbc6dc9c5ddbfbd367@45.9.63.55:18656,b64af8e179c391423fff2b3596ab34ecbe21921e@152.53.151.154:18656,4efbc056eeefdb3d07c51a056af63d2b16426375@148.72.141.64:26652,85807889c06713452d5a330f7660bbf3106aa598@152.53.136.97:18656,4e451a841ff2c74d2a9ed77f87f7e633d89fd991@213.136.73.245:41656,9ced90025b0f4c47373c677bce12d96116b49355@65.108.111.225:60856,125f67a29e96c7c7fb6fbc7e6914207c2099f5f4@92.145.5.211:41656,77b1370e4c14496f44d9893e5b74ba5efba14d6b@162.55.224.194:26656,6089ea41e8003ebf81e22f1f78d7558c5e20b302@144.76.29.90:61256,f8fd5c186c01f568b3620d3554d0235b81770339@185.233.107.75:18656,6f1ba284e755d26ba3a28631ec6fb1d0c2e44847@152.53.138.77:18656,130ecc3bd7dcd99d0daa9216f760c5f804872ffc@167.235.178.134:27356,fb3c995373c0feee597dd3ed32e56cb5e0f0d1c2@65.108.120.161:26726,4f0c7c817e1a964a04b8bb490050669909fd2153@135.181.232.241:64656,9c7564f341a9ac63217b7bc8f1de65cbecb09f55@188.40.66.173:27356,7b4a217429f859deacdbe725f4fd6bdf989db5e0@193.203.15.135:26656,73e12eaef3fda57d881e49c22cf01902f86e7299@65.109.35.107:18656,e0ac809671933ee5c88da4f91446a3d0e811cdf2@147.93.157.69:18656"
sed -i -e "/^\[p2p\]/,/^\[/{s/^[[:space:]]*seeds *=.*/seeds = \"$SEEDS\"/}" \
       -e "/^\[p2p\]/,/^\[/{s/^[[:space:]]*persistent_peers *=.*/persistent_peers = \"$PEERS\"/}" $HOME/.warden/config/config.toml
```
### config pruning
```
sed -i -e "s/^pruning *=.*/pruning = \"custom\"/" $HOME/.warden/config/app.toml
sed -i -e "s/^pruning-keep-recent *=.*/pruning-keep-recent = \"100\"/" $HOME/.warden/config/app.toml
sed -i -e "s/^pruning-interval *=.*/pruning-interval = \"10\"/" $HOME/.warden/config/app.toml
```
### 🚧 Snap
```
wardend tendermint unsafe-reset-all --home $HOME/.warden
if curl -s --head curl http://37.120.189.81/warden_chi_testnet/warden_snap.tar.lz4 | head -n 1 | grep "200" > /dev/null; then
  curl http://37.120.189.81/warden_chi_testnet/warden_snap.tar.lz4 | lz4 -dc - | tar -xf - -C $HOME/.warden
    else
  echo no have snap
fi
```

### 🚧 Port ayarı
```
echo "export WARDEN_PORT="19"" >> $HOME/.bash_profile
source $HOME/.bash_profile
```
```
sed -i.bak -e "s%:1317%:${WARDEN_PORT}317%g;
s%:8080%:${WARDEN_PORT}080%g;
s%:9090%:${WARDEN_PORT}090%g;
s%:9091%:${WARDEN_PORT}091%g;
s%:8545%:${WARDEN_PORT}545%g;
s%:8546%:${WARDEN_PORT}546%g;
s%:6065%:${WARDEN_PORT}065%g" $HOME/.warden/config/app.toml
```
```
sed -i.bak -e "s%:26658%:${WARDEN_PORT}658%g;
s%:26657%:${WARDEN_PORT}657%g;
s%:6060%:${WARDEN_PORT}060%g;
s%:26656%:${WARDEN_PORT}656%g;
s%^external_address = \"\"%external_address = \"$(wget -qO- eth0.me):${WARDEN_PORT}656\"%;
s%:26660%:${WARDEN_PORT}660%g" $HOME/.warden/config/config.toml
```
```
sed -i -e "s|^node *=.*|node = \"tcp://localhost:${WARDEN_PORT}657\"|" $HOME/.warden/config/client.toml
```
### 🚧 Başlatalım
```
sudo systemctl restart wardend
journalctl -fu wardend -o cat
```


### 🚧 Cüzdan olusturalım
```
wardend keys add cüzdan-adi
```
### 🚧 Cüzdan import
```
wardend keys add cüzdan-adi --recover
```
### 🚧 Validator Olusturma
NOT: Faucet adresi : https://faucet.chiado.wardenprotocol.org/
Not: altaki kodla pubkey öğren
```
wardend tendermint show-validator
```
Not: öğrendiğin pubkeyi aşağıda nano ile içine akataracağın yere yazıcan
```
nano /root/validator.json
```
NOT: baska bele validator olusturmalı proje kuruluysa içi dolu olabilir. önemli değil zaten bikere kullanıyoruz sil bastan ekle yok sa zaten içi boş
```
{
        "pubkey": pubyaz,
        "amount": "1000000000000000000award",
        "moniker": "myvalidator",
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
Not: ctrl xy enter kaydet çık.
### Validator olusturucaz ama eşleşmesini beklemeniz gerek....
```
wardend tx staking create-validator /root/validator.json \
    --from=cüzdan-adi \
    --chain-id=barra_9191-1 \
    --gas auto --gas-adjustment 1.6 --fees 250000000000000award \
    --node=http://localhost:11957
```
### oto validator olusturma yukardaki ile yapamadıysız deneyin
```
cd $HOME
```
# Create validator.json file
```
echo ""{\"pubkey\":{\"@type\":\"/cosmos.crypto.ed25519.PubKey\",\"key\":\"$(wardend tendermint show-validator | grep -Po '\"key\":\s*\"\K[^"]*')\"},
    \"amount\": \"1000000000000000000award\",
    \"moniker\": \"nodeismin\",
    \"identity\": \"keybasecode\",
    \"website\": \"\",
    \"security\": \"\",
    \"details\": \"details\",
    \"commission-rate\": \"0.1\",
    \"commission-max-rate\": \"0.2\",
    \"commission-max-change-rate\": \"0.01\",
    \"min-self-delegation\": \"1\"
}" > validator.json
```
# Create a validator using the JSON configuration
```
wardend tx staking create-validator validator.json \
    --from cuzdanismin \
    --chain-id barra_9191-1 \
    --gas auto --gas-adjustment 1.6 --fees 250000000000000award \
    --node=http://localhost:11957
```


### Delege 
```
wardend tx staking delegate valoper-adresi miktar000000000000000000award \
--chain-id barra_9191-1 \
--from "cüzdan-adi" \
--gas auto --gas-adjustment 1.6 --fees 250000000000000award \
--node=http://localhost:11957
```

### Komple Silme
```
sudo systemctl stop wardend
sudo systemctl disable wardend
sudo rm -rf /etc/systemd/system/wardend.service
sudo rm $(which wardend)
sudo rm -rf $HOME/.warden
sed -i "/WARDEN_/d" $HOME/.bash_profile
```

### Gentx işlemleri
```
wardend keys add wallet
```
### Cüzdan import
```
wardend keys add wallet --recover
```
### Gentx oluşturma
```
wardend genesis add-genesis-account wallet 1000000000000000000award
```
```
wardend genesis gentx wallet 1000000000000000000award --chain-id mainnet \
  --moniker "" \
  --identity="" \
  --website="" \
  --details="" \
  --security-contact="" \
  --commission-rate "0.10" \
  --commission-max-rate "0.20" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1" \
  --pubkey "$(wardend tendermint show-validator)"
```
```
