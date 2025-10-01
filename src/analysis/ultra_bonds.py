"""
Ultra Bonds Analysis Module
Ultra Tahvil Analizi Modülü

Bu modül gelişmiş tahvil yield curve analizi, faiz oranı modelleme,
credit risk assessment ve fixed income araçlarının analizini sağlar.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from scipy.optimize import minimize
from scipy.interpolate import interp1d

print("INFO: Ultra Bonds Analysis modülü aktif")

class BondType(Enum):
    """Tahvil türleri"""
    GOVERNMENT = "government"       # Devlet tahvilleri
    CORPORATE = "corporate"         # Kurumsal tahviller
    MUNICIPAL = "municipal"         # Belediye tahvilleri
    TREASURY = "treasury"          # Hazine bonoları
    INFLATION_LINKED = "tips"      # Enflasyon korumalı
    HIGH_YIELD = "high_yield"      # Yüksek verimli (junk)
    EMERGING_MARKET = "emerging"   # Gelişen piyasa

class CreditRating(Enum):
    """Kredi notları"""
    AAA = "AAA"
    AA = "AA"
    A = "A"
    BBB = "BBB"
    BB = "BB"
    B = "B"
    CCC = "CCC"
    CC = "CC"
    C = "C"
    D = "D"

@dataclass
class YieldCurve:
    """Yield curve verisi"""
    maturities: List[float]  # Years
    yields: List[float]      # Percent
    curve_date: datetime
    curve_type: str          # zero, par, forward
    currency: str
    interpolated_yields: Dict[float, float]  # Interpolated points

@dataclass
class BondProfile:
    """Tahvil profili"""
    symbol: str
    issuer: str
    bond_type: BondType
    credit_rating: CreditRating
    maturity_date: datetime
    coupon_rate: float
    face_value: float
    issue_date: datetime
    callable: bool
    puttable: bool
    currency: str
    sector: Optional[str]

@dataclass
class InterestRateEnvironment:
    """Faiz oranı ortamı"""
    fed_funds_rate: float
    central_bank_trend: str  # hiking, cutting, holding
    real_rates: float
    term_premium: float
    inflation_expectations: float
    policy_uncertainty: float
    rate_cycle_phase: str
    next_meeting_probability: Dict[str, float]

@dataclass
class CreditRiskMetrics:
    """Kredi riski metrikleri"""
    default_probability: float
    loss_given_default: float
    expected_loss: float
    credit_spread: float
    cds_spread: Optional[float]
    credit_score: float
    financial_health_score: float
    sector_risk_premium: float

@dataclass
class YieldCurveAnalysis:
    """Yield curve analizi"""
    curve_shape: str  # normal, inverted, flat, humped
    steepness: float
    curvature: float
    level_shift: float
    slope_change: float
    twist_factor: float
    butterfly_spread: float
    recession_signal: bool

@dataclass
class BondValuationMetrics:
    """Tahvil değerleme metrikleri"""
    fair_value: float
    current_yield: float
    yield_to_maturity: float
    yield_to_call: Optional[float]
    duration: float
    modified_duration: float
    convexity: float
    dv01: float  # Dollar value of 01
    option_adjusted_spread: Optional[float]

@dataclass
class BondAnalysisResult:
    """Tahvil analizi sonucu"""
    ultra_bond_score: float
    bond_profile: BondProfile
    yield_curve: YieldCurve
    yield_curve_analysis: YieldCurveAnalysis
    interest_rate_environment: InterestRateEnvironment
    credit_risk: CreditRiskMetrics
    valuation_metrics: BondValuationMetrics
    trading_recommendation: str
    risk_assessment: Dict[str, str]
    relative_value_analysis: Dict[str, Any]
    technical_signals: Dict[str, float]
    macro_sensitivity: Dict[str, float]

class UltraBondsAnalyzer:
    """Ultra gelişmiş tahvil analizi"""
    
    def __init__(self):
        """Ultra Bonds Analyzer başlat"""
        self.yield_curves = self._initialize_yield_curves()
        self.credit_spreads = self._initialize_credit_spreads()
        self.sector_premiums = self._get_sector_premiums()
        print("INFO: Ultra Bonds Analyzer gelişmiş fixed income modelleri ile başlatıldı")
    
    def _initialize_yield_curves(self) -> Dict[str, YieldCurve]:
        """Yield curve'leri başlat"""
        curves = {}
        
        # US Treasury Curve
        us_maturities = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
        us_yields = [5.25, 5.15, 5.0, 4.8, 4.6, 4.4, 4.5, 4.6, 4.8, 4.9]
        
        curves['USD'] = YieldCurve(
            maturities=us_maturities,
            yields=us_yields,
            curve_date=datetime.now(),
            curve_type="par",
            currency="USD",
            interpolated_yields={}
        )
        
        # German Bund Curve
        eur_maturities = [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
        eur_yields = [3.8, 3.7, 3.5, 3.3, 3.2, 3.1, 3.2, 3.3, 3.5, 3.6]
        
        curves['EUR'] = YieldCurve(
            maturities=eur_maturities,
            yields=eur_yields,
            curve_date=datetime.now(),
            curve_type="par",
            currency="EUR",
            interpolated_yields={}
        )
        
        # Turkish Government Curve
        try_maturities = [0.25, 0.5, 1, 2, 3, 5, 7, 10]
        try_yields = [50.0, 48.5, 47.0, 45.0, 43.0, 40.0, 38.0, 35.0]
        
        curves['TRY'] = YieldCurve(
            maturities=try_maturities,
            yields=try_yields,
            curve_date=datetime.now(),
            curve_type="par",
            currency="TRY",
            interpolated_yields={}
        )
        
        # Interpolate curves
        for currency, curve in curves.items():
            curve.interpolated_yields = self._interpolate_curve(curve)
        
        return curves
    
    def _interpolate_curve(self, curve: YieldCurve) -> Dict[float, float]:
        """Yield curve interpolasyonu"""
        try:
            f = interp1d(curve.maturities, curve.yields, kind='cubic', fill_value='extrapolate')
            
            # Common interpolation points
            interp_points = [0.083, 0.167, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 7, 10, 15, 20, 25, 30]
            interpolated = {}
            
            for point in interp_points:
                if point <= max(curve.maturities):
                    interpolated[point] = float(f(point))
            
            return interpolated
            
        except Exception as e:
            print(f"WARNING: Curve interpolation hatası: {str(e)}")
            return {}
    
    def _initialize_credit_spreads(self) -> Dict[str, Dict[str, float]]:
        """Kredi spreadlerini başlat"""
        return {
            'USD': {
                'AAA': 0.15, 'AA': 0.25, 'A': 0.45, 'BBB': 0.85,
                'BB': 2.50, 'B': 4.50, 'CCC': 8.50, 'CC': 15.0, 'C': 25.0
            },
            'EUR': {
                'AAA': 0.20, 'AA': 0.35, 'A': 0.55, 'BBB': 1.00,
                'BB': 3.00, 'B': 5.50, 'CCC': 10.0, 'CC': 18.0, 'C': 30.0
            },
            'TRY': {
                'AAA': 2.0, 'AA': 3.5, 'A': 5.0, 'BBB': 7.5,
                'BB': 12.0, 'B': 18.0, 'CCC': 25.0, 'CC': 35.0, 'C': 50.0
            }
        }
    
    def _get_sector_premiums(self) -> Dict[str, float]:
        """Sektör risk primlerini al"""
        return {
            'financials': 0.5, 'energy': 0.8, 'utilities': 0.3,
            'technology': 0.4, 'healthcare': 0.3, 'industrials': 0.5,
            'materials': 0.7, 'consumer_discretionary': 0.6,
            'consumer_staples': 0.4, 'telecommunications': 0.6,
            'real_estate': 0.9, 'government': 0.0
        }
    
    def analyze_bond(self, symbol: str, bond_data: Optional[Dict] = None,
                    historical_data: Optional[pd.DataFrame] = None, **kwargs) -> BondAnalysisResult:
        """Kapsamlı tahvil analizi"""
        try:
            # Bond profile oluştur
            bond_profile = self._create_bond_profile(symbol, bond_data)
            
            # Yield curve al
            yield_curve = self._get_relevant_yield_curve(bond_profile.currency)
            
            # Yield curve analizi
            yield_curve_analysis = self._analyze_yield_curve(yield_curve)
            
            # Interest rate environment
            ir_environment = self._analyze_interest_rate_environment(bond_profile.currency)
            
            # Credit risk analizi
            credit_risk = self._analyze_credit_risk(bond_profile, historical_data)
            
            # Bond valuation
            valuation_metrics = self._calculate_bond_valuation(bond_profile, yield_curve, credit_risk)
            
            # Relative value analizi
            relative_value = self._analyze_relative_value(bond_profile, yield_curve, credit_risk)
            
            # Technical signals
            technical_signals = self._generate_bond_technical_signals(historical_data)
            
            # Macro sensitivity
            macro_sensitivity = self._calculate_macro_sensitivity(bond_profile, valuation_metrics)
            
            # Ultra bond score hesapla
            ultra_score = self._calculate_ultra_bond_score(
                valuation_metrics, credit_risk, yield_curve_analysis, ir_environment
            )
            
            # Trading recommendation
            trading_recommendation = self._generate_bond_recommendation(
                ultra_score, valuation_metrics, credit_risk, yield_curve_analysis
            )
            
            # Risk assessment
            risk_assessment = self._assess_bond_risks(bond_profile, credit_risk, ir_environment)
            
            return BondAnalysisResult(
                ultra_bond_score=ultra_score,
                bond_profile=bond_profile,
                yield_curve=yield_curve,
                yield_curve_analysis=yield_curve_analysis,
                interest_rate_environment=ir_environment,
                credit_risk=credit_risk,
                valuation_metrics=valuation_metrics,
                trading_recommendation=trading_recommendation,
                risk_assessment=risk_assessment,
                relative_value_analysis=relative_value,
                technical_signals=technical_signals,
                macro_sensitivity=macro_sensitivity
            )
            
        except Exception as e:
            print(f"ERROR: Bond analizi hatası: {str(e)}")
            return self._get_default_bond_result(symbol)
    
    def _create_bond_profile(self, symbol: str, bond_data: Optional[Dict]) -> BondProfile:
        """Bond profili oluştur"""
        try:
            if bond_data:
                return BondProfile(
                    symbol=symbol,
                    issuer=bond_data.get('issuer', 'Unknown'),
                    bond_type=BondType(bond_data.get('bond_type', 'government')),
                    credit_rating=CreditRating(bond_data.get('rating', 'BBB')),
                    maturity_date=datetime.strptime(bond_data.get('maturity', '2030-01-01'), '%Y-%m-%d'),
                    coupon_rate=bond_data.get('coupon', 4.0),
                    face_value=bond_data.get('face_value', 1000),
                    issue_date=datetime.strptime(bond_data.get('issue_date', '2020-01-01'), '%Y-%m-%d'),
                    callable=bond_data.get('callable', False),
                    puttable=bond_data.get('puttable', False),
                    currency=bond_data.get('currency', 'USD'),
                    sector=bond_data.get('sector', 'government')
                )
            else:
                # Default bond based on symbol
                if 'TR' in symbol.upper() or 'TL' in symbol.upper():
                    currency, rating = 'TRY', 'B'
                elif 'DE' in symbol.upper() or 'BUND' in symbol.upper():
                    currency, rating = 'EUR', 'AAA'
                else:
                    currency, rating = 'USD', 'AA'
                
                return BondProfile(
                    symbol=symbol,
                    issuer='Government',
                    bond_type=BondType.GOVERNMENT,
                    credit_rating=CreditRating(rating),
                    maturity_date=datetime.now() + timedelta(days=365*5),
                    coupon_rate=4.0,
                    face_value=1000,
                    issue_date=datetime.now() - timedelta(days=365),
                    callable=False,
                    puttable=False,
                    currency=currency,
                    sector='government'
                )
                
        except Exception as e:
            print(f"WARNING: Bond profile oluşturma hatası: {str(e)}")
            return BondProfile(
                symbol=symbol, issuer='Unknown', bond_type=BondType.GOVERNMENT,
                credit_rating=CreditRating.BBB, maturity_date=datetime.now() + timedelta(days=1825),
                coupon_rate=4.0, face_value=1000, issue_date=datetime.now(),
                callable=False, puttable=False, currency='USD', sector='government'
            )
    
    def _get_relevant_yield_curve(self, currency: str) -> YieldCurve:
        """İlgili yield curve'ü al"""
        return self.yield_curves.get(currency, self.yield_curves['USD'])
    
    def _analyze_yield_curve(self, yield_curve: YieldCurve) -> YieldCurveAnalysis:
        """Yield curve analizi"""
        try:
            yields = np.array(yield_curve.yields)
            maturities = np.array(yield_curve.maturities)
            
            # Curve shape
            short_yield = yields[0]  # 3M
            long_yield = yields[-1]  # 30Y
            mid_yield = yields[len(yields)//2]  # ~5-7Y
            
            if long_yield > short_yield + 0.5:
                shape = "normal"
            elif short_yield > long_yield + 0.2:
                shape = "inverted"
            elif abs(long_yield - short_yield) < 0.3:
                shape = "flat"
            else:
                shape = "humped"
            
            # Steepness (10Y-2Y spread)
            ten_year_idx = np.argmin(np.abs(maturities - 10))
            two_year_idx = np.argmin(np.abs(maturities - 2))
            steepness = yields[ten_year_idx] - yields[two_year_idx]
            
            # Curvature (butterfly: 2*5Y - 2Y - 10Y)
            five_year_idx = np.argmin(np.abs(maturities - 5))
            curvature = 2 * yields[five_year_idx] - yields[two_year_idx] - yields[ten_year_idx]
            
            # Level (average of curve)
            level_shift = np.mean(yields)
            
            # Recession signal (inverted curve)
            recession_signal = steepness < -0.5
            
            return YieldCurveAnalysis(
                curve_shape=shape,
                steepness=steepness,
                curvature=curvature,
                level_shift=level_shift,
                slope_change=steepness,  # Simplified
                twist_factor=curvature,
                butterfly_spread=curvature,
                recession_signal=recession_signal
            )
            
        except Exception as e:
            print(f"ERROR: Yield curve analizi hatası: {str(e)}")
            return YieldCurveAnalysis("normal", 1.0, 0.1, 4.0, 1.0, 0.1, 0.1, False)
    
    def _analyze_interest_rate_environment(self, currency: str) -> InterestRateEnvironment:
        """Faiz oranı ortamı analizi"""
        try:
            # Currency-specific rates
            if currency == 'USD':
                fed_funds = 5.25
                trend = "holding"
                real_rates = 2.5
                inflation_exp = 2.8
            elif currency == 'EUR':
                fed_funds = 4.0
                trend = "cutting"
                real_rates = 1.5
                inflation_exp = 2.5
            elif currency == 'TRY':
                fed_funds = 50.0
                trend = "cutting"
                real_rates = 30.0
                inflation_exp = 20.0
            else:
                fed_funds = 4.0
                trend = "holding"
                real_rates = 2.0
                inflation_exp = 2.5
            
            # Rate cycle phase
            if trend == "hiking":
                cycle_phase = "tightening"
            elif trend == "cutting":
                cycle_phase = "easing"
            else:
                cycle_phase = "neutral"
            
            return InterestRateEnvironment(
                fed_funds_rate=fed_funds,
                central_bank_trend=trend,
                real_rates=real_rates,
                term_premium=np.random.uniform(0.5, 1.5),
                inflation_expectations=inflation_exp,
                policy_uncertainty=np.random.uniform(0.2, 0.8),
                rate_cycle_phase=cycle_phase,
                next_meeting_probability={
                    'hike': 15 if trend == "hiking" else 5,
                    'hold': 70 if trend == "holding" else 30,
                    'cut': 60 if trend == "cutting" else 10
                }
            )
            
        except Exception:
            return InterestRateEnvironment(4.0, "holding", 2.0, 1.0, 2.5, 0.5, "neutral", {"hold": 70})
    
    def _analyze_credit_risk(self, bond_profile: BondProfile, historical_data: Optional[pd.DataFrame]) -> CreditRiskMetrics:
        """Kredi riski analizi"""
        try:
            rating = bond_profile.credit_rating.value
            currency = bond_profile.currency
            
            # Default probabilities by rating
            default_probs = {
                'AAA': 0.001, 'AA': 0.002, 'A': 0.005, 'BBB': 0.015,
                'BB': 0.050, 'B': 0.120, 'CCC': 0.300, 'CC': 0.500, 'C': 0.800, 'D': 1.000
            }
            
            base_default_prob = default_probs.get(rating, 0.015)
            
            # Adjust for currency/country risk
            if currency == 'TRY':
                base_default_prob *= 3.0
            elif currency == 'EUR':
                base_default_prob *= 0.8
            
            # Loss given default
            if bond_profile.bond_type == BondType.GOVERNMENT:
                lgd = 0.10  # Low recovery for government
            elif bond_profile.bond_type == BondType.CORPORATE:
                lgd = 0.40  # Standard corporate
            else:
                lgd = 0.30
            
            # Expected loss
            expected_loss = base_default_prob * lgd
            
            # Credit spread
            base_spread = self.credit_spreads.get(currency, {}).get(rating, 1.0)
            sector_premium = self.sector_premiums.get(bond_profile.sector or 'government', 0.0)
            credit_spread = base_spread + sector_premium
            
            # Credit score (0-100)
            credit_score = 100 - (base_default_prob * 100 * 10)  # Scale to 0-100
            credit_score = max(0, min(100, credit_score))
            
            # Financial health score
            if rating in ['AAA', 'AA', 'A']:
                health_score = np.random.uniform(75, 95)
            elif rating in ['BBB']:
                health_score = np.random.uniform(60, 80)
            elif rating in ['BB', 'B']:
                health_score = np.random.uniform(40, 65)
            else:
                health_score = np.random.uniform(10, 45)
            
            return CreditRiskMetrics(
                default_probability=base_default_prob,
                loss_given_default=lgd,
                expected_loss=expected_loss,
                credit_spread=credit_spread,
                cds_spread=credit_spread * 0.8 if bond_profile.bond_type == BondType.CORPORATE else None,
                credit_score=credit_score,
                financial_health_score=health_score,
                sector_risk_premium=sector_premium
            )
            
        except Exception as e:
            print(f"ERROR: Credit risk analizi hatası: {str(e)}")
            return CreditRiskMetrics(0.015, 0.4, 0.006, 1.0, None, 70, 70, 0.5)
    
    def _calculate_bond_valuation(self, bond_profile: BondProfile, yield_curve: YieldCurve, 
                                 credit_risk: CreditRiskMetrics) -> BondValuationMetrics:
        """Bond değerleme metrikleri"""
        try:
            # Time to maturity
            time_to_maturity = (bond_profile.maturity_date - datetime.now()).days / 365.25
            
            # Risk-free rate from curve
            if time_to_maturity in yield_curve.interpolated_yields:
                risk_free_rate = yield_curve.interpolated_yields[time_to_maturity] / 100
            else:
                # Find closest maturity
                closest_maturity = min(yield_curve.maturities, key=lambda x: abs(x - time_to_maturity))
                closest_idx = yield_curve.maturities.index(closest_maturity)
                risk_free_rate = yield_curve.yields[closest_idx] / 100
            
            # Yield to maturity (risk-free + credit spread)
            ytm = risk_free_rate + (credit_risk.credit_spread / 100)
            
            # Current yield
            current_yield = bond_profile.coupon_rate / 100  # Simplified
            
            # Fair value calculation (present value of cash flows)
            coupon_pmt = bond_profile.face_value * (bond_profile.coupon_rate / 100)
            periods = max(1, int(time_to_maturity * 2))  # Semi-annual
            
            # PV of coupons
            pv_coupons = sum([coupon_pmt / ((1 + ytm/2) ** t) for t in range(1, periods + 1)])
            
            # PV of principal
            pv_principal = bond_profile.face_value / ((1 + ytm/2) ** periods)
            
            fair_value = pv_coupons + pv_principal
            
            # Duration (simplified Macaulay duration)
            duration = time_to_maturity * 0.85  # Approximation
            
            # Modified duration
            modified_duration = duration / (1 + ytm/2)
            
            # Convexity (approximation)
            convexity = duration ** 2 + duration
            
            # DV01 (dollar value of 01 basis point)
            dv01 = fair_value * modified_duration * 0.0001
            
            return BondValuationMetrics(
                fair_value=fair_value,
                current_yield=current_yield * 100,
                yield_to_maturity=ytm * 100,
                yield_to_call=ytm * 100 + 0.2 if bond_profile.callable else None,
                duration=duration,
                modified_duration=modified_duration,
                convexity=convexity,
                dv01=dv01,
                option_adjusted_spread=credit_risk.credit_spread if bond_profile.callable else None
            )
            
        except Exception as e:
            print(f"ERROR: Bond valuation hatası: {str(e)}")
            return BondValuationMetrics(1000, 4.0, 4.5, None, 5.0, 4.8, 25.0, 0.48, None)
    
    def _analyze_relative_value(self, bond_profile: BondProfile, yield_curve: YieldCurve, 
                               credit_risk: CreditRiskMetrics) -> Dict[str, Any]:
        """Relative value analizi"""
        try:
            # Spread to benchmark
            time_to_maturity = (bond_profile.maturity_date - datetime.now()).days / 365.25
            
            # Find benchmark yield
            closest_maturity = min(yield_curve.maturities, key=lambda x: abs(x - time_to_maturity))
            closest_idx = yield_curve.maturities.index(closest_maturity)
            benchmark_yield = yield_curve.yields[closest_idx]
            
            # Current bond yield (risk-free + spread)
            bond_yield = benchmark_yield + credit_risk.credit_spread
            
            # Z-spread analysis
            z_spread = credit_risk.credit_spread
            
            # Sector comparison
            sector_avg_spread = self.sector_premiums.get(bond_profile.sector or 'government', 0.5)
            sector_relative = credit_risk.credit_spread - sector_avg_spread
            
            # Rating comparison
            rating_avg_spread = self.credit_spreads.get(bond_profile.currency, {}).get(bond_profile.credit_rating.value, 1.0)
            rating_relative = credit_risk.credit_spread - rating_avg_spread
            
            return {
                'spread_to_benchmark': z_spread,
                'z_spread': z_spread,
                'sector_relative_spread': sector_relative,
                'rating_relative_spread': rating_relative,
                'value_assessment': 'Ucuz' if sector_relative < -0.2 else 'Pahalı' if sector_relative > 0.2 else 'Adil',
                'benchmark_maturity': closest_maturity,
                'benchmark_yield': benchmark_yield,
                'bond_yield': bond_yield
            }
            
        except Exception:
            return {'spread_to_benchmark': 1.0, 'value_assessment': 'Adil'}
    
    def _generate_bond_technical_signals(self, historical_data: Optional[pd.DataFrame]) -> Dict[str, float]:
        """Bond technical sinyalleri"""
        try:
            if historical_data is None or len(historical_data) < 20:
                return {
                    'price_momentum': np.random.uniform(-5, 5),
                    'yield_momentum': np.random.uniform(-10, 10),
                    'volume_trend': np.random.choice([-1, 0, 1]),
                    'support_resistance': np.random.uniform(95, 105)
                }
            
            # Price-based signals
            price = historical_data['Close'] if 'Close' in historical_data else historical_data.iloc[:, 0]
            
            # Momentum
            price_momentum = ((price.iloc[-1] / price.iloc[-20]) - 1) * 100
            
            # Moving average
            ma_20 = price.rolling(20).mean()
            ma_signal = 1 if price.iloc[-1] > ma_20.iloc[-1] else -1
            
            return {
                'price_momentum': price_momentum,
                'yield_momentum': -price_momentum,  # Inverse relationship
                'volume_trend': ma_signal,
                'support_resistance': float(ma_20.iloc[-1]) if not np.isnan(ma_20.iloc[-1]) else 100.0
            }
            
        except Exception:
            return {'price_momentum': 0, 'yield_momentum': 0, 'volume_trend': 0, 'support_resistance': 100}
    
    def _calculate_macro_sensitivity(self, bond_profile: BondProfile, valuation: BondValuationMetrics) -> Dict[str, float]:
        """Makroekonomik duyarlılık"""
        try:
            # Duration-based interest rate sensitivity
            ir_sensitivity = valuation.modified_duration
            
            # Credit sensitivity
            if bond_profile.credit_rating.value in ['AAA', 'AA']:
                credit_sensitivity = 0.1
            elif bond_profile.credit_rating.value in ['A', 'BBB']:
                credit_sensitivity = 0.3
            else:
                credit_sensitivity = 0.6
            
            # Currency sensitivity
            if bond_profile.currency == 'USD':
                fx_sensitivity = 0.0  # Base currency
            elif bond_profile.currency == 'EUR':
                fx_sensitivity = 0.4
            elif bond_profile.currency == 'TRY':
                fx_sensitivity = 0.8
            else:
                fx_sensitivity = 0.5
            
            # Inflation sensitivity
            if bond_profile.bond_type == BondType.INFLATION_LINKED:
                inflation_sensitivity = -0.2  # Protected
            else:
                inflation_sensitivity = ir_sensitivity * 0.6
            
            return {
                'interest_rate_sensitivity': ir_sensitivity,
                'credit_sensitivity': credit_sensitivity,
                'currency_sensitivity': fx_sensitivity,
                'inflation_sensitivity': inflation_sensitivity,
                'gdp_sensitivity': credit_sensitivity * 0.5,
                'volatility_sensitivity': credit_sensitivity * 0.3
            }
            
        except Exception:
            return {'interest_rate_sensitivity': 5.0, 'credit_sensitivity': 0.3}
    
    def _calculate_ultra_bond_score(self, valuation: BondValuationMetrics, credit_risk: CreditRiskMetrics,
                                   yield_curve_analysis: YieldCurveAnalysis, ir_env: InterestRateEnvironment) -> float:
        """Ultra bond skoru hesapla"""
        try:
            scores = []
            
            # Credit quality score (30%)
            credit_score = credit_risk.credit_score
            scores.append(credit_score * 0.3)
            
            # Value score (25%)
            # Higher yield = higher score, but adjusted for credit risk
            value_score = min(100, (valuation.yield_to_maturity - 2.0) * 10)
            value_score = max(0, value_score - (credit_risk.default_probability * 1000))
            scores.append(value_score * 0.25)
            
            # Interest rate environment score (25%)
            if ir_env.central_bank_trend == "cutting":
                ir_score = 80  # Good for bonds
            elif ir_env.central_bank_trend == "hiking":
                ir_score = 30  # Bad for bonds
            else:
                ir_score = 60  # Neutral
            
            # Adjust for curve shape
            if yield_curve_analysis.curve_shape == "inverted":
                ir_score += 15  # Recession signal good for quality bonds
            elif yield_curve_analysis.curve_shape == "normal":
                ir_score += 5
            
            scores.append(ir_score * 0.25)
            
            # Duration risk score (20%)
            duration_score = max(0, 100 - (valuation.modified_duration * 8))  # Penalize long duration
            scores.append(duration_score * 0.2)
            
            return sum(scores)
            
        except Exception:
            return 50.0
    
    def _generate_bond_recommendation(self, ultra_score: float, valuation: BondValuationMetrics,
                                     credit_risk: CreditRiskMetrics, yield_curve_analysis: YieldCurveAnalysis) -> str:
        """Bond trading önerisi"""
        try:
            # Base recommendation from score
            if ultra_score >= 80:
                base_rec = "GÜÇLÜ ALIŞ"
            elif ultra_score >= 65:
                base_rec = "ALIŞ"
            elif ultra_score >= 45:
                base_rec = "BEKLE"
            elif ultra_score >= 30:
                base_rec = "SAT"
            else:
                base_rec = "GÜÇLÜ SAT"
            
            # Adjustments
            if credit_risk.default_probability > 0.1:  # High default risk
                if "ALIŞ" in base_rec:
                    base_rec = "DİKKATLİ " + base_rec
            
            if valuation.modified_duration > 10:  # High duration risk
                if "GÜÇLÜ" in base_rec and "SAT" not in base_rec:
                    base_rec = base_rec.replace("GÜÇLÜ ", "")
            
            if yield_curve_analysis.recession_signal and credit_risk.credit_score < 60:
                if "ALIŞ" in base_rec:
                    base_rec = "DİKKATLİ BEKLE"
            
            return base_rec
            
        except Exception:
            return "BEKLE"
    
    def _assess_bond_risks(self, bond_profile: BondProfile, credit_risk: CreditRiskMetrics,
                          ir_env: InterestRateEnvironment) -> Dict[str, str]:
        """Bond risk değerlendirmesi"""
        try:
            # Credit risk
            if credit_risk.default_probability > 0.05:
                credit_risk_level = "Yüksek"
            elif credit_risk.default_probability > 0.01:
                credit_risk_level = "Orta"
            else:
                credit_risk_level = "Düşük"
            
            # Interest rate risk (duration-based)
            time_to_maturity = (bond_profile.maturity_date - datetime.now()).days / 365.25
            if time_to_maturity > 10:
                ir_risk_level = "Yüksek"
            elif time_to_maturity > 3:
                ir_risk_level = "Orta"
            else:
                ir_risk_level = "Düşük"
            
            # Liquidity risk
            if bond_profile.bond_type in [BondType.GOVERNMENT, BondType.TREASURY]:
                liquidity_risk = "Düşük"
            elif bond_profile.bond_type == BondType.CORPORATE:
                liquidity_risk = "Orta"
            else:
                liquidity_risk = "Yüksek"
            
            # Currency risk
            if bond_profile.currency == 'TRY':
                currency_risk = "Yüksek"
            elif bond_profile.currency in ['EUR', 'GBP']:
                currency_risk = "Orta"
            else:
                currency_risk = "Düşük"
            
            # Overall risk
            risk_factors = [credit_risk_level, ir_risk_level, liquidity_risk, currency_risk]
            high_count = risk_factors.count("Yüksek")
            
            if high_count >= 2:
                overall_risk = "Yüksek Risk"
            elif high_count == 1 or risk_factors.count("Orta") >= 2:
                overall_risk = "Orta Risk"
            else:
                overall_risk = "Düşük Risk"
            
            return {
                'overall_risk': overall_risk,
                'credit_risk': credit_risk_level,
                'interest_rate_risk': ir_risk_level,
                'liquidity_risk': liquidity_risk,
                'currency_risk': currency_risk,
                'inflation_risk': 'Yüksek' if bond_profile.currency == 'TRY' else 'Orta'
            }
            
        except Exception:
            return {'overall_risk': 'Orta Risk'}
    
    def _get_default_bond_result(self, symbol: str) -> BondAnalysisResult:
        """Varsayılan bond sonucu"""
        default_profile = BondProfile(
            symbol=symbol, issuer='Unknown', bond_type=BondType.GOVERNMENT,
            credit_rating=CreditRating.BBB, maturity_date=datetime.now() + timedelta(days=1825),
            coupon_rate=4.0, face_value=1000, issue_date=datetime.now(),
            callable=False, puttable=False, currency='USD', sector='government'
        )
        
        return BondAnalysisResult(
            ultra_bond_score=50.0,
            bond_profile=default_profile,
            yield_curve=self.yield_curves['USD'],
            yield_curve_analysis=YieldCurveAnalysis("normal", 1.0, 0.1, 4.0, 1.0, 0.1, 0.1, False),
            interest_rate_environment=InterestRateEnvironment(4.0, "holding", 2.0, 1.0, 2.5, 0.5, "neutral", {"hold": 70}),
            credit_risk=CreditRiskMetrics(0.015, 0.4, 0.006, 1.0, None, 70, 70, 0.5),
            valuation_metrics=BondValuationMetrics(1000, 4.0, 4.5, None, 5.0, 4.8, 25.0, 0.48, None),
            trading_recommendation='BEKLE',
            risk_assessment={'overall_risk': 'Orta Risk'},
            relative_value_analysis={'value_assessment': 'Adil'},
            technical_signals={'price_momentum': 0},
            macro_sensitivity={'interest_rate_sensitivity': 5.0}
        )

print("INFO: Ultra Bonds Analyzer başarıyla yüklendi")
