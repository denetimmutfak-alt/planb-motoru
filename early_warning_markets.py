import pandas as pd
import talib
import numpy as np
from fix_series_bool import safe_comparison

def nasdaq_early_score(df_daily):
    """NASDAQ özel – scale: x3"""
    score = 0
    try:
        # RSI(3) kontrolü
        rsi3 = talib.RSI(df_daily["Close"], 3)
        if len(rsi3) > 0 and not pd.isna(rsi3.iloc[-1]):
            rsi_val = float(rsi3.iloc[-1])
            ema8 = talib.EMA(df_daily["Close"], 8)
            if len(ema8) > 0 and not pd.isna(ema8.iloc[-1]):
                ema_val = float(ema8.iloc[-1])
                current_price = float(df_daily["Close"].iloc[-1])
                if rsi_val < 60 and current_price > ema_val:
                    score += 12
        
        # Hacim patlaması – NASDAQ için x3 scale
        current_vol = float(df_daily["Volume"].iloc[-1])
        avg_vol_20 = float(df_daily["Volume"].rolling(20).mean().iloc[-1])
        vol_spike = safe_comparison(current_vol, avg_vol_20 * 3.0, 'gt')
        
        ret1d = (float(df_daily["Close"].iloc[-1]) / float(df_daily["Close"].iloc[-2]) - 1) * 100
        if vol_spike and ret1d > 1.5:
            score += 10
        
        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = talib.BBANDS(df_daily["Close"], 20, 2, 2)
        if len(bb_upper) > 0 and not pd.isna(bb_upper.iloc[-1]):
            bb_b = (float(df_daily["Close"].iloc[-1]) - float(bb_lower.iloc[-1])) / (float(bb_upper.iloc[-1]) - float(bb_lower.iloc[-1]))
            if bb_b < 0.75:
                score += 8
        
        # Slope ve volatilite
        prices = df_daily["Close"].iloc[-5:].values
        if len(prices) == 5:
            slope = np.polyfit(range(5), prices, 1)[0]
            vola5 = float(df_daily["Close"].pct_change(fill_method=None).rolling(5).std().iloc[-1])
            vola20 = float(df_daily["Close"].pct_change(fill_method=None).rolling(20).std().iloc[-1])
            if slope > 0 and vola5 > vola20 * 1.2:
                score += 10
                
    except Exception as e:
        print(f"NASDAQ early warning hatası: {e}")
        return 0
    
    return min(40, score)

def xetra_early_score(df_daily):
    """XETRA özel – scale: x2"""
    score = 0
    try:
        # RSI(3) kontrolü
        rsi3 = talib.RSI(df_daily["Close"], 3)
        if len(rsi3) > 0 and not pd.isna(rsi3.iloc[-1]):
            rsi_val = float(rsi3.iloc[-1])
            ema8 = talib.EMA(df_daily["Close"], 8)
            if len(ema8) > 0 and not pd.isna(ema8.iloc[-1]):
                ema_val = float(ema8.iloc[-1])
                current_price = float(df_daily["Close"].iloc[-1])
                if rsi_val < 60 and current_price > ema_val:
                    score += 12
        
        # Hacim patlaması – XETRA için x2 scale
        current_vol = float(df_daily["Volume"].iloc[-1])
        avg_vol_20 = float(df_daily["Volume"].rolling(20).mean().iloc[-1])
        vol_spike = safe_comparison(current_vol, avg_vol_20 * 2.0, 'gt')
        
        ret1d = (float(df_daily["Close"].iloc[-1]) / float(df_daily["Close"].iloc[-2]) - 1) * 100
        if vol_spike and ret1d > 1.5:
            score += 10
        
        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = talib.BBANDS(df_daily["Close"], 20, 2, 2)
        if len(bb_upper) > 0 and not pd.isna(bb_upper.iloc[-1]):
            bb_b = (float(df_daily["Close"].iloc[-1]) - float(bb_lower.iloc[-1])) / (float(bb_upper.iloc[-1]) - float(bb_lower.iloc[-1]))
            if bb_b < 0.75:
                score += 8
        
        # Slope ve volatilite
        prices = df_daily["Close"].iloc[-5:].values
        if len(prices) == 5:
            slope = np.polyfit(range(5), prices, 1)[0]
            vola5 = float(df_daily["Close"].pct_change(fill_method=None).rolling(5).std().iloc[-1])
            vola20 = float(df_daily["Close"].pct_change(fill_method=None).rolling(20).std().iloc[-1])
            if slope > 0 and vola5 > vola20 * 1.2:
                score += 10
                
    except Exception as e:
        print(f"XETRA early warning hatası: {e}")
        return 0
    
    return min(40, score)

def emtia_early_score(df_daily):
    """EMTIA özel – scale: x2"""
    score = 0
    try:
        # RSI(3) kontrolü
        rsi3 = talib.RSI(df_daily["Close"], 3)
        if len(rsi3) > 0 and not pd.isna(rsi3.iloc[-1]):
            rsi_val = float(rsi3.iloc[-1])
            ema8 = talib.EMA(df_daily["Close"], 8)
            if len(ema8) > 0 and not pd.isna(ema8.iloc[-1]):
                ema_val = float(ema8.iloc[-1])
                current_price = float(df_daily["Close"].iloc[-1])
                if rsi_val < 60 and current_price > ema_val:
                    score += 12
        
        # Hacim patlaması – EMTIA için x2 scale
        current_vol = float(df_daily["Volume"].iloc[-1])
        avg_vol_20 = float(df_daily["Volume"].rolling(20).mean().iloc[-1])
        vol_spike = safe_comparison(current_vol, avg_vol_20 * 2.0, 'gt')
        
        ret1d = (float(df_daily["Close"].iloc[-1]) / float(df_daily["Close"].iloc[-2]) - 1) * 100
        if vol_spike and ret1d > 1.5:
            score += 10
        
        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = talib.BBANDS(df_daily["Close"], 20, 2, 2)
        if len(bb_upper) > 0 and not pd.isna(bb_upper.iloc[-1]):
            bb_b = (float(df_daily["Close"].iloc[-1]) - float(bb_lower.iloc[-1])) / (float(bb_upper.iloc[-1]) - float(bb_lower.iloc[-1]))
            if bb_b < 0.75:
                score += 8
        
        # Slope ve volatilite
        prices = df_daily["Close"].iloc[-5:].values
        if len(prices) == 5:
            slope = np.polyfit(range(5), prices, 1)[0]
            vola5 = float(df_daily["Close"].pct_change(fill_method=None).rolling(5).std().iloc[-1])
            vola20 = float(df_daily["Close"].pct_change(fill_method=None).rolling(20).std().iloc[-1])
            if slope > 0 and vola5 > vola20 * 1.2:
                score += 10
                
    except Exception as e:
        print(f"EMTIA early warning hatası: {e}")
        return 0
    
    return min(40, score)

def crypto_early_score(df_daily):
    """CRYPTO özel – scale: x10 (volatilite yüksek)"""
    score = 0
    try:
        # RSI(3) kontrolü
        rsi3 = talib.RSI(df_daily["Close"], 3)
        if len(rsi3) > 0 and not pd.isna(rsi3.iloc[-1]):
            rsi_val = float(rsi3.iloc[-1])
            ema8 = talib.EMA(df_daily["Close"], 8)
            if len(ema8) > 0 and not pd.isna(ema8.iloc[-1]):
                ema_val = float(ema8.iloc[-1])
                current_price = float(df_daily["Close"].iloc[-1])
                if rsi_val < 60 and current_price > ema_val:
                    score += 12
        
        # Hacim patlaması – CRYPTO için x10 scale (volatilite yüksek)
        current_vol = float(df_daily["Volume"].iloc[-1])
        avg_vol_20 = float(df_daily["Volume"].rolling(20).mean().iloc[-1])
        vol_spike = safe_comparison(current_vol, avg_vol_20 * 10.0, 'gt')
        
        ret1d = (float(df_daily["Close"].iloc[-1]) / float(df_daily["Close"].iloc[-2]) - 1) * 100
        if vol_spike and ret1d > 1.5:
            score += 10
        
        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = talib.BBANDS(df_daily["Close"], 20, 2, 2)
        if len(bb_upper) > 0 and not pd.isna(bb_upper.iloc[-1]):
            bb_b = (float(df_daily["Close"].iloc[-1]) - float(bb_lower.iloc[-1])) / (float(bb_upper.iloc[-1]) - float(bb_lower.iloc[-1]))
            if bb_b < 0.75:
                score += 8
        
        # Slope ve volatilite
        prices = df_daily["Close"].iloc[-5:].values
        if len(prices) == 5:
            slope = np.polyfit(range(5), prices, 1)[0]
            vola5 = float(df_daily["Close"].pct_change(fill_method=None).rolling(5).std().iloc[-1])
            vola20 = float(df_daily["Close"].pct_change(fill_method=None).rolling(20).std().iloc[-1])
            if slope > 0 and vola5 > vola20 * 1.2:
                score += 10
                
    except Exception as e:
        print(f"CRYPTO early warning hatası: {e}")
        return 0
    
    return min(40, score)
