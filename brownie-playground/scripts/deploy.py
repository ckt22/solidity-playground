from brownie import accounts, config, ApeSchool, network
import os

# to connect to testnet account, do the following 
# brownie accounts new {account-name}
# when asked for private key, fill in your mm wallet pk (Add 0x in front)
# then set a password

# once you load an account tob brownie, you can run
# account = accounts.load("{account-name}")
# to get the account

# or to import from a dotenv file
# account = accounts.add(os.getenv('PRIVATE_KEY'))

# or to import from yaml config file
# account = accounts.add(config["wallets"]["from_key"])

def deploy_ape_school():

    account = get_account()
    print(account)
    ape_school = ApeSchool.deploy({
        "from": account
    })

    # brownie run scripts/deploy --network rinkeby 

    # call a view function
    ape_favourite_number = ape_school.getApeFavouriteNumber("Mary")
    print(ape_favourite_number)

    # transaction
    transaction = ape_school.addApe("Mary", 7)
    transaction.wait(1)
    ape_favourite_number = ape_school.getApeFavouriteNumber("Mary")
    print(ape_favourite_number)

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def main():
    deploy_ape_school()
