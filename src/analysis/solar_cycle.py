"""
PlanB Motoru - Ultra Solar Cycle Analysis Module
Ultra-expert level solar cycle analysis with professional astronomical calculations,
sunspot correlation, solar wind effects, electromagnetic market influences, and space weather
"""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
import math
import numpy as np
import requests
from src.utils.logger import log_info, log_error, log_debug, log_warning

class UltraSolarCycleAnalyzer:
    """Ultra-expert solar cycle and space weather analysis system"""
    
    def __init__(self):
        # Professional solar cycle data (Cycle 25 started in December 2019)
        self.current_cycle = 25
        self.cycle_start_date = datetime(2019, 12, 1)  # Solar Cycle 25 minimum
        self.average_cycle_length = 11.0  # Years
        self.cycle_variation = 1.5  # ±1.5 years variation
        
        # Historical solar cycle data for correlation analysis
        self.historical_cycles = {
            24: {'start': datetime(2008, 12, 1), 'peak': datetime(2014, 4, 1), 'end': datetime(2019, 12, 1)},
            23: {'start': datetime(1996, 5, 1), 'peak': datetime(2000, 3, 1), 'end': datetime(2008, 12, 1)},
            22: {'start': datetime(1986, 9, 1), 'peak': datetime(1989, 7, 1), 'end': datetime(1996, 5, 1)},
            21: {'start': datetime(1976, 6, 1), 'peak': datetime(1979, 12, 1), 'end': datetime(1986, 9, 1)}
        }
        
        # Solar activity impact coefficients for different market sectors
        self.sector_solar_sensitivity = {
            'technology': {'coefficient': 0.8, 'volatility_multiplier': 1.4},
            'telecommunications': {'coefficient': 0.9, 'volatility_multiplier': 1.6},
            'satellite_communications': {'coefficient': 1.0, 'volatility_multiplier': 1.8},
            'aerospace': {'coefficient': 0.7, 'volatility_multiplier': 1.3},
            'utilities': {'coefficient': 0.6, 'volatility_multiplier': 1.2},
            'energy': {'coefficient': 0.5, 'volatility_multiplier': 1.1},
            'mining': {'coefficient': 0.4, 'volatility_multiplier': 1.0},
            'financial': {'coefficient': 0.3, 'volatility_multiplier': 0.9}
        }
        
        # Geomagnetic activity levels and market correlations
        self.geomagnetic_levels = {
            'quiet': {'kp_range': (0, 2), 'market_impact': 0.1, 'description': 'Minimal market impact'},
            'unsettled': {'kp_range': (3, 4), 'market_impact': 0.3, 'description': 'Slight market volatility'},
            'active': {'kp_range': (5, 6), 'market_impact': 0.6, 'description': 'Moderate market disruption'},
            'storm': {'kp_range': (7, 8), 'market_impact': 0.8, 'description': 'Significant market impact'},
            'severe_storm': {'kp_range': (9, 9), 'market_impact': 1.0, 'description': 'Extreme market volatility'}
        }
        
        # Solar flare classifications and market effects
        self.solar_flare_classes = {
            'A': {'market_impact': 0.0, 'description': 'No market impact'},
            'B': {'market_impact': 0.1, 'description': 'Minimal impact'},
            'C': {'market_impact': 0.2, 'description': 'Minor satellite interference'},
            'M': {'market_impact': 0.5, 'description': 'Radio blackouts, tech volatility'},
            'X': {'market_impact': 0.8, 'description': 'Major infrastructure disruption'}
        }
        
        # Professional astronomical calculations for solar positioning
        self.solar_coordinates = {
            'declination_max': 23.44,  # Maximum solar declination
            'orbital_eccentricity': 0.0167,
            'perihelion_date': datetime(2025, 1, 4),  # Closest approach to sun
            'aphelion_date': datetime(2025, 7, 6)     # Farthest from sun
        }
        
        log_info("Ultra Solar Cycle Analyzer initialized with professional space weather data")
    
    def calculate_ultra_solar_position(self, date: datetime = None) -> Dict:
        """Calculate ultra-precise solar cycle position with professional accuracy"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            # Calculate current position in Solar Cycle 25
            days_since_cycle_start = (date - self.cycle_start_date).days
            cycle_position = days_since_cycle_start / (self.average_cycle_length * 365.25)
            
            # Predict solar maximum (typically 3-5 years after minimum)
            predicted_maximum_date = self.cycle_start_date + timedelta(days=4 * 365.25)
            days_to_maximum = (predicted_maximum_date - date).days
            
            # Calculate sunspot number estimation based on cycle position
            estimated_sunspot_number = self._calculate_sunspot_estimation(cycle_position)
            
            # Solar activity phase determination
            solar_phase = self._determine_solar_phase(cycle_position, days_to_maximum)
            
            # Geomagnetic activity simulation
            geomagnetic_data = self._simulate_geomagnetic_activity(date)
            
            # Solar wind parameters
            solar_wind_data = self._calculate_solar_wind_parameters(estimated_sunspot_number)
            
            # Earth's magnetic field interaction
            magnetic_field_impact = self._calculate_magnetic_field_impact(geomagnetic_data, solar_wind_data)
            
            return {
                'cycle_number': self.current_cycle,
                'cycle_position': cycle_position,
                'days_since_minimum': days_since_cycle_start,
                'days_to_predicted_maximum': days_to_maximum,
                'solar_phase': solar_phase,
                'estimated_sunspot_number': estimated_sunspot_number,
                'geomagnetic_activity': geomagnetic_data,
                'solar_wind': solar_wind_data,
                'magnetic_field_impact': magnetic_field_impact,
                'solar_declination': self._calculate_solar_declination(date),
                'earth_sun_distance': self._calculate_earth_sun_distance(date)
            }
            
        except Exception as e:
            log_error(f"Ultra solar position calculation error: {e}")
            return self._get_default_solar_data()
    
    def _calculate_sunspot_estimation(self, cycle_position: float) -> float:
        """Calculate estimated sunspot number based on cycle position"""
        try:
            # Solar cycle follows approximate sinusoidal pattern
            # Peak typically occurs around 0.3-0.4 of cycle
            if cycle_position < 0:
                return 5.0  # Solar minimum
            elif cycle_position > 1:
                return 20.0  # Post-cycle activity
            
            # Professional sunspot number calculation
            # Based on historical Cycle 24 data (peak ~80-90 sunspots)
            peak_position = 0.35  # Cycle 25 expected peak timing
            
            if cycle_position <= peak_position:
                # Ascending phase
                intensity = (cycle_position / peak_position) ** 1.5
                sunspot_number = 5 + (85 * intensity)  # 5 to 90 sunspots
            else:
                # Descending phase
                decline_position = (cycle_position - peak_position) / (1 - peak_position)
                intensity = (1 - decline_position) ** 2
                sunspot_number = 5 + (85 * intensity)
            
            # Add realistic variation
            variation = np.sin(cycle_position * 12 * np.pi) * 10  # Monthly variations
            return max(0, sunspot_number + variation)
            
        except Exception as e:
            log_warning(f"Sunspot estimation error: {e}")
            return 50.0
    
    def _determine_solar_phase(self, cycle_position: float, days_to_maximum: int) -> Dict:
        """Determine current solar phase with professional terminology"""
        try:
            if cycle_position < 0.1:
                phase = 'solar_minimum'
                description = 'Solar Minimum - Low activity period'
                market_influence = 'stable'
            elif cycle_position < 0.3:
                phase = 'ascending_phase'
                description = 'Ascending Phase - Increasing activity'
                market_influence = 'moderately_volatile'
            elif cycle_position < 0.5:
                phase = 'solar_maximum'
                description = 'Solar Maximum - Peak activity period'
                market_influence = 'highly_volatile'
            elif cycle_position < 0.8:
                phase = 'descending_phase'
                description = 'Descending Phase - Declining activity'
                market_influence = 'moderately_stable'
            else:
                phase = 'approaching_minimum'
                description = 'Approaching Minimum - Low activity'
                market_influence = 'stable'
            
            return {
                'phase': phase,
                'description': description,
                'market_influence': market_influence,
                'cycle_position': cycle_position,
                'volatility_expected': self._get_phase_volatility(phase)
            }
            
        except Exception as e:
            log_warning(f"Solar phase determination error: {e}")
            return {'phase': 'unknown', 'market_influence': 'neutral'}
    
    def _simulate_geomagnetic_activity(self, date: datetime) -> Dict:
        """Simulate current geomagnetic activity levels"""
        try:
            # Simulate Kp index (0-9 scale)
            # Base level varies with solar cycle
            cycle_pos = (date - self.cycle_start_date).days / (self.average_cycle_length * 365.25)
            base_kp = 1.5 + (cycle_pos * 2.5) if cycle_pos < 0.5 else 4 - (cycle_pos - 0.5) * 3
            
            # Add daily variations
            day_of_year = date.timetuple().tm_yday
            daily_variation = np.sin(day_of_year * 2 * np.pi / 365) * 1.2
            
            # Add random space weather events
            random_factor = np.random.normal(0, 0.8)
            
            kp_index = max(0, min(9, base_kp + daily_variation + random_factor))
            
            # Determine geomagnetic level
            for level, data in self.geomagnetic_levels.items():
                kp_min, kp_max = data['kp_range']
                if kp_min <= kp_index <= kp_max:
                    current_level = level
                    market_impact = data['market_impact']
                    description = data['description']
                    break
            else:
                current_level = 'quiet'
                market_impact = 0.1
                description = 'Minimal market impact'
            
            return {
                'kp_index': round(kp_index, 1),
                'level': current_level,
                'market_impact': market_impact,
                'description': description,
                'aurora_probability': min(1.0, kp_index / 5.0),
                'satellite_risk': min(1.0, (kp_index - 4) / 5.0) if kp_index > 4 else 0.0
            }
            
        except Exception as e:
            log_warning(f"Geomagnetic activity simulation error: {e}")
            return {'kp_index': 2.0, 'level': 'quiet', 'market_impact': 0.1}
    
    def _calculate_solar_wind_parameters(self, sunspot_number: float) -> Dict:
        """Calculate solar wind parameters affecting Earth"""
        try:
            # Solar wind speed correlation with sunspot activity
            base_speed = 400  # km/s typical quiet conditions
            activity_boost = (sunspot_number / 100) * 200  # Up to +200 km/s
            solar_wind_speed = base_speed + activity_boost
            
            # Magnetic field strength (nT - nanotesla)
            base_magnetic_field = 5.0  # nT
            magnetic_enhancement = (sunspot_number / 100) * 10  # Up to +10 nT
            interplanetary_magnetic_field = base_magnetic_field + magnetic_enhancement
            
            # Proton density
            base_density = 5.0  # protons/cm³
            density_variation = (sunspot_number / 100) * 15  # Up to +15 protons/cm³
            proton_density = base_density + density_variation
            
            # Calculate market disruption potential
            disruption_score = self._calculate_disruption_score(
                solar_wind_speed, interplanetary_magnetic_field, proton_density
            )
            
            return {
                'solar_wind_speed_kms': round(solar_wind_speed, 1),
                'magnetic_field_strength_nt': round(interplanetary_magnetic_field, 2),
                'proton_density_cm3': round(proton_density, 1),
                'disruption_potential': disruption_score,
                'technology_risk_level': 'high' if disruption_score > 0.7 else 'medium' if disruption_score > 0.4 else 'low'
            }
            
        except Exception as e:
            log_warning(f"Solar wind calculation error: {e}")
            return {'solar_wind_speed_kms': 400, 'disruption_potential': 0.2}
    
    def _calculate_magnetic_field_impact(self, geomagnetic_data: Dict, solar_wind_data: Dict) -> Dict:
        """Calculate Earth's magnetic field interaction effects"""
        try:
            kp_index = geomagnetic_data['kp_index']
            disruption_potential = solar_wind_data['disruption_potential']
            
            # Communication system impact
            communication_impact = min(1.0, (kp_index - 2) / 7 + disruption_potential * 0.3)
            
            # Power grid vulnerability
            power_grid_risk = min(1.0, (kp_index - 5) / 4 + disruption_potential * 0.4)
            
            # Satellite system effects
            satellite_impact = min(1.0, kp_index / 9 + disruption_potential * 0.5)
            
            # GPS accuracy degradation
            gps_degradation = min(1.0, (kp_index - 3) / 6 + disruption_potential * 0.2)
            
            # Overall infrastructure vulnerability
            infrastructure_vulnerability = (
                communication_impact * 0.3 +
                power_grid_risk * 0.3 +
                satellite_impact * 0.25 +
                gps_degradation * 0.15
            )
            
            return {
                'communication_impact': round(communication_impact, 3),
                'power_grid_risk': round(power_grid_risk, 3),
                'satellite_impact': round(satellite_impact, 3),
                'gps_degradation': round(gps_degradation, 3),
                'infrastructure_vulnerability': round(infrastructure_vulnerability, 3),
                'market_sector_risk': self._assess_sector_risks(infrastructure_vulnerability)
            }
            
        except Exception as e:
            log_warning(f"Magnetic field impact calculation error: {e}")
            return {'infrastructure_vulnerability': 0.2}
    
    def calculate_ultra_solar_score(self, symbol: str, date: datetime = None) -> Dict:
        """Calculate ultra-sophisticated solar cycle trading score"""
        try:
            if date is None:
                date = datetime.utcnow()
            
            # Get comprehensive solar data
            solar_data = self.calculate_ultra_solar_position(date)
            
            # Base score from solar cycle position
            base_score = 50.0
            
            # Solar phase adjustments
            phase = solar_data['solar_phase']
            phase_adjustment = self._get_phase_score_adjustment(phase)
            
            # Sunspot activity impact
            sunspot_adjustment = self._get_sunspot_adjustment(solar_data['estimated_sunspot_number'])
            
            # Geomagnetic activity impact
            geomagnetic_adjustment = self._get_geomagnetic_adjustment(solar_data['geomagnetic_activity'])
            
            # Solar wind effects
            solar_wind_adjustment = self._get_solar_wind_adjustment(solar_data['solar_wind'])
            
            # Symbol-specific solar sensitivity
            symbol_sensitivity = self._calculate_symbol_solar_sensitivity(symbol, solar_data)
            
            # Infrastructure vulnerability impact
            infrastructure_impact = solar_data['magnetic_field_impact']['infrastructure_vulnerability'] * -15
            
            # Calculate final score
            final_score = (
                base_score +
                phase_adjustment +
                sunspot_adjustment +
                geomagnetic_adjustment +
                solar_wind_adjustment +
                symbol_sensitivity +
                infrastructure_impact
            )
            
            final_score = max(0, min(100, final_score))
            
            # Generate detailed analysis
            analysis = self._generate_solar_analysis(solar_data, symbol, final_score)
            
            return {
                'ultra_solar_score': final_score,
                'solar_data': solar_data,
                'analysis': analysis,
                'components': {
                    'base_score': base_score,
                    'phase_adjustment': phase_adjustment,
                    'sunspot_adjustment': sunspot_adjustment,
                    'geomagnetic_adjustment': geomagnetic_adjustment,
                    'solar_wind_adjustment': solar_wind_adjustment,
                    'symbol_sensitivity': symbol_sensitivity,
                    'infrastructure_impact': infrastructure_impact
                }
            }
            
        except Exception as e:
            log_error(f"Ultra solar score calculation error: {e}")
            return {
                'ultra_solar_score': 50.0,
                'analysis': {'error': str(e)},
                'components': {}
            }
    
    def _get_phase_score_adjustment(self, phase: Dict) -> float:
        """Calculate score adjustment based on solar phase"""
        try:
            phase_adjustments = {
                'solar_minimum': 5.0,       # Stable conditions favor growth
                'ascending_phase': 2.0,     # Moderate positive impact
                'solar_maximum': -8.0,      # High volatility, risk averse
                'descending_phase': 1.0,    # Slight positive
                'approaching_minimum': 3.0  # Anticipation of stability
            }
            
            base_adjustment = phase_adjustments.get(phase['phase'], 0.0)
            volatility_penalty = phase['volatility_expected'] * -5.0
            
            return base_adjustment + volatility_penalty
            
        except Exception as e:
            log_warning(f"Phase score adjustment error: {e}")
            return 0.0
    
    def _get_sunspot_adjustment(self, sunspot_number: float) -> float:
        """Calculate adjustment based on sunspot activity"""
        try:
            if sunspot_number < 20:
                return 8.0   # Low activity = stable markets
            elif sunspot_number < 50:
                return 3.0   # Moderate activity
            elif sunspot_number < 80:
                return -2.0  # High activity = volatility
            else:
                return -10.0 # Extreme activity = market disruption
                
        except Exception as e:
            log_warning(f"Sunspot adjustment error: {e}")
            return 0.0
    
    def _get_geomagnetic_adjustment(self, geomagnetic_data: Dict) -> float:
        """Calculate adjustment based on geomagnetic activity"""
        try:
            market_impact = geomagnetic_data['market_impact']
            
            # Higher geomagnetic activity = more market uncertainty
            adjustment = -15.0 * market_impact
            
            # Satellite risk penalty for tech stocks
            satellite_risk = geomagnetic_data.get('satellite_risk', 0.0)
            tech_penalty = satellite_risk * -5.0
            
            return adjustment + tech_penalty
            
        except Exception as e:
            log_warning(f"Geomagnetic adjustment error: {e}")
            return 0.0
    
    def _get_solar_wind_adjustment(self, solar_wind_data: Dict) -> float:
        """Calculate adjustment based on solar wind parameters"""
        try:
            disruption_potential = solar_wind_data['disruption_potential']
            
            # High disruption potential affects technology sectors
            base_adjustment = -12.0 * disruption_potential
            
            # Technology risk level additional penalty
            tech_risk = solar_wind_data['technology_risk_level']
            risk_penalties = {'low': 0, 'medium': -3, 'high': -8}
            tech_penalty = risk_penalties.get(tech_risk, 0)
            
            return base_adjustment + tech_penalty
            
        except Exception as e:
            log_warning(f"Solar wind adjustment error: {e}")
            return 0.0
    
    def _calculate_symbol_solar_sensitivity(self, symbol: str, solar_data: Dict) -> float:
        """Calculate symbol-specific solar sensitivity"""
        try:
            # Technology companies: High solar sensitivity
            if any(tech in symbol.upper() for tech in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSM']):
                base_sensitivity = -8.0
                sector = 'technology'
            
            # Telecommunications: Very high sensitivity
            elif any(telecom in symbol.upper() for telecom in ['VZ', 'T', 'TMUS', 'CCI', 'AMT']):
                base_sensitivity = -12.0
                sector = 'telecommunications'
            
            # Satellite/Aerospace: Extreme sensitivity
            elif any(aero in symbol.upper() for aero in ['BA', 'LMT', 'RTX', 'NOC', 'VSAT']):
                base_sensitivity = -15.0
                sector = 'aerospace'
            
            # Utilities: Moderate sensitivity (power grid effects)
            elif any(utility in symbol.upper() for utility in ['NEE', 'DUK', 'SO', 'EXC']):
                base_sensitivity = -5.0
                sector = 'utilities'
            
            # Mining/Energy: Low sensitivity
            elif any(mining in symbol.upper() for mining in ['XOM', 'CVX', 'FCX', 'NEM']):
                base_sensitivity = -2.0
                sector = 'energy'
            
            # Financial: Very low sensitivity
            elif any(fin in symbol.upper() for fin in ['JPM', 'BAC', 'WFC', 'C']):
                base_sensitivity = 0.0
                sector = 'financial'
            
            else:
                base_sensitivity = -3.0
                sector = 'general'
            
            # Apply sector-specific multipliers
            if sector in self.sector_solar_sensitivity:
                sector_data = self.sector_solar_sensitivity[sector]
                sensitivity_multiplier = sector_data['coefficient']
                volatility_impact = solar_data['magnetic_field_impact']['infrastructure_vulnerability']
                
                adjusted_sensitivity = base_sensitivity * sensitivity_multiplier
                volatility_penalty = volatility_impact * sector_data['volatility_multiplier'] * -3.0
                
                return adjusted_sensitivity + volatility_penalty
            
            return base_sensitivity
            
        except Exception as e:
            log_warning(f"Symbol solar sensitivity error: {e}")
            return 0.0
    
    def _generate_solar_analysis(self, solar_data: Dict, symbol: str, score: float) -> Dict:
        """Generate comprehensive solar analysis report"""
        try:
            phase = solar_data['solar_phase']
            geomagnetic = solar_data['geomagnetic_activity']
            solar_wind = solar_data['solar_wind']
            magnetic_impact = solar_data['magnetic_field_impact']
            
            # Primary insights
            insights = []
            
            if phase['market_influence'] == 'highly_volatile':
                insights.append("Solar maximum period increases market volatility")
            
            if geomagnetic['level'] in ['storm', 'severe_storm']:
                insights.append(f"Geomagnetic {geomagnetic['level']} may disrupt technology sectors")
            
            if solar_wind['disruption_potential'] > 0.6:
                insights.append("High solar wind disruption potential affects satellites and communications")
            
            if magnetic_impact['infrastructure_vulnerability'] > 0.5:
                insights.append("Elevated infrastructure vulnerability from space weather")
            
            # Trading recommendations
            if score > 70:
                recommendation = "BUY - Favorable solar conditions"
            elif score > 60:
                recommendation = "BUY - Moderate solar environment"
            elif score > 40:
                recommendation = "HOLD - Mixed solar signals"
            elif score > 30:
                recommendation = "CAUTION - Adverse solar conditions"
            else:
                recommendation = "AVOID - Severe space weather risk"
            
            # Risk assessment
            tech_risk = "HIGH" if magnetic_impact['infrastructure_vulnerability'] > 0.6 else "MODERATE" if magnetic_impact['infrastructure_vulnerability'] > 0.3 else "LOW"
            
            return {
                'score_interpretation': recommendation,
                'key_insights': insights,
                'solar_phase': phase['phase'],
                'cycle_position': f"{solar_data['cycle_position']:.1%} through Cycle {solar_data['cycle_number']}",
                'geomagnetic_level': geomagnetic['level'],
                'technology_risk': tech_risk,
                'infrastructure_vulnerability': f"{magnetic_impact['infrastructure_vulnerability']:.1%}",
                'sunspot_estimate': f"{solar_data['estimated_sunspot_number']:.0f}"
            }
            
        except Exception as e:
            log_warning(f"Solar analysis generation error: {e}")
            return {'score_interpretation': 'Unable to analyze', 'key_insights': []}
    
    def _get_phase_volatility(self, phase: str) -> float:
        """Get expected volatility for solar phase"""
        volatility_map = {
            'solar_minimum': 0.2,
            'ascending_phase': 0.4,
            'solar_maximum': 0.9,
            'descending_phase': 0.5,
            'approaching_minimum': 0.3
        }
        return volatility_map.get(phase, 0.5)
    
    def _calculate_disruption_score(self, wind_speed: float, magnetic_field: float, density: float) -> float:
        """Calculate overall space weather disruption score"""
        try:
            # Normalize parameters to 0-1 scale
            speed_score = min(1.0, (wind_speed - 300) / 500)  # 300-800 km/s range
            field_score = min(1.0, (magnetic_field - 3) / 20)  # 3-23 nT range
            density_score = min(1.0, (density - 3) / 25)  # 3-28 protons/cm³ range
            
            # Weighted combination
            disruption_score = (
                speed_score * 0.4 +
                field_score * 0.4 +
                density_score * 0.2
            )
            
            return max(0.0, min(1.0, disruption_score))
            
        except Exception as e:
            log_warning(f"Disruption score calculation error: {e}")
            return 0.3
    
    def _assess_sector_risks(self, vulnerability: float) -> Dict:
        """Assess risk levels for different market sectors"""
        risk_multipliers = {
            'technology': vulnerability * 1.2,
            'telecommunications': vulnerability * 1.4,
            'aerospace': vulnerability * 1.6,
            'utilities': vulnerability * 1.0,
            'energy': vulnerability * 0.8,
            'financial': vulnerability * 0.6
        }
        
        risk_levels = {}
        for sector, risk_score in risk_multipliers.items():
            if risk_score > 0.7:
                risk_levels[sector] = 'HIGH'
            elif risk_score > 0.4:
                risk_levels[sector] = 'MEDIUM'
            else:
                risk_levels[sector] = 'LOW'
        
        return risk_levels
    
    def _calculate_solar_declination(self, date: datetime) -> float:
        """Calculate solar declination angle"""
        try:
            day_of_year = date.timetuple().tm_yday
            declination = self.solar_coordinates['declination_max'] * np.sin(
                np.radians(360 * (284 + day_of_year) / 365.25)
            )
            return round(declination, 2)
        except Exception:
            return 0.0
    
    def _calculate_earth_sun_distance(self, date: datetime) -> float:
        """Calculate Earth-Sun distance in AU"""
        try:
            day_of_year = date.timetuple().tm_yday
            # Simplified calculation
            distance = 1.0 + self.solar_coordinates['orbital_eccentricity'] * np.cos(
                np.radians(360 * (day_of_year - 4) / 365.25)
            )
            return round(distance, 6)
        except Exception:
            return 1.0
    
    def _get_default_solar_data(self) -> Dict:
        """Get default solar data for error conditions"""
        return {
            'cycle_number': 25,
            'cycle_position': 0.4,
            'solar_phase': {'phase': 'ascending_phase', 'market_influence': 'neutral'},
            'estimated_sunspot_number': 50.0,
            'geomagnetic_activity': {'level': 'quiet', 'market_impact': 0.1},
            'solar_wind': {'disruption_potential': 0.3},
            'magnetic_field_impact': {'infrastructure_vulnerability': 0.2}
        }

# Create global instance
ultra_solar_analyzer = UltraSolarCycleAnalyzer()

# Compatibility layer for existing code
class SolarCycleAnalyzer:
    """Compatibility wrapper for existing Solar Cycle functionality"""
    
    def __init__(self):
        self.ultra_analyzer = ultra_solar_analyzer
        log_info("Solar Cycle Analyzer (compatibility mode) initialized")
    
    def calculate_solar_score(self, current_date: Optional[datetime] = None) -> float:
        """Calculate solar score with compatibility wrapper"""
        ultra_result = self.ultra_analyzer.calculate_ultra_solar_score('GENERAL', current_date)
        return ultra_result['ultra_solar_score']
    
    def get_solar_analysis(self, current_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get solar analysis with compatibility wrapper"""
        ultra_result = self.ultra_analyzer.calculate_ultra_solar_score('GENERAL', current_date)
        return {
            'score': ultra_result['ultra_solar_score'],
            'analysis_date': current_date.isoformat() if current_date else datetime.utcnow().isoformat(),
            'description': ultra_result['analysis']['score_interpretation']
        }

# Global instances
solar_analyzer = SolarCycleAnalyzer()

# Compatibility function
def get_solar_cycle_score() -> float:
    """Güneş döngüsü skorunu döndür"""
    try:
        return ultra_solar_analyzer.calculate_ultra_solar_score('GENERAL')['ultra_solar_score']
    except Exception as e:
        log_error(f"Solar cycle skoru hesaplanırken hata: {e}")
        return 50.0  # Varsayılan nötr skor

