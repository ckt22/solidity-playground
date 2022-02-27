# This is a Python script for deploying smart contracts
# and compiles them into ABI

from audioop import add
import os
import json
from dotenv import load_dotenv

load_dotenv()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, "ApeSchool.sol")
from solcx import compile_standard, install_solc

from web3 import Web3

with open(my_file, "r") as file:
    ape_school_file = file.read()

install_solc("0.8.7")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"ApeSchool.sol": {"content": ape_school_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    }
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get the bytecode from the json abi
bytecode = compiled_sol["contracts"]["ApeSchool.sol"]["ApeSchool"]["evm"]["bytecode"]["object"]

# get abi
abi = compiled_sol["contracts"]["ApeSchool.sol"]["ApeSchool"]["abi"]

# connect to the blockchain
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/ff285d97298a47e3aae359128323d40d"))
# check chain id on https://chainlist.org/
network_id = 4
blockchain_address = "0x63Ed5a2f1f7dfbe87449379e520A88585C1e233a"
# blockchain_priv_key = "0x3b41f5d10ad3be0cb6b9761a39ff7eb0697f5f3616afbf0637cf7ad33f2e029f"
blockchain_priv_key = os.getenv("PRIVATE_KEY_RINKEBEY")

# create new contract
ApeSchool = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.get_transaction_count(blockchain_address)

# build, sign, deploy
transaction = ApeSchool.constructor().buildTransaction({
    "gasPrice": w3.eth.gas_price,
    "chainId": network_id,
    "from": blockchain_address,
    "nonce": nonce
})
signed_tx = w3.eth.account.sign_transaction(transaction, blockchain_priv_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# work with the deployed contract
ape_school = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# calling functions of the contract

# simulation. has no impact on the actual contract
print(ape_school.functions.getApeFavouriteNumber("Mary").call())

# actually modifies the contract
add_ape_transaction = ape_school.functions.addApe("Mary", 7).buildTransaction({
    "gasPrice": w3.eth.gas_price, 
    "chainId": network_id,
    "from": blockchain_address,
    "nonce": nonce + 1
})
add_ape_transaction_tx = w3.eth.account.sign_transaction(add_ape_transaction, blockchain_priv_key)
transaction_hash = w3.eth.send_raw_transaction(add_ape_transaction_tx.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print(ape_school.functions.getApeFavouriteNumber("Mary").call())