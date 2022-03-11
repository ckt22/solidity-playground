from brownie import ApeSchool, accounts, config
# we can also run brownie console to deploy and interact with contracts

def read_contract():
    # work with the most recent version of the deployed contract
    # in the selected network
    ape_school = ApeSchool[-1]
    print(ape_school.getApeFavouriteNumber("Mary"))

def main():
    read_contract()