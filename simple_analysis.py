#!/usr/bin/env python3
"""
Basit analiz test
"""
print("Analiz test başlıyor...")

try:
    from src.core.analysis_engine import PlanBAnalysisEngine
    print("✅ Import başarılı")
    
    engine = PlanBAnalysisEngine()
    print("✅ Engine oluşturuldu")
    
    # Tek sembol analizi
    print("AAPL analizi başlatılıyor...")
    result = engine.analyze_single_symbol("AAPL")
    
    if result:
        print(f"✅ Analiz tamamlandı: {result['symbol']} - {result['total_score']:.2f} puan")
        print(f"Result keys: {list(result.keys())}")
        
        # Veritabanını kontrol et
        import sqlite3
        conn = sqlite3.connect('data/planb_motoru.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM analizler')
        count = cursor.fetchone()[0]
        print(f"Veritabanında {count} kayıt var")
        conn.close()
    else:
        print("❌ Analiz başarısız")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()
