"""
PlanB Motoru - Döngü21 Analiz Modülü
21 Günlük Döngü Analizi
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from src.utils.logger import log_info, log_error, log_debug, log_warning

# Global analyzer instance
_cycle21_analyzer = None

def get_cycle21_score() -> float:
    """21 günlük döngü skorunu döndür"""
    global _cycle21_analyzer
    try:
        if _cycle21_analyzer is None:
            _cycle21_analyzer = Cycle21Analyzer()
        return _cycle21_analyzer.calculate_cycle_score("DEFAULT")
    except Exception as e:
        log_error(f"Cycle21 skoru hesaplanırken hata: {e}")
        return 50.0  # Varsayılan nötr skor

class Cycle21Analyzer:
    """21 günlük döngü analiz işlemlerini yöneten sınıf"""
    
    def __init__(self):
        self.cycle_length = 21  # 21 günlük döngü
        self.lookback_periods = 3  # 3 döngü geriye bak
    
    def calculate_cycle_position(self, target_date: datetime = None) -> int:
        """Verilen tarihin 21 günlük döngüdeki pozisyonunu hesapla"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            # 2000 yılından itibaren gün sayısını hesapla
            epoch_date = datetime(2000, 1, 1)
            days_since_epoch = (target_date - epoch_date).days
            
            # 21 günlük döngüdeki pozisyon (1-21 arası)
            cycle_position = (days_since_epoch % self.cycle_length) + 1
            
            return cycle_position
            
        except Exception as e:
            log_error(f"Döngü pozisyonu hesaplanırken hata: {e}")
            return 1
    
    def get_cycle_phase(self, target_date: datetime = None) -> str:
        """Döngü fazını belirle"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            cycle_position = self.calculate_cycle_position(target_date)
            
            if cycle_position <= 5:
                return "Başlangıç"
            elif cycle_position <= 10:
                return "Büyüme"
            elif cycle_position <= 15:
                return "Olgunluk"
            elif cycle_position <= 18:
                return "Doruğa Çıkış"
            else:
                return "Düşüş"
                
        except Exception as e:
            log_error(f"Döngü fazı belirlenirken hata: {e}")
            return "Bilinmiyor"
    
    def calculate_cycle_score(self, symbol: str, target_date: datetime = None) -> float:
        """Döngü pozisyonuna göre skor hesapla"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            cycle_position = self.calculate_cycle_position(target_date)
            cycle_phase = self.get_cycle_phase(target_date)
            
            # Döngü pozisyonuna göre skor hesapla
            if cycle_position <= 3:  # Başlangıç
                score = 70  # Yeni başlangıçlar için iyi skor
            elif cycle_position <= 7:  # Büyüme
                score = 85  # En yüksek büyüme potansiyeli
            elif cycle_position <= 12:  # Olgunluk
                score = 75  # İyi performans
            elif cycle_position <= 16:  # Doruğa çıkış
                score = 60  # Dikkatli olun
            elif cycle_position <= 19:  # Düşüş başlangıcı
                score = 40  # Düşük performans
            else:  # Son günler
                score = 25  # En düşük skor
            
            log_debug(f"{symbol}: Döngü pozisyonu {cycle_position} ({cycle_phase}), Skor: {score}")
            return float(score)
            
        except Exception as e:
            log_error(f"{symbol} döngü skoru hesaplanırken hata: {e}")
            return 50.0
    
    def analyze_historical_cycles(self, price_data: pd.DataFrame) -> Dict[str, any]:
        """Geçmiş döngü performansını analiz et"""
        try:
            if price_data.empty or len(price_data) < 63:  # En az 3 döngü
                log_warning("Döngü analizi için yetersiz veri")
                return {}
            
            # Son 3 döngüyü analiz et
            recent_data = price_data.tail(63)  # 3 * 21 = 63 gün
            
            cycle_performance = []
            
            for cycle_num in range(3):
                start_idx = cycle_num * 21
                end_idx = start_idx + 21
                cycle_data = recent_data.iloc[start_idx:end_idx]
                
                if len(cycle_data) < 21:
                    continue
                
                # Döngü performansını hesapla
                start_price = cycle_data['Close'].iloc[0]
                end_price = cycle_data['Close'].iloc[-1]
                cycle_return = ((end_price - start_price) / start_price) * 100
                
                # Volatilite hesapla
                cycle_volatility = cycle_data['Close'].std() / cycle_data['Close'].mean() * 100
                
                cycle_performance.append({
                    'cycle_number': cycle_num + 1,
                    'return': cycle_return,
                    'volatility': cycle_volatility,
                    'start_price': start_price,
                    'end_price': end_price
                })
            
            if not cycle_performance:
                return {}
            
            # Ortalama performans
            avg_return = np.mean([c['return'] for c in cycle_performance])
            avg_volatility = np.mean([c['volatility'] for c in cycle_performance])
            
            return {
                'cycle_performance': cycle_performance,
                'average_return': avg_return,
                'average_volatility': avg_volatility,
                'cycles_analyzed': len(cycle_performance)
            }
            
        except Exception as e:
            log_error(f"Geçmiş döngü analizi yapılırken hata: {e}")
            return {}
    
    def predict_cycle_performance(self, symbol: str, target_date: datetime = None) -> Dict[str, any]:
        """Mevcut döngü için performans tahmini"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            cycle_position = self.calculate_cycle_position(target_date)
            cycle_phase = self.get_cycle_phase(target_date)
            cycle_score = self.calculate_cycle_score(symbol, target_date)
            
            # Döngü pozisyonuna göre tahmin
            if cycle_position <= 5:
                prediction = "Pozitif başlangıç bekleniyor"
                confidence = 70
            elif cycle_position <= 10:
                prediction = "Güçlü büyüme bekleniyor"
                confidence = 85
            elif cycle_position <= 15:
                prediction = "Kararlı performans bekleniyor"
                confidence = 75
            elif cycle_position <= 18:
                prediction = "Dikkatli olun, düşüş riski"
                confidence = 60
            else:
                prediction = "Düşüş eğilimi bekleniyor"
                confidence = 80
            
            # Döngüde kalan gün sayısı
            days_remaining = self.cycle_length - cycle_position + 1
            
            return {
                'cycle_position': cycle_position,
                'cycle_phase': cycle_phase,
                'cycle_score': cycle_score,
                'prediction': prediction,
                'confidence': confidence,
                'days_remaining': days_remaining,
                'cycle_progress': (cycle_position / self.cycle_length) * 100
            }
            
        except Exception as e:
            log_error(f"{symbol} döngü tahmini yapılırken hata: {e}")
            return {
                'cycle_position': 1,
                'cycle_phase': 'Bilinmiyor',
                'cycle_score': 50.0,
                'prediction': 'Tahmin yapılamadı',
                'confidence': 0,
                'days_remaining': 21,
                'cycle_progress': 0
            }
    
    def get_cycle_insights(self, symbol: str, price_data: pd.DataFrame = None, target_date: datetime = None) -> Dict[str, any]:
        """Döngü21 analizi içgörüleri"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            cycle_position = self.calculate_cycle_position(target_date)
            cycle_phase = self.get_cycle_phase(target_date)
            cycle_score = self.calculate_cycle_score(symbol, target_date)
            prediction = self.predict_cycle_performance(symbol, target_date)
            
            insights = {
                'analysis_date': target_date.strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'cycle_position': cycle_position,
                'cycle_phase': cycle_phase,
                'cycle_score': cycle_score,
                'prediction': prediction,
                'cycle_length': self.cycle_length
            }
            
            # Geçmiş döngü analizi varsa ekle
            if price_data is not None and not price_data.empty:
                historical_analysis = self.analyze_historical_cycles(price_data)
                insights['historical_analysis'] = historical_analysis
            
            return insights
            
        except Exception as e:
            log_error(f"{symbol} döngü içgörüleri oluşturulurken hata: {e}")
            return {
                'analysis_date': target_date.strftime('%Y-%m-%d %H:%M:%S') if target_date else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'cycle_score': 50.0,
                'error': str(e)
            }
    
    def get_cycle_timing_recommendation(self, symbol: str, target_date: datetime = None) -> str:
        """Döngü zamanlaması önerisi"""
        try:
            if target_date is None:
                target_date = datetime.now()
            
            cycle_position = self.calculate_cycle_position(target_date)
            cycle_score = self.calculate_cycle_score(symbol, target_date)
            
            if cycle_position <= 5 and cycle_score >= 70:
                return "AL"  # Başlangıç dönemi, güçlü sinyal
            elif cycle_position <= 10 and cycle_score >= 80:
                return "AL"  # Büyüme dönemi, çok güçlü sinyal
            elif cycle_position <= 15 and cycle_score >= 60:
                return "TUT"  # Olgunluk dönemi, bekle
            elif cycle_position <= 18 and cycle_score < 50:
                return "SAT"  # Doruğa çıkış, satış sinyali
            elif cycle_position > 18:
                return "SAT"  # Düşüş dönemi, güçlü satış sinyali
            else:
                return "TUT"  # Belirsiz durum
                
        except Exception as e:
            log_error(f"{symbol} döngü zamanlama önerisi belirlenirken hata: {e}")
            return "TUT"



