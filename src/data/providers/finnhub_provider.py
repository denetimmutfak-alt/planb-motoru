"""
PlanB Motoru - Finnhub Veri Sağlayıcısı
Finnhub API ile hızlı ve stabil veri çekme
"""
import finnhub
import time
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from .base_provider import BaseProvider
from src.utils.logger import log_info, log_error, log_debug, log_warning

class FinnhubProvider(BaseProvider):
    """Finnhub API veri sağlayıcısı"""
    
    def __init__(self):
        super().__init__("Finnhub")
        # Ücretsiz API key - günlük 60 istek limiti
        self.api_key = "demo"  # Demo key - gerçek kullanım için kayıt ol
        self.client = finnhub.Client(api_key=self.api_key)
        self.request_delay = 1  # 60 istek/dakika limiti için
        
    def get_stock_data(self, symbol: str, period: str = "1y") -> Optional[Dict]:
        """Hisse senedi verilerini getir"""
        try:
            # Tarih aralığı hesapla
            end_date = int(datetime.now().timestamp())
            start_date = int((datetime.now() - timedelta(days=365)).timestamp())
            
            # Finnhub'dan veri çek
            data = self.client.stock_candles(
                symbol=symbol,
                resolution='D',  # Günlük
                _from=start_date,
                to=end_date
            )
            
            if data and data.get('s') == 'ok':
                formatted_data = self._format_candles(data)
                log_debug(f"{symbol} verisi Finnhub'dan alındı")
                return formatted_data
            else:
                log_warning(f"{symbol} için veri bulunamadı")
                return None
                
        except Exception as e:
            log_error(f"Finnhub API hatası ({symbol}): {e}")
            return None
    
    def get_crypto_data(self, symbol: str) -> Optional[Dict]:
        """Kripto para verilerini getir"""
        try:
            # Crypto sembolünü temizle
            clean_symbol = symbol.replace("-USD", "")
            
            end_date = int(datetime.now().timestamp())
            start_date = int((datetime.now() - timedelta(days=365)).timestamp())
            
            data = self.client.crypto_candles(
                symbol=clean_symbol,
                resolution='D',
                _from=start_date,
                to=end_date
            )
            
            if data and data.get('s') == 'ok':
                formatted_data = self._format_candles(data)
                log_debug(f"{symbol} crypto verisi Finnhub'dan alındı")
                return formatted_data
            else:
                log_warning(f"{symbol} crypto için veri bulunamadı")
                return None
                
        except Exception as e:
            log_error(f"Finnhub Crypto API hatası ({symbol}): {e}")
            return None
    
    def _format_candles(self, data: Dict) -> Dict:
        """Mum verilerini formatla"""
        formatted = {}
        
        if 't' in data and 'o' in data and 'h' in data and 'l' in data and 'c' in data and 'v' in data:
            timestamps = data['t']
            opens = data['o']
            highs = data['h']
            lows = data['l']
            closes = data['c']
            volumes = data['v']
            
            for i, timestamp in enumerate(timestamps):
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                formatted[date] = {
                    'open': float(opens[i]),
                    'high': float(highs[i]),
                    'low': float(lows[i]),
                    'close': float(closes[i]),
                    'volume': int(volumes[i])
                }
        
        return formatted
    
    def get_company_info(self, symbol: str) -> Optional[Dict]:
        """Şirket bilgilerini getir"""
        try:
            profile = self.client.company_profile2(symbol=symbol)
            
            if profile:
                return {
                    'name': profile.get('name', ''),
                    'sector': profile.get('finnhubIndustry', ''),
                    'industry': profile.get('finnhubIndustry', ''),
                    'market_cap': profile.get('marketCapitalization', ''),
                    'country': profile.get('country', ''),
                    'currency': profile.get('currency', '')
                }
            else:
                return None
                
        except Exception as e:
            log_error(f"Şirket bilgisi alınamadı ({symbol}): {e}")
            return None
    
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """Anlık fiyat bilgisi getir"""
        try:
            quote = self.client.quote(symbol)
            
            if quote:
                return {
                    'current_price': quote.get('c', 0),
                    'change': quote.get('d', 0),
                    'change_percent': quote.get('dp', 0),
                    'high': quote.get('h', 0),
                    'low': quote.get('l', 0),
                    'open': quote.get('o', 0),
                    'previous_close': quote.get('pc', 0)
                }
            else:
                return None
                
        except Exception as e:
            log_error(f"Anlık fiyat alınamadı ({symbol}): {e}")
            return None
    
    def wait_for_rate_limit(self):
        """Rate limit için bekle"""
        time.sleep(self.request_delay)
        log_debug(f"Rate limit için {self.request_delay} saniye beklendi")

