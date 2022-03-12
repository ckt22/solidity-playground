from brownie import PayMeEthereum, MockV3Aggregator, network, config
from scripts.helper import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS
)
from web3 import Web3

def deploy():
    account = get_account()
    # pass priceFeed address

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else: # deploy a mock
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    pay_me = PayMeEthereum.deploy(
        price_feed_address,
        { "from": account },
        publish_source=config["networks"][network.show_active()].get("verify"))
    print(pay_me)
    return pay_me

def main():
    deploy()