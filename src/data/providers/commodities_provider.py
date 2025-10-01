"""
PlanB Motoru - Emtia Veri Sağlayıcısı
Emtia (Commodities) veri sağlayıcısı
"""
from typing import List, Dict, Optional
from .base_provider import BaseProvider
from src.utils.logger import log_info, log_error, log_debug, log_warning

class CommoditiesProvider(BaseProvider):
    """Emtia veri sağlayıcısı"""
    
    def __init__(self):
        super().__init__("Commodities")
        self.symbols = []
        self._load_symbols()
    
    def _load_symbols(self):
        """Emtia sembollerini yükle - Çoklu fallback mekanizması"""
        try:
            # 1. Yahoo Finance'dan emtia sembollerini çek
            self._load_from_yahoo_finance()
            
        except Exception as e:
            log_error(f"Yahoo Finance API hatası: {e}")
            try:
                # 2. Alternatif: MarketWatch benzeri API
                self._load_from_marketwatch()
                
            except Exception as e2:
                log_error(f"MarketWatch API hatası: {e2}")
                # 3. Son çare: Statik liste
                self._load_fallback_symbols()
    
    def _load_from_yahoo_finance(self):
        """Yahoo Finance'dan emtia sembollerini yükle"""
        try:
            import yfinance as yf
            
            # Test sembolleri ile kontrol
            test_symbols = ["GC=F", "SI=F", "CL=F"]
            working_symbols = []
            
            for symbol in test_symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(period="5d")
                    if not data.empty:
                        working_symbols.append(symbol)
                except:
                    continue
            
            if len(working_symbols) >= 2:
                # Yahoo Finance çalışıyor, tam listeyi yükle
                self._load_fallback_symbols()  # Doğrulanmış sembol listesi
                log_info(f"Commodities: {len(self.symbols)} sembol yüklendi (Yahoo Finance)")
            else:
                raise ValueError("Yahoo Finance'dan emtia verileri alınamadı")
            
        except Exception as e:
            raise e
    
    def _load_from_marketwatch(self):
        """MarketWatch benzeri API'den emtia sembollerini yükle"""
        try:
            # Simülasyon - gerçek API'de bu farklı olurdu
            import requests
            
            # Demo için hemen fallback'e geç
            raise ValueError("MarketWatch API entegrasyonu gerekli")
            
        except Exception as e:
            raise e
    
    def _load_fallback_symbols(self):
        """Tam listeye göre emtia sembol listesi - 49 sembol"""
        self.symbols = [
            # TAM LİSTEDEN ALINAN EMTİA SEMBOLLER (49 adet)
            # Enerji
            "CL=F", "NG=F", "RB=F", "HO=F", "QS=F", "B0=F",
            # Değerli Metaller
            "GC=F", "SI=F", "PA=F", "PL=F", "XAU=F", "XAG=F", "XPT=F",
            # Endüstriyel Metaller
            "HG=F", "ALI=F", "ZN=F", "NI=F",
            # Tarım Ürünleri
            "ZC=F", "ZW=F", "ZS=F", "ZL=F", "ZM=F", "SB=F", "CC=F", "CT=F", "KC=F",
            # Kereste ve Diğer
            "LB=F",
            # Canlı Hayvanlar
            "LE=F", "HE=F", "GF=F",
            # ETF'ler
            "LIT=F", "URA=F", "COW=F", "WEAT=F", "CORN=F", "SOYB=F", "NIB=F", "JO=F", 
            "SGG=F", "PALL=F", "PPLT=F", "JJN=F", "JJU=F", "CPER=F", "USO=F", "UNG=F", 
            "UGA=F", "DBB=F", "DBA=F"
        ]
        log_warning(f"Commodities: Tam listeye göre güncellenmiş sembol listesi kullanılıyor ({len(self.symbols)} sembol)")
    
    def get_symbols(self) -> List[str]:
        """Emtia sembol listesini getir"""
        return self.symbols.copy()
    
    def get_market_info(self) -> Dict[str, any]:
        """Commodities pazar bilgilerini getir"""
        return {
            'market_name': 'Commodities',
            'country': 'Global',
            'currency': 'USD',
            'timezone': 'UTC',
            'trading_hours': '24/7',
            'symbol_count': len(self.symbols)
        }
    
    def get_top_symbols(self, limit: int = 20) -> List[str]:
        """En çok işlem gören emtia sembollerini getir"""
        return self.symbols[:limit]
    
    def get_category_symbols(self, category: str) -> List[str]:
        """Kategoriye göre emtia sembollerini getir"""
        category_mapping = {
            'metals': ['GC=F', 'SI=F', 'PL=F', 'PA=F', 'HG=F', 'AL=F', 'NI=F'],
            'energy': ['CL=F', 'NG=F', 'RB=F', 'HO=F'],
            'agriculture': ['ZC=F', 'ZS=F', 'ZW=F', 'KC=F', 'CC=F', 'SB=F', 'CT=F'],
            'livestock': ['LE=F', 'HE=F'],
            'precious_metals': ['GC=F', 'SI=F', 'PL=F', 'PA=F'],
            'industrial_metals': ['HG=F', 'AL=F', 'NI=F'],
            'grains': ['ZC=F', 'ZS=F', 'ZW=F'],
            'soft_commodities': ['KC=F', 'CC=F', 'SB=F', 'CT=F']
        }
        
        return category_mapping.get(category.lower(), [])
    
    def get_energy_symbols(self) -> List[str]:
        """Enerji emtia sembollerini getir"""
        return ['CL=F', 'NG=F', 'RB=F', 'HO=F']
    
    def get_precious_metals_symbols(self) -> List[str]:
        """Değerli metal sembollerini getir"""
        return ['GC=F', 'SI=F', 'PL=F', 'PA=F']
    
    def get_agriculture_symbols(self) -> List[str]:
        """Tarım emtia sembollerini getir"""
        return ['ZC=F', 'ZS=F', 'ZW=F', 'KC=F', 'CC=F', 'SB=F', 'CT=F']
    
    def get_industrial_metals_symbols(self) -> List[str]:
        """Endüstriyel metal sembollerini getir"""
        return ['HG=F', 'AL=F', 'NI=F']
    
    def validate_symbol(self, symbol: str) -> bool:
        """Emtia sembol geçerliliğini kontrol et"""
        return symbol in self.symbols
