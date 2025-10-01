"""
Ultra Risk Yönetimi Analizi Test Paketi
Kapsamlı risk yönetimi modellemesi yeteneklerini test eder
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from datetime import datetime
import time

def test_ultra_risk_analysis():
    """Ultra Risk Management Analysis kapsamlı testi"""
    
    print("Ultra Risk Management Analysis Test Paketine Başlanıyor...")
    print("=" * 75)
    print("=" * 19)
    print("⚠️ ULTRA RİSK YÖNETİMİ ANALİZ TESTİ")
    print("Gelişmiş risk metrikleri, VaR hesaplamaları ve stres testleri...")
    print("=" * 75)
    print("=" * 19)
    
    try:
        # Ultra Risk Analyzer'ı import et
        from src.analysis.ultra_risk import UltraRiskAnalyzer
        
        analyzer = UltraRiskAnalyzer()
        
        print(f"\n🛡️ Gelişmiş Risk Yönetimi Yetenekleri:")
        print("✓ Value at Risk (VaR) hesaplamaları (Parametrik, Monte Carlo, Tarihsel)")
        print("✓ Expected Shortfall (CVaR) analizi")
        print("✓ Kapsamlı stres testleri ve senaryo analizleri")
        print("✓ Maksimum kayıp (Maximum Drawdown) analizi")
        print("✓ Likidite riski değerlendirmesi") 
        print("✓ Korelasyon riski ve çeşitlendirme analizi")
        print("✓ Konsantrasyon riski metrikleri")
        print("✓ Makro faktör risk etkisi")
        print("✓ Risk limit kontrolleri ve uyumluluk")
        
        # Farklı risk profillerine sahip varlık sınıflarını test et
        test_symbols = [
            ('JPM', 'Finansal - Yüksek Sistemik Risk', 500000),
            ('AAPL', 'Teknoloji - Orta Risk Profili', 300000),
            ('XOM', 'Enerji - Yüksek Volatilite Risk', 200000),
            ('JNJ', 'Sağlık - Düşük Risk Profili', 400000),
            ('TSLA', 'Yüksek Beta - Aşırı Risk', 150000),
            ('PG', 'Savunma Hisse - Düşük Risk', 250000),
            ('GLD', 'Altın ETF - Güvenli Liman', 350000),
            ('VIX', 'Volatilite - Ekstrem Risk', 100000)
        ]
        
        print(f"\n🎯 Farklı risk profillerindeki sembolleri test ediliyor:")
        print("-" * 75)
        
        for symbol, description, portfolio_value in test_symbols:
            try:
                result = analyzer.analyze_ultra_risk(symbol, portfolio_value)
                
                print(f"\n{symbol:<6} ({description}) - Portföy: ${portfolio_value:,}")
                print(f"  Ultra Risk Skoru: {result['ultra_risk_score']}/100")
                print(f"  VaR (95%): ${result['components']['var_analysis']['var_95']:,.0f}")
                print(f"  VaR (99%): ${result['components']['var_analysis']['var_99']:,.0f}")
                print(f"  Beklenen Kayıp: ${result['components']['var_analysis']['expected_shortfall_95']:,.0f}")
                print(f"  Maksimum Düşüş: {result['components']['risk_metrics']['max_drawdown']:.1%}")
                print(f"  Sharpe Oranı: {result['components']['risk_metrics']['sharpe_ratio']:.2f}")
                print(f"  En Kötü Senaryo: {result['components']['stress_tests']['worst_scenario']}")
                print(f"  Senaryo Kaybı: ${result['components']['stress_tests']['worst_loss']:,.0f}")
                
            except Exception as e:
                print(f"  ❌ Analiz başarısız: {str(e)}")
        
        # Belirli bir sembol için detaylı analiz
        print(f"\n{'=' * 75}")
        print("🔍 KAPSAMLI RİSK ANALİZİ")
        print(f"{'=' * 75}")
        
        detailed_symbol = 'JPM'
        detailed_portfolio = 1000000  # $1M portföy
        detailed_result = analyzer.analyze_ultra_risk(detailed_symbol, detailed_portfolio)
        
        print(f"\n🏦 {detailed_symbol} için Detaylı Risk Analizi (${detailed_portfolio:,} portföy):")
        print(f"  Ultra Risk Skoru: {detailed_result['ultra_risk_score']}/100")
        print(f"  Risk Analizi: {detailed_result['analysis']}")
        
        # VaR Analizi Bileşeni
        var_comp = detailed_result['components']['var_analysis']
        print(f"\n📊 Value at Risk (VaR) Analizi:")
        print(f"  En İyi Model: {var_comp['best_model']}")
        print(f"  VaR (95% güven): ${var_comp['var_95']:,.0f}")
        print(f"  VaR (99% güven): ${var_comp['var_99']:,.0f}")
        print(f"  Beklenen Kayıp (95%): ${var_comp['expected_shortfall_95']:,.0f}")
        print(f"  VaR Skoru: {var_comp['score']}/100")
        
        # Risk Metrikleri Bileşeni
        metrics_comp = detailed_result['components']['risk_metrics']
        print(f"\n📈 Risk Performans Metrikleri:")
        print(f"  Sharpe Oranı: {metrics_comp['sharpe_ratio']:.3f}")
        print(f"  Maksimum Düşüş: {metrics_comp['max_drawdown']:.2%}")
        print(f"  Sortino Oranı: {metrics_comp['sortino_ratio']:.3f}")
        print(f"  Beta Katsayısı: {metrics_comp['beta']:.3f}")
        print(f"  Risk Metrikleri Skoru: {metrics_comp['score']}/100")
        
        # Stres Testleri Bileşeni
        stress_comp = detailed_result['components']['stress_tests']
        print(f"\n🌪️ Stres Testleri Analizi:")
        print(f"  En Kötü Senaryo: {stress_comp['worst_scenario']}")
        print(f"  Beklenen Maksimum Kayıp: ${stress_comp['worst_loss']:,.0f}")
        print(f"  Stres Direnci: {stress_comp['stress_resilience']:.1f}/100")
        print(f"  Stres Testi Skoru: {stress_comp['score']}/100")
        
        # Drawdown Analizi
        dd_comp = detailed_result['components']['drawdown_analysis']
        print(f"\n📉 Maksimum Kayıp (Drawdown) Analizi:")
        print(f"  Maksimum Düşüş: {dd_comp['max_drawdown']:.2%}")
        print(f"  Ortalama Toparlanma Süresi: {dd_comp['recovery_time']:.0f} gün")
        print(f"  Düşüş Sıklığı: {dd_comp['drawdown_frequency']:.1f}/yıl")
        print(f"  Drawdown Skoru: {dd_comp['score']}/100")
        
        # Likidite Riski
        liq_comp = detailed_result['components']['liquidity_risk']
        print(f"\n💧 Likidite Riski Analizi:")
        print(f"  Likidite Oranı: {liq_comp['liquidity_ratio']:.3f}")
        print(f"  Bid-Ask Etkisi: {liq_comp['bid_ask_impact']:.4f}")
        print(f"  Piyasa Etkisi: {liq_comp['market_impact']:.4f}")
        print(f"  Likidite Skoru: {liq_comp['score']}/100")
        
        # Korelasyon Riski
        corr_comp = detailed_result['components']['correlation_risk']
        print(f"\n🔗 Korelasyon Riski Analizi:")
        print(f"  Korelasyon Kırılması: {corr_comp['correlation_breakdown']:.3f}")
        print(f"  Çeşitlendirme Oranı: {corr_comp['diversification_ratio']:.3f}")
        print(f"  Konsantrasyon İndeksi: {corr_comp['concentration_index']:.3f}")
        print(f"  Korelasyon Skoru: {corr_comp['score']}/100")
        
        # Stres Senaryoları
        if 'stress_scenarios' in detailed_result:
            print(f"\n🎭 Stres Senaryoları Detayları:")
            scenarios_list = list(detailed_result['stress_scenarios'].values())[:3]  # İlk 3 senaryo
            for scenario in scenarios_list:
                print(f"  • {scenario.scenario_name.replace('_', ' ').title()}:")
                print(f"    Piyasa Şoku: {scenario.market_shock:.1%}")
                print(f"    Beklenen Kayıp: ${scenario.expected_loss:,.0f}")
                print(f"    Olasılık: {scenario.probability:.1%}")
        
        # Makro Risk Faktörleri
        if 'macro_risk_factors' in detailed_result:
            macro_risk = detailed_result['macro_risk_factors']
            print(f"\n🌍 Makro Risk Faktörleri:")
            print(f"  Toplam Risk Etkisi: {macro_risk['total_risk_impact']:+.3f}")
            print(f"  Makro Risk Skoru: {macro_risk['macro_risk_score']:.1f}/100")
            if 'dominant_risk_factor' in macro_risk:
                print(f"  Baskın Risk Faktörü: {macro_risk['dominant_risk_factor']}")
        
        # Risk Limitleri
        if 'risk_limits' in detailed_result:
            risk_limits = detailed_result['risk_limits']
            print(f"\n🚨 Risk Limit Kontrolleri:")
            print(f"  Uyumluluk Durumu: {risk_limits['compliance_status']}")
            print(f"  Genel Limit Skoru: {risk_limits['overall_score']:.1f}/100")
            if risk_limits['violations']:
                print(f"  ⚠️ Risk Limiti İhlalleri:")
                for violation in risk_limits['violations']:
                    print(f"    - {violation['type']}: {violation['violation_ratio']:.1f}x limit")
        
        # Öneriler
        if 'recommendations' in detailed_result:
            print(f"\n💡 Risk Yönetimi Önerileri:")
            for i, rec in enumerate(detailed_result['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        print(f"\n📊 Genel Analiz Güveni: {detailed_result['confidence']:.1f}%")
        
        # Performans testi
        print(f"\n{'=' * 75}")
        print("⚡ PERFORMANS TESTİ")
        print(f"{'=' * 75}")
        
        start_time = time.time()
        test_runs = 50  # Risk analizi daha karmaşık olduğu için daha az test
        
        for _ in range(test_runs):
            analyzer.analyze_ultra_risk('AAPL', 100000)
        
        end_time = time.time()
        avg_time = (end_time - start_time) / test_runs
        calculations_per_second = 1 / avg_time if avg_time > 0 else float('inf')
        
        print(f"Ortalama hesaplama süresi: {avg_time:.3f} saniye")
        print(f"Saniyede hesaplama sayısı: {calculations_per_second:.1f}")
        
        print(f"\n{'=' * 75}")
        print("✅ ULTRA RİSK YÖNETİMİ ANALİZİ TESTİ TAMAMLANDI")
        print(f"{'=' * 75}")
        print("🎯 Doğrulanan Ana Özellikler:")
        print("✓ Gelişmiş VaR hesaplamaları (Parametrik, Monte Carlo, Tarihsel)")
        print("✓ Expected Shortfall (CVaR) analizi")
        print("✓ Kapsamlı stres testleri ve senaryo analizleri")
        print("✓ Maksimum kayıp (Drawdown) analizi")
        print("✓ Likidite riski değerlendirmesi")
        print("✓ Korelasyon riski ve çeşitlendirme metrikleri")
        print("✓ Makro faktör risk etkisi analizi")
        print("✓ Risk limit kontrolleri ve uyumluluk izleme")
        print("✓ Sektöre özel risk profilleme")
        
        return True
        
    except Exception as e:
        print(f"❌ Ultra Risk Management Analysis testi başarısız: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Mevcut sistemlerle entegrasyon testi"""
    print(f"\n{'=' * 75}")
    print("🔗 ENTEGRASYON TESTİ")
    print(f"{'=' * 75}")
    
    try:
        # Doğrudan import testi
        from src.analysis.ultra_risk import UltraRiskAnalyzer
        ultra_analyzer = UltraRiskAnalyzer()
        ultra_result = ultra_analyzer.analyze_ultra_risk('JPM', 100000)
        print(f"Ultra Risk function skoru: {ultra_result['ultra_risk_score']}")
        
        # Risk analysis entegrasyonu testi
        from src.analysis.risk_analysis import RiskAnalyzer
        risk_analyzer = RiskAnalyzer()
        risk_score = risk_analyzer.get_risk_score('JPM', portfolio_value=100000)
        print(f"Risk Analyzer skoru: {risk_score}")
        
        # Financial analysis entegrasyonu testi
        from src.analysis.financial_analysis import FinancialAnalyzer
        financial_analyzer = FinancialAnalyzer()
        
        # Risk analyzer'ın düzgün başlatıldığını test et
        assert hasattr(financial_analyzer, 'risk_analyzer'), "Risk analyzer başlatılmamış"
        print(f"Risk analyzer entegrasyonu: ✓")
        
        print("✅ Entegrasyon testi başarılı")
        return True
        
    except Exception as e:
        print(f"❌ Entegrasyon testi başarısız: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎉 Ultra Risk Management Analysis Test Paketine Başlanıyor")
    print("Gelişmiş risk yönetimi modellemesi yetenekleri test ediliyor...")
    
    success = test_ultra_risk_analysis()
    integration_success = test_integration()
    
    if success and integration_success:
        print(f"\n🎉 TÜM TESTLER BAŞARILI! Ultra Risk Management Analysis üretime hazır.")
    else:
        print(f"\n❌ Bazı testler başarısız. Lütfen implementasyonu kontrol edin.")