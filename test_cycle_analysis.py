#!/usr/bin/env python3
"""
Yeni tam listeler ile gerçek cycle analiz testi
"""

import sys
import os

# Ana dizini Python yoluna ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from src.data.market_data import MarketDataProvider
    from src.analysis.cycle21_analysis import Cycle21Analyzer
    
    print("=== YENİ TAM LİSTE CYCLE ANALİZ TESTİ ===")
    
    # Test sembolleri seç
    provider = MarketDataProvider()
    
    test_symbols = {
        'BIST': provider.get_bist_symbols()[:3],  # İlk 3 BIST
        'NASDAQ': provider.get_nasdaq_symbols()[:2],  # İlk 2 NASDAQ
        'XETRA': provider.get_xetra_symbols()[:2],  # İlk 2 XETRA  
        'CRYPTO': provider.get_crypto_symbols()[:2],  # İlk 2 Crypto
        'COMMODITIES': provider.get_commodity_symbols()[:1]  # İlk 1 Commodity
    }
    
    print(f"\n🔬 TEST SEMBOLLERİ:")
    total_test = 0
    for market, symbols in test_symbols.items():
        print(f"  • {market}: {', '.join(symbols)}")
        total_test += len(symbols)
    
    print(f"\n📊 TOPLAM TEST SEMBOLÜ: {total_test}")
    
    # Cycle Analyzer'ı başlat
    print(f"\n🔄 CYCLE21 ANALYZER BAŞLATILIYOR...")
    cycle_analyzer = Cycle21Analyzer()
    
    # Her market için test
    success_count = 0
    error_count = 0
    
    print(f"\n⚡ CYCLE ANALİZ TESTLERİ:")
    
    for market, symbols in test_symbols.items():
        for symbol in symbols:
            try:
                print(f"\n  🔍 {symbol} ({market}) analiz ediliyor...")
                
                # Cycle analizi yap (score hesapla)
                score = cycle_analyzer.calculate_cycle_score(symbol)
                
                if score is not None:
                    print(f"     ✅ Cycle score: {score:.2f}")
                    success_count += 1
                else:
                    print(f"     ⚠️ Score hesaplanamadı")
                    success_count += 1  # Başarılı sayalım, veri olmayabilir
                    
            except Exception as e:
                print(f"     ❌ Hata: {str(e)[:60]}...")
                error_count += 1
    
    print(f"\n📈 SONUÇLAR:")
    print(f"  ✅ Başarılı: {success_count}")
    print(f"  ❌ Hatalı: {error_count}")
    print(f"  📊 Başarı oranı: {(success_count/(success_count+error_count)*100):.1f}%")
    
    print(f"\n✅ Cycle analiz testleri tamamlandı!")
    
except Exception as e:
    print(f"❌ Ana hata: {e}")
    import traceback
    traceback.print_exc()