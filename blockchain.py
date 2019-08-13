#Initializing the blockchain list
genesis_block = {
    'previous_hash':'',
    'index':0,
    'transactions':[]
}
blockchain = []
open_transactions = []
owner = 'Arun'

blockchain.append(genesis_block)

#Get the last block data from a blockchain

def get_last_blockchain_value():
    """ returns the last value in the blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

#Add a new transavtion to the blockchain

def add_value(recipient , sender = owner, amount = 1.0):
    """append a new value as well as the last blockchain value to the blockchain
    Arguments:
    :sender: The sender of the coins
    :reciever: The reciever of the coins
    :amount: The amount of coins to be sent

    """
    transaction = {
        'sender':sender,
        'recipient':recipient,
        'amount':amount
    }
    open_transactions.append(transaction)




def mine_block():
    last_block = blockchain[-1]
    hashed_block = ''
    for key in last_block:
        value = last_block[key]
        hashed_block = hashed_block + str(value)
    block = {
        'previous_hash':hashed_block,
        'index':len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)
 
#Get transaction amount from the user
def get_transaction_value():
    """ returns the user input transaction amount in float"""
    tx_recipient = input('Recipient')
    tx_amount = float(input('Enter the amount:'))
    transaction = (tx_recipient,tx_amount)
    return transaction

#Get the user choice
def get_user_choice():
    return input('Your Choice:')

#Output the blockchain blocks
def print_blockchain_elements():
    print('Outputting blockchain')
    for block in blockchain:
        print(block)

#Verify the blockchain
def verify_chain():
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        if blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    return is_valid


#Get subsequent transactions and add to blockchain

while True:
    print('Please choose')
    print('1.Add a new transaction value')
    print('2.Mine a block')
    print('3.Print the blocks')
    print('h:Manipulate the blockchain')
    print('q.Quit')
    user_choice=get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient , amount = tx_data
        add_value(recipient , amount = amount)
        print(open_transactions)
    elif user_choice == '2':
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'q':
        break
    elif user_choice == 'h':
        if len(blockchain) >=1:
            blockchain[0] = 3.3
    else:
        print('Invalid choice')
    #if not verify_chain():
     #   print('Invalid Blockchain')
      #  break                      

print('Done')