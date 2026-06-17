### Nulla Relay Mainnet Validator Installation Guide
This repository provides a clean, isolated, and secure way to run a Polkadot-based Nulla Relay node.

Official guides usually scatter binaries, configuration files, and blockchain databases across system root directories like /usr/local/bin, /var/lib, and /etc. This repository restructures everything into a single, isolated folder inside the user's home directory. Essential binaries are linked to the system via Symlinks to ensure Polkadot sub-workers function perfectly without polluting your global environment.

Repository Structure
Before you begin the installation, make sure your cloned repository folder looks exactly like this:

- binaries/

    - nulla-relay

    - polkadot-execute-worker

     - polkadot-prepare-worker

- chainspec/

     - nulla-mainnet.raw.json

- README.md

### Step-by-Step Installation
1. Define Environment Variables
To avoid path mistakes during setup, define your workspace variables. By default, everything will be stored safely under your user's home directory (~/nulla-node).

```
export NODE_HOME="$HOME/nulla-node"
export NODE_USER="$USER"
```

2. Create the Isolated Directory Structure
Create the dedicated directories for your custom environment:

```
mkdir -p "$NODE_HOME/bin"
mkdir -p "$NODE_HOME/config"
mkdir -p "$NODE_HOME/data"
mkdir -p "$NODE_HOME/keystore"
```
3. Download Binaries & Create System Symlinks
We download the official network binaries directly into your isolated environment, apply executable permissions, and link them to /usr/local/bin via symbolic links. This allows the system and Polkadot sub-workers to discover each other globally.

```
wget -O "$NODE_HOME/bin/nulla-relay" "https://github.com/NullaZK/mainnet/releases/download/v1/nulla-relay"
wget -O "$NODE_HOME/bin/polkadot-execute-worker" "https://github.com/NullaZK/mainnet/releases/download/v1/polkadot-execute-worker"
wget -O "$NODE_HOME/bin/polkadot-prepare-worker" "https://github.com/NullaZK/mainnet/releases/download/v1/polkadot-prepare-worker"
```
```
chmod +x "$NODE_HOME/bin/"*
```
```
sudo ln -sf "$NODE_HOME/bin/nulla-relay" /usr/local/bin/nulla-relay
sudo ln -sf "$NODE_HOME/bin/polkadot-prepare-worker" /usr/local/bin/polkadot-prepare-worker
sudo ln -sf "$NODE_HOME/bin/polkadot-execute-worker" /usr/local/bin/polkadot-execute-worker
```
3b. Move Binaries & Create System Symlinks
Copy the network binaries from the repository into your isolated environment, then link them to /usr/local/bin using symbolic links. This allows the system and sub-workers to discover them globally.

```
cp binaries/nulla-relay             "$NODE_HOME/bin/"
cp binaries/polkadot-prepare-worker "$NODE_HOME/bin/"
cp binaries/polkadot-execute-worker "$NODE_HOME/bin/"
chmod +x "$NODE_HOME/bin/"*
```
```
sudo ln -sf "$NODE_HOME/bin/nulla-relay" /usr/local/bin/nulla-relay
sudo ln -sf "$NODE_HOME/bin/polkadot-prepare-worker" /usr/local/bin/polkadot-prepare-worker
sudo ln -sf "$NODE_HOME/bin/polkadot-execute-worker" /usr/local/bin/polkadot-execute-worker
```
4. Setup Chain Specification & Node Key
Move the network configuration file and generate your unique node key inside your data directory.

```
cp chainspec/nulla-mainnet.raw.json "$NODE_HOME/config/"
chmod 644 "$NODE_HOME/config/nulla-mainnet.raw.json"
```
### Generate Node Key
```
"$NODE_HOME/bin/nulla-relay" key generate-node-key \
  --file "$NODE_HOME/data/node.key"
```
```
"$NODE_HOME/bin/nulla-relay" key inspect-node-key --file "$NODE_HOME/data/node.key"
```
5. Import Validator Session Keys
Set up your security mnemonic phrases and inject your session keys into your isolated keystore folder.

NOT: 12 kelime den oluşan bir cüzdan kelimeleri girin.
```
MNEMONIC="your twelve word mnemonic phrase here"
KEYSTORE="$NODE_HOME/keystore"
```
```
chmod 700 "$KEYSTORE"
```
### Insert Aura/Babe/Grandpa/Para keys
```
for TYPE in babe gran audi asgn para; do
  SCHEME=sr25519
  [ "$TYPE" = "gran" ] && SCHEME=ed25519
  "$NODE_HOME/bin/nulla-relay" key insert \
    --keystore-path "$KEYSTORE" \
    --scheme $SCHEME \
    --key-type $TYPE \
    --suri "$MNEMONIC"
done
```
### Insert BEEFY key (ecdsa)
```
"$NODE_HOME/bin/nulla-relay" key insert \
  --keystore-path "$KEYSTORE" \
  --scheme ecdsa \
  --key-type beef \
  --suri "$MNEMONIC"
```
```
chmod 600 "$KEYSTORE"/*
```
### Create Systemd Service
For better security, the node will run under your local system user account instead of root. Run the entire block below to generate the custom systemd service file automatically.

Note: Remember to change YOUR_NODE_NAME to your preferred on-chain moniker before running the command.

```
NODE_NAME="YOUR_NODE_NAME"
```
```
sudo tee /etc/systemd/system/nullad.service > /dev/null <<EOF
[Unit]
Description=Nulla Relay Mainnet Validator (Isolated Env)
After=network-online.target
Wants=network-online.target

[Service]
User=$NODE_USER
Type=simple
Restart=always
RestartSec=10
LimitNOFILE=65536

ExecStart=$NODE_HOME/bin/nulla-relay \\
  --chain $NODE_HOME/config/nulla-mainnet.raw.json \\
  --validator \\
  --name "$NODE_NAME" \\
  --base-path $NODE_HOME/data \\
  --keystore-path $NODE_HOME/keystore \\
  --node-key-file $NODE_HOME/data/node.key \\
  --port 30333 \\
  --rpc-port 9944 \\
  --rpc-methods Safe \\
  --no-telemetry

[Install]
WantedBy=multi-user.target
EOF
```
### Launch and Manage Node
Now that everything is cleanly configured in your custom folder, reload systemd, activate the service, and start your node.

```
sudo systemctl daemon-reload
```
```
sudo systemctl enable nullad
```
```
sudo systemctl start nullad
```
Useful Management Commands

Check Node Status: 
```
sudo 
```
systemctl status nullad
```
View Live Logs: 
```
journalctl -u nullad -f -o cat
```
Restart Node: 
```
sudo systemctl restart nullad
```
Stop Node: 
```
sudo systemctl stop nullad
```
