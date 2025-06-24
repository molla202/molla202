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
    0xef6b2c3749657fEAfDE44E82498Fc14f92F40F09 \
    32000000000 \
    /root/.0gchaind/0g-home/0gchaind-home/config/genesis.json \
    --home /root/.0gchaind/0g-home/0gchaind-home \
    --chaincfg.chain-spec=devnet
```

- evet pubkey aldık adres aldık adresi yazıp imza oluşturduk şimdi remixe gidip kontrat deploy edicez. https://remix.ethereum.org/
- yeni file oluşturuyoruz isim veriyoruz. sonra altaki kodu yapıstırıyoruz değiştirilcek yerler moniker vs ve pubkeyle imzada aldığımız singature ekleyip compile edip deploy edicez. 32 og lazım valuse kısmına soldaki 32 yazmanız gerek.





```
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IStakingContract {
    function createAndInitializeValidatorIfNecessary(
        Description calldata description,
        uint32 commissionRate, 
        uint96 withdrawalFeeInGwei,
        bytes calldata pubkey,
        bytes calldata signature
    ) external payable returns (address);

    struct Description {
        string moniker;
        string identity;
        string website;
        string securityContact;
        string details;
    }
}

contract ValidatorExample {
    IStakingContract constant STAKING = IStakingContract(0xea224dBB52F57752044c0C86aD50930091F561B9);

    function createValidator() external payable {
        IStakingContract.Description memory desc = IStakingContract.Description({
            moniker: "monikerovski",
            identity: "",
            website: "",
            securityContact: "",
            details: ""
        });

        // ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        // ↓↓↓ KENDİ PUBKEY ve SIGNATURE'INI BURAYA YAPIŞTIR ↓↓↓ yukarıdaki moniker kısmınlarını unutma
        bytes memory pubkey = hex"we are 0g";       // 48 byte compressed eth/beacon pubkey (başında 0x yok)
        bytes memory signature = hex"we are 0g";    // Çok uzun hex string
        // ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        STAKING.createAndInitializeValidatorIfNecessary{value: msg.value}(
            desc,
            50000, // 5% komisyon oranı
            1,     // 1 Gwei withdrawal fee
            pubkey,
            signature
        );
    }
}
```


![image](https://github.com/user-attachments/assets/e1c5d864-6b9a-4b72-8810-4a0793c62056)

![image](https://github.com/user-attachments/assets/8584f634-a389-4841-a20a-ff982abbb9d3)

![image](https://github.com/user-attachments/assets/be795c20-4ec5-44b7-a02a-3453cba79579)



### Cast ile validator oluşturma
```
cast send 0xea224dBB52F57752044c0C86aD50930091F561B9 \
"createAndInitializeValidatorIfNecessary((string,string,string,string,string),uint32,uint96,bytes,bytes)" \
'("MollaValidator","molla-keybase","https://molla-node.com","security@molla.com","Güvenli ve hızlı node")' \
50000 1 \
pubkey-yaz \
singature-yaz \
--value 32000000000 \
--rpc-url https://0g-galileo-evmrpc.corenodehq.xyz \
--private-key 0xSENIN_PRIVATE_KEYIN
```





