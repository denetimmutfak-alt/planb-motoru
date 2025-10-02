#!/usr/bin/env python3
"""
Final API ve Sistem Durum Kontrolü
Tüm güncellenmiş API key'ler ile tam test
"""

import os
from dotenv import load_dotenv
import requests
from datetime import datetime

# Load environment
load_dotenv()

def final_system_check():
    print("🚀 FINAL API VE SİSTEM DURUM KONTROLÜ")
    print("=" * 60)
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Environment variables check
    print(f"\n🔑 ENVIRONMENT VARIABLES:")
    print("-" * 30)
    
    env_vars = {
        "FINNHUB_KEY": "Finnhub API Key",
        "FINNHUB_WEBHOOK_SECRET": "Finnhub Webhook Secret", 
        "TELEGRAM_BOT_TOKEN": "Telegram Bot Token",
        "TELEGRAM_CHAT_ID": "Telegram Chat ID",
        "NEWS_API_KEY": "News API Key",
        "TWITTER_BEARER_TOKEN": "Twitter Bearer Token",
        "REDDIT_CLIENT_ID": "Reddit Client ID"
    }
    
    active_keys = 0
    total_keys = len(env_vars)
    
    for var_name, description in env_vars.items():
        value = os.getenv(var_name, "")
        if value and not value.startswith("YOUR_"):
            masked = value[:8] + "..." if len(value) > 8 else value
            print(f"✅ {var_name}: {masked}")
            active_keys += 1
        else:
            print(f"❌ {var_name}: Bulunamadı")
    
    print(f"\n📊 API Key Status: {active_keys}/{total_keys} ({(active_keys/total_keys)*100:.0f}%)")
    
    # API Functionality Tests
    print(f"\n🔧 API FONKSİYONALİTE TESTLERİ:")
    print("-" * 35)
    
    working_apis = 0
    total_tests = 0
    
    # Finnhub Test
    print(f"🔍 Finnhub API Test:")
    total_tests += 1
    finnhub_key = os.getenv("FINNHUB_KEY", "")
    if finnhub_key:
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={finnhub_key}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                price = data.get('c', 'N/A')
                print(f"   ✅ Aktif (AAPL: ${price})")
                working_apis += 1
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")
    else:
        print(f"   ❌ Key bulunamadı")
    
    # Telegram Bot Test
    print(f"🔍 Telegram Bot Test:")
    total_tests += 1
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if telegram_token:
        try:
            url = f"https://api.telegram.org/bot{telegram_token}/getMe"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data.get('result', {})
                    username = bot_info.get('username', 'N/A')
                    print(f"   ✅ Aktif (@{username})")
                    working_apis += 1
                else:
                    print(f"   ❌ Bot response error")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Connection Error: {e}")
    else:
        print(f"   ❌ Token bulunamadı")
    
    # Yahoo Finance Test
    print(f"🔍 Yahoo Finance Test:")
    total_tests += 1
    try:
        import yfinance as yf
        ticker = yf.Ticker("AAPL")
        data = ticker.history(period="1d")
        if not data.empty:
            latest_price = data['Close'].iloc[-1]
            print(f"   ✅ Aktif (AAPL: ${latest_price:.2f})")
            working_apis += 1
        else:
            print(f"   ❌ Veri boş")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # CoinGecko Test
    print(f"🔍 CoinGecko Test:")
    total_tests += 1
    try:
        url = "https://api.coingecko.com/api/v3/ping"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Aktif")
            working_apis += 1
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    print(f"\n📊 API Test Results: {working_apis}/{total_tests} ({(working_apis/total_tests)*100:.0f}%)")
    
    # Data Routing Test
    print(f"\n📊 VERİ YÖNLENDİRME TESTİ:")
    print("-" * 30)
    
    try:
        from resilient_loader_v2 import is_finnhub_supported
        
        test_symbols = {
            "BIST": "THYAO.IS",
            "NASDAQ": "AAPL", 
            "CRYPTO": "BTC-USD",
            "EMTIA": "GC=F",
            "XETRA": "SAP.DE"
        }
        
        for market, symbol in test_symbols.items():
            finnhub_support = is_finnhub_supported(symbol)
            primary = "Yahoo Finance"
            fallback = "Finnhub" if finnhub_support else "Yahoo Only"
            print(f"   {market} ({symbol}): {primary} → {fallback}")
            
    except ImportError:
        print(f"   ❌ Resilient loader import hatası")
    
    # Overall Assessment
    print(f"\n🎯 GENEL DEĞERLENDİRME:")
    print("-" * 25)
    
    total_score = active_keys + working_apis
    max_score = total_keys + total_tests
    percentage = (total_score / max_score) * 100
    
    print(f"🔑 API Keys: {active_keys}/{total_keys} ({(active_keys/total_keys)*100:.0f}%)")
    print(f"🌐 API Tests: {working_apis}/{total_tests} ({(working_apis/total_tests)*100:.0f}%)")
    print(f"🎯 TOTAL SCORE: {total_score}/{max_score} ({percentage:.1f}%)")
    
    if percentage >= 80:
        status = "🟢 EXCELLENT - Production Ready"
        action = "✅ Hetzner'a deploy edilebilir"
    elif percentage >= 60:
        status = "🟡 GOOD - Minor issues"
        action = "⚠️ Bazı optimizasyonlar gerekli"
    else:
        status = "🔴 NEEDS WORK - Major issues"
        action = "❌ Daha fazla düzeltme gerekli"
    
    print(f"\n📊 System Status: {status}")
    print(f"🚀 Action: {action}")
    
    # Final Recommendations
    print(f"\n📋 SONRAKİ ADIMLAR:")
    print("-" * 20)
    
    if active_keys >= 4 and working_apis >= 3:
        print("1. ✅ Sistem Hetzner'a deploy için hazır")
        print("2. 🔄 git commit && git push")
        print("3. 🖥️ SSH ile Hetzner'a bağlan")
        print("4. 📥 git pull && systemctl restart planb.service")
        print("5. 📱 Telegram'dan ilk mesajı bekle")
    else:
        print("1. 🔧 Eksik API key'leri tamamla")
        print("2. 🧪 Testleri tekrar çalıştır")
        print("3. 🚀 Sistem hazır olunca deploy et")
    
    print(f"\n✨ Final kontrol tamamlandı!")
    
    # Webhook note
    webhook_secret = os.getenv("FINNHUB_WEBHOOK_SECRET", "")
    if webhook_secret:
        print(f"\n📡 WEBHOOK BİLGİSİ:")
        print(f"   Finnhub Webhook Secret: {webhook_secret[:8]}...")
        print(f"   Not: Real-time data için webhook kullanılabilir")

if __name__ == "__main__":
    final_system_check()