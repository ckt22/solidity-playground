// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "./ApeSchool.sol"; 

// Through inheritance, the child contact will have access to
// all the variables and functions of the parent contract
contract ApeFactoryInheritance is ApeSchool {
    ApeSchool[] public apeSchoolArray;

    function createApeSchoolContract() public {
        ApeSchool apeSchool = new ApeSchool();
        apeSchoolArray.push(apeSchool);
    }

    function apeSchoolAddApe(uint256 _index, string memory _name, uint256 _favouriteNumber) public {
        // Address
        // ABI (Application Binary Interface)
        ApeSchool apeSchool = ApeSchool(address(apeSchoolArray[_index]));
        apeSchool.addApe(_name, _favouriteNumber);
    }

    function apeSchoolGetApeFavouriteNumber(uint256 _index, string memory _name) public view returns(uint256) {
        return ApeSchool(address(apeSchoolArray[_index])).getApeFavouriteNumber(_name);
    }
}