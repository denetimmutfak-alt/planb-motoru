# -*- coding: utf-8 -*-
"""
PlanB Motoru - Ultra Fibonacci & Elliott Wave Enhanced Analysis Module
Professional Technical Analysis - Expert Level
Fibonacci Retracements, Extensions, Time Zones, Elliott Wave Patterns, Harmonic Patterns
"""

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


class UltraFibonacciElliottModule(ExpertModule):
    """Ultra Fibonacci & Elliott Wave Enhanced - Professional Technical Analysis"""
    
    def __init__(self, module_name: str = "Ultra Fibonacci Elliott Enhanced"):
        super().__init__(module_name)
        super().__init__(module_name)
        
        # Fibonacci ratios - Classic and Extended
        self.fibonacci_ratios = {
            'classic_retracements': [0.236, 0.382, 0.500, 0.618, 0.786],
            'extended_retracements': [0.146, 0.236, 0.382, 0.500, 0.618, 0.702, 0.786, 0.886],
            'extensions': [1.000, 1.272, 1.382, 1.618, 2.000, 2.618, 3.618, 4.236],
            'projections': [0.618, 0.786, 1.000, 1.272, 1.414, 1.618, 2.000, 2.618]
        }
        
        # Elliott Wave patterns and characteristics
        self.elliott_wave_patterns = {
            'impulse_waves': {
                'wave_1': {'fibonacci_relation': 'base', 'characteristics': ['initial_move', 'moderate_volume']},
                'wave_2': {'fibonacci_relation': [0.382, 0.618], 'characteristics': ['correction', 'low_volume']},
                'wave_3': {'fibonacci_relation': [1.618, 2.618], 'characteristics': ['strongest_move', 'high_volume']},
                'wave_4': {'fibonacci_relation': [0.236, 0.382], 'characteristics': ['complex_correction', 'sideways']},
                'wave_5': {'fibonacci_relation': [0.618, 1.000], 'characteristics': ['final_move', 'divergence']}
            },
            'corrective_waves': {
                'zigzag': {'structure': 'A-B-C', 'fibonacci_c': [0.618, 1.000, 1.618]},
                'flat': {'structure': 'A-B-C', 'fibonacci_b': [0.618, 0.786], 'fibonacci_c': [1.000, 1.272]},
                'triangle': {'structure': 'A-B-C-D-E', 'fibonacci_relations': [0.618, 0.786]},
                'complex': {'structure': 'W-X-Y-Z', 'fibonacci_y': [0.618, 1.000, 1.618]}
            }
        }
        
        # Harmonic patterns with Fibonacci relationships
        self.harmonic_patterns = {
            'gartley': {'XA': 0.618, 'AB': [0.382, 0.886], 'BC': [0.382, 0.886], 'CD': [1.13, 1.618]},
            'butterfly': {'XA': 0.786, 'AB': [0.382, 0.886], 'BC': [0.382, 0.886], 'CD': [1.618, 2.618]},
            'bat': {'XA': [0.382, 0.500], 'AB': [0.382, 0.886], 'BC': [0.382, 0.886], 'CD': [1.618, 2.618]},
            'crab': {'XA': [0.382, 0.618], 'AB': [0.382, 0.886], 'BC': [0.382, 0.886], 'CD': [2.24, 3.618]},
            'shark': {'XA': [0.382, 0.618], 'AB': [1.13, 1.618], 'BC': [1.618, 2.24], 'CD': [0.886, 1.13]},
            'cypher': {'XA': [0.382, 0.618], 'AB': [0.382, 0.886], 'BC': [1.13, 1.414], 'CD': [0.786]}
        }
        
        # Fibonacci time zones and cycles
        self.fibonacci_time_cycles = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
        
        # Golden ratio applications
        self.golden_ratio = 1.618033988749
        self.phi_ratios = {
            'phi': 1.618, 'phi_squared': 2.618, 'phi_cubed': 4.236,
            'inverse_phi': 0.618, 'inverse_phi_squared': 0.382, 'sqrt_phi': 1.272
        }
        
        # Wave degree classification
        self.wave_degrees = {
            'supercycle': {'duration_years': [20, 100], 'fibonacci_multiplier': 377},
            'cycle': {'duration_years': [1, 20], 'fibonacci_multiplier': 233},
            'primary': {'duration_months': [2, 24], 'fibonacci_multiplier': 144},
            'intermediate': {'duration_weeks': [2, 52], 'fibonacci_multiplier': 89},
            'minor': {'duration_days': [5, 90], 'fibonacci_multiplier': 55},
            'minute': {'duration_hours': [1, 24], 'fibonacci_multiplier': 34},
            'minuette': {'duration_minutes': [5, 480], 'fibonacci_multiplier': 21}
        }
        
        logger.info("Ultra Fibonacci Elliott Enhanced Module initialized with professional technical analysis")
    
    def prepare_features(self, data: Dict) -> Dict:
        """Fibonacci ve Elliott Wave analizi için özellikleri hazırla"""
        try:
            symbol = data.get('symbol', 'UNKNOWN')
            
            # Generate synthetic price data for analysis
            features = self._create_synthetic_price_data(symbol)
            
            # Add context
            features['symbol'] = symbol
            features['analysis_date'] = datetime.now()
            
            # Fibonacci retracement analysis
            features['fibonacci_retracements'] = self._calculate_fibonacci_retracements(features['price_data'])
            
            # Fibonacci extensions analysis
            features['fibonacci_extensions'] = self._calculate_fibonacci_extensions(features['price_data'])
            
            # Elliott Wave pattern recognition
            features['elliott_wave_analysis'] = self._analyze_elliott_wave_patterns(features['price_data'])
            
            # Harmonic pattern detection
            features['harmonic_patterns'] = self._detect_harmonic_patterns(features['price_data'])
            
            # Fibonacci time analysis
            features['fibonacci_time_zones'] = self._calculate_fibonacci_time_zones(features['price_data'])
            
            # Golden ratio cluster analysis
            features['golden_ratio_clusters'] = self._analyze_golden_ratio_clusters(features)
            
            # Market structure analysis
            features['market_structure'] = self._analyze_market_structure(features['price_data'])
            
            return features
            
        except Exception as e:
            logger.error(f"Fibonacci Elliott feature preparation error: {e}")
            return {'error': str(e)}
    
    def infer(self, features: Dict) -> Tuple[float, float]:
        """Fibonacci Elliott analizi inference"""
        try:
            if 'error' in features:
                return 50.0, 0.8
            
            base_score = 50.0
            uncertainty = 0.5
            
            # 1. Fibonacci Retracements scoring (25% weight)
            retracement_score = self._score_fibonacci_retracements(features.get('fibonacci_retracements', {}))
            
            # 2. Elliott Wave Patterns scoring (30% weight)
            elliott_score = self._score_elliott_wave_patterns(features.get('elliott_wave_analysis', {}))
            
            # 3. Harmonic Patterns scoring (20% weight)
            harmonic_score = self._score_harmonic_patterns(features.get('harmonic_patterns', {}))
            
            # 4. Golden Ratio Clusters scoring (15% weight)
            golden_ratio_score = self._score_golden_ratio_clusters(features.get('golden_ratio_clusters', {}))
            
            # 5. Market Structure scoring (10% weight)
            structure_score = self._score_market_structure(features.get('market_structure', {}))
            
            # Weighted combination
            final_score = (
                retracement_score * 0.25 +
                elliott_score * 0.30 +
                harmonic_score * 0.20 +
                golden_ratio_score * 0.15 +
                structure_score * 0.10
            )
            
            # Dynamic uncertainty based on pattern strength
            total_patterns = self._count_significant_patterns(features)
            pattern_density = min(total_patterns / 5, 1.0)  # Normalize to 0-1
            uncertainty = max(0.2, 0.7 - pattern_density * 0.3)
            
            # Clamp to valid range
            final_score = max(0, min(100, final_score))
            
            self.confidence_level = 1.0 - uncertainty
            
            logger.info(f"Fibonacci Elliott analysis completed: {final_score:.2f} (uncertainty: {uncertainty:.3f})")
            return final_score, uncertainty
            
        except Exception as e:
            logger.error(f"Fibonacci Elliott inference error: {e}")
            return 50.0, 0.8
    
    def retrain(self, data: Dict) -> None:
        """Fibonacci Elliott model retraining (mathematical ratios are constant)"""
        logger.info("Fibonacci Elliott module: Mathematical ratios are constant, no retraining needed")
        pass
    
    def _create_synthetic_price_data(self, symbol: str) -> Dict:
        """Create synthetic price data for analysis"""
        try:
            # Generate synthetic price movements
            symbol_hash = hash(symbol) % 10000
            base_price = 100 + (symbol_hash % 300)
            
            # Create 500 periods of price data
            periods = 500
            price_data = []
            
            # Generate Elliott Wave-like price movements
            current_price = base_price
            trend_direction = 1
            wave_count = 0
            
            for i in range(periods):
                # Add some randomness with trend bias
                daily_change = np.random.normal(0, 0.02) + (trend_direction * 0.005)
                current_price *= (1 + daily_change)
                
                # Ensure positive prices
                current_price = max(current_price, 1.0)
                
                # Create high/low based on daily change
                if daily_change > 0:
                    high = current_price * (1 + abs(daily_change) * 0.5)
                    low = current_price * (1 - abs(daily_change) * 0.3)
                else:
                    high = current_price * (1 + abs(daily_change) * 0.3)
                    low = current_price * (1 - abs(daily_change) * 0.5)
                
                price_data.append({
                    'date': datetime.now() - timedelta(days=periods-i),
                    'open': current_price,
                    'high': high,
                    'low': low,
                    'close': current_price,
                    'volume': 1000000 + np.random.randint(0, 500000)
                })
                
                # Change trend occasionally to create waves
                if i % 50 == 0:
                    trend_direction *= -1
                    wave_count += 1
            
            return {
                'price_data': price_data,
                'total_periods': periods,
                'base_price': base_price,
                'current_price': current_price
            }
            
        except Exception as e:
            logger.error(f"Synthetic price data creation error: {e}")
            return {'error': str(e)}
    
    def _calculate_fibonacci_retracements(self, price_data: List[Dict]) -> Dict:
        """Calculate Fibonacci retracement levels"""
        try:
            if len(price_data) < 20:
                return {'error': 'Insufficient data'}
            
            # Find significant swing highs and lows
            swings = self._identify_significant_swings(price_data)
            
            retracement_levels = []
            
            for i, swing in enumerate(swings[:-1]):
                next_swing = swings[i + 1]
                
                # Determine if this is a high-to-low or low-to-high move
                if swing['type'] == 'high' and next_swing['type'] == 'low':
                    # Downward move - calculate retracements from low back up
                    range_high = swing['price']
                    range_low = next_swing['price']
                    move_direction = 'down'
                elif swing['type'] == 'low' and next_swing['type'] == 'high':
                    # Upward move - calculate retracements from high back down
                    range_high = next_swing['price']
                    range_low = swing['price']
                    move_direction = 'up'
                else:
                    continue
                
                range_size = range_high - range_low
                
                # Calculate classic Fibonacci retracement levels
                levels = {}
                for ratio in self.fibonacci_ratios['classic_retracements']:
                    if move_direction == 'up':
                        # For upward moves, retracements are from high back down
                        level_price = range_high - (range_size * ratio)
                    else:
                        # For downward moves, retracements are from low back up
                        level_price = range_low + (range_size * ratio)
                    
                    levels[f'fib_{ratio:.3f}'] = {
                        'price': level_price,
                        'ratio': ratio,
                        'distance_from_current': abs(level_price - price_data[-1]['close']) / price_data[-1]['close']
                    }
                
                retracement_levels.append({
                    'swing_start': swing,
                    'swing_end': next_swing,
                    'range_high': range_high,
                    'range_low': range_low,
                    'range_size': range_size,
                    'move_direction': move_direction,
                    'levels': levels
                })
            
            # Find most relevant retracement (recent and significant)
            if retracement_levels:
                current_retracement = retracement_levels[-1]  # Most recent
                
                # Check which levels are closest to current price
                closest_levels = []
                current_price = price_data[-1]['close']
                
                for level_name, level_data in current_retracement['levels'].items():
                    distance = level_data['distance_from_current']
                    if distance < 0.05:  # Within 5% of current price
                        closest_levels.append({
                            'level': level_name,
                            'price': level_data['price'],
                            'ratio': level_data['ratio'],
                            'distance': distance
                        })
                
                return {
                    'retracement_levels': retracement_levels,
                    'current_retracement': current_retracement,
                    'closest_levels': closest_levels,
                    'total_retracements': len(retracement_levels)
                }
            
            return {'error': 'No significant swings found'}
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_fibonacci_extensions(self, price_data: List[Dict]) -> Dict:
        """Calculate Fibonacci extension levels"""
        try:
            swings = self._identify_significant_swings(price_data)
            
            if len(swings) < 3:
                return {'error': 'Insufficient swings for extensions'}
            
            extensions = []
            
            # Calculate extensions using ABC pattern (3 swings)
            for i in range(len(swings) - 2):
                swing_a = swings[i]
                swing_b = swings[i + 1]
                swing_c = swings[i + 2]
                
                # AB move
                ab_range = abs(swing_b['price'] - swing_a['price'])
                
                # Extension levels from C
                extension_levels = {}
                for ratio in self.fibonacci_ratios['extensions']:
                    if swing_c['type'] == 'low':
                        # Upward extension
                        extension_price = swing_c['price'] + (ab_range * ratio)
                    else:
                        # Downward extension
                        extension_price = swing_c['price'] - (ab_range * ratio)
                    
                    extension_levels[f'ext_{ratio:.3f}'] = {
                        'price': extension_price,
                        'ratio': ratio,
                        'distance_from_current': abs(extension_price - price_data[-1]['close']) / price_data[-1]['close']
                    }
                
                extensions.append({
                    'swing_a': swing_a,
                    'swing_b': swing_b,
                    'swing_c': swing_c,
                    'ab_range': ab_range,
                    'levels': extension_levels
                })
            
            return {
                'extensions': extensions,
                'total_extensions': len(extensions),
                'most_recent': extensions[-1] if extensions else None
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_elliott_wave_patterns(self, price_data: List[Dict]) -> Dict:
        """Analyze Elliott Wave patterns"""
        try:
            swings = self._identify_significant_swings(price_data)
            
            if len(swings) < 5:
                return {'error': 'Insufficient swings for Elliott Wave analysis'}
            
            # Attempt to identify 5-wave impulse patterns
            impulse_patterns = []
            
            for i in range(len(swings) - 4):
                wave_sequence = swings[i:i+5]
                
                # Check if this could be a 5-wave impulse
                if self._validate_impulse_pattern(wave_sequence):
                    # Calculate wave relationships
                    wave_relationships = self._calculate_wave_relationships(wave_sequence)
                    
                    impulse_patterns.append({
                        'waves': wave_sequence,
                        'relationships': wave_relationships,
                        'pattern_strength': self._calculate_pattern_strength(wave_relationships),
                        'wave_degree': self._estimate_wave_degree(wave_sequence)
                    })
            
            # Look for corrective patterns (ABC)
            corrective_patterns = []
            
            for i in range(len(swings) - 2):
                abc_sequence = swings[i:i+3]
                
                # Check if this could be an ABC correction
                if self._validate_corrective_pattern(abc_sequence):
                    corrective_relationships = self._calculate_corrective_relationships(abc_sequence)
                    
                    corrective_patterns.append({
                        'waves': abc_sequence,
                        'relationships': corrective_relationships,
                        'pattern_type': self._classify_corrective_pattern(corrective_relationships),
                        'pattern_strength': self._calculate_corrective_strength(corrective_relationships)
                    })
            
            return {
                'impulse_patterns': impulse_patterns,
                'corrective_patterns': corrective_patterns,
                'total_impulse': len(impulse_patterns),
                'total_corrective': len(corrective_patterns),
                'current_wave_count': len(swings),
                'wave_analysis_summary': self._create_wave_summary(impulse_patterns, corrective_patterns)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _detect_harmonic_patterns(self, price_data: List[Dict]) -> Dict:
        """Detect harmonic patterns (Gartley, Butterfly, etc.)"""
        try:
            swings = self._identify_significant_swings(price_data)
            
            if len(swings) < 4:
                return {'error': 'Insufficient swings for harmonic patterns'}
            
            detected_patterns = []
            
            # Check for 4-point harmonic patterns (XABC)
            for i in range(len(swings) - 3):
                xabc_points = swings[i:i+4]
                
                # Calculate ratios between points
                xa_range = abs(xabc_points[1]['price'] - xabc_points[0]['price'])
                ab_range = abs(xabc_points[2]['price'] - xabc_points[1]['price'])
                bc_range = abs(xabc_points[3]['price'] - xabc_points[2]['price'])
                
                if xa_range == 0:
                    continue
                
                ab_xa_ratio = ab_range / xa_range
                bc_ab_ratio = bc_range / ab_range if ab_range > 0 else 0
                
                # Check against known harmonic patterns
                for pattern_name, pattern_ratios in self.harmonic_patterns.items():
                    pattern_match = self._check_harmonic_pattern_match(
                        ab_xa_ratio, bc_ab_ratio, pattern_ratios
                    )
                    
                    if pattern_match['is_match']:
                        # Calculate potential D point
                        cd_target = self._calculate_harmonic_d_point(xabc_points, pattern_ratios)
                        
                        detected_patterns.append({
                            'pattern_name': pattern_name,
                            'points': xabc_points,
                            'ratios': {
                                'AB/XA': ab_xa_ratio,
                                'BC/AB': bc_ab_ratio
                            },
                            'match_quality': pattern_match['quality'],
                            'd_point_target': cd_target,
                            'pattern_completion': pattern_match['completion_percentage']
                        })
            
            return {
                'detected_patterns': detected_patterns,
                'total_patterns': len(detected_patterns),
                'strongest_pattern': max(detected_patterns, key=lambda x: x['match_quality']) if detected_patterns else None
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_fibonacci_time_zones(self, price_data: List[Dict]) -> Dict:
        """Calculate Fibonacci time-based analysis"""
        try:
            # Find significant time-based events
            significant_dates = []
            
            # Look for major price turning points
            for i, data_point in enumerate(price_data[10:-10]):
                actual_index = i + 10
                
                # Check if this is a local extreme
                local_highs = [p['high'] for p in price_data[actual_index-5:actual_index+6]]
                local_lows = [p['low'] for p in price_data[actual_index-5:actual_index+6]]
                
                if data_point['high'] == max(local_highs) or data_point['low'] == min(local_lows):
                    significant_dates.append({
                        'date': data_point['date'],
                        'price': data_point['close'],
                        'index': actual_index,
                        'type': 'high' if data_point['high'] == max(local_highs) else 'low'
                    })
            
            # Calculate Fibonacci time projections
            time_projections = []
            
            if len(significant_dates) >= 2:
                base_date = significant_dates[0]['date']
                
                for i, event in enumerate(significant_dates[1:], 1):
                    time_diff = (event['date'] - base_date).days
                    
                    # Project Fibonacci time cycles forward
                    for fib_number in self.fibonacci_time_cycles:
                        projected_date = base_date + timedelta(days=time_diff * fib_number)
                        
                        time_projections.append({
                            'base_event': significant_dates[0],
                            'reference_event': event,
                            'fibonacci_multiplier': fib_number,
                            'projected_date': projected_date,
                            'days_from_base': time_diff * fib_number
                        })
            
            return {
                'significant_dates': significant_dates,
                'time_projections': time_projections,
                'total_significant_events': len(significant_dates)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_golden_ratio_clusters(self, features: Dict) -> Dict:
        """Analyze clusters of Golden Ratio levels"""
        try:
            clusters = []
            
            # Collect all Fibonacci levels from different analyses
            all_levels = []
            
            # From retracements
            retracements = features.get('fibonacci_retracements', {})
            if 'retracement_levels' in retracements:
                for retracement in retracements['retracement_levels']:
                    for level_name, level_data in retracement['levels'].items():
                        all_levels.append({
                            'price': level_data['price'],
                            'ratio': level_data['ratio'],
                            'type': 'retracement',
                            'source': level_name
                        })
            
            # From extensions
            extensions = features.get('fibonacci_extensions', {})
            if 'extensions' in extensions:
                for extension in extensions['extensions']:
                    for level_name, level_data in extension['levels'].items():
                        all_levels.append({
                            'price': level_data['price'],
                            'ratio': level_data['ratio'],
                            'type': 'extension',
                            'source': level_name
                        })
            
            # Sort levels by price
            all_levels.sort(key=lambda x: x['price'])
            
            # Find clusters (levels within 2% of each other)
            current_price = features.get('current_price', 100)
            cluster_threshold = current_price * 0.02  # 2% threshold
            
            i = 0
            while i < len(all_levels):
                cluster_levels = [all_levels[i]]
                cluster_price = all_levels[i]['price']
                
                # Find all levels within threshold
                j = i + 1
                while j < len(all_levels) and abs(all_levels[j]['price'] - cluster_price) <= cluster_threshold:
                    cluster_levels.append(all_levels[j])
                    j += 1
                
                # If cluster has multiple levels, it's significant
                if len(cluster_levels) >= 2:
                    cluster_center = np.mean([level['price'] for level in cluster_levels])
                    cluster_strength = len(cluster_levels)
                    
                    # Check for Golden Ratio presence
                    golden_ratio_present = any(
                        abs(level['ratio'] - 0.618) < 0.01 or 
                        abs(level['ratio'] - 1.618) < 0.01 or
                        abs(level['ratio'] - 0.382) < 0.01
                        for level in cluster_levels
                    )
                    
                    clusters.append({
                        'center_price': cluster_center,
                        'levels': cluster_levels,
                        'strength': cluster_strength,
                        'golden_ratio_present': golden_ratio_present,
                        'distance_from_current': abs(cluster_center - current_price) / current_price
                    })
                
                i = j if j > i else i + 1
            
            # Sort clusters by strength
            clusters.sort(key=lambda x: x['strength'], reverse=True)
            
            return {
                'clusters': clusters,
                'total_clusters': len(clusters),
                'strongest_cluster': clusters[0] if clusters else None,
                'golden_ratio_clusters': [c for c in clusters if c['golden_ratio_present']]
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_market_structure(self, price_data: List[Dict]) -> Dict:
        """Analyze overall market structure using Fibonacci principles"""
        try:
            # Calculate market trend using multiple timeframes
            short_term_trend = self._calculate_trend(price_data[-20:])  # Last 20 periods
            medium_term_trend = self._calculate_trend(price_data[-50:])  # Last 50 periods
            long_term_trend = self._calculate_trend(price_data[-100:])  # Last 100 periods
            
            # Fibonacci spiral analysis (simplified)
            spiral_analysis = self._calculate_fibonacci_spiral(price_data)
            
            # Wave count and structure
            swings = self._identify_significant_swings(price_data)
            current_wave_count = len(swings)
            
            # Check if we're at a Fibonacci number of waves
            fibonacci_wave_count = current_wave_count in self.fibonacci_time_cycles
            
            return {
                'trends': {
                    'short_term': short_term_trend,
                    'medium_term': medium_term_trend,
                    'long_term': long_term_trend
                },
                'spiral_analysis': spiral_analysis,
                'wave_structure': {
                    'total_waves': current_wave_count,
                    'fibonacci_wave_count': fibonacci_wave_count,
                    'structure_quality': 'strong' if fibonacci_wave_count else 'moderate'
                },
                'market_phase': self._determine_market_phase(short_term_trend, medium_term_trend, long_term_trend)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _identify_significant_swings(self, price_data: List[Dict]) -> List[Dict]:
        """Identify significant price swings for analysis"""
        if len(price_data) < 10:
            return []
        
        swings = []
        lookback = 5  # Periods to look back/forward for swing identification
        
        for i in range(lookback, len(price_data) - lookback):
            current = price_data[i]
            
            # Check for swing high
            is_high = all(
                current['high'] >= price_data[j]['high'] 
                for j in range(i - lookback, i + lookback + 1) 
                if j != i
            )
            
            # Check for swing low
            is_low = all(
                current['low'] <= price_data[j]['low'] 
                for j in range(i - lookback, i + lookback + 1) 
                if j != i
            )
            
            if is_high:
                swings.append({
                    'date': current['date'],
                    'price': current['high'],
                    'type': 'high',
                    'index': i
                })
            elif is_low:
                swings.append({
                    'date': current['date'],
                    'price': current['low'],
                    'type': 'low',
                    'index': i
                })
        
        return swings
    
    def _validate_impulse_pattern(self, wave_sequence: List[Dict]) -> bool:
        """Validate if wave sequence could be a 5-wave impulse"""
        if len(wave_sequence) != 5:
            return False
        
        # Basic Elliott Wave rules:
        # 1. Wave 2 cannot retrace more than 100% of wave 1
        # 2. Wave 3 cannot be the shortest wave
        # 3. Wave 4 cannot overlap wave 1 price territory
        
        try:
            # Simplified validation
            wave_1_range = abs(wave_sequence[1]['price'] - wave_sequence[0]['price'])
            wave_2_range = abs(wave_sequence[2]['price'] - wave_sequence[1]['price'])
            wave_3_range = abs(wave_sequence[3]['price'] - wave_sequence[2]['price'])
            
            # Wave 2 retracement check
            if wave_2_range > wave_1_range:
                return False
            
            # Wave 3 cannot be shortest
            wave_ranges = [wave_1_range, wave_3_range, abs(wave_sequence[4]['price'] - wave_sequence[3]['price'])]
            if wave_3_range == min(wave_ranges):
                return False
            
            return True
            
        except:
            return False
    
    def _calculate_wave_relationships(self, wave_sequence: List[Dict]) -> Dict:
        """Calculate Fibonacci relationships between waves"""
        relationships = {}
        
        try:
            # Calculate wave ranges
            wave_1 = abs(wave_sequence[1]['price'] - wave_sequence[0]['price'])
            wave_2 = abs(wave_sequence[2]['price'] - wave_sequence[1]['price'])
            wave_3 = abs(wave_sequence[3]['price'] - wave_sequence[2]['price'])
            wave_4 = abs(wave_sequence[4]['price'] - wave_sequence[3]['price'])
            
            # Common Elliott Wave Fibonacci relationships
            relationships['wave_3_to_1'] = wave_3 / wave_1 if wave_1 > 0 else 0
            relationships['wave_2_retracement'] = wave_2 / wave_1 if wave_1 > 0 else 0
            relationships['wave_4_retracement'] = wave_4 / wave_3 if wave_3 > 0 else 0
            
            return relationships
            
        except:
            return {}
    
    def _calculate_pattern_strength(self, wave_relationships: Dict) -> float:
        """Calculate strength of Elliott Wave pattern based on Fibonacci relationships"""
        if not wave_relationships:
            return 0.0
        
        strength = 0.0
        
        # Check wave 3 to wave 1 relationship
        wave_3_to_1 = wave_relationships.get('wave_3_to_1', 0)
        if 1.6 <= wave_3_to_1 <= 1.65:  # Close to 1.618
            strength += 0.4
        elif 2.6 <= wave_3_to_1 <= 2.65:  # Close to 2.618
            strength += 0.3
        
        # Check wave 2 retracement
        wave_2_retrace = wave_relationships.get('wave_2_retracement', 0)
        if 0.38 <= wave_2_retrace <= 0.62:  # Common retracement range
            strength += 0.3
        
        # Check wave 4 retracement
        wave_4_retrace = wave_relationships.get('wave_4_retracement', 0)
        if 0.23 <= wave_4_retrace <= 0.38:  # Common retracement range
            strength += 0.3
        
        return min(strength, 1.0)
    
    def _validate_corrective_pattern(self, abc_sequence: List[Dict]) -> bool:
        """Validate if sequence could be an ABC correction"""
        if len(abc_sequence) != 3:
            return False
        
        # Basic ABC validation
        try:
            a_range = abs(abc_sequence[1]['price'] - abc_sequence[0]['price'])
            c_range = abs(abc_sequence[2]['price'] - abc_sequence[1]['price'])
            
            # C wave should have some relationship to A wave
            c_to_a_ratio = c_range / a_range if a_range > 0 else 0
            
            # Typical C wave is 0.618 to 1.618 times A wave
            return 0.5 <= c_to_a_ratio <= 2.0
            
        except:
            return False
    
    def _calculate_corrective_relationships(self, abc_sequence: List[Dict]) -> Dict:
        """Calculate relationships in ABC correction"""
        try:
            a_range = abs(abc_sequence[1]['price'] - abc_sequence[0]['price'])
            c_range = abs(abc_sequence[2]['price'] - abc_sequence[1]['price'])
            
            return {
                'c_to_a_ratio': c_range / a_range if a_range > 0 else 0,
                'a_range': a_range,
                'c_range': c_range
            }
        except:
            return {}
    
    def _classify_corrective_pattern(self, relationships: Dict) -> str:
        """Classify type of corrective pattern"""
        c_to_a = relationships.get('c_to_a_ratio', 0)
        
        if 0.6 <= c_to_a <= 0.65:
            return 'zigzag_618'
        elif 0.95 <= c_to_a <= 1.05:
            return 'zigzag_100'
        elif 1.6 <= c_to_a <= 1.65:
            return 'zigzag_162'
        else:
            return 'complex_correction'
    
    def _calculate_corrective_strength(self, relationships: Dict) -> float:
        """Calculate strength of corrective pattern"""
        c_to_a = relationships.get('c_to_a_ratio', 0)
        
        # Strong patterns have C waves at common Fibonacci ratios
        fibonacci_distances = [
            abs(c_to_a - 0.618),
            abs(c_to_a - 1.000),
            abs(c_to_a - 1.618)
        ]
        
        min_distance = min(fibonacci_distances)
        return max(0, 1 - min_distance * 5)  # Closer to Fib ratio = stronger
    
    def _check_harmonic_pattern_match(self, ab_xa_ratio: float, bc_ab_ratio: float, pattern_ratios: Dict) -> Dict:
        """Check if ratios match a harmonic pattern"""
        # Simplified harmonic pattern matching
        match_quality = 0.0
        
        # Check XA ratio (placeholder - would need full XABC analysis)
        target_xa = pattern_ratios.get('XA', 0.618)
        if isinstance(target_xa, list):
            target_xa = target_xa[0]  # Use first value for simplicity
        
        # Check AB ratio
        target_ab = pattern_ratios.get('AB', [0.382, 0.886])
        if isinstance(target_ab, list):
            ab_match = any(abs(ab_xa_ratio - target) < 0.1 for target in target_ab)
        else:
            ab_match = abs(ab_xa_ratio - target_ab) < 0.1
        
        if ab_match:
            match_quality += 0.5
        
        # Additional checks would be performed for BC and CD ratios
        is_match = match_quality > 0.3
        
        return {
            'is_match': is_match,
            'quality': match_quality,
            'completion_percentage': match_quality * 100
        }
    
    def _calculate_harmonic_d_point(self, xabc_points: List[Dict], pattern_ratios: Dict) -> Dict:
        """Calculate potential D point for harmonic pattern completion"""
        try:
            x_price = xabc_points[0]['price']
            a_price = xabc_points[1]['price']
            c_price = xabc_points[2]['price']
            
            xa_range = abs(a_price - x_price)
            
            # Get CD ratio from pattern
            cd_ratio = pattern_ratios.get('CD', 1.618)
            if isinstance(cd_ratio, list):
                cd_ratio = cd_ratio[0]
            
            # Calculate D point (simplified)
            if a_price > x_price:  # Upward XA
                d_price = c_price + (xa_range * cd_ratio)
            else:  # Downward XA
                d_price = c_price - (xa_range * cd_ratio)
            
            return {
                'price': d_price,
                'ratio_used': cd_ratio,
                'distance_from_c': abs(d_price - c_price)
            }
        except:
            return {'error': 'Could not calculate D point'}
    
    def _calculate_fibonacci_spiral(self, price_data: List[Dict]) -> Dict:
        """Calculate Fibonacci spiral analysis (simplified)"""
        try:
            # Simplified spiral calculation
            prices = [p['close'] for p in price_data[-50:]]  # Last 50 prices
            
            # Calculate if price movements follow golden ratio proportions
            spiral_strength = 0.0
            
            for i in range(1, len(prices)):
                price_change_ratio = prices[i] / prices[i-1] if prices[i-1] > 0 else 1
                
                # Check if change is close to golden ratio or its inverse
                if abs(price_change_ratio - self.golden_ratio) < 0.1:
                    spiral_strength += 0.02
                elif abs(price_change_ratio - (1/self.golden_ratio)) < 0.1:
                    spiral_strength += 0.02
            
            return {
                'spiral_strength': min(spiral_strength, 1.0),
                'golden_ratio_adherence': spiral_strength > 0.3
            }
        except:
            return {'error': 'Could not calculate spiral'}
    
    def _calculate_trend(self, price_data: List[Dict]) -> Dict:
        """Calculate trend direction and strength"""
        if len(price_data) < 2:
            return {'direction': 'sideways', 'strength': 0}
        
        prices = [p['close'] for p in price_data]
        
        # Simple linear regression for trend
        x = np.arange(len(prices))
        slope = np.polyfit(x, prices, 1)[0]
        
        # Normalize slope to strength (0-1)
        avg_price = np.mean(prices)
        strength = abs(slope) / avg_price * len(prices) if avg_price > 0 else 0
        strength = min(strength, 1.0)
        
        direction = 'upward' if slope > 0 else 'downward' if slope < 0 else 'sideways'
        
        return {
            'direction': direction,
            'strength': strength,
            'slope': slope
        }
    
    def _determine_market_phase(self, short_trend: Dict, medium_trend: Dict, long_trend: Dict) -> str:
        """Determine current market phase"""
        short_dir = short_trend.get('direction', 'sideways')
        medium_dir = medium_trend.get('direction', 'sideways')
        long_dir = long_trend.get('direction', 'sideways')
        
        if short_dir == medium_dir == long_dir == 'upward':
            return 'strong_uptrend'
        elif short_dir == medium_dir == long_dir == 'downward':
            return 'strong_downtrend'
        elif long_dir == 'upward' and short_dir == 'downward':
            return 'pullback_in_uptrend'
        elif long_dir == 'downward' and short_dir == 'upward':
            return 'bounce_in_downtrend'
        else:
            return 'sideways_consolidation'
    
    def _count_significant_patterns(self, features: Dict) -> int:
        """Count total significant patterns found"""
        count = 0
        
        # Count Fibonacci retracements
        retracements = features.get('fibonacci_retracements', {})
        count += len(retracements.get('closest_levels', []))
        
        # Count Elliott Wave patterns
        elliott = features.get('elliott_wave_analysis', {})
        count += elliott.get('total_impulse', 0) + elliott.get('total_corrective', 0)
        
        # Count harmonic patterns
        harmonics = features.get('harmonic_patterns', {})
        count += harmonics.get('total_patterns', 0)
        
        # Count golden ratio clusters
        clusters = features.get('golden_ratio_clusters', {})
        count += len(clusters.get('golden_ratio_clusters', []))
        
        return count
    
    def _score_fibonacci_retracements(self, retracement_data: Dict) -> float:
        """Score based on Fibonacci retracement analysis"""
        if not retracement_data or 'error' in retracement_data:
            return 50.0
        
        score = 50.0
        
        # Bonus for close levels to current price
        closest_levels = retracement_data.get('closest_levels', [])
        for level in closest_levels:
            distance = level.get('distance', 1.0)
            if distance < 0.02:  # Very close (within 2%)
                score += 15
            elif distance < 0.05:  # Close (within 5%)
                score += 10
        
        # Bonus for key Fibonacci ratios
        for level in closest_levels:
            ratio = level.get('ratio', 0)
            if abs(ratio - 0.618) < 0.01:  # Golden ratio
                score += 20
            elif abs(ratio - 0.382) < 0.01:  # Important ratio
                score += 15
            elif abs(ratio - 0.5) < 0.01:  # 50% retracement
                score += 10
        
        return max(0, min(100, score))
    
    def _score_elliott_wave_patterns(self, elliott_data: Dict) -> float:
        """Score based on Elliott Wave pattern analysis"""
        if not elliott_data or 'error' in elliott_data:
            return 50.0
        
        score = 50.0
        
        # Bonus for impulse patterns
        impulse_patterns = elliott_data.get('impulse_patterns', [])
        for pattern in impulse_patterns:
            strength = pattern.get('pattern_strength', 0)
            score += strength * 20  # Up to 20 points per strong pattern
        
        # Bonus for corrective patterns
        corrective_patterns = elliott_data.get('corrective_patterns', [])
        for pattern in corrective_patterns:
            strength = pattern.get('pattern_strength', 0)
            score += strength * 15  # Up to 15 points per strong pattern
        
        return max(0, min(100, score))
    
    def _score_harmonic_patterns(self, harmonic_data: Dict) -> float:
        """Score based on harmonic pattern detection"""
        if not harmonic_data or 'error' in harmonic_data:
            return 50.0
        
        score = 50.0
        
        patterns = harmonic_data.get('detected_patterns', [])
        for pattern in patterns:
            quality = pattern.get('match_quality', 0)
            completion = pattern.get('pattern_completion', 0)
            
            score += quality * 25  # Quality bonus
            if completion > 80:  # Near completion
                score += 15
        
        return max(0, min(100, score))
    
    def _score_golden_ratio_clusters(self, cluster_data: Dict) -> float:
        """Score based on Golden Ratio cluster analysis"""
        if not cluster_data or 'error' in cluster_data:
            return 50.0
        
        score = 50.0
        
        golden_clusters = cluster_data.get('golden_ratio_clusters', [])
        for cluster in golden_clusters:
            strength = cluster.get('strength', 0)
            distance = cluster.get('distance_from_current', 1.0)
            
            # Closer clusters with higher strength get more points
            cluster_score = (strength * 10) / (1 + distance * 5)
            score += cluster_score
        
        return max(0, min(100, score))
    
    def _score_market_structure(self, structure_data: Dict) -> float:
        """Score based on market structure analysis"""
        if not structure_data or 'error' in structure_data:
            return 50.0
        
        score = 50.0
        
        # Trend alignment bonus
        trends = structure_data.get('trends', {})
        short_strength = trends.get('short_term', {}).get('strength', 0)
        medium_strength = trends.get('medium_term', {}).get('strength', 0)
        long_strength = trends.get('long_term', {}).get('strength', 0)
        
        # Average trend strength
        avg_strength = (short_strength + medium_strength + long_strength) / 3
        score += avg_strength * 30
        
        # Fibonacci wave count bonus
        wave_structure = structure_data.get('wave_structure', {})
        if wave_structure.get('fibonacci_wave_count', False):
            score += 20
        
        return max(0, min(100, score))
    
    def _create_wave_summary(self, impulse_patterns: List[Dict], corrective_patterns: List[Dict]) -> Dict:
        """Create summary of wave analysis"""
        return {
            'total_patterns': len(impulse_patterns) + len(corrective_patterns),
            'strongest_impulse': max(impulse_patterns, key=lambda x: x['pattern_strength']) if impulse_patterns else None,
            'strongest_corrective': max(corrective_patterns, key=lambda x: x['pattern_strength']) if corrective_patterns else None,
            'wave_quality': 'high' if len(impulse_patterns) >= 2 else 'medium' if len(impulse_patterns) >= 1 else 'low'
        }
    
    def _estimate_wave_degree(self, wave_sequence: List[Dict]) -> str:
        """Estimate the degree/timeframe of the wave pattern"""
        if len(wave_sequence) < 2:
            return 'unknown'
        
        # Calculate time span of pattern
        start_date = wave_sequence[0]['date']
        end_date = wave_sequence[-1]['date']
        duration_days = (end_date - start_date).days
        
        # Classify based on duration
        if duration_days > 365:
            return 'cycle'
        elif duration_days > 30:
            return 'primary'
        elif duration_days > 7:
            return 'intermediate'
        else:
            return 'minor'
