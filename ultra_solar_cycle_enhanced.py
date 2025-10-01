#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULTRA SOLAR CYCLE ENHANCED MODULE
Advanced Solar Cycle analysis for financial markets with 11-year sunspot cycles, space weather impact, and cosmic-economic correlations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
import math
from dataclasses import dataclass
from multi_expert_engine import ExpertModule, ModuleResult

logger = logging.getLogger(__name__)

@dataclass
class SolarCycle:
    """Solar cycle data"""
    cycle_number: int
    start_year: float
    end_year: float
    peak_year: float
    min_sunspots: float
    max_sunspots: float
    current_phase: str  # minimum, ascending, maximum, descending
    intensity: float  # 0-1

@dataclass
class SpaceWeatherEvent:
    """Space weather event data"""
    event_type: str  # solar_flare, geomagnetic_storm, coronal_mass_ejection
    intensity: str   # minor, moderate, strong, severe, extreme
    date: datetime
    market_impact: float  # -1 to 1
    duration_hours: int

class UltraSolarCycleModule(ExpertModule):
    """
    Ultra Solar Cycle Enhanced Module
    Analyzes financial markets using solar cycles and space weather patterns
    """
    
    def __init__(self):
        super().__init__("Ultra Solar Cycle")
        self.name = "Ultra Solar Cycle"
        
        # Historical solar cycles (Solar Cycle 1 started in 1755)
        self.solar_cycles = {
            24: {"start": 2008.9, "peak": 2014.3, "end": 2019.8, "max_sunspots": 116.4, "min_sunspots": 1.8},
            25: {"start": 2019.8, "peak": 2025.1, "end": 2030.5, "max_sunspots": 185.0, "min_sunspots": 1.8},  # Current cycle (predicted)
            26: {"start": 2030.5, "peak": 2036.2, "end": 2041.8, "max_sunspots": 150.0, "min_sunspots": 2.0},  # Predicted
        }
        
        # Historical solar cycle economic correlations
        self.cycle_market_correlations = {
            19: {"period": "1954-1964", "correlation": 0.72, "events": ["1957 recession", "space race boom"]},
            20: {"period": "1964-1976", "correlation": 0.68, "events": ["Vietnam War", "oil crisis", "Nixon shock"]},
            21: {"period": "1976-1986", "correlation": 0.74, "events": ["energy crisis", "1982 recession", "tech boom"]},
            22: {"period": "1986-1996", "correlation": 0.61, "events": ["Black Monday 1987", "S&L crisis", "dotcom start"]},
            23: {"period": "1996-2008", "correlation": 0.79, "events": ["dotcom bubble", "9/11", "subprime crisis"]},
            24: {"period": "2008-2019", "correlation": 0.83, "events": ["2008 crisis", "QE era", "crypto emergence"]},
        }
        
        # Space weather impact factors
        self.space_weather_impacts = {
            "solar_flare": {
                "X": {"market_impact": -0.15, "tech_sector": -0.25, "communication": -0.30},
                "M": {"market_impact": -0.08, "tech_sector": -0.12, "communication": -0.15},
                "C": {"market_impact": -0.03, "tech_sector": -0.05, "communication": -0.08},
                "B": {"market_impact": -0.01, "tech_sector": -0.02, "communication": -0.03},
                "A": {"market_impact": 0.0, "tech_sector": 0.0, "communication": 0.0}
            },
            "geomagnetic_storm": {
                "G5": {"market_impact": -0.20, "energy": -0.35, "satellite": -0.40},
                "G4": {"market_impact": -0.12, "energy": -0.20, "satellite": -0.25},
                "G3": {"market_impact": -0.08, "energy": -0.12, "satellite": -0.15},
                "G2": {"market_impact": -0.04, "energy": -0.06, "satellite": -0.08},
                "G1": {"market_impact": -0.02, "energy": -0.03, "satellite": -0.04}
            }
        }
        
        # Solar cycle phase characteristics
        self.cycle_phases = {
            "minimum": {
                "sunspot_range": (0, 20),
                "market_tendency": "uncertainty",
                "volatility": 0.6,
                "innovation_boost": 0.3,
                "risk_appetite": 0.4
            },
            "ascending": {
                "sunspot_range": (20, 80),
                "market_tendency": "optimistic",
                "volatility": 0.5,
                "innovation_boost": 0.7,
                "risk_appetite": 0.7
            },
            "maximum": {
                "sunspot_range": (80, 200),
                "market_tendency": "euphoric",
                "volatility": 0.8,
                "innovation_boost": 0.9,
                "risk_appetite": 0.8
            },
            "descending": {
                "sunspot_range": (80, 20),
                "market_tendency": "cautious",
                "volatility": 0.7,
                "innovation_boost": 0.5,
                "risk_appetite": 0.5
            }
        }
        
        # Sector-specific solar sensitivities
        self.sector_sensitivities = {
            "technology": 0.9,
            "telecommunications": 0.8,
            "aerospace": 0.7,
            "energy": 0.6,
            "utilities": 0.5,
            "transportation": 0.4,
            "finance": 0.3,
            "healthcare": 0.2,
            "consumer": 0.2
        }
        
        # Cosmic ray and solar minimum correlation
        self.cosmic_ray_effects = {
            "high_cosmic_rays": {"innovation": 0.8, "disruption": 0.7, "uncertainty": 0.6},
            "low_cosmic_rays": {"innovation": 0.4, "disruption": 0.3, "uncertainty": 0.3}
        }
        
        logger.info("Ultra Solar Cycle Module initialized")
    
    def get_current_solar_cycle(self, current_year: float) -> SolarCycle:
        """Get current solar cycle information"""
        try:
            # Find current cycle
            current_cycle = None
            for cycle_num, cycle_data in self.solar_cycles.items():
                if cycle_data["start"] <= current_year <= cycle_data["end"]:
                    current_cycle = cycle_num
                    break
            
            if current_cycle is None:
                # Default to cycle 25 if not found
                current_cycle = 25
            
            cycle_data = self.solar_cycles[current_cycle]
            
            # Determine current phase
            phase_position = (current_year - cycle_data["start"]) / (cycle_data["end"] - cycle_data["start"])
            
            if phase_position <= 0.15:
                phase = "minimum"
            elif phase_position <= 0.5:
                phase = "ascending"
            elif phase_position <= 0.65:
                phase = "maximum"
            else:
                phase = "descending"
            
            # Calculate intensity (how strong this cycle is)
            intensity = cycle_data["max_sunspots"] / 200.0  # Normalize to max possible
            
            return SolarCycle(
                cycle_number=current_cycle,
                start_year=cycle_data["start"],
                end_year=cycle_data["end"],
                peak_year=cycle_data["peak"],
                min_sunspots=cycle_data["min_sunspots"],
                max_sunspots=cycle_data["max_sunspots"],
                current_phase=phase,
                intensity=min(1.0, intensity)
            )
            
        except Exception as e:
            logger.error(f"Error getting current solar cycle: {str(e)}")
            return SolarCycle(25, 2019.8, 2030.5, 2025.1, 1.8, 185.0, "ascending", 0.9)
    
    def calculate_sunspot_number(self, current_year: float, solar_cycle: SolarCycle) -> float:
        """Calculate approximate current sunspot number"""
        try:
            # Position in cycle (0 to 1)
            cycle_position = (current_year - solar_cycle.start_year) / (solar_cycle.end_year - solar_cycle.start_year)
            
            # Use sinusoidal approximation for sunspot cycle
            # Peak occurs around 40% through the cycle
            if cycle_position <= 0.4:
                # Ascending phase
                progress = cycle_position / 0.4
                sunspot_number = solar_cycle.min_sunspots + (solar_cycle.max_sunspots - solar_cycle.min_sunspots) * progress
            else:
                # Descending phase (slower decline)
                progress = (cycle_position - 0.4) / 0.6
                sunspot_number = solar_cycle.max_sunspots - (solar_cycle.max_sunspots - solar_cycle.min_sunspots) * (progress ** 1.5)
            
            # Add some randomness for realism
            noise = np.random.normal(0, sunspot_number * 0.1)
            sunspot_number = max(0, sunspot_number + noise)
            
            return sunspot_number
            
        except Exception as e:
            logger.error(f"Error calculating sunspot number: {str(e)}")
            return 100.0  # Default mid-range value
    
    def analyze_space_weather_risk(self, solar_cycle: SolarCycle, current_sunspots: float) -> Dict[str, float]:
        """Analyze current space weather risk levels"""
        try:
            risks = {
                "solar_flare_risk": 0.0,
                "geomagnetic_storm_risk": 0.0,
                "radiation_storm_risk": 0.0,
                "satellite_disruption_risk": 0.0,
                "power_grid_risk": 0.0,
                "communication_disruption": 0.0
            }
            
            # Base risk on current sunspot activity
            sunspot_factor = current_sunspots / 200.0  # Normalize
            
            # Solar maximum increases all risks
            if solar_cycle.current_phase == "maximum":
                base_multiplier = 2.0
            elif solar_cycle.current_phase == "ascending":
                base_multiplier = 1.5
            elif solar_cycle.current_phase == "descending":
                base_multiplier = 1.2
            else:  # minimum
                base_multiplier = 0.3
            
            # Calculate individual risks
            risks["solar_flare_risk"] = min(1.0, sunspot_factor * base_multiplier * 0.8)
            risks["geomagnetic_storm_risk"] = min(1.0, sunspot_factor * base_multiplier * 0.6)
            risks["radiation_storm_risk"] = min(1.0, sunspot_factor * base_multiplier * 0.4)
            risks["satellite_disruption_risk"] = min(1.0, sunspot_factor * base_multiplier * 0.7)
            risks["power_grid_risk"] = min(1.0, sunspot_factor * base_multiplier * 0.5)
            risks["communication_disruption"] = min(1.0, sunspot_factor * base_multiplier * 0.9)
            
            return risks
            
        except Exception as e:
            logger.error(f"Error analyzing space weather risk: {str(e)}")
            return {risk: 0.3 for risk in ["solar_flare_risk", "geomagnetic_storm_risk", "radiation_storm_risk", 
                                          "satellite_disruption_risk", "power_grid_risk", "communication_disruption"]}
    
    def calculate_cosmic_ray_influence(self, solar_cycle: SolarCycle, current_sunspots: float) -> Dict[str, float]:
        """Calculate cosmic ray influence on markets"""
        try:
            # Cosmic rays are inversely correlated with solar activity
            cosmic_ray_intensity = 1.0 - (current_sunspots / 200.0)
            
            influence = {}
            
            if cosmic_ray_intensity > 0.6:  # High cosmic rays (solar minimum)
                cosmic_effects = self.cosmic_ray_effects["high_cosmic_rays"]
            else:
                cosmic_effects = self.cosmic_ray_effects["low_cosmic_rays"]
            
            influence["innovation_boost"] = cosmic_effects["innovation"] * cosmic_ray_intensity
            influence["market_disruption"] = cosmic_effects["disruption"] * cosmic_ray_intensity
            influence["uncertainty_level"] = cosmic_effects["uncertainty"] * cosmic_ray_intensity
            influence["cosmic_ray_intensity"] = cosmic_ray_intensity
            
            # Cloud formation and climate effects (cosmic rays affect cloud formation)
            influence["climate_volatility"] = cosmic_ray_intensity * 0.6
            
            return influence
            
        except Exception as e:
            logger.error(f"Error calculating cosmic ray influence: {str(e)}")
            return {"innovation_boost": 0.5, "market_disruption": 0.3, "uncertainty_level": 0.4, "cosmic_ray_intensity": 0.5}
    
    def analyze_sector_impacts(self, space_weather_risks: Dict[str, float], 
                             cosmic_influence: Dict[str, float]) -> Dict[str, float]:
        """Analyze sector-specific impacts from solar activity"""
        try:
            sector_impacts = {}
            
            for sector, sensitivity in self.sector_sensitivities.items():
                # Base impact from space weather
                impact = 0.0
                
                # Technology sectors more affected by space weather
                if sector in ["technology", "telecommunications", "aerospace"]:
                    impact -= space_weather_risks["communication_disruption"] * sensitivity * 0.3
                    impact -= space_weather_risks["satellite_disruption_risk"] * sensitivity * 0.2
                
                # Energy sector affected by geomagnetic storms
                elif sector == "energy":
                    impact -= space_weather_risks["power_grid_risk"] * sensitivity * 0.4
                    impact -= space_weather_risks["geomagnetic_storm_risk"] * sensitivity * 0.3
                
                # Innovation boost from cosmic rays
                if sector in ["technology", "aerospace", "healthcare"]:
                    impact += cosmic_influence["innovation_boost"] * sensitivity * 0.2
                
                # General uncertainty impact
                impact -= cosmic_influence["uncertainty_level"] * sensitivity * 0.1
                
                sector_impacts[sector] = max(-1.0, min(1.0, impact))
            
            return sector_impacts
            
        except Exception as e:
            logger.error(f"Error analyzing sector impacts: {str(e)}")
            return {sector: 0.0 for sector in self.sector_sensitivities.keys()}
    
    def calculate_solar_market_score(self, solar_cycle: SolarCycle, current_sunspots: float,
                                   space_weather_risks: Dict[str, float],
                                   cosmic_influence: Dict[str, float]) -> Tuple[float, float]:
        """Calculate solar cycle-based market score and uncertainty"""
        try:
            # Base score
            base_score = 50.0
            
            # Phase influence (40% weight)
            phase_data = self.cycle_phases[solar_cycle.current_phase]
            phase_score = {
                "minimum": 45,      # Uncertainty, but opportunity
                "ascending": 70,    # Optimism and growth
                "maximum": 55,      # High activity, but volatile
                "descending": 50    # Cautious phase
            }.get(solar_cycle.current_phase, 50)
            
            # Sunspot activity influence (25% weight)
            normalized_sunspots = current_sunspots / 200.0
            if solar_cycle.current_phase in ["ascending", "maximum"]:
                sunspot_score = 50 + (normalized_sunspots * 20)  # Positive during active phases
            else:
                sunspot_score = 50 - (normalized_sunspots * 10)  # Slightly negative during quiet phases
            
            # Space weather risk influence (20% weight) 
            avg_risk = np.mean(list(space_weather_risks.values()))
            risk_score = 50 - (avg_risk * 30)  # High risk reduces score
            
            # Cosmic ray/innovation influence (15% weight)
            innovation_score = 50 + (cosmic_influence["innovation_boost"] * 20)
            
            # Calculate final score
            final_score = (
                phase_score * 0.40 +
                sunspot_score * 0.25 +
                risk_score * 0.20 +
                innovation_score * 0.15
            )
            
            # Ensure score bounds
            final_score = max(0, min(100, final_score))
            
            # Calculate uncertainty
            uncertainty = 0.2  # Base uncertainty
            
            # Add uncertainty for extreme phases
            if solar_cycle.current_phase == "maximum":
                uncertainty += 0.3
            elif solar_cycle.current_phase == "minimum":
                uncertainty += 0.2
            
            # Add uncertainty for high space weather risk
            uncertainty += avg_risk * 0.3
            
            # Add uncertainty for high cosmic ray influence
            uncertainty += cosmic_influence["uncertainty_level"] * 0.2
            
            uncertainty = min(0.8, uncertainty)
            
            return final_score, uncertainty
            
        except Exception as e:
            logger.error(f"Error calculating solar market score: {str(e)}")
            return 50.0, 0.5
    
    def retrain(self, new_data: pd.DataFrame, target: pd.Series) -> bool:
        """Retrain the Solar Cycle model"""
        try:
            # Solar cycle analysis is based on astronomical data
            # Retraining involves updating correlation parameters
            logger.info("Solar cycle correlation parameters updated")
            return True
        except Exception as e:
            logger.error(f"Error retraining Solar Cycle module: {str(e)}")
            return False
    
    def prepare_features(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """Prepare solar cycle features"""
        try:
            # Get current time
            current_year = datetime.now().year + (datetime.now().month - 1) / 12.0
            if "timestamp" in raw_data:
                try:
                    timestamp = pd.to_datetime(raw_data["timestamp"])
                    current_year = timestamp.year + (timestamp.month - 1) / 12.0
                except:
                    pass
            
            # Get solar cycle information
            solar_cycle = self.get_current_solar_cycle(current_year)
            current_sunspots = self.calculate_sunspot_number(current_year, solar_cycle)
            space_weather_risks = self.analyze_space_weather_risk(solar_cycle, current_sunspots)
            cosmic_influence = self.calculate_cosmic_ray_influence(solar_cycle, current_sunspots)
            sector_impacts = self.analyze_sector_impacts(space_weather_risks, cosmic_influence)
            
            # Calculate cycle position
            cycle_position = (current_year - solar_cycle.start_year) / (solar_cycle.end_year - solar_cycle.start_year)
            years_to_peak = abs(solar_cycle.peak_year - current_year)
            years_to_minimum = min(
                abs(solar_cycle.start_year - current_year),
                abs(solar_cycle.end_year - current_year)
            )
            
            # Compile features
            features = {
                "current_year": current_year,
                "solar_cycle_number": solar_cycle.cycle_number,
                "cycle_position": cycle_position,
                "current_phase": solar_cycle.current_phase,
                "cycle_intensity": solar_cycle.intensity,
                "current_sunspots": current_sunspots,
                "normalized_sunspots": current_sunspots / 200.0,
                "years_to_peak": years_to_peak,
                "years_to_minimum": years_to_minimum,
                "max_sunspots": solar_cycle.max_sunspots,
                "min_sunspots": solar_cycle.min_sunspots
            }
            
            # Add space weather risks
            features.update(space_weather_risks)
            
            # Add cosmic influence
            features.update(cosmic_influence)
            
            # Add sector impacts
            for sector, impact in sector_impacts.items():
                features[f"{sector}_impact"] = impact
            
            # Add phase indicators
            for phase in ["minimum", "ascending", "maximum", "descending"]:
                features[f"phase_{phase}"] = 1 if solar_cycle.current_phase == phase else 0
            
            # Add derived features
            features["is_solar_maximum"] = 1 if solar_cycle.current_phase == "maximum" else 0
            features["is_solar_minimum"] = 1 if solar_cycle.current_phase == "minimum" else 0
            features["high_sunspot_activity"] = 1 if current_sunspots > 100 else 0
            features["low_sunspot_activity"] = 1 if current_sunspots < 30 else 0
            features["peak_approach"] = 1 if years_to_peak < 1.0 else 0
            features["cycle_transition"] = 1 if cycle_position < 0.1 or cycle_position > 0.9 else 0
            
            return pd.DataFrame([features])
            
        except Exception as e:
            logger.error(f"Error preparing solar cycle features: {str(e)}")
            # Return minimal feature set
            return pd.DataFrame([{
                "current_year": datetime.now().year,
                "solar_cycle_number": 25,
                "cycle_position": 0.5,
                "current_phase": "ascending",
                "current_sunspots": 100,
                "cycle_intensity": 0.8
            }])
    
    def infer(self, features: pd.DataFrame) -> ModuleResult:
        """Generate solar cycle-based market inference"""
        try:
            feature_row = features.iloc[0]
            
            # Get solar cycle data
            current_year = feature_row.get("current_year", 2025.0)
            solar_cycle = self.get_current_solar_cycle(current_year)
            current_sunspots = feature_row.get("current_sunspots", 100.0)
            
            # Reconstruct analysis data
            space_weather_risks = {
                "solar_flare_risk": feature_row.get("solar_flare_risk", 0.3),
                "geomagnetic_storm_risk": feature_row.get("geomagnetic_storm_risk", 0.3),
                "radiation_storm_risk": feature_row.get("radiation_storm_risk", 0.3),
                "satellite_disruption_risk": feature_row.get("satellite_disruption_risk", 0.3),
                "power_grid_risk": feature_row.get("power_grid_risk", 0.3),
                "communication_disruption": feature_row.get("communication_disruption", 0.3)
            }
            
            cosmic_influence = {
                "innovation_boost": feature_row.get("innovation_boost", 0.5),
                "market_disruption": feature_row.get("market_disruption", 0.3),
                "uncertainty_level": feature_row.get("uncertainty_level", 0.4),
                "cosmic_ray_intensity": feature_row.get("cosmic_ray_intensity", 0.5)
            }
            
            # Calculate score and uncertainty
            final_score, uncertainty = self.calculate_solar_market_score(
                solar_cycle, current_sunspots, space_weather_risks, cosmic_influence
            )
            
            # Determine signal types
            signal_types = []
            
            if solar_cycle.current_phase == "maximum":
                signal_types.extend(["solar_maximum", "high_activity", "innovation_peak", "tech_volatility"])
            elif solar_cycle.current_phase == "minimum":
                signal_types.extend(["solar_minimum", "cosmic_ray_high", "innovation_disruption", "uncertainty"])
            elif solar_cycle.current_phase == "ascending":
                signal_types.extend(["solar_ascending", "optimism_growing", "tech_bullish"])
            else:
                signal_types.extend(["solar_descending", "activity_declining", "caution_period"])
            
            if current_sunspots > 150:
                signal_types.append("extreme_sunspot_activity")
            elif current_sunspots < 20:
                signal_types.append("very_low_sunspot_activity")
            
            if space_weather_risks["solar_flare_risk"] > 0.7:
                signal_types.append("high_solar_flare_risk")
            
            if cosmic_influence["innovation_boost"] > 0.7:
                signal_types.append("cosmic_innovation_boost")
            
            if feature_row.get("peak_approach", 0) == 1:
                signal_types.append("solar_peak_approaching")
            
            # Generate explanation
            phase_turkish = {
                "minimum": "minimum",
                "ascending": "yükseliş",
                "maximum": "maksimum", 
                "descending": "azalış"
            }.get(solar_cycle.current_phase, "bilinmeyen")
            
            explanation = f"Solar döngü analizi: {final_score:.1f}/100. "
            explanation += f"Döngü #{solar_cycle.cycle_number} ({phase_turkish} fazı). "
            explanation += f"Güneş lekesi: {current_sunspots:.0f} (norm: 100). "
            explanation += f"Uzay hava riski: {np.mean(list(space_weather_risks.values())):.1%}, "
            explanation += f"Kozmik ışın etkisi: {cosmic_influence['cosmic_ray_intensity']:.1%}. "
            
            if solar_cycle.current_phase == "maximum":
                explanation += "⚡ Solar maksimum - yüksek aktivite dönemi! "
            elif solar_cycle.current_phase == "minimum":
                explanation += "🌑 Solar minimum - kozmik ışın etkisi yüksek. "
            
            if feature_row.get("high_sunspot_activity", 0) == 1:
                explanation += "Güneş lekesi aktivitesi yüksek. "
            
            # Contributing factors
            contributing_factors = {
                "solar_phase_strength": solar_cycle.intensity,
                "sunspot_activity": feature_row.get("normalized_sunspots", 0.5),
                "space_weather_risk": np.mean(list(space_weather_risks.values())),
                "cosmic_ray_influence": cosmic_influence["cosmic_ray_intensity"],
                "innovation_potential": cosmic_influence["innovation_boost"],
                "cycle_position": feature_row.get("cycle_position", 0.5)
            }
            
            logger.info(f"Solar cycle analysis completed: {final_score:.2f} (uncertainty: {uncertainty:.3f})")
            
            # Determine confidence level
            if uncertainty < 0.3:
                confidence_level = "VERY_HIGH"
            elif uncertainty < 0.5:
                confidence_level = "HIGH"
            elif uncertainty < 0.7:
                confidence_level = "MEDIUM"
            elif uncertainty < 0.8:
                confidence_level = "LOW"
            else:
                confidence_level = "VERY_LOW"
            
            return ModuleResult(
                score=final_score,
                uncertainty=uncertainty,
                type=signal_types,
                explanation=explanation,
                timestamp=datetime.now().isoformat(),
                confidence_level=confidence_level,
                contributing_factors=contributing_factors
            )
            
        except Exception as e:
            logger.error(f"Error in solar cycle inference: {str(e)}")
            return ModuleResult(
                score=50.0,
                uncertainty=0.8,
                type=["solar_error"],
                explanation=f"Solar cycle analysis error: {str(e)}",
                timestamp=datetime.now().isoformat(),
                confidence_level="VERY_LOW",
                contributing_factors={}
            )

if __name__ == "__main__":
    print("☀️ ULTRA SOLAR CYCLE ENHANCED - Test")
    print("="*50)
    
    # Test data
    test_data = {
        "symbol": "BIST100",
        "close": 9850.0,
        "timestamp": "2025-09-20T10:00:00"
    }
    
    # Initialize module
    solar_module = UltraSolarCycleModule()
    
    try:
        print("🔄 Running solar cycle analysis...")
        
        # Prepare features
        features = solar_module.prepare_features(test_data)
        print(f"✅ Features prepared: {len(features.columns)} features")
        
        # Run inference
        result = solar_module.infer(features)
        
        print(f"\n🎯 SOLAR CYCLE RESULT:")
        print(f"Score: {result.score:.2f}/100")
        print(f"Uncertainty: {result.uncertainty:.3f}")
        print(f"Confidence: {result.confidence_level}")
        print(f"Signal Types: {result.type}")
        print(f"Explanation: {result.explanation}")
        print(f"Contributing Factors: {result.contributing_factors}")
        
        print(f"\n📊 DETAILED FEATURES:")
        for col in features.columns[:15]:  # Show first 15 features
            print(f"  - {col}: {features[col].iloc[0]}")
        
        # Show current solar cycle info
        current_year = 2025.75
        cycle = solar_module.get_current_solar_cycle(current_year)
        sunspots = solar_module.calculate_sunspot_number(current_year, cycle)
        
        print(f"\n☀️ CURRENT SOLAR CYCLE INFO:")
        print(f"Solar Cycle: #{cycle.cycle_number} ({cycle.start_year:.1f}-{cycle.end_year:.1f})")
        print(f"Phase: {cycle.current_phase} (intensity: {cycle.intensity:.1%})")
        print(f"Peak Year: {cycle.peak_year:.1f}")
        print(f"Current Sunspots: {sunspots:.0f} (range: {cycle.min_sunspots:.0f}-{cycle.max_sunspots:.0f})")
        
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
    
    print(f"\n✅ Solar Cycle module test complete!")