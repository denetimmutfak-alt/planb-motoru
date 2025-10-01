"""
PlanB Motoru - Alpha Vantage Veri Sağlayıcısı
Alpha Vantage API ile stabil veri çekme
"""
import requests
import time
from typing import Dict, Optional, List
from .base_provider import BaseProvider
from src.utils.logger import log_info, log_error, log_debug, log_warning

class AlphaVantageProvider(BaseProvider):
    """Alpha Vantage API veri sağlayıcısı"""
    
    def __init__(self):
        super().__init__("AlphaVantage")
        # Ücretsiz API key - günlük 25 istek limiti
        self.api_key = "demo"  # Demo key - gerçek kullanım için kayıt ol
        self.base_url = "https://www.alphavantage.co/query"
        self.request_delay = 12  # 5 istek/dakika limiti için
        
    def get_stock_data(self, symbol: str, period: str = "1y") -> Optional[Dict]:
        """Hisse senedi verilerini getir"""
        try:
            # Alpha Vantage parametreleri
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'outputsize': 'compact',  # Son 100 gün
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Hata kontrolü
            if 'Error Message' in data:
                log_error(f"Alpha Vantage API hatası: {data['Error Message']}")
                return None
                
            if 'Note' in data:
                log_warning(f"Alpha Vantage API limiti: {data['Note']}")
                return None
            
            # Veri formatla
            if 'Time Series (Daily)' in data:
                time_series = data['Time Series (Daily)']
                formatted_data = self._format_time_series(time_series)
                log_debug(f"{symbol} verisi Alpha Vantage'den alındı")
                return formatted_data
            else:
                log_warning(f"{symbol} için veri bulunamadı")
                return None
                
        except Exception as e:
            log_error(f"Alpha Vantage API hatası ({symbol}): {e}")
            return None
    
    def get_crypto_data(self, symbol: str) -> Optional[Dict]:
        """Kripto para verilerini getir"""
        try:
            # Crypto sembolünü temizle
            clean_symbol = symbol.replace("-USD", "")
            
            params = {
                'function': 'DIGITAL_CURRENCY_DAILY',
                'symbol': clean_symbol,
                'market': 'USD',
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Error Message' in data:
                log_error(f"Alpha Vantage Crypto API hatası: {data['Error Message']}")
                return None
                
            if 'Note' in data:
                log_warning(f"Alpha Vantage Crypto API limiti: {data['Note']}")
                return None
            
            if 'Time Series (Digital Currency Daily)' in data:
                time_series = data['Time Series (Digital Currency Daily)']
                formatted_data = self._format_crypto_time_series(time_series)
                log_debug(f"{symbol} crypto verisi Alpha Vantage'den alındı")
                return formatted_data
            else:
                log_warning(f"{symbol} crypto için veri bulunamadı")
                return None
                
        except Exception as e:
            log_error(f"Alpha Vantage Crypto API hatası ({symbol}): {e}")
            return None
    
    def _format_time_series(self, time_series: Dict) -> Dict:
        """Zaman serisi verilerini formatla"""
        formatted = {}
        for date, values in time_series.items():
            formatted[date] = {
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
                'volume': int(values['5. volume'])
            }
        return formatted
    
    def _format_crypto_time_series(self, time_series: Dict) -> Dict:
        """Kripto zaman serisi verilerini formatla"""
        formatted = {}
        for date, values in time_series.items():
            formatted[date] = {
                'open': float(values['1a. open (USD)']),
                'high': float(values['2a. high (USD)']),
                'low': float(values['3a. low (USD)']),
                'close': float(values['4a. close (USD)']),
                'volume': int(values['5. volume'])
            }
        return formatted
    
    def get_company_info(self, symbol: str) -> Optional[Dict]:
        """Şirket bilgilerini getir"""
        try:
            params = {
                'function': 'OVERVIEW',
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Error Message' in data:
                return None
                
            if 'Note' in data:
                return None
            
            return {
                'name': data.get('Name', ''),
                'sector': data.get('Sector', ''),
                'industry': data.get('Industry', ''),
                'market_cap': data.get('MarketCapitalization', ''),
                'pe_ratio': data.get('PERatio', ''),
                'dividend_yield': data.get('DividendYield', '')
            }
            
        except Exception as e:
            log_error(f"Şirket bilgisi alınamadı ({symbol}): {e}")
            return None
    
    def wait_for_rate_limit(self):
        """Rate limit için bekle"""
        time.sleep(self.request_delay)
        log_debug(f"Rate limit için {self.request_delay} saniye beklendi")

