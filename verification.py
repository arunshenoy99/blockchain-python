from hash_util import hash_block,hash_string_256
class Verification:
    #VERIFY HASHES AND PROOF OF WORK'S
    def verify_chain(self,blockchain):
        """Checks block hashes and proof of works and returns true or false based on success or failure"""
        for (index,block) in enumerate(blockchain):
            if(index == 0):
                continue
            if(block.previous_hash != hash_block(blockchain[index-1])):
                return False
            if (not self.valid_proof(block.transactions[:-1],block.previous_hash,block.proof)):
                print('Proof is invalid')
                return False
        return True
    
    #VERIFY EACH TRANSACTION
    def verify_transactions(self,open_transactions,get_balance):
        """Verifies all the transactions and returns true if all are valid else false"""
        return all([self.verify_transaction(tx,get_balance) for tx in open_transactions])
    
    #VERFIY THE TRANSACTION
    def verify_transaction(self,transaction,get_balance):
        """Returns the boolean True if balance is greater than transaction amount else it returns false"""
        sender_balance = get_balance(transaction.sender)
        return sender_balance >= transaction.amount
    
    #DEFINE THE VALID PROOF OF WORK CRITERIA
    def valid_proof(self,transactions , last_hash , proof):
        """Checks if the given pow number is valid
        :transactions:The transactions of the block(open transactions if new block)
        :last_hash:The previous hash value of the block
        :proof:The pow number
        """
        guess = str(str([tx.to_ordered_dict() for tx in transactions])+str(last_hash)+str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == '00'
    