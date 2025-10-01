"""
PlanB Motoru - BIST Veri Sağlayıcısı
BIST (Borsa İstanbul) veri sağlayıcısı
"""
import pandas as pd
import requests
from typing import List, Dict, Optional
from .base_provider import BaseProvider
from src.utils.logger import log_info, log_error, log_debug, log_warning

class BISTProvider(BaseProvider):
    """BIST (Borsa İstanbul) veri sağlayıcısı"""
    
    def __init__(self):
        super().__init__("BIST")
        self.symbols = []
        self._load_symbols()
    
    def _load_symbols(self):
        """BIST sembollerini yükle - Tüm aktif hisseler"""
        try:
            # BIST resmi sitesinden tüm sembolleri çek
            url = "https://www.borsaistanbul.com/en/sayfa/395/Listed-Companies"
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
                        if symbol_text and len(symbol_text) <= 10 and symbol_text.isalpha():
                            symbols.append(f"{symbol_text}.IS")
            
            if symbols:
                self.symbols = list(set(symbols))  # Duplikatları kaldır
                log_info(f"BIST: {len(self.symbols)} sembol yüklendi (resmi siteden)")
            else:
                raise ValueError("Sembol bulunamadı")
            
        except Exception as e:
            log_error(f"BIST sembolleri resmi siteden yüklenirken hata: {e}")
            try:
                # Alternatif: Investing.com'dan BIST hisselerini çek
                self._load_from_investing()
            except Exception as e2:
                log_error(f"Investing'den yükleme hatası: {e2}")
                # Son çare: Genişletilmiş fallback liste
                self._load_fallback_symbols()
    
    def _load_from_investing(self):
        """Investing.com'dan BIST hisselerini yükle"""
        try:
            url = "https://www.investing.com/equities/turkey"
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
                            symbols.append(f"{symbol_text}.IS")
            
            if symbols:
                self.symbols = list(set(symbols))
                log_info(f"BIST: {len(self.symbols)} sembol yüklendi (Investing'den)")
            else:
                raise ValueError("Investing'den sembol bulunamadı")
                
        except Exception as e:
            raise e
    
    def _load_fallback_symbols(self):
        """Genişletilmiş fallback sembol listesi"""
        self.symbols = [
            # BIST 30
            "ASELS.IS", "AKBNK.IS", "BIMAS.IS", "EREGL.IS", "FROTO.IS",
            "GARAN.IS", "HALKB.IS", "ISCTR.IS", "KCHOL.IS", "KOZAL.IS",
            "PETKM.IS", "SAHOL.IS", "SASA.IS", "THYAO.IS", "TUPRS.IS",
            "VAKBN.IS", "YKBNK.IS", "ARCLK.IS", "BRSAN.IS", "CCOLA.IS",
            "DOHOL.IS", "EKGYO.IS", "ENKAI.IS", "FMIZP.IS", "GUBRF.IS",
            "HUNER.IS", "KRDMD.IS", "LOGO.IS", "MGROS.IS", "NETAS.IS",
            
            # BIST 50 ek hisseler
            "ADANA.IS", "ADNAC.IS", "AGHOL.IS", "AKCNS.IS", "AKGRT.IS",
            "AKSEN.IS", "ALARK.IS", "ALBRK.IS", "ALCTL.IS", "ALFAS.IS",
            "ALGYO.IS", "ALKIM.IS", "ALTIN.IS", "ANACM.IS", "ANSGR.IS",
            "ARENA.IS", "ASTOR.IS", "ATAGY.IS", "ATLAS.IS", "AVOD.IS",
            "AYCES.IS", "AYDEM.IS", "AYEN.IS", "AYGAZ.IS", "BAGFS.IS",
            "BAKAB.IS", "BALAT.IS", "BANVT.IS", "BARMA.IS", "BASGZ.IS",
            "BFREN.IS", "BIOEN.IS", "BIZIM.IS", "BLCYT.IS", "BMSCH.IS",
            "BNTAS.IS", "BOBET.IS", "BOSSA.IS", "BRISA.IS", "BRKO.IS",
            "BRKVY.IS", "BRYAT.IS", "BUCIM.IS", "BURCE.IS", "BURCE.IS",
            
            # Ek hisseler
            "CANTE.IS", "CEMTS.IS", "CIMSA.IS", "DAGI.IS", "DEVA.IS",
            "DURDO.IS", "ECILC.IS", "EGEEN.IS", "EGEPO.IS", "EKIZ.IS",
            "EMKEL.IS", "ENJSI.IS", "ERBOS.IS", "ESCOM.IS", "FENER.IS",
            "FORTE.IS", "GENTS.IS", "GSDHO.IS", "GUBRF.IS", "HAVVA.IS",
            "HDFGS.IS", "HEKTS.IS", "HUNER.IS", "ISDMR.IS", "IZINV.IS",
            "IZMDC.IS", "KAREL.IS", "KARSN.IS", "KARTN.IS", "KATMR.IS",
            "KONTR.IS", "KORDS.IS", "KRDMD.IS", "KRONT.IS", "LOGO.IS",
            "MEGAP.IS", "MERIT.IS", "METUR.IS", "MGROS.IS", "MPARK.IS",
            "NETAS.IS", "NTHOL.IS", "ODAS.IS", "OTKAR.IS", "PAPIL.IS",
            "PARSN.IS", "PETUN.IS", "PINSU.IS", "PNSUT.IS", "POLHO.IS",
            "PRKAB.IS", "QUAGR.IS", "RAYSG.IS", "ROYAL.IS", "SANEL.IS",
            "SARKY.IS", "SEYKM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS",
            "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS",
            "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS",
            "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS",
            "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS",
            "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS",
            "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS",
            "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS",
            "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS",
            "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS", "SNPAM.IS"
        ]
        log_warning(f"BIST: Fallback sembol listesi kullanılıyor ({len(self.symbols)} sembol)")
    
    def get_symbols(self) -> List[str]:
        """BIST sembol listesini getir"""
        return self.symbols.copy()
    
    def get_market_info(self) -> Dict[str, any]:
        """BIST pazar bilgilerini getir"""
        return {
            'market_name': 'Borsa İstanbul',
            'country': 'Turkey',
            'currency': 'TRY',
            'timezone': 'Europe/Istanbul',
            'trading_hours': '09:30-18:00',
            'symbol_count': len(self.symbols)
        }
    
    def get_market_data(self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """BIST hisse verilerini getir"""
        try:
            # yfinance ile veri çek
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                log_warning(f"BIST {symbol} için veri bulunamadı")
                return None
            
            return data
            
        except Exception as e:
            log_error(f"BIST {symbol} veri çekme hatası: {e}")
            return None
