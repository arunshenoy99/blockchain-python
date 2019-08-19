import functools
import hashlib
from collections import OrderedDict
import json

from hash_util import hash_block,hash_string_256
from block import Block
from transaction import Transaction
from verification import Verification

verifier = Verification()
#REWARD FOR THE MINER FOR MINIG A NEW BLOCK FROM THE OPEN TRANSACTIONS,PREVIOUS HASH AND INDEX
MINING_REWARD = 10
class Blockchain:
    def __init__(self , hosting_node_id):
        genesis_block = Block(0,'',[],100,0)
        self.chain = [genesis_block]
        self.open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

#SAVE THE BLOCKCHAIN DATA
    def save_data(self):
        """Saves the blockchain and open transactions as strings"""
        try:
            with open('blockchain.txt',mode = 'w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index,block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions],block_el.proof,block_el.timestamp) for block_el in self.chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_tx))
                #save_data = {
                    #'chain':blockchain,
                    #'ot':open_transactions
                #}
                #f.write(pickle.dumps(save_data))
        except (IOError,IndexError):
            print('Saving failed')

#LOAD THE BLOCKCHAIN DATA
    def load_data(self):
        try:
            with open('blockchain.txt', mode = 'r') as f:
                file_content = f.readlines()
                #file_content= pickle.loads(f.read())
                #blockchain = file_content['chain']
                #open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'],tx['recipient'],tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx,block['proof'],block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                self.open_transactions = json.loads(file_content[1])
                self.open_transactions = [Transaction(tx['sender'],tx['recipient'],tx['amount']) for tx in self.open_transactions]
        except (IOError,IndexError):
            pass

#GET THE BALANCE FOR A PARTICIPANT
    def get_balance(self):
        """ Returns the balance of the participant by considering sent and recieved amounts in previous transactions and open transactions
        """
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender==participant] for block in self.chain]
        open_tx_sender = [tx.amount for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum+sum(tx_amt) if len(tx_amt)>0 else tx_sum+0,tx_sender,0)
        tx_recieved = [[tx.amount for tx in block.transactions if tx.recipient==participant] for block in self.chain]
        amount_recieved = functools.reduce(lambda tx_sum,tx_amt: tx_sum+sum(tx_amt) if len(tx_amt)>0 else tx_sum+0,tx_recieved,0)
        return amount_recieved-amount_sent



#GENERATE THE VALID PROOF OF WORK
    def proof_of_work(self):
        """Generates the valid proof of work number"""
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not verifier.valid_proof(self.open_transactions , last_hash , proof):
            proof = proof+1
        return proof

#GET THE LAST BLOCK IN THE BLOCKCHAIN
    def get_last_blockchain_value(self):
        """Returns the last block in the blockchain"""
        if len(self.chain) < 1:
            return None
        return self.chain[-1]



#ADD A NEW TRANSACTION TO OPEN TRANSACTIONS
    def add_transaction(self,recipient , sender, amount = 1.0):
        """Adds the new transactions to the list of open transactions and returns boolean true or false based on completion status
        :recipient:The person who is the reciever
        :sender:The sender of the amount
        "amount:The amount to be sent
        """
        transaction = Transaction(sender,recipient,amount)
        if(verifier.verify_transaction(transaction,self.get_balance)):
            self.open_transactions.append(transaction)
            return True
        return False

#MINE A NEW BLOCK
    def mine_block(self):
        """Adds a new block to the blockchain after validation and proof of work"""
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)
        proof=self.proof_of_work()
        reward_transaction = Transaction('Mining',self.hosting_node,MINING_REWARD)
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.chain) , hashed_block , copied_transactions , proof)
        self.chain.append(block)
        self.open_transactions = []
        self.save_data()
        return True