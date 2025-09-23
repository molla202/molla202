


  

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
git checkout v0.7.0-rc5
```
```
just wardend
```
//////////////////////////////
```
cd
wget wget https://github.com/warden-protocol/wardenprotocol/releases/download/v0.7.0-rc5/wardend-v0.7.0-rc5-linux-amd64
chmod +x wardend-v0.7.0-rc5-linux-amd64
```
```
mkdir -p $HOME/.warden/cosmovisor/genesis/bin/
mv $HOME/wardend-v0.7.0-rc5-linux-amd64 $HOME/.warden/cosmovisor/genesis/bin/wardend
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
wardend init "isim-yaz" --chain-id testlaunch_123123-1
```
### 🚧 Genesis addrbook
```
wget -O $HOME/.warden/config/genesis.json "https://raw.githubusercontent.com/warden-protocol/networks/refs/heads/main/mainnet/init_genesis.json"
```
### Ayarlar.
```
sed -i.bak 's|^\s*evm-chain-id\s*=.*|evm-chain-id = 123123-1|' $HOME/.warden/config/app.toml
sed -i.bak 's|^\s*chain-id\s*=.*|chain-id = "testlaunch_123123-1"|' $HOME/.warden/config/client.toml
sed -i.bak 's|^\s*seeds\s*=.*|seeds = ""|' $HOME/.warden/config/config.toml
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
SEEDS=""
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
    \"amount\": \"900000000000000000award\",
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
    --chain-id testlaunch_123123-1 \
    --gas auto --gas-adjustment 1.6 --fees 250000000000000award \
    --node=http://localhost:11957
```


### Delege 
```
wardend tx staking delegate valoper-adresi miktar000000000000000000award \
--chain-id testlaunch_123123-1 \
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
wardend genesis gentx wallet 900000000000000000award --chain-id testlaunch_123123-1 \
  --moniker "" \
  --identity="" \
  --website="" \
  --details="" \
  --security-contact="" \
  --commission-rate "0.10" \
  --commission-max-rate "0.20" \
  --commission-max-change-rate "0.01" \
  --min-self-delegation "1" \
  --pubkey "$(wardend comet show-validator)"
```
```
