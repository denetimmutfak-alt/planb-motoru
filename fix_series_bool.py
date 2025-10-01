#!/usr/bin/env python3
"""
PlanB ULTRA - Series Boolean Fix
Pandas 2.2+ "The truth value of a Series is ambiguous" hatası için çözüm
"""
import pandas as pd
import numpy as np

def bool_series(ser):
    """
    Tek elemanlı Series → bool (True/False)
    Çok elemanlı → ValueError atmaz, ama biz tek eleman bekliyoruz.
    """
    if ser.empty:
        return False
    if len(ser) == 1:
        return bool(ser.iloc[0])
    # Çok elemanlı ise ilk elemanı al (güvenlik için)
    return bool(ser.iloc[0])

def safe_bool(df_daily, condition_col, threshold):
    """
    Koşul: df_daily[condition_col] > threshold
    → Tek elemanlı Series → bool
    """
    try:
        cond = df_daily[condition_col] > threshold
        return bool_series(cond)
    except:
        return False

def safe_float_from_series(series_val):
    """
    Series'ten güvenli float çıkarma
    """
    try:
        if isinstance(series_val, pd.Series):
            if series_val.empty:
                return 0.0
            return float(series_val.iloc[0])
        else:
            return float(series_val)
    except:
        return 0.0

def safe_comparison(series_val, threshold, operator="gt"):
    """
    Series değer karşılaştırması için güvenli yöntem
    operator: 'gt', 'lt', 'gte', 'lte', 'eq'
    """
    try:
        if isinstance(series_val, pd.Series):
            if series_val.empty:
                return False
            val = series_val.iloc[0]
        else:
            val = series_val
            
        if operator == "gt":
            return bool(val > threshold)
        elif operator == "lt":
            return bool(val < threshold)
        elif operator == "gte":
            return bool(val >= threshold)
        elif operator == "lte":
            return bool(val <= threshold)
        elif operator == "eq":
            return bool(val == threshold)
        else:
            return False
    except:
        return False

def fix_volume_comparison(current_vol, avg_vol, factor=2.0):
    """
    Hacim karşılaştırması için özel fonksiyon
    """
    try:
        curr_val = safe_float_from_series(current_vol)
        avg_val = safe_float_from_series(avg_vol)
        
        if avg_val <= 0:
            return False
            
        return bool(curr_val > (factor * avg_val))
    except:
        return False

def fix_price_movement(price_chg, threshold=1.5):
    """
    Fiyat hareketi kontrolü için güvenli fonksiyon
    """
    try:
        chg_val = safe_float_from_series(price_chg)
        return bool(abs(chg_val) > threshold)
    except:
        return False

# Test fonksiyonu
if __name__ == "__main__":
    print("🔧 Series Boolean Fix Test")
    
    # Test Series
    test_series = pd.Series([75.5])
    test_threshold = 70
    
    # Eski yöntem (hata verir)
    try:
        if test_series > test_threshold:
            print("❌ Bu satır hata verecek")
    except ValueError as e:
        print(f"❌ Eski yöntem hatası: {e}")
    
    # Yeni yöntem
    result = safe_comparison(test_series, test_threshold, "gt")
    print(f"✅ Yeni yöntem sonucu: {result}")
    
    print("🚀 Fix modülü hazır!")