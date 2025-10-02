#!/usr/bin/env python3
"""
Hızlı sunucu durum kontrolü
"""

import subprocess
import os

print("=== HETZNER SUNUCU DURUM KONTROLÜ ===\n")

# Hetzner IP'sini bulalım
print("🔍 HETZNER SUNUCU BİLGİLERİ:")
print("Lütfen aşağıdaki bilgileri kontrol edin:\n")

print("1. Hetzner Cloud Console'dan IP adresinizi alın")
print("2. SSH bağlantısını test edin:")
print("   ssh root@HETZNER_IP")
print("\n3. Sunucuda servisleri kontrol edin:")
print("   sudo systemctl status planb")
print("   sudo systemctl status docker")
print("   docker ps")

print("\n🤖 TELEGRAM BOT DURUMU:")
print("Telegram bot şu an nerede çalışıyor?")
print("a) Bu Windows bilgisayarda (Terminal/PowerShell'de)")
print("b) Hetzner sunucusunda (systemd servisi olarak)")
print("c) Docker container'da")

print("\n📋 KONTROL LİSTESİ:")
print("□ Hetzner sunucusu açık mı?")
print("□ SSH bağlantısı çalışıyor mu?") 
print("□ Docker servisleri ayakta mı?")
print("□ planb systemd servisi aktif mi?")
print("□ Telegram bot token'ı doğru mu?")

print(f"\n💡 ÇÖZÜM:")
print("Eğer bot Windows'ta çalışıyorsa -> Hetzner'a taşımalıyız")
print("Eğer bot Hetzner'da çalışıyorsa -> Servis enable edilmeli")

print(f"\n🚀 SONRAKI ADIM:")
print("Hetzner IP adresinizi paylaşın, birlikte kontrol edelim!")