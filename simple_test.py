#!/usr/bin/env python3
"""
Basit test
"""
print("Test başlıyor...")

try:
    print("Import ediliyor...")
    from src.core.analysis_engine import PlanBAnalysisEngine
    print("✅ Import başarılı")
    
    print("Engine oluşturuluyor...")
    engine = PlanBAnalysisEngine()
    print("✅ Engine oluşturuldu")
    
    print("Test tamamlandı!")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()

