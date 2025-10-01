#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MULTI-EXPERT ENGINE CORE SYSTEM
Arkadaş fikirlerinin entegrasyonu - Ortak ExpertModule arayüzü
Tüm ultra modüller için standart API kontratı
"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import logging
import json
from dataclasses import dataclass
import pickle
from pathlib import Path

# CompanyFoundingDates entegrasyonu
try:
    from src.data.company_founding_dates import CompanyFoundingDates
    FOUNDING_DATES_AVAILABLE = True
    print("INFO: CompanyFoundingDates modülü Multi-Expert Engine'e entegre edildi")
except ImportError:
    FOUNDING_DATES_AVAILABLE = False
    print("WARNING: CompanyFoundingDates modülü Multi-Expert Engine'de bulunamadı")

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ModuleResult:
    """Modül sonuç standardı - arkadaşın önerdiği format"""
    score: float  # 0-100 arası normalize edilmiş skor
    uncertainty: float  # 0-1 arası modelin bu çıkarımdan ne kadar emin olduğu
    type: List[str]  # Skoru etkileyen olay/pattern türleri
    explanation: str  # İnsanların anlayabileceği kısa açıklama (XAI)
    timestamp: str  # Analiz zamanı
    confidence_level: str  # "HIGH", "MEDIUM", "LOW"
    contributing_factors: Dict[str, float]  # Hangi faktörler ne kadar katkı verdi
    
    def __post_init__(self):
        """Validasyon ve otomatik hesaplamalar"""
        # Skor validasyonu
        if not 0 <= self.score <= 100:
            raise ValueError(f"Score must be between 0-100, got {self.score}")
        
        # Uncertainty validasyonu
        if not 0 <= self.uncertainty <= 1:
            raise ValueError(f"Uncertainty must be between 0-1, got {self.uncertainty}")
        
        # Confidence level otomatik hesaplama
        if self.uncertainty <= 0.2:
            self.confidence_level = "HIGH"
        elif self.uncertainty <= 0.5:
            self.confidence_level = "MEDIUM"
        else:
            self.confidence_level = "LOW"
        
        # Timestamp otomatik ekleme
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Dict formatına çevir"""
        return {
            "score": self.score,
            "uncertainty": self.uncertainty,
            "type": self.type,
            "explanation": self.explanation,
            "timestamp": self.timestamp,
            "confidence_level": self.confidence_level,
            "contributing_factors": self.contributing_factors
        }

class ExpertModule(ABC):
    """
    Tüm ultra modüllerin uygulayacağı ortak arayüz
    Arkadaşın önerdiği Multi-Expert Engine'in temeli
    """
    
    def __init__(self, module_name: str, config: Dict[str, Any] = None):
        self.name = module_name
        self.config = config or {}
        self.is_trained = False
        self.model = None
        self.scaler = None
        self.feature_columns = []
        self.last_training_date = None
        self.performance_metrics = {}
        
        # CompanyFoundingDates entegrasyonu
        self.founding_dates = None
        if FOUNDING_DATES_AVAILABLE:
            try:
                self.founding_dates = CompanyFoundingDates()
                logger.info(f"{self.name}: CompanyFoundingDates başarıyla entegre edildi")
            except Exception as e:
                logger.warning(f"{self.name}: CompanyFoundingDates entegre edilemedi: {str(e)}")
        
        # Modül bilgileri
        self.version = "1.0.0"
        self.description = ""
        self.dependencies = []
        
        # İstatistikler
        self.prediction_count = 0
        self.error_count = 0
        self.last_prediction_time = None
        
        logger.info(f"Expert Module initialized: {self.name}")
    
    @abstractmethod
    def prepare_features(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Ham veriyi alır, modüle özgü özellikleri (features) hesaplar
        
        Args:
            raw_data: Ham piyasa verisi, haberler, astronomik veri etc.
            
        Returns:
            pd.DataFrame: Modülün kullanacağı özellikler
        """
        pass
    
    @abstractmethod
    def infer(self, features: pd.DataFrame) -> ModuleResult:
        """
        Hazırlanan özellikler üzerinden çıkarım yapar
        
        Args:
            features: prepare_features'dan gelen hazır özellikler
            
        Returns:
            ModuleResult: Standart format çıktı
        """
        pass
    
    @abstractmethod
    def retrain(self, training_data: pd.DataFrame, labels: pd.Series = None) -> Dict[str, Any]:
        """
        Modeli yeniden eğitmek veya calibrate etmek için kullanılır
        
        Args:
            training_data: Eğitim verisi
            labels: Hedef değişken (varsa)
            
        Returns:
            Dict: Eğitim metrikleri ve sonuçları
        """
        pass
    
    def validate_input(self, raw_data: Dict[str, Any]) -> bool:
        """Giriş verisini doğrula"""
        try:
            if not isinstance(raw_data, dict):
                logger.error(f"{self.name}: Input must be dictionary")
                return False
            
            # Temel veri kontrolü
            required_fields = self.get_required_fields()
            for field in required_fields:
                if field not in raw_data:
                    logger.warning(f"{self.name}: Missing required field: {field}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"{self.name}: Input validation error: {str(e)}")
            return False
    
    def get_required_fields(self) -> List[str]:
        """Modülün ihtiyaç duyduğu veri alanları"""
        return ["symbol", "timestamp"]  # Base requirement
    
    def handle_missing_data(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Eksik veri durumunda standart işlem
        Arkadaşın 'zorunlu katkı' prensibine uygun
        """
        try:
            # Numeric kolonları forward fill + backward fill
            numeric_cols = features.select_dtypes(include=[np.number]).columns
            features[numeric_cols] = features[numeric_cols].fillna(method='ffill').fillna(method='bfill')
            
            # Hala eksik olan numeric değerleri median ile doldur
            for col in numeric_cols:
                if features[col].isnull().any():
                    features[col].fillna(features[col].median(), inplace=True)
            
            # Categorical kolonları mode ile doldur
            categorical_cols = features.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if features[col].isnull().any():
                    mode_val = features[col].mode()
                    if len(mode_val) > 0:
                        features[col].fillna(mode_val[0], inplace=True)
                    else:
                        features[col].fillna("unknown", inplace=True)
            
            return features
        except Exception as e:
            logger.error(f"{self.name}: Error handling missing data: {str(e)}")
            return features
    
    def get_founding_date(self, symbol: str) -> Optional[str]:
        """
        Symbol için kuruluş tarihini getir
        
        Args:
            symbol: Şirket sembolü
            
        Returns:
            Optional[str]: Kuruluş tarihi (YYYY-MM-DD formatında) veya None
        """
        if not self.founding_dates:
            return None
            
        try:
            founding_date = self.founding_dates.get_founding_date(symbol)
            if founding_date:
                logger.debug(f"{self.name}: {symbol} founding date: {founding_date}")
                return founding_date
            else:
                logger.debug(f"{self.name}: {symbol} founding date not found")
                return None
        except Exception as e:
            logger.error(f"{self.name}: Error getting founding date for {symbol}: {str(e)}")
            return None
    
    def add_founding_date_features(self, features: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """
        Features dataframe'ine kuruluş tarihi temelli özellikler ekle
        
        Args:
            features: Mevcut feature dataframe
            symbol: Şirket sembolü
            
        Returns:
            pd.DataFrame: Founding date özellikleri eklenmiş dataframe
        """
        try:
            founding_date = self.get_founding_date(symbol)
            if founding_date:
                founding_year = int(founding_date.split('-')[0])
                current_year = datetime.now().year
                
                # Yaş hesapla
                company_age = current_year - founding_year
                
                # Özellikler ekle
                features['founding_year'] = founding_year
                features['company_age'] = company_age
                features['is_old_company'] = 1 if company_age > 50 else 0
                features['is_mature_company'] = 1 if company_age > 25 else 0
                features['is_young_company'] = 1 if company_age < 10 else 0
                
                # Decade categorization
                if founding_year < 1950:
                    features['founding_era'] = 0  # Very old
                elif founding_year < 1980:
                    features['founding_era'] = 1  # Old
                elif founding_year < 2000:
                    features['founding_era'] = 2  # Modern
                else:
                    features['founding_era'] = 3  # New age
                
                logger.debug(f"{self.name}: Added founding date features for {symbol} (age: {company_age})")
            else:
                # Default values for companies without founding date
                features['founding_year'] = 2000  # Default
                features['company_age'] = 25  # Default mature
                features['is_old_company'] = 0
                features['is_mature_company'] = 1
                features['is_young_company'] = 0
                features['founding_era'] = 2  # Modern default
                
                logger.debug(f"{self.name}: Used default founding date features for {symbol}")
            
            return features
        except Exception as e:
            logger.error(f"{self.name}: Error adding founding date features: {str(e)}")
            return features
    
    def create_fallback_result(self, error_msg: str = "") -> ModuleResult:
        """
        Hata durumunda fallback sonuç üret
        Arkadaşın 'zorunlu katkı' prensibine uygun - modül asla çalışmayı bırakmaz
        """
        return ModuleResult(
            score=50.0,  # Nötr skor
            uncertainty=1.0,  # Maksimum belirsizlik
            type=["fallback", "error"],
            explanation=f"Module fallback activated. {error_msg}",
            timestamp=datetime.now().isoformat(),
            confidence_level="LOW",
            contributing_factors={"fallback": 1.0}
        )
    
    def run_safe_inference(self, raw_data: Dict[str, Any]) -> ModuleResult:
        """
        Güvenli çıkarım - hata olsa bile sonuç döner
        Arkadaşın 'hiçbir modül skip edemez' prensibini uygular
        """
        try:
            self.prediction_count += 1
            self.last_prediction_time = datetime.now()
            
            # 1. Input validation
            if not self.validate_input(raw_data):
                return self.create_fallback_result("Input validation failed")
            
            # 2. Feature preparation
            features = self.prepare_features(raw_data)
            
            # 3. Missing data handling
            features = self.handle_missing_data(features)
            
            # 4. Inference
            result = self.infer(features)
            
            # 5. Result validation
            if not isinstance(result, ModuleResult):
                return self.create_fallback_result("Invalid result format")
            
            logger.info(f"{self.name}: Successful inference - Score: {result.score:.2f}, Uncertainty: {result.uncertainty:.3f}")
            return result
            
        except Exception as e:
            self.error_count += 1
            error_msg = f"Inference error: {str(e)}"
            logger.error(f"{self.name}: {error_msg}")
            return self.create_fallback_result(error_msg)
    
    def get_module_info(self) -> Dict[str, Any]:
        """Modül bilgilerini döner"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "is_trained": self.is_trained,
            "last_training_date": self.last_training_date,
            "prediction_count": self.prediction_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(1, self.prediction_count),
            "dependencies": self.dependencies,
            "required_fields": self.get_required_fields()
        }
    
    def save_model(self, filepath: str) -> bool:
        """Modeli kaydet"""
        try:
            model_data = {
                "name": self.name,
                "version": self.version,
                "model": self.model,
                "scaler": self.scaler,
                "feature_columns": self.feature_columns,
                "config": self.config,
                "performance_metrics": self.performance_metrics,
                "last_training_date": self.last_training_date
            }
            
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"{self.name}: Model saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"{self.name}: Error saving model: {str(e)}")
            return False
    
    def load_model(self, filepath: str) -> bool:
        """Modeli yükle"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data.get("model")
            self.scaler = model_data.get("scaler")
            self.feature_columns = model_data.get("feature_columns", [])
            self.performance_metrics = model_data.get("performance_metrics", {})
            self.last_training_date = model_data.get("last_training_date")
            
            self.is_trained = self.model is not None
            
            logger.info(f"{self.name}: Model loaded from {filepath}")
            return True
        except Exception as e:
            logger.error(f"{self.name}: Error loading model: {str(e)}")
            return False

class ModuleRegistry:
    """
    Expert Module kayıt sistemi
    Tüm modülleri merkezi olarak yönetir
    """
    
    def __init__(self):
        self.modules: Dict[str, ExpertModule] = {}
        self.module_configs: Dict[str, Dict] = {}
        self.load_order: List[str] = []
        
        # CompanyFoundingDates global registry entegrasyonu
        self.founding_dates = None
        if FOUNDING_DATES_AVAILABLE:
            try:
                self.founding_dates = CompanyFoundingDates()
                logger.info("ModuleRegistry: CompanyFoundingDates başarıyla entegre edildi")
            except Exception as e:
                logger.warning(f"ModuleRegistry: CompanyFoundingDates entegre edilemedi: {str(e)}")
        
    def register_module(self, module: ExpertModule, load_order: int = 0) -> bool:
        """Modül kaydet"""
        try:
            if not isinstance(module, ExpertModule):
                raise ValueError("Module must inherit from ExpertModule")
            
            self.modules[module.name] = module
            self.load_order.append((load_order, module.name))
            self.load_order.sort()  # Load order'a göre sırala
            
            logger.info(f"Module registered: {module.name}")
            return True
        except Exception as e:
            logger.error(f"Error registering module: {str(e)}")
            return False
    
    def get_module(self, name: str) -> Optional[ExpertModule]:
        """Modül getir"""
        return self.modules.get(name)
    
    def list_modules(self) -> List[str]:
        """Kayıtlı modül listesi"""
        return list(self.modules.keys())
    
    def get_modules_info(self) -> Dict[str, Dict]:
        """Tüm modüllerin bilgileri"""
        return {name: module.get_module_info() for name, module in self.modules.items()}
    
    def validate_all_modules(self, sample_data: Dict[str, Any]) -> Dict[str, bool]:
        """Tüm modülleri test et"""
        results = {}
        for name, module in self.modules.items():
            try:
                result = module.run_safe_inference(sample_data)
                results[name] = isinstance(result, ModuleResult) and result.score is not None
            except Exception as e:
                logger.error(f"Module validation failed for {name}: {str(e)}")
                results[name] = False
        return results
    
    def get_founding_date_for_all_modules(self, symbol: str) -> Optional[str]:
        """
        Tüm modüller için ortak founding date erişimi
        
        Args:
            symbol: Şirket sembolü
            
        Returns:
            Optional[str]: Kuruluş tarihi veya None
        """
        if not self.founding_dates:
            return None
            
        try:
            return self.founding_dates.get_founding_date(symbol)
        except Exception as e:
            logger.error(f"ModuleRegistry: Error getting founding date for {symbol}: {str(e)}")
            return None
    
    def get_founding_dates_stats(self) -> Dict[str, Any]:
        """
        Founding dates veritabanı istatistikleri
        
        Returns:
            Dict: İstatistik bilgileri
        """
        if not self.founding_dates:
            return {"status": "not_available", "count": 0}
            
        try:
            # CompanyFoundingDates sınıfında get_stats metodu varsa çağır
            if hasattr(self.founding_dates, 'get_stats'):
                return self.founding_dates.get_stats()
            else:
                return {"status": "available", "count": "unknown"}
        except Exception as e:
            logger.error(f"ModuleRegistry: Error getting founding dates stats: {str(e)}")
            return {"status": "error", "error": str(e)}

# Global module registry
module_registry = ModuleRegistry()

def get_registry() -> ModuleRegistry:
    """Global registry'ye erişim"""
    return module_registry

if __name__ == "__main__":
    # Test örneği
    print("🏗️ MULTI-EXPERT ENGINE CORE SYSTEM")
    print("="*50)
    
    # Sample test data
    test_data = {
        "symbol": "GARAN",
        "timestamp": datetime.now().isoformat(),
        "price": 25.50,
        "volume": 1000000,
        "market_cap": 50000000000
    }
    
    print(f"✅ ExpertModule base class implemented")
    print(f"✅ ModuleResult standardized")
    print(f"✅ ModuleRegistry created")
    print(f"✅ Safe inference with mandatory contribution")
    print(f"✅ Error handling and fallback system")
    
    print(f"\n🎯 Ready for module implementations!")
    print(f"📊 Test data format: {list(test_data.keys())}")
    
    # Registry test
    registry = get_registry()
    print(f"📋 Registry initialized: {len(registry.modules)} modules")