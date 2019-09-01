class Food:
    def __init__(self,name,kind):
        self.name = name
        self.kind = kind
    def describe(self):
        print('Name:{} and Kind:{}'.format(self.name,self.kind))

    def __repr__(self):
        return '{} and {}'.format(self.name,self.kind)


class Meat(Food):
    def cook(self):
        print('Cooking')


class Fruit(Food):
    def clean(self):
        print('Cleaning')


f1 = Food('Nuts','nuts')
print(f1)

m1 = Meat('Chicken','chicken')
m1.describe()
m1.cook()
print(m1)

fr1 = Fruit('Apple','Winter fruits')
fr1.describe()
fr1.clean()
print(fr1)