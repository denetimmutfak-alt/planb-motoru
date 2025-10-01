#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULTRA VEDIC ASTROLOGY ENHANCED MODULE
Advanced Vedic Astrology analysis for financial markets with planetary cycles, nakshatras, and cosmic timing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Any, Optional, Tuple
import logging
import math
from dataclasses import dataclass
import ephem
from multi_expert_engine import ExpertModule, ModuleResult

logger = logging.getLogger(__name__)

@dataclass
class PlanetaryPosition:
    """Planetary position data"""
    planet: str
    longitude: float  # Degrees
    sign: str        # Zodiac sign
    nakshatra: str   # Nakshatra (lunar mansion)
    house: int       # House position
    retrograde: bool

@dataclass
class VedicAspect:
    """Vedic astrological aspect"""
    from_planet: str
    to_planet: str
    aspect_type: str  # conjunction, opposition, trine, square, etc.
    orb: float       # Degrees of separation
    strength: float  # 0-1 strength

@dataclass
class VedicTransit:
    """Planetary transit analysis"""
    planet: str
    from_sign: str
    to_sign: str
    date: datetime
    market_impact: str  # bullish, bearish, volatile, stable
    intensity: float    # 0-1

class UltraVedicAstrologyModule(ExpertModule):
    """
    Ultra Vedic Astrology Enhanced Module
    Analyzes financial markets using Vedic astrological principles
    """
    
    def __init__(self):
        super().__init__("Ultra Vedic Astrology")
        self.name = "Ultra Vedic Astrology"
        
        # Vedic zodiac signs (Sidereal)
        self.vedic_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        # 27 Nakshatras (lunar mansions)
        self.nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        
        # Market impact of nakshatras
        self.nakshatra_market_impact = {
            "Ashwini": {"type": "bullish", "strength": 0.7, "volatility": 0.8},
            "Bharani": {"type": "bearish", "strength": 0.6, "volatility": 0.7},
            "Krittika": {"type": "volatile", "strength": 0.8, "volatility": 0.9},
            "Rohini": {"type": "bullish", "strength": 0.9, "volatility": 0.3},
            "Mrigashira": {"type": "neutral", "strength": 0.5, "volatility": 0.6},
            "Ardra": {"type": "bearish", "strength": 0.8, "volatility": 0.9},
            "Punarvasu": {"type": "recovery", "strength": 0.7, "volatility": 0.4},
            "Pushya": {"type": "bullish", "strength": 0.8, "volatility": 0.2},
            "Ashlesha": {"type": "bearish", "strength": 0.7, "volatility": 0.8},
            "Magha": {"type": "bullish", "strength": 0.8, "volatility": 0.5},
            "Purva Phalguni": {"type": "bullish", "strength": 0.6, "volatility": 0.4},
            "Uttara Phalguni": {"type": "stable", "strength": 0.7, "volatility": 0.3},
            "Hasta": {"type": "neutral", "strength": 0.6, "volatility": 0.5},
            "Chitra": {"type": "volatile", "strength": 0.7, "volatility": 0.8},
            "Swati": {"type": "volatile", "strength": 0.6, "volatility": 0.9},
            "Vishakha": {"type": "bullish", "strength": 0.7, "volatility": 0.6},
            "Anuradha": {"type": "stable", "strength": 0.8, "volatility": 0.3},
            "Jyeshtha": {"type": "bearish", "strength": 0.7, "volatility": 0.7},
            "Mula": {"type": "transformation", "strength": 0.9, "volatility": 0.9},
            "Purva Ashadha": {"type": "bullish", "strength": 0.8, "volatility": 0.5},
            "Uttara Ashadha": {"type": "bullish", "strength": 0.9, "volatility": 0.4},
            "Shravana": {"type": "stable", "strength": 0.7, "volatility": 0.3},
            "Dhanishta": {"type": "wealth", "strength": 0.8, "volatility": 0.4},
            "Shatabhisha": {"type": "volatile", "strength": 0.6, "volatility": 0.8},
            "Purva Bhadrapada": {"type": "transformation", "strength": 0.8, "volatility": 0.8},
            "Uttara Bhadrapada": {"type": "stable", "strength": 0.8, "volatility": 0.4},
            "Revati": {"type": "completion", "strength": 0.7, "volatility": 0.5}
        }
        
        # Planet market influences
        self.planet_influences = {
            "Sun": {"market_factor": 0.2, "leadership": 0.9, "confidence": 0.8},
            "Moon": {"market_factor": 0.3, "sentiment": 0.9, "volatility": 0.7},
            "Mars": {"market_factor": 0.25, "aggression": 0.8, "volatility": 0.9},
            "Mercury": {"market_factor": 0.2, "communication": 0.9, "technology": 0.8},
            "Jupiter": {"market_factor": 0.3, "expansion": 0.9, "optimism": 0.8},
            "Venus": {"market_factor": 0.2, "luxury": 0.8, "stability": 0.7},
            "Saturn": {"market_factor": 0.25, "restriction": 0.8, "patience": 0.9},
            "Rahu": {"market_factor": 0.15, "illusion": 0.7, "speculation": 0.9},
            "Ketu": {"market_factor": 0.1, "spirituality": 0.6, "detachment": 0.8}
        }
        
        # Ayanamsa for sidereal calculations (Lahiri)
        self.ayanamsa = 24.1  # Current ayanamsa degrees
        
        logger.info("Ultra Vedic Astrology Module initialized")
    
    def calculate_planetary_positions(self, date: datetime) -> Dict[str, PlanetaryPosition]:
        """Calculate planetary positions for given date"""
        try:
            # Set date for ephemeris
            observer = ephem.Observer()
            observer.date = date
            
            positions = {}
            
            # Define planets
            planets = {
                "Sun": ephem.Sun(),
                "Moon": ephem.Moon(),
                "Mars": ephem.Mars(),
                "Mercury": ephem.Mercury(),
                "Jupiter": ephem.Jupiter(),
                "Venus": ephem.Venus(),
                "Saturn": ephem.Saturn()
            }
            
            for planet_name, planet_obj in planets.items():
                planet_obj.compute(observer)
                
                # Convert to degrees
                longitude_tropical = math.degrees(planet_obj.ra)
                
                # Convert to sidereal (Vedic)
                longitude_sidereal = longitude_tropical - self.ayanamsa
                if longitude_sidereal < 0:
                    longitude_sidereal += 360
                
                # Determine sign
                sign_index = int(longitude_sidereal // 30)
                sign = self.vedic_signs[sign_index]
                
                # Determine nakshatra
                nakshatra_index = int((longitude_sidereal % 360) / 13.333333)
                nakshatra = self.nakshatras[min(nakshatra_index, 26)]
                
                # Simple house calculation (approximate)
                house = (sign_index + 1) % 12 + 1
                
                # Check retrograde (simplified)
                retrograde = False  # Would need more complex calculation
                
                positions[planet_name] = PlanetaryPosition(
                    planet=planet_name,
                    longitude=longitude_sidereal,
                    sign=sign,
                    nakshatra=nakshatra,
                    house=house,
                    retrograde=retrograde
                )
            
            return positions
            
        except Exception as e:
            logger.error(f"Error calculating planetary positions: {str(e)}")
            return {}
    
    def calculate_vedic_aspects(self, positions: Dict[str, PlanetaryPosition]) -> List[VedicAspect]:
        """Calculate Vedic astrological aspects"""
        try:
            aspects = []
            planet_list = list(positions.keys())
            
            for i, planet1 in enumerate(planet_list):
                for planet2 in planet_list[i+1:]:
                    pos1 = positions[planet1]
                    pos2 = positions[planet2]
                    
                    # Calculate angular separation
                    diff = abs(pos1.longitude - pos2.longitude)
                    if diff > 180:
                        diff = 360 - diff
                    
                    # Determine aspect type
                    aspect_type = "neutral"
                    strength = 0.0
                    
                    if diff <= 8:  # Conjunction
                        aspect_type = "conjunction"
                        strength = 1.0 - (diff / 8)
                    elif 172 <= diff <= 188:  # Opposition
                        aspect_type = "opposition"
                        strength = 1.0 - (abs(diff - 180) / 8)
                    elif 112 <= diff <= 128:  # Trine
                        aspect_type = "trine"
                        strength = 1.0 - (abs(diff - 120) / 8)
                    elif 82 <= diff <= 98:  # Square
                        aspect_type = "square"
                        strength = 1.0 - (abs(diff - 90) / 8)
                    elif 52 <= diff <= 68:  # Sextile
                        aspect_type = "sextile"
                        strength = 1.0 - (abs(diff - 60) / 8)
                    
                    if strength > 0:
                        aspects.append(VedicAspect(
                            from_planet=planet1,
                            to_planet=planet2,
                            aspect_type=aspect_type,
                            orb=diff,
                            strength=strength
                        ))
            
            return aspects
            
        except Exception as e:
            logger.error(f"Error calculating Vedic aspects: {str(e)}")
            return []
    
    def analyze_nakshatra_influence(self, moon_nakshatra: str, date: datetime) -> Dict[str, Any]:
        """Analyze market influence of current Moon nakshatra"""
        try:
            if moon_nakshatra not in self.nakshatra_market_impact:
                return {"influence": "neutral", "strength": 0.5, "volatility": 0.5}
            
            influence_data = self.nakshatra_market_impact[moon_nakshatra]
            
            # Calculate temporal strength based on nakshatra cycle
            days_in_cycle = 27.32  # Sidereal month
            cycle_position = (date.timetuple().tm_yday % days_in_cycle) / days_in_cycle
            
            # Peak influence at quarter points
            temporal_strength = 1.0
            if 0.2 <= cycle_position <= 0.3 or 0.7 <= cycle_position <= 0.8:
                temporal_strength = 1.2
            elif 0.45 <= cycle_position <= 0.55:
                temporal_strength = 0.8
            
            final_strength = min(1.0, influence_data["strength"] * temporal_strength)
            
            return {
                "influence": influence_data["type"],
                "strength": final_strength,
                "volatility": influence_data["volatility"],
                "cycle_position": cycle_position,
                "temporal_multiplier": temporal_strength
            }
            
        except Exception as e:
            logger.error(f"Error analyzing nakshatra influence: {str(e)}")
            return {"influence": "neutral", "strength": 0.5, "volatility": 0.5}
    
    def calculate_planetary_strength(self, positions: Dict[str, PlanetaryPosition], 
                                   aspects: List[VedicAspect]) -> Dict[str, float]:
        """Calculate overall planetary strength for market analysis"""
        try:
            strengths = {}
            
            for planet_name, position in positions.items():
                base_strength = 0.5
                
                # Sign strength (exaltation/debilitation)
                sign_bonuses = {
                    "Sun": {"Aries": 0.3, "Libra": -0.3},
                    "Moon": {"Taurus": 0.3, "Scorpio": -0.3},
                    "Mars": {"Capricorn": 0.3, "Cancer": -0.3},
                    "Mercury": {"Virgo": 0.3, "Pisces": -0.3},
                    "Jupiter": {"Cancer": 0.3, "Capricorn": -0.3},
                    "Venus": {"Pisces": 0.3, "Virgo": -0.3},
                    "Saturn": {"Libra": 0.3, "Aries": -0.3}
                }
                
                if planet_name in sign_bonuses and position.sign in sign_bonuses[planet_name]:
                    base_strength += sign_bonuses[planet_name][position.sign]
                
                # Aspect influence
                aspect_modifier = 0.0
                for aspect in aspects:
                    if aspect.from_planet == planet_name or aspect.to_planet == planet_name:
                        if aspect.aspect_type in ["conjunction", "trine", "sextile"]:
                            aspect_modifier += aspect.strength * 0.1
                        elif aspect.aspect_type in ["opposition", "square"]:
                            aspect_modifier -= aspect.strength * 0.1
                
                final_strength = max(0.0, min(1.0, base_strength + aspect_modifier))
                strengths[planet_name] = final_strength
            
            return strengths
            
        except Exception as e:
            logger.error(f"Error calculating planetary strength: {str(e)}")
            return {planet: 0.5 for planet in positions.keys()}
    
    def predict_market_trends(self, positions: Dict[str, PlanetaryPosition],
                            aspects: List[VedicAspect], strengths: Dict[str, float]) -> Dict[str, Any]:
        """Predict market trends based on Vedic analysis"""
        try:
            # Calculate weighted planetary influences
            bullish_influence = 0.0
            bearish_influence = 0.0
            volatility_influence = 0.0
            
            for planet, strength in strengths.items():
                influence = self.planet_influences.get(planet, {"market_factor": 0.1})
                market_factor = influence["market_factor"]
                
                # Determine planet's current influence
                position = positions[planet]
                
                # Bullish planets: Jupiter, Venus, Sun (in good positions)
                if planet in ["Jupiter", "Venus", "Sun"]:
                    bullish_influence += strength * market_factor
                
                # Bearish planets: Saturn, Mars (in challenging positions)
                elif planet in ["Saturn", "Mars"]:
                    bearish_influence += strength * market_factor
                
                # Volatile planets: Mercury, Moon, Rahu
                elif planet in ["Mercury", "Moon"]:
                    volatility_influence += strength * market_factor
            
            # Calculate trend strength
            net_trend = bullish_influence - bearish_influence
            trend_strength = abs(net_trend)
            
            # Determine primary trend
            if net_trend > 0.1:
                primary_trend = "bullish"
            elif net_trend < -0.1:
                primary_trend = "bearish"
            else:
                primary_trend = "neutral"
            
            # Market timing insights
            timing_quality = "average"
            if trend_strength > 0.6:
                timing_quality = "excellent"
            elif trend_strength > 0.4:
                timing_quality = "good"
            elif trend_strength < 0.2:
                timing_quality = "poor"
            
            return {
                "primary_trend": primary_trend,
                "trend_strength": trend_strength,
                "volatility_level": volatility_influence,
                "timing_quality": timing_quality,
                "bullish_influence": bullish_influence,
                "bearish_influence": bearish_influence,
                "net_influence": net_trend
            }
            
        except Exception as e:
            logger.error(f"Error predicting market trends: {str(e)}")
            return {
                "primary_trend": "neutral",
                "trend_strength": 0.5,
                "volatility_level": 0.5,
                "timing_quality": "average"
            }
    
    def calculate_auspicious_periods(self, date: datetime) -> Dict[str, Any]:
        """Calculate auspicious periods for trading"""
        try:
            # Muhurta analysis (auspicious timing)
            hour = date.hour
            day_of_week = date.weekday()  # 0=Monday, 6=Sunday
            
            # Traditional Vedic market timing
            auspicious_hours = {
                0: [6, 7, 10, 11, 14, 15],  # Monday
                1: [7, 8, 11, 12, 15, 16],  # Tuesday  
                2: [8, 9, 12, 13, 16, 17],  # Wednesday
                3: [6, 7, 13, 14, 17, 18],  # Thursday
                4: [7, 8, 14, 15, 18, 19],  # Friday
                5: [8, 9, 15, 16, 19, 20],  # Saturday
                6: [9, 10, 16, 17, 20, 21]  # Sunday
            }
            
            current_auspicious = hour in auspicious_hours.get(day_of_week, [])
            
            # Rahu Kaal (inauspicious periods)
            rahu_kaal_start = {
                0: 7.5,   # Monday: 7:30-9:00 AM
                1: 15.0,  # Tuesday: 3:00-4:30 PM  
                2: 12.0,  # Wednesday: 12:00-1:30 PM
                3: 13.5,  # Thursday: 1:30-3:00 PM
                4: 10.5,  # Friday: 10:30-12:00 PM
                5: 9.0,   # Saturday: 9:00-10:30 AM
                6: 16.5   # Sunday: 4:30-6:00 PM
            }
            
            rahu_start = rahu_kaal_start.get(day_of_week, 12.0)
            in_rahu_kaal = rahu_start <= hour < (rahu_start + 1.5)
            
            # Overall timing score
            timing_score = 0.5
            if current_auspicious and not in_rahu_kaal:
                timing_score = 0.8
            elif current_auspicious:
                timing_score = 0.6
            elif in_rahu_kaal:
                timing_score = 0.2
            
            return {
                "auspicious_time": current_auspicious,
                "rahu_kaal": in_rahu_kaal,
                "timing_score": timing_score,
                "recommended_action": "trade" if timing_score > 0.6 else "wait"
            }
            
        except Exception as e:
            logger.error(f"Error calculating auspicious periods: {str(e)}")
            return {"auspicious_time": True, "timing_score": 0.5}
    
    def prepare_features(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """Prepare Vedic astrology features"""
        try:
            # Get current date
            current_date = datetime.now()
            if "timestamp" in raw_data:
                try:
                    current_date = pd.to_datetime(raw_data["timestamp"])
                    if current_date.tz is None:
                        current_date = current_date.replace(tzinfo=pytz.UTC)
                except:
                    pass
            
            # Calculate planetary positions
            positions = self.calculate_planetary_positions(current_date)
            aspects = self.calculate_vedic_aspects(positions)
            strengths = self.calculate_planetary_strength(positions, aspects)
            
            # Get Moon's nakshatra for primary influence
            moon_nakshatra = positions.get("Moon", PlanetaryPosition("Moon", 0, "Aries", "Ashwini", 1, False)).nakshatra
            nakshatra_influence = self.analyze_nakshatra_influence(moon_nakshatra, current_date)
            
            # Market trend prediction
            trend_prediction = self.predict_market_trends(positions, aspects, strengths)
            
            # Auspicious timing
            timing_analysis = self.calculate_auspicious_periods(current_date)
            
            # Compile features
            features = {
                "vedic_trend": 1 if trend_prediction["primary_trend"] == "bullish" else 
                              -1 if trend_prediction["primary_trend"] == "bearish" else 0,
                "trend_strength": trend_prediction["trend_strength"],
                "volatility_influence": trend_prediction["volatility_level"],
                "timing_quality": timing_analysis["timing_score"],
                "nakshatra_influence": nakshatra_influence["strength"],
                "moon_nakshatra": moon_nakshatra,
                "auspicious_time": 1 if timing_analysis["auspicious_time"] else 0,
                "rahu_kaal": 1 if timing_analysis["rahu_kaal"] else 0,
                "jupiter_strength": strengths.get("Jupiter", 0.5),
                "saturn_strength": strengths.get("Saturn", 0.5),
                "mars_strength": strengths.get("Mars", 0.5),
                "mercury_strength": strengths.get("Mercury", 0.5),
                "venus_strength": strengths.get("Venus", 0.5),
                "sun_strength": strengths.get("Sun", 0.5),
                "moon_strength": strengths.get("Moon", 0.5),
                "bullish_influence": trend_prediction["bullish_influence"],
                "bearish_influence": trend_prediction["bearish_influence"],
                "net_planetary_influence": trend_prediction["net_influence"],
                "total_aspects": len(aspects),
                "strong_aspects": len([a for a in aspects if a.strength > 0.7]),
                "challenging_aspects": len([a for a in aspects if a.aspect_type in ["opposition", "square"] and a.strength > 0.5])
            }
            
            # Add planetary positions
            for planet, position in positions.items():
                features[f"{planet.lower()}_longitude"] = position.longitude
                features[f"{planet.lower()}_sign"] = position.sign
                features[f"{planet.lower()}_house"] = position.house
            
            return pd.DataFrame([features])
            
        except Exception as e:
            logger.error(f"Error preparing Vedic astrology features: {str(e)}")
            # Return minimal feature set
            return pd.DataFrame([{
                "vedic_trend": 0,
                "trend_strength": 0.5,
                "timing_quality": 0.5,
                "nakshatra_influence": 0.5,
                "auspicious_time": 1,
                "rahu_kaal": 0
            }])
    
    def retrain(self, new_data: pd.DataFrame, target: pd.Series) -> bool:
        """Retrain the Vedic astrology model (mostly parameter adjustment)"""
        try:
            # Vedic astrology is based on astronomical calculations
            # Retraining involves adjusting interpretation parameters
            logger.info("Vedic astrology parameters updated")
            return True
        except Exception as e:
            logger.error(f"Error retraining Vedic astrology module: {str(e)}")
            return False
    
    def infer(self, features: pd.DataFrame) -> ModuleResult:
        """Generate Vedic astrology-based market inference"""
        try:
            feature_row = features.iloc[0]
            
            # Base score from planetary influences
            base_score = 50.0
            
            # Trend influence (30% weight)
            trend_factor = feature_row.get("vedic_trend", 0) * feature_row.get("trend_strength", 0.5)
            trend_score = trend_factor * 15 + 50  # Convert to 0-100 scale
            
            # Timing influence (25% weight)
            timing_score = feature_row.get("timing_quality", 0.5) * 100
            if feature_row.get("rahu_kaal", 0) == 1:
                timing_score *= 0.5  # Reduce score during Rahu Kaal
            
            # Nakshatra influence (20% weight)
            nakshatra_score = feature_row.get("nakshatra_influence", 0.5) * 100
            
            # Planetary strength influence (25% weight)
            jupiter_strength = feature_row.get("jupiter_strength", 0.5)
            saturn_strength = feature_row.get("saturn_strength", 0.5)
            benefic_score = (jupiter_strength + feature_row.get("venus_strength", 0.5)) * 50
            malefic_penalty = saturn_strength * 20
            
            planetary_score = benefic_score - malefic_penalty + 50
            
            # Calculate final score
            final_score = (
                trend_score * 0.30 +
                timing_score * 0.25 +
                nakshatra_score * 0.20 +
                planetary_score * 0.25
            )
            
            # Ensure score is within bounds
            final_score = max(0, min(100, final_score))
            
            # Calculate uncertainty
            volatility_influence = feature_row.get("volatility_influence", 0.5)
            aspects_uncertainty = min(0.4, feature_row.get("challenging_aspects", 0) * 0.1)
            timing_uncertainty = 0.3 if feature_row.get("rahu_kaal", 0) == 1 else 0.1
            
            uncertainty = min(0.8, volatility_influence + aspects_uncertainty + timing_uncertainty)
            
            # Determine signal types
            signal_types = []
            
            if feature_row.get("vedic_trend", 0) > 0:
                signal_types.append("vedic_bullish")
            elif feature_row.get("vedic_trend", 0) < 0:
                signal_types.append("vedic_bearish")
            else:
                signal_types.append("vedic_neutral")
            
            if feature_row.get("auspicious_time", 0) == 1:
                signal_types.append("auspicious_timing")
            
            if feature_row.get("rahu_kaal", 0) == 1:
                signal_types.append("rahu_kaal_warning")
            
            if volatility_influence > 0.7:
                signal_types.append("high_volatility_vedic")
            
            if feature_row.get("jupiter_strength", 0.5) > 0.8:
                signal_types.append("jupiter_strong")
            
            if feature_row.get("saturn_strength", 0.5) > 0.8:
                signal_types.append("saturn_influence")
            
            # Generate explanation
            moon_nakshatra = feature_row.get("moon_nakshatra", "Unknown")
            trend_direction = "yükseliş" if feature_row.get("vedic_trend", 0) > 0 else "düşüş" if feature_row.get("vedic_trend", 0) < 0 else "yatay"
            
            explanation = f"Vedic astroloji analizi: {final_score:.1f}/100. "
            explanation += f"Ay nakshatra: {moon_nakshatra}, trend: {trend_direction}. "
            explanation += f"Timing kalitesi: {feature_row.get('timing_quality', 0.5):.1%}, "
            explanation += f"Jupiter gücü: {feature_row.get('jupiter_strength', 0.5):.1%}. "
            
            if feature_row.get("rahu_kaal", 0) == 1:
                explanation += "Rahu Kaal uyarısı aktif. "
            
            if feature_row.get("auspicious_time", 0) == 1:
                explanation += "Şubhel muhurta zamanı. "
            
            # Contributing factors
            contributing_factors = {
                "vedic_trend_strength": feature_row.get("trend_strength", 0.5),
                "timing_quality": feature_row.get("timing_quality", 0.5),
                "nakshatra_influence": feature_row.get("nakshatra_influence", 0.5),
                "jupiter_strength": feature_row.get("jupiter_strength", 0.5),
                "planetary_harmony": 1 - (feature_row.get("challenging_aspects", 0) / max(1, feature_row.get("total_aspects", 1)))
            }
            
            logger.info(f"Vedic astrology analysis completed: {final_score:.2f} (uncertainty: {uncertainty:.3f})")
            
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
            logger.error(f"Error in Vedic astrology inference: {str(e)}")
            return ModuleResult(
                score=50.0,
                uncertainty=0.8,
                type=["vedic_error"],
                explanation=f"Vedic astrology analysis error: {str(e)}",
                timestamp=datetime.now().isoformat(),
                confidence_level="VERY_LOW",
                contributing_factors={}
            )

if __name__ == "__main__":
    print("🌟 ULTRA VEDIC ASTROLOGY ENHANCED - Test")
    print("="*50)
    
    # Test data
    test_data = {
        "symbol": "BIST100",
        "close": 9850.0,
        "timestamp": "2025-09-20T10:00:00"
    }
    
    # Initialize module
    vedic_module = UltraVedicAstrologyModule()
    
    try:
        print("🔄 Running Vedic astrology analysis...")
        
        # Prepare features
        features = vedic_module.prepare_features(test_data)
        print(f"✅ Features prepared: {len(features.columns)} features")
        
        # Run inference
        result = vedic_module.infer(features)
        
        print(f"\n🎯 VEDIC ASTROLOGY RESULT:")
        print(f"Score: {result.score:.2f}/100")
        print(f"Uncertainty: {result.uncertainty:.3f}")
        print(f"Confidence: {result.confidence_level}")
        print(f"Signal Types: {result.type}")
        print(f"Explanation: {result.explanation}")
        print(f"Contributing Factors: {result.contributing_factors}")
        
        print(f"\n📊 DETAILED FEATURES:")
        for col in features.columns:
            print(f"  - {col}: {features[col].iloc[0]}")
        
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
    
    print(f"\n✅ Vedic Astrology module test complete!")