persons = [
{'name':'Jen','age':21,'hobbies':['swimming','badminton']},
{'name':'Jock','age':30,'hobbies':['cricket']},
{'name':'Jess','age':25,'hobbies':['football','swimming']}]

person_names = [person['name'] for person in persons]
print(person_names)

print(all([person['age']>20 for person in persons]))

copied_persons = [person.copy() for person in persons]
copied_persons[0]['name'] = 'Max'
print(persons)
print(copied_persons)

a,b,c = persons
print(a)
print(b)
print(c)