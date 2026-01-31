
<img width="407" height="111" alt="image" src="https://github.com/user-attachments/assets/b4b3e478-8435-4354-9673-6bcbb42d4583" />


## 💻 Sistem Gereksinimleri
| Bileşenler | Minimum Gereksinimler | 
| ------------ | ------------ |
| CPU |	32 cores, 2.8GHz or faster, AMD Milan EPYC or Intel Xeon Platinum |
| RAM	| 256 GB |
| Storage	| 5 TB SSD with at least 350MiB/s bandwidth and 30000 IOPS |


### 1. Create working directory and download binary package

```
export WORKSPACE=pharos
```
```
mkdir -p $HOME/data/$WORKSPACE && cd $HOME/data/$WORKSPACE
```
```
wget https://github.com/PharosNetwork/resources/releases/latest/download/pharos-v0.11.1-034a3b78.tar.gz
tar -zxvf pharos-v0.11.1-034a3b78.tar.gz
```
```
The extracted package contains:

bin/pharos_light - Pharos node binary

bin/pharos_cli - Pharos CLI tool

bin/libevmone.so - EVM execution engine library

bin/VERSION - Version information
```
### 2. Download configuration files
Download the genesis configuration file:


```
wget -O genesis.conf https://raw.githubusercontent.com/PharosNetwork/resources/refs/heads/main/atlantic/genesis.conf
```
Download the node configuration file (choose one based on your node type):

For Archive/Full/Validator Node:


```
wget -O pharos.conf https://raw.githubusercontent.com/PharosNetwork/resources/refs/heads/main/atlantic/conf/full.conf
```
Note: Pruning is disabled by default. To enable pruning, see Enable Pruning in Pharos Node.

For TraceDB Node:


```
wget -O pharos.conf https://raw.githubusercontent.com/PharosNetwork/resources/refs/heads/main/atlantic/conf/traceDB.conf
```
### 3. Download and setup ops tool
Download the latest ops tool for Linux:


```
wget https://github.com/PharosNetwork/ops/releases/latest/download/ops-linux-amd64 -O ops
```
```
chmod +x ops
```
```
sudo ln -sf $HOME/data/pharos/ops /usr/local/bin/ops
```
### 4. Set password for key encryption
Set a password that will be used to encrypt your node's cryptographic keys:


```
ops set-password YOUR_SECURE_PASSWORD
```
Important:

Remember this password - you'll need it to start your node

The password is stored in ./.password file

Keep this password secure and backed up

### 5. Generate cryptographic keys
Generate the domain and stabilizing keys for your node:


```
ops generate-keys
```
This will create the following files in the ./keys/ directory:
```
domain.key - ECDSA private key (prime256v1)

domain.pub - ECDSA public key

stabilizing.key - BLS12-381 private key

stabilizing.pub - BLS12-381 public key
```
### 6. Bootstrap the node
Initialize the node with genesis state:


```
ops bootstrap --config $HOME/data/pharos/pharos.conf
```
This command will:

Create the storage database

Initialize the genesis block

Prepare the node for first startup

### 7. Start the node
Start the Pharos node service:


```
ops start --config ./pharos.conf
```
The node will start in daemon mode and begin syncing with the network.

Check the logs to verify the node is running:


```
tail -f $HOME/data/pharos/log/aldaba.log
```
### 8. (Optional) Setup systemd service
For production deployments, it's recommended to manage the Pharos node with systemd.

Create a systemd service file:


```
sudo tee /etc/systemd/system/pharosd.service > /dev/null <<EOF
[Unit]
Description=Pharos Node
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/$HOMEdata/$WORKSPACE/bin
Environment="CONSENSUS_KEY_PWD=$(cat $HOME/data/$WORKSPACE/.password)"
Environment="PORTAL_SSL_PWD=$(cat $HOME/data/$WORKSPACE/.password)"
Environment="LD_PRELOAD=$HOME/data/$WORKSPACE/bin/libevmone.so"
ExecStart=$HOME/data/$WORKSPACE/bin/pharos_light -c $HOME/data/$WORKSPACE/pharos.conf
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits
LimitNOFILE=655350

[Install]
WantedBy=multi-user.target
EOF
```

Enable and start the service:


```
sudo systemctl daemon-reload
sudo systemctl enable pharosd
sudo systemctl start pharosd
```
Check service status:


```
sudo systemctl status pharosd
```
View logs:


```
sudo journalctl -u pharosd -f
```
Note: If not using systemd, you can manually stop the node with pkill pharos_light and restart with ./ops start --config ./pharos.conf

Directory Structure
After deployment, your directory structure should look like:


```
/data/pharos/
├── bin/
│   ├── pharos_light
│   ├── pharos_cli
│   ├── libevmone.so
│   └── VERSION
├── keys/
│   ├── domain.key
│   ├── domain.pub
│   ├── stabilizing.key
│   └── stabilizing.pub
├── data/
│   └── (blockchain data)
├── log/
│   ├── aldaba.log
│   ├── pamir.log
│   └── (other logs)
├── genesis.conf
├── pharos.conf
├── ops
└── .password
```
```
Security Recommendations
Protect your keys: The files in keys/ directory contain your node's private keys

Secure your password: Keep the .password file secure with proper permissions

Backup important files: Backup keys/, .password, and pharos.conf

Firewall configuration: Ensure required ports are open (18100, 19000, 20000)

Regular updates: Keep your node software up to date with latest releases
```
