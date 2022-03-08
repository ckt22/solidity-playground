// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

// This contract is to demonstrate how data in a smart contract is stored.
contract ApeSchool {

    uint256 favouriteNumber = 5; // public keyword exposes the variable to the contract.
    bool favoriteBool = true;
    string favouriteString = "string";
    int256 favoriteInt = -5;
    address favoriteAddress = 0x63Ed5a2f1f7dfbe87449379e520A88585C1e233a;
    bytes32 favoriteBytes = "cat";

    struct Ape {
        string name;
        uint256 favouriteNumber;
    }

    // Ape public hodler = Ape({name: "Mary", favouriteNumber: 7});

    // dynamic array
    Ape[] apes;
    mapping(string => uint256) public nameToFavouriteNumber;

    // fixed array
    // Ape[1] public oneApe;

    // function
    // memory keyword - data is stored only during execution
    // need memory/storage keyword for string since string is an object
    function addApe(string memory _name, uint256 _favouriteNumber) public {
        apes.push(Ape({name: _name, favouriteNumber: _favouriteNumber}));
        nameToFavouriteNumber[_name] = _favouriteNumber;
    }

    // view, pure
    function getApeFavouriteNumber(string memory _name) public view returns(uint256) {
        return (nameToFavouriteNumber[_name] == 0) ? 1 : nameToFavouriteNumber[_name];
    }

} 