def first_function(*args):
    for (index,value) in enumerate(args):
        if(index==0):
            continue
        print('{:^20}'.format(args[0](value)))


first_function(lambda val:str(val*2),2,3,4,5,6)