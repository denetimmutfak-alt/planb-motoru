# -*- coding: utf-8 -*-
"""
PlanB Motoru - Gann + Astroloji Hibrit Açı Sistemi
W.D. Gann'ın gezegen açıları ile astrolojik kombinasyonu
"""

import math
import ephem
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from src.utils.logger import log_info, log_error, log_debug, log_warning

class GannAstroHybridAnalyzer:
    """Gann + Astroloji hibrit açı analiz işlemlerini yöneten sınıf"""
    
    def __init__(self):
        # Gann açıları (derece cinsinden)
        self.gann_angles = {
            'conjunction': 0,        # Kavuşum (0°)
            'sextile': 60,          # Sextil (60°)
            'square': 90,           # Kare (90°)
            'trine': 120,           # Trine (120°)
            'opposition': 180,      # Karşıtlık (180°)
            'quincunx': 150,        # Quincunx (150°)
            'semi_sextile': 30,     # Semi-sextil (30°)
            'semi_square': 45,      # Semi-kare (45°)
            'sesquiquadrate': 135   # Sesquiquadrate (135°)
        }
        
        # Gezegenler (Ephem ile uyumlu)
        self.planets = {
            'sun': ephem.Sun,
            'moon': ephem.Moon,
            'mercury': ephem.Mercury,
            'venus': ephem.Venus,
            'mars': ephem.Mars,
            'jupiter': ephem.Jupiter,
            'saturn': ephem.Saturn,
            'uranus': ephem.Uranus,
            'neptune': ephem.Neptune,
            'pluto': ephem.Pluto
        }
        
        # Gann'ın önemli gezegen kombinasyonları
        self.gann_combinations = {
            'mars_saturn': {'planets': ['mars', 'saturn'], 'angle': 180, 'effect': 'bearish', 'strength': 0.9},
            'jupiter_venus': {'planets': ['jupiter', 'venus'], 'angle': 120, 'effect': 'bullish', 'strength': 0.8},
            'sun_moon': {'planets': ['sun', 'moon'], 'angle': 0, 'effect': 'neutral', 'strength': 0.7},
            'mercury_venus': {'planets': ['mercury', 'venus'], 'angle': 0, 'effect': 'bullish', 'strength': 0.6},
            'jupiter_saturn': {'planets': ['jupiter', 'saturn'], 'angle': 90, 'effect': 'bearish', 'strength': 0.8},
            'mars_venus': {'planets': ['mars', 'venus'], 'angle': 180, 'effect': 'bearish', 'strength': 0.7},
            'sun_jupiter': {'planets': ['sun', 'jupiter'], 'angle': 120, 'effect': 'bullish', 'strength': 0.8},
            'moon_venus': {'planets': ['moon', 'venus'], 'angle': 60, 'effect': 'bullish', 'strength': 0.6}
        }
        
        # Açı toleransları (derece)
        self.angle_tolerances = {
            'exact': 1,      # Tam açı (±1°)
            'close': 3,      # Yakın açı (±3°)
            'wide': 8        # Geniş açı (±8°)
        }
        
        # Açı ağırlıkları
        self.angle_weights = {
            'conjunction': 0.3,
            'opposition': 0.25,
            'square': 0.2,
            'trine': 0.15,
            'sextile': 0.1
        }
        
        log_info("Gann Astro Hybrid Analyzer başlatıldı")
    
    def get_planet_positions(self, date: datetime = None, location: str = "Istanbul") -> Dict:
        """
        Gezegen pozisyonlarını hesapla
        
        Args:
            date: Analiz edilecek tarih
            location: Konum
            
        Returns:
            Gezegen pozisyonları
        """
        try:
            if date is None:
                date = datetime.utcnow()
            
            # Ephem observer oluştur
            observer = ephem.Observer()
            observer.lat = '41.0082'  # İstanbul enlemi
            observer.lon = '28.9784'  # İstanbul boylamı
            observer.date = date
            
            planet_positions = {}
            
            for planet_name, planet_class in self.planets.items():
                try:
                    planet = planet_class(observer)
                    planet_positions[planet_name] = {
                        'ra': math.degrees(planet.ra),  # Sağ açıklık (derece)
                        'dec': math.degrees(planet.dec),  # Dik açıklık (derece)
                        'longitude': math.degrees(planet.ra)  # Basit longitude
                    }
                except Exception as e:
                    log_warning(f"{planet_name} pozisyonu hesaplanamadı: {e}")
                    planet_positions[planet_name] = {
                        'ra': 0, 'dec': 0, 'longitude': 0
                    }
            
            return planet_positions
            
        except Exception as e:
            log_error(f"Gezegen pozisyonları hesaplama hatası: {e}")
            return {}
    
    def calculate_planet_aspects(self, planet_positions: Dict) -> List[Dict]:
        """
        Gezegen açılarını hesapla
        
        Args:
            planet_positions: Gezegen pozisyonları
            
        Returns:
            Gezegen açıları listesi
        """
        try:
            aspects = []
            planet_names = list(planet_positions.keys())
            
            # Tüm gezegen çiftlerini kontrol et
            for i in range(len(planet_names)):
                for j in range(i + 1, len(planet_names)):
                    planet1 = planet_names[i]
                    planet2 = planet_names[j]
                    
                    if planet1 in planet_positions and planet2 in planet_positions:
                        # Açıyı hesapla
                        angle = abs(planet_positions[planet1]['longitude'] - 
                                  planet_positions[planet2]['longitude'])
                        
                        # 0-360° aralığına normalize et
                        angle = angle % 360
                        if angle > 180:
                            angle = 360 - angle
                        
                        # Açı türünü belirle
                        aspect_type = self._get_aspect_type(angle)
                        
                        if aspect_type:
                            # Açı gücünü hesapla
                            aspect_strength = self._calculate_aspect_strength(angle, aspect_type)
                            
                            aspects.append({
                                'planet1': planet1,
                                'planet2': planet2,
                                'angle': angle,
                                'aspect_type': aspect_type,
                                'strength': aspect_strength,
                                'exactness': self._get_aspect_exactness(angle, aspect_type)
                            })
            
            # Güce göre sırala
            aspects.sort(key=lambda x: x['strength'], reverse=True)
            
            return aspects
            
        except Exception as e:
            log_error(f"Gezegen açıları hesaplama hatası: {e}")
            return []
    
    def _get_aspect_type(self, angle: float) -> Optional[str]:
        """Açı türünü belirle"""
        for aspect_name, aspect_angle in self.gann_angles.items():
            tolerance = self.angle_tolerances['wide']
            if abs(angle - aspect_angle) <= tolerance:
                return aspect_name
        return None
    
    def _calculate_aspect_strength(self, angle: float, aspect_type: str) -> float:
        """Açı gücünü hesapla"""
        try:
            target_angle = self.gann_angles[aspect_type]
            deviation = abs(angle - target_angle)
            
            # Tam açıya yakınlık
            if deviation <= self.angle_tolerances['exact']:
                strength = 1.0
            elif deviation <= self.angle_tolerances['close']:
                strength = 0.8
            elif deviation <= self.angle_tolerances['wide']:
                strength = 0.6
            else:
                strength = 0.0
            
            # Açı türü ağırlığı
            weight = self.angle_weights.get(aspect_type, 0.1)
            
            return strength * weight
            
        except Exception as e:
            log_warning(f"Açı gücü hesaplama hatası: {e}")
            return 0.0
    
    def _get_aspect_exactness(self, angle: float, aspect_type: str) -> str:
        """Açı hassasiyetini belirle"""
        target_angle = self.gann_angles[aspect_type]
        deviation = abs(angle - target_angle)
        
        if deviation <= self.angle_tolerances['exact']:
            return 'exact'
        elif deviation <= self.angle_tolerances['close']:
            return 'close'
        else:
            return 'wide'
    
    def analyze_gann_combinations(self, aspects: List[Dict]) -> List[Dict]:
        """
        Gann'ın önemli gezegen kombinasyonlarını analiz et
        
        Args:
            aspects: Gezegen açıları
            
        Returns:
            Gann kombinasyonları
        """
        try:
            gann_results = []
            
            for combo_name, combo_info in self.gann_combinations.items():
                planets = combo_info['planets']
                target_angle = combo_info['angle']
                expected_effect = combo_info['effect']
                base_strength = combo_info['strength']
                
                # Bu kombinasyonu aspects'te ara
                for aspect in aspects:
                    if ((aspect['planet1'] in planets and aspect['planet2'] in planets) or
                        (aspect['planet2'] in planets and aspect['planet1'] in planets)):
                        
                        # Açı uygunluğu
                        angle_match = abs(aspect['angle'] - target_angle) <= self.angle_tolerances['wide']
                        
                        if angle_match:
                            # Final güç hesaplama
                            final_strength = aspect['strength'] * base_strength
                            
                            gann_results.append({
                                'combination': combo_name,
                                'planets': planets,
                                'aspect_type': aspect['aspect_type'],
                                'angle': aspect['angle'],
                                'expected_effect': expected_effect,
                                'strength': final_strength,
                                'exactness': aspect['exactness'],
                                'market_impact': self._get_market_impact(expected_effect, final_strength)
                            })
            
            # Güce göre sırala
            gann_results.sort(key=lambda x: x['strength'], reverse=True)
            
            return gann_results
            
        except Exception as e:
            log_error(f"Gann kombinasyonları analiz hatası: {e}")
            return []
    
    def _get_market_impact(self, effect: str, strength: float) -> str:
        """Piyasa etkisini belirle"""
        if strength >= 0.7:
            if effect == 'bullish':
                return 'strong_bullish'
            elif effect == 'bearish':
                return 'strong_bearish'
            else:
                return 'strong_neutral'
        elif strength >= 0.4:
            if effect == 'bullish':
                return 'moderate_bullish'
            elif effect == 'bearish':
                return 'moderate_bearish'
            else:
                return 'moderate_neutral'
        else:
            return 'weak'
    
    def calculate_gann_astro_score(self, symbol: str, date: datetime = None) -> Dict:
        """
        Gann + Astroloji hibrit skorunu hesapla
        
        Args:
            symbol: Analiz edilecek sembol
            date: Analiz tarihi
            
        Returns:
            Gann-Astro skor ve analiz bilgileri
        """
        try:
            if date is None:
                date = datetime.utcnow()
            
            # Gezegen pozisyonlarını al
            planet_positions = self.get_planet_positions(date)
            
            if not planet_positions:
                return self._get_default_gann_astro_score()
            
            # Gezegen açılarını hesapla
            aspects = self.calculate_planet_aspects(planet_positions)
            
            # Gann kombinasyonlarını analiz et
            gann_combinations = self.analyze_gann_combinations(aspects)
            
            # Temel skor hesaplama
            base_score = 50.0  # Nötr skor
            
            # Gann kombinasyonları etkisi
            combination_adjustment = 0.0
            bullish_signals = 0
            bearish_signals = 0
            
            for combo in gann_combinations[:5]:  # En güçlü 5 kombinasyon
                strength = combo['strength']
                effect = combo['expected_effect']
                
                if effect == 'bullish':
                    combination_adjustment += strength * 10
                    bullish_signals += 1
                elif effect == 'bearish':
                    combination_adjustment -= strength * 10
                    bearish_signals += 1
            
            # Genel açı etkisi
            aspect_adjustment = 0.0
            for aspect in aspects[:10]:  # En güçlü 10 açı
                aspect_adjustment += aspect['strength'] * 2
            
            # Sembol türüne göre ek ayarlama
            symbol_adjustment = self._get_symbol_gann_astro_adjustment(symbol, gann_combinations)
            
            # Final skor
            final_score = base_score + combination_adjustment + aspect_adjustment + symbol_adjustment
            final_score = max(0, min(100, final_score))
            
            result = {
                'gann_astro_score': final_score,
                'planet_positions': planet_positions,
                'aspects': aspects[:10],  # En güçlü 10 açı
                'gann_combinations': gann_combinations[:5],  # En güçlü 5 kombinasyon
                'signal_balance': {
                    'bullish_signals': bullish_signals,
                    'bearish_signals': bearish_signals,
                    'net_signal': bullish_signals - bearish_signals
                },
                'analysis_type': 'Gann Astro Hybrid',
                'details': {
                    'base_score': base_score,
                    'combination_adjustment': combination_adjustment,
                    'aspect_adjustment': aspect_adjustment,
                    'symbol_adjustment': symbol_adjustment,
                    'total_aspects': len(aspects),
                    'active_combinations': len(gann_combinations)
                }
            }
            
            log_info(f"{symbol}: Gann-Astro skoru: {final_score:.2f} ({bullish_signals}B/{bearish_signals}S)")
            return result
            
        except Exception as e:
            log_error(f"{symbol} Gann-Astro skor hesaplama hatası: {e}")
            return self._get_default_gann_astro_score()
    
    def _get_symbol_gann_astro_adjustment(self, symbol: str, gann_combinations: List[Dict]) -> float:
        """
        Sembol türüne göre Gann-Astro etki ayarlaması
        
        Args:
            symbol: Sembol kodu
            gann_combinations: Gann kombinasyonları
            
        Returns:
            Ayarlama değeri
        """
        try:
            # Teknoloji hisseleri: Jüpiter-Venüs kombinasyonları ile güçlü korelasyon
            if any(tech in symbol.upper() for tech in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA']):
                for combo in gann_combinations:
                    if 'jupiter_venus' in combo['combination'] and combo['expected_effect'] == 'bullish':
                        return 8.0
                return 2.0
            
            # Bankacılık hisseleri: Mars-Satürn kombinasyonları ile korelasyon
            elif any(bank in symbol.upper() for bank in ['JPM', 'BAC', 'WFC', 'C', 'GS']):
                for combo in gann_combinations:
                    if 'mars_saturn' in combo['combination'] and combo['expected_effect'] == 'bearish':
                        return -6.0
                return -1.0
            
            # Enerji hisseleri: Güneş-Jüpiter kombinasyonları ile korelasyon
            elif any(energy in symbol.upper() for energy in ['XOM', 'CVX', 'COP', 'EOG']):
                for combo in gann_combinations:
                    if 'sun_jupiter' in combo['combination'] and combo['expected_effect'] == 'bullish':
                        return 6.0
                return 1.0
            
            # Altın ve değerli metaller: Ay-Venüs kombinasyonları ile korelasyon
            elif any(metal in symbol.upper() for metal in ['GC', 'GOLD', 'SILVER', 'PLATINUM']):
                for combo in gann_combinations:
                    if 'moon_venus' in combo['combination'] and combo['expected_effect'] == 'bullish':
                        return 7.0
                return 2.0
            
            # Varsayılan: Nötr
            else:
                return 0.0
                
        except Exception as e:
            log_warning(f"Sembol Gann-Astro ayarlama hatası: {e}")
            return 0.0
    
    def _get_default_gann_astro_score(self) -> Dict:
        """Varsayılan Gann-Astro skoru"""
        return {
            'gann_astro_score': 50.0,
            'planet_positions': {},
            'aspects': [],
            'gann_combinations': [],
            'signal_balance': {'bullish_signals': 0, 'bearish_signals': 0, 'net_signal': 0},
            'analysis_type': 'Gann Astro Hybrid',
            'details': {'error': 'Gezegen pozisyonları hesaplanamadı'}
        }
    
    def get_gann_astro_forecast(self, symbol: str, days_ahead: int = 30) -> List[Dict]:
        """
        Gann-Astro gelecek tahmini
        
        Args:
            symbol: Analiz edilecek sembol
            days_ahead: Kaç gün ileriye bakılacak
            
        Returns:
            Gelecek tahminleri
        """
        try:
            start_date = datetime.utcnow()
            forecast = []
            
            for i in range(0, days_ahead, 3):  # Her 3 günde bir kontrol
                check_date = start_date + timedelta(days=i)
                result = self.calculate_gann_astro_score(symbol, check_date)
                
                # Güçlü sinyaller
                if result['gann_combinations']:
                    strongest_combo = result['gann_combinations'][0]
                    if strongest_combo['strength'] > 0.6:
                        forecast.append({
                            'date': check_date.strftime('%Y-%m-%d'),
                            'combination': strongest_combo['combination'],
                            'effect': strongest_combo['expected_effect'],
                            'strength': strongest_combo['strength'],
                            'market_impact': strongest_combo['market_impact']
                        })
            
            log_info(f"{symbol}: {days_ahead} günlük Gann-Astro tahmini oluşturuldu")
            return forecast
            
        except Exception as e:
            log_error(f"Gann-Astro tahmin hatası: {e}")
            return []

# Global instance
gann_astro_analyzer = GannAstroHybridAnalyzer()





