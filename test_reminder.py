#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PlanB ULTRA Simple Reminder Test
Ana scriptten Telegram bilgilerini çekip test reminder gönderir.
"""

import asyncio
import sys
import os
from pathlib import Path

# Ana scripti import et ve Telegram ayarlarını al
sys.path.append('/home/planb/planb-motoru')

try:
    # Ana script çalışan process'ten environment'ı öğren
    import subprocess
    
    # Alternatif 1: Ana scriptten değerleri çek
    import telegram_full_trader_with_sentiment
    
    BOT_TOKEN = telegram_full_trader_with_sentiment.TELEGRAM_BOT_TOKEN
    CHAT_ID = telegram_full_trader_with_sentiment.TELEGRAM_CHAT_ID
    
    print(f"Token bulundu: {'Evet' if BOT_TOKEN else 'Hayır'}")
    print(f"Chat ID bulundu: {'Evet' if CHAT_ID else 'Hayır'}")
    
    if BOT_TOKEN and CHAT_ID:
        from signal_tracker import ReminderBot
        
        async def test_reminder():
            reminder_bot = ReminderBot(BOT_TOKEN, CHAT_ID)
            
            # Test mesajı gönder
            await reminder_bot.bot.send_message(
                CHAT_ID,
                "🔔 <b>PlanB ULTRA Reminder System Aktif!</b>\n\n"
                "✅ Signal tracking başlatıldı\n"
                "✅ Günlük hatırlatmalar aktif\n"
                "✅ Her sabah 09:00'da otomatik kontrol\n\n"
                "💡 Artık AL sinyallerini unutmayacaksınız!",
                parse_mode="HTML"
            )
            print("✅ Test reminder gönderildi!")
            
        asyncio.run(test_reminder())
    else:
        print("❌ Telegram bilgileri bulunamadı")
        
except Exception as e:
    print(f"❌ Test hatası: {e}")
    
    # Fallback: Sistem process'lerini kontrol et
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'telegram_full_trader_with_sentiment.py' in result.stdout:
            print("🔍 Ana script çalışıyor durumda")
        else:
            print("⚠️ Ana script çalışmıyor olabilir")
    except:
        pass