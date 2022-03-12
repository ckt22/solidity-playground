from scripts.helper import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy_pay_me import deploy
from brownie import network, accounts, exceptions
import pytest

def test_can_fund_and_withdraw():
    account = get_account()
    pay_me = deploy()
    entrance_fee = pay_me.getEntranceFee() + 100
    tx = pay_me.buyMeACoffee({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert pay_me.addressToAmountPaidMap(account) == entrance_fee

    tx2 = pay_me.withdraw({"from": account})
    tx2.wait(1)
    assert pay_me.addressToAmountPaidMap(account) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Local testing only")
    account = get_account()
    pay_me = deploy()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        pay_me.withdraw({"from": bad_actor})
    

