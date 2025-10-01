import pandas as pd
import numpy as np
from fix_series_bool import safe_float_from_series, fix_volume_comparison, fix_price_movement, safe_comparison

def refined_volume_spike(df_daily, factor=2.0, sma_window=10):
    """
    Gelişmiş hacim patlaması tespiti
    True = spike + %1.5 hareket
    """
    try:
        if len(df_daily) < sma_window + 1:
            return False
            
        # Hacim ortalaması (1 gün shift)
        vol_sma = df_daily["Volume"].rolling(sma_window).mean().shift(1)
        
        # Günlük fiyat degisimi
        close_now = safe_float_from_series(df_daily["Close"].iloc[-1])
        close_prev = safe_float_from_series(df_daily["Close"].iloc[-2])
        price_chg = (close_now / close_prev - 1) * 100
        
        # Hacim patlamasi + fiyat hareketi kontrolü
        current_vol = safe_float_from_series(df_daily["Volume"].iloc[-1])
        sma_value = vol_sma.iloc[-1]
        
        # Güvenli değer kontrolü
        try:
            if pd.isna(sma_value):
                avg_vol_sma = 1.0
            else:
                avg_vol_sma = float(sma_value)
                if avg_vol_sma <= 0:
                    avg_vol_sma = 1.0
        except:
            avg_vol_sma = 1.0
            
        volume_spike = fix_volume_comparison(current_vol, avg_vol_sma, factor)
        price_move = fix_price_movement(price_chg, 1.5)
        
        return volume_spike and price_move
        
    except Exception as e:
        print(f"Hacim spike hesaplama hatası: {e}")
        return False

def volume_spike_indicator(df_daily, factor=2.0, sma_window=10):
    """
    Hacim patlaması için detaylı bilgi döndür
    """
    try:
        if len(df_daily) < sma_window + 1:
            return {"spike": False, "ratio": 0, "price_chg": 0}
            
        # Hacim ortalaması
        vol_sma = df_daily["Volume"].rolling(sma_window).mean().shift(1)
        current_vol = safe_float_from_series(df_daily["Volume"].iloc[-1])
        sma_value = vol_sma.iloc[-1]
        
        # Güvenli değer kontrolü
        try:
            if pd.isna(sma_value):
                avg_vol = 1.0
            else:
                avg_vol = float(sma_value)
                if avg_vol <= 0:
                    avg_vol = 1.0
        except:
            avg_vol = 1.0
        
        # Hacim oranı
        vol_ratio = current_vol / avg_vol if avg_vol > 0 else 0
        
        # Fiyat değişimi
        close_now = safe_float_from_series(df_daily["Close"].iloc[-1])
        close_prev = safe_float_from_series(df_daily["Close"].iloc[-2])
        price_chg = (close_now / close_prev - 1) * 100
        
        # Spike kontrolü
        spike = fix_volume_comparison(current_vol, avg_vol, factor) and fix_price_movement(price_chg, 1.5)
        
        return {
            "spike": spike,
            "ratio": vol_ratio,
            "price_chg": price_chg,
            "factor": factor
        }
        
    except Exception as e:
        print(f"Hacim spike indicator hatası: {e}")
        return {"spike": False, "ratio": 0, "price_chg": 0}

def adaptive_volume_threshold(df_daily, base_factor=2.0):
    """
    Adaptif hacim eşiği belirleme
    Volatiliteye göre faktörü ayarlar
    """
    try:
        if len(df_daily) < 20:
            return base_factor
            
        # Son 20 günün volatilitesi
        returns = df_daily["Close"].pct_change(fill_method=None).dropna()
        volatility = returns.rolling(20).std().iloc[-1]
        
        # Yüksek volatilitede daha düşük eşik
        if volatility > 0.05:  # %5+ volatilite
            return base_factor * 0.8
        elif volatility < 0.02:  # %2- volatilite
            return base_factor * 1.2
        else:
            return base_factor
            
    except:
        return base_factor