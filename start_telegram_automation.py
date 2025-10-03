#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱⚡ TELEGRAM ULTRA AUTOMATION BAŞLATICI ⚡📱
Her 60 dakikada bir otomatik Telegram mesajları başlatır

KULLANIM:
1. .env dosyasına TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID ekleyin
2. Bu dosyayı çalıştırın: python start_telegram_automation.py
3. Sistem 60 dakikada bir mesaj gönderecek
4. Ana sinyaller ↔ Hacim patlaması rotasyonu aktif

Created: 2025-10-03
Author: Ultra Automation Team
Version: v27.0 Production
"""

import os
import sys
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_environment():
    """Environment variables kontrolü"""
    print("🔧 Environment Variables kontrolü...")
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN bulunamadı!")
        print("   Lütfen .env dosyasına ekleyin: TELEGRAM_BOT_TOKEN=your_bot_token")
        return False
    
    if not chat_id:
        print("❌ TELEGRAM_CHAT_ID bulunamadı!")
        print("   Lütfen .env dosyasına ekleyin: TELEGRAM_CHAT_ID=your_chat_id")
        return False
    
    print(f"✅ TELEGRAM_BOT_TOKEN: {token[:10]}...")
    print(f"✅ TELEGRAM_CHAT_ID: {chat_id}")
    return True

def start_automation():
    """Telegram otomasyonunu başlat"""
    try:
        print("🚀 PlanB Ultra Telegram Automation başlatılıyor...")
        
        # Environment check
        if not check_environment():
            return False
        
        # Import and start main system
        print("📱 Ana sistem yükleniyor...")
        from telegram_full_trader_with_sentiment import planb_ultra_system
        
        print(f"✅ Sistem versiyonu: {planb_ultra_system.version}")
        
        # Check telegram scheduler
        if not planb_ultra_system.telegram_scheduler:
            print("❌ Telegram scheduler bulunamadı!")
            print("   TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID'yi kontrol edin")
            return False
        
        print("✅ Telegram scheduler hazır")
        
        # Start automation
        print("⏰ 60 dakikalık otomatik mesajlar başlatılıyor...")
        success = planb_ultra_system.start_telegram_automation()
        
        if success:
            print("🎉 TELEGRAM AUTOMATION BAŞLATILDI!")
            print("="*50)
            print("📱 Her 60 dakikada otomatik mesaj gönderilecek")
            print("🔄 Ana Sinyaller ↔ Hacim Patlaması rotasyonu")
            print("🧠 27-Modül Meta-Enhanced formatı")
            print("📱 Mobile-optimized design")
            print("🇹🇷 Turkish localized content")
            print("="*50)
            
            # Status göster
            status = planb_ultra_system.get_telegram_status()
            if status.get('next_run_time'):
                print(f"⏰ Sonraki mesaj: {status['next_run_time']}")
            
            print("\n🔄 Sistem çalışıyor... (Ctrl+C ile durdurun)")
            
            # Keep alive
            try:
                while True:
                    time.sleep(60)  # Check every minute
                    
                    # Status update her 10 dakikada
                    if datetime.now().minute % 10 == 0:
                        status = planb_ultra_system.get_telegram_status()
                        print(f"⏰ Durum: {status.get('is_running', False)} | Son mesaj: {status.get('last_message_time', 'Henüz gönderilmedi')}")
                        
            except KeyboardInterrupt:
                print("\n⏹️ Kullanıcı tarafından durduruldu")
                planb_ultra_system.stop_telegram_automation()
                print("✅ Telegram automation durduruldu")
                return True
        else:
            print("❌ Telegram automation başlatılamadı!")
            return False
            
    except Exception as e:
        print(f"❌ Başlatma hatası: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ana fonksiyon"""
    print("📱⚡ TELEGRAM ULTRA AUTOMATION ⚡📱")
    print("=" * 50)
    print("🚀 PlanB Ultra Trading System")
    print("⏰ 60 Dakikalık Otomatik Mesaj Sistemi")
    print("🧠 27-Modül Meta-Enhanced Analysis")
    print("=" * 50)
    
    success = start_automation()
    
    if success:
        print("\n✅ Sistem başarıyla tamamlandı")
    else:
        print("\n❌ Sistem başlatılamadı")
        print("📋 Kontrol Listesi:")
        print("   1. .env dosyasında TELEGRAM_BOT_TOKEN var mı?")
        print("   2. .env dosyasında TELEGRAM_CHAT_ID var mı?")
        print("   3. Bot token'ı geçerli mi?")
        print("   4. Chat ID doğru mu?")
        print("   5. Internet bağlantısı var mı?")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)