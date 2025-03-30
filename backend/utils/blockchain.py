from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.defaultAccount = web3.eth.accounts[0]

contract_address = os.getenv('CONTRACT_ADDRESS')

contract_path = os.path.join(os.path.dirname(__file__), '../build/contracts/Voting.json')
with open(contract_path, encoding='utf-8') as f:
    contract_abi = json.load(f)['abi']

voting_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def is_voting_active():
    current_time = web3.eth.get_block('latest')['timestamp']
    start_time = voting_contract.functions.startTime().call()
    end_time = voting_contract.functions.endTime().call()
    return start_time <= current_time <= end_time

def vote(candidate_id, user_id):
    if not is_voting_active():
        raise Exception("Voting is not currently active. Please check the voting period.")
    tx_hash = voting_contract.functions.vote(candidate_id, user_id).transact({'from': web3.eth.defaultAccount})
    web3.eth.wait_for_transaction_receipt(tx_hash)

def get_votes_from_blockchain():
    votes = voting_contract.functions.getVotes().call()
    return [{"voter": vote[0], "candidate": vote[1]} for vote in votes]

def get_candidate_votes(candidate):
    return voting_contract.functions.getCandidateVotes(candidate).call()

def has_voted(user_id):
    return voting_contract.functions.hasVoted(user_id).call()

def get_total_voters():
    return voting_contract.functions.getTotalVoters().call()