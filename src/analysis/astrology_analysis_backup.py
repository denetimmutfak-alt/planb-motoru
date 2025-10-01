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
        
        # Asteroid and additional bodies for financial astrology
        self.asteroids = {
            'ceres': ephem.Ceres,
            'pallas': ephem.Pallas,
            'juno': ephem.Juno,
            'vesta': ephem.Vesta
        }
        
        # Financial astrology aspects (degrees)
        self.major_aspects = {
            'conjunction': 0,
            'sextile': 60,
            'square': 90,
            'trine': 120,
            'opposition': 180
        }
        
        self.minor_aspects = {
            'semi_sextile': 30,
            'semi_square': 45,
            'quintile': 72,
            'sesquiquadrate': 135,
            'quincunx': 150,
            'biquintile': 144
        }
        
        # Harmonic numbers for financial analysis
        self.harmonics = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 24]
        
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
        
        # Eclipse effects on markets
        self.eclipse_orb = 10.0  # degrees
        self.eclipse_duration = 180  # days of influence
        
        self.founding_dates = CompanyFoundingDates()
        
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
            
            # 5. Planetary returns and cycles
            cycle_score = self._calculate_planetary_cycles_score(current_date)
            
            # 6. Harmonic analysis
            harmonic_score = self._calculate_harmonic_score(current_date)
            
            # 7. Company founding chart analysis (if available)
            founding_score = self._calculate_company_founding_score(symbol, current_date)
            
            # 8. Retrograde effects
            retrograde_score = self._calculate_retrograde_effects(current_date)
            
            # 9. Financial astrology indicators
            financial_indicators = self._calculate_financial_astrology_indicators(current_date)
            
            # 10. Vedic astrology elements
            vedic_score = self._calculate_vedic_elements(current_date)
            
            # Weighted combination
            total_score = (
                transit_score * 0.15 +
                lunar_score * 0.10 +
                aspect_score * 0.15 +
                eclipse_score * 0.10 +
                cycle_score * 0.12 +
                harmonic_score * 0.08 +
                founding_score * 0.10 +
                retrograde_score * 0.05 +
                financial_indicators * 0.10 +
                vedic_score * 0.05
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
                ('sun', 'jupiter'),     # Leadership and optimism
                ('pluto', 'jupiter'),   # Transformation and growth
                ('uranus', 'saturn'),   # Innovation vs tradition
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
                                # Context dependent
                                if planet1 == 'jupiter' or planet2 == 'jupiter':
                                    score += aspect_strength * 1.5  # Jupiter conjunctions often positive
                                else:
                                    score += aspect_strength * 0.5
                            elif aspect_name in ['square', 'opposition']:
                                score -= aspect_strength * 1.5  # Challenging aspects
            
            return max(0, min(100, score))
            
        except Exception as e:
            log_error(f"Planetary aspects score hesaplama hatası: {e}")
            return 50.0
    
    def _calculate_eclipse_influence(self, date: datetime) -> float:
        """Tutulma etkilerini hesapla"""
        try:
            # Approximate eclipse dates (would need ephemeris for exact calculation)
            # This is simplified - in real implementation, use ephemeris data
            
            score = 50.0
            
            # Check if we're near eclipse season
            sun = ephem.Sun(date)
            moon = ephem.Moon(date)
            
            sun_lon = float(sun.hlon) * 180 / math.pi
            moon_lon = float(moon.hlon) * 180 / math.pi
            
            # Lunar nodes approximation (simplified)
            # Real implementation would track actual nodes
            node_position = (date.year - 2020) * 19.3  # Approximate node movement
            
            # If Sun or Moon is near nodes, eclipse possibility
            if (abs((sun_lon - node_position) % 360) < self.eclipse_orb or
                abs((moon_lon - node_position) % 360) < self.eclipse_orb):
                score -= 15  # Eclipse periods often bring volatility
            
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
            
            # Mars cycle (approximately 2 years)
            mars_cycle_position = ((date.year * 12 + date.month) % 24) / 24
            if 0.3 <= mars_cycle_position <= 0.7:  # Active phase
                score += 8
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50.0
    
    def _calculate_harmonic_score(self, date: datetime) -> float:
        """Harmonik analiz skorunu hesapla"""
        try:
            score = 50.0
            planet_positions = {}
            
            # Get planet positions
            for name, planet_func in self.planets.items():
                planet = planet_func(date)
                planet_positions[name] = float(planet.hlon) * 180 / math.pi
            
            # Check harmonic patterns
            for harmonic in [4, 8, 16]:  # Business-oriented harmonics
                harmonic_score = 0
                harmonic_positions = {name: (pos * harmonic) % 360 
                                    for name, pos in planet_positions.items()}
                
                # Look for clusters in harmonic chart
                if self._has_harmonic_cluster(harmonic_positions):
                    harmonic_score += 10
                
                score += harmonic_score / len(self.harmonics)
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50.0
    
    def _calculate_company_founding_score(self, symbol: str, current_date: datetime) -> float:
        """Şirket kuruluş tarihi astroloji skorunu hesapla"""
        try:
            # This would require company founding date data
            # Simplified version
            score = 50.0
            
            # Example: Check if current transits are favorable to company's "birth chart"
            # In real implementation, this would involve:
            # 1. Company founding date astrology chart
            # 2. Current transits to founding chart
            # 3. Progressions and directions
            
            return score
            
        except Exception as e:
            return 50.0
    
    def _calculate_retrograde_effects(self, date: datetime) -> float:
        """Retrograde gezegenlerinin etkisini hesapla"""
        try:
            score = 50.0
            
            for planet_name, planet_func in self.planets.items():
                if planet_name in ['sun', 'moon']:
                    continue  # Sun and Moon don't go retrograde
                
                # Check if planet is retrograde (simplified check)
                planet_today = planet_func(date)
                planet_yesterday = planet_func(date - timedelta(days=1))
                
                lon_today = float(planet_today.hlon)
                lon_yesterday = float(planet_yesterday.hlon)
                
                # If longitude decreased, planet might be retrograde
                if lon_today < lon_yesterday:
                    weight = self.financial_planet_weights.get(planet_name, 0.05)
                    
                    if planet_name == 'mercury':
                        score -= weight * 40  # Mercury retrograde affects communication/trade
                    elif planet_name == 'venus':
                        score -= weight * 30  # Venus retrograde affects values/money
                    elif planet_name in ['mars', 'jupiter', 'saturn']:
                        score -= weight * 25  # Other retrogrades
                    else:
                        score -= weight * 15  # Outer planet retrogrades
            
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
            mars = ephem.Mars(date)
            
            jupiter_lon = float(jupiter.hlon) * 180 / math.pi
            saturn_lon = float(saturn.hlon) * 180 / math.pi
            mars_lon = float(mars.hlon) * 180 / math.pi
            
            # Jupiter in financial signs (Taurus, Virgo, Capricorn)
            if self._is_in_earth_sign(jupiter_lon):
                score += 20  # Earth signs favor material stability
            
            # Saturn aspects to Jupiter (business cycle indicator)
            jupiter_saturn_angle = abs(jupiter_lon - saturn_lon)
            jupiter_saturn_angle = min(jupiter_saturn_angle, 360 - jupiter_saturn_angle)
            
            if 115 <= jupiter_saturn_angle <= 125:  # Trine aspect (120°)
                score += 15  # Favorable business conditions
            elif 85 <= jupiter_saturn_angle <= 95:  # Square aspect (90°)
                score -= 15  # Business challenges
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50.0
    
    def _calculate_vedic_elements(self, date: datetime) -> float:
        """Vedik astroloji unsurları"""
        try:
            # Simplified Vedic calculation
            # Real implementation would include:
            # - Nakshatra positions
            # - Dasha periods
            # - Yogas
            
            score = 50.0
            
            # Moon's nakshatra (simplified)
            moon = ephem.Moon(date)
            moon_lon = float(moon.hlon) * 180 / math.pi
            
            # 27 nakshatras, each 13°20'
            nakshatra = int(moon_lon / 13.333) + 1
            
            # Some nakshatras are considered more favorable for business
            favorable_nakshatras = [2, 3, 7, 10, 13, 17, 22, 26]  # Simplified list
            
            if nakshatra in favorable_nakshatras:
                score += 20
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50.0
    
    def _is_market_sensitive_degree(self, longitude: float) -> bool:
        """Piyasa hassas derecelerini kontrol et"""
        # Aries 0°, Cancer 0°, Libra 0°, Capricorn 0° (Cardinal points)
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
    
    def _has_harmonic_cluster(self, harmonic_positions: Dict[str, float]) -> bool:
        """Harmonik kümelenme var mı kontrol et"""
        positions = list(harmonic_positions.values())
        
        # Check if multiple planets are within 30 degrees of each other
        for i, pos1 in enumerate(positions):
            cluster_count = 1
            for j, pos2 in enumerate(positions):
                if i != j:
                    angle_diff = abs(pos1 - pos2)
                    angle_diff = min(angle_diff, 360 - angle_diff)
                    if angle_diff <= 30:
                        cluster_count += 1
            
            if cluster_count >= 3:  # 3 or more planets in cluster
                return True
        
        return False

# Compatibility with old interface
class AstrologyAnalyzer(UltraAstrologyAnalyzer):
    """Backwards compatibility wrapper"""
    
    def calculate_astrology_score(self, symbol: str, date: datetime = None) -> float:
        """Legacy method compatibility"""
        return self.calculate_comprehensive_astrology_score(symbol)
            
            # Skor hesapla (0-100 arası)
            score = (1 - (angle_diff / (2 * np.pi))) * 100
            
            log_debug(f"Mars-Jupiter açı farkı: {angle_diff:.4f}, Skor: {score:.2f}")
            return round(max(0, min(100, score)), 2)
            
        except Exception as e:
            log_error(f"Mars-Jupiter açı analizi yapılırken hata: {e}")
            return 50.0
    
    def calculate_moon_phase_analysis(self, date: datetime = None) -> Dict[str, any]:
        """Ay fazı analizi"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            moon = ephem.Moon(date)
            phase = moon.phase  # 0-100 arası
            
            # Ay fazına göre analiz
            if phase < 5:
                phase_name = "Yeni Ay"
                market_sentiment = "Başlangıç enerjisi - Yeni pozisyonlar için uygun"
                score = 60
            elif phase < 25:
                phase_name = "Büyüyen Ay"
                market_sentiment = "Büyüme enerjisi - Alım sinyali güçlü"
                score = 80
            elif phase < 45:
                phase_name = "İlk Dördün"
                market_sentiment = "Kararsızlık - Dikkatli olun"
                score = 40
            elif phase < 55:
                phase_name = "Dolunay"
                market_sentiment = "Volatilite artışı - Satış sinyali güçlü"
                score = 20
            elif phase < 75:
                phase_name = "Son Dördün"
                market_sentiment = "Kararsızlık - Dikkatli olun"
                score = 40
            else:
                phase_name = "Küçülen Ay"
                market_sentiment = "Azalma enerjisi - Satış sinyali"
                score = 30
            
            return {
                'phase': phase,
                'phase_name': phase_name,
                'market_sentiment': market_sentiment,
                'score': score
            }
            
        except Exception as e:
            log_error(f"Ay fazı analizi yapılırken hata: {e}")
            return {'phase': 0, 'phase_name': 'Bilinmiyor', 'market_sentiment': 'Analiz yapılamadı', 'score': 50}
    
    def calculate_planetary_aspects(self, date: datetime = None) -> Dict[str, float]:
        """Gezegen açıları analizi"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            aspects = {}
            
            # Önemli gezegen çiftleri
            important_pairs = [
                ('mars', 'jupiter'),
                ('venus', 'mars'),
                ('mercury', 'venus'),
                ('sun', 'moon'),
                ('jupiter', 'saturn')
            ]
            
            for planet1_name, planet2_name in important_pairs:
                try:
                    planet1 = self.planets[planet1_name](date)
                    planet2 = self.planets[planet2_name](date)
                    
                    angle_diff = abs(planet1.ra - planet2.ra) % (2 * np.pi)
                    
                    # Açıya göre skor hesapla
                    if angle_diff < np.pi/6:  # 30 derece içinde
                        score = 90
                    elif angle_diff < np.pi/3:  # 60 derece içinde
                        score = 70
                    elif angle_diff < np.pi/2:  # 90 derece içinde
                        score = 50
                    else:
                        score = 30
                    
                    aspects[f"{planet1_name}_{planet2_name}"] = score
                    
                except Exception as e:
                    log_debug(f"{planet1_name}-{planet2_name} açısı hesaplanamadı: {e}")
                    aspects[f"{planet1_name}_{planet2_name}"] = 50
            
            return aspects
            
        except Exception as e:
            log_error(f"Gezegen açıları hesaplanırken hata: {e}")
            return {}
    
    def calculate_astrology_score(self, symbol: str, date: datetime = None) -> float:
        """Genel astroloji skoru hesapla - Kuruluş tarihi entegrasyonlu + Vedik Astroloji"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            # Vedik astroloji aktif mi kontrol et
            if config.VEDIC_ASTROLOGY_ENABLED:
                try:
                    from src.analysis.vedic_astrology import vedic_analyzer
                    
                    # Şirketin kuruluş tarihini al
                    founding_date = self.founding_dates.get_founding_date(symbol)
                    if founding_date:
                        # String ise datetime'a çevir
                        if isinstance(founding_date, str):
                            try:
                                founding_date = datetime.strptime(founding_date, '%Y-%m-%d')
                            except:
                                founding_date = None
                        
                        if founding_date:
                            # Vedik astroloji analizi
                            vedic_result = vedic_analyzer.calculate_vedic_score(
                                symbol, 
                                founding_date.strftime('%Y-%m-%d'),
                                date.strftime('%Y-%m-%d')
                            )
                            
                            if 'vedic_score' in vedic_result and vedic_result['vedic_score'] != config.VEDIC_FALLBACK_SCORE:
                                log_info(f"{symbol}: Vedik astroloji skoru kullanılıyor: {vedic_result['vedic_score']}")
                                return vedic_result['vedic_score']
                            else:
                                log_warning(f"{symbol}: Vedik analiz başarısız, geleneksel analiz kullanılıyor")
                        else:
                            log_warning(f"{symbol}: Kuruluş tarihi geçersiz, geleneksel analiz kullanılıyor")
                    else:
                        log_warning(f"{symbol}: Kuruluş tarihi bulunamadı, geleneksel analiz kullanılıyor")
                        
                except Exception as e:
                    log_error(f"{symbol}: Vedik astroloji analizi hatası: {e}, geleneksel analiz kullanılıyor")
            
            # Geleneksel astroloji analizi (fallback)
            return self._calculate_traditional_astrology_score(symbol, date)
            
        except Exception as e:
            log_error(f"{symbol} astroloji skoru hesaplanırken hata: {e}")
            return config.VEDIC_FALLBACK_SCORE
    
    def _calculate_traditional_astrology_score(self, symbol: str, date: datetime) -> float:
        """Geleneksel astroloji skoru hesapla (mevcut sistem)"""
        try:
            # Şirketin kuruluş tarihini al
            founding_date = self.founding_dates.get_founding_date(symbol)
            if founding_date:
                # String ise datetime'a çevir
                if isinstance(founding_date, str):
                    try:
                        founding_date = datetime.strptime(founding_date, '%Y-%m-%d')
                    except:
                        founding_date = None
                
                if founding_date:
                    company_age = (datetime.utcnow() - founding_date).days / 365.25
                else:
                    company_age = 0
            else:
                company_age = 0
            
            total_score = 0
            weight_count = 0
            
            # Mevcut gezegen konumları analizi
            current_score = self._calculate_current_astrology_score(date)
            total_score += current_score * 0.6  # Mevcut konumlar %60
            weight_count += 0.6
            
            # Kuruluş tarihi analizi (eğer biliniyorsa)
            if founding_date:
                founding_score = self._calculate_founding_astrology_score(founding_date)
                
                # Şirket yaşına göre ağırlık
                if company_age:
                    if company_age < 10:
                        founding_weight = 0.4  # Genç şirketler için kuruluş tarihi daha önemli
                    elif company_age < 25:
                        founding_weight = 0.3
                    else:
                        founding_weight = 0.2  # Eski şirketler için mevcut konumlar daha önemli
                else:
                    founding_weight = 0.3
                
                total_score += founding_score * founding_weight
                weight_count += founding_weight
                
                log_debug(f"{symbol}: Kuruluş skoru: {founding_score:.2f}, Mevcut skor: {current_score:.2f}")
            else:
                log_debug(f"{symbol}: Kuruluş tarihi bilinmiyor, sadece mevcut analiz kullanılıyor")
            
            # Normalize et
            if weight_count > 0:
                final_score = total_score / weight_count
            else:
                final_score = 50.0
            
            log_info(f"{symbol}: Geleneksel astroloji skoru: {final_score:.2f}")
            return round(max(0, min(100, final_score)), 2)
            
        except Exception as e:
            log_error(f"{symbol} geleneksel astroloji skoru hesaplanırken hata: {e}")
            return config.VEDIC_FALLBACK_SCORE
    
    def _calculate_current_astrology_score(self, date: datetime) -> float:
        """Mevcut gezegen konumlarından skor hesapla"""
        try:
            total_score = 0
            weight_count = 0
            
            # Mars-Jupiter açı analizi (ağırlık: 0.4)
            mars_jupiter_score = self.calculate_mars_jupiter_aspect(date)
            total_score += mars_jupiter_score * 0.4
            weight_count += 0.4
            
            # Ay fazı analizi (ağırlık: 0.3)
            moon_analysis = self.calculate_moon_phase_analysis(date)
            total_score += moon_analysis['score'] * 0.3
            weight_count += 0.3
            
            # Gezegen açıları analizi (ağırlık: 0.3)
            aspects = self.calculate_planetary_aspects(date)
            if aspects:
                avg_aspect_score = sum(aspects.values()) / len(aspects)
                total_score += avg_aspect_score * 0.3
                weight_count += 0.3
            
            # Normalize et
            if weight_count > 0:
                return total_score / weight_count
            else:
                return 50.0
                
        except Exception as e:
            log_error(f"Mevcut astroloji skoru hesaplanırken hata: {e}")
            return 50.0
    
    def _calculate_founding_astrology_score(self, founding_date) -> float:
        """Kuruluş tarihinden astrolojik skor hesapla"""
        try:
            from datetime import date as date_class
            if isinstance(founding_date, date_class):
                founding_datetime = datetime.combine(founding_date, datetime.min.time())
            else:
                founding_datetime = founding_date
            
            total_score = 0
            weight_count = 0
            
            # Kuruluş tarihindeki Mars-Jupiter açısı
            mars_jupiter_score = self.calculate_mars_jupiter_aspect(founding_datetime)
            total_score += mars_jupiter_score * 0.4
            weight_count += 0.4
            
            # Kuruluş tarihindeki Ay fazı
            moon_analysis = self.calculate_moon_phase_analysis(founding_datetime)
            total_score += moon_analysis['score'] * 0.3
            weight_count += 0.3
            
            # Kuruluş tarihindeki gezegen açıları
            aspects = self.calculate_planetary_aspects(founding_datetime)
            if aspects:
                avg_aspect_score = sum(aspects.values()) / len(aspects)
                total_score += avg_aspect_score * 0.3
                weight_count += 0.3
            
            # Normalize et
            if weight_count > 0:
                return total_score / weight_count
            else:
                return 50.0
                
        except Exception as e:
            log_error(f"Kuruluş astroloji skoru hesaplanırken hata: {e}")
            return 50.0
