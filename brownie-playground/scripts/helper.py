from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

DECIMALS=18
STARTING_VALUE=2000
LOCAL_BLOCKCHAIN_ENVIRONMENTS=["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS=["mainnet-fork-dev"]

def get_account():
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS 
    or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    account = get_account()
    if len(MockV3Aggregator) <= 0:
        print(f"The active network is: {network.show_active()}")
        print(f"Deploying mocks...")
        mock_v3_aggregator = MockV3Aggregator.deploy(DECIMALS, Web3.toWei(STARTING_VALUE, "ether"),
        { "from": account })