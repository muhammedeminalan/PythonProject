# Bu dosya, aynı kaynaktan veri çekmeyi senkron (tek iş parçacığı) ve çoklu iş parçacığı (threading) ile karşılaştırır.
# Amaç: Basit bir örnek üzerinden zaman kazancını görmek ve temel threading kullanımını göstermek.

import threading  # Python'un yerleşik çoklu iş parçacığı (thread) kütüphanesi
import requests   # HTTP istekleri için popüler kütüphane
import time       # Zaman ölçümü (başlangıç/bitiş) için kullanılır
import asyncio
import aiohttp

# Senkron (tek iş parçacığı) veri çekme örneği
# Not: Aşağıdaki fonksiyon her URL için sırayla (peş peşe) istek atar.
# List comprehension ile kısa yazılmıştır; her istek tamamlanmadan diğeri başlamaz.
def get_data_async(urls):
    st = time.time()  # Başlangıç zamanı
    json_array = [requests.get(url).json() for url in urls]  # Her URL için GET isteği at ve JSON dön
    et = time.time()  # Bitiş zamanı
    print(f"Elapsed Time without threading: {et - st} seconds")  # Toplam süreyi yazdır
    return json_array  # JSON yanıtlar listesi


# Çoklu iş parçacığı ile paralel veri çekme için Thread sınıfı
class ThreadingDownloader(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url      # Bu thread'in indireceği URL
        self.result = None  # Sonuç (JSON) burada tutulacak

    def run(self):
        # Thread başlatıldığında çalışan metod (iş mantığı burada)
        response = requests.get(self.url)  # İstek atılır (bloklayıcı çağrı)
        self.result = response.json()      # JSON sonuç saklanır


# Çoklu iş parçacığı ile birden fazla URL'yi aynı anda indirir
# Adımlar:
# 1) Her URL için bir ThreadingDownloader oluştur ve başlat
# 2) Bütün thread'lerin bitmesini bekle (join)
# 3) Her thread'in ürettiği sonucu topla ve geri döndür
def getDataThreading(urls):
    st = time.time()  # Başlangıç zamanı
    threads = []      # Oluşturulan thread'leri tutacağımız liste

    for url in urls:
        t = ThreadingDownloader(url)  # Thread oluştur
        t.start()                      # Çalıştır (run çağrılır)
        threads.append(t)              # Listeye ekle

    results = []  # Toplanacak sonuçlar
    for t in threads:
        t.join()               # Thread tamamlanana kadar bekle
        results.append(t.result)  # Üretilen sonucu al

    et = time.time()  # Bitiş zamanı
    print(f"Elapsed Time with threading: {et - st} seconds")  # Toplam süreyi yazdır
    return results  # JSON sonuçlar listesi


aSYNCIO_SECTION_MARK = True  # edit yardımcısı için imza (işlevsel değil)

# Asenkron (asyncio + aiohttp) yaklaşım
# Notlar:
# - asyncio: Python'un asenkron programlama çatısıdır. Tek iş parçacığında birden fazla bekleme (I/O) işini aynı anda sürdürebilir.
# - aiohttp: HTTP isteklerini asenkron şekilde göndermeyi sağlar. 'await' ile non-blocking çağrılar yapılır.
# Avantaj: Çok sayıda HTTP isteğinde, threading'e göre daha az overhead ile yüksek eşzamanlılık sağlayabilir.

async def fetch_json(session: aiohttp.ClientSession, url: str):
    """Tek bir URL'den JSON döndüren asenkron yardımcı fonksiyon.
    Hata durumunda anlaşılır bir dict döner.
    """
    try:
        # session.get() asenkron bir çağrıdır; yanıt gelene kadar başka görevler çalıştırılabilir
        async with session.get(url) as resp:
            resp.raise_for_status()  # HTTP 4xx/5xx ise hata fırlatır
            return await resp.json()  # Yanıt gövdesini JSON olarak parse et
    except Exception as e:
        return {"error": str(e), "url": url}


async def get_data_asyncio(urls):
    """aiohttp ile URL'leri eşzamanlı (concurrent) olarak indirir ve sonuçları döndürür.
    asyncio.gather ile tüm görevler aynı anda başlatılır.
    """
    st = time.time()  # Başlangıç zamanı

    # Toplam istek süresine makul bir sınır koymak için timeout belirliyoruz
    timeout = aiohttp.ClientTimeout(total=30)

    # Eşzamanlı bağlantı sayısını sınırlamak için connector kullanabiliriz (örn. 100)
    connector = aiohttp.TCPConnector(limit=100)

    # ClientSession: bağlantı havuzu ve ortak ayarlar için kullanılır
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        # Her URL için bir görev (coroutine) hazırla
        tasks = [fetch_json(session, url) for url in urls]

        # Tüm görevleri aynı anda çalıştır; return_exceptions=False ile hataları helper içinde yakalıyoruz
        results = await asyncio.gather(*tasks, return_exceptions=False)

    et = time.time()  # Bitiş zamanı
    print(f"Elapsed Time with asyncio + aiohttp: {et - st} seconds")
    return results


# Test amaçlı: Aynı URL'i 10 kez çağırıyoruz ki paralelleşme etkisi görülebilsin.
urls = ["https://jsonplaceholder.typicode.com/posts/1"]*10

# Test
# get_data_async(urls)        # Senkron (tek iş parçacıklı) çalıştırmak için yorumdan çıkar
# asyncio.run(get_data_asyncio(urls))  # Asenkron (asyncio + aiohttp) çalıştırmak için yorumdan çıkar
getDataThreading(urls)        # Threading ile paralel çağrı (aktif)
