import functools

#Initializing the blockchain list

MINING_REWARD = 10

genesis_block = {
    'previous_hash':'',
    'index':0,
    'transactions':[]
}
blockchain = []
open_transactions = []
owner = 'Arun'
participants = {owner}

blockchain.append(genesis_block)

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender']==participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum+tx_amt[0] if len(tx_amt)>0 else 0,tx_sender,0)
    tx_recieved = [[tx['amount'] for tx in block['transactions'] if tx['recipient']==participant] for block in blockchain]
    amount_recieved = functools.reduce(lambda tx_sum,tx_amt: tx_sum+tx_amt[0] if len(tx_amt)>0 else 0,tx_recieved,0)
    return amount_recieved-amount_sent
#Get the last block data from a blockchain

def get_last_blockchain_value():
    """ returns the last value in the blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']



#Add a new transaction to the blockchain

def add_transaction(recipient , sender = owner, amount = 1.0):
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
    if(verify_transaction(transaction)):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False




def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender':'MINING',
        'recipient':owner,
        'amount':MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash':hashed_block,
        'index':len(blockchain),
        'transactions': copied_transactions
    }
    blockchain.append(block)
    return True
 
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
    for (index,block) in enumerate(blockchain):
        if(index == 0):
            continue
        if(block['previous_hash'] != hash_block(blockchain[index-1])):
            return False
    return True

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])

#Get subsequent transactions and add to blockchain

while True:
    print('Please choose')
    print('1.Add a new transaction value')
    print('2.Mine a block')
    print('3.Print the blocks')
    print('4.Check transactions validity')
    print('h:Manipulate the blockchain')
    print('q.Quit')
    user_choice=get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient , amount = tx_data
        if(add_transaction(recipient , amount = amount)):
            print('Added Transaction')
        else:
            print('Transaction failed')
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        if verify_transactions():
            print('Transactions are valid')
        else:
            print('Transactions are not valid')
    elif user_choice == 'q':
        break
    elif user_choice == 'h':
        if len(blockchain) >=1:
            blockchain[0] = genesis_block = {'previous_hash':'','index':0,'transactions':[{'sender':'Chris','recipient':'Jess','amount':100}]}
    else:
        print('Invalid choice')
    if not verify_chain():
        print('Invalid Blockchain')
        break    
    print('Balance of {} is {:6.2f}'.format(owner,get_balance(owner)))                  

print('Done')