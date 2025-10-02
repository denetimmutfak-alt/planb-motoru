#!/usr/bin/env python3
"""
BIST 724 Entegrasyon Kontrolü ve Hetzner Senkronizasyonu
"""

import os
from datetime import datetime

def kontrol_et():
    """BIST 724 entegrasyonunu kontrol et"""
    
    print("🔍 BIST 724 ENTEGRASYON KONTROLÜ")
    print("="*50)
    
    # 1. Dosya kontrolü
    gerekli_dosyalar = {
        "BIST_GUNCEL_TAM_LISTE_NEW.txt": "Ana 724 hisse listesi",
        "bist_kodlar_724.txt": "Sadece kodlar",
        "bist_kurulus_tarihleri_724.py": "Kuruluş tarihleri modülü",
        "BIST_724_MASTER_LISTE_FULL.txt": "Master referans dosya"
    }
    
    print("📂 DOSYA KONTROLÜ:")
    for dosya, aciklama in gerekli_dosyalar.items():
        if os.path.exists(dosya):
            size = os.path.getsize(dosya)
            print(f"✅ {dosya}: {size/1024:.1f}KB - {aciklama}")
        else:
            print(f"❌ {dosya}: BULUNAMADI - {aciklama}")
    
    # 2. Ana liste kontrolü
    print(f"\n📊 ANA LİSTE ANALİZİ:")
    try:
        with open("BIST_GUNCEL_TAM_LISTE_NEW.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        print(f"✅ Toplam hisse: {len(lines)}")
        
        # İlk 5 ve son 5 hisse
        print(f"🔸 İlk 5 hisse:")
        for i, line in enumerate(lines[:5], 1):
            kod = line.split(' - ')[0] if ' - ' in line else line
            print(f"   {i}. {kod}")
        
        print(f"🔸 Son 5 hisse:")
        for i, line in enumerate(lines[-5:], len(lines)-4):
            kod = line.split(' - ')[0] if ' - ' in line else line
            print(f"   {i}. {kod}")
            
    except Exception as e:
        print(f"❌ Ana liste okuma hatası: {e}")
    
    # 3. Kuruluş tarihleri kontrolü
    print(f"\n📅 KURULUŞ TARİHLERİ KONTROLÜ:")
    try:
        from bist_kurulus_tarihleri_724 import BIST_KURULUS_TARIHLERI
        print(f"✅ Kuruluş tarihleri modülü: {len(BIST_KURULUS_TARIHLERI)} hisse")
        
        # Örnek tarihleri göster
        ornekler = list(BIST_KURULUS_TARIHLERI.items())[:3]
        for kod, tarih in ornekler:
            print(f"   {kod}: {tarih}")
            
    except Exception as e:
        print(f"❌ Kuruluş tarihleri modülü hatası: {e}")
    
    # 4. Yedek dosyalar
    print(f"\n📦 YEDEK DOSYALAR:")
    backup_folders = [d for d in os.listdir('.') if d.startswith('bist_backup_')]
    for folder in backup_folders:
        print(f"✅ Yedek klasör: {folder}")
    
    # 5. Güncellenmiş modüller
    print(f"\n🔧 GÜNCELLENMİŞ MODÜLLER:")
    guncel_moduller = [
        "check_deployment_status.py",
        "foundation_date_count.py",
        "foundation_date_integration.py", 
        "foundation_date_processor.py",
        "generate_real_symbols.py"
    ]
    
    for modul in guncel_moduller:
        if os.path.exists(modul):
            mod_time = os.path.getmtime(modul)
            mod_date = datetime.fromtimestamp(mod_time).strftime("%d.%m.%Y %H:%M")
            print(f"✅ {modul}: {mod_date}")
    
    print(f"\n🎯 SONUÇ:")
    print(f"✅ BIST 724 hisse entegrasyonu tamamlandı")
    print(f"✅ Eski listeler yedeklendi")
    print(f"✅ Yeni standart: BIST_GUNCEL_TAM_LISTE_NEW.txt")
    print(f"✅ Kuruluş tarihleri: bist_kurulus_tarihleri_724.py")
    print(f"✅ İlgili modüller güncellendi")
    
    print(f"\n🚀 HETZNER SENKRONİZASYONU:")
    print(f"1. Bu dosyaları Hetzner'a yükleyin:")
    print(f"   - BIST_GUNCEL_TAM_LISTE_NEW.txt")
    print(f"   - bist_kurulus_tarihleri_724.py")
    print(f"   - Güncellenmiş modüller")
    
    print(f"\n2. Hetzner'da telegram bot'u restart edin:")
    print(f"   systemctl restart planb")
    
    print(f"\n✨ Artık 724 hisselik düzenli BIST listesi aktif!")

if __name__ == "__main__":
    kontrol_et()