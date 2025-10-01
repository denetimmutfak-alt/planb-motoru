#!/usr/bin/env python3
"""
PlanB Motoru - Sistem Durum Kontrol Paneli
Bulut Sunucu, Veri Akışı ve Telegram Bot Kontrolü
"""

import requests
import sqlite3
import os
import subprocess
import json
from datetime import datetime, timedelta

class SistemKontrolPaneli:
    def __init__(self):
        self.local_api = "http://localhost:8001"
        self.local_dashboard = "http://localhost:8080"
        self.db_path = "data/planb_ultra.db"
        
        # Bulut sunucu bilgileri (eğer varsa)
        self.cloud_api = "https://your-cloud-server.com/api"  # Değiştirin
        self.cloud_dashboard = "https://your-cloud-dashboard.com"  # Değiştirin
        
    def print_header(self, title):
        print("\n" + "="*60)
        print(f"🔍 {title}")
        print("="*60)
    
    def kontrol_local_sunucu(self):
        """Local sunucu durumunu kontrol et"""
        self.print_header("LOCAL SUNUCU DURUMU")
        
        try:
            response = requests.get(f"{self.local_api}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print("✅ LOCAL API SUNUCU: ÇALIŞIYOR")
                print(f"   🎯 Status: {health_data.get('status', 'unknown')}")
                print(f"   📊 Database: {health_data.get('database', {}).get('status', 'unknown')}")
                print(f"   🤖 ML Engine: {health_data.get('services', {}).get('ml_engine', 'unknown')}")
                return True
            else:
                print(f"❌ LOCAL API SUNUCU: HATA - Status Code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ LOCAL API SUNUCU: KAPALI - Bağlantı reddedildi")
            print("💡 Çözüm: 'python ultra_api_server.py' ile başlatın")
            return False
        except Exception as e:
            print(f"❌ LOCAL API SUNUCU: HATA - {e}")
            return False
    
    def kontrol_bulut_sunucu(self):
        """Bulut sunucu durumunu kontrol et"""
        self.print_header("BULUT SUNUCU DURUMU")
        
        # Hetzner veya başka bulut sağlayıcı kontrolü
        print("🔍 Bulut sunucu kontrolü yapılıyor...")
        
        try:
            # Eğer bulut sunucu URL'i ayarlanmışsa test et
            if "your-cloud-server.com" not in self.cloud_api:
                response = requests.get(f"{self.cloud_api}/health", timeout=10)
                if response.status_code == 200:
                    print("✅ BULUT SUNUCU: AKTİF")
                    health_data = response.json()
                    print(f"   🌐 URL: {self.cloud_api}")
                    print(f"   🎯 Status: {health_data.get('status', 'unknown')}")
                    return True
                else:
                    print(f"❌ BULUT SUNUCU: HATA - Status: {response.status_code}")
                    return False
            else:
                print("⚠️  BULUT SUNUCU: AYARLANMAMIŞ")
                print("💡 Bilgi: Bulut sunucu URL'lerini ayarlayın:")
                print("   • self.cloud_api = 'https://your-hetzner-server.com/api'")
                print("   • self.cloud_dashboard = 'https://your-dashboard.com'")
                return None
                
        except requests.exceptions.ConnectionError:
            print("❌ BULUT SUNUCU: ULAŞILAMIYOR")
            return False
        except Exception as e:
            print(f"❌ BULUT SUNUCU: HATA - {e}")
            return False
    
    def kontrol_veri_akisi(self):
        """Veri akışının sorunsuz olup olmadığını kontrol et"""
        self.print_header("VERİ AKIŞI DURUMU")
        
        try:
            # Database bağlantısını kontrol et
            if os.path.exists(self.db_path):
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Son veri girişini kontrol et
                cursor.execute("SELECT MAX(timestamp), COUNT(*) FROM market_data WHERE timestamp > datetime('now', '-1 hour')")
                latest_time, recent_count = cursor.fetchone()
                
                print(f"✅ DATABASE: Bağlantı başarılı")
                print(f"   📊 Database boyutu: {os.path.getsize(self.db_path)/1024/1024:.2f} MB")
                
                if latest_time:
                    latest_dt = datetime.fromisoformat(latest_time)
                    time_diff = datetime.now() - latest_dt
                    
                    if time_diff < timedelta(hours=1):
                        print(f"✅ VERİ TÜRETİLMESİ: GÜNCEL")
                        print(f"   ⏰ Son veri: {latest_time[:19]}")
                        print(f"   📈 Son 1 saatte: {recent_count} kayıt")
                    else:
                        print(f"⚠️  VERİ TÜRETİLMESİ: ESKİ")
                        print(f"   ⏰ Son veri: {latest_time[:19]} ({time_diff} önce)")
                else:
                    print("❌ VERİ TÜRETİLMESİ: VERİ YOK")
                
                # Market data analizi
                cursor.execute("SELECT market, COUNT(*) FROM market_data GROUP BY market")
                market_counts = cursor.fetchall()
                
                print(f"📊 MARKET DAĞILIMI:")
                for market, count in market_counts:
                    print(f"   • {market}: {count} kayıt")
                
                # Analiz sonuçları kontrolü
                cursor.execute("SELECT COUNT(*) FROM analysis_results WHERE timestamp > datetime('now', '-24 hours')")
                analysis_count = cursor.fetchone()[0]
                
                print(f"🤖 ML ANALİZ SONUÇLARI:")
                print(f"   • Son 24 saatte: {analysis_count} analiz")
                
                conn.close()
                return True
                
            else:
                print("❌ DATABASE: Dosya bulunamadı")
                print(f"💡 Çözüm: 'python ultra_database.py' ile database oluşturun")
                return False
                
        except Exception as e:
            print(f"❌ VERİ AKIŞI: HATA - {e}")
            return False
    
    def kontrol_telegram_bot(self):
        """Telegram bot durumunu kontrol et"""
        self.print_header("TELEGRAM BOT DURUMU")
        
        # Bot token kontrolü
        try:
            with open('ultra_telegram_bot.py', 'r', encoding='utf-8') as f:
                bot_content = f.read()
                
            if 'YOUR_BOT_TOKEN_HERE' in bot_content:
                print("❌ TELEGRAM BOT: TOKEN AYARLANMAMIŞ")
                print("💡 Çözüm:")
                print("   1. @BotFather ile yeni bot oluşturun")
                print("   2. ultra_telegram_bot.py dosyasında BOT_TOKEN ayarlayın")
                print("   3. CHAT_ID'nizi ayarlayın")
                return False
            else:
                print("✅ TELEGRAM BOT: Token ayarlanmış")
                
                # Bot çalışıyor mu kontrol et
                try:
                    response = requests.get(f"{self.local_api}/api/v1/telegram/status", timeout=5)
                    if response.status_code == 200:
                        telegram_data = response.json()
                        print("✅ TELEGRAM ENTEGRASYONU: AKTİF")
                        print(f"   🤖 Status: {telegram_data.get('status', 'unknown')}")
                        print(f"   📱 Bot configured: {telegram_data.get('bot_configured', False)}")
                        print(f"   🔔 Auto execute: {telegram_data.get('auto_execute_enabled', False)}")
                        return True
                    else:
                        print("⚠️  TELEGRAM ENTEGRASYONU: API'den yanıt yok")
                        return None
                except requests.exceptions.ConnectionError:
                    print("⚠️  TELEGRAM ENTEGRASYONU: API kapalı")
                    return None
                    
        except FileNotFoundError:
            print("❌ TELEGRAM BOT: Dosya bulunamadı")
            return False
        except Exception as e:
            print(f"❌ TELEGRAM BOT: HATA - {e}")
            return False
    
    def telegram_test_komutu(self):
        """Telegram bot test komutları"""
        self.print_header("TELEGRAM BOT TEST KOMUTLARI")
        
        print("🤖 Bot'unuzu test etmek için:")
        print("   • /start - Bot'u başlat")
        print("   • /status - Sistem durumu")
        print("   • /signals - Son sinyaller")
        print("   • /stats - İstatistikler")
        print("")
        print("📱 Bot'unuzu bulma:")
        print("   1. Telegram'da bot_username'inizi arayın")
        print("   2. /start komutu ile başlatın")
        print("   3. Chat ID'nizi alın ve ayarlayın")
    
    def sistem_baslat_komutu(self):
        """Sistem başlatma komutları"""
        self.print_header("SİSTEM BAŞLATMA KOMUTLARI")
        
        print("🚀 Sistemi başlatmak için:")
        print("")
        print("1️⃣ DATABASE başlat:")
        print("   python ultra_database.py")
        print("")
        print("2️⃣ API SERVER başlat:")
        print("   python ultra_api_server.py")
        print("")
        print("3️⃣ DASHBOARD başlat:")
        print("   python quick_test_dashboard.py")
        print("")
        print("4️⃣ MARKET DATA PIPELINE başlat:")
        print("   python ultra_market_pipeline.py")
        print("")
        print("5️⃣ TELEGRAM BOT başlat (token ayarlandıktan sonra):")
        print("   python ultra_telegram_bot.py")
    
    def tam_sistem_kontrolu(self):
        """Tam sistem kontrolü yap"""
        print("🔍 PLANB MOTORU - TAM SİSTEM KONTROLÜ")
        print("=" * 60)
        print(f"⏰ Kontrol zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Tüm kontrolleri yap
        local_status = self.kontrol_local_sunucu()
        cloud_status = self.kontrol_bulut_sunucu()
        data_status = self.kontrol_veri_akisi()
        telegram_status = self.kontrol_telegram_bot()
        
        # Özet rapor
        self.print_header("ÖZET RAPOR")
        
        print(f"🖥️  Local Sunucu: {'✅ ÇALIŞIYOR' if local_status else '❌ KAPALI'}")
        
        if cloud_status is True:
            print(f"☁️  Bulut Sunucu: ✅ AKTİF")
        elif cloud_status is False:
            print(f"☁️  Bulut Sunucu: ❌ ULAŞILAMIYOR")
        else:
            print(f"☁️  Bulut Sunucu: ⚠️  AYARLANMAMIŞ")
            
        print(f"📊 Veri Akışı: {'✅ SORUNSUZ' if data_status else '❌ SORUNLU'}")
        
        if telegram_status is True:
            print(f"🤖 Telegram Bot: ✅ AKTİF")
        elif telegram_status is False:
            print(f"🤖 Telegram Bot: ❌ AYARLANMAMIŞ")
        else:
            print(f"🤖 Telegram Bot: ⚠️  BİLİNMİYOR")
        
        # Öneriler
        if not local_status:
            print("\n💡 ÖNERİLER:")
            print("   • API server'ı başlatın: python ultra_api_server.py")
            
        if not data_status:
            print("   • Database'i yeniden oluşturun: python ultra_database.py")
            
        if telegram_status is False:
            print("   • Telegram bot token'ını ayarlayın")
        
        # Sistem başlatma komutları
        self.sistem_baslat_komutu()
        self.telegram_test_komutu()

if __name__ == "__main__":
    kontrol = SistemKontrolPaneli()
    kontrol.tam_sistem_kontrolu()