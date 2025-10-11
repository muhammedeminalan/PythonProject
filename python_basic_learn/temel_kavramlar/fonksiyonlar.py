def toplama(a, b):
    return a + b
def cikarma(a, b):
    return a - b
def carpma(a, b):
    return a * b
def bolme(a, b):
    if b != 0:
        return a / b
    else:
        return "Bir sayı sıfıra bölünemez"
print("Toplama:", toplama(5, 3))
print("Çıkarma:", cikarma(5, 3))
print("Çarpma:", carpma(5, 3))
print("Bölme:", bolme(5, 0))
print("Bölme:", bolme(5, 2))
print("Fonksiyon bloğu bitti")

def faktoriyel(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * faktoriyel(n - 1)
print("5! =", faktoriyel(5))
print("0! =", faktoriyel(0))
print("Faktöriyel fonksiyonu bitti")
def arg_sum(*args):
    return sum(args)
print("Arg sum:", arg_sum(1, 2, 3, 4, 5))
print("Arg sum:", arg_sum(10, 20))
print("Arg sum fonksiyonu bitti")
def kwargs_example(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
print("Kwargs example:")
kwargs_example(name="Ali", age=30, city="Istanbul")
print("Kwargs fonksiyonu bitti")
def default_param(a, b=10):
    return a + b
print("Default param:", default_param(5))
print("Default param:", default_param(5, 20))
print("Default param fonksiyonu bitti")
