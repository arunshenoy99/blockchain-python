"""Provides verification helper methods"""

from utility.hash_util import hash_block,hash_string_256
from wallet import Wallet
class Verification:
    @classmethod
    #VERIFY HASHES AND PROOF OF WORK'S
    def verify_chain(cls,blockchain):
        """Checks block hashes and proof of works and returns true or false based on success or failure"""
        for (index,block) in enumerate(blockchain):
            if(index == 0):
                continue
            if(block.previous_hash != hash_block(blockchain[index-1])):
                return False
            if (not cls.valid_proof(block.transactions[:-1],block.previous_hash,block.proof)):
                print('Proof is invalid')
                return False
        return True
    
    #VERIFY EACH TRANSACTION
    @classmethod
    def verify_transactions(cls,open_transactions,get_balance):
        """Verifies all the transactions and returns true if all are valid else false"""
        return all([cls.verify_transaction(tx,get_balance,False) for tx in open_transactions])
    
    #VERFIY THE TRANSACTION
    @staticmethod
    def verify_transaction(transaction,get_balance, check_funds=True):
        """Returns the boolean True if balance is greater than transaction amount else it returns false"""
        if check_funds == True:
            sender_balance = get_balance(transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            Wallet.verify_transaction(transaction)
    
    #DEFINE THE VALID PROOF OF WORK CRITERIA
    @staticmethod
    def valid_proof(transactions , last_hash , proof):
        """Checks if the given pow number is valid
        :transactions:The transactions of the block(open transactions if new block)
        :last_hash:The previous hash value of the block
        :proof:The pow number
        """
        guess = str(str([tx.to_ordered_dict() for tx in transactions])+str(last_hash)+str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == '00'
    