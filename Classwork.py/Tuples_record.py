from collections import namedtuple

Record = namedtuple('Person',['name', 'age'])

person1 = Record(name="Alice in chains", age=215)
person2 = Record(name="Who the is Alice", age=252)
person3 = Record(name="Alice in wonderland", age=25)


print(person2.name)
print(person1.age)
print(person3.name)