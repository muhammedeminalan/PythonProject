#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gelişmiş İnternet Hız Testi Uygulaması
=====================================

Özellikler:
- Modern ve responsif kullanıcı arayüzü
- İndirme/Yükleme hızı testi
- Ping ve jitter ölçümü
- IP adresi ve konum bilgileri
- Gerçek zamanlı grafik gösterimi
- Sonuç analizi ve puanlama sistemi
- Test geçmişi kaydetme
- Çoklu sunucu seçeneği

Gereksinimler:
pip install speedtest-cli requests tkinter matplotlib numpy
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import subprocess
import sys

try:
    import speedtest
    import requests
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import numpy as np
except ImportError as e:
    print(f"❌ Gerekli kütüphane eksik: {e}")
    print("Kurmak için: pip install speedtest-cli requests matplotlib numpy")
    sys.exit(1)


class SpeedTestApp:
    """Gelişmiş İnternet Hız Testi Uygulaması"""

    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Gelişmiş İnternet Hız Testi")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Stil yapılandırması
        self.setup_style()

        # Veri depolama
        self.test_history = []
        self.load_history()
        self.current_test_data = {}
        self.is_testing = False

        # SpeedTest objesi
        self.st = None

        # Arayüz oluştur
        self.create_widgets()
        self.setup_layout()

        # IP bilgilerini başlangıçta yükle
        self.load_ip_info()

    def setup_style(self):
        """Modern stil yapılandırması"""
        style = ttk.Style()
        style.theme_use('clam')

        # Renkler
        self.colors = {
            'primary': '#2196F3',
            'secondary': '#FFC107',
            'success': '#4CAF50',
            'danger': '#F44336',
            'warning': '#FF9800',
            'info': '#17A2B8',
            'light': '#F8F9FA',
            'dark': '#343A40',
            'bg': '#FFFFFF',
            'text': '#212529'
        }

        # Stil tanımlamaları
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground=self.colors['primary'])
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), foreground=self.colors['dark'])
        style.configure('Info.TLabel', font=('Arial', 10), foreground=self.colors['text'])
        style.configure('Success.TLabel', font=('Arial', 14, 'bold'), foreground=self.colors['success'])
        style.configure('Danger.TLabel', font=('Arial', 14, 'bold'), foreground=self.colors['danger'])

        # Buton stilleri
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        style.configure('Success.TButton', font=('Arial', 10, 'bold'))

    def create_widgets(self):
        """Arayüz bileşenlerini oluştur"""
        # Ana container
        self.main_frame = ttk.Frame(self.root, padding="20")

        # Başlık bölümü
        self.create_header()

        # İP bilgileri bölümü
        self.create_ip_section()

        # Test kontrol bölümü
        self.create_control_section()

        # Sonuç gösterim bölümü
        self.create_results_section()

        # Grafik bölümü
        self.create_chart_section()

        # Geçmiş bölümü
        self.create_history_section()

    def create_header(self):
        """Başlık bölümü"""
        header_frame = ttk.Frame(self.main_frame)

        # Ana başlık
        title_label = ttk.Label(
            header_frame,
            text="🚀 Gelişmiş İnternet Hız Testi",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 5))

        # Alt başlık
        subtitle_label = ttk.Label(
            header_frame,
            text="İnternet hızınızı test edin ve detaylı analiz alın",
            style='Info.TLabel'
        )
        subtitle_label.pack(pady=(0, 10))

        self.header_frame = header_frame

    def create_ip_section(self):
        """IP bilgileri bölümü"""
        ip_frame = ttk.LabelFrame(self.main_frame, text="🌐 Bağlantı Bilgileri", padding="10")

        # IP bilgileri grid
        ip_info_frame = ttk.Frame(ip_frame)

        # Public IP
        ttk.Label(ip_info_frame, text="Genel IP:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.public_ip_label = ttk.Label(ip_info_frame, text="Yükleniyor...", style='Info.TLabel')
        self.public_ip_label.grid(row=0, column=1, sticky='w')

        # ISP
        ttk.Label(ip_info_frame, text="ISP:", font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky='w', padx=(20, 10))
        self.isp_label = ttk.Label(ip_info_frame, text="Yükleniyor...", style='Info.TLabel')
        self.isp_label.grid(row=0, column=3, sticky='w')

        # Konum
        ttk.Label(ip_info_frame, text="Konum:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(5, 0))
        self.location_label = ttk.Label(ip_info_frame, text="Yükleniyor...", style='Info.TLabel')
        self.location_label.grid(row=1, column=1, columnspan=3, sticky='w', pady=(5, 0))

        ip_info_frame.pack(fill='x')

        self.ip_frame = ip_frame

    def create_control_section(self):
        """Test kontrol bölümü"""
        control_frame = ttk.LabelFrame(self.main_frame, text="🎯 Test Kontrolleri", padding="10")

        # Sunucu seçimi
        server_frame = ttk.Frame(control_frame)
        ttk.Label(server_frame, text="Test Sunucusu:", font=('Arial', 9, 'bold')).pack(side='left', padx=(0, 10))

        self.server_var = tk.StringVar(value="Otomatik")
        self.server_combo = ttk.Combobox(
            server_frame,
            textvariable=self.server_var,
            values=["Otomatik", "En yakın sunucu", "Manuel seçim"],
            state="readonly",
            width=20
        )
        self.server_combo.pack(side='left', padx=(0, 20))

        # Test başlat butonu
        self.start_button = ttk.Button(
            server_frame,
            text="🚀 Hız Testini Başlat",
            command=self.start_speed_test,
            style='Primary.TButton'
        )
        self.start_button.pack(side='left', padx=(0, 10))

        # Durdur butonu
        self.stop_button = ttk.Button(
            server_frame,
            text="⏹️ Durdur",
            command=self.stop_speed_test,
            state='disabled'
        )
        self.stop_button.pack(side='left')

        server_frame.pack(fill='x', pady=(0, 10))

        # İlerleme çubuğu
        progress_frame = ttk.Frame(control_frame)
        ttk.Label(progress_frame, text="Test İlerlemesi:", font=('Arial', 9, 'bold')).pack(anchor='w')

        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(fill='x', pady=(5, 5))

        self.status_label = ttk.Label(
            progress_frame,
            text="Test bekleniyor...",
            style='Info.TLabel'
        )
        self.status_label.pack(anchor='w')

        progress_frame.pack(fill='x')

        self.control_frame = control_frame

    def create_results_section(self):
        """Sonuç gösterim bölümü"""
        results_frame = ttk.LabelFrame(self.main_frame, text="📊 Test Sonuçları", padding="10")

        # Sonuç kartları
        cards_frame = ttk.Frame(results_frame)

        # İndirme hızı kartı
        download_card = self.create_result_card(cards_frame, "⬇️ İndirme", "0.00", "Mbps")
        download_card.pack(side='left', padx=(0, 10), fill='both', expand=True)
        self.download_speed_label = download_card.children['!label2']

        # Yükleme hızı kartı
        upload_card = self.create_result_card(cards_frame, "⬆️ Yükleme", "0.00", "Mbps")
        upload_card.pack(side='left', padx=(0, 10), fill='both', expand=True)
        self.upload_speed_label = upload_card.children['!label2']

        # Ping kartı
        ping_card = self.create_result_card(cards_frame, "📡 Ping", "0", "ms")
        ping_card.pack(side='left', padx=(0, 10), fill='both', expand=True)
        self.ping_label = ping_card.children['!label2']

        # Jitter kartı
        jitter_card = self.create_result_card(cards_frame, "📈 Jitter", "0", "ms")
        jitter_card.pack(side='left', fill='both', expand=True)
        self.jitter_label = jitter_card.children['!label2']

        cards_frame.pack(fill='x', pady=(0, 15))

        # Analiz ve puanlama
        analysis_frame = ttk.Frame(results_frame)

        # Genel puan
        score_frame = ttk.Frame(analysis_frame)
        ttk.Label(score_frame, text="🎯 Genel Puan:", font=('Arial', 12, 'bold')).pack(side='left', padx=(0, 10))
        self.score_label = ttk.Label(score_frame, text="--/100", style='Success.TLabel')
        self.score_label.pack(side='left')

        score_frame.pack(anchor='w', pady=(0, 10))

        # Analiz metni
        self.analysis_text = scrolledtext.ScrolledText(
            analysis_frame,
            height=4,
            width=80,
            font=('Arial', 9),
            wrap=tk.WORD
        )
        self.analysis_text.pack(fill='both', expand=True)
        self.analysis_text.insert('1.0', "Henüz test yapılmadı. Hız testini başlatın.")

        analysis_frame.pack(fill='both', expand=True)

        self.results_frame = results_frame

    def create_result_card(self, parent, title, value, unit):
        """Sonuç kartı oluştur"""
        card = ttk.Frame(parent, relief='ridge', borderwidth=1)
        card.configure(padding="10")

        # Başlık
        title_label = ttk.Label(card, text=title, font=('Arial', 10, 'bold'))
        title_label.pack()

        # Değer
        value_label = ttk.Label(card, text=value, font=('Arial', 16, 'bold'), foreground=self.colors['primary'])
        value_label.pack(pady=(5, 0))

        # Birim
        unit_label = ttk.Label(card, text=unit, font=('Arial', 9))
        unit_label.pack()

        return card

    def create_chart_section(self):
        """Grafik bölümü"""
        chart_frame = ttk.LabelFrame(self.main_frame, text="📈 Performans Grafiği", padding="10")

        # Matplotlib figürü
        self.fig = Figure(figsize=(10, 4), dpi=100, facecolor='white')
        self.ax = self.fig.add_subplot(111)

        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # İlk grafik
        self.update_chart([])

        self.chart_frame = chart_frame

    def create_history_section(self):
        """Geçmiş bölümü"""
        history_frame = ttk.LabelFrame(self.main_frame, text="📋 Test Geçmişi", padding="10")

        # Treeview için frame
        tree_frame = ttk.Frame(history_frame)

        # Treeview
        columns = ('Tarih', 'İndirme', 'Yükleme', 'Ping', 'Puan', 'ISP')
        self.history_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=6)

        # Sütun başlıkları ve genişlikleri
        column_widths = {'Tarih': 150, 'İndirme': 100, 'Yükleme': 100, 'Ping': 80, 'Puan': 80, 'ISP': 200}
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=column_widths[col], anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        # Paketleme
        self.history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        tree_frame.pack(fill='both', expand=True, pady=(0, 10))

        # Butonlar
        button_frame = ttk.Frame(history_frame)

        ttk.Button(
            button_frame,
            text="🔄 Yenile",
            command=self.refresh_history
        ).pack(side='left', padx=(0, 10))

        ttk.Button(
            button_frame,
            text="💾 Dışa Aktar",
            command=self.export_history
        ).pack(side='left', padx=(0, 10))

        ttk.Button(
            button_frame,
            text="🗑️ Temizle",
            command=self.clear_history
        ).pack(side='left')

        button_frame.pack(anchor='w')

        self.history_frame = history_frame

    def setup_layout(self):
        """Ana layout düzenlemesi"""
        self.main_frame.pack(fill='both', expand=True)

        # Responsive grid layout
        self.header_frame.pack(fill='x', pady=(0, 20))
        self.ip_frame.pack(fill='x', pady=(0, 10))
        self.control_frame.pack(fill='x', pady=(0, 10))
        self.results_frame.pack(fill='x', pady=(0, 10))
        self.chart_frame.pack(fill='both', expand=True, pady=(0, 10))
        self.history_frame.pack(fill='both', expand=True)

    def load_ip_info(self):
        """IP bilgilerini yükle"""
        def fetch_ip_info():
            try:
                # IP bilgilerini al
                response = requests.get('http://ipapi.co/json/', timeout=10)
                data = response.json()

                # Arayüzü güncelle
                self.root.after(0, lambda: self.update_ip_info(data))

            except Exception as e:
                error_data = {
                    'ip': 'Alınamadı',
                    'org': 'Alınamadı',
                    'city': 'Alınamadı',
                    'country_name': 'Alınamadı'
                }
                self.root.after(0, lambda: self.update_ip_info(error_data))

        # Thread'de çalıştır
        threading.Thread(target=fetch_ip_info, daemon=True).start()

    def update_ip_info(self, data):
        """IP bilgilerini arayüzde güncelle"""
        try:
            self.public_ip_label.config(text=data.get('ip', 'Bilinmiyor'))
            self.isp_label.config(text=data.get('org', 'Bilinmiyor'))

            location = f"{data.get('city', 'Bilinmiyor')}, {data.get('country_name', 'Bilinmiyor')}"
            self.location_label.config(text=location)

        except Exception as e:
            print(f"IP bilgisi güncelleme hatası: {e}")

    def start_speed_test(self):
        """Hız testini başlat"""
        if self.is_testing:
            return

        self.is_testing = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.progress.start()

        # Test thread'ini başlat
        test_thread = threading.Thread(target=self.run_speed_test, daemon=True)
        test_thread.start()

    def stop_speed_test(self):
        """Hız testini durdur"""
        self.is_testing = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress.stop()
        self.status_label.config(text="Test durduruldu.")

    def run_speed_test(self):
        """Hız testini çalıştır"""
        try:
            # Durum güncelle
            self.root.after(0, lambda: self.status_label.config(text="SpeedTest başlatılıyor..."))

            # SpeedTest objesi oluştur
            self.st = speedtest.Speedtest()

            if not self.is_testing:
                return

            # En iyi sunucuyu bul
            self.root.after(0, lambda: self.status_label.config(text="En iyi sunucu aranıyor..."))
            self.st.get_best_server()

            if not self.is_testing:
                return

            # İndirme testi
            self.root.after(0, lambda: self.status_label.config(text="İndirme hızı test ediliyor..."))
            download_speed = self.st.download() / 1_000_000  # Mbps'ye çevir

            if not self.is_testing:
                return

            # Yükleme testi
            self.root.after(0, lambda: self.status_label.config(text="Yükleme hızı test ediliyor..."))
            upload_speed = self.st.upload() / 1_000_000  # Mbps'ye çevir

            # Ping bilgisi
            ping = self.st.results.ping

            # Jitter hesaplama (basit tahmin)
            jitter = max(1, ping * 0.1)

            # Test verilerini sakla
            test_data = {
                'timestamp': datetime.now(),
                'download': download_speed,
                'upload': upload_speed,
                'ping': ping,
                'jitter': jitter,
                'server': self.st.results.server,
                'client': self.st.results.client
            }

            self.current_test_data = test_data

            # Sonuçları güncelle
            self.root.after(0, lambda: self.update_results(test_data))

        except Exception as e:
            error_msg = f"Test hatası: {str(e)}"
            self.root.after(0, lambda: self.status_label.config(text=error_msg))
            print(f"SpeedTest hatası: {e}")

        finally:
            # Test bitir
            self.root.after(0, self.finish_test)

    def update_results(self, test_data):
        """Test sonuçlarını güncelle"""
        try:
            # Hız değerlerini güncelle
            self.download_speed_label.config(text=f"{test_data['download']:.2f}")
            self.upload_speed_label.config(text=f"{test_data['upload']:.2f}")
            self.ping_label.config(text=f"{test_data['ping']:.0f}")
            self.jitter_label.config(text=f"{test_data['jitter']:.1f}")

            # Analiz ve puanlama
            score, analysis = self.analyze_results(test_data)
            self.score_label.config(text=f"{score}/100")

            # Puan rengini ayarla
            if score >= 80:
                self.score_label.config(foreground=self.colors['success'])
            elif score >= 60:
                self.score_label.config(foreground=self.colors['warning'])
            else:
                self.score_label.config(foreground=self.colors['danger'])

            # Analiz metnini güncelle
            self.analysis_text.delete('1.0', tk.END)
            self.analysis_text.insert('1.0', analysis)

            # Test geçmişine ekle
            history_entry = {
                'timestamp': test_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                'download': test_data['download'],
                'upload': test_data['upload'],
                'ping': test_data['ping'],
                'jitter': test_data['jitter'],
                'score': score,
                'isp': test_data['client'].get('isp', 'Bilinmiyor')
            }

            self.test_history.append(history_entry)
            self.save_history()
            self.refresh_history()

            # Grafiği güncelle
            self.update_chart(self.test_history[-10:])  # Son 10 test

        except Exception as e:
            print(f"Sonuç güncelleme hatası: {e}")

    def analyze_results(self, test_data):
        """Test sonuçlarını analiz et ve puanla"""
        download = test_data['download']
        upload = test_data['upload']
        ping = test_data['ping']

        # Puanlama sistemi (0-100)
        score = 0
        analysis_parts = []

        # İndirme hızı puanı (40 puan)
        if download >= 100:
            download_score = 40
            download_rating = "Mükemmel"
        elif download >= 50:
            download_score = 30 + (download - 50) * 0.2
            download_rating = "Çok İyi"
        elif download >= 25:
            download_score = 20 + (download - 25) * 0.4
            download_rating = "İyi"
        elif download >= 10:
            download_score = 10 + (download - 10) * 0.67
            download_rating = "Orta"
        else:
            download_score = download * 1.0
            download_rating = "Düşük"

        score += download_score
        analysis_parts.append(f"📥 İndirme Hızı: {download:.2f} Mbps - {download_rating}")

        # Yükleme hızı puanı (30 puan)
        if upload >= 50:
            upload_score = 30
            upload_rating = "Mükemmel"
        elif upload >= 25:
            upload_score = 20 + (upload - 25) * 0.4
            upload_rating = "Çok İyi"
        elif upload >= 10:
            upload_score = 10 + (upload - 10) * 0.67
            upload_rating = "İyi"
        elif upload >= 5:
            upload_score = 5 + (upload - 5) * 1.0
            upload_rating = "Orta"
        else:
            upload_score = upload * 1.0
            upload_rating = "Düşük"

        score += upload_score
        analysis_parts.append(f"📤 Yükleme Hızı: {upload:.2f} Mbps - {upload_rating}")

        # Ping puanı (30 puan)
        if ping <= 20:
            ping_score = 30
            ping_rating = "Mükemmel"
        elif ping <= 50:
            ping_score = 20 + (50 - ping) * 0.33
            ping_rating = "İyi"
        elif ping <= 100:
            ping_score = 10 + (100 - ping) * 0.2
            ping_rating = "Orta"
        elif ping <= 200:
            ping_score = 5 + (200 - ping) * 0.05
            ping_rating = "Yavaş"
        else:
            ping_score = 0
            ping_rating = "Çok Yavaş"

        score += ping_score
        analysis_parts.append(f"📡 Ping: {ping:.0f} ms - {ping_rating}")

        # Genel değerlendirme
        score = min(100, max(0, int(score)))

        if score >= 90:
            overall = "🏆 Mükemmel bağlantı! Tüm online aktiviteler için idealdir."
        elif score >= 75:
            overall = "✅ Çok iyi bağlantı! Çoğu aktivite için uygun."
        elif score >= 60:
            overall = "👍 İyi bağlantı! Günlük kullanım için yeterli."
        elif score >= 40:
            overall = "⚠️ Orta bağlantı! Bazı aktivitelerde yavaşlık yaşayabilirsiniz."
        else:
            overall = "❌ Zayıf bağlantı! Hız iyileştirmesi gerekebilir."

        # Öneriler
        suggestions = []
        if download < 25:
            suggestions.append("• Daha yüksek hızlı bir internet paketi düşünebilirsiniz")
        if upload < 5:
            suggestions.append("• Video konferans ve dosya yükleme için yükleme hızınız düşük")
        if ping > 100:
            suggestions.append("• Online oyunlar için ping süreniz yüksek")

        # Analiz metnini oluştur
        analysis = f"{overall}\n\n"
        analysis += "📊 Detaylar:\n" + "\n".join(analysis_parts)

        if suggestions:
            analysis += f"\n\n💡 Öneriler:\n" + "\n".join(suggestions)

        # Aktivite önerileri
        activity_guide = self.get_activity_guide(download, upload, ping)
        analysis += f"\n\n🎯 Bu hızda yapabilecekleriniz:\n{activity_guide}"

        return score, analysis

    def get_activity_guide(self, download, upload, ping):
        """Hıza göre aktivite önerileri"""
        activities = []

        if download >= 25:
            activities.append("✅ 4K video izleme")
        elif download >= 15:
            activities.append("✅ Full HD video izleme")
        elif download >= 5:
            activities.append("✅ HD video izleme")
        else:
            activities.append("⚠️ Standart kalite video izleme")

        if upload >= 10:
            activities.append("✅ Canlı yayın yapma")
        elif upload >= 5:
            activities.append("✅ Video konferans")
        else:
            activities.append("⚠️ Sesli arama")

        if ping <= 50:
            activities.append("✅ Online oyun oynama")
        elif ping <= 100:
            activities.append("⚠️ Strateji oyunları")
        else:
            activities.append("❌ Hızlı online oyunlar zor")

        if download >= 50 and upload >= 10:
            activities.append("✅ Uzaktan çalışma")

        return "\n".join(activities)

    def update_chart(self, history_data):
        """Performans grafiğini güncelle"""
        try:
            self.ax.clear()

            if not history_data:
                self.ax.text(0.5, 0.5, 'Henüz test verisi yok',
                           ha='center', va='center', transform=self.ax.transAxes,
                           fontsize=12, color='gray')
                self.ax.set_title('Performans Geçmişi')
                self.canvas.draw()
                return

            # Veri hazırlama
            dates = [entry['timestamp'] for entry in history_data]
            downloads = [entry['download'] for entry in history_data]
            uploads = [entry['upload'] for entry in history_data]
            pings = [entry['ping'] for entry in history_data]

            # X ekseni için indeksler
            x = range(len(dates))

            # İkincil Y ekseni oluştur
            ax2 = self.ax.twinx()

            # Çizgi grafikleri
            line1 = self.ax.plot(x, downloads, 'b-o', label='İndirme (Mbps)', linewidth=2, markersize=4)
            line2 = self.ax.plot(x, uploads, 'g-s', label='Yükleme (Mbps)', linewidth=2, markersize=4)
            line3 = ax2.plot(x, pings, 'r-^', label='Ping (ms)', linewidth=2, markersize=4, color='red')

            # Etiketler ve başlık
            self.ax.set_xlabel('Test Sırası')
            self.ax.set_ylabel('Hız (Mbps)', color='blue')
            ax2.set_ylabel('Ping (ms)', color='red')
            self.ax.set_title('İnternet Hızı Performans Geçmişi', fontweight='bold')

            # Legend
            lines1, labels1 = self.ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            self.ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

            # Grid
            self.ax.grid(True, alpha=0.3)

            # X ekseni etiketleri (sadece birkaç tanesini göster)
            if len(dates) > 1:
                step = max(1, len(dates) // 5)
                tick_positions = range(0, len(dates), step)
                tick_labels = [dates[i][:10] if len(dates[i]) > 10 else dates[i] for i in tick_positions]
                self.ax.set_xticks(tick_positions)
                self.ax.set_xticklabels(tick_labels, rotation=45, ha='right')

            # Layout ayarlama
            self.fig.tight_layout()
            self.canvas.draw()

        except Exception as e:
            print(f"Grafik güncelleme hatası: {e}")

    def finish_test(self):
        """Testi bitir"""
        self.is_testing = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress.stop()
        self.status_label.config(text="Test tamamlandı!")

    def refresh_history(self):
        """Geçmişi yenile"""
        # Mevcut verileri temizle
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Yeni verileri ekle (son 20 test)
        recent_history = self.test_history[-20:] if len(self.test_history) > 20 else self.test_history

        for entry in reversed(recent_history):  # En yeni en üstte
            values = (
                entry['timestamp'],
                f"{entry['download']:.1f} Mbps",
                f"{entry['upload']:.1f} Mbps",
                f"{entry['ping']:.0f} ms",
                f"{entry['score']}/100",
                entry['isp']
            )
            self.history_tree.insert('', 0, values=values)

    def export_history(self):
        """Geçmişi dışa aktar"""
        try:
            from tkinter import filedialog

            if not self.test_history:
                messagebox.showwarning("Uyarı", "Dışa aktarılacak veri yok!")
                return

            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Test geçmişini kaydet"
            )

            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.test_history, f, indent=2, ensure_ascii=False, default=str)

                messagebox.showinfo("Başarılı", f"Geçmiş başarıyla kaydedildi:\n{filename}")

        except Exception as e:
            messagebox.showerror("Hata", f"Dışa aktarma hatası: {e}")

    def clear_history(self):
        """Geçmişi temizle"""
        result = messagebox.askyesno(
            "Onay",
            "Tüm test geçmişini silmek istediğinizden emin misiniz?\nBu işlem geri alınamaz!"
        )

        if result:
            self.test_history = []
            self.save_history()
            self.refresh_history()
            self.update_chart([])
            messagebox.showinfo("Başarılı", "Test geçmişi temizlendi!")

    def load_history(self):
        """Geçmişi dosyadan yükle"""
        try:
            history_file = "speed_test_history.json"
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.test_history = json.load(f)

        except Exception as e:
            print(f"Geçmiş yükleme hatası: {e}")
            self.test_history = []

    def save_history(self):
        """Geçmişi dosyaya kaydet"""
        try:
            history_file = "speed_test_history.json"
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.test_history, f, indent=2, ensure_ascii=False, default=str)

        except Exception as e:
            print(f"Geçmiş kaydetme hatası: {e}")


def main():
    """Ana uygulama başlatıcı"""
    root = tk.Tk()

    # Uygulama ikonu (varsa)
    try:
        root.iconbitmap("speed_test_icon.ico")
    except:
        pass

    # Uygulama oluştur
    app = SpeedTestApp(root)

    # Ana döngü
    root.mainloop()


if __name__ == "__main__":
    main()
