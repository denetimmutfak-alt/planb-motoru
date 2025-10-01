#!/usr/bin/env python3
"""
🚀 ULTIMATE PlanB SYSTEM FIX
============================
Bu script tüm sorunları çözecek:
1. Doğru BIST TAM LİSTESİ (488 firma)
2. Güncel telegram_full_trader.py
3. Tüm varlık listelerini servera yükler
4. Servisi yeniden başlatır
"""

import subprocess
import os
import time

# Kopyalanacak dosyalar
FILES_TO_COPY = [
    "telegram_full_trader.py",
    "bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt", 
    "nasdaq tam liste.txt",
    "kripto tam liste.txt", 
    "emtia tam liste.txt",
    "XETRA TAM LİSTE-.txt"
]

SERVER = "root@116.203.57.250"
SERVER_PATH = "/root/"

def run_command(cmd):
    """Komutu çalıştır ve sonucu döndür"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def copy_files():
    """Tüm dosyaları servera kopyala"""
    print("🚀 Dosyalar servera kopyalanıyor...")
    
    for file in FILES_TO_COPY:
        if not os.path.exists(file):
            print(f"❌ Dosya bulunamadı: {file}")
            continue
            
        print(f"📁 Kopyalanıyor: {file}")
        cmd = f'scp -o StrictHostKeyChecking=no "{file}" {SERVER}:{SERVER_PATH}'
        success, stdout, stderr = run_command(cmd)
        
        if success:
            print(f"✅ {file} başarıyla kopyalandı")
        else:
            print(f"❌ {file} kopyalanamadı: {stderr}")

def restart_service():
    """Servisi yeniden başlat"""
    print("🔄 Servis yeniden başlatılıyor...")
    
    commands = [
        "systemctl stop planb-trader",
        "pkill -f telegram_full_trader",
        "sleep 3", 
        "systemctl start planb-trader",
        "systemctl status planb-trader --no-pager"
    ]
    
    for cmd in commands:
        print(f"🔧 Çalıştırılıyor: {cmd}")
        ssh_cmd = f'ssh {SERVER} "{cmd}"'
        success, stdout, stderr = run_command(ssh_cmd)
        
        if stdout:
            print(f"📤 {stdout}")
        if stderr:
            print(f"📥 {stderr}")

def check_system():
    """Sistem durumunu kontrol et"""
    print("🔍 Sistem durumu kontrol ediliyor...")
    
    check_commands = [
        "ls -la /root/*.txt | head -10",
        "head -5 /root/telegram_full_trader.py",
        "systemctl is-active planb-trader",
        "tail -10 /root/full_trader.log"
    ]
    
    for cmd in check_commands:
        print(f"\n🔍 {cmd}")
        ssh_cmd = f'ssh {SERVER} "{cmd}"'
        success, stdout, stderr = run_command(ssh_cmd)
        
        if stdout:
            print(stdout)
        if stderr and "Warning" not in stderr:
            print(f"❌ {stderr}")

if __name__ == "__main__":
    print("🚀 ULTIMATE PlanB SYSTEM FIX BAŞLIYOR!")
    print("=" * 50)
    
    # 1. Dosyaları kopyala
    copy_files()
    
    print("\n" + "=" * 50)
    
    # 2. Servisi yeniden başlat
    restart_service()
    
    print("\n" + "=" * 50)
    
    # 3. Sistem durumunu kontrol et
    check_system()
    
    print("\n🎉 ULTIMATE SYSTEM FIX TAMAMLANDI!")
    print("✅ Tüm dosyalar güncellenmiş olmalı")
    print("✅ Servis yeniden başlatılmış olmalı") 
    print("✅ Sistem 991+ varlık analizi yapacak")