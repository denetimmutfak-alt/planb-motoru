#!/usr/bin/env python3
"""
PlanB Motoru - API ve Kütüphane Durum Kontrolü
Tüm kullanılan API'ler ve kütüphanelerin aktif durumunu kontrol eder
"""

import os
import sys
import importlib
import requests
from datetime import datetime
from typing import Dict, List, Tuple

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("⚠️ python-dotenv not found, using system environment only")

def check_color(status: bool) -> str:
    """Renk kodları"""
    return "🟢" if status else "🔴"

def test_import(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """Modül import test"""
    try:
        if package_name:
            module = importlib.import_module(f"{package_name}.{module_name}")
        else:
            module = importlib.import_module(module_name)
        return True, f"✅ {module_name} yüklü"
    except ImportError as e:
        return False, f"❌ {module_name} bulunamadı: {str(e)}"
    except Exception as e:
        return False, f"⚠️ {module_name} hata: {str(e)}"

def test_api_connection(api_name: str, test_url: str, timeout: int = 10) -> Tuple[bool, str]:
    """API bağlantı testi"""
    try:
        response = requests.get(test_url, timeout=timeout)
        if response.status_code == 200:
            return True, f"✅ {api_name} API aktif"
        else:
            return False, f"⚠️ {api_name} API yanıt kodu: {response.status_code}"
    except requests.exceptions.Timeout:
        return False, f"❌ {api_name} API zaman aşımı"
    except requests.exceptions.ConnectionError:
        return False, f"❌ {api_name} API bağlantı hatası"
    except Exception as e:
        return False, f"❌ {api_name} API hatası: {str(e)}"

def main():
    print("🔍 PlanB Motoru - API ve Kütüphane Durum Kontrolü")
    print("=" * 60)
    print(f"📅 Kontrol Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 1. Temel Kütüphaneler
    print("📚 TEMEL KÜTÜPHANELERİ:")
    print("-" * 30)
    
    core_libraries = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("yfinance", "yfinance"),
        ("requests", "requests"),
        ("flask", "flask"),
        ("fastapi", "fastapi"),
        ("aiohttp", "aiohttp"),
    ]
    
    core_results = []
    for lib_name, import_name in core_libraries:
        status, message = test_import(import_name)
        core_results.append((lib_name, status))
        print(f"{check_color(status)} {message}")
    
    print()

    # 2. Teknik Analiz Kütüphaneleri  
    print("📈 TEKNİK ANALİZ KÜTÜPHANELERİ:")
    print("-" * 35)
    
    ta_libraries = [
        ("TA-Lib", "talib"),
        ("pandas-ta", "pandas_ta"),
        ("ta", "ta"),
        ("scipy", "scipy"),
        ("scikit-learn", "sklearn"),
    ]
    
    ta_results = []
    for lib_name, import_name in ta_libraries:
        status, message = test_import(import_name)
        ta_results.append((lib_name, status))
        print(f"{check_color(status)} {message}")
    
    print()

    # 3. API Kütüphaneleri
    print("🔌 API KÜTÜPHANELERİ:")
    print("-" * 20)
    
    api_libraries = [
        ("Finnhub", "finnhub"),
        ("NewsAPI", "newsapi"),
        ("Tweepy (Twitter)", "tweepy"),
        ("python-telegram-bot", "telegram"),
        ("beautifulsoup4", "bs4"),
        ("PRAW (Reddit)", "praw"),  # Eğer varsa
    ]
    
    api_results = []
    for lib_name, import_name in api_libraries:
        status, message = test_import(import_name)
        api_results.append((lib_name, status))
        print(f"{check_color(status)} {message}")
    
    print()

    # 4. API Bağlantı Testleri
    print("🌐 API BAĞLANTI TESTLERİ:")
    print("-" * 25)
    
    api_tests = [
        ("Yahoo Finance", "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"),
        ("Finnhub", "https://finnhub.io/api/v1/quote?symbol=AAPL&token=demo"),
        ("NewsAPI", "https://newsapi.org/v2/top-headlines?country=us&apiKey=demo"),
        ("Reddit", "https://www.reddit.com/r/investing.json"),
        ("CoinGecko", "https://api.coingecko.com/api/v3/ping"),
    ]
    
    connection_results = []
    for api_name, test_url in api_tests:
        status, message = test_api_connection(api_name, test_url)
        connection_results.append((api_name, status))
        print(f"{check_color(status)} {message}")
    
    print()

    # 5. Özel Finnhub Testi
    print("🔧 FİNNHUB DETAYLI TEST:")
    print("-" * 25)
    
    try:
        import finnhub
        finnhub_client = finnhub.Client(api_key="demo")
        
        # Demo quote testi
        try:
            quote = finnhub_client.quote('AAPL')
            if quote and 'c' in quote:
                print(f"✅ Finnhub quote testi başarılı (AAPL: ${quote['c']})")
                finnhub_quote_ok = True
            else:
                print("⚠️ Finnhub quote testi: Veri bulunamadı")
                finnhub_quote_ok = False
        except Exception as e:
            print(f"❌ Finnhub quote testi hatası: {e}")
            finnhub_quote_ok = False
            
    except ImportError:
        print("❌ Finnhub kütüphanesi yüklü değil")
        finnhub_quote_ok = False
    except Exception as e:
        print(f"❌ Finnhub genel hatası: {e}")
        finnhub_quote_ok = False
    
    print()

    # 6. Ortam Değişkenleri Kontrolü
    print("🔑 ORTAM DEĞİŞKENLERİ:")
    print("-" * 22)
    
    env_vars = [
        "FINNHUB_KEY",
        "NEWS_API_KEY", 
        "TWITTER_BEARER_TOKEN",
        "REDDIT_CLIENT_ID",
        "TELEGRAM_BOT_TOKEN",
    ]
    
    env_results = []
    for var_name in env_vars:
        value = os.getenv(var_name)
        if value:
            masked_value = value[:8] + "..." if len(value) > 8 else value
            print(f"✅ {var_name}: {masked_value}")
            env_results.append((var_name, True))
        else:
            print(f"❌ {var_name}: Bulunamadı")
            env_results.append((var_name, False))
    
    print()

    # 7. Özet Rapor
    print("📊 ÖZET RAPOR:")
    print("-" * 15)
    
    total_core = len(core_results)
    success_core = sum(1 for _, status in core_results if status)
    
    total_ta = len(ta_results)
    success_ta = sum(1 for _, status in ta_results if status)
    
    total_api = len(api_results)
    success_api = sum(1 for _, status in api_results if status)
    
    total_conn = len(connection_results)
    success_conn = sum(1 for _, status in connection_results if status)
    
    total_env = len(env_results)
    success_env = sum(1 for _, status in env_results if status)
    
    print(f"📚 Temel Kütüphaneler: {success_core}/{total_core} ({(success_core/total_core)*100:.0f}%)")
    print(f"📈 Teknik Analiz: {success_ta}/{total_ta} ({(success_ta/total_ta)*100:.0f}%)")
    print(f"🔌 API Kütüphaneleri: {success_api}/{total_api} ({(success_api/total_api)*100:.0f}%)")
    print(f"🌐 API Bağlantıları: {success_conn}/{total_conn} ({(success_conn/total_conn)*100:.0f}%)")
    print(f"🔑 Ortam Değişkenleri: {success_env}/{total_env} ({(success_env/total_env)*100:.0f}%)")
    
    overall_success = (success_core + success_ta + success_api + success_conn + success_env)
    overall_total = (total_core + total_ta + total_api + total_conn + total_env)
    overall_percentage = (overall_success / overall_total) * 100
    
    print()
    print(f"🎯 GENEL BAŞARI ORANI: {overall_success}/{overall_total} ({overall_percentage:.1f}%)")
    
    if overall_percentage >= 80:
        print("🟢 Sistem durumu: MÜKEMMEL")
    elif overall_percentage >= 60:
        print("🟡 Sistem durumu: İYİ") 
    else:
        print("🔴 Sistem durumu: DİKKAT GEREKTİRİR")
    
    print()
    print("=" * 60)
    print("✨ Kontrol tamamlandı!")

if __name__ == "__main__":
    main()