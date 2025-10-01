#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PlanB ULTRA Reminder Configuration Helper"""

import json
import os
from pathlib import Path

def save_telegram_config():
    """Telegram config'ini kaydet"""
    print("🔧 PlanB ULTRA Reminder System Konfigürasyonu")
    print("=" * 50)
    
    bot_token = input("Telegram Bot Token: ").strip()
    chat_id = input("Telegram Chat ID: ").strip()
    
    if not bot_token or not chat_id:
        print("❌ Token ve Chat ID gerekli!")
        return False
        
    config = {
        "TELEGRAM_BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": chat_id,
        "REMINDER_ENABLED": True,
        "DAILY_REMINDER_TIME": "09:00"
    }
    
    config_path = Path("config/reminder_config.json")
    config_path.parent.mkdir(exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
        
    print(f"✅ Konfigürasyon kaydedildi: {config_path}")
    return True

def load_telegram_config():
    """Telegram config'ini yükle"""
    config_path = Path("config/reminder_config.json")
    
    if not config_path.exists():
        return None, None
        
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        return config.get("TELEGRAM_BOT_TOKEN"), config.get("TELEGRAM_CHAT_ID")
    except:
        return None, None

if __name__ == "__main__":
    success = save_telegram_config()
    
    if success:
        # Test config
        token, chat_id = load_telegram_config()
        print(f"\n✅ Test: Token {'✓' if token else '✗'}, Chat ID {'✓' if chat_id else '✗'}")
        
        print("\n🚀 Şimdi bu komutu çalıştırın:")
        print("python3 daily_reminder.py")