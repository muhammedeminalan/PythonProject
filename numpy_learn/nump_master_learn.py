import numpy as np

# ==========================================================
# 1️⃣ ARRAY OLUŞTURMA
# ==========================================================
# Normal Python listesi
python_list = [1, 2, 3, 4, 5]

# Listeyi NumPy array'e dönüştür
arr = np.array(python_list)
print("Array:", arr)
print("Tür:", type(arr))

# Çok boyutlu array (matris)
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print("Matris:\n", matrix)

# Sıfırlardan oluşan array
zeros = np.zeros((2, 4))
print("Sıfır matrisi:\n", zeros)

# Birlerden oluşan array
ones = np.ones((3, 3))
print("Bir matrisi:\n", ones)

# Belirli aralıkta sayılar
arange_arr = np.arange(0, 10, 2)
print("Arange array:", arange_arr)

# Eşit aralıklı sayılar
linspace_arr = np.linspace(0, 1, 5)
print("Linspace array:", linspace_arr)

# Rastgele sayı üretimi
rand_arr = np.random.rand(3, 3)
print("Rastgele (0-1):\n", rand_arr)

rand_ints = np.random.randint(0, 50, 5)
print("Rastgele tam sayılar:", rand_ints)

# ==========================================================
# 2️⃣ TEMEL ARRAY ÖZELLİKLERİ
# ==========================================================
print("Shape (boyut):", matrix.shape)
print("Boyut sayısı:", matrix.ndim)
print("Eleman tipi:", matrix.dtype)
print("Eleman sayısı:", matrix.size)

# ==========================================================
# 3️⃣ İNDEKSLEME ve DİLİMLEME
# ==========================================================
arr2 = np.arange(10, 20)
print("Array:", arr2)

print("İlk eleman:", arr2[0])
print("Son eleman:", arr2[-1])
print("İlk 3 eleman:", arr2[:3])
print("Son 3 eleman:", arr2[-3:])
print("2'den 8'e kadar 2'şer artış:", arr2[2:9:2])

# Matris dilimleme
mat = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])
print("Matris:\n", mat)
print("İlk satır:", mat[0])
print("İkinci satır, üçüncü sütun:", mat[1, 2])
print("Alt matris:\n", mat[:2, 1:])

# ==========================================================
# 4️⃣ MATEMATİKSEL İŞLEMLER
# ==========================================================
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("Toplama:", a + b)
print("Çıkarma:", a - b)
print("Çarpma:", a * b)
print("Bölme:", a / b)
print("Kare alma:", a ** 2)

# Evrensel fonksiyonlar (ufuncs)
print("Karekök:", np.sqrt(a))
print("Sinüs:", np.sin(a))
print("Logaritma:", np.log(a))

# ==========================================================
# 5️⃣ İSTATİSTİKSEL İŞLEMLER
# ==========================================================
nums = np.array([5, 10, 15, 20, 25])
print("Toplam:", nums.sum())
print("Ortalama:", nums.mean())
print("Maksimum:", nums.max())
print("Minimum:", nums.min())
print("Standart sapma:", nums.std())
print("Varyans:", nums.var())

# Axis kullanımı (satır/sütun işlemleri)
big_mat = np.array([[1, 2, 3], [4, 5, 6]])
print("Sütun ortalaması:", big_mat.mean(axis=0))  # dikey
print("Satır ortalaması:", big_mat.mean(axis=1))  # yatay

# ==========================================================
# 6️⃣ MATRİS İŞLEMLERİ (Lineer Cebir)
# ==========================================================
matA = np.array([[1, 2], [3, 4]])
matB = np.array([[5, 6], [7, 8]])

# Matris çarpımı
print("Matris çarpımı (A @ B):\n", matA @ matB)

# Transpoze (satır ↔ sütun)
print("A Transpoze:\n", matA.T)

# Determinant
print("Determinant:", np.linalg.det(matA))

# Ters matris (inverse)
print("Ters matris:\n", np.linalg.inv(matA))

# Özdeğer ve özvektörler
vals, vecs = np.linalg.eig(matA)
print("Özdeğerler:", vals)
print("Özvektörler:\n", vecs)

# ==========================================================
# 7️⃣ RASTGELE ve TEKRARLANABİLİR SAYILAR
# ==========================================================
np.random.seed(42)  # aynı sayıları üretmek için sabitle
rand1 = np.random.randint(0, 100, 5)
rand2 = np.random.randint(0, 100, 5)
print("Seed kullanılmış rastgele sayılar:", rand1, rand2)

# ==========================================================
# 8️⃣ BOOLEAN FİLTRELEME
# ==========================================================
arr3 = np.arange(1, 10)
print("Array:", arr3)

# 5'ten büyük elemanları bul
print("5'ten büyükler:", arr3[arr3 > 5])

# Çift sayılar
print("Çift sayılar:", arr3[arr3 % 2 == 0])

# Koşullu atama
arr3[arr3 > 5] = 99
print("Koşullu değiştirme:", arr3)

# ==========================================================
# 9️⃣ SHAPE DEĞİŞTİRME (reshape)
# ==========================================================
data = np.arange(1, 13)
reshaped = data.reshape(3, 4)
print("3x4 matris:\n", reshaped)

# Flatten (tek boyut yapma)
flat = reshaped.flatten()
print("Flatten edilmiş:", flat)

# ==========================================================
# 🔟 KOPYALAMA ve GÖNDERME
# ==========================================================
original = np.array([1, 2, 3])
copy_arr = original.copy()
copy_arr[0] = 99

print("Orijinal:", original)
print("Kopya:", copy_arr)