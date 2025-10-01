#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kuruluş Tarihi Otomatik İşleme Sistemi
SEMBOL - ŞİRKET ADI - TARİH formatındaki verileri otomatik parse eder ve sisteme entegre eder
"""

import os
import re
import csv
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class FoundationRecord:
    """Kuruluş tarihi kaydı"""
    symbol: str
    company_name: str
    foundation_date: str
    parsed_date: datetime
    age_years: int
    market_type: str  # NASDAQ, XETRA, BIST, CRYPTO, COMMODITY

class FoundationDateProcessor:
    """Kuruluş tarihi otomatik işleme sistemi"""
    
    def __init__(self):
        self.records: Dict[str, FoundationRecord] = {}
        self.data_dir = "data/foundation_dates"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Gerekli dizinleri oluştur"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def parse_foundation_line(self, line: str, market_type: str) -> Optional[FoundationRecord]:
        """Tek satırı parse et: SEMBOL - ŞİRKET ADI - TARİH"""
        line = line.strip()
        if not line or line.startswith('#'):
            return None
        
        # Format: SEMBOL - ŞİRKET ADI - TARİH
        parts = line.split(' - ')
        if len(parts) < 3:
            return None
        
        symbol = parts[0].strip()
        company_name = parts[1].strip()
        date_str = parts[2].strip()
        
        try:
            # Tarihi parse et (dd.mm.yyyy formatı)
            parsed_date = datetime.strptime(date_str, "%d.%m.%Y")
            age_years = 2025 - parsed_date.year
            
            return FoundationRecord(
                symbol=symbol,
                company_name=company_name,
                foundation_date=date_str,
                parsed_date=parsed_date,
                age_years=age_years,
                market_type=market_type
            )
        except ValueError:
            print(f"⚠️ Tarih parse hatası: {line}")
            return None
    
    def load_from_file(self, file_path: str, market_type: str) -> int:
        """Dosyadan kuruluş tarihlerini yükle"""
        count = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                record = self.parse_foundation_line(line, market_type)
                if record:
                    self.records[record.symbol] = record
                    count += 1
            
            print(f"✅ {market_type}: {count} kayıt yüklendi")
            
        except Exception as e:
            print(f"❌ {file_path} yüklenirken hata: {e}")
        
        return count
    
    def load_all_foundation_lists(self) -> Dict[str, int]:
        """Tüm kuruluş tarihi listelerini yükle"""
        
        print("🔍 KURULUŞ TARİHİ LİSTELERİ YÜKLENİYOR...")
        print("=" * 60)
        
        loading_stats = {}
        
        # Dosya yolları ve market türleri
        file_mappings = [
            ("nasdaq tam liste.txt", "NASDAQ"),
            ("emtia tam liste.txt", "COMMODITY"),
            ("XETRA TAM LİSTE-.txt", "XETRA"),
            ("bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt", "BIST")
        ]
        
        for file_path, market_type in file_mappings:
            if os.path.exists(file_path):
                count = self.load_from_file(file_path, market_type)
                loading_stats[market_type] = count
            else:
                print(f"⚠️ {file_path} bulunamadı")
                loading_stats[market_type] = 0
        
        # Kripto listesi (varsayılan veriler)
        crypto_count = self.load_crypto_foundations()
        loading_stats["CRYPTO"] = crypto_count
        
        return loading_stats
    
    def load_crypto_foundations(self) -> int:
        """Kripto para kuruluş tarihlerini yükle"""
        crypto_foundations = [
            "BTC-USD - Bitcoin - 03.01.2009",
            "ETH-USD - Ethereum - 30.07.2015",
            "BNB-USD - Binance Coin - 08.07.2017",
            "SOL-USD - Solana - 16.04.2020",
            "XRP-USD - Ripple - 01.01.2013",
            "ADA-USD - Cardano - 27.09.2017",
            "DOGE-USD - Dogecoin - 06.12.2013",
            "AVAX-USD - Avalanche - 21.09.2020",
            "DOT-USD - Polkadot - 26.05.2020",
            "LINK-USD - Chainlink - 20.09.2017",
            "MATIC-USD - Polygon - 01.10.2017",
            "LTC-USD - Litecoin - 07.10.2011",
            "UNI-USD - Uniswap - 01.11.2018",
            "ATOM-USD - Cosmos - 13.03.2019",
            "XLM-USD - Stellar - 31.07.2014",
            "XMR-USD - Monero - 18.04.2014",
            "BCH-USD - Bitcoin Cash - 01.08.2017",
            "VET-USD - VeChain - 15.08.2017",
            "FIL-USD - Filecoin - 15.10.2020",
            "AAVE-USD - Aave - 02.10.2017"
        ]
        
        count = 0
        for crypto_line in crypto_foundations:
            record = self.parse_foundation_line(crypto_line, "CRYPTO")
            if record:
                self.records[record.symbol] = record
                count += 1
        
        print(f"✅ CRYPTO: {count} kayıt yüklendi")
        return count
    
    def save_to_database(self):
        """Verileri JSON veritabanına kaydet"""
        db_file = os.path.join(self.data_dir, "foundation_database.json")
        
        # Kayıtları dict'e çevir
        data = {}
        for symbol, record in self.records.items():
            data[symbol] = {
                "company_name": record.company_name,
                "foundation_date": record.foundation_date,
                "age_years": record.age_years,
                "market_type": record.market_type,
                "parsed_timestamp": record.parsed_date.timestamp()
            }
        
        with open(db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Veritabanı kaydedildi: {db_file}")
    
    def save_to_csv(self):
        """CSV formatında kaydet"""
        csv_file = os.path.join(self.data_dir, "foundation_database.csv")
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Company_Name", "Foundation_Date", "Age_Years", "Market_Type"])
            
            for record in sorted(self.records.values(), key=lambda x: x.parsed_date):
                writer.writerow([
                    record.symbol,
                    record.company_name,
                    record.foundation_date,
                    record.age_years,
                    record.market_type
                ])
        
        print(f"📊 CSV kaydedildi: {csv_file}")
    
    def generate_provider_integration_code(self):
        """Provider entegrasyonu için kod üret"""
        
        # Market türlerine göre grupla
        by_market = {}
        for record in self.records.values():
            if record.market_type not in by_market:
                by_market[record.market_type] = []
            by_market[record.market_type].append(record)
        
        integration_code = []
        
        for market_type, records in by_market.items():
            code = f"""
# {market_type} Provider Foundation Dates Integration
{market_type.lower()}_foundation_dates = {{
"""
            for record in sorted(records, key=lambda x: x.symbol):
                code += f'    "{record.symbol}": ("{record.company_name}", "{record.foundation_date}"),\n'
            
            code += "}\n"
            integration_code.append(code)
        
        # Kodu dosyaya kaydet
        code_file = os.path.join(self.data_dir, "provider_integration.py")
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python3\n")
            f.write("# -*- coding: utf-8 -*-\n")
            f.write('"""\nOtomatik üretilmiş provider entegrasyon kodu\n"""\n\n')
            f.write("\n".join(integration_code))
        
        print(f"🔧 Provider kodu üretildi: {code_file}")
    
    def analyze_statistics(self):
        """İstatistik analizi yap"""
        
        print(f"\n📊 KURULUŞ TARİHİ İSTATİSTİKLERİ")
        print("=" * 60)
        
        # Market türü dağılımı
        by_market = {}
        for record in self.records.values():
            by_market[record.market_type] = by_market.get(record.market_type, 0) + 1
        
        print("Market Türü Dağılımı:")
        for market, count in sorted(by_market.items()):
            print(f"  {market}: {count:,} enstrüman")
        
        print(f"\n🎯 TOPLAM: {len(self.records):,} enstrüman")
        
        # Yaş dağılımı
        ages = [record.age_years for record in self.records.values()]
        print(f"\nYaş İstatistikleri:")
        print(f"  En eski: {max(ages)} yıl")
        print(f"  En yeni: {min(ages)} yıl")
        print(f"  Ortalama: {sum(ages)/len(ages):.1f} yıl")
        
        # En eski ve en yeni şirketler
        oldest = max(self.records.values(), key=lambda x: x.age_years)
        newest = min(self.records.values(), key=lambda x: x.age_years)
        
        print(f"\nEn Eski: {oldest.symbol} - {oldest.company_name} ({oldest.age_years} yıl)")
        print(f"En Yeni: {newest.symbol} - {newest.company_name} ({newest.age_years} yıl)")
    
    def get_foundation_date(self, symbol: str) -> Optional[FoundationRecord]:
        """Belirli bir sembol için kuruluş tarihini getir"""
        return self.records.get(symbol)
    
    def search_by_age_range(self, min_age: int, max_age: int) -> List[FoundationRecord]:
        """Yaş aralığına göre ara"""
        return [
            record for record in self.records.values()
            if min_age <= record.age_years <= max_age
        ]
    
    def search_by_market_type(self, market_type: str) -> List[FoundationRecord]:
        """Market türüne göre ara"""
        return [
            record for record in self.records.values()
            if record.market_type == market_type
        ]

def create_ultra_module_integration():
    """Ultra modül entegrasyonu için kod üret"""
    
    integration_template = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultra Modül Kuruluş Tarihi Entegrasyonu
Otomatik üretilmiş - Foundation Date Processor tarafından
"""

from datetime import datetime
from typing import Optional, Dict, Any
import sys
import os

# Foundation Date Processor'ı import et
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from foundation_date_processor import FoundationDateProcessor

class UltraFoundationIntegration:
    """Ultra modüller için kuruluş tarihi entegrasyonu"""
    
    def __init__(self):
        self.processor = FoundationDateProcessor()
        # Mevcut veritabanını yükle
        self.load_foundation_database()
    
    def load_foundation_database(self):
        """Kuruluş tarihi veritabanını yükle"""
        try:
            self.processor.load_all_foundation_lists()
            print(f"✅ {len(self.processor.records)} kuruluş tarihi yüklendi")
        except Exception as e:
            print(f"❌ Kuruluş tarihi yüklenirken hata: {e}")
    
    def get_astrology_features(self, symbol: str) -> Dict[str, Any]:
        """Astroloji modülü için kuruluş tarihi özellikleri"""
        record = self.processor.get_foundation_date(symbol)
        if not record:
            return {}
        
        return {
            "birth_date": record.parsed_date,
            "zodiac_sign": self._get_zodiac_sign(record.parsed_date),
            "planetary_positions": self._calculate_planetary_positions(record.parsed_date),
            "company_age": record.age_years,
            "foundation_era": self._get_foundation_era(record.parsed_date.year)
        }
    
    def get_shemitah_features(self, symbol: str) -> Dict[str, Any]:
        """Shemitah modülü için kuruluş tarihi özellikleri"""
        record = self.processor.get_foundation_date(symbol)
        if not record:
            return {}
        
        return {
            "shemitah_year": self._is_shemitah_year(record.parsed_date.year),
            "cycles_since_foundation": (2025 - record.parsed_date.year) // 7,
            "foundation_in_crisis": self._founded_in_crisis_period(record.parsed_date.year),
            "economic_context": self._get_economic_context(record.parsed_date.year)
        }
    
    def get_statistical_features(self, symbol: str) -> Dict[str, Any]:
        """İstatistiksel modül için kuruluş tarihi özellikleri"""
        record = self.processor.get_foundation_date(symbol)
        if not record:
            return {}
        
        return {
            "company_age": record.age_years,
            "age_category": self._categorize_age(record.age_years),
            "generation": self._get_generation(record.parsed_date.year),
            "market_maturity": self._calculate_market_maturity(record.age_years),
            "survival_score": self._calculate_survival_score(record.age_years)
        }
    
    def get_risk_features(self, symbol: str) -> Dict[str, Any]:
        """Risk modülü için kuruluş tarihi özellikleri"""
        record = self.processor.get_foundation_date(symbol)
        if not record:
            return {}
        
        return {
            "age_risk_factor": self._calculate_age_risk(record.age_years),
            "foundation_era_risk": self._get_era_risk(record.parsed_date.year),
            "economic_cycle_risk": self._get_cycle_risk(record.parsed_date.year),
            "market_experience": record.age_years / 100.0  # Normalize to 0-1
        }
    
    def get_ml_features(self, symbol: str) -> Dict[str, Any]:
        """ML modülü için kuruluş tarihi özellikleri"""
        record = self.processor.get_foundation_date(symbol)
        if not record:
            return {}
        
        return {
            "foundation_timestamp": record.parsed_date.timestamp(),
            "age_normalized": min(record.age_years / 100.0, 1.0),
            "decade_founded": record.parsed_date.year // 10 * 10,
            "market_type_encoded": self._encode_market_type(record.market_type),
            "seasonal_founding": record.parsed_date.month,
            "historical_context": self._get_historical_context_vector(record.parsed_date.year)
        }
    
    # Yardımcı metodlar
    def _get_zodiac_sign(self, date: datetime) -> str:
        """Astrolojik burç hesapla"""
        month, day = date.month, date.day
        
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus"
        # ... diğer burçlar
        else:
            return "Unknown"
    
    def _is_shemitah_year(self, year: int) -> bool:
        """Shemitah yılı kontrolü"""
        # 5775 = 2014-2015 Shemitah yılı
        shemitah_base = 2015
        return (year - shemitah_base) % 7 == 0
    
    def _categorize_age(self, age: int) -> str:
        """Yaş kategorisi"""
        if age < 5:
            return "startup"
        elif age < 20:
            return "young"
        elif age < 50:
            return "mature"
        else:
            return "established"
    
    def _calculate_age_risk(self, age: int) -> float:
        """Yaş bazlı risk hesaplama"""
        if age < 5:
            return 0.8  # Yüksek risk
        elif age < 20:
            return 0.6  # Orta-yüksek risk
        elif age < 50:
            return 0.4  # Orta risk
        else:
            return 0.2  # Düşük risk
    
    def _encode_market_type(self, market_type: str) -> int:
        """Market türü encoding"""
        encodings = {
            "NASDAQ": 1,
            "XETRA": 2, 
            "BIST": 3,
            "CRYPTO": 4,
            "COMMODITY": 5
        }
        return encodings.get(market_type, 0)
    
    def _get_historical_context_vector(self, year: int) -> List[float]:
        """Tarihsel kontekst vektörü"""
        # Önemli dönemler için binary encoding
        features = [
            1.0 if 1929 <= year <= 1939 else 0.0,  # Great Depression
            1.0 if 1970 <= year <= 1990 else 0.0,  # Tech boom start
            1.0 if 1990 <= year <= 2000 else 0.0,  # Dot-com era
            1.0 if 2008 <= year <= 2012 else 0.0,  # Financial crisis
            1.0 if 2020 <= year <= 2025 else 0.0,  # COVID/Digital era
        ]
        return features

# Global instance
foundation_integration = UltraFoundationIntegration()

def get_foundation_features(symbol: str, module_type: str) -> Dict[str, Any]:
    """Tüm modüller için unified interface"""
    
    if module_type == "astrology":
        return foundation_integration.get_astrology_features(symbol)
    elif module_type == "shemitah":
        return foundation_integration.get_shemitah_features(symbol)
    elif module_type == "statistical":
        return foundation_integration.get_statistical_features(symbol)
    elif module_type == "risk":
        return foundation_integration.get_risk_features(symbol)
    elif module_type == "ml":
        return foundation_integration.get_ml_features(symbol)
    else:
        return {}
'''
    
    # Entegrasyon dosyasını kaydet
    with open("src/utils/ultra_foundation_integration.py", 'w', encoding='utf-8') as f:
        f.write(integration_template)
    
    print("🔧 Ultra modül entegrasyonu oluşturuldu!")

if __name__ == "__main__":
    print("🎯 KURULUŞ TARİHİ OTOMATIK İŞLEME SİSTEMİ")
    print("=" * 60)
    
    # İşlemciyi başlat
    processor = FoundationDateProcessor()
    
    # Tüm listeleri yükle
    stats = processor.load_all_foundation_lists()
    
    # İstatistikleri göster
    processor.analyze_statistics()
    
    # Veritabanlarını kaydet
    processor.save_to_database()
    processor.save_to_csv()
    
    # Provider entegrasyonu oluştur
    processor.generate_provider_integration_code()
    
    # Ultra modül entegrasyonu oluştur
    create_ultra_module_integration()
    
    print(f"\n✅ SİSTEM HAZIR!")
    print(f"Toplam {len(processor.records):,} kuruluş tarihi işlendi!")
    print(f"6 ultra modül için entegrasyon kodu oluşturuldu!")