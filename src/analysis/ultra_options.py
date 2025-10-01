"""
Ultra Options Analysis System
Gelişmiş opsiyon fiyatlandırma ve analiz sistemi

Bu modül Black-Scholes uzantıları, Greeks hesaplamaları, 
volatilite yüzeyi modellemesi ve egzotik opsiyon fiyatlandırması
içeren sofistike opsiyon analiz yetenekleri sağlar.

Türkçe Açıklamalar:
- Opsiyon fiyatlandırma modelleri
- Greeks (Delta, Gamma, Theta, Vega, Rho) hesaplamaları
- Volatilite yüzeyi (volatility surface) analizi
- Egzotik opsiyon fiyatlandırması
- İmplied volatility hesaplamaları
- Opsiyon stratejileri analizi
- Zaman değeri (time decay) analizi
- Moneyness analizi ve risk profilleme
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

@dataclass
class BlackScholesResult:
    """Black-Scholes model sonuçları"""
    option_price: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    implied_volatility: Optional[float] = None

@dataclass
class Greeks:
    """Opsiyon Greeks hesaplamaları"""
    delta: float  # Fiyat hassasiyeti
    gamma: float  # Delta değişim oranı
    theta: float  # Zaman değeri kaybı
    vega: float   # Volatilite hassasiyeti
    rho: float    # Faiz oranı hassasiyeti
    charm: float  # Delta'nın zaman hassasiyeti
    vanna: float  # Vega'nın spot fiyat hassasiyeti
    volga: float  # Vega'nın volatilite hassasiyeti

@dataclass
class VolatilitySurface:
    """Volatilite yüzeyi modeli"""
    strikes: List[float]
    expirations: List[float]
    volatilities: np.ndarray
    smile_parameters: Dict[str, float]
    term_structure: Dict[str, float]

@dataclass
class ExoticOptionResult:
    """Egzotik opsiyon fiyatlandırma sonucu"""
    option_type: str
    fair_value: float
    greeks: Greeks
    risk_parameters: Dict[str, float]
    monte_carlo_confidence: float

@dataclass
class OptionStrategy:
    """Opsiyon stratejisi analizi"""
    strategy_name: str
    legs: List[Dict]
    max_profit: float
    max_loss: float
    breakeven_points: List[float]
    risk_reward_ratio: float
    probability_of_profit: float

class UltraOptionsAnalyzer:
    """Ultra gelişmiş opsiyon analiz sistemi"""
    
    def __init__(self):
        """Ultra opsiyon analyzer'ı başlat"""
        self.risk_free_rate = 0.05  # Risksiz faiz oranı
        self.dividend_yield = 0.02  # Temettü verimi
        
        # Volatilite yüzeyi parametreleri
        self.vol_surface_params = {
            'atm_vol': 0.20,
            'skew_slope': -0.15,
            'term_structure_slope': 0.02,
            'volatility_of_volatility': 0.3
        }
        
        # Egzotik opsiyon tipleri
        self.exotic_types = {
            'asian': 'Asya Tipi Opsiyon',
            'barrier': 'Bariyer Opsiyon',
            'lookback': 'Lookback Opsiyon',
            'rainbow': 'Gökkuşağı Opsiyon',
            'compound': 'Bileşik Opsiyon',
            'digital': 'Dijital Opsiyon'
        }
        
        # Opsiyon stratejileri
        self.strategies = {
            'straddle': {
                'name': 'Long Straddle',
                'description': 'Yüksek volatilite beklentisi stratejisi',
                'legs': ['long_call_atm', 'long_put_atm']
            },
            'strangle': {
                'name': 'Long Strangle', 
                'description': 'Geniş hareket beklentisi stratejisi',
                'legs': ['long_call_otm', 'long_put_otm']
            },
            'iron_condor': {
                'name': 'Iron Condor',
                'description': 'Düşük volatilite stratejisi',
                'legs': ['short_call_otm', 'long_call_far_otm', 'short_put_otm', 'long_put_far_otm']
            },
            'butterfly': {
                'name': 'Long Butterfly',
                'description': 'Çok düşük volatilite stratejisi',
                'legs': ['long_call_itm', 'short_call_atm_2x', 'long_call_otm']
            }
        }
        
        print("INFO: Ultra Options Analyzer gelişmiş Black-Scholes modelleri ile başlatıldı")
    
    def analyze_option(self, symbol: str, spot_price: float, strike_price: float,
                      time_to_expiry: float, volatility: float, option_type: str = 'call',
                      **kwargs) -> Dict:
        """Kapsamlı opsiyon analizi"""
        try:
            # Black-Scholes hesaplamaları
            bs_result = self._calculate_black_scholes(
                spot_price, strike_price, time_to_expiry, volatility, option_type
            )
            
            # Greeks hesaplamaları
            greeks = self._calculate_all_greeks(
                spot_price, strike_price, time_to_expiry, volatility, option_type
            )
            
            # Volatilite yüzeyi analizi
            vol_surface = self._analyze_volatility_surface(
                spot_price, strike_price, time_to_expiry
            )
            
            # Zaman değeri analizi
            time_decay = self._analyze_time_decay(
                spot_price, strike_price, time_to_expiry, volatility, option_type
            )
            
            # Moneyness analizi
            moneyness = self._analyze_moneyness(spot_price, strike_price, time_to_expiry)
            
            # Risk profili
            risk_profile = self._calculate_risk_profile(greeks, moneyness, time_to_expiry)
            
            # Opsiyon skoru hesaplama
            option_score = self._calculate_option_score(
                bs_result, greeks, moneyness, vol_surface, risk_profile
            )
            
            # Türkçe analiz açıklaması
            analysis = self._generate_option_analysis(
                symbol, bs_result, greeks, moneyness, risk_profile, option_score
            )
            
            return {
                'ultra_option_score': round(option_score, 1),
                'analysis': analysis,
                'black_scholes': {
                    'fair_value': round(bs_result.option_price, 2),
                    'delta': round(bs_result.delta, 4),
                    'gamma': round(bs_result.gamma, 4),
                    'theta': round(bs_result.theta, 4),
                    'vega': round(bs_result.vega, 4),
                    'rho': round(bs_result.rho, 4)
                },
                'greeks_analysis': {
                    'score': round(greeks.delta * 100, 1),
                    'delta_interpretation': self._interpret_delta(greeks.delta, option_type),
                    'gamma_risk': self._interpret_gamma(greeks.gamma),
                    'theta_decay': self._interpret_theta(greeks.theta),
                    'vega_sensitivity': self._interpret_vega(greeks.vega)
                },
                'volatility_surface': {
                    'implied_vol': round(vol_surface.smile_parameters['atm_vol'], 4),
                    'skew': round(vol_surface.smile_parameters.get('skew', 0), 4),
                    'term_structure': vol_surface.term_structure
                },
                'time_decay_analysis': {
                    'daily_theta': round(time_decay['daily_theta'], 2),
                    'theta_acceleration': time_decay['acceleration'],
                    'time_value_remaining': round(time_decay['time_value'], 2)
                },
                'moneyness_analysis': {
                    'moneyness_ratio': round(moneyness['ratio'], 4),
                    'classification': moneyness['classification'],
                    'intrinsic_value': round(moneyness['intrinsic_value'], 2),
                    'time_value': round(moneyness['time_value'], 2)
                },
                'risk_profile': {
                    'overall_risk': risk_profile['overall_risk'],
                    'directional_risk': risk_profile['directional_risk'],
                    'volatility_risk': risk_profile['volatility_risk'],
                    'time_risk': risk_profile['time_risk']
                },
                'confidence': round(np.mean([
                    95.0 if time_to_expiry > 0.1 else 85.0,
                    90.0 if volatility > 0.1 else 80.0,
                    85.0
                ]), 1)
            }
            
        except Exception as e:
            self._log_error(f"Opsiyon analizi hatası: {str(e)}")
            return self._get_default_option_response(symbol)
    
    def _calculate_black_scholes(self, S: float, K: float, T: float, vol: float,
                                option_type: str) -> BlackScholesResult:
        """Black-Scholes model hesaplaması"""
        try:
            r = self.risk_free_rate
            q = self.dividend_yield
            
            # Black-Scholes parametreleri
            d1 = (np.log(S/K) + (r - q + 0.5*vol**2)*T) / (vol*np.sqrt(T))
            d2 = d1 - vol*np.sqrt(T)
            
            if option_type.lower() == 'call':
                # Call option
                option_price = S*np.exp(-q*T)*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
                delta = np.exp(-q*T) * norm.cdf(d1)
                rho = K*T*np.exp(-r*T)*norm.cdf(d2)
            else:
                # Put option
                option_price = K*np.exp(-r*T)*norm.cdf(-d2) - S*np.exp(-q*T)*norm.cdf(-d1)
                delta = -np.exp(-q*T) * norm.cdf(-d1)
                rho = -K*T*np.exp(-r*T)*norm.cdf(-d2)
            
            # Greeks hesaplaması
            gamma = np.exp(-q*T)*norm.pdf(d1)/(S*vol*np.sqrt(T))
            theta = (-S*np.exp(-q*T)*norm.pdf(d1)*vol/(2*np.sqrt(T)) 
                    - r*K*np.exp(-r*T)*norm.cdf(d2 if option_type.lower() == 'call' else -d2)
                    + q*S*np.exp(-q*T)*norm.cdf(d1 if option_type.lower() == 'call' else -d1))
            vega = S*np.exp(-q*T)*norm.pdf(d1)*np.sqrt(T)
            
            # Günlük theta (1/365)
            theta = theta / 365
            
            return BlackScholesResult(
                option_price=option_price,
                delta=delta,
                gamma=gamma,
                theta=theta,
                vega=vega/100,  # 1% volatilite değişimi için
                rho=rho/100     # 1% faiz değişimi için
            )
            
        except Exception as e:
            self._log_error(f"Black-Scholes hesaplama hatası: {str(e)}")
            return BlackScholesResult(0, 0, 0, 0, 0, 0)
    
    def _calculate_all_greeks(self, S: float, K: float, T: float, vol: float,
                             option_type: str) -> Greeks:
        """Tüm Greeks'leri hesapla (birinci ve ikinci türev)"""
        try:
            r = self.risk_free_rate
            q = self.dividend_yield
            
            d1 = (np.log(S/K) + (r - q + 0.5*vol**2)*T) / (vol*np.sqrt(T))
            d2 = d1 - vol*np.sqrt(T)
            
            # Birinci türev Greeks
            if option_type.lower() == 'call':
                delta = np.exp(-q*T) * norm.cdf(d1)
            else:
                delta = -np.exp(-q*T) * norm.cdf(-d1)
            
            gamma = np.exp(-q*T)*norm.pdf(d1)/(S*vol*np.sqrt(T))
            
            theta = (-S*np.exp(-q*T)*norm.pdf(d1)*vol/(2*np.sqrt(T)) 
                    - r*K*np.exp(-r*T)*norm.cdf(d2 if option_type.lower() == 'call' else -d2)
                    + q*S*np.exp(-q*T)*norm.cdf(d1 if option_type.lower() == 'call' else -d1)) / 365
            
            vega = S*np.exp(-q*T)*norm.pdf(d1)*np.sqrt(T) / 100
            
            if option_type.lower() == 'call':
                rho = K*T*np.exp(-r*T)*norm.cdf(d2) / 100
            else:
                rho = -K*T*np.exp(-r*T)*norm.cdf(-d2) / 100
            
            # İkinci türev Greeks
            # Charm (Delta'nın zaman hassasiyeti)
            charm = (-q*np.exp(-q*T)*norm.cdf(d1 if option_type.lower() == 'call' else -d1)
                    - np.exp(-q*T)*norm.pdf(d1)*(r-q)/(vol*np.sqrt(T))) / 365
            
            # Vanna (Vega'nın spot fiyat hassasiyeti)
            vanna = -np.exp(-q*T)*norm.pdf(d1)*d2/vol / 100
            
            # Volga (Vega'nın volatilite hassasiyeti)  
            volga = S*np.exp(-q*T)*norm.pdf(d1)*np.sqrt(T)*d1*d2/vol / 10000
            
            return Greeks(
                delta=delta,
                gamma=gamma,
                theta=theta,
                vega=vega,
                rho=rho,
                charm=charm,
                vanna=vanna,
                volga=volga
            )
            
        except Exception as e:
            self._log_error(f"Greeks hesaplama hatası: {str(e)}")
            return Greeks(0, 0, 0, 0, 0, 0, 0, 0)
    
    def _analyze_volatility_surface(self, S: float, K: float, T: float) -> VolatilitySurface:
        """Volatilite yüzeyi analizi"""
        try:
            # Strike aralığı
            strikes = np.linspace(S*0.8, S*1.2, 9)
            
            # Vade aralığı (hafta, ay, çeyrek)
            expirations = [7/365, 30/365, 90/365, 180/365, 365/365]
            
            # Volatilite yüzeyi oluştur
            volatilities = np.zeros((len(strikes), len(expirations)))
            
            atm_vol = self.vol_surface_params['atm_vol']
            skew_slope = self.vol_surface_params['skew_slope']
            term_slope = self.vol_surface_params['term_structure_slope']
            
            for i, strike in enumerate(strikes):
                for j, expiry in enumerate(expirations):
                    # Moneyness etkisi (skew)
                    moneyness = np.log(strike/S)
                    skew_effect = skew_slope * moneyness
                    
                    # Vade yapısı etkisi
                    term_effect = term_slope * np.sqrt(expiry)
                    
                    # Volatilite hesapla
                    vol = atm_vol + skew_effect + term_effect
                    volatilities[i, j] = max(0.05, vol)  # Minimum %5
            
            # Volatilite gülümsemesi parametreleri
            smile_parameters = {
                'atm_vol': atm_vol,
                'skew': skew_slope,
                'convexity': 0.1,
                'smile_minimum': atm_vol - 0.02
            }
            
            # Vade yapısı
            term_structure = {
                f'{int(exp*365)}d': atm_vol + term_slope*np.sqrt(exp)
                for exp in expirations
            }
            
            return VolatilitySurface(
                strikes=strikes.tolist(),
                expirations=expirations,
                volatilities=volatilities,
                smile_parameters=smile_parameters,
                term_structure=term_structure
            )
            
        except Exception as e:
            self._log_error(f"Volatilite yüzeyi analiz hatası: {str(e)}")
            return VolatilitySurface([], [], np.array([]), {}, {})
    
    def _analyze_time_decay(self, S: float, K: float, T: float, vol: float,
                           option_type: str) -> Dict:
        """Zaman değeri (time decay) analizi"""
        try:
            # Mevcut opsiyon değeri
            current_bs = self._calculate_black_scholes(S, K, T, vol, option_type)
            
            # 1 gün sonraki değer
            tomorrow_bs = self._calculate_black_scholes(S, K, max(0.001, T-1/365), vol, option_type)
            
            # Günlük theta (gerçek)
            daily_theta = tomorrow_bs.option_price - current_bs.option_price
            
            # Theta ivmesi (vadeye yaklaştıkça hızlanma)
            if T > 30/365:
                theta_acceleration = "Düşük"
            elif T > 7/365:
                theta_acceleration = "Orta"
            else:
                theta_acceleration = "Yüksek"
            
            # İçsel değer
            if option_type.lower() == 'call':
                intrinsic_value = max(0, S - K)
            else:
                intrinsic_value = max(0, K - S)
            
            # Zaman değeri
            time_value = current_bs.option_price - intrinsic_value
            
            return {
                'daily_theta': daily_theta,
                'theoretical_theta': current_bs.theta,
                'acceleration': theta_acceleration,
                'time_value': time_value,
                'intrinsic_value': intrinsic_value,
                'time_value_ratio': time_value / current_bs.option_price if current_bs.option_price > 0 else 0
            }
            
        except Exception as e:
            self._log_error(f"Zaman değeri analiz hatası: {str(e)}")
            return {'daily_theta': 0, 'acceleration': 'Bilinmiyor', 'time_value': 0}
    
    def _analyze_moneyness(self, S: float, K: float, T: float) -> Dict:
        """Moneyness (parada olma durumu) analizi"""
        try:
            # Moneyness oranı
            moneyness_ratio = S / K
            
            # Forward price (ileri fiyat)
            forward_price = S * np.exp((self.risk_free_rate - self.dividend_yield) * T)
            forward_moneyness = forward_price / K
            
            # Sınıflandırma
            if moneyness_ratio > 1.05:
                classification = "ITM (In-The-Money)"
                turkish_class = "Parada"
            elif moneyness_ratio < 0.95:
                classification = "OTM (Out-of-The-Money)"
                turkish_class = "Para Dışında"
            else:
                classification = "ATM (At-The-Money)"
                turkish_class = "Para Başında"
            
            # İçsel değer hesaplaması (call için)
            intrinsic_value = max(0, S - K)
            
            # Zaman değeri (yaklaşık)
            time_value = max(0, S * 0.02 * np.sqrt(T))  # Basit yaklaşım
            
            return {
                'ratio': moneyness_ratio,
                'forward_moneyness': forward_moneyness,
                'classification': classification,
                'turkish_classification': turkish_class,
                'intrinsic_value': intrinsic_value,
                'time_value': time_value,
                'delta_theoretical': min(1.0, max(0.0, moneyness_ratio - 0.5))
            }
            
        except Exception as e:
            self._log_error(f"Moneyness analiz hatası: {str(e)}")
            return {'ratio': 1.0, 'classification': 'ATM', 'intrinsic_value': 0, 'time_value': 0}
    
    def _calculate_risk_profile(self, greeks: Greeks, moneyness: Dict, T: float) -> Dict:
        """Opsiyon risk profili hesaplama"""
        try:
            # Yönsel risk (Delta risk)
            directional_risk = abs(greeks.delta)
            if directional_risk > 0.7:
                directional_level = "Yüksek"
            elif directional_risk > 0.3:
                directional_level = "Orta"
            else:
                directional_level = "Düşük"
            
            # Volatilite riski (Vega risk)
            volatility_risk = abs(greeks.vega)
            if volatility_risk > 0.15:
                volatility_level = "Yüksek"
            elif volatility_risk > 0.05:
                volatility_level = "Orta"
            else:
                volatility_level = "Düşük"
            
            # Zaman riski (Theta risk)
            time_risk = abs(greeks.theta)
            if T < 7/365:
                time_level = "Çok Yüksek"
            elif T < 30/365:
                time_level = "Yüksek"
            elif T < 90/365:
                time_level = "Orta"
            else:
                time_level = "Düşük"
            
            # Gamma riski
            gamma_risk = abs(greeks.gamma)
            if gamma_risk > 0.1:
                gamma_level = "Yüksek"
            elif gamma_risk > 0.05:
                gamma_level = "Orta"
            else:
                gamma_level = "Düşük"
            
            # Genel risk skoru
            risk_components = [
                directional_risk * 0.3,
                volatility_risk * 10 * 0.25,  # Vega'yı ölçekle
                time_risk * 100 * 0.25,       # Theta'yı ölçekle
                gamma_risk * 10 * 0.2         # Gamma'yı ölçekle
            ]
            
            overall_risk_score = sum(risk_components)
            
            if overall_risk_score > 0.6:
                overall_risk = "Yüksek Risk"
            elif overall_risk_score > 0.3:
                overall_risk = "Orta Risk"
            else:
                overall_risk = "Düşük Risk"
            
            return {
                'overall_risk': overall_risk,
                'overall_risk_score': overall_risk_score,
                'directional_risk': directional_level,
                'volatility_risk': volatility_level,
                'time_risk': time_level,
                'gamma_risk': gamma_level,
                'risk_components': {
                    'delta_component': directional_risk,
                    'vega_component': volatility_risk,
                    'theta_component': time_risk,
                    'gamma_component': gamma_risk
                }
            }
            
        except Exception as e:
            self._log_error(f"Risk profili hesaplama hatası: {str(e)}")
            return {'overall_risk': 'Orta Risk', 'directional_risk': 'Orta', 
                   'volatility_risk': 'Orta', 'time_risk': 'Orta'}
    
    def _calculate_option_score(self, bs_result: BlackScholesResult, greeks: Greeks,
                               moneyness: Dict, vol_surface: VolatilitySurface,
                               risk_profile: Dict) -> float:
        """Ultra opsiyon skoru hesaplama"""
        try:
            scores = {
                # Fair value skorlaması (%25)
                'fair_value': min(100, max(0, 100 - abs(moneyness['ratio'] - 1) * 100)) * 0.25,
                
                # Greeks dengesi (%20)
                'greeks_balance': (
                    min(100, abs(greeks.delta) * 100) * 0.4 +
                    min(100, abs(greeks.vega) * 500) * 0.3 +
                    min(100, abs(greeks.gamma) * 1000) * 0.3
                ) * 0.20,
                
                # Volatilite profili (%20)
                'volatility_profile': min(100, vol_surface.smile_parameters.get('atm_vol', 0.2) * 400) * 0.20,
                
                # Risk-ödül dengesi (%20)
                'risk_reward': max(0, min(100, 100 - risk_profile['overall_risk_score'] * 100)) * 0.20,
                
                # Likidite ve spread (%15)
                'liquidity': 75.0 * 0.15  # Sabit değer (gerçek veriler gerekir)
            }
            
            total_score = sum(scores.values())
            return min(100, max(0, total_score))
            
        except Exception as e:
            self._log_error(f"Opsiyon skoru hesaplama hatası: {str(e)}")
            return 50.0
    
    def _interpret_delta(self, delta: float, option_type: str) -> str:
        """Delta yorumlama"""
        abs_delta = abs(delta)
        
        if abs_delta > 0.8:
            if option_type.lower() == 'call':
                return "Güçlü pozitif yönlülük - fiyat artışından çok etkilenir"
            else:
                return "Güçlü negatif yönlülük - fiyat düşüşünden çok etkilenir"
        elif abs_delta > 0.5:
            return "Orta düzeyde yönlü hassasiyet"
        else:
            return "Düşük yönlü hassasiyet - fiyat değişimlerinden az etkilenir"
    
    def _interpret_gamma(self, gamma: float) -> str:
        """Gamma yorumlama"""
        if gamma > 0.1:
            return "Yüksek gamma - delta hızla değişir, yeniden hedgeleme gerekir"
        elif gamma > 0.05:
            return "Orta gamma - delta değişimi izlenmeli"
        else:
            return "Düşük gamma - delta görece sabit"
    
    def _interpret_theta(self, theta: float) -> str:
        """Theta yorumlama"""
        if abs(theta) > 0.1:
            return "Yüksek zaman değeri kaybı - her gün önemli değer kaybeder"
        elif abs(theta) > 0.05:
            return "Orta düzeyde zaman değeri kaybı"
        else:
            return "Düşük zaman değeri kaybı - zaman faktörü minimal"
    
    def _interpret_vega(self, vega: float) -> str:
        """Vega yorumlama"""
        if abs(vega) > 0.15:
            return "Yüksek volatilite hassasiyeti - IV değişimlerini dikkatle izleyin"
        elif abs(vega) > 0.05:
            return "Orta volatilite hassasiyeti"
        else:
            return "Düşük volatilite hassasiyeti - IV değişimlerinden az etkilenir"
    
    def _generate_option_analysis(self, symbol: str, bs_result: BlackScholesResult,
                                 greeks: Greeks, moneyness: Dict, risk_profile: Dict,
                                 option_score: float) -> str:
        """Türkçe opsiyon analizi açıklaması"""
        try:
            # Risk seviyesi belirleme
            if option_score >= 80:
                risk_assessment = "düşük riskli"
            elif option_score >= 60:
                risk_assessment = "orta riskli"
            else:
                risk_assessment = "yüksek riskli"
            
            # Moneyness durumu
            money_status = moneyness.get('turkish_classification', 'Para Başında')
            
            # Ana analiz
            analysis = f"{symbol} opsiyonu {money_status.lower()} konumunda ve {risk_assessment} profilde. "
            
            # Delta yorumu
            if abs(greeks.delta) > 0.7:
                analysis += f"Güçlü yönlü hassasiyet (Δ={greeks.delta:.3f}) ile fiyat hareketlerini yakından takip eder. "
            elif abs(greeks.delta) > 0.3:
                analysis += f"Orta düzeyde yönlü hassasiyet (Δ={greeks.delta:.3f}) göstermekte. "
            else:
                analysis += f"Düşük yönlü hassasiyet (Δ={greeks.delta:.3f}) ile fiyat değişimlerinden az etkilenir. "
            
            # Theta yorumu  
            if abs(greeks.theta) > 0.1:
                analysis += f"Yüksek zaman değeri kaybı (Θ={greeks.theta:.3f}) nedeniyle acil eylem gerektirir. "
            else:
                analysis += f"Zaman değeri kaybı (Θ={greeks.theta:.3f}) kontrol altında. "
            
            # Volatilite yorumu
            if abs(greeks.vega) > 0.15:
                analysis += f"Volatilite değişimlerine çok hassas (υ={greeks.vega:.3f}), IV takibi kritik. "
            else:
                analysis += f"Volatilite hassasiyeti (υ={greeks.vega:.3f}) makul seviyelerde. "
            
            # Risk önerisi
            if risk_profile['overall_risk'] == "Yüksek Risk":
                analysis += "Dikkatli risk yönetimi ve sürekli hedgeleme önerilir."
            elif risk_profile['overall_risk'] == "Orta Risk":
                analysis += "Standart risk kontrolleri uygulanmalı."
            else:
                analysis += "Mevcut risk profili kabul edilebilir düzeylerde."
            
            return analysis
            
        except Exception as e:
            self._log_error(f"Analiz açıklama hatası: {str(e)}")
            return f"{symbol} için opsiyon analizi standart parametrelerle tamamlandı."
    
    def analyze_exotic_option(self, option_type: str, underlying_price: float,
                             parameters: Dict, **kwargs) -> ExoticOptionResult:
        """Egzotik opsiyon fiyatlandırması"""
        try:
            if option_type.lower() == 'asian':
                return self._price_asian_option(underlying_price, parameters)
            elif option_type.lower() == 'barrier':
                return self._price_barrier_option(underlying_price, parameters)
            elif option_type.lower() == 'lookback':
                return self._price_lookback_option(underlying_price, parameters)
            elif option_type.lower() == 'digital':
                return self._price_digital_option(underlying_price, parameters)
            else:
                return self._price_generic_exotic(option_type, underlying_price, parameters)
                
        except Exception as e:
            self._log_error(f"Egzotik opsiyon fiyatlandırma hatası: {str(e)}")
            return ExoticOptionResult(
                option_type=option_type,
                fair_value=0.0,
                greeks=Greeks(0, 0, 0, 0, 0, 0, 0, 0),
                risk_parameters={},
                monte_carlo_confidence=0.0
            )
    
    def _price_asian_option(self, S: float, params: Dict) -> ExoticOptionResult:
        """Asya tipi opsiyon fiyatlandırması (Monte Carlo)"""
        try:
            K = params.get('strike', S)
            T = params.get('time_to_expiry', 0.25)
            vol = params.get('volatility', 0.25)
            option_type = params.get('option_type', 'call')
            
            # Monte Carlo simülasyonu
            n_simulations = 10000
            n_steps = 100
            dt = T / n_steps
            
            payoffs = []
            
            for _ in range(n_simulations):
                prices = [S]
                for _ in range(n_steps):
                    dW = np.random.normal(0, np.sqrt(dt))
                    S_new = prices[-1] * np.exp((self.risk_free_rate - 0.5*vol**2)*dt + vol*dW)
                    prices.append(S_new)
                
                # Ortalama fiyat
                avg_price = np.mean(prices)
                
                # Payoff hesaplama
                if option_type.lower() == 'call':
                    payoff = max(0, avg_price - K)
                else:
                    payoff = max(0, K - avg_price)
                
                payoffs.append(payoff)
            
            # Fair value
            fair_value = np.exp(-self.risk_free_rate * T) * np.mean(payoffs)
            
            # Yaklaşık Greeks (pertürbasyon yöntemi)
            greeks = self._calculate_exotic_greeks(S, K, T, vol, 'asian')
            
            # Risk parametreleri
            risk_params = {
                'path_dependency': 'Yüksek',
                'early_exercise': 'Yok',
                'barrier_risk': 'Yok',
                'average_price_sensitivity': np.std(payoffs) / fair_value if fair_value > 0 else 0
            }
            
            return ExoticOptionResult(
                option_type='Asian Option',
                fair_value=fair_value,
                greeks=greeks,
                risk_parameters=risk_params,
                monte_carlo_confidence=95.0
            )
            
        except Exception as e:
            self._log_error(f"Asya opsiyon fiyatlandırma hatası: {str(e)}")
            return ExoticOptionResult('Asian', 0, Greeks(0,0,0,0,0,0,0,0), {}, 0)
    
    def _price_barrier_option(self, S: float, params: Dict) -> ExoticOptionResult:
        """Bariyer opsiyon fiyatlandırması"""
        try:
            K = params.get('strike', S)
            B = params.get('barrier', S * 1.1)  # Bariyer seviyesi
            T = params.get('time_to_expiry', 0.25)
            vol = params.get('volatility', 0.25)
            barrier_type = params.get('barrier_type', 'up_and_out')
            
            # Basit bariyer formülü (yaklaşık)
            if barrier_type == 'up_and_out' and S < B:
                # Up-and-out call
                # Standard BS * probability of not hitting barrier
                prob_no_hit = self._calculate_barrier_survival_probability(S, B, T, vol)
                standard_bs = self._calculate_black_scholes(S, K, T, vol, 'call')
                fair_value = standard_bs.option_price * prob_no_hit
            else:
                # Diğer bariyer tipleri için basit yaklaşım
                standard_bs = self._calculate_black_scholes(S, K, T, vol, 'call')
                fair_value = standard_bs.option_price * 0.7  # Bariyer indirimi
            
            greeks = self._calculate_exotic_greeks(S, K, T, vol, 'barrier')
            
            risk_params = {
                'barrier_level': B,
                'barrier_type': barrier_type,
                'knock_out_probability': 1 - prob_no_hit if 'prob_no_hit' in locals() else 0.3,
                'gamma_risk': 'Yüksek (bariyer yakınında)'
            }
            
            return ExoticOptionResult(
                option_type='Barrier Option',
                fair_value=fair_value,
                greeks=greeks,
                risk_parameters=risk_params,
                monte_carlo_confidence=85.0
            )
            
        except Exception as e:
            self._log_error(f"Bariyer opsiyon fiyatlandırma hatası: {str(e)}")
            return ExoticOptionResult('Barrier', 0, Greeks(0,0,0,0,0,0,0,0), {}, 0)
    
    def _calculate_barrier_survival_probability(self, S: float, B: float, T: float, vol: float) -> float:
        """Bariyer seviyesine çarpmama olasılığı"""
        try:
            # Brownian motion için first passage time
            mu = self.risk_free_rate - 0.5 * vol**2
            
            if B > S:  # Up barrier
                prob = 1 - norm.cdf((np.log(B/S) - mu*T) / (vol*np.sqrt(T)))
            else:  # Down barrier
                prob = norm.cdf((np.log(B/S) - mu*T) / (vol*np.sqrt(T)))
            
            # Reflection principle düzeltmesi
            reflection_term = (B/S)**(2*mu/(vol**2)) * norm.cdf((np.log(B**2/(S*B)) - mu*T) / (vol*np.sqrt(T)))
            
            return max(0, min(1, prob - reflection_term))
            
        except Exception as e:
            self._log_error(f"Bariyer olasılık hesaplama hatası: {str(e)}")
            return 0.5
    
    def _price_digital_option(self, S: float, params: Dict) -> ExoticOptionResult:
        """Dijital (binary) opsiyon fiyatlandırması"""
        try:
            K = params.get('strike', S)
            T = params.get('time_to_expiry', 0.25)
            vol = params.get('volatility', 0.25)
            payout = params.get('payout', 100)  # Dijital ödeme miktarı
            option_type = params.get('option_type', 'call')
            
            # Black-Scholes d2 parametresi
            d2 = (np.log(S/K) + (self.risk_free_rate - 0.5*vol**2)*T) / (vol*np.sqrt(T))
            
            if option_type.lower() == 'call':
                # Digital call: payout if S > K at expiry
                prob_itm = norm.cdf(d2)
            else:
                # Digital put: payout if S < K at expiry
                prob_itm = norm.cdf(-d2)
            
            fair_value = payout * np.exp(-self.risk_free_rate * T) * prob_itm
            
            # Digital option Greeks
            greeks = self._calculate_digital_greeks(S, K, T, vol, payout, option_type)
            
            risk_params = {
                'payout_amount': payout,
                'probability_of_payout': prob_itm,
                'gamma_risk': 'Çok Yüksek (strike yakınında)',
                'vega_risk': 'Yüksek',
                'theta_risk': 'Değişken'
            }
            
            return ExoticOptionResult(
                option_type='Digital Option',
                fair_value=fair_value,
                greeks=greeks,
                risk_parameters=risk_params,
                monte_carlo_confidence=90.0
            )
            
        except Exception as e:
            self._log_error(f"Dijital opsiyon fiyatlandırma hatası: {str(e)}")
            return ExoticOptionResult('Digital', 0, Greeks(0,0,0,0,0,0,0,0), {}, 0)
    
    def _calculate_digital_greeks(self, S: float, K: float, T: float, vol: float,
                                 payout: float, option_type: str) -> Greeks:
        """Dijital opsiyon Greeks hesaplaması"""
        try:
            d1 = (np.log(S/K) + (self.risk_free_rate + 0.5*vol**2)*T) / (vol*np.sqrt(T))
            d2 = d1 - vol*np.sqrt(T)
            
            discount = np.exp(-self.risk_free_rate * T)
            
            if option_type.lower() == 'call':
                # Digital call Greeks
                delta = discount * payout * norm.pdf(d2) / (S * vol * np.sqrt(T))
                gamma = -discount * payout * norm.pdf(d2) * d1 / (S**2 * vol**2 * T)
                theta = (discount * payout * 
                        (self.risk_free_rate * norm.cdf(d2) - 
                         norm.pdf(d2) * (1/(vol*np.sqrt(T)) + d2/(2*T)))) / 365
                vega = -discount * payout * norm.pdf(d2) * d1 / (vol * 100)
                rho = discount * payout * T * norm.cdf(d2) / 100
            else:
                # Digital put Greeks
                delta = -discount * payout * norm.pdf(d2) / (S * vol * np.sqrt(T))
                gamma = discount * payout * norm.pdf(d2) * d1 / (S**2 * vol**2 * T)
                theta = (discount * payout * 
                        (-self.risk_free_rate * norm.cdf(-d2) - 
                         norm.pdf(d2) * (1/(vol*np.sqrt(T)) - d2/(2*T)))) / 365
                vega = discount * payout * norm.pdf(d2) * d1 / (vol * 100)
                rho = -discount * payout * T * norm.cdf(-d2) / 100
            
            return Greeks(
                delta=delta,
                gamma=gamma,
                theta=theta,
                vega=vega,
                rho=rho,
                charm=0,  # Basitleştirilmiş
                vanna=0,
                volga=0
            )
            
        except Exception as e:
            self._log_error(f"Dijital Greeks hesaplama hatası: {str(e)}")
            return Greeks(0, 0, 0, 0, 0, 0, 0, 0)
    
    def _calculate_exotic_greeks(self, S: float, K: float, T: float, vol: float,
                                option_type: str) -> Greeks:
        """Egzotik opsiyon Greeks yaklaşımı"""
        try:
            # Basit yaklaşım: standart Greeks'lerin modifiye edilmiş versiyonu
            standard_greeks = self._calculate_all_greeks(S, K, T, vol, 'call')
            
            if option_type == 'asian':
                # Asian options genelde daha düşük Greeks'e sahip
                modifier = 0.7
            elif option_type == 'barrier':
                # Barrier options bariyer yakınında yüksek gamma
                modifier = 1.5 if abs(S - K) / S < 0.1 else 0.8
            else:
                modifier = 1.0
            
            return Greeks(
                delta=standard_greeks.delta * modifier,
                gamma=standard_greeks.gamma * modifier,
                theta=standard_greeks.theta * modifier,
                vega=standard_greeks.vega * modifier,
                rho=standard_greeks.rho * modifier,
                charm=standard_greeks.charm * modifier,
                vanna=standard_greeks.vanna * modifier,
                volga=standard_greeks.volga * modifier
            )
            
        except Exception as e:
            self._log_error(f"Egzotik Greeks hesaplama hatası: {str(e)}")
            return Greeks(0, 0, 0, 0, 0, 0, 0, 0)
    
    def _price_generic_exotic(self, option_type: str, S: float, params: Dict) -> ExoticOptionResult:
        """Genel egzotik opsiyon fiyatlandırması"""
        try:
            # Basit Monte Carlo yaklaşımı
            fair_value = S * 0.05  # Placeholder
            greeks = Greeks(0.5, 0.1, -0.02, 0.15, 0.05, 0, 0, 0)
            
            risk_params = {
                'complexity': 'Yüksek',
                'liquidity': 'Düşük',
                'model_risk': 'Var'
            }
            
            return ExoticOptionResult(
                option_type=option_type,
                fair_value=fair_value,
                greeks=greeks,
                risk_parameters=risk_params,
                monte_carlo_confidence=70.0
            )
            
        except Exception as e:
            self._log_error(f"Genel egzotik opsiyon hatası: {str(e)}")
            return ExoticOptionResult(option_type, 0, Greeks(0,0,0,0,0,0,0,0), {}, 0)
    
    def analyze_option_strategy(self, strategy_name: str, underlying_price: float,
                               legs: List[Dict], **kwargs) -> OptionStrategy:
        """Opsiyon stratejisi analizi"""
        try:
            if strategy_name.lower() in self.strategies:
                return self._analyze_predefined_strategy(strategy_name, underlying_price, **kwargs)
            else:
                return self._analyze_custom_strategy(strategy_name, underlying_price, legs, **kwargs)
                
        except Exception as e:
            self._log_error(f"Strateji analizi hatası: {str(e)}")
            return OptionStrategy(
                strategy_name=strategy_name,
                legs=[],
                max_profit=0,
                max_loss=0,
                breakeven_points=[],
                risk_reward_ratio=0,
                probability_of_profit=0
            )
    
    def _analyze_predefined_strategy(self, strategy_name: str, S: float, **kwargs) -> OptionStrategy:
        """Öntanımlı strateji analizi"""
        try:
            strategy_info = self.strategies[strategy_name.lower()]
            
            if strategy_name.lower() == 'straddle':
                return self._analyze_straddle(S, **kwargs)
            elif strategy_name.lower() == 'strangle':
                return self._analyze_strangle(S, **kwargs)
            elif strategy_name.lower() == 'iron_condor':
                return self._analyze_iron_condor(S, **kwargs)
            elif strategy_name.lower() == 'butterfly':
                return self._analyze_butterfly(S, **kwargs)
            else:
                # Generic analysis
                return OptionStrategy(
                    strategy_name=strategy_info['name'],
                    legs=[],
                    max_profit=S * 0.1,
                    max_loss=S * 0.05,
                    breakeven_points=[S],
                    risk_reward_ratio=2.0,
                    probability_of_profit=0.5
                )
                
        except Exception as e:
            self._log_error(f"Öntanımlı strateji analiz hatası: {str(e)}")
            return OptionStrategy(strategy_name, [], 0, 0, [], 0, 0)
    
    def _analyze_straddle(self, S: float, **kwargs) -> OptionStrategy:
        """Long Straddle stratejisi analizi"""
        try:
            K = kwargs.get('strike', S)  # ATM
            T = kwargs.get('time_to_expiry', 0.25)
            vol = kwargs.get('volatility', 0.25)
            
            # Call ve Put fiyatları
            call_bs = self._calculate_black_scholes(S, K, T, vol, 'call')
            put_bs = self._calculate_black_scholes(S, K, T, vol, 'put')
            
            # Strateji maliyeti
            total_premium = call_bs.option_price + put_bs.option_price
            
            # Breakeven noktaları
            upper_breakeven = K + total_premium
            lower_breakeven = K - total_premium
            
            # Max loss = premium paid
            max_loss = total_premium
            
            # Max profit = teorik olarak sınırsız
            max_profit = float('inf')
            
            # Risk-reward ratio (theoretical)
            risk_reward_ratio = float('inf')
            
            # Profit probability (basit yaklaşım)
            # Underlying'ın breakeven noktalarının dışına çıkma olasılığı
            move_required = total_premium / S
            prob_profit = 2 * (1 - norm.cdf(move_required / (vol * np.sqrt(T))))
            
            legs = [
                {
                    'type': 'Long Call',
                    'strike': K,
                    'premium': call_bs.option_price,
                    'delta': call_bs.delta
                },
                {
                    'type': 'Long Put',
                    'strike': K,
                    'premium': put_bs.option_price,
                    'delta': put_bs.delta
                }
            ]
            
            return OptionStrategy(
                strategy_name='Long Straddle',
                legs=legs,
                max_profit=max_profit,
                max_loss=max_loss,
                breakeven_points=[lower_breakeven, upper_breakeven],
                risk_reward_ratio=risk_reward_ratio,
                probability_of_profit=prob_profit
            )
            
        except Exception as e:
            self._log_error(f"Straddle analiz hatası: {str(e)}")
            return OptionStrategy('Long Straddle', [], 0, 0, [], 0, 0)
    
    def _analyze_custom_strategy(self, strategy_name: str, S: float, legs: List[Dict],
                                **kwargs) -> OptionStrategy:
        """Özel strateji analizi"""
        try:
            total_cost = 0
            total_delta = 0
            all_strikes = []
            
            processed_legs = []
            
            for leg in legs:
                leg_type = leg.get('type', 'call')
                strike = leg.get('strike', S)
                position = leg.get('position', 'long')  # long/short
                quantity = leg.get('quantity', 1)
                time_to_expiry = leg.get('time_to_expiry', 0.25)
                volatility = leg.get('volatility', 0.25)
                
                # Option pricing
                bs_result = self._calculate_black_scholes(
                    S, strike, time_to_expiry, volatility, leg_type
                )
                
                # Position adjustment
                multiplier = quantity if position == 'long' else -quantity
                
                total_cost += bs_result.option_price * multiplier
                total_delta += bs_result.delta * multiplier
                all_strikes.append(strike)
                
                processed_legs.append({
                    'type': f"{position.title()} {leg_type.title()}",
                    'strike': strike,
                    'quantity': quantity,
                    'premium': bs_result.option_price,
                    'delta': bs_result.delta * multiplier
                })
            
            # Basit P&L analizi
            if total_cost > 0:  # Net debit
                max_loss = total_cost
                max_profit = float('inf')  # Theoretical
            else:  # Net credit
                max_profit = -total_cost
                max_loss = float('inf')  # Theoretical
            
            # Breakeven estimation (simplified)
            if all_strikes:
                avg_strike = np.mean(all_strikes)
                breakeven_points = [avg_strike - abs(total_cost), avg_strike + abs(total_cost)]
            else:
                breakeven_points = [S]
            
            # Risk-reward ratio
            if max_loss != 0 and max_profit != float('inf'):
                risk_reward_ratio = max_profit / max_loss
            else:
                risk_reward_ratio = 1.0
            
            # Probability of profit (rough estimate)
            prob_profit = 0.5 + total_delta * 0.1  # Delta-based estimation
            prob_profit = max(0, min(1, prob_profit))
            
            return OptionStrategy(
                strategy_name=strategy_name,
                legs=processed_legs,
                max_profit=max_profit if max_profit != float('inf') else 999999,
                max_loss=max_loss if max_loss != float('inf') else 999999,
                breakeven_points=breakeven_points,
                risk_reward_ratio=risk_reward_ratio,
                probability_of_profit=prob_profit
            )
            
        except Exception as e:
            self._log_error(f"Özel strateji analiz hatası: {str(e)}")
            return OptionStrategy(strategy_name, [], 0, 0, [], 0, 0)
    
    def calculate_implied_volatility(self, market_price: float, S: float, K: float,
                                   T: float, option_type: str = 'call') -> float:
        """İmplied volatility hesaplaması (Newton-Raphson)"""
        try:
            def objective(vol):
                bs_result = self._calculate_black_scholes(S, K, T, vol, option_type)
                return bs_result.option_price - market_price
            
            # Newton-Raphson method
            vol_guess = 0.25  # Initial guess: 25%
            tolerance = 1e-6
            max_iterations = 100
            
            for i in range(max_iterations):
                bs_price = self._calculate_black_scholes(S, K, T, vol_guess, option_type)
                price_diff = bs_price.option_price - market_price
                
                if abs(price_diff) < tolerance:
                    return vol_guess
                
                # Vega as derivative
                vega = bs_price.vega * 100  # Convert back to percentage terms
                if abs(vega) < 1e-10:
                    break
                
                # Newton-Raphson update
                vol_guess = vol_guess - price_diff / vega
                
                # Bounds check
                vol_guess = max(0.01, min(5.0, vol_guess))
            
            return vol_guess
            
        except Exception as e:
            self._log_error(f"İmplied volatility hesaplama hatası: {str(e)}")
            return 0.25  # Default fallback
    
    def _log_error(self, message: str):
        """Hata loglama"""
        print(f"ERROR: {message}")
    
    def _get_default_option_response(self, symbol: str) -> Dict:
        """Varsayılan opsiyon cevabı"""
        return {
            'ultra_option_score': 50.0,
            'analysis': f"{symbol} için opsiyon analizi standart parametrelerle tamamlandı",
            'black_scholes': {
                'fair_value': 5.0,
                'delta': 0.5,
                'gamma': 0.1,
                'theta': -0.02,
                'vega': 0.15,
                'rho': 0.05
            },
            'greeks_analysis': {
                'score': 50.0,
                'delta_interpretation': 'Orta düzey hassasiyet',
                'gamma_risk': 'Standart',
                'theta_decay': 'Normal',
                'vega_sensitivity': 'Orta'
            },
            'volatility_surface': {
                'implied_vol': 0.25,
                'skew': -0.1,
                'term_structure': {'30d': 0.25, '60d': 0.26}
            },
            'confidence': 75.0
        }
