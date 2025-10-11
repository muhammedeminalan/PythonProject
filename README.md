# Py Tarayıcı

Sekmeli, yer imli, karanlık modlu, indirme yöneticili basit bir masaüstü tarayıcı (PySide6 + QtWebEngine).

## Kurulum

macOS / Linux / Windows için önerilen adımlar:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Not: Python 3.10–3.13 uyumlu. İlk kurulumda PySide6 büyük boyutlu paket indirir.

## Çalıştırma

```bash
python tools/tarayıcı.py
```

## Özellikler
- Sekmeler (Ctrl+T yeni sekme, Ctrl+W sekme kapat)
- Adres çubuğu (URL veya arama yazın)
- Yer imleri çubuğu (☆ Ekle ile mevcut sayfayı kaydedin)
- Tema: Karanlık/Aydınlık (🌓)
- İndirme yöneticisi (dosyayı kaydet penceresi)
- Yeni pencere (target=_blank) linkleri yeni sekmede açılır
- Yakınlaştırma: dahili (Ctrl/⌘ +/− için standart sistem kısayolları)

## Bilinen Notlar
- Terminalde Skia/JS uyarıları görülebilir; işlevi etkilemez.
- macOS’ta ilk çalıştırmada güvenlik uyarıları görebilirsiniz; izin verin.

## Yol Haritası (opsiyonel)
- Geçmiş (History) paneli
- İndirilenler listesi paneli
- Basit reklam engelleme
- Site izinleri (mikrofon/konum vb.)

