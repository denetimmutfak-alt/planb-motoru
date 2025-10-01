#!/usr/bin/env python3
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

