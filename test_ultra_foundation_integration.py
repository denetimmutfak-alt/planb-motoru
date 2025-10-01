#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultra Astroloji Modülü - Kuruluş Tarihi Entegrasyonu Test
"""

import sys
import os

# Foundation date integration'ı import et
sys.path.append('data/foundation_dates')

try:
    from ultra_module_integration import foundation_integration
    
    print("🔮 ULTRA ASTROLOJİ MODÜLÜ - KURULUŞ TARİHİ ENTEGRASYOnu TEST")
    print("=" * 70)
    
    # Test sembolleri
    test_symbols = [
        "AAPL.US",  # Apple (if exists)
        "ISATR.IS", # İş Bankası (oldest BIST)
        "BTC-USD",  # Bitcoin
        "AKBNK.IS", # Akbank
        "ETH-USD"   # Ethereum
    ]
    
    for symbol in test_symbols:
        print(f"\n🎯 {symbol} ANALİZİ:")
        print("-" * 40)
        
        # Temel bilgiler
        foundation_date = foundation_integration.get_foundation_date(symbol)
        age = foundation_integration.get_company_age(symbol)
        market_type = foundation_integration.get_market_type(symbol)
        
        if foundation_date:
            print(f"📅 Kuruluş Tarihi: {foundation_date}")
            print(f"⏳ Yaş: {age} yıl")
            print(f"🏪 Market: {market_type}")
            
            # Astroloji faktörleri
            astro_factors = foundation_integration.get_astrology_factors(symbol)
            if astro_factors:
                print(f"🪐 Jüpiter Döngüsü: {astro_factors['jupiter_cycle_position']:.3f}")
                print(f"🪐 Satürn Döngüsü: {astro_factors['saturn_cycle_position']:.3f}")
                print(f"📆 Yılın Günü: {astro_factors['foundation_day_of_year']}")
            
            # Shemitah pozisyonu
            shemitah = foundation_integration.get_shemitah_position(symbol)
            if shemitah:
                print(f"🔯 Shemitah Pozisyon: {shemitah['shemitah_cycle_position']:.3f}")
                print(f"🔯 Tamamlanan Döngü: {shemitah['cycles_completed']}")
            
            # Risk faktörleri
            risk_factors = foundation_integration.get_risk_factors(symbol)
            if risk_factors:
                print(f"⚠️ Yaş Risk Skoru: {risk_factors['age_risk_score']:.3f}")
                print(f"🛡️ Stabilite Skoru: {risk_factors['stability_score']:.3f}")
        else:
            print("❌ Kuruluş tarihi bulunamadı")
    
    print(f"\n📊 TOPLAM VERİ ÖZETİ:")
    print("=" * 40)
    print(f"💾 Yüklenen Toplam Veri: {len(foundation_integration.foundation_data)} şirket")
    
    # Market türü dağılımı
    market_distribution = {}
    for data in foundation_integration.foundation_data.values():
        market = data["market_type"]
        market_distribution[market] = market_distribution.get(market, 0) + 1
    
    for market, count in market_distribution.items():
        print(f"🏪 {market}: {count} şirket")
    
    print("\n✅ ULTRA MODÜL KURULUŞ TARİHİ ENTEGRASYOnu BAŞARILI!")
    
except ImportError as e:
    print(f"❌ Import hatası: {e}")
    print("Ultra modül entegrasyonu henüz oluşturulmamış olabilir.")

except Exception as e:
    print(f"❌ Test hatası: {e}")