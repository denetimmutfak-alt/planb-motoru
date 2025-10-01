#!/usr/bin/env python3
"""
PlanB Motoru - Monitoring Daemon
5 dakikada bir sistem sağlığını kontrol eder
"""

import time
import subprocess
import requests
import os
import logging
from datetime import datetime

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/monitoring.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN', '')
CHAT_ID = os.getenv('CHAT_ID', '')

def send_telegram_alert(message):
    """Telegram'a uyarı gönder"""
    if not BOT_TOKEN or not CHAT_ID:
        logger.warning("Telegram bot token veya chat ID eksik")
        return
    
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': CHAT_ID,
            'text': f"🚨 PlanB Motoru Uyarısı\n{message}\n\nZaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            logger.info("Telegram uyarısı gönderildi")
        else:
            logger.error(f"Telegram uyarısı gönderilemedi: {response.status_code}")
    except Exception as e:
        logger.error(f"Telegram uyarısı hatası: {e}")

def check_api_health():
    """API sağlığını kontrol et"""
    try:
        response = requests.get('http://planb-api:8000/health', timeout=10)
        if response.status_code == 200:
            logger.info("API sağlıklı")
            return True
        else:
            logger.error(f"API sağlıksız: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error("API'ye bağlanılamıyor")
        return False
    except Exception as e:
        logger.error(f"API health check hatası: {e}")
        return False

def check_database():
    """Veritabanı sağlığını kontrol et"""
    try:
        result = subprocess.run([
            'python', '-c', 
            """
import sqlite3
import sys
try:
    conn = sqlite3.connect('/app/data/planb_motoru.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM market_data')
    count = cursor.fetchone()[0]
    print(f'Database OK: {count} records')
    conn.close()
    sys.exit(0)
except Exception as e:
    print(f'Database ERROR: {e}')
    sys.exit(1)
"""
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            logger.info(f"Database sağlıklı: {result.stdout.strip()}")
            return True
        else:
            logger.error(f"Database hatası: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("Database kontrolü zaman aşımı")
        return False
    except Exception as e:
        logger.error(f"Database check hatası: {e}")
        return False

def check_disk_space():
    """Disk alanını kontrol et"""
    try:
        result = subprocess.run(['df', '-h', '/app'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 5:
                usage_percent = int(parts[4].replace('%', ''))
                if usage_percent > 80:
                    logger.warning(f"Disk kullanımı yüksek: %{usage_percent}")
                    return False
                else:
                    logger.info(f"Disk kullanımı normal: %{usage_percent}")
                    return True
    except Exception as e:
        logger.error(f"Disk space check hatası: {e}")
    return True

def health_check():
    """Genel sistem sağlık kontrolü"""
    logger.info("🔍 Sistem sağlık kontrolü başlıyor...")
    
    errors = []
    
    # API kontrolü
    if not check_api_health():
        errors.append("API servis hatası")
    
    # Database kontrolü
    if not check_database():
        errors.append("Database erişim hatası")
    
    # Disk alanı kontrolü
    if not check_disk_space():
        errors.append("Disk alanı yetersiz")
    
    if errors:
        error_message = "\n".join([f"❌ {error}" for error in errors])
        logger.error(f"Sistem hataları tespit edildi:\n{error_message}")
        send_telegram_alert(f"Sistem kontrol hatası:\n{error_message}")
    else:
        logger.info("✅ Tüm sistemler normal çalışıyor")

def main():
    """Ana döngü"""
    logger.info("🚀 PlanB Motoru Monitoring Daemon başlatıldı")
    
    # İlk kontrol
    health_check()
    
    # 5 dakikalık döngü
    while True:
        try:
            time.sleep(300)  # 5 dakika bekle
            health_check()
        except KeyboardInterrupt:
            logger.info("Monitoring daemon durduruldu")
            break
        except Exception as e:
            logger.error(f"Monitoring daemon hatası: {e}")
            time.sleep(60)  # Hata durumunda 1 dakika bekle

if __name__ == "__main__":
    main()