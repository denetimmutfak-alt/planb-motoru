"""
Volatility Analysis Module
Enhanced volatility analysis with ultra integration support

Bu modül volatilite analizi sağlar ve ultra volatilite modülü ile entegrasyon destekler
"""

import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Optional

try:
    from .ultra_volatility import UltraVolatilityAnalyzer
    ULTRA_AVAILABLE = True
except ImportError:
    ULTRA_AVAILABLE = False


class VolatilityAnalyzer:
    """Volatilite analizi sistemi"""
    
    def __init__(self):
        """Analyzer'ı başlat"""
        self.name = "Volatility Analyzer"
        
        # Ultra analyzer'ı yükle (varsa)
        if ULTRA_AVAILABLE:
            try:
                self.ultra_analyzer = UltraVolatilityAnalyzer()
                self.ultra_mode = True
                self._log_info("Ultra Volatility Analyzer imported successfully")
            except Exception as e:
                self.ultra_mode = False
                self._log_error(f"Ultra Volatility Analyzer import failed: {str(e)}")
        else:
            self.ultra_mode = False
            self._log_info("Volatility Analyzer (compatibility mode) initialized")
    
    def get_volatility_score(self, symbol: str, data: Optional[pd.DataFrame] = None, 
                           timeframe: str = 'daily') -> float:
        """
        Volatilite skoru hesapla
        
        Args:
            symbol: Sembol
            data: Fiyat verisi (opsiyonel)
            timeframe: Zaman dilimi
            
        Returns:
            float: Volatilite skoru (0-100)
        """
        try:
            # Ultra modu aktifse ultra analiz kullan
            if self.ultra_mode:
                ultra_result = self.ultra_analyzer.analyze_ultra_volatility(symbol, timeframe)
                return ultra_result['ultra_volatility_score']
            
            # Compatibility mode - basit volatilite analizi
            return self._calculate_basic_volatility_score(symbol, data)
            
        except Exception as e:
            self._log_error(f"Volatility score calculation error: {str(e)}")
            return 50.0
    
    def _calculate_basic_volatility_score(self, symbol: str, data: Optional[pd.DataFrame] = None) -> float:
        """Basit volatilite skoru hesaplama"""
        try:
            # Simülasyon için basit volatilite skoru
            base_score = 50.0
            
            # Sektör volatilite ayarlaması
            sector_adjustment = self._get_sector_volatility_adjustment(symbol)
            
            # Random volatilite faktörü (gerçek implementasyonda piyasa verisi kullanılır)
            volatility_factor = np.random.uniform(0.8, 1.2)
            
            # Final score
            final_score = base_score + sector_adjustment + (volatility_factor - 1) * 20
            
            return max(0, min(100, final_score))
            
        except Exception as e:
            self._log_error(f"Basic volatility score calculation error: {str(e)}")
            return 50.0
    
    def _get_sector_volatility_adjustment(self, symbol: str) -> float:
        """Sektör volatilite ayarlaması"""
        # Basit sektör belirleme
        tech_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA']
        financial_symbols = ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C']
        energy_symbols = ['XOM', 'CVX', 'COP', 'SLB', 'HAL']
        
        if symbol in tech_symbols:
            return -5  # Tech genelde yüksek volatilite
        elif symbol in financial_symbols:
            return -10  # Financial volatilite riskli
        elif symbol in energy_symbols:
            return -15  # Energy en volatil
        else:
            return 0
    
    def _log_info(self, message: str):
        """Info log"""
        print(f"INFO: {message}")
    
    def _log_error(self, message: str):
        """Error log"""
        print(f"ERROR: {message}")
