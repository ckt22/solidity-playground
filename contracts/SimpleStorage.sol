pragma solidity ^0.8.0;

contract SimpleStorage {

    uint256 public favouriteNumber = 5; // public keyword exposes the variable to the contract.
    bool favoriteBool = true;
    string favouriteString = "string";
    int256 favoriteInt = -5;
    address favoriteAddress = 0x63Ed5a2f1f7dfbe87449379e520A88585C1e233a;
    bytes32 favoriteBytes = "cat";

    struct People {
        string name;
        uint256 favouriteNumber;
    }

    People public person = People({name: "Mary", favouriteNumber: 7});
    

    // function
    function store(uint256 _favoriteNumber) public {
        favouriteNumber = _favoriteNumber;
    }

    // view, pure
    function retrieve() public view returns(uint256) {
        return favouriteNumber;
    }

} 