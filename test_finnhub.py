#!/usr/bin/env python3
"""
Finnhub API Gerçek Test
"""

import os
from dotenv import load_dotenv
import requests

# Load environment
load_dotenv()

# API key
api_key = os.getenv("FINNHUB_KEY", "")
print(f"🔑 API Key: {api_key[:10]}..." if api_key else "❌ API Key bulunamadı")

if api_key:
    # Test URL
    test_url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={api_key}"
    
    try:
        response = requests.get(test_url, timeout=10)
        print(f"📡 HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Finnhub API çalışıyor!")
            print(f"📊 AAPL Data: {data}")
        else:
            print(f"❌ API Hatası: {response.text}")
            
    except Exception as e:
        print(f"❌ Bağlantı Hatası: {e}")

# Test finnhub-python package
try:
    import finnhub
    client = finnhub.Client(api_key=api_key)
    
    print("\n🔧 Finnhub-python ile test:")
    try:
        quote = client.quote('AAPL')
        print(f"✅ Package çalışıyor! AAPL: ${quote.get('c', 'N/A')}")
    except Exception as e:
        print(f"❌ Package hatası: {e}")
        
except ImportError:
    print("❌ finnhub-python paketi bulunamadı")