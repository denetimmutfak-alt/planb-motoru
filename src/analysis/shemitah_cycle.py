"""
Shemitah Cycle Analyzer
"""
from datetime import datetime, timedelta
from typing import Dict, Any
from src.utils.logger import log_info

class ShemitahCycleAnalyzer:
    """Shemitah döngü analizörü"""
    
    def __init__(self):
        self.shemitah_years = [2001, 2008, 2015, 2022, 2029]  # 7 yıllık döngü
        log_info("Shemitah Cycle Analyzer başlatıldı")
    
    def calculate_shemitah_score(self, symbol: str, current_date: datetime = None) -> Dict[str, Any]:
        """Shemitah skoru hesapla"""
        try:
            if current_date is None:
                current_date = datetime.now()
            
            current_year = current_date.year
            
            # En yakın Shemitah yılını bul
            closest_shemitah = min(self.shemitah_years, key=lambda x: abs(x - current_year))
            years_to_shemitah = closest_shemitah - current_year
            
            # Döngü pozisyonu (0-6 arası)
            cycle_position = (current_year - 2001) % 7
            
            # Skor hesaplama
            if years_to_shemitah == 0:  # Shemitah yılı
                score = 30.0  # Düşük skor (riskli)
                phase = "Shemitah Year"
                intensity = "High"
            elif years_to_shemitah == 1:  # Shemitah sonrası
                score = 70.0  # Yüksek skor (iyileşme)
                phase = "Post-Shemitah Recovery"
                intensity = "Medium"
            elif years_to_shemitah == 6:  # Shemitah öncesi
                score = 40.0  # Düşük skor (hazırlık)
                phase = "Pre-Shemitah Preparation"
                intensity = "Medium"
            else:  # Normal döngü
                score = 60.0  # Orta skor
                phase = "Normal Cycle"
                intensity = "Low"
            
            return {
                'score': score,
                'phase': phase,
                'intensity': intensity,
                'cycle_position': cycle_position,
                'years_to_shemitah': years_to_shemitah,
                'closest_shemitah': closest_shemitah
            }
            
        except Exception as e:
            return {
                'score': 50.0,
                'phase': 'Unknown',
                'intensity': 'Low',
                'error': str(e)
            }

# Global instance
shemitah_analyzer = ShemitahCycleAnalyzer()
