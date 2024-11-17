// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ImageVerifier {
    struct Verification {
        string imageHash;
        string result;
        uint256 timestamp;
    }

    Verification[] public verifications;

    function addVerification(string memory _imageHash, string memory _result) public {
        verifications.push(Verification({
            imageHash: _imageHash,
            result: _result,
            timestamp: block.timestamp
        }));
    }

    function getVerification(uint256 index) public view returns (string memory, string memory, uint256) {
        require(index < verifications.length, "Index out of bounds");
        Verification storage verification = verifications[index];
        return (verification.imageHash, verification.result, verification.timestamp);
    }
}
