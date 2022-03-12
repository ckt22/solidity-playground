from brownie import PayMeEthereum
from scripts.helper import get_account

def fund():
    pay_me = PayMeEthereum[-1]
    account = get_account()
    entrance_fee = pay_me.getEntranceFee()
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    pay_me.buyMeACoffee({"from": account, "value": entrance_fee})

def withdraw():
    pay_me = PayMeEthereum[-1]
    account = get_account()
    pay_me.withdraw({"from": account})

def main():
    fund()
    withdraw()