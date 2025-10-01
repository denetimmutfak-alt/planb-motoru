"""
PlanB Motoru - Konfigürasyon Ayarları
"""
import os
from pathlib import Path
from typing import Dict, Any
import json

class Config:
    """Ana konfigürasyon sınıfı"""
    
    # Proje Yolları
    BASE_DIR = Path(__file__).parent.parent
    SRC_DIR = BASE_DIR / "src"
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    CONFIG_DIR = BASE_DIR / "config"
    
    # Veritabanı
    DATABASE_PATH = DATA_DIR / "analiz_gecmisi.db"
    
    # API Ayarları
    YAHOO_FINANCE_TIMEOUT = 30
    REQUEST_RETRY_COUNT = 3
    REQUEST_DELAY = 3  # saniye - rate limit için artırıldı
    
    # Analiz Ayarları
    DEFAULT_PERIOD = "1y"
    RSI_PERIOD = 14
    GANN_PERIOD = 52  # hafta
    
    # Dashboard Ayarları
    DASHBOARD_HOST = "0.0.0.0"
    DASHBOARD_PORT_RANGE = (5000, 5100)
    AUTO_REFRESH_INTERVAL = 30  # saniye
    
    # Loglama
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    
    # Test Modu
    TEST_MODE = False
    TEST_SYMBOLS = ["AAPL", "BTC-USD"]  # Test sembolleri
    
    # Vedik Astroloji
    VEDIC_ASTROLOGY_ENABLED = True  # Vedik astroloji analizi aktif/pasif
    VEDIC_FALLBACK_SCORE = 52.05   # Vedik analiz başarısız olursa kullanılacak skor
    
    @classmethod
    def load_from_file(cls, config_path: str = None) -> Dict[str, Any]:
        """JSON dosyasından konfigürasyon yükle"""
        if config_path is None:
            config_path = cls.CONFIG_DIR / "app_config.json"
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Konfigürasyon dosyası yüklenemedi: {e}")
                return {}
        return {}
    
    @classmethod
    def save_to_file(cls, config_data: Dict[str, Any], config_path: str = None):
        """Konfigürasyonu JSON dosyasına kaydet"""
        if config_path is None:
            config_path = cls.CONFIG_DIR / "app_config.json"
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Konfigürasyon dosyası kaydedilemedi: {e}")

# Geliştirme ortamı ayarları
class DevelopmentConfig(Config):
    DEBUG = False  # Debug mode'u kapat - stabil çalışma için
    LOG_LEVEL = "INFO"
    TEST_MODE = False

# Üretim ortamı ayarları  
class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "WARNING"
    TEST_MODE = False

# Aktif konfigürasyon
config = DevelopmentConfig()
