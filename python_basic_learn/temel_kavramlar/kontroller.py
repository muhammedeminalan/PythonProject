x = 5
y = 2

if x == 5:
    for i in range(5):
        if y == i:
            print("x 5 e eşit ve y i ye eşit")
            break
elif x > 5:
    print("x 5 ten büyük")
else:
    print("x 5 ten küçük")
print("if bloğu bitti")

for i in range(5):
    if i == 3:
        print("i 3 e eşit")
print("for bloğu bitti")
while x > 0:
    print("x:", x)
    x -= 1
print("while bloğu bitti")
def kontrol_et(sayi):
    if sayi % 2 == 0:
        return "Çift"
    else:
        return "Tek"
for i in range(10):
    if kontrol_et(i):
        print(f"{i} sayısı {kontrol_et(i)}")

print(kontrol_et(4))
print(kontrol_et(7))
print("fonksiyon bloğu bitti")