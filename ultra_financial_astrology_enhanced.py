# -*- coding: utf-8 -*-
"""
PlanB Motoru - Ultra Financial Astrology Enhanced Analysis Module
Professional Financial Astrology - Expert Level
Planetary Transits, Aspects, Retrograde Effects, Harmonics, Heliocentric Analysis
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


class UltraFinancialAstrologyModule(ExpertModule):
    """Ultra Financial Astrology Enhanced - Professional Financial Astrology Analysis"""
    
    def __init__(self, module_name: str = "Ultra Financial Astrology Enhanced"):
        super().__init__(module_name)
        super().__init__(module_name)
        
        # Professional planetary definitions for financial analysis
        self.planets = {
            'sun': {'ephem_func': ephem.Sun, 'financial_weight': 0.08, 'keywords': ['vitality', 'leadership', 'government']},
            'moon': {'ephem_func': ephem.Moon, 'financial_weight': 0.12, 'keywords': ['emotions', 'public', 'liquidity']},
            'mercury': {'ephem_func': ephem.Mercury, 'financial_weight': 0.15, 'keywords': ['communication', 'trade', 'technology']},
            'venus': {'ephem_func': ephem.Venus, 'financial_weight': 0.18, 'keywords': ['values', 'luxury', 'currencies']},
            'mars': {'ephem_func': ephem.Mars, 'financial_weight': 0.20, 'keywords': ['energy', 'volatility', 'commodities']},
            'jupiter': {'ephem_func': ephem.Jupiter, 'financial_weight': 0.25, 'keywords': ['expansion', 'optimism', 'banks']},
            'saturn': {'ephem_func': ephem.Saturn, 'financial_weight': 0.23, 'keywords': ['structure', 'discipline', 'real_estate']},
            'uranus': {'ephem_func': ephem.Uranus, 'financial_weight': 0.15, 'keywords': ['innovation', 'disruption', 'crypto']},
            'neptune': {'ephem_func': ephem.Neptune, 'financial_weight': 0.12, 'keywords': ['illusion', 'oil', 'pharmaceuticals']},
            'pluto': {'ephem_func': ephem.Pluto, 'financial_weight': 0.18, 'keywords': ['transformation', 'power', 'mining']}
        }
        
        # Major astrological aspects with market interpretation
        self.major_aspects = {
            'conjunction': {'angle': 0, 'orb': 8, 'nature': 'neutral', 'intensity': 1.0, 'market_effect': 'concentration'},
            'sextile': {'angle': 60, 'orb': 6, 'nature': 'harmonious', 'intensity': 0.6, 'market_effect': 'opportunity'},
            'square': {'angle': 90, 'orb': 8, 'nature': 'tension', 'intensity': 0.8, 'market_effect': 'volatility'},
            'trine': {'angle': 120, 'orb': 8, 'nature': 'harmonious', 'intensity': 0.7, 'market_effect': 'flow'},
            'opposition': {'angle': 180, 'orb': 8, 'nature': 'tension', 'intensity': 0.9, 'market_effect': 'polarity'}
        }
        
        # Minor aspects for fine-tuning
        self.minor_aspects = {
            'semisextile': {'angle': 30, 'orb': 2, 'nature': 'minor_harmonious', 'intensity': 0.3},
            'semisquare': {'angle': 45, 'orb': 2, 'nature': 'minor_tension', 'intensity': 0.4},
            'quintile': {'angle': 72, 'orb': 2, 'nature': 'creative', 'intensity': 0.5},
            'sesquiquadrate': {'angle': 135, 'orb': 2, 'nature': 'minor_tension', 'intensity': 0.4},
            'quincunx': {'angle': 150, 'orb': 3, 'nature': 'adjustment', 'intensity': 0.5}
        }
        
        # Zodiac signs with financial sector correlations
        self.zodiac_signs = {
            'aries': {'element': 'fire', 'quality': 'cardinal', 'ruler': 'mars', 'sectors': ['military', 'sports', 'startups']},
            'taurus': {'element': 'earth', 'quality': 'fixed', 'ruler': 'venus', 'sectors': ['banking', 'real_estate', 'agriculture']},
            'gemini': {'element': 'air', 'quality': 'mutable', 'ruler': 'mercury', 'sectors': ['media', 'transportation', 'telecom']},
            'cancer': {'element': 'water', 'quality': 'cardinal', 'ruler': 'moon', 'sectors': ['food', 'housing', 'utilities']},
            'leo': {'element': 'fire', 'quality': 'fixed', 'ruler': 'sun', 'sectors': ['entertainment', 'luxury', 'gold']},
            'virgo': {'element': 'earth', 'quality': 'mutable', 'ruler': 'mercury', 'sectors': ['healthcare', 'services', 'analytics']},
            'libra': {'element': 'air', 'quality': 'cardinal', 'ruler': 'venus', 'sectors': ['law', 'beauty', 'partnerships']},
            'scorpio': {'element': 'water', 'quality': 'fixed', 'ruler': 'pluto', 'sectors': ['insurance', 'research', 'resources']},
            'sagittarius': {'element': 'fire', 'quality': 'mutable', 'ruler': 'jupiter', 'sectors': ['education', 'travel', 'publishing']},
            'capricorn': {'element': 'earth', 'quality': 'cardinal', 'ruler': 'saturn', 'sectors': ['government', 'infrastructure', 'time']},
            'aquarius': {'element': 'air', 'quality': 'fixed', 'ruler': 'uranus', 'sectors': ['technology', 'innovation', 'social']},
            'pisces': {'element': 'water', 'quality': 'mutable', 'ruler': 'neptune', 'sectors': ['oil', 'pharmaceuticals', 'music']}
        }
        
        # Financial houses system (market-focused)
        self.financial_houses = {
            1: {'theme': 'market_identity', 'strength': 'high'},
            2: {'theme': 'values_resources', 'strength': 'very_high'},
            3: {'theme': 'communication_trade', 'strength': 'medium'},
            4: {'theme': 'foundation_real_estate', 'strength': 'high'},
            5: {'theme': 'speculation_risk', 'strength': 'high'},
            6: {'theme': 'work_services', 'strength': 'medium'},
            7: {'theme': 'partnerships_contracts', 'strength': 'high'},
            8: {'theme': 'shared_resources_debt', 'strength': 'very_high'},
            9: {'theme': 'international_expansion', 'strength': 'medium'},
            10: {'theme': 'reputation_leadership', 'strength': 'high'},
            11: {'theme': 'networks_innovation', 'strength': 'medium'},
            12: {'theme': 'hidden_factors_dissolution', 'strength': 'medium'}
        }
        
        # Retrograde effects on different market sectors
        self.retrograde_effects = {
            'mercury': {'frequency_days': 88, 'duration_days': 24, 'sectors': ['technology', 'communication', 'transport']},
            'venus': {'frequency_days': 225, 'duration_days': 42, 'sectors': ['luxury', 'art', 'currencies']},
            'mars': {'frequency_days': 687, 'duration_days': 58, 'sectors': ['energy', 'defense', 'commodities']},
            'jupiter': {'frequency_days': 399, 'duration_days': 120, 'sectors': ['finance', 'education', 'travel']},
            'saturn': {'frequency_days': 378, 'duration_days': 138, 'sectors': ['real_estate', 'mining', 'government']},
            'uranus': {'frequency_days': 371, 'duration_days': 151, 'sectors': ['technology', 'innovation', 'crypto']},
            'neptune': {'frequency_days': 367, 'duration_days': 158, 'sectors': ['oil', 'pharmaceuticals', 'entertainment']},
            'pluto': {'frequency_days': 366, 'duration_days': 160, 'sectors': ['mining', 'insurance', 'transformation']}
        }
        
        # Harmonic analysis (advanced astrology)
        self.harmonic_series = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 18, 24, 36]
        
        logger.info("Ultra Financial Astrology Enhanced Module initialized with professional financial astrology")
    
    def prepare_features(self, data: Dict) -> Dict:
        """Astroloji analizi için özellikleri hazırla"""
        try:
            symbol = data.get('symbol', 'UNKNOWN')
            current_date = datetime.now()
            
            # Calculate all planetary positions
            features = self._calculate_planetary_positions(current_date)
            
            # Add context
            features['symbol'] = symbol
            features['analysis_date'] = current_date
            
            # Calculate major planetary aspects
            features['major_aspects'] = self._calculate_major_aspects(features['planetary_positions'])
            
            # Calculate minor aspects for precision
            features['minor_aspects'] = self._calculate_minor_aspects(features['planetary_positions'])
            
            # Retrograde analysis
            features['retrograde_planets'] = self._analyze_retrograde_planets(current_date)
            
            # Current transits analysis
            features['current_transits'] = self._analyze_current_transits(features['planetary_positions'])
            
            # Harmonic analysis
            features['harmonic_patterns'] = self._calculate_harmonic_patterns(features['planetary_positions'])
            
            # Financial sector analysis
            features['sector_influences'] = self._analyze_sector_influences(features)
            
            # Market timing analysis
            features['market_timing'] = self._calculate_market_timing(features)
            
            return features
            
        except Exception as e:
            logger.error(f"Astrology feature preparation error: {e}")
            return {'error': str(e)}
    
    def infer(self, features: Dict) -> Tuple[float, float]:
        """Astroloji analizi inference"""
        try:
            if 'error' in features:
                return 50.0, 0.8
            
            base_score = 50.0
            uncertainty = 0.6
            
            # 1. Major Aspects scoring (30% weight)
            aspects_score = self._score_major_aspects(features.get('major_aspects', []))
            
            # 2. Planetary Transits scoring (25% weight)
            transits_score = self._score_current_transits(features.get('current_transits', {}))
            
            # 3. Retrograde Effects scoring (20% weight)
            retrograde_score = self._score_retrograde_effects(features.get('retrograde_planets', []))
            
            # 4. Harmonic Patterns scoring (15% weight)
            harmonic_score = self._score_harmonic_patterns(features.get('harmonic_patterns', {}))
            
            # 5. Market Timing scoring (10% weight)
            timing_score = self._score_market_timing(features.get('market_timing', {}))
            
            # Weighted combination
            final_score = (
                aspects_score * 0.30 +
                transits_score * 0.25 +
                retrograde_score * 0.20 +
                harmonic_score * 0.15 +
                timing_score * 0.10
            )
            
            # Dynamic uncertainty based on aspect strength
            total_aspects = len(features.get('major_aspects', [])) + len(features.get('minor_aspects', []))
            aspect_density = min(total_aspects / 10, 1.0)  # Normalize to 0-1
            uncertainty = max(0.2, 0.8 - aspect_density * 0.4)
            
            # Clamp to valid range
            final_score = max(0, min(100, final_score))
            
            self.confidence_level = 1.0 - uncertainty
            
            logger.info(f"Financial astrology analysis completed: {final_score:.2f} (uncertainty: {uncertainty:.3f})")
            return final_score, uncertainty
            
        except Exception as e:
            logger.error(f"Astrology inference error: {e}")
            return 50.0, 0.8
    
    def retrain(self, data: Dict) -> None:
        """Astrology model retraining (astronomical data is constant)"""
        logger.info("Financial astrology module: Astronomical calculations are constant, no retraining needed")
        pass
    
    def _calculate_planetary_positions(self, date: datetime) -> Dict:
        """Calculate precise planetary positions"""
        try:
            # Create observer (Istanbul for Turkish market)
            observer = ephem.Observer()
            observer.lat = '41.0082'   # Istanbul latitude
            observer.lon = '28.9784'   # Istanbul longitude
            observer.date = date
            
            planetary_positions = {}
            
            for planet_name, planet_data in self.planets.items():
                try:
                    planet = planet_data['ephem_func'](observer)
                    
                    # Get position in degrees
                    longitude = float(planet.hlon) * 180 / math.pi
                    latitude = float(planet.hlat) * 180 / math.pi if hasattr(planet, 'hlat') else 0
                    
                    # Determine zodiac sign
                    sign_number = int(longitude / 30) + 1
                    sign_degree = longitude % 30
                    sign_names = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
                                 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
                    current_sign = sign_names[(sign_number - 1) % 12]
                    
                    # Determine house (simplified)
                    house_number = ((longitude + 90) % 360) / 30 + 1  # Simplified house calculation
                    
                    planetary_positions[planet_name] = {
                        'longitude': longitude,
                        'latitude': latitude,
                        'sign': current_sign,
                        'sign_degree': sign_degree,
                        'house': int(house_number),
                        'financial_weight': planet_data['financial_weight'],
                        'keywords': planet_data['keywords']
                    }
                    
                except Exception as e:
                    logger.warning(f"Error calculating {planet_name}: {e}")
                    continue
            
            return {
                'planetary_positions': planetary_positions,
                'calculation_date': date,
                'observer_location': 'Istanbul',
                'total_planets': len(planetary_positions)
            }
            
        except Exception as e:
            logger.error(f"Planetary positions calculation error: {e}")
            return {'error': str(e)}
    
    def _calculate_major_aspects(self, planetary_positions: Dict) -> List[Dict]:
        """Calculate major planetary aspects"""
        try:
            aspects = []
            planet_list = list(planetary_positions.keys())
            
            for i, planet1 in enumerate(planet_list):
                for planet2 in planet_list[i+1:]:
                    pos1 = planetary_positions[planet1]['longitude']
                    pos2 = planetary_positions[planet2]['longitude']
                    
                    # Calculate angular separation
                    separation = abs(pos1 - pos2)
                    separation = min(separation, 360 - separation)
                    
                    # Check for major aspects
                    for aspect_name, aspect_data in self.major_aspects.items():
                        target_angle = aspect_data['angle']
                        orb = aspect_data['orb']
                        
                        if abs(separation - target_angle) <= orb:
                            exactness = 1 - (abs(separation - target_angle) / orb)
                            
                            # Calculate aspect strength
                            weight1 = planetary_positions[planet1]['financial_weight']
                            weight2 = planetary_positions[planet2]['financial_weight']
                            aspect_strength = (weight1 + weight2) * aspect_data['intensity'] * exactness
                            
                            aspects.append({
                                'planet1': planet1,
                                'planet2': planet2,
                                'aspect': aspect_name,
                                'exact_angle': separation,
                                'target_angle': target_angle,
                                'orb_difference': abs(separation - target_angle),
                                'exactness': exactness,
                                'strength': aspect_strength,
                                'nature': aspect_data['nature'],
                                'market_effect': aspect_data['market_effect']
                            })
            
            # Sort by strength
            aspects.sort(key=lambda x: x['strength'], reverse=True)
            return aspects
            
        except Exception as e:
            logger.error(f"Major aspects calculation error: {e}")
            return []
    
    def _calculate_minor_aspects(self, planetary_positions: Dict) -> List[Dict]:
        """Calculate minor planetary aspects for precision"""
        try:
            minor_aspects = []
            planet_list = list(planetary_positions.keys())
            
            for i, planet1 in enumerate(planet_list):
                for planet2 in planet_list[i+1:]:
                    pos1 = planetary_positions[planet1]['longitude']
                    pos2 = planetary_positions[planet2]['longitude']
                    
                    separation = abs(pos1 - pos2)
                    separation = min(separation, 360 - separation)
                    
                    # Check for minor aspects
                    for aspect_name, aspect_data in self.minor_aspects.items():
                        target_angle = aspect_data['angle']
                        orb = aspect_data['orb']
                        
                        if abs(separation - target_angle) <= orb:
                            exactness = 1 - (abs(separation - target_angle) / orb)
                            
                            weight1 = planetary_positions[planet1]['financial_weight']
                            weight2 = planetary_positions[planet2]['financial_weight']
                            aspect_strength = (weight1 + weight2) * aspect_data['intensity'] * exactness
                            
                            minor_aspects.append({
                                'planet1': planet1,
                                'planet2': planet2,
                                'aspect': aspect_name,
                                'strength': aspect_strength,
                                'exactness': exactness,
                                'nature': aspect_data['nature']
                            })
            
            return minor_aspects
            
        except Exception as e:
            return []
    
    def _analyze_retrograde_planets(self, date: datetime) -> List[Dict]:
        """Analyze current retrograde planets"""
        try:
            retrograde_planets = []
            
            for planet_name, retrograde_data in self.retrograde_effects.items():
                if planet_name in ['sun', 'moon']:
                    continue  # Sun and Moon don't go retrograde
                
                # Simplified retrograde calculation
                planet_func = self.planets[planet_name]['ephem_func']
                
                try:
                    # Calculate planet position for today and yesterday
                    observer = ephem.Observer()
                    observer.date = date
                    planet_today = planet_func(observer)
                    
                    observer.date = date - timedelta(days=1)
                    planet_yesterday = planet_func(observer)
                    
                    # Check if longitude decreased (retrograde motion)
                    lon_today = float(planet_today.hlon)
                    lon_yesterday = float(planet_yesterday.hlon)
                    
                    # Handle longitude wrap-around
                    if abs(lon_today - lon_yesterday) > math.pi:
                        if lon_today < lon_yesterday:
                            lon_today += 2 * math.pi
                        else:
                            lon_yesterday += 2 * math.pi
                    
                    if lon_today < lon_yesterday:
                        # Planet is retrograde
                        financial_weight = self.planets[planet_name]['financial_weight']
                        affected_sectors = retrograde_data['sectors']
                        
                        retrograde_planets.append({
                            'planet': planet_name,
                            'financial_weight': financial_weight,
                            'affected_sectors': affected_sectors,
                            'typical_duration_days': retrograde_data['duration_days'],
                            'impact_strength': financial_weight * 0.7  # Retrograde reduces effectiveness
                        })
                        
                except Exception as e:
                    logger.warning(f"Retrograde calculation error for {planet_name}: {e}")
                    continue
            
            return retrograde_planets
            
        except Exception as e:
            logger.error(f"Retrograde analysis error: {e}")
            return []
    
    def _analyze_current_transits(self, planetary_positions: Dict) -> Dict:
        """Analyze current planetary transits"""
        try:
            transits = {
                'fire_signs': [], 'earth_signs': [], 'air_signs': [], 'water_signs': [],
                'cardinal_signs': [], 'fixed_signs': [], 'mutable_signs': [],
                'financial_houses': []
            }
            
            for planet_name, position_data in planetary_positions.items():
                current_sign = position_data['sign']
                current_house = position_data['house']
                financial_weight = position_data['financial_weight']
                
                # Element analysis
                sign_data = self.zodiac_signs[current_sign]
                element = sign_data['element']
                quality = sign_data['quality']
                
                transits[f'{element}_signs'].append({
                    'planet': planet_name,
                    'sign': current_sign,
                    'weight': financial_weight,
                    'sectors': sign_data['sectors']
                })
                
                transits[f'{quality}_signs'].append({
                    'planet': planet_name,
                    'sign': current_sign,
                    'weight': financial_weight
                })
                
                # House analysis
                if current_house in self.financial_houses:
                    house_data = self.financial_houses[current_house]
                    transits['financial_houses'].append({
                        'planet': planet_name,
                        'house': current_house,
                        'theme': house_data['theme'],
                        'strength': house_data['strength'],
                        'weight': financial_weight
                    })
            
            # Calculate elemental balance
            element_strengths = {}
            for element in ['fire', 'earth', 'air', 'water']:
                total_weight = sum(p['weight'] for p in transits[f'{element}_signs'])
                element_strengths[element] = total_weight
            
            transits['elemental_balance'] = element_strengths
            
            return transits
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_harmonic_patterns(self, planetary_positions: Dict) -> Dict:
        """Calculate harmonic astrological patterns"""
        try:
            harmonic_patterns = {}
            
            # Get all planetary longitudes
            longitudes = [pos['longitude'] for pos in planetary_positions.values()]
            
            for harmonic in self.harmonic_series:
                # Calculate harmonic chart positions
                harmonic_positions = [(lon * harmonic) % 360 for lon in longitudes]
                
                # Look for clusters in harmonic chart
                clusters = self._find_harmonic_clusters(harmonic_positions)
                
                if clusters:
                    harmonic_patterns[f'harmonic_{harmonic}'] = {
                        'clusters': clusters,
                        'strength': sum(cluster['strength'] for cluster in clusters),
                        'market_significance': self._interpret_harmonic_market_effect(harmonic, clusters)
                    }
            
            return harmonic_patterns
            
        except Exception as e:
            return {'error': str(e)}
    
    def _find_harmonic_clusters(self, positions: List[float]) -> List[Dict]:
        """Find clusters in harmonic positions"""
        clusters = []
        cluster_threshold = 15  # degrees
        
        for i, pos1 in enumerate(positions):
            cluster_positions = [pos1]
            
            for j, pos2 in enumerate(positions[i+1:], i+1):
                # Calculate minimum separation (considering 360-degree wrap)
                separation = min(abs(pos1 - pos2), 360 - abs(pos1 - pos2))
                
                if separation <= cluster_threshold:
                    cluster_positions.append(pos2)
            
            if len(cluster_positions) >= 3:  # At least 3 planets in cluster
                cluster_center = np.mean(cluster_positions) % 360
                cluster_strength = len(cluster_positions) / len(positions)
                
                clusters.append({
                    'center_degree': cluster_center,
                    'planet_count': len(cluster_positions),
                    'strength': cluster_strength,
                    'positions': cluster_positions
                })
        
        return clusters
    
    def _interpret_harmonic_market_effect(self, harmonic: int, clusters: List[Dict]) -> str:
        """Interpret harmonic patterns for market effects"""
        harmonic_meanings = {
            2: 'polarity_dynamics', 3: 'creative_tension', 4: 'stability_structure',
            5: 'innovation_creativity', 6: 'harmony_balance', 7: 'spiritual_transformation',
            8: 'material_manifestation', 9: 'completion_mastery', 10: 'worldly_success',
            11: 'intuitive_breakthrough', 12: 'comprehensive_integration'
        }
        
        return harmonic_meanings.get(harmonic, 'complex_pattern')
    
    def _analyze_sector_influences(self, features: Dict) -> Dict:
        """Analyze planetary influences on market sectors"""
        try:
            sector_influences = {}
            planetary_positions = features.get('planetary_positions', {})
            
            # Initialize sector influence tracker
            all_sectors = set()
            for planet_data in planetary_positions.values():
                sign = planet_data['sign']
                if sign in self.zodiac_signs:
                    all_sectors.update(self.zodiac_signs[sign]['sectors'])
            
            for sector in all_sectors:
                sector_influences[sector] = {'total_influence': 0, 'contributing_planets': []}
            
            # Calculate influences
            for planet_name, position_data in planetary_positions.items():
                sign = position_data['sign']
                weight = position_data['financial_weight']
                
                if sign in self.zodiac_signs:
                    sign_sectors = self.zodiac_signs[sign]['sectors']
                    
                    for sector in sign_sectors:
                        sector_influences[sector]['total_influence'] += weight
                        sector_influences[sector]['contributing_planets'].append({
                            'planet': planet_name,
                            'contribution': weight
                        })
            
            # Sort sectors by influence
            sorted_sectors = sorted(sector_influences.items(), 
                                  key=lambda x: x[1]['total_influence'], reverse=True)
            
            return {
                'sector_rankings': sorted_sectors[:10],  # Top 10 sectors
                'total_sectors_analyzed': len(all_sectors),
                'strongest_sector': sorted_sectors[0] if sorted_sectors else None
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_market_timing(self, features: Dict) -> Dict:
        """Calculate astrological market timing indicators"""
        try:
            timing_indicators = {}
            
            # Major aspects timing
            major_aspects = features.get('major_aspects', [])
            harmonious_aspects = [a for a in major_aspects if a['nature'] in ['harmonious', 'neutral']]
            tension_aspects = [a for a in major_aspects if a['nature'] == 'tension']
            
            timing_indicators['aspect_balance'] = {
                'harmonious_count': len(harmonious_aspects),
                'tension_count': len(tension_aspects),
                'balance_ratio': len(harmonious_aspects) / max(len(tension_aspects), 1),
                'recommendation': 'bullish' if len(harmonious_aspects) > len(tension_aspects) else 'bearish'
            }
            
            # Retrograde timing
            retrograde_planets = features.get('retrograde_planets', [])
            timing_indicators['retrograde_caution'] = {
                'retrograde_count': len(retrograde_planets),
                'caution_level': 'high' if len(retrograde_planets) >= 3 else 'medium' if len(retrograde_planets) >= 1 else 'low'
            }
            
            # Elemental timing
            current_transits = features.get('current_transits', {})
            elemental_balance = current_transits.get('elemental_balance', {})
            dominant_element = max(elemental_balance, key=elemental_balance.get) if elemental_balance else 'earth'
            
            element_timing = {
                'fire': 'aggressive_growth', 'earth': 'steady_accumulation',
                'air': 'communication_driven', 'water': 'sentiment_based'
            }
            
            timing_indicators['elemental_timing'] = {
                'dominant_element': dominant_element,
                'market_approach': element_timing.get(dominant_element, 'balanced'),
                'elemental_distribution': elemental_balance
            }
            
            return timing_indicators
            
        except Exception as e:
            return {'error': str(e)}
    
    def _score_major_aspects(self, aspects: List[Dict]) -> float:
        """Score based on major planetary aspects"""
        if not aspects:
            return 50.0
        
        score = 50.0
        
        for aspect in aspects[:5]:  # Top 5 strongest aspects
            strength = aspect.get('strength', 0)
            nature = aspect.get('nature', 'neutral')
            
            if nature == 'harmonious':
                score += strength * 15
            elif nature == 'tension':
                score -= strength * 10
            else:  # neutral
                score += strength * 5
        
        return max(0, min(100, score))
    
    def _score_current_transits(self, transits: Dict) -> float:
        """Score based on current planetary transits"""
        if not transits or 'error' in transits:
            return 50.0
        
        score = 50.0
        
        # Elemental balance scoring
        elemental_balance = transits.get('elemental_balance', {})
        if elemental_balance:
            earth_strength = elemental_balance.get('earth', 0)
            fire_strength = elemental_balance.get('fire', 0)
            
            # Earth = stability, Fire = growth
            score += earth_strength * 8 + fire_strength * 12
        
        # Financial houses scoring
        financial_houses = transits.get('financial_houses', [])
        for house_transit in financial_houses:
            strength = house_transit.get('strength', 'medium')
            weight = house_transit.get('weight', 0)
            
            strength_multipliers = {'very_high': 2.0, 'high': 1.5, 'medium': 1.0}
            score += weight * 10 * strength_multipliers.get(strength, 1.0)
        
        return max(0, min(100, score))
    
    def _score_retrograde_effects(self, retrograde_planets: List[Dict]) -> float:
        """Score based on retrograde planetary effects"""
        score = 50.0
        
        for retro_planet in retrograde_planets:
            impact_strength = retro_planet.get('impact_strength', 0)
            score -= impact_strength * 20  # Retrograde generally reduces market confidence
        
        return max(0, min(100, score))
    
    def _score_harmonic_patterns(self, harmonic_patterns: Dict) -> float:
        """Score based on harmonic astrological patterns"""
        if not harmonic_patterns or 'error' in harmonic_patterns:
            return 50.0
        
        score = 50.0
        
        for pattern_name, pattern_data in harmonic_patterns.items():
            pattern_strength = pattern_data.get('strength', 0)
            score += pattern_strength * 20  # Harmonic patterns add stability
        
        return max(0, min(100, score))
    
    def _score_market_timing(self, timing_data: Dict) -> float:
        """Score based on astrological market timing"""
        if not timing_data or 'error' in timing_data:
            return 50.0
        
        score = 50.0
        
        # Aspect balance
        aspect_balance = timing_data.get('aspect_balance', {})
        balance_ratio = aspect_balance.get('balance_ratio', 1.0)
        
        if balance_ratio > 1.5:  # More harmonious
            score += 15
        elif balance_ratio < 0.5:  # More tension
            score -= 15
        
        # Retrograde caution
        retrograde_caution = timing_data.get('retrograde_caution', {})
        caution_level = retrograde_caution.get('caution_level', 'low')
        
        caution_penalties = {'low': 0, 'medium': 5, 'high': 15}
        score -= caution_penalties.get(caution_level, 0)
        
        return max(0, min(100, score))
