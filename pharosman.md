
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
### 4. Set password for key encryption
Set a password that will be used to encrypt your node's cryptographic keys:


```
./ops set-password YOUR_SECURE_PASSWORD
```
Important:

Remember this password - you'll need it to start your node

The password is stored in ./.password file

Keep this password secure and backed up

### 5. Generate cryptographic keys
Generate the domain and stabilizing keys for your node:


```
./ops generate-keys
```
This will create the following files in the ./keys/ directory:
```
domain.key - ECDSA private key (prime256v1)

domain.pub - ECDSA public key

stabilizing.key - BLS12-381 private key

stabilizing.pub - BLS12-381 public key
```

### 5B Get Node ID
Get the Node ID from your domain public key:

```
./ops get-nodeid
```
This calculates the SHA256 hash of the domain public key (with prefix stripped) and displays the Node ID.

Options:

--keys-dir - Directory containing domain.pub (default: ./keys)

### 6. Bootstrap the node
Initialize the node with genesis state:


```
./ops bootstrap --config ./pharos.conf
```
This command will:

Create the storage database

Initialize the genesis block

Prepare the node for first startup

### 7. Start the node Manuel
Start the Pharos node service:


```
./ops start --config ./pharos.conf
```
The node will start in daemon mode and begin syncing with the network.

Check the logs to verify the node is running:


```
tail -f $HOME/data/pharos/log/aldaba.log
```

### 7B Stop Node
Stop the running node:

* Graceful stop
```
ops stop
```
* Force stop
```
ops stop --force
```
### 8. Setup systemd service
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
WorkingDirectory=$HOME/data/$WORKSPACE
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
sudo systemctl restart pharosd
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


### Validator Management
Register as Validator
Register your node as a validator on the network:

Set private key via environment variable (required)
```
cd
```
```
export WORKSPACE=pharos
```
```
cd $HOME/data/$WORKSPACE
```
```
export VALIDATOR_PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE
```
```
./ops add-validator \
  --domain-label my-validator \
  --domain-endpoint tcp://47.84.7.245:19000 \
  --stake 1000000
```
```
Environment Variable (Required):

VALIDATOR_PRIVATE_KEY - Private key for transaction signing (hex format, with or without 0x prefix)
Required Parameters:

--domain-label - Validator name/description
--domain-endpoint - Your validator's public endpoint URL
For IP:PORT format: must use tcp:// prefix (e.g., tcp://127.0.0.1:19000)
For domain names: can use any protocol (e.g., https://pharos.validator.com)
Optional Parameters:

--rpc-endpoint - RPC endpoint to send transaction (default: http://127.0.0.1:18100)
--stake - Stake amount in tokens (default: 1000000)
--domain-pubkey - Path to domain public key (default: ./keys/domain.pub)
--stabilizing-pubkey - Path to stabilizing public key (default: ./keys/stabilizing.pub)
Example:

export VALIDATOR_PRIVATE_KEY=abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890

./ops add-validator \
  --rpc-endpoint http://127.0.0.1:18100 \
  --domain-label golang-validator \
  --domain-endpoint tcp://127.0.0.1:19000 \
  --stake 10000000
Output:

Adding validator...
Account address: 0x1234567890abcdef...
Connected to endpoint
Stake amount: 10000000 tokens (10000000000000000000000000 wei)
Validator register tx: 0xabcdef1234567890...
Validator register success
Exit Validator
Request to exit from the validator set:
```
### Exit Validator
```
cd
```
```
export WORKSPACE=pharos
```
```
cd $HOME/data/$WORKSPACE
```
```
export VALIDATOR_PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE
```
```
./ops exit-validator
```
```
VALIDATOR_PRIVATE_KEY - Private key for transaction signing (hex format, with or without 0x prefix)
Optional Parameters:

--rpc-endpoint - RPC endpoint to send transaction (default: http://127.0.0.1:18100)
--domain-pubkey - Path to domain public key (default: ./keys/domain.pub)
Example:

export VALIDATOR_PRIVATE_KEY=abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890

./ops exit-validator \
  --rpc-endpoint http://127.0.0.1:18100
Output:

Exiting validator...
Account address: 0x1234567890abcdef...
Pool ID: abc123def456789...
Connected to endpoint
Validator exit tx: 0xfedcba0987654321...
Validator exit success
```
