#!/usr/bin/env python3
"""
Ultra Astrology Analysis Test
"""

from src.analysis.astrology_analysis import get_astrology_score

def test_ultra_astrology():
    """Ultra astrology test"""
    
    print("🔮 Ultra Astrology Analysis Testi")
    print("=" * 50)
    
    try:
        # Test symbolleri
        symbols = ['THYAO', 'AKBNK', 'EREGL', 'BIMAS', 'TCELL']
        
        for symbol in symbols:
            score = get_astrology_score(symbol)
            print(f"🌟 {symbol}: Astroloji Skoru = {score:.2f}")
        
        print("\n✅ Ultra Astrology Analysis başarıyla çalışıyor!")
        
    except Exception as e:
        print(f"❌ Test Hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ultra_astrology()