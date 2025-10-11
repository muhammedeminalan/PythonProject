from  abc import ABC, abstractmethod

class Car(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class Tesla(Car):
    def start(self):
        print("Tesla is starting")

    def stop(self):
        print("Tesla is stopping")

araba = Tesla()
araba.start()
araba.stop()