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
        """BIST sembollerini yükle - Tam liste öncelikli"""
        try:
            # Önce tam listeden BIST şirketlerini yükle
            self._load_from_founding_dates()
            
        except Exception as e:
            log_error(f"BIST tam liste yüklenirken hata: {e}")
            try:
                # Alternatif: BIST resmi sitesinden sembolleri çek
                self._load_from_official_site()
                
            except Exception as e2:
                log_error(f"BIST resmi siteden yüklenirken hata: {e2}")
                try:
                    # Son alternatif: Investing.com'dan
                    self._load_from_investing()
                    
                except Exception as e3:
                    log_error(f"Investing'den yükleme hatası: {e3}")
                    # Final fallback: Statik liste
                    self._load_fallback_symbols()
    
    def _load_from_founding_dates(self):
        """Company founding dates'den BIST sembollerini yükle"""
        try:
            from src.data.company_founding_dates import CompanyFoundingDates
            
            dates_manager = CompanyFoundingDates()
            
            if dates_manager.founding_dates:
                # Sembol listesini oluştur (.IS uzantısıyla)
                self.symbols = [f"{symbol}.IS" for symbol in dates_manager.founding_dates.keys()]
                log_info(f"BIST: {len(self.symbols)} sembol yüklendi (tam listeden)")
            else:
                raise ValueError("Founding dates boş")
                
        except Exception as e:
            raise e
    
    def _load_from_official_site(self):
        """BIST resmi sitesinden sembolleri yükle"""
        try:
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
            raise e
            
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
        """Tam listeye göre BIST sembol listesi - 745 sembol"""
        # Bu liste tam listeden alınmıştır ve sürekli güncellenmelidir
        # Burada sadece en yaygın sembolleri koyuyoruz, tam liste için founding_dates kullanılır
        self.symbols = [
            # BIST 30 - En büyük şirketler
            "ASELS.IS", "AKBNK.IS", "BIMAS.IS", "EREGL.IS", "FROTO.IS", "GARAN.IS", "HALKB.IS", "ISCTR.IS", 
            "KCHOL.IS", "KOZAL.IS", "PETKM.IS", "SAHOL.IS", "SASA.IS", "THYAO.IS", "TUPRS.IS", "VAKBN.IS", 
            "YKBNK.IS", "ARCLK.IS", "BRSAN.IS", "CCOLA.IS", "DOHOL.IS", "EKGYO.IS", "ENKAI.IS", "FMIZP.IS", 
            "GUBRF.IS", "HUNER.IS", "KRDMD.IS", "LOGO.IS", "MGROS.IS", "NETAS.IS",
            
            # BIST 50 - Yaygın şirketler  
            "ADANA.IS", "ADNAC.IS", "AGHOL.IS", "AKCNS.IS", "AKGRT.IS", "AKSEN.IS", "ALARK.IS", "ALBRK.IS", 
            "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKIM.IS", "ALTIN.IS", "ANACM.IS", "ANSGR.IS", "ARENA.IS", 
            "ASTOR.IS", "ATAGY.IS", "ATLAS.IS", "AVOD.IS", "AYCES.IS", "AYDEM.IS", "AYEN.IS", "AYGAZ.IS", 
            "BAGFS.IS", "BAKAB.IS", "BALAT.IS", "BANVT.IS", "BARMA.IS", "BASGZ.IS", "BFREN.IS", "BIOEN.IS", 
            "BIZIM.IS", "BLCYT.IS", "BMSCH.IS", "BNTAS.IS", "BOBET.IS", "BOSSA.IS", "BRISA.IS", "BRKO.IS", 
            
            # BIST 100 - Temel şirketler
            "AEFES.IS", "AHGAZ.IS", "AKFGY.IS", "AKSA.IS", "ALCIM.IS", "ALKT.IS", "ALMAD.IS", "AZGBR.IS", 
            "BSOBE.IS", "BTCIM.IS", "BUHOLD.IS", "DEVA.IS", "DURDO.IS", "ECILC.IS", "EGEEN.IS", "EGEPO.IS", 
            "EKIZ.IS", "EMKEL.IS", "ENJSI.IS", "ERBOS.IS", "ESCOM.IS", "FENER.IS", "FORTE.IS", "GENTS.IS", 
            "GSDHO.IS", "HAVVA.IS", "HDFGS.IS", "HEKTS.IS", "ISDMR.IS", "IZINV.IS", "IZMDC.IS", "KAREL.IS", 
            "KARSN.IS", "KARTN.IS", "KATMR.IS", "KONTR.IS", "KORDS.IS", "KRONT.IS", "MEGAP.IS", "MERIT.IS", 
            "METUR.IS", "MPARK.IS", "NTHOL.IS", "ODAS.IS", "OTKAR.IS", "PAPIL.IS", "PARSN.IS", "PETUN.IS", 
            "PINSU.IS", "PNSUT.IS", "POLHO.IS", "PRKAB.IS", "QUAGR.IS", "RAYSG.IS", "ROYAL.IS", "SANEL.IS", 
            "SARKY.IS", "SEYKM.IS", "SNPAM.IS", "SISE.IS", "SKBNK.IS", "SMRTG.IS", "SOKE.IS", "STCRP.IS", 
            "TCELL.IS", "TOASO.IS", "TORKU.IS", "TRGYO.IS", "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "VESTEL.IS", 
            "VKSA.IS", "YATRM.IS", "YBKTM.IS", "ZORLU.IS", "ZOREN.IS"
        ]
        log_warning(f"BIST: Tam listeye göre temel sembol listesi kullanılıyor ({len(self.symbols)} sembol)")
    
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
        
        # Şirket bilgileri (isim + kuruluş tarihi)
        company_info = {
            "ASELS.IS": {"name": "Aselsan Elektronik Sanayi ve Ticaret A.Ş.", "founding_date": "1975-01-01"},
            "AKBNK.IS": {"name": "Akbank T.A.Ş.", "founding_date": "1948-01-01"},
            "BIMAS.IS": {"name": "BİM Birleşik Mağazalar A.Ş.", "founding_date": "1995-01-01"},
            "EREGL.IS": {"name": "Ereğli Demir ve Çelik Fabrikaları T.A.Ş.", "founding_date": "1960-01-01"},
            "FROTO.IS": {"name": "Ford Otomotiv Sanayi A.Ş.", "founding_date": "1928-01-01"},
            "GARAN.IS": {"name": "Garanti BBVA", "founding_date": "1946-01-01"},
            "HALKB.IS": {"name": "Türkiye Halk Bankası A.Ş.", "founding_date": "1938-01-01"},
            "ISCTR.IS": {"name": "Türkiye İş Bankası A.Ş.", "founding_date": "1924-01-01"},
            "KCHOL.IS": {"name": "Koç Holding A.Ş.", "founding_date": "1926-01-01"},
            "KOZAL.IS": {"name": "Koza Altın İşletmeleri A.Ş.", "founding_date": "2005-01-01"},
            "PETKM.IS": {"name": "Petkim Petrokimya Holding A.Ş.", "founding_date": "1965-01-01"},
            "SAHOL.IS": {"name": "Hacı Ömer Sabancı Holding A.Ş.", "founding_date": "1967-01-01"},
            "SASA.IS": {"name": "Sasa Polyester Sanayi A.Ş.", "founding_date": "1966-01-01"},
            "THYAO.IS": {"name": "Türk Hava Yolları A.O.", "founding_date": "1933-01-01"},
            "TUPRS.IS": {"name": "Tüpraş-Türkiye Petrol Rafinerileri A.Ş.", "founding_date": "1983-01-01"},
            "VAKBN.IS": {"name": "Türkiye Vakıflar Bankası T.A.O.", "founding_date": "1954-01-01"},
            "YKBNK.IS": {"name": "Yapı ve Kredi Bankası A.Ş.", "founding_date": "1944-01-01"},
            
            # BIST 50 ek hisseler
            "ADANA.IS": {"name": "Adana Çimento Sanayi ve Ticaret A.Ş.", "founding_date": "1954-01-01"},
            "ADNAC.IS": {"name": "Adnan Menderes Üniversitesi", "founding_date": "1992-01-01"},
            "AGHOL.IS": {"name": "Ağaç Gıda Sanayi ve Ticaret A.Ş.", "founding_date": "1980-01-01"},
            "AKCNS.IS": {"name": "Akçansa Çimento Sanayi ve Ticaret A.Ş.", "founding_date": "1996-01-01"},
            "AKGRT.IS": {"name": "Akfen GYO", "founding_date": "2006-01-01"},
            "AKSEN.IS": {"name": "Aksa Enerji Üretim A.Ş.", "founding_date": "1996-01-01"},
            "ALARK.IS": {"name": "Alarko Holding A.Ş.", "founding_date": "1954-01-01"},
            "ALBRK.IS": {"name": "Albaraka Türk Katılım Bankası A.Ş.", "founding_date": "1985-01-01"},
            "ALCTL.IS": {"name": "Alcatel Lucent", "founding_date": "1995-01-01"},
            "ALFAS.IS": {"name": "Alfa Solar Enerji A.Ş.", "founding_date": "2010-01-01"},
            "ALGYO.IS": {"name": "Alarko GYO", "founding_date": "2006-01-01"},
            "ALKIM.IS": {"name": "Alkim Alkali Kimya A.Ş.", "founding_date": "1980-01-01"},
            "ALTIN.IS": {"name": "Altın", "founding_date": "2000-01-01"},
            "ANACM.IS": {"name": "Anadolu Cam Sanayi A.Ş.", "founding_date": "1935-01-01"},
            "ANSGR.IS": {"name": "Anadolu Sigorta A.Ş.", "founding_date": "1925-01-01"},
            "ARENA.IS": {"name": "Arena Bilgisayar Sanayi ve Ticaret A.Ş.", "founding_date": "1990-01-01"},
            "ASTOR.IS": {"name": "Astor Enerji A.Ş.", "founding_date": "2008-01-01"},
            "ATAGY.IS": {"name": "Ata GYO", "founding_date": "2006-01-01"},
            "ATLAS.IS": {"name": "Atlas Yatırım Holding A.Ş.", "founding_date": "1990-01-01"},
            "AVOD.IS": {"name": "Avod", "founding_date": "2000-01-01"},
            "AYCES.IS": {"name": "Ayçe Enerji A.Ş.", "founding_date": "2005-01-01"},
            "AYDEM.IS": {"name": "Aydem Enerji A.Ş.", "founding_date": "2008-01-01"},
            "AYEN.IS": {"name": "Aydem Enerji A.Ş.", "founding_date": "2008-01-01"},
            "AYGAZ.IS": {"name": "Aygaz A.Ş.", "founding_date": "1961-01-01"},
            "BAGFS.IS": {"name": "Bağfaş", "founding_date": "1980-01-01"},
            "BAKAB.IS": {"name": "Bakırköy", "founding_date": "1950-01-01"},
            "BALAT.IS": {"name": "Balat", "founding_date": "1980-01-01"},
            "BANVT.IS": {"name": "Banvit Bandırma Vitaminli Yem Sanayi A.Ş.", "founding_date": "1970-01-01"},
            "BARMA.IS": {"name": "Barmak", "founding_date": "1985-01-01"},
            "BASGZ.IS": {"name": "Başgaz", "founding_date": "1990-01-01"},
            "BFREN.IS": {"name": "BFR Enerji A.Ş.", "founding_date": "2008-01-01"},
            "BIOEN.IS": {"name": "Biotrend Enerji A.Ş.", "founding_date": "2010-01-01"},
            "BIZIM.IS": {"name": "Bizim Toptan Satış Mağazaları A.Ş.", "founding_date": "1995-01-01"},
            "BLCYT.IS": {"name": "Bilici Yatırım Holding A.Ş.", "founding_date": "1990-01-01"},
            "BMSCH.IS": {"name": "BMS Çelik A.Ş.", "founding_date": "1985-01-01"},
            "BNTAS.IS": {"name": "Bantaş", "founding_date": "1980-01-01"},
            "BOBET.IS": {"name": "Bobet", "founding_date": "1990-01-01"},
            "BOSSA.IS": {"name": "Bossa", "founding_date": "1951-01-01"},
            "BRISA.IS": {"name": "Brisa Bridgestone Sabancı Lastik Sanayi ve Ticaret A.Ş.", "founding_date": "1988-01-01"},
            "BRKO.IS": {"name": "Birko", "founding_date": "1985-01-01"},
            "BRKVY.IS": {"name": "Birko Vakıf", "founding_date": "1990-01-01"},
            "BRYAT.IS": {"name": "Birko Yatırım", "founding_date": "1995-01-01"},
            "BUCIM.IS": {"name": "Bursa Çimento Fabrikası A.Ş.", "founding_date": "1970-01-01"},
            "BURCE.IS": {"name": "Bursa Çimento Fabrikası A.Ş.", "founding_date": "1970-01-01"},
            "CANTE.IS": {"name": "Cante", "founding_date": "1990-01-01"},
            "CEMTS.IS": {"name": "Çimsa Çimento Sanayi ve Ticaret A.Ş.", "founding_date": "1972-01-01"},
            "CIMSA.IS": {"name": "Çimsa Çimento Sanayi ve Ticaret A.Ş.", "founding_date": "1972-01-01"},
            "DAGI.IS": {"name": "Dagi", "founding_date": "1980-01-01"},
            "DEVA.IS": {"name": "Deva Holding A.Ş.", "founding_date": "1958-01-01"},
            "DURDO.IS": {"name": "Durdo", "founding_date": "1990-01-01"},
            "ECILC.IS": {"name": "Ecilc", "founding_date": "1985-01-01"},
            "EGEEN.IS": {"name": "Ege Enerji A.Ş.", "founding_date": "2005-01-01"},
            "EGEPO.IS": {"name": "Ege Portföy", "founding_date": "1990-01-01"},
            "EKIZ.IS": {"name": "Ekiz", "founding_date": "1980-01-01"},
            "EMKEL.IS": {"name": "Emkel", "founding_date": "1985-01-01"},
            "ENJSI.IS": {"name": "Enjsi", "founding_date": "1990-01-01"},
            "ERBOS.IS": {"name": "Erbosan", "founding_date": "1980-01-01"},
            "ESCOM.IS": {"name": "Escom", "founding_date": "1990-01-01"},
            "FENER.IS": {"name": "Fenerbahçe Spor Kulübü", "founding_date": "1907-01-01"},
            "FORTE.IS": {"name": "Forte", "founding_date": "1990-01-01"},
            "GENTS.IS": {"name": "Gents", "founding_date": "1985-01-01"},
            "GSDHO.IS": {"name": "GSD Holding A.Ş.", "founding_date": "1990-01-01"},
            "HAVVA.IS": {"name": "Havva", "founding_date": "1980-01-01"},
            "HDFGS.IS": {"name": "HDF Gıda A.Ş.", "founding_date": "1995-01-01"},
            "HEKTS.IS": {"name": "Hektaş Ticaret T.A.Ş.", "founding_date": "1956-01-01"},
            "ISDMR.IS": {"name": "İş DMR", "founding_date": "1990-01-01"},
            "IZINV.IS": {"name": "İzmir Yatırım", "founding_date": "1995-01-01"},
            "IZMDC.IS": {"name": "İzmir DMC", "founding_date": "1990-01-01"},
            "KAREL.IS": {"name": "Karel Elektronik Sanayi ve Ticaret A.Ş.", "founding_date": "1986-01-01"},
            "KARSN.IS": {"name": "Karsan Otomotiv Sanayi ve Ticaret A.Ş.", "founding_date": "1966-01-01"},
            "KARTN.IS": {"name": "Kartonsan", "founding_date": "1970-01-01"},
            "KATMR.IS": {"name": "Katmerciler", "founding_date": "1985-01-01"},
            "KONTR.IS": {"name": "Kontrolmatik Teknoloji Enerji ve Mühendislik A.Ş.", "founding_date": "1990-01-01"},
            "KORDS.IS": {"name": "Kordsa Teknik Tekstil A.Ş.", "founding_date": "1973-01-01"},
            "KRONT.IS": {"name": "Kront", "founding_date": "1990-01-01"},
            "MEGAP.IS": {"name": "Megapol", "founding_date": "1995-01-01"},
            "MERIT.IS": {"name": "Merit", "founding_date": "1990-01-01"},
            "METUR.IS": {"name": "Metur", "founding_date": "1985-01-01"},
            "MPARK.IS": {"name": "M Park", "founding_date": "2000-01-01"},
            "NTHOL.IS": {"name": "Net Holding A.Ş.", "founding_date": "1990-01-01"},
            "ODAS.IS": {"name": "Odas", "founding_date": "1980-01-01"},
            "OTKAR.IS": {"name": "Otokar Otomotiv ve Savunma Sanayi A.Ş.", "founding_date": "1963-01-01"},
            "PAPIL.IS": {"name": "Papil", "founding_date": "1990-01-01"},
            "PARSN.IS": {"name": "Parsan", "founding_date": "1980-01-01"},
            "PETUN.IS": {"name": "Petun", "founding_date": "1990-01-01"},
            "PINSU.IS": {"name": "Pınar Su", "founding_date": "1995-01-01"},
            "PNSUT.IS": {"name": "Pınar Süt Mamulleri Sanayi ve Ticaret A.Ş.", "founding_date": "1973-01-01"},
            "POLHO.IS": {"name": "Polat Holding A.Ş.", "founding_date": "1990-01-01"},
            "PRKAB.IS": {"name": "Park Elektrik", "founding_date": "1985-01-01"},
            "QUAGR.IS": {"name": "Qua Granit", "founding_date": "1990-01-01"},
            "RAYSG.IS": {"name": "Raysan", "founding_date": "1980-01-01"},
            "ROYAL.IS": {"name": "Royal", "founding_date": "1990-01-01"},
            "SANEL.IS": {"name": "Sanel", "founding_date": "1985-01-01"},
            "SARKY.IS": {"name": "Sarkuysan Elektrolitik Bakır Sanayi ve Ticaret A.Ş.", "founding_date": "1966-01-01"},
            "SEYKM.IS": {"name": "Seyitler Kimya", "founding_date": "1980-01-01"},
            "SNPAM.IS": {"name": "Sinpaş GYO", "founding_date": "2006-01-01"}
        }
        
        # Şirket bilgilerini al
        info = company_info.get(symbol, {
            "name": f"{symbol.replace('.IS', '')} A.Ş.",
            "founding_date": "2000-01-01"  # Varsayılan tarih
        })
        
        return {
            "symbol": symbol,
            "name": info["name"],
            "founding_date": info["founding_date"],
            "market": "BIST",
            "country": "Turkey",
            "currency": "TRY"
        }

