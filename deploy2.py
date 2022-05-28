from solcx import compile_standard , install_solc
import json
import os
from dotenv import load_dotenv
from web3 import Web3 

load_dotenv()

with open("./SimpleStorages.sol","r") as file:
    simple_storage_file = file.read()
    #print(simple_storage_file)

install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorages.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
#print(compiled_sol)
with open("compiled_code.json","w") as file:
        json.dump(compiled_sol , file)

#get_bytecode
bytecode = compiled_sol["contracts"]["SimpleStorages.sol"]["SimpleStorage"][
    "evm"
    ]["bytecode"]["object"]
#get_abi
abi = compiled_sol["contracts"]["SimpleStorages.sol"]["SimpleStorage"]["abi"]
#connect web3 rinkeby
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/abadc6c834c5405db38243031cbaef6e"))
chain_id = 4 
my_address = "0x26a3167bea25075e8018b47CAf8ce4Caeab43665"
private_key = os.getenv("PRIVIATE_KEY")
#create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
#print(SimpleStorage)
nonce = w3.eth.getTransactionCount(my_address)
print(my_address,"nonce=", nonce)
###################################
# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
###################################
# 1. Build a transaction
transaction = SimpleStorage.constructor().buildTransaction( {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id, 
        "from": my_address, 
        "nonce": nonce
    }
)
#print("transaction::",transaction)
# 2. Sign a transaction
print("Delploying Contract....")
signed_txn = w3.eth.account.sign_transaction(transaction,private_key=private_key)
# 3. Send a transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#wait transaction finish(very fast,could be mask)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract Deploied!")

#Working with Contract, you need:
#Contract ABI
#Contract Address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
#Call -> Simulate making the call and getting a return value
#Transaction -> Actually make a state change

#Inital value of store value
print("Initial Contract value=",simple_storage.functions.retrieve().call() )

#print of store is only simulate...never execution
#print(simple_storage.functions.store(37).call() )
value = 37
print("Updating  Contract value ",value,"....")
store_transaction = simple_storage.functions.store(value).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id, 
        "from": my_address, 
        "nonce": w3.eth.getTransactionCount(my_address)
    }
)
signed_txn = w3.eth.account.sign_transaction(store_transaction,private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
### check result really exectuion?
print("Contract Value Updated! value=",simple_storage.functions.retrieve().call() )

#print is only simulate...never execution
#print(simple_storage.functions.store(97).call() )
value = 97
print("Updating  Contract value",value,"....")
store_transaction = simple_storage.functions.store(value).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id, 
        "from": my_address, 
        "nonce": w3.eth.getTransactionCount(my_address)
    }
)
signed_txn = w3.eth.account.sign_transaction(store_transaction,private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract Value Updated! value=",simple_storage.functions.retrieve().call() )