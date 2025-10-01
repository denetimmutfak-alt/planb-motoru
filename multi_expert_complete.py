#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MULTI-EXPERT ENGINE - COMPLETE INTEGRATION
Arkadaş fikirlerinin uygulanması - All 17 Enhanced Ultra Modules Integration
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import asyncio
import concurrent.futures
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Import all enhanced modules
from multi_expert_engine import ExpertModule, ModuleResult, ModuleRegistry
from ultra_risk_enhanced import UltraRiskModule
from ultra_volatility_enhanced import UltraVolatilityModule
from ultra_ml_enhanced import UltraMLModule
from ultra_currency_enhanced import UltraCurrencyModule
from ultra_commodities_enhanced import UltraCommoditiesModule
from ultra_bonds_enhanced import UltraBondsModule
from ultra_options_enhanced import UltraOptionsModule
from ultra_crypto_enhanced import UltraCryptoModule
from ultra_economic_indicators_enhanced import UltraEconomicIndicatorsModule
from ultra_news_enhanced import UltraNewsModule
from ultra_insider_trading_enhanced import UltraInsiderTradingModule
from ultra_sector_analysis_enhanced import UltraSectorAnalysisModule
from ultra_esg_enhanced import UltraESGModule
from ultra_geopolitical_enhanced import UltraGeopoliticalModule
from ultra_alternative_data_enhanced import UltraAlternativeDataModule
from ultra_international_enhanced import UltraInternationalModule
from ultra_credit_enhanced import UltraCreditModule
from ultra_vedic_astrology_enhanced import UltraVedicAstrologyModule
from ultra_shemitah_enhanced import UltraShemitahModule
from ultra_solar_cycle_enhanced import UltraSolarCycleModule
from ultra_cycle_analysis_enhanced import UltraCycleAnalysisModule
from ultra_gann_enhanced import UltraGannModule
from ultra_moon_phases_enhanced import UltraMoonPhasesModule
from ultra_financial_astrology_enhanced import UltraFinancialAstrologyModule
from ultra_fibonacci_elliott_enhanced import UltraFibonacciElliottModule

logger = logging.getLogger(__name__)

@dataclass
class EnsembleResult:
    """Multi-Expert Engine ensemble result"""
    final_score: float
    weighted_uncertainty: float
    confidence_level: str
    consensus_strength: float
    module_contributions: Dict[str, float]
    signal_distribution: Dict[str, int]
    risk_factors: Dict[str, float]
    opportunity_factors: Dict[str, float]
    explanation: str
    timestamp: str
    individual_results: Dict[str, ModuleResult]

@dataclass
class MarketRegime:
    """Current market regime analysis"""
    regime_type: str  # bull, bear, sideways, crisis, recovery
    volatility_regime: str  # low, normal, high, extreme
    risk_sentiment: str  # risk_on, risk_off, neutral, transition
    confidence: float
    regime_strength: float
    duration_estimate: str  # short, medium, long

class MultiExpertEngine:
    """
    Complete Multi-Expert Engine
    Arkadaş önerisi: Integration of all 17 enhanced ultra modules for comprehensive financial analysis
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the complete Multi-Expert Engine"""
        self.config = config or {}
        self.module_registry = ModuleRegistry()
        self.modules = {}
        
        # Ensemble configuration
        self.ensemble_config = {
            "voting_method": "weighted_average",  # weighted_average, median, trimmed_mean
            "uncertainty_weighting": True,
            "confidence_threshold": 0.6,
            "consensus_threshold": 0.7,
            "outlier_detection": True,
            "adaptive_weights": True,
            "regime_adjustment": True
        }
        
        # Module weights (normalized for 25 modules, total = 1.0)
        self.module_weights = {
            "Ultra Risk": 0.070,
            "Ultra Volatility": 0.050,
            "Ultra ML": 0.075,
            "Ultra Currency": 0.035,
            "Ultra Commodities": 0.025,
            "Ultra Bonds": 0.035,
            "Ultra Options": 0.025,
            "Ultra Crypto": 0.020,
            "Ultra Economic Indicators": 0.060,
            "Ultra News": 0.050,
            "Ultra Insider Trading": 0.035,
            "Ultra Sector Analysis": 0.070,
            "Ultra ESG": 0.025,
            "Ultra Geopolitical": 0.035,
            "Ultra Alternative Data": 0.040,
            "Ultra International": 0.040,
            "Ultra Credit": 0.060,
            "Ultra Vedic Astrology": 0.035,
            "Ultra Shemitah": 0.025,
            "Ultra Solar Cycle": 0.025,
            "Ultra Cycle Analysis": 0.040,
            "Ultra Gann Enhanced": 0.035,
            "Ultra Moon Phases Enhanced": 0.025,
            "Ultra Financial Astrology Enhanced": 0.025,
            "Ultra Fibonacci Elliott Enhanced": 0.040
        }
        
        # Risk factor categories for comprehensive analysis
        self.risk_categories = {
            "market_risk": ["Ultra Risk", "Ultra Volatility", "Ultra Economic Indicators"],
            "credit_risk": ["Ultra Credit", "Ultra Bonds"],
            "operational_risk": ["Ultra News", "Ultra ESG", "Ultra Geopolitical"],
            "liquidity_risk": ["Ultra Currency", "Ultra International"],
            "systematic_risk": ["Ultra Sector Analysis", "Ultra ML"],
            "alternative_risk": ["Ultra Alternative Data", "Ultra Insider Trading"],
            "derivatives_risk": ["Ultra Options", "Ultra Crypto"],
            "commodity_risk": ["Ultra Commodities"],
            "cycle_risk": ["Ultra Vedic Astrology", "Ultra Shemitah", "Ultra Solar Cycle", "Ultra Cycle Analysis"],
            "technical_risk": ["Ultra Gann Enhanced", "Ultra Fibonacci Elliott Enhanced"],
            "astro_risk": ["Ultra Moon Phases Enhanced", "Ultra Financial Astrology Enhanced"]
        }
        
        # Opportunity factor categories
        self.opportunity_categories = {
            "growth_opportunities": ["Ultra ML", "Ultra Sector Analysis", "Ultra ESG"],
            "value_opportunities": ["Ultra Risk", "Ultra Credit", "Ultra International"],
            "momentum_opportunities": ["Ultra News", "Ultra Insider Trading", "Ultra Alternative Data"],
            "arbitrage_opportunities": ["Ultra Currency", "Ultra Options", "Ultra Commodities"],
            "macro_opportunities": ["Ultra Economic Indicators", "Ultra Geopolitical", "Ultra Bonds"],
            "innovation_opportunities": ["Ultra Crypto", "Ultra ESG"],
            "volatility_opportunities": ["Ultra Volatility", "Ultra Options"],
            "cycle_opportunities": ["Ultra Vedic Astrology", "Ultra Shemitah", "Ultra Solar Cycle", "Ultra Cycle Analysis"],
            "technical_opportunities": ["Ultra Gann Enhanced", "Ultra Fibonacci Elliott Enhanced"],
            "astro_opportunities": ["Ultra Moon Phases Enhanced", "Ultra Financial Astrology Enhanced"]
        }
        
        self.initialize_modules()
        logger.info("Multi-Expert Engine fully initialized with 25 enhanced modules")
    
    def initialize_modules(self):
        """Initialize all enhanced modules"""
        try:
            # Initialize all 25 enhanced modules
            modules_to_init = [
                ("Ultra Risk", UltraRiskModule),
                ("Ultra Volatility", UltraVolatilityModule),
                ("Ultra ML", UltraMLModule),
                ("Ultra Currency", UltraCurrencyModule),
                ("Ultra Commodities", UltraCommoditiesModule),
                ("Ultra Bonds", UltraBondsModule),
                ("Ultra Options", UltraOptionsModule),
                ("Ultra Crypto", UltraCryptoModule),
                ("Ultra Economic Indicators", UltraEconomicIndicatorsModule),
                ("Ultra News", UltraNewsModule),
                ("Ultra Insider Trading", UltraInsiderTradingModule),
                ("Ultra Sector Analysis", UltraSectorAnalysisModule),
                ("Ultra ESG", UltraESGModule),
                ("Ultra Geopolitical", UltraGeopoliticalModule),
                ("Ultra Alternative Data", UltraAlternativeDataModule),
                ("Ultra International", UltraInternationalModule),
                ("Ultra Credit", UltraCreditModule),
                ("Ultra Vedic Astrology", UltraVedicAstrologyModule),
                ("Ultra Shemitah", UltraShemitahModule),
                ("Ultra Solar Cycle", UltraSolarCycleModule),
                ("Ultra Cycle Analysis", UltraCycleAnalysisModule),
                ("Ultra Gann Enhanced", UltraGannModule),
                ("Ultra Moon Phases Enhanced", UltraMoonPhasesModule),
                ("Ultra Financial Astrology Enhanced", UltraFinancialAstrologyModule),
                ("Ultra Fibonacci Elliott Enhanced", UltraFibonacciElliottModule)
            ]
            
            for name, module_class in modules_to_init:
                try:
                    module = module_class()
                    self.modules[name] = module
                    self.module_registry.register_module(module)
                    logger.info(f"Successfully initialized {name}")
                except Exception as e:
                    logger.error(f"Failed to initialize {name}: {str(e)}")
                    # Continue with other modules
            
            logger.info(f"Initialized {len(self.modules)} out of {len(modules_to_init)} modules")
            
        except Exception as e:
            logger.error(f"Error initializing modules: {str(e)}")
    
    def analyze_market_regime(self, market_data: Dict[str, Any]) -> MarketRegime:
        """Analyze current market regime using multiple indicators"""
        try:
            # Get regime indicators from various modules
            regime_indicators = {}
            
            # Volatility regime
            if "Ultra Volatility" in self.modules:
                vol_data = self.modules["Ultra Volatility"].prepare_features(market_data)
                vol_regime = vol_data.iloc[0].get("volatility_regime", "normal")
                regime_indicators["volatility"] = vol_regime
            
            # Risk sentiment from multiple modules
            risk_indicators = []
            if "Ultra Risk" in self.modules:
                risk_indicators.append("risk_assessment")
            if "Ultra Economic Indicators" in self.modules:
                risk_indicators.append("macro_environment")
            if "Ultra Geopolitical" in self.modules:
                risk_indicators.append("geopolitical_climate")
            
            # Determine regime type
            regime_type = "sideways"  # Default
            volatility_regime = regime_indicators.get("volatility", "normal")
            
            # Simple regime classification
            if volatility_regime == "high":
                regime_type = "crisis" if len(risk_indicators) > 2 else "bear"
            elif volatility_regime == "low":
                regime_type = "bull" if len(risk_indicators) < 2 else "recovery"
            
            # Risk sentiment
            risk_sentiment = "neutral"
            if regime_type in ["bull", "recovery"]:
                risk_sentiment = "risk_on"
            elif regime_type in ["bear", "crisis"]:
                risk_sentiment = "risk_off"
            
            return MarketRegime(
                regime_type=regime_type,
                volatility_regime=volatility_regime,
                risk_sentiment=risk_sentiment,
                confidence=0.7,
                regime_strength=0.6,
                duration_estimate="medium"
            )
            
        except Exception as e:
            logger.error(f"Error analyzing market regime: {str(e)}")
            return MarketRegime("sideways", "normal", "neutral", 0.5, 0.5, "medium")
    
    def calculate_adaptive_weights(self, individual_results: Dict[str, ModuleResult],
                                 market_regime: MarketRegime) -> Dict[str, float]:
        """Calculate adaptive weights based on module performance and market regime"""
        try:
            adaptive_weights = self.module_weights.copy()
            
            # Adjust weights based on market regime
            if market_regime.regime_type == "crisis":
                # Increase weight on risk and credit modules
                adaptive_weights["Ultra Risk"] *= 1.5
                adaptive_weights["Ultra Credit"] *= 1.4
                adaptive_weights["Ultra Volatility"] *= 1.3
                adaptive_weights["Ultra Geopolitical"] *= 1.2
                # Decrease weight on growth-oriented modules
                adaptive_weights["Ultra ML"] *= 0.8
                adaptive_weights["Ultra ESG"] *= 0.7
            
            elif market_regime.regime_type == "bull":
                # Increase weight on growth and momentum modules
                adaptive_weights["Ultra ML"] *= 1.4
                adaptive_weights["Ultra Sector Analysis"] *= 1.3
                adaptive_weights["Ultra News"] *= 1.2
                adaptive_weights["Ultra Alternative Data"] *= 1.2
                # Decrease weight on defensive modules
                adaptive_weights["Ultra Risk"] *= 0.8
                adaptive_weights["Ultra Credit"] *= 0.9
            
            elif market_regime.volatility_regime == "high":
                # Increase weight on volatility and options modules
                adaptive_weights["Ultra Volatility"] *= 1.4
                adaptive_weights["Ultra Options"] *= 1.3
                adaptive_weights["Ultra Currency"] *= 1.2
            
            # Adjust based on individual module confidence
            for module_name, result in individual_results.items():
                if module_name in adaptive_weights:
                    confidence_multiplier = 0.5 + result.uncertainty  # Higher uncertainty = lower weight
                    adaptive_weights[module_name] *= confidence_multiplier
            
            # Normalize weights
            total_weight = sum(adaptive_weights.values())
            if total_weight > 0:
                adaptive_weights = {k: v/total_weight for k, v in adaptive_weights.items()}
            
            return adaptive_weights
            
        except Exception as e:
            logger.error(f"Error calculating adaptive weights: {str(e)}")
            return self.module_weights
    
    def detect_outliers(self, scores: List[float], threshold: float = 2.0) -> List[bool]:
        """Detect outlier scores using statistical methods"""
        try:
            if len(scores) < 3:
                return [False] * len(scores)
            
            scores_array = np.array(scores)
            median_score = np.median(scores_array)
            mad = np.median(np.abs(scores_array - median_score))
            
            if mad == 0:
                return [False] * len(scores)
            
            modified_z_scores = 0.6745 * (scores_array - median_score) / mad
            outliers = np.abs(modified_z_scores) > threshold
            
            return outliers.tolist()
            
        except Exception as e:
            logger.error(f"Error detecting outliers: {str(e)}")
            return [False] * len(scores)
    
    def calculate_consensus_strength(self, scores: List[float], weights: List[float]) -> float:
        """Calculate consensus strength among modules"""
        try:
            if len(scores) < 2:
                return 0.5
            
            weighted_mean = np.average(scores, weights=weights)
            weighted_variance = np.average((scores - weighted_mean)**2, weights=weights)
            weighted_std = np.sqrt(weighted_variance)
            
            # Consensus strength inversely related to standard deviation
            # High consensus = low standard deviation
            max_possible_std = 50.0  # Assuming scores are 0-100
            consensus_strength = max(0.0, 1.0 - (weighted_std / max_possible_std))
            
            return consensus_strength
            
        except Exception as e:
            logger.error(f"Error calculating consensus strength: {str(e)}")
            return 0.5
    
    def aggregate_risk_factors(self, individual_results: Dict[str, ModuleResult]) -> Dict[str, float]:
        """Aggregate risk factors from all modules"""
        try:
            risk_factors = {}
            
            for category, module_names in self.risk_categories.items():
                category_risks = []
                for module_name in module_names:
                    if module_name in individual_results:
                        result = individual_results[module_name]
                        # Convert score to risk (inverse relationship)
                        risk_level = (100 - result.score) / 100
                        # Weight by uncertainty (more uncertain = higher risk)
                        weighted_risk = risk_level * (1 + result.uncertainty)
                        category_risks.append(weighted_risk)
                
                if category_risks:
                    risk_factors[category] = min(1.0, np.mean(category_risks))
                else:
                    risk_factors[category] = 0.5  # Default moderate risk
            
            return risk_factors
            
        except Exception as e:
            logger.error(f"Error aggregating risk factors: {str(e)}")
            return {category: 0.5 for category in self.risk_categories.keys()}
    
    def aggregate_opportunity_factors(self, individual_results: Dict[str, ModuleResult]) -> Dict[str, float]:
        """Aggregate opportunity factors from all modules"""
        try:
            opportunity_factors = {}
            
            for category, module_names in self.opportunity_categories.items():
                category_opportunities = []
                for module_name in module_names:
                    if module_name in individual_results:
                        result = individual_results[module_name]
                        # Convert score to opportunity (direct relationship)
                        opportunity_level = result.score / 100
                        # Weight by confidence (more confident = higher opportunity)
                        weighted_opportunity = opportunity_level * (1 - result.uncertainty)
                        category_opportunities.append(weighted_opportunity)
                
                if category_opportunities:
                    opportunity_factors[category] = min(1.0, np.mean(category_opportunities))
                else:
                    opportunity_factors[category] = 0.5  # Default moderate opportunity
            
            return opportunity_factors
            
        except Exception as e:
            logger.error(f"Error aggregating opportunity factors: {str(e)}")
            return {category: 0.5 for category in self.opportunity_categories.keys()}
    
    async def run_module_async(self, module_name: str, module: ExpertModule, 
                              raw_data: Dict[str, Any]) -> Tuple[str, ModuleResult]:
        """Run a single module asynchronously"""
        try:
            features = module.prepare_features(raw_data)
            result = module.infer(features)
            
            # Handle both ModuleResult and tuple (score, uncertainty) returns
            if isinstance(result, tuple):
                score, uncertainty = result
                module_result = ModuleResult(
                    score=score,
                    uncertainty=uncertainty,
                    type=["prediction"],
                    explanation=f"{module_name} analysis",
                    timestamp=datetime.now().isoformat(),
                    confidence_level="",  # Will be auto-calculated
                    contributing_factors={}
                )
                return module_name, module_result
            else:
                return module_name, result
        except Exception as e:
            logger.error(f"Error running {module_name}: {str(e)}")
            fallback_result = ModuleResult(
                score=50.0,
                uncertainty=0.8,
                type=["error"],
                explanation=f"Module error: {str(e)}",
                timestamp=datetime.now().isoformat(),
                confidence_level="VERY_LOW",
                contributing_factors={}
            )
            return module_name, fallback_result
    
    async def analyze_async(self, raw_data: Dict[str, Any]) -> EnsembleResult:
        """Run complete multi-expert analysis asynchronously"""
        try:
            # Analyze market regime first
            market_regime = self.analyze_market_regime(raw_data)
            
            # Run all modules concurrently
            tasks = []
            for module_name, module in self.modules.items():
                task = self.run_module_async(module_name, module, raw_data)
                tasks.append(task)
            
            # Wait for all modules to complete
            results = await asyncio.gather(*tasks)
            individual_results = dict(results)
            
            # Calculate adaptive weights
            adaptive_weights = self.calculate_adaptive_weights(individual_results, market_regime)
            
            # Extract scores and weights for ensemble
            scores = []
            weights = []
            module_contributions = {}
            
            for module_name, result in individual_results.items():
                if module_name in adaptive_weights:
                    scores.append(result.score)
                    weights.append(adaptive_weights[module_name])
                    module_contributions[module_name] = result.score * adaptive_weights[module_name]
            
            # Detect outliers
            if self.ensemble_config["outlier_detection"]:
                outliers = self.detect_outliers(scores)
                # Remove outliers
                filtered_scores = [s for i, s in enumerate(scores) if not outliers[i]]
                filtered_weights = [w for i, w in enumerate(weights) if not outliers[i]]
                if len(filtered_scores) > 0:
                    scores = filtered_scores
                    weights = filtered_weights
            
            # Calculate ensemble score
            if self.ensemble_config["voting_method"] == "weighted_average":
                final_score = np.average(scores, weights=weights)
            elif self.ensemble_config["voting_method"] == "median":
                final_score = np.median(scores)
            elif self.ensemble_config["voting_method"] == "trimmed_mean":
                # Remove top and bottom 10%
                sorted_scores = sorted(scores)
                trim_count = max(1, len(sorted_scores) // 10)
                trimmed_scores = sorted_scores[trim_count:-trim_count] if len(sorted_scores) > 2*trim_count else sorted_scores
                final_score = np.mean(trimmed_scores)
            else:
                final_score = np.mean(scores)
            
            # Calculate weighted uncertainty
            uncertainties = [result.uncertainty for result in individual_results.values()]
            if weights:
                weighted_uncertainty = np.average(uncertainties[:len(weights)], weights=weights)
            else:
                weighted_uncertainty = np.mean(uncertainties)
            
            # Calculate consensus strength
            consensus_strength = self.calculate_consensus_strength(scores, weights)
            
            # Determine confidence level
            if weighted_uncertainty < 0.3 and consensus_strength > 0.7:
                confidence_level = "VERY_HIGH"
            elif weighted_uncertainty < 0.5 and consensus_strength > 0.6:
                confidence_level = "HIGH"
            elif weighted_uncertainty < 0.7 and consensus_strength > 0.4:
                confidence_level = "MEDIUM"
            elif weighted_uncertainty < 0.8:
                confidence_level = "LOW"
            else:
                confidence_level = "VERY_LOW"
            
            # Aggregate signal distribution
            signal_distribution = defaultdict(int)
            for result in individual_results.values():
                for signal_type in result.type:
                    signal_distribution[signal_type] += 1
            
            # Aggregate risk and opportunity factors
            risk_factors = self.aggregate_risk_factors(individual_results)
            opportunity_factors = self.aggregate_opportunity_factors(individual_results)
            
            # Generate comprehensive explanation
            explanation = self.generate_explanation(
                final_score, consensus_strength, market_regime, 
                risk_factors, opportunity_factors, signal_distribution
            )
            
            return EnsembleResult(
                final_score=final_score,
                weighted_uncertainty=weighted_uncertainty,
                confidence_level=confidence_level,
                consensus_strength=consensus_strength,
                module_contributions=module_contributions,
                signal_distribution=dict(signal_distribution),
                risk_factors=risk_factors,
                opportunity_factors=opportunity_factors,
                explanation=explanation,
                timestamp=datetime.now().isoformat(),
                individual_results=individual_results
            )
            
        except Exception as e:
            logger.error(f"Error in async analysis: {str(e)}")
            # Return fallback result
            return EnsembleResult(
                final_score=50.0,
                weighted_uncertainty=0.8,
                confidence_level="VERY_LOW",
                consensus_strength=0.2,
                module_contributions={},
                signal_distribution={},
                risk_factors={},
                opportunity_factors={},
                explanation=f"Analysis error: {str(e)}",
                timestamp=datetime.now().isoformat(),
                individual_results={}
            )
    
    def analyze(self, raw_data: Dict[str, Any]) -> EnsembleResult:
        """Run complete multi-expert analysis (synchronous wrapper)"""
        try:
            # Run async analysis
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.analyze_async(raw_data))
            loop.close()
            return result
        except Exception as e:
            logger.error(f"Error in synchronous analysis wrapper: {str(e)}")
            return EnsembleResult(
                final_score=50.0,
                weighted_uncertainty=0.8,
                confidence_level="VERY_LOW",
                consensus_strength=0.2,
                module_contributions={},
                signal_distribution={},
                risk_factors={},
                opportunity_factors={},
                explanation=f"Wrapper error: {str(e)}",
                timestamp=datetime.now().isoformat(),
                individual_results={}
            )
    
    def generate_explanation(self, final_score: float, consensus_strength: float,
                           market_regime: MarketRegime, risk_factors: Dict[str, float],
                           opportunity_factors: Dict[str, float], 
                           signal_distribution: Dict[str, int]) -> str:
        """Generate comprehensive explanation of the analysis"""
        try:
            explanation = f"Multi-Expert analizi: {final_score:.1f}/100 "
            explanation += f"(konsensüs: {consensus_strength:.1%}). "
            
            # Market regime
            explanation += f"Piyasa rejimi: {market_regime.regime_type} "
            explanation += f"({market_regime.risk_sentiment}). "
            
            # Top risk factors
            top_risks = sorted(risk_factors.items(), key=lambda x: x[1], reverse=True)[:2]
            if top_risks:
                explanation += f"Ana riskler: {', '.join([risk.replace('_', ' ') for risk, _ in top_risks])}. "
            
            # Top opportunities
            top_opportunities = sorted(opportunity_factors.items(), key=lambda x: x[1], reverse=True)[:2]
            if top_opportunities:
                explanation += f"Fırsatlar: {', '.join([opp.replace('_', ' ') for opp, _ in top_opportunities])}. "
            
            # Signal summary
            if signal_distribution:
                total_signals = sum(signal_distribution.values())
                top_signals = sorted(signal_distribution.items(), key=lambda x: x[1], reverse=True)[:3]
                signal_summary = ", ".join([f"{signal}({count})" for signal, count in top_signals])
                explanation += f"Toplam {total_signals} sinyal: {signal_summary}."
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return f"Multi-Expert analizi: {final_score:.1f}/100"
    
    def get_module_status(self) -> Dict[str, Any]:
        """Get status of all modules"""
        status = {
            "total_modules": len(self.modules),
            "active_modules": len([m for m in self.modules.values() if m is not None]),
            "module_list": list(self.modules.keys()),
            "engine_config": self.ensemble_config,
            "last_updated": datetime.now().isoformat()
        }
        return status

# Global instance for easy access
multi_expert_engine = None

def get_multi_expert_engine() -> MultiExpertEngine:
    """Get or create global Multi-Expert Engine instance"""
    global multi_expert_engine
    if multi_expert_engine is None:
        multi_expert_engine = MultiExpertEngine()
    return multi_expert_engine

if __name__ == "__main__":
    print(f"🚀 MULTI-EXPERT ENGINE - COMPLETE INTEGRATION WITH CYCLE ANALYSIS")
    print("="*70)
    
    # Test data
    test_data = {
        "symbol": "BIST100", 
        "close": 9850.0,
        "volume": 125000000,
        "timestamp": "2025-09-20T10:00:00"
    }
    
    # Initialize Multi-Expert Engine
    engine = MultiExpertEngine()
    
    print(f"✅ Multi-Expert Engine initialized")
    print(f"📊 Active modules: {len(engine.modules)}")
    print(f"🎯 Module list: {list(engine.modules.keys())}")
    
    # Run comprehensive analysis
    try:
        print(f"\n🔄 Running comprehensive multi-expert analysis...")
        start_time = datetime.now()
        
        result = engine.analyze(test_data)
        
        end_time = datetime.now()
        analysis_time = (end_time - start_time).total_seconds()
        
        print(f"\n🎯 MULTI-EXPERT ANALYSIS COMPLETE!")
        print(f"Analysis Time: {analysis_time:.2f} seconds")
        print(f"="*50)
        
        print(f"\n📊 ENSEMBLE RESULT:")
        print(f"Final Score: {result.final_score:.2f}/100")
        print(f"Uncertainty: {result.weighted_uncertainty:.3f}")
        print(f"Confidence: {result.confidence_level}")
        print(f"Consensus Strength: {result.consensus_strength:.1%}")
        print(f"Explanation: {result.explanation}")
        
        print(f"\n🏆 MODULE CONTRIBUTIONS:")
        for module, contribution in sorted(result.module_contributions.items(), 
                                         key=lambda x: x[1], reverse=True)[:10]:
            print(f"  - {module}: {contribution:.1f}")
        
        print(f"\n📡 SIGNAL DISTRIBUTION:")
        for signal, count in sorted(result.signal_distribution.items(), 
                                  key=lambda x: x[1], reverse=True)[:10]:
            print(f"  - {signal}: {count}")
        
        print(f"\n⚠️ RISK FACTORS:")
        for risk_category, risk_level in sorted(result.risk_factors.items(), 
                                               key=lambda x: x[1], reverse=True):
            print(f"  - {risk_category.replace('_', ' ').title()}: {risk_level:.1%}")
        
        print(f"\n🎯 OPPORTUNITY FACTORS:")
        for opp_category, opp_level in sorted(result.opportunity_factors.items(), 
                                            key=lambda x: x[1], reverse=True):
            print(f"  - {opp_category.replace('_', ' ').title()}: {opp_level:.1%}")
        
        print(f"\n📈 INDIVIDUAL MODULE RESULTS:")
        for module_name, module_result in result.individual_results.items():
            print(f"  - {module_name}: {module_result.score:.1f} (±{module_result.uncertainty:.2f})")
        
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
    
    print(f"\n🎉 Multi-Expert Engine integration complete!")