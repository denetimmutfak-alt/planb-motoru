# -*- coding: utf-8 -*-
"""
PlanB Motoru - Ultra Moon Phases Enhanced Analysis Module
Professional Lunar Cycle Analysis - Expert Level
28 Lunar Mansions, Void-of-Course Periods, Eclipse Cycles, Tidal Finance Theory
"""

import ephem
import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import logging

# Module logger
logger = logging.getLogger(__name__)

# ExpertModule base class interface
from multi_expert_engine import ExpertModule


class UltraMoonPhasesModule(ExpertModule):
    """Ultra Moon Phases Enhanced - Professional Lunar Market Analysis"""
    
    def __init__(self, module_name: str = "Ultra Moon Phases Enhanced"):
        super().__init__(module_name)
        super().__init__(module_name)
        
        # 28 Lunar Mansions (Nakshatras) with financial market correlations
        self.lunar_mansions = {
            'ashwini': {'degrees': (0, 13.33), 'market_sector': 'technology', 'volatility': 'high', 'energy': 'initiation'},
            'bharani': {'degrees': (13.33, 26.67), 'market_sector': 'agriculture', 'volatility': 'medium', 'energy': 'restraint'},
            'krittika': {'degrees': (26.67, 40), 'market_sector': 'energy', 'volatility': 'high', 'energy': 'cutting'},
            'rohini': {'degrees': (40, 53.33), 'market_sector': 'luxury', 'volatility': 'low', 'energy': 'growth'},
            'mrigashira': {'degrees': (53.33, 66.67), 'market_sector': 'exploration', 'volatility': 'medium', 'energy': 'seeking'},
            'ardra': {'degrees': (66.67, 80), 'market_sector': 'disruption', 'volatility': 'very_high', 'energy': 'destruction'},
            'punarvasu': {'degrees': (80, 93.33), 'market_sector': 'recovery', 'volatility': 'low', 'energy': 'restoration'},
            'pushya': {'degrees': (93.33, 106.67), 'market_sector': 'nurturing', 'volatility': 'very_low', 'energy': 'nourishment'},
            'ashlesha': {'degrees': (106.67, 120), 'market_sector': 'psychological', 'volatility': 'high', 'energy': 'clinging'},
            'magha': {'degrees': (120, 133.33), 'market_sector': 'leadership', 'volatility': 'medium', 'energy': 'power'},
            'purva_phalguni': {'degrees': (133.33, 146.67), 'market_sector': 'entertainment', 'volatility': 'medium', 'energy': 'pleasure'},
            'uttara_phalguni': {'degrees': (146.67, 160), 'market_sector': 'service', 'volatility': 'low', 'energy': 'patronage'},
            'hasta': {'degrees': (160, 173.33), 'market_sector': 'craftsmanship', 'volatility': 'low', 'energy': 'skill'},
            'chitra': {'degrees': (173.33, 186.67), 'market_sector': 'beauty', 'volatility': 'medium', 'energy': 'creativity'},
            'swati': {'degrees': (186.67, 200), 'market_sector': 'trade', 'volatility': 'high', 'energy': 'independence'},
            'vishakha': {'degrees': (200, 213.33), 'market_sector': 'achievement', 'volatility': 'medium', 'energy': 'purpose'},
            'anuradha': {'degrees': (213.33, 226.67), 'market_sector': 'cooperation', 'volatility': 'low', 'energy': 'friendship'},
            'jyeshtha': {'degrees': (226.67, 240), 'market_sector': 'seniority', 'volatility': 'high', 'energy': 'protection'},
            'mula': {'degrees': (240, 253.33), 'market_sector': 'transformation', 'volatility': 'very_high', 'energy': 'uprooting'},
            'purva_ashadha': {'degrees': (253.33, 266.67), 'market_sector': 'victory', 'volatility': 'high', 'energy': 'invincibility'},
            'uttara_ashadha': {'degrees': (266.67, 280), 'market_sector': 'achievement', 'volatility': 'medium', 'energy': 'permanent_victory'},
            'shravana': {'degrees': (280, 293.33), 'market_sector': 'communication', 'volatility': 'low', 'energy': 'listening'},
            'dhanishta': {'degrees': (293.33, 306.67), 'market_sector': 'wealth', 'volatility': 'medium', 'energy': 'prosperity'},
            'shatabhisha': {'degrees': (306.67, 320), 'market_sector': 'healing', 'volatility': 'high', 'energy': 'mystery'},
            'purva_bhadrapada': {'degrees': (320, 333.33), 'market_sector': 'transformation', 'volatility': 'very_high', 'energy': 'purification'},
            'uttara_bhadrapada': {'degrees': (333.33, 346.67), 'market_sector': 'spirituality', 'volatility': 'medium', 'energy': 'compassion'},
            'revati': {'degrees': (346.67, 360), 'market_sector': 'completion', 'volatility': 'low', 'energy': 'nourishment'}
        }
        
        # Ultra-precise moon phase definitions
        self.ultra_moon_phases = {
            'dark_moon': {'range': (350, 10), 'power': 0.95, 'energy': 'new_beginnings', 'market_effect': 'accumulation'},
            'new_moon': {'range': (350, 20), 'power': 0.90, 'energy': 'intention_setting', 'market_effect': 'trend_start'},
            'waxing_crescent': {'range': (20, 80), 'power': 0.40, 'energy': 'growth', 'market_effect': 'bullish_momentum'},
            'first_quarter': {'range': (80, 100), 'power': 0.70, 'energy': 'action', 'market_effect': 'breakout'},
            'waxing_gibbous': {'range': (100, 160), 'power': 0.50, 'energy': 'refinement', 'market_effect': 'consolidation'},
            'full_moon': {'range': (160, 200), 'power': 1.00, 'energy': 'culmination', 'market_effect': 'high_volatility'},
            'waning_gibbous': {'range': (200, 260), 'power': 0.60, 'energy': 'gratitude', 'market_effect': 'profit_taking'},
            'last_quarter': {'range': (260, 280), 'power': 0.70, 'energy': 'release', 'market_effect': 'correction'},
            'waning_crescent': {'range': (280, 340), 'power': 0.30, 'energy': 'reflection', 'market_effect': 'bearish_momentum'},
            'balsamic_moon': {'range': (340, 350), 'power': 0.80, 'energy': 'wisdom', 'market_effect': 'preparation'}
        }
        
        # Void-of-Course (VOC) Moon periods and market effects
        self.voc_effects = {
            'short': {'duration_hours': (0, 2), 'market_impact': 0.1, 'trading_advice': 'normal_activity'},
            'medium': {'duration_hours': (2, 8), 'market_impact': 0.3, 'trading_advice': 'reduced_activity'},
            'long': {'duration_hours': (8, 24), 'market_impact': 0.6, 'trading_advice': 'avoid_new_positions'},
            'very_long': {'duration_hours': (24, 72), 'market_impact': 0.9, 'trading_advice': 'market_uncertainty'}
        }
        
        # Eclipse cycles and market volatility periods
        self.eclipse_cycles = {
            'saros_223': {'period_months': 223, 'intensity': 'high', 'market_effect': 'major_trend_change'},
            'inex_358': {'period_months': 358, 'intensity': 'medium', 'market_effect': 'sector_rotation'},
            'tritos_135': {'period_months': 135, 'intensity': 'low', 'market_effect': 'minor_volatility'}
        }
        
        # Lunar node cycles (18.6 years)
        self.lunar_node_cycle = {
            'ascending_node': {'energy': 'growth', 'market_bias': 'bullish'},
            'descending_node': {'energy': 'release', 'market_bias': 'bearish'}
        }
        
        # Tidal coefficients and market correlation
        self.tidal_finance_theory = {
            'spring_tides': {'range': (80, 120), 'volatility_multiplier': 1.4, 'liquidity_effect': 'high'},
            'neap_tides': {'range': (20, 60), 'volatility_multiplier': 0.7, 'liquidity_effect': 'low'},
            'extreme_tides': {'range': (100, 120), 'volatility_multiplier': 1.8, 'liquidity_effect': 'extreme'}
        }
        
        logger.info("Ultra Moon Phases Enhanced Module initialized with professional lunar analysis")
    
    def prepare_features(self, data: Dict) -> Dict:
        """Ay evresi analizi için özellikleri hazırla"""
        try:
            symbol = data.get('symbol', 'UNKNOWN')
            current_date = datetime.now()
            
            # Calculate precise lunar position
            features = self._calculate_ultra_lunar_position(current_date)
            
            # Add symbol and date context
            features['symbol'] = symbol
            features['analysis_date'] = current_date
            
            # Calculate Lunar Mansion (Nakshatra)
            features['lunar_mansion'] = self._calculate_lunar_mansion(features['moon_longitude'])
            
            # Determine current moon phase with precision
            features['moon_phase'] = self._determine_ultra_precise_phase(features['moon_phase_angle'])
            
            # Calculate Void-of-Course periods
            features['voc_moon'] = self._calculate_voc_periods(current_date)
            
            # Eclipse proximity analysis
            features['eclipse_influence'] = self._analyze_eclipse_proximity(current_date)
            
            # Lunar node position and cycle
            features['lunar_nodes'] = self._calculate_lunar_node_position(current_date)
            
            # Tidal coefficient calculation
            features['tidal_coefficient'] = self._calculate_tidal_coefficient(features)
            
            # Market correlation analysis
            features['market_correlation'] = self._calculate_moon_market_correlation(features)
            
            return features
            
        except Exception as e:
            logger.error(f"Moon phases feature preparation error: {e}")
            return {'error': str(e)}
    
    def infer(self, features: Dict) -> Tuple[float, float]:
        """Ay evresi analizi inference"""
        try:
            if 'error' in features:
                return 50.0, 0.8
            
            # Base moon phase score
            base_score = 50.0
            uncertainty = 0.6
            
            # 1. Moon Phase Power scoring (30% weight)
            phase_score = self._score_moon_phase(features.get('moon_phase', {}))
            
            # 2. Lunar Mansion scoring (25% weight)
            mansion_score = self._score_lunar_mansion(features.get('lunar_mansion', {}))
            
            # 3. Void-of-Course impact (20% weight)
            voc_score = self._score_voc_periods(features.get('voc_moon', {}))
            
            # 4. Eclipse influence (15% weight)
            eclipse_score = self._score_eclipse_influence(features.get('eclipse_influence', {}))
            
            # 5. Tidal coefficient (10% weight)
            tidal_score = self._score_tidal_coefficient(features.get('tidal_coefficient', {}))
            
            # Weighted combination
            final_score = (
                phase_score * 0.30 +
                mansion_score * 0.25 +
                voc_score * 0.20 +
                eclipse_score * 0.15 +
                tidal_score * 0.10
            )
            
            # Dynamic uncertainty based on lunar precision
            moon_precision = features.get('moon_phase', {}).get('power', 0.5)
            uncertainty = max(0.2, 1.0 - moon_precision)
            
            # Apply market correlation adjustments
            correlation_data = features.get('market_correlation', {})
            correlation_multiplier = correlation_data.get('correlation_strength', 1.0)
            final_score *= correlation_multiplier
            
            # Clamp to valid range
            final_score = max(0, min(100, final_score))
            
            self.confidence_level = 1.0 - uncertainty
            
            logger.info(f"Moon phases analysis completed: {final_score:.2f} (uncertainty: {uncertainty:.3f})")
            return final_score, uncertainty
            
        except Exception as e:
            logger.error(f"Moon phases inference error: {e}")
            return 50.0, 0.8
    
    def retrain(self, data: Dict) -> None:
        """Lunar model retraining (astronomical data is constant)"""
        logger.info("Moon phases module: Astronomical calculations are constant, no retraining needed")
        pass
    
    def _calculate_ultra_lunar_position(self, date: datetime) -> Dict:
        """Calculate ultra-precise lunar position"""
        try:
            # Create observer (Greenwich)
            observer = ephem.Observer()
            observer.lat = '51.4769'  # Greenwich
            observer.lon = '0.0'
            observer.date = date
            
            # Calculate Moon position
            moon = ephem.Moon(observer)
            sun = ephem.Sun(observer)
            
            # Moon longitude in degrees
            moon_longitude = float(moon.hlon) * 180 / math.pi
            sun_longitude = float(sun.hlon) * 180 / math.pi
            
            # Phase angle calculation
            moon_phase_angle = (moon_longitude - sun_longitude) % 360
            
            # Moon illumination percentage
            moon_illumination = float(moon.moon_phase) * 100
            
            # Angular separation from Sun
            moon_sun_separation = float(moon.earth_distance)
            
            return {
                'moon_longitude': moon_longitude,
                'sun_longitude': sun_longitude,
                'moon_phase_angle': moon_phase_angle,
                'moon_illumination': moon_illumination,
                'moon_distance_km': float(moon.earth_distance) * 149597870.7,  # Convert to km
                'moon_angular_size': float(moon.size),
                'calculation_precision': 'professional_ephemeris'
            }
            
        except Exception as e:
            logger.error(f"Lunar position calculation error: {e}")
            # Fallback calculation
            day_of_month = date.day
            return {
                'moon_longitude': (day_of_month * 12) % 360,
                'moon_phase_angle': (day_of_month * 12) % 360,
                'moon_illumination': abs(math.sin(day_of_month * 0.2)) * 100,
                'calculation_precision': 'simplified_fallback'
            }
    
    def _calculate_lunar_mansion(self, moon_longitude: float) -> Dict:
        """Calculate current Lunar Mansion (Nakshatra)"""
        try:
            # Find which mansion the Moon is in
            for mansion_name, mansion_data in self.lunar_mansions.items():
                start_degree, end_degree = mansion_data['degrees']
                
                if start_degree <= moon_longitude <= end_degree:
                    # Calculate position within mansion
                    mansion_position = (moon_longitude - start_degree) / (end_degree - start_degree)
                    
                    return {
                        'name': mansion_name,
                        'position_in_mansion': mansion_position,
                        'market_sector': mansion_data['market_sector'],
                        'volatility_level': mansion_data['volatility'],
                        'energy_type': mansion_data['energy'],
                        'degrees_in_mansion': moon_longitude - start_degree
                    }
            
            # Fallback for edge cases
            return {
                'name': 'unknown',
                'position_in_mansion': 0.5,
                'market_sector': 'general',
                'volatility_level': 'medium',
                'energy_type': 'neutral'
            }
            
        except Exception as e:
            logger.error(f"Lunar mansion calculation error: {e}")
            return {'error': str(e)}
    
    def _determine_ultra_precise_phase(self, phase_angle: float) -> Dict:
        """Determine ultra-precise moon phase"""
        try:
            for phase_name, phase_data in self.ultra_moon_phases.items():
                start_angle, end_angle = phase_data['range']
                
                # Handle wrap-around for angles near 0/360
                if start_angle > end_angle:
                    if phase_angle >= start_angle or phase_angle <= end_angle:
                        return {
                            'name': phase_name,
                            'power': phase_data['power'],
                            'energy': phase_data['energy'],
                            'market_effect': phase_data['market_effect'],
                            'angle': phase_angle
                        }
                else:
                    if start_angle <= phase_angle <= end_angle:
                        return {
                            'name': phase_name,
                            'power': phase_data['power'],
                            'energy': phase_data['energy'],
                            'market_effect': phase_data['market_effect'],
                            'angle': phase_angle
                        }
            
            # Fallback
            return {
                'name': 'intermediate',
                'power': 0.5,
                'energy': 'neutral',
                'market_effect': 'stable',
                'angle': phase_angle
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_voc_periods(self, date: datetime) -> Dict:
        """Calculate Void-of-Course Moon periods"""
        try:
            # Simplified VOC calculation
            # In reality, this requires complex aspect calculations
            
            # Simulate VOC based on lunar day cycle
            lunar_day = (date.timetuple().tm_yday % 28) + 1
            
            # Estimate VOC duration based on lunar day
            if lunar_day in [7, 14, 21, 28]:  # Quarter moon days
                voc_duration = np.random.uniform(6, 12)  # Longer VOC
                voc_intensity = 'high'
            elif lunar_day in [3, 10, 17, 24]:
                voc_duration = np.random.uniform(2, 6)   # Medium VOC
                voc_intensity = 'medium'
            else:
                voc_duration = np.random.uniform(0.5, 3) # Short VOC
                voc_intensity = 'low'
            
            # Determine VOC category
            if voc_duration < 2:
                voc_category = 'short'
            elif voc_duration < 8:
                voc_category = 'medium'
            elif voc_duration < 24:
                voc_category = 'long'
            else:
                voc_category = 'very_long'
            
            voc_data = self.voc_effects[voc_category]
            
            return {
                'is_voc': voc_duration > 1,
                'duration_hours': voc_duration,
                'category': voc_category,
                'market_impact': voc_data['market_impact'],
                'trading_advice': voc_data['trading_advice'],
                'intensity': voc_intensity
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_eclipse_proximity(self, date: datetime) -> Dict:
        """Analyze proximity to eclipse events"""
        try:
            # Simplified eclipse calculation
            # In practice, would use precise ephemeris data
            
            # Eclipse cycles are approximately every 6 months
            days_since_epoch = (date - datetime(2020, 1, 1)).days
            eclipse_cycle_position = (days_since_epoch % 177) / 177  # ~6 month cycle
            
            # Determine eclipse proximity
            if eclipse_cycle_position < 0.1 or eclipse_cycle_position > 0.9:
                eclipse_proximity = 'very_close'
                volatility_multiplier = 1.5
            elif eclipse_cycle_position < 0.2 or eclipse_cycle_position > 0.8:
                eclipse_proximity = 'close'
                volatility_multiplier = 1.3
            elif eclipse_cycle_position < 0.3 or eclipse_cycle_position > 0.7:
                eclipse_proximity = 'moderate'
                volatility_multiplier = 1.1
            else:
                eclipse_proximity = 'distant'
                volatility_multiplier = 1.0
            
            return {
                'eclipse_proximity': eclipse_proximity,
                'cycle_position': eclipse_cycle_position,
                'volatility_multiplier': volatility_multiplier,
                'days_to_next_eclipse': int((1 - eclipse_cycle_position) * 177)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_lunar_node_position(self, date: datetime) -> Dict:
        """Calculate lunar node position and cycle"""
        try:
            # Lunar node cycle is approximately 18.6 years
            days_since_epoch = (date - datetime(2020, 1, 1)).days
            node_cycle_days = 18.6 * 365.25
            node_position = (days_since_epoch % node_cycle_days) / node_cycle_days
            
            # Determine if ascending or descending node is prominent
            if node_position < 0.5:
                dominant_node = 'ascending_node'
                node_strength = 1 - (node_position * 2)
            else:
                dominant_node = 'descending_node'
                node_strength = (node_position - 0.5) * 2
            
            node_data = self.lunar_node_cycle[dominant_node]
            
            return {
                'dominant_node': dominant_node,
                'node_strength': node_strength,
                'cycle_position': node_position,
                'energy_type': node_data['energy'],
                'market_bias': node_data['market_bias']
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_tidal_coefficient(self, features: Dict) -> Dict:
        """Calculate tidal coefficient and market correlation"""
        try:
            moon_phase_angle = features.get('moon_phase_angle', 180)
            moon_distance = features.get('moon_distance_km', 384400)
            
            # Simplified tidal coefficient calculation
            # Real calculation involves Sun-Moon-Earth gravitational interaction
            
            # Phase component (spring vs neap tides)
            if 160 <= moon_phase_angle <= 200 or moon_phase_angle <= 20 or moon_phase_angle >= 340:
                phase_component = 1.0  # Spring tides (new/full moon)
            elif 80 <= moon_phase_angle <= 100 or 260 <= moon_phase_angle <= 280:
                phase_component = 0.5  # Neap tides (quarter moons)
            else:
                phase_component = 0.7  # Intermediate
            
            # Distance component (closer moon = stronger tides)
            distance_component = (400000 / moon_distance) ** 3  # Inverse cube law
            
            # Combined tidal coefficient (0-120 scale)
            tidal_coefficient = phase_component * distance_component * 100
            
            # Determine tidal category
            if 100 <= tidal_coefficient <= 120:
                tidal_category = 'extreme_tides'
            elif 80 <= tidal_coefficient < 100:
                tidal_category = 'spring_tides'
            else:
                tidal_category = 'neap_tides'
            
            tidal_data = self.tidal_finance_theory[tidal_category]
            
            return {
                'coefficient': tidal_coefficient,
                'category': tidal_category,
                'volatility_multiplier': tidal_data['volatility_multiplier'],
                'liquidity_effect': tidal_data['liquidity_effect'],
                'phase_component': phase_component,
                'distance_component': distance_component
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_moon_market_correlation(self, features: Dict) -> Dict:
        """Calculate comprehensive moon-market correlation"""
        try:
            # Combine all lunar factors
            moon_phase = features.get('moon_phase', {})
            lunar_mansion = features.get('lunar_mansion', {})
            voc_moon = features.get('voc_moon', {})
            eclipse_influence = features.get('eclipse_influence', {})
            tidal_coefficient = features.get('tidal_coefficient', {})
            
            # Base correlation strength
            correlation_strength = 1.0
            
            # Moon phase correlation
            phase_power = moon_phase.get('power', 0.5)
            correlation_strength *= (0.5 + phase_power * 0.5)
            
            # Mansion volatility effect
            volatility_level = lunar_mansion.get('volatility_level', 'medium')
            volatility_multipliers = {
                'very_low': 0.8, 'low': 0.9, 'medium': 1.0, 
                'high': 1.1, 'very_high': 1.2
            }
            correlation_strength *= volatility_multipliers.get(volatility_level, 1.0)
            
            # VOC impact
            if voc_moon.get('is_voc', False):
                voc_impact = voc_moon.get('market_impact', 0)
                correlation_strength *= (1 - voc_impact * 0.3)
            
            # Eclipse amplification
            eclipse_multiplier = eclipse_influence.get('volatility_multiplier', 1.0)
            correlation_strength *= eclipse_multiplier
            
            # Tidal amplification
            tidal_multiplier = tidal_coefficient.get('volatility_multiplier', 1.0)
            correlation_strength *= tidal_multiplier
            
            # Calculate market sentiment
            energy_type = moon_phase.get('energy', 'neutral')
            market_effect = moon_phase.get('market_effect', 'stable')
            
            sentiment_score = 50  # Neutral
            if market_effect in ['bullish_momentum', 'breakout', 'trend_start']:
                sentiment_score += 20
            elif market_effect in ['bearish_momentum', 'correction']:
                sentiment_score -= 20
            elif market_effect in ['high_volatility', 'accumulation']:
                sentiment_score += 10
            
            return {
                'correlation_strength': max(0.5, min(1.5, correlation_strength)),
                'market_sentiment_score': max(0, min(100, sentiment_score)),
                'energy_type': energy_type,
                'market_effect': market_effect,
                'composite_lunar_power': phase_power * correlation_strength
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _score_moon_phase(self, phase_data: Dict) -> float:
        """Score based on moon phase power and energy"""
        if not phase_data or 'error' in phase_data:
            return 50.0
        
        phase_power = phase_data.get('power', 0.5)
        market_effect = phase_data.get('market_effect', 'stable')
        
        # Base score from phase power
        score = 30 + (phase_power * 40)  # 30-70 range
        
        # Market effect adjustments
        effect_bonuses = {
            'new_beginnings': 15, 'trend_start': 12, 'bullish_momentum': 10,
            'breakout': 8, 'high_volatility': -5, 'correction': -8,
            'bearish_momentum': -10, 'accumulation': 5
        }
        
        score += effect_bonuses.get(market_effect, 0)
        
        return max(0, min(100, score))
    
    def _score_lunar_mansion(self, mansion_data: Dict) -> float:
        """Score based on lunar mansion characteristics"""
        if not mansion_data or 'error' in mansion_data:
            return 50.0
        
        score = 50.0
        
        # Volatility level impact
        volatility_level = mansion_data.get('volatility_level', 'medium')
        volatility_scores = {
            'very_low': 75, 'low': 65, 'medium': 50, 
            'high': 40, 'very_high': 30
        }
        
        score = volatility_scores.get(volatility_level, 50)
        
        # Energy type adjustments
        energy_type = mansion_data.get('energy_type', 'neutral')
        energy_bonuses = {
            'growth': 10, 'prosperity': 15, 'achievement': 8,
            'nourishment': 12, 'transformation': -5, 'destruction': -15
        }
        
        score += energy_bonuses.get(energy_type, 0)
        
        return max(0, min(100, score))
    
    def _score_voc_periods(self, voc_data: Dict) -> float:
        """Score based on Void-of-Course periods"""
        if not voc_data or 'error' in voc_data:
            return 50.0
        
        score = 50.0
        
        if voc_data.get('is_voc', False):
            market_impact = voc_data.get('market_impact', 0)
            score -= market_impact * 30  # Reduce score during VOC
            
            # Additional penalty for longer VOC periods
            category = voc_data.get('category', 'short')
            category_penalties = {
                'short': 0, 'medium': 5, 'long': 15, 'very_long': 25
            }
            score -= category_penalties.get(category, 0)
        else:
            score += 10  # Bonus for not being in VOC
        
        return max(0, min(100, score))
    
    def _score_eclipse_influence(self, eclipse_data: Dict) -> float:
        """Score based on eclipse proximity"""
        if not eclipse_data or 'error' in eclipse_data:
            return 50.0
        
        score = 50.0
        
        proximity = eclipse_data.get('eclipse_proximity', 'distant')
        volatility_multiplier = eclipse_data.get('volatility_multiplier', 1.0)
        
        # Eclipse proximity effects
        proximity_effects = {
            'very_close': -20, 'close': -10, 'moderate': -5, 'distant': 5
        }
        
        score += proximity_effects.get(proximity, 0)
        
        # Volatility multiplier effect
        score *= (2 - volatility_multiplier)  # Inverse relationship
        
        return max(0, min(100, score))
    
    def _score_tidal_coefficient(self, tidal_data: Dict) -> float:
        """Score based on tidal coefficient"""
        if not tidal_data or 'error' in tidal_data:
            return 50.0
        
        score = 50.0
        
        category = tidal_data.get('category', 'neap_tides')
        volatility_multiplier = tidal_data.get('volatility_multiplier', 1.0)
        
        # Tidal category effects
        category_effects = {
            'neap_tides': 10,      # Stable, low volatility
            'spring_tides': -5,    # Higher volatility
            'extreme_tides': -15   # Very high volatility
        }
        
        score += category_effects.get(category, 0)
        
        # Liquidity effect
        liquidity_effect = tidal_data.get('liquidity_effect', 'low')
        if liquidity_effect == 'high':
            score += 5
        elif liquidity_effect == 'extreme':
            score -= 5
        
        return max(0, min(100, score))
