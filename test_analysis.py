#!/usr/bin/env python3
"""
Test analizi çalıştır
"""
from src.core.analysis_engine import PlanBAnalysisEngine

def main():
    try:
        print("PlanB Motoru - Test Analizi Başlatılıyor...")
        
        # Analysis engine'i başlat
        print("Analysis engine başlatılıyor...")
        engine = PlanBAnalysisEngine()
        print("✅ Analysis engine başlatıldı")
        
        # Test modunda analiz çalıştır
        print("Test modunda analiz çalıştırılıyor...")
        # Sadece bir sembol ile test et
        test_symbols = ["AAPL"]
        print(f"Test sembolleri: {test_symbols}")
        
        results = engine.analyze_multiple_symbols(test_symbols, max_workers=1)
        
        print(f"✅ Test analizi tamamlandı: {len(results)} sonuç")
        
        if results:
            print("\nSonuçlar:")
            for i, result in enumerate(results):
                print(f"{i+1}. {result['symbol']}: {result['total_score']:.2f} puan - {result['signal']}")
        else:
            print("❌ Hiç sonuç dönmedi")
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
