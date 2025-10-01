# -*- coding: utf-8 -*-
"""
PlanB Motoru - Gann Tekniği Analiz Modülü
W.D. Gann'ın zaman-mekan simetrisi prensiplerine göre analiz
"""

import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from src.utils.logger import log_info, log_error, log_debug, log_warning

class GannTechniqueAnalyzer:
    """Gann tekniği analiz işlemlerini yöneten sınıf"""
    
    def __init__(self):
        # Gann açıları (derece cinsinden)
        self.gann_angles = {
            '1x1': 45,      # 1:1 oranı (45 derece)
            '1x2': 26.57,   # 1:2 oranı
            '1x3': 18.43,   # 1:3 oranı
            '1x4': 14.04,   # 1:4 oranı
            '1x8': 7.13,    # 1:8 oranı
            '2x1': 63.43,   # 2:1 oranı
            '3x1': 71.57,   # 3:1 oranı
            '4x1': 75.96,   # 4:1 oranı
            '8x1': 82.87    # 8:1 oranı
        }
        
        # Gann zaman döngüleri (gün cinsinden)
        self.time_cycles = {
            'short': [45, 90, 144, 180],      # Kısa döngüler
            'medium': [360, 720, 1080],       # Orta döngüler
            'long': [1440, 2160, 2880]       # Uzun döngüler
        }
        
        # Gann kareleri için önemli sayılar
        self.gann_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 20, 24, 30, 36, 45, 60, 90, 144, 180, 360]
        
        log_info("Gann Technique Analyzer başlatıldı")
    
    def calculate_gann_square(self, price: float, date: datetime) -> Dict:
        """
        Gann karesi hesapla
        
        Args:
            price: Fiyat değeri
            date: Tarih
            
        Returns:
            Gann kare analizi
        """
        try:
            # Gann karesi köşegenini hesapla
            diagonal = math.sqrt(price)
            
            # Gann karesi sınırları
            square_root = int(diagonal)
            lower_bound = square_root ** 2
            upper_bound = (square_root + 1) ** 2
            
            # Kare içindeki pozisyon
            position_in_square = (price - lower_bound) / (upper_bound - lower_bound)
            
            # Gann açılarını hesapla
            angles = {}
            for ratio, angle in self.gann_angles.items():
                angles[ratio] = {
                    'angle': angle,
                    'price_level': lower_bound + (upper_bound - lower_bound) * (angle / 90)
                }
            
            result = {
                'square_root': square_root,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'position_in_square': position_in_square,
                'angles': angles,
                'diagonal': diagonal
            }
            
            log_debug(f"Gann karesi: {lower_bound}-{upper_bound}, Pozisyon: {position_in_square:.2f}")
            return result
            
        except Exception as e:
            log_error(f"Gann karesi hesaplama hatası: {e}")
            return {}
    
    def find_gann_time_cycles(self, start_date: datetime, current_date: datetime) -> Dict:
        """
        Gann zaman döngülerini bul
        
        Args:
            start_date: Başlangıç tarihi (genelde önemli dip/zirve)
            current_date: Mevcut tarih
            
        Returns:
            Gann zaman döngü analizi
        """
        try:
            # Tarih farkını hesapla
            time_diff = (current_date - start_date).days
            
            # Hangi döngülerde olduğumuzu kontrol et
            active_cycles = {}
            
            for cycle_type, cycles in self.time_cycles.items():
                active_cycles[cycle_type] = []
                for cycle in cycles:
                    if time_diff % cycle == 0 or abs(time_diff % cycle - cycle) < 5:
                        active_cycles[cycle_type].append({
                            'cycle_days': cycle,
                            'exact_match': time_diff % cycle == 0,
                            'days_remaining': cycle - (time_diff % cycle)
                        })
            
            # Sonraki önemli döngü tarihlerini hesapla
            next_cycles = []
            for cycle_type, cycles in self.time_cycles.items():
                for cycle in cycles:
                    next_cycle_date = start_date + timedelta(days=cycle)
                    if next_cycle_date > current_date:
                        next_cycles.append({
                            'date': next_cycle_date,
                            'cycle_days': cycle,
                            'type': cycle_type,
                            'days_ahead': (next_cycle_date - current_date).days
                        })
            
            # En yakın döngüyü bul
            next_cycles.sort(key=lambda x: x['days_ahead'])
            nearest_cycle = next_cycles[0] if next_cycles else None
            
            result = {
                'time_diff_days': time_diff,
                'active_cycles': active_cycles,
                'next_cycles': next_cycles,
                'nearest_cycle': nearest_cycle
            }
            
            log_debug(f"Gann zaman döngüleri: {time_diff} gün, {len([c for cycles in active_cycles.values() for c in cycles])} aktif döngü")
            return result
            
        except Exception as e:
            log_error(f"Gann zaman döngü hesaplama hatası: {e}")
            return {}
    
    def calculate_gann_score(self, symbol: str, price_data: Dict = None, date: datetime = None) -> Dict:
        """
        Gann tekniğine göre skor hesapla
        
        Args:
            symbol: Analiz edilecek sembol
            price_data: Fiyat verisi
            date: Analiz tarihi
            
        Returns:
            Gann skor ve analiz bilgileri
        """
        try:
            if date is None:
                date = datetime.utcnow()
            
            if price_data is None:
                # Varsayılan fiyat verisi oluştur
                price_data = {
                    date.strftime('%Y-%m-%d'): {'Close': 100.0, 'High': 105.0, 'Low': 95.0, 'Volume': 1000000}
                }
            
            # Son fiyatı al
            latest_date = max(price_data.keys())
            current_price = price_data[latest_date]['Close']
            
            # Gann karesi hesapla
            gann_square = self.calculate_gann_square(current_price, date)
            
            # Önemli dip/zirve noktalarını bul
            significant_points = self._find_significant_points(price_data)
            
            # Zaman döngülerini analiz et
            time_analysis = {}
            if significant_points:
                for point in significant_points[-3:]:  # Son 3 önemli nokta
                    point_date = datetime.strptime(point['date'], '%Y-%m-%d')
                    time_analysis[point['date']] = self.find_gann_time_cycles(point_date, date)
            
            # Gann skorunu hesapla
            score = self._calculate_gann_score_value(gann_square, time_analysis, current_price)
            
            result = {
                'gann_score': score,
                'gann_square': gann_square,
                'time_analysis': time_analysis,
                'significant_points': significant_points,
                'analysis_type': 'Gann Technique',
                'details': {
                    'current_price': current_price,
                    'square_position': gann_square.get('position_in_square', 0),
                    'active_cycles_count': sum(len(cycles) for cycles in time_analysis.values() if isinstance(cycles, dict) and 'active_cycles' in cycles)
                }
            }
            
            log_info(f"{symbol}: Gann skoru: {score:.2f}")
            return result
            
        except Exception as e:
            log_error(f"{symbol} Gann skor hesaplama hatası: {e}")
            return self._get_default_gann_score()
    
    def _find_significant_points(self, price_data: Dict) -> List[Dict]:
        """
        Önemli dip/zirve noktalarını bul
        
        Args:
            price_data: Fiyat verisi
            
        Returns:
            Önemli noktalar listesi
        """
        try:
            if len(price_data) < 10:
                return []
            
            # Fiyatları sırala
            sorted_prices = sorted(price_data.items(), key=lambda x: x[1]['Close'])
            
            # En düşük ve en yüksek noktaları al
            significant_points = []
            
            # En düşük 3 nokta
            for i in range(min(3, len(sorted_prices))):
                date, data = sorted_prices[i]
                significant_points.append({
                    'date': date,
                    'price': data['Close'],
                    'type': 'dip',
                    'significance': 3 - i
                })
            
            # En yüksek 3 nokta
            for i in range(min(3, len(sorted_prices))):
                date, data = sorted_prices[-(i+1)]
                significant_points.append({
                    'date': date,
                    'price': data['Close'],
                    'type': 'peak',
                    'significance': 3 - i
                })
            
            # Tarihe göre sırala
            significant_points.sort(key=lambda x: x['date'])
            
            return significant_points
            
        except Exception as e:
            log_warning(f"Önemli nokta bulma hatası: {e}")
            return []
    
    def _calculate_gann_score_value(self, gann_square: Dict, time_analysis: Dict, current_price: float) -> float:
        """
        Gann skor değerini hesapla
        
        Args:
            gann_square: Gann kare analizi
            time_analysis: Zaman analizi
            current_price: Mevcut fiyat
            
        Returns:
            Gann skoru (0-100)
        """
        try:
            base_score = 50.0
            
            # Gann karesi pozisyonu etkisi
            if gann_square:
                position = gann_square.get('position_in_square', 0.5)
                if position < 0.2 or position > 0.8:  # Kare sınırlarına yakın
                    base_score += 10.0
                elif 0.4 < position < 0.6:  # Kare ortasında
                    base_score -= 5.0
            
            # Zaman döngüleri etkisi
            cycle_bonus = 0
            for analysis in time_analysis.values():
                if isinstance(analysis, dict) and 'active_cycles' in analysis:
                    for cycle_type, cycles in analysis['active_cycles'].items():
                        if cycles:
                            cycle_bonus += len(cycles) * 5
            
            # Final skor
            final_score = base_score + cycle_bonus
            return max(0, min(100, final_score))
            
        except Exception as e:
            log_warning(f"Gann skor hesaplama hatası: {e}")
            return 50.0
    
    def _get_default_gann_score(self) -> Dict:
        """Varsayılan Gann skoru"""
        return {
            'gann_score': 50.0,
            'gann_square': {},
            'time_analysis': {},
            'significant_points': [],
            'analysis_type': 'Gann Technique',
            'details': {'error': 'Yetersiz veri'}
        }
    
    def get_gann_forecast(self, symbol: str, price_data: Dict, days_ahead: int = 90) -> List[Dict]:
        """
        Gann tekniğine göre gelecek tahmini
        
        Args:
            symbol: Analiz edilecek sembol
            price_data: Fiyat verisi
            days_ahead: Kaç gün ileriye bakılacak
            
        Returns:
            Gelecek tahminleri
        """
        try:
            if not price_data:
                return []
            
            current_date = datetime.utcnow()
            forecast = []
            
            # Önemli noktaları bul
            significant_points = self._find_significant_points(price_data)
            
            for i in range(0, days_ahead, 7):  # Her hafta kontrol
                check_date = current_date + timedelta(days=i)
                
                # Her önemli nokta için döngü kontrolü
                cycle_signals = []
                for point in significant_points[-2:]:  # Son 2 önemli nokta
                    point_date = datetime.strptime(point['date'], '%Y-%m-%d')
                    time_analysis = self.find_gann_time_cycles(point_date, check_date)
                    
                    if time_analysis.get('active_cycles'):
                        for cycle_type, cycles in time_analysis['active_cycles'].items():
                            if cycles:
                                cycle_signals.extend([f"{cycle['cycle_days']} günlük döngü" for cycle in cycles])
                
                if cycle_signals:
                    forecast.append({
                        'date': check_date.strftime('%Y-%m-%d'),
                        'signals': cycle_signals,
                        'signal_count': len(cycle_signals)
                    })
            
            log_info(f"{symbol}: {days_ahead} günlük Gann tahmini oluşturuldu")
            return forecast
            
        except Exception as e:
            log_error(f"Gann tahmin hatası: {e}")
            return []

# Global instance
gann_analyzer = GannTechniqueAnalyzer()



