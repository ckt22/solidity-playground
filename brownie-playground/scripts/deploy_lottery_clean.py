from scripts.helper import get_account, get_account_v2, get_contract, fund_with_link
from brownie import Lottery, LotteryClean, network, config
import time


def deploy_lottery():
    account = get_account_v2()
    lottery = LotteryClean.deploy(
        {"from":account},
        publish_source=config["networks"][network.show_active()].get("verify")
    )
    print("Deployed lottery")
    return lottery

def enter_lottery():
    account = get_account_v2()
    lottery = LotteryClean[-1]
    value = 100000000000000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(3)

def end_lottery():
    account = get_account_v2()
    print(f"Account is {account}")
    lottery = LotteryClean[-1]
    # fund the contract
    tx = fund_with_link(lottery.address)
    tx.wait(3)

    ending_transaction = lottery.pickWinner({"from": account})
    ending_transaction.wait(3)
    time.sleep(60)
    print(f"{lottery.getWinnerByLottery(0)}")


def main():
    deploy_lottery()
    # start_lottery()
    enter_lottery()
    end_lottery()