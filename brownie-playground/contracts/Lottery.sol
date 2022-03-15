// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

// the ownable abstract contract provides the onlyOwner modifier
// that sets the access right to owner only
contract Lottery is Ownable, VRFConsumerBase {

    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE { OPEN, CLOSED, CALCULATING_WINNER }
    LOTTERY_STATE public lotteryState;

    // variables from VRFConsumerBase
    uint256 public fee;
    bytes32 public keyhash;
    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lotteryState = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(lotteryState == LOTTERY_STATE.OPEN);
        require(msg.value > getEntranceFee(), "Not enough fee to enter!");
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns(uint256) {
        (,int256 price,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10 ** 10; // convert to gwei (18 decimals)
        return (usdEntryFee * 10**18) / adjustedPrice;
    }

    // only the owner can start the lottery
    function startLottery() public onlyOwner {
        require(lotteryState == LOTTERY_STATE.CLOSED, "Can't start the lottery yet!");
        lotteryState = LOTTERY_STATE.OPEN;
    }

    // only the owner can close the lottery
    function endLottery() public onlyOwner {

        // insecure practice
        // uint256(
        //     keccak256(
        //         abi.encodePacked(
        //             nonce, // predictable
        //             msg.sender, // predictable
        //             block.difficulty, // can be manipulated
        //             block.timestamp // predictable
        //         )
        //     )
        // ) % players.length;

        lotteryState = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);
        emit RequestedRandomness(requestId);
    }

    // callback of the VRF contract
    function fulfillRandomness(bytes32 requestId, uint256 _randomness) internal override {
        require(lotteryState == LOTTERY_STATE.CALCULATING_WINNER, "Incorrect lottery state.");
        require(randomness > 0, "random-not-found");

        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);

        // reset
        players = new address payable[](0);
        lotteryState = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }

}