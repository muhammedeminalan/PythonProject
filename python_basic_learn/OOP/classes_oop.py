class Person:
    #properties
    # properties tanımlamaak bile inite algılar otomatik yazmaya gerek yok keyfi parametre
    name=""
    age=0
    gender=""
    # constructor
    # self: instance of the class
    # sefl->this anllamına gelir.
    #__init__ -> constructor anlamına geliyor.

    def __init__(self, name, age, gender):
        print("person init called")
        self.name=name
        self.age=age
        self.gender=gender
    def denemeFnc(self):
        self.age=18
        print("deneme fnc called")
x=Person("Ahmet", 25,gender="male" )
print(x.name)
x.name="Ali"
print(x.name)
print(x.denemeFnc())

class Dog:
    year=7
    def __init__(self,age=5):
        self.age=age
        self.dogHumanAge=self.year
    def humanAge(self):
        return self.age*7
myDog = Dog(25)
print(myDog.humanAge())
print(myDog.age)
print(myDog.dogHumanAge)