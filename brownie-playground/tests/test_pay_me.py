from scripts.helper import get_account
from scripts.deploy_pay_me import deploy

def test_can_fund_and_withdraw():
    account = get_account()
    pay_me = deploy()
    entrance_fee = pay_me.getEntranceFee()
    tx = pay_me.buyMeACoffee({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert pay_me.addressToAmountPaidMap(account) == entrance_fee

    tx2 = pay_me.withdraw({"from": account})
    tx2.wait(1)
    assert pay_me.addressToAmountPaidMap(account) == 0

