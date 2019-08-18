import pickle,json
text_list = []
while True:
    print('1.Enter data')
    print('2.Load data')
    print('q.Quit')
    user_choice = input('Choice:')
    if user_choice == '1':
        text = input('Enter the text:')
        text_list.append(text)
        with open('demo.txt', 'w') as f:
            f.write(json.dumps(text_list))
        with open('demo.p','wb') as f:
            f.write(pickle.dumps(text_list))
    elif user_choice == '2':
        with open('demo.txt','r') as f:
            file_content = json.loads(f.read())
            print(file_content)
        with open ('demo.p','rb') as f:
            file_content = pickle.loads(f.read())
            print(file_content)
    elif user_choice == 'q':
        break
