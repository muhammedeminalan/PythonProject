#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gelişmiş Sesli Asistan
======================

Özellikler:
- Sürekli ses dinleme ve tanıma
- Doğal dil komut işleme
- Sistem komutları yürütme
- Hava durumu, saat, hesaplama gibi temel işlevler
- Sesli yanıt verme
- Özelleştirilebilir komutlar
- Güvenlik kontrolü

Gereksinimler:
pip install speechrecognition pyttsx3 pyaudio requests wikipedia-api

Kullanım:
python sesli_asistan.py
"""

import os
import sys
import json
import re
import time
import threading
import subprocess
import webbrowser
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
import logging

try:
    import speech_recognition as sr
    import pyttsx3
    import requests
    import wikipediaapi as wikipedia
except ImportError as e:
    print(f"❌ Gerekli kütüphane eksik: {e}")
    print("Kurmak için: pip install speechrecognition pyttsx3 pyaudio requests wikipedia-api")
    sys.exit(1)

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('voice_assistant.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class VoiceAssistant:
    """Gelişmiş Sesli Asistan Sınıfı"""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.is_listening = False
        self.wake_words = ["asistan", "hey asistan", "bilgisayar"]
        self.exit_words = ["çık", "kapat", "durdur", "bitir"]

        # Komut eşleştirme desenleri
        self.command_patterns = {
            r"saat\s*kaç|saati\s*söyle": self.get_time,
            r"tarih\s*ne|bugün\s*ne": self.get_date,
            r"hava\s*durumu|hava\s*nasıl": self.get_weather,
            r"hesapla\s*(.*)|matematik\s*(.*)": self.calculate,
            r"arama\s*yap\s*(.*)|google.*arama\s*(.*)": self.web_search,
            r"wikipedia.*ara\s*(.*)|vikipedi.*ara\s*(.*)": self.wikipedia_search,
            r"müzik\s*aç|youtube.*müzik": self.play_music,
            r"not\s*al\s*(.*)|kaydet\s*(.*)": self.take_note,
            r"notları\s*oku|notları\s*göster": self.read_notes,
            r"sistem\s*bilgisi|bilgisayar\s*durumu": self.system_info,
            r"uygulama\s*aç\s*(.*)|program\s*aç\s*(.*)": self.open_application,
            r"dosya\s*aç\s*(.*)|klasör\s*aç\s*(.*)": self.open_file,
            r"ses\s*seviyesi\s*(.*)|volume\s*(.*)": self.volume_control,
            r"ekran\s*görüntüsü|screenshot": self.take_screenshot,
            r"hatırlatıcı\s*kur\s*(.*)|alarm\s*kur\s*(.*)": self.set_reminder,
            r"yardım|komutlar|neler\s*yapabilirsin": self.show_help,
        }

        # TTS ayarları
        self.setup_tts()

        # Mikrofon kalibrasyonu
        self.calibrate_microphone()

        # Notlar dosyası
        self.notes_file = "assistant_notes.json"
        self.load_notes()

        # Hatırlatıcılar
        self.reminders = []

    def setup_tts(self):
        """Text-to-Speech motorunu yapılandır"""
        voices = self.tts_engine.getProperty('voices')
        # Türkçe ses varsa kullan
        for voice in voices:
            if 'tr' in voice.id.lower() or 'turkish' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break

        # Ses hızı ve ses seviyesi
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.8)

    def calibrate_microphone(self):
        """Mikrofonu çevresel gürültüye göre kalibre et"""
        try:
            with self.microphone as source:
                print("🎤 Mikrofon kalibre ediliyor...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("✅ Mikrofon kalibrasyonu tamamlandı")
        except Exception as e:
            logger.error(f"Mikrofon kalibrasyonu hatası: {e}")

    def speak(self, text: str):
        """Metni sesli olarak söyle"""
        try:
            print(f"🗣️  {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS hatası: {e}")
            print(f"💬 {text}")

    def listen(self, timeout: int = 5) -> Optional[str]:
        """Mikrofonu dinle ve metne çevir"""
        try:
            with self.microphone as source:
                # Kısa süre sessizlik bekle
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)

            # Google Speech Recognition kullan
            text = self.recognizer.recognize_google(audio, language='tr-TR')
            print(f"👂 Duydum: {text}")
            return text.lower()

        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            logger.error(f"Ses tanıma servisi hatası: {e}")
            return None
        except Exception as e:
            logger.error(f"Dinleme hatası: {e}")
            return None

    def process_command(self, command: str) -> bool:
        """Komutu işle ve uygun fonksiyonu çalıştır"""
        command = command.strip().lower()

        # Çıkış komutları kontrol et
        if any(word in command for word in self.exit_words):
            self.speak("Görüşürüz! Hoşça kal.")
            return False

        # Komut desenlerini kontrol et
        for pattern, function in self.command_patterns.items():
            match = re.search(pattern, command)
            if match:
                try:
                    # Eşleşen grupları fonksiyona geç
                    groups = match.groups()
                    if groups and any(groups):
                        # Boş olmayan ilk grubu kullan
                        param = next((g for g in groups if g), "").strip()
                        if param:
                            function(param)
                        else:
                            function()
                    else:
                        function()
                    return True
                except Exception as e:
                    logger.error(f"Komut yürütme hatası: {e}")
                    self.speak("Üzgünüm, bu komutu yerine getiremiyorum.")
                    return True

        # Bilinmeyen komut
        self.speak("Bu komutu anlayamadım. Yardım için 'yardım' deyin.")
        return True

    # Komut fonksiyonları
    def get_time(self, param: str = ""):
        """Şu anki saati söyle"""
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        self.speak(f"Şu an saat {time_str}")

    def get_date(self, param: str = ""):
        """Bugünün tarihini söyle"""
        now = datetime.now()
        date_str = now.strftime("%d %B %Y, %A")
        # Türkçe gün ve ay isimleri
        turkish_days = {
            'Monday': 'Pazartesi', 'Tuesday': 'Salı', 'Wednesday': 'Çarşamba',
            'Thursday': 'Perşembe', 'Friday': 'Cuma', 'Saturday': 'Cumartesi', 'Sunday': 'Pazar'
        }
        turkish_months = {
            'January': 'Ocak', 'February': 'Şubat', 'March': 'Mart', 'April': 'Nisan',
            'May': 'Mayıs', 'June': 'Haziran', 'July': 'Temmuz', 'August': 'Ağustos',
            'September': 'Eylül', 'October': 'Ekim', 'November': 'Kasım', 'December': 'Aralık'
        }

        for eng, tr in turkish_days.items():
            date_str = date_str.replace(eng, tr)
        for eng, tr in turkish_months.items():
            date_str = date_str.replace(eng, tr)

        self.speak(f"Bugün {date_str}")

    def get_weather(self, param: str = ""):
        """Hava durumu bilgisi al"""
        try:
            # OpenWeatherMap API (ücretsiz API key gerekli)
            # Bu örnekte basit bir yanıt veriyoruz
            self.speak("Hava durumu servisi şu anda kullanılamıyor. Weather API anahtarı gerekli.")
        except Exception as e:
            logger.error(f"Hava durumu hatası: {e}")
            self.speak("Hava durumu bilgisi alınamadı.")

    def calculate(self, expression: str):
        """Matematiksel hesaplama yap"""
        try:
            # Güvenlik için sadece belirli karakterlere izin ver
            allowed_chars = "0123456789+-*/()., "
            if not all(c in allowed_chars for c in expression):
                self.speak("Sadece temel matematik işlemleri yapabilirim.")
                return

            # Türkçe sayıları İngilizce'ye çevir
            expression = expression.replace("çarpı", "*").replace("bölü", "/")
            expression = expression.replace("artı", "+").replace("eksi", "-")
            expression = expression.replace("kere", "*")

            result = eval(expression)
            self.speak(f"Sonuç: {result}")

        except Exception as e:
            logger.error(f"Hesaplama hatası: {e}")
            self.speak("Hesaplama yapılamadı. Lütfen geçerli bir matematik ifadesi kullanın.")

    def web_search(self, query: str):
        """Web araması yap"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            self.speak(f"{query} için arama yapıyorum.")
        except Exception as e:
            logger.error(f"Web arama hatası: {e}")
            self.speak("Web araması yapılamadı.")

    def wikipedia_search(self, query: str):
        """Wikipedia araması yap"""
        try:
            wiki_wiki = wikipedia.Wikipedia('tr')
            page = wiki_wiki.page(query)

            if page.exists():
                # İlk 2 cümleyi al
                text = page.text
                sentences = text.split('. ')[:2]
                summary = '. '.join(sentences) + '.'
                self.speak(f"{query} hakkında: {summary}")
            else:
                self.speak(f"{query} hakkında bilgi bulunamadı.")

        except Exception as e:
            logger.error(f"Wikipedia arama hatası: {e}")
            self.speak("Wikipedia araması yapılamadı.")

    def play_music(self, param: str = ""):
        """Müzik çal"""
        try:
            music_url = "https://www.youtube.com/results?search_query=müzik"
            webbrowser.open(music_url)
            self.speak("YouTube müzik açılıyor.")
        except Exception as e:
            logger.error(f"Müzik çalma hatası: {e}")
            self.speak("Müzik çalınamadı.")

    def take_note(self, note: str):
        """Not al"""
        try:
            timestamp = datetime.now().isoformat()
            self.notes.append({"timestamp": timestamp, "note": note})
            self.save_notes()
            self.speak("Not alındı.")
        except Exception as e:
            logger.error(f"Not alma hatası: {e}")
            self.speak("Not alınamadı.")

    def read_notes(self, param: str = ""):
        """Notları oku"""
        try:
            if not self.notes:
                self.speak("Hiç not yok.")
                return

            self.speak(f"Toplam {len(self.notes)} notunuz var.")
            for i, note_data in enumerate(self.notes[-5:], 1):  # Son 5 notu oku
                note = note_data["note"]
                self.speak(f"Not {i}: {note}")

        except Exception as e:
            logger.error(f"Not okuma hatası: {e}")
            self.speak("Notlar okunamadı.")

    def system_info(self, param: str = ""):
        """Sistem bilgilerini ver"""
        try:
            import platform
            import psutil

            system = platform.system()
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()

            info = f"İşletim sistemi: {system}. "
            info += f"İşlemci sayısı: {cpu_count}. "
            info += f"Bellek kullanımı: yüzde {memory.percent}."

            self.speak(info)

        except ImportError:
            self.speak("Sistem bilgileri için psutil kütüphanesi gerekli.")
        except Exception as e:
            logger.error(f"Sistem bilgisi hatası: {e}")
            self.speak("Sistem bilgileri alınamadı.")

    def open_application(self, app_name: str):
        """Uygulama aç"""
        try:
            # macOS için yaygın uygulamalar
            apps = {
                "safari": "Safari",
                "chrome": "Google Chrome",
                "firefox": "Firefox",
                "calculator": "Calculator",
                "hesap makinesi": "Calculator",
                "finder": "Finder",
                "terminal": "Terminal",
                "konsol": "Terminal",
                "notes": "Notes",
                "notlar": "Notes",
                "music": "Music",
                "müzik": "Music"
            }

            app_name = app_name.lower().strip()
            if app_name in apps:
                subprocess.run(["open", "-a", apps[app_name]])
                self.speak(f"{apps[app_name]} açılıyor.")
            else:
                # Direkt isim ile dene
                subprocess.run(["open", "-a", app_name])
                self.speak(f"{app_name} açılıyor.")

        except Exception as e:
            logger.error(f"Uygulama açma hatası: {e}")
            self.speak("Uygulama açılamadı.")

    def open_file(self, file_path: str):
        """Dosya veya klasör aç"""
        try:
            if os.path.exists(file_path):
                subprocess.run(["open", file_path])
                self.speak("Dosya açılıyor.")
            else:
                self.speak("Dosya bulunamadı.")
        except Exception as e:
            logger.error(f"Dosya açma hatası: {e}")
            self.speak("Dosya açılamadı.")

    def volume_control(self, level: str):
        """Ses seviyesini kontrol et"""
        try:
            if "aç" in level or "yükselt" in level:
                subprocess.run(["osascript", "-e", "set volume output volume 80"])
                self.speak("Ses seviyesi yükseltildi.")
            elif "kapat" in level or "alçalt" in level:
                subprocess.run(["osascript", "-e", "set volume output volume 20"])
                self.speak("Ses seviyesi alçaltıldı.")
            elif "sustur" in level:
                subprocess.run(["osascript", "-e", "set volume output muted true"])
                self.speak("Ses kapatıldı.")
            else:
                self.speak("Ses komutu anlaşılamadı.")
        except Exception as e:
            logger.error(f"Ses kontrolü hatası: {e}")
            self.speak("Ses ayarı değiştirilemedi.")

    def take_screenshot(self, param: str = ""):
        """Ekran görüntüsü al"""
        try:
            subprocess.run(["screencapture", "-x", f"screenshot_{int(time.time())}.png"])
            self.speak("Ekran görüntüsü alındı.")
        except Exception as e:
            logger.error(f"Ekran görüntüsü hatası: {e}")
            self.speak("Ekran görüntüsü alınamadı.")

    def set_reminder(self, reminder_text: str):
        """Hatırlatıcı kur"""
        try:
            # Basit hatırlatıcı sistemi
            reminder_time = datetime.now() + timedelta(minutes=5)  # 5 dakika sonra
            self.reminders.append({
                "time": reminder_time,
                "text": reminder_text
            })
            self.speak("5 dakika sonra hatırlatacağım.")
        except Exception as e:
            logger.error(f"Hatırlatıcı kurma hatası: {e}")
            self.speak("Hatırlatıcı kurulamadı.")

    def show_help(self, param: str = ""):
        """Yardım bilgilerini göster"""
        help_text = """
        Yapabileceğim işlemler:
        - Saat ve tarih bilgisi
        - Matematik hesaplamaları
        - Web araması
        - Wikipedia araması
        - Not alma ve okuma
        - Uygulama açma
        - Sistem bilgileri
        - Ses kontrolü
        - Ekran görüntüsü alma
        - Hatırlatıcı kurma
        
        Örnek komutlar:
        'Saat kaç', 'Hesapla 5 çarpı 3', 'Not al bugün toplantı var',
        'Safari aç', 'Sistem bilgisi', 'Ekran görüntüsü al'
        """
        self.speak("Yardım bilgilerini konsola yazdırıyorum.")
        print(help_text)

    def load_notes(self):
        """Notları dosyadan yükle"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
            else:
                self.notes = []
        except Exception as e:
            logger.error(f"Not yükleme hatası: {e}")
            self.notes = []

    def save_notes(self):
        """Notları dosyaya kaydet"""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Not kaydetme hatası: {e}")

    def check_reminders(self):
        """Hatırlatıcıları kontrol et"""
        now = datetime.now()
        for reminder in self.reminders[:]:
            if now >= reminder["time"]:
                self.speak(f"Hatırlatma: {reminder['text']}")
                self.reminders.remove(reminder)

    def start_listening(self):
        """Sürekli dinleme modunu başlat"""
        self.is_listening = True
        self.speak("Sesli asistan aktif. Beni uyandırmak için 'asistan' deyin.")

        while self.is_listening:
            try:
                # Hatırlatıcıları kontrol et
                self.check_reminders()

                # Uyandırma kelimesini dinle
                command = self.listen(timeout=1)
                if command is None:
                    continue

                # Uyandırma kelimesi var mı?
                if any(wake_word in command for wake_word in self.wake_words):
                    self.speak("Evet, dinliyorum.")

                    # Komutu dinle
                    command = self.listen(timeout=10)
                    if command:
                        if not self.process_command(command):
                            self.is_listening = False
                            break
                    else:
                        self.speak("Sizi duyamadım.")

            except KeyboardInterrupt:
                self.speak("Kapatılıyor...")
                self.is_listening = False
                break
            except Exception as e:
                logger.error(f"Dinleme döngüsü hatası: {e}")
                time.sleep(1)

        logger.info("Sesli asistan kapatıldı.")


def main():
    """Ana fonksiyon"""
    print("🎙️ Gelişmiş Sesli Asistan")
    print("=" * 50)

    try:
        assistant = VoiceAssistant()
        assistant.start_listening()
    except KeyboardInterrupt:
        print("\n👋 Görüşürüz!")
    except Exception as e:
        logger.error(f"Ana hata: {e}")
        print(f"❌ Hata: {e}")


if __name__ == "__main__":
    main()
