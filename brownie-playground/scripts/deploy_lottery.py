from scripts.helper import get_account, get_account_v2, get_contract, fund_with_link
from brownie import Lottery, LotteryClean, network, config
import time


def deploy_lottery():
    account = get_account_v2()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["subscription_id"],
        {"from": account, "gas_limit": 20000000},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery")
    print(lottery.getEntranceFee())
    return lottery

def start_lottery():
    account = get_account_v2()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)

def enter_lottery():
    account = get_account_v2()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 1000000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)

def end_lottery():
    account = get_account_v2()
    print(f"Account is {account}")
    lottery = Lottery[-1]
    # fund the contract
    # tx = fund_with_link(lottery.address)
    # tx.wait(1)

    # ending_transaction = lottery.endLottery({"from": account})
    # ending_transaction.wait(1)
    # time.sleep(60)
    # print(f"{lottery.recentWinner()} is the new winner!")

    ending_transaction = lottery.pickWinner({"from": account})
    ending_transaction.wait(1)
    print(f"{lottery.getWinnerByLottery(0)}")


def main():
    deploy_lottery()
    # start_lottery()
    enter_lottery()
    end_lottery()