from symtable import Class


class Musician:
    def __init__(self, name):
        self.name = name
        print("Musician init called")

    def test1(self):
        print("test1 from Musician")

    def test2(self):
        print("test2 from Musician")


class MusicianPlus(Musician):
    def __init__(self, name):
        Musician.__init__(self, name)
        print("MusicianPlus init called")

    # override etmek
    def test1(self):
        print("test1 from MusicianPlus")


atlas = MusicianPlus("atlas")
print(atlas.name)
atlas.test1()

#polimorphism
print("----------Polimorphism-------")
class Banana:
    def __init__(self, name):
        self.name = name
    def info(self):
        return  f"100 colorie {self.name}"

class Apple:
    def __init__(self, name):
        self.name = name
    def info(self):
        return  f"200 colorie {self.name}"
banana = Banana("banana")
apple = Apple("apple")
print(banana.info())
print(apple.info())
frutisList = [banana, apple]
for fruti in frutisList:
    print(fruti.info())

# encapsulation
print("----------Encapsulation-------")
class Phone:
    def __init__(self, name, price):
        self.name = name
        self.__price = price # private
    def info(self):
         print(f"{self.name} price is {self.__price}")
    def changePrice(self, price):
        self.__price = price

iphone = Phone("redmi", 100)
iphone.info()
iphone.__price = 100
print(iphone.__price) # dışarıdan erişim yok
iphone.info() # dışarıdan erişim yok
iphone.changePrice(200)
iphone.info() # dışarıdan erişim yok
