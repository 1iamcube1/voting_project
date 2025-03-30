const Voting = artifacts.require("Voting");

module.exports = function(deployer) {
    const candidateIds = [1, 2];
    const startTime = Math.floor(Date.now() / 1000); // Thời gian hiện tại
    const endTime = Math.floor(new Date('2025-01-15T23:59:59Z').getTime() / 1000); // Hết ngày 15/01/2025
    deployer.deploy(Voting, candidateIds, startTime, endTime);
};