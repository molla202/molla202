

## Hardware Requirements

| Component | Minimum | Recommended |
|---|---|---|
| Operating System | Ubuntu 22.04+ | Ubuntu 24.04 |
| CPU | 4 cores | 8 cores |
| RAM | 8 GB | 16 GB |
| Disk | 200 GB SSD | 500 GB NVMe SSD |
| Network | 100 Mbps | 1 Gbps |


| Type | Endpoint |
|---|---|
| RPC | https://rpc.test13.testnets.gno.land |
| Explorer | https://test13.testnets.gno.land |
| Faucet | https://test13.testnets.gno.land/faucet |
| Valopers | https://test13.testnets.gno.land/r/gnops/valopers |
| Active Validators | https://test13.testnets.gno.land/r/sys/validators/v3 |
| Official Docs | https://docs.gno.land |
| GitHub | https://github.com/gnolang/gno |

---



### Install Go

Gnoland requires **Go 1.22+**. This step installs Go 1.23 and configures the PATH:

```bash
cd $HOME
VER="1.23.0"
wget "https://golang.org/dl/go$VER.linux-amd64.tar.gz"
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf "go$VER.linux-amd64.tar.gz"
rm "go$VER.linux-amd64.tar.gz"

[ ! -f ~/.bash_profile ] && touch ~/.bash_profile
echo 'export PATH=/usr/local/go/bin:$HOME/go/bin:$PATH' >> ~/.bash_profile
echo 'export GNOROOT=$HOME/gno' >> ~/.bash_profile
source $HOME/.bash_profile
[ ! -d ~/go/bin ] && mkdir -p ~/go/bin
export PATH="$HOME/go/bin:$PATH"
```

### set vars
```
echo "export WALLET="wallet"" >> $HOME/.bash_profile
echo "export MONIKER="test"" >> $HOME/.bash_profile
echo "export GNOLAND_CHAIN_ID="test13"" >> $HOME/.bash_profile
echo "export GNOLAND_PORT="54"" >> $HOME/.bash_profile
source $HOME/.bash_profile
```
###  Binary
```
cd $HOME
rm -rf gno
git clone https://github.com/gnolang/gno.git
git checkout chain/test13
cd gno
make -C gno.land install.gnoland install.gnokey
```
### Config set
```
cd $HOME/gno
gnoland config init
gnoland secrets init -data-dir $HOME/gno/gnoland-data/secrets/
gnoland config set rpc.laddr tcp://0.0.0.0:${GNOLAND_PORT}657
gnoland config set p2p.laddr tcp://0.0.0.0:${GNOLAND_PORT}656
gnoland config set proxy_app tcp://127.0.0.1:${GNOLAND_PORT}658
gnoland config set moniker $MONIKER
gnoland config set application.prune_strategy syncable
gnoland config set consensus.timeout_commit 3s
gnoland config set consensus.peer_gossip_sleep_duration 10ms
gnoland config set p2p.flush_throttle_timeout 10ms
gnoland config set mempool.size 10000
gnoland config set p2p.external_address "$(wget -qO- eth0.me):${GNOLAND_PORT}656"
gnoland config set p2p.max_num_outbound_peers 40
```
```
gnoland config set p2p.persistent_peers \
  "g142k7zc2qym3c0u6jmkf6rv26llgr2f4nakmlmt@sentry-1.test13.testnets.gno.land:26656,g1lxkf9gn7kddrr26c640ww5wg3ezsm22we8cjpc@sentry-2.test13.testnets.gno.land:26656"
```
### Move folder and download genesis
```
mv $HOME/gno/gnoland-data $HOME/gnoland-data
```
```
cd $HOME/gnoland-data/config
wget -O genesis.json https://github.com/gnolang/gno/releases/download/chain/test13/genesis.json
```
### Service
```
sudo tee /etc/systemd/system/gnoland.service > /dev/null <<EOF
[Unit]
Description=Gnoland node
After=network-online.target
[Service]
User=$USER
WorkingDirectory=$HOME
Environment=HOME=$HOME
Environment=GNOROOT=$HOME/gno
ExecStart=$(which gnoland) start \
--chainid test-13 \
--genesis  $HOME/gnoland-data/config/genesis.json \
--data-dir $HOME/gnoland-data/ \
--skip-genesis-sig-verification
Restart=on-failure
RestartSec=5
LimitNOFILE=65535
[Install]
WantedBy=multi-user.target
EOF
```
###  Start
```
sudo systemctl daemon-reload
sudo systemctl enable gnoland
```
```
sudo systemctl restart gnoland && sudo journalctl -u gnoland -f
```

### Vali Register
```
gnoland secrets get validator_key
```
NOT: save pubkey. `https://gno.satai.0xgen.online/register`
