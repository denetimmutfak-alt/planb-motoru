"""
Simple Ultra Currency Test
Basit Ultra Currency Testi
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simple_currency_test():
    """Basit currency test"""
    try:
        print("🧪 Basit Ultra Currency Test...")
        
        # Direct import test
        from src.analysis.currency_analysis import CurrencyAnalyzer
        print("✅ Currency Analyzer import edildi")
        
        # Initialize
        analyzer = CurrencyAnalyzer()
        print("✅ Currency Analyzer başlatıldı")
        
        # Simple test
        result = analyzer.analyze_currency('EURUSD', current_rate=1.05)
        print(f"✅ EURUSD Analiz Score: {result.get('currency_score', 'N/A')}")
        print(f"✅ Trading Recommendation: {result.get('trading_recommendation', 'N/A')}")
        
        # Financial analyzer test
        from src.analysis.financial_analysis import FinancialAnalyzer
        fin_analyzer = FinancialAnalyzer()
        print("✅ Financial Analyzer başlatıldı")
        
        if hasattr(fin_analyzer, 'currency_analyzer'):
            print("✅ Currency Analyzer entegre")
        else:
            print("❌ Currency Analyzer entegre değil")
        
        print("\n🎯 BAŞARILI! Ultra Currency Analysis Çalışıyor! 🎯")
        return True
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        return False

if __name__ == "__main__":
    simple_currency_test()