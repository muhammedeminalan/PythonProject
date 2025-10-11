# -*- coding: utf-8 -*-
"""
Gelişmiş animasyonlu bar chart race.
- Veri kaynağı: Eğer global 'df' tanımlı ve uygun kolonlara sahipse onu kullanır; yoksa örnek veri üretir.
- Ölçüt: Ürün bazında günlük kümülatif gelir (price * quantity)
- Özellikler:
  * Top-N ürün (varsayılan 8)
  * Tween (ara kare) ile yumuşatılmış geçişler
  * Renk eşlemesi, değer ve delta etiketleri
  * CLI: --save/--out/--show/--days/--products/--top/--tween/--fps/--interval/--seed
  * PillowWriter ile GIF kaydı (mevcutsa); yoksa ffmpeg'e düşer; o da yoksa sadece gösterir
"""

from __future__ import annotations

import os
import sys
import argparse
from dataclasses import dataclass
from typing import List, Tuple, Optional

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as mtick
import matplotlib.colors as mcolors

# Daha hoş görünüm için bir stil seçelim (Matplotlib 3.6+ uyumlu)
plt.style.use("seaborn-v0_8-darkgrid")
# Unicode karakterleri (₺) için geniş kapsamlı font ve eksi çizgisi
matplotlib.rcParams["font.family"] = [
    "DejaVu Sans",
    "Arial Unicode MS",
    "Arial",
]
matplotlib.rcParams["axes.unicode_minus"] = False


@dataclass
class Config:
    top_n: int = 8
    tween: int = 6            # günler arası ara kare sayısı (yumuşatma)
    fps: int = 15             # kayıtta saniyedeki kare
    interval: int = 150       # milisaniye (ekranda animasyon)
    days: int = 90
    products: int = 10
    seed: int = 42
    save: bool = False
    show: bool = True
    out: str = "bar_race.gif"
    csv: Optional[str] = None


def parse_args() -> Config:
    p = argparse.ArgumentParser(description="Gelişmiş bar chart race animasyonu")
    p.add_argument("--top", type=int, default=Config.top_n)
    p.add_argument("--tween", type=int, default=Config.tween)
    p.add_argument("--fps", type=int, default=Config.fps)
    p.add_argument("--interval", type=int, default=Config.interval)
    p.add_argument("--days", type=int, default=Config.days)
    p.add_argument("--products", type=int, default=Config.products)
    p.add_argument("--seed", type=int, default=Config.seed)
    p.add_argument("--save", action="store_true", help="Animasyonu dosyaya kaydet")
    p.add_argument("--show", action="store_true", help="Animasyonu ekranda göster")
    p.add_argument("--out", type=str, default=Config.out)
    p.add_argument("--csv", type=str, default=None, help="CSV veri dosyası (kolonlar: order_date, product, price, quantity)")
    args = p.parse_args(args=None if sys.argv[1:] else [])

    # Varsayılan davranış: eğer --save verilmişse show=False, aksi halde show=True
    show = args.show if args.show else (False if args.save else True)
    return Config(
        top_n=args.top,
        tween=max(1, args.tween),
        fps=max(1, args.fps),
        interval=max(1, args.interval),
        days=max(2, args.days),
        products=max(2, args.products),
        seed=args.seed,
        save=bool(args.save),
        show=bool(show),
        out=args.out,
        csv=args.csv,
    )


# ------------------------------------------------------------
# Veri hazırlık
# ------------------------------------------------------------

def has_valid_df() -> bool:
    """Global df mevcut ve gerekli kolonlara sahip mi?"""
    g = globals()
    if "df" not in g:
        return False
    required = {"order_date", "product", "price", "quantity"}
    if not required.issubset(set(g["df"].columns)):
        return False
    return True


def coerce_df(dfi: pd.DataFrame) -> pd.DataFrame:
    dfi = dfi.copy()
    # Tarih kolonu datetime olsun
    if not np.issubdtype(dfi["order_date"].dtype, np.datetime64):
        dfi["order_date"] = pd.to_datetime(dfi["order_date"], errors="coerce")
    dfi.dropna(subset=["order_date", "product", "price", "quantity"], inplace=True)
    # Tür düzeltmeleri
    dfi["price"] = pd.to_numeric(dfi["price"], errors="coerce").fillna(0.0)
    dfi["quantity"] = pd.to_numeric(dfi["quantity"], downcast="integer", errors="coerce").fillna(0).astype(int)
    return dfi


def generate_sample_data(days: int, n_products: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    start = pd.Timestamp.today().normalize() - pd.Timedelta(days=days)
    dates = pd.date_range(start=start, periods=days, freq="D")

    # Ürün isimleri
    prods = [f"Ürün {i+1}" for i in range(n_products)]

    # Her ürün için baz fiyat ve talep; günden güne küçük rastgele yürüyüşler
    base_price = rng.uniform(50, 300, size=n_products)
    base_demand = rng.uniform(20, 120, size=n_products)

    rows = []
    for d in dates:
        # Günlük pazar faktörü (kampanya/hafta sonu etkisi gibi)
        market_boost = 1.0 + float(rng.normal(0.0, 0.08))
        for i, prod in enumerate(prods):
            # Günlük fiyat ve talep varyasyonu (random walk hissiyatı)
            price_noise = float(rng.normal(0, 0.03))
            price = max(5.0, float(base_price[i]) * (1 + price_noise))
            demand_noise = float(rng.normal(0, 0.12))
            demand = max(1.0, float(base_demand[i]) * (1 + demand_noise)) * market_boost
            # O gün oluşan sipariş sayısını kaba tahmin (Poisson çevresinde)
            lam = 5 + demand / 30.0
            orders = int(rng.poisson(lam))
            if orders == 0:
                # En az 1 satır olsun
                orders = 1
            for _ in range(orders):
                rnd_qty = int(rng.integers(1, 6))
                qty = max(1, rnd_qty)
                # Minik fiyat gürültüsü
                p = max(3.0, price * (1 + float(rng.normal(0, 0.02))))
                rows.append((d, prod, p, qty))

    dfa = pd.DataFrame(rows, columns=["order_date", "product", "price", "quantity"])
    return dfa


def build_cumulative(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[pd.Timestamp]]:
    dfx = coerce_df(df)
    dfx["date"] = dfx["order_date"].dt.date
    dfx["total"] = dfx["price"] * dfx["quantity"]

    daily_total = (
        dfx.groupby(["date", "product"])["total"]
          .sum()
          .unstack(fill_value=0)
          .sort_index()
    )
    cum = daily_total.cumsum()
    dates = list(pd.to_datetime(cum.index))
    return cum, dates


# ------------------------------------------------------------
# Animasyon
# ------------------------------------------------------------

def make_color_map(labels: List[str]) -> dict:
    # Tab20 + Set3 karışımı ile geniş palet
    palettes = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
    # Çok koyu/açık renkleri filtrelemek yerine basit döngü yeterli
    color_map = {}
    for i, lab in enumerate(labels):
        color_map[lab] = palettes[i % len(palettes)]
    return color_map


def build_tween_frames(cum: pd.DataFrame, tween: int) -> List[pd.Series]:
    # İlk kare doğrudan ilk gün
    frames: List[pd.Series] = [cum.iloc[0]]
    for i in range(len(cum) - 1):
        v0 = cum.iloc[i]
        v1 = cum.iloc[i + 1]
        for s in range(tween):
            alpha = (s + 1) / tween
            frames.append(v0 * (1 - alpha) + v1 * alpha)
    return frames


def format_currency(x: float) -> str:
    return f"{x:,.0f} ₺".replace(",", ".")  # TR için basit nokta ayracı


def animate_bar_race(cum: pd.DataFrame, dates: List[pd.Timestamp], cfg: Config) -> FuncAnimation:
    products = list(cum.columns)
    color_map = make_color_map(products)

    frames = build_tween_frames(cum, cfg.tween)
    total_frames = len(frames)

    fig, ax = plt.subplots(figsize=(11, 7))
    fmt = mtick.StrMethodFormatter("{x:,.0f} ₺")

    def update(frame_idx: int):
        ax.clear()
        artists = []
        cur = frames[frame_idx]
        # Kaçıncı tarih aralığındayız?
        day_idx = min(frame_idx // cfg.tween, len(dates) - 1)
        cur_date = dates[day_idx]

        top = cur.nlargest(cfg.top_n).sort_values()
        bar_colors = [color_map.get(p, "C0") for p in top.index]
        bars = ax.barh(top.index, top.values, color=bar_colors, edgecolor="#333", alpha=0.9)
        artists.extend(bars)

        # Dinamik x limiti: mevcut tepe değerin %15 üstü
        local_max = max(1.0, float(top.values.max()))
        ax.set_xlim(0, local_max * 1.15)

        ax.set_xlabel("Kümülatif Gelir", fontsize=11)
        ax.xaxis.set_major_formatter(fmt)
        ax.set_title("En çok gelir getiren ürünler [kümülatif]", fontsize=14, pad=12)

        # Etiketler (değer ve delta)
        prev = frames[frame_idx - 1] if frame_idx > 0 else cur
        for y, (name, val) in enumerate(zip(top.index, top.values)):
            dv = float(val - prev.get(name, 0.0))
            sign = "+" if dv >= 0 else "−"
            dv_abs = abs(dv)
            t = ax.text(val, y, f"  {format_currency(val)}  ({sign}{dv_abs:,.0f})",
                        va="center", ha="left", fontsize=10, color="#222")
            artists.append(t)

        # Büyük tarih etiketi (sağ alt)
        t_date = ax.text(0.98, 0.06, cur_date.strftime("%d %b %Y"), transform=ax.transAxes,
                         ha="right", va="center", fontsize=13, color="#555")
        artists.append(t_date)

        # Sıra numarası (sol tarafa küçük)
        for i, (name, val) in enumerate(zip(top.index, top.values)):
            t_rank = ax.text(0.01, i, f"{i + 1}.", transform=ax.get_yaxis_transform(),
                             ha="left", va="center", fontsize=10, color="#666")
            artists.append(t_rank)

        ax.grid(axis="x", linestyle=":", alpha=0.5)
        ax.set_ylabel("")
        # Y eksenini okunaklı yapalım
        ax.tick_params(axis="y", labelsize=10)

        # Küçük dipnot
        t_note = ax.text(0.005, 0.98,
                         "Kaynak: Sentetik veri veya sağlanan df | Ölçek: ₺",
                         transform=ax.transAxes, ha="left", va="top", fontsize=8, color="#777")
        artists.append(t_note)

        return artists

    ani = FuncAnimation(fig, update, frames=total_frames, interval=cfg.interval, repeat=True)
    fig.tight_layout()
    return ani


# ------------------------------------------------------------
# Çalıştırma
# ------------------------------------------------------------

def main():
    cfg = parse_args()

    # Headless koşullarda kaydetmek istiyorsak Agg kullan
    if cfg.save and not cfg.show:
        try:
            matplotlib.use("Agg", force=True)
        except Exception:
            pass

    # Veri kaynağı: öncelik --csv
    if cfg.csv and os.path.exists(cfg.csv):
        try:
            dfx_raw = pd.read_csv(cfg.csv)
            # order_date'i parse etmeyi dene
            if "order_date" in dfx_raw.columns:
                dfx_raw["order_date"] = pd.to_datetime(dfx_raw["order_date"], errors="coerce")
            dfx = coerce_df(dfx_raw)
        except Exception as e:
            print("CSV okunamadı, sentetik veriye düşülüyor:", e)
            dfx = generate_sample_data(cfg.days, cfg.products, cfg.seed)
    elif has_valid_df():
        dfx = coerce_df(globals()["df"])  # type: ignore[name-defined]
    else:
        dfx = generate_sample_data(cfg.days, cfg.products, cfg.seed)

    cum, dates = build_cumulative(dfx)

    # Koruma: veri yoksa minimal sentetik oluştur
    if cum.shape[0] < 2 or cum.shape[1] == 0:
        dfx = generate_sample_data(cfg.days, max(cfg.products, 6), cfg.seed)
        cum, dates = build_cumulative(dfx)

    ani = animate_bar_race(cum, dates, cfg)

    # Kaydetme/gösterme mantığı
    if cfg.save:
        # Çıktı uzantısına göre writer seçimi
        out_path = cfg.out
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        try:
            from matplotlib.animation import PillowWriter
            writer = PillowWriter(fps=cfg.fps)
            ani.save(out_path, writer=writer)
            print(f"Animasyon kaydedildi: {out_path}")
        except Exception as e_gif:
            try:
                alt_out = out_path.replace(".gif", ".mp4")
                ani.save(alt_out, writer="ffmpeg", fps=cfg.fps)
                print(f"Animasyon kaydedildi: {alt_out}")
            except Exception as e_mp4:
                # Son çare: tek kare PNG
                png_out = out_path.rsplit(".", 1)[0] + ".png"
                plt.gcf().savefig(png_out, dpi=150)
                print("Animasyon kaydetme başarısız oldu, tek kare PNG kaydedildi:", png_out)
                print("Hata detayları:", e_gif, e_mp4)
    if cfg.show:
        plt.show()


if __name__ == "__main__":
    main()
