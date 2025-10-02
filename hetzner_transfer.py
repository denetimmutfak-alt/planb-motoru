#!/usr/bin/env python3
"""
BIST 724 Listesini Hetzner'a SSH ile Transfer
"""

import paramiko
import os

def transfer_bist_list():
    """BIST listesini SSH ile Hetzner'a transfer et"""
    
    # SSH bağlantı bilgileri
    hostname = "116.203.57.250"
    username = "root"
    password = input("Hetzner SSH şifresi: ")
    
    # Yerel dosya
    local_file = "BIST_GUNCEL_TAM_LISTE_NEW.txt"
    remote_file = "/root/PlanB_Motoru/BIST_GUNCEL_TAM_LISTE_NEW.txt"
    
    if not os.path.exists(local_file):
        print(f"❌ Yerel dosya bulunamadı: {local_file}")
        return False
    
    try:
        print("🔄 SSH bağlantısı kuruluyor...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        
        print("📤 Dosya transfer ediliyor...")
        sftp = ssh.open_sftp()
        sftp.put(local_file, remote_file)
        sftp.close()
        
        # Kontrol
        stdin, stdout, stderr = ssh.exec_command(f"wc -l {remote_file}")
        line_count = stdout.read().decode().strip()
        print(f"✅ Transfer başarılı: {line_count}")
        
        # Kuruluş tarihleri modülünü de transfer et
        local_py = "bist_kurulus_tarihleri_724.py"
        remote_py = "/root/PlanB_Motoru/bist_kurulus_tarihleri_724.py"
        
        if os.path.exists(local_py):
            print("📤 Kuruluş tarihleri modülü transfer ediliyor...")
            sftp = ssh.open_sftp()
            sftp.put(local_py, remote_py)
            sftp.close()
            print("✅ Kuruluş tarihleri modülü transfer edildi")
        
        # Telegram bot'u restart et
        print("🔄 Telegram bot'u restart ediliyor...")
        stdin, stdout, stderr = ssh.exec_command("systemctl restart planb")
        
        print("📊 Final kontrol...")
        stdin, stdout, stderr = ssh.exec_command("systemctl status planb --no-pager")
        status = stdout.read().decode()
        if "active (running)" in status:
            print("✅ Telegram bot aktif çalışıyor")
        else:
            print("❌ Telegram bot sorunu var")
        
        ssh.close()
        return True
        
    except Exception as e:
        print(f"❌ Transfer hatası: {e}")
        return False

if __name__ == "__main__":
    print("🚀 BIST 724 HETZNER TRANSFER")
    print("="*40)
    
    success = transfer_bist_list()
    if success:
        print("\n🎉 Transfer başarıyla tamamlandı!")
        print("✅ BIST 724 hisse listesi Hetzner'da aktif")
        print("✅ Telegram bot güncellendi")
    else:
        print("\n❌ Transfer başarısız!")