#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PlanB ULTRA Daily Reminder Script
Her gün sabah 09:00'da çalışır ve SAT zamanı gelen varlıkları hatırlatır.
"""

import os
import requests
from signal_tracker import SignalTracker
from pathlib import Path
from datetime import datetime
import pandas as pd

# Telegram ayarları - ana sistemdeki ile aynı
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7994708397:AAGUWY92gsAO7cOIXV_ShwsojH28riKCyXE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "6263576109")

def send_telegram_message(message: str) -> bool:
    """Telegram'a mesaj gönder - ana sistemdeki fonksiyonun aynısı"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[WARN] Telegram token/chat id bulunamadı")
        return False
        
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        r = requests.post(url, data=data, timeout=20)
        
        if r.status_code != 200:
            print(f"[ERROR] Telegram HTTP {r.status_code}: {r.text[:200]}")
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Telegram gönderim hatası: {e}")
        return False

def main():
    """Günlük hatırlatma ana fonksiyonu"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID environment variables gerekli!")
        return
        
    print("🔔 PlanB ULTRA Daily Reminder başlatılıyor...")
    
    try:
        # Signal tracker'ı başlat
        tracker = SignalTracker()
        
        # Hatırlatılacak sinyalleri al
        pending = tracker.get_pending_reminders()
        
        if pending.empty:
            print("📅 Bugün hatırlatılacak sinyal yok")
            return
            
        # Her bir sinyal için hatırlatma gönder
        for _, signal in pending.iterrows():
            days_held = (datetime.now() - pd.to_datetime(signal.signal_date)).days
            
            message = (
                f"⏰ <b>SAT ZAMANI GELDİ!</b>\n\n"
                f"🎯 <b>{signal.symbol}</b>\n"
                f"📅 AL tarihi: {pd.to_datetime(signal.signal_date).strftime('%d.%m.%Y')}\n"
                f"📊 AL puanı: {signal.score}/100\n"
                f"💰 AL fiyatı: ${signal.price:.2f}\n" if signal.price else "" +
                f"⏱️ Elde tutma: {days_held} gün\n"
                f"🎯 Önerilen: <u>BUGÜN SAT</u>\n\n"
                f"💡 Unutma: Kar/zarar kontrolü yap!"
            )
            
            if send_telegram_message(message):
                tracker.mark_reminded(signal.id)
                print(f"✅ Hatırlatma gönderildi: {signal.symbol}")
            else:
                print(f"❌ Hatırlatma gönderilemedi: {signal.symbol}")
                
        # Haftalık özet (Pazartesi günleri)
        if datetime.now().weekday() == 0:  # Pazartesi
            holdings = tracker.get_active_holdings()
            
            if not holdings.empty:
                message = "📊 <b>Haftalık Pozisyon Özeti:</b>\n\n"
                
                for _, h in holdings.iterrows():
                    days_left = int(h.days_remaining)
                    status = "🔴 SAT ZAMANI!" if days_left <= 0 else f"🟡 {days_left} gün kaldı"
                    
                    message += (
                        f"• <b>{h.symbol}</b> - {status}\n"
                        f"  AL: {pd.to_datetime(h.signal_date).strftime('%d.%m')}, "
                        f"Puan: {h.score}/100\n\n"
                    )
                    
                send_telegram_message(message)
                print("✅ Haftalık özet gönderildi")
            
        print("✅ Günlük hatırlatma tamamlandı")
        
    except Exception as e:
        print(f"❌ Hatırlatma hatası: {e}")
        
        # Hata durumunda admin'e bildir
        error_message = f"⚠️ <b>Reminder System Hatası</b>\n\n<code>{str(e)}</code>"
        send_telegram_message(error_message)

if __name__ == "__main__":
    main()