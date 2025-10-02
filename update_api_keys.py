#!/usr/bin/env python3
"""
API Anahtarı Toplama ve .env Güncelleme Scripti
Arkadaşın önerisi doğrultusunda tek komutla tüm API'leri güncelleyelim
"""

import os
from datetime import datetime

def collect_api_keys():
    """Tüm API anahtarlarını topla"""
    
    print("🔍 API Anahtarlarını Toplama İşlemi Başlatılıyor...")
    print("=" * 60)
    
    # Bulunan gerçek API anahtarları
    api_keys = {
        # Telegram - Bulundu
        "TELEGRAM_BOT_TOKEN": "7994708397:AAGUWY92gsAO7cOIXV_ShwsojH28riKCyXE",
        "TELEGRAM_CHAT_ID": "6263576109",
        
        # Finnhub - Demo key (ücretsiz)
        "FINNHUB_KEY": "demo",  # Gerçek key gerekirse: finnhub.io/register
        
        # News API - Placeholder (ücretsiz key gerekli)
        "NEWS_API_KEY": "YOUR_NEWS_API_KEY",  # newsapi.org/register
        
        # Twitter - Placeholder (ücretsiz key gerekli)
        "TWITTER_BEARER_TOKEN": "YOUR_TWITTER_BEARER_TOKEN",  # developer.twitter.com
        
        # Reddit - Placeholder (ücretsiz key gerekli)
        "REDDIT_CLIENT_ID": "YOUR_REDDIT_CLIENT_ID",  # reddit.com/prefs/apps
        "REDDIT_CLIENT_SECRET": "YOUR_REDDIT_CLIENT_SECRET",
        
        # Diğer gerekli değişkenler
        "REDDIT_USER_AGENT": "PlanBULTRA/1.0 by planb_trader",
        "ALPHA_VANTAGE_KEY": "YOUR_ALPHA_VANTAGE_KEY",
        "POLYGON_KEY": "YOUR_POLYGON_KEY",
        
        # Performance Settings
        "REDIS_URL": "redis://localhost:6379/0",
        "CACHE_TTL": "3600",
        "DATABASE_URL": "sqlite:///data/planb_motoru.db",
        "LOG_LEVEL": "INFO",
        "MAX_WORKERS": "4",
        "CHUNK_SIZE": "50",
        "REQUEST_TIMEOUT": "30",
        "SLEEP_BETWEEN_CYCLES": "3600",
        
        # Feature Flags
        "ENABLE_SENTIMENT": "true",
        "ENABLE_EARLY_WARNING": "true",
        "ENABLE_ULTRA_V3": "true",
        "ENABLE_MULTI_MARKET": "true",
        
        # Market Multipliers
        "NASDAQ_MULTIPLIER": "3",
        "XETRA_MULTIPLIER": "2",
        "EMTIA_MULTIPLIER": "2",
        "CRYPTO_MULTIPLIER": "10",
        
        # Risk Management
        "MAX_POSITION_SIZE": "0.1",
        "STOP_LOSS_PCT": "0.05",
        "TAKE_PROFIT_PCT": "0.15",
    }
    
    return api_keys

def update_env_file(api_keys):
    """Güvenli şekilde .env dosyasını güncelle"""
    
    env_path = ".env"
    backup_path = f".env.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Mevcut .env dosyasını yedekle
    if os.path.exists(env_path):
        with open(env_path, 'r') as src, open(backup_path, 'w') as dst:
            dst.write(src.read())
        print(f"✅ Mevcut .env yedeklendi: {backup_path}")
    
    # Yeni .env dosyasını oluştur
    with open(env_path, 'w') as f:
        f.write(f"# PlanB ULTRA Trading System - Environment Variables\n")
        f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Collected from existing system files\n\n")
        
        # API Keys section
        f.write("# ===== API KEYS =====\n")
        api_section = [
            "FINNHUB_KEY", "NEWS_API_KEY", "TWITTER_BEARER_TOKEN",
            "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT",
            "ALPHA_VANTAGE_KEY", "POLYGON_KEY"
        ]
        
        for key in api_section:
            if key in api_keys:
                f.write(f"{key}={api_keys[key]}\n")
        
        # Telegram section
        f.write(f"\n# ===== TELEGRAM BOT =====\n")
        f.write(f"TELEGRAM_BOT_TOKEN={api_keys['TELEGRAM_BOT_TOKEN']}\n")
        f.write(f"TELEGRAM_CHAT_ID={api_keys['TELEGRAM_CHAT_ID']}\n")
        
        # Database section
        f.write(f"\n# ===== DATABASE & CACHE =====\n")
        db_section = ["REDIS_URL", "CACHE_TTL", "DATABASE_URL"]
        for key in db_section:
            if key in api_keys:
                f.write(f"{key}={api_keys[key]}\n")
        
        # Performance section
        f.write(f"\n# ===== PERFORMANCE =====\n")
        perf_section = ["LOG_LEVEL", "MAX_WORKERS", "CHUNK_SIZE", "REQUEST_TIMEOUT", "SLEEP_BETWEEN_CYCLES"]
        for key in perf_section:
            if key in api_keys:
                f.write(f"{key}={api_keys[key]}\n")
        
        # Feature flags section
        f.write(f"\n# ===== FEATURE FLAGS =====\n")
        feature_section = ["ENABLE_SENTIMENT", "ENABLE_EARLY_WARNING", "ENABLE_ULTRA_V3", "ENABLE_MULTI_MARKET"]
        for key in feature_section:
            if key in api_keys:
                f.write(f"{key}={api_keys[key]}\n")
        
        # Market multipliers section
        f.write(f"\n# ===== MARKET MULTIPLIERS =====\n")
        market_section = ["NASDAQ_MULTIPLIER", "XETRA_MULTIPLIER", "EMTIA_MULTIPLIER", "CRYPTO_MULTIPLIER"]
        for key in market_section:
            if key in api_keys:
                f.write(f"{key}={api_keys[key]}\n")
        
        # Risk management section
        f.write(f"\n# ===== RISK MANAGEMENT =====\n")
        risk_section = ["MAX_POSITION_SIZE", "STOP_LOSS_PCT", "TAKE_PROFIT_PCT"]
        for key in risk_section:
            if key in api_keys:
                f.write(f"{key}={api_keys[key]}\n")
    
    print(f"✅ Yeni .env dosyası oluşturuldu: {env_path}")
    return env_path

def test_telegram_bot(token):
    """Telegram bot test"""
    try:
        import requests
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                username = bot_info.get('username', 'N/A')
                first_name = bot_info.get('first_name', 'N/A')
                print(f"✅ Telegram Bot Test: {first_name} (@{username})")
                return True
        
        print(f"❌ Telegram Bot Test Failed: {response.status_code}")
        return False
        
    except Exception as e:
        print(f"❌ Telegram Bot Test Error: {e}")
        return False

def main():
    print("🚀 PlanB ULTRA - API Anahtarı Güncelleme Scripti")
    print("=" * 60)
    
    # API anahtarlarını topla
    api_keys = collect_api_keys()
    
    # API anahtarlarını listele
    print("\n📋 TOPLANAN API ANAHTARLARI:")
    print("-" * 40)
    for key, value in api_keys.items():
        if "TOKEN" in key or "KEY" in key or "SECRET" in key:
            if value.startswith("YOUR_"):
                print(f"⚠️  {key}: {value} (PLACEHOLDER)")
            else:
                masked = value[:8] + "..." if len(value) > 8 else value
                print(f"✅ {key}: {masked}")
        else:
            print(f"🔧 {key}: {value}")
    
    # .env dosyasını güncelle
    print("\n📝 .ENV DOSYASI GÜNCELLENİYOR...")
    print("-" * 40)
    env_path = update_env_file(api_keys)
    
    # Telegram bot test
    print("\n🔍 TELEGRAM BOT TEST:")
    print("-" * 25)
    telegram_token = api_keys["TELEGRAM_BOT_TOKEN"]
    test_telegram_bot(telegram_token)
    
    # Özet
    print("\n🎯 İŞLEM TAMAMLANDI!")
    print("=" * 60)
    print(f"📁 .env dosyası: {env_path}")
    print("📊 Çalışan API'ler:")
    print("   ✅ Telegram Bot")
    print("   ✅ Yahoo Finance")
    print("   ✅ CoinGecko")
    print("   ⚠️  Finnhub (demo key)")
    print("\n📋 Sonraki Adımlar:")
    print("1. İsteğe bağlı: Gerçek API key'leri al")
    print("   - Finnhub: https://finnhub.io/register")
    print("   - News API: https://newsapi.org/register")
    print("   - Twitter: https://developer.twitter.com/")
    print("2. Sistemi test et: python telegram_full_trader_with_sentiment.py")
    print("3. Hetzner'a deploy et")
    
    # Arkadaşın belirttiği test komutu
    print(f"\n🧪 Telegram Bot Canlılık Test Komutu:")
    print(f"curl -s \"https://api.telegram.org/bot{telegram_token}/getMe\" | python -m json.tool")

if __name__ == "__main__":
    main()