### Binary çekelim
```
cd $HOME
mkdir -p $HOME/.republic/cosmovisor/genesis/bin
curl -L "https://media.githubusercontent.com/media/RepublicAI/networks/main/testnet/releases/v0.3.0/republicd-linux-amd64" -o $HOME/.republic/cosmovisor/genesis/bin/republicd
chmod +x $HOME/.republic/cosmovisor/genesis/bin/republicd
```
### sistem link
```
sudo ln -s $HOME/.republic/cosmovisor/genesis $HOME/.republic/cosmovisor/current -f
sudo ln -s $HOME/.republic/cosmovisor/current/bin/republicd /usr/local/bin/republicd -f
```
### ubuntu 22 için gblic ayarları
```
cd $HOME
wget -O glibc-2.39-ubuntu24.tar.gz https://github.com/molla202/molla202/raw/refs/heads/main/glibc-2.39-ubuntu24.tar.gz
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
### cüzdan import
```
republicd keys add wallet --recover --keyring-backend test
```
### Servis
```
sudo tee /etc/systemd/system/republic-job-sidecar.service > /dev/null << EOF
[Unit]
Description=Republic Job Sidecar (Compute Validation Miner)
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=$(whoami)
Restart=always
RestartSec=10

ExecStart=republicd tx computevalidation job-sidecar \\
  --from wallet \\
  --work-dir $HOME/republic/jobs \\
  --poll-interval 10s \\
  --node https://republic-test-rpc.corenodehq.xyz \\
  --chain-id raitestnet_77701-1 \\
  --gas auto \\
  --gas-adjustment 1.5 \\
  --keyring-backend test

StandardOutput=journal
StandardError=journal
SyslogIdentifier=republic-job-sidecar

[Install]
WantedBy=multi-user.target
EOF
```
```
sudo systemctl daemon-reload
sudo systemctl enable republic-job-sidecar
sudo systemctl start republic-job-sidecar
sudo systemctl status republic-job-sidecar
```
### Log
```
journalctl -u republic-job-sidecar -fo cat
```

<img width="789" height="64" alt="image" src="https://github.com/user-attachments/assets/f3219d39-d293-44e2-9119-983f22f380f5" />


NOT: çalıştırmak için Vram lazım yani GPU - validator olmak gerekiyor ve vali olduğunuz cüzdanı import ediceksiniz.

### Görevleri görmek
```
republicd query computevalidation list-job --node https://republic-test-rpc.corenodehq.xyz
```
<img width="924" height="983" alt="image" src="https://github.com/user-attachments/assets/e2ca1cc8-6976-4d54-8a38-540161fbf50b" />

