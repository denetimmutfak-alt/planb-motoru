"""
PlanB Motoru - Ultra Shemitah Analiz Modülü
Enhanced Biblical Financial Cycles Analysis with Historical Correlation
"""
from datetime import datetime, date
from typing import Dict, Optional
from src.utils.logger import log_info, log_error, log_debug, log_warning

# Import ultra analyzer
try:
    from .ultra_shemitah import ultra_shemitah_analyzer, shemitah_analyzer
    log_info("Ultra Shemitah Analyzer imported successfully")
except ImportError as e:
    log_warning(f"Ultra Shemitah import failed, using basic analyzer: {e}")
    ultra_shemitah_analyzer = None
    shemitah_analyzer = None

# Global analyzer instance
_shemitah_analyzer = None

def get_shemitah_score() -> float:
    """Shemitah döngü skorunu döndür"""
    global _shemitah_analyzer
    try:
        if ultra_shemitah_analyzer is not None:
            return ultra_shemitah_analyzer.calculate_ultra_shemitah_score()['ultra_shemitah_score']
        
        if _shemitah_analyzer is None:
            _shemitah_analyzer = ShemitahAnalyzer()
        return _shemitah_analyzer.calculate_shemitah_score("DEFAULT")
    except Exception as e:
        log_error(f"Shemitah skoru hesaplanırken hata: {e}")
        return 50.0  # Varsayılan nötr skor

class ShemitahAnalyzer:
    """Shemitah (7 yıllık döngü) analiz işlemlerini yöneten sınıf"""
    
    def __init__(self):
        # Shemitah döngüsü başlangıç yılı (yaklaşık)
        self.shemitah_start_year = 2001  # Son büyük Shemitah yılı
        self.cycle_length = 7
    
    def get_shemitah_year(self, target_date: datetime = None) -> int:
        """Verilen tarihin Shemitah yılını hesapla"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            year = target_date.year
            
            # Shemitah döngüsünü hesapla
            years_since_start = year - self.shemitah_start_year
            shemitah_year = (years_since_start % self.cycle_length) + 1
            
            return shemitah_year
            
        except Exception as e:
            log_error(f"Shemitah yılı hesaplanırken hata: {e}")
            return 1
    
    def get_shemitah_phase(self, target_date: datetime = None) -> str:
        """Shemitah döngüsündeki fazı belirle"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            shemitah_year = self.get_shemitah_year(target_date)
            
            phase_mapping = {
                1: "Başlangıç",
                2: "Büyüme",
                3: "Olgunlaşma",
                4: "Doruğa Çıkış",
                5: "Kararsızlık",
                6: "Düşüş",
                7: "Shemitah (Dinlenme)"
            }
            
            return phase_mapping.get(shemitah_year, "Bilinmiyor")
            
        except Exception as e:
            log_error(f"Shemitah fazı belirlenirken hata: {e}")
            return "Bilinmiyor"
    
    def calculate_shemitah_score(self, symbol: str, target_date: datetime = None) -> float:
        """Shemitah döngüsüne göre skor hesapla"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            shemitah_year = self.get_shemitah_year(target_date)
            shemitah_phase = self.get_shemitah_phase(target_date)
            
            # Shemitah yılına göre skor hesapla
            if shemitah_year == 1:  # Başlangıç
                score = 85  # Yeni başlangıçlar için yüksek skor
            elif shemitah_year == 2:  # Büyüme
                score = 90  # En yüksek büyüme potansiyeli
            elif shemitah_year == 3:  # Olgunlaşma
                score = 75  # İyi performans
            elif shemitah_year == 4:  # Doruğa çıkış
                score = 80  # Yüksek performans
            elif shemitah_year == 5:  # Kararsızlık
                score = 45  # Dikkatli olun
            elif shemitah_year == 6:  # Düşüş
                score = 25  # Düşük performans
            elif shemitah_year == 7:  # Shemitah (Dinlenme)
                score = 15  # En düşük skor - dinlenme dönemi
            else:
                score = 50  # Varsayılan
            
            log_debug(f"{symbol}: Shemitah yılı {shemitah_year} ({shemitah_phase}), Skor: {score}")
            return float(score)
            
        except Exception as e:
            log_error(f"{symbol} Shemitah skoru hesaplanırken hata: {e}")
            return 50.0
    
    def get_shemitah_insights(self, symbol: str, target_date: datetime = None) -> Dict[str, any]:
        """Shemitah döngüsü içgörüleri"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            shemitah_year = self.get_shemitah_year(target_date)
            shemitah_phase = self.get_shemitah_phase(target_date)
            score = self.calculate_shemitah_score(symbol, target_date)
            
            # Faz açıklamaları
            phase_descriptions = {
                "Başlangıç": "Yeni döngünün başlangıcı. Yeni yatırımlar için uygun dönem.",
                "Büyüme": "En güçlü büyüme dönemi. Alım sinyalleri güçlü.",
                "Olgunlaşma": "Olgun performans dönemi. Kararlı büyüme beklenir.",
                "Doruğa Çıkış": "Döngünün zirve noktası. Dikkatli olun.",
                "Kararsızlık": "Belirsizlik dönemi. Pozisyonları gözden geçirin.",
                "Düşüş": "Düşüş eğilimi. Satış sinyalleri güçlü.",
                "Shemitah (Dinlenme)": "Dinlenme ve yeniden yapılanma dönemi. Yatırım yapmaktan kaçının."
            }
            
            # Sonraki Shemitah yılına kalan süre
            current_year = target_date.year
            next_shemitah_year = current_year + (7 - shemitah_year + 1)
            years_to_next_shemitah = next_shemitah_year - current_year
            
            insights = {
                'analysis_date': target_date.strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'shemitah_year': shemitah_year,
                'shemitah_phase': shemitah_phase,
                'phase_description': phase_descriptions.get(shemitah_phase, "Açıklama bulunamadı"),
                'score': score,
                'years_to_next_shemitah': years_to_next_shemitah,
                'next_shemitah_year': next_shemitah_year,
                'cycle_progress': (shemitah_year / 7) * 100
            }
            
            return insights
            
        except Exception as e:
            log_error(f"{symbol} Shemitah içgörüleri oluşturulurken hata: {e}")
            return {
                'analysis_date': target_date.strftime('%Y-%m-%d %H:%M:%S') if target_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'score': 50.0,
                'error': str(e)
            }
    
    def is_shemitah_year(self, target_date: datetime = None) -> bool:
        """Verilen tarih Shemitah yılı mı?"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            shemitah_year = self.get_shemitah_year(target_date)
            return shemitah_year == 7
            
        except Exception as e:
            log_error(f"Shemitah yılı kontrolü yapılırken hata: {e}")
            return False
    
    def get_shemitah_warning_level(self, symbol: str, target_date: datetime = None) -> str:
        """Shemitah uyarı seviyesi"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            shemitah_year = self.get_shemitah_year(target_date)
            score = self.calculate_shemitah_score(symbol, target_date)
            
            if shemitah_year == 7:  # Shemitah yılı
                return "YÜKSEK"  # En yüksek uyarı
            elif shemitah_year == 6:  # Düşüş yılı
                return "ORTA"    # Orta uyarı
            elif shemitah_year == 5:  # Kararsızlık yılı
                return "DÜŞÜK"   # Düşük uyarı
            elif score >= 80:
                return "YOK"     # Uyarı yok
            elif score >= 60:
                return "DÜŞÜK"   # Düşük uyarı
            elif score >= 40:
                return "ORTA"    # Orta uyarı
            else:
                return "YÜKSEK"  # Yüksek uyarı
                
        except Exception as e:
            log_error(f"{symbol} Shemitah uyarı seviyesi belirlenirken hata: {e}")
            return "BİLİNMİYOR"



