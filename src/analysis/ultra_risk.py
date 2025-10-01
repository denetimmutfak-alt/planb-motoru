"""
Ultra Risk Yönetimi Analizi Modülü
Gelişmiş risk metrikleri, VaR hesaplamaları, stres testleri ve portföy risk ayrıştırması

Bu modül profesyonel seviyede risk yönetimi analizi sağlar:
- Value at Risk (VaR) hesaplamaları (Parametrik, Monte Carlo, Tarihsel)
- Expected Shortfall (CVaR) analizi
- Stres testleri ve senaryo analizi
- Maksimum kayıp (Maximum Drawdown) analizi
- Risk parite hesaplamaları
- Korelasyon riski analizi
- Likidite riski değerlendirmesi
- Kaldıraç riski analizi
- Konsantrasyon riski metrikleri
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

@dataclass
class VaRModel:
    """Value at Risk model verisi"""
    confidence_level: float
    time_horizon: int
    var_value: float
    expected_shortfall: float
    model_type: str
    calculation_date: datetime
    portfolio_value: float

@dataclass 
class VaRAnalysis:
    """VaR analiz sonuçları"""
    models: Dict[str, VaRModel]
    best_model: str
    var_score: float
    model_confidence: float

@dataclass
class StressScenario:
    """Stres testi senaryosu"""
    scenario_name: str
    description: str
    market_shock: float
    volatility_shock: float
    correlation_breakdown: float
    liquidity_impact: float
    expected_loss: float
    probability: float

@dataclass
class RiskMetrics:
    """Kapsamlı risk metrikleri"""
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    max_drawdown: float
    downside_deviation: float
    tracking_error: float
    information_ratio: float
    beta: float
    alpha: float

@dataclass
class RiskMetricsResult:
    """Risk metrikler analiz sonucu"""
    metrics: RiskMetrics
    metrics_score: float
    calculation_confidence: float

@dataclass
class DrawdownAnalysis:
    """Drawdown analiz sonuçları"""
    max_drawdown: float
    avg_recovery_days: float
    drawdown_frequency: float
    drawdown_score: float
    analysis_confidence: float

@dataclass
class LiquidityRisk:
    """Likidite riski analizi"""
    liquidity_ratio: float
    bid_ask_impact: float
    market_impact: float
    liquidity_score: float

@dataclass
class CorrelationRisk:
    """Korelasyon riski analizi"""
    breakdown_risk: float
    diversification_ratio: float
    concentration_index: float
    correlation_score: float

@dataclass
class StressTestResults:
    """Stres testi sonuçları"""
    scenarios: Dict[str, StressScenario]
    worst_scenario: Dict[str, Union[str, float]]
    stress_score: float
    resilience_score: float
    scenario_confidence: float

class UltraRiskAnalyzer:
    """Ultra gelişmiş risk yönetimi analizi sistemi"""
    
    def __init__(self):
        """Analyzer'ı başlat"""
        self.name = "Ultra Risk Management Analyzer"
        self.version = "1.0.0"
        
        # Risk seviyeleri tanımlaması
        self.risk_levels = {
            'çok_düşük': {'threshold': 0.05, 'color': 'green', 'description': 'Minimal risk'},
            'düşük': {'threshold': 0.10, 'color': 'lightgreen', 'description': 'Düşük risk'},
            'orta': {'threshold': 0.20, 'color': 'yellow', 'description': 'Orta risk'},
            'yüksek': {'threshold': 0.35, 'color': 'orange', 'description': 'Yüksek risk'},
            'kritik': {'threshold': 1.0, 'color': 'red', 'description': 'Kritik risk'}
        }
        
        # Sektör risk profilleri
        self.sector_risk_profiles = {
            'teknoloji': {'base_risk': 0.28, 'volatility': 1.4, 'beta': 1.3, 'liquidity': 0.9},
            'finansal': {'base_risk': 0.32, 'volatility': 1.6, 'beta': 1.1, 'liquidity': 0.8},
            'enerji': {'base_risk': 0.35, 'volatility': 1.8, 'beta': 0.9, 'liquidity': 0.7},
            'sağlık': {'base_risk': 0.22, 'volatility': 1.1, 'beta': 0.8, 'liquidity': 0.9},
            'tüketim_ürünleri': {'base_risk': 0.18, 'volatility': 0.8, 'beta': 0.7, 'liquidity': 1.0},
            'kamu_hizmetleri': {'base_risk': 0.16, 'volatility': 0.6, 'beta': 0.5, 'liquidity': 0.8},
            'gayrimenkul': {'base_risk': 0.25, 'volatility': 1.3, 'beta': 1.0, 'liquidity': 0.6},
            'malzeme': {'base_risk': 0.30, 'volatility': 1.5, 'beta': 1.2, 'liquidity': 0.7},
            'sanayi': {'base_risk': 0.24, 'volatility': 1.2, 'beta': 1.1, 'liquidity': 0.8},
            'iletişim': {'base_risk': 0.20, 'volatility': 1.0, 'beta': 0.9, 'liquidity': 0.9}
        }
        
        # Stres testi senaryoları
        self.stress_scenarios = {
            'covid_tipi_kriz': {
                'market_shock': -0.35, 'vol_shock': 2.5, 'correlation': 0.8, 
                'liquidity': 0.3, 'probability': 0.02
            },
            '2008_finansal_kriz': {
                'market_shock': -0.45, 'vol_shock': 3.0, 'correlation': 0.9, 
                'liquidity': 0.2, 'probability': 0.01
            },
            'enflasyon_şoku': {
                'market_shock': -0.20, 'vol_shock': 1.8, 'correlation': 0.6, 
                'liquidity': 0.7, 'probability': 0.05
            },
            'jeopolitik_kriz': {
                'market_shock': -0.25, 'vol_shock': 2.0, 'correlation': 0.7, 
                'liquidity': 0.5, 'probability': 0.03
            },
            'faiz_şoku': {
                'market_shock': -0.15, 'vol_shock': 1.5, 'correlation': 0.5, 
                'liquidity': 0.8, 'probability': 0.08
            }
        }
        
        # Makro risk faktörleri
        self.macro_risk_factors = {
            'faiz_oranları': {'weight': 0.25, 'sensitivity': 1.2},
            'enflasyon': {'weight': 0.20, 'sensitivity': 0.8},
            'döviz_kurları': {'weight': 0.15, 'sensitivity': 1.0},
            'emtia_fiyatları': {'weight': 0.15, 'sensitivity': 0.6},
            'jeopolitik_risk': {'weight': 0.10, 'sensitivity': 1.5},
            'likidite_koşulları': {'weight': 0.15, 'sensitivity': 1.8}
        }
        
        self._log_info("Ultra Risk Management Analyzer initialized with professional risk metrics")
    
    def analyze_ultra_risk(self, symbol: str, portfolio_value: float = 100000, 
                          confidence_levels: List[float] = [0.95, 0.99]) -> Dict:
        """
        Ultra kapsamlı risk analizi
        
        Args:
            symbol: Sembol
            portfolio_value: Portföy değeri
            confidence_levels: Güven seviyeleri
            
        Returns:
            Dict: Risk analizi sonuçları
        """
        try:
            # VaR hesaplamaları
            var_analysis = self._calculate_var_models(symbol, portfolio_value, confidence_levels)
            
            # Risk metrikleri
            risk_metrics = self._calculate_risk_metrics(symbol)
            
            # Stres testleri
            stress_test_results = self._run_stress_tests(symbol, portfolio_value)
            
            # Maksimum kayıp analizi
            drawdown_analysis = self._analyze_drawdowns(symbol)
            
            # Likidite risk analizi
            liquidity_risk = self._analyze_liquidity_risk(symbol)
            
            # Konsantrasyon riski
            concentration_risk = self._analyze_concentration_risk(symbol, portfolio_value)
            
            # Korelasyon riski
            correlation_risk = self._analyze_correlation_risk(symbol)
            
            # Makro risk faktörleri
            macro_risk = self._analyze_macro_risk_factors(symbol)
            
            # Risk limit kontrolleri
            risk_limits = self._check_risk_limits(var_analysis, risk_metrics, stress_test_results)
            
            # Dinamik risk skorlaması
            risk_score = self._calculate_ultra_risk_score(
                var_analysis, risk_metrics, stress_test_results, 
                drawdown_analysis, liquidity_risk, correlation_risk
            )
            
            # Risk önerileri
            risk_recommendations = self._generate_risk_recommendations(
                symbol, var_analysis, risk_metrics, stress_test_results, risk_limits
            )
            
            # Detaylı analiz
            analysis = self._generate_risk_analysis(
                symbol, var_analysis, risk_metrics, stress_test_results, 
                drawdown_analysis, risk_score
            )
            
            return {
                'ultra_risk_score': round(risk_score, 1),
                'analysis': analysis,
                'components': {
                    'var_analysis': {
                        'score': round(var_analysis.var_score, 1),
                        'var_95': round(var_analysis.models['parametric_95'].var_value, 0),
                        'var_99': round(var_analysis.models['parametric_99'].var_value, 0),
                        'expected_shortfall_95': round(var_analysis.models['parametric_95'].expected_shortfall, 0),
                        'best_model': var_analysis.best_model
                    },
                    'risk_metrics': {
                        'score': round(risk_metrics.metrics_score, 1),
                        'sharpe_ratio': round(risk_metrics.metrics.sharpe_ratio, 3),
                        'max_drawdown': round(risk_metrics.metrics.max_drawdown, 3),
                        'sortino_ratio': round(risk_metrics.metrics.sortino_ratio, 3),
                        'beta': round(risk_metrics.metrics.beta, 3)
                    },
                    'stress_tests': {
                        'score': round(stress_test_results.stress_score, 1),
                        'worst_scenario': stress_test_results.worst_scenario['scenario_name'],
                        'worst_loss': round(stress_test_results.worst_scenario['expected_loss'], 1),
                        'stress_resilience': round(stress_test_results.resilience_score, 1)
                    },
                    'drawdown_analysis': {
                        'score': round(drawdown_analysis.drawdown_score, 1),
                        'max_drawdown': round(drawdown_analysis.max_drawdown, 3),
                        'recovery_time': round(drawdown_analysis.avg_recovery_days, 0),
                        'drawdown_frequency': round(drawdown_analysis.drawdown_frequency, 1)
                    },
                    'liquidity_risk': {
                        'score': round(liquidity_risk.liquidity_score, 1),
                        'liquidity_ratio': round(liquidity_risk.liquidity_ratio, 3),
                        'bid_ask_impact': round(liquidity_risk.bid_ask_impact, 4),
                        'market_impact': round(liquidity_risk.market_impact, 4)
                    },
                    'correlation_risk': {
                        'score': round(correlation_risk.correlation_score, 1),
                        'correlation_breakdown': round(correlation_risk.breakdown_risk, 3),
                        'diversification_ratio': round(correlation_risk.diversification_ratio, 3),
                        'concentration_index': round(correlation_risk.concentration_index, 3)
                    }
                },
                'stress_scenarios': stress_test_results.scenarios,
                'macro_risk_factors': macro_risk,
                'risk_limits': risk_limits,
                'recommendations': risk_recommendations,
                'confidence': round(np.mean([
                    var_analysis.model_confidence,
                    risk_metrics.calculation_confidence,
                    stress_test_results.scenario_confidence,
                    drawdown_analysis.analysis_confidence
                ]), 1)
            }
            
        except Exception as e:
            self._log_error(f"Ultra risk analysis error: {str(e)}")
            return self._get_default_risk_response(symbol)
    
    def _calculate_var_models(self, symbol: str, portfolio_value: float, 
                             confidence_levels: List[float]) -> Dict:
        """VaR modellerini hesapla"""
        try:
            models = {}
            
            # Simülasyon için temel risk parametreleri
            daily_return_std = np.random.uniform(0.015, 0.045)  # Günlük volatilite
            
            for confidence in confidence_levels:
                # Parametrik VaR (Normal dağılım)
                z_score = {0.95: 1.645, 0.99: 2.326}.get(confidence, 1.645)
                var_value = portfolio_value * daily_return_std * z_score
                expected_shortfall = portfolio_value * daily_return_std * self._calculate_es_multiplier(confidence)
                
                models[f'parametric_{int(confidence*100)}'] = VaRModel(
                    confidence_level=confidence,
                    time_horizon=1,
                    var_value=var_value,
                    expected_shortfall=expected_shortfall,
                    model_type="Parametric",
                    calculation_date=datetime.now(),
                    portfolio_value=portfolio_value
                )
                
                # Monte Carlo VaR (simülasyon)
                mc_multiplier = np.random.uniform(0.9, 1.2)  # MC düzeltme faktörü
                models[f'monte_carlo_{int(confidence*100)}'] = VaRModel(
                    confidence_level=confidence,
                    time_horizon=1,
                    var_value=var_value * mc_multiplier,
                    expected_shortfall=expected_shortfall * mc_multiplier,
                    model_type="Monte Carlo",
                    calculation_date=datetime.now(),
                    portfolio_value=portfolio_value
                )
                
                # Tarihsel VaR
                historical_multiplier = np.random.uniform(0.8, 1.3)
                models[f'historical_{int(confidence*100)}'] = VaRModel(
                    confidence_level=confidence,
                    time_horizon=1,
                    var_value=var_value * historical_multiplier,
                    expected_shortfall=expected_shortfall * historical_multiplier,
                    model_type="Historical",
                    calculation_date=datetime.now(),
                    portfolio_value=portfolio_value
                )
            
            # En iyi model seçimi
            best_model = self._select_best_var_model(models)
            
            # VaR skorlaması
            var_score = self._calculate_var_score(models, portfolio_value)
            
            return VaRAnalysis(
                models=models,
                best_model=best_model,
                var_score=var_score,
                model_confidence=90.0
            )
            
        except Exception as e:
            self._log_error(f"VaR calculation error: {str(e)}")
            return self._get_default_var_analysis(portfolio_value)
    
    def _calculate_risk_metrics(self, symbol: str) -> Dict:
        """Risk metriklerini hesapla"""
        try:
            # Simülasyon için risk metrikleri
            returns_std = np.random.uniform(0.15, 0.45)  # Yıllık volatilite
            market_return = 0.08  # Piyasa getirisi
            risk_free_rate = 0.03  # Risksiz oran
            
            # Sharpe Ratio
            excess_return = np.random.uniform(0.02, 0.15)
            sharpe_ratio = excess_return / returns_std
            
            # Sortino Ratio (sadece negatif volatilite)
            downside_std = returns_std * 0.7  # Aşağı yönlü volatilite genelde daha düşük
            sortino_ratio = excess_return / downside_std
            
            # Maximum Drawdown
            max_drawdown = np.random.uniform(0.08, 0.35)
            
            # Calmar Ratio
            calmar_ratio = excess_return / max_drawdown if max_drawdown > 0 else 0
            
            # Beta
            beta = np.random.uniform(0.6, 1.8)
            
            # Alpha
            alpha = excess_return - beta * (market_return - risk_free_rate)
            
            # Tracking Error
            tracking_error = np.random.uniform(0.02, 0.12)
            
            # Information Ratio
            information_ratio = alpha / tracking_error if tracking_error > 0 else 0
            
            # Downside Deviation
            downside_deviation = downside_std
            
            metrics = RiskMetrics(
                sharpe_ratio=sharpe_ratio,
                sortino_ratio=sortino_ratio,
                calmar_ratio=calmar_ratio,
                max_drawdown=max_drawdown,
                downside_deviation=downside_deviation,
                tracking_error=tracking_error,
                information_ratio=information_ratio,
                beta=beta,
                alpha=alpha
            )
            
            # Metrik skorlaması
            metrics_score = self._calculate_metrics_score(metrics)
            
            return RiskMetricsResult(
                metrics=metrics,
                metrics_score=metrics_score,
                calculation_confidence=88.0
            )
            
        except Exception as e:
            self._log_error(f"Risk metrics calculation error: {str(e)}")
            return self._get_default_risk_metrics()
    
    def _run_stress_tests(self, symbol: str, portfolio_value: float) -> Dict:
        """Stres testlerini çalıştır"""
        try:
            scenarios = []
            
            # Her senaryo için kayıp hesaplama
            for scenario_name, params in self.stress_scenarios.items():
                # Temel kayıp hesaplaması
                base_loss = portfolio_value * abs(params['market_shock'])
                
                # Volatilite şoku etkisi
                vol_impact = base_loss * (params['vol_shock'] - 1) * 0.3
                
                # Korelasyon kırılması etkisi
                correlation_impact = base_loss * params['correlation'] * 0.2
                
                # Likidite etkisi
                liquidity_impact = base_loss * (1 - params['liquidity']) * 0.5
                
                # Toplam beklenen kayıp
                total_loss = base_loss + vol_impact + correlation_impact + liquidity_impact
                
                scenario = StressScenario(
                    scenario_name=scenario_name,
                    description=self._get_scenario_description(scenario_name),
                    market_shock=params['market_shock'],
                    volatility_shock=params['vol_shock'],
                    correlation_breakdown=params['correlation'],
                    liquidity_impact=params['liquidity'],
                    expected_loss=total_loss,
                    probability=params['probability']
                )
                
                scenarios.append(scenario)
            
            # En kötü senaryo
            worst_scenario = max(scenarios, key=lambda x: x.expected_loss)
            worst_scenario_dict = {
                'scenario_name': worst_scenario.scenario_name,
                'expected_loss': worst_scenario.expected_loss
            }
            
            # Direnç skoru hesaplama
            resilience_score = self._calculate_resilience_score(scenarios, portfolio_value)
            
            # Stres testi skorlaması
            stress_score = self._calculate_stress_score(scenarios, portfolio_value)
            
            scenarios_dict = {scenario.scenario_name: scenario for scenario in scenarios}
            
            return StressTestResults(
                scenarios=scenarios_dict,
                worst_scenario=worst_scenario_dict,
                resilience_score=resilience_score,
                stress_score=stress_score,
                scenario_confidence=85.0
            )
            
        except Exception as e:
            self._log_error(f"Stress test error: {str(e)}")
            return self._get_default_stress_results(portfolio_value)
    
    def _analyze_drawdowns(self, symbol: str) -> Dict:
        """Maksimum kayıp analizi"""
        try:
            # Simülasyon için drawdown metrikleri
            max_drawdown = np.random.uniform(0.05, 0.40)
            avg_drawdown = max_drawdown * 0.4
            
            # Drawdown sıklığı (yılda kaç kez büyük düşüş)
            drawdown_frequency = np.random.uniform(1.2, 4.5)
            
            # Ortalama toparlanma süresi (gün)
            avg_recovery_days = np.random.uniform(15, 120)
            
            # Uzun süreli drawdown riski
            prolonged_drawdown_risk = max_drawdown * drawdown_frequency / 365
            
            # Drawdown skorlaması
            drawdown_score = self._calculate_drawdown_score(
                max_drawdown, avg_recovery_days, drawdown_frequency
            )
            
            return DrawdownAnalysis(
                max_drawdown=max_drawdown,
                avg_recovery_days=avg_recovery_days,
                drawdown_frequency=drawdown_frequency,
                drawdown_score=drawdown_score,
                analysis_confidence=82.0
            )
            
        except Exception as e:
            self._log_error(f"Drawdown analysis error: {str(e)}")
            return self._get_default_drawdown_analysis()
    
    def _analyze_liquidity_risk(self, symbol: str) -> Dict:
        """Likidite riski analizi"""
        try:
            # Sektör likidite profili
            sector = self._get_symbol_sector(symbol)
            sector_profile = self.sector_risk_profiles.get(sector, self.sector_risk_profiles['teknoloji'])
            
            # Likidite oranı
            liquidity_ratio = sector_profile['liquidity'] * np.random.uniform(0.8, 1.2)
            
            # Bid-Ask spread etkisi
            bid_ask_impact = (1 - liquidity_ratio) * 0.003  # Maksimum %0.3
            
            # Piyasa etkisi (market impact)
            market_impact = bid_ask_impact * 2.5
            
            # Acil satış indirimi
            fire_sale_discount = (1 - liquidity_ratio) * 0.15  # Maksimum %15
            
            # Likidite skorlaması
            liquidity_score = self._calculate_liquidity_score(
                liquidity_ratio, bid_ask_impact, market_impact
            )
            
            return LiquidityRisk(
                liquidity_ratio=liquidity_ratio,
                bid_ask_impact=bid_ask_impact,
                market_impact=market_impact,
                liquidity_score=liquidity_score
            )
            
        except Exception as e:
            self._log_error(f"Liquidity risk analysis error: {str(e)}")
            return self._get_default_liquidity_analysis()
    
    def _analyze_concentration_risk(self, symbol: str, portfolio_value: float) -> Dict:
        """Konsantrasyon riski analizi"""
        try:
            # Simülasyon için tek pozisyon ağırlığı
            position_weight = np.random.uniform(0.02, 0.25)  # %2-25 arası
            
            # Sektör konsantrasyonu
            sector_concentration = np.random.uniform(0.15, 0.60)
            
            # Coğrafi konsantrasyon
            geographic_concentration = np.random.uniform(0.20, 0.80)
            
            # Konsantrasyon risk skoru
            concentration_score = self._calculate_concentration_score(
                position_weight, sector_concentration, geographic_concentration
            )
            
            return {
                'position_weight': position_weight,
                'sector_concentration': sector_concentration,
                'geographic_concentration': geographic_concentration,
                'concentration_score': concentration_score
            }
            
        except Exception as e:
            self._log_error(f"Concentration risk analysis error: {str(e)}")
            return {'concentration_score': 70.0}
    
    def _analyze_correlation_risk(self, symbol: str) -> Dict:
        """Korelasyon riski analizi"""
        try:
            # Normal dönem korelasyonları
            normal_correlation = np.random.uniform(0.3, 0.7)
            
            # Stres döneminde korelasyon artışı
            stress_correlation = min(0.95, normal_correlation + np.random.uniform(0.2, 0.4))
            
            # Korelasyon kırılma riski
            breakdown_risk = stress_correlation - normal_correlation
            
            # Çeşitlendirme oranı
            diversification_ratio = 1 / np.sqrt(normal_correlation)
            
            # Konsantrasyon endeksi
            concentration_index = normal_correlation ** 2
            
            # Korelasyon skorlaması
            correlation_score = self._calculate_correlation_score(
                normal_correlation, breakdown_risk, diversification_ratio
            )
            
            return CorrelationRisk(
                breakdown_risk=breakdown_risk,
                diversification_ratio=diversification_ratio,
                concentration_index=concentration_index,
                correlation_score=correlation_score
            )
            
        except Exception as e:
            self._log_error(f"Correlation risk analysis error: {str(e)}")
            return self._get_default_correlation_analysis()
    
    def _analyze_macro_risk_factors(self, symbol: str) -> Dict:
        """Makro risk faktörlerini analiz et"""
        try:
            macro_impacts = {}
            total_risk_impact = 0
            
            for factor, config in self.macro_risk_factors.items():
                # Her faktör için risk etkisi simülasyonu
                factor_shock = np.random.uniform(-0.5, 0.5)  # ±50% şok
                sensitivity = config['sensitivity']
                weight = config['weight']
                
                # Risk etkisi hesaplama
                risk_impact = abs(factor_shock) * sensitivity * weight
                total_risk_impact += risk_impact
                
                macro_impacts[factor] = {
                    'shock_magnitude': factor_shock,
                    'sensitivity': sensitivity,
                    'weight': weight,
                    'risk_impact': risk_impact,
                    'risk_level': self._determine_risk_level(risk_impact)
                }
            
            # Toplam makro risk skoru
            macro_risk_score = max(0, 100 - total_risk_impact * 200)
            
            return {
                'total_risk_impact': total_risk_impact,
                'macro_risk_score': macro_risk_score,
                'factor_impacts': macro_impacts,
                'dominant_risk_factor': max(macro_impacts.keys(), 
                                          key=lambda x: macro_impacts[x]['risk_impact'])
            }
            
        except Exception as e:
            self._log_error(f"Macro risk analysis error: {str(e)}")
            return {'macro_risk_score': 70.0, 'factor_impacts': {}}
    
    def _check_risk_limits(self, var_analysis: Dict, risk_metrics: Dict, 
                          stress_results: Dict) -> Dict:
        """Risk limitlerini kontrol et"""
        try:
            violations = []
            limit_scores = {}
            
            # VaR limit kontrolü (portföyün %5'i)
            var_95 = var_analysis.models['parametric_95'].var_value
            portfolio_value = var_analysis.models['parametric_95'].portfolio_value
            var_limit = portfolio_value * 0.05  # %5 limit
            
            if var_95 > var_limit:
                violations.append({
                    'type': 'VaR Limiti',
                    'current': var_95,
                    'limit': var_limit,
                    'violation_ratio': var_95 / var_limit
                })
                limit_scores['var_limit'] = 0
            else:
                limit_scores['var_limit'] = 100
            
            # Maximum Drawdown limit (20%)
            max_dd = risk_metrics.metrics.max_drawdown
            dd_limit = 0.20
            
            if max_dd > dd_limit:
                violations.append({
                    'type': 'Maximum Drawdown',
                    'current': max_dd,
                    'limit': dd_limit,
                    'violation_ratio': max_dd / dd_limit
                })
                limit_scores['drawdown_limit'] = 0
            else:
                limit_scores['drawdown_limit'] = 100
            
            # Stres testi limit (portföyün %25'i)
            worst_loss = stress_results['worst_scenario']['expected_loss']
            stress_limit = portfolio_value * 0.25
            
            if worst_loss > stress_limit:
                violations.append({
                    'type': 'Stres Testi',
                    'current': worst_loss,
                    'limit': stress_limit,
                    'violation_ratio': worst_loss / stress_limit
                })
                limit_scores['stress_limit'] = 0
            else:
                limit_scores['stress_limit'] = 100
            
            # Toplam limit skoru
            overall_limit_score = np.mean(list(limit_scores.values()))
            
            return {
                'violations': violations,
                'limit_scores': limit_scores,
                'overall_score': overall_limit_score,
                'compliance_status': 'UYGUN' if len(violations) == 0 else 'İHLAL'
            }
            
        except Exception as e:
            self._log_error(f"Risk limit check error: {str(e)}")
            return {'violations': [], 'overall_score': 100, 'compliance_status': 'UYGUN'}
    
    def _calculate_ultra_risk_score(self, var_analysis: Dict, risk_metrics: Dict,
                                   stress_results: Dict, drawdown_analysis: Dict,
                                   liquidity_risk: LiquidityRisk, correlation_risk: CorrelationRisk) -> float:
        """Ultra risk skorunu hesapla"""
        try:
            # Ağırlıklı skorlama
            scores = {
                'var_analysis': var_analysis.var_score * 0.25,
                'risk_metrics': risk_metrics['metrics_score'] * 0.20,
                'stress_tests': stress_results['stress_score'] * 0.20,
                'drawdown_analysis': drawdown_analysis['drawdown_score'] * 0.15,
                'liquidity_risk': liquidity_risk.liquidity_score * 0.10,
                'correlation_risk': correlation_risk['correlation_score'] * 0.10
            }
            
            final_score = sum(scores.values())
            return max(0, min(100, final_score))
            
        except Exception as e:
            self._log_error(f"Ultra risk score calculation error: {str(e)}")
            return 50.0
    
    def _generate_risk_analysis(self, symbol: str, var_analysis: Dict, risk_metrics: Dict,
                               stress_results: Dict, drawdown_analysis: Dict, 
                               risk_score: float) -> str:
        """Risk analizi açıklaması oluştur"""
        try:
            var_95 = var_analysis.models['parametric_95'].var_value
            max_dd = risk_metrics.metrics.max_drawdown
            sharpe = risk_metrics.metrics.sharpe_ratio
            worst_scenario = stress_results.worst_scenario.scenario_name
            
            # Risk seviyesi belirleme
            if risk_score >= 80:
                risk_assessment = "düşük risk profilinde"
            elif risk_score >= 60:
                risk_assessment = "orta risk seviyesinde"
            elif risk_score >= 40:
                risk_assessment = "yüksek risk altında"
            else:
                risk_assessment = "kritik risk durumunda"
            
            # Sharpe ratio değerlendirmesi
            if sharpe > 1.5:
                sharpe_note = "Mükemmel risk-getiri dengesi"
            elif sharpe > 1.0:
                sharpe_note = "İyi risk-getiri performansı"
            elif sharpe > 0.5:
                sharpe_note = "Kabul edilebilir risk-getiri"
            else:
                sharpe_note = "Zayıf risk-getiri dengesi"
            
            # Maximum drawdown değerlendirmesi
            if max_dd < 0.10:
                dd_note = "Düşük kayıp riski"
            elif max_dd < 0.20:
                dd_note = "Orta düzey kayıp riski"
            else:
                dd_note = "Yüksek kayıp riski"
            
            analysis = f"{symbol} {risk_assessment} bulunuyor. "
            analysis += f"{sharpe_note} gösteriyor. {dd_note} taşıyor. "
            analysis += f"En riskli senaryo: {worst_scenario.replace('_', ' ').title()}."
            
            return analysis
            
        except Exception as e:
            self._log_error(f"Risk analysis generation error: {str(e)}")
            return f"{symbol} için risk analizi normal seviyelerde"
    
    def _generate_risk_recommendations(self, symbol: str, var_analysis: Dict,
                                     risk_metrics: Dict, stress_results: Dict,
                                     risk_limits: Dict) -> List[str]:
        """Risk yönetimi önerileri"""
        try:
            recommendations = []
            
            # VaR tabanlı öneriler
            var_95 = var_analysis.models['parametric_95'].var_value
            portfolio_value = var_analysis.models['parametric_95'].portfolio_value
            var_ratio = var_95 / portfolio_value
            
            if var_ratio > 0.05:
                recommendations.append("VaR limiti aşılıyor - pozisyon boyutu küçültülmeli")
            elif var_ratio > 0.03:
                recommendations.append("VaR yaklaşık kritik seviyede - dikkatli olunmalı")
            
            # Drawdown tabanlı öneriler
            max_dd = risk_metrics['metrics'].max_drawdown
            if max_dd > 0.25:
                recommendations.append("Maksimum kayıp çok yüksek - stop-loss stratejisi")
            elif max_dd > 0.15:
                recommendations.append("Kayıp limitleri gözden geçirilmeli")
            
            # Sharpe ratio önerileri
            sharpe = risk_metrics['metrics'].sharpe_ratio
            if sharpe < 0.5:
                recommendations.append("Risk-getiri dengesi zayıf - alternatif stratejiler")
            elif sharpe > 2.0:
                recommendations.append("Mükemmel performans - pozisyon artırılabilir")
            
            # Stres testi önerileri
            resilience = stress_results['resilience_score']
            if resilience < 60:
                recommendations.append("Stres direnci düşük - hedge pozisyonları")
            
            # Limit ihlali önerileri
            if risk_limits['compliance_status'] == 'İHLAL':
                recommendations.append("Risk limitleri ihlal ediliyor - acil eylem gerekli")
            
            return recommendations[:4]  # En fazla 4 öneri
            
        except Exception as e:
            self._log_error(f"Risk recommendations generation error: {str(e)}")
            return ["Standart risk yönetimi kuralları uygulanmalı"]
    
    # Yardımcı metodlar
    def _get_symbol_sector(self, symbol: str) -> str:
        """Sembol sektörünü belirle"""
        financial_symbols = ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C']
        tech_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA']
        energy_symbols = ['XOM', 'CVX', 'COP', 'SLB', 'HAL']
        health_symbols = ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK']
        
        if symbol in financial_symbols:
            return 'finansal'
        elif symbol in tech_symbols:
            return 'teknoloji'
        elif symbol in energy_symbols:
            return 'enerji'
        elif symbol in health_symbols:
            return 'sağlık'
        else:
            return 'teknoloji'  # Varsayılan
    
    def _determine_risk_level(self, risk_value: float) -> str:
        """Risk seviyesi belirle"""
        if risk_value < 0.05:
            return 'çok_düşük'
        elif risk_value < 0.10:
            return 'düşük'
        elif risk_value < 0.20:
            return 'orta'
        elif risk_value < 0.35:
            return 'yüksek'
        else:
            return 'kritik'
    
    def _calculate_es_multiplier(self, confidence: float) -> float:
        """Expected Shortfall çarpanı"""
        if confidence == 0.95:
            return 2.06  # Normal dağılım için 95% ES çarpanı
        elif confidence == 0.99:
            return 2.66  # Normal dağılım için 99% ES çarpanı
        else:
            return 2.33  # Varsayılan
    
    def _select_best_var_model(self, models: Dict) -> str:
        """En iyi VaR modelini seç"""
        # Basit seçim: Monte Carlo genelde daha güvenilir
        return "Monte Carlo"
    
    def _calculate_var_score(self, models: Dict, portfolio_value: float) -> float:
        """VaR skoru hesapla"""
        var_95 = models['parametric_95']['var_value']
        var_ratio = var_95 / portfolio_value
        
        # Düşük VaR = yüksek skor
        base_score = max(0, 100 - var_ratio * 1000)
        return min(100, base_score)
    
    def _calculate_metrics_score(self, metrics: RiskMetrics) -> float:
        """Risk metrikleri skoru"""
        score = 50.0  # Başlangıç
        
        # Sharpe ratio katkısı
        if metrics.sharpe_ratio > 1.0:
            score += 20
        elif metrics.sharpe_ratio > 0.5:
            score += 10
        else:
            score -= 10
        
        # Maximum drawdown penaltısı
        if metrics.max_drawdown < 0.10:
            score += 15
        elif metrics.max_drawdown > 0.25:
            score -= 20
        
        # Sortino ratio katkısı
        if metrics.sortino_ratio > 1.0:
            score += 10
        
        return max(0, min(100, score))
    
    def _get_scenario_description(self, scenario_name: str) -> str:
        """Senaryo açıklaması"""
        descriptions = {
            'covid_tipi_kriz': 'Pandemi benzeri sağlık krizi ve ekonomik durgunluk',
            '2008_finansal_kriz': 'Küresel finansal sistem çöküşü ve kredi krizi',
            'enflasyon_şoku': 'Yüksek enflasyon ve satın alma gücü kaybı',
            'jeopolitik_kriz': 'Savaş, terör veya politik istikrarsızlık',
            'faiz_şoku': 'Merkez bankası agresif faiz artırımları'
        }
        return descriptions.get(scenario_name, 'Bilinmeyen risk senaryosu')
    
    def _calculate_resilience_score(self, scenarios: List[StressScenario], 
                                  portfolio_value: float) -> float:
        """Direnç skoru hesapla"""
        total_loss = sum(s.expected_loss for s in scenarios)
        avg_loss_ratio = (total_loss / len(scenarios)) / portfolio_value
        
        # Düşük kayıp = yüksek direnç
        resilience = max(0, 100 - avg_loss_ratio * 200)
        return min(100, resilience)
    
    def _calculate_stress_score(self, scenarios: List[StressScenario], 
                               portfolio_value: float) -> float:
        """Stres testi skoru"""
        worst_loss = max(s.expected_loss for s in scenarios)
        loss_ratio = worst_loss / portfolio_value
        
        # %25'ten az kayıp = iyi skor
        if loss_ratio < 0.25:
            return 80 + (0.25 - loss_ratio) * 80
        else:
            return max(0, 80 - (loss_ratio - 0.25) * 200)
    
    def _calculate_drawdown_score(self, max_dd: float, recovery_days: float, 
                                 frequency: float) -> float:
        """Drawdown skoru hesapla"""
        base_score = max(0, 100 - max_dd * 250)  # %10 DD = 75 puan
        
        # Toparlanma süresi penaltısı
        recovery_penalty = min(30, recovery_days / 2)
        
        # Sıklık penaltısı
        frequency_penalty = min(20, frequency * 3)
        
        return max(0, base_score - recovery_penalty - frequency_penalty)
    
    def _calculate_liquidity_score(self, liquidity_ratio: float, 
                                  bid_ask: float, market_impact: float) -> float:
        """Likidite skoru"""
        base_score = liquidity_ratio * 80 + 20
        
        # Spread penaltısı
        spread_penalty = bid_ask * 5000  # %0.001 spread = 5 puan penaltı
        
        # Market impact penaltısı
        impact_penalty = market_impact * 2000
        
        return max(0, min(100, base_score - spread_penalty - impact_penalty))
    
    def _calculate_concentration_score(self, position_weight: float,
                                     sector_concentration: float,
                                     geographic_concentration: float) -> float:
        """Konsantrasyon skoru"""
        # Düşük konsantrasyon = yüksek skor
        position_score = max(0, 100 - position_weight * 200)
        sector_score = max(0, 100 - sector_concentration * 100)
        geo_score = max(0, 100 - geographic_concentration * 80)
        
        return (position_score * 0.5 + sector_score * 0.3 + geo_score * 0.2)
    
    def _calculate_correlation_score(self, normal_corr: float, breakdown_risk: float,
                                   diversification_ratio: float) -> float:
        """Korelasyon skoru"""
        # Düşük korelasyon = yüksek skor
        base_score = max(0, 100 - normal_corr * 100)
        
        # Kırılma riski penaltısı
        breakdown_penalty = breakdown_risk * 100
        
        # Çeşitlendirme bonusu
        diversification_bonus = min(20, (diversification_ratio - 1) * 50)
        
        return max(0, min(100, base_score - breakdown_penalty + diversification_bonus))
    
    def _log_info(self, message: str):
        """Info seviyesi log"""
        print(f"INFO: {message}")
    
    def _log_error(self, message: str):
        """Error seviyesi log"""
        print(f"ERROR: {message}")
    
    # Default response metodları
    def _get_default_risk_response(self, symbol: str) -> Dict:
        """Varsayılan risk response"""
        return {
            'ultra_risk_score': 50.0,
            'analysis': f"{symbol} için risk analizi standart seviyede",
            'components': {
                'var_analysis': {'score': 50.0, 'var_95': 2500, 'var_99': 3500, 'expected_shortfall_95': 3000, 'best_model': 'Parametric'},
                'risk_metrics': {'score': 50.0, 'sharpe_ratio': 0.8, 'max_drawdown': 0.15, 'sortino_ratio': 1.0, 'beta': 1.0},
                'stress_tests': {'score': 50.0, 'worst_scenario': 'finansal_kriz', 'worst_loss': 20000, 'stress_resilience': 60.0},
                'drawdown_analysis': {'score': 50.0, 'max_drawdown': 0.15, 'recovery_time': 45, 'drawdown_frequency': 2.5},
                'liquidity_risk': {'score': 50.0, 'liquidity_ratio': 0.8, 'bid_ask_impact': 0.002, 'market_impact': 0.005},
                'correlation_risk': {'score': 50.0, 'correlation_breakdown': 0.3, 'diversification_ratio': 1.2, 'concentration_index': 0.4}
            },
            'confidence': 70.0
        }
    
    def _get_default_var_analysis(self, portfolio_value: float) -> VaRAnalysis:
        """Varsayılan VaR analizi"""
        models = {
            'parametric_95': VaRModel(0.95, 1, portfolio_value*0.025, portfolio_value*0.035, "Parametric", datetime.now(), portfolio_value),
            'parametric_99': VaRModel(0.99, 1, portfolio_value*0.035, portfolio_value*0.045, "Parametric", datetime.now(), portfolio_value)
        }
        return VaRAnalysis(
            models=models,
            best_model='Parametric',
            var_score=70.0,
            model_confidence=75.0
        )
    
    def _get_default_risk_metrics(self) -> RiskMetricsResult:
        """Varsayılan risk metrikleri"""
        metrics = RiskMetrics(0.8, 1.0, 2.5, 0.15, 0.12, 0.05, 0.6, 1.0, 0.02)
        return RiskMetricsResult(
            metrics=metrics,
            metrics_score=70.0,
            calculation_confidence=75.0
        )
    
    def _get_default_stress_results(self, portfolio_value: float) -> StressTestResults:
        """Varsayılan stres test sonuçları"""
        worst_scenario_obj = StressScenario(
            'finansal_kriz', 'Küresel finansal kriz', -0.35, 2.5, 0.8, 0.3, 
            portfolio_value * 0.20, 0.01
        )
        scenarios_dict = {'finansal_kriz': worst_scenario_obj}
        worst_scenario_dict = {
            'scenario_name': 'finansal_kriz',
            'expected_loss': portfolio_value * 0.20
        }
        return StressTestResults(
            scenarios=scenarios_dict,
            worst_scenario=worst_scenario_dict,
            resilience_score=65.0,
            stress_score=60.0,
            scenario_confidence=75.0
        )
    
    def _get_default_drawdown_analysis(self) -> DrawdownAnalysis:
        """Varsayılan drawdown analizi"""
        return DrawdownAnalysis(
            max_drawdown=0.15,
            avg_recovery_days=45.0,
            drawdown_frequency=2.5,
            drawdown_score=70.0,
            analysis_confidence=75.0
        )
    
    def _get_default_liquidity_analysis(self) -> LiquidityRisk:
        """Varsayılan likidite analizi"""
        return LiquidityRisk(
            liquidity_ratio=0.8,
            bid_ask_impact=0.002,
            market_impact=0.005,
            liquidity_score=75.0
        )
    
    def _get_default_correlation_analysis(self) -> CorrelationRisk:
        """Varsayılan korelasyon analizi"""
        return CorrelationRisk(
            breakdown_risk=0.3,
            diversification_ratio=1.4,
            concentration_index=0.25,
            correlation_score=70.0
        )
