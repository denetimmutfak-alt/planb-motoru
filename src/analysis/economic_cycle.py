# -*- coding: utf-8 -*-
"""
PlanB Motoru - Ultra Economic Cycle Analysis Module
Ultra-expert level economic cycle analysis with professional macro indicators,
recession probability modeling, business cycle identification, and macro correlations
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import yfinance as yf
from src.utils.logger import log_info, log_error, log_debug, log_warning

class UltraEconomicCycleAnalyzer:
    """Ultra-expert economic cycle and macro analysis system"""
    
    def __init__(self):
        # Professional economic indicators with weights
        self.leading_indicators = {
            'yield_curve': {'weight': 0.25, 'inversion_threshold': -0.5, 'description': '10Y-2Y Treasury Spread'},
            'unemployment_rate': {'weight': 0.20, 'recession_threshold': 0.5, 'description': 'Unemployment Rate Change'},
            'consumer_confidence': {'weight': 0.15, 'threshold': -15, 'description': 'Consumer Confidence Index'},
            'manufacturing_pmi': {'weight': 0.15, 'contraction_threshold': 50, 'description': 'Manufacturing PMI'},
            'housing_starts': {'weight': 0.10, 'decline_threshold': -20, 'description': 'Housing Starts YoY%'},
            'credit_spreads': {'weight': 0.10, 'stress_threshold': 3.0, 'description': 'High Yield Credit Spreads'},
            'money_supply': {'weight': 0.05, 'growth_threshold': 15, 'description': 'M2 Money Supply Growth'}
        }
        
        # Business cycle phases with characteristics
        self.business_cycle_phases = {
            'expansion': {
                'duration_months': (36, 120),
                'gdp_growth': (2.0, 5.0),
                'unemployment_trend': 'declining',
                'inflation_trend': 'rising',
                'market_performance': 'strong',
                'sector_leaders': ['technology', 'consumer_discretionary', 'industrials']
            },
            'peak': {
                'duration_months': (3, 12),
                'gdp_growth': (1.0, 3.0),
                'unemployment_trend': 'stable_low',
                'inflation_trend': 'elevated',
                'market_performance': 'volatile',
                'sector_leaders': ['energy', 'materials', 'utilities']
            },
            'contraction': {
                'duration_months': (6, 18),
                'gdp_growth': (-3.0, 1.0),
                'unemployment_trend': 'rising',
                'inflation_trend': 'falling',
                'market_performance': 'declining',
                'sector_leaders': ['consumer_staples', 'healthcare', 'utilities']
            },
            'trough': {
                'duration_months': (3, 9),
                'gdp_growth': (-2.0, 2.0),
                'unemployment_trend': 'stable_high',
                'inflation_trend': 'low',
                'market_performance': 'bottoming',
                'sector_leaders': ['technology', 'financials', 'real_estate']
            }
        }
        
        # Recession probability model factors
        self.recession_factors = {
            'sahm_rule': {'weight': 0.30, 'description': 'Sahm Rule Recession Indicator'},
            'yield_inversion': {'weight': 0.25, 'description': 'Yield Curve Inversion'},
            'credit_conditions': {'weight': 0.20, 'description': 'Credit Market Stress'},
            'employment_momentum': {'weight': 0.15, 'description': 'Employment Momentum'},
            'consumer_spending': {'weight': 0.10, 'description': 'Consumer Spending Weakness'}
        }
        
        # Sector rotation patterns by cycle phase
        self.sector_rotation_map = {
            'early_expansion': ['financials', 'real_estate', 'consumer_discretionary'],
            'mid_expansion': ['technology', 'industrials', 'materials'],
            'late_expansion': ['energy', 'consumer_staples', 'healthcare'],
            'early_contraction': ['utilities', 'consumer_staples', 'healthcare'],
            'mid_contraction': ['technology', 'communications', 'consumer_discretionary'],
            'late_contraction': ['financials', 'real_estate', 'industrials']
        }
        
        # Economic data simulation parameters (in practice, would use real APIs)
        self.simulation_params = {
            'gdp_base_growth': 2.5,
            'unemployment_base': 4.0,
            'inflation_base': 2.0,
            'cycle_length_years': 8.5,
            'volatility_factor': 0.3
        }
        
        log_info("Ultra Economic Cycle Analyzer initialized with professional macro indicators")
    
    def calculate_ultra_economic_position(self, date: datetime = None) -> Dict:
        """Calculate ultra-precise economic cycle position with professional accuracy"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            # Simulate current economic indicators
            economic_indicators = self._simulate_economic_indicators(date)
            
            # Calculate business cycle position
            cycle_analysis = self._analyze_business_cycle_position(economic_indicators, date)
            
            # Calculate recession probability
            recession_prob = self._calculate_recession_probability(economic_indicators)
            
            # Analyze yield curve dynamics
            yield_curve_analysis = self._analyze_yield_curve(date)
            
            # Calculate leading economic indicators composite
            lei_composite = self._calculate_lei_composite(economic_indicators)
            
            # Analyze credit conditions
            credit_analysis = self._analyze_credit_conditions(date)
            
            # Calculate consumer and business sentiment
            sentiment_analysis = self._analyze_economic_sentiment(date)
            
            # Determine optimal sector allocation
            sector_allocation = self._calculate_sector_allocation(cycle_analysis['current_phase'])
            
            return {
                'economic_indicators': economic_indicators,
                'business_cycle': cycle_analysis,
                'recession_probability': recession_prob,
                'yield_curve': yield_curve_analysis,
                'lei_composite': lei_composite,
                'credit_conditions': credit_analysis,
                'economic_sentiment': sentiment_analysis,
                'sector_allocation': sector_allocation,
                'macro_environment': self._assess_macro_environment(economic_indicators, recession_prob)
            }
            
        except Exception as e:
            log_error(f"Ultra economic position calculation error: {e}")
            return self._get_default_economic_data()
    
    def _simulate_economic_indicators(self, date: datetime) -> Dict:
        """Simulate current economic indicators (in practice, would fetch real data)"""
        try:
            # Calculate cycle position (years since 2020 recession)
            years_since_trough = (date - datetime(2020, 4, 1)).days / 365.25
            cycle_position = (years_since_trough % self.simulation_params['cycle_length_years']) / self.simulation_params['cycle_length_years']
            
            # Simulate GDP growth
            gdp_cycle = np.sin(cycle_position * 2 * np.pi) * 2.0 + self.simulation_params['gdp_base_growth']
            gdp_noise = np.random.normal(0, 0.5)
            gdp_growth = gdp_cycle + gdp_noise
            
            # Simulate unemployment rate
            unemployment_cycle = -np.sin(cycle_position * 2 * np.pi + np.pi/2) * 2.0 + self.simulation_params['unemployment_base']
            unemployment_noise = np.random.normal(0, 0.3)
            unemployment_rate = max(2.0, unemployment_cycle + unemployment_noise)
            
            # Simulate inflation
            inflation_cycle = np.sin(cycle_position * 2 * np.pi + np.pi/4) * 1.5 + self.simulation_params['inflation_base']
            inflation_noise = np.random.normal(0, 0.4)
            inflation_rate = max(0.0, inflation_cycle + inflation_noise)
            
            # Simulate yield curve (10Y - 2Y spread)
            yield_spread_base = 1.5 - (cycle_position * 3.0)  # Flattens as cycle matures
            yield_spread_noise = np.random.normal(0, 0.3)
            yield_spread = yield_spread_base + yield_spread_noise
            
            # Simulate PMI
            pmi_cycle = np.sin(cycle_position * 2 * np.pi) * 8.0 + 52.0
            pmi_noise = np.random.normal(0, 2.0)
            manufacturing_pmi = max(35.0, min(65.0, pmi_cycle + pmi_noise))
            
            # Simulate consumer confidence
            confidence_cycle = np.sin(cycle_position * 2 * np.pi) * 20.0 + 100.0
            confidence_noise = np.random.normal(0, 5.0)
            consumer_confidence = max(60.0, min(140.0, confidence_cycle + confidence_noise))
            
            # Calculate momentum indicators
            unemployment_change = unemployment_rate - self.simulation_params['unemployment_base']
            
            return {
                'gdp_growth_rate': round(gdp_growth, 2),
                'unemployment_rate': round(unemployment_rate, 1),
                'unemployment_change': round(unemployment_change, 1),
                'inflation_rate': round(inflation_rate, 2),
                'yield_spread_10y2y': round(yield_spread, 2),
                'manufacturing_pmi': round(manufacturing_pmi, 1),
                'consumer_confidence': round(consumer_confidence, 1),
                'cycle_position': round(cycle_position, 3),
                'analysis_date': date.isoformat()
            }
            
        except Exception as e:
            log_warning(f"Economic indicators simulation error: {e}")
            return self._get_default_indicators()
    
    def _analyze_business_cycle_position(self, indicators: Dict, date: datetime) -> Dict:
        """Analyze current business cycle position with professional methodology"""
        try:
            gdp_growth = indicators['gdp_growth_rate']
            unemployment_rate = indicators['unemployment_rate']
            unemployment_change = indicators['unemployment_change']
            pmi = indicators['manufacturing_pmi']
            cycle_position = indicators['cycle_position']
            
            # Determine cycle phase using multiple indicators
            phase_scores = {}
            
            # Expansion phase indicators
            expansion_score = 0
            if gdp_growth > 2.0:
                expansion_score += 2
            if unemployment_change < -0.2:
                expansion_score += 2
            if pmi > 52:
                expansion_score += 1
            if 0.1 < cycle_position < 0.6:
                expansion_score += 1
            
            # Peak phase indicators
            peak_score = 0
            if 1.0 < gdp_growth < 3.0:
                peak_score += 1
            if unemployment_rate < 4.5 and abs(unemployment_change) < 0.3:
                peak_score += 2
            if pmi > 50:
                peak_score += 1
            if 0.6 < cycle_position < 0.8:
                peak_score += 2
            
            # Contraction phase indicators
            contraction_score = 0
            if gdp_growth < 1.0:
                contraction_score += 2
            if unemployment_change > 0.3:
                contraction_score += 2
            if pmi < 50:
                contraction_score += 2
            if 0.8 < cycle_position or cycle_position < 0.1:
                contraction_score += 1
            
            # Trough phase indicators
            trough_score = 0
            if -2.0 < gdp_growth < 2.0:
                trough_score += 1
            if unemployment_rate > 6.0 and abs(unemployment_change) < 0.2:
                trough_score += 2
            if 45 < pmi < 52:
                trough_score += 1
            if cycle_position < 0.2:
                trough_score += 1
            
            phase_scores = {
                'expansion': expansion_score,
                'peak': peak_score,
                'contraction': contraction_score,
                'trough': trough_score
            }
            
            # Determine most likely phase
            current_phase = max(phase_scores.items(), key=lambda x: x[1])[0]
            phase_confidence = phase_scores[current_phase] / 6.0  # Normalize to 0-1
            
            # Get phase characteristics
            phase_data = self.business_cycle_phases[current_phase]
            
            # Calculate phase progression
            phase_progression = self._calculate_phase_progression(current_phase, cycle_position)
            
            return {
                'current_phase': current_phase,
                'phase_confidence': round(phase_confidence, 2),
                'phase_scores': phase_scores,
                'phase_characteristics': phase_data,
                'phase_progression': phase_progression,
                'expected_duration_months': phase_data['duration_months'],
                'market_outlook': phase_data['market_performance'],
                'recommended_sectors': phase_data['sector_leaders']
            }
            
        except Exception as e:
            log_warning(f"Business cycle analysis error: {e}")
            return {
                'current_phase': 'expansion', 
                'phase_confidence': 0.5,
                'phase_scores': {},
                'phase_characteristics': {},
                'market_outlook': 'neutral',
                'recommended_sectors': []
            }
    
    def _calculate_recession_probability(self, indicators: Dict) -> Dict:
        """Calculate recession probability using professional models"""
        try:
            # Sahm Rule: 3-month average unemployment rise of 0.5% or more
            unemployment_change = indicators['unemployment_change']
            sahm_rule_triggered = unemployment_change >= 0.5
            sahm_probability = min(1.0, max(0.0, unemployment_change / 1.0))
            
            # Yield curve inversion
            yield_spread = indicators['yield_spread_10y2y']
            yield_inversion = yield_spread < 0
            yield_probability = max(0.0, -yield_spread / 2.0) if yield_inversion else 0.0
            
            # Credit conditions (simulated)
            credit_stress_probability = 0.2  # Baseline credit stress
            
            # Employment momentum
            employment_probability = min(1.0, max(0.0, unemployment_change / 1.5))
            
            # Consumer spending weakness (simulated)
            consumer_confidence = indicators['consumer_confidence']
            consumer_probability = max(0.0, (100 - consumer_confidence) / 40.0)
            
            # Calculate composite recession probability
            total_probability = 0.0
            factor_contributions = {}
            
            for factor, data in self.recession_factors.items():
                weight = data['weight']
                
                if factor == 'sahm_rule':
                    prob = sahm_probability
                elif factor == 'yield_inversion':
                    prob = yield_probability
                elif factor == 'credit_conditions':
                    prob = credit_stress_probability
                elif factor == 'employment_momentum':
                    prob = employment_probability
                elif factor == 'consumer_spending':
                    prob = consumer_probability
                else:
                    prob = 0.0
                
                factor_contributions[factor] = {
                    'probability': round(prob, 3),
                    'weight': weight,
                    'contribution': round(prob * weight, 3)
                }
                total_probability += prob * weight
            
            # Cap at 100%
            total_probability = min(1.0, total_probability)
            
            # Risk level classification
            if total_probability > 0.7:
                risk_level = 'VERY_HIGH'
            elif total_probability > 0.5:
                risk_level = 'HIGH'
            elif total_probability > 0.3:
                risk_level = 'MODERATE'
            elif total_probability > 0.15:
                risk_level = 'LOW'
            else:
                risk_level = 'VERY_LOW'
            
            return {
                'total_probability': round(total_probability, 3),
                'risk_level': risk_level,
                'factor_contributions': factor_contributions,
                'sahm_rule_triggered': sahm_rule_triggered,
                'yield_curve_inverted': yield_inversion,
                'key_warning_signals': self._identify_warning_signals(factor_contributions)
            }
            
        except Exception as e:
            log_warning(f"Recession probability calculation error: {e}")
            return {
                'total_probability': 0.2, 
                'risk_level': 'LOW',
                'sahm_rule_triggered': False,
                'yield_curve_inverted': False,
                'factor_contributions': {}
            }
    
    def _analyze_yield_curve(self, date: datetime) -> Dict:
        """Analyze yield curve dynamics and implications"""
        try:
            # Simulate yield curve data (in practice, would fetch from FRED/Bloomberg)
            current_date = date
            
            # Simulate various spreads
            spread_10y2y = np.random.normal(1.5, 0.8)
            spread_10y3m = np.random.normal(2.0, 1.0)
            spread_5y2y = np.random.normal(0.8, 0.5)
            
            # Analyze curve shape
            if spread_10y2y < -0.25 and spread_10y3m < 0:
                curve_shape = 'deeply_inverted'
                recession_signal = 'STRONG'
            elif spread_10y2y < 0:
                curve_shape = 'inverted'
                recession_signal = 'MODERATE'
            elif spread_10y2y < 0.5:
                curve_shape = 'flattening'
                recession_signal = 'WEAK'
            elif spread_10y2y > 2.0:
                curve_shape = 'steep'
                recession_signal = 'NONE'
            else:
                curve_shape = 'normal'
                recession_signal = 'NONE'
            
            # Historical context
            percentile_10y2y = self._calculate_historical_percentile(spread_10y2y, 1.5, 1.0)
            
            return {
                'spread_10y2y': round(spread_10y2y, 2),
                'spread_10y3m': round(spread_10y3m, 2),
                'spread_5y2y': round(spread_5y2y, 2),
                'curve_shape': curve_shape,
                'recession_signal_strength': recession_signal,
                'historical_percentile': round(percentile_10y2y, 1),
                'market_implications': self._get_yield_curve_implications(curve_shape)
            }
            
        except Exception as e:
            log_warning(f"Yield curve analysis error: {e}")
            return {'curve_shape': 'normal', 'recession_signal_strength': 'NONE'}
    
    def calculate_ultra_economic_score(self, symbol: str, date: datetime = None) -> Dict:
        """Calculate ultra-sophisticated economic cycle trading score"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            # Get comprehensive economic data
            economic_data = self.calculate_ultra_economic_position(date)
            
            # Base score from economic cycle
            base_score = 50.0
            
            # Business cycle phase adjustment
            cycle_adjustment = self._get_cycle_phase_adjustment(economic_data['business_cycle'])
            
            # Recession probability penalty
            recession_penalty = economic_data['recession_probability']['total_probability'] * -25.0
            
            # Yield curve impact
            yield_curve_adjustment = self._get_yield_curve_adjustment(economic_data['yield_curve'])
            
            # Leading indicators impact
            lei_adjustment = self._get_lei_adjustment(economic_data['lei_composite'])
            
            # Credit conditions impact
            credit_adjustment = self._get_credit_adjustment(economic_data['credit_conditions'])
            
            # Symbol-specific economic sensitivity
            symbol_sensitivity = self._calculate_symbol_economic_sensitivity(symbol, economic_data)
            
            # Sector rotation benefit
            sector_rotation_bonus = self._calculate_sector_rotation_bonus(symbol, economic_data['business_cycle'])
            
            # Calculate final score
            final_score = (
                base_score +
                cycle_adjustment +
                recession_penalty +
                yield_curve_adjustment +
                lei_adjustment +
                credit_adjustment +
                symbol_sensitivity +
                sector_rotation_bonus
            )
            
            final_score = max(0, min(100, final_score))
            
            # Generate detailed analysis
            analysis = self._generate_economic_analysis(economic_data, symbol, final_score)
            
            return {
                'ultra_economic_score': final_score,
                'economic_data': economic_data,
                'analysis': analysis,
                'components': {
                    'base_score': base_score,
                    'cycle_adjustment': cycle_adjustment,
                    'recession_penalty': recession_penalty,
                    'yield_curve_adjustment': yield_curve_adjustment,
                    'lei_adjustment': lei_adjustment,
                    'credit_adjustment': credit_adjustment,
                    'symbol_sensitivity': symbol_sensitivity,
                    'sector_rotation_bonus': sector_rotation_bonus
                }
            }
            
        except Exception as e:
            log_error(f"Ultra economic score calculation error: {e}")
            return {
                'ultra_economic_score': 50.0,
                'analysis': {'error': str(e)},
                'components': {}
            }
    
    def _get_cycle_phase_adjustment(self, cycle_data: Dict) -> float:
        """Calculate score adjustment based on business cycle phase"""
        try:
            phase = cycle_data['current_phase']
            confidence = cycle_data['phase_confidence']
            
            phase_adjustments = {
                'expansion': 8.0,      # Positive for growth
                'peak': -2.0,          # Neutral to slightly negative
                'contraction': -12.0,  # Negative for recession risk
                'trough': 6.0          # Positive for recovery potential
            }
            
            base_adjustment = phase_adjustments.get(phase, 0.0)
            confidence_multiplier = confidence
            
            return base_adjustment * confidence_multiplier
            
        except Exception as e:
            log_warning(f"Cycle phase adjustment error: {e}")
            return 0.0
    
    def _get_yield_curve_adjustment(self, yield_data: Dict) -> float:
        """Calculate adjustment based on yield curve analysis"""
        try:
            curve_shape = yield_data['curve_shape']
            signal_strength = yield_data['recession_signal_strength']
            
            shape_adjustments = {
                'deeply_inverted': -15.0,
                'inverted': -10.0,
                'flattening': -5.0,
                'normal': 2.0,
                'steep': 5.0
            }
            
            signal_multipliers = {
                'STRONG': 1.2,
                'MODERATE': 1.0,
                'WEAK': 0.7,
                'NONE': 0.5
            }
            
            base_adjustment = shape_adjustments.get(curve_shape, 0.0)
            signal_multiplier = signal_multipliers.get(signal_strength, 1.0)
            
            return base_adjustment * signal_multiplier
            
        except Exception as e:
            log_warning(f"Yield curve adjustment error: {e}")
            return 0.0
    
    def _calculate_symbol_economic_sensitivity(self, symbol: str, economic_data: Dict) -> float:
        """Calculate symbol-specific economic sensitivity"""
        try:
            recession_prob = economic_data['recession_probability']['total_probability']
            gdp_growth = economic_data['economic_indicators']['gdp_growth_rate']
            
            # Cyclical stocks: High economic sensitivity
            if any(cyclical in symbol.upper() for cyclical in ['CAT', 'DE', 'BA', 'MMM', 'GE']):
                base_sensitivity = gdp_growth * 3.0 - recession_prob * 20.0
                
            # Technology: Moderate sensitivity with growth bias
            elif any(tech in symbol.upper() for tech in ['AAPL', 'MSFT', 'GOOGL', 'AMZN']):
                base_sensitivity = gdp_growth * 2.0 - recession_prob * 10.0
                
            # Financial: High recession sensitivity
            elif any(fin in symbol.upper() for fin in ['JPM', 'BAC', 'WFC', 'C']):
                base_sensitivity = gdp_growth * 2.5 - recession_prob * 25.0
                
            # Consumer Discretionary: Very high sensitivity
            elif any(disc in symbol.upper() for disc in ['AMZN', 'TSLA', 'HD', 'MCD']):
                base_sensitivity = gdp_growth * 4.0 - recession_prob * 30.0
                
            # Defensive sectors: Low sensitivity
            elif any(def_sec in symbol.upper() for def_sec in ['PG', 'JNJ', 'KO', 'WMT']):
                base_sensitivity = gdp_growth * 1.0 - recession_prob * 5.0
                
            # Utilities: Recession resistant
            elif any(util in symbol.upper() for util in ['NEE', 'DUK', 'SO']):
                base_sensitivity = -recession_prob * 3.0 + 2.0
                
            else:
                base_sensitivity = gdp_growth * 1.5 - recession_prob * 10.0
            
            return min(15.0, max(-15.0, base_sensitivity))
            
        except Exception as e:
            log_warning(f"Symbol economic sensitivity error: {e}")
            return 0.0
    
    def _calculate_sector_rotation_bonus(self, symbol: str, cycle_data: Dict) -> float:
        """Calculate bonus based on sector rotation patterns"""
        try:
            phase = cycle_data['current_phase']
            confidence = cycle_data['phase_confidence']
            
            # Map current phase to rotation phase
            if phase == 'trough':
                rotation_phase = 'late_contraction'
            elif phase == 'expansion':
                rotation_phase = 'early_expansion'
            elif phase == 'peak':
                rotation_phase = 'late_expansion'
            else:  # contraction
                rotation_phase = 'early_contraction'
            
            # Get favored sectors for this phase
            favored_sectors = self.sector_rotation_map.get(rotation_phase, [])
            
            # Check if symbol belongs to favored sector
            sector_bonus = 0.0
            
            for sector in favored_sectors:
                if sector == 'financials' and any(fin in symbol.upper() for fin in ['JPM', 'BAC', 'WFC']):
                    sector_bonus = 8.0
                elif sector == 'technology' and any(tech in symbol.upper() for tech in ['AAPL', 'MSFT', 'GOOGL']):
                    sector_bonus = 8.0
                elif sector == 'consumer_discretionary' and any(disc in symbol.upper() for disc in ['AMZN', 'TSLA']):
                    sector_bonus = 8.0
                elif sector == 'industrials' and any(ind in symbol.upper() for ind in ['CAT', 'BA', 'GE']):
                    sector_bonus = 8.0
                elif sector == 'utilities' and any(util in symbol.upper() for util in ['NEE', 'DUK']):
                    sector_bonus = 8.0
                elif sector == 'healthcare' and any(health in symbol.upper() for health in ['JNJ', 'PFE']):
                    sector_bonus = 8.0
                elif sector == 'consumer_staples' and any(staple in symbol.upper() for staple in ['PG', 'KO']):
                    sector_bonus = 8.0
            
            return sector_bonus * confidence
            
        except Exception as e:
            log_warning(f"Sector rotation bonus error: {e}")
            return 0.0
    
    def _generate_economic_analysis(self, economic_data: Dict, symbol: str, score: float) -> Dict:
        """Generate comprehensive economic analysis report"""
        try:
            cycle = economic_data['business_cycle']
            recession = economic_data['recession_probability']
            yield_curve = economic_data['yield_curve']
            
            # Primary insights
            insights = []
            
            if cycle['current_phase'] == 'expansion':
                insights.append("Economy in expansion phase supports growth stocks")
            elif cycle['current_phase'] == 'contraction':
                insights.append("Economic contraction favors defensive sectors")
            elif cycle['current_phase'] == 'peak':
                insights.append("Economic peak suggests increased volatility ahead")
            elif cycle['current_phase'] == 'trough':
                insights.append("Economic trough presents recovery opportunities")
            
            if recession['total_probability'] > 0.5:
                insights.append(f"High recession probability ({recession['total_probability']:.1%}) suggests caution")
            
            if yield_curve['curve_shape'] in ['inverted', 'deeply_inverted']:
                insights.append("Inverted yield curve signals economic slowdown")
            
            if recession['sahm_rule_triggered']:
                insights.append("Sahm Rule triggered - recession may have begun")
            
            # Trading recommendations
            if score > 70:
                recommendation = "BUY - Favorable economic conditions"
            elif score > 60:
                recommendation = "BUY - Positive economic backdrop"
            elif score > 40:
                recommendation = "HOLD - Mixed economic signals"
            elif score > 30:
                recommendation = "CAUTION - Challenging economic environment"
            else:
                recommendation = "AVOID - Adverse economic conditions"
            
            return {
                'score_interpretation': recommendation,
                'key_insights': insights,
                'business_cycle_phase': cycle['current_phase'],
                'phase_confidence': f"{cycle['phase_confidence']:.1%}",
                'recession_probability': f"{recession['total_probability']:.1%}",
                'recession_risk_level': recession['risk_level'],
                'yield_curve_shape': yield_curve['curve_shape'],
                'economic_outlook': cycle['market_outlook'],
                'recommended_sectors': cycle['recommended_sectors'][:3]  # Top 3
            }
            
        except Exception as e:
            log_warning(f"Economic analysis generation error: {e}")
            return {'score_interpretation': 'Unable to analyze', 'key_insights': []}
    
    def _calculate_lei_composite(self, indicators: Dict) -> Dict:
        """Calculate Leading Economic Indicators composite"""
        try:
            # Weighted composite of leading indicators
            lei_components = {
                'consumer_confidence': indicators['consumer_confidence'],
                'manufacturing_pmi': indicators['manufacturing_pmi'],
                'yield_spread': indicators['yield_spread_10y2y'],
                'unemployment_momentum': -indicators['unemployment_change']  # Negative is good
            }
            
            # Normalize and weight components
            normalized_components = {}
            total_score = 0.0
            
            # Consumer confidence (scale 60-140, normalize to -1 to 1)
            normalized_components['consumer_confidence'] = (lei_components['consumer_confidence'] - 100) / 40
            total_score += normalized_components['consumer_confidence'] * 0.3
            
            # PMI (scale 35-65, normalize to -1 to 1)
            normalized_components['manufacturing_pmi'] = (lei_components['manufacturing_pmi'] - 50) / 15
            total_score += normalized_components['manufacturing_pmi'] * 0.3
            
            # Yield spread (scale -2 to 4, normalize to -1 to 1)
            normalized_components['yield_spread'] = (lei_components['yield_spread'] - 1) / 3
            total_score += normalized_components['yield_spread'] * 0.25
            
            # Unemployment momentum (scale -2 to 2, already normalized)
            normalized_components['unemployment_momentum'] = max(-1, min(1, lei_components['unemployment_momentum']))
            total_score += normalized_components['unemployment_momentum'] * 0.15
            
            # Convert to 0-100 scale
            lei_composite_score = (total_score + 1) * 50
            
            # Determine trend
            if lei_composite_score > 60:
                trend = 'IMPROVING'
            elif lei_composite_score > 40:
                trend = 'STABLE'
            else:
                trend = 'DETERIORATING'
            
            return {
                'composite_score': round(lei_composite_score, 1),
                'trend': trend,
                'components': normalized_components,
                'interpretation': 'Economic conditions are ' + trend.lower()
            }
            
        except Exception as e:
            log_warning(f"LEI composite calculation error: {e}")
            return {'composite_score': 50.0, 'trend': 'STABLE'}
    
    def _analyze_credit_conditions(self, date: datetime) -> Dict:
        """Analyze credit market conditions"""
        try:
            # Simulate credit spreads and conditions
            high_yield_spread = max(2.0, np.random.normal(4.5, 1.5))
            investment_grade_spread = max(0.5, np.random.normal(1.5, 0.5))
            
            # Credit conditions assessment
            if high_yield_spread > 8.0:
                credit_conditions = 'SEVERELY_STRESSED'
                market_impact = 0.9
            elif high_yield_spread > 6.0:
                credit_conditions = 'STRESSED'
                market_impact = 0.7
            elif high_yield_spread > 4.0:
                credit_conditions = 'CAUTIOUS'
                market_impact = 0.4
            elif high_yield_spread > 2.5:
                credit_conditions = 'NORMAL'
                market_impact = 0.2
            else:
                credit_conditions = 'ACCOMMODATIVE'
                market_impact = 0.1
            
            return {
                'high_yield_spread': round(high_yield_spread, 1),
                'investment_grade_spread': round(investment_grade_spread, 1),
                'conditions': credit_conditions,
                'market_impact': market_impact,
                'lending_environment': 'tight' if market_impact > 0.6 else 'normal' if market_impact > 0.3 else 'loose'
            }
            
        except Exception as e:
            log_warning(f"Credit conditions analysis error: {e}")
            return {'conditions': 'NORMAL', 'market_impact': 0.2}
    
    def _analyze_economic_sentiment(self, date: datetime) -> Dict:
        """Analyze consumer and business sentiment"""
        try:
            # Simulate sentiment indicators
            consumer_sentiment = max(60, min(140, np.random.normal(95, 15)))
            business_confidence = max(30, min(70, np.random.normal(52, 8)))
            
            # Overall sentiment assessment
            avg_sentiment = (consumer_sentiment / 100 + business_confidence / 50) / 2
            
            if avg_sentiment > 1.1:
                sentiment_level = 'VERY_OPTIMISTIC'
            elif avg_sentiment > 0.95:
                sentiment_level = 'OPTIMISTIC'
            elif avg_sentiment > 0.85:
                sentiment_level = 'NEUTRAL'
            elif avg_sentiment > 0.75:
                sentiment_level = 'PESSIMISTIC'
            else:
                sentiment_level = 'VERY_PESSIMISTIC'
            
            return {
                'consumer_sentiment': round(consumer_sentiment, 1),
                'business_confidence': round(business_confidence, 1),
                'overall_sentiment': sentiment_level,
                'sentiment_score': round(avg_sentiment, 2)
            }
            
        except Exception as e:
            log_warning(f"Economic sentiment analysis error: {e}")
            return {'overall_sentiment': 'NEUTRAL', 'sentiment_score': 0.9}
    
    def _calculate_sector_allocation(self, cycle_phase: str) -> Dict:
        """Calculate optimal sector allocation based on cycle phase"""
        try:
            # Base allocation templates by phase
            allocations = {
                'expansion': {
                    'technology': 25, 'consumer_discretionary': 20, 'industrials': 15,
                    'financials': 12, 'materials': 10, 'energy': 8,
                    'healthcare': 5, 'utilities': 3, 'consumer_staples': 2
                },
                'peak': {
                    'energy': 20, 'materials': 18, 'utilities': 15,
                    'consumer_staples': 12, 'healthcare': 10, 'technology': 8,
                    'financials': 7, 'industrials': 5, 'consumer_discretionary': 5
                },
                'contraction': {
                    'consumer_staples': 25, 'healthcare': 20, 'utilities': 15,
                    'technology': 12, 'communications': 10, 'financials': 8,
                    'real_estate': 5, 'materials': 3, 'energy': 2
                },
                'trough': {
                    'technology': 20, 'financials': 18, 'real_estate': 15,
                    'consumer_discretionary': 12, 'industrials': 10, 'materials': 8,
                    'healthcare': 7, 'energy': 5, 'utilities': 5
                }
            }
            
            return {
                'recommended_allocation': allocations.get(cycle_phase, allocations['expansion']),
                'allocation_rationale': f"Optimized for {cycle_phase} phase characteristics",
                'rebalancing_frequency': 'quarterly' if cycle_phase in ['peak', 'trough'] else 'semi-annually'
            }
            
        except Exception as e:
            log_warning(f"Sector allocation calculation error: {e}")
            return {'recommended_allocation': {}, 'allocation_rationale': 'Unable to calculate'}
    
    # Helper methods
    def _calculate_phase_progression(self, phase: str, cycle_position: float) -> float:
        """Calculate how far through the current phase we are"""
        phase_ranges = {
            'expansion': (0.1, 0.6),
            'peak': (0.6, 0.8),
            'contraction': (0.8, 1.0),
            'trough': (0.0, 0.1)
        }
        
        if phase in phase_ranges:
            start, end = phase_ranges[phase]
            if phase == 'contraction' and cycle_position < 0.1:
                cycle_position += 1.0  # Handle wrap-around
            progression = (cycle_position - start) / (end - start)
            return max(0.0, min(1.0, progression))
        
        return 0.5
    
    def _identify_warning_signals(self, factor_contributions: Dict) -> List[str]:
        """Identify key economic warning signals"""
        warnings = []
        for factor, data in factor_contributions.items():
            if data['probability'] > 0.5:
                warnings.append(data['description'] if 'description' in data else factor)
        return warnings
    
    def _calculate_historical_percentile(self, value: float, mean: float, std: float) -> float:
        """Calculate historical percentile of a value"""
        z_score = (value - mean) / std
        # Convert to percentile (simplified)
        percentile = 50 + (z_score * 20)
        return max(0, min(100, percentile))
    
    def _get_yield_curve_implications(self, curve_shape: str) -> Dict:
        """Get market implications of yield curve shape"""
        implications = {
            'deeply_inverted': {'equity_outlook': 'bearish', 'bond_outlook': 'bullish', 'sectors_favored': ['utilities', 'consumer_staples']},
            'inverted': {'equity_outlook': 'cautious', 'bond_outlook': 'positive', 'sectors_favored': ['healthcare', 'consumer_staples']},
            'flattening': {'equity_outlook': 'neutral', 'bond_outlook': 'neutral', 'sectors_favored': ['technology', 'healthcare']},
            'normal': {'equity_outlook': 'positive', 'bond_outlook': 'neutral', 'sectors_favored': ['financials', 'industrials']},
            'steep': {'equity_outlook': 'bullish', 'bond_outlook': 'bearish', 'sectors_favored': ['financials', 'technology']}
        }
        return implications.get(curve_shape, {'equity_outlook': 'neutral', 'bond_outlook': 'neutral'})
    
    def _assess_macro_environment(self, indicators: Dict, recession_prob: Dict) -> str:
        """Assess overall macro environment"""
        gdp_growth = indicators['gdp_growth_rate']
        recession_probability = recession_prob['total_probability']
        
        if recession_probability > 0.6:
            return 'RECESSIONARY'
        elif recession_probability > 0.3:
            return 'CONTRACTIONARY'
        elif gdp_growth > 3.0:
            return 'EXPANSIONARY'
        elif gdp_growth > 1.5:
            return 'MODERATE_GROWTH'
        else:
            return 'SLOW_GROWTH'
    
    def _get_lei_adjustment(self, lei_data: Dict) -> float:
        """Calculate adjustment based on Leading Economic Indicators"""
        try:
            lei_score = lei_data['composite_score']
            # Convert LEI score to adjustment (-10 to +10)
            adjustment = (lei_score - 50) / 5
            return max(-10.0, min(10.0, adjustment))
        except Exception:
            return 0.0
    
    def _get_credit_adjustment(self, credit_data: Dict) -> float:
        """Calculate adjustment based on credit conditions"""
        try:
            market_impact = credit_data['market_impact']
            # Higher credit stress = negative adjustment
            adjustment = -market_impact * 12.0
            return adjustment
        except Exception:
            return 0.0
    
    def _get_default_economic_data(self) -> Dict:
        """Get default economic data for error conditions"""
        return {
            'business_cycle': {'current_phase': 'expansion', 'phase_confidence': 0.5},
            'recession_probability': {
                'total_probability': 0.2, 
                'risk_level': 'LOW',
                'sahm_rule_triggered': False,
                'yield_curve_inverted': False
            },
            'yield_curve': {'curve_shape': 'normal', 'recession_signal_strength': 'NONE'},
            'lei_composite': {'composite_score': 50.0, 'trend': 'STABLE'},
            'credit_conditions': {'conditions': 'NORMAL', 'market_impact': 0.2},
            'economic_sentiment': {'overall_sentiment': 'NEUTRAL'},
            'economic_indicators': {'gdp_growth_rate': 2.5, 'unemployment_rate': 4.0}
        }
    
    def _get_default_indicators(self) -> Dict:
        """Get default economic indicators"""
        return {
            'gdp_growth_rate': 2.5,
            'unemployment_rate': 4.0,
            'unemployment_change': 0.0,
            'inflation_rate': 2.0,
            'yield_spread_10y2y': 1.5,
            'manufacturing_pmi': 52.0,
            'consumer_confidence': 100.0,
            'cycle_position': 0.5
        }

# Create global instance
ultra_economic_analyzer = UltraEconomicCycleAnalyzer()

# Compatibility layer for existing code
class EconomicCycleAnalyzer:
    """Compatibility wrapper for existing Economic Cycle functionality"""
    
    def __init__(self):
        self.ultra_analyzer = ultra_economic_analyzer
        log_info("Economic Cycle Analyzer (compatibility mode) initialized")
    
    def calculate_economic_score(self, symbol: str = 'GENERAL', date: datetime = None) -> float:
        """Calculate economic score with compatibility wrapper"""
        ultra_result = self.ultra_analyzer.calculate_ultra_economic_score(symbol, date)
        return ultra_result['ultra_economic_score']
    
    def get_economic_analysis(self, date: datetime = None) -> Dict:
        """Get economic analysis with compatibility wrapper"""
        ultra_result = self.ultra_analyzer.calculate_ultra_economic_score('GENERAL', date)
        return {
            'score': ultra_result['ultra_economic_score'],
            'analysis_date': date.isoformat() if date else datetime.utcnow().isoformat(),
            'description': ultra_result['analysis']['score_interpretation']
        }

# Global instances
economic_analyzer = EconomicCycleAnalyzer()

# Compatibility function
def get_economic_cycle_score(symbol: str = 'GENERAL') -> float:
    """Economic cycle skorunu döndür"""
    try:
        return ultra_economic_analyzer.calculate_ultra_economic_score(symbol)['ultra_economic_score']
    except Exception as e:
        log_error(f"Economic cycle skoru hesaplanırken hata: {e}")
        return 50.0  # Varsayılan nötr skor
