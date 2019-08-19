from verification import Verification
from blockchain import Blockchain
from uuid import uuid4
verifier = Verification()
class Node:
    def __init__(self):
        self.id = uuid4()
        self.blockchain = Blockchain(self.id)
        self.listen_for_input()
    def listen_for_input(self):
        #BLOCKCHAIN COMMAND LINE INTERFACE
        while True:
            print('Please choose')
            print('1.Add a new transaction value')
            print('2.Mine a block')
            print('3.Print the blocks')
            print('4.Check transactions validity')
            print('q.Quit')
            user_choice=self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient , amount = tx_data
                if(self.blockchain.add_transaction(recipient , amount = amount , sender=self.id)):
                    print('Added Transaction')
                    self.blockchain.save_data()
                else:
                    print('Transaction failed')
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if verifier.verify_transactions(self.blockchain.open_transactions,self.blockchain.get_balance):
                    print('Transactions are valid')
                else:
                    print('Transactions are not valid')
            elif user_choice == 'q':
                break
            else:
                print('Invalid choice')
            if not verifier.verify_chain(self.blockchain.chain):
                print('Invalid Blockchain')
                break    
            print('Balance of {} is {:6.2f}'.format(self.id,self.blockchain.get_balance()))                  
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

node = Node()