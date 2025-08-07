```
wget https://snapshot.corenodehq.xyz/0g_testnet/galileo-v1.2.1.zip
unzip galileo-v1.2.1.zip
```
```
cd galileo-v1.2.1
```
```
cp -r $HOME/galileo-v1.2.1/bin/geth $HOME/go/bin/geth
chmod +x $HOME/go/bin/geth
```
```
sed -i 's/beacon-kit/chaincfg/g' $HOME/.0gchaind/0g-home/0gchaind-home/config/app.toml
```
```
systemctl restart geth
```
```
0gchaind rollback --hard --home $HOME/.0gchaind/0g-home/0gchaind-home --chaincfg.chain-spec=devnet
```

<img width="1551" height="95" alt="image" src="https://github.com/user-attachments/assets/9a2296cc-5919-4539-be94-9f0eea6422bb" />

```
rm /root/.0gchaind/0g-home/0gchaind-home/data/priv_validator_state.json
echo '{}' > /root/.0gchaind/0g-home/0gchaind-home/data/priv_validator_state.json
```
```
systemctl restart 0gchaind
```
