"""
PlanB Motoru - Temel Veri Sağlayıcı Sınıfı
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import pandas as pd
from src.utils.logger import log_info, log_error, log_debug

class BaseProvider(ABC):
    """Tüm veri sağlayıcıları için temel sınıf"""
    
    def __init__(self, name: str):
        self.name = name
        self.symbols = []
        self.market_data = {}
    
    @abstractmethod
    def get_symbols(self) -> List[str]:
        """Sembol listesini getir"""
        pass
    
    @abstractmethod
    def get_market_info(self) -> Dict[str, any]:
        """Pazar bilgilerini getir"""
        pass
    
    def validate_symbol(self, symbol: str) -> bool:
        """Sembol geçerliliğini kontrol et"""
        try:
            symbols = self.get_symbols()
            return symbol in symbols
        except Exception as e:
            log_error(f"{self.name} sembol doğrulama hatası: {e}")
            return False
    
    def get_symbol_count(self) -> int:
        """Sembol sayısını getir"""
        try:
            return len(self.get_symbols())
        except Exception as e:
            log_error(f"{self.name} sembol sayısı alınamadı: {e}")
            return 0
    
    def get_provider_stats(self) -> Dict[str, any]:
        """Sağlayıcı istatistiklerini getir"""
        try:
            symbols = self.get_symbols()
            market_info = self.get_market_info()
            
            return {
                'provider_name': self.name,
                'symbol_count': len(symbols),
                'market_info': market_info,
                'status': 'active' if symbols else 'inactive'
            }
        except Exception as e:
            log_error(f"{self.name} istatistik alınamadı: {e}")
            return {
                'provider_name': self.name,
                'symbol_count': 0,
                'status': 'error',
                'error': str(e)
            }





