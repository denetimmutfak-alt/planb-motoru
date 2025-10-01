#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PlanB ULTRA Reminder System Basit Test
Mevcut sistemdeki Telegram fonksiyonunu kullanır.
"""

import sys
import os

# Ana scriptten Telegram fonksiyonunu import et
try:
    from telegram_full_trader_with_sentiment import send_telegram_message
    
    print("🔔 PlanB ULTRA Reminder System Test")
    print("=" * 40)
    
    # Test mesajı
    test_message = (
        "🔔 <b>PlanB ULTRA Reminder System Aktif!</b>\n\n"
        "✅ Signal tracking başlatıldı\n"
        "✅ Günlük hatırlatmalar aktif (09:00)\n"
        "✅ Otomatik SAT uyarıları çalışıyor\n\n"
        "💡 Artık AL sinyallerini unutmayacaksınız!\n\n"
        "🎯 Test mesajı: " + str(os.getpid())
    )
    
    if send_telegram_message(test_message):
        print("✅ Test mesajı başarıyla gönderildi!")
        
        # Signal tracker test
        try:
            from signal_tracker import SignalTracker
            tracker = SignalTracker()
            print("✅ Signal Tracker modülü çalışıyor")
            
            # Test signal ekle
            tracker.add_signal("TEST.IS", "AL", 75.5, 100.50, "2-4 hafta")
            print("✅ Test signal eklendi")
            
        except Exception as e:
            print(f"⚠️ Signal tracker hatası: {e}")
            
    else:
        print("❌ Test mesajı gönderilemedi")
        print("Muhtemelen TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID ayarlanmamış")
        
except ImportError as e:
    print(f"❌ Import hatası: {e}")
except Exception as e:
    print(f"❌ Test hatası: {e}")