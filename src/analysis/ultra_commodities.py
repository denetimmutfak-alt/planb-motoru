"""
Ultra Commodities Analysis Module
Ultra Emtia Analizi Modülü

Bu modül gelişmiş emtia fiyat analizi, supply-demand dinamikleri
ve makroekonomik faktörlerin modellenmesini sağlar.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

print("INFO: Ultra Commodities Analysis modülü aktif")

class CommodityType(Enum):
    """Emtia türleri"""
    ENERGY = "energy"           # Petrol, Doğalgaz, Kömür
    PRECIOUS_METALS = "precious" # Altın, Gümüş, Platin
    BASE_METALS = "base"        # Bakır, Demir, Çinko
    AGRICULTURE = "agriculture"  # Buğday, Mısır, Soya
    LIVESTOCK = "livestock"     # Sığır, Domuz
    SOFT_COMMODITIES = "soft"   # Kahve, Şeker, Kakao

@dataclass
class CommodityProfile:
    """Emtia profili"""
    symbol: str
    name: str
    commodity_type: CommodityType
    unit: str
    exchange: str
    is_storable: bool
    seasonality_factor: float
    supply_elasticity: float
    demand_elasticity: float
    geopolitical_sensitivity: float

@dataclass 
class SupplyDemandAnalysis:
    """Supply-Demand analizi"""
    global_supply: float
    global_demand: float
    supply_growth_rate: float
    demand_growth_rate: float
    inventory_levels: float
    inventory_to_usage_ratio: float
    supply_disruption_risk: float
    demand_shock_probability: float
    balance_score: float

@dataclass
class MacroFactors:
    """Makroekonomik faktörler"""
    global_gdp_growth: float
    industrial_production_index: float
    dollar_strength_index: float
    inflation_expectations: float
    interest_rate_environment: float
    china_pmi: float
    us_economic_strength: float
    geopolitical_risk_score: float

@dataclass
class CommodityAnalysisResult:
    """Emtia analizi sonucu"""
    ultra_commodity_score: float
    commodity_profile: CommodityProfile
    supply_demand: SupplyDemandAnalysis
    macro_factors: MacroFactors
    price_forecast: Dict[str, float]
    volatility_analysis: Dict[str, Any]
    trading_recommendation: str
    risk_assessment: Dict[str, str]
    seasonal_patterns: Dict[str, Any]
    technical_signals: Dict[str, float]
    fundamental_signals: Dict[str, Any]

class UltraCommoditiesAnalyzer:
    """Ultra gelişmiş emtia analizi"""
    
    def __init__(self):
        """Ultra Commodities Analyzer başlat"""
        self.commodity_profiles = self._initialize_commodity_profiles()
        self.macro_weights = self._get_macro_weights()
        print("INFO: Ultra Commodities Analyzer gelişmiş emtia modelleri ile başlatıldı")
    
    def _initialize_commodity_profiles(self) -> Dict[str, CommodityProfile]:
        """Emtia profillerini başlat"""
        profiles = {}
        
        # Energy Commodities
        profiles['CRUDE_OIL'] = CommodityProfile(
            symbol='CL=F', name='Crude Oil WTI', commodity_type=CommodityType.ENERGY,
            unit='barrel', exchange='NYMEX', is_storable=True, seasonality_factor=0.3,
            supply_elasticity=0.2, demand_elasticity=-0.4, geopolitical_sensitivity=0.9
        )
        
        profiles['NATURAL_GAS'] = CommodityProfile(
            symbol='NG=F', name='Natural Gas', commodity_type=CommodityType.ENERGY,
            unit='MMBtu', exchange='NYMEX', is_storable=True, seasonality_factor=0.8,
            supply_elasticity=0.3, demand_elasticity=-0.6, geopolitical_sensitivity=0.7
        )
        
        # Precious Metals
        profiles['GOLD'] = CommodityProfile(
            symbol='GC=F', name='Gold', commodity_type=CommodityType.PRECIOUS_METALS,
            unit='oz', exchange='COMEX', is_storable=True, seasonality_factor=0.2,
            supply_elasticity=0.1, demand_elasticity=-0.3, geopolitical_sensitivity=0.8
        )
        
        profiles['SILVER'] = CommodityProfile(
            symbol='SI=F', name='Silver', commodity_type=CommodityType.PRECIOUS_METALS,
            unit='oz', exchange='COMEX', is_storable=True, seasonality_factor=0.2,
            supply_elasticity=0.2, demand_elasticity=-0.5, geopolitical_sensitivity=0.6
        )
        
        # Base Metals
        profiles['COPPER'] = CommodityProfile(
            symbol='HG=F', name='Copper', commodity_type=CommodityType.BASE_METALS,
            unit='lb', exchange='COMEX', is_storable=True, seasonality_factor=0.4,
            supply_elasticity=0.3, demand_elasticity=-0.7, geopolitical_sensitivity=0.5
        )
        
        # Agriculture
        profiles['WHEAT'] = CommodityProfile(
            symbol='ZW=F', name='Wheat', commodity_type=CommodityType.AGRICULTURE,
            unit='bushel', exchange='CBOT', is_storable=True, seasonality_factor=0.9,
            supply_elasticity=0.4, demand_elasticity=-0.4, geopolitical_sensitivity=0.6
        )
        
        profiles['CORN'] = CommodityProfile(
            symbol='ZC=F', name='Corn', commodity_type=CommodityType.AGRICULTURE,
            unit='bushel', exchange='CBOT', is_storable=True, seasonality_factor=0.8,
            supply_elasticity=0.5, demand_elasticity=-0.5, geopolitical_sensitivity=0.4
        )
        
        return profiles
    
    def _get_macro_weights(self) -> Dict[str, Dict[str, float]]:
        """Emtia türlerine göre makro ağırlıkları"""
        return {
            CommodityType.ENERGY.value: {
                'global_gdp': 0.3, 'dollar_strength': 0.25, 'geopolitical': 0.3, 'inflation': 0.15
            },
            CommodityType.PRECIOUS_METALS.value: {
                'global_gdp': 0.2, 'dollar_strength': 0.4, 'geopolitical': 0.25, 'inflation': 0.15
            },
            CommodityType.BASE_METALS.value: {
                'global_gdp': 0.4, 'dollar_strength': 0.3, 'geopolitical': 0.15, 'inflation': 0.15
            },
            CommodityType.AGRICULTURE.value: {
                'global_gdp': 0.25, 'dollar_strength': 0.2, 'geopolitical': 0.3, 'inflation': 0.25
            }
        }
    
    def analyze_commodity(self, symbol: str, current_price: float = None,
                         historical_data: Optional[pd.DataFrame] = None, **kwargs) -> CommodityAnalysisResult:
        """Kapsamlı emtia analizi"""
        try:
            # Commodity profile al
            commodity_profile = self._get_commodity_profile(symbol)
            
            # Supply-Demand analizi
            supply_demand = self._analyze_supply_demand(commodity_profile, historical_data)
            
            # Makroekonomik faktörler
            macro_factors = self._analyze_macro_factors(commodity_profile)
            
            # Fiyat tahmini
            price_forecast = self._forecast_prices(commodity_profile, supply_demand, macro_factors, current_price)
            
            # Volatilite analizi
            volatility_analysis = self._analyze_volatility(commodity_profile, historical_data)
            
            # Seasonal patterns
            seasonal_patterns = self._analyze_seasonality(commodity_profile, historical_data)
            
            # Technical signals
            technical_signals = self._generate_technical_signals(historical_data)
            
            # Fundamental signals  
            fundamental_signals = self._generate_fundamental_signals(supply_demand, macro_factors)
            
            # Ultra commodity score hesapla
            ultra_score = self._calculate_ultra_commodity_score(
                supply_demand, macro_factors, volatility_analysis, seasonal_patterns
            )
            
            # Trading recommendation
            trading_recommendation = self._generate_trading_recommendation(
                ultra_score, price_forecast, volatility_analysis, commodity_profile
            )
            
            # Risk assessment
            risk_assessment = self._assess_risks(commodity_profile, supply_demand, macro_factors)
            
            return CommodityAnalysisResult(
                ultra_commodity_score=ultra_score,
                commodity_profile=commodity_profile,
                supply_demand=supply_demand,
                macro_factors=macro_factors,
                price_forecast=price_forecast,
                volatility_analysis=volatility_analysis,
                trading_recommendation=trading_recommendation,
                risk_assessment=risk_assessment,
                seasonal_patterns=seasonal_patterns,
                technical_signals=technical_signals,
                fundamental_signals=fundamental_signals
            )
            
        except Exception as e:
            print(f"ERROR: Commodity analizi hatası: {str(e)}")
            return self._get_default_commodity_result(symbol, current_price)
    
    def _get_commodity_profile(self, symbol: str) -> CommodityProfile:
        """Emtia profilini al"""
        # Symbol mapping
        symbol_mapping = {
            'GOLD': 'GOLD', 'XAU': 'GOLD', 'GC': 'GOLD',
            'SILVER': 'SILVER', 'XAG': 'SILVER', 'SI': 'SILVER',
            'OIL': 'CRUDE_OIL', 'CRUDE': 'CRUDE_OIL', 'CL': 'CRUDE_OIL',
            'GAS': 'NATURAL_GAS', 'NG': 'NATURAL_GAS',
            'COPPER': 'COPPER', 'HG': 'COPPER',
            'WHEAT': 'WHEAT', 'ZW': 'WHEAT',
            'CORN': 'CORN', 'ZC': 'CORN'
        }
        
        mapped_symbol = symbol_mapping.get(symbol.upper(), 'GOLD')
        return self.commodity_profiles.get(mapped_symbol, self.commodity_profiles['GOLD'])
    
    def _analyze_supply_demand(self, profile: CommodityProfile, historical_data: Optional[pd.DataFrame]) -> SupplyDemandAnalysis:
        """Supply-Demand analizi"""
        try:
            # Simulated supply-demand data (gerçekte API'den gelir)
            base_supply = 100.0
            base_demand = 98.0
            
            # Commodity type'a göre adjust
            if profile.commodity_type == CommodityType.ENERGY:
                supply_growth = np.random.normal(2.5, 1.5)
                demand_growth = np.random.normal(3.0, 1.0)
            elif profile.commodity_type == CommodityType.PRECIOUS_METALS:
                supply_growth = np.random.normal(1.5, 0.8)
                demand_growth = np.random.normal(2.0, 1.2)
            elif profile.commodity_type == CommodityType.AGRICULTURE:
                supply_growth = np.random.normal(1.8, 2.0)  # Weather dependent
                demand_growth = np.random.normal(2.2, 0.8)
            else:
                supply_growth = np.random.normal(2.0, 1.0)
                demand_growth = np.random.normal(2.5, 1.0)
            
            # Inventory levels
            inventory_levels = np.random.uniform(85, 115)
            inventory_ratio = inventory_levels / base_demand
            
            # Risk factors
            supply_disruption_risk = profile.geopolitical_sensitivity * np.random.uniform(0.1, 0.4)
            demand_shock_probability = abs(profile.demand_elasticity) * np.random.uniform(0.1, 0.3)
            
            # Balance score
            balance_score = 50 + (base_demand - base_supply) * 2
            balance_score = max(0, min(100, balance_score))
            
            return SupplyDemandAnalysis(
                global_supply=base_supply,
                global_demand=base_demand,
                supply_growth_rate=supply_growth,
                demand_growth_rate=demand_growth,
                inventory_levels=inventory_levels,
                inventory_to_usage_ratio=inventory_ratio,
                supply_disruption_risk=supply_disruption_risk,
                demand_shock_probability=demand_shock_probability,
                balance_score=balance_score
            )
            
        except Exception as e:
            print(f"ERROR: Supply-demand analizi hatası: {str(e)}")
            return SupplyDemandAnalysis(100, 100, 2, 2, 100, 1.0, 0.2, 0.2, 50)
    
    def _analyze_macro_factors(self, profile: CommodityProfile) -> MacroFactors:
        """Makroekonomik faktör analizi"""
        try:
            # Simulated macro data
            return MacroFactors(
                global_gdp_growth=np.random.normal(2.8, 0.8),
                industrial_production_index=np.random.normal(102.5, 3.0),
                dollar_strength_index=np.random.normal(103.2, 2.5),
                inflation_expectations=np.random.normal(2.5, 0.5),
                interest_rate_environment=np.random.normal(4.5, 1.0),
                china_pmi=np.random.normal(50.5, 2.0),
                us_economic_strength=np.random.normal(75.0, 10.0),
                geopolitical_risk_score=np.random.uniform(30, 70)
            )
            
        except Exception:
            return MacroFactors(2.8, 102.5, 103.2, 2.5, 4.5, 50.5, 75.0, 50.0)
    
    def _forecast_prices(self, profile: CommodityProfile, supply_demand: SupplyDemandAnalysis, 
                        macro: MacroFactors, current_price: float) -> Dict[str, float]:
        """Fiyat tahmini"""
        try:
            if current_price is None:
                current_price = 100.0
            
            # Supply-demand impact
            sd_impact = (supply_demand.demand_growth_rate - supply_demand.supply_growth_rate) * 0.05
            
            # Macro impact
            macro_impact = (macro.global_gdp_growth - 2.0) * 0.03
            macro_impact += (macro.inflation_expectations - 2.0) * 0.02
            
            # Dollar impact (negative for commodities)
            dollar_impact = -(macro.dollar_strength_index - 100) * 0.001
            
            # Total price change forecast
            total_impact = sd_impact + macro_impact + dollar_impact
            
            return {
                '1_month': current_price * (1 + total_impact * 0.3),
                '3_months': current_price * (1 + total_impact * 0.6),
                '6_months': current_price * (1 + total_impact),
                '12_months': current_price * (1 + total_impact * 1.5),
                'supply_demand_impact': sd_impact,
                'macro_impact': macro_impact,
                'dollar_impact': dollar_impact
            }
            
        except Exception:
            return {'1_month': current_price or 100, '3_months': current_price or 100}
    
    def _analyze_volatility(self, profile: CommodityProfile, historical_data: Optional[pd.DataFrame]) -> Dict[str, Any]:
        """Volatilite analizi"""
        try:
            if historical_data is not None and len(historical_data) > 30:
                returns = historical_data['Close'].pct_change(fill_method=None).dropna()
                realized_vol = returns.std() * np.sqrt(252)
            else:
                # Default volatility by commodity type
                vol_map = {
                    CommodityType.ENERGY: 0.35,
                    CommodityType.PRECIOUS_METALS: 0.20,
                    CommodityType.BASE_METALS: 0.25,
                    CommodityType.AGRICULTURE: 0.30
                }
                realized_vol = vol_map.get(profile.commodity_type, 0.25)
            
            # Volatility regime
            if realized_vol > 0.4:
                vol_regime = 'extreme'
            elif realized_vol > 0.3:
                vol_regime = 'high'
            elif realized_vol > 0.15:
                vol_regime = 'normal'
            else:
                vol_regime = 'low'
            
            return {
                'realized_volatility': realized_vol,
                'volatility_regime': vol_regime,
                'volatility_percentile': np.random.uniform(20, 80),
                'vol_forecast': {
                    '1_month': realized_vol * np.random.uniform(0.9, 1.1),
                    '3_months': realized_vol * np.random.uniform(0.8, 1.2)
                }
            }
            
        except Exception:
            return {'realized_volatility': 0.25, 'volatility_regime': 'normal'}
    
    def _analyze_seasonality(self, profile: CommodityProfile, historical_data: Optional[pd.DataFrame]) -> Dict[str, Any]:
        """Seasonality analizi"""
        try:
            # Strong seasonal commodities
            if profile.commodity_type == CommodityType.AGRICULTURE:
                seasonal_strength = 'Güçlü'
                best_months = [8, 9, 10]  # Harvest season
                worst_months = [3, 4, 5]  # Planting season
            elif profile.commodity_type == CommodityType.ENERGY and 'GAS' in profile.name.upper():
                seasonal_strength = 'Güçlü'
                best_months = [11, 12, 1, 2]  # Winter
                worst_months = [6, 7, 8]  # Summer
            else:
                seasonal_strength = 'Orta'
                best_months = [np.random.randint(1, 13)]
                worst_months = [np.random.randint(1, 13)]
            
            current_month = datetime.now().month
            current_bias = 'Pozitif' if current_month in best_months else 'Negatif' if current_month in worst_months else 'Nötr'
            
            return {
                'seasonal_strength': seasonal_strength,
                'seasonality_factor': profile.seasonality_factor,
                'best_months': best_months,
                'worst_months': worst_months,
                'current_month_bias': current_bias
            }
            
        except Exception:
            return {'seasonal_strength': 'Orta', 'current_month_bias': 'Nötr'}
    
    def _generate_technical_signals(self, historical_data: Optional[pd.DataFrame]) -> Dict[str, float]:
        """Technical sinyaller"""
        try:
            if historical_data is None or len(historical_data) < 50:
                return {
                    'rsi': np.random.uniform(30, 70),
                    'ma_signal': np.random.choice([-1, 0, 1]),
                    'macd_signal': np.random.uniform(-2, 2),
                    'momentum': np.random.uniform(-10, 10)
                }
            
            close = historical_data['Close']
            
            # RSI
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Moving averages
            ma_20 = close.rolling(20).mean()
            ma_50 = close.rolling(50).mean()
            ma_signal = 1 if ma_20.iloc[-1] > ma_50.iloc[-1] else -1
            
            return {
                'rsi': rsi.iloc[-1] if not np.isnan(rsi.iloc[-1]) else 50,
                'ma_signal': ma_signal,
                'macd_signal': np.random.uniform(-2, 2),
                'momentum': np.random.uniform(-10, 10)
            }
            
        except Exception:
            return {'rsi': 50, 'ma_signal': 0, 'macd_signal': 0, 'momentum': 0}
    
    def _generate_fundamental_signals(self, supply_demand: SupplyDemandAnalysis, macro: MacroFactors) -> Dict[str, Any]:
        """Fundamental sinyaller"""
        try:
            # Supply-demand signal
            sd_signal = 'Pozitif' if supply_demand.demand_growth_rate > supply_demand.supply_growth_rate else 'Negatif'
            
            # Inventory signal
            inventory_signal = 'Düşük Stok' if supply_demand.inventory_to_usage_ratio < 0.9 else 'Yüksek Stok'
            
            # Macro signal
            macro_signal = 'Pozitif' if macro.global_gdp_growth > 2.5 else 'Negatif'
            
            # Dollar signal
            dollar_signal = 'Negatif' if macro.dollar_strength_index > 105 else 'Pozitif'
            
            return {
                'supply_demand_signal': sd_signal,
                'inventory_signal': inventory_signal,
                'macro_signal': macro_signal,
                'dollar_signal': dollar_signal,
                'overall_fundamental': 'ALIŞ' if [sd_signal, macro_signal, dollar_signal].count('Pozitif') >= 2 else 'SATIŞ'
            }
            
        except Exception:
            return {'overall_fundamental': 'BEKLE'}
    
    def _calculate_ultra_commodity_score(self, supply_demand: SupplyDemandAnalysis, 
                                       macro: MacroFactors, volatility: Dict, seasonality: Dict) -> float:
        """Ultra commodity skoru hesapla"""
        try:
            scores = []
            
            # Supply-demand score (40%)
            sd_score = supply_demand.balance_score
            scores.append(sd_score * 0.4)
            
            # Macro score (30%)
            macro_score = 50 + (macro.global_gdp_growth - 2.0) * 10
            macro_score = max(0, min(100, macro_score))
            scores.append(macro_score * 0.3)
            
            # Volatility score (20%)
            vol_regime = volatility.get('volatility_regime', 'normal')
            vol_scores = {'low': 80, 'normal': 65, 'high': 40, 'extreme': 20}
            vol_score = vol_scores.get(vol_regime, 50)
            scores.append(vol_score * 0.2)
            
            # Seasonality score (10%)
            seasonal_bias = seasonality.get('current_month_bias', 'Nötr')
            seasonal_score = 70 if seasonal_bias == 'Pozitif' else 30 if seasonal_bias == 'Negatif' else 50
            scores.append(seasonal_score * 0.1)
            
            return sum(scores)
            
        except Exception:
            return 50.0
    
    def _generate_trading_recommendation(self, ultra_score: float, price_forecast: Dict, 
                                       volatility: Dict, profile: CommodityProfile) -> str:
        """Trading önerisi üret"""
        try:
            # Score-based recommendation
            if ultra_score >= 75:
                base_rec = "GÜÇLÜ ALIŞ"
            elif ultra_score >= 60:
                base_rec = "ALIŞ"
            elif ultra_score >= 40:
                base_rec = "BEKLE"
            elif ultra_score >= 25:
                base_rec = "SAT"
            else:
                base_rec = "GÜÇLÜ SAT"
            
            # Volatility adjustment
            vol_regime = volatility.get('volatility_regime', 'normal')
            if vol_regime in ['high', 'extreme'] and 'GÜÇLÜ' in base_rec:
                base_rec = base_rec.replace('GÜÇLÜ ', 'DİKKATLİ ')
            
            return base_rec
            
        except Exception:
            return "BEKLE"
    
    def _assess_risks(self, profile: CommodityProfile, supply_demand: SupplyDemandAnalysis, 
                     macro: MacroFactors) -> Dict[str, str]:
        """Risk değerlendirmesi"""
        try:
            # Geopolitical risk
            geo_risk = 'Yüksek' if profile.geopolitical_sensitivity > 0.7 else 'Orta' if profile.geopolitical_sensitivity > 0.4 else 'Düşük'
            
            # Supply risk
            supply_risk = 'Yüksek' if supply_demand.supply_disruption_risk > 0.3 else 'Orta' if supply_demand.supply_disruption_risk > 0.15 else 'Düşük'
            
            # Demand risk
            demand_risk = 'Yüksek' if supply_demand.demand_shock_probability > 0.25 else 'Orta' if supply_demand.demand_shock_probability > 0.15 else 'Düşük'
            
            # Overall risk
            risk_factors = [geo_risk, supply_risk, demand_risk]
            high_count = risk_factors.count('Yüksek')
            
            if high_count >= 2:
                overall_risk = 'Yüksek Risk'
            elif high_count == 1 or risk_factors.count('Orta') >= 2:
                overall_risk = 'Orta Risk'
            else:
                overall_risk = 'Düşük Risk'
            
            return {
                'overall_risk': overall_risk,
                'geopolitical_risk': geo_risk,
                'supply_risk': supply_risk,
                'demand_risk': demand_risk,
                'volatility_risk': 'Yüksek' if profile.commodity_type == CommodityType.ENERGY else 'Orta'
            }
            
        except Exception:
            return {'overall_risk': 'Orta Risk'}
    
    def _get_default_commodity_result(self, symbol: str, current_price: float) -> CommodityAnalysisResult:
        """Varsayılan emtia sonucu"""
        default_profile = CommodityProfile(
            symbol=symbol, name=symbol, commodity_type=CommodityType.ENERGY,
            unit='unit', exchange='EXCHANGE', is_storable=True, seasonality_factor=0.5,
            supply_elasticity=0.3, demand_elasticity=-0.4, geopolitical_sensitivity=0.5
        )
        
        return CommodityAnalysisResult(
            ultra_commodity_score=50.0,
            commodity_profile=default_profile,
            supply_demand=SupplyDemandAnalysis(100, 100, 2, 2, 100, 1.0, 0.2, 0.2, 50),
            macro_factors=MacroFactors(2.5, 100, 100, 2.5, 4.0, 50, 70, 50),
            price_forecast={'1_month': current_price or 100},
            volatility_analysis={'realized_volatility': 0.25, 'volatility_regime': 'normal'},
            trading_recommendation='BEKLE',
            risk_assessment={'overall_risk': 'Orta Risk'},
            seasonal_patterns={'seasonal_strength': 'Orta'},
            technical_signals={'rsi': 50},
            fundamental_signals={'overall_fundamental': 'BEKLE'}
        )

print("INFO: Ultra Commodities Analyzer başarıyla yüklendi")
