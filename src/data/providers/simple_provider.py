"""
PlanB Motoru - Basit Veri Sağlayıcısı
Sadece çalışan API'leri kullanır
"""
import yfinance as yf
import time
import random
from typing import Dict, Optional, List
from .base_provider import BaseProvider
from src.utils.logger import log_info, log_error, log_debug, log_warning

class SimpleProvider(BaseProvider):
    """Basit ve güvenilir veri sağlayıcısı"""
    
    def __init__(self):
        super().__init__("Simple")
        self.request_count = 0
        self.max_requests_per_minute = 5  # Çok güvenli limit
        self.symbols = []  # Abstract method için
        
    def get_stock_data(self, symbol: str, period: str = "1y") -> Optional[Dict]:
        """Hisse senedi verilerini getir - sadece Yahoo Finance"""
        try:
            # Rate limiting
            self._wait_for_rate_limit()
            
            log_debug(f"{symbol} için veri alınıyor...")
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            # DataFrame kontrolü düzeltildi
            if data is None or len(data) == 0:
                log_warning(f"{symbol} için veri bulunamadı")
                return None
            
            # Dict'e çevir - SÜTUN İSİMLERİNİ BÜYÜK HARFLE GÖNDER!
            formatted_data = {}
            for date, row in data.iterrows():
                formatted_data[date.strftime('%Y-%m-%d')] = {
                    'Open': float(row['Open']),
                    'High': float(row['High']),
                    'Low': float(row['Low']),
                    'Close': float(row['Close']),
                    'Volume': int(row['Volume'])
                }
            
            log_info(f"{symbol} verisi alındı ({len(formatted_data)} gün)")
            return formatted_data
            
        except Exception as e:
            log_error(f"{symbol} veri alınırken hata: {e}")
            return None
    
    def get_crypto_data(self, symbol: str) -> Optional[Dict]:
        """Kripto para verilerini getir"""
        return self.get_stock_data(symbol, "1y")
    
    def get_company_info(self, symbol: str) -> Optional[Dict]:
        """Şirket bilgilerini getir"""
        try:
            self._wait_for_rate_limit()
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info:
                return None
            
            return {
                'name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', ''),
                'pe_ratio': info.get('trailingPE', ''),
                'dividend_yield': info.get('dividendYield', '')
            }
            
        except Exception as e:
            log_error(f"{symbol} bilgisi alınırken hata: {e}")
            return None
    
    def _wait_for_rate_limit(self):
        """Rate limit için bekle"""
        self.request_count += 1
        
        if self.request_count >= self.max_requests_per_minute:
            log_debug("Rate limit - 60 saniye bekleniyor...")
            time.sleep(60)
            self.request_count = 0
        else:
            # 5 istek/dakika için 12 saniye bekle
            wait_time = 12 + random.uniform(0, 3)  # Rastgele ekleme
            log_debug(f"Rate limit için {wait_time:.1f} saniye bekleniyor...")
            time.sleep(wait_time)
    
    def get_symbols(self) -> List[str]:
        """Sembol listesini getir"""
        return self.symbols.copy()
    
    def get_market_info(self) -> Dict[str, any]:
        """Pazar bilgilerini getir"""
        return {
            'market_name': 'Simple',
            'country': 'Global',
            'currency': 'USD',
            'timezone': 'UTC',
            'trading_hours': '24/7',
            'symbol_count': len(self.symbols)
        }

