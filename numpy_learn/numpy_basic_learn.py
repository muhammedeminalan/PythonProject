import numpy as np

# -----------------------------
# NumPy array oluşturma
# -----------------------------
my_list = [1, 2, 3, 4, 5]

# Python listesi türü
print(type(my_list))

# Listeyi NumPy array’e dönüştürme
np.array(my_list)

# Hâlâ orijinal Python listesi
print(type(my_list))

# NumPy array değişkeni oluşturma
my_numpy_array = np.array(my_list)
print(type(my_numpy_array))

# Array içeriğini yazdır
print(my_numpy_array)

# Elemanlara erişim
print(my_numpy_array[0])  # ilk eleman
print(my_numpy_array[1])  # ikinci eleman

# Eleman değiştirme
my_numpy_array[0] = 10
print(my_numpy_array)

# Temel istatistiksel işlemler
print("max :", my_numpy_array.max())    # maksimum değer
print("min :", my_numpy_array.min())    # minimum değer
print("mean :", my_numpy_array.mean())  # ortalama

# -----------------------------
# 2 Boyutlu NumPy Matris
# -----------------------------
my_matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12]
])

print(my_matrix)

# Satır ve eleman erişimi
print(my_matrix[0])        # ilk satır
print(my_matrix[0][1])     # ilk satır, ikinci eleman
print(my_matrix[1, 2])     # 2. satır, 3. sütun

# NumPy matris bilgisi
numpy_matrix_list = np.array(my_matrix)
print("numpy array :", numpy_matrix_list)
print("Shape (satır, sütun):", numpy_matrix_list.shape)

# -----------------------------
# Arange (sıralı sayılar oluşturma)
# -----------------------------
print("-------------- arange ----------------")
# np.arange(start, stop, step)
# Belirtilen aralıkta düzenli sayılar üretir (stop dahil değil)

my_arange = np.arange(0, 10)
print(my_arange)

my_arange2 = np.arange(5, 20, 2)
print(my_arange2)

# -----------------------------
# Sıfırlardan oluşan matris
# -----------------------------
print(np.zeros((3, 4)))  # 3x4’lük sıfırlardan oluşan matris

# Birlerden oluşan matris
print(np.ones((2, 3)))   # 2x3’lük birlerden oluşan matris

# Eşit aralıklı sayılar üretme
print(np.linspace(0, 100, 5))  # 0’dan 100’e kadar 5 eşit aralık

# Rastgele sayılar (0-1 arasında)
print(np.random.rand(3, 3))    # 3x3 matris

# Normal dağılımlı rastgele sayılar
print(np.random.randn(4, 4))   # 4x4 matris

# Rastgele tam sayılar
print(np.random.randint(0, 10, 5))    # 0–10 arası 5 sayı
print(np.random.randint(0, 100, 10))  # 0–100 arası 10 sayı