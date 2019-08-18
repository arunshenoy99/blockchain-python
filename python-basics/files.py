f = open('demos.txt', mode = 'a')
f.write('This is a text string!\n')
f.close()

f = open('demos.txt', mode = 'r')
#file_content = f.readlines()
#for line in file_content:
   # print(line[:-1])

line = f.readline()
while line:
    print(line[:-1])
    line = f.readline()
f.close()