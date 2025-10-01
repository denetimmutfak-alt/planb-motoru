"""
Bonds Analysis Module
Tahvil Analizi Ana Modülü
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

# CompanyFoundingDates entegrasyonu
try:
    from ..data.company_founding_dates import CompanyFoundingDates
    FOUNDING_DATES_AVAILABLE = True
    print("INFO: CompanyFoundingDates modülü bonds analysis'e entegre edildi")
except ImportError:
    FOUNDING_DATES_AVAILABLE = False
    print("WARNING: CompanyFoundingDates modülü bulunamadı")

try:
    from .ultra_bonds import UltraBondsAnalyzer
    ULTRA_AVAILABLE = True
    print("INFO: Ultra Bonds Analysis modülü aktif")
except ImportError:
    ULTRA_AVAILABLE = False
    print("WARNING: Ultra Bonds Analysis modülü bulunamadı, temel analiz kullanılacak")

class BondsAnalyzer:
    """Ana bonds analiz sınıfı"""
    
    def __init__(self):
        """Bonds analyzer'ı başlat"""
        # CompanyFoundingDates entegrasyonu
        self.founding_dates = None
        if FOUNDING_DATES_AVAILABLE:
            try:
                self.founding_dates = CompanyFoundingDates()
                print("INFO: CompanyFoundingDates bonds analyzer'a başarıyla entegre edildi")
            except Exception as e:
                print(f"WARNING: CompanyFoundingDates bonds analyzer'a entegre edilemedi: {str(e)}")
        
        self.ultra_analyzer = None
        if ULTRA_AVAILABLE:
            try:
                self.ultra_analyzer = UltraBondsAnalyzer()
                print("INFO: Ultra Bonds Analyzer başarıyla başlatıldı")
            except Exception as e:
                print(f"WARNING: Ultra Bonds Analyzer başlatılamadı: {str(e)}")
        
        # Temel tahvil kategorileri
        self.bond_categories = {
            'GOVERNMENT': ['TREASURY', 'GOVT', 'BOND'],
            'CORPORATE': ['CORP', 'COMPANY'],
            'MUNICIPAL': ['MUNI', 'CITY'],
            'INFLATION_LINKED': ['TIPS', 'LINKER']
        }
        
        # Basit yield tahminleri
        self.base_yields = {
            'USD': {'1Y': 5.0, '5Y': 4.4, '10Y': 4.6, '30Y': 4.9},
            'EUR': {'1Y': 3.5, '5Y': 3.1, '10Y': 3.3, '30Y': 3.6},
            'TRY': {'1Y': 47.0, '5Y': 40.0, '10Y': 35.0, '30Y': 30.0}
        }
    
    def analyze_bond(self, symbol: str, bond_data: Optional[Dict] = None,
                    historical_data: Optional[pd.DataFrame] = None, **kwargs) -> Dict:
        """Kapsamlı bond analizi"""
        try:
            # Founding date bilgisini al
            founding_date = None
            founding_info = "Founding date bilgisi mevcut değil"
            if self.founding_dates:
                try:
                    founding_date = self.founding_dates.get_founding_date(symbol)
                    if founding_date:
                        founding_info = f"Founding date: {founding_date}"
                        print(f"INFO: {symbol} founding date bulundu: {founding_date}")
                    else:
                        founding_info = f"{symbol} founding date veritabanında bulunamadı"
                        print(f"DEBUG: {symbol} için founding date bulunamadı")
                except Exception as e:
                    founding_info = f"Founding date alınırken hata: {str(e)}"
                    print(f"ERROR: {symbol} founding date hatası: {str(e)}")
            
            if self.ultra_analyzer and ULTRA_AVAILABLE:
                result = self._ultra_bond_analysis(symbol, bond_data, historical_data, **kwargs)
                # Founding date bilgisini ekle
                result['founding_date_info'] = founding_info
                if founding_date:
                    result['founding_date'] = founding_date
                return result
            else:
                result = self._basic_bond_analysis(symbol, bond_data, historical_data, **kwargs)
                # Founding date bilgisini ekle
                result['founding_date_info'] = founding_info
                if founding_date:
                    result['founding_date'] = founding_date
                return result
                
        except Exception as e:
            print(f"ERROR: Bond analizi hatası: {str(e)}")
            return self._get_default_bond_response(symbol)
    
    def _ultra_bond_analysis(self, symbol: str, bond_data: Optional[Dict],
                            historical_data: Optional[pd.DataFrame], **kwargs) -> Dict:
        """Ultra gelişmiş bond analizi"""
        try:
            # Ana bond analizi
            result = self.ultra_analyzer.analyze_bond(
                symbol=symbol,
                bond_data=bond_data,
                historical_data=historical_data,
                **kwargs
            )
            
            # Bond score hesaplama
            bond_score = self._calculate_bond_score(result)
            
            # Yield curve insights
            curve_insights = self._analyze_curve_insights(result.yield_curve_analysis)
            
            # Credit analysis
            credit_analysis = self._analyze_credit_quality(result.credit_risk)
            
            # Duration analysis
            duration_analysis = self._analyze_duration_risk(result.valuation_metrics)
            
            # Investment strategies
            investment_strategies = self._recommend_bond_strategies(result)
            
            # Risk management
            risk_management = self._generate_bond_risk_management(result)
            
            return {
                'bond_score': round(bond_score, 1),
                'analysis_summary': self._generate_bond_summary(
                    symbol, result, bond_score
                ),
                'trading_recommendation': result.trading_recommendation,
                'ultra_analysis': {
                    'ultra_bond_score': result.ultra_bond_score,
                    'bond_type': result.bond_profile.bond_type.value,
                    'credit_rating': result.bond_profile.credit_rating.value,
                    'time_to_maturity': (result.bond_profile.maturity_date - datetime.now()).days / 365.25,
                    'valuation': {
                        'fair_value': round(result.valuation_metrics.fair_value, 2),
                        'yield_to_maturity': round(result.valuation_metrics.yield_to_maturity, 2),
                        'current_yield': round(result.valuation_metrics.current_yield, 2),
                        'duration': round(result.valuation_metrics.duration, 2),
                        'modified_duration': round(result.valuation_metrics.modified_duration, 2),
                        'convexity': round(result.valuation_metrics.convexity, 2),
                        'dv01': round(result.valuation_metrics.dv01, 4)
                    },
                    'credit_risk': {
                        'default_probability': round(result.credit_risk.default_probability * 100, 3),
                        'credit_spread': round(result.credit_risk.credit_spread, 2),
                        'credit_score': round(result.credit_risk.credit_score, 1),
                        'financial_health': round(result.credit_risk.financial_health_score, 1)
                    },
                    'yield_curve': {
                        'curve_shape': result.yield_curve_analysis.curve_shape,
                        'steepness': round(result.yield_curve_analysis.steepness, 2),
                        'recession_signal': result.yield_curve_analysis.recession_signal
                    },
                    'interest_rate_env': {
                        'central_bank_trend': result.interest_rate_environment.central_bank_trend,
                        'rate_cycle_phase': result.interest_rate_environment.rate_cycle_phase,
                        'fed_funds_rate': result.interest_rate_environment.fed_funds_rate
                    }
                },
                'relative_value': result.relative_value_analysis,
                'curve_insights': curve_insights,
                'credit_analysis': credit_analysis,
                'duration_analysis': duration_analysis,
                'investment_strategies': investment_strategies,
                'risk_management': risk_management,
                'macro_sensitivity': result.macro_sensitivity,
                'technical_signals': result.technical_signals,
                'risk_assessment': result.risk_assessment,
                'confidence': round(np.mean([
                    85.0 if result.ultra_bond_score > 70 else 75.0,
                    90.0 if result.risk_assessment.get('overall_risk') == 'Düşük Risk' else 70.0,
                    80.0
                ]), 1)
            }
            
        except Exception as e:
            print(f"ERROR: Ultra bond analizi hatası: {str(e)}")
            return self._basic_bond_analysis(symbol, bond_data, historical_data, **kwargs)
    
    def _basic_bond_analysis(self, symbol: str, bond_data: Optional[Dict],
                            historical_data: Optional[pd.DataFrame], **kwargs) -> Dict:
        """Temel bond analizi"""
        try:
            # Bond currency belirleme
            if bond_data and 'currency' in bond_data:
                currency = bond_data['currency']
            elif 'TR' in symbol.upper():
                currency = 'TRY'
            elif 'DE' in symbol.upper() or 'BUND' in symbol.upper():
                currency = 'EUR'
            else:
                currency = 'USD'
            
            # Bond type belirleme
            bond_type = 'GOVERNMENT'  # Default
            for cat, symbols in self.bond_categories.items():
                if any(sym in symbol.upper() for sym in symbols):
                    bond_type = cat
                    break
            
            # Maturity tahmin et
            if bond_data and 'maturity' in bond_data:
                maturity = datetime.strptime(bond_data['maturity'], '%Y-%m-%d')
            else:
                # Symbol'den maturity çıkar (basit)
                if '30' in symbol:
                    maturity = datetime.now() + timedelta(days=365*30)
                elif '10' in symbol:
                    maturity = datetime.now() + timedelta(days=365*10)
                elif '5' in symbol:
                    maturity = datetime.now() + timedelta(days=365*5)
                else:
                    maturity = datetime.now() + timedelta(days=365*5)  # Default 5Y
            
            time_to_maturity = (maturity - datetime.now()).days / 365.25
            
            # Yield tahmin et
            if time_to_maturity <= 2:
                ytm = self.base_yields.get(currency, {}).get('1Y', 4.0)
            elif time_to_maturity <= 7:
                ytm = self.base_yields.get(currency, {}).get('5Y', 4.0)
            elif time_to_maturity <= 15:
                ytm = self.base_yields.get(currency, {}).get('10Y', 4.0)
            else:
                ytm = self.base_yields.get(currency, {}).get('30Y', 4.0)
            
            # Credit spread ekle
            if bond_type == 'CORPORATE':
                ytm += 1.0  # Corporate spread
            elif bond_type == 'MUNICIPAL':
                ytm += 0.5  # Municipal spread
            
            # Duration hesapla (approximation)
            duration = time_to_maturity * 0.85
            
            # Bond score hesapla
            score_components = [
                70 if bond_type == 'GOVERNMENT' else 60,  # Credit quality
                60 if time_to_maturity < 10 else 40,     # Duration risk
                65 if currency == 'USD' else 50 if currency == 'EUR' else 30,  # Currency
                60 if ytm > 3 else 50  # Yield attractiveness
            ]
            bond_score = np.mean(score_components)
            
            # Trading recommendation
            if bond_score >= 65:
                recommendation = "ALIŞ"
            elif bond_score >= 50:
                recommendation = "BEKLE"
            else:
                recommendation = "SAT"
            
            return {
                'bond_score': round(bond_score, 1),
                'analysis_summary': f"{symbol} tahvil analizi: {bond_type} türü, {currency} denominasyonu, temel analiz ile değerlendirildi",
                'trading_recommendation': recommendation,
                'basic_metrics': {
                    'bond_type': bond_type,
                    'currency': currency,
                    'time_to_maturity': round(time_to_maturity, 2),
                    'estimated_ytm': round(ytm, 2),
                    'estimated_duration': round(duration, 2),
                    'maturity_date': maturity.strftime('%Y-%m-%d')
                },
                'risk_assessment': {
                    'overall_risk': 'Yüksek' if currency == 'TRY' else 'Orta' if time_to_maturity > 10 else 'Düşük',
                    'credit_risk': 'Düşük' if bond_type == 'GOVERNMENT' else 'Orta',
                    'interest_rate_risk': 'Yüksek' if duration > 10 else 'Orta' if duration > 5 else 'Düşük',
                    'currency_risk': 'Yüksek' if currency == 'TRY' else 'Orta' if currency != 'USD' else 'Düşük'
                },
                'confidence': 70.0
            }
            
        except Exception as e:
            print(f"ERROR: Temel bond analizi hatası: {str(e)}")
            return self._get_default_bond_response(symbol)
    
    def _calculate_bond_score(self, ultra_result) -> float:
        """Genel bond skoru hesaplama"""
        try:
            scores = []
            
            # Ultra bond score (%40)
            scores.append(ultra_result.ultra_bond_score * 0.4)
            
            # Credit quality (%25)
            credit_score = ultra_result.credit_risk.credit_score
            scores.append(credit_score * 0.25)
            
            # Value assessment (%20)
            value_assessment = ultra_result.relative_value_analysis.get('value_assessment', 'Adil')
            if value_assessment == 'Ucuz':
                value_score = 80
            elif value_assessment == 'Pahalı':
                value_score = 30
            else:
                value_score = 60
            scores.append(value_score * 0.2)
            
            # Interest rate environment (%15)
            ir_trend = ultra_result.interest_rate_environment.central_bank_trend
            if ir_trend == "cutting":
                ir_score = 85  # Good for bonds
            elif ir_trend == "hiking":
                ir_score = 25  # Bad for bonds
            else:
                ir_score = 60
            scores.append(ir_score * 0.15)
            
            return sum(scores)
            
        except Exception:
            return 50.0
    
    def _analyze_curve_insights(self, curve_analysis) -> Dict:
        """Yield curve insights"""
        try:
            insights = {
                'curve_shape': curve_analysis.curve_shape,
                'economic_signal': '',
                'strategy_implication': '',
                'steepness_level': '',
                'recession_probability': 0
            }
            
            # Economic signals
            if curve_analysis.curve_shape == "inverted":
                insights['economic_signal'] = "Recession Warning"
                insights['recession_probability'] = 70
            elif curve_analysis.curve_shape == "flat":
                insights['economic_signal'] = "Economic Uncertainty"
                insights['recession_probability'] = 30
            elif curve_analysis.curve_shape == "normal":
                insights['economic_signal'] = "Healthy Growth"
                insights['recession_probability'] = 10
            else:
                insights['economic_signal'] = "Mixed Signals"
                insights['recession_probability'] = 20
            
            # Steepness
            if abs(curve_analysis.steepness) > 2.0:
                insights['steepness_level'] = "Çok Steep"
            elif abs(curve_analysis.steepness) > 1.0:
                insights['steepness_level'] = "Steep"
            else:
                insights['steepness_level'] = "Flat"
            
            # Strategy implications
            if curve_analysis.steepness > 1.5:
                insights['strategy_implication'] = "Uzun vadeli tahvillerde fırsat"
            elif curve_analysis.steepness < -1.0:
                insights['strategy_implication'] = "Kısa vadeli tahvilleri tercih et"
            else:
                insights['strategy_implication'] = "Barrel strategy uygun"
            
            return insights
            
        except Exception:
            return {'curve_shape': 'normal', 'economic_signal': 'Healthy Growth'}
    
    def _analyze_credit_quality(self, credit_risk) -> Dict:
        """Credit kalite analizi"""
        try:
            # Credit health assessment
            if credit_risk.credit_score >= 80:
                credit_health = "Mükemmel"
                investment_grade = True
            elif credit_risk.credit_score >= 65:
                credit_health = "İyi"
                investment_grade = True
            elif credit_risk.credit_score >= 50:
                credit_health = "Orta"
                investment_grade = True
            elif credit_risk.credit_score >= 35:
                credit_health = "Zayıf"
                investment_grade = False
            else:
                credit_health = "Riskli"
                investment_grade = False
            
            # Default risk assessment
            if credit_risk.default_probability < 0.01:
                default_risk = "Çok Düşük"
            elif credit_risk.default_probability < 0.05:
                default_risk = "Düşük"
            elif credit_risk.default_probability < 0.15:
                default_risk = "Orta"
            else:
                default_risk = "Yüksek"
            
            return {
                'credit_health': credit_health,
                'investment_grade': investment_grade,
                'default_risk_level': default_risk,
                'credit_score': round(credit_risk.credit_score, 1),
                'spread_vs_benchmark': round(credit_risk.credit_spread, 2),
                'financial_strength': round(credit_risk.financial_health_score, 1)
            }
            
        except Exception:
            return {'credit_health': 'Orta', 'investment_grade': True}
    
    def _analyze_duration_risk(self, valuation) -> Dict:
        """Duration risk analizi"""
        try:
            duration = valuation.modified_duration
            
            # Duration risk level
            if duration > 15:
                risk_level = "Çok Yüksek"
                sensitivity = "Extreme"
            elif duration > 10:
                risk_level = "Yüksek"
                sensitivity = "High"
            elif duration > 5:
                risk_level = "Orta"
                sensitivity = "Moderate"
            elif duration > 2:
                risk_level = "Düşük"
                sensitivity = "Low"
            else:
                risk_level = "Çok Düşük"
                sensitivity = "Minimal"
            
            # Price impact calculation
            # 1% rate change impact
            price_impact_1pct = duration
            
            return {
                'duration_risk_level': risk_level,
                'interest_rate_sensitivity': sensitivity,
                'modified_duration': round(duration, 2),
                'convexity': round(valuation.convexity, 2),
                'price_impact_1pct_rate_change': f"{price_impact_1pct:.1f}%",
                'dv01': round(valuation.dv01, 4),
                'recommendation': self._get_duration_recommendation(duration)
            }
            
        except Exception:
            return {'duration_risk_level': 'Orta', 'interest_rate_sensitivity': 'Moderate'}
    
    def _get_duration_recommendation(self, duration: float) -> str:
        """Duration bazlı öneri"""
        if duration > 12:
            return "Yüksek faiz riski - sadece faiz düşüş beklentisi varsa al"
        elif duration > 7:
            return "Orta-yüksek faiz riski - dikkatli pozisyon al"
        elif duration > 3:
            return "Dengeli faiz riski - standart pozisyon uygun"
        else:
            return "Düşük faiz riski - güvenli pozisyon"
    
    def _recommend_bond_strategies(self, ultra_result) -> List[Dict]:
        """Bond investment strategies"""
        try:
            strategies = []
            
            # Duration strategy
            duration = ultra_result.valuation_metrics.modified_duration
            ir_trend = ultra_result.interest_rate_environment.central_bank_trend
            
            if ir_trend == "cutting" and duration > 7:
                strategies.append({
                    'strategy': 'Long Duration Play',
                    'description': 'Faiz düşüş döneminde uzun vadeli tahvillerden faydalanma',
                    'risk_level': 'Orta-Yüksek',
                    'expected_return': '8-15%',
                    'time_horizon': '6-12 ay'
                })
            
            # Credit strategy
            credit_score = ultra_result.credit_risk.credit_score
            if credit_score < 60 and ultra_result.relative_value_analysis.get('value_assessment') == 'Ucuz':
                strategies.append({
                    'strategy': 'Distressed Credit',
                    'description': 'Düşük fiyatlı credit fırsatlarından yararlanma',
                    'risk_level': 'Yüksek',
                    'expected_return': '12-25%',
                    'time_horizon': '1-2 yıl'
                })
            
            # Yield curve strategy
            curve_shape = ultra_result.yield_curve_analysis.curve_shape
            if curve_shape == "steep":
                strategies.append({
                    'strategy': 'Curve Steepener',
                    'description': 'Kısa short, uzun long pozisyon',
                    'risk_level': 'Orta',
                    'expected_return': '5-10%',
                    'time_horizon': '3-6 ay'
                })
            
            # Carry strategy
            ytm = ultra_result.valuation_metrics.yield_to_maturity
            if ytm > 6.0:
                strategies.append({
                    'strategy': 'High Yield Carry',
                    'description': 'Yüksek getirili tahvillerden carry elde etme',
                    'risk_level': 'Orta',
                    'expected_return': f'{ytm:.1f}% annual',
                    'time_horizon': 'Hold to maturity'
                })
            
            return strategies[:3]  # Top 3 strategies
            
        except Exception:
            return [{
                'strategy': 'Buy and Hold',
                'description': 'Vadeye kadar elde tutma',
                'risk_level': 'Düşük'
            }]
    
    def _generate_bond_risk_management(self, ultra_result) -> Dict:
        """Bond risk management"""
        try:
            risk_mgmt = {
                'position_sizing': {},
                'hedging_strategies': [],
                'risk_monitoring': [],
                'stop_loss_levels': {}
            }
            
            # Position sizing
            overall_risk = ultra_result.risk_assessment.get('overall_risk', 'Orta Risk')
            duration = ultra_result.valuation_metrics.modified_duration
            
            if 'Yüksek' in overall_risk or duration > 12:
                position_size = 'Küçük pozisyon (2-5% portföy)'
            elif 'Düşük' in overall_risk and duration < 5:
                position_size = 'Büyük pozisyon (10-20% portföy)'
            else:
                position_size = 'Normal pozisyon (5-10% portföy)'
            
            risk_mgmt['position_sizing'] = {
                'recommended_size': position_size,
                'max_single_bond': '5%',
                'duration_limit': f'Max {duration + 2:.0f} years'
            }
            
            # Hedging strategies
            if duration > 8:
                risk_mgmt['hedging_strategies'].append({
                    'type': 'Duration Hedge',
                    'description': 'Interest rate futures ile hedge',
                    'instruments': 'Treasury futures, interest rate swaps'
                })
            
            credit_score = ultra_result.credit_risk.credit_score
            if credit_score < 60:
                risk_mgmt['hedging_strategies'].append({
                    'type': 'Credit Hedge',
                    'description': 'CDS veya credit hedge',
                    'instruments': 'Credit default swaps, high-grade bonds'
                })
            
            # Risk monitoring
            risk_mgmt['risk_monitoring'] = [
                'Yield curve shifts (daily)',
                'Credit spread changes',
                'Rating agency actions',
                'Central bank policy updates',
                'Economic data releases',
                'Bond price vs fair value'
            ]
            
            # Stop loss levels
            fair_value = ultra_result.valuation_metrics.fair_value
            risk_mgmt['stop_loss_levels'] = {
                'conservative': f'{fair_value * 0.95:.2f} (-5%)',
                'moderate': f'{fair_value * 0.92:.2f} (-8%)',
                'aggressive': f'{fair_value * 0.88:.2f} (-12%)'
            }
            
            return risk_mgmt
            
        except Exception:
            return {
                'position_sizing': {'recommended_size': 'Normal pozisyon'},
                'risk_monitoring': ['Daily price monitoring']
            }
    
    def _generate_bond_summary(self, symbol: str, ultra_result, bond_score: float) -> str:
        """Bond analizi özeti"""
        try:
            # Score assessment
            if bond_score >= 75:
                score_assessment = "mükemmel"
            elif bond_score >= 65:
                score_assessment = "iyi"
            elif bond_score >= 50:
                score_assessment = "orta"
            else:
                score_assessment = "zayıf"
            
            bond_type = ultra_result.bond_profile.bond_type.value
            credit_rating = ultra_result.bond_profile.credit_rating.value
            currency = ultra_result.bond_profile.currency
            
            summary = f"{symbol} tahvil analizi {score_assessment} skorla tamamlandı (%{bond_score:.1f}). "
            summary += f"{bond_type.title()} türü {credit_rating} rating ile {currency} denominasyonu. "
            
            # Yield and duration
            ytm = ultra_result.valuation_metrics.yield_to_maturity
            duration = ultra_result.valuation_metrics.modified_duration
            summary += f"YTM %{ytm:.2f}, duration {duration:.1f} yıl. "
            
            # Interest rate environment
            ir_trend = ultra_result.interest_rate_environment.central_bank_trend
            if ir_trend == "cutting":
                summary += "Faiz indirimi ortamı tahvil fiyatlarını destekliyor. "
            elif ir_trend == "hiking":
                summary += "Faiz artırımı ortamı tahvil fiyatları için olumsuz. "
            else:
                summary += "Sabit faiz ortamı. "
            
            # Yield curve
            curve_shape = ultra_result.yield_curve_analysis.curve_shape
            if curve_shape == "inverted":
                summary += "Ters yield curve resesyon sinyali veriyor. "
            elif curve_shape == "normal":
                summary += "Normal yield curve sağlıklı ekonomik büyüme gösteriyor. "
            
            # Trading recommendation
            recommendation = ultra_result.trading_recommendation
            summary += f"Genel öneri: {recommendation.lower()}."
            
            return summary
            
        except Exception:
            return f"{symbol} için tahvil analizi tamamlandı"
    
    def _get_default_bond_response(self, symbol: str) -> Dict:
        """Varsayılan bond cevabı"""
        return {
            'bond_score': 50.0,
            'analysis_summary': f"{symbol} için tahvil analizi temel parametrelerle tamamlandı",
            'trading_recommendation': 'BEKLE',
            'basic_metrics': {
                'bond_type': 'GOVERNMENT',
                'currency': 'USD',
                'estimated_ytm': 4.5
            },
            'risk_assessment': {
                'overall_risk': 'Orta Risk'
            },
            'confidence': 70.0
        }
