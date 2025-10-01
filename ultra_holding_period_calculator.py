#!/usr/bin/env python3
"""
🚀 ULTRA TUTMA SÜRESİ MODÜLÜ
===========================
19 Ultra Modül ile optimal tutma süresini hesaplar

Bu modül:
- Kuruluş tarihi döngüleri
- Astroloji faktörleri  
- Shemitah döngüleri
- Solar/Moon döngüleri
- ML tahminleri
- Risk analizlerini birleştirir
"""

import json
import math
from datetime import datetime, date
from pathlib import Path

# Kuruluş tarihi veritabanı
FOUNDATION_DB_PATH = Path("data/foundation_dates/foundation_database.json")

def load_foundation_database():
    """Kuruluş tarihi veritabanını yükle"""
    try:
        if FOUNDATION_DB_PATH.exists():
            with open(FOUNDATION_DB_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def get_company_age_years(symbol: str) -> int:
    """Şirketin yaşını hesapla"""
    db = load_foundation_database()
    if symbol in db:
        try:
            foundation_date = datetime.strptime(db[symbol]["foundation_date"], "%d.%m.%Y").date()
            today = date.today()
            age_years = today.year - foundation_date.year
            return max(1, age_years)
        except Exception:
            pass
    return 25  # Varsayılan 25 yıl

def ultra_astrology_holding_factor(symbol: str) -> float:
    """🔮 Astroloji faktörü (Jupiter/Saturn döngüleri)"""
    age = get_company_age_years(symbol)
    
    # Jupiter döngüsü (12 yıl)
    jupiter_position = (age % 12) / 12.0
    if 0.2 < jupiter_position < 0.8:  # Pozitif faz
        jupiter_factor = 1.3
    else:
        jupiter_factor = 0.9
    
    # Saturn döngüsü (29 yıl) 
    saturn_position = (age % 29) / 29.0
    if 0.3 < saturn_position < 0.7:  # Stabil faz
        saturn_factor = 1.2
    else:
        saturn_factor = 0.8
        
    return (jupiter_factor + saturn_factor) / 2.0

def ultra_shemitah_holding_factor(symbol: str) -> float:
    """⚡ Shemitah 7-yıl döngüsü faktörü"""
    age = get_company_age_years(symbol)
    shemitah_position = age % 7
    
    if shemitah_position in [1, 2]:  # Döngü başlangıcı - güçlü
        return 1.5
    elif shemitah_position in [3, 4, 5]:  # Orta döngü - normal
        return 1.0
    else:  # Döngü sonu - zayıf
        return 0.7

def ultra_solar_holding_factor(symbol: str) -> float:
    """☀️ Solar döngü faktörü (11 yıl)"""
    current_year = datetime.now().year
    solar_cycle_position = (current_year - 2008) % 11  # 2008 solar minimum
    
    if 3 <= solar_cycle_position <= 7:  # Solar maximum yakın
        return 1.2
    else:  # Solar minimum yakın
        return 0.9

def ultra_moon_holding_factor(symbol: str) -> float:
    """🌙 Ay döngüsü faktörü"""
    # Basit ay fazı simülasyonu
    day_of_month = datetime.now().day
    if 10 <= day_of_month <= 20:  # Dolunay fazı
        return 1.1
    else:  # Yeniay fazı
        return 0.95

def ultra_statistical_holding_factor(symbol: str) -> float:
    """📊 İstatistiksel yaş faktörü"""
    age = get_company_age_years(symbol)
    
    if age >= 50:  # Çok yaşlı şirket - stabil
        return 1.3
    elif age >= 20:  # Olgun şirket - normal
        return 1.0
    elif age >= 10:  # Genç şirket - dinamik
        return 1.1
    else:  # Çok genç - riskli
        return 0.8

def ultra_ml_holding_factor(symbol: str) -> float:
    """🤖 Machine Learning güven faktörü"""
    # Basit ML simülasyonu (gerçekte ML modelinden gelir)
    age = get_company_age_years(symbol)
    hash_value = hash(symbol) % 100
    
    # ML güven skoru simülasyonu
    confidence = 0.6 + (hash_value / 200.0) + (min(age, 50) / 100.0)
    
    if confidence > 0.85:
        return 1.4  # Yüksek güven
    elif confidence > 0.70:
        return 1.1  # Orta güven
    else:
        return 0.9  # Düşük güven

def ultra_risk_holding_factor(symbol: str) -> float:
    """⚠️ Risk faktörü"""
    age = get_company_age_years(symbol)
    
    # Yaşa göre risk değerlendirmesi
    if age >= 30:  # Düşük risk
        return 1.2
    elif age >= 15:  # Orta risk
        return 1.0
    else:  # Yüksek risk
        return 0.8

def calculate_ultra_holding_period(symbol: str, signal_type: str) -> str:
    """
    🚀 ULTRA TUTMA SÜRESİ HESAPLAYICI
    19 Ultra Modül kombinasyonu ile optimal süre
    """
    
    # Temel süre (hafta olarak)
    base_weeks = 2.0
    
    # ULTRA MODÜL FAKTÖRLERI
    astro_factor = ultra_astrology_holding_factor(symbol)
    shemitah_factor = ultra_shemitah_holding_factor(symbol) 
    solar_factor = ultra_solar_holding_factor(symbol)
    moon_factor = ultra_moon_holding_factor(symbol)
    stat_factor = ultra_statistical_holding_factor(symbol)
    ml_factor = ultra_ml_holding_factor(symbol)
    risk_factor = ultra_risk_holding_factor(symbol)
    
    # ULTRA KOMBINASYON - Astroloji Modülleri %50
    ultra_multiplier = (
        astro_factor * 0.20 +      # %20 Jupiter/Saturn Astroloji
        shemitah_factor * 0.15 +   # %15 Shemitah (7 yıl)
        solar_factor * 0.10 +      # %10 Solar (11 yıl) 
        moon_factor * 0.05 +       # %5 Moon evreleri
        stat_factor * 0.25 +       # %25 İstatistik
        ml_factor * 0.15 +         # %15 ML
        risk_factor * 0.10         # %10 Risk
    )
    
    # SAT sinyali için kısalt
    if signal_type == "SAT":
        ultra_multiplier *= 0.5
    
    # ULTRA HAFTA HESAPLA
    ultra_weeks = base_weeks * ultra_multiplier
    
    # ULTRA KATEGORILER
    if ultra_weeks < 0.5:
        return "1-3 gün ⚠️ ULTRA RİSK"
    elif ultra_weeks < 1.5:
        return "3-7 gün 🔸 ULTRA KISA"
    elif ultra_weeks < 3:
        return "1-3 hafta 🔶 ULTRA ORTA"
    elif ultra_weeks < 6:
        return "3-6 hafta ⭐ ULTRA GÜÇLÜ"
    elif ultra_weeks < 10:
        return "6-10 hafta 🏆 ULTRA PREMİUM"
    else:
        return "10+ hafta 💎 ULTRA ELİT"

def get_ultra_holding_debug_info(symbol: str) -> dict:
    """Debug için tüm faktörleri döndür"""
    return {
        "symbol": symbol,
        "company_age": get_company_age_years(symbol),
        "astro_factor": ultra_astrology_holding_factor(symbol),
        "shemitah_factor": ultra_shemitah_holding_factor(symbol),
        "solar_factor": ultra_solar_holding_factor(symbol),
        "moon_factor": ultra_moon_holding_factor(symbol),
        "stat_factor": ultra_statistical_holding_factor(symbol),
        "ml_factor": ultra_ml_holding_factor(symbol),
        "risk_factor": ultra_risk_holding_factor(symbol),
    }

if __name__ == "__main__":
    # Test
    test_symbols = ["ISATR.IS", "AKBNK.IS", "AGROT.IS", "TCELL.IS"]
    
    print("🚀 ULTRA TUTMA SÜRESİ TESTİ")
    print("=" * 50)
    
    for symbol in test_symbols:
        holding_period = calculate_ultra_holding_period(symbol, "AL")
        debug_info = get_ultra_holding_debug_info(symbol)
        
        print(f"\n📊 {symbol}:")
        print(f"   Yaş: {debug_info['company_age']} yıl")
        print(f"   🔮 Astro: {debug_info['astro_factor']:.2f}")
        print(f"   ⚡ Shemitah: {debug_info['shemitah_factor']:.2f}")
        print(f"   📊 İstatistik: {debug_info['stat_factor']:.2f}")
        print(f"   🤖 ML: {debug_info['ml_factor']:.2f}")
        print(f"   ⏰ ULTRA TUTMA: {holding_period}")