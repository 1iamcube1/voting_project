// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    struct Vote {
        uint userId;
        uint candidate;
    }

    mapping(uint => uint) public candidateVotes;
    mapping(uint => uint) public userVotes;
    mapping(uint => bool) public validCandidates;
    uint public startTime;
    uint public endTime;

    event Voted(uint indexed userId, uint indexed candidate);

    constructor(uint[] memory candidateIds, uint _startTime, uint _endTime) {
        startTime = _startTime;
        endTime = _endTime;

        for (uint i = 0; i < candidateIds.length; i++) {
            candidateVotes[candidateIds[i]] = 0;
            validCandidates[candidateIds[i]] = true;
        }
    }

    modifier onlyDuringVotingPeriod() {
        require(block.timestamp >= startTime && block.timestamp <= endTime, "Voting is not active");
        _;
    }

    function vote(uint candidateId, uint userId) public onlyDuringVotingPeriod {
        require(validCandidates[candidateId], "Invalid candidate");

        
        if (userVotes[userId] != 0) {
            candidateVotes[userVotes[userId]] -= 1;
        }

        
        userVotes[userId] = candidateId;
        candidateVotes[candidateId] += 1;

        emit Voted(userId, candidateId);
    }

    function hasVoted(uint userId) public view returns (bool) {
        return userVotes[userId] != 0;
    }

    function getVotes() public view returns (Vote[] memory) {
        // Implement logic to return all votes
    }

    function getCandidateVotes(uint candidateId) public view returns (uint) {
        return candidateVotes[candidateId];
    }
}