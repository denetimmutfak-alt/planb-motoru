#!/usr/bin/env python3
"""
BIST Master Liste Entegrasyonu
724 hisselik düzenli listeyi sisteme entegre eder
"""

import os
import shutil
from datetime import datetime

def bist_liste_entegrasyonu():
    """BIST 724 master listesini sisteme entegre et"""
    
    print("🔄 BIST MASTER LİSTE ENTEGRASYONU BAŞLIYOR...")
    print("="*60)
    
    # 1. Yeni master liste dosyası
    master_file = "BIST_724_MASTER_LISTE_FULL.txt"
    
    if not os.path.exists(master_file):
        print(f"❌ Master liste bulunamadı: {master_file}")
        return
    
    # 2. Master listeyi oku
    with open(master_file, "r", encoding="utf-8") as f:
        master_content = f.read()
    
    master_lines = [line.strip() for line in master_content.split('\n') 
                   if line.strip() and not line.startswith('#')]
    
    print(f"✅ Master liste okundu: {len(master_lines)} hisse")
    
    # 3. Eski BIST dosyalarını yedekle
    backup_folder = f"bist_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_folder, exist_ok=True)
    
    eski_dosyalar = [
        "BIST_GUNCEL_TAM_LISTE_NEW.txt",
        "bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt",
        "bist_guncel_listesi.csv",
        "bist_liste_TEMIZ.txt"
    ]
    
    for dosya in eski_dosyalar:
        if os.path.exists(dosya):
            shutil.move(dosya, os.path.join(backup_folder, dosya))
            print(f"📦 Yedeklendi: {dosya}")
    
    # 4. Yeni standart dosyaları oluştur
    print(f"\n🎯 YENİ STANDART DOSYALAR OLUŞTURULUYOR...")
    
    # Ana BIST listesi
    with open("BIST_GUNCEL_TAM_LISTE_NEW.txt", "w", encoding="utf-8") as f:
        f.write(f"# BIST 724 Hisse - Standart Liste\n")
        f.write(f"# Güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
        f.write(f"# Toplam: {len(master_lines)} hisse\n\n")
        f.write('\n'.join(master_lines))
    
    # Sadece kodlar (modüller için)
    kodlar = []
    for line in master_lines:
        if ' - ' in line:
            kod = line.split(' - ')[0].strip()
            if kod:
                kodlar.append(kod)
    
    with open("bist_kodlar_724.txt", "w", encoding="utf-8") as f:
        f.write('\n'.join(kodlar))
    
    # Kuruluş tarihleri sözlüğü
    kurulus_sozluk = {}
    for line in master_lines:
        parts = line.split(' - ')
        if len(parts) >= 3:
            kod = parts[0].strip()
            tarih = parts[2].strip()
            kurulus_sozluk[kod] = tarih
    
    # Python sözlük dosyası
    with open("bist_kurulus_tarihleri_724.py", "w", encoding="utf-8") as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('# -*- coding: utf-8 -*-\n')
        f.write(f'"""\nBIST 724 Hisse Kuruluş Tarihleri\n')
        f.write(f'Güncelleme: {datetime.now().strftime("%d.%m.%Y %H:%M")}\n"""\n\n')
        f.write('BIST_KURULUS_TARIHLERI = {\n')
        for kod, tarih in sorted(kurulus_sozluk.items()):
            f.write(f'    "{kod}": "{tarih}",\n')
        f.write('}\n\n')
        f.write(f'# Toplam: {len(kurulus_sozluk)} hisse\n')
    
    print(f"✅ BIST_GUNCEL_TAM_LISTE_NEW.txt: {len(master_lines)} satır")
    print(f"✅ bist_kodlar_724.txt: {len(kodlar)} kod")
    print(f"✅ bist_kurulus_tarihleri_724.py: {len(kurulus_sozluk)} tarih")
    
    # 5. Modül referanslarını güncelleme önerileri
    print(f"\n📋 MODÜL GÜNCELLEMELER:")
    guncellenecek_dosyalar = [
        "check_deployment_status.py",
        "foundation_date_count.py", 
        "foundation_date_integration.py",
        "foundation_date_processor.py",
        "generate_real_symbols.py",
        "bist_liste_temizleyici.py"
    ]
    
    for dosya in guncellenecek_dosyalar:
        if os.path.exists(dosya):
            print(f"🔧 Güncellenecek: {dosya}")
    
    print(f"\n🎉 ENTEGRASYON TAMAMLANDI!")
    print(f"📁 Yedek klasör: {backup_folder}")
    print(f"🎯 Yeni standart: BIST_GUNCEL_TAM_LISTE_NEW.txt ({len(master_lines)} hisse)")

if __name__ == "__main__":
    bist_liste_entegrasyonu()