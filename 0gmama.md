### pubkey alma
```
0gchaind deposit validator-keys --home /root/.0gchaind/0g-home/0gchaind-home --chaincfg.chain-spec=devnet
```
NOT: çıktıyı kaydet. pubkey gösterecek.


```
curl -L https://foundry.paradigm.xyz | bash
```
```
source ~/.bashrc
```
```
foundryup
```
```
cast --version
```

### Adress alma
```
cast call \
    0xea224dBB52F57752044c0C86aD50930091F561B9 \
    "computeValidatorAddress(bytes)(address)" \
    "pub-key-yaz" \
    --rpc-url https://0g-galileo-evmrpc.corenodehq.xyz
```
### İmza Oluştur
```
0gchaind deposit create-validator \
    yukarda-aldığın-adresi-yazıcan \
    32000000000 \
    /root/.0gchaind/0g-home/0gchaind-home/config/genesis.json \
    --home /root/.0gchaind/0g-home/0gchaind-home \
    --chaincfg.chain-spec=devnet
```

### Cast ile validator oluşturma
```
cast send 0xea224dBB52F57752044c0C86aD50930091F561B9 \
"createAndInitializeValidatorIfNecessary((string,string,string,string,string),uint32,uint96,bytes,bytes)" \
'("MollaValidator","molla-keybase","https://molla-node.com","security@molla.com","Güvenli ve hızlı node")' \
50000 1 \
pubkey-yaz \
singature-yaz \
--gas-limit 1000000 \
--gas-price 50000000000 \
--value 32000000000000000000 \
--rpc-url https://0g-galileo-evmrpc.corenodehq.xyz \
--private-key 0xSENIN_PRIVATE_KEYIN
```


### Vali bilgi güncelleme
```
cast send 0xVALIDATOR_KONTRAT_ADRESI \
"updateDescription((string,string,string,string,string))" \
'("YeniMolla","yeni-keybase","https://yenisite.com","güvenlik@site.com","Yepyeni açıklama")' \
--rpc-url https://evmrpc-testnet.0g.ai \
--private-key 0xSENIN_PRIVATE_KEYIN
```
