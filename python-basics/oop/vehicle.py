class Vehicle:
    def __init__(self,value = 100):
        self.top_speed = value
        self.__warnings = []        #PRIVATE VARIABLE HAS DOUBLE UNDERSCORE BEFORE NAME
    def __repr__(self):
        return 'printing'
    def drive(self):
        print('I am driving but not faster than {}'.format(self.top_speed))
    def add_warning(self):
        self.__warnings.append('Lol')