from utility.verification import Verification
from blockchain import Blockchain
from uuid import uuid4
from wallet import Wallet
class Node:
    def __init__(self):
        #self.wallet.public_key = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)
        self.listen_for_input()
    def listen_for_input(self):
        #BLOCKCHAIN COMMAND LINE INTERFACE
        while True:
            print('Please choose')
            print('1.Add a new transaction value')
            print('2.Mine a block')
            print('3.Print the blocks')
            print('4.Check transactions validity')
            print('5.Create Wallet')
            print('6.Load Wallet')
            print('7.Save Keys')
            print('q.Quit')
            user_choice=self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient , amount = tx_data
                signature = self.wallet.sign_transaction(self.wallet.public_key , recipient , amount)
                if(self.blockchain.add_transaction(recipient,signature=signature, amount = amount , sender=self.wallet.public_key)):
                    print('Added Transaction')
                    self.blockchain.save_data()
                else:
                    print('Transaction failed')
            elif user_choice == '2':
                if not self.blockchain.mine_block():
                    print('Mining failed got no wallet')
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(),self.blockchain.get_balance):
                    print('Transactions are valid')
                else:
                    print('Transactions are not valid')
            elif user_choice == '5':
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '6':
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == '7':
                self.wallet.save_keys()
            elif user_choice == 'q':
                break
            else:
                print('Invalid choice')
            if not Verification.verify_chain(self.blockchain.chain):
                print('Invalid Blockchain')
                break    
            print('Balance of {} is {:6.2f}'.format(self.wallet.public_key,self.blockchain.get_balance()))                  
        print('Done')
    #GET A TRANSACTION
    def get_transaction_value(self):
        """Returns the user input transaction amount in float"""
        tx_recipient = input('Recipient')
        tx_amount = float(input('Enter the amount:'))
        transaction = (tx_recipient,tx_amount)
        return transaction

    #GET THE USER CHOICE OF THE MENU
    def get_user_choice(self):
        """retunrs the user choice"""
        return input('Your Choice:')

    #OUTPUT THE BLOCKCHAIN ELEMENTS
    def print_blockchain_elements(self):
        """prints the blockchain elements"""
        print('Outputting blockchain')
        for block in self.blockchain.chain:
            print(block)

if __name__ == '__main__':
    node = Node()