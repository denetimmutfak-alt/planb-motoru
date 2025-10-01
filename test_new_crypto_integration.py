#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yeni Kripto Verilerinin Ultra Modül Entegrasyonu Test
"""

import os
import sys
sys.path.append('data/foundation_dates')

from ultra_module_integration import foundation_integration

def test_new_crypto_data():
    """Yeni kripto verilerini test et"""
    print("🔮 YENİ KRİPTO VERİLERİ ULTRA MODÜL ENTEGRASYOnu TEST")
    print("=" * 70)
    
    # Test edilecek yeni kripto paralar
    new_cryptos = [
        "BTC",    # En eski kripto
        "JUP",    # En yeni kripto (2024)
        "SOL",    # Popüler kripto
        "DOGE",   # Meme coin
        "XRP",    # Ripple
        "BNB",    # Binance
        "PYTH",   # Pyth Network (2023)
        "SEI",    # Sei (2023)
        "SUI"     # Sui (2023)
    ]
    
    for symbol in new_cryptos:
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
            astro = foundation_integration.get_astrology_factors(symbol)
            if astro:
                print(f"🪐 Jüpiter Döngüsü: {astro['jupiter_cycle_position']:.3f}")
                print(f"🪐 Satürn Döngüsü: {astro['saturn_cycle_position']:.3f}")
                print(f"📆 Yılın Günü: {astro['foundation_day_of_year']}")
            
            # Shemitah pozisyonu
            shemitah = foundation_integration.get_shemitah_position(symbol)
            if shemitah:
                print(f"🔯 Shemitah Pozisyon: {shemitah['shemitah_cycle_position']:.3f}")
                print(f"🔯 Tamamlanan Döngü: {shemitah['cycles_completed']}")
            
            # Risk faktörleri
            risk = foundation_integration.get_risk_factors(symbol)
            if risk:
                print(f"⚠️ Yaş Risk Skoru: {risk['age_risk_score']:.3f}")
                print(f"🛡️ Stabilite Skoru: {risk['stability_score']:.3f}")
                
        else:
            print("❌ Kuruluş tarihi bulunamadı")
    
    # Toplam veri özeti
    print(f"\n📊 TOPLAM VERİ ÖZETİ:")
    print("=" * 40)
    print(f"💾 Yüklenen Toplam Veri: {len(foundation_integration.foundation_data)} şirket")
    
    # Market türü sayımı
    market_counts = {}
    for data in foundation_integration.foundation_data.values():
        market = data.get("market_type", "UNKNOWN")
        market_counts[market] = market_counts.get(market, 0) + 1
    
    for market, count in market_counts.items():
        print(f"🏪 {market}: {count} şirket")
    
    print("\n✅ YENİ KRİPTO VERİLERİ ULTRA MODÜL ENTEGRASYOnu BAŞARILI!")

if __name__ == "__main__":
    test_new_crypto_data()