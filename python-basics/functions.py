def unlimited_arguments(*args):
    for argument in args:
        print(argument)

unlimited_arguments(1,2,3,4)
unlimited_arguments(*[5,6,7,8])