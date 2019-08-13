names = ['John','JessicaN','Jen','num','Andrew','Maximus','Nadia']

for name in names:
    if len(name)>5 and ('n' in name or 'N' in name):
        print(name)
while len(names)>0:
    names.pop()
print(names)

