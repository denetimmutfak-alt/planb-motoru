"""
PlanB Motoru - Hibrit Veri Sağlayıcısı
Birden fazla API'yi kullanarak güvenilirlik sağlar
"""
import yfinance as yf
import requests
import time
import random
from typing import Dict, Optional, List
from .base_provider import BaseProvider
from src.utils.logger import log_info, log_error, log_debug, log_warning

class HybridProvider(BaseProvider):
    """Hibrit veri sağlayıcısı - birden fazla API kullanır"""
    
    def __init__(self):
        super().__init__("Hybrid")
        self.request_count = 0
        self.max_requests_per_minute = 30  # Daha hızlı
        self.symbols = []
        
        # API anahtarları (config'den alınacak)
        self.alpha_vantage_key = self._load_api_key('ALPHA_VANTAGE')
        self.fmp_key = self._load_api_key('FINANCIAL_MODELING_PREP')
        
        # API öncelik sırası
        self.api_priority = [
            'alpha_vantage',
            'financial_modeling_prep', 
            'yahoo_finance',
            'static_fallback'
        ]
        
    def get_stock_data(self, symbol: str, period: str = "1y") -> Optional[Dict]:
        """Hisse senedi verilerini getir - hibrit yaklaşım"""
        
        for api_name in self.api_priority:
            try:
                log_debug(f"{symbol} için {api_name} deneniyor...")
                
                if api_name == 'alpha_vantage':
                    data = self._get_alpha_vantage_data(symbol, period)
                elif api_name == 'financial_modeling_prep':
                    data = self._get_fmp_data(symbol, period)
                elif api_name == 'yahoo_finance':
                    data = self._get_yahoo_data(symbol, period)
                elif api_name == 'static_fallback':
                    data = self._get_static_data(symbol)
                
                if data is not None:
                    # DataFrame kontrolü
                    if hasattr(data, 'empty'):
                        if not data.empty:
                            log_info(f"{symbol} verisi {api_name} ile alındı ({len(data)} gün)")
                            return self._format_data(data)
                    else:
                        # Dict format
                        log_info(f"{symbol} verisi {api_name} ile alındı ({len(data)} gün)")
                        return self._format_data(data)
                    
            except Exception as e:
                log_warning(f"{symbol} {api_name} ile alınamadı: {e}")
                continue
        
        log_error(f"{symbol} hiçbir API ile alınamadı")
        return None
    
    def _get_alpha_vantage_data(self, symbol: str, period: str) -> Optional[Dict]:
        """Alpha Vantage API'den veri al"""
        if not self.alpha_vantage_key:
            raise Exception("Alpha Vantage API key yok")
            
        # Rate limiting
        self._wait_for_rate_limit()
        
        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'apikey': self.alpha_vantage_key,
            'outputsize': 'full'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'Error Message' in data:
            raise Exception(data['Error Message'])
            
        if 'Note' in data:
            raise Exception("API limit aşıldı")
            
        return self._parse_alpha_vantage_data(data)
    
    def _get_fmp_data(self, symbol: str, period: str) -> Optional[Dict]:
        """Financial Modeling Prep API'den veri al"""
        if not self.fmp_key:
            raise Exception("FMP API key yok")
            
        # Rate limiting
        self._wait_for_rate_limit()
        
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}"
        params = {
            'apikey': self.fmp_key,
            'from': self._get_start_date(period),
            'to': self._get_end_date()
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'Error Message' in data:
            raise Exception(data['Error Message'])
            
        return self._parse_fmp_data(data)
    
    def _get_yahoo_data(self, symbol: str, period: str) -> Optional[Dict]:
        """Yahoo Finance'den veri al (fallback)"""
        # Rate limiting
        self._wait_for_rate_limit()
        
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        
        # DataFrame kontrolü düzeltildi
        if data is None or len(data) == 0:
            raise Exception("Veri bulunamadı")
            
        return data
    
    def _get_static_data(self, symbol: str) -> Optional[Dict]:
        """Statik veri (son çare)"""
        # Bu sembol için önceden kaydedilmiş veri varsa kullan
        # Şimdilik None döndür
        return None
    
    def _format_data(self, data) -> Dict:
        """Veriyi standart formata çevir"""
        if hasattr(data, 'iterrows'):  # Pandas DataFrame
            formatted_data = {}
            for date, row in data.iterrows():
                formatted_data[date.strftime('%Y-%m-%d')] = {
                    'Open': float(row['Open']),
                    'High': float(row['High']),
                    'Low': float(row['Low']),
                    'Close': float(row['Close']),
                    'Volume': int(row['Volume'])
                }
            return formatted_data
        else:  # Dict format
            return data
    
    def _wait_for_rate_limit(self):
        """Rate limiting kontrolü - optimize edildi"""
        self.request_count += 1
        if self.request_count >= self.max_requests_per_minute:
            log_info("Rate limit - 5 saniye bekleniyor...")
            time.sleep(5)  # 60 saniye yerine 5 saniye
            self.request_count = 0
        else:
            time.sleep(random.uniform(0.1, 0.3))  # Daha hızlı random delay
    
    def _get_start_date(self, period: str) -> str:
        """Period'dan başlangıç tarihi hesapla"""
        from datetime import datetime, timedelta
        
        if period == "1y":
            return (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        elif period == "6mo":
            return (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
        elif period == "3mo":
            return (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        else:
            return (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    def _get_end_date(self) -> str:
        """Bugünün tarihini döndür"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')
    
    def _parse_alpha_vantage_data(self, data: Dict) -> Dict:
        """Alpha Vantage verisini parse et"""
        import pandas as pd
        
        if 'Time Series (Daily)' not in data:
            raise Exception("Alpha Vantage veri formatı beklenmiyor")
        
        time_series = data['Time Series (Daily)']
        formatted_data = {}
        
        for date_str, values in time_series.items():
            formatted_data[date_str] = {
                'Open': float(values['1. open']),
                'High': float(values['2. high']),
                'Low': float(values['3. low']),
                'Close': float(values['4. close']),
                'Volume': int(values['5. volume'])
            }
        
        return formatted_data
    
    def _parse_fmp_data(self, data: Dict) -> Dict:
        """FMP verisini parse et"""
        if 'historical' not in data:
            raise Exception("FMP veri formatı beklenmiyor")
        
        historical = data['historical']
        formatted_data = {}
        
        for item in historical:
            date_str = item['date']
            formatted_data[date_str] = {
                'Open': float(item['open']),
                'High': float(item['high']),
                'Low': float(item['low']),
                'Close': float(item['close']),
                'Volume': int(item['volume'])
            }
        
        return formatted_data
    
    def get_market_info(self, symbol: str) -> Optional[Dict]:
        """Market bilgilerini getir"""
        try:
            # Basit market bilgisi
            if symbol.endswith('.IS'):
                return {'market': 'BIST', 'currency': 'TRY', 'country': 'Turkey'}
            elif symbol.endswith('.DE'):
                return {'market': 'XETRA', 'currency': 'EUR', 'country': 'Germany'}
            elif symbol.endswith('-USD'):
                return {'market': 'Crypto', 'currency': 'USD', 'country': 'Global'}
            elif symbol.endswith('=F'):
                return {'market': 'Commodities', 'currency': 'USD', 'country': 'Global'}
            else:
                return {'market': 'NASDAQ', 'currency': 'USD', 'country': 'USA'}
        except Exception as e:
            log_error(f"Market bilgisi alınırken hata: {e}")
            return None
    
    def get_symbols(self, market: str = None) -> List[str]:
        """Sembol listesini getir"""
        # Basit sembol listesi
        symbols = []
        if market == 'BIST' or market is None:
            symbols.extend(['THYAO.IS', 'AKBNK.IS', 'TUPRS.IS'])
        if market == 'NASDAQ' or market is None:
            symbols.extend(['AAPL', 'MSFT', 'GOOGL'])
        if market == 'Crypto' or market is None:
            symbols.extend(['BTC-USD', 'ETH-USD', 'ADA-USD'])
        
        return symbols
    
    def _load_api_key(self, service: str) -> Optional[str]:
        """API anahtarını config'den yükle"""
        try:
            from config.api_keys import get_api_key, is_api_enabled
            
            if not is_api_enabled(service):
                log_debug(f"{service} API devre dışı")
                return None
                
            key = get_api_key(service)
            if key:
                log_info(f"{service} API anahtarı yüklendi")
                return key
            else:
                log_warning(f"{service} API anahtarı bulunamadı")
                return None
                
        except Exception as e:
            log_error(f"API anahtarı yüklenirken hata: {e}")
            return None
    
    def get_company_info(self, symbol: str) -> Optional[Dict]:
        """Şirket bilgilerini getir"""
        try:
            # Basit şirket bilgisi
            if symbol.endswith('.IS'):
                return {
                    'name': f'{symbol} Şirketi',
                    'sector': 'Finansal',
                    'industry': 'Bankacılık',
                    'market_cap': 'Bilinmiyor',
                    'pe_ratio': 'Bilinmiyor',
                    'dividend_yield': 'Bilinmiyor'
                }
            elif symbol.endswith('.DE'):
                return {
                    'name': f'{symbol} Şirketi',
                    'sector': 'Teknoloji',
                    'industry': 'Yazılım',
                    'market_cap': 'Bilinmiyor',
                    'pe_ratio': 'Bilinmiyor',
                    'dividend_yield': 'Bilinmiyor'
                }
            elif symbol.endswith('-USD'):
                return {
                    'name': f'{symbol} Kripto Para',
                    'sector': 'Kripto',
                    'industry': 'Dijital Varlık',
                    'market_cap': 'Bilinmiyor',
                    'pe_ratio': 'Bilinmiyor',
                    'dividend_yield': 'Bilinmiyor'
                }
            elif symbol.endswith('=F'):
                return {
                    'name': f'{symbol} Emtia',
                    'sector': 'Emtia',
                    'industry': 'Ham Madde',
                    'market_cap': 'Bilinmiyor',
                    'pe_ratio': 'Bilinmiyor',
                    'dividend_yield': 'Bilinmiyor'
                }
            else:
                return {
                    'name': f'{symbol} Şirketi',
                    'sector': 'Teknoloji',
                    'industry': 'Yazılım',
                    'market_cap': 'Bilinmiyor',
                    'pe_ratio': 'Bilinmiyor',
                    'dividend_yield': 'Bilinmiyor'
                }
                
        except Exception as e:
            log_error(f"{symbol} bilgisi alınırken hata: {e}")
            return None
