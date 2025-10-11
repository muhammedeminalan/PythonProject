# PythonProject

Çok parçalı bir öğrenme ve araç seti projesi. İçerik: modern arayüzlü masaüstü tarayıcı (PySide6 + QtWebEngine), gelişmiş internet hız testi (Tkinter + Matplotlib), ve sesli asistan (SpeechRecognition + pyttsx3). Ayrıca Flask, FastAPI, NumPy, Pandas öğrenme örnekleri de bulunur.

## İçerik Başlıkları
- Özellikler
- Hızlı kurulum
- Nasıl çalıştırılır (araç bazında)
- Sorun giderme (macOS odaklı)
- Geliştirme akışı ve komutlar

---

## Özellikler
- Tarayıcı (tools/tarayıcı.py)
  - Sekmeler, adres çubuğu, yer imleri çubuğu
  - Karanlık/Aydınlık tema
  - İndirme yöneticisi (dosyayı kaydet)
  - Yeni pencere linklerini sekmede açma
- İnternet Hız Testi (tools/speed_test.py)
  - Responsif Tkinter arayüzü
  - Ping, jitter, indirme/yükleme ölçümleri
  - IP/ISP/konum bilgileri ve geçmiş kaydı
  - Gerçek zamanlı performans grafikleri ve puanlama
- Sesli Asistan (tools/sesli_asistan.py)
  - TR dilinde ses tanıma, TTS ile yanıt
  - Web arama, Wikipedia özeti, not alma/okuma, sistem bilgisi, uygulama/dosya açma, hatırlatıcı, ses kontrolü

---

## Hızlı Kurulum
Python 3.10–3.13 ile test edildi. Öneri: sanal ortam kullanın.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Notlar:
- PySide6 ilk kurulumda büyük boyutlu paket indirir.
- PyAudio, macOS’ta PortAudio’a ihtiyaç duyabilir (aşağıdaki Sorun Giderme bölümüne bakın).

---

## Nasıl Çalıştırılır
Aşağıdaki komutlar proje kökünden (README’nin olduğu klasör) çalıştırılmalıdır.

- Tarayıcı (PySide6 + QtWebEngine):
  ```bash
  python tools/tarayıcı.py
  ```

- İnternet Hız Testi (Tkinter + Matplotlib):
  ```bash
  python tools/speed_test.py
  ```

- Sesli Asistan (SpeechRecognition + pyttsx3):
  ```bash
  python tools/sesli_asistan.py
  ```

Ek örnekler:
- Flask denemesi: `python flask_learn/app.py`
- FastAPI denemesi: `uvicorn fast_api_learn.fast_app:app --reload`

---

## Sorun Giderme (macOS)
- PySide6 / QtWebEngine
  - Hata: `ImportError: cannot import name 'QWebEngineProfile' from PySide6.QtWebEngineWidgets`
    - Çözüm: Kodda `from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineDownloadRequest, QWebEnginePage` kullanılır (projedeki tarayıcı dosyasında uygulanmıştır).
  - Eğer QtWebEngine modülleri bulunamıyorsa: `pip install PySide6 PySide6-Addons shiboken6` güncel olsun.

- PyAudio kurulumu
  - macOS’ta şu adım gerekebilir:
    ```bash
    brew install portaudio  # Homebrew yüklü değilse: https://brew.sh
    pip install pyaudio
    ```
  - Alternatif: `pip install pipwin` (Windows) ve `pipwin install pyaudio`.

- SpeechRecognition / Wikipedia hataları
  - ModuleNotFoundError için: `pip install SpeechRecognition wikipedia-api wikipedia`.
  - Ses tanıma internet bağlantısı gerektirir (Google Speech API).

- Tkinter
  - macOS Python resmi sürümlerinde Tkinter yüklü gelir. Sorun olursa Python’u yeniden kurmayı deneyin.

---

## Geliştirme Akışı ve Komutlar
- Kod stili: Mevcut dosya stillerini koruyun; küçük, odaklı commit’ler.
- Sanal ortam (önerilir): `.venv` dizini git’te yok sayılır.

Sık kullanılan komutlar:
```bash
# Sanal ortam
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Çalıştırma
python tools/tarayıcı.py
python tools/speed_test.py
python tools/sesli_asistan.py

# Test (hızlı import testi)
python - <<'PY'
import sys
mods = [
  'PySide6', 'PySide6.QtWebEngineCore', 'PySide6.QtWebEngineWidgets',
  'speedtest', 'requests', 'matplotlib', 'numpy',
  'speech_recognition', 'pyttsx3', 'wikipedia', 'wikipediaapi', 'psutil'
]
for m in mods:
    try:
        __import__(m)
        print('OK  ', m)
    except Exception as e:
        print('FAIL', m, e)
PY

# Git
git add -A
git commit -m "docs: kapsamlı README, .gitignore ve bağımlılıklar"
```

### GitHub’a Gönderme
1) GitHub’da boş bir repo oluşturun (ör. `PythonProject`).
2) Aşağıdaki komutlarla uzak adresi ekleyip push edin:
```bash
git remote add origin https://github.com/<kullanici-adi>/PythonProject.git
# Varsayılan dalı öğrenin
git branch --show-current
# Örn. main ise:
git push -u origin main
```
Eğer daha önce uzak tanımlıysa kontrol edin:
```bash
git remote -v
```

---

## Proje Yapısı (özet)
```
PythonProject/
  tools/
    tarayıcı.py         # PySide6 tarayıcı
    speed_test.py       # Tkinter hız testi + grafik
    sesli_asistan.py    # Sesli asistan
  flask_learn/          # Flask örnekleri
  fast_api_learn/       # FastAPI örnekleri
  numpy_learn/, pandas_learn/  # Bilimsel örnekler
  requirements.txt
  README.md
```

İyi çalışmalar! Soruların için issue açabilirsin veya README’yi genişletebilirsin.
