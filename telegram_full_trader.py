#!/usr/bin/env python3
"""
PlanB Ultra - Full Market Telegram Trader
• 991+ varlık için paralel analiz
• 65+ puan güçlü sinyal bildirimi
• Pazar bazında toplam/başarılı/güçlü özetleri
"""
import os
import time
import math
import concurrent.futures as cf
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import requests
import yfinance as yf
try:
    # Dev convenience: load .env if available (no-op in production systemd)
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

# ULTRA Tutma Süresi Modülü
try:
    from ultra_holding_period_calculator import calculate_ultra_holding_period
    ULTRA_HOLDING_AVAILABLE = True
except ImportError:
    ULTRA_HOLDING_AVAILABLE = False

# -------------------------------------------------
# Ayarlar
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# YFinance güvenli parametreler
YF_PERIOD = os.getenv("YF_PERIOD", "1y")
YF_INTERVAL = os.getenv("YF_INTERVAL", "1d")
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "10"))
SYMBOL_TIMEOUT = int(os.getenv("SYMBOL_TIMEOUT", "30"))
BATCH_TIMEOUT = int(os.getenv("BATCH_TIMEOUT", "300"))
SLEEP_BETWEEN_CYCLES = int(os.getenv("SLEEP_BETWEEN_CYCLES", "900"))  # 15 dk

STRONG_THRESHOLD = float(os.getenv("STRONG_THRESHOLD", "65"))  # 65+
MAX_SIGNALS_IN_FIRST_MSG = int(os.getenv("MAX_SIGNALS_IN_FIRST_MSG", "12"))


# -------------------------------------------------
# Yardımcılar
# -------------------------------------------------
def send_telegram_message(message: str) -> bool:
    """Telegram'a mesaj gönderir. Token/Chat ID yoksa loglayıp False döndürür."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[WARN] Telegram token/chat id bulunamadı. .env dosyasında TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID ayarlayın.")
        print(f"[MSG PREVIEW]\n{message}")
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        r = requests.post(url, data=data, timeout=20)
        ok = r.status_code == 200
        if not ok:
            print(f"[ERROR] Telegram HTTP {r.status_code}: {r.text[:200]}")
        return ok
    except Exception as e:
        print(f"[ERROR] Telegram gönderim hatası: {e}")
        return False


def _safe_read_lines(path: Path) -> List[str]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
    except FileNotFoundError:
        print(f"[WARN] Dosya bulunamadı: {path}")
    except Exception as e:
        print(f"[WARN] Dosya okunamadı: {path} -> {e}")
    return []


def _first_token(line: str) -> str:
    """Satırdan ilk ' - ' öncesi token'ı alır (ör: 'AAPL - Apple' -> 'AAPL')"""
    try:
        return line.split(' - ', 1)[0].strip()
    except Exception:
        return line.strip()


def load_bist_symbols() -> List[str]:
    """BIST için ana referans: 'bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt'.
    CSV sadece yedek olarak kullanılır."""
    import csv
    tam_liste = BASE_DIR / "bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt"
    if tam_liste.exists():
        # TAM LİSTE: her satır 'SYMBOL\tCOMPANY\tDATE' formatında
        lines = _safe_read_lines(tam_liste)
        symbols = []
        for ln in lines:
            parts = ln.split("\t")
            if parts and parts[0].strip().endswith(".IS"):
                symbols.append(parts[0].strip())
        if symbols:
            return sorted(set(symbols))

    # Yedek: CSV dosyası
    csv_path = BASE_DIR / "bist_guncel_listesi.csv"
    symbols: List[str] = []
    if csv_path.exists():
        try:
            with csv_path.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    code = (row.get("Hisse Kodu") or "").strip()
                    if code:
                        symbols.append(code)
        except Exception as e:
            print(f"[WARN] BIST csv okunamadı: {e}")
        if symbols:
            return sorted(set(symbols))

    # Son çare: boş liste
    return []


def load_nasdaq_symbols() -> List[str]:
    lines = _safe_read_lines(BASE_DIR / "nasdaq tam liste.txt")
    symbols = [_first_token(l) for l in lines]
    # NASDAQ: doğrudan kodlar (AAPL, MSFT, NVDA ...)
    return sorted(set(s for s in symbols if s))


def load_crypto_symbols() -> List[str]:
    lines = _safe_read_lines(BASE_DIR / "kripto tam liste.txt")
    base = [_first_token(l) for l in lines]
    # CRYPTO: BTC -> BTC-USD formatına çevir
    mapped = [f"{b}-USD" for b in base if b]
    return sorted(set(mapped))


def load_commodity_symbols() -> List[str]:
    lines = _safe_read_lines(BASE_DIR / "emtia tam liste.txt")
    base = [_first_token(l) for l in lines]
    special_map = {
        # Enerji ve metaller (futures)
        "CL": "CL=F", "NG": "NG=F", "GC": "GC=F", "SI": "SI=F", "HG": "HG=F",
        "ZC": "ZC=F", "ZW": "ZW=F", "ZS": "ZS=F", "ZL": "ZL=F", "ZM": "ZM=F",
        "SB": "SB=F", "KC": "KC=F", "CT": "CT=F", "RB": "RB=F", "HO": "HO=F",
        "LE": "LE=F", "HE": "HE=F", "GF": "GF=F", "PA": "PA=F", "PL": "PL=F",
        # Brent özel
        "B0": "BZ=F",
        # Spot metaller
        "XAU": "XAUUSD=X", "XAG": "XAGUSD=X", "XPT": "XPTUSD=X",
        # Kereste (yahoo genelde LBS=F kullanır)
        "LB": "LBS=F",
    }
    mapped: List[str] = []
    for code in base:
        if not code:
            continue
        if code in special_map:
            mapped.append(special_map[code])
        elif len(code) >= 3 and code.isalpha():
            # ETF benzeri kodları olduğu gibi bırak (LIT, URA, WEAT, CORN, USO, UNG ...)
            mapped.append(code)
        else:
            # Genel kural: Fiyatlı vadeli işlemler için =F soneki
            mapped.append(f"{code}=F")
    return sorted(set(mapped))


def load_xetra_symbols() -> List[str]:
    lines = _safe_read_lines(BASE_DIR / "XETRA TAM LİSTE-.txt")
    base = [_first_token(l) for l in lines]
    # XETRA: .DE soneki
    mapped = [f"{b}.DE" for b in base if b]
    return sorted(set(mapped))


def calculate_rsi(prices, period: int = 14) -> float:
    try:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / (loss.replace(0, math.nan))
        rsi = 100 - (100 / (1 + rs))
        val = float(rsi.iloc[-1])
        if math.isnan(val):
            return 50.0
        return max(0.0, min(100.0, val))
    except Exception:
        return 50.0


def analyze_symbol_fast(symbol: str) -> dict | None:
    """Sembol için hızlı skor analizi; başarısızsa None döner."""
    try:
        df = yf.download(symbol, period=YF_PERIOD, interval=YF_INTERVAL, auto_adjust=False, progress=False, threads=False)
        if df is None or df.empty or "Close" not in df.columns:
            return None

        close = df["Close"].dropna()
        if close.empty:
            return None
        price = float(close.iloc[-1])

        # Basit skorlama: RSI + MA + Hacim
        rsi = calculate_rsi(close, period=14)
        try:
            ma20 = float(close.rolling(20).mean().iloc[-1])
            ma50 = float(close.rolling(50).mean().iloc[-1])
        except Exception:
            ma20 = ma50 = price

        ma_score = 50.0
        if price > ma20 > ma50:
            ma_score = 80.0
        elif price > ma20 and price > ma50:
            ma_score = 70.0
        elif price > ma20 or price > ma50:
            ma_score = 60.0
        else:
            ma_score = 40.0

        vol_score = 50.0
        try:
            vol = df["Volume"].dropna()
            if not vol.empty:
                v_now = float(vol.iloc[-1])
                v_avg = float(vol.rolling(20).mean().iloc[-1]) if len(vol) >= 20 else float(vol.mean())
                if v_avg > 0:
                    ratio = v_now / v_avg
                    if ratio >= 1.5:
                        vol_score = 70.0
                    elif ratio >= 1.0:
                        vol_score = 60.0
                    else:
                        vol_score = 45.0
        except Exception:
            vol_score = 50.0

        score = round((rsi + ma_score + vol_score) / 3.0, 1)
        if score >= 80:
            signal = "🟢 AL_GÜÇLÜ"
        elif score >= STRONG_THRESHOLD:
            signal = "🟢 AL"
        elif score >= 50:
            signal = "⚪ TUT"
        else:
            signal = "🔴 SAT"

        return {
            "symbol": symbol,
            "price": round(price, 2),
            "score": score,
            "signal": signal,
            "time": datetime.now().strftime('%H:%M'),
        }
    except Exception as e:
        print(f"[WARN] Analiz hatası {symbol}: {e}")
        return None


def analyze_batch(symbols: List[str], market_name: str) -> Tuple[List[dict], List[dict]]:
    """Listeyi paralel analiz eder. (results, strong) döndürür"""
    results: List[dict] = []
    strong: List[dict] = []
    print(f"📊 {market_name} analizi başlıyor... ({len(symbols)} sembol)")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_symbol = {executor.submit(analyze_symbol_fast, s): s for s in symbols}
        try:
            for future in cf.as_completed(future_to_symbol, timeout=BATCH_TIMEOUT):
                sym = future_to_symbol[future]
                try:
                    r = future.result(timeout=SYMBOL_TIMEOUT)
                    if r:
                        r["market"] = market_name
                        results.append(r)
                        if r["score"] >= STRONG_THRESHOLD:
                            strong.append(r)
                except Exception as e:
                    print(f"❌ {sym} timeout/hata: {e}")
        except Exception as e:
            print(f"[WARN] {market_name} batch zaman aşımı: {e}")

    print(f"✅ {market_name}: {len(results)} analiz OK, {len(strong)} güçlü sinyal")
    return results, strong


def full_market_analysis() -> Tuple[List[dict], Dict[str, Dict[str, int]], int]:
    """Tüm pazarları yükle, analiz et, özetleri hazırla"""
    markets: Dict[str, List[str]] = {
        "BIST": load_bist_symbols(),
        "NASDAQ": load_nasdaq_symbols(),
        "CRYPTO": load_crypto_symbols(),
        "EMTIA": load_commodity_symbols(),
        "XETRA": load_xetra_symbols(),
    }

    market_summary: Dict[str, Dict[str, int]] = {}
    all_strong: List[dict] = []
    total_attempted = 0

    for name, symbols in markets.items():
        total_attempted += len(symbols)
        res, strong = analyze_batch(symbols, name)
        market_summary[name] = {
            "total": len(symbols),
            "ok": len(res),
            "strong": len(strong),
        }
        all_strong.extend(strong)

    # Skora göre sırala
    all_strong.sort(key=lambda x: x.get("score", 0), reverse=True)
    return all_strong, market_summary, total_attempted


def format_signal_line(s: dict) -> str:
    """Sinyal satırını ULTRA tutma süresi ile formatla"""
    base_line = f"{s['signal']} <b>{s['symbol']}</b> | 💰 {s['price']} | 📈 {s['score']}/100"
    
    # ULTRA Tutma Süresi ekle
    if ULTRA_HOLDING_AVAILABLE and 'signal' in s:
        try:
            ultra_holding = calculate_ultra_holding_period(s['symbol'], s['signal'])
            base_line += f" | ⏰ {ultra_holding}"
        except Exception:
            base_line += " | ⏰ 2-4 hafta 🔶 STANDART"
    else:
        base_line += " | ⏰ 2-4 hafta 🔶 STANDART"
    
    return base_line + "\n"


def send_analysis_results(strong_signals: List[dict], market_summary: Dict[str, Dict[str, int]], total_symbols: int):
    """Analiz sonuçlarını Telegram'a gönder"""
    ts = datetime.now().strftime('%d.%m.%Y %H:%M')
    if not strong_signals:
        message = (
            f"📊 <b>PlanB Full Market Analizi</b>\n"
            f"⏰ {ts}\n\n"
            f"📈 Toplam {total_symbols} varlık denendi\n"
            f"⚡ Güçlü sinyal bulunamadı (65+ puan)\n\n"
        )
        for market, data in market_summary.items():
            message += f"{market}: {data['ok']}/{data['total']} analiz\n"
        message += "\n🎯 Tüm pozisyonlar TUT durumunda"
        send_telegram_message(message)
        return

    # Ana mesaj
    message = (
        f"🚀 <b>PlanB ULTRA ANALİZ SONUÇLARI</b>\n"
        f"⏰ {ts}\n\n"
        f"📊 Toplam denenen: {total_symbols}\n"
        f"⚡ Güçlü sinyal: {len(strong_signals)} adet (≥{int(STRONG_THRESHOLD)})\n\n"
    )

    first_batch = strong_signals[:MAX_SIGNALS_IN_FIRST_MSG]
    for s in first_batch:
        message += format_signal_line(s)

    # Pazar özeti
    message += "\n📈 <b>Pazar Özeti:</b>\n"
    for market, data in market_summary.items():
        message += f"{market}: {data['strong']}/{data['total']} güçlü\n"

    message += "\n🤖 <i>PlanB Ultra v2.1 - Full Market</i>"
    send_telegram_message(message)

    # Eğer çok fazla güçlü sinyal varsa, ikinci mesaj gönder
    if len(strong_signals) > MAX_SIGNALS_IN_FIRST_MSG:
        remaining = strong_signals[MAX_SIGNALS_IN_FIRST_MSG:MAX_SIGNALS_IN_FIRST_MSG*2]
        if remaining:
            message2 = "📊 <b>Diğer Güçlü Sinyaller</b>\n\n"
            for s in remaining:
                message2 += format_signal_line(s)
            message2 += f"\n⚡ Toplam {len(strong_signals)} güçlü sinyal"
            send_telegram_message(message2)


def continuous_full_analysis():
    cycle = 0
    while True:
        try:
            cycle += 1
            print(f"\n============================\n🔄 Döngü #{cycle} başlıyor: {datetime.now().strftime('%H:%M:%S')}")
            strong, summary, total = full_market_analysis()
            send_analysis_results(strong, summary, total)
            print(f"😴 {SLEEP_BETWEEN_CYCLES//60} dakika uyku")
            time.sleep(SLEEP_BETWEEN_CYCLES)
        except KeyboardInterrupt:
            print("👋 Sistem durduruldu")
            break
        except Exception as e:
            print(f"[ERROR] Genel hata: {e}")
            time.sleep(60)


if __name__ == "__main__":
    print("🚀 PlanB ULTRA FULL TRADER başlatılıyor...")
    print("📊 991+ varlık analiz sistemi")

    start_msg = (
        f"🤖 <b>PlanB ULTRA SİSTEM BAŞLATILDI!</b>\n"
        f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        f"📊 <b>Analiz Kapsamı:</b>\n"
        f"🇹🇷 BIST: 480+ hisse\n"
        f"🇺🇸 NASDAQ: 109 hisse\n"
        f"💰 CRYPTO: 80 kripto\n"
        f"🏭 EMTIA: 49 emtia\n"
        f"🇩🇪 XETRA: 273 hisse\n\n"
        f"⚡ <b>Toplam: 991+ varlık</b>\n"
        f"🔄 Her 15 dakikada tam analiz\n"
        f"🎯 Sadece {int(STRONG_THRESHOLD)}+ puan sinyaller bildirilir\n"
        f"🚀 Ultra hızlı paralel işlem"
    )

    if send_telegram_message(start_msg):
        print("✅ Sistem başlatıldı, Telegram bildirimi gönderildi")
    else:
        print("❌ Telegram gönderimi yapılamadı (env değişkenlerini kontrol edin)")
    continuous_full_analysis()