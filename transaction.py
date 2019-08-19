from collections import OrderedDict
from printable import Printable
class Transaction(Printable):
    def __init__(self, sender, recipient , amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    
    def __repr__(self):
        return str(self.__dict__)

    def to_ordered_dict(self):
        return OrderedDict([('sender',self.sender),('reciever',self.recipient),('amount',self.amount)])