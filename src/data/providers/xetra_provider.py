"""
PlanB Motoru - XETRA Veri Sağlayıcısı
XETRA (Frankfurt) borsası veri sağlayıcısı
"""
import pandas as pd
import requests
from typing import List, Dict, Optional
from .base_provider import BaseProvider
from src.utils.logger import log_info, log_error, log_debug, log_warning

class XETRAProvider(BaseProvider):
    """XETRA veri sağlayıcısı"""
    
    def __init__(self):
        super().__init__("XETRA")
        self.symbols = []
        self._load_symbols()
    
    def _load_symbols(self):
        """XETRA sembollerini yükle - Tüm aktif hisseler"""
        try:
            # Deutsche Börse resmi sitesinden tüm sembolleri çek
            url = "https://www.boerse-frankfurt.de/en/data/equities"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # HTML'den sembolleri çıkar
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            symbols = []
            # Farklı tablo yapılarını deneyelim
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')[1:]  # Header'ı atla
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        symbol_text = cells[0].get_text(strip=True)
                        if symbol_text and len(symbol_text) <= 10 and '.' in symbol_text:
                            symbols.append(symbol_text)
            
            if symbols:
                self.symbols = list(set(symbols))  # Duplikatları kaldır
                log_info(f"XETRA: {len(self.symbols)} sembol yüklendi (resmi siteden)")
            else:
                raise ValueError("Sembol bulunamadı")
            
        except Exception as e:
            log_error(f"XETRA sembolleri resmi siteden yüklenirken hata: {e}")
            try:
                # Alternatif: Investing.com'dan XETRA hisselerini çek
                self._load_from_investing()
            except Exception as e2:
                log_error(f"Investing'den yükleme hatası: {e2}")
                # Son çare: Genişletilmiş fallback liste
                self._load_fallback_symbols()
    
    def _load_from_investing(self):
        """Investing.com'dan XETRA hisselerini yükle"""
        try:
            url = "https://www.investing.com/equities/germany"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            symbols = []
            # Investing.com tablo yapısı
            table = soup.find('table', {'class': 'genTbl closedTbl crossRatesTbl'})
            if table:
                rows = table.find_all('tr')[1:]  # Header'ı atla
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        symbol_text = cells[0].get_text(strip=True).split()[0]
                        if symbol_text and len(symbol_text) <= 10:
                            symbols.append(symbol_text)
            
            if symbols:
                self.symbols = list(set(symbols))
                log_info(f"XETRA: {len(self.symbols)} sembol yüklendi (Investing'den)")
            else:
                raise ValueError("Investing'den sembol bulunamadı")
                
        except Exception as e:
            raise e
    
    def _load_fallback_symbols(self):
        """Tam listeye göre XETRA sembol listesi - 157 sembol"""
        self.symbols = [
            # TAM LİSTEDEN ALINAN XETRA SEMBOLLER (157 adet)
            "ADS", "AIR", "ALV", "BAS", "BAYN", "BEI", "BMW", "CON", "1COV", "DAI", 
            "DBK", "DB1", "DHL", "DTE", "EOAN", "FME", "FRE", "HEN3", "IFX", "MBG", 
            "MRK", "MTX", "MUV2", "PUM", "RWE", "SAP", "SIE", "VNA", "VOW3", "ZAL", 
            "ENR", "QIA", "SHL", "NDA", "EVK", "HFG", "BNR", "SRT3", "AFX", "GXI", 
            "DUE", "HEI", "RHM", "SY1", "HOT", "FNTN", "UN01", "O2D", "PSM", "TLX", 
            "WCH", "BOSS", "KRN", "LEG", "LIN", "NEM", "PAH3", "1N8", "SOW", "TEG", 
            "UTDI", "ACX", "AOF", "ARL", "BYW6", "CEC", "CLS", "COP", "DBAN", "DEQ", 
            "DEZ", "DRI", "DRW3", "EVD", "EVT", "FIE", "FPE3", "GFT", "G24", "GMM", 
            "HBH", "HLE", "HNR1", "JUN3", "KCO", "KWS", "LXS", "MOR", "NDX1", "OSR", 
            "PBB", "RAA", "RHK", "SANT", "DHER", "S92", "SPR", "ADJ", "AIXA", "AMA", 
            "AOX", "AT1", "BC8", "BDT", "B4B", "B5A", "CAP", "CBK", "D6H", "DKG", 
            "DMP", "EWK", "FRA", "FPH", "G1A", "GBF", "GSC1", "HAG", "HAW", "HBM", 
            "HDD", "HHFA", "HXL", "INH", "KTG", "LHA", "LXC", "MBQ", "M5Z", "NOEJ", 
            "RRTL", "SAX", "SDF", "SGL", "STM", "SUSE", "SZG", "SZX", "TKA", "TTK", 
            "TTR", "VOS", "WAC", "WDI", "WUW", "ZIL2", "3BG", "4PS", "5CV", "7CD", 
            "8GP", "AAD", "AAH", "ABR", "ABEA", "BBZA", "ADL"
        ]
        log_warning(f"XETRA: Tam listeye göre güncellenmiş sembol listesi kullanılıyor ({len(self.symbols)} sembol)")
    
    def get_symbols(self) -> List[str]:
        """XETRA sembol listesini getir"""
        return self.symbols.copy()
    
    def get_market_info(self) -> Dict[str, any]:
        """XETRA pazar bilgilerini getir"""
        return {
            'market_name': 'XETRA',
            'country': 'Germany',
            'currency': 'EUR',
            'timezone': 'Europe/Berlin',
            'trading_hours': '09:00-17:30',
            'symbol_count': len(self.symbols)
        }
    
    def get_top_symbols(self, limit: int = 20) -> List[str]:
        """En çok işlem gören sembolleri getir (DAX 40)"""
        dax_40 = [
            "SAP.DE", "SIE.DE", "ALV.DE", "DTE.DE", "BAYN.DE",
            "BMW.DE", "DAI.DE", "VOW3.DE", "BAS.DE", "MRK.DE",
            "ADS.DE", "CON.DE", "DBK.DE", "FRE.DE", "HEI.DE",
            "IFX.DE", "LHA.DE", "LIN.DE", "MTX.DE", "RWE.DE",
            "VNA.DE", "ZAL.DE", "1COV.DE", "DHER.DE", "EOAN.DE",
            "HEN3.DE", "HNR1.DE", "QGEN.DE", "SHL.DE", "SY1.DE",
            "VOW3.DE", "WCH.DE", "BEI.DE", "BMW.DE", "CON.DE",
            "DAI.DE", "DBK.DE", "DTE.DE", "FRE.DE", "HEI.DE"
        ]
        
        return dax_40[:limit]
    
    def get_sector_symbols(self, sector: str) -> List[str]:
        """Belirli sektördeki sembolleri getir"""
        sector_mapping = {
            'technology': ['SAP.DE', 'SIE.DE', 'IFX.DE', 'QGEN.DE'],
            'automotive': ['BMW.DE', 'DAI.DE', 'VOW3.DE', 'VNA.DE'],
            'pharmaceuticals': ['BAYN.DE', 'MRK.DE', 'SHL.DE'],
            'chemicals': ['BAS.DE', 'LIN.DE', '1COV.DE'],
            'banking': ['DBK.DE', 'CBK.DE', 'WCH.DE'],
            'insurance': ['ALV.DE', 'FRE.DE', 'HNR1.DE'],
            'energy': ['RWE.DE', 'EOAN.DE', 'UN01.DE'],
            'retail': ['ADS.DE', 'ZAL.DE', 'BEI.DE'],
            'telecommunications': ['DTE.DE', 'VOW3.DE'],
            'utilities': ['RWE.DE', 'EOAN.DE', 'UN01.DE']
        }
        
        return sector_mapping.get(sector.lower(), [])
    
    def get_dax_symbols(self) -> List[str]:
        """DAX 40 sembollerini getir"""
        return self.get_top_symbols(40)
    
    def get_mdax_symbols(self) -> List[str]:
        """MDAX sembollerini getir (Mid Cap)"""
        mdax_symbols = [
            "AIR.DE", "ALG.DE", "ARL.DE", "AT1.DE", "BIO3.DE",
            "BOSS.DE", "BVB.DE", "COK.DE", "DUE.DE", "EVK.DE",
            "FIE.DE", "FPE3.DE", "G1A.DE", "GIL.DE", "GXI.DE",
            "HLE.DE", "HOT.DE", "JEN.DE", "KGX.DE", "KRN.DE"
        ]
        
        return mdax_symbols
    
    def get_sdax_symbols(self) -> List[str]:
        """SDAX sembollerini getir (Small Cap)"""
        sdax_symbols = [
            "AAD.DE", "ACX.DE", "ADJ.DE", "ADN1.DE", "ADV.DE",
            "AEIN.DE", "AFX.DE", "AG1.DE", "AOF.DE", "ARL.DE",
            "AT1.DE", "AUS.DE", "B8F.DE", "BCO.DE", "BDT.DE"
        ]
        
        return sdax_symbols
    
    def validate_symbol(self, symbol: str) -> bool:
        """XETRA sembol geçerliliğini kontrol et"""
        return symbol in self.symbols
    
    def get_company_info(self, symbol: str) -> Optional[Dict[str, any]]:
        """Şirket bilgilerini getir"""
        if not symbol.endswith('.DE'):
            symbol = f"{symbol}.DE"
        
        if symbol not in self.symbols:
            return None
        
        # XETRA şirket bilgileri (isim + kuruluş tarihi)
        company_info = {
            "SAP.DE": {"name": "SAP SE", "founding_date": "1972-04-01"},
            "SIE.DE": {"name": "Siemens AG", "founding_date": "1847-10-12"},
            "BAS.DE": {"name": "BASF SE", "founding_date": "1865-04-06"},
            "BAYN.DE": {"name": "Bayer AG", "founding_date": "1863-08-01"},
            "ALV.DE": {"name": "Allianz SE", "founding_date": "1871-05-19"},
            "DAI.DE": {"name": "Daimler AG", "founding_date": "1926-06-28"},
            "BMW.DE": {"name": "BMW AG", "founding_date": "1916-03-07"},
            "VOW3.DE": {"name": "Volkswagen AG", "founding_date": "1937-05-28"},
            "ADS.DE": {"name": "Adidas AG", "founding_date": "1949-08-18"},
            "LHA.DE": {"name": "Deutsche Lufthansa AG", "founding_date": "1953-01-01"},
            "MRK.DE": {"name": "Merck KGaA", "founding_date": "1668-01-01"},
            "FRE.DE": {"name": "Fresenius SE & Co. KGaA", "founding_date": "1912-01-01"},
            "DTE.DE": {"name": "Deutsche Telekom AG", "founding_date": "1995-01-01"},
            "VNA.DE": {"name": "Vonovia SE", "founding_date": "2001-01-01"},
            "RWE.DE": {"name": "RWE AG", "founding_date": "1898-04-25"},
            "ENR.DE": {"name": "Siemens Energy AG", "founding_date": "2020-04-01"},
            "IFX.DE": {"name": "Infineon Technologies AG", "founding_date": "1999-04-01"},
            "CON.DE": {"name": "Continental AG", "founding_date": "1871-10-08"},
            "HEN3.DE": {"name": "Henkel AG & Co. KGaA", "founding_date": "1876-09-26"},
            "ZAL.DE": {"name": "Zalando SE", "founding_date": "2008-01-01"},
            "DHER.DE": {"name": "Delivery Hero SE", "founding_date": "2011-05-01"},
            "PUM.DE": {"name": "Puma SE", "founding_date": "1948-01-01"},
            "BEI.DE": {"name": "Beiersdorf AG", "founding_date": "1882-01-01"},
            "FME.DE": {"name": "Fresenius Medical Care AG & Co. KGaA", "founding_date": "1996-01-01"},
            "MTX.DE": {"name": "MTU Aero Engines AG", "founding_date": "1934-01-01"},
            "HEI.DE": {"name": "HeidelbergCement AG", "founding_date": "1873-01-01"},
            "LIN.DE": {"name": "Linde plc", "founding_date": "1879-01-01"},
            "QGEN.DE": {"name": "Qiagen N.V.", "founding_date": "1984-01-01"},
            "SHL.DE": {"name": "Siemens Healthineers AG", "founding_date": "2018-03-01"},
            "DB1.DE": {"name": "Deutsche Börse AG", "founding_date": "1992-01-01"}
        }
        
        # Şirket bilgilerini al
        info = company_info.get(symbol, {
            "name": f"{symbol.replace('.DE', '')} AG",
            "founding_date": "2000-01-01"  # Varsayılan tarih
        })
        
        return {
            "symbol": symbol,
            "name": info["name"],
            "founding_date": info["founding_date"],
            "market": "XETRA",
            "country": "Germany",
            "currency": "EUR"
        }

