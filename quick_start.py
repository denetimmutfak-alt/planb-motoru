#!/usr/bin/env python3
"""
Hızlı analiz başlat
"""
from src.core.analysis_engine import PlanBAnalysisEngine

def main():
    try:
        print("🚀 Hızlı analiz başlatılıyor...")
        
        engine = PlanBAnalysisEngine()
        
        # Sadece 5 popüler sembol ile test
        test_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "META"]
        print(f"Test sembolleri: {test_symbols}")
        
        results = engine.analyze_multiple_symbols(test_symbols, max_workers=5)
        
        print(f"✅ Analiz tamamlandı: {len(results)} sonuç")
        
        if results:
            print("\nSonuçlar:")
            for i, result in enumerate(results):
                print(f"{i+1}. {result['symbol']}: {result['total_score']:.2f} puan - {result['signal']}")
        
        # Veritabanını kontrol et
        import sqlite3
        conn = sqlite3.connect('data/planb_motoru.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM analizler')
        count = cursor.fetchone()[0]
        print(f"\nVeritabanında {count} kayıt var")
        conn.close()
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

