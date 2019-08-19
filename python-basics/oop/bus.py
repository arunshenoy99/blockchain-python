from vehicle import Vehicle

class Bus(Vehicle):
    def __init__(self,starting_top_speed):
        super().__init__(starting_top_speed)
        self.passengers = []
    def add_group(self):
        self.passengers.extend('Lol')
    def get_data(self):
        print(self.top_speed,self.passengers)

bus1 = Bus(50)
bus1.add_warning()
bus1.get_data()