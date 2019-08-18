import random
import datetime
rand1 = random.random()
rand2 = random.randint(1,10)
print(rand1,rand2)


ru = str(rand1) + str(datetime.datetime.now())

print(ru)