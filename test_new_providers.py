#!/usr/bin/env python3
"""
Yeni tam listeler ile provider testleri
"""

import sys
import os

# Ana dizini Python yoluna ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from src.data.market_data import MarketDataProvider
    
    print("=== YENİ TAM LİSTE PROVİDER TESTLERİ ===")
    
    # Market data provider'ı başlat
    provider = MarketDataProvider()
    
    # Tüm semboller
    all_symbols = provider.get_all_symbols()
    print(f"\n📊 TOPLAM SEMBOL SAYISI: {len(all_symbols)}")
    
    # Provider'lar ve sembol sayıları
    providers = ['bist', 'nasdaq', 'xetra', 'crypto', 'commodities']
    total_expected = 0
    
    print(f"\n🔍 PROVIDER DETAYLARI:")
    
    # Her provider için özel metodları kullan
    provider_methods = {
        'bist': provider.get_bist_symbols,
        'nasdaq': provider.get_nasdaq_symbols, 
        'xetra': provider.get_xetra_symbols,
        'crypto': provider.get_crypto_symbols,
        'commodities': provider.get_commodity_symbols
    }
    
    for p in providers:
        if p in provider_methods:
            symbols = provider_methods[p]()
            count = len(symbols)
            print(f"  • {p.upper()}: {count} sembol")
            
            # Beklenen sayıları kontrol et
            expected = {
                'bist': 745,
                'nasdaq': 109, 
                'xetra': 157,
                'crypto': 80,
                'commodities': 49
            }
            
            if p in expected:
                exp_count = expected[p]
                status = "✅" if count == exp_count else f"❌ (beklenen: {exp_count})"
                print(f"     Durum: {status}")
                total_expected += exp_count
    
    print(f"\n📈 BEKLENEN TOPLAM: {total_expected}")
    print(f"📈 GERÇEK TOPLAM: {len(all_symbols)}")
    
    # Örnek semboller göster
    print(f"\n🔤 ÖRNEK SEMBOLLER:")
    for p in providers:
        if p in provider_methods:
            symbols = provider_methods[p]()
            if symbols:
                sample = symbols[:3] if len(symbols) >= 3 else symbols
                print(f"  • {p.upper()}: {', '.join(sample)}")
    
    print(f"\n✅ Test tamamlandı!")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()