"""
Ultra Options Analysis Test Modülü
Gelişmiş opsiyon analiz sistemi test dosyası

Bu test modülü Ultra Options Analysis'in tüm özelliklerini
kapsamlı olarak test eder ve Türkçe çıktılar sağlar.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Proje kök dizinini path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.analysis.ultra_options import UltraOptionsAnalyzer
    from src.analysis.options_analysis import OptionsAnalyzer
    MODULES_AVAILABLE = True
    print("✓ Ultra Options Analysis modülleri başarıyla yüklendi")
except ImportError as e:
    MODULES_AVAILABLE = False
    print(f"⚠ Modül yükleme hatası: {e}")

def create_sample_stock_data():
    """Test için örnek hisse senedi verisi oluştur"""
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    
    # Rastgele fiyat verileri (geometrik Brownian motion)
    np.random.seed(42)
    price = 100.0
    prices = [price]
    
    for _ in range(len(dates)-1):
        price *= np.exp(np.random.normal(0.0005, 0.02))  # Daily return with drift
        prices.append(price)
    
    df = pd.DataFrame({
        'Date': dates,
        'Open': np.array(prices) * (1 + np.random.normal(0, 0.01, len(prices))),
        'High': np.array(prices) * (1 + abs(np.random.normal(0, 0.02, len(prices)))),
        'Low': np.array(prices) * (1 - abs(np.random.normal(0, 0.02, len(prices)))),
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, len(prices))
    })
    
    return df

def test_ultra_options_analyzer():
    """Ultra Options Analyzer'ı test et"""
    print("\n" + "="*60)
    print("🔥 ULTRA OPTIONS ANALYSIS TESTİ")
    print("="*60)
    
    try:
        analyzer = UltraOptionsAnalyzer()
        
        # Test parametreleri
        symbol = "THYAO"
        spot_price = 125.50
        strike_price = 120.00
        time_to_expiry = 0.25  # 3 ay
        volatility = 0.28
        option_type = "call"
        
        print(f"\n📊 Test Parametreleri:")
        print(f"   Hisse: {symbol}")
        print(f"   Spot Fiyat: ${spot_price}")
        print(f"   Strike Fiyat: ${strike_price}")
        print(f"   Vade: {time_to_expiry*365:.0f} gün")
        print(f"   Volatilite: %{volatility*100:.1f}")
        print(f"   Opsiyon Tipi: {option_type.title()}")
        
        # Ana opsiyon analizi
        print(f"\n🎯 {symbol} Call Opsiyon Analizi:")
        result = analyzer.analyze_option(
            symbol=symbol,
            spot_price=spot_price,
            strike_price=strike_price,
            time_to_expiry=time_to_expiry,
            volatility=volatility,
            option_type=option_type
        )
        
        print(f"   Ultra Opsiyon Skoru: {result['ultra_option_score']}")
        print(f"   Analiz: {result['analysis']}")
        
        # Black-Scholes sonuçları
        bs = result['black_scholes']
        print(f"\n💰 Black-Scholes Fiyatlandırması:")
        print(f"   Teorik Değer: ${bs['fair_value']}")
        print(f"   Delta (Δ): {bs['delta']:.4f}")
        print(f"   Gamma (Γ): {bs['gamma']:.4f}")
        print(f"   Theta (Θ): ${bs['theta']:.4f}/gün")
        print(f"   Vega (υ): {bs['vega']:.4f}")
        print(f"   Rho (ρ): {bs['rho']:.4f}")
        
        # Greeks analizi
        greeks = result['greeks_analysis']
        print(f"\n🔢 Greeks Analizi:")
        print(f"   Greeks Skoru: {greeks['score']}")
        print(f"   Delta Yorumu: {greeks['delta_interpretation']}")
        print(f"   Gamma Riski: {greeks['gamma_risk']}")
        print(f"   Theta Kaybı: {greeks['theta_decay']}")
        print(f"   Vega Hassasiyeti: {greeks['vega_sensitivity']}")
        
        # Volatilite yüzeyi
        vol_surface = result['volatility_surface']
        print(f"\n📈 Volatilite Yüzeyi:")
        print(f"   İmplied Vol: %{vol_surface['implied_vol']*100:.2f}")
        print(f"   Skew: {vol_surface['skew']:.4f}")
        print(f"   Term Structure: {vol_surface['term_structure']}")
        
        # Zaman değeri analizi
        time_decay = result['time_decay_analysis']
        print(f"\n⏰ Zaman Değeri Analizi:")
        print(f"   Günlük Theta: ${time_decay['daily_theta']:.4f}")
        print(f"   Theta İvmesi: {time_decay['theta_acceleration']}")
        print(f"   Kalan Zaman Değeri: ${time_decay['time_value_remaining']:.2f}")
        
        # Moneyness analizi
        moneyness = result['moneyness_analysis']
        print(f"\n🎯 Moneyness Analizi:")
        print(f"   Moneyness Oranı: {moneyness['moneyness_ratio']:.4f}")
        print(f"   Sınıflandırma: {moneyness['classification']}")
        print(f"   İçsel Değer: ${moneyness['intrinsic_value']:.2f}")
        print(f"   Zaman Değeri: ${moneyness['time_value']:.2f}")
        
        # Risk profili
        risk = result['risk_profile']
        print(f"\n⚠️ Risk Profili:")
        print(f"   Genel Risk: {risk['overall_risk']}")
        print(f"   Yönsel Risk: {risk['directional_risk']}")
        print(f"   Volatilite Riski: {risk['volatility_risk']}")
        print(f"   Zaman Riski: {risk['time_risk']}")
        
        print(f"\n✅ Ultra Options Analysis başarıyla tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ Ultra Options Analysis test hatası: {e}")
        return False

def test_exotic_options():
    """Egzotik opsiyon testleri"""
    print("\n" + "="*60)
    print("🌟 EGZOTİK OPSİYON TESTLERİ")
    print("="*60)
    
    try:
        analyzer = UltraOptionsAnalyzer()
        
        # Asian Option Test
        print(f"\n🏯 Asian Option Testi:")
        asian_params = {
            'strike': 100,
            'time_to_expiry': 0.25,
            'volatility': 0.3,
            'option_type': 'call'
        }
        
        asian_result = analyzer.analyze_exotic_option('asian', 105, asian_params)
        print(f"   Opsiyon Tipi: {asian_result.option_type}")
        print(f"   Fair Value: ${asian_result.fair_value:.2f}")
        print(f"   Monte Carlo Güven: %{asian_result.monte_carlo_confidence:.1f}")
        print(f"   Risk Parametreleri: {asian_result.risk_parameters}")
        
        # Barrier Option Test  
        print(f"\n🚧 Barrier Option Testi:")
        barrier_params = {
            'strike': 100,
            'barrier': 110,
            'time_to_expiry': 0.25,
            'volatility': 0.3,
            'barrier_type': 'up_and_out'
        }
        
        barrier_result = analyzer.analyze_exotic_option('barrier', 105, barrier_params)
        print(f"   Opsiyon Tipi: {barrier_result.option_type}")
        print(f"   Fair Value: ${barrier_result.fair_value:.2f}")
        print(f"   Risk Parametreleri: {barrier_result.risk_parameters}")
        
        # Digital Option Test
        print(f"\n💻 Digital Option Testi:")
        digital_params = {
            'strike': 100,
            'time_to_expiry': 0.25,
            'volatility': 0.3,
            'payout': 100,
            'option_type': 'call'
        }
        
        digital_result = analyzer.analyze_exotic_option('digital', 105, digital_params)
        print(f"   Opsiyon Tipi: {digital_result.option_type}")
        print(f"   Fair Value: ${digital_result.fair_value:.2f}")
        print(f"   Risk Parametreleri: {digital_result.risk_parameters}")
        
        print(f"\n✅ Egzotik opsiyon testleri tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ Egzotik opsiyon test hatası: {e}")
        return False

def test_option_strategies():
    """Opsiyon stratejileri testleri"""
    print("\n" + "="*60)
    print("📋 OPSİYON STRATEJİLERİ TESTLERİ")
    print("="*60)
    
    try:
        analyzer = UltraOptionsAnalyzer()
        
        # Straddle Strategy
        print(f"\n🎯 Long Straddle Stratejisi:")
        straddle = analyzer._analyze_straddle(100, time_to_expiry=0.25, volatility=0.3)
        print(f"   Strateji: {straddle.strategy_name}")
        print(f"   Max Kar: {straddle.max_profit}")
        print(f"   Max Zarar: ${straddle.max_loss:.2f}")
        print(f"   Breakeven Noktaları: {[f'${bp:.2f}' for bp in straddle.breakeven_points]}")
        print(f"   Kar Olasılığı: %{straddle.probability_of_profit*100:.1f}")
        print(f"   Pozisyonlar: {len(straddle.legs)} adet")
        
        # Custom Strategy Test
        print(f"\n🛠️ Özel Strateji Testi:")
        custom_legs = [
            {'type': 'call', 'strike': 100, 'position': 'long', 'quantity': 1},
            {'type': 'call', 'strike': 110, 'position': 'short', 'quantity': 1}
        ]
        
        custom_strategy = analyzer._analyze_custom_strategy(
            'Bull Call Spread', 105, custom_legs
        )
        print(f"   Strateji: {custom_strategy.strategy_name}")
        print(f"   Max Kar: ${custom_strategy.max_profit:.2f}")
        print(f"   Max Zarar: ${custom_strategy.max_loss:.2f}")
        print(f"   Risk-Ödül Oranı: {custom_strategy.risk_reward_ratio:.2f}")
        print(f"   Pozisyonlar: {len(custom_strategy.legs)} adet")
        
        print(f"\n✅ Opsiyon stratejileri testleri tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ Opsiyon stratejileri test hatası: {e}")
        return False

def test_implied_volatility():
    """İmplied volatility testi"""
    print("\n" + "="*60)
    print("📊 İMPLIED VOLATİLİTE TESTİ")
    print("="*60)
    
    try:
        analyzer = UltraOptionsAnalyzer()
        
        # IV hesaplama testi
        market_price = 8.50
        spot_price = 100
        strike_price = 100
        time_to_expiry = 0.25
        
        print(f"\n🔍 IV Hesaplama Parametreleri:")
        print(f"   Piyasa Fiyatı: ${market_price}")
        print(f"   Spot Fiyat: ${spot_price}")
        print(f"   Strike Fiyat: ${strike_price}")
        print(f"   Vade: {time_to_expiry*365:.0f} gün")
        
        implied_vol = analyzer.calculate_implied_volatility(
            market_price, spot_price, strike_price, time_to_expiry, 'call'
        )
        
        print(f"\n📈 Sonuçlar:")
        print(f"   Hesaplanan IV: %{implied_vol*100:.2f}")
        print(f"   IV Yıllık Bazda: %{implied_vol*100:.2f}")
        
        # Doğrulama testi - IV ile BS fiyatı hesapla
        bs_result = analyzer._calculate_black_scholes(
            spot_price, strike_price, time_to_expiry, implied_vol, 'call'
        )
        
        print(f"\n✅ Doğrulama:")
        print(f"   BS Fiyatı (Hesaplanan IV ile): ${bs_result.option_price:.2f}")
        print(f"   Hedef Piyasa Fiyatı: ${market_price:.2f}")
        print(f"   Fark: ${abs(bs_result.option_price - market_price):.4f}")
        
        print(f"\n✅ İmplied volatility testi tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ Implied volatility test hatası: {e}")
        return False

def test_options_analyzer_integration():
    """Options Analyzer entegrasyon testi"""
    print("\n" + "="*60)
    print("🔗 OPTIONS ANALYZER ENTEGRASYON TESTİ")
    print("="*60)
    
    try:
        analyzer = OptionsAnalyzer()
        
        # Test verileri
        symbol = "AKBNK"
        current_price = 42.50
        stock_data = create_sample_stock_data()
        
        print(f"\n🏦 Test Parametreleri:")
        print(f"   Hisse: {symbol}")
        print(f"   Mevcut Fiyat: ${current_price}")
        print(f"   Veri Noktaları: {len(stock_data)} gün")
        
        # Kapsamlı opsiyon analizi
        result = analyzer.analyze_options(
            symbol=symbol,
            current_price=current_price,
            options_data=None,
            strike_price=current_price,
            time_to_expiry=0.2,  # 2.4 ay
            volatility=0.32
        )
        
        print(f"\n📊 Analiz Sonuçları:")
        print(f"   Options Skoru: {result['options_score']}")
        print(f"   Analiz Özeti: {result['analysis_summary']}")
        print(f"   Güven Seviyesi: %{result['confidence']}")
        
        if 'main_option' in result:
            main = result['main_option']
            print(f"\n🎯 Ana Opsiyon:")
            print(f"   Ultra Skor: {main.get('ultra_option_score', 'N/A')}")
            print(f"   Fair Value: ${main.get('black_scholes', {}).get('fair_value', 'N/A')}")
        
        if 'volatility_environment' in result:
            vol_env = result['volatility_environment']
            print(f"\n📈 Volatilite Ortamı:")
            print(f"   Rejim: {vol_env.get('volatility_regime', 'N/A')}")
            print(f"   Skor: {vol_env.get('volatility_score', 'N/A')}")
            print(f"   Görünüm: {vol_env.get('market_outlook', 'N/A')}")
        
        if 'strategy_recommendations' in result:
            strategies = result['strategy_recommendations']
            print(f"\n📋 Strateji Önerileri ({len(strategies)} adet):")
            for i, strategy in enumerate(strategies[:3], 1):
                print(f"   {i}. {strategy.get('strategy', 'N/A')}")
                print(f"      Risk: {strategy.get('risk_level', 'N/A')}")
                print(f"      Açıklama: {strategy.get('description', 'N/A')}")
        
        if 'risk_management' in result:
            risk_mgmt = result['risk_management']
            hedging = risk_mgmt.get('hedging_recommendations', [])
            print(f"\n⚠️ Risk Yönetimi ({len(hedging)} öneri):")
            for rec in hedging[:2]:
                print(f"   • {rec.get('type', 'N/A')}: {rec.get('action', 'N/A')}")
                print(f"     Öncelik: {rec.get('priority', 'N/A')}")
        
        print(f"\n✅ Options Analyzer entegrasyon testi tamamlandı!")
        return True
        
    except Exception as e:
        print(f"❌ Options Analyzer entegrasyon test hatası: {e}")
        return False

def run_comprehensive_options_tests():
    """Kapsamlı opsiyon analiz testlerini çalıştır"""
    print("🚀 ULTRA OPTIONS ANALYSIS - KAPSAMLI TEST SÜİTİ")
    print("="*60)
    print(f"📅 Test Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python Sürümü: {sys.version.split()[0]}")
    print(f"📊 NumPy Sürümü: {np.__version__}")
    print(f"🐼 Pandas Sürümü: {pd.__version__}")
    
    if not MODULES_AVAILABLE:
        print("❌ Gerekli modüller yüklenemedi, testler durduruluyor.")
        return False
    
    test_results = []
    
    # Test 1: Ultra Options Analyzer
    test_results.append(test_ultra_options_analyzer())
    
    # Test 2: Egzotik Opsiyonlar
    test_results.append(test_exotic_options())
    
    # Test 3: Opsiyon Stratejileri
    test_results.append(test_option_strategies())
    
    # Test 4: Implied Volatility
    test_results.append(test_implied_volatility())
    
    # Test 5: Entegrasyon Testi
    test_results.append(test_options_analyzer_integration())
    
    # Sonuç özeti
    print("\n" + "="*60)
    print("📋 TEST SONUÇLARI ÖZETİ")
    print("="*60)
    
    test_names = [
        "Ultra Options Analyzer",
        "Egzotik Opsiyonlar", 
        "Opsiyon Stratejileri",
        "Implied Volatility",
        "Entegrasyon Testi"
    ]
    
    passed = sum(test_results)
    total = len(test_results)
    
    for i, (name, result) in enumerate(zip(test_names, test_results), 1):
        status = "✅ BAŞARILI" if result else "❌ BAŞARISIZ"
        print(f"{i}. {name}: {status}")
    
    print(f"\n📊 Genel Sonuç: {passed}/{total} test başarılı")
    print(f"🎯 Başarı Oranı: %{(passed/total)*100:.1f}")
    
    if passed == total:
        print("\n🎉 TÜM TESTLER BAŞARILI! Ultra Options Analysis tam operasyonel.")
    else:
        print(f"\n⚠️ {total-passed} test başarısız oldu. Lütfen hataları kontrol edin.")
    
    print("\n🔥 Ultra Options Analysis test süreci tamamlandı!")
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_options_tests()
    sys.exit(0 if success else 1)