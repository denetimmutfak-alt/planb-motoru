#!/usr/bin/env python3
"""
Hızlı test: Düzeltilen analiz sistemini test et
"""

import sys
import os

# Ana dizini Python yoluna ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from src.data.market_data import MarketDataProvider
    from src.analysis.financial_analysis import FinancialAnalyzer
    
    print("=== DÜZELTME TESTLERİ ===")
    
    # Market data provider'ı başlat
    provider = MarketDataProvider()
    analyzer = FinancialAnalyzer()
    
    # Test sembolü
    test_symbols = provider.get_bist_symbols()[:3]
    print(f"\n🔬 TEST SEMBOLLERİ: {', '.join(test_symbols)}")
    
    for symbol in test_symbols:
        try:
            print(f"\n🔍 {symbol} analiz ediliyor...")
            
            # Basit veri simülasyonu
            import pandas as pd
            import numpy as np
            
            # Örnek veri oluştur
            dates = pd.date_range('2024-01-01', periods=100, freq='D')
            prices = np.random.random(100) * 100 + 50
            
            stock_data = pd.DataFrame({
                'Open': prices * 0.99,
                'High': prices * 1.01,
                'Low': prices * 0.98,
                'Close': prices,
                'Volume': np.random.randint(1000, 10000, 100)
            }, index=dates)
            
            # Teknik indikatörler testi
            indicators = analyzer.calculate_technical_indicators(stock_data)
            print(f"     ✅ Teknik indikatörler: {len(indicators)} adet")
            
            # Gann analizi testi
            gann_result = analyzer.calculate_gann_analysis(stock_data)
            print(f"     ✅ Gann analizi: {gann_result.get('gann_score', 'N/A')}")
            
            print(f"     ✅ {symbol} başarıyla analiz edildi")
            
        except Exception as e:
            print(f"     ❌ {symbol} hata: {str(e)[:50]}...")
    
    print(f"\n✅ Düzeltme testleri tamamlandı!")
    
except Exception as e:
    print(f"❌ Ana hata: {e}")
    import traceback
    traceback.print_exc()