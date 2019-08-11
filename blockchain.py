#Initializing the blockchain list
blockchain = []

def get_last_blockchain_value():
    """ returns the last value in the blockchain """
    return blockchain[-1]

def add_value(transaction_amount, last_transaction = [1]):
    blockchain.append([last_transaction,transaction_amount])

def get_user_input():
    return float(input('Please enter the transaction amount:'))

tx_amt = get_user_input()
add_value(tx_amt)
tx_amt = get_user_input()
add_value(tx_amt,get_last_blockchain_value())
tx_amt = get_user_input()
add_value(tx_amt,get_last_blockchain_value())

print(blockchain)