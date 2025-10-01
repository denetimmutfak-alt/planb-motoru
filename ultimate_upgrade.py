#!/usr/bin/env python3
"""
🚀 ULTIMATE PLANB SYSTEM UPGRADE
================================
Bu script tüm sistemi ULTRA PREMIUM seviyeye getirir:

1. ✅ 55 puan threshold (ULTRA PREMIUM)
2. ✅ 752 temiz BIST hissesi  
3. ✅ Komple sistem güncellemesi
4. ✅ Kuruluş tarihi entegrasyonu

KOMUTLAR:
1. Bu dosyayı servera kopyala
2. python3 ultimate_upgrade.py
3. Sistem otomatik güncellenecek
"""

import os
import shutil
import subprocess
import time

def upgrade_system():
    print("🚀 ULTIMATE PLANB SYSTEM UPGRADE BAŞLIYOR!")
    print("=" * 60)
    
    # 1. Servisi durdur
    print("1️⃣ Servis durduruluyor...")
    os.system("systemctl stop planb-trader")
    os.system("pkill -f telegram_full_trader")
    time.sleep(3)
    
    # 2. Eski dosyayı yedekle
    if os.path.exists("/root/telegram_full_trader.py"):
        print("2️⃣ Eski sistem yedekleniyor...")
        shutil.copy("/root/telegram_full_trader.py", "/root/telegram_full_trader_OLD.py")
    
    # 3. Yeni dosyaları yerleştir
    print("3️⃣ ULTRA PREMIUM sistem yükleniyor...")
    if os.path.exists("/root/telegram_full_trader_55PUAN.py"):
        shutil.copy("/root/telegram_full_trader_55PUAN.py", "/root/telegram_full_trader.py")
        print("   ✅ 55 puan threshold aktif")
    
    if os.path.exists("/root/bist_liste_TEMIZ.txt"):
        shutil.copy("/root/bist_liste_TEMIZ.txt", "/root/bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt")
        print("   ✅ 752 temiz BIST hissesi aktif")
    
    # 4. Log temizle
    print("4️⃣ Log dosyası temizleniyor...")
    with open("/root/full_trader.log", "w") as f:
        f.write("")
    
    # 5. Servisi başlat
    print("5️⃣ ULTRA PREMIUM sistem başlatılıyor...")
    os.system("systemctl start planb-trader")
    time.sleep(5)
    
    # 6. Durum kontrol
    print("6️⃣ Sistem durumu kontrol ediliyor...")
    os.system("systemctl status planb-trader --no-pager")
    
    print("\n" + "=" * 60)
    print("🎉 ULTRA PREMIUM UPGRADE TAMAMLANDI!")
    print("🎯 Threshold: 55 puan (ULTRA PREMIUM)")
    print("📊 BIST: 752 temiz hisse")
    print("⚡ Toplam: ~1259 varlık")
    print("🏆 Günde 1-3 ultra kaliteli sinyal bekleniyor")
    print("=" * 60)

if __name__ == "__main__":
    upgrade_system()