#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PlanB ULTRA Early Warning System
Erken uyarı ve hacim patlaması tespiti için bonus skorlama sistemi
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from fix_series_bool import safe_float_from_series, safe_comparison
from fix_series_bool import safe_comparison, safe_float_from_series

def early_score(df_daily, market="BIST"):
    """
    Erken uyarı skoru hesapla - hacim patlaması ve momentum bazlı
    """
    try:
        if df_daily is None or df_daily.empty or len(df_daily) < 10:
            return 0.0
            
        # Hacim analizi
        volume = df_daily['Volume'].dropna()
        if volume.empty:
            return 0.0
            
        current_vol = volume.iloc[-1]
        avg_vol_20 = volume.rolling(20).mean().iloc[-1]
        
        # Hacim patlaması bonus
        volume_bonus = 0.0
        avg_vol_val = safe_float_from_series(avg_vol_20)
        current_vol_val = safe_float_from_series(current_vol)
        
        if avg_vol_val > 0:
            vol_ratio = current_vol_val / avg_vol_val
            if vol_ratio >= 3.0:
                volume_bonus = 15.0  # 🔊 Hacim Patlaması
            elif vol_ratio >= 2.0:
                volume_bonus = 8.0
            elif vol_ratio >= 1.5:
                volume_bonus = 4.0
        
        # Fiyat momentum bonus
        close = df_daily['Close'].dropna()
        if len(close) >= 5:
            price_now = close.iloc[-1]
            price_5d = close.iloc[-5]
            
            momentum_bonus = 0.0
            price_now_val = safe_float_from_series(price_now)
            price_5d_val = safe_float_from_series(price_5d)
            
            if price_5d_val > 0:
                change_5d = ((price_now_val - price_5d_val) / price_5d_val) * 100
                if change_5d >= 15:
                    momentum_bonus = 10.0
                elif change_5d >= 8:
                    momentum_bonus = 5.0
                elif change_5d >= 3:
                    momentum_bonus = 2.0
        
        total_bonus = volume_bonus + momentum_bonus
        return min(total_bonus, 20.0)  # Max 20 bonus puan
        
    except Exception as e:
        print(f"[DEBUG] Early score error: {e}")
        return 0.0


def hourly_momentum(symbol):
    """
    1 saatlik momentum skoru (0-1 arası)
    """
    try:
        # 1 saatlik veri al (son 3 gün)
        ticker = yf.Ticker(symbol)
        df_1h = ticker.history(period="3d", interval="1h")
        
        if df_1h.empty or len(df_1h) < 12:
            return 0.0
            
        close = df_1h['Close'].dropna()
        if len(close) < 12:
            return 0.0
            
        # Son 6 saat vs önceki 6 saat momentum
        recent_6h = close.iloc[-6:].mean()
        previous_6h = close.iloc[-12:-6].mean()
        
        if previous_6h > 0:
            momentum = ((recent_6h - previous_6h) / previous_6h)
            return max(0, min(1.0, momentum * 10))  # 0-1 arası normalize
            
        return 0.0
        
    except Exception as e:
        print(f"[DEBUG] Hourly momentum error for {symbol}: {e}")
        return 0.0


def dynamic_threshold(market="BIST"):
    """
    Pazar bazlı dinamik eşik
    """
    thresholds = {
        "BIST": 60,      # BIST için erken sinyal (IS suffix)
        "NASDAQ": 65,    # NASDAQ için standart
        "CRYPTO": 62,    # Crypto için orta (-USD suffix)
        "EMTIA": 63,     # Emtia için orta (=F suffix)
        "XETRA": 64,     # XETRA için orta (DE suffix)
    }
    
    # Market detection
    if market in thresholds:
        return thresholds[market]
    else:
        return 65  # Default


def volume_spike_detected(df_daily):
    """
    Hacim patlaması var mı? (boolean)
    """
    try:
        if df_daily is None or df_daily.empty:
            return False
            
        volume = df_daily['Volume'].dropna()
        if len(volume) < 20:
            return False
            
        current_vol = volume.iloc[-1]
        avg_vol_20 = volume.rolling(20).mean().iloc[-1]
        
        current_vol_val = safe_float_from_series(current_vol)
        avg_vol_val = safe_float_from_series(avg_vol_20)
        
        return bool(safe_comparison(avg_vol_20, 0, 'gt') and safe_comparison(current_vol, avg_vol_20 * 2.5, 'gte'))
        
    except:
        return False


def get_market_from_symbol(symbol):
    """
    Sembol'den pazar türünü tespit et
    """
    if symbol.endswith('.IS'):
        return "BIST"
    elif symbol.endswith('-USD'):
        return "CRYPTO"
    elif '=F' in symbol:
        return "EMTIA"
    elif symbol.endswith('.DE'):
        return "XETRA"
    else:
        return "NASDAQ"


# Test fonksiyonu
if __name__ == "__main__":
    # Test
    print("🔍 Early Warning System Test")
    
    test_symbols = ["AAPL", "THYAO.IS", "BTC-USD"]
    
    for symbol in test_symbols:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1mo", interval="1d")
            
            market = get_market_from_symbol(symbol)
            early = early_score(df, market)
            hourly = hourly_momentum(symbol)
            threshold = dynamic_threshold(market)
            spike = volume_spike_detected(df)
            
            print(f"{symbol} ({market}): Early={early:.1f}, Hourly={hourly:.3f}, Threshold={threshold}, Spike={spike}")
            
        except Exception as e:
            print(f"{symbol}: Error - {e}")