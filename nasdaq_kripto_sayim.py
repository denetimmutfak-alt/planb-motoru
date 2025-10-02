#!/usr/bin/env python3
"""
NASDAQ ve KRİPTO Listelerini Doğru Sayılarla Güncelle
"""

def nasdaq_ve_kripto_sayim():
    print("🔍 NASDAQ VE KRİPTO LİSTELERİ GERÇEK SAYIM")
    print("="*50)
    
    # NASDAQ analizi
    with open("NASDAQ_TAM_LISTE_NEW.txt", "r", encoding="utf-8") as f:
        nasdaq_lines = f.readlines()
    
    nasdaq_data = [line.strip() for line in nasdaq_lines if line.strip() and not line.startswith('#')]
    
    print(f"📊 NASDAQ:")
    print(f"   Toplam satırlar: {len(nasdaq_lines)}")
    print(f"   Veri satırları: {len(nasdaq_data)}")
    
    # KRİPTO analizi  
    with open("KRIPTO_TAM_LISTE_NEW.txt", "r", encoding="utf-8") as f:
        kripto_lines = f.readlines()
    
    kripto_data = [line.strip() for line in kripto_lines if line.strip() and not line.startswith('#')]
    
    print(f"📊 KRİPTO:")
    print(f"   Toplam satırlar: {len(kripto_lines)}")
    print(f"   Veri satırları: {len(kripto_data)}")
    
    return len(nasdaq_data), len(kripto_data)

if __name__ == "__main__":
    nasdaq_count, kripto_count = nasdaq_ve_kripto_sayim()
    print(f"\n✅ SONUÇ:")
    print(f"   NASDAQ: {nasdaq_count} hisse")
    print(f"   KRİPTO: {kripto_count} kripto")