from vehicle import Vehicle
class Car(Vehicle):
    #top_speed = 100
    def brag(self):
        print('Dude im faster')
    def getData(self):
        print(self.top_speed)       #cant access warnings as private
car1 = Car(200)
car1.getData()