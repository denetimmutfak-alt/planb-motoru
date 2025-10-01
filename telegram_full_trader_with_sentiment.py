#!/usr/bin/env python3
"""
PlanB Ultra if SENTIMENT_ENABLED:
    try:
        from enhanced_sentiment_analyzer import EnhancedSentimentAnalyzer
        SENTIMENT_ANALYZER = EnhancedSentimentAnalyzer()
        print("✅ Enhanced Sentiment Analysis activated")
    except ImportError as e:
        print(f"⚠️ Sentiment analyzer not available: {e}")
        SENTIMENT_ENABLED = False

# Initialize Signal Tracker
if REMINDER_ENABLED:
    try:
        from signal_tracker import SignalTracker
        SIGNAL_TRACKER = SignalTracker()
        print("✅ Signal Tracker & Reminder System activated")
    except ImportError as e:
        print(f"⚠️ Signal tracker not available: {e}")
        REMINDER_ENABLED = Falsearket Telegram Trader
• 991+ varlık için paralel analiz
• 65+ puan güçlü sinyal bildirimi
• Pazar bazında toplam/başarılı/güçlü özetleri
• Enhanced Sentiment Analysis Integration
"""
import os
import time
import math
import concurrent.futures as cf
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import json
import csv

import requests
import yfinance as yf  # Keep for compatibility
from resilient_loader_v2 import cached_download  # Enhanced v2 with parquet + 2-day TTL
from proxy_rotate import enhanced_download_with_fallback  # Optional proxy fallback
from fix_series_bool import safe_float_from_series
import json
import csv
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

# V2 Optimization Modules
try:
    from early_v2 import ew_optimized
    from ultra_v3 import compute_ultra_v3
    from vol_spike import refined_volume_spike, volume_spike_indicator
    from early_warning import early_score, hourly_momentum, dynamic_threshold, get_market_from_symbol, volume_spike_detected
    from early_warning_markets import nasdaq_early_score, xetra_early_score, emtia_early_score, crypto_early_score
    V2_MODULES_AVAILABLE = True
    print("✅ V2 Optimization modules loaded")
except ImportError as e:
    V2_MODULES_AVAILABLE = False
    print(f"⚠️ V2 modules not available: {e}")

# Enhanced Sentiment Analysis - Optional Integration
SENTIMENT_ENABLED = os.getenv("SENTIMENT_ENABLED", "false").lower() == "true"
SENTIMENT_ANALYZER = None

# Signal Tracking & Reminder System
REMINDER_ENABLED = os.getenv("REMINDER_ENABLED", "true").lower() == "true"
SIGNAL_TRACKER = None

if SENTIMENT_ENABLED:
    try:
        from enhanced_sentiment_analyzer import EnhancedSentimentAnalyzer
        SENTIMENT_ANALYZER = EnhancedSentimentAnalyzer()
        print("✅ Enhanced Sentiment Analysis activated")
    except Exception as e:
        print(f"⚠️ Sentiment analyzer not available: {e}")
        SENTIMENT_ENABLED = False

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

# Sentiment analysis settings
SENTIMENT_WEIGHT = float(os.getenv("SENTIMENT_WEIGHT", "0.15"))  # %15 weight for sentiment
SENTIMENT_MIN_IMPACT = float(os.getenv("SENTIMENT_MIN_IMPACT", "5.0"))  # Minimum 5 point impact


# -------------------------------------------------
# Yardımcılar
# -------------------------------------------------
def send_telegram_message(message: str, reply_markup: dict = None) -> bool:
    """Telegram'a mesaj gönderir. İsteğe bağlı inline keyboard desteği."""
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
        if reply_markup:
            data["reply_markup"] = reply_markup
        
        r = requests.post(url, json=data, timeout=20)
        ok = r.status_code == 200
        if not ok:
            print(f"[ERROR] Telegram HTTP {r.status_code}: {r.text[:200]}")
        return ok
    except Exception as e:
        print(f"[ERROR] Telegram gönderim hatası: {e}")
        return False


def create_reminder_button(symbol: str, price: float = 0, score: float = 0) -> dict:
    """Enhanced AL sinyali için hatırlatma butonu oluşturur"""
    try:
        from interactive_reminder import create_reminder_button as create_v2_button
        return create_v2_button(symbol)
    except ImportError:
        # Fallback to old method
        return {
            "inline_keyboard": [[
                {
                    "text": f"⏰ {symbol} için SAT hatırlatması kur",
                    "callback_data": f"rem_{symbol}"
                }
            ]]
        }


def save_reminder_request(user_id: str, symbol: str, price: float, score: float, days: int):
    """Hatırlatma isteğini CSV dosyasına kaydeder"""
    try:
        reminder_file = BASE_DIR / "data" / "reminders.csv"
        reminder_file.parent.mkdir(exist_ok=True)
        
        deadline = datetime.now() + timedelta(days=days)
        
        # CSV başlık kontrolü
        file_exists = reminder_file.exists()
        with open(reminder_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["user_id", "symbol", "price", "score", "signal_date", "deadline", "reminded"])
            
            writer.writerow([
                user_id,
                symbol,
                price,
                score,
                datetime.now().strftime("%Y-%m-%d"),
                deadline.strftime("%Y-%m-%d"),
                0  # reminded flag
            ])
        
        print(f"✅ Hatırlatma kaydedildi: {symbol} -> {deadline.strftime('%d.%m.%Y')}")
        return True
        
    except Exception as e:
        print(f"❌ Hatırlatma kayıt hatası: {e}")
        return False




def save_reminder_request(symbol: str, price: float, score: float, user_id: str = None) -> bool:
    """Hatırlatma isteğini CSV'ye kaydet"""
    try:
        # ULTRA tutma süresini hesapla
        holding_days = 21  # Varsayılan 3 hafta
        if ULTRA_HOLDING_AVAILABLE:
            try:
                ultra_period = calculate_ultra_holding_period(symbol, "🟢 AL")
                if "1-2 hafta" in ultra_period:
                    holding_days = 10
                elif "2-4 hafta" in ultra_period:
                    holding_days = 21
                elif "4-6 hafta" in ultra_period:
                    holding_days = 35
            except:
                holding_days = 21
        
        deadline = datetime.now() + timedelta(days=holding_days)
        
        # CSV dosyasına kaydet
        csv_file = BASE_DIR / "data" / "reminders.csv"
        csv_file.parent.mkdir(exist_ok=True)
        
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Header yoksa ekle
            if csv_file.stat().st_size == 0:
                writer.writerow(["user_id", "symbol", "al_price", "al_score", "al_date", "deadline", "notified"])
            
            writer.writerow([
                user_id or TELEGRAM_CHAT_ID,
                symbol,
                price,
                score, 
                datetime.now().strftime("%Y-%m-%d"),
                deadline.strftime("%Y-%m-%d"),
                0
            ])
        
        print(f"✅ Hatırlatma kaydedildi: {symbol} -> {deadline.strftime('%Y-%m-%d')}")
        return True
        
    except Exception as e:
        print(f"❌ Hatırlatma kaydetme hatası: {e}")
        return False


def handle_callback_query(update_data: dict) -> bool:
    """Enhanced Telegram callback query işle (button tıklamaları)"""
    try:
        callback_data = update_data.get('callback_data', '')
        user_id = str(update_data.get('from', {}).get('id', TELEGRAM_CHAT_ID))
        
        # Enhanced reminder system callback (rem_TICKER format)
        if callback_data.startswith("rem_"):
            try:
                from interactive_reminder import add_reminder
                ticker = callback_data.split("_")[1]
                
                # Add reminder with 28 days default
                if add_reminder(user_id, ticker, 28):
                    success_msg = f"✅ <b>Hatırlatma kuruldu!</b>\n\n🎯 {ticker} için 28 gün sonra SAT hatırlatması alacaksınız."
                    send_telegram_message(success_msg)
                    return True
                else:
                    send_telegram_message("❌ Hatırlatma kurulumunda hata oluştu.")
                    return False
            except ImportError:
                pass
        
        # Legacy reminder system (remind_SYMBOL_PRICE_SCORE format)        
        if callback_data.startswith('remind_'):
            parts = callback_data.split('_')
            if len(parts) >= 4:
                symbol = parts[1]
                price = float(parts[2])
                score = float(parts[3])
                
                # Hatırlatmayı kaydet
                if save_reminder_request(symbol, price, score, user_id):
                    # Kullanıcıya onay mesajı gönder
                    success_msg = f"✅ <b>Hatırlatma kuruldu!</b>\n\n🎯 {symbol} için SAT zamanı gelince hatırlatılacaksınız."
                    send_telegram_message(success_msg)
                    return True
                else:
                    send_telegram_message("❌ Hatırlatma kurulumunda hata oluştu.")
                    return False
                    
        return False
    except Exception as e:
        print(f"❌ Callback işleme hatası: {e}")
        return False


def setup_webhook() -> bool:
    """Telegram webhook kurulum (opsiyonel)"""
    try:
        # Webhook URL - production'da gerçek URL kullanın
        webhook_url = "https://your-domain.com/webhook"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
        data = {"url": webhook_url}
        
        r = requests.post(url, json=data, timeout=10)
        if r.status_code == 200:
            print("✅ Webhook kuruldu")
            return True
        else:
            print(f"❌ Webhook kurulum hatası: {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Webhook hatası: {e}")
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
    """Satırdan ilk token'ı alır - TAB veya ' - ' ile ayrılmış formatları destekler"""
    try:
        # Önce TAB ile ayırmaya çalış (BIST formatı için)
        if '\t' in line:
            return line.split('\t', 1)[0].strip()
        # Sonra ' - ' ile ayır (NASDAQ formatı için)
        elif ' - ' in line:
            return line.split(' - ', 1)[0].strip()
        # Hiçbiri yoksa boşlukla ayır ve ilk parçayı al
        else:
            return line.split()[0].strip() if line.split() else line.strip()
    except Exception:
        return line.strip()


def load_bist_symbols() -> List[str]:
    """BIST için önce yeni temiz liste, sonra eski liste, CSV sadece yedek."""
    # Önce yeni temiz format listesini dene
    lines = _safe_read_lines(BASE_DIR / "BIST_GUNCEL_TAM_LISTE_NEW.txt")
    if lines:
        print(f"[INFO] Yeni BIST listesi kullanılıyor: {len(lines)} sembol")
        return [_first_token(line) + ".IS" for line in lines]
    
    # Eski liste ile devam et
    print("[WARN] Yeni BIST listesi bulunamadı, eski listeye geçiş")
    lines = _safe_read_lines(BASE_DIR / "bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt")
    if lines:
        return [_first_token(line) + ".IS" for line in lines]
        
    # Son çare CSV
    print("[WARN] Ana BIST listesi bulunamadı, CSV'ye geçiş")
    try:
        import pandas as pd
        df = pd.read_csv(BASE_DIR / "bist_guncel_listesi.csv")
        if "Symbol" in df.columns:
            return [s + ".IS" for s in df["Symbol"].dropna().astype(str).tolist()]
        elif "Kod" in df.columns:
            return [s + ".IS" for s in df["Kod"].dropna().astype(str).tolist()]
    except Exception as e:
        print(f"[WARN] CSV yedek hatası: {e}. Fallback listeye geçiş")
        return [f"{s}.IS" for s in ["THYAO", "ASELS", "TUPRS", "GARAN", "ISCTR"]]


def load_nasdaq_symbols() -> List[str]:
    """NASDAQ hisseleri"""
    lines = _safe_read_lines(BASE_DIR / "nasdaq tam liste.txt")
    return [_first_token(line) for line in lines]


def load_crypto_symbols() -> List[str]:
    """Kripto listesi"""
    lines = _safe_read_lines(BASE_DIR / "kripto tam liste.txt")
    return [_first_token(line) for line in lines]


def load_commodity_symbols() -> List[str]:
    """Emtia listesi"""
    lines = _safe_read_lines(BASE_DIR / "emtia tam liste.txt")
    return [_first_token(line) for line in lines]


def load_xetra_symbols() -> List[str]:
    """XETRA (Almanya) listesi"""
    lines = _safe_read_lines(BASE_DIR / "XETRA TAM LİSTE-.txt")
    return [_first_token(line) for line in lines]


def get_sentiment_score(symbol: str) -> float:
    """
    Get sentiment score for a symbol (safe fallback if sentiment not available)
    Returns score between 0-100, defaults to neutral (50) if unavailable
    """
    if not SENTIMENT_ENABLED or not SENTIMENT_ANALYZER:
        return 50.0  # Neutral sentiment if not enabled
    
    try:
        # Remove market suffix for sentiment analysis (e.g., AAPL.IS -> AAPL)
        clean_symbol = symbol.split('.')[0]
        sentiment_score = SENTIMENT_ANALYZER.get_symbol_sentiment(clean_symbol)
        return float(sentiment_score) if sentiment_score is not None else 50.0
    except Exception as e:
        print(f"[DEBUG] Sentiment error for {symbol}: {e}")
        return 50.0  # Return neutral on any error


def calculate_rsi(prices, period=14):
    """RSI hesaplaması"""
    try:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return safe_float_from_series(rsi.iloc[-1:]) if not rsi.empty else 50.0
    except Exception:
        return 50.0


def analyze_symbol_fast(symbol: str) -> dict | None:
    """Sembol için hızlı skor analizi; başarısızsa None döner."""
    try:
        # Use resilient loader instead of direct yfinance
        df = cached_download(symbol, period=YF_PERIOD, interval=YF_INTERVAL, ttl=3600)
        if df is None or df.empty or "Close" not in df.columns:
            return None

        close = df["Close"].dropna()
        if close.empty:
            return None
        price = safe_float_from_series(close.iloc[-1:]) if not close.empty else 0.0

        # Basit skorlama: RSI + MA + Hacim
        rsi = calculate_rsi(close, period=14)
        try:
            ma20_series = close.rolling(20).mean()
            ma50_series = close.rolling(50).mean()
            ma20 = safe_float_from_series(ma20_series.iloc[-1]) if not ma20_series.empty else price
            ma50 = safe_float_from_series(ma50_series.iloc[-1]) if not ma50_series.empty else price
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
                v_now = safe_float_from_series(vol.iloc[-1]) if not vol.empty else 0.0
                vol_mean_series = vol.rolling(20).mean() if len(vol) >= 20 else vol
                v_avg = safe_float_from_series(vol_mean_series.iloc[-1]) if not vol_mean_series.empty else safe_float_from_series(vol.mean()) if not vol.empty else 1.0
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

        # Calculate base technical score (45% weight)
        base_technical_score = (rsi + ma_score + vol_score) / 3.0
        
        # Get ULTRA modül contributions (40% weight)
        ultra_score = 50.0  # Default neutral score
        if ULTRA_HOLDING_AVAILABLE:
            try:
                # Get ULTRA holding period data which includes module scores
                ultra_data = calculate_ultra_holding_period(symbol, "ANALYSIS_MODE")
                if isinstance(ultra_data, dict) and 'total_score' in ultra_data:
                    # Convert ULTRA score (typically 50-150) to 0-100 scale
                    ultra_raw = ultra_data['total_score']
                    ultra_score = min(100, max(0, (ultra_raw - 50) * 1.0 + 50))
                    
                    # Enhanced scoring for CRYPTO and COMMODITIES
                    if symbol.endswith('-USD'):  # Crypto
                        try:
                            from crypto_corporate_data import get_crypto_corporate_score
                            crypto_data = get_crypto_corporate_score(symbol)
                            ultra_score = (ultra_score * (1 - crypto_data['weight'])) + (crypto_data['score'] * crypto_data['weight'])
                        except ImportError:
                            pass
                    elif '=F' in symbol:  # Commodities
                        try:
                            from commodity_corporate_data import get_commodity_corporate_score
                            commodity_data = get_commodity_corporate_score(symbol)
                            ultra_score = (ultra_score * (1 - commodity_data['weight'])) + (commodity_data['score'] * commodity_data['weight'])
                        except ImportError:
                            pass
                            
            except Exception as e:
                print(f"[DEBUG] ULTRA score calculation error for {symbol}: {e}")
        
        # Add sentiment analysis if enabled (15% weight)
        sentiment_score = 50.0  # Default neutral
        sentiment_info = ""
        
        if SENTIMENT_ENABLED:
            try:
                # Enhanced sentiment for CRYPTO and COMMODITIES
                if symbol.endswith('-USD'):  # Crypto
                    try:
                        from enhanced_sentiment_sources import get_enhanced_crypto_sentiment
                        crypto_sentiment = get_enhanced_crypto_sentiment(symbol)
                        sentiment_score = crypto_sentiment['final_score']
                    except ImportError:
                        sentiment_score = get_sentiment_score(symbol)
                elif '=F' in symbol:  # Commodities
                    try:
                        from enhanced_sentiment_sources import get_enhanced_commodity_sentiment
                        commodity_sentiment = get_enhanced_commodity_sentiment(symbol)
                        sentiment_score = commodity_sentiment['final_score']
                    except ImportError:
                        sentiment_score = get_sentiment_score(symbol)
                else:
                    sentiment_score = get_sentiment_score(symbol)
                    
                # Add sentiment indicator to output
                if sentiment_score >= 60:
                    sentiment_info = f" 📈{sentiment_score:.0f}"
                elif sentiment_score <= 40:
                    sentiment_info = f" 📉{sentiment_score:.0f}"
                else:
                    sentiment_info = f" ➡️{sentiment_score:.0f}"
                        
            except Exception as e:
                print(f"[DEBUG] Sentiment integration error for {symbol}: {e}")
        
        # Final weighted score calculation
        # Technical: 45%, ULTRA: 40%, Sentiment: 15%
        final_score = (base_technical_score * 0.45) + (ultra_score * 0.40) + (sentiment_score * 0.15)
        
        # Enhanced Warning System Integration - v2 optimizations
        try:
            if V2_MODULES_AVAILABLE:
                market = get_market_from_symbol(symbol)
                
                # Original early warning
                bonus = early_score(df, market)
                h1_mom = hourly_momentum(symbol) * 10
                
                # v2 Enhanced Early Warning (0-40 bonus)
                ew_v2_bonus = ew_optimized(df, market)
            
            # Calculate returns for ULTRA v3
            returns = df['Close'].pct_change(fill_method=None).dropna().values
            
            # ULTRA v3 with enhanced sensitivity (45 max vs old 35)
            ultra_v3_score = compute_ultra_v3(returns) if len(returns) >= 19 else 0
            
            # Apply all bonuses
            final_score += bonus + h1_mom + ew_v2_bonus + ultra_v3_score
            
            # >>> Pazar özel early-warning (ekleme, mevcut mimariyi bozmaz)
            try:
                market_early_score = 0
                if market == "NASDAQ":
                    market_early_score = nasdaq_early_score(df_daily)
                    if market_early_score > 15:
                        print(f"🇺🇸 NASDAQ Early Warning: {symbol} → +{market_early_score} puan")
                
                elif market == "XETRA":
                    market_early_score = xetra_early_score(df_daily)
                    if market_early_score > 15:
                        print(f"🇩🇪 XETRA Early Warning: {symbol} → +{market_early_score} puan")
                
                elif market == "EMTIA":
                    market_early_score = emtia_early_score(df_daily)
                    if market_early_score > 15:
                        print(f"🌾 EMTIA Early Warning: {symbol} → +{market_early_score} puan")
                
                elif market == "CRYPTO":
                    market_early_score = crypto_early_score(df_daily)
                    if market_early_score > 15:
                        print(f"💰 CRYPTO Early Warning: {symbol} → +{market_early_score} puan")
                
                final_score += market_early_score
                
            except Exception as e:
                print(f"Market early warning hatası {market}: {e}")
            # <<< ------------------------------------------
            
            # Volume spike detection (v2)
            thresh = dynamic_threshold(market)
            volume_spike = volume_spike_detected(df)
            try:
                vol_spike_v2 = bool(refined_volume_spike(df, factor=2.0))
                vol_info = volume_spike_indicator(df)
            except:
                vol_spike_v2 = False
                vol_info = {"spike": False, "ratio": 0, "price_chg": 0}
            
        except ImportError as e:
            print(f"Warning system import error: {e}")
            thresh = STRONG_THRESHOLD
            volume_spike = False
            vol_spike_v2 = False
            vol_info = {"spike": False, "ratio": 0, "price_chg": 0}
        
        # Ensure score stays within reasonable bounds
        final_score = max(0, min(100, final_score))
        final_score = round(final_score, 1)
        
        # Dynamic threshold signal determination
        if thresh > final_score >= 50:
            signal = f"🟡 İZLEME - Potansiyel AL ({final_score:.0f}/{thresh})"
        elif final_score >= 80:
            signal = "🟢 AL_GÜÇLÜ"
        elif final_score >= thresh:
            signal = "🟢 AL"
        elif final_score >= 50:
            signal = "⚪ TUT"
        else:
            signal = "🔴 SAT"
            
        # Enhanced Volume spike indicators
        volume_msg = ""
        if vol_spike_v2:
            volume_msg += f" 🔊 Hacim Patlaması (x{vol_info['ratio']:.1f})"
        elif volume_spike:
            volume_msg += " 🔊 Hacim Patlaması"
            
        if volume_msg:
            signal += volume_msg

        return {
            "symbol": symbol,
            "price": round(price, 2),
            "score": final_score,
            "signal": signal,
            "time": datetime.now().strftime('%H:%M'),
            "sentiment_info": sentiment_info,
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
    """Sinyal satırını pazar bilgisi ve ULTRA tutma süresi ile formatla"""
    sentiment_info = s.get("sentiment_info", "")
    market = s.get("market", "")
    
    # Pazar emoji'leri ve isimleri
    market_info = {
        "BIST": {"emoji": "🇹🇷", "name": "BIST"},
        "NASDAQ": {"emoji": "🇺🇸", "name": "NASDAQ"}, 
        "CRYPTO": {"emoji": "💰", "name": "CRYPTO"},
        "EMTIA": {"emoji": "🌾", "name": "EMTIA"},
        "XETRA": {"emoji": "🇩🇪", "name": "XETRA"}
    }
    
    market_data = market_info.get(market, {"emoji": "📊", "name": "OTHER"})
    market_display = f"{market_data['emoji']} {market_data['name']}"
    
    base_line = f"{s['signal']} <b>{s['symbol']}</b> ({market_display}) | 💰 {s['price']} | 📈 {s['score']}/100{sentiment_info}"
    
    # ULTRA Tutma Süresi ekle ve Signal Tracker'a kaydet
    ultra_holding = "2-4 hafta 🔶 STANDART"
    if ULTRA_HOLDING_AVAILABLE and 'signal' in s:
        try:
            ultra_holding = calculate_ultra_holding_period(s['symbol'], s['signal'])
            base_line += f" | ⏰ {ultra_holding}"
        except Exception:
            base_line += " | ⏰ 2-4 hafta 🔶 STANDART"
    else:
        base_line += " | ⏰ 2-4 hafta 🔶 STANDART"
    
    # AL sinyalini signal tracker'a kaydet
    if REMINDER_ENABLED and SIGNAL_TRACKER and s.get('signal') == '🟢 AL':
        try:
            SIGNAL_TRACKER.add_signal(
                symbol=s['symbol'],
                signal_type='AL',
                score=s.get('score', 0),
                price=s.get('price', 0),
                holding_period=ultra_holding.replace('🔶 STANDART', '').replace('⚡ ULTRA', '').strip()
            )
        except Exception as e:
            print(f"⚠️ Signal tracker kaydı başarısız {s['symbol']}: {e}")
    
    return base_line + "\n"


def send_analysis_results(strong_signals: List[dict], market_summary: Dict[str, Dict[str, int]], total_symbols: int):
    """Analiz sonuçlarını Telegram'a gönder"""
    ts = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    # Add sentiment status to header
    sentiment_status = ""
    if SENTIMENT_ENABLED:
        sentiment_status = " 🧠 + Sentiment"
    
    if not strong_signals:
        message = (
            f"📊 <b>PlanB Full Market Analizi{sentiment_status}</b>\n"
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
        f"🚀 <b>PlanB ULTRA ANALİZ SONUÇLARI{sentiment_status}</b>\n"
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

    version_info = "🤖 <i>PlanB Ultra v2.1 - Full Market"
    if SENTIMENT_ENABLED:
        version_info += " + Enhanced Sentiment"
    version_info += " + Interactive Reminders"
    version_info += "</i>"
    message += f"\n{version_info}"
    
    # Ana mesajı gönder
    send_telegram_message(message)
    
    # Her güçlü AL sinyali için ayrı interaktif mesaj gönder
    for s in first_batch:
        if s.get("signal") in ["🟢 AL_GÜÇLÜ", "🟢 AL"]:
            holding_period = "2-4 hafta 🔶 STANDART"  # Default
            if ULTRA_HOLDING_AVAILABLE:
                try:
                    holding_period = calculate_ultra_holding_period(s['symbol'], s['signal'])
                except:
                    pass
            
            interactive_msg = (
                f"🎯 <b>Hatırlatma Sistemi</b>\n\n"
                f"📊 <b>{s['symbol']}</b> için AL sinyali verildi\n"
                f"💰 Fiyat: {s['price']}\n"
                f"📈 Puan: {s['score']}/100\n"
                f"⏰ Önerilen tutma: {holding_period}\n\n"
                f"💡 SAT zamanı gelince hatırlatmak ister misiniz?"
            )
            
            button = create_reminder_button(s['symbol'], s['price'], s['score'])
            send_telegram_message(interactive_msg, button)

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
    
    if SENTIMENT_ENABLED:
        print("🧠 Enhanced Sentiment Analysis: ENABLED")
    else:
        print("📈 Enhanced Sentiment Analysis: DISABLED (set SENTIMENT_ENABLED=true to enable)")

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
    
    if SENTIMENT_ENABLED:
        start_msg += "\n🧠 Enhanced Sentiment Analysis: ACTİVE"

    if send_telegram_message(start_msg):
        print("✅ Sistem başlatıldı, Telegram bildirimi gönderildi")
    else:
        print("❌ Telegram gönderimi yapılamadı (env değişkenlerini kontrol edin)")
    continuous_full_analysis()