import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# ----------------------------
# ANA PENCERE OLUŞTUR
# ----------------------------
root = tk.Tk()
root.title("Tkinter Profesyonel GUI Örneği")
root.geometry("700x550")
root.resizable(False, False)

# ----------------------------
# MENÜ ÇUBUĞU
# ----------------------------
menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Yeni")
file_menu.add_command(label="Aç")
file_menu.add_separator()
file_menu.add_command(label="Çıkış", command=root.quit)
menubar.add_cascade(label="Dosya", menu=file_menu)

# ----------------------------
# NOTEBOOK (SEKME YAPISI)
# ----------------------------
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, pady=10, padx=10)

# Sekme 1 – Form Alanı
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Form")

# Sekme 2 – Çizim Alanı
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Çizim")

# Sekme 3 – İlerleme Çubuğu
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="İlerleme")

# ===================================================
# SEKME 1: FORM ALANI
# ===================================================
frame_top = ttk.Frame(tab1, padding=10)
frame_top.pack(fill='x')

ttk.Label(frame_top, text="Adınız:").pack(side='left', padx=5)
name_var = tk.StringVar()
ttk.Entry(frame_top, textvariable=name_var).pack(side='left', padx=5)

def greet_user():
    ad = name_var.get()
    if ad.strip() == "":
        messagebox.showwarning("Uyarı", "Lütfen adınızı girin!")
    else:
        messagebox.showinfo("Merhaba!", f"Hoş geldin {ad}! 👋")

ttk.Button(frame_top, text="Selamla", command=greet_user).pack(side='left', padx=10)

# Radiobutton & Checkbutton
frame_bottom = ttk.Frame(tab1, padding=10)
frame_bottom.pack(fill='x')

gender_var = tk.StringVar(value="Belirtilmedi")
ttk.Label(frame_bottom, text="Cinsiyet:").grid(column=0, row=0, sticky='w')
ttk.Radiobutton(frame_bottom, text="Kadın", value="Kadın", variable=gender_var).grid(column=1, row=0)
ttk.Radiobutton(frame_bottom, text="Erkek", value="Erkek", variable=gender_var).grid(column=2, row=0)

agree_var = tk.BooleanVar()
ttk.Checkbutton(frame_bottom, text="Kullanım koşullarını kabul ediyorum", variable=agree_var).grid(column=0, row=1, columnspan=3, pady=5)

# Combobox
ttk.Label(frame_bottom, text="Şehir:").grid(column=0, row=2, sticky='w')
city_var = tk.StringVar()
city_box = ttk.Combobox(frame_bottom, textvariable=city_var, values=["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya"])
city_box.grid(column=1, row=2, columnspan=2, pady=5)
city_box.current(0)

# Listbox
ttk.Label(frame_bottom, text="Sevdiğiniz diller:").grid(column=0, row=3, sticky='w')
lang_listbox = tk.Listbox(frame_bottom, selectmode='multiple', height=5)
for lang in ["Python", "JavaScript", "C#", "Java", "C++"]:
    lang_listbox.insert('end', lang)
lang_listbox.grid(column=1, row=3, columnspan=2, pady=5)

# ===================================================
# SEKME 2: ÇİZİM ALANI
# ===================================================
canvas = tk.Canvas(tab2, width=400, height=300, bg="white", borderwidth=2, relief="ridge")
canvas.pack(pady=20)

# Şekiller çizelim
canvas.create_rectangle(50, 50, 150, 150, fill="lightblue", outline="black")
canvas.create_oval(200, 50, 300, 150, fill="pink", outline="black")

# Fare tıklamasıyla etkileşim
def on_click(event):
    canvas.create_text(event.x, event.y, text="⭐", font=("Arial", 12))

canvas.bind("<Button-1>", on_click)

# ===================================================
# SEKME 3: İLERLEME ÇUBUĞU
# ===================================================
frame_progress = ttk.Frame(tab3, padding=20)
frame_progress.pack(fill='x')

ttk.Label(frame_progress, text="Dosya yükleme simülasyonu:").pack(pady=10)

progress = ttk.Progressbar(frame_progress, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=10)

# İlerlemeyi artıran fonksiyon
def start_progress():
    progress["value"] = 0
    max_value = 100
    for i in range(max_value + 1):
        progress["value"] = i
        progress.update_idletasks()  # GUI'yi güncel tutar
        root.after(20)  # her adımda küçük gecikme

    messagebox.showinfo("Tamamlandı", "Yükleme tamamlandı ✅")

ttk.Button(frame_progress, text="Başlat", command=start_progress).pack(pady=10)

# ===================================================
# STİL AYARLARI
# ===================================================
style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
style.configure("TLabel", font=("Arial", 10))
style.configure("TCheckbutton", font=("Arial", 9))
style.configure("TRadiobutton", font=("Arial", 9))
style.configure("TNotebook", tabmargins=[2, 5, 2, 0])
style.configure("TNotebook.Tab", font=("Arial", 10, "bold"))

# ===================================================
# ANA DÖNGÜ
# ===================================================
root.mainloop()