#!/usr/bin/env python3
"""
PlanB Motoru - Tam API Durum Raporu
Detaylı sistem ve API durum analizi
"""

import os
import sys
import importlib
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

def print_section(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_subsection(title):
    print(f"\n📋 {title}")
    print("-" * 40)

def test_yfinance():
    """Yahoo Finance Test"""
    try:
        import yfinance as yf
        ticker = yf.Ticker("AAPL")
        # Get just 1 day of data to avoid rate limiting
        data = ticker.history(period="1d")
        if not data.empty:
            latest_price = data['Close'].iloc[-1]
            print(f"✅ Yahoo Finance: AAPL = ${latest_price:.2f}")
            return True
        else:
            print("⚠️ Yahoo Finance: Veri boş")
            return False
    except Exception as e:
        print(f"❌ Yahoo Finance Hatası: {e}")
        return False

def test_telegram():
    """Telegram Test"""
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
    
    if not token or token == "YOUR_TELEGRAM_BOT_TOKEN":
        print("❌ Telegram: Token bulunamadı")
        return False
        
    if not chat_id or chat_id == "YOUR_TELEGRAM_CHAT_ID":
        print("❌ Telegram: Chat ID bulunamadı")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print(f"✅ Telegram Bot: {bot_info.get('first_name', 'Unknown')} (@{bot_info.get('username', 'N/A')})")
                return True
            else:
                print(f"❌ Telegram API Hatası: {data}")
                return False
        else:
            print(f"❌ Telegram HTTP Hatası: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Telegram Bağlantı Hatası: {e}")
        return False

def main():
    print("🚀 PlanB Motoru - Tam API Durum Raporu")
    print(f"📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Python Environment Info
    print_section("PYTHON ENVIRONMENT")
    print(f"🐍 Python Version: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"🔧 Platform: {sys.platform}")
    
    # Critical Libraries Test
    print_section("CORE LIBRARIES")
    
    critical_libs = [
        ("pandas", "Data Processing"),
        ("numpy", "Numerical Computing"), 
        ("yfinance", "Yahoo Finance API"),
        ("requests", "HTTP Requests"),
        ("talib", "Technical Analysis"),
        ("pandas_ta", "Pandas TA"),
        ("flask", "Web Framework"),
        ("fastapi", "Modern API Framework"),
        ("telegram", "Telegram Bot"),
        ("finnhub", "Finnhub API"),
        ("newsapi", "News API"),
        ("tweepy", "Twitter API"),
        ("praw", "Reddit API"),
        ("bs4", "Web Scraping"),
        ("aiohttp", "Async HTTP"),
    ]
    
    working_libs = 0
    total_libs = len(critical_libs)
    
    for lib_name, description in critical_libs:
        try:
            importlib.import_module(lib_name)
            print(f"✅ {lib_name:15} - {description}")
            working_libs += 1
        except ImportError:
            print(f"❌ {lib_name:15} - {description} (NOT INSTALLED)")
        except Exception as e:
            print(f"⚠️ {lib_name:15} - {description} (ERROR: {e})")
    
    print(f"\n📊 Library Status: {working_libs}/{total_libs} ({(working_libs/total_libs)*100:.1f}%)")
    
    # Environment Variables
    print_section("ENVIRONMENT VARIABLES")
    
    env_vars = [
        ("FINNHUB_KEY", "Finnhub API Key"),
        ("NEWS_API_KEY", "News API Key"),
        ("TWITTER_BEARER_TOKEN", "Twitter Bearer Token"),
        ("REDDIT_CLIENT_ID", "Reddit Client ID"),
        ("TELEGRAM_BOT_TOKEN", "Telegram Bot Token"),
        ("TELEGRAM_CHAT_ID", "Telegram Chat ID"),
    ]
    
    working_envs = 0
    total_envs = len(env_vars)
    
    for var_name, description in env_vars:
        value = os.getenv(var_name, "")
        if value and not value.startswith("YOUR_"):
            masked = value[:8] + "..." if len(value) > 8 else value
            print(f"✅ {var_name:20} - {description} ({masked})")
            working_envs += 1
        else:
            print(f"❌ {var_name:20} - {description} (NOT SET)")
    
    print(f"\n📊 Environment Status: {working_envs}/{total_envs} ({(working_envs/total_envs)*100:.1f}%)")
    
    # API Functionality Tests
    print_section("API FUNCTIONALITY TESTS")
    
    working_apis = 0
    total_apis = 0
    
    # Yahoo Finance Test
    print_subsection("Yahoo Finance")
    total_apis += 1
    if test_yfinance():
        working_apis += 1
    
    # Telegram Test  
    print_subsection("Telegram Bot")
    total_apis += 1
    if test_telegram():
        working_apis += 1
    
    # API Connection Tests (Basic)
    print_subsection("Basic API Connectivity")
    
    basic_tests = [
        ("CoinGecko", "https://api.coingecko.com/api/v3/ping"),
        ("JSONPlaceholder", "https://jsonplaceholder.typicode.com/posts/1"),
    ]
    
    for api_name, test_url in basic_tests:
        total_apis += 1
        try:
            response = requests.get(test_url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {api_name}: Online")
                working_apis += 1
            else:
                print(f"⚠️ {api_name}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {api_name}: {e}")
    
    print(f"\n📊 API Status: {working_apis}/{total_apis} ({(working_apis/total_apis)*100:.1f}%)")
    
    # Overall Assessment
    print_section("OVERALL ASSESSMENT")
    
    total_score = working_libs + working_envs + working_apis
    max_score = total_libs + total_envs + total_apis
    percentage = (total_score / max_score) * 100
    
    print(f"📚 Libraries: {working_libs}/{total_libs} ({(working_libs/total_libs)*100:.1f}%)")
    print(f"🔑 Environment: {working_envs}/{total_envs} ({(working_envs/total_envs)*100:.1f}%)")
    print(f"🌐 APIs: {working_apis}/{total_apis} ({(working_apis/total_apis)*100:.1f}%)")
    print(f"\n🎯 TOTAL SCORE: {total_score}/{max_score} ({percentage:.1f}%)")
    
    if percentage >= 85:
        status = "🟢 EXCELLENT - System ready for production"
    elif percentage >= 70:
        status = "🟡 GOOD - Minor issues, mostly functional"
    elif percentage >= 50:
        status = "🟠 FAIR - Some critical issues need attention"
    else:
        status = "🔴 POOR - Major issues, system needs work"
    
    print(f"📊 System Status: {status}")
    
    # Recommendations
    print_section("RECOMMENDATIONS")
    
    if working_libs < total_libs:
        print("📚 Install missing libraries: pip install -r requirements.txt")
    
    if working_envs < total_envs:
        print("🔑 Update .env file with real API keys")
        print("   - Get Finnhub key: https://finnhub.io/register")
        print("   - Get News API key: https://newsapi.org/register")
        print("   - Get Twitter API: https://developer.twitter.com/")
    
    if working_apis < total_apis:
        print("🌐 Check API rate limits and connectivity")
        print("   - Yahoo Finance: May have rate limiting")
        print("   - Telegram: Verify bot token is correct")
    
    print("\n✨ Analysis complete!")
    print(f"💾 Working Directory: {os.getcwd()}")
    print("🔄 Run 'python telegram_full_trader_with_sentiment.py' to test full system")

if __name__ == "__main__":
    main()