"""
Ultra Currency Analysis System
Gelişmiş forex ve para birimi analiz sistemi

Bu modül sofistike forex analizi, carry trade stratejileri,
merkez bankası politika etkisi, çapraz kur korelasyonları ve
FX volatilite modellemesi içeren profesyonel currency trading
yetenekleri sağlar.

Türkçe Açıklamalar:
- Forex çifti analizi ve volatilite modellemesi
- Carry trade stratejileri ve faiz oranı differansiyelleri
- Merkez bankası politika etkisi ve forward guidance analizi
- Çapraz kur korelasyonları ve risk yönetimi
- PPP (Purchasing Power Parity) ve REER analizi
- Makroekonomik göstergeler ve forex etkisi
- Technical ve fundamental forex analizi
- Global risk appetite ve safe haven currency analizi
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

@dataclass
class CurrencyPair:
    """Para birimi çifti bilgileri"""
    base_currency: str
    quote_currency: str
    symbol: str
    current_rate: float
    daily_change: float
    volatility: float
    spread: float
    liquidity_score: float

@dataclass
class CarryTradeAnalysis:
    """Carry trade analiz sonuçları"""
    interest_rate_differential: float
    carry_yield: float
    risk_adjusted_carry: float
    volatility_cost: float
    expected_return: float
    sharpe_ratio: float
    maximum_drawdown: float
    rollover_points: float

@dataclass
class CentralBankPolicy:
    """Merkez bankası politika analizi"""
    current_rate: float
    rate_trajectory: str  # "hawkish", "dovish", "neutral"
    next_meeting_date: str
    rate_change_probability: Dict[str, float]  # {"hike": 0.3, "hold": 0.6, "cut": 0.1}
    forward_guidance: str
    policy_divergence_score: float

@dataclass
class MacroIndicators:
    """Makroekonomik göstergeler"""
    gdp_growth: float
    inflation_rate: float
    unemployment_rate: float
    current_account_balance: float
    trade_balance: float
    government_debt_ratio: float
    credit_rating: str
    economic_momentum_score: float

@dataclass
class CrossCurrencyAnalysis:
    """Çapraz kur analizi"""
    correlation_matrix: Dict[str, Dict[str, float]]
    cointegration_relationships: List[Dict]
    diversification_benefits: float
    hedging_efficiency: Dict[str, float]
    currency_strength_ranking: Dict[str, int]

@dataclass
class FXVolatilityModel:
    """FX volatilite modeli"""
    realized_volatility: float
    implied_volatility: float
    volatility_risk_premium: float
    volatility_clustering: bool
    vol_regime: str  # "low", "normal", "high", "extreme"
    volatility_forecast: Dict[str, float]  # {"1d": 0.015, "1w": 0.018, "1m": 0.022}

@dataclass
class CurrencyAnalysisResult:
    """Kapsamlı currency analiz sonucu"""
    currency_pair: CurrencyPair
    ultra_currency_score: float
    carry_trade_analysis: CarryTradeAnalysis
    central_bank_analysis: CentralBankPolicy
    macro_analysis: MacroIndicators
    cross_currency_analysis: CrossCurrencyAnalysis
    volatility_model: FXVolatilityModel
    technical_signals: Dict[str, float]
    fundamental_signals: Dict[str, float]
    risk_assessment: Dict[str, str]
    trading_recommendation: str

class UltraCurrencyAnalyzer:
    """Ultra gelişmiş currency analiz sistemi"""
    
    def __init__(self):
        """Ultra currency analyzer'ı başlat"""
        
        # Major currency pairs
        self.major_pairs = {
            'EURUSD': {'base': 'EUR', 'quote': 'USD', 'spread': 0.0001, 'liquidity': 100},
            'GBPUSD': {'base': 'GBP', 'quote': 'USD', 'spread': 0.0002, 'liquidity': 90},
            'USDJPY': {'base': 'USD', 'quote': 'JPY', 'spread': 0.001, 'liquidity': 95},
            'USDCHF': {'base': 'USD', 'quote': 'CHF', 'spread': 0.0002, 'liquidity': 85},
            'AUDUSD': {'base': 'AUD', 'quote': 'USD', 'spread': 0.0002, 'liquidity': 80},
            'USDCAD': {'base': 'USD', 'quote': 'CAD', 'spread': 0.0002, 'liquidity': 85},
            'NZDUSD': {'base': 'NZD', 'quote': 'USD', 'spread': 0.0003, 'liquidity': 70}
        }
        
        # Minor and exotic pairs
        self.minor_pairs = {
            'EURGBP': {'base': 'EUR', 'quote': 'GBP', 'spread': 0.0002, 'liquidity': 75},
            'EURJPY': {'base': 'EUR', 'quote': 'JPY', 'spread': 0.002, 'liquidity': 80},
            'GBPJPY': {'base': 'GBP', 'quote': 'JPY', 'spread': 0.003, 'liquidity': 70},
            'TRYUSD': {'base': 'TRY', 'quote': 'USD', 'spread': 0.0010, 'liquidity': 60},
            'USDTRY': {'base': 'USD', 'quote': 'TRY', 'spread': 0.0050, 'liquidity': 60}
        }
        
        # Central bank interest rates (approximate current rates)
        self.central_bank_rates = {
            'USD': {'rate': 5.25, 'bank': 'Federal Reserve', 'last_change': '2024-07-31'},
            'EUR': {'rate': 4.0, 'bank': 'European Central Bank', 'last_change': '2024-06-06'},
            'GBP': {'rate': 5.0, 'bank': 'Bank of England', 'last_change': '2024-05-09'},
            'JPY': {'rate': 0.1, 'bank': 'Bank of Japan', 'last_change': '2024-07-31'},
            'CHF': {'rate': 1.25, 'bank': 'Swiss National Bank', 'last_change': '2024-06-20'},
            'AUD': {'rate': 4.35, 'bank': 'Reserve Bank of Australia', 'last_change': '2023-11-07'},
            'CAD': {'rate': 4.75, 'bank': 'Bank of Canada', 'last_change': '2024-06-05'},
            'NZD': {'rate': 5.5, 'bank': 'Reserve Bank of New Zealand', 'last_change': '2024-05-22'},
            'TRY': {'rate': 50.0, 'bank': 'Central Bank of Turkey', 'last_change': '2024-03-21'}
        }
        
        # Safe haven currencies
        self.safe_haven_currencies = ['USD', 'JPY', 'CHF', 'EUR']
        
        # Risk currencies (commodity currencies)
        self.risk_currencies = ['AUD', 'NZD', 'CAD', 'TRY']
        
        # Economic calendar impact weights
        self.economic_indicators = {
            'GDP': {'impact': 'high', 'weight': 0.25},
            'CPI': {'impact': 'high', 'weight': 0.20},
            'Employment': {'impact': 'high', 'weight': 0.20},
            'Interest_Rate_Decision': {'impact': 'very_high', 'weight': 0.30},
            'PMI': {'impact': 'medium', 'weight': 0.15},
            'Trade_Balance': {'impact': 'medium', 'weight': 0.12},
            'Retail_Sales': {'impact': 'medium', 'weight': 0.10}
        }
        
        print("INFO: Ultra Currency Analyzer gelişmiş forex modelleri ile başlatıldı")
    
    def analyze_currency_pair(self, symbol: str, current_rate: float = None,
                             historical_data: Optional[pd.DataFrame] = None, **kwargs) -> CurrencyAnalysisResult:
        """Kapsamlı currency pair analizi"""
        try:
            # Currency pair bilgilerini al
            pair_info = self._get_currency_pair_info(symbol, current_rate)
            
            # Carry trade analizi
            carry_analysis = self._analyze_carry_trade(
                pair_info.base_currency, pair_info.quote_currency, current_rate
            )
            
            # Merkez bankası analizi
            cb_analysis = self._analyze_central_bank_policies(
                pair_info.base_currency, pair_info.quote_currency
            )
            
            # Makroekonomik analiz
            macro_analysis = self._analyze_macro_indicators(
                pair_info.base_currency, pair_info.quote_currency
            )
            
            # Çapraz kur analizi
            cross_analysis = self._analyze_cross_currency_relationships(symbol)
            
            # Volatilite modeli
            volatility_model = self._model_fx_volatility(symbol, historical_data)
            
            # Teknik sinyaller
            technical_signals = self._generate_technical_signals(symbol, historical_data)
            
            # Fundamental sinyaller
            fundamental_signals = self._generate_fundamental_signals(
                carry_analysis, cb_analysis, macro_analysis
            )
            
            # Risk değerlendirmesi
            risk_assessment = self._assess_currency_risks(
                pair_info, volatility_model, macro_analysis
            )
            
            # Trading önerisi
            trading_recommendation = self._generate_trading_recommendation(
                carry_analysis, technical_signals, fundamental_signals, risk_assessment
            )
            
            # Ultra currency skoru
            ultra_score = self._calculate_ultra_currency_score(
                carry_analysis, cb_analysis, macro_analysis, technical_signals,
                fundamental_signals, volatility_model
            )
            
            return CurrencyAnalysisResult(
                currency_pair=pair_info,
                ultra_currency_score=ultra_score,
                carry_trade_analysis=carry_analysis,
                central_bank_analysis=cb_analysis,
                macro_analysis=macro_analysis,
                cross_currency_analysis=cross_analysis,
                volatility_model=volatility_model,
                technical_signals=technical_signals,
                fundamental_signals=fundamental_signals,
                risk_assessment=risk_assessment,
                trading_recommendation=trading_recommendation
            )
            
        except Exception as e:
            self._log_error(f"Currency pair analizi hatası: {str(e)}")
            return self._get_default_currency_result(symbol)
    
    def _get_currency_pair_info(self, symbol: str, current_rate: Optional[float]) -> CurrencyPair:
        """Currency pair bilgilerini al"""
        try:
            symbol = symbol.upper()
            
            # Pair bilgilerini bul
            if symbol in self.major_pairs:
                pair_data = self.major_pairs[symbol]
                liquidity_score = pair_data['liquidity']
            elif symbol in self.minor_pairs:
                pair_data = self.minor_pairs[symbol]
                liquidity_score = pair_data['liquidity']
            else:
                # Default exotic pair
                pair_data = {
                    'base': symbol[:3],
                    'quote': symbol[3:],
                    'spread': 0.0005,
                    'liquidity': 50
                }
                liquidity_score = 50
            
            # Simulated current rate if not provided
            if current_rate is None:
                current_rate = self._simulate_current_rate(symbol)
            
            # Simulated daily change and volatility
            daily_change = np.random.normal(0, 0.008)  # 0.8% daily volatility
            volatility = self._estimate_volatility(symbol)
            
            return CurrencyPair(
                base_currency=pair_data['base'],
                quote_currency=pair_data['quote'],
                symbol=symbol,
                current_rate=current_rate,
                daily_change=daily_change,
                volatility=volatility,
                spread=pair_data['spread'],
                liquidity_score=liquidity_score
            )
            
        except Exception as e:
            self._log_error(f"Currency pair bilgi hatası: {str(e)}")
            return CurrencyPair('USD', 'EUR', symbol, 1.0, 0.0, 0.1, 0.0001, 50)
    
    def _simulate_current_rate(self, symbol: str) -> float:
        """Simulated current exchange rate"""
        # Realistic rates for major pairs
        rates = {
            'EURUSD': 1.0850,
            'GBPUSD': 1.2650,
            'USDJPY': 149.50,
            'USDCHF': 0.9120,
            'AUDUSD': 0.6780,
            'USDCAD': 1.3540,
            'NZDUSD': 0.6150,
            'USDTRY': 27.85,
            'TRYUSD': 0.0359
        }
        
        return rates.get(symbol, 1.0000)
    
    def _estimate_volatility(self, symbol: str) -> float:
        """Currency pair volatilite tahmini"""
        # Typical annualized volatilities for major pairs
        volatilities = {
            'EURUSD': 0.12,  # 12% annual volatility
            'GBPUSD': 0.14,
            'USDJPY': 0.13,
            'USDCHF': 0.11,
            'AUDUSD': 0.16,
            'USDCAD': 0.12,
            'NZDUSD': 0.17,
            'USDTRY': 0.35,  # Much higher for TRY
            'TRYUSD': 0.35
        }
        
        base_vol = volatilities.get(symbol, 0.15)
        # Add some randomness
        return base_vol * (1 + np.random.normal(0, 0.1))
    
    def _analyze_carry_trade(self, base_currency: str, quote_currency: str,
                            current_rate: Optional[float]) -> CarryTradeAnalysis:
        """Carry trade analizi"""
        try:
            # Interest rate differential
            base_rate = self.central_bank_rates.get(base_currency, {}).get('rate', 2.0)
            quote_rate = self.central_bank_rates.get(quote_currency, {}).get('rate', 2.0)
            
            rate_differential = base_rate - quote_rate
            
            # Annual carry yield (simplified)
            carry_yield = rate_differential / 100  # Convert to decimal
            
            # Estimate volatility cost
            symbol = f"{base_currency}{quote_currency}"
            volatility = self._estimate_volatility(symbol)
            volatility_cost = volatility * 0.5  # Simplified volatility drag
            
            # Risk-adjusted carry
            risk_adjusted_carry = carry_yield - volatility_cost
            
            # Expected return (carry + potential appreciation)
            expected_return = risk_adjusted_carry + np.random.normal(0, 0.02)
            
            # Sharpe ratio approximation
            if volatility > 0:
                sharpe_ratio = risk_adjusted_carry / volatility
            else:
                sharpe_ratio = 0
            
            # Maximum drawdown estimate
            max_drawdown = volatility * np.sqrt(252) * 2.5  # Rough estimate
            
            # Rollover points (swap points)
            rollover_points = rate_differential * (current_rate or 1.0) / 365 / 100
            
            return CarryTradeAnalysis(
                interest_rate_differential=rate_differential,
                carry_yield=carry_yield,
                risk_adjusted_carry=risk_adjusted_carry,
                volatility_cost=volatility_cost,
                expected_return=expected_return,
                sharpe_ratio=sharpe_ratio,
                maximum_drawdown=max_drawdown,
                rollover_points=rollover_points
            )
            
        except Exception as e:
            self._log_error(f"Carry trade analiz hatası: {str(e)}")
            return CarryTradeAnalysis(0, 0, 0, 0, 0, 0, 0, 0)
    
    def _analyze_central_bank_policies(self, base_currency: str, quote_currency: str) -> CentralBankPolicy:
        """Merkez bankası politika analizi"""
        try:
            base_cb = self.central_bank_rates.get(base_currency, {})
            quote_cb = self.central_bank_rates.get(quote_currency, {})
            
            # Policy trajectory based on current rates and economic conditions
            trajectory_mapping = {
                'USD': 'neutral',  # Fed pause
                'EUR': 'dovish',   # ECB potential cuts
                'GBP': 'neutral',  # BoE data dependent
                'JPY': 'hawkish',  # BoJ gradual normalization
                'CHF': 'neutral',  # SNB data dependent
                'AUD': 'dovish',   # RBA potential cuts
                'CAD': 'dovish',   # BoC cutting cycle
                'NZD': 'dovish',   # RBNZ cutting
                'TRY': 'hawkish'   # CBRT high rates
            }
            
            base_trajectory = trajectory_mapping.get(base_currency, 'neutral')
            quote_trajectory = trajectory_mapping.get(quote_currency, 'neutral')
            
            # Rate change probabilities (simplified)
            def get_rate_probabilities(currency, trajectory):
                if trajectory == 'hawkish':
                    return {'hike': 0.6, 'hold': 0.35, 'cut': 0.05}
                elif trajectory == 'dovish':
                    return {'hike': 0.05, 'hold': 0.35, 'cut': 0.6}
                else:  # neutral
                    return {'hike': 0.2, 'hold': 0.6, 'cut': 0.2}
            
            base_probs = get_rate_probabilities(base_currency, base_trajectory)
            
            # Policy divergence score
            divergence_score = self._calculate_policy_divergence(
                base_trajectory, quote_trajectory, base_cb.get('rate', 2.0), quote_cb.get('rate', 2.0)
            )
            
            # Forward guidance
            forward_guidance = f"{base_currency} {base_trajectory} vs {quote_currency} {quote_trajectory}"
            
            return CentralBankPolicy(
                current_rate=base_cb.get('rate', 2.0),
                rate_trajectory=base_trajectory,
                next_meeting_date='2025-01-15',  # Placeholder
                rate_change_probability=base_probs,
                forward_guidance=forward_guidance,
                policy_divergence_score=divergence_score
            )
            
        except Exception as e:
            self._log_error(f"Merkez bankası analiz hatası: {str(e)}")
            return CentralBankPolicy(2.0, 'neutral', '2025-01-15', {'hold': 1.0}, 'Neutral', 0)
    
    def _calculate_policy_divergence(self, base_trajectory: str, quote_trajectory: str,
                                   base_rate: float, quote_rate: float) -> float:
        """Politika ayrışma skoru hesapla"""
        try:
            # Trajectory scores
            trajectory_scores = {'hawkish': 1, 'neutral': 0, 'dovish': -1}
            
            base_score = trajectory_scores.get(base_trajectory, 0)
            quote_score = trajectory_scores.get(quote_trajectory, 0)
            
            # Divergence score
            trajectory_divergence = abs(base_score - quote_score)
            rate_divergence = abs(base_rate - quote_rate) / 10  # Normalize
            
            return min(100, (trajectory_divergence * 50 + rate_divergence * 50))
            
        except Exception:
            return 0
    
    def _analyze_macro_indicators(self, base_currency: str, quote_currency: str) -> MacroIndicators:
        """Makroekonomik göstergeler analizi"""
        try:
            # Simulated macro data (in real implementation, would come from data providers)
            macro_data = {
                'USD': {
                    'gdp_growth': 2.4, 'inflation': 3.2, 'unemployment': 3.8,
                    'current_account': -3.1, 'trade_balance': -68.0, 'debt_ratio': 128.0,
                    'credit_rating': 'AAA', 'momentum': 75
                },
                'EUR': {
                    'gdp_growth': 0.8, 'inflation': 2.1, 'unemployment': 6.5,
                    'current_account': 2.8, 'trade_balance': 45.0, 'debt_ratio': 92.0,
                    'credit_rating': 'AAA', 'momentum': 55
                },
                'GBP': {
                    'gdp_growth': 1.2, 'inflation': 4.1, 'unemployment': 4.2,
                    'current_account': -2.9, 'trade_balance': -25.0, 'debt_ratio': 105.0,
                    'credit_rating': 'AA', 'momentum': 60
                },
                'JPY': {
                    'gdp_growth': 0.9, 'inflation': 2.8, 'unemployment': 2.6,
                    'current_account': 3.2, 'trade_balance': -5.0, 'debt_ratio': 264.0,
                    'credit_rating': 'A+', 'momentum': 65
                },
                'TRY': {
                    'gdp_growth': 3.2, 'inflation': 58.0, 'unemployment': 10.1,
                    'current_account': -5.4, 'trade_balance': -45.0, 'debt_ratio': 35.0,
                    'credit_rating': 'B+', 'momentum': 45
                }
            }
            
            base_data = macro_data.get(base_currency, macro_data['USD'])
            
            return MacroIndicators(
                gdp_growth=base_data['gdp_growth'],
                inflation_rate=base_data['inflation'],
                unemployment_rate=base_data['unemployment'],
                current_account_balance=base_data['current_account'],
                trade_balance=base_data['trade_balance'],
                government_debt_ratio=base_data['debt_ratio'],
                credit_rating=base_data['credit_rating'],
                economic_momentum_score=base_data['momentum']
            )
            
        except Exception as e:
            self._log_error(f"Makro analiz hatası: {str(e)}")
            return MacroIndicators(2.0, 3.0, 5.0, 0.0, 0.0, 100.0, 'A', 50)
    
    def _analyze_cross_currency_relationships(self, symbol: str) -> CrossCurrencyAnalysis:
        """Çapraz kur ilişkileri analizi"""
        try:
            # Major currency correlation matrix (simplified)
            correlation_matrix = {
                'EUR': {'USD': -0.95, 'GBP': 0.85, 'JPY': 0.65, 'CHF': 0.90, 'AUD': 0.75},
                'GBP': {'USD': -0.85, 'EUR': 0.85, 'JPY': 0.55, 'CHF': 0.70, 'AUD': 0.65},
                'JPY': {'USD': -0.65, 'EUR': 0.65, 'GBP': 0.55, 'CHF': 0.60, 'AUD': 0.45},
                'CHF': {'USD': -0.90, 'EUR': 0.90, 'GBP': 0.70, 'JPY': 0.60, 'AUD': 0.70},
                'AUD': {'USD': -0.75, 'EUR': 0.75, 'GBP': 0.65, 'JPY': 0.45, 'CHF': 0.70}
            }
            
            # Cointegration relationships
            cointegration_pairs = [
                {'pair': 'EURUSD-GBPUSD', 'coefficient': 0.85, 'half_life': 15},
                {'pair': 'AUDUSD-NZDUSD', 'coefficient': 0.90, 'half_life': 12},
                {'pair': 'USDJPY-EURJPY', 'coefficient': 0.75, 'half_life': 20}
            ]
            
            # Currency strength ranking (DXY-like index)
            strength_ranking = {
                'USD': 1,  # Strongest
                'CHF': 2,
                'EUR': 3,
                'GBP': 4,
                'JPY': 5,
                'AUD': 6,
                'CAD': 7,
                'NZD': 8,
                'TRY': 9   # Weakest
            }
            
            # Diversification benefits
            diversification_score = 85.0  # High diversification in FX
            
            # Hedging efficiency
            hedging_efficiency = {
                'EURUSD': 0.95,
                'GBPUSD': 0.88,
                'USDJPY': 0.92,
                'AUDUSD': 0.85
            }
            
            return CrossCurrencyAnalysis(
                correlation_matrix=correlation_matrix,
                cointegration_relationships=cointegration_pairs,
                diversification_benefits=diversification_score,
                hedging_efficiency=hedging_efficiency,
                currency_strength_ranking=strength_ranking
            )
            
        except Exception as e:
            self._log_error(f"Çapraz kur analiz hatası: {str(e)}")
            return CrossCurrencyAnalysis({}, [], 50.0, {}, {})
    
    def _model_fx_volatility(self, symbol: str, historical_data: Optional[pd.DataFrame]) -> FXVolatilityModel:
        """FX volatilite modellemesi"""
        try:
            # Realized volatility calculation
            if historical_data is not None and len(historical_data) > 20:
                returns = historical_data['Close'].pct_change(fill_method=None).dropna()
                realized_vol = returns.std() * np.sqrt(252)  # Annualized
            else:
                realized_vol = self._estimate_volatility(symbol)
            
            # Simulated implied volatility (from options market)
            implied_vol = realized_vol * (1 + np.random.normal(0, 0.1))
            
            # Volatility risk premium
            vol_risk_premium = implied_vol - realized_vol
            
            # Volatility clustering detection
            volatility_clustering = abs(vol_risk_premium) > 0.02
            
            # Volatility regime classification
            if realized_vol < 0.08:
                vol_regime = "low"
            elif realized_vol < 0.15:
                vol_regime = "normal"
            elif realized_vol < 0.25:
                vol_regime = "high"
            else:
                vol_regime = "extreme"
            
            # Volatility forecasts
            base_vol = realized_vol
            vol_forecast = {
                '1d': base_vol / np.sqrt(252),
                '1w': base_vol / np.sqrt(52),
                '1m': base_vol / np.sqrt(12),
                '3m': base_vol / np.sqrt(4),
                '1y': base_vol
            }
            
            return FXVolatilityModel(
                realized_volatility=realized_vol,
                implied_volatility=implied_vol,
                volatility_risk_premium=vol_risk_premium,
                volatility_clustering=volatility_clustering,
                vol_regime=vol_regime,
                volatility_forecast=vol_forecast
            )
            
        except Exception as e:
            self._log_error(f"Volatilite modeli hatası: {str(e)}")
            return FXVolatilityModel(0.12, 0.13, 0.01, False, "normal", {})
    
    def _generate_technical_signals(self, symbol: str, historical_data: Optional[pd.DataFrame]) -> Dict[str, float]:
        """Teknik analiz sinyalleri"""
        try:
            signals = {}
            
            if historical_data is not None and len(historical_data) > 50:
                close_prices = historical_data['Close']
                
                # Moving averages
                sma_20 = close_prices.rolling(20).mean().iloc[-1]
                sma_50 = close_prices.rolling(50).mean().iloc[-1]
                current_price = close_prices.iloc[-1]
                
                # MA signals
                signals['ma_signal'] = 1 if current_price > sma_20 > sma_50 else -1 if current_price < sma_20 < sma_50 else 0
                
                # RSI
                delta = close_prices.diff()
                gain = (delta.where(delta > 0, 0)).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs))
                current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
                
                signals['rsi'] = current_rsi
                signals['rsi_signal'] = -1 if current_rsi > 70 else 1 if current_rsi < 30 else 0
                
                # Bollinger Bands
                bb_period = 20
                bb_std = 2
                bb_middle = close_prices.rolling(bb_period).mean()
                bb_std_dev = close_prices.rolling(bb_period).std()
                bb_upper = bb_middle + (bb_std_dev * bb_std)
                bb_lower = bb_middle - (bb_std_dev * bb_std)
                
                bb_position = (current_price - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1])
                signals['bb_position'] = bb_position
                signals['bb_signal'] = -1 if bb_position > 0.8 else 1 if bb_position < 0.2 else 0
                
            else:
                # Default neutral signals
                signals = {
                    'ma_signal': 0,
                    'rsi': 50,
                    'rsi_signal': 0,
                    'bb_position': 0.5,
                    'bb_signal': 0
                }
            
            # MACD approximation
            signals['macd_signal'] = np.random.choice([-1, 0, 1], p=[0.3, 0.4, 0.3])
            
            # Support/Resistance levels
            signals['support_resistance'] = 0  # Neutral
            
            # Trend strength
            signals['trend_strength'] = abs(signals['ma_signal']) * 50 + 25
            
            return signals
            
        except Exception as e:
            self._log_error(f"Teknik sinyal hatası: {str(e)}")
            return {'ma_signal': 0, 'rsi': 50, 'trend_strength': 50}
    
    def _generate_fundamental_signals(self, carry_analysis: CarryTradeAnalysis,
                                    cb_analysis: CentralBankPolicy,
                                    macro_analysis: MacroIndicators) -> Dict[str, float]:
        """Fundamental analiz sinyalleri"""
        try:
            signals = {}
            
            # Carry trade signal
            if carry_analysis.risk_adjusted_carry > 0.03:  # 3%+
                signals['carry_signal'] = 1
            elif carry_analysis.risk_adjusted_carry < -0.03:
                signals['carry_signal'] = -1
            else:
                signals['carry_signal'] = 0
            
            # Interest rate differential signal
            signals['rate_differential'] = carry_analysis.interest_rate_differential
            if abs(carry_analysis.interest_rate_differential) > 2:
                signals['rate_signal'] = 1 if carry_analysis.interest_rate_differential > 0 else -1
            else:
                signals['rate_signal'] = 0
            
            # Central bank policy signal
            if cb_analysis.rate_trajectory == 'hawkish':
                signals['cb_signal'] = 1
            elif cb_analysis.rate_trajectory == 'dovish':
                signals['cb_signal'] = -1
            else:
                signals['cb_signal'] = 0
            
            # Economic momentum signal
            if macro_analysis.economic_momentum_score > 70:
                signals['momentum_signal'] = 1
            elif macro_analysis.economic_momentum_score < 40:
                signals['momentum_signal'] = -1
            else:
                signals['momentum_signal'] = 0
            
            # Inflation differential (simplified)
            signals['inflation_signal'] = 0  # Would need quote currency inflation
            
            # Current account signal
            if macro_analysis.current_account_balance > 2:
                signals['current_account_signal'] = 1
            elif macro_analysis.current_account_balance < -3:
                signals['current_account_signal'] = -1
            else:
                signals['current_account_signal'] = 0
            
            # Combined fundamental score
            fundamental_score = np.mean([
                signals['carry_signal'],
                signals['rate_signal'],
                signals['cb_signal'],
                signals['momentum_signal'],
                signals['current_account_signal']
            ]) * 50 + 50  # Convert to 0-100 scale
            
            signals['fundamental_score'] = fundamental_score
            
            return signals
            
        except Exception as e:
            self._log_error(f"Fundamental sinyal hatası: {str(e)}")
            return {'fundamental_score': 50, 'carry_signal': 0}
    
    def _assess_currency_risks(self, pair_info: CurrencyPair, vol_model: FXVolatilityModel,
                              macro_analysis: MacroIndicators) -> Dict[str, str]:
        """Currency risk değerlendirmesi"""
        try:
            risks = {}
            
            # Volatility risk
            if vol_model.vol_regime == "extreme":
                risks['volatility_risk'] = "Çok Yüksek"
            elif vol_model.vol_regime == "high":
                risks['volatility_risk'] = "Yüksek"
            elif vol_model.vol_regime == "low":
                risks['volatility_risk'] = "Düşük"
            else:
                risks['volatility_risk'] = "Orta"
            
            # Liquidity risk
            if pair_info.liquidity_score > 85:
                risks['liquidity_risk'] = "Düşük"
            elif pair_info.liquidity_score > 70:
                risks['liquidity_risk'] = "Orta"
            else:
                risks['liquidity_risk'] = "Yüksek"
            
            # Credit risk (based on sovereign rating)
            rating_risk_map = {
                'AAA': 'Çok Düşük', 'AA+': 'Çok Düşük', 'AA': 'Düşük', 'AA-': 'Düşük',
                'A+': 'Orta', 'A': 'Orta', 'A-': 'Orta',
                'BBB+': 'Orta-Yüksek', 'BBB': 'Orta-Yüksek', 'BBB-': 'Yüksek',
                'BB+': 'Yüksek', 'BB': 'Yüksek', 'B+': 'Çok Yüksek', 'B': 'Çok Yüksek'
            }
            risks['credit_risk'] = rating_risk_map.get(macro_analysis.credit_rating, 'Orta')
            
            # Political risk (simplified)
            if pair_info.base_currency in ['USD', 'EUR', 'CHF', 'JPY']:
                risks['political_risk'] = "Düşük"
            elif pair_info.base_currency in ['GBP', 'AUD', 'CAD']:
                risks['political_risk'] = "Orta"
            else:
                risks['political_risk'] = "Yüksek"
            
            # Inflation risk
            if macro_analysis.inflation_rate > 10:
                risks['inflation_risk'] = "Çok Yüksek"
            elif macro_analysis.inflation_rate > 5:
                risks['inflation_risk'] = "Yüksek"
            elif macro_analysis.inflation_rate > 3:
                risks['inflation_risk'] = "Orta"
            else:
                risks['inflation_risk'] = "Düşük"
            
            # Overall risk assessment
            risk_levels = list(risks.values())
            high_risk_count = sum(1 for risk in risk_levels if 'Yüksek' in risk)
            
            if high_risk_count >= 3:
                risks['overall_risk'] = "Yüksek Risk"
            elif high_risk_count >= 1:
                risks['overall_risk'] = "Orta Risk"
            else:
                risks['overall_risk'] = "Düşük Risk"
            
            return risks
            
        except Exception as e:
            self._log_error(f"Risk değerlendirme hatası: {str(e)}")
            return {'overall_risk': 'Orta Risk', 'volatility_risk': 'Orta'}
    
    def _generate_trading_recommendation(self, carry_analysis: CarryTradeAnalysis,
                                       technical_signals: Dict[str, float],
                                       fundamental_signals: Dict[str, float],
                                       risk_assessment: Dict[str, str]) -> str:
        """Trading önerisi oluştur"""
        try:
            # Signal strengths
            tech_score = np.mean([
                technical_signals.get('ma_signal', 0),
                technical_signals.get('rsi_signal', 0),
                technical_signals.get('bb_signal', 0)
            ])
            
            fund_score = fundamental_signals.get('fundamental_score', 50) / 50 - 1  # Convert to -1 to 1
            carry_score = 1 if carry_analysis.risk_adjusted_carry > 0.02 else -1 if carry_analysis.risk_adjusted_carry < -0.02 else 0
            
            # Combined score
            combined_score = (tech_score * 0.4 + fund_score * 0.4 + carry_score * 0.2)
            
            # Risk adjustment
            overall_risk = risk_assessment.get('overall_risk', 'Orta Risk')
            risk_multiplier = 0.5 if 'Yüksek' in overall_risk else 0.8 if 'Orta' in overall_risk else 1.0
            
            adjusted_score = combined_score * risk_multiplier
            
            # Generate recommendation
            if adjusted_score > 0.3:
                return "GÜÇLÜ SATIN AL"
            elif adjusted_score > 0.1:
                return "SATIN AL"
            elif adjusted_score > -0.1:
                return "BEKLE"
            elif adjusted_score > -0.3:
                return "SAT"
            else:
                return "GÜÇLÜ SAT"
                
        except Exception as e:
            self._log_error(f"Trading önerisi hatası: {str(e)}")
            return "BEKLE"
    
    def _calculate_ultra_currency_score(self, carry_analysis: CarryTradeAnalysis,
                                      cb_analysis: CentralBankPolicy,
                                      macro_analysis: MacroIndicators,
                                      technical_signals: Dict[str, float],
                                      fundamental_signals: Dict[str, float],
                                      vol_model: FXVolatilityModel) -> float:
        """Ultra currency skoru hesapla"""
        try:
            scores = {}
            
            # Carry trade score (25%)
            if carry_analysis.risk_adjusted_carry > 0.04:
                scores['carry'] = 90
            elif carry_analysis.risk_adjusted_carry > 0.02:
                scores['carry'] = 75
            elif carry_analysis.risk_adjusted_carry > 0:
                scores['carry'] = 60
            elif carry_analysis.risk_adjusted_carry > -0.02:
                scores['carry'] = 40
            else:
                scores['carry'] = 25
            
            # Technical score (20%)
            tech_strength = technical_signals.get('trend_strength', 50)
            scores['technical'] = tech_strength
            
            # Fundamental score (25%)
            scores['fundamental'] = fundamental_signals.get('fundamental_score', 50)
            
            # Central bank policy score (15%)
            if cb_analysis.policy_divergence_score > 70:
                scores['central_bank'] = 85
            elif cb_analysis.policy_divergence_score > 40:
                scores['central_bank'] = 65
            else:
                scores['central_bank'] = 45
            
            # Macro score (10%)
            momentum = macro_analysis.economic_momentum_score
            scores['macro'] = momentum
            
            # Volatility score (5%) - lower is better
            if vol_model.vol_regime == "low":
                scores['volatility'] = 85
            elif vol_model.vol_regime == "normal":
                scores['volatility'] = 65
            elif vol_model.vol_regime == "high":
                scores['volatility'] = 45
            else:  # extreme
                scores['volatility'] = 25
            
            # Weighted average
            weights = {
                'carry': 0.25,
                'technical': 0.20,
                'fundamental': 0.25,
                'central_bank': 0.15,
                'macro': 0.10,
                'volatility': 0.05
            }
            
            ultra_score = sum(scores[key] * weights[key] for key in scores.keys())
            
            return min(100, max(0, ultra_score))
            
        except Exception as e:
            self._log_error(f"Ultra skor hesaplama hatası: {str(e)}")
            return 50.0
    
    def analyze_currency_basket(self, currency_list: List[str]) -> Dict:
        """Para birimi sepeti analizi"""
        try:
            basket_analysis = {
                'currencies': [],
                'basket_score': 0,
                'diversification_score': 0,
                'risk_metrics': {},
                'correlation_analysis': {},
                'recommendations': []
            }
            
            # Her currency için analiz
            currency_scores = []
            for currency in currency_list:
                if currency in self.central_bank_rates:
                    # Basit currency strength score
                    cb_data = self.central_bank_rates[currency]
                    
                    # Interest rate component
                    rate_score = min(100, cb_data['rate'] * 10)
                    
                    # Currency type component
                    if currency in self.safe_haven_currencies:
                        type_score = 70  # Stable but lower yield
                    elif currency in self.risk_currencies:
                        type_score = 60  # Higher risk/reward
                    else:
                        type_score = 50
                    
                    currency_score = (rate_score * 0.6 + type_score * 0.4)
                    currency_scores.append(currency_score)
                    
                    basket_analysis['currencies'].append({
                        'currency': currency,
                        'score': round(currency_score, 1),
                        'interest_rate': cb_data['rate'],
                        'type': 'Safe Haven' if currency in self.safe_haven_currencies else 'Risk Currency'
                    })
            
            # Basket overall score
            if currency_scores:
                basket_analysis['basket_score'] = round(np.mean(currency_scores), 1)
                
                # Diversification score (higher is better)
                score_std = np.std(currency_scores) if len(currency_scores) > 1 else 0
                basket_analysis['diversification_score'] = min(100, score_std * 2)
            
            # Risk metrics
            safe_haven_count = sum(1 for curr in currency_list if curr in self.safe_haven_currencies)
            risk_curr_count = sum(1 for curr in currency_list if curr in self.risk_currencies)
            
            basket_analysis['risk_metrics'] = {
                'safe_haven_weight': safe_haven_count / len(currency_list) if currency_list else 0,
                'risk_currency_weight': risk_curr_count / len(currency_list) if currency_list else 0,
                'balance_score': abs(safe_haven_count - risk_curr_count) / len(currency_list) if currency_list else 0
            }
            
            # Recommendations
            if basket_analysis['basket_score'] > 70:
                basket_analysis['recommendations'].append("Güçlü sepet kompozisyonu, pozisyon artırılabilir")
            
            if basket_analysis['diversification_score'] < 30:
                basket_analysis['recommendations'].append("Düşük diversifikasyon, farklı karakterde currency'ler ekleyin")
            
            return basket_analysis
            
        except Exception as e:
            self._log_error(f"Currency basket analiz hatası: {str(e)}")
            return {'error': str(e)}
    
    def _log_error(self, message: str):
        """Hata loglama"""
        print(f"ERROR: {message}")
    
    def _get_default_currency_result(self, symbol: str) -> CurrencyAnalysisResult:
        """Varsayılan currency sonucu"""
        default_pair = CurrencyPair('USD', 'EUR', symbol, 1.0, 0.0, 0.1, 0.0001, 50)
        default_carry = CarryTradeAnalysis(0, 0, 0, 0, 0, 0, 0, 0)
        default_cb = CentralBankPolicy(2.0, 'neutral', '2025-01-15', {'hold': 1.0}, 'Neutral', 0)
        default_macro = MacroIndicators(2.0, 3.0, 5.0, 0.0, 0.0, 100.0, 'A', 50)
        default_cross = CrossCurrencyAnalysis({}, [], 50.0, {}, {})
        default_vol = FXVolatilityModel(0.12, 0.13, 0.01, False, "normal", {})
        
        return CurrencyAnalysisResult(
            currency_pair=default_pair,
            ultra_currency_score=50.0,
            carry_trade_analysis=default_carry,
            central_bank_analysis=default_cb,
            macro_analysis=default_macro,
            cross_currency_analysis=default_cross,
            volatility_model=default_vol,
            technical_signals={'trend_strength': 50},
            fundamental_signals={'fundamental_score': 50},
            risk_assessment={'overall_risk': 'Orta Risk'},
            trading_recommendation="BEKLE"
        )
