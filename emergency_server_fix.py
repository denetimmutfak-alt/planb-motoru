#!/usr/bin/env python3
"""
Hetzner Sunucu Acil Durum Kontrolü
"""

print("🚨 HETZNER SUNUCU ACİL DURUM KONTROLÜ")
print("="*50)

print("\n📋 KONTROL LİSTESİ:")
print("1. Hetzner Cloud Console'a gidin")
print("2. CPX31 (PlanB-Motor) sunucusunu bulun")
print("3. Status'ü kontrol edin:")
print("   ✅ Running (Yeşil) = Sunucu açık")
print("   🔴 Stopped (Kırmızı) = Sunucu kapalı")
print("   🟡 Starting = Başlatılıyor")

print("\n🔧 ACİL ÇÖZÜM ADIMLARI:")
print("Eğer sunucu KAPALI ise:")
print("  → Actions > Power On")
print("  → 2-3 dakika bekleyin")
print("  → SSH'ı tekrar deneyin")

print("\nEğer sunucu AÇIK ama SSH çalışmıyor ise:")
print("  → Actions > Console")
print("  → Web terminal ile giriş yapın")
print("  → systemctl status sshd kontrol edin")

print("\n🤖 TELEGRAM BOT DURUMU:")
print("SORUN: Sunucuya erişemediğimiz için")
print("Telegram bot şu an büyük ihtimalle:")
print("❌ Sunucuda çalışmıyor")
print("❌ Windows'ta da çalışmıyor")
print("= TELEGRAM MESAJLARI KESİK!")

print("\n🚀 ACİL EYLEM PLANI:")
print("1. Hetzner Console → Sunucuyu başlatın")
print("2. SSH erişimini restore edin") 
print("3. systemctl enable planb && systemctl start planb")
print("4. Telegram bot'u yeniden başlatın")

print("\n💡 İLERİDE ÖNLEM:")
print("Bu sorunu bir daha yaşamamak için:")
print("- Auto-restart politikası")
print("- Monitoring sistemi")
print("- Backup plan hazırlayalım")

print(f"\n🔄 ŞİMDİ YAPMANIZ GEREKEN:")
print("Hetzner Console'dan sunucuyu başlatın ve bana bildirin!")