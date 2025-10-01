#!/usr/bin/env python3
"""
PlanB Motoru - Otomatik Telegram Bildirim Sistemi
7/24 sürekli analiz ve bildirim
"""
import sys
import os
sys.path.append('/root')

import requests
import json
import time
import yfinance as yf
from datetime import datetime
import threading

# Telegram Bot Config
TELEGRAM_BOT_TOKEN = "7994708397:AAGUWY92gsAO7cOIXV_ShwsojH28riKCyXE"
CHAT_ID = "6263576109"  # Chat ID düzeltildi!

def send_telegram_message(message):
    """Telegram'a mesaj gönder"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram mesaj hatası: {e}")
        return False

def analyze_symbol(symbol):
    """Sembol analiz et"""
    try:
        # Gerçek veri çek
        stock_data = yf.download(symbol, period='1y', progress=False)
        if stock_data.empty:
            return None
        
        current_price = stock_data['Close'].iloc[-1]
        
        # Basit analiz skorları
        rsi = calculate_rsi(stock_data['Close'])
        ma_signal = calculate_ma_signal(stock_data['Close'])
        volume_signal = calculate_volume_signal(stock_data)
        
        # Toplam skor
        total_score = (rsi + ma_signal + volume_signal) / 3
        
        # Sinyal belirle
        if total_score >= 70:
            signal = "🟢 AL"
        elif total_score >= 60:
            signal = "🔵 TUT_GÜÇLÜ"
        elif total_score >= 40:
            signal = "⚪ TUT"
        else:
            signal = "🔴 SAT"
        
        return {
            'symbol': symbol,
            'price': round(current_price, 2),
            'score': round(total_score, 1),
            'signal': signal,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
    except Exception as e:
        print(f"Analiz hatası {symbol}: {e}")
        return None

def calculate_rsi(prices, period=14):
    """RSI hesapla"""
    try:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return min(100, max(0, rsi.iloc[-1]))
    except:
        return 50

def calculate_ma_signal(prices):
    """Moving Average sinyali"""
    try:
        ma_20 = prices.rolling(20).mean().iloc[-1]
        ma_50 = prices.rolling(50).mean().iloc[-1]
        current = prices.iloc[-1]
        
        if current > ma_20 > ma_50:
            return 80
        elif current > ma_20:
            return 60
        elif current > ma_50:
            return 40
        else:
            return 20
    except:
        return 50

def calculate_volume_signal(data):
    """Hacim sinyali"""
    try:
        vol_avg = data['Volume'].rolling(20).mean().iloc[-1]
        vol_current = data['Volume'].iloc[-1]
        
        if vol_current > vol_avg * 1.5:
            return 70
        elif vol_current > vol_avg:
            return 60
        else:
            return 40
    except:
        return 50

def continuous_analysis():
    """Sürekli analiz döngüsü"""
    # Test sembolleri
    symbols = {
        'BIST': ['ASELS.IS', 'TUPRS.IS', 'THYAO.IS', 'EREGL.IS', 'AKBNK.IS'],
        'NASDAQ': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
        'CRYPTO': ['BTC-USD', 'ETH-USD', 'ADA-USD'],
        'EMTIA': ['GC=F', 'SI=F', 'CL=F', 'NG=F', 'HG=F'],
        'XETRA': ['SAP.DE', 'BMW.DE', 'VOW3.DE', 'SIE.DE', 'DBK.DE']
    }
    
    cycle_count = 0
    
    while True:
        try:
            cycle_count += 1
            current_time = datetime.now().strftime('%H:%M:%S')
            
            print(f"🔄 Analiz Döngüsü #{cycle_count} - {current_time}")
            
            # Her pazar için analiz
            for market, symbol_list in symbols.items():
                print(f"📊 {market} analizi başlıyor...")
                
                strong_signals = []
                
                for symbol in symbol_list:
                    result = analyze_symbol(symbol)
                    if result and result['score'] >= 65:  # Sadece güçlü sinyaller
                        strong_signals.append(result)
                
                # Güçlü sinyal varsa Telegram'a gönder
                if strong_signals:
                    message = f"🚀 <b>PlanB {market} ANALİZİ</b>\n"
                    message += f"⏰ {current_time}\n\n"
                    
                    for signal in strong_signals:
                        message += f"{signal['signal']} <b>{signal['symbol']}</b>\n"
                        message += f"💰 Fiyat: {signal['price']}\n"
                        message += f"📈 Skor: {signal['score']}/100\n"
                        message += f"────────────────\n"
                    
                    message += f"\n🎯 Toplam {len(strong_signals)} güçlü sinyal tespit edildi!"
                    
                    if send_telegram_message(message):
                        print(f"✅ {market} sinyalleri Telegram'a gönderildi")
                    else:
                        print(f"❌ {market} Telegram gönderimi başarısız")
            
            # Durum mesajı
            if cycle_count % 4 == 0:  # Her 4 döngüde bir durum raporu (1 saat)
                status_msg = f"🤖 <b>PlanB Motoru Durum Raporu</b>\n"
                status_msg += f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                status_msg += f"🔄 Tamamlanan döngü: {cycle_count}\n"
                status_msg += f"✅ Sistem aktif ve çalışıyor!\n"
                status_msg += f"📡 Sonraki analiz: 15 dakika sonra"
                
                send_telegram_message(status_msg)
            
            print(f"😴 15 dakika bekleniyor...")
            time.sleep(900)  # 15 dakika bekle
            
        except KeyboardInterrupt:
            print("👋 Sistem durduruldu")
            break
        except Exception as e:
            print(f"❌ Genel hata: {e}")
            time.sleep(60)  # Hata durumunda 1 dakika bekle

if __name__ == "__main__":
    print("🚀 PlanB Otomatik Telegram Trader başlatılıyor...")
    
    # İlk test mesajı
    test_message = f"🤖 <b>PlanB Motoru BAŞLATILDI!</b>\n"
    test_message += f"⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
    test_message += f"🎯 7/24 otomatik analiz sistemi aktif!\n"
    test_message += f"📊 BIST, NASDAQ, CRYPTO, EMTIA ve XETRA takip ediliyor\n"
    test_message += f"⚡ Her 15 dakikada analiz yapılıyor\n"
    test_message += f"🎯 Sadece 65+ puan alan sinyaller bildirilecek"
    
    if send_telegram_message(test_message):
        print("✅ Başlangıç mesajı gönderildi")
        continuous_analysis()
    else:
        print("❌ Telegram bağlantısı başarısız - Chat ID kontrol edin")