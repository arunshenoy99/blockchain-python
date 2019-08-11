name = 'Arun'

def greeting(age):
    global name
    name = 'Jess'
    print('Hello '+name+' your age is '+str(age))
greeting(age=29)
print(name)
