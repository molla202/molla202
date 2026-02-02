<h1 align="center"> RAI


</h1>

<img width="939" height="714" alt="image" src="https://github.com/user-attachments/assets/65d091ad-2604-44eb-aae0-f59fe63309f5" />




 * [Topluluk kanalımız](https://t.me/corenodechat)<br>
 * [Topluluk Twitter](https://twitter.com/corenodeHQ)<br>


```
EVM ağı ekleyin

Network Name: Republic Testnet
RPC URL: https://evm-rpc.republicai.io
Chain ID: 77701
Currency Symbol: RAI
Block Explorer URL: https://explorer.republicai.io
```

## 💻 Sistem Gereksinimleri
| Bileşenler | Minimum Gereksinimler | 
| ------------ | ------------ |
| CPU |	4|
| RAM	| 8+ GB |
| Storage	| 400 GB SSD |

**//////UBUNTU 24//////**


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
ExecStart=$(which cosmovisor) run start --home $HOME/.republicd --chain-id raitestnet_77701-1
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
### Giblic ayar
```
cd $HOME
wget -O glibc-2.39-ubuntu24.tar.gz https://raw.githubusercontent.com/coinsspor/coinsspor/main/glibc-2.39-ubuntu24.tar.gz
tar -xzvf glibc-2.39-ubuntu24.tar.gz
```
```
sudo mkdir -p /opt/glibc-2.39/lib
sudo mv glibc-transfer/* /opt/glibc-2.39/lib/
```
```
REP_PATH=$(which republicd)
```
```
patchelf --set-interpreter /opt/glibc-2.39/lib/ld-linux-x86-64.so.2 --set-rpath /opt/glibc-2.39/lib $REP_PATH
```
### 🚧İnit
```
republicd init "MONIKER" --chain-id raitestnet_77701-1 --home $HOME/.republicd
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
PEERS="20a9721219f5056eacf89c19fd60c1999b398ea3@65.21.88.99:18656,bd892704441b02388b0527a0d15e40fee89b05b9@159.195.26.108:18656,e281dc6e4ebf5e32fb7e6c4a111c06f02a1d4d62@3.92.139.74:26656,dc254b98cebd6383ed8cf2e766557e3d240100a9@54.227.57.160:26656,08de17e0a650192861a6dd2ef63bbaca73f73592@34.55.100.110:26656,f4435ef54602a368802f662a5a6a2b7b923f7071@103.171.146.57:26656,cfb2cb90a241f7e1c076a43954f0ee6d42794d04@54.173.6.183:26656,1999732342c6c89de4112f82008766bf3342aba2@104.152.210.127:55856,93d1e37cf97435491aaca98e04e18d2f6df99192@103.138.70.189:26656,d97efec4de6bcfa2c81052c0e7ebeff2a37655ea@34.51.40.253:26656,525ad7484153172c199433ed8ac7af26c2b228bc@14.169.16.64:26656,6dd3a10b5157d2ac68bd76922de849244ea1f4fa@65.109.55.116:34656,bce8776b32c57d97acfcbe2ec80808acbeae6409@54.71.14.217:26656,2c9641378e9dacc49b269b0efb807b475d033e56@89.167.15.180:26656,194d200f41374b508bd79c062b29c75937c37103@38.49.209.147:26656,a698525f90433d6069a2fcc22b2b3f1cc13593cc@192.99.54.87:26656,6ab1b623e0c1a0f2d3099cc502d9f3b4f9bc8a73@95.216.102.220:13356,cc13360aec4a5ef532fce577f70bbc8fd665c211@65.108.110.246:26656,a5b245a4734167c9377ce3f7828947240cc7fd60@154.12.117.35:23656,ec9cbd29992dea64e8adb26af1ebc5cc6a958875@34.44.164.13:26656,d1a6a7cfbd80805d486e12560ba3af6d868f108a@72.61.158.34:26656,65cf55232924bebfdd02c32446df5a101188a05e@161.97.95.86:26656,cc2504dd639c01038444b309f4549139a43b77d3@206.168.81.49:26656,31e30d2dd6d10933c5a7281f7dffeb09d93fdf12@154.12.116.93:26656,f6d854d1b5d3cc3cc73fb46fbfe53e0df1c05d02@154.12.118.215:26656,e2e2e02d42860e421294485740b48baf9e3e0b0b@179.43.150.242:26656,233fde2cfd5d8f87c15a2bf6ac0b19697e53897e@107.222.215.224:26656,f990e33b674c0e91dc74e1067785bfe493985a34@182.9.2.84:26656,b9f252664aad3370c4e186409c1fda71505a43b7@152.53.251.43:13356,0f81a50876840f3aabb63afb39c27b199fc226c5@147.93.18.162:13356,9ab906725d5a7f6eb513b4f0cbbe7ca357ebceea@213.109.161.44:26656,5b4af65c46e97cf8ee991f07dca1f02d55cb2256@82.112.237.186:26656,ea12408721fd0ed1865021add1f4789988783643@2.56.97.139:13356,d8798195b453a24b7d31b8075ac46de93267e6ea@2.50.222.30:26656,bd4394f8de7fa34c5223d1f65ad3460a7fb40458@14.187.123.136:56656,7971d6669264775653766efcbcb87f8e9664faa6@192.151.150.34:13356,8daac380638c9be321b2ab28a56cb6ab3f48d696@149.50.110.9:26656,70f278d4b63f029a80c2f5fbd5953044f96b9909@152.53.254.226:43656,d5401bc2fe46760e06f5c3af62b57463d83f90ad@89.167.26.162:26656,d5f910e658965da487e5537eac6a382f807e6a03@154.12.118.123:26756,462fd3cf9880438ac732f221bc271b22a0ce7132@172.104.155.28:26656,d42950d61ff958d9f3a12549ef7a535b10357ce4@38.49.212.156:26656,2a939e0322783f1b85a16cf768091c79430457f1@138.197.115.112:26656,b97f371120741a76abc21baea936659f9204f8b1@146.19.24.206:43656,007ee0fafbad23ec7e132a708281bdbdb7d89350@69.62.113.85:26656,802eb4f06de829544c09101cb60d58d3522ab38f@167.86.76.130:26656,68d4cd0d55c24d281dc988e24be4856a8d8ac56f@14.241.251.186:36656"
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

Copy
PUBKEY=$(jq -r '.pub_key.value' $HOME/.republicd/config/priv_validator_key.json)

cat > validator.json << EOF
{
  "pubkey": {"@type":"/cosmos.crypto.ed25519.PubKey","key":"$PUBKEY"},
  "amount": "20000000000000000000arai",
  "moniker": "validator ismin",
  "identity": "keybaseidlazimyoksabosbirak",
  "website": "web sitesi yoksa twitter link koy",
  "security": "mailadresi",
  "details": "validatoraciklaması",
  "commission-rate": "0.05",
  "commission-max-rate": "0.15",
  "commission-max-change-rate": "0.02",
  "min-self-delegation": "1"
}
EOF
```
```
Copy
republicd tx staking create-validator validator.json \
--from $REPUBLIC_WALLET \
--chain-id raitestnet_77701-1 \
--gas auto \
--gas-adjustment 1.5 \
--gas-prices "1000000000arai" \
--node tcp://localhost:38657 \
-y
```

### unjail
```
republicd tx slashing unjail --from wallet --chain-id raitestnet_77701-1 -gas=auto --gas-adjustment=1.5 --gas-prices=250000000arai
```
### kendine stake
```
republicd tx staking delegate $(republicd keys show wallet --bech val -a) 1000000arai --from wallet --chain-id raitestnet_77701-1 --gas=auto --gas-adjustment=1.5 --gas-prices=250000000arai
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
