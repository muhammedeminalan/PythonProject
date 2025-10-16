import requests

url = "https://jsonplaceholder.typicode.com/posts/"
empty_list=[]
# İlk 5 postu listele
response = requests.get(url)

if response.status_code == 200:
    posts = response.json()
    for post in posts[:5]:  # ilk 5 postu al
        print(f"Post ID: {post['id']}, Başlık: {post['title']}")
else:
    print("Veri alınamadı:", response.status_code)

print("--------------------------------------------------------------------------------------")

# Tek bir postu kullanıcıdan alıp gösteren fonksiyon
def fetch_data(url):
    post_id = input("Post ID giriniz: ").strip()  # kullanıcıdan id al
    try:
        response = requests.get(f"{url}{post_id}")  # güvenli birleştirme
        response.raise_for_status()  # hata varsa fırlat
        return response.json()
    except requests.RequestException as e:
        print("Veri alınırken hata oluştu:", e)
        return None

# Fonksiyonu çağır ve sonucu ekrana yazdır
veri = fetch_data(url)

if veri:
    print("\n--- Post Detayları ---")
    print(f"Post ID: {veri['id']}")
    print(f"Başlık: {veri['title']}")
    print(f"İçerik: {veri['body']}")
else:
    print("Post bulunamadı veya veri alınamadı.")

empty_list.append(fetch_data(url))
print(f" list : {empty_list}")