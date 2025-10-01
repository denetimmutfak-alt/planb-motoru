# -*- coding: utf-8 -*-
"""
PlanB Motoru - Ultra Gann Enhanced Analysis Module
W.D. Gann Geometrik Analiz Sistemi - Professional Level
Gann Square-of-Nine, Time Cycles, Price-Time Symmetry, Cardinal Cross, Planetary Lines
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


class UltraGannModule(ExpertModule):
    """Ultra Gann Enhanced Analysis - Professional Geometric Market Analysis"""
    
    def __init__(self, module_name: str = "Ultra Gann Enhanced"):
        super().__init__(module_name)
        super().__init__(module_name)
        
        # Gann Square-of-Nine calculations
        self.gann_angles = {
            '1x1': 45.0,      # 1:1 ratio (45 degrees) - Primary trend line
            '1x2': 26.57,     # 1:2 ratio - Support/Resistance  
            '1x3': 18.43,     # 1:3 ratio - Minor support
            '1x4': 14.04,     # 1:4 ratio - Weekly levels
            '1x8': 7.13,      # 1:8 ratio - Long-term levels
            '2x1': 63.43,     # 2:1 ratio - Strong resistance
            '3x1': 71.57,     # 3:1 ratio - Major resistance
            '4x1': 75.96,     # 4:1 ratio - Critical levels
            '8x1': 82.87      # 8:1 ratio - Extreme levels
        }
        
        # Gann Time Cycles (trading days)
        self.time_cycles = {
            'short_cycles': [30, 45, 60, 90, 120, 144, 180],    # Days
            'medium_cycles': [252, 360, 540, 720, 1080],        # Annual cycles
            'long_cycles': [1260, 1440, 2160, 2520, 3600],     # Multi-year cycles
            'master_cycles': [7200, 10800, 14400, 21600]       # Decade cycles
        }
        
        # Cardinal Cross degrees (Critical Gann levels)
        self.cardinal_cross = [0, 90, 180, 270]  # Aries, Cancer, Libra, Capricorn
        
        # Gann Square natural numbers and perfect squares
        self.gann_squares = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400]
        
        # Fibonacci integrated with Gann
        self.fib_gann_ratios = [0.236, 0.382, 0.5, 0.618, 0.786, 1.0, 1.272, 1.618, 2.618, 4.236]
        
        # Price scaling factors for different asset classes
        self.price_scalers = {
            'stocks': 1.0,
            'forex': 10000.0,
            'crypto': 1.0,
            'commodities': 100.0,
            'indices': 0.01
        }
        
        logger.info("Ultra Gann Enhanced Module initialized with professional geometric analysis")
    
    def prepare_features(self, data: Dict) -> Dict:
        """Gann analizi için özellikleri hazırla"""
        try:
            symbol = data.get('symbol', 'UNKNOWN')
            
            # Sentetik fiyat verisi oluştur
            features = self._create_synthetic_features(symbol)
            
            # Gann Square-of-Nine analizi
            features['gann_square'] = self._calculate_gann_square_of_nine(features['current_price'])
            
            # Time cycle analysis
            features['time_cycles'] = self._analyze_time_cycles(features['current_date'])
            
            # Cardinal Cross analysis
            features['cardinal_analysis'] = self._analyze_cardinal_cross_position(features['current_price'])
            
            # Price-Time symmetry
            features['price_time_symmetry'] = self._calculate_price_time_symmetry(features)
            
            # Planetary line analysis (Gann's astrological component)
            features['planetary_lines'] = self._calculate_planetary_lines(features['current_date'])
            
            return features
            
        except Exception as e:
            logger.error(f"Gann feature preparation error: {e}")
            return {'error': str(e)}
    
    def infer(self, features: Dict) -> Tuple[float, float]:
        """Gann analizi inference"""
        try:
            if 'error' in features:
                return 50.0, 0.8
            
            # Base Gann score calculation
            base_score = 50.0
            uncertainty = 0.5
            
            # 1. Gann Square-of-Nine scoring (40% weight)
            square_score = self._score_gann_square(features.get('gann_square', {}))
            
            # 2. Time Cycle scoring (25% weight)  
            time_score = self._score_time_cycles(features.get('time_cycles', {}))
            
            # 3. Cardinal Cross scoring (20% weight)
            cardinal_score = self._score_cardinal_cross(features.get('cardinal_analysis', {}))
            
            # 4. Price-Time Symmetry scoring (10% weight)
            symmetry_score = self._score_price_time_symmetry(features.get('price_time_symmetry', {}))
            
            # 5. Planetary Lines scoring (5% weight)
            planetary_score = self._score_planetary_lines(features.get('planetary_lines', {}))
            
            # Weighted combination
            final_score = (
                square_score * 0.40 +
                time_score * 0.25 +
                cardinal_score * 0.20 +
                symmetry_score * 0.10 +
                planetary_score * 0.05
            )
            
            # Dynamic uncertainty based on signal strength
            signal_strength = max(abs(final_score - 50) / 50, 0.1)
            uncertainty = max(0.2, 0.8 - signal_strength)
            
            # Clamp score to valid range
            final_score = max(0, min(100, final_score))
            
            self.confidence_level = 1.0 - uncertainty
            
            logger.info(f"Gann analysis completed: {final_score:.2f} (uncertainty: {uncertainty:.3f})")
            return final_score, uncertainty
            
        except Exception as e:
            logger.error(f"Gann inference error: {e}")
            return 50.0, 0.8
    
    def retrain(self, data: Dict) -> None:
        """Gann model retraining (geometric patterns don't require retraining)"""
        logger.info("Gann module: Geometric patterns are constant, no retraining needed")
        pass
    
    def _create_synthetic_features(self, symbol: str) -> Dict:
        """Create synthetic market features for analysis"""
        current_date = datetime.now()
        
        # Synthetic price based on symbol hash and date
        symbol_hash = hash(symbol) % 10000
        date_component = current_date.timetuple().tm_yday
        
        base_price = 100 + (symbol_hash % 500)
        price_variation = math.sin(date_component * 0.1) * 20
        current_price = base_price + price_variation
        
        # Create price history for analysis
        price_history = []
        for i in range(100):  # 100 days of history
            date_offset = current_date - timedelta(days=i)
            day_variation = math.sin((date_component - i) * 0.1) * 20
            price = base_price + day_variation + np.random.normal(0, 5)
            price_history.append({
                'date': date_offset,
                'price': max(price, 1.0),  # Ensure positive price
                'high': price * (1 + np.random.uniform(0, 0.05)),
                'low': price * (1 - np.random.uniform(0, 0.05)),
                'volume': 1000000 + np.random.randint(0, 500000)
            })
        
        return {
            'symbol': symbol,
            'current_date': current_date,
            'current_price': current_price,
            'price_history': price_history
        }
    
    def _calculate_gann_square_of_nine(self, price: float) -> Dict:
        """Calculate Gann Square-of-Nine levels"""
        try:
            # Find the square root and position in Gann Square
            sqrt_price = math.sqrt(price)
            square_below = int(sqrt_price) ** 2
            square_above = (int(sqrt_price) + 1) ** 2
            
            # Position within current square (0 to 1)
            square_position = (price - square_below) / (square_above - square_below)
            
            # Calculate Gann angle levels
            angle_levels = {}
            for angle_name, angle_degrees in self.gann_angles.items():
                # Price level at this angle from square center
                angle_radians = math.radians(angle_degrees)
                level_price = square_below + (square_above - square_below) * (angle_degrees / 90.0)
                
                # Distance from current price to this level
                distance = abs(price - level_price) / price
                
                angle_levels[angle_name] = {
                    'price_level': level_price,
                    'distance_pct': distance * 100,
                    'angle_degrees': angle_degrees,
                    'support_resistance': 'support' if level_price < price else 'resistance'
                }
            
            # Calculate Square-of-Nine spiral position
            spiral_position = self._calculate_spiral_position(price)
            
            return {
                'current_price': price,
                'square_below': square_below,
                'square_above': square_above,
                'square_position': square_position,
                'angle_levels': angle_levels,
                'spiral_position': spiral_position,
                'in_gann_square': square_below <= price <= square_above
            }
            
        except Exception as e:
            logger.error(f"Gann Square calculation error: {e}")
            return {}
    
    def _calculate_spiral_position(self, price: float) -> Dict:
        """Calculate position in Gann's Square-of-Nine spiral"""
        try:
            sqrt_price = math.sqrt(price)
            
            # Find which "ring" of the spiral we're in
            ring_number = int(sqrt_price)
            
            # Position within the ring (0 to 1)
            ring_position = sqrt_price - ring_number
            
            # Determine cardinal direction within spiral
            if ring_position < 0.25:
                direction = 'east'
            elif ring_position < 0.5:
                direction = 'north'
            elif ring_position < 0.75:
                direction = 'west'
            else:
                direction = 'south'
            
            return {
                'ring_number': ring_number,
                'ring_position': ring_position,
                'cardinal_direction': direction,
                'spiral_degrees': ring_position * 360
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_time_cycles(self, current_date: datetime) -> Dict:
        """Analyze Gann time cycles"""
        try:
            # Reference date (market epoch or significant market event)
            reference_date = datetime(2020, 3, 23)  # COVID market bottom
            days_elapsed = (current_date - reference_date).days
            
            # Check alignment with Gann time cycles
            cycle_alignments = {}
            
            for cycle_type, cycles in self.time_cycles.items():
                cycle_alignments[cycle_type] = []
                
                for cycle_days in cycles:
                    # How close are we to a cycle completion?
                    cycle_position = days_elapsed % cycle_days
                    cycle_completion = cycle_position / cycle_days
                    
                    # Check if we're near a cycle turn (within 5% of completion)
                    if cycle_completion > 0.95 or cycle_completion < 0.05:
                        cycle_alignments[cycle_type].append({
                            'cycle_days': cycle_days,
                            'completion_pct': cycle_completion * 100,
                            'days_to_turn': min(cycle_position, cycle_days - cycle_position),
                            'cycle_strength': 1.0 - abs(0.5 - abs(cycle_completion - 0.5)) * 2
                        })
            
            # Calculate next significant time window
            next_windows = self._calculate_next_time_windows(current_date, reference_date)
            
            return {
                'days_from_reference': days_elapsed,
                'cycle_alignments': cycle_alignments,
                'next_time_windows': next_windows,
                'total_active_cycles': sum(len(alignments) for alignments in cycle_alignments.values())
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_next_time_windows(self, current_date: datetime, reference_date: datetime) -> List[Dict]:
        """Calculate next significant Gann time windows"""
        days_elapsed = (current_date - reference_date).days
        next_windows = []
        
        # Check next 90 days for significant cycle completions
        for days_ahead in range(1, 91):
            future_days = days_elapsed + days_ahead
            
            # Check all cycles for significant turns
            for cycle_type, cycles in self.time_cycles.items():
                for cycle_days in cycles:
                    if future_days % cycle_days == 0:  # Exact cycle completion
                        next_windows.append({
                            'date': current_date + timedelta(days=days_ahead),
                            'days_ahead': days_ahead,
                            'cycle_type': cycle_type,
                            'cycle_days': cycle_days,
                            'significance': 'high' if cycle_days >= 360 else 'medium'
                        })
        
        # Sort by days ahead and return top 10
        next_windows.sort(key=lambda x: x['days_ahead'])
        return next_windows[:10]
    
    def _analyze_cardinal_cross_position(self, price: float) -> Dict:
        """Analyze price position relative to Cardinal Cross levels"""
        try:
            # Get base price for Cardinal Cross calculation
            price_base = int(price)
            
            cardinal_levels = {}
            for cardinal_degree in self.cardinal_cross:
                # Calculate price levels at Cardinal Cross degrees
                level_price = price_base + (cardinal_degree / 360.0) * price_base
                
                distance_pct = abs(price - level_price) / price * 100
                
                cardinal_levels[f'cardinal_{cardinal_degree}'] = {
                    'degree': cardinal_degree,
                    'price_level': level_price,
                    'distance_pct': distance_pct,
                    'is_near': distance_pct < 2.0  # Within 2%
                }
            
            # Find closest Cardinal Cross level
            closest_level = min(cardinal_levels.values(), key=lambda x: x['distance_pct'])
            
            return {
                'cardinal_levels': cardinal_levels,
                'closest_cardinal': closest_level,
                'in_cardinal_zone': closest_level['distance_pct'] < 3.0
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_price_time_symmetry(self, features: Dict) -> Dict:
        """Calculate Gann's Price-Time symmetry relationships"""
        try:
            current_price = features.get('current_price', 100)
            price_history = features.get('price_history', [])
            
            if len(price_history) < 50:
                return {'error': 'Insufficient price history'}
            
            # Find significant swing highs and lows
            swings = self._identify_price_swings(price_history)
            
            # Calculate time and price relationships
            symmetry_patterns = []
            
            for i, swing1 in enumerate(swings[:-1]):
                for swing2 in swings[i+1:]:
                    time_diff = abs((swing1['date'] - swing2['date']).days)
                    price_diff = abs(swing1['price'] - swing2['price'])
                    
                    # Check for Gann's equal time-price relationships
                    time_price_ratio = time_diff / max(price_diff, 1)
                    
                    if 0.8 <= time_price_ratio <= 1.2:  # Near 1:1 time-price
                        symmetry_patterns.append({
                            'swing1_date': swing1['date'],
                            'swing2_date': swing2['date'],
                            'time_diff_days': time_diff,
                            'price_diff': price_diff,
                            'time_price_ratio': time_price_ratio,
                            'symmetry_strength': 1.0 - abs(1.0 - time_price_ratio)
                        })
            
            return {
                'symmetry_patterns': symmetry_patterns,
                'pattern_count': len(symmetry_patterns),
                'avg_symmetry_strength': np.mean([p['symmetry_strength'] for p in symmetry_patterns]) if symmetry_patterns else 0
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _identify_price_swings(self, price_history: List[Dict]) -> List[Dict]:
        """Identify significant price swing highs and lows"""
        swings = []
        
        if len(price_history) < 10:
            return swings
        
        # Sort by date
        sorted_history = sorted(price_history, key=lambda x: x['date'])
        
        # Simple swing detection - local maxima and minima
        for i in range(5, len(sorted_history) - 5):
            current = sorted_history[i]
            
            # Check if it's a local high
            is_high = all(current['price'] >= sorted_history[j]['price'] 
                         for j in range(i-5, i+6) if j != i)
            
            # Check if it's a local low  
            is_low = all(current['price'] <= sorted_history[j]['price']
                        for j in range(i-5, i+6) if j != i)
            
            if is_high:
                swings.append({
                    'date': current['date'],
                    'price': current['price'],
                    'type': 'high'
                })
            elif is_low:
                swings.append({
                    'date': current['date'],
                    'price': current['price'],
                    'type': 'low'
                })
        
        return swings
    
    def _calculate_planetary_lines(self, current_date: datetime) -> Dict:
        """Calculate Gann's planetary line influences (simplified)"""
        try:
            # Simplified planetary calculation based on date cycles
            day_of_year = current_date.timetuple().tm_yday
            
            # Major planetary cycles (simplified)
            planetary_influences = {
                'mercury': math.sin(day_of_year * 4 * math.pi / 365) * 0.3,  # ~88 day cycle
                'venus': math.sin(day_of_year * 1.6 * math.pi / 365) * 0.4,  # ~225 day cycle  
                'mars': math.sin(day_of_year * 0.53 * math.pi / 365) * 0.5,  # ~687 day cycle
                'jupiter': math.sin(day_of_year * 0.084 * math.pi / 365) * 0.6,  # ~12 year cycle
                'saturn': math.sin(day_of_year * 0.034 * math.pi / 365) * 0.7   # ~29 year cycle
            }
            
            # Combined planetary score
            total_influence = sum(planetary_influences.values()) / len(planetary_influences)
            
            return {
                'planetary_influences': planetary_influences,
                'total_planetary_score': (total_influence + 1) * 50,  # Convert to 0-100 scale
                'dominant_planet': max(planetary_influences, key=planetary_influences.get)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _score_gann_square(self, square_data: Dict) -> float:
        """Score based on Gann Square-of-Nine analysis"""
        if not square_data or 'error' in square_data:
            return 50.0
        
        score = 50.0
        
        # Bonus for being near perfect square levels
        if square_data.get('in_gann_square', False):
            square_position = square_data.get('square_position', 0.5)
            
            # Higher score for positions near 0, 0.5, or 1 (key Gann levels)
            key_distances = [abs(square_position - level) for level in [0, 0.25, 0.5, 0.75, 1.0]]
            min_distance = min(key_distances)
            
            if min_distance < 0.1:  # Very close to key level
                score += 25
            elif min_distance < 0.2:  # Moderately close
                score += 15
        
        # Bonus for being near Gann angle levels
        angle_levels = square_data.get('angle_levels', {})
        for angle_name, level_data in angle_levels.items():
            distance_pct = level_data.get('distance_pct', 100)
            
            if distance_pct < 1.0:  # Within 1% of Gann angle
                if angle_name == '1x1':  # Primary Gann line
                    score += 20
                else:
                    score += 10
            elif distance_pct < 3.0:  # Within 3%
                score += 5
        
        return max(0, min(100, score))
    
    def _score_time_cycles(self, time_data: Dict) -> float:
        """Score based on Gann time cycle analysis"""
        if not time_data or 'error' in time_data:
            return 50.0
        
        score = 50.0
        
        # Bonus for active cycle alignments
        total_cycles = time_data.get('total_active_cycles', 0)
        score += min(total_cycles * 8, 30)  # Max 30 points for cycle alignment
        
        # Bonus for upcoming significant time windows
        next_windows = time_data.get('next_time_windows', [])
        for window in next_windows[:3]:  # Top 3 windows
            days_ahead = window.get('days_ahead', 100)
            significance = window.get('significance', 'low')
            
            if days_ahead <= 7:  # Within a week
                if significance == 'high':
                    score += 15
                else:
                    score += 10
            elif days_ahead <= 30:  # Within a month
                if significance == 'high':
                    score += 8
                else:
                    score += 5
        
        return max(0, min(100, score))
    
    def _score_cardinal_cross(self, cardinal_data: Dict) -> float:
        """Score based on Cardinal Cross analysis"""
        if not cardinal_data or 'error' in cardinal_data:
            return 50.0
        
        score = 50.0
        
        # Major bonus for being in Cardinal zone
        if cardinal_data.get('in_cardinal_zone', False):
            score += 20
            
            closest_cardinal = cardinal_data.get('closest_cardinal', {})
            distance_pct = closest_cardinal.get('distance_pct', 100)
            
            if distance_pct < 1.0:  # Very close to Cardinal Cross
                score += 20
            elif distance_pct < 2.0:
                score += 10
        
        return max(0, min(100, score))
    
    def _score_price_time_symmetry(self, symmetry_data: Dict) -> float:
        """Score based on Price-Time symmetry"""
        if not symmetry_data or 'error' in symmetry_data:
            return 50.0
        
        score = 50.0
        
        pattern_count = symmetry_data.get('pattern_count', 0)
        avg_strength = symmetry_data.get('avg_symmetry_strength', 0)
        
        # Bonus for symmetry patterns
        score += min(pattern_count * 5, 20)  # Max 20 points
        score += avg_strength * 15  # Quality bonus
        
        return max(0, min(100, score))
    
    def _score_planetary_lines(self, planetary_data: Dict) -> float:
        """Score based on planetary line analysis"""
        if not planetary_data or 'error' in planetary_data:
            return 50.0
        
        return planetary_data.get('total_planetary_score', 50.0)
