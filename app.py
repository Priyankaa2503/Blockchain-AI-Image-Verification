from flask import Flask, request, jsonify
import hashlib
import os
from ai_module import analyze_image
from web3 import Web3

app = Flask(__name__)

# Blockchain Setup
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.default_account = w3.eth.accounts[
    0
]  # Make sure this account is funded in Ganache

# ABI from the deployed contract
abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "_imageHash", "type": "string"},
            {"internalType": "string", "name": "_result", "type": "string"},
        ],
        "name": "addVerification",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
        "name": "getVerification",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "verifications",
        "outputs": [
            {"internalType": "string", "name": "imageHash", "type": "string"},
            {"internalType": "string", "name": "result", "type": "string"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
]

contract_address = "0x4bFA09697F4A48C0ac60CcD95f55ffa4dD706B3f"
contract = w3.eth.contract(address=contract_address, abi=abi)


@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    file.save(file_path)

    # Analyze Image
    analysis = analyze_image(file_path)
    if "error" in analysis:
        return jsonify(analysis), 500

    # Hash Image
    with open(file_path, "rb") as f:
        image_hash = hashlib.sha256(f.read()).hexdigest()

    # Store in Blockchain
    try:
        tx_hash = contract.functions.addVerification(
            image_hash, analysis["result"]
        ).transact({"from": w3.eth.default_account})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(
        {
            "result": analysis["result"],
            "confidence": analysis["confidence"],
            "transaction_id": tx_hash.hex(),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
