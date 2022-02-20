// SPDX-License-Identifier: MIT

pragma solidity >= 0.7.0 <= 0.8.7;

// chainlink interface
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";


contract PayMeEthreum {

    // Math overflow problem is handled in solidity v8+
    // using SafeMathChainlink for uint256;

    mapping(address => uint256) public addressToAmountPaidMap;
    address[] public funders;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // receive fees according to user input
    function buyMeACoffee() public payable {

        // $50 USD
        uint256 minPrice = 50 * 10 * 18; // 50 USD
        require(getConversationRate(minPrice) >= minPrice, "You need to spend more ETH!"); // if the condition returns false, revert transaction
        addressToAmountPaidMap[msg.sender] += msg.value;
        funders.push(msg.sender);

    }

    // getting contract version by calling the version() function in chainlink cntract interface
    // Chainlink Data Feeds are the quickest way to connect your smart contracts 
    // to the real-world market prices of assets.
    function getVersion() public view returns(uint256) {
        // get contract address at: https://docs.chain.link/docs/ethereum-addresses/
        address ethToUsdRinkbeyContractAddress = 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e;
        AggregatorV3Interface priceFeed = AggregatorV3Interface(ethToUsdRinkbeyContractAddress);
        return priceFeed.version();
    }

    function getPrice() public view returns(uint256) {
        address ethToUsdRinkbeyContractAddress = 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e;
        AggregatorV3Interface priceFeed = AggregatorV3Interface(ethToUsdRinkbeyContractAddress);
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000); // convert eth to gwei
    }

    function getConversationRate(uint256 ethAmount) public view returns(uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice*ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    // change the behavior of a function in a declarative way
    modifier onlyOwner {
        require(msg.sender == owner, "You do not own the contract!");
        _;
    }

    // transfer balance of the contract to the owner of the contract
    function withdraw() public payable onlyOwner {
        require(msg.sender == owner, "You do not own the contract!");
        payable(msg.sender).transfer(address(this).balance);

        // reset
        for (uint256 funderIndex=0; funderIndex <  funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountPaidMap[funder] = 0;
        }
        funders = new address[](0);
    }
}