# solidity-playground

This is the repo showing my learning progress in smart contract development.

## Ape School (Simple Storage Simulation)
This contract is to demonstrate the storage behavior of smart contracts. We will be creating apes and we can query its attributes by the name.

Contract deployed on Rinkbey network: 0xF14c4a380bE790d6aFB4e5B1FA9B024d8f82DcAA

## Ape School Factory (Smart Contract Factory)
This contract demonstrates how a contract can deploy other contracts as at the same time keep track of each contract.

## Pay Me Ethereum (Payment)
This contract demonstrates how to accept payment from users and allow ethereum withdrawl of the contract owner.

## Brownie
To add a network to brownie
```
brownie networks add Ethereum ganache-local host=http://127.0.0.1:7545 chainid=5777
```

To add a mainnet fork to brownie (with the help of infura)
```
brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/JXpMtAZnjtcDSZg4L0AAtv1LuvwsDRQO accounts=10 mnemonic=brownie port=8545
```

Testing a selected function
```
brownie test -k test_function_name --network blah
```