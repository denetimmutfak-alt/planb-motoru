import talib
import numpy as np
import pandas as pd
from datetime import datetime as dt

def ew_optimized(df_daily, market="BIST"):
    """
    Enhanced Early Warning System v2
    0-40 arası bonus; 50+ için yeterli
    """
    bonus = 0
    
    # 1) RSI(3) < 60 & fiyat > EMA8
    try:
        rsi3 = talib.RSI(df_daily["Close"], 3)[-1]
        ema8 = talib.EMA(df_daily["Close"], 8)[-1]
        if not np.isnan(rsi3) and not np.isnan(ema8):
            current_price = float(df_daily["Close"].iloc[-1])
            if rsi3 < 60 and current_price > ema8:
                bonus += 12
    except:
        pass
    
    # 2) Hacim > 20-ort * 1.8 & kapanış > %1.5
    try:
        vol_spike = bool(df_daily["Volume"].iloc[-1] > df_daily["Volume"].rolling(20).mean().iloc[-1] * 1.8)
        ret1d = (df_daily["Close"].iloc[-1] / df_daily["Close"].iloc[-2] - 1) * 100
        if vol_spike and ret1d > 1.5:
            bonus += 10
    except:
        pass
    
    # 3) Bollinger %b < 0.75 (henüz üst banda değil)
    try:
        bb_upper, bb_middle, bb_lower = talib.BBANDS(df_daily["Close"], 20, 2, 2)
        bb_b = (df_daily["Close"].iloc[-1] - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1])
        if not np.isnan(bb_b) and bb_b < 0.75:
            bonus += 8
    except:
        pass
    
    # 4) Günlük slope > 0 & vola artışı
    try:
        slope = np.polyfit(range(5), df_daily["Close"].iloc[-5:], 1)[0]
        vola5 = df_daily["Close"].pct_change(fill_method=None).rolling(5).std().iloc[-1]
        vola20 = df_daily["Close"].pct_change(fill_method=None).rolling(20).std().iloc[-1]
        if slope > 0 and vola5 > vola20 * 1.2:
            bonus += 10
    except:
        pass
    
    return min(40, bonus)