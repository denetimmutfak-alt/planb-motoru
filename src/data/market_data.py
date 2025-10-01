
"""
PlanB Motoru - Piyasa Veri Yönetimi
Hephaistos & Hermes Entegrasyonlu
"""
import yfinance as yf
import pandas as pd
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug, log_warning
from config.settings import config
from src.data.providers import (
    BISTProvider, NASDAQProvider, XETRAProvider, 
    CryptoProvider, CommoditiesProvider
)
from src.data.providers.simple_provider import SimpleProvider
from src.data.providers.hybrid_provider import HybridProvider

class MarketDataProvider:
    """Piyasa verilerini yöneten ana sınıf"""
    
    def __init__(self):
        self.config = config.load_from_file()
        self.markets_config = self.config.get('markets', {})
        
        # Provider'ları başlat
        self.providers = {
            'bist': BISTProvider(),
            'nasdaq': NASDAQProvider(),
            'xetra': XETRAProvider(),
            'crypto': CryptoProvider(),
            'commodities': CommoditiesProvider()
        }
        
        # Basit veri sağlayıcısı
        # Hibrit provider'ı aktif et (fallback olarak SimpleProvider)
        # Basit ve hızlı çözüm: Sadece Yahoo Finance
        self.data_provider = SimpleProvider()
        log_info("SimpleProvider (Yahoo Finance) aktif edildi")
        
        # Eski uyumluluk için
        self.simple_provider = self.data_provider
        
        log_info("Market data provider başlatıldı")
    
    def get_bist_symbols(self) -> List[str]:
        """BIST hisse senetlerini getir"""
        try:
            if not self.markets_config.get('bist', {}).get('enabled', True):
                return []
            
            symbols = self.providers['bist'].get_symbols()
            log_info(f"BIST: {len(symbols)} hisse senedi yüklendi")
            return symbols
            
        except Exception as e:
            log_error(f"BIST listesi alınamadı: {e}")
            return []
    
    def get_nasdaq_symbols(self) -> List[str]:
        """NASDAQ hisse senetlerini getir"""
        try:
            if not self.markets_config.get('nasdaq', {}).get('enabled', True):
                return []
            
            symbols = self.providers['nasdaq'].get_symbols()
            log_info(f"NASDAQ: {len(symbols)} hisse senedi yüklendi")
            return symbols
            
        except Exception as e:
            log_error(f"NASDAQ listesi alınamadı: {e}")
            return []
    
    def get_xetra_symbols(self) -> List[str]:
        """XETRA hisse senetlerini getir"""
        try:
            if not self.markets_config.get('xetra', {}).get('enabled', True):
                return []
            
            symbols = self.providers['xetra'].get_symbols()
            log_info(f"XETRA: {len(symbols)} hisse senedi yüklendi")
            return symbols
            
        except Exception as e:
            log_error(f"XETRA listesi alınamadı: {e}")
            return []
    
    def get_crypto_symbols(self) -> List[str]:
        """Kripto para sembollerini getir"""
        try:
            if not self.markets_config.get('crypto', {}).get('enabled', True):
                return []
            
            symbols = self.providers['crypto'].get_symbols()
            log_info(f"Kripto: {len(symbols)} coin yüklendi")
            return symbols
            
        except Exception as e:
            log_error(f"Kripto listesi alınamadı: {e}")
            return []
    
    def get_commodity_symbols(self) -> List[str]:
        """Emtia sembollerini getir"""
        try:
            if not self.markets_config.get('commodities', {}).get('enabled', True):
                return []
            
            symbols = self.providers['commodities'].get_symbols()
            log_info(f"Emtia: {len(symbols)} sembol yüklendi")
            return symbols
            
        except Exception as e:
            log_error(f"Emtia listesi alınamadı: {e}")
            return []
    
    def get_all_symbols(self, test_mode: bool = None) -> List[str]:
        """Tüm piyasa sembollerini getir"""
        if test_mode is None:
            test_mode = config.TEST_MODE
            
        if test_mode:
            log_info("Test modu aktif - sadece test sembolleri yüklenecek")
            log_info(f"Test sembolleri: {config.TEST_SYMBOLS}")
            return config.TEST_SYMBOLS
        
        all_symbols = []
        all_symbols.extend(self.get_bist_symbols())
        all_symbols.extend(self.get_nasdaq_symbols())
        all_symbols.extend(self.get_xetra_symbols())
        all_symbols.extend(self.get_crypto_symbols())
        all_symbols.extend(self.get_commodity_symbols())
        
        # Tekrarları kaldır
        unique_symbols = list(set(all_symbols))
        log_info(f"Toplam {len(unique_symbols)} benzersiz sembol yüklendi")
        
        return unique_symbols
    
    def get_stock_data(self, symbol: str, period: str = None) -> Optional[pd.DataFrame]:
        """Belirli bir sembol için hisse senedi verilerini getir - Hibrit API kullanır"""
        if period is None:
            period = config.DEFAULT_PERIOD
        
        try:
            # Basit provider kullan
            data_dict = self.simple_provider.get_stock_data(symbol, period)
            
            if not data_dict:
                log_warning(f"{symbol} için veri bulunamadı")
                return None
            
            # Dict'i DataFrame'e çevir
            data = pd.DataFrame.from_dict(data_dict, orient='index')
            data.index = pd.to_datetime(data.index)
            data = data.sort_index()
            
            log_debug(f"{symbol} için {len(data)} günlük veri yüklendi (Hibrit API)")
            return data
            
        except Exception as e:
            log_error(f"{symbol} veri alınırken hata: {e}")
            return None
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """Hisse senedi bilgilerini getir - Hibrit API kullanır"""
        try:
            # Basit provider kullan
            info = self.simple_provider.get_company_info(symbol)
            
            if not info:
                log_warning(f"{symbol} için bilgi bulunamadı")
                return None
            
            return info
            
        except Exception as e:
            log_error(f"{symbol} bilgisi alınırken hata: {e}")
            return None
    
    def get_provider_stats(self) -> Dict[str, any]:
        """Tüm provider'ların istatistiklerini getir"""
        stats = {}
        
        for provider_name, provider in self.providers.items():
            try:
                stats[provider_name] = provider.get_provider_stats()
            except Exception as e:
                log_error(f"{provider_name} istatistikleri alınamadı: {e}")
                stats[provider_name] = {
                    'provider_name': provider_name,
                    'status': 'error',
                    'error': str(e)
                }
        
        return stats
    
    def get_market_summary(self) -> Dict[str, any]:
        """Piyasa özetini getir"""
        try:
            summary = {
                'total_symbols': 0,
                'markets': {},
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            for provider_name, provider in self.providers.items():
                try:
                    provider_stats = provider.get_provider_stats()
                    market_info = provider.get_market_info()
                    
                    summary['markets'][provider_name] = {
                        'symbol_count': provider_stats['symbol_count'],
                        'market_name': market_info['market_name'],
                        'country': market_info['country'],
                        'currency': market_info['currency'],
                        'status': provider_stats['status']
                    }
                    
                    summary['total_symbols'] += provider_stats['symbol_count']
                    
                except Exception as e:
                    log_error(f"{provider_name} özet bilgisi alınamadı: {e}")
                    summary['markets'][provider_name] = {
                        'symbol_count': 0,
                        'status': 'error',
                        'error': str(e)
                    }
            
            return summary
            
        except Exception as e:
            log_error(f"Piyasa özeti oluşturulurken hata: {e}")
            return {
                'total_symbols': 0,
                'markets': {},
                'error': str(e),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def get_top_symbols_by_market(self, market: str, limit: int = 20) -> List[str]:
        """Belirli piyasada en çok işlem gören sembolleri getir"""
        try:
            if market.lower() not in self.providers:
                log_error(f"Bilinmeyen piyasa: {market}")
                return []
            
            provider = self.providers[market.lower()]
            return provider.get_top_symbols(limit)
            
        except Exception as e:
            log_error(f"{market} top sembolleri alınamadı: {e}")
            return []
    
    def get_sector_symbols(self, market: str, sector: str) -> List[str]:
        """Belirli piyasa ve sektördeki sembolleri getir"""
        try:
            if market.lower() not in self.providers:
                log_error(f"Bilinmeyen piyasa: {market}")
                return []
            
            provider = self.providers[market.lower()]
            
            # Provider'ın sektör metodunu kontrol et
            if hasattr(provider, 'get_sector_symbols'):
                return provider.get_sector_symbols(sector)
            elif hasattr(provider, 'get_category_symbols'):
                return provider.get_category_symbols(sector)
            else:
                log_warning(f"{market} provider'ı sektör desteği sağlamıyor")
                return []
                
        except Exception as e:
            log_error(f"{market} {sector} sektör sembolleri alınamadı: {e}")
            return []
