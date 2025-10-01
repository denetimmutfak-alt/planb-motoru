#!/usr/bin/env python3
"""
Hızlı test
"""
print("Test başlıyor...")

try:
    from src.core.analysis_engine import PlanBAnalysisEngine
    print("✅ Import başarılı")
    
    engine = PlanBAnalysisEngine()
    print("✅ Engine oluşturuldu")
    
    # Tek sembol analizi
    result = engine.analyze_single_symbol("AAPL")
    print(f"✅ Analiz tamamlandı: {result}")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()

