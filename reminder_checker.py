#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PlanB ULTRA Interactive Reminder Checker
Her gün sabah 09:00'da çalışır ve SAT zamanı gelen varlıkları hatırlatır.
"""

import os
import csv
import requests
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# Telegram ayarları
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7994708397:AAGUWY92gsAO7cOIXV_ShwsojH28riKCyXE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "6263576109")

BASE_DIR = Path(__file__).resolve().parent

def send_telegram_message(message: str, chat_id: str = None) -> bool:
    """Telegram'a mesaj gönder"""
    target_chat = chat_id or TELEGRAM_CHAT_ID
    
    if not TELEGRAM_BOT_TOKEN or not target_chat:
        print("[WARN] Telegram token/chat id bulunamadı")
        return False
        
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": target_chat,
            "text": message,
            "parse_mode": "HTML"
        }
        r = requests.post(url, json=data, timeout=20)
        
        if r.status_code != 200:
            print(f"[ERROR] Telegram HTTP {r.status_code}: {r.text[:200]}")
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Telegram gönderim hatası: {e}")
        return False

def get_current_price(symbol: str) -> float:
    """Mevcut fiyatı al"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1d")
        if not data.empty:
            return float(data['Close'].iloc[-1])
    except:
        pass
    return 0.0

def calculate_profit_loss(al_price: float, current_price: float) -> dict:
    """Kar/zarar hesapla"""
    if al_price <= 0:
        return {"change": 0.0, "percent": 0.0, "status": "➡️"}
    
    change = current_price - al_price
    percent = (change / al_price) * 100
    
    if percent > 5:
        status = "🟢"
    elif percent < -5:
        status = "🔴" 
    else:
        status = "🟡"
        
    return {
        "change": change,
        "percent": percent,
        "status": status
    }

def main():
    """Ana hatırlatma kontrolü"""
    print("🔔 PlanB ULTRA Interactive Reminder başlatılıyor...")
    
    csv_file = BASE_DIR / "data" / "reminders.csv"
    
    if not csv_file.exists():
        print("📅 Hatırlatma dosyası bulunamadı")
        return
    
    try:
        # CSV dosyasını oku
        df = pd.read_csv(csv_file)
        today = datetime.now().date()
        
        # Bugün hatırlatılacak kayıtları bul
        df['deadline'] = pd.to_datetime(df['deadline']).dt.date
        pending = df[(df['deadline'] <= today) & (df['notified'] == 0)]
        
        if pending.empty:
            print("📅 Bugün hatırlatılacak sinyal yok")
            return
        
        # Her hatırlatma için mesaj gönder
        for idx, row in pending.iterrows():
            # Mevcut fiyatı al
            current_price = get_current_price(row['symbol'])
            
            # Kar/zarar hesapla
            pnl = calculate_profit_loss(row['al_price'], current_price)
            
            # Hatırlatma mesajı
            message = (
                f"⏰ <b>SAT ZAMANI GELDİ!</b>\n\n"
                f"🎯 <b>{row['symbol']}</b>\n"
                f"📅 AL tarihi: {row['al_date']}\n"
                f"📊 AL puanı: {row['al_score']}/100\n"
                f"💰 AL fiyatı: ${row['al_price']:.2f}\n"
            )
            
            if current_price > 0:
                message += (
                    f"💲 Şu anki fiyat: ${current_price:.2f}\n"
                    f"{pnl['status']} Kar/Zarar: {pnl['percent']:+.1f}%\n"
                )
            
            days_held = (today - pd.to_datetime(row['al_date']).date()).days
            message += (
                f"⏱️ Elde tutma: {days_held} gün\n"
                f"🎯 Önerilen: <u>BUGÜN SAT</u>\n\n"
                f"💡 Pozisyonu kapatmayı unutma!"
            )
            
            # Mesajı gönder
            if send_telegram_message(message, str(row['user_id'])):
                # Hatırlatıldı olarak işaretle
                df.loc[idx, 'notified'] = 1
                print(f"✅ Hatırlatma gönderildi: {row['symbol']} -> {row['user_id']}")
            else:
                print(f"❌ Hatırlatma gönderilemedi: {row['symbol']}")
        
        # CSV'yi güncelle
        df.to_csv(csv_file, index=False)
        
        # Haftalık özet (Pazartesi günleri)
        if datetime.now().weekday() == 0:  # Pazartesi
            active = df[df['notified'] == 0]
            
            if not active.empty:
                summary_msg = "📊 <b>Haftalık Aktif Pozisyonlar:</b>\n\n"
                
                for _, pos in active.iterrows():
                    days_left = (pd.to_datetime(pos['deadline']).date() - today).days
                    if days_left <= 0:
                        status = "🔴 SAT ZAMANI!"
                    elif days_left <= 3:
                        status = f"🟡 {days_left} gün kaldı"
                    else:
                        status = f"🟢 {days_left} gün kaldı"
                    
                    summary_msg += (
                        f"• <b>{pos['symbol']}</b> - {status}\n"
                        f"  AL: {pos['al_date']}, Puan: {pos['al_score']}/100\n\n"
                    )
                
                send_telegram_message(summary_msg)
                print("✅ Haftalık özet gönderildi")
        
        print(f"✅ Hatırlatma kontrolü tamamlandı: {len(pending)} bildirim")
        
    except Exception as e:
        print(f"❌ Hatırlatma kontrol hatası: {e}")
        
        # Hata durumunda admin'e bildir
        error_message = f"⚠️ <b>Interactive Reminder Hatası</b>\n\n<code>{str(e)}</code>"
        send_telegram_message(error_message)

if __name__ == "__main__":
    main()