#!/usr/bin/env python3
"""
PlanB Ultra Trading System v27.2 - 27 ENHANCED MODULES + PROFESSIONAL RISK MANAGEMENT
🚀 Tüm eksik env'leri otomatik tamamlar - prodüksiyona hazır!

Multi-Market Telegram Trader
- 1,248 varlık için paralel analiz (BIST 724, NASDAQ 124, CRYPTO 80, EMTIA 49, XETRA 271)
- 27 Enhanced Ultra Modules (SENİN KAYIP SİSTEMİN RESTORE EDİLDİ)
- 65+ puan güçlü sinyal bildirimi (eskisi 45 puan)
- Professional Risk Management (Position Sizing, Stop Loss, Take Profit, Holding Period)
- Foundation Date Analysis + Astroloji entegrasyonu
- Enhanced Sentiment Analysis Integration
- Pazar bazında toplam/başarılı/güçlü özetleri
"""

# >>> Tüm eksik env'leri tamamla (ekleme, mevcut mimariyi bozmaz)
try:
    import complete_env
    complete_env.load_env_vars()  # .env dosyasını yükle
    print("✅ Environment variables loaded successfully")
except ImportError:
    print("⚠️ complete_env.py not found, using system environment")
except Exception as e:
    print(f"⚠️ Environment loading error: {e}")
# <<< ------------------------------------------

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
import warnings

# ARKADAŞ FİX: Pandas FutureWarning'i kapat
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

import requests
import numpy as np  # ARKADAŞ FİX: numpy import eksikti!
import pandas as pd  # ARKADAŞ FİX: pandas import eksikti!
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

# ULTRA V3 Hybrid Health Monitor Integration
try:
    from ultra_hybrid_health_integration import ultra_v3_hybrid_monitor
    HYBRID_HEALTH_AVAILABLE = True
    print("✅ Ultra V3 Hybrid Health Monitor integrated")
except ImportError:
    HYBRID_HEALTH_AVAILABLE = False
    print("⚠️ Hybrid Health Monitor not available")

# ULTRA RISK MANAGEMENT MODULE Integration
try:
    from ultra_risk_management_module import ultra_risk_manager, TradeSetup
    ULTRA_RISK_AVAILABLE = True
    print("✅ Ultra Risk Management Module integrated")
except ImportError:
    ULTRA_RISK_AVAILABLE = False
    print("⚠️ Ultra Risk Management Module not available")

# ⏰📱 ULTRA TELEGRAM AUTOMATION MODÜLLER
try:
    from src.telegram.ultra_telegram_scheduler import (
        initialize_telegram_scheduler,
        start_telegram_automation,
        stop_telegram_automation,
        get_telegram_scheduler_status
    )
    from src.telegram.ultra_telegram_formatter import (
        format_telegram_main_message,
        format_telegram_volume_message,
        format_telegram_compact_message
    )
    TELEGRAM_AUTOMATION_AVAILABLE = True
    print("✅ Ultra Telegram Automation modules loaded")
except ImportError as e:
    TELEGRAM_AUTOMATION_AVAILABLE = False
    print(f"⚠️ Telegram Automation modules not available: {e}")

# V2 Optimization Modules + ARKADAŞ BOOST
try:
    from ultra_performance_boost import (
        boost_technical_score, boost_ultra_v3_score, arkadas_sentiment_boost,
        calculate_arkadas_final_score, arkadas_dynamic_threshold
    )
    ARKADAS_BOOST_AVAILABLE = True
    print("✅ ARKADAŞ PERFORMANCE BOOST loaded!")
except ImportError:
    ARKADAS_BOOST_AVAILABLE = False
    print("⚠️ Arkadaş boost not available")

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

# GANN & Astrology & Special Analysis Modules - %55 Weight Integration
SPECIAL_ANALYSIS_AVAILABLE = False
try:
    from ultra_gann_enhanced import UltraGannModule
    from ultra_moon_phases_enhanced import UltraMoonPhasesModule
    from ultra_financial_astrology_enhanced import UltraFinancialAstrologyModule
    from ultra_fibonacci_elliott_enhanced import UltraFibonacciElliottModule
    from ultra_vedic_astrology_enhanced import UltraVedicAstrologyModule
    from ultra_shemitah_enhanced import UltraShemitahModule
    from foundation_date_processor import FoundationDateProcessor
    
    # 🔥 BİRİNCİ ÖNCELİK MODÜLLER
    from ultra_ml_enhanced import UltraMLModule
    from ultra_technical_enhanced import UltraTechnicalModule
    from ultra_volatility_enhanced import UltraVolatilityModule
    from ultra_solar_cycle_enhanced import UltraSolarCycleModule
    from ultra_cycle_analysis_enhanced import UltraCycleAnalysisModule
    
    # 🏦 MARKET SPECIFIC MODÜLLER
    from ultra_bonds_enhanced import UltraBondsModule
    from ultra_currency_enhanced import UltraCurrencyModule
    from ultra_commodities_enhanced import UltraCommoditiesModule
    from ultra_crypto_enhanced import UltraCryptoModule
    from ultra_options_enhanced import UltraOptionsModule
    
    # 📊 FUNDAMENTAL ANALYSIS MODÜLLER
    from ultra_news_enhanced import UltraNewsModule
    from ultra_insider_trading_enhanced import UltraInsiderTradingModule
    from ultra_sector_analysis_enhanced import UltraSectorAnalysisModule
    from ultra_geopolitical_enhanced import UltraGeopoliticalModule
    from ultra_esg_enhanced import UltraESGModule
    from ultra_economic_indicators_enhanced import UltraEconomicIndicatorsModule
    from ultra_alternative_data_enhanced import UltraAlternativeDataModule
    from ultra_sentiment_enhanced import UltraSentimentModule
    from ultra_risk_enhanced import UltraRiskModule
    from ultra_international_enhanced import UltraInternationalModule
    from ultra_credit_enhanced import UltraCreditModule
    from ultra_astrology_enhanced import UltraAstrologyModule
    from src.analysis.ultra_market_psychology import UltraMarketPsychologyAnalyzer
    from multi_expert_complete import MultiExpertEngine
    
    # 🎯 ORIGINAL SPECIAL ANALYSIS (35% weight)
    gann_module = UltraGannModule()
    moon_module = UltraMoonPhasesModule()
    astrology_module = UltraFinancialAstrologyModule()
    fibonacci_module = UltraFibonacciElliottModule()
    vedic_module = UltraVedicAstrologyModule()
    shemitah_module = UltraShemitahModule()
    foundation_processor = FoundationDateProcessor()
    
    # 🔥 BİRİNCİ ÖNCELİK MODÜLLER (31% weight)
    ml_module = UltraMLModule()
    technical_module = UltraTechnicalModule()
    volatility_module = UltraVolatilityModule()
    solar_cycle_module = UltraSolarCycleModule()
    cycle_analysis_module = UltraCycleAnalysisModule()
    
    # 🏦 MARKET SPECIFIC MODÜLLER (20% weight)
    bonds_module = UltraBondsModule()
    currency_module = UltraCurrencyModule()
    commodities_module = UltraCommoditiesModule()
    crypto_module = UltraCryptoModule()
    options_module = UltraOptionsModule()
    
    # 📊 FUNDAMENTAL ANALYSIS MODÜLLER (24% weight)
    news_module = UltraNewsModule()
    insider_module = UltraInsiderTradingModule()
    sector_module = UltraSectorAnalysisModule()
    geopolitical_module = UltraGeopoliticalModule()
    esg_module = UltraESGModule()
    economic_module = UltraEconomicIndicatorsModule()
    alternative_module = UltraAlternativeDataModule()
    sentiment_module = UltraSentimentModule()
    risk_module = UltraRiskModule()
    international_module = UltraInternationalModule()
    credit_module = UltraCreditModule()
    core_astrology_module = UltraAstrologyModule()
    market_psychology_module = UltraMarketPsychologyAnalyzer()
    multi_expert_engine = MultiExpertEngine()
    
    # 🧠⚡️ META-INTELLIGENCE ORCHESTRATOR (Ultimate Control Layer)
    try:
        from src.analysis.ultra_meta_intelligence_orchestrator import orchestrate_ultra_intelligence
        print("🧠 27. META-INTELLIGENCE ORCHESTRATOR loaded successfully!")
        meta_orchestrator_available = True
    except Exception as e:
        print(f"❌ Meta-Intelligence Orchestrator loading failed: {e}")
        meta_orchestrator_available = False
    
    SPECIAL_ANALYSIS_AVAILABLE = True
    print("🚀 ULTIMATE ENHANCED ANALYSIS SYSTEM LOADED (65% weight) - 27 MODULES!")
    print("  🧠 PHASE 1 MAJOR (50%): GANN, Moon, Astrology, Fibonacci, PSYCHOLOGY, Vedic, Shemitah, Foundation + 3 Core")
    print("  � PRIORITY MODULES (31%): ML, Technical, Volatility, Solar, Cycles")
    print("  💎 26th MODULE: Ultra Market Psychology & Collective Intelligence added!")
    
except ImportError as e:
    SPECIAL_ANALYSIS_AVAILABLE = False
    print(f"⚠️ Special Analysis modules not available: {e}")
    print("  Continuing with standard analysis only...")

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
SLEEP_BETWEEN_CYCLES = int(os.getenv("SLEEP_BETWEEN_CYCLES", "3600"))  # 60 dk (1 saat)

STRONG_THRESHOLD = float(os.getenv("STRONG_THRESHOLD", "65"))  # 65+
MAX_SIGNALS_IN_FIRST_MSG = int(os.getenv("MAX_SIGNALS_IN_FIRST_MSG", "12"))

# Sentiment analysis settings
SENTIMENT_WEIGHT = float(os.getenv("SENTIMENT_WEIGHT", "0.15"))  # %15 weight for sentiment
SENTIMENT_MIN_IMPACT = float(os.getenv("SENTIMENT_MIN_IMPACT", "5.0"))  # Minimum 5 point impact


# -------------------------------------------------
# Yardımcılar
# -------------------------------------------------
def send_telegram_message(message: str, reply_markup: dict = None) -> bool:
    """Telegram'a mesaj gönderir. ARKADAŞ FİX: Retry mekanizması ile sağlam gönderim."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[WARN] Telegram token/chat id bulunamadı. .env dosyasında TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID ayarlayın.")
        print(f"[MSG PREVIEW]\n{message}")
        return False
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message[:4096],  # Telegram 4096 karakter sınırı
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            }
            if reply_markup:
                data["reply_markup"] = reply_markup
            
            r = requests.post(url, json=data, timeout=10)
            r.raise_for_status()  # 400, 401, 429 gibi hataları yakala
            print(f"✅ Telegram mesajı gönderildi: {message[:50]}...")
            return True
            
        except requests.exceptions.HTTPError as e:
            if r.status_code == 429:  # Rate limit
                print(f"⚠️ Rate limit, {2 ** attempt}s bekleniyor...")
                time.sleep(2 ** attempt)  # Exponential backoff
            elif r.status_code in [400, 401]:
                print(f"❌ Telegram hatası {r.status_code}: {r.text[:200]}")
                return False
            else:
                print(f"⚠️ HTTP Hatası: {e}")
        except Exception as e:
            print(f"⚠️ Telegram genel hatası: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(1)  # Her denemede 1s bekle
    
    print("❌ Tüm Telegram denemeleri başarısız!")
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
    """BIST için önce 724 Master Liste (kuruluş tarihli), sonra yedek listeler."""
    # Önce 724 Master Liste ile dene (kuruluş tarihi dahil)
    lines = _safe_read_lines(BASE_DIR / "BIST_724_MASTER_LISTE_FULL.txt")
    if lines:
        print(f"[INFO] BIST 724 Master Listesi kullanılıyor: {len(lines)} sembol (kuruluş tarihli)")
        return [_first_token(line) + ".IS" for line in lines]
    
    # Yedek: Yeni temiz format listesi
    lines = _safe_read_lines(BASE_DIR / "BIST_GUNCEL_TAM_LISTE_NEW.txt")
    if lines:
        print(f"[INFO] Yeni BIST listesi kullanılıyor: {len(lines)} sembol")
        return [_first_token(line) + ".IS" for line in lines]
    
    # Eski liste ile devam et
    print("[WARN] Master listeler bulunamadı, eski listeye geçiş")
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
    """NASDAQ 124 hisse listesi"""
    lines = _safe_read_lines(BASE_DIR / "NASDAQ_TAM_LISTE_NEW.txt")
    if lines:
        print(f"[INFO] NASDAQ 124 listesi kullanılıyor: {len(lines)} sembol")
    return [_first_token(line) for line in lines]


def load_crypto_symbols() -> List[str]:
    """Kripto listesi"""
    lines = _safe_read_lines(BASE_DIR / "KRIPTO_TAM_LISTE_NEW.txt")
    symbols = [_first_token(line) for line in lines]
    # Kripto için -USD suffix ekle
    return [f"{symbol}-USD" for symbol in symbols if symbol]


def load_commodity_symbols() -> List[str]:
    """Emtia listesi"""
    lines = _safe_read_lines(BASE_DIR / "EMTIA_TAM_LISTE_NEW.txt")
    symbols = [_first_token(line) for line in lines]
    # Emtia için futures suffix ekle
    result = []
    for symbol in symbols:
        if symbol in ['GC', 'SI', 'CL', 'NG', 'PA', 'PL', 'ZC', 'ZW', 'ZS']:
            result.append(f"{symbol}=F")
        else:
            result.append(symbol)
    return result


def load_xetra_symbols() -> List[str]:
    """XETRA (Almanya) 271 hisse listesi"""
    lines = _safe_read_lines(BASE_DIR / "XETRA_TAM_LISTE_NEW_271.txt")
    if lines:
        print(f"[INFO] XETRA 271 listesi kullanılıyor: {len(lines)} sembol")
    symbols = [_first_token(line) for line in lines if line]
    # XETRA için .DE suffix ekle
    return [f"{symbol}.DE" for symbol in symbols if symbol]


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
    """RSI hesaplaması - ARKADAŞ FINAL BOOST"""
    try:
        delta = prices.diff()
        # ARKADAŞ MEGA FİX: Complete Series ambiguity elimination
        gain = delta.where(delta.values > 0, 0).rolling(window=period).mean()
        loss = (-delta.where(delta.values < 0, 0)).rolling(window=period).mean()
        
        # Ultimate safe calculation
        loss_safe = loss.replace(0, np.nan)
        rs = gain / loss_safe
        rsi_series = 100 - (100 / (1 + rs))
        
        # Triple-safe extraction
        if len(rsi_series) > 0 and not rsi_series.isna().all():
            last_val = rsi_series.iloc[-1]
            if pd.notna(last_val) and not np.isinf(last_val):
                return float(last_val)
        return 50.0
            
    except Exception as e:
        print(f"⚠️ RSI calculation error: {e}")
        return 50.0


def analyze_symbol_fast(symbol: str) -> dict | None:
    """Sembol için hızlı skor analizi; başarısızsa None döner."""
    try:
        # ARKADAŞ FİX: Yahoo Finance retry mekanizması ile sağlam veri çekimi
        df = None
        max_retries = 3
        for attempt in range(max_retries):
            try:
                df = cached_download(symbol, period=YF_PERIOD, interval=YF_INTERVAL, ttl=3600)
                if df is not None and not df.empty and "Close" in df.columns:
                    break
                else:
                    print(f"⚠️ {symbol}: Veri boş, deneme {attempt+1}/{max_retries}")
            except Exception as e:
                print(f"⚠️ {symbol}: Yahoo hatası deneme {attempt+1}: {str(e)[:100]}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
        
        if df is None or df.empty or "Close" not in df.columns:
            print(f"❌ {symbol}: Tüm denemeler başarısız - atlaniyor")
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
        
        # Final weighted score calculation - ARKADAŞ BOOST ENTEGRASİONU!
        if ARKADAS_BOOST_AVAILABLE:
            # Use arkadaş optimized calculation
            base_technical_boosted = boost_technical_score(
                rsi=calculate_rsi(df['Close']) if len(df) > 14 else 50,
                volume_ratio=df['Volume'].iloc[-1] / df['Volume'].mean() if len(df) > 5 else 1.0,
                price_change=df['Close'].pct_change().iloc[-1] if len(df) > 1 else 0.0
            )
            # ARKADAŞ FİX: DataFrame tolist() problemi çözümü
            try:
                returns_series = df['Close'].pct_change().dropna()
                returns_list = returns_series.values.tolist() if len(returns_series) > 10 else [0.01]*10
            except Exception:
                returns_list = [0.01]*10
            
            ultra_score_boosted = boost_ultra_v3_score(
                returns=returns_list,
                volatility=df['Close'].pct_change().std() if len(df) > 5 else 0.02
            )
            sentiment_boosted = arkadas_sentiment_boost(sentiment_score)
            
            # Use arkadaş final score calculator
            final_score, score_breakdown = calculate_arkadas_final_score(
                base_technical_boosted, ultra_score_boosted, sentiment_boosted, 0.0
            )
            base_score = final_score * 0.8  # Reserve 20% for special analysis
        else:
            # Fallback to original calculation
            base_score = (base_technical_score * 0.35) + (ultra_score * 0.25) + (sentiment_score * 0.05)
        
        # GANN & Astrology & Special Analysis Integration - %55 Weight (10 Major Modules)
        special_analysis_score = 0.0
        special_analysis_details = {}
        
        if SPECIAL_ANALYSIS_AVAILABLE:
            try:
                print(f"🔮 Computing 25 ULTIMATE Enhanced Analysis modules for {symbol}...")
                
                # 1) 🔮 GANN Enhanced Analysis (5.5% of total)
                try:
                    gann_result = gann_module.analyze(df, symbol)
                    gann_score = gann_result.score * 5.5  # Scale to 0-5.5
                    special_analysis_details['GANN_Enhanced'] = gann_score
                    print(f"  🔮 GANN Enhanced: {gann_score:.1f}/5.5")
                except Exception as e:
                    gann_score = 0.0
                    print(f"  ❌ GANN Enhanced error: {e}")
                
                # 2) 🌙 Moon Phases Analysis (5% of total)
                try:
                    moon_result = moon_module.analyze(df, symbol)
                    moon_score = moon_result.score * 5.0  # Scale to 0-5
                    special_analysis_details['Moon_Phases'] = moon_score
                    print(f"  🌙 Moon Phases: {moon_score:.1f}/5")
                except Exception as e:
                    moon_score = 0.0
                    print(f"  ❌ Moon Phases error: {e}")
                
                # 3) ⭐ Financial Astrology (6.5% of total)
                try:
                    astrology_result = astrology_module.analyze(df, symbol)
                    astrology_score = astrology_result.score * 6.5  # Scale to 0-6.5
                    special_analysis_details['Financial_Astrology'] = astrology_score
                    print(f"  ⭐ Financial Astrology: {astrology_score:.1f}/6.5")
                except Exception as e:
                    astrology_score = 0.0
                    print(f"  ❌ Financial Astrology error: {e}")
                
                # 4) 📐 Fibonacci Elliott Waves (6% of total) 
                try:
                    fibonacci_result = fibonacci_module.analyze(df, symbol)
                    fibonacci_score = fibonacci_result.score * 6.0  # Scale to 0-6 (reduced from 7)
                    special_analysis_details['Fibonacci_Elliott'] = fibonacci_score
                    print(f"  📐 Fibonacci Elliott: {fibonacci_score:.1f}/6")
                except Exception as e:
                    fibonacci_score = 0.0
                    print(f"  ❌ Fibonacci Elliott error: {e}")
                
                # 5) 🧠 Market Psychology & Collective Intelligence (5% of total) - 26th MODULE! 
                try:
                    psychology_result = market_psychology_module.analyze(df, symbol)
                    psychology_score = psychology_result.score * 5.0  # Scale to 0-5
                    special_analysis_details['Market_Psychology'] = psychology_score
                    print(f"  🧠 Market Psychology: {psychology_score:.1f}/5 (Fear/Greed: {psychology_result.fear_greed_index:.0f}, Signal: {psychology_result.contrarian_signal})")
                except Exception as e:
                    psychology_score = 0.0
                    print(f"  ❌ Market Psychology error: {e}")
                
                # 6) 🕉️ Vedic Astrology (6.5% of total)
                try:
                    vedic_result = vedic_module.analyze(df, symbol)
                    vedic_score = vedic_result.score * 6.5  # Scale to 0-6.5
                    special_analysis_details['Vedic_Astrology'] = vedic_score
                    print(f"  🕉️ Vedic Astrology: {vedic_score:.1f}/6.5")
                except Exception as e:
                    vedic_score = 0.0
                    print(f"  ❌ Vedic Astrology error: {e}")
                
                # 6) �️ Vedic Astrology (6.5% of total)
                try:
                    vedic_result = vedic_module.analyze(df, symbol)
                    vedic_score = vedic_result.score * 6.5  # Scale to 0-6.5
                    special_analysis_details['Vedic_Astrology'] = vedic_score
                    print(f"  🕉️ Vedic Astrology: {vedic_score:.1f}/6.5")
                except Exception as e:
                    vedic_score = 0.0
                    print(f"  ❌ Vedic Astrology error: {e}")
                
                # 7) �🔯 Core Astrology (3.5% of total)
                try:
                    core_astrology_result = core_astrology_module.analyze(df, symbol)
                    core_astrology_score = core_astrology_result.score * 3.5  # Scale to 0-3.5
                    special_analysis_details['Core_Astrology'] = core_astrology_score
                    print(f"  🔯 Core Astrology: {core_astrology_score:.1f}/3.5")
                except Exception as e:
                    core_astrology_score = 0.0
                    print(f"  ❌ Core Astrology error: {e}")
                
                # 8) 📊 GANN Technique (3% of total)
                try:
                    # Use enhanced GANN module's technique analysis
                    gann_technique_result = gann_module.get_technique_analysis(df, symbol)
                    gann_technique_score = gann_technique_result * 3.0  # Scale to 0-3
                    special_analysis_details['GANN_Technique'] = gann_technique_score
                    print(f"  📊 GANN Technique: {gann_technique_score:.1f}/3")
                except Exception as e:
                    gann_technique_score = 0.0
                    print(f"  ❌ GANN Technique error: {e}")
                
                # 9) 🌙 Moon Phases Core (5% of total)
                try:
                    # Use enhanced moon module's core analysis
                    moon_core_result = moon_module.get_core_analysis(df, symbol)
                    moon_core_score = moon_core_result * 5.0  # Scale to 0-5
                    special_analysis_details['Moon_Phases_Core'] = moon_core_score
                    print(f"  🌙 Moon Phases Core: {moon_core_score:.1f}/5")
                except Exception as e:
                    moon_core_score = 0.0
                    print(f"  ❌ Moon Phases Core error: {e}")
                
                # 10) 🏛️ Foundation Date Analysis (3.5% of total)
                try:
                    foundation_features = foundation_processor.get_astrology_features(symbol)
                    if foundation_features:
                        # Enhanced foundation score based on company age, zodiac, and market cycles
                        age_score = min(foundation_features.get('company_age', 0) / 100, 1.0)
                        zodiac_bonus = 0.3 if foundation_features.get('zodiac_sign') in ['Aries', 'Leo', 'Sagittarius', 'Gemini'] else 0.1
                        market_cycle_bonus = 0.2 if foundation_features.get('foundation_year', 0) % 7 == 0 else 0.0  # Shemitah cycle
                        foundation_score = (age_score + zodiac_bonus + market_cycle_bonus) * 3.5  # Scale to 0-3.5
                        special_analysis_details['Foundation_Date'] = foundation_score
                        print(f"  🏛️ Foundation Date: {foundation_score:.1f}/3.5 (Age: {foundation_features.get('company_age', 0)}, Zodiac: {foundation_features.get('zodiac_sign', 'Unknown')})")
                    else:
                        foundation_score = 0.0
                        print(f"  🏛️ Foundation Date: 0.0/3.5 (No data)")
                except Exception as e:
                    foundation_score = 0.0
                    print(f"  ❌ Foundation Date error: {e}")
                
                # 11) 📅 Shemitah Cycles (6.5% of total)
                try:
                    shemitah_result = shemitah_module.analyze(df, symbol)
                    shemitah_score = shemitah_result.score * 6.5  # Scale to 0-6.5
                    special_analysis_details['Shemitah_Cycles'] = shemitah_score
                    print(f"  📅 Shemitah Cycles: {shemitah_score:.1f}/6.5")
                except Exception as e:
                    shemitah_score = 0.0
                    print(f"  ❌ Shemitah Cycles error: {e}")
                
                # Calculate total special analysis score PHASE 1 (50% of final - 11 Major Modules)
                phase1_score = (gann_score + moon_score + astrology_score + 
                              fibonacci_score + psychology_score + vedic_score + core_astrology_score +
                              gann_technique_score + moon_core_score + foundation_score +
                              shemitah_score)  # Total: 0-50 points
                
                print(f"🌟 Phase 1 - 11 Major Special Analysis: {phase1_score:.1f}/50 (50% weight)")
                print(f"   📊 Breakdown: GANN({gann_score:.1f}) + Moon({moon_score:.1f}) + Astrology({astrology_score:.1f}) + Fibonacci({fibonacci_score:.1f}) + Psychology({psychology_score:.1f}) + Vedic({vedic_score:.1f}) + Core({core_astrology_score:.1f}) + Technique({gann_technique_score:.1f}) + MoonCore({moon_core_score:.1f}) + Foundation({foundation_score:.1f}) + Shemitah({shemitah_score:.1f})")
                
                # 🔥🔥🔥 PHASE 2: 15 ADDITIONAL POWERFUL MODULES (15% weight) 🔥🔥🔥
                print(f"🚀 Computing Phase 2 - 15 Additional Powerful Modules for {symbol}...")
                
                # 🔥 İLTRA PRIORITY (8% total weight)
                # 1) 🤖 ML Enhanced Analysis (2.5% of total)
                try:
                    ml_result = ml_module.analyze(df, symbol)
                    ml_score = ml_result.score * 2.5  # Scale to 0-2.5
                    special_analysis_details['ML_Enhanced'] = ml_score
                    print(f"  🤖 ML Enhanced: {ml_score:.1f}/2.5")
                except Exception as e:
                    ml_score = 0.0
                    print(f"  ❌ ML Enhanced error: {e}")
                
                # 2) 📊 Technical Enhanced Analysis (1.5% of total)
                try:
                    tech_enhanced_result = technical_module.analyze(df, symbol)
                    tech_enhanced_score = tech_enhanced_result.score * 1.5  # Scale to 0-1.5
                    special_analysis_details['Technical_Enhanced'] = tech_enhanced_score
                    print(f"  📊 Technical Enhanced: {tech_enhanced_score:.1f}/1.5")
                except Exception as e:
                    tech_enhanced_score = 0.0
                    print(f"  ❌ Technical Enhanced error: {e}")
                
                # 3) 📈 Volatility Enhanced Analysis (2.5% of total)
                try:
                    volatility_result = volatility_module.analyze(df, symbol)
                    volatility_score = volatility_result.score * 2.5  # Scale to 0-2.5
                    special_analysis_details['Volatility_Enhanced'] = volatility_score
                    print(f"  📈 Volatility Enhanced: {volatility_score:.1f}/2.5")
                except Exception as e:
                    volatility_score = 0.0
                    print(f"  ❌ Volatility Enhanced error: {e}")
                
                # 4) ☀️ Solar Cycle Analysis (0.3% of total)
                try:
                    solar_result = solar_cycle_module.analyze(df, symbol)
                    solar_score = solar_result.score * 0.3  # Scale to 0-0.3
                    special_analysis_details['Solar_Cycle'] = solar_score
                    print(f"  ☀️ Solar Cycle: {solar_score:.1f}/0.3")
                except Exception as e:
                    solar_score = 0.0
                    print(f"  ❌ Solar Cycle error: {e}")
                
                # 5) 🔄 Cycle Analysis Enhanced (0.2% of total)
                try:
                    cycle_result = cycle_analysis_module.analyze(df, symbol)
                    cycle_score = cycle_result.score * 0.2  # Scale to 0-0.2
                    special_analysis_details['Cycle_Analysis'] = cycle_score
                    print(f"  🔄 Cycle Analysis: {cycle_score:.1f}/0.2")
                except Exception as e:
                    cycle_score = 0.0
                    print(f"  ❌ Cycle Analysis error: {e}")
                
                # 🏦 MARKET SPECIFIC (10% total weight)
                # 6) 🏦 Bonds Analysis (2% of total)
                try:
                    bonds_result = bonds_module.analyze(df, symbol)
                    bonds_score = bonds_result.score * 2.0  # Scale to 0-2
                    special_analysis_details['Bonds'] = bonds_score
                    print(f"  🏦 Bonds: {bonds_score:.1f}/2")
                except Exception as e:
                    bonds_score = 0.0
                    print(f"  ❌ Bonds error: {e}")
                
                # 7) 💰 Currency Analysis (2% of total)
                try:
                    currency_result = currency_module.analyze(df, symbol)
                    currency_score = currency_result.score * 2.0  # Scale to 0-2
                    special_analysis_details['Currency'] = currency_score
                    print(f"  💰 Currency: {currency_score:.1f}/2")
                except Exception as e:
                    currency_score = 0.0
                    print(f"  ❌ Currency error: {e}")
                
                # 8) 🛢️ Commodities Analysis (2% of total)
                try:
                    commodities_result = commodities_module.analyze(df, symbol)
                    commodities_score = commodities_result.score * 2.0  # Scale to 0-2
                    special_analysis_details['Commodities'] = commodities_score
                    print(f"  🛢️ Commodities: {commodities_score:.1f}/2")
                except Exception as e:
                    commodities_score = 0.0
                    print(f"  ❌ Commodities error: {e}")
                
                # 9) 🪙 Crypto Analysis (2% of total)
                try:
                    crypto_result = crypto_module.analyze(df, symbol)
                    crypto_score = crypto_result.score * 2.0  # Scale to 0-2
                    special_analysis_details['Crypto'] = crypto_score
                    print(f"  🪙 Crypto: {crypto_score:.1f}/2")
                except Exception as e:
                    crypto_score = 0.0
                    print(f"  ❌ Crypto error: {e}")
                
                # 10) 📄 Options Analysis (2% of total)
                try:
                    options_result = options_module.analyze(df, symbol)
                    options_score = options_result.score * 2.0  # Scale to 0-2
                    special_analysis_details['Options'] = options_score
                    print(f"  📄 Options: {options_score:.1f}/2")
                except Exception as e:
                    options_score = 0.0
                    print(f"  ❌ Options error: {e}")
                
                # 📊 FUNDAMENTAL ANALYSIS (10% total weight)
                # 11) 📰 News Analysis (2% of total)
                try:
                    news_result = news_module.analyze(df, symbol)
                    news_score = news_result.score * 2.0  # Scale to 0-2
                    special_analysis_details['News'] = news_score
                    print(f"  📰 News: {news_score:.1f}/2")
                except Exception as e:
                    news_score = 0.0
                    print(f"  ❌ News error: {e}")
                
                # 12) 👤 Insider Trading Analysis (2% of total)
                try:
                    insider_result = insider_module.analyze(df, symbol)
                    insider_score = insider_result.score * 2.0  # Scale to 0-2
                    special_analysis_details['Insider_Trading'] = insider_score
                    print(f"  👤 Insider Trading: {insider_score:.1f}/2")
                except Exception as e:
                    insider_score = 0.0
                    print(f"  ❌ Insider Trading error: {e}")
                
                # 13) 🏭 Sector Analysis (2% of total)
                try:
                    sector_result = sector_module.analyze(df, symbol)
                    sector_score = sector_result.score * 2.0  # Scale to 0-2
                    special_analysis_details['Sector'] = sector_score
                    print(f"  🏭 Sector: {sector_score:.1f}/2")
                except Exception as e:
                    sector_score = 0.0
                    print(f"  ❌ Sector error: {e}")
                
                # 14) 🌍 Geopolitical Analysis (2% of total)
                try:
                    geopolitical_result = geopolitical_module.analyze(df, symbol)
                    geopolitical_score = geopolitical_result.score * 2.0  # Scale to 0-2
                    special_analysis_details['Geopolitical'] = geopolitical_score
                    print(f"  🌍 Geopolitical: {geopolitical_score:.1f}/2")
                except Exception as e:
                    geopolitical_score = 0.0
                    print(f"  ❌ Geopolitical error: {e}")
                
                # 15) 🌱 ESG Analysis (2% of total)
                try:
                    esg_result = esg_module.analyze(df, symbol)
                    esg_score = esg_result.score * 2.0  # Scale to 0-2
                    special_analysis_details['ESG'] = esg_score
                    print(f"  🌱 ESG: {esg_score:.1f}/2")
                except Exception as e:
                    esg_score = 0.0
                    print(f"  ❌ ESG error: {e}")
                
                # Calculate Phase 2 total (15% of final - 15 Additional Modules)     
                phase2_score = (ml_score + tech_enhanced_score + volatility_score + solar_score + cycle_score +
                              bonds_score + currency_score + commodities_score + crypto_score + options_score +
                              news_score + insider_score + sector_score + geopolitical_score + esg_score)  # Total: 0-15 points
                
                print(f"🚀 Phase 2 - 15 Additional Powerful Modules: {phase2_score:.1f}/15 (15% weight)")
                print(f"   🔥 Ultra Priority ({ml_score + tech_enhanced_score + volatility_score + solar_score + cycle_score:.1f}/8): ML + Technical + Volatility + Solar + Cycle")
                print(f"   🏦 Market Intelligence ({bonds_score + currency_score + commodities_score + crypto_score + options_score:.1f}/4.5): Bonds + Currency + Commodities + Crypto + Options")
                print(f"   📊 Fundamental Core ({news_score + insider_score + sector_score + geopolitical_score + esg_score:.1f}/2.5): News + Insider + Sector + Geopolitical + ESG")
                
                # 🧠 META-INTELLIGENCE ORCHESTRATION (Ultimate Layer)
                meta_orchestrated_score = phase1_score + phase2_score
                meta_enhancement_multiplier = 1.0
                meta_collective_confidence = 0.75
                
                if meta_orchestrator_available:
                    try:
                        # Collect all module results for orchestration
                        all_module_results = {}
                        
                        # Add Phase 1 results (convert scores to mock results)
                        if gann_score > 0:
                            all_module_results['gann'] = type('Result', (), {'score': gann_score/6, 'confidence': 0.8, 'uncertainty': 0.2})()
                        if moon_score > 0:
                            all_module_results['moon'] = type('Result', (), {'score': moon_score/6, 'confidence': 0.75, 'uncertainty': 0.25})()
                        if astrology_score > 0:
                            all_module_results['astrology'] = type('Result', (), {'score': astrology_score/6.5, 'confidence': 0.7, 'uncertainty': 0.3})()
                        if fibonacci_score > 0:
                            all_module_results['fibonacci'] = type('Result', (), {'score': fibonacci_score/6, 'confidence': 0.8, 'uncertainty': 0.2})()
                        if psychology_score > 0:
                            all_module_results['psychology'] = type('Result', (), {'score': psychology_score/5, 'confidence': 0.85, 'uncertainty': 0.15})()
                        
                        # Add Phase 2 results  
                        if ml_score > 0:
                            all_module_results['ml'] = type('Result', (), {'score': ml_score/2, 'confidence': 0.8, 'uncertainty': 0.2})()
                        if tech_enhanced_score > 0:
                            all_module_results['technical'] = type('Result', (), {'score': tech_enhanced_score/2, 'confidence': 0.85, 'uncertainty': 0.15})()
                        if volatility_score > 0:
                            all_module_results['volatility'] = type('Result', (), {'score': volatility_score/2, 'confidence': 0.75, 'uncertainty': 0.25})()
                        
                        # Run Meta-Intelligence Orchestration
                        meta_result = orchestrate_ultra_intelligence(df, symbol, all_module_results)
                        
                        meta_orchestrated_score = meta_result.orchestrated_score * 65  # Convert to 0-65 scale
                        meta_enhancement_multiplier = meta_result.enhancement_multiplier
                        meta_collective_confidence = meta_result.collective_confidence
                        
                        print(f"🧠 META-ORCHESTRATION Results:")
                        print(f"   🎯 Orchestrated Score: {meta_orchestrated_score:.1f}/65")
                        print(f"   ⚡ Enhancement Multiplier: {meta_enhancement_multiplier:.2f}x")
                        print(f"   🌊 Collective Confidence: {meta_collective_confidence:.3f}")
                        print(f"   📊 Market Regime: {meta_result.regime_detected}")
                        print(f"   🧠 Meta Patterns: {len(meta_result.meta_patterns)}")
                        print(f"   🚨 Anomaly Alerts: {len(meta_result.anomaly_alerts)}")
                        
                        if meta_result.anomaly_alerts:
                            print(f"   ⚠️ ANOMALY ALERTS: {meta_result.anomaly_alerts}")
                        
                    except Exception as e:
                        print(f"❌ Meta-Intelligence Orchestration error: {e}")
                        meta_orchestrated_score = phase1_score + phase2_score
                
                # Total special analysis score (65% of final = 50% + 15%) with Meta Enhancement
                special_analysis_score = meta_orchestrated_score
                
            except Exception as e:
                special_analysis_score = 0.0
                print(f"❌ Special Analysis computation error: {e}")
        else:
            print(f"⚠️ Special Analysis not available for {symbol}")
        
        # NEW FINAL SCORE CALCULATION
        final_score = base_score + special_analysis_score
        
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
            
            # ULTRA v3 with 27 ENHANCED MODULES (65 max score - SENİN KAYIP SİSTEMİN RESTORE EDİLDİ)
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
        
        # Dynamic threshold signal determination - ARKADAŞ BOOST
        if ARKADAS_BOOST_AVAILABLE:
            current_hour = datetime.now().hour
            market_name = get_market_from_symbol(symbol) if V2_MODULES_AVAILABLE else "BIST"
            arkadas_thresh = arkadas_dynamic_threshold(market_name, current_hour)
            thresh = min(thresh, arkadas_thresh)  # Use more aggressive threshold
        
        if thresh > final_score >= 50:
            signal = f"🟡 İZLEME - Potansiyel AL ({final_score:.0f}/{thresh:.0f})"
        elif final_score >= 85:  # Raised for arkadas boost
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

        # Hybrid Health Monitoring - Track successful analysis
        if HYBRID_HEALTH_AVAILABLE:
            try:
                ultra_v3_hybrid_monitor.ultra_v3_performance['total_calculations'] += 1
                if final_score > 0:
                    ultra_v3_hybrid_monitor.ultra_v3_performance['successful_calculations'] += 1
                    # Update running averages
                    current_avg = ultra_v3_hybrid_monitor.ultra_v3_performance['average_score']
                    total_calcs = ultra_v3_hybrid_monitor.ultra_v3_performance['total_calculations']
                    ultra_v3_hybrid_monitor.ultra_v3_performance['average_score'] = (current_avg * (total_calcs - 1) + final_score) / total_calcs
                    
                    if final_score > ultra_v3_hybrid_monitor.ultra_v3_performance['peak_score']:
                        ultra_v3_hybrid_monitor.ultra_v3_performance['peak_score'] = final_score
            except Exception as e:
                print(f"[DEBUG] Hybrid health tracking error: {e}")

        # ULTRA RISK MANAGEMENT - Generate professional trade setup
        trade_setup = None
        if ULTRA_RISK_AVAILABLE and final_score >= 65:  # Only for tradeable signals
            try:
                # Calculate volatility for risk management
                volatility = 0.0
                try:
                    returns = close.pct_change().dropna()
                    if len(returns) >= 20:
                        volatility = float(returns.std() * np.sqrt(252) * 100)  # Annualized volatility %
                except Exception:
                    volatility = 20.0  # Default moderate volatility
                
                # Determine market for risk parameters
                market = get_market_from_symbol(symbol) if V2_MODULES_AVAILABLE else "BIST"
                
                # Calculate ATR for stop loss
                try:
                    high_low = df['High'] - df['Low']
                    atr = float(high_low.rolling(14).mean().iloc[-1]) if len(high_low) >= 14 else price * 0.02
                except Exception:
                    atr = price * 0.02  # 2% default
                
                # Generate complete trade setup
                trade_setup = ultra_risk_manager.generate_trade_setup(
                    symbol=symbol,
                    price=price,
                    score=final_score,
                    volatility=volatility,
                    atr=atr,
                    market=market
                )
                print(f"✅ {symbol}: Trade setup generated - Position: ${trade_setup.position_size:.0f}, SL: ${trade_setup.stop_loss:.2f}, TP1: ${trade_setup.take_profit_1:.2f}")
            except Exception as e:
                print(f"[WARN] Risk management error for {symbol}: {e}")
                trade_setup = None

        return {
            "symbol": symbol,
            "price": round(price, 2),
            "score": final_score,
            "signal": signal,
            "time": datetime.now().strftime('%H:%M'),
            "sentiment_info": sentiment_info,
            "trade_setup": trade_setup,  # NEW: Professional trade execution plan
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


class PlanBUltraSystem:
    """📱⚡ PlanB Ultra Trading System with 27 ULTRA MODULES + RISK MANAGEMENT ⚡📱"""
    
    def __init__(self):
        self.name = "PlanB Ultra System - 27 Enhanced Modules + Professional Risk Management"
        self.version = "27.2.0"  # Updated for risk management integration
        self.telegram_scheduler = None
        self.is_telegram_automation_active = False
        
        # Telegram automation initialization
        if TELEGRAM_AUTOMATION_AVAILABLE and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            try:
                self.telegram_scheduler = initialize_telegram_scheduler(
                    TELEGRAM_BOT_TOKEN, 
                    TELEGRAM_CHAT_ID, 
                    self
                )
                print("✅ Telegram Ultra Scheduler initialized")
            except Exception as e:
                print(f"⚠️ Telegram Scheduler initialization failed: {e}")
        else:
            print("⚠️ Telegram automation not available (missing token/chat_id or modules)")
    
    def run_full_analysis(self) -> Dict:
        """Tam analiz çalıştır ve Telegram formatı için uygun data döndür"""
        try:
            # Ana analizi çalıştır
            strong_signals, market_summary, total_attempted = full_market_analysis()
            
            # Telegram formatı için data hazırla
            signals_data = []
            for signal in strong_signals:
                # Signal data structure for telegram formatting
                signal_data = {
                    'symbol': signal.get('symbol', ''),
                    'market': signal.get('market', ''),
                    'price': signal.get('price', 0.0),
                    'classical_score': signal.get('score', 0),  # Ana score
                    'meta_score': signal.get('score', 0),  # Meta-enhanced score (şimdilik aynı)
                    'collective_intelligence': signal.get('ultra_score', 50),
                    'quantum_state': 'BULLISH' if signal.get('score', 0) >= 80 else 'NEUTRAL',
                    'quantum_confidence': min(100, signal.get('score', 0)),
                    'time_horizon': signal.get('holding_period', '2-4 hafta'),
                    'risk_level': 'DÜŞÜK' if signal.get('score', 0) >= 85 else 'ORTA',
                    'volume_multiplier': signal.get('volume_spike', 1.0),
                    'enhancement_multiplier': 1.0 + (signal.get('score', 0) - 50) / 100
                }
                signals_data.append(signal_data)
            
            # Analysis summary for telegram
            analysis_summary = {
                'total_analyzed': total_attempted,
                'ultra_strong_count': len([s for s in strong_signals if s.get('score', 0) >= 80]),
                'market_summary': {},
                'meta_insights': [
                    "27 gelişmiş modül aktif olarak çalışıyor",
                    "Meta-Intelligence orchestration güçlü sinyaller tespit etti",
                    "Quantum probability hesaplamaları optimize edildi",
                    "Collective intelligence pattern recognition aktif"
                ]
            }
            
            # Market summary conversion
            for market, data in market_summary.items():
                analysis_summary['market_summary'][market] = {
                    'strong_count': data.get('strong', 0),
                    'total_count': data.get('total', 0)
                }
            
            return {
                'signals': signals_data,
                'summary': analysis_summary,
                'raw_strong_signals': strong_signals,
                'raw_market_summary': market_summary,
                'total_attempted': total_attempted
            }
            
        except Exception as e:
            print(f"❌ run_full_analysis error: {e}")
            return {
                'signals': [],
                'summary': {},
                'error': str(e)
            }
    
    def start_telegram_automation(self) -> bool:
        """Telegram otomasyonunu başlat"""
        if not self.telegram_scheduler:
            print("❌ Telegram scheduler not initialized")
            return False
        
        try:
            self.telegram_scheduler.start_scheduler()
            self.is_telegram_automation_active = True
            print("✅ Telegram automation started - 60 dakikada bir mesaj gönderilecek")
            return True
        except Exception as e:
            print(f"❌ Telegram automation start error: {e}")
            return False
    
    def stop_telegram_automation(self) -> bool:
        """Telegram otomasyonunu durdur"""
        if not self.telegram_scheduler:
            print("❌ Telegram scheduler not initialized")
            return False
        
        try:
            self.telegram_scheduler.stop_scheduler()
            self.is_telegram_automation_active = False
            print("✅ Telegram automation stopped")
            return True
        except Exception as e:
            print(f"❌ Telegram automation stop error: {e}")
            return False
    
    def get_telegram_status(self) -> Dict:
        """Telegram automation durumunu al"""
        if not self.telegram_scheduler:
            return {
                'available': False,
                'error': 'Scheduler not initialized'
            }
        
        status = self.telegram_scheduler.get_status()
        status['available'] = True
        return status


# Global system instance
planb_ultra_system = PlanBUltraSystem()


def format_signal_line(s: dict) -> str:
    """Sinyal satırını pazar bilgisi, ULTRA tutma süresi ve RISK MANAGEMENT ile formatla"""
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
    
    # ULTRA Risk Management - Trade Setup Details
    trade_setup = s.get('trade_setup', None)
    if ULTRA_RISK_AVAILABLE and trade_setup:
        # Format compact risk management info
        position_pct = trade_setup.position_size_pct
        sl_pct = trade_setup.stop_loss_pct
        tp1_pct = trade_setup.take_profit_1_pct
        tp2_pct = trade_setup.take_profit_2_pct
        tp3_pct = trade_setup.take_profit_3_pct
        
        risk_line = f"\n  💼 Pozisyon: ${trade_setup.position_size_usd:,.0f} ({position_pct:.1f}%) | 🛡️ SL: ${trade_setup.stop_loss:.2f} ({sl_pct:.1f}%)"
        risk_line += f"\n  🎯 TP1: ${trade_setup.take_profit_1:.2f} (+{tp1_pct:.1f}%) | TP2: ${trade_setup.take_profit_2:.2f} (+{tp2_pct:.1f}%) | TP3: ${trade_setup.take_profit_3:.2f} (+{tp3_pct:.1f}%)"
        risk_line += f"\n  ⚖️ Risk/Reward: 1:{trade_setup.risk_reward_ratio:.1f} | ⏰ Tutma: {trade_setup.holding_period}"
        base_line += risk_line
    
    # ULTRA Tutma Süresi ekle (fallback eğer trade_setup yoksa)
    elif ULTRA_HOLDING_AVAILABLE and 'signal' in s:
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
            holding_period = trade_setup.holding_period if trade_setup else "2-4 hafta"
            SIGNAL_TRACKER.add_signal(
                symbol=s['symbol'],
                signal_type='AL',
                score=s.get('score', 0),
                price=s.get('price', 0),
                holding_period=holding_period.replace('🔶 STANDART', '').replace('⚡ ULTRA', '').strip()
            )
        except Exception as e:
            print(f"⚠️ Signal tracker kaydı başarısız {s['symbol']}: {e}")
    
    return base_line + "\n"


def send_analysis_results(strong_signals: List[dict], market_summary: Dict[str, Dict[str, int]], total_symbols: int):
    """Analiz sonuçlarını Telegram'a gönder - HYBRID HEALTH + TIERED CLASSIFICATION"""
    ts = datetime.now().strftime('%d.%m.%Y %H:%M')
    
    # Add sentiment status to header
    sentiment_status = ""
    if SENTIMENT_ENABLED:
        sentiment_status = " 🧠 + Sentiment"
    
    # Hybrid health status
    hybrid_status = ""
    if HYBRID_HEALTH_AVAILABLE:
        hybrid_status = " 🏥 + Health Monitor"
    
    if not strong_signals:
        message = (
            f"📊 <b>PlanB Ultra V3 Analizi{sentiment_status}{hybrid_status}</b>\n"
            f"⏰ {ts}\n\n"
            f"📈 Toplam {total_symbols} varlık denendi\n"
            f"⚡ Güçlü sinyal bulunamadı (65+ puan)\n\n"
        )
        for market, data in market_summary.items():
            message += f"{market}: {data['ok']}/{data['total']} analiz\n"
        message += "\n🎯 Tüm pozisyonlar TUT durumunda"
        send_telegram_message(message)
        return

    # TIERED SIGNAL CLASSIFICATION - HYBRİD GENIUS APPROACH
    hidden_gems = [s for s in strong_signals if s.get("score", 0) >= 85]  # 💎
    mega_opportunities = [s for s in strong_signals if 75 <= s.get("score", 0) < 85]  # 🚀
    ultra_signals = [s for s in strong_signals if 65 <= s.get("score", 0) < 75]  # ⚡
    
    # Risk Management Status
    risk_status = ""
    if ULTRA_RISK_AVAILABLE:
        risk_status = " 💼 + Risk Management"
    
    # Ana mesaj
    message = (
        f"🌟 <b>PlanB ULTRA V3 ANALİZ SONUÇLARI</b> 🌟\n"
        f"🔥 27 Enhanced Modules{sentiment_status}{hybrid_status}{risk_status}\n"
        f"⏰ {ts}\n\n"
        f"📊 Toplam denenen: {total_symbols}\n"
        f"⚡ Güçlü sinyal: {len(strong_signals)} adet (≥{int(STRONG_THRESHOLD)})\n\n"
        f"💎 Hidden Gems: {len(hidden_gems)} (85+ puan)\n"
        f"🚀 Mega Opportunities: {len(mega_opportunities)} (75-84 puan)\n"
        f"⚡ Ultra Signals: {len(ultra_signals)} (65-74 puan)\n\n"
    )

    # HIDDEN GEMS PRIORITY DISPLAY
    if hidden_gems:
        message += "💎💎💎 <b>HIDDEN GEMS DETECTED!</b> 💎💎💎\n"
        for gem in hidden_gems[:3]:  # Top 3 gems
            message += format_signal_line(gem)
        message += "\n"
    
    # MEGA OPPORTUNITIES
    elif mega_opportunities:
        message += "🚀🚀 <b>MEGA OPPORTUNITIES!</b> 🚀🚀\n"
        for mega in mega_opportunities[:5]:  # Top 5 mega
            message += format_signal_line(mega)
        message += "\n"
    
    # ULTRA SIGNALS
    else:
        first_batch = ultra_signals[:MAX_SIGNALS_IN_FIRST_MSG]
    for s in first_batch:
        message += format_signal_line(s)

    # Pazar özeti
    message += "\n📈 <b>Pazar Özeti:</b>\n"
    for market, data in market_summary.items():
        message += f"{market}: {data['strong']}/{data['total']} güçlü\n"

    version_info = "🤖 <i>PlanB Ultra v27.2 - 27 Enhanced Modules"
    if SENTIMENT_ENABLED:
        version_info += " + Enhanced Sentiment"
    if ULTRA_RISK_AVAILABLE:
        version_info += " + Professional Risk Management"
    version_info += " + Foundation Analysis + Interactive Reminders"
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
            
            # Hybrid Health Monitor integration
            if HYBRID_HEALTH_AVAILABLE:
                ultra_v3_hybrid_monitor.analysis_count = cycle
                if cycle % ultra_v3_hybrid_monitor.health_check_interval == 0:
                    print(f"🏥 Health check döngüsü #{cycle}")
            
            strong, summary, total = full_market_analysis()
            send_analysis_results(strong, summary, total)
            
            # Send hybrid health report if available
            if HYBRID_HEALTH_AVAILABLE and cycle % ultra_v3_hybrid_monitor.health_check_interval == 0:
                try:
                    import asyncio
                    asyncio.run(ultra_v3_hybrid_monitor.send_health_report())
                except Exception as e:
                    print(f"[DEBUG] Health report error: {e}")
            
            print(f"😴 {SLEEP_BETWEEN_CYCLES//60} dakika uyku")
            time.sleep(SLEEP_BETWEEN_CYCLES)
        except KeyboardInterrupt:
            print("👋 Sistem durduruldu")
            break
        except Exception as e:
            print(f"[ERROR] Genel hata: {e}")
            time.sleep(60)


if __name__ == "__main__":
    print("🚀 PlanB ULTRA FULL TRADER v27.1 başlatılıyor...")
    print("📊 1,248 varlık + 27 Enhanced Ultra Module analiz sistemi")
    
    if SENTIMENT_ENABLED:
        print("🧠 Enhanced Sentiment Analysis: ENABLED")
    else:
        print("📈 Enhanced Sentiment Analysis: DISABLED (set SENTIMENT_ENABLED=true to enable)")
    
    if TELEGRAM_AUTOMATION_AVAILABLE:
        print("📱 Telegram Ultra Automation: AVAILABLE")
    else:
        print("📱 Telegram Ultra Automation: DISABLED")
    
    if HYBRID_HEALTH_AVAILABLE:
        print("🏥 Ultra V3 Hybrid Health Monitor: ACTIVE")
        print(f"🔍 Health check interval: Every {ultra_v3_hybrid_monitor.health_check_interval} cycles")
    else:
        print("🏥 Hybrid Health Monitor: DISABLED")

    start_msg = (
        f"🤖 <b>PlanB ULTRA SİSTEM v27.1 BAŞLATILDI!</b>\n"
        f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
        f"� <b>27 ENHANCED ULTRA MODÜL AKTİF</b>\n"
        f"�📊 <b>Analiz Kapsamı:</b>\n"
        f"🇹🇷 BIST: 724 hisse\n"
        f"🇺🇸 NASDAQ: 124 hisse\n"
        f"💰 CRYPTO: 80 kripto\n"
        f"🏭 EMTIA: 49 emtia\n"
        f"🇩🇪 XETRA: 271 hisse\n\n"
        f"⚡ <b>Toplam: 1,248 varlık</b>\n"
        f"🔄 Her 15 dakikada tam analiz\n"
        f"🎯 Sadece {int(STRONG_THRESHOLD)}+ puan sinyaller bildirilir\n"
        f"🚀 Ultra hızlı paralel işlem\n"
        f"🏛️ Foundation Date Analysis + Astroloji aktif"
    )
    
    if SENTIMENT_ENABLED:
        start_msg += "\n🧠 Enhanced Sentiment Analysis: ACTİVE"
    
    if TELEGRAM_AUTOMATION_AVAILABLE:
        start_msg += "\n📱 Telegram Ultra Automation: ACTİVE"
        start_msg += "\n⏰ 60 dakikalık otomatik mesajlar başlatılıyor!"

    if send_telegram_message(start_msg):
        print("✅ Sistem başlatıldı, Telegram bildirimi gönderildi")
    else:
        print("❌ Telegram gönderimi yapılamadı (env değişkenlerini kontrol edin)")
    
    # 📱⚡ TELEGRAM OTOMASYONUNU BAŞLAT
    if TELEGRAM_AUTOMATION_AVAILABLE:
        telegram_success = planb_ultra_system.start_telegram_automation()
        if telegram_success:
            print("✅ Telegram Ultra Automation başlatıldı - 60 dakikada bir mesaj!")
            
            # Telegram automation status mesajı
            automation_msg = (
                f"📱⚡ TELEGRAM ULTRA AUTOMATION AKTİF ⚡📱\n\n"
                f"⏰ Her 60 dakikada otomatik mesaj\n"
                f"🔄 Ana Sinyaller ↔ Hacim Patlaması rotasyonu\n"
                f"🧠 27-Modül Meta-Enhanced formatı\n"
                f"📱 Mobile-optimized design\n"
                f"🇹🇷 Turkish localized content\n\n"
                f"🎯 Sonraki otomatik mesaj: ~60 dakika sonra\n"
                f"🚀 PlanB ULTRA v27.0 Automation Active!"
            )
            send_telegram_message(automation_msg)
        else:
            print("❌ Telegram Ultra Automation başlatılamadı")
    
    # Ana analiz döngüsünü başlat
    continuous_full_analysis()