"""
PlanB Motoru - BIST Veri Sağlayıcısı (Güncellenmiş)
BIST (Borsa İstanbul) veri sağlayıcısı - BIST 300 kapsamlı liste
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
        """Genişletilmiş fallback sembol listesi - BIST 300"""
        self.symbols = [
            # BIST 30 - Büyük Şirketler
            "ASELS.IS", "AKBNK.IS", "BIMAS.IS", "EREGL.IS", "FROTO.IS", "GARAN.IS", "HALKB.IS", "ISCTR.IS", 
            "KCHOL.IS", "KOZAL.IS", "PETKM.IS", "SAHOL.IS", "SASA.IS", "THYAO.IS", "TUPRS.IS", "VAKBN.IS", 
            "YKBNK.IS", "ARCLK.IS", "BRSAN.IS", "CCOLA.IS", "DOHOL.IS", "EKGYO.IS", "ENKAI.IS", "FMIZP.IS", 
            "GUBRF.IS", "HUNER.IS", "KRDMD.IS", "LOGO.IS", "MGROS.IS", "NETAS.IS",
            
            # BIST 50 - Orta Büyüklükteki Şirketler
            "ADANA.IS", "ADNAC.IS", "AGHOL.IS", "AKCNS.IS", "AKGRT.IS", "AKSEN.IS", "ALARK.IS", "ALBRK.IS", 
            "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKIM.IS", "ALTIN.IS", "ANACM.IS", "ANSGR.IS", "ARENA.IS", 
            "ASTOR.IS", "ATAGY.IS", "ATLAS.IS", "AVOD.IS", "AYCES.IS", "AYDEM.IS", "AYEN.IS", "AYGAZ.IS", 
            "BAGFS.IS", "BAKAB.IS", "BALAT.IS", "BANVT.IS", "BARMA.IS", "BASGZ.IS", "BFREN.IS", "BIOEN.IS", 
            "BIZIM.IS", "BLCYT.IS", "BMSCH.IS", "BNTAS.IS", "BOBET.IS", "BOSSA.IS", "BRISA.IS", "BRKO.IS", 
            "BRKVY.IS", "BRYAT.IS", "BUCIM.IS", "BURCE.IS", "CANTE.IS", "CEMTS.IS", "CIMSA.IS", "DAGI.IS", 
            "DEVA.IS", "DURDO.IS", "ECILC.IS", "EGEEN.IS", "EGEPO.IS", "EKIZ.IS", "EMKEL.IS", "ENJSI.IS", 
            "ERBOS.IS", "ESCOM.IS", "FENER.IS", "FORTE.IS", "GENTS.IS", "GSDHO.IS", "HAVVA.IS", "HDFGS.IS", 
            "HEKTS.IS", "ISDMR.IS", "IZINV.IS", "IZMDC.IS", "KAREL.IS", "KARSN.IS", "KARTN.IS", "KATMR.IS", 
            "KONTR.IS", "KORDS.IS", "KRONT.IS", "MEGAP.IS", "MERIT.IS", "METUR.IS", "MPARK.IS", "NTHOL.IS", 
            "ODAS.IS", "OTKAR.IS", "PAPIL.IS", "PARSN.IS", "PETUN.IS", "PINSU.IS", "PNSUT.IS", "POLHO.IS", 
            "PRKAB.IS", "QUAGR.IS", "RAYSG.IS", "ROYAL.IS", "SANEL.IS", "SARKY.IS", "SEYKM.IS", "SNPAM.IS",
            
            # BIST 100 - Genişletilmiş Liste
            "AEFES.IS", "AHGAZ.IS", "AKFGY.IS", "AKSA.IS", "ALCIM.IS", "ALKT.IS", "ALMAD.IS", "AZGBR.IS", 
            "BARIŞ.IS", "BERA.IS", "BIENY.IS", "BIGCH.IS", "BLBGY.IS", "BLSYM.IS", "BSOBE.IS", "BTCIM.IS", 
            "BUHOLD.IS", "BVGZO.IS", "CDIGO.IS", "CEDMO.IS", "CFRAM.IS", "DOAS.IS", "ECZYT.IS", "ENERY.IS", 
            "ENSER.IS", "ERENK.IS", "ERGOV.IS", "ERUYG.IS", "ESTIM.IS", "EUHOLD.IS", "EUREN.IS", "EYDES.IS", 
            "EYILM.IS", "FADEF.IS", "FGENP.IS", "FRONT.IS", "GESAN.IS", "GUVEN.IS", "HUMBT.IS", "HYDRO.IS", 
            "ICBGM.IS", "ICFAS.IS", "ICHLF.IS", "IEYHO.IS", "ISMEN.IS", "IZENR.IS", "IZFAS.IS", "KCAHE.IS", 
            "KENT.IS", "KERVT.IS", "KLNKA.IS", "NUHCMR.IS", "OYAKCN.IS", "OZGYO.IS", "OZKAR.IS", "OZKCM.IS", 
            "OZKSP.IS", "PENTA.IS", "PETGM.IS", "PGSUS.IS", "PKBHN.IS", "PLAZA.IS", "POLEN.IS", "POLTK.IS", 
            "PRTS.IS", "PSDUD.IS", "RENBIL.IS", "RENTS.IS", "RHBYO.IS", "RNPOL.IS", "RODRG.IS", "SAYIL.IS", 
            "SDTBT.IS", "SEGAY.IS", "SEKURY.IS", "SELEC.IS", "SERBL.IS", "SETUR.IS", "SISE.IS", "SKBNK.IS", 
            "SMRTG.IS", "SOKE.IS", "STCRP.IS", "STRATE.IS", "SUNER.IS", "SUNGUR.IS", "SURAL.IS", "SUSYO.IS", 
            "SVCHE.IS", "TABGD.IS", "TALEN.IS", "TAVHL.IS", "TCELL.IS", "TEKTAS.IS", "TEPEGM.IS", "TERA.IS", 
            "TESBM.IS", "TGRT.IS", "TOASO.IS", "TOGG.IS", "TOKI.IS", "TORKU.IS", "TPKS.IS", "TRGYO.IS", 
            "TRILC.IS", "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TURIZ.IS", "TURSG.IS", "TUSAŞ.IS", "TUVSD.IS", 
            "TWFEV.IS", "TYFIL.IS", "ULKAL.IS", "ULUSE.IS", "UMNEV.IS", "UNEURO.IS", "UPCYN.IS", "VESTEL.IS", 
            "VKSA.IS", "VNSYM.IS", "YATRM.IS", "YAYLA.IS", "YBKTM.IS", "YATRK.IS", "YTLGM.IS", "ZRGYO.IS", 
            "ZORLU.IS", "ZOREN.IS", "AYNAP.IS", "AYPAS.IS", "BIGCH.IS", "BIENY.IS", "BLBGY.IS", "BLSYM.IS", 
            "BSOBE.IS", "BTCIM.IS", "BUHOLD.IS", "BVGZO.IS", "CDIGO.IS", "CEDMO.IS", "CFRAM.IS", "DOAS.IS", 
            "ECZYT.IS", "ENERY.IS", "ENSER.IS", "ERENK.IS", "ERGOV.IS", "ERUYG.IS", "ESTIM.IS", "EUHOLD.IS", 
            "EUREN.IS", "EYDES.IS", "EYILM.IS", "FADEF.IS", "FGENP.IS", "FRONT.IS", "GESAN.IS", "GUVEN.IS", 
            "HUMBT.IS", "HYDRO.IS", "ICBGM.IS", "ICFAS.IS", "ICHLF.IS", "IEYHO.IS", "ISMEN.IS", "IZENR.IS", 
            "IZFAS.IS", "KCAHE.IS", "KENT.IS", "KERVT.IS", "KLNKA.IS", "NUHCMR.IS", "OYAKCN.IS", "OZGYO.IS", 
            "OZKAR.IS", "OZKCM.IS", "OZKSP.IS", "PENTA.IS", "PETGM.IS", "PGSUS.IS", "PKBHN.IS", "PLAZA.IS", 
            "POLEN.IS", "POLTK.IS", "PRTS.IS", "PSDUD.IS", "RENBIL.IS", "RENTS.IS", "RHBYO.IS", "RNPOL.IS", 
            "RODRG.IS", "SAYIL.IS", "SDTBT.IS", "SEGAY.IS", "SEKURY.IS", "SELEC.IS", "SERBL.IS", "SETUR.IS", 
            "SISE.IS", "SKBNK.IS", "SMRTG.IS", "SOKE.IS", "STCRP.IS", "STRATE.IS", "SUNER.IS", "SUNGUR.IS", 
            "SURAL.IS", "SUSYO.IS", "SVCHE.IS", "TABGD.IS", "TALEN.IS", "TAVHL.IS", "TCELL.IS", "TEKTAS.IS", 
            "TEPEGM.IS", "TERA.IS", "TESBM.IS", "TGRT.IS", "TOASO.IS", "TOGG.IS", "TOKI.IS", "TORKU.IS", 
            "TPKS.IS", "TRGYO.IS", "TRILC.IS", "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TURIZ.IS", "TURSG.IS", 
            "TUSAŞ.IS", "TUVSD.IS", "TWFEV.IS", "TYFIL.IS", "ULKAL.IS", "ULUSE.IS", "UMNEV.IS", "UNEURO.IS", 
            "UPCYN.IS", "VESTEL.IS", "VKSA.IS", "VNSYM.IS", "YATRM.IS", "YAYLA.IS", "YBKTM.IS", "YATRK.IS", 
            "YTLGM.IS", "ZRGYO.IS", "ZORLU.IS", "ZOREN.IS"
        ]
        log_warning(f"BIST: Fallback sembol listesi kullanılıyor ({len(self.symbols)} sembol)")
    
    def get_symbols(self) -> List[str]:
        """BIST sembol listesini getir"""
        return self.symbols.copy()
    
    def get_market_info(self) -> Dict[str, any]:
        """BIST pazar bilgilerini getir"""
        return {
            "name": "Borsa İstanbul",
            "country": "Turkey",
            "currency": "TRY",
            "timezone": "Europe/Istanbul",
            "symbols_count": len(self.symbols),
            "market_type": "Stock Exchange"
        }
    
    def get_company_info(self, symbol: str) -> Optional[Dict[str, any]]:
        """Şirket bilgilerini getir"""
        if not symbol.endswith('.IS'):
            symbol = f"{symbol}.IS"
        
        if symbol not in self.symbols:
            return None
        
        # Basit şirket bilgileri
        company_names = {
            "ASELS.IS": "Aselsan Elektronik Sanayi ve Ticaret A.Ş.",
            "AKBNK.IS": "Akbank T.A.Ş.",
            "BIMAS.IS": "BİM Birleşik Mağazalar A.Ş.",
            "EREGL.IS": "Ereğli Demir ve Çelik Fabrikaları T.A.Ş.",
            "FROTO.IS": "Ford Otomotiv Sanayi A.Ş.",
            "GARAN.IS": "Garanti BBVA",
            "HALKB.IS": "Türkiye Halk Bankası A.Ş.",
            "ISCTR.IS": "Türkiye İş Bankası A.Ş.",
            "KCHOL.IS": "Koç Holding A.Ş.",
            "KOZAL.IS": "Koza Altın İşletmeleri A.Ş.",
            "PETKM.IS": "Petkim Petrokimya Holding A.Ş.",
            "SAHOL.IS": "Hacı Ömer Sabancı Holding A.Ş.",
            "SASA.IS": "Sasa Polyester Sanayi A.Ş.",
            "THYAO.IS": "Türk Hava Yolları A.O.",
            "TUPRS.IS": "Tüpraş-Türkiye Petrol Rafinerileri A.Ş.",
            "VAKBN.IS": "Türkiye Vakıflar Bankası T.A.O.",
            "YKBNK.IS": "Yapı ve Kredi Bankası A.Ş."
        }
        
        return {
            "symbol": symbol,
            "name": company_names.get(symbol, f"{symbol.replace('.IS', '')} A.Ş."),
            "market": "BIST",
            "country": "Turkey",
            "currency": "TRY"
        }

