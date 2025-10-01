#!/usr/bin/env python3
"""
Kapsamlı Skorlama Sistemi Test Dosyası
"""

from src.analysis.financial_analysis import FinancialAnalyzer
import pandas as pd
import numpy as np

def test_comprehensive_scoring():
    """Yeni kapsamlı skorlama sistemini test et"""
    
    # Test verileri oluştur
    test_data = pd.DataFrame({
        'Close': np.random.randn(30) + 100,
        'Volume': np.random.randint(1000, 10000, 30)
    })
    
    analyzer = FinancialAnalyzer()
    
    # Test parametreleri
    financial_score = 75
    technical_indicators = {'rsi': 35}  # Aşırı satım bölgesi
    trend_analysis = {'strength': 80, 'trend': 'yukselen'}
    gann_analysis = 65
    
    print("🔥 Kapsamlı Skorlama Sistemi Testi")
    print("=" * 50)
    
    try:
        # Sinyal üret
        signal, total_score, detailed = analyzer.generate_signal(
            financial_score=financial_score,
            technical_indicators=technical_indicators, 
            trend_analysis=trend_analysis,
            gann_analysis=gann_analysis,
            symbol='THYAO',
            stock_data=test_data
        )
        
        print(f"✅ Test Başarılı!")
        print(f"📊 Sinyal: {signal}")
        print(f"🎯 Toplam Skor: {total_score:.2f}")
        print(f"🔢 Kullanılan Modül Sayısı: {len(detailed['scores'])}")
        print(f"⏱️ Tutma Süresi: {detailed['hold_days']} gün")
        
        print("\n📈 Modül Skorları:")
        print("-" * 30)
        for module, score in detailed['scores'].items():
            weight = detailed['weights'].get(module, 0)
            print(f"  {module:15}: {score:5.1f} (ağırlık: {weight:.2f})")
        
        print(f"\n💡 Sinyal Açıklaması: {detailed['signal_explanation']}")
        
        # Ağırlık kontrolü
        total_weight = sum(detailed['weights'].values())
        print(f"\n⚖️ Toplam Ağırlık: {total_weight:.2f}")
        
        if total_weight > 0.95:  # %95'ten fazla ise tamam
            print("✅ Ağırlık dağılımı doğru")
        else:
            print("⚠️ Ağırlık dağılımında eksiklik var")
            
    except Exception as e:
        print(f"❌ Test Hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comprehensive_scoring()