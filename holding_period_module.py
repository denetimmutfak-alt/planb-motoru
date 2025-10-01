def calculate_holding_period(df, signal_type: str) -> str:
    """
    🎯 TUTMA SÜRESİ ANALİZİ
    =======================
    Teknik göstergelere göre optimal tutma süresini hesaplar
    
    AL sinyali için:
    - RSI momentum gücü
    - MA konverjansı  
    - Hacim trendi
    - Volatilite analizi
    """
    
    try:
        close = df["Close"].dropna()
        if len(close) < 50:
            return "1-2 hafta"
            
        # RSI momentum analizi
        rsi = calculate_rsi(close, 14)
        current_rsi = float(rsi.iloc[-1]) if not rsi.empty else 50
        
        # MA trend analizi
        ma20 = close.rolling(20).mean()
        ma50 = close.rolling(50).mean()
        ma_trend = "YÜKSELİŞ" if ma20.iloc[-1] > ma50.iloc[-1] else "DÜŞÜŞ"
        
        # Volatilite analizi
        volatility = close.pct_change(fill_method=None).std() * 100
        
        # Hacim trendi (varsa)
        volume_trend = 1.0
        if "Volume" in df.columns:
            vol = df["Volume"].dropna()
            if len(vol) >= 20:
                vol_ma = vol.rolling(20).mean()
                volume_trend = vol.iloc[-1] / vol_ma.iloc[-1] if vol_ma.iloc[-1] > 0 else 1.0
        
        # TUTMA SÜRESİ HESAPLAMA ALGORİTMASI
        if signal_type == "AL":
            # Güçlü momentum + düşük volatilite = uzun tutma
            if current_rsi > 60 and ma_trend == "YÜKSELİŞ" and volatility < 2.0:
                return "3-4 hafta ⭐"
            # Orta momentum = orta vadeli
            elif current_rsi > 45 and ma_trend == "YÜKSELİŞ":
                return "2-3 hafta"
            # Zayıf momentum = kısa vadeli
            elif current_rsi > 35:
                return "1-2 hafta"
            else:
                return "3-7 gün ⚠️"
                
        elif signal_type == "SAT":
            # SAT sinyalinde hızlı çıkış önerilir
            if current_rsi < 30:
                return "1-3 gün"
            else:
                return "3-7 gün"
        else:
            return "1-2 hafta"
            
    except Exception:
        return "1-2 hafta"


def format_signal_line_with_holding(s: dict) -> str:
    """Tutma süresi dahil sinyal formatı"""
    holding_period = s.get('holding_period', '1-2 hafta')
    return f"{s['signal']} <b>{s['symbol']}</b> | 💰 {s['price']} | 📈 {s['score']}/100 | ⏰ {holding_period}\n"