from web3 import Web3
from solcx import compile_standard
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.default_account = w3.eth.accounts[0]

# Compile Contract
with open("blockchain/contracts/ImageVerifier.sol", "r") as file:
    contract_source_code = file.read()

compiled_contract = compile_standard(
    {
        "language": "Solidity",
        "sources": {"ImageVerifier.sol": {"content": contract_source_code}},
        "settings": {
            "outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode"]}}
        },
    },
    solc_version="0.8.0",
)

# Extract bytecode and ABI
bytecode = compiled_contract["contracts"]["ImageVerifier.sol"]["ImageVerifier"]["evm"][
    "bytecode"
]["object"]
abi = compiled_contract["contracts"]["ImageVerifier.sol"]["ImageVerifier"]["abi"]

# Print ABI for debugging
print(json.dumps(abi, indent=4))

# Deploy Contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contract deployed at: {tx_receipt.contractAddress}")
