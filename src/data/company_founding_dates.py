"""
PlanB Motoru - Şirket Kuruluş Tarihleri
TAM LİSTE: 487 BIST Firması
"""
import os
from src.utils.logger import log_info, log_error, log_debug, log_warning

class CompanyFoundingDates:
    """Şirket kuruluş tarihlerini yöneten sınıf"""
    
    def __init__(self):
        self.founding_dates = {}
        self._load_founding_dates()
    
    def _load_founding_dates(self):
        """Şirket kuruluş tarihlerini yükle"""
        try:
            # TAM LİSTEYİ DOSYADAN YÜKLE
            self.founding_dates = {}
            self._load_from_file()
            
            # Eğer dosya yüklenemezse fallback
            if not self.founding_dates:
                # BIST Şirket Kuruluş Tarihleri (Fallback)
                self.founding_dates = {
                    "ASELS": "1975-04-14",  # Aselsan Elektronik
                    "AKBNK": "1948-01-30",  # Akbank
                    "BIMAS": "1995-06-26",  # BİM Birleşik Mağazalar
                    "EREGL": "1960-06-01",  # Ereğli Demir Çelik
                    "GARAN": "1946-06-01",  # Garanti Bankası
                    "ISCTR": "1924-06-01",  # İş Bankası
                    "HALKB": "1938-06-01",  # Halk Bankası
                    "TUPRS": "1955-06-01",  # Tüpraş
                    "KRDMD": "1937-06-01",  # Kardemir
                    "SAHOL": "1967-06-01",  # Sabancı Holding
                    "THYAO": "1956-06-01",  # Türk Hava Yolları
                    "ARCLK": "1955-02-19",  # Arçelik
                    "KOZAL": "1995-06-01",  # Koza Altın
                    "PETKM": "1965-06-01",  # Petkim
                    "TCELL": "1994-06-01",  # Turkcell
                    "VAKBN": "1954-06-01",  # VakıfBank
                    "YKBNK": "1946-06-01",  # Yapı Kredi Bankası
                    "SASA": "1968-06-01",   # Sasa Polyester
                    "TOASO": "1968-06-01",  # Tofaş
                    "FROTO": "1959-06-01",  # Ford Otosan
                    "KCHOL": "1963-06-01",  # Koç Holding
                    "DOHOL": "1997-06-01",  # Doğan Holding
                    "ALARK": "1954-08-06",  # Alarko Holding
                    "ENKAI": "1957-06-01",  # Enka İnşaat
                    "AKSA": "1968-01-30",   # Aksa Akrilik
                    "CCOLA": "1964-04-01",  # Coca-Cola İçecek
                    "PGSUS": "1990-06-01",  # Pegasus
                    "BRSAN": "1958-04-01",  # Borusan
                    "BRISA": "1988-04-01",  # Brisa
                }
            
            # Sessiz yükleme - log_debug kullan
            # log_info(f"Company founding dates: {len(self.founding_dates)} şirket yüklendi")
            
        except Exception as e:
            log_error(f"Şirket kuruluş tarihleri yüklenirken hata: {e}")
            self.founding_dates = {}
    
    def _load_from_file(self):
        """TAM LİSTEYİ DOSYADAN YÜKLE"""
        try:
            file_path = "c:/Users/sardunya/Desktop/bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt"
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                lines = content.split('\n')
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    
                    # Tek satır format: SYMBOL.IS\tNAME\tDATE
                    if '\t' in line:
                        parts = line.split('\t')
                        if len(parts) >= 3 and parts[0] and parts[0].endswith('.IS'):
                            symbol = parts[0].replace('.IS', '')
                            name = parts[1]
                            date = parts[2]
                            
                            if symbol and name and date and date.strip():
                                # Tarih formatını düzelt
                                if '.' in date:
                                    day, month, year = date.split('.')
                                    fixed_date = f'{year}-{month.zfill(2)}-{day.zfill(2)}'
                                else:
                                    fixed_date = date
                                
                                self.founding_dates[symbol] = fixed_date
                    
                    # Multi-line format: SYMBOL.IS / NAME / DATE (3 ayrı satır)
                    elif line.endswith('.IS') and i + 2 < len(lines):
                        symbol = line.replace('.IS', '')
                        name = lines[i + 1].strip()
                        date = lines[i + 2].strip()
                        
                        if symbol and name and date and date.strip():
                            # Tarih formatını düzelt
                            if '.' in date:
                                day, month, year = date.split('.')
                                fixed_date = f'{year}-{month.zfill(2)}-{day.zfill(2)}'
                            else:
                                fixed_date = date
                            
                            self.founding_dates[symbol] = fixed_date
                        
                        i += 2  # 3 satırı birden atla
                    
                    i += 1
                
                # Sessiz yükleme - log_debug kullan  
                # log_info(f"TAM LİSTE yüklendi: {len(self.founding_dates)} firma")
            else:
                log_warning("TAM LİSTE dosyası bulunamadı")
                
        except Exception as e:
            log_error(f"TAM LİSTE yüklenirken hata: {e}")
    
    def get_founding_date(self, symbol: str) -> str:
        """Şirket kuruluş tarihini getir"""
        return self.founding_dates.get(symbol.upper(), "")
    
    def get_count(self) -> int:
        """Yüklenen şirket sayısını getir"""
        return len(self.founding_dates)
    
    def add_founding_date(self, symbol: str, date: str):
        """Yeni kuruluş tarihi ekle"""
        self.founding_dates[symbol.upper()] = date
        log_debug(f"Kuruluş tarihi eklendi: {symbol} - {date}")
    
    def remove_founding_date(self, symbol: str):
        """Kuruluş tarihini kaldır"""
        if symbol.upper() in self.founding_dates:
            del self.founding_dates[symbol.upper()]
            log_debug(f"Kuruluş tarihi kaldırıldı: {symbol}")
    
    def get_symbols_with_dates(self) -> list:
        """Kuruluş tarihi olan sembolleri getir"""
        return list(self.founding_dates.keys())
    
    def get_count(self) -> int:
        """Toplam şirket sayısını getir"""
        return len(self.founding_dates)
    
    def get_all_companies(self) -> dict:
        """Tüm şirketleri getir"""
        return self.founding_dates.copy()
    
    def search_company(self, search_term: str) -> dict:
        """Şirket ara"""
        results = {}
        search_term = search_term.upper()
        
        for symbol, date in self.founding_dates.items():
            if search_term in symbol.upper():
                results[symbol] = date
        
        return results
