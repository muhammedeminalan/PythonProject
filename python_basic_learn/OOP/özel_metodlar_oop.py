# Python özel (magic) metotların hepsini örnekleyen sınıf
# Amaç: her metodun ne işe yaradığını görmek
# Sınıfın adı: DemoClass

class DemoClass:
    # -----------------------------
    # 🔹 Nesne oluşturma
    def __new__(cls, *args, **kwargs):
        print("__new__ çağrıldı → nesne oluşturuluyor")
        return super().__new__(cls)  # Bellekte yer ayırır

    def __init__(self, name, value):
        print("__init__ çağrıldı → nesne başlatılıyor")
        self.name = name
        self.value = value

    def __del__(self):
        print(f"__del__ çağrıldı → {self.name} yok ediliyor")

    # -----------------------------
    # 🔹 String temsili
    def __repr__(self):
        # Geliştiriciye özel gösterim
        return f"DemoClass(name={self.name!r}, value={self.value!r})"

    def __str__(self):
        # Kullanıcı dostu gösterim
        return f"{self.name} ({self.value})"

    # -----------------------------
    # 🔹 Karşılaştırma operatörleri
    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    # -----------------------------
    # 🔹 Aritmetik operatörleri
    def __add__(self, other):
        print("__add__ çağrıldı (+)")
        return DemoClass(self.name + "+" + other.name, self.value + other.value)

    def __sub__(self, other):
        print("__sub__ çağrıldı (-)")
        return DemoClass(self.name + "-" + other.name, self.value - other.value)

    def __mul__(self, other):
        print("__mul__ çağrıldı (*)")
        return DemoClass(self.name + "*" + other.name, self.value * other.value)

    def __truediv__(self, other):
        print("__truediv__ çağrıldı (/)")
        return DemoClass(self.name + "/" + other.name, self.value / other.value)

    # -----------------------------
    # 🔹 İterasyon & koleksiyon davranışı
    def __getitem__(self, index):
        print("__getitem__ çağrıldı")
        return self.name[index]  # isme göre örnek

    def __len__(self):
        print("__len__ çağrıldı")
        return len(self.name)

    def __contains__(self, item):
        print("__contains__ çağrıldı")
        return item in self.name

    def __iter__(self):
        print("__iter__ çağrıldı")
        return iter(self.name)

    # -----------------------------
    # 🔹 Fonksiyon gibi çağırma
    def __call__(self, x):
        print("__call__ çağrıldı → nesne fonksiyon gibi kullanıldı")
        return self.value * x

    # -----------------------------
    # 🔹 Tür dönüşümleri
    def __int__(self):
        print("__int__ çağrıldı")
        return int(self.value)

    def __float__(self):
        print("__float__ çağrıldı")
        return float(self.value)

    def __bool__(self):
        print("__bool__ çağrıldı")
        return self.value != 0

    # -----------------------------
    # 🔹 Attribute işlemleri
    def __getattr__(self, name):
        print(f"__getattr__ çağrıldı → {name} yok")
        return f"{name} bulunamadı"

    def __setattr__(self, name, value):
        print(f"__setattr__ çağrıldı → {name} = {value}")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        print(f"__delattr__ çağrıldı → {name} siliniyor")
        super().__delattr__(name)

    # -----------------------------
    # 🔹 Context manager (with)
    def __enter__(self):
        print("__enter__ çağrıldı (with bloğuna girildi)")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__ çağrıldı (with bloğundan çıkıldı)")
        if exc_type:
            print(f"Hata yakalandı: {exc_type}")

    # -----------------------------
    # 🔹 Hash ve formatlama
    def __hash__(self):
        print("__hash__ çağrıldı")
        return hash((self.name, self.value))

    def __format__(self, spec):
        print("__format__ çağrıldı")
        return f"{self.name}:{self.value:{spec}}"


# ===========================================================
# 📌 ÖRNEK KULLANIMLAR
# ===========================================================

a = DemoClass("Bir", 10)
b = DemoClass("İki", 5)

print(a + b)        # __add__
print(a - b)        # __sub__
print(a * b)        # __mul__
print(a / b)        # __truediv__

print(len(a))       # __len__
print("i" in a)     # __contains__
print(a[0])         # __getitem__

print(a(3))         # __call__

print(int(a))       # __int__
print(bool(b))      # __bool__

print(a == b)       # __eq__
print(a > b)        # __gt__

with a as x:        # __enter__ ve __exit__
    print("with içindeyiz")

print(format(a, ".2f"))  # __format__

print(a.olmayanyer)  # __getattr__

del a.value          # __delattr__