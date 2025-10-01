# -*- coding: utf-8 -*-
"""
PlanB Motoru - 21'li Spiral Döngü Analiz Modülü
Hüseyin Kantürk'ün 21'li spiral döngü modeline göre analiz
"""

import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from src.utils.logger import log_info, log_error, log_debug, log_warning

class Spiral21CycleAnalyzer:
    """21'li spiral döngü analiz işlemlerini yöneten sınıf"""
    
    def __init__(self):
        # 21'li spiral temel döngüleri
        self.spiral_cycles = {
            'micro': [21, 42, 63, 84],           # Mikro döngüler (gün)
            'short': [105, 126, 147, 168],       # Kısa döngüler (gün)
            'medium': [189, 210, 231, 252],      # Orta döngüler (gün)
            'long': [273, 294, 315, 336]         # Uzun döngüler (gün)
        }
        
        # Fibonacci spiral oranları
        self.fibonacci_ratios = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        
        # Spiral döngü ağırlıkları
        self.cycle_weights = {
            'micro': 0.4,    # En yüksek ağırlık
            'short': 0.3,
            'medium': 0.2,
            'long': 0.1
        }
        
        # Spiral dönüş noktaları
        self.turning_points = [21, 42, 63, 84, 105, 126, 147, 168, 189, 210, 231, 252, 273, 294, 315, 336]
        
        log_info("Spiral21 Cycle Analyzer başlatıldı")
    
    def calculate_spiral_position(self, start_date: datetime, current_date: datetime) -> Dict:
        """
        Spiral pozisyonunu hesapla
        
        Args:
            start_date: Başlangıç tarihi
            current_date: Mevcut tarih
            
        Returns:
            Spiral pozisyon bilgileri
        """
        try:
            # Tarih farkını hesapla
            days_diff = (current_date - start_date).days
            
            # Hangi spiral döngüsünde olduğumuzu bul
            current_cycle = None
            cycle_type = None
            position_in_cycle = 0
            
            for cycle_type_name, cycles in self.spiral_cycles.items():
                for cycle in cycles:
                    if days_diff <= cycle:
                        current_cycle = cycle
                        cycle_type = cycle_type_name
                        # Önceki döngüyü bul
                        prev_cycle = 0
                        for prev_cycle_type, prev_cycles in self.spiral_cycles.items():
                            for prev_c in prev_cycles:
                                if prev_c < cycle:
                                    prev_cycle = max(prev_cycle, prev_c)
                        position_in_cycle = days_diff - prev_cycle
                        break
                if current_cycle:
                    break
            
            # Spiral dönüş noktasına yakınlık
            nearest_turning_point = min(self.turning_points, key=lambda x: abs(x - days_diff))
            distance_to_turning = abs(days_diff - nearest_turning_point)
            
            # Spiral yoğunluğu (dönüş noktasına yakınlık)
            if distance_to_turning <= 3:
                intensity = 1.0
                phase = 'turning_point'
            elif distance_to_turning <= 7:
                intensity = 0.8
                phase = 'near_turning'
            elif distance_to_turning <= 14:
                intensity = 0.6
                phase = 'approaching_turning'
            else:
                intensity = 0.3
                phase = 'mid_cycle'
            
            result = {
                'days_from_start': days_diff,
                'current_cycle': current_cycle,
                'cycle_type': cycle_type,
                'position_in_cycle': position_in_cycle,
                'nearest_turning_point': nearest_turning_point,
                'distance_to_turning': distance_to_turning,
                'intensity': intensity,
                'phase': phase
            }
            
            log_debug(f"Spiral pozisyon: {days_diff} gün, Döngü: {cycle_type}, Yoğunluk: {intensity}")
            return result
            
        except Exception as e:
            log_error(f"Spiral pozisyon hesaplama hatası: {e}")
            return {
                'days_from_start': 0,
                'current_cycle': 21,
                'cycle_type': 'micro',
                'position_in_cycle': 0,
                'intensity': 0.1,
                'phase': 'unknown'
            }
    
    def calculate_spiral21_score(self, symbol: str, price_data: Dict = None, founding_date: str = None, date: datetime = None) -> Dict:
        """
        21'li spiral döngüsüne göre skor hesapla
        
        Args:
            symbol: Analiz edilecek sembol
            price_data: Fiyat verisi
            founding_date: Kuruluş tarihi (opsiyonel)
            date: Analiz tarihi
            
        Returns:
            Spiral skor ve analiz bilgileri
        """
        try:
            if date is None:
                date = datetime.utcnow()
            
            # Varsayılan fiyat verisi oluştur
            if price_data is None:
                price_data = {
                    date.strftime('%Y-%m-%d'): {'Close': 100.0, 'High': 105.0, 'Low': 95.0, 'Volume': 1000000}
                }
            
            # Başlangıç tarihini belirle
            start_date = self._determine_start_date(symbol, founding_date, price_data)
            
            # Spiral pozisyonunu hesapla
            spiral_position = self.calculate_spiral_position(start_date, date)
            
            # Fiyat spiral analizi
            price_spiral = self._analyze_price_spiral(price_data, spiral_position)
            
            # Spiral skorunu hesapla
            score = self._calculate_spiral_score_value(spiral_position, price_spiral)
            
            # Sonraki dönüş noktalarını hesapla
            next_turning_points = self._get_next_turning_points(start_date, date)
            
            result = {
                'spiral21_score': score,
                'spiral_position': spiral_position,
                'price_spiral': price_spiral,
                'next_turning_points': next_turning_points,
                'analysis_type': 'Spiral21 Cycle',
                'details': {
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'current_phase': spiral_position['phase'],
                    'intensity': spiral_position['intensity'],
                    'next_turning_days': next_turning_points[0]['days_ahead'] if next_turning_points else 0
                }
            }
            
            log_info(f"{symbol}: Spiral21 skoru: {score:.2f} ({spiral_position['phase']})")
            return result
            
        except Exception as e:
            log_error(f"{symbol} Spiral21 skor hesaplama hatası: {e}")
            return {
                'spiral21_score': 50.0,
                'spiral_position': {'phase': 'error'},
                'price_spiral': {},
                'next_turning_points': [],
                'analysis_type': 'Spiral21 Cycle',
                'details': {'error': str(e)}
            }
    
    def _determine_start_date(self, symbol: str, founding_date: str, price_data: Dict) -> datetime:
        """
        Spiral analizi için başlangıç tarihini belirle
        
        Args:
            symbol: Sembol
            founding_date: Kuruluş tarihi
            price_data: Fiyat verisi
            
        Returns:
            Başlangıç tarihi
        """
        try:
            # Önce kuruluş tarihini dene
            if founding_date:
                try:
                    return datetime.strptime(founding_date, '%Y-%m-%d')
                except:
                    pass
            
            # Fiyat verisinden en eski tarihi al
            if price_data:
                oldest_date = min(price_data.keys())
                return datetime.strptime(oldest_date, '%Y-%m-%d')
            
            # Varsayılan: 1 yıl önce
            return datetime.utcnow() - timedelta(days=365)
            
        except Exception as e:
            log_warning(f"Başlangıç tarihi belirleme hatası: {e}")
            return datetime.utcnow() - timedelta(days=365)
    
    def _analyze_price_spiral(self, price_data: Dict, spiral_position: Dict) -> Dict:
        """
        Fiyat spiral analizi yap
        
        Args:
            price_data: Fiyat verisi
            spiral_position: Spiral pozisyon bilgileri
            
        Returns:
            Fiyat spiral analizi
        """
        try:
            if not price_data or len(price_data) < 21:
                return {'spiral_pattern': 'insufficient_data'}
            
            # Son 21 günlük fiyat verilerini al
            sorted_dates = sorted(price_data.keys())
            recent_prices = [price_data[date]['Close'] for date in sorted_dates[-21:]]
            
            # Spiral pattern analizi
            price_changes = []
            for i in range(1, len(recent_prices)):
                change = (recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1] * 100
                price_changes.append(change)
            
            # Spiral momentum hesapla
            momentum = sum(price_changes[-7:]) / 7  # Son 7 günlük ortalama momentum
            
            # Spiral volatilite
            volatility = np.std(price_changes) if len(price_changes) > 1 else 0
            
            # Spiral pattern türü
            if abs(momentum) < 0.5 and volatility < 2:
                pattern = 'consolidation'
            elif momentum > 1:
                pattern = 'ascending_spiral'
            elif momentum < -1:
                pattern = 'descending_spiral'
            else:
                pattern = 'neutral_spiral'
            
            return {
                'spiral_pattern': pattern,
                'momentum': momentum,
                'volatility': volatility,
                'recent_prices': recent_prices[-5:],  # Son 5 gün
                'price_changes': price_changes[-5:]
            }
            
        except Exception as e:
            log_warning(f"Fiyat spiral analizi hatası: {e}")
            return {'spiral_pattern': 'error'}
    
    def _calculate_spiral_score_value(self, spiral_position: Dict, price_spiral: Dict) -> float:
        """
        Spiral skor değerini hesapla
        
        Args:
            spiral_position: Spiral pozisyon bilgileri
            price_spiral: Fiyat spiral analizi
            
        Returns:
            Spiral skoru (0-100)
        """
        try:
            base_score = 50.0
            
            # Spiral pozisyon etkisi
            intensity = spiral_position.get('intensity', 0.3)
            phase = spiral_position.get('phase', 'mid_cycle')
            
            if phase == 'turning_point':
                base_score += 20.0
            elif phase == 'near_turning':
                base_score += 15.0
            elif phase == 'approaching_turning':
                base_score += 10.0
            
            # Fiyat spiral pattern etkisi
            pattern = price_spiral.get('spiral_pattern', 'neutral_spiral')
            if pattern == 'ascending_spiral':
                base_score += 10.0
            elif pattern == 'descending_spiral':
                base_score -= 10.0
            elif pattern == 'consolidation':
                base_score += 5.0
            
            # Momentum etkisi
            momentum = price_spiral.get('momentum', 0)
            if abs(momentum) > 2:
                base_score += momentum * 2
            
            # Final skor
            final_score = base_score * intensity + base_score * (1 - intensity) * 0.5
            return max(0, min(100, final_score))
            
        except Exception as e:
            log_warning(f"Spiral skor hesaplama hatası: {e}")
            return 50.0
    
    def _get_next_turning_points(self, start_date: datetime, current_date: datetime) -> List[Dict]:
        """
        Sonraki dönüş noktalarını hesapla
        
        Args:
            start_date: Başlangıç tarihi
            current_date: Mevcut tarih
            
        Returns:
            Sonraki dönüş noktaları
        """
        try:
            days_from_start = (current_date - start_date).days
            next_points = []
            
            for turning_point in self.turning_points:
                if turning_point > days_from_start:
                    turning_date = start_date + timedelta(days=turning_point)
                    days_ahead = (turning_date - current_date).days
                    
                    # Döngü türünü belirle
                    cycle_type = 'micro'
                    for cycle_type_name, cycles in self.spiral_cycles.items():
                        if turning_point in cycles:
                            cycle_type = cycle_type_name
                            break
                    
                    next_points.append({
                        'date': turning_date.strftime('%Y-%m-%d'),
                        'days_ahead': days_ahead,
                        'cycle_days': turning_point,
                        'cycle_type': cycle_type,
                        'weight': self.cycle_weights.get(cycle_type, 0.1)
                    })
            
            # Gün sayısına göre sırala
            next_points.sort(key=lambda x: x['days_ahead'])
            
            return next_points[:5]  # En yakın 5 dönüş noktası
            
        except Exception as e:
            log_warning(f"Sonraki dönüş noktaları hesaplama hatası: {e}")
            return []
    
    def get_spiral_forecast(self, symbol: str, start_date: datetime, days_ahead: int = 90) -> List[Dict]:
        """
        21'li spiral döngüsüne göre gelecek tahmini
        
        Args:
            symbol: Analiz edilecek sembol
            start_date: Başlangıç tarihi
            days_ahead: Kaç gün ileriye bakılacak
            
        Returns:
            Gelecek tahminleri
        """
        try:
            current_date = datetime.utcnow()
            forecast = []
            
            for i in range(0, days_ahead, 7):  # Her hafta kontrol
                check_date = current_date + timedelta(days=i)
                spiral_position = self.calculate_spiral_position(start_date, check_date)
                
                if spiral_position['intensity'] > 0.6:  # Yüksek yoğunluk
                    forecast.append({
                        'date': check_date.strftime('%Y-%m-%d'),
                        'phase': spiral_position['phase'],
                        'intensity': spiral_position['intensity'],
                        'cycle_type': spiral_position['cycle_type'],
                        'days_from_start': spiral_position['days_from_start']
                    })
            
            log_info(f"{symbol}: {days_ahead} günlük Spiral21 tahmini oluşturuldu")
            return forecast
            
        except Exception as e:
            log_error(f"Spiral21 tahmin hatası: {e}")
            return []

# Global instance
spiral21_analyzer = Spiral21CycleAnalyzer()



