import functools
import hashlib
from collections import OrderedDict
import json
import requests

from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

#REWARD FOR THE MINER FOR MINIG A NEW BLOCK FROM THE OPEN TRANSACTIONS,PREVIOUS HASH AND INDEX
MINING_REWARD = 10
class Blockchain:
    def __init__(self,public_key,node_id):
        genesis_block = Block(0,'',[],100,0)
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.__peer_nodes = set()
        self.public_key = public_key
        self.node_id = node_id
        self.load_data()
        
    
    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self,val):
        self.__chain = val

#SAVE THE BLOCKCHAIN DATA
    def save_data(self):
        """Saves the blockchain and open transactions as strings"""
        try:
            with open('blockchain-{}.txt'.format(self.node_id),mode = 'w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index,block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions],block_el.proof,block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                #save_data = {
                    #'chain':blockchain,
                    #'ot':open_transactions
                #}
                #f.write(pickle.dumps(save_data))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
        except (IOError,IndexError):
            print('Saving failed')

#LOAD THE BLOCKCHAIN DATA
    def load_data(self):
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode = 'r') as f:
                file_content = f.readlines()
                #file_content= pickle.loads(f.read())
                #blockchain = file_content['chain']
                #open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'],tx['recipient'],tx['amount'],tx['signature']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx,block['proof'],block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                self.__open_transactions = json.loads(file_content[1][:-1])
                self.__open_transactions = [Transaction(tx['sender'],tx['recipient'],tx['amount'],tx['signature']) for tx in self.__open_transactions]
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError,IndexError):
            pass

#GET THE BALANCE FOR A PARTICIPANT
    def get_balance(self,sender=None):
        """ Returns the balance of the participant by considering sent and recieved amounts in previous transactions and open transactions
        """
        if sender == None:
            if self.public_key == None:
                return None
            participant = self.public_key
        else:
            participant = sender
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender==participant] for block in self.__chain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum+sum(tx_amt) if len(tx_amt)>0 else tx_sum+0,tx_sender,0)
        tx_recieved = [[tx.amount for tx in block.transactions if tx.recipient==participant] for block in self.__chain]
        amount_recieved = functools.reduce(lambda tx_sum,tx_amt: tx_sum+sum(tx_amt) if len(tx_amt)>0 else tx_sum+0,tx_recieved,0)
        return amount_recieved-amount_sent



#GENERATE THE VALID PROOF OF WORK
    def proof_of_work(self):
        """Generates the valid proof of work number"""
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions , last_hash , proof):
            proof = proof+1
        return proof

#GET THE LAST BLOCK IN THE BLOCKCHAIN
    def get_last_blockchain_value(self):
        """Returns the last block in the blockchain"""
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]



#ADD A NEW TRANSACTION TO OPEN TRANSACTIONS
    def add_transaction(self,recipient,sender,signature,amount = 1.0,is_recieving = False):
        """Adds the new transactions to the list of open transactions and returns boolean true or false based on completion status
        :recipient:The person who is the reciever
        :sender:The sender of the amount
        "amount:The amount to be sent
        """
        if(self.public_key == None):
            return False
        transaction = Transaction(sender,recipient,amount,signature=signature)
        if(Verification.verify_transaction(transaction,self.get_balance)):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_recieving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={'sender':sender,'recipient':recipient,'amount':amount,'signature:':signature})
                        if response.status_code == 400 or response.status_code == 500:
                            print('Transaction declined needs resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
                return True
            return False

#MINE A NEW BLOCK
    def mine_block(self):
        """Adds a new block to the blockchain after validation and proof of work"""
        if(self.public_key == None):
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof=self.proof_of_work()
        reward_transaction = Transaction('Mining',self.public_key,MINING_REWARD,'')
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain) , hashed_block , copied_transactions , proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block
    
    def get_open_transactions(self):
        return self.__open_transactions
    
    def add_peer_node(self,node):
        """ Adds a new node to peer_nodes """
        self.__peer_nodes.add(node)
        self.save_data()
    
    def remove_peer_node(self,node):
        """Remove a node from peer node set """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        return (list(self.__peer_nodes))[:]