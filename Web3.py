from web3 import Web3

# Connect to a local or test Ethereum node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))  # Adjust URL for your node

# Replace with your contract address
contract_address = "0x16334576227f952f296b52D1a06a1dF2451FBC4d"

# You can get the ABI from Etherscan if deployed on the public network, or use a deployed contract's ABI
# Example: Fetch ABI directly from Etherscan for a known contract
api_url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}"
import requests

response = requests.get(api_url)
abi = response.json()["result"]

# Print the ABI
print(abi)
