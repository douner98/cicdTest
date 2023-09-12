#from operator import itemgetter
import operator
#import operator

students = [
    ("jane", 22, 'A'),
    ("dave", 32, 'B'),
    ("sally", 17, 'B'),
]

result = sorted(students, key=operator.itemgetter(1))
print(result)

def sub(a, b):
    return a - b

result = sub(a=7, b=3)  # a에 7, b에 3을 전달
print(result)

result = sub(7, 2)  # a에 7, b에 3을 전달
print(result)

def add_many(*args): 
    result = 0 
    for i in args: 
        result = result + i 
    return result 

result = add_many(1,2,3,4,5)
print(result)

def add_mul(choice, *args): 
    if choice == "add": 
        result = 0 
        for i in args: 
            result = result + i 
    elif choice == "mul": 
        result = 1 
        for i in args: 
            result = result * i 
    return result 

result = add_mul('mul', 1,2,3,4,5)
print(result)

def print_kwargs(**kwargs):
    return kwargs

kkk = print_kwargs(name='foo', age=3)
print(kkk['name'])

print('na2me' in kkk)

