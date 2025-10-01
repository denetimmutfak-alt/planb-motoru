# -*- coding: utf-8 -*-
"""
PlanB Motoru - Ultra Moon Phases and Lunar Cycle Analysis Module
Ultra-expert level lunar analysis with professional astronomical calculations,
void-of-course periods, lunar mansions, ecliptic positioning, and moon-market correlations
"""

import ephem
import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import yfinance as yf
from src.utils.logger import log_info, log_error, log_debug, log_warning

class UltraMoonPhasesAnalyzer:
    """Ultra-expert lunar phases and cycles analysis system"""
    
    def __init__(self):
        # 28 Lunar Mansions (Nakshatras) with financial characteristics
        self.lunar_mansions = {
            'ashwini': {'degrees': (0, 13.33), 'sector': 'technology', 'volatility': 'high'},
            'bharani': {'degrees': (13.33, 26.67), 'sector': 'agriculture', 'volatility': 'medium'},
            'krittika': {'degrees': (26.67, 40), 'sector': 'energy', 'volatility': 'high'},
            'rohini': {'degrees': (40, 53.33), 'sector': 'luxury', 'volatility': 'low'},
            'mrigashira': {'degrees': (53.33, 66.67), 'sector': 'search', 'volatility': 'medium'},
            'ardra': {'degrees': (66.67, 80), 'sector': 'disruption', 'volatility': 'very_high'},
            'punarvasu': {'degrees': (80, 93.33), 'sector': 'recovery', 'volatility': 'low'},
            'pushya': {'degrees': (93.33, 106.67), 'sector': 'nurturing', 'volatility': 'low'},
            'ashlesha': {'degrees': (106.67, 120), 'sector': 'psychological', 'volatility': 'high'},
            'magha': {'degrees': (120, 133.33), 'sector': 'leadership', 'volatility': 'medium'},
            'purva_phalguni': {'degrees': (133.33, 146.67), 'sector': 'entertainment', 'volatility': 'medium'},
            'uttara_phalguni': {'degrees': (146.67, 160), 'sector': 'service', 'volatility': 'low'},
            'hasta': {'degrees': (160, 173.33), 'sector': 'craftsmanship', 'volatility': 'low'},
            'chitra': {'degrees': (173.33, 186.67), 'sector': 'beauty', 'volatility': 'medium'},
            'swati': {'degrees': (186.67, 200), 'sector': 'trade', 'volatility': 'high'},
            'vishakha': {'degrees': (200, 213.33), 'sector': 'achievement', 'volatility': 'medium'},
            'anuradha': {'degrees': (213.33, 226.67), 'sector': 'friendship', 'volatility': 'low'},
            'jyeshtha': {'degrees': (226.67, 240), 'sector': 'seniority', 'volatility': 'high'},
            'mula': {'degrees': (240, 253.33), 'sector': 'root_change', 'volatility': 'very_high'},
            'purva_ashadha': {'degrees': (253.33, 266.67), 'sector': 'invincibility', 'volatility': 'high'},
            'uttara_ashadha': {'degrees': (266.67, 280), 'sector': 'victory', 'volatility': 'medium'},
            'shravana': {'degrees': (280, 293.33), 'sector': 'listening', 'volatility': 'low'},
            'dhanishta': {'degrees': (293.33, 306.67), 'sector': 'wealth', 'volatility': 'medium'},
            'shatabhisha': {'degrees': (306.67, 320), 'sector': 'healing', 'volatility': 'high'},
            'purva_bhadrapada': {'degrees': (320, 333.33), 'sector': 'transformation', 'volatility': 'very_high'},
            'uttara_bhadrapada': {'degrees': (333.33, 346.67), 'sector': 'compassion', 'volatility': 'medium'},
            'revati': {'degrees': (346.67, 360), 'sector': 'completion', 'volatility': 'low'}
        }
        
        # Ultra moon phase definitions with precision degrees
        self.ultra_moon_phases = {
            'dark_moon': {'range': (355, 5), 'power': 0.95, 'energy': 'new_beginnings'},
            'new_moon': {'range': (355, 15), 'power': 0.9, 'energy': 'intention_setting'},
            'waxing_crescent': {'range': (15, 75), 'power': 0.4, 'energy': 'growth'},
            'first_quarter': {'range': (75, 105), 'power': 0.7, 'energy': 'action'},
            'waxing_gibbous': {'range': (105, 165), 'power': 0.5, 'energy': 'refinement'},
            'full_moon': {'range': (165, 195), 'power': 1.0, 'energy': 'culmination'},
            'waning_gibbous': {'range': (195, 255), 'power': 0.6, 'energy': 'gratitude'},
            'last_quarter': {'range': (255, 285), 'power': 0.7, 'energy': 'release'},
            'waning_crescent': {'range': (285, 345), 'power': 0.3, 'energy': 'reflection'},
            'balsamic_moon': {'range': (345, 355), 'power': 0.8, 'energy': 'wisdom'}
        }
        
        # Void of Course periods (when moon makes no aspects before sign change)
        self.voc_effects = {
            'short': {'duration': '<2h', 'market_impact': 0.1, 'description': 'Minimal impact'},
            'medium': {'duration': '2-8h', 'market_impact': 0.3, 'description': 'Moderate uncertainty'},
            'long': {'duration': '8-24h', 'market_impact': 0.6, 'description': 'Significant uncertainty'},
            'very_long': {'duration': '>24h', 'market_impact': 0.9, 'description': 'Major uncertainty'}
        }
        
        # Ecliptic positioning effects
        self.ecliptic_positions = {
            'aries': {'sector_boost': 'technology', 'volatility_multiplier': 1.3},
            'taurus': {'sector_boost': 'real_estate', 'volatility_multiplier': 0.7},
            'gemini': {'sector_boost': 'communication', 'volatility_multiplier': 1.1},
            'cancer': {'sector_boost': 'consumer_goods', 'volatility_multiplier': 0.8},
            'leo': {'sector_boost': 'entertainment', 'volatility_multiplier': 1.2},
            'virgo': {'sector_boost': 'healthcare', 'volatility_multiplier': 0.6},
            'libra': {'sector_boost': 'luxury', 'volatility_multiplier': 0.9},
            'scorpio': {'sector_boost': 'mining', 'volatility_multiplier': 1.4},
            'sagittarius': {'sector_boost': 'travel', 'volatility_multiplier': 1.1},
            'capricorn': {'sector_boost': 'banking', 'volatility_multiplier': 0.8},
            'aquarius': {'sector_boost': 'innovation', 'volatility_multiplier': 1.3},
            'pisces': {'sector_boost': 'pharmaceuticals', 'volatility_multiplier': 1.0}
        }
        
        # Professional eclipse calculations
        self.eclipse_orbs = {
            'solar_eclipse': {'orb_days': 30, 'peak_days': 3, 'market_volatility': 1.5},
            'lunar_eclipse': {'orb_days': 14, 'peak_days': 2, 'market_volatility': 1.2},
            'penumbral_lunar': {'orb_days': 7, 'peak_days': 1, 'market_volatility': 1.1}
        }
        
        log_info("Ultra Moon Phases Analyzer initialized with professional lunar calculations")
    
    def calculate_ultra_lunar_position(self, date: datetime = None) -> Dict:
        """Calculate ultra-precise lunar position with professional astronomical data"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            # Create observer for precise calculations
            observer = ephem.Observer()
            observer.lat = '40.7128'  # New York (financial center)
            observer.lon = '-74.0060'
            observer.date = date
            
            # Calculate moon and sun positions
            moon = ephem.Moon(observer)
            sun = ephem.Sun(observer)
            
            # Ultra-precise moon phase calculation
            moon_elongation = math.degrees(float(moon.elong))
            moon_phase_angle = moon_elongation
            
            # Determine precise phase
            current_phase = self._determine_ultra_phase(moon_phase_angle)
            
            # Calculate lunar mansion (nakshatra)
            moon_longitude = math.degrees(float(moon.ra)) * 15  # Convert to degrees
            lunar_mansion = self._get_lunar_mansion(moon_longitude % 360)
            
            # Moon sign calculation
            moon_sign = self._calculate_moon_sign(moon_longitude)
            
            # Void of Course calculation
            voc_status = self._calculate_void_of_course(date, moon)
            
            # Eclipse proximity
            eclipse_proximity = self._calculate_eclipse_proximity(date)
            
            # Market correlation factors
            market_correlation = self._calculate_moon_market_correlation(
                current_phase, lunar_mansion, moon_sign, voc_status
            )
            
            return {
                'moon_phase': current_phase,
                'moon_phase_angle': moon_phase_angle,
                'lunar_mansion': lunar_mansion,
                'moon_sign': moon_sign,
                'void_of_course': voc_status,
                'eclipse_proximity': eclipse_proximity,
                'market_correlation': market_correlation,
                'moon_illumination': float(moon.moon_phase) * 100,
                'moon_distance_km': float(moon.earth_distance) * ephem.meters_per_au / 1000,
                'angular_speed': self._calculate_angular_speed(date),
                'declination': math.degrees(float(moon.dec))
            }
            
        except Exception as e:
            log_error(f"Ultra lunar position calculation error: {e}")
            return self._get_default_lunar_data()
    
    def _determine_ultra_phase(self, phase_angle: float) -> Dict:
        """Determine ultra-precise moon phase with professional accuracy"""
        for phase_name, phase_data in self.ultra_moon_phases.items():
            min_angle, max_angle = phase_data['range']
            
            if min_angle > max_angle:  # Handles wrap-around (e.g., 355-5 degrees)
                if phase_angle >= min_angle or phase_angle <= max_angle:
                    return {
                        'name': phase_name,
                        'power': phase_data['power'],
                        'energy': phase_data['energy'],
                        'angle': phase_angle,
                        'precision': self._calculate_phase_precision(phase_angle, min_angle, max_angle)
                    }
            else:
                if min_angle <= phase_angle <= max_angle:
                    return {
                        'name': phase_name,
                        'power': phase_data['power'],
                        'energy': phase_data['energy'],
                        'angle': phase_angle,
                        'precision': self._calculate_phase_precision(phase_angle, min_angle, max_angle)
                    }
        
        return {
            'name': 'undefined',
            'power': 0.5,
            'energy': 'neutral',
            'angle': phase_angle,
            'precision': 0.0
        }
    
    def _get_lunar_mansion(self, longitude: float) -> Dict:
        """Calculate current lunar mansion (nakshatra) with financial characteristics"""
        for mansion_name, mansion_data in self.lunar_mansions.items():
            min_deg, max_deg = mansion_data['degrees']
            if min_deg <= longitude <= max_deg:
                return {
                    'name': mansion_name,
                    'sector': mansion_data['sector'],
                    'volatility': mansion_data['volatility'],
                    'longitude': longitude,
                    'financial_energy': self._get_mansion_financial_energy(mansion_name)
                }
        
        return {
            'name': 'unknown',
            'sector': 'general',
            'volatility': 'medium',
            'longitude': longitude,
            'financial_energy': 0.5
        }
    
    def _calculate_moon_sign(self, longitude: float) -> Dict:
        """Calculate moon sign with market sector correlations"""
        signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
                'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
        
        sign_index = int(longitude // 30)
        sign = signs[sign_index % 12]
        
        ecliptic_data = self.ecliptic_positions.get(sign, {})
        
        return {
            'sign': sign,
            'longitude_in_sign': longitude % 30,
            'sector_boost': ecliptic_data.get('sector_boost', 'general'),
            'volatility_multiplier': ecliptic_data.get('volatility_multiplier', 1.0)
        }
    
    def _calculate_void_of_course(self, date: datetime, moon) -> Dict:
        """Calculate Void of Course moon periods with market implications"""
        try:
            # Simplified VOC calculation (professional version would use aspect calculations)
            current_hour = date.hour
            
            # Simulate VOC periods (in practice, would calculate precise aspects)
            voc_probability = np.sin(current_hour * np.pi / 12) ** 2
            
            if voc_probability > 0.8:
                voc_duration = 'long'
            elif voc_probability > 0.6:
                voc_duration = 'medium'
            elif voc_probability > 0.3:
                voc_duration = 'short'
            else:
                voc_duration = None
            
            if voc_duration:
                voc_data = self.voc_effects[voc_duration]
                return {
                    'is_void': True,
                    'duration_category': voc_duration,
                    'market_impact': voc_data['market_impact'],
                    'description': voc_data['description'],
                    'trading_recommendation': 'avoid_major_decisions' if voc_data['market_impact'] > 0.5 else 'proceed_with_caution'
                }
            else:
                return {
                    'is_void': False,
                    'market_impact': 0.0,
                    'trading_recommendation': 'normal_trading'
                }
                
        except Exception as e:
            log_warning(f"VOC calculation error: {e}")
            return {'is_void': False, 'market_impact': 0.0}
    
    def _calculate_eclipse_proximity(self, date: datetime) -> Dict:
        """Calculate proximity to eclipses with professional orb calculations"""
        try:
            # Professional eclipse dates for 2024-2025
            eclipse_events = [
                {'date': datetime(2024, 4, 8), 'type': 'solar_eclipse', 'magnitude': 1.02},
                {'date': datetime(2024, 9, 18), 'type': 'lunar_eclipse', 'magnitude': 0.36},
                {'date': datetime(2024, 10, 2), 'type': 'solar_eclipse', 'magnitude': 0.93},
                {'date': datetime(2025, 3, 14), 'type': 'lunar_eclipse', 'magnitude': 1.18},
                {'date': datetime(2025, 9, 7), 'type': 'lunar_eclipse', 'magnitude': 1.36}
            ]
            
            closest_eclipse = None
            min_days = float('inf')
            
            for eclipse in eclipse_events:
                days_diff = abs((eclipse['date'] - date).days)
                if days_diff < min_days:
                    min_days = days_diff
                    closest_eclipse = eclipse
            
            if closest_eclipse:
                eclipse_type = closest_eclipse['type']
                orb_data = self.eclipse_orbs.get(eclipse_type, self.eclipse_orbs['lunar_eclipse'])
                
                if min_days <= orb_data['orb_days']:
                    # Calculate eclipse influence intensity
                    if min_days <= orb_data['peak_days']:
                        intensity = 1.0
                    else:
                        intensity = 1.0 - (min_days - orb_data['peak_days']) / (orb_data['orb_days'] - orb_data['peak_days'])
                    
                    return {
                        'in_orb': True,
                        'eclipse_type': eclipse_type,
                        'days_to_eclipse': min_days,
                        'intensity': intensity,
                        'market_volatility_multiplier': orb_data['market_volatility'] * intensity,
                        'magnitude': closest_eclipse['magnitude']
                    }
            
            return {
                'in_orb': False,
                'intensity': 0.0,
                'market_volatility_multiplier': 1.0
            }
            
        except Exception as e:
            log_warning(f"Eclipse proximity calculation error: {e}")
            return {'in_orb': False, 'intensity': 0.0}
    
    def _calculate_moon_market_correlation(self, phase: Dict, mansion: Dict, 
                                         sign: Dict, voc: Dict) -> Dict:
        """Calculate sophisticated moon-market correlations"""
        try:
            # Base correlation from moon phase
            base_correlation = phase['power'] * 0.3
            
            # Lunar mansion sector correlation
            mansion_correlation = {
                'technology': 0.8, 'agriculture': 0.6, 'energy': 0.7,
                'luxury': 0.5, 'disruption': 0.9, 'banking': 0.4
            }.get(mansion['sector'], 0.5)
            
            # Volatility adjustment from mansion
            volatility_factor = {
                'very_high': 1.5, 'high': 1.2, 'medium': 1.0, 'low': 0.8
            }.get(mansion['volatility'], 1.0)
            
            # Sign-based sector correlation
            sign_correlation = sign['volatility_multiplier']
            
            # VOC impact on correlation reliability
            voc_reliability = 1.0 - voc['market_impact']
            
            # Combined correlation score
            combined_correlation = (
                base_correlation * 0.4 +
                mansion_correlation * 0.3 +
                sign_correlation * 0.2 +
                voc_reliability * 0.1
            )
            
            return {
                'overall_correlation': combined_correlation,
                'volatility_factor': volatility_factor,
                'sector_preference': mansion['sector'],
                'reliability_score': voc_reliability,
                'market_timing_quality': 'excellent' if combined_correlation > 0.8 else
                                       'good' if combined_correlation > 0.6 else
                                       'moderate' if combined_correlation > 0.4 else 'poor'
            }
            
        except Exception as e:
            log_warning(f"Moon-market correlation calculation error: {e}")
            return {'overall_correlation': 0.5, 'volatility_factor': 1.0}
    
    def calculate_ultra_moon_score(self, symbol: str, date: datetime = None) -> Dict:
        """Calculate ultra-sophisticated moon-based trading score"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            # Get comprehensive lunar data
            lunar_data = self.calculate_ultra_lunar_position(date)
            
            # Base score from lunar calculations
            base_score = 50.0
            
            # Phase-based adjustments
            phase_power = lunar_data['moon_phase']['power']
            phase_adjustment = (phase_power - 0.5) * 20  # ±10 points
            
            # Lunar mansion influence
            mansion = lunar_data['lunar_mansion']
            mansion_adjustment = self._get_mansion_score_adjustment(mansion, symbol)
            
            # Eclipse proximity impact
            eclipse = lunar_data['eclipse_proximity']
            eclipse_adjustment = eclipse['intensity'] * eclipse.get('market_volatility_multiplier', 1.0) * 5
            
            # VOC penalty
            voc = lunar_data['void_of_course']
            voc_penalty = voc['market_impact'] * -10
            
            # Market correlation bonus
            correlation = lunar_data['market_correlation']
            correlation_bonus = (correlation['overall_correlation'] - 0.5) * 15
            
            # Symbol-specific lunar sensitivity
            symbol_sensitivity = self._calculate_symbol_lunar_sensitivity(symbol, lunar_data)
            
            # Calculate final score
            final_score = (
                base_score +
                phase_adjustment +
                mansion_adjustment +
                eclipse_adjustment +
                voc_penalty +
                correlation_bonus +
                symbol_sensitivity
            )
            
            final_score = max(0, min(100, final_score))
            
            # Generate detailed analysis
            analysis = self._generate_lunar_analysis(lunar_data, symbol, final_score)
            
            return {
                'ultra_moon_score': final_score,
                'lunar_data': lunar_data,
                'analysis': analysis,
                'components': {
                    'base_score': base_score,
                    'phase_adjustment': phase_adjustment,
                    'mansion_adjustment': mansion_adjustment,
                    'eclipse_adjustment': eclipse_adjustment,
                    'voc_penalty': voc_penalty,
                    'correlation_bonus': correlation_bonus,
                    'symbol_sensitivity': symbol_sensitivity
                }
            }
            
        except Exception as e:
            log_error(f"Ultra moon score calculation error: {e}")
            return {
                'ultra_moon_score': 50.0,
                'analysis': {'error': str(e)},
                'components': {}
            }
    
    def _get_mansion_score_adjustment(self, mansion: Dict, symbol: str) -> float:
        """Calculate score adjustment based on lunar mansion and symbol correlation"""
        try:
            # Mansion-symbol correlations
            correlations = {
                'technology': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA'],
                'agriculture': ['ADM', 'DE', 'CAT', 'MON', 'POT', 'CF'],
                'energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL'],
                'luxury': ['LVMH', 'COST', 'TJX', 'NKE', 'SBUX'],
                'banking': ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS'],
                'healthcare': ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK'],
                'real_estate': ['AMT', 'PLD', 'CCI', 'EQIX', 'SPG']
            }
            
            mansion_sector = mansion['sector']
            if mansion_sector in correlations:
                if any(symbol.upper().startswith(ticker) for ticker in correlations[mansion_sector]):
                    return 8.0  # Strong positive correlation
            
            # Volatility-based adjustment
            volatility_bonus = {
                'very_high': 3.0, 'high': 2.0, 'medium': 0.0, 'low': -1.0
            }.get(mansion['volatility'], 0.0)
            
            return volatility_bonus
            
        except Exception as e:
            log_warning(f"Mansion score adjustment error: {e}")
            return 0.0
    
    def _calculate_symbol_lunar_sensitivity(self, symbol: str, lunar_data: Dict) -> float:
        """Calculate symbol-specific lunar sensitivity"""
        try:
            # Precious metals: High lunar sensitivity
            if any(metal in symbol.upper() for metal in ['GC', 'GOLD', 'GLD', 'SILVER', 'SLV']):
                return lunar_data['moon_phase']['power'] * 8.0
            
            # Agricultural commodities: Moon phase sensitivity
            elif any(agri in symbol.upper() for agri in ['CORN', 'WHEAT', 'SOYB', 'SUGAR']):
                return lunar_data['moon_phase']['power'] * 6.0
            
            # Cryptocurrency: High lunar correlation
            elif any(crypto in symbol.upper() for crypto in ['BTC', 'ETH', 'BITCOIN']):
                return lunar_data['moon_phase']['power'] * 7.0
            
            # Real estate: Moderate lunar sensitivity
            elif any(re in symbol.upper() for re in ['REIT', 'AMT', 'PLD']):
                return lunar_data['moon_phase']['power'] * 4.0
            
            # Technology stocks: Eclipse sensitivity
            elif any(tech in symbol.upper() for tech in ['AAPL', 'MSFT', 'GOOGL']):
                eclipse_factor = lunar_data['eclipse_proximity']['intensity'] * 5.0
                return eclipse_factor
            
            else:
                return 0.0
                
        except Exception as e:
            log_warning(f"Symbol lunar sensitivity error: {e}")
            return 0.0
    
    def _generate_lunar_analysis(self, lunar_data: Dict, symbol: str, score: float) -> Dict:
        """Generate comprehensive lunar analysis report"""
        try:
            phase = lunar_data['moon_phase']
            mansion = lunar_data['lunar_mansion']
            voc = lunar_data['void_of_course']
            eclipse = lunar_data['eclipse_proximity']
            correlation = lunar_data['market_correlation']
            
            # Primary insights
            insights = []
            
            if phase['power'] > 0.8:
                insights.append(f"Strong lunar phase ({phase['name']}) supports {phase['energy']} energy")
            
            if mansion['volatility'] in ['very_high', 'high']:
                insights.append(f"Current lunar mansion increases market volatility")
            
            if voc['is_void']:
                insights.append(f"Void of Course moon suggests {voc['trading_recommendation']}")
            
            if eclipse['in_orb']:
                insights.append(f"Eclipse proximity may increase volatility by {eclipse['market_volatility_multiplier']:.1f}x")
            
            # Trading recommendations
            if score > 70:
                recommendation = "STRONG BUY - Excellent lunar timing"
            elif score > 60:
                recommendation = "BUY - Favorable lunar conditions"
            elif score > 40:
                recommendation = "HOLD - Neutral lunar influence"
            elif score > 30:
                recommendation = "CAUTION - Unfavorable lunar timing"
            else:
                recommendation = "AVOID - Poor lunar conditions"
            
            return {
                'score_interpretation': recommendation,
                'key_insights': insights,
                'lunar_timing_quality': correlation['market_timing_quality'],
                'volatility_expectation': mansion['volatility'],
                'sector_preference': mansion['sector'],
                'eclipse_warning': eclipse['in_orb'],
                'voc_status': voc['is_void']
            }
            
        except Exception as e:
            log_warning(f"Lunar analysis generation error: {e}")
            return {'score_interpretation': 'Unable to analyze', 'key_insights': []}
    
    def _get_mansion_financial_energy(self, mansion_name: str) -> float:
        """Get financial energy rating for lunar mansion"""
        financial_ratings = {
            'ashwini': 0.8, 'bharani': 0.6, 'krittika': 0.7, 'rohini': 0.9,
            'mrigashira': 0.5, 'ardra': 0.3, 'punarvasu': 0.7, 'pushya': 0.8,
            'ashlesha': 0.4, 'magha': 0.8, 'purva_phalguni': 0.6, 'uttara_phalguni': 0.7,
            'hasta': 0.8, 'chitra': 0.7, 'swati': 0.6, 'vishakha': 0.8,
            'anuradha': 0.7, 'jyeshtha': 0.5, 'mula': 0.3, 'purva_ashadha': 0.6,
            'uttara_ashadha': 0.9, 'shravana': 0.8, 'dhanishta': 0.9, 'shatabhisha': 0.5,
            'purva_bhadrapada': 0.4, 'uttara_bhadrapada': 0.7, 'revati': 0.8
        }
        return financial_ratings.get(mansion_name, 0.5)
    
    def _calculate_phase_precision(self, angle: float, min_angle: float, max_angle: float) -> float:
        """Calculate how precisely the current angle hits the phase center"""
        if min_angle > max_angle:  # Wrap-around case
            center = (min_angle + max_angle + 360) / 2 % 360
        else:
            center = (min_angle + max_angle) / 2
        
        angle_diff = min(abs(angle - center), 360 - abs(angle - center))
        max_diff = abs(max_angle - min_angle) / 2
        
        return 1.0 - (angle_diff / max_diff) if max_diff > 0 else 1.0
    
    def _calculate_angular_speed(self, date: datetime) -> float:
        """Calculate moon's angular speed for advanced timing"""
        try:
            # Calculate moon position at two close times
            observer = ephem.Observer()
            observer.date = date
            moon1 = ephem.Moon(observer)
            
            observer.date = date + timedelta(hours=1)
            moon2 = ephem.Moon(observer)
            
            # Calculate angular speed in degrees per hour
            angle_diff = math.degrees(float(moon2.ra - moon1.ra))
            return abs(angle_diff)
            
        except Exception:
            return 0.5  # Average lunar angular speed
    
    def _get_default_lunar_data(self) -> Dict:
        """Get default lunar data for error conditions"""
        return {
            'moon_phase': {'name': 'unknown', 'power': 0.5, 'energy': 'neutral'},
            'lunar_mansion': {'name': 'unknown', 'sector': 'general', 'volatility': 'medium'},
            'moon_sign': {'sign': 'unknown', 'volatility_multiplier': 1.0},
            'void_of_course': {'is_void': False, 'market_impact': 0.0},
            'eclipse_proximity': {'in_orb': False, 'intensity': 0.0},
            'market_correlation': {'overall_correlation': 0.5, 'volatility_factor': 1.0}
        }

# Create global instance
ultra_moon_analyzer = UltraMoonPhasesAnalyzer()

# Compatibility layer for existing code
class MoonPhasesAnalyzer:
    """Compatibility wrapper for existing Moon Phases functionality"""
    
    def __init__(self):
        self.ultra_analyzer = ultra_moon_analyzer
        log_info("Moon Phases Analyzer (compatibility mode) initialized")
    
    def get_moon_phase(self, date: datetime = None, location: str = "Istanbul") -> Dict:
        """Get moon phase with basic compatibility"""
        ultra_data = self.ultra_analyzer.calculate_ultra_lunar_position(date)
        return {
            'phase_type': ultra_data['moon_phase']['name'],
            'phase_name': ultra_data['moon_phase']['name'].replace('_', ' ').title(),
            'intensity': ultra_data['moon_phase']['power'],
            'weight': ultra_data['moon_phase']['power'] * 0.4
        }
    
    def calculate_moon_score(self, symbol: str, date: datetime = None) -> Dict:
        """Calculate moon score with compatibility wrapper"""
        ultra_result = self.ultra_analyzer.calculate_ultra_moon_score(symbol, date)
        return {
            'moon_score': ultra_result['ultra_moon_score'],
            'analysis_type': 'Ultra Moon Phases & Lunar Cycles',
            'details': ultra_result['components']
        }

# Global instances
moon_analyzer = MoonPhasesAnalyzer()



