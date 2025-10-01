"""
Ultra Vedic Astrology Analysis - Professional Grade
Sofistike Vedik astroloji analizi modülü
"""

import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np

from src.utils.logger import log_info, log_warning, log_error, log_debug


@dataclass
class VedicPlanet:
    """Vedik gezegen bilgisi"""
    name: str
    degree: float
    rashi: str
    nakshatra: str
    nakshatra_lord: str
    is_retrograde: bool = False


@dataclass
class VedicChart:
    """Vedik doğum haritası"""
    lagna: str
    planets: Dict[str, VedicPlanet]
    dasha_lord: str
    dasha_period: str
    current_transits: Dict[str, str]


class UltraVedicAnalyzer:
    """Ultra-advanced Vedic astrology analysis for financial markets"""
    
    def __init__(self):
        # Enhanced 27 Nakshatras with precise degrees and financial characteristics
        self.nakshatras = {
            'Ashwini': {'start': 0.0, 'lord': 'Ketu', 'nature': 'swift', 'finance_impact': 'volatile_gains'},
            'Bharani': {'start': 13.33, 'lord': 'Venus', 'nature': 'transformative', 'finance_impact': 'deep_value'},
            'Krittika': {'start': 26.67, 'lord': 'Sun', 'nature': 'cutting', 'finance_impact': 'sharp_moves'},
            'Rohini': {'start': 40.0, 'lord': 'Moon', 'nature': 'growth', 'finance_impact': 'steady_bull'},
            'Mrigashira': {'start': 53.33, 'lord': 'Mars', 'nature': 'searching', 'finance_impact': 'discovery_phase'},
            'Ardra': {'start': 66.67, 'lord': 'Rahu', 'nature': 'stormy', 'finance_impact': 'disruption'},
            'Punarvasu': {'start': 80.0, 'lord': 'Jupiter', 'nature': 'renewal', 'finance_impact': 'recovery'},
            'Pushya': {'start': 93.33, 'lord': 'Saturn', 'nature': 'nourishing', 'finance_impact': 'safe_growth'},
            'Ashlesha': {'start': 106.67, 'lord': 'Mercury', 'nature': 'embracing', 'finance_impact': 'tight_control'},
            'Magha': {'start': 120.0, 'lord': 'Ketu', 'nature': 'royal', 'finance_impact': 'leadership_premium'},
            'Purva Phalguni': {'start': 133.33, 'lord': 'Venus', 'nature': 'enjoyment', 'finance_impact': 'luxury_gains'},
            'Uttara Phalguni': {'start': 146.67, 'lord': 'Sun', 'nature': 'patronage', 'finance_impact': 'institutional_support'},
            'Hasta': {'start': 160.0, 'lord': 'Moon', 'nature': 'skillful', 'finance_impact': 'crafted_value'},
            'Chitra': {'start': 173.33, 'lord': 'Mars', 'nature': 'brilliant', 'finance_impact': 'breakthrough_gains'},
            'Swati': {'start': 186.67, 'lord': 'Rahu', 'nature': 'independent', 'finance_impact': 'autonomous_growth'},
            'Vishakha': {'start': 200.0, 'lord': 'Jupiter', 'nature': 'forked', 'finance_impact': 'choice_driven'},
            'Anuradha': {'start': 213.33, 'lord': 'Saturn', 'nature': 'devotional', 'finance_impact': 'loyal_returns'},
            'Jyeshtha': {'start': 226.67, 'lord': 'Mercury', 'nature': 'elder', 'finance_impact': 'mature_strength'},
            'Mula': {'start': 240.0, 'lord': 'Ketu', 'nature': 'root', 'finance_impact': 'fundamental_shift'},
            'Purva Ashadha': {'start': 253.33, 'lord': 'Venus', 'nature': 'invincible', 'finance_impact': 'unstoppable_rise'},
            'Uttara Ashadha': {'start': 266.67, 'lord': 'Sun', 'nature': 'victory', 'finance_impact': 'ultimate_success'},
            'Shravana': {'start': 280.0, 'lord': 'Moon', 'nature': 'listening', 'finance_impact': 'information_edge'},
            'Dhanishtha': {'start': 293.33, 'lord': 'Mars', 'nature': 'wealthy', 'finance_impact': 'prosperity'},
            'Shatabhisha': {'start': 306.67, 'lord': 'Rahu', 'nature': 'healing', 'finance_impact': 'corrective_action'},
            'Purva Bhadrapada': {'start': 320.0, 'lord': 'Jupiter', 'nature': 'burning', 'finance_impact': 'intense_transformation'},
            'Uttara Bhadrapada': {'start': 333.33, 'lord': 'Saturn', 'nature': 'depth', 'finance_impact': 'deep_value_creation'},
            'Revati': {'start': 346.67, 'lord': 'Mercury', 'nature': 'wealthy', 'finance_impact': 'wealth_accumulation'}
        }
        
        # Enhanced Rashis (signs) with financial characteristics
        self.rashis = {
            'Mesha': {'element': 'fire', 'nature': 'cardinal', 'finance_impact': 'aggressive_growth', 'strength': 85},
            'Vrishabha': {'element': 'earth', 'nature': 'fixed', 'finance_impact': 'stable_value', 'strength': 90},
            'Mithuna': {'element': 'air', 'nature': 'mutable', 'finance_impact': 'information_driven', 'strength': 70},
            'Karka': {'element': 'water', 'nature': 'cardinal', 'finance_impact': 'emotional_swings', 'strength': 75},
            'Simha': {'element': 'fire', 'nature': 'fixed', 'finance_impact': 'royal_premium', 'strength': 95},
            'Kanya': {'element': 'earth', 'nature': 'mutable', 'finance_impact': 'analytical_precision', 'strength': 80},
            'Tula': {'element': 'air', 'nature': 'cardinal', 'finance_impact': 'balanced_growth', 'strength': 85},
            'Vrishchika': {'element': 'water', 'nature': 'fixed', 'finance_impact': 'transformative_gains', 'strength': 88},
            'Dhanu': {'element': 'fire', 'nature': 'mutable', 'finance_impact': 'expansive_vision', 'strength': 82},
            'Makara': {'element': 'earth', 'nature': 'cardinal', 'finance_impact': 'long_term_build', 'strength': 92},
            'Kumbha': {'element': 'air', 'nature': 'fixed', 'finance_impact': 'innovative_disruption', 'strength': 78},
            'Meena': {'element': 'water', 'nature': 'mutable', 'finance_impact': 'intuitive_gains', 'strength': 76}
        }
        
        # Enhanced Dasha system with financial implications
        self.dasha_system = {
            'Ketu': {'years': 7, 'finance_nature': 'detachment_profits', 'volatility': 'high'},
            'Venus': {'years': 20, 'finance_nature': 'luxury_growth', 'volatility': 'low'},
            'Sun': {'years': 6, 'finance_nature': 'leadership_gains', 'volatility': 'medium'},
            'Moon': {'years': 10, 'finance_nature': 'emotional_cycles', 'volatility': 'high'},
            'Mars': {'years': 7, 'finance_nature': 'aggressive_expansion', 'volatility': 'very_high'},
            'Rahu': {'years': 18, 'finance_nature': 'sudden_changes', 'volatility': 'extreme'},
            'Jupiter': {'years': 16, 'finance_nature': 'wisdom_wealth', 'volatility': 'low'},
            'Saturn': {'years': 19, 'finance_nature': 'slow_steady_build', 'volatility': 'low'},
            'Mercury': {'years': 17, 'finance_nature': 'intelligent_trades', 'volatility': 'medium'}
        }
        
        # Planetary dignities and debilities for financial strength
        self.planetary_strengths = {
            'Sun': {'exalted': 'Mesha', 'own': ['Simha'], 'debilitated': 'Tula', 'finance_power': 85},
            'Moon': {'exalted': 'Vrishabha', 'own': ['Karka'], 'debilitated': 'Vrishchika', 'finance_power': 75},
            'Mars': {'exalted': 'Makara', 'own': ['Mesha', 'Vrishchika'], 'debilitated': 'Karka', 'finance_power': 80},
            'Mercury': {'exalted': 'Kanya', 'own': ['Mithuna', 'Kanya'], 'debilitated': 'Meena', 'finance_power': 82},
            'Jupiter': {'exalted': 'Karka', 'own': ['Dhanu', 'Meena'], 'debilitated': 'Makara', 'finance_power': 90},
            'Venus': {'exalted': 'Meena', 'own': ['Vrishabha', 'Tula'], 'debilitated': 'Kanya', 'finance_power': 88},
            'Saturn': {'exalted': 'Tula', 'own': ['Makara', 'Kumbha'], 'debilitated': 'Mesha', 'finance_power': 78},
            'Rahu': {'exalted': 'Mithuna', 'own': [], 'debilitated': 'Dhanu', 'finance_power': 70},
            'Ketu': {'exalted': 'Dhanu', 'own': [], 'debilitated': 'Mithuna', 'finance_power': 65}
        }
        
        # Advanced yoga combinations for financial success
        self.wealth_yogas = {
            'Dhana_Yoga': 'Wealth combination',
            'Lakshmi_Yoga': 'Prosperity blessing',
            'Kubera_Yoga': 'Lord of wealth favor',
            'Chandra_Mangal_Yoga': 'Moon-Mars wealth',
            'Gaja_Kesari_Yoga': 'Elephant-Lion power',
            'Raj_Yoga': 'Royal combination',
            'Dhan_Yoga': 'Direct wealth yoga',
            'Viparita_Raja_Yoga': 'Reversal fortune'
        }
        
    def analyze_vedic_astrology(self, symbol, stock_data, founding_date=None):
        """Comprehensive Vedic astrology analysis for financial markets"""
        try:
            if founding_date is None:
                # Use a default date based on symbol characteristics
                founding_date = self._estimate_founding_date(symbol)
            
            current_date = datetime.now()
            
            # Calculate natal chart
            natal_chart = self._calculate_natal_chart(founding_date)
            
            # Current planetary positions
            current_positions = self._calculate_current_positions(current_date)
            
            # Dasha analysis
            dasha_analysis = self._analyze_dasha_periods(founding_date, current_date)
            
            # Transit analysis
            transit_analysis = self._analyze_transits(natal_chart, current_positions)
            
            # Nakshatra analysis
            nakshatra_analysis = self._analyze_nakshatras(natal_chart, current_positions)
            
            # Yoga combinations
            yoga_analysis = self._analyze_yogas(natal_chart)
            
            # Divisional chart analysis (simplified)
            divisional_analysis = self._analyze_divisional_charts(natal_chart)
            
            # Timing analysis
            timing_analysis = self._analyze_timing(dasha_analysis, transit_analysis)
            
            # Calculate final Vedic score
            final_score = self._calculate_vedic_score(
                natal_chart, dasha_analysis, transit_analysis,
                nakshatra_analysis, yoga_analysis, timing_analysis
            )
            
            return {
                'vedic_score': final_score,
                'natal_chart': natal_chart,
                'dasha_analysis': dasha_analysis,
                'transit_analysis': transit_analysis,
                'nakshatra_analysis': nakshatra_analysis,
                'yoga_analysis': yoga_analysis,
                'timing_analysis': timing_analysis,
                'current_positions': current_positions
            }
            
        except Exception as e:
            log_error(f"Vedic astrology analysis error for {symbol}: {e}")
            return self._default_score()
    
    def _estimate_founding_date(self, symbol):
        """Estimate founding date based on symbol characteristics"""
        try:
            # Simple hash-based date generation for consistency
            hash_value = abs(hash(symbol)) % 10000
            
            # Generate a date between 1980-2020
            base_year = 1980 + (hash_value % 40)
            base_month = 1 + (hash_value % 12)
            base_day = 1 + (hash_value % 28)
            
            return datetime(base_year, base_month, base_day)
            
        except:
            return datetime(2000, 1, 1)  # Default fallback
    
    def _calculate_natal_chart(self, founding_date):
        """Calculate natal chart positions"""
        try:
            # Simplified planetary calculations (in a real system, use Swiss Ephemeris)
            chart = {}
            
            # Calculate Julian day for more accurate positioning
            julian_day = self._to_julian_day(founding_date)
            
            # Simplified planetary positions based on orbital periods
            planetary_periods = {
                'Sun': 365.25,
                'Moon': 27.32,
                'Mars': 686.98,
                'Mercury': 87.97,
                'Jupiter': 4332.59,
                'Venus': 224.70,
                'Saturn': 10759.22,
                'Rahu': 6798.38,  # Nodal period
                'Ketu': 6798.38   # Nodal period
            }
            
            for planet, period in planetary_periods.items():
                # Calculate position based on orbital period
                position = (julian_day * 360 / period) % 360
                
                # Add some variation for different planets
                if planet == 'Moon':
                    position = (position + 45) % 360
                elif planet == 'Mars':
                    position = (position + 90) % 360
                elif planet == 'Mercury':
                    position = (position + 30) % 360
                elif planet == 'Jupiter':
                    position = (position + 180) % 360
                elif planet == 'Venus':
                    position = (position + 60) % 360
                elif planet == 'Saturn':
                    position = (position + 270) % 360
                elif planet == 'Rahu':
                    position = (360 - position) % 360  # Rahu moves backward
                elif planet == 'Ketu':
                    position = (180 + (360 - position)) % 360  # Ketu opposite Rahu
                
                rashi = self._get_rashi_from_degree(position)
                nakshatra = self._get_nakshatra_from_degree(position)
                
                chart[planet] = {
                    'degree': position,
                    'rashi': rashi,
                    'nakshatra': nakshatra,
                    'strength': self._calculate_planetary_strength(planet, rashi)
                }
            
            # Calculate Ascendant (simplified)
            ascendant_degree = (chart['Sun']['degree'] + 90) % 360
            chart['Ascendant'] = {
                'degree': ascendant_degree,
                'rashi': self._get_rashi_from_degree(ascendant_degree),
                'nakshatra': self._get_nakshatra_from_degree(ascendant_degree),
                'strength': 85
            }
            
            return chart
            
        except Exception as e:
            log_debug(f"Natal chart calculation error: {e}")
            return {}
    
    def _calculate_current_positions(self, current_date):
        """Calculate current planetary positions"""
        try:
            # Use the same method as natal chart but for current date
            return self._calculate_natal_chart(current_date)
        except:
            return {}
    
    def _analyze_dasha_periods(self, founding_date, current_date):
        """Analyze Vimshottari Dasha periods"""
        try:
            # Calculate years since founding
            years_elapsed = (current_date - founding_date).days / 365.25
            
            # Find current Mahadasha
            total_cycle = 120  # Total Vimshottari cycle
            cycle_position = years_elapsed % total_cycle
            
            # Determine current Mahadasha
            cumulative_years = 0
            current_mahadasha = 'Ketu'  # Starting with Ketu
            
            dasha_sequence = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
            
            for dasha_lord in dasha_sequence:
                dasha_years = self.dasha_system[dasha_lord]['years']
                if cycle_position <= cumulative_years + dasha_years:
                    current_mahadasha = dasha_lord
                    years_into_dasha = cycle_position - cumulative_years
                    years_remaining = dasha_years - years_into_dasha
                    break
                cumulative_years += dasha_years
            
            # Calculate Antardasha (simplified)
            antardasha_position = (years_into_dasha / dasha_years) * 100
            current_antardasha = dasha_sequence[int(antardasha_position / 11.11) % len(dasha_sequence)]
            
            # Dasha strength based on planet's natal strength and current nature
            dasha_strength = self._calculate_dasha_strength(current_mahadasha, current_antardasha)
            
            return {
                'mahadasha': current_mahadasha,
                'antardasha': current_antardasha,
                'years_into_dasha': years_into_dasha,
                'years_remaining': years_remaining,
                'dasha_strength': dasha_strength,
                'financial_nature': self.dasha_system[current_mahadasha]['finance_nature'],
                'volatility_level': self.dasha_system[current_mahadasha]['volatility']
            }
            
        except Exception as e:
            log_debug(f"Dasha analysis error: {e}")
            return {
                'mahadasha': 'Jupiter',
                'antardasha': 'Venus',
                'dasha_strength': 65,
                'financial_nature': 'wisdom_wealth',
                'volatility_level': 'low'
            }
    
    def _analyze_transits(self, natal_chart, current_positions):
        """Analyze planetary transits"""
        try:
            transit_effects = {}
            total_transit_strength = 0
            
            for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
                if planet in natal_chart and planet in current_positions:
                    natal_pos = natal_chart[planet]['degree']
                    current_pos = current_positions[planet]['degree']
                    
                    # Calculate aspect between natal and current position
                    aspect_angle = abs(current_pos - natal_pos)
                    if aspect_angle > 180:
                        aspect_angle = 360 - aspect_angle
                    
                    # Determine aspect type
                    aspect_type = self._get_aspect_type(aspect_angle)
                    
                    # Calculate transit strength
                    transit_strength = self._calculate_transit_strength(planet, aspect_type)
                    
                    transit_effects[planet] = {
                        'aspect_type': aspect_type,
                        'aspect_angle': aspect_angle,
                        'transit_strength': transit_strength,
                        'current_rashi': current_positions[planet]['rashi'],
                        'current_nakshatra': current_positions[planet]['nakshatra']
                    }
                    
                    total_transit_strength += transit_strength
            
            avg_transit_strength = total_transit_strength / len(transit_effects) if transit_effects else 50
            
            # Special emphasis on Jupiter and Saturn transits
            jupiter_emphasis = self._analyze_jupiter_transit(natal_chart, current_positions)
            saturn_emphasis = self._analyze_saturn_transit(natal_chart, current_positions)
            
            return {
                'transit_effects': transit_effects,
                'average_transit_strength': avg_transit_strength,
                'jupiter_emphasis': jupiter_emphasis,
                'saturn_emphasis': saturn_emphasis,
                'overall_transit_nature': self._determine_transit_nature(avg_transit_strength)
            }
            
        except Exception as e:
            log_debug(f"Transit analysis error: {e}")
            return {
                'average_transit_strength': 50,
                'overall_transit_nature': 'neutral'
            }
    
    def _analyze_nakshatras(self, natal_chart, current_positions):
        """Advanced Nakshatra analysis"""
        try:
            nakshatra_effects = {}
            
            # Analyze key planets in nakshatras
            key_planets = ['Sun', 'Moon', 'Ascendant', 'Jupiter', 'Venus']
            
            for planet in key_planets:
                if planet in natal_chart:
                    nakshatra_name = natal_chart[planet]['nakshatra']
                    if nakshatra_name in self.nakshatras:
                        nakshatra_info = self.nakshatras[nakshatra_name]
                        
                        # Financial impact based on nakshatra
                        financial_impact = self._evaluate_nakshatra_finance_impact(
                            nakshatra_info['finance_impact'],
                            nakshatra_info['lord']
                        )
                        
                        nakshatra_effects[planet] = {
                            'nakshatra': nakshatra_name,
                            'lord': nakshatra_info['lord'],
                            'nature': nakshatra_info['nature'],
                            'financial_impact': financial_impact,
                            'strength': self._calculate_nakshatra_strength(nakshatra_name)
                        }
            
            # Current Moon nakshatra (important for timing)
            current_moon_nakshatra = None
            if 'Moon' in current_positions:
                current_moon_nakshatra = current_positions['Moon']['nakshatra']
            
            return {
                'natal_nakshatra_effects': nakshatra_effects,
                'current_moon_nakshatra': current_moon_nakshatra,
                'nakshatra_compatibility': self._analyze_nakshatra_compatibility(nakshatra_effects)
            }
            
        except Exception as e:
            log_debug(f"Nakshatra analysis error: {e}")
            return {'natal_nakshatra_effects': {}}
    
    def _analyze_yogas(self, natal_chart):
        """Analyze wealth and success yogas"""
        try:
            detected_yogas = []
            yoga_strength = 0
            
            # Check for various wealth yogas
            
            # 1. Dhana Yoga - Money house lords in good positions
            dhana_yoga_strength = self._check_dhana_yoga(natal_chart)
            if dhana_yoga_strength > 60:
                detected_yogas.append('Dhana_Yoga')
                yoga_strength += dhana_yoga_strength
            
            # 2. Lakshmi Yoga - Venus in good position
            if 'Venus' in natal_chart:
                venus_strength = natal_chart['Venus']['strength']
                if venus_strength > 80:
                    detected_yogas.append('Lakshmi_Yoga')
                    yoga_strength += venus_strength
            
            # 3. Gaja Kesari Yoga - Jupiter and Moon in good relation
            if 'Jupiter' in natal_chart and 'Moon' in natal_chart:
                jupiter_moon_angle = abs(natal_chart['Jupiter']['degree'] - natal_chart['Moon']['degree'])
                if jupiter_moon_angle < 60 or jupiter_moon_angle > 300:  # Angular relationship
                    detected_yogas.append('Gaja_Kesari_Yoga')
                    yoga_strength += 75
            
            # 4. Raj Yoga - Combination of angular and trinal lords
            raj_yoga_strength = self._check_raj_yoga(natal_chart)
            if raj_yoga_strength > 70:
                detected_yogas.append('Raj_Yoga')
                yoga_strength += raj_yoga_strength
            
            # 5. Chandra Mangal Yoga - Moon and Mars together
            if 'Moon' in natal_chart and 'Mars' in natal_chart:
                moon_mars_angle = abs(natal_chart['Moon']['degree'] - natal_chart['Mars']['degree'])
                if moon_mars_angle < 30:  # Conjunction
                    detected_yogas.append('Chandra_Mangal_Yoga')
                    yoga_strength += 65
            
            avg_yoga_strength = yoga_strength / len(detected_yogas) if detected_yogas else 50
            
            return {
                'detected_yogas': detected_yogas,
                'yoga_count': len(detected_yogas),
                'average_yoga_strength': avg_yoga_strength,
                'total_yoga_power': min(100, yoga_strength / 2)  # Normalized
            }
            
        except Exception as e:
            log_debug(f"Yoga analysis error: {e}")
            return {
                'detected_yogas': [],
                'yoga_count': 0,
                'average_yoga_strength': 50,
                'total_yoga_power': 50
            }
    
    def _analyze_divisional_charts(self, natal_chart):
        """Simplified divisional chart analysis"""
        try:
            # D9 (Navamsha) - Strength and fortune
            navamsha_strength = self._calculate_navamsha_strength(natal_chart)
            
            # D10 (Dasamsha) - Career and status
            dasamsha_strength = self._calculate_dasamsha_strength(natal_chart)
            
            # D2 (Hora) - Wealth
            hora_strength = self._calculate_hora_strength(natal_chart)
            
            return {
                'navamsha_strength': navamsha_strength,
                'dasamsha_strength': dasamsha_strength,
                'hora_strength': hora_strength,
                'overall_divisional_strength': (navamsha_strength + dasamsha_strength + hora_strength) / 3
            }
            
        except Exception as e:
            log_debug(f"Divisional chart analysis error: {e}")
            return {
                'overall_divisional_strength': 60
            }
    
    def _analyze_timing(self, dasha_analysis, transit_analysis):
        """Advanced timing analysis"""
        try:
            timing_factors = []
            
            # Dasha timing
            dasha_strength = dasha_analysis.get('dasha_strength', 50)
            timing_factors.append(dasha_strength)
            
            # Transit timing
            transit_strength = transit_analysis.get('average_transit_strength', 50)
            timing_factors.append(transit_strength)
            
            # Current period assessment
            volatility_level = dasha_analysis.get('volatility_level', 'medium')
            volatility_scores = {'low': 80, 'medium': 60, 'high': 40, 'very_high': 20, 'extreme': 10}
            volatility_score = volatility_scores.get(volatility_level, 60)
            timing_factors.append(volatility_score)
            
            # Overall timing strength
            timing_strength = np.mean(timing_factors)
            
            # Timing recommendation
            if timing_strength > 75:
                timing_recommendation = 'excellent_timing'
            elif timing_strength > 60:
                timing_recommendation = 'good_timing'
            elif timing_strength > 45:
                timing_recommendation = 'moderate_timing'
            else:
                timing_recommendation = 'wait_for_better_timing'
            
            return {
                'timing_strength': timing_strength,
                'dasha_contribution': dasha_strength,
                'transit_contribution': transit_strength,
                'volatility_assessment': volatility_level,
                'timing_recommendation': timing_recommendation,
                'favorable_period_duration': self._estimate_favorable_period(dasha_analysis)
            }
            
        except Exception as e:
            log_debug(f"Timing analysis error: {e}")
            return {
                'timing_strength': 55,
                'timing_recommendation': 'moderate_timing'
            }
    
    def _calculate_vedic_score(self, natal_chart, dasha_analysis, transit_analysis,
                             nakshatra_analysis, yoga_analysis, timing_analysis):
        """Calculate final comprehensive Vedic score"""
        try:
            score_components = []
            
            # 1. Natal chart strength (25%)
            if natal_chart:
                chart_strength = np.mean([planet_info.get('strength', 50) for planet_info in natal_chart.values()])
                score_components.append(chart_strength * 0.25)
            else:
                score_components.append(50 * 0.25)
            
            # 2. Dasha strength (20%)
            dasha_strength = dasha_analysis.get('dasha_strength', 50)
            score_components.append(dasha_strength * 0.20)
            
            # 3. Transit strength (15%)
            transit_strength = transit_analysis.get('average_transit_strength', 50)
            score_components.append(transit_strength * 0.15)
            
            # 4. Nakshatra effects (15%)
            nakshatra_effects = nakshatra_analysis.get('natal_nakshatra_effects', {})
            if nakshatra_effects:
                nakshatra_strength = np.mean([effect.get('financial_impact', 50) for effect in nakshatra_effects.values()])
                score_components.append(nakshatra_strength * 0.15)
            else:
                score_components.append(50 * 0.15)
            
            # 5. Yoga strength (15%)
            yoga_power = yoga_analysis.get('total_yoga_power', 50)
            score_components.append(yoga_power * 0.15)
            
            # 6. Timing strength (10%)
            timing_strength = timing_analysis.get('timing_strength', 50)
            score_components.append(timing_strength * 0.10)
            
            final_score = sum(score_components)
            
            # Apply Vedic-specific adjustments
            
            # Jupiter blessing bonus
            if 'Jupiter' in natal_chart:
                jupiter_strength = natal_chart['Jupiter']['strength']
                if jupiter_strength > 85:
                    final_score += 5  # Jupiter blessing
            
            # Saturn discipline bonus
            if 'Saturn' in natal_chart:
                saturn_strength = natal_chart['Saturn']['strength']
                if saturn_strength > 80:
                    final_score += 3  # Saturn discipline
            
            # Rahu-Ketu penalty for extreme volatility
            if 'Rahu' in natal_chart and natal_chart['Rahu']['strength'] > 80:
                if dasha_analysis.get('volatility_level') == 'extreme':
                    final_score -= 5  # Extreme volatility penalty
            
            # Ensure score is within bounds
            final_score = min(95, max(15, final_score))
            
            return final_score
            
        except Exception as e:
            log_debug(f"Vedic score calculation error: {e}")
            return 55.0
    
    # Helper methods for detailed calculations
    
    def _to_julian_day(self, date):
        """Convert date to Julian day number"""
        try:
            a = (14 - date.month) // 12
            y = date.year + 4800 - a
            m = date.month + 12 * a - 3
            return date.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        except:
            return 2451545  # J2000 epoch
    
    def _get_rashi_from_degree(self, degree):
        """Get Rashi (sign) from degree"""
        rashi_names = list(self.rashis.keys())
        rashi_index = int(degree / 30)
        return rashi_names[rashi_index % 12]
    
    def _get_nakshatra_from_degree(self, degree):
        """Get Nakshatra from degree"""
        nakshatra_names = list(self.nakshatras.keys())
        nakshatra_index = int(degree / 13.33)
        return nakshatra_names[nakshatra_index % 27]
    
    def _calculate_planetary_strength(self, planet, rashi):
        """Calculate planetary strength in a rashi"""
        try:
            if planet in self.planetary_strengths:
                strength_info = self.planetary_strengths[planet]
                base_strength = strength_info['finance_power']
                
                if rashi == strength_info.get('exalted'):
                    return min(100, base_strength + 15)  # Exalted
                elif rashi in strength_info.get('own', []):
                    return min(100, base_strength + 10)  # Own sign
                elif rashi == strength_info.get('debilitated'):
                    return max(20, base_strength - 20)  # Debilitated
                else:
                    return base_strength  # Neutral
            return 60  # Default strength
        except:
            return 60
    
    def _get_aspect_type(self, angle):
        """Determine aspect type from angle"""
        if angle <= 8:
            return 'conjunction'
        elif 52 <= angle <= 68:
            return 'sextile'
        elif 82 <= angle <= 98:
            return 'square'
        elif 112 <= angle <= 128:
            return 'trine'
        elif 172 <= angle <= 188:
            return 'opposition'
        else:
            return 'minor'
    
    def _calculate_transit_strength(self, planet, aspect_type):
        """Calculate strength of planetary transit"""
        aspect_strengths = {
            'conjunction': 85,
            'trine': 75,
            'sextile': 65,
            'square': 45,
            'opposition': 35,
            'minor': 50
        }
        
        base_strength = aspect_strengths.get(aspect_type, 50)
        
        # Adjust based on planet
        if planet in ['Jupiter', 'Venus']:
            base_strength += 10  # Benefics are stronger
        elif planet in ['Mars', 'Saturn', 'Rahu', 'Ketu']:
            base_strength -= 5   # Malefics need careful handling
        
        return min(100, max(20, base_strength))
    
    def _calculate_dasha_strength(self, mahadasha, antardasha):
        """Calculate combined dasha strength"""
        try:
            maha_strength = self.planetary_strengths.get(mahadasha, {}).get('finance_power', 60)
            antar_strength = self.planetary_strengths.get(antardasha, {}).get('finance_power', 60)
            
            # Weighted combination (Mahadasha more important)
            combined_strength = maha_strength * 0.7 + antar_strength * 0.3
            
            return min(100, max(20, combined_strength))
        except:
            return 60
    
    def _evaluate_nakshatra_finance_impact(self, impact_type, lord):
        """Evaluate financial impact of nakshatra"""
        impact_scores = {
            'volatile_gains': 45,
            'deep_value': 75,
            'sharp_moves': 55,
            'steady_bull': 85,
            'discovery_phase': 60,
            'disruption': 35,
            'recovery': 70,
            'safe_growth': 80,
            'tight_control': 65,
            'leadership_premium': 85,
            'luxury_gains': 75,
            'institutional_support': 80,
            'crafted_value': 70,
            'breakthrough_gains': 65,
            'autonomous_growth': 75,
            'choice_driven': 60,
            'loyal_returns': 75,
            'mature_strength': 80,
            'fundamental_shift': 50,
            'unstoppable_rise': 90,
            'ultimate_success': 95,
            'information_edge': 70,
            'prosperity': 85,
            'corrective_action': 55,
            'intense_transformation': 60,
            'deep_value_creation': 85,
            'wealth_accumulation': 90
        }
        
        base_score = impact_scores.get(impact_type, 60)
        
        # Adjust based on nakshatra lord
        lord_adjustments = {
            'Jupiter': 10, 'Venus': 8, 'Mercury': 5, 'Sun': 5, 'Moon': 3,
            'Saturn': 2, 'Mars': 0, 'Rahu': -5, 'Ketu': -5
        }
        
        adjustment = lord_adjustments.get(lord, 0)
        
        return min(100, max(20, base_score + adjustment))
    
    def _calculate_nakshatra_strength(self, nakshatra_name):
        """Calculate strength of a nakshatra"""
        # Some nakshatras are naturally more powerful for wealth
        powerful_nakshatras = [
            'Rohini', 'Uttara Phalguni', 'Uttara Ashadha', 'Revati',
            'Pushya', 'Magha', 'Dhanishtha', 'Purva Ashadha'
        ]
        
        if nakshatra_name in powerful_nakshatras:
            return 85
        else:
            return 65
    
    def _analyze_nakshatra_compatibility(self, nakshatra_effects):
        """Analyze compatibility between different nakshatras in chart"""
        try:
            if len(nakshatra_effects) < 2:
                return 60
            
            # Count harmonious combinations
            harmonious_count = 0
            total_combinations = 0
            
            lords = [effect.get('lord') for effect in nakshatra_effects.values()]
            
            for i, lord1 in enumerate(lords):
                for j, lord2 in enumerate(lords[i+1:], i+1):
                    total_combinations += 1
                    
                    # Friendly combinations
                    friendly_pairs = [
                        ('Jupiter', 'Venus'), ('Sun', 'Moon'), ('Mercury', 'Venus'),
                        ('Jupiter', 'Moon'), ('Sun', 'Jupiter'), ('Moon', 'Venus')
                    ]
                    
                    if (lord1, lord2) in friendly_pairs or (lord2, lord1) in friendly_pairs:
                        harmonious_count += 1
            
            if total_combinations > 0:
                compatibility_score = (harmonious_count / total_combinations) * 100
                return min(100, max(30, compatibility_score))
            
            return 60
            
        except:
            return 60
    
    def _check_dhana_yoga(self, natal_chart):
        """Check for Dhana (wealth) yoga"""
        try:
            # Simplified check - strong Venus and Jupiter
            strength_sum = 0
            count = 0
            
            for planet in ['Venus', 'Jupiter', 'Mercury']:
                if planet in natal_chart:
                    strength_sum += natal_chart[planet]['strength']
                    count += 1
            
            if count > 0:
                return strength_sum / count
            return 50
            
        except:
            return 50
    
    def _check_raj_yoga(self, natal_chart):
        """Check for Raj (royal) yoga"""
        try:
            # Simplified check - strong Sun and Jupiter
            if 'Sun' in natal_chart and 'Jupiter' in natal_chart:
                sun_strength = natal_chart['Sun']['strength']
                jupiter_strength = natal_chart['Jupiter']['strength']
                
                # Both should be strong
                if sun_strength > 75 and jupiter_strength > 75:
                    return (sun_strength + jupiter_strength) / 2
            
            return 50
            
        except:
            return 50
    
    def _analyze_jupiter_transit(self, natal_chart, current_positions):
        """Special analysis for Jupiter transit"""
        try:
            if 'Jupiter' not in natal_chart or 'Jupiter' not in current_positions:
                return 60
            
            natal_jupiter = natal_chart['Jupiter']['degree']
            current_jupiter = current_positions['Jupiter']['degree']
            
            aspect_angle = abs(current_jupiter - natal_jupiter)
            if aspect_angle > 180:
                aspect_angle = 360 - aspect_angle
            
            # Jupiter return cycle (approximately every 12 years)
            if aspect_angle < 30:  # Near return
                return 90
            elif 112 <= aspect_angle <= 128:  # Trine
                return 85
            elif 82 <= aspect_angle <= 98:  # Square (challenging but growth)
                return 60
            else:
                return 70
                
        except:
            return 70
    
    def _analyze_saturn_transit(self, natal_chart, current_positions):
        """Special analysis for Saturn transit"""
        try:
            if 'Saturn' not in natal_chart or 'Saturn' not in current_positions:
                return 60
            
            natal_saturn = natal_chart['Saturn']['degree']
            current_saturn = current_positions['Saturn']['degree']
            
            aspect_angle = abs(current_saturn - natal_saturn)
            if aspect_angle > 180:
                aspect_angle = 360 - aspect_angle
            
            # Saturn return cycle (approximately every 29 years)
            if aspect_angle < 30:  # Near return
                return 75  # Saturn return brings discipline
            elif 172 <= aspect_angle <= 188:  # Opposition
                return 55  # Challenging but necessary
            else:
                return 65
                
        except:
            return 65
    
    def _determine_transit_nature(self, avg_strength):
        """Determine overall nature of transits"""
        if avg_strength > 75:
            return 'highly_favorable'
        elif avg_strength > 60:
            return 'favorable'
        elif avg_strength > 45:
            return 'neutral'
        else:
            return 'challenging'
    
    def _calculate_navamsha_strength(self, natal_chart):
        """Calculate D9 (Navamsha) strength"""
        try:
            # Simplified: check if planets are strong in navamsha
            total_strength = 0
            count = 0
            
            for planet, info in natal_chart.items():
                if planet != 'Ascendant':
                    # Navamsha position (simplified)
                    navamsha_degree = (info['degree'] * 9) % 360
                    navamsha_rashi = self._get_rashi_from_degree(navamsha_degree)
                    navamsha_strength = self._calculate_planetary_strength(planet, navamsha_rashi)
                    
                    total_strength += navamsha_strength
                    count += 1
            
            return total_strength / count if count > 0 else 60
            
        except:
            return 60
    
    def _calculate_dasamsha_strength(self, natal_chart):
        """Calculate D10 (Dasamsha) strength"""
        try:
            # Focus on career planets
            career_planets = ['Sun', 'Saturn', 'Jupiter', 'Mercury']
            total_strength = 0
            count = 0
            
            for planet in career_planets:
                if planet in natal_chart:
                    total_strength += natal_chart[planet]['strength']
                    count += 1
            
            return total_strength / count if count > 0 else 60
            
        except:
            return 60
    
    def _calculate_hora_strength(self, natal_chart):
        """Calculate D2 (Hora) strength for wealth"""
        try:
            # Focus on wealth planets
            wealth_planets = ['Venus', 'Jupiter', 'Mercury', 'Moon']
            total_strength = 0
            count = 0
            
            for planet in wealth_planets:
                if planet in natal_chart:
                    total_strength += natal_chart[planet]['strength']
                    count += 1
            
            return total_strength / count if count > 0 else 60
            
        except:
            return 60
    
    def _estimate_favorable_period(self, dasha_analysis):
        """Estimate duration of favorable period"""
        try:
            volatility_level = dasha_analysis.get('volatility_level', 'medium')
            years_remaining = dasha_analysis.get('years_remaining', 5)
            
            if volatility_level in ['low', 'medium']:
                return f"{years_remaining:.1f} years"
            else:
                return f"{years_remaining * 0.5:.1f} years"  # Shorter for high volatility
                
        except:
            return "2-3 years"
    
    def _default_score(self):
        """Return default score when analysis fails"""
        return {
            'vedic_score': 55,
            'natal_chart': {},
            'dasha_analysis': {'mahadasha': 'Jupiter', 'dasha_strength': 65},
            'transit_analysis': {'average_transit_strength': 60},
            'nakshatra_analysis': {'natal_nakshatra_effects': {}},
            'yoga_analysis': {'detected_yogas': [], 'total_yoga_power': 55},
            'timing_analysis': {'timing_strength': 55}
        }

# Backward compatibility with existing system
class VedicAstrologyAnalyzer:
    """Vedik astroloji analiz motoru"""
    
    def __init__(self):
        self.rasi_names = [
            "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
            "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"
        ]
        
        self.nakshatra_names = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        
        self.nakshatra_lords = [
            "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
            "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun",
            "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
            "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
            "Jupiter", "Saturn", "Mercury"
        ]
        
        self.dasha_sequence = [
            "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
            "Jupiter", "Saturn", "Mercury"
        ]
        
        self.dasha_periods = {
            "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
            "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
        }
    
    def calculate_vedic_score(self, symbol: str, founding_date: str, current_date: str = None) -> Dict:
        """
        Vedik astroloji skoru hesapla
        Mevcut sistemi bozmadan yeni analiz ekler
        """
        try:
            if current_date is None:
                current_date = datetime.now().strftime('%Y-%m-%d')
            
            log_info(f"{symbol} için Vedik astroloji analizi başlatılıyor...")
            
            # 1. Doğum haritası hesapla
            chart = self._calculate_birth_chart(symbol, founding_date)
            
            # 2. Dasha analizi
            dasha_analysis = self._analyze_dasha(chart, founding_date, current_date)
            
            # 3. Transit analizi
            transit_analysis = self._analyze_transits(chart, current_date)
            
            # 4. Vedik skor hesapla
            vedic_score = self._calculate_vedic_score_from_chart(chart, dasha_analysis, transit_analysis)
            
            # 5. Detaylı analiz
            detailed_analysis = self._get_detailed_vedic_analysis(chart, dasha_analysis, transit_analysis)
            
            result = {
                'vedic_score': vedic_score,
                'vedic_chart': chart,
                'dasha_analysis': dasha_analysis,
                'transit_analysis': transit_analysis,
                'detailed_analysis': detailed_analysis,
                'analysis_date': current_date
            }
            
            log_info(f"{symbol} Vedik astroloji skoru: {vedic_score}")
            return result
            
        except Exception as e:
            log_error(f"{symbol} Vedik astroloji analizi hatası: {e}")
            # Fallback: Mevcut sistemi bozmadan varsayılan değer döndür
            return {
                'vedic_score': 52.05,  # Mevcut sistem değeri
                'vedic_chart': None,
                'dasha_analysis': None,
                'transit_analysis': None,
                'detailed_analysis': "Vedik analiz mevcut değil",
                'analysis_date': current_date,
                'error': str(e)
            }
    
    def _calculate_birth_chart(self, symbol: str, founding_date: str) -> VedicChart:
        """Doğum haritası hesapla"""
        try:
            # Basit hesaplama (gerçek implementasyon için swisseph gerekli)
            founding_dt = datetime.strptime(founding_date, '%Y-%m-%d')
            
            # Simüle edilmiş gezegen konumları (gerçek hesaplama için astronomi kütüphanesi gerekli)
            planets = {}
            
            # Güneş konumu (basit hesaplama)
            sun_degree = (founding_dt.timetuple().tm_yday / 365.25) * 360
            sun_rashi = self._get_rashi_from_degree(sun_degree)
            sun_nakshatra = self._get_nakshatra_from_degree(sun_degree)
            
            planets['Sun'] = VedicPlanet(
                name='Sun',
                degree=sun_degree,
                rashi=sun_rashi,
                nakshatra=sun_nakshatra,
                nakshatra_lord=self._get_nakshatra_lord(sun_nakshatra)
            )
            
            # Diğer gezegenler için simüle edilmiş konumlar
            planet_offsets = {
                'Moon': 120, 'Mars': 240, 'Mercury': 60, 'Jupiter': 300,
                'Venus': 180, 'Saturn': 30, 'Rahu': 150, 'Ketu': 330
            }
            
            for planet, offset in planet_offsets.items():
                degree = (sun_degree + offset) % 360
                rashi = self._get_rashi_from_degree(degree)
                nakshatra = self._get_nakshatra_from_degree(degree)
                
                planets[planet] = VedicPlanet(
                    name=planet,
                    degree=degree,
                    rashi=rashi,
                    nakshatra=nakshatra,
                    nakshatra_lord=self._get_nakshatra_lord(nakshatra)
                )
            
            # Lagna hesaplama (basit)
            lagna_degree = (sun_degree + 90) % 360
            lagna = self._get_rashi_from_degree(lagna_degree)
            
            return VedicChart(
                lagna=lagna,
                planets=planets,
                dasha_lord="Sun",  # Varsayılan
                dasha_period="Maha Dasha",
                current_transits={}
            )
            
        except Exception as e:
            log_error(f"Doğum haritası hesaplama hatası: {e}")
            return None
    
    def _analyze_dasha(self, chart: VedicChart, founding_date: str, current_date: str) -> Dict:
        """Dasha analizi"""
        try:
            founding_dt = datetime.strptime(founding_date, '%Y-%m-%d')
            current_dt = datetime.strptime(current_date, '%Y-%m-%d')
            
            # Basit dasha hesaplama
            years_since_founding = (current_dt - founding_dt).days / 365.25
            
            # Vimshottari dasha sırası
            total_period = sum(self.dasha_periods.values())
            current_period = years_since_founding % total_period
            
            # Aktif dasha bul
            cumulative_period = 0
            active_dasha = "Sun"
            
            for dasha_lord in self.dasha_sequence:
                if current_period <= cumulative_period + self.dasha_periods[dasha_lord]:
                    active_dasha = dasha_lord
                    break
                cumulative_period += self.dasha_periods[dasha_lord]
            
            return {
                'active_dasha': active_dasha,
                'dasha_period': self.dasha_periods[active_dasha],
                'years_since_founding': years_since_founding,
                'dasha_strength': self._calculate_dasha_strength(active_dasha, chart)
            }
            
        except Exception as e:
            log_error(f"Dasha analizi hatası: {e}")
            return {'active_dasha': 'Sun', 'dasha_period': 6, 'dasha_strength': 50}
    
    def _analyze_transits(self, chart: VedicChart, current_date: str) -> Dict:
        """Transit analizi"""
        try:
            # Basit transit hesaplama
            current_dt = datetime.strptime(current_date, '%Y-%m-%d')
            
            # Güncel gezegen konumları (simüle edilmiş)
            transit_planets = {}
            
            for planet in chart.planets.keys():
                # Basit transit hesaplama
                base_degree = chart.planets[planet].degree
                transit_degree = (base_degree + (current_dt.timetuple().tm_yday / 365.25) * 360) % 360
                transit_rashi = self._get_rashi_from_degree(transit_degree)
                
                transit_planets[planet] = {
                    'degree': transit_degree,
                    'rashi': transit_rashi,
                    'aspect': self._calculate_aspect(transit_degree, chart.planets[planet].degree)
                }
            
            return {
                'transit_planets': transit_planets,
                'transit_strength': self._calculate_transit_strength(transit_planets, chart)
            }
            
        except Exception as e:
            log_error(f"Transit analizi hatası: {e}")
            return {'transit_planets': {}, 'transit_strength': 50}
    
    def _calculate_vedic_score_from_chart(self, chart: VedicChart, dasha_analysis: Dict, transit_analysis: Dict) -> float:
        """Vedik skor hesapla"""
        try:
            if not chart:
                return 52.05  # Fallback değer
            
            score = 50.0  # Başlangıç skoru
            
            # 1. Lagna gücü
            lagna_strength = self._calculate_lagna_strength(chart)
            score += lagna_strength * 0.2
            
            # 2. Dasha gücü
            dasha_strength = dasha_analysis.get('dasha_strength', 50)
            score += (dasha_strength - 50) * 0.3
            
            # 3. Transit gücü
            transit_strength = transit_analysis.get('transit_strength', 50)
            score += (transit_strength - 50) * 0.2
            
            # 4. Gezegen güçleri
            planet_strength = self._calculate_planet_strength(chart)
            score += planet_strength * 0.3
            
            # Skoru 0-100 aralığına sınırla
            score = max(0, min(100, score))
            
            return round(score, 2)
            
        except Exception as e:
            log_error(f"Vedik skor hesaplama hatası: {e}")
            return 52.05  # Fallback değer
    
    def _get_detailed_vedic_analysis(self, chart: VedicChart, dasha_analysis: Dict, transit_analysis: Dict) -> str:
        """Detaylı Vedik analiz metni"""
        try:
            if not chart:
                return "Vedik analiz mevcut değil"
            
            analysis_parts = []
            
            # Lagna analizi
            lagna = chart.lagna
            analysis_parts.append(f"Lagna (Yükselen): {lagna}")
            
            # Dasha analizi
            active_dasha = dasha_analysis.get('active_dasha', 'Sun')
            analysis_parts.append(f"Aktif Dasha: {active_dasha}")
            
            # Transit analizi
            transit_strength = transit_analysis.get('transit_strength', 50)
            if transit_strength > 60:
                analysis_parts.append("Güçlü transit dönemi")
            elif transit_strength < 40:
                analysis_parts.append("Zayıf transit dönemi")
            else:
                analysis_parts.append("Orta seviye transit dönemi")
            
            return " | ".join(analysis_parts)
            
        except Exception as e:
            log_error(f"Detaylı analiz hatası: {e}")
            return "Vedik analiz mevcut değil"
    
    def _get_rashi_from_degree(self, degree: float) -> str:
        """Dereceden burç bul"""
        rashi_index = int(degree / 30)
        return self.rasi_names[rashi_index % 12]
    
    def _get_nakshatra_from_degree(self, degree: float) -> str:
        """Dereceden nakşatra bul"""
        nakshatra_index = int(degree / 13.33)
        return self.nakshatra_names[nakshatra_index % 27]
    
    def _get_nakshatra_lord(self, nakshatra: str) -> str:
        """Nakşatra efendisi bul"""
        try:
            index = self.nakshatra_names.index(nakshatra)
            return self.nakshatra_lords[index]
        except ValueError:
            return "Sun"
    
    def _calculate_dasha_strength(self, dasha_lord: str, chart: VedicChart) -> float:
        """Dasha gücü hesapla"""
        try:
            if not chart or dasha_lord not in chart.planets:
                return 50.0
            
            planet = chart.planets[dasha_lord]
            
            # Basit güç hesaplama
            strength = 50.0
            
            # Güçlü burçlar
            strong_signs = ["Simha", "Vrishabha", "Dhanu", "Karka"]
            if planet.rashi in strong_signs:
                strength += 20
            
            # Güçlü nakşatralar
            strong_nakshatras = ["Rohini", "Magha", "Mula", "Uttara Ashadha"]
            if planet.nakshatra in strong_nakshatras:
                strength += 15
            
            return min(100, strength)
            
        except Exception as e:
            log_error(f"Dasha gücü hesaplama hatası: {e}")
            return 50.0
    
    def _calculate_lagna_strength(self, chart: VedicChart) -> float:
        """Lagna gücü hesapla"""
        try:
            if not chart:
                return 50.0
            
            # Basit lagna gücü hesaplama
            lagna = chart.lagna
            
            # Güçlü lagna burçları
            strong_lagnas = ["Simha", "Vrishabha", "Dhanu", "Karka"]
            if lagna in strong_lagnas:
                return 70.0
            else:
                return 50.0
                
        except Exception as e:
            log_error(f"Lagna gücü hesaplama hatası: {e}")
            return 50.0
    
    def _calculate_planet_strength(self, chart: VedicChart) -> float:
        """Gezegen güçleri hesapla"""
        try:
            if not chart:
                return 50.0
            
            total_strength = 0
            planet_count = 0
            
            for planet in chart.planets.values():
                strength = 50.0
                
                # Güçlü burçlar
                strong_signs = ["Simha", "Vrishabha", "Dhanu", "Karka"]
                if planet.rashi in strong_signs:
                    strength += 15
                
                # Güçlü nakşatralar
                strong_nakshatras = ["Rohini", "Magha", "Mula", "Uttara Ashadha"]
                if planet.nakshatra in strong_nakshatras:
                    strength += 10
                
                total_strength += strength
                planet_count += 1
            
            return total_strength / planet_count if planet_count > 0 else 50.0
            
        except Exception as e:
            log_error(f"Gezegen gücü hesaplama hatası: {e}")
            return 50.0
    
    def _calculate_aspect(self, degree1: float, degree2: float) -> str:
        """Aspect hesapla"""
        try:
            diff = abs(degree1 - degree2)
            if diff > 180:
                diff = 360 - diff
            
            if diff <= 30:
                return "Conjunction"
            elif diff <= 60:
                return "Sextile"
            elif diff <= 90:
                return "Square"
            elif diff <= 120:
                return "Trine"
            elif diff <= 150:
                return "Quincunx"
            else:
                return "Opposition"
                
        except Exception as e:
            log_error(f"Aspect hesaplama hatası: {e}")
            return "Unknown"
    
    def _calculate_transit_strength(self, transit_planets: Dict, chart: VedicChart) -> float:
        """Transit gücü hesapla"""
        try:
            if not chart or not transit_planets:
                return 50.0
            
            total_strength = 0
            aspect_count = 0
            
            for planet_name, transit_info in transit_planets.items():
                if planet_name in chart.planets:
                    aspect = transit_info.get('aspect', 'Unknown')
                    
                    # Aspect güçleri
                    aspect_strengths = {
                        'Conjunction': 80,
                        'Trine': 70,
                        'Sextile': 60,
                        'Square': 40,
                        'Quincunx': 30,
                        'Opposition': 20
                    }
                    
                    strength = aspect_strengths.get(aspect, 50)
                    total_strength += strength
                    aspect_count += 1
            
            return total_strength / aspect_count if aspect_count > 0 else 50.0
            
        except Exception as e:
            log_error(f"Transit gücü hesaplama hatası: {e}")
            return 50.0


# Global analyzer instances
vedic_analyzer = VedicAstrologyAnalyzer()
ultra_vedic_analyzer = UltraVedicAnalyzer()

def get_vedic_score(symbol, stock_data=None):
    """
    Get ultra-sophisticated Vedic astrology score for a stock
    
    Args:
        symbol: Stock symbol
        stock_data: DataFrame with OHLCV data (optional)
        
    Returns:
        float: Vedic astrology score (0-100)
    """
    try:
        result = ultra_vedic_analyzer.analyze_vedic_astrology(symbol, stock_data)
        return result['vedic_score']
    except:
        return 55.0


