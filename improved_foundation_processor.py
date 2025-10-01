#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geliştirilmiş Kuruluş Tarihi İşleme Sistemi
Çoklu format desteği ile kuruluş tarihi verilerini işler
"""

import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class FoundationRecord:
    """Kuruluş tarihi kaydı"""
    symbol: str
    company_name: str
    foundation_date: str
    age_years: int
    market_type: str

class ImprovedFoundationProcessor:
    """Geliştirilmiş kuruluş tarihi işleme sistemi"""
    
    def __init__(self):
        self.records: Dict[str, FoundationRecord] = {}
        self.data_dir = "data/foundation_dates"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Gerekli dizinleri oluştur"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def parse_foundation_line(self, line: str, market_type: str) -> Optional[FoundationRecord]:
        """
        Çoklu format desteği ile satır parse et
        Desteklenen formatlar:
        1. "SYMBOL - COMPANY NAME - DD.MM.YYYY" (User format)
        2. "SYMBOL\tCOMPANY NAME\tDD.MM.YYYY" (BIST format)
        """
        line = line.strip()
        if not line or line.startswith('#'):
            return None
        
        # Tab ile ayrılmış format (BIST)
        if '\t' in line:
            parts = line.split('\t')
            if len(parts) >= 3:
                symbol = parts[0].strip()
                company_name = parts[1].strip()
                date_str = parts[2].strip()
            else:
                return None
        # Tire ile ayrılmış format (User format)
        elif ' - ' in line:
            parts = line.split(' - ')
            if len(parts) >= 3:
                symbol = parts[0].strip()
                company_name = parts[1].strip()
                date_str = parts[2].strip()
            else:
                return None
        else:
            return None
        
        try:
            # Tarihi parse et
            parsed_date = datetime.strptime(date_str, "%d.%m.%Y")
            age_years = 2025 - parsed_date.year
            
            return FoundationRecord(
                symbol=symbol,
                company_name=company_name,
                foundation_date=date_str,
                age_years=age_years,
                market_type=market_type
            )
        except ValueError as e:
            print(f"⚠️ Tarih parse hatası: {date_str} - {e}")
            return None
    
    def load_from_file(self, file_path: str, market_type: str) -> int:
        """Dosyadan kuruluş tarihi verilerini yükle"""
        if not os.path.exists(file_path):
            print(f"⚠️ {file_path} bulunamadı")
            return 0
        
        count = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    record = self.parse_foundation_line(line, market_type)
                    if record:
                        self.records[record.symbol] = record
                        count += 1
                        
            print(f"✅ {market_type}: {count} kayıt yüklendi")
            return count
            
        except Exception as e:
            print(f"❌ {file_path} okuma hatası: {e}")
            return 0
    
    def load_crypto_data(self):
        """Kripto para kuruluş tarihlerini yükle - önce dosyadan, yoksa varsayılan verilerden"""
        
        # Önce kripto tam liste dosyasını kontrol et
        crypto_file = "kripto tam liste.txt"
        if os.path.exists(crypto_file):
            return self.load_from_file(crypto_file, "CRYPTO")
        
        # Dosya yoksa varsayılan kripto verilerini yükle
        crypto_data = {
            "BTC-USD": {"name": "Bitcoin", "foundation": "03.01.2009"},
            "ETH-USD": {"name": "Ethereum", "foundation": "30.07.2015"},
            "ADA-USD": {"name": "Cardano", "foundation": "27.09.2017"},
            "DOT-USD": {"name": "Polkadot", "foundation": "26.05.2020"},
            "LINK-USD": {"name": "Chainlink", "foundation": "20.09.2017"},
            "LTC-USD": {"name": "Litecoin", "foundation": "07.10.2011"},
            "XRP-USD": {"name": "Ripple", "foundation": "01.01.2012"},
            "BCH-USD": {"name": "Bitcoin Cash", "foundation": "01.08.2017"},
            "BNB-USD": {"name": "Binance Coin", "foundation": "25.07.2017"},
            "SOL-USD": {"name": "Solana", "foundation": "16.03.2020"},
            "MATIC-USD": {"name": "Polygon", "foundation": "01.10.2017"},
            "AVAX-USD": {"name": "Avalanche", "foundation": "21.09.2020"},
            "UNI-USD": {"name": "Uniswap", "foundation": "17.09.2020"},
            "ATOM-USD": {"name": "Cosmos", "foundation": "14.03.2019"},
            "ALGO-USD": {"name": "Algorand", "foundation": "19.06.2019"},
            "VET-USD": {"name": "VeChain", "foundation": "15.08.2015"},
            "ICP-USD": {"name": "Internet Computer", "foundation": "10.05.2021"},
            "FIL-USD": {"name": "Filecoin", "foundation": "15.10.2020"},
            "TRX-USD": {"name": "TRON", "foundation": "13.09.2017"},
            "XLM-USD": {"name": "Stellar", "foundation": "31.07.2014"}
        }
        
        count = 0
        for symbol, data in crypto_data.items():
            try:
                parsed_date = datetime.strptime(data["foundation"], "%d.%m.%Y")
                age_years = 2025 - parsed_date.year
                
                record = FoundationRecord(
                    symbol=symbol,
                    company_name=data["name"],
                    foundation_date=data["foundation"],
                    age_years=age_years,
                    market_type="CRYPTO"
                )
                self.records[symbol] = record
                count += 1
            except ValueError:
                continue
                
        return count
    
    def process_all_files(self):
        """Tüm dosyaları işle"""
        print("🎯 GELİŞTİRİLMİŞ KURULUŞ TARİHİ İŞLEME SİSTEMİ")
        print("=" * 60)
        print("🔍 KURULUŞ TARİHİ LİSTELERİ YÜKLENİYOR...")
        print("=" * 60)
        
        loading_stats = {}
        
        # Dosya tarama - mevcut dosyaları bul
        foundation_files = []
        for file in os.listdir("."):
            if file.endswith(".txt"):
                file_lower = file.lower()
                if "nasdaq" in file_lower and "tam" in file_lower:
                    foundation_files.append((file, "NASDAQ"))
                elif "emtia" in file_lower and "tam" in file_lower:
                    foundation_files.append((file, "COMMODITY"))
                elif "xetra" in file_lower and "tam" in file_lower:
                    foundation_files.append((file, "XETRA"))
                elif "bist" in file_lower and ("kuruluş" in file_lower or "tam" in file_lower):
                    foundation_files.append((file, "BIST"))
        
        # Dosyaları işle
        for file_path, market_type in foundation_files:
            count = self.load_from_file(file_path, market_type)
            loading_stats[market_type] = count
        
        # Kripto verilerini yükle
        crypto_count = self.load_crypto_data()
        loading_stats["CRYPTO"] = crypto_count
        print(f"✅ CRYPTO: {crypto_count} kayıt yüklendi")
        
        return loading_stats
    
    def generate_statistics(self):
        """İstatistik üret"""
        print("\n📊 KURULUŞ TARİHİ İSTATİSTİKLERİ")
        print("=" * 60)
        
        # Market türü dağılımı
        market_stats = {}
        for record in self.records.values():
            market_stats[record.market_type] = market_stats.get(record.market_type, 0) + 1
        
        print("Market Türü Dağılımı:")
        for market, count in market_stats.items():
            print(f"  {market}: {count} enstrüman")
        
        print(f"\n🎯 TOPLAM: {len(self.records)} enstrüman")
        
        # Yaş istatistikleri
        if self.records:
            ages = [r.age_years for r in self.records.values()]
            print(f"\nYaş İstatistikleri:")
            print(f"  En eski: {max(ages)} yıl")
            print(f"  En yeni: {min(ages)} yıl")
            print(f"  Ortalama: {sum(ages)/len(ages):.1f} yıl")
            
            # En eski ve en yeni
            oldest = max(self.records.values(), key=lambda x: x.age_years)
            newest = min(self.records.values(), key=lambda x: x.age_years)
            print(f"\nEn Eski: {oldest.symbol} - {oldest.company_name} ({oldest.age_years} yıl)")
            print(f"En Yeni: {newest.symbol} - {newest.company_name} ({newest.age_years} yıl)")
    
    def save_to_database(self):
        """Veritabanına kaydet"""
        # JSON formatında kaydet
        json_path = os.path.join(self.data_dir, "foundation_database.json")
        json_data = {}
        for symbol, record in self.records.items():
            json_data[symbol] = {
                "company_name": record.company_name,
                "foundation_date": record.foundation_date,
                "age_years": record.age_years,
                "market_type": record.market_type
            }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"💾 Veritabanı kaydedildi: {json_path}")
        
        # CSV formatında kaydet
        csv_path = os.path.join(self.data_dir, "foundation_database.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Symbol', 'Company', 'Foundation_Date', 'Age_Years', 'Market_Type'])
            for record in self.records.values():
                writer.writerow([
                    record.symbol,
                    record.company_name,
                    record.foundation_date,
                    record.age_years,
                    record.market_type
                ])
        print(f"📊 CSV kaydedildi: {csv_path}")
    
    def generate_ultra_integration(self):
        """Ultra modüller için entegrasyon kodu üret"""
        integration_code = '''"""
Ultra Modüller için Kuruluş Tarihi Entegrasyonu
Bu kod ultra modüllerde kuruluş tarihi verilerini kullanmak için üretilmiştir
"""

import json
import os
from datetime import datetime, timedelta

class FoundationDateIntegration:
    """Ultra modüller için kuruluş tarihi entegrasyonu"""
    
    def __init__(self):
        self.foundation_data = self.load_foundation_data()
    
    def load_foundation_data(self):
        """Kuruluş tarihi verilerini yükle"""
        json_path = "data/foundation_dates/foundation_database.json"
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_foundation_date(self, symbol: str):
        """Sembol için kuruluş tarihini getir"""
        if symbol in self.foundation_data:
            return self.foundation_data[symbol]["foundation_date"]
        return None
    
    def get_company_age(self, symbol: str):
        """Şirket yaşını getir"""
        if symbol in self.foundation_data:
            return self.foundation_data[symbol]["age_years"]
        return None
    
    def get_market_type(self, symbol: str):
        """Market türünü getir"""
        if symbol in self.foundation_data:
            return self.foundation_data[symbol]["market_type"]
        return None
    
    # Ultra Astroloji Modülü için
    def get_astrology_factors(self, symbol: str):
        """Astroloji faktörlerini hesapla"""
        foundation_date = self.get_foundation_date(symbol)
        if not foundation_date:
            return None
        
        date_obj = datetime.strptime(foundation_date, "%d.%m.%Y")
        
        # Astroloji hesaplamaları
        jupiter_cycle = (datetime.now() - date_obj).days / (12 * 365.25)  # Jüpiter döngüsü
        saturn_cycle = (datetime.now() - date_obj).days / (29 * 365.25)   # Satürn döngüsü
        
        return {
            "jupiter_cycle_position": jupiter_cycle % 1,
            "saturn_cycle_position": saturn_cycle % 1,
            "foundation_day_of_year": date_obj.timetuple().tm_yday
        }
    
    # Ultra Shemitah Modülü için
    def get_shemitah_position(self, symbol: str):
        """Shemitah döngüsündeki pozisyonu hesapla"""
        foundation_date = self.get_foundation_date(symbol)
        if not foundation_date:
            return None
        
        date_obj = datetime.strptime(foundation_date, "%d.%m.%Y")
        
        # Shemitah döngüsü (7 yıl)
        shemitah_cycle = (datetime.now() - date_obj).days / (7 * 365.25)
        
        return {
            "shemitah_cycle_position": shemitah_cycle % 1,
            "cycles_completed": int(shemitah_cycle)
        }
    
    # Ultra Solar/Lunar Modülleri için
    def get_solar_lunar_factors(self, symbol: str):
        """Güneş ve ay döngülerini hesapla"""
        foundation_date = self.get_foundation_date(symbol)
        if not foundation_date:
            return None
        
        date_obj = datetime.strptime(foundation_date, "%d.%m.%Y")
        days_since = (datetime.now() - date_obj).days
        
        return {
            "solar_cycles": days_since / 365.25,
            "lunar_cycles": days_since / 29.5,  # Lunar month
            "foundation_moon_phase": (date_obj.timetuple().tm_yday % 29.5) / 29.5
        }
    
    # Ultra Statistical Modülü için
    def get_age_statistics(self, symbol: str):
        """Yaş bazlı istatistikler"""
        age = self.get_company_age(symbol)
        if not age:
            return None
        
        # Yaş kategorileri
        if age < 5:
            category = "STARTUP"
        elif age < 15:
            category = "GROWING"
        elif age < 30:
            category = "MATURE"
        else:
            category = "ESTABLISHED"
        
        return {
            "age_category": category,
            "age_score": min(age / 50, 1.0),  # 0-1 arası normalleştirilmiş
            "decade_position": age % 10
        }
    
    # Ultra Risk Modülü için
    def get_risk_factors(self, symbol: str):
        """Yaş bazlı risk faktörleri"""
        age = self.get_company_age(symbol)
        market_type = self.get_market_type(symbol)
        
        if not age:
            return None
        
        # Yaş bazlı risk skorları
        if age < 3:
            age_risk = 0.8  # Yüksek risk
        elif age < 10:
            age_risk = 0.6  # Orta-yüksek risk
        elif age < 25:
            age_risk = 0.4  # Orta risk
        else:
            age_risk = 0.2  # Düşük risk
        
        # Market türü bazlı risk çarpanı
        market_multiplier = {
            "CRYPTO": 1.5,
            "COMMODITY": 1.2,
            "NASDAQ": 1.0,
            "XETRA": 1.0,
            "BIST": 1.3
        }.get(market_type, 1.0)
        
        return {
            "age_risk_score": age_risk * market_multiplier,
            "stability_score": min(age / 20, 1.0)
        }
    
    # Ultra ML Modülü için
    def get_ml_features(self, symbol: str):
        """Machine Learning için özellik vektörü"""
        foundation_date = self.get_foundation_date(symbol)
        age = self.get_company_age(symbol)
        market_type = self.get_market_type(symbol)
        
        if not all([foundation_date, age, market_type]):
            return None
        
        date_obj = datetime.strptime(foundation_date, "%d.%m.%Y")
        
        return {
            "age_normalized": min(age / 100, 1.0),
            "foundation_month": date_obj.month / 12,
            "foundation_day": date_obj.day / 31,
            "market_encoding": {
                "CRYPTO": [1, 0, 0, 0, 0],
                "NASDAQ": [0, 1, 0, 0, 0],
                "XETRA": [0, 0, 1, 0, 0],
                "BIST": [0, 0, 0, 1, 0],
                "COMMODITY": [0, 0, 0, 0, 1]
            }.get(market_type, [0, 0, 0, 0, 0]),
            "decade_encoding": [1 if (age // 10) == i else 0 for i in range(10)]
        }

# Global instance
foundation_integration = FoundationDateIntegration()
'''
        
        integration_path = os.path.join(self.data_dir, "ultra_module_integration.py")
        with open(integration_path, 'w', encoding='utf-8') as f:
            f.write(integration_code)
        print(f"🔧 Ultra modül entegrasyonu oluşturuldu: {integration_path}")

def main():
    """Ana fonksiyon"""
    processor = ImprovedFoundationProcessor()
    
    # Tüm dosyaları işle
    stats = processor.process_all_files()
    
    # İstatistikleri göster
    processor.generate_statistics()
    
    # Veritabanına kaydet
    processor.save_to_database()
    
    # Ultra modül entegrasyonu oluştur
    processor.generate_ultra_integration()
    
    print(f"\n✅ SİSTEM HAZIR!")
    print(f"Toplam {len(processor.records)} kuruluş tarihi işlendi!")
    
    # Ultra modül entegrasyon sayısı
    ultra_modules = ["Astrology", "Shemitah", "Solar", "Lunar", "Statistical", "Risk", "ML"]
    print(f"{len(ultra_modules)} ultra modül için entegrasyon kodu oluşturuldu!")

if __name__ == "__main__":
    main()