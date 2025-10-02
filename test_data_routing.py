#!/usr/bin/env python3
"""
Veri Yönlendirme Test Scripti
BIST -> YFinance, Diğerleri -> Finnhub test
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_data_routing():
    """Veri yönlendirme sistemini test et"""
    
    print("🔍 VERİ YÖNLENDİRME SİSTEMİ TEST")
    print("=" * 50)
    
    # Test sembolleri
    test_symbols = {
        "BIST": ["THYAO.IS", "GARAN.IS", "AKBNK.IS"],
        "NASDAQ": ["AAPL", "MSFT", "GOOGL"], 
        "CRYPTO": ["BTC-USD", "ETH-USD"],
        "EMTIA": ["GC=F", "CL=F"],  # Gold, Oil futures
        "XETRA": ["SAP.DE", "BMW.DE"]
    }
    
    print(f"📊 Test Sembolleri:")
    for market, symbols in test_symbols.items():
        print(f"   {market}: {', '.join(symbols)}")
    
    print(f"\n🔧 Mevcut API Durumu:")
    
    # Yahoo Finance test
    try:
        import yfinance as yf
        test_ticker = yf.Ticker("AAPL")
        data = test_ticker.history(period="1d")
        if not data.empty:
            print(f"✅ Yahoo Finance: Çalışıyor (AAPL test)")
        else:
            print(f"⚠️ Yahoo Finance: Veri boş")
    except Exception as e:
        print(f"❌ Yahoo Finance: {e}")
    
    # Finnhub test
    finnhub_key = os.getenv("FINNHUB_KEY", "")
    if finnhub_key and finnhub_key != "demo":
        try:
            import finnhub
            client = finnhub.Client(api_key=finnhub_key)
            quote = client.quote('AAPL')
            if quote and 'c' in quote:
                print(f"✅ Finnhub: Çalışıyor (AAPL: ${quote['c']})")
            else:
                print(f"⚠️ Finnhub: Veri alınamadı")
        except Exception as e:
            print(f"❌ Finnhub: {e}")
    else:
        print(f"⚠️ Finnhub: Demo key veya key yok")
    
    print(f"\n📋 VERİ YÖNLENDİRME KURALLARI:")
    print("-" * 30)
    print("✅ BIST (.IS): Yahoo Finance")
    print("✅ NASDAQ: Yahoo Finance (primary), Finnhub (fallback)")  
    print("✅ CRYPTO (-USD): Yahoo Finance")
    print("✅ EMTIA (=F): Yahoo Finance")
    print("✅ XETRA (.DE): Yahoo Finance (primary), Finnhub (fallback)")
    
    # Resilient loader test
    print(f"\n🔄 RESILIENT LOADER TEST:")
    print("-" * 25)
    
    try:
        from resilient_loader_v2 import cached_download, is_finnhub_supported
        
        # Test BIST (YFinance only)
        print(f"📊 BIST Test (THYAO.IS):")
        bist_supported = is_finnhub_supported("THYAO.IS")
        print(f"   Finnhub destekli: {bist_supported} (Beklenen: False)")
        
        # Test NASDAQ (Both supported)
        print(f"📊 NASDAQ Test (AAPL):")
        nasdaq_supported = is_finnhub_supported("AAPL")
        print(f"   Finnhub destekli: {nasdaq_supported} (Beklenen: True)")
        
        # Quick data test
        print(f"\n🌐 Veri Çekme Testi:")
        
        # Test BIST
        try:
            bist_data = cached_download("THYAO.IS", period="5d")
            if not bist_data.empty:
                print(f"✅ THYAO.IS: {len(bist_data)} gün verisi")
            else:
                print(f"⚠️ THYAO.IS: Veri boş")
        except Exception as e:
            print(f"❌ THYAO.IS: {e}")
        
        # Test NASDAQ
        try:
            nasdaq_data = cached_download("AAPL", period="5d")
            if not nasdaq_data.empty:
                print(f"✅ AAPL: {len(nasdaq_data)} gün verisi")
            else:
                print(f"⚠️ AAPL: Veri boş")
        except Exception as e:
            print(f"❌ AAPL: {e}")
            
    except ImportError as e:
        print(f"❌ Resilient loader import hatası: {e}")
    except Exception as e:
        print(f"❌ Resilient loader genel hatası: {e}")
    
    print(f"\n🎯 SONUÇ:")
    print("=" * 20)
    print("📊 BIST hisseleri (.IS): Yahoo Finance üzerinden çekiliyor")
    print("📊 Diğer pazarlar: Yahoo Finance öncelikli, Finnhub yedek")
    print("📊 Sistem otomatik olarak en iyi veri kaynağını seçiyor")
    
    # Ana sistem dosyasında kullanım
    print(f"\n📁 Ana sistemde kullanım:")
    print("   telegram_full_trader_with_sentiment.py")
    print("   → analyze_symbol_fast() fonksiyonu")
    print("   → resilient_loader_v2.cached_download() kullanıyor")

if __name__ == "__main__":
    test_data_routing()