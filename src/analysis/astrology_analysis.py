"""
PlanB Motoru - Ultra Advanced Astrology Analysis Module
Financial Astrology & Planetary Cycles - Professional Level
Market Astrology, Harmonics, Eclipses, Lunar Nodes, Planetary Returns
"""
import ephem
import numpy as np
import math
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, List
from src.utils.logger import log_info, log_error, log_debug, log_warning
from src.data.company_founding_dates import CompanyFoundingDates
from config.settings import config

# Global analyzer instance
_analyzer = None

def get_astrology_score(symbol: str, stock_data=None) -> float:
    """Ultra gelişmiş astroloji skorunu döndür"""
    global _analyzer
    try:
        if _analyzer is None:
            _analyzer = UltraAstrologyAnalyzer()
        return _analyzer.calculate_comprehensive_astrology_score(symbol, stock_data)
    except Exception as e:
        log_error(f"Astroloji skoru hesaplanırken hata: {e}")
        return 50.0  # Varsayılan nötr skor

class UltraAstrologyAnalyzer:
    """Ultra gelişmiş finansal astroloji analiz sistemi"""
    
    def __init__(self):
        # Traditional planets
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
        
        # Financial astrology aspects (degrees)
        self.major_aspects = {
            'conjunction': 0,
            'sextile': 60,
            'square': 90,
            'trine': 120,
            'opposition': 180
        }
        
        # Market-related planetary weights
        self.financial_planet_weights = {
            'jupiter': 0.20,  # Expansion, growth, optimism
            'saturn': 0.18,   # Contraction, discipline, structure
            'mars': 0.15,     # Action, volatility, energy
            'venus': 0.12,    # Values, money, beauty
            'mercury': 0.10,  # Communication, trade, data
            'pluto': 0.08,    # Transformation, power, extremes
            'uranus': 0.07,   # Innovation, sudden changes, technology
            'neptune': 0.05,  # Illusion, speculation, oil/gas
            'sun': 0.03,      # Vitality, leadership
            'moon': 0.02      # Emotions, public sentiment
        }
        
        try:
            self.founding_dates = CompanyFoundingDates()
        except:
            self.founding_dates = None
        
    def calculate_comprehensive_astrology_score(self, symbol: str, stock_data=None) -> float:
        """Kapsamlı astroloji skoru hesaplama"""
        try:
            current_date = datetime.utcnow()
            
            # 1. Current planetary transits
            transit_score = self._calculate_transit_score(current_date)
            
            # 2. Lunar phases impact
            lunar_score = self._calculate_lunar_phase_score(current_date)
            
            # 3. Planetary aspects score
            aspect_score = self._calculate_planetary_aspects_score(current_date)
            
            # 4. Eclipse influence
            eclipse_score = self._calculate_eclipse_influence(current_date)
            
            # 5. Planetary cycles
            cycle_score = self._calculate_planetary_cycles_score(current_date)
            
            # 6. Company founding chart analysis (if available)
            founding_score = self._calculate_company_founding_score(symbol, current_date)
            
            # 7. Retrograde effects
            retrograde_score = self._calculate_retrograde_effects(current_date)
            
            # 8. Financial astrology indicators
            financial_indicators = self._calculate_financial_astrology_indicators(current_date)
            
            # Weighted combination
            total_score = (
                transit_score * 0.20 +
                lunar_score * 0.15 +
                aspect_score * 0.15 +
                eclipse_score * 0.10 +
                cycle_score * 0.15 +
                founding_score * 0.10 +
                retrograde_score * 0.05 +
                financial_indicators * 0.10
            )
            
            # Normalize to 0-100 range
            final_score = max(0, min(100, total_score))
            
            log_info(f"{symbol}: Kapsamlı astroloji skoru: {final_score:.2f}")
            return final_score
            
        except Exception as e:
            log_error(f"Kapsamlı astroloji skoru hesaplama hatası: {e}")
            return 50.0
    
    def _calculate_transit_score(self, date: datetime) -> float:
        """Güncel gezegen geçişleri skorunu hesapla"""
        try:
            score = 50.0
            
            # Major transits affecting markets
            for planet_name, planet_func in self.planets.items():
                planet = planet_func(date)
                
                # Get zodiac position (0-360 degrees)
                lon = float(planet.hlon) * 180 / math.pi
                
                # Market-sensitive degrees
                if self._is_market_sensitive_degree(lon):
                    weight = self.financial_planet_weights.get(planet_name, 0.05)
                    if planet_name in ['jupiter', 'saturn']:
                        score += weight * 30  # Major planets have more impact
                    else:
                        score += weight * 20
                
                # Critical degrees (0, 15, 30 of cardinal signs)
                if self._is_critical_degree(lon):
                    score += self.financial_planet_weights.get(planet_name, 0.05) * 15
            
            return max(0, min(100, score))
            
        except Exception as e:
            log_error(f"Transit score hesaplama hatası: {e}")
            return 50.0
    
    def _calculate_lunar_phase_score(self, date: datetime) -> float:
        """Ay evrelerinin piyasa etkisini hesapla"""
        try:
            moon = ephem.Moon(date)
            sun = ephem.Sun(date)
            
            # Moon phase calculation
            moon_lon = float(moon.hlon) * 180 / math.pi
            sun_lon = float(sun.hlon) * 180 / math.pi
            
            phase_angle = (moon_lon - sun_lon) % 360
            
            # New Moon (0°) - Fresh starts, new trends
            if 0 <= phase_angle <= 15 or 345 <= phase_angle <= 360:
                return 75.0  # Positive for new beginnings
            
            # Waxing Quarter (90°) - Growth phase
            elif 75 <= phase_angle <= 105:
                return 80.0  # Growth energy
            
            # Full Moon (180°) - Peak energy, volatility
            elif 165 <= phase_angle <= 195:
                return 40.0  # High volatility, caution
            
            # Waning Quarter (270°) - Release, correction
            elif 255 <= phase_angle <= 285:
                return 45.0  # Correction phase
            
            # Waxing phases
            elif 15 < phase_angle < 75:
                return 65.0  # Building energy
            elif 105 < phase_angle < 165:
                return 70.0  # Approaching peak
            
            # Waning phases
            elif 195 < phase_angle < 255:
                return 55.0  # Releasing energy
            elif 285 < phase_angle < 345:
                return 60.0  # Preparing for new cycle
            
            return 50.0
            
        except Exception as e:
            log_error(f"Lunar phase score hesaplama hatası: {e}")
            return 50.0
    
    def _calculate_planetary_aspects_score(self, date: datetime) -> float:
        """Gezegen açıları skorunu hesapla"""
        try:
            score = 50.0
            planet_positions = {}
            
            # Get all planet positions
            for name, planet_func in self.planets.items():
                planet = planet_func(date)
                planet_positions[name] = float(planet.hlon) * 180 / math.pi
            
            # Check major aspects between key planets
            key_pairs = [
                ('jupiter', 'saturn'),  # Major business cycle
                ('mars', 'jupiter'),    # Action and expansion
                ('venus', 'mars'),      # Values and action
                ('mercury', 'jupiter'), # Communication and growth
            ]
            
            for planet1, planet2 in key_pairs:
                if planet1 in planet_positions and planet2 in planet_positions:
                    aspect_angle = abs(planet_positions[planet1] - planet_positions[planet2])
                    aspect_angle = min(aspect_angle, 360 - aspect_angle)
                    
                    # Check for major aspects
                    for aspect_name, degree in self.major_aspects.items():
                        if abs(aspect_angle - degree) <= 8:  # 8-degree orb
                            aspect_strength = 8 - abs(aspect_angle - degree)
                            
                            if aspect_name in ['trine', 'sextile']:
                                score += aspect_strength * 2  # Positive aspects
                            elif aspect_name in ['conjunction']:
                                score += aspect_strength * 1  # Neutral
                            elif aspect_name in ['square', 'opposition']:
                                score -= aspect_strength * 1  # Challenging aspects
            
            return max(0, min(100, score))
            
        except Exception as e:
            log_error(f"Planetary aspects score hesaplama hatası: {e}")
            return 50.0
    
    def _calculate_eclipse_influence(self, date: datetime) -> float:
        """Tutulma etkilerini hesapla"""
        try:
            # Simplified eclipse calculation
            score = 50.0
            
            # Check if we're near eclipse season (simplified)
            sun = ephem.Sun(date)
            moon = ephem.Moon(date)
            
            sun_lon = float(sun.hlon) * 180 / math.pi
            moon_lon = float(moon.hlon) * 180 / math.pi
            
            # If Sun and Moon are close to opposite (Full Moon) or conjunction (New Moon)
            angle_diff = abs(sun_lon - moon_lon)
            angle_diff = min(angle_diff, 360 - angle_diff)
            
            if angle_diff < 10 or angle_diff > 170:  # Near eclipse conditions
                score -= 10  # Eclipse periods can bring volatility
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50.0
    
    def _calculate_planetary_cycles_score(self, date: datetime) -> float:
        """Gezegen döngüleri skorunu hesapla"""
        try:
            score = 50.0
            
            # Jupiter cycle (approximately 12 years)
            jupiter_cycle_position = (date.year % 12) / 12
            if 0.2 <= jupiter_cycle_position <= 0.8:  # Growth phase
                score += 15
            
            # Saturn cycle (approximately 29 years)
            saturn_cycle_position = (date.year % 29) / 29
            if 0.1 <= saturn_cycle_position <= 0.3:  # Building phase
                score += 10
            elif 0.7 <= saturn_cycle_position <= 0.9:  # Testing phase
                score -= 10
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50.0
    
    def _calculate_company_founding_score(self, symbol: str, current_date: datetime) -> float:
        """Şirket kuruluş tarihi astroloji skorunu hesapla"""
        try:
            # Simplified - would need actual founding dates
            return 50.0
            
        except Exception as e:
            return 50.0
    
    def _calculate_retrograde_effects(self, date: datetime) -> float:
        """Retrograde gezegenlerinin etkisini hesapla"""
        try:
            score = 50.0
            
            for planet_name, planet_func in self.planets.items():
                if planet_name in ['sun', 'moon']:
                    continue  # Sun and Moon don't go retrograde
                
                # Simplified retrograde check
                try:
                    planet_today = planet_func(date)
                    planet_yesterday = planet_func(date - timedelta(days=1))
                    
                    lon_today = float(planet_today.hlon)
                    lon_yesterday = float(planet_yesterday.hlon)
                    
                    # If longitude decreased, planet might be retrograde
                    if lon_today < lon_yesterday:
                        weight = self.financial_planet_weights.get(planet_name, 0.05)
                        
                        if planet_name == 'mercury':
                            score -= weight * 30  # Mercury retrograde affects communication/trade
                        elif planet_name == 'venus':
                            score -= weight * 20  # Venus retrograde affects values/money
                        else:
                            score -= weight * 10  # Other retrogrades
                except:
                    continue
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50.0
    
    def _calculate_financial_astrology_indicators(self, date: datetime) -> float:
        """Finansal astroloji göstergeleri"""
        try:
            score = 50.0
            
            # Get key planet positions
            jupiter = ephem.Jupiter(date)
            saturn = ephem.Saturn(date)
            
            jupiter_lon = float(jupiter.hlon) * 180 / math.pi
            saturn_lon = float(saturn.hlon) * 180 / math.pi
            
            # Jupiter in earth signs (simplified)
            if self._is_in_earth_sign(jupiter_lon):
                score += 15  # Earth signs favor material stability
            
            # Saturn aspects to Jupiter
            jupiter_saturn_angle = abs(jupiter_lon - saturn_lon)
            jupiter_saturn_angle = min(jupiter_saturn_angle, 360 - jupiter_saturn_angle)
            
            if 115 <= jupiter_saturn_angle <= 125:  # Trine aspect
                score += 10  # Favorable business conditions
            elif 85 <= jupiter_saturn_angle <= 95:  # Square aspect
                score -= 10  # Business challenges
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50.0
    
    def _is_market_sensitive_degree(self, longitude: float) -> bool:
        """Piyasa hassas derecelerini kontrol et"""
        # Cardinal points (0°, 90°, 180°, 270°)
        cardinal_points = [0, 90, 180, 270]
        for point in cardinal_points:
            if abs((longitude - point) % 360) <= 5:
                return True
        return False
    
    def _is_critical_degree(self, longitude: float) -> bool:
        """Kritik dereceleri kontrol et"""
        # Critical degrees in astrology
        critical_degrees = [0, 13, 26]  # For cardinal signs
        sign_position = longitude % 30
        
        for degree in critical_degrees:
            if abs(sign_position - degree) <= 2:
                return True
        return False
    
    def _is_in_earth_sign(self, longitude: float) -> bool:
        """Toprak burçlarında mı kontrol et"""
        # Taurus (30-60), Virgo (150-180), Capricorn (270-300)
        earth_signs = [(30, 60), (150, 180), (270, 300)]
        
        for start, end in earth_signs:
            if start <= longitude <= end:
                return True
        return False

# Compatibility with old interface
class AstrologyAnalyzer(UltraAstrologyAnalyzer):
    """Backwards compatibility wrapper"""
    
    def calculate_astrology_score(self, symbol: str, date: datetime = None) -> float:
        """Legacy method compatibility"""
        return self.calculate_comprehensive_astrology_score(symbol)
