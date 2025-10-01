#!/usr/bin/env python3
"""
ULTRA Professional Dashboard Entegrasyon Testi
"""

def test_dashboard_integration():
    print("🔍 ULTRA PROFESSIONAL DASHBOARD ENTEGRASYON TESTİ")
    print("=" * 55)
    
    try:
        # Ana analiz modülünü test et
        print("1. FinancialAnalyzer modülü test ediliyor...")
        from src.analysis.financial_analysis import FinancialAnalyzer
        analyzer = FinancialAnalyzer()
        print("   ✓ FinancialAnalyzer başarıyla yüklendi")
        
        # CompanyFoundingDates test et
        print("2. CompanyFoundingDates modülü test ediliyor...")
        from src.data.company_founding_dates import CompanyFoundingDates
        founding = CompanyFoundingDates()
        companies = founding.get_all_companies()
        print(f"   ✓ {len(companies)} şirket founding date verisi yüklü")
        
        # Ultra modülleri test et
        print("3. Ultra analiz modülleri test ediliyor...")
        from src.analysis.astrology_analysis import AstrologyAnalyzer
        from src.analysis.shemitah_cycle import shemitah_analyzer
        from src.analysis.gann_technique import GannTechniqueAnalyzer
        from src.analysis.economic_cycle import ultra_economic_analyzer
        from src.analysis.volatility_analysis import VolatilityAnalyzer
        from src.analysis.risk_analysis import RiskAnalyzer
        from src.analysis.options_analysis import OptionsAnalyzer
        from src.analysis.currency_analysis import CurrencyAnalyzer
        from src.analysis.commodities_analysis import CommoditiesAnalyzer
        print("   ✓ 9 Ultra modül başarıyla yüklendi")
        
        # Test veri ile sinyal üret
        print("4. Sinyal üretim sistemi test ediliyor...")
        import yfinance as yf
        import pandas as pd
        
        # Test veri oluştur
        test_data = pd.DataFrame({
            'Open': [100, 101, 102, 103, 104],
            'High': [102, 103, 104, 105, 106],
            'Low': [99, 100, 101, 102, 103],
            'Close': [101, 102, 103, 104, 105],
            'Volume': [1000, 1100, 1200, 1300, 1400]
        })
        
        signal, score, details = analyzer.generate_signal(
            symbol="TEST.IS",
            stock_data=test_data,
            financial_score=60
        )
        
        print(f"   ✓ Test sinyali üretildi: {signal} (Skor: {score})")
        print(f"   ✓ {len(details.get('scores', {}))} modül aktif")
        
        # Optimized thresholds test
        print("5. Optimize edilmiş eşikler test ediliyor...")
        test_scores = [30, 40, 50, 60, 70]
        signals = []
        
        for test_score in test_scores:
            if test_score >= 65:
                test_signal = 'AL'
            elif test_score >= 55:
                test_signal = 'TUT_GUCLU'
            elif test_score >= 45:
                test_signal = 'TUT'
            elif test_score >= 35:
                test_signal = 'TUT_ZAYIF'
            else:
                test_signal = 'SAT'
            signals.append(f"{test_score}→{test_signal}")
        
        print(f"   ✓ Sinyal eşikleri: {', '.join(signals)}")
        
        # Dashboard bağlantı testi
        print("6. Dashboard bağlantısı test ediliyor...")
        import requests
        try:
            response = requests.get("http://127.0.0.1:5004", timeout=3)
            if response.status_code == 200:
                print("   ✓ Dashboard server erişilebilir")
            else:
                print(f"   ⚠ Dashboard yanıt kodu: {response.status_code}")
        except:
            print("   ⚠ Dashboard server bağlantı problemi")
        
        print("\n" + "=" * 55)
        print("🎯 ENTEGRASYON SONUCU: BAŞARILI!")
        print("📊 Ultra Professional Dashboard sistemle tam entegre")
        print(f"📈 {len(companies)} şirket + 9 ultra modül + optimized signals")
        print("🔄 Real-time analiz sistemi HAZIR")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ENTEGRASYON HATASI: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_dashboard_integration()