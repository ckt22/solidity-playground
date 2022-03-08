from brownie import ApeSchool, accounts

def test_deploy():
    account = accounts[0]

    ape_school = ApeSchool.deploy({
        "from": account
    })
    ape_favourite_number = ape_school.getApeFavouriteNumber("Mary")
    expected = 0
    
    assert ape_favourite_number == expected

def test_add_ape():
    account = accounts[0]
    ape_school = ApeSchool.deploy({
        "from": account
    })

    expected = 7
    transaction = ape_school.addApe("Mary", 7)
    transaction.wait(1)

    assert ape_school.getApeFavouriteNumber("Mary") == expected
