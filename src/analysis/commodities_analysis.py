"""
Commodities Analysis Module
Emtia Analizi Ana Modülü
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# CompanyFoundingDates entegrasyonu
try:
    from ..data.company_founding_dates import CompanyFoundingDates
    FOUNDING_DATES_AVAILABLE = True
    print("INFO: CompanyFoundingDates modülü commodities analysis'e entegre edildi")
except ImportError:
    FOUNDING_DATES_AVAILABLE = False
    print("WARNING: CompanyFoundingDates modülü bulunamadı")

try:
    from .ultra_commodities import UltraCommoditiesAnalyzer
    ULTRA_AVAILABLE = True
    print("INFO: Ultra Commodities Analysis modülü aktif")
except ImportError:
    ULTRA_AVAILABLE = False
    print("WARNING: Ultra Commodities Analysis modülü bulunamadı, temel analiz kullanılacak")

class CommoditiesAnalyzer:
    """Ana commodities analiz sınıfı"""
    
    def __init__(self):
        """Commodities analyzer'ı başlat"""
        # CompanyFoundingDates entegrasyonu
        self.founding_dates = None
        if FOUNDING_DATES_AVAILABLE:
            try:
                self.founding_dates = CompanyFoundingDates()
                print("INFO: CompanyFoundingDates commodities analyzer'a başarıyla entegre edildi")
            except Exception as e:
                print(f"WARNING: CompanyFoundingDates commodities analyzer'a entegre edilemedi: {str(e)}")
        
        self.ultra_analyzer = None
        if ULTRA_AVAILABLE:
            try:
                self.ultra_analyzer = UltraCommoditiesAnalyzer()
                print("INFO: Ultra Commodities Analyzer başarıyla başlatıldı")
            except Exception as e:
                print(f"WARNING: Ultra Commodities Analyzer başlatılamadı: {str(e)}")
        
        # Temel emtia kategorileri
        self.commodity_categories = {
            'ENERGY': ['OIL', 'GAS', 'CRUDE', 'BRENT'],
            'METALS': ['GOLD', 'SILVER', 'COPPER', 'PLATINUM'],
            'AGRICULTURE': ['WHEAT', 'CORN', 'SOYA', 'SUGAR'],
            'LIVESTOCK': ['CATTLE', 'HOGS']
        }
        
        # Basit volatilite mapping
        self.volatility_expectations = {
            'ENERGY': 0.35, 'METALS': 0.22, 'AGRICULTURE': 0.28, 'LIVESTOCK': 0.25
        }
    
    def analyze_commodity(self, symbol: str, current_price: float = None,
                         historical_data: Optional[pd.DataFrame] = None, **kwargs) -> Dict:
        """Kapsamlı commodity analizi"""
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
                result = self._ultra_commodity_analysis(symbol, current_price, historical_data, **kwargs)
                # Founding date bilgisini ekle
                result['founding_date_info'] = founding_info
                if founding_date:
                    result['founding_date'] = founding_date
                return result
            else:
                result = self._basic_commodity_analysis(symbol, current_price, historical_data, **kwargs)
                # Founding date bilgisini ekle
                result['founding_date_info'] = founding_info
                if founding_date:
                    result['founding_date'] = founding_date
                return result
                
        except Exception as e:
            print(f"ERROR: Commodity analizi hatası: {str(e)}")
            return self._get_default_commodity_response(symbol, current_price)
    
    def _ultra_commodity_analysis(self, symbol: str, current_price: float,
                                 historical_data: Optional[pd.DataFrame], **kwargs) -> Dict:
        """Ultra gelişmiş commodity analizi"""
        try:
            # Ana commodity analizi
            result = self.ultra_analyzer.analyze_commodity(
                symbol=symbol,
                current_price=current_price,
                historical_data=historical_data,
                **kwargs
            )
            
            # Commodity score hesaplama
            commodity_score = self._calculate_commodity_score(result)
            
            # Market cycle analizi
            market_cycle = self._analyze_commodity_cycle(result, historical_data)
            
            # Supply chain analizi
            supply_chain = self._analyze_supply_chain(result)
            
            # Investment strategies
            investment_strategies = self._recommend_commodity_strategies(result, market_cycle)
            
            # Risk management
            risk_management = self._generate_commodity_risk_management(result)
            
            return {
                'commodity_score': round(commodity_score, 1),
                'analysis_summary': self._generate_commodity_summary(
                    symbol, result, commodity_score
                ),
                'trading_recommendation': result.trading_recommendation,
                'ultra_analysis': {
                    'ultra_commodity_score': result.ultra_commodity_score,
                    'commodity_type': result.commodity_profile.commodity_type.value,
                    'supply_demand': {
                        'balance_score': result.supply_demand.balance_score,
                        'supply_growth': round(result.supply_demand.supply_growth_rate, 2),
                        'demand_growth': round(result.supply_demand.demand_growth_rate, 2),
                        'inventory_ratio': round(result.supply_demand.inventory_to_usage_ratio, 2),
                        'supply_risk': round(result.supply_demand.supply_disruption_risk * 100, 1),
                        'demand_shock_risk': round(result.supply_demand.demand_shock_probability * 100, 1)
                    },
                    'macro_factors': {
                        'global_gdp_growth': round(result.macro_factors.global_gdp_growth, 2),
                        'dollar_strength': round(result.macro_factors.dollar_strength_index, 1),
                        'inflation_expectations': round(result.macro_factors.inflation_expectations, 2),
                        'china_pmi': round(result.macro_factors.china_pmi, 1),
                        'geopolitical_risk': round(result.macro_factors.geopolitical_risk_score, 1)
                    },
                    'price_forecast': {
                        '1_month': round(result.price_forecast.get('1_month', current_price or 100), 2),
                        '3_months': round(result.price_forecast.get('3_months', current_price or 100), 2),
                        '6_months': round(result.price_forecast.get('6_months', current_price or 100), 2)
                    }
                },
                'volatility_analysis': {
                    'realized_volatility': round(result.volatility_analysis.get('realized_volatility', 0.25) * 100, 2),
                    'volatility_regime': result.volatility_analysis.get('volatility_regime', 'normal'),
                    'vol_percentile': round(result.volatility_analysis.get('volatility_percentile', 50), 1)
                },
                'seasonality': result.seasonal_patterns,
                'market_cycle': market_cycle,
                'supply_chain': supply_chain,
                'investment_strategies': investment_strategies,
                'risk_management': risk_management,
                'technical_signals': result.technical_signals,
                'fundamental_signals': result.fundamental_signals,
                'risk_assessment': result.risk_assessment,
                'confidence': round(np.mean([
                    85.0 if result.ultra_commodity_score > 70 else 75.0,
                    90.0 if result.risk_assessment.get('overall_risk') == 'Düşük Risk' else 70.0,
                    80.0
                ]), 1)
            }
            
        except Exception as e:
            print(f"ERROR: Ultra commodity analizi hatası: {str(e)}")
            return self._basic_commodity_analysis(symbol, current_price, historical_data, **kwargs)
    
    def _basic_commodity_analysis(self, symbol: str, current_price: float,
                                 historical_data: Optional[pd.DataFrame], **kwargs) -> Dict:
        """Temel commodity analizi"""
        try:
            # Commodity category belirleme
            category = 'ENERGY'  # Default
            for cat, symbols in self.commodity_categories.items():
                if any(sym in symbol.upper() for sym in symbols):
                    category = cat
                    break
            
            # Basit volatilite hesaplama
            expected_vol = self.volatility_expectations.get(category, 0.25)
            if historical_data is not None and len(historical_data) > 20:
                returns = historical_data['Close'].pct_change(fill_method=None).dropna()
                realized_vol = returns.std() * np.sqrt(252)
            else:
                realized_vol = expected_vol
            
            # Basit supply-demand score
            supply_demand_score = np.random.uniform(40, 80)  # Simulated
            
            # Basit commodity score
            commodity_score = np.mean([
                supply_demand_score,
                70 if category in ['METALS', 'ENERGY'] else 60,  # Category premium
                60 if realized_vol < expected_vol * 1.2 else 40,  # Volatility penalty
                65  # Base score
            ])
            
            # Basit trading recommendation
            if commodity_score >= 70:
                recommendation = "ALIŞ"
            elif commodity_score >= 50:
                recommendation = "BEKLE"
            else:
                recommendation = "SAT"
            
            return {
                'commodity_score': round(commodity_score, 1),
                'analysis_summary': f"{symbol} emtia analizi: {category} kategorisi, temel analiz ile değerlendirildi",
                'trading_recommendation': recommendation,
                'basic_metrics': {
                    'category': category,
                    'expected_volatility': round(expected_vol * 100, 2),
                    'realized_volatility': round(realized_vol * 100, 2),
                    'supply_demand_score': round(supply_demand_score, 1),
                    'current_price': current_price or 100.0
                },
                'risk_assessment': {
                    'overall_risk': 'Yüksek' if realized_vol > expected_vol * 1.5 else 'Orta' if realized_vol > expected_vol * 1.2 else 'Düşük',
                    'volatility_risk': 'Yüksek' if realized_vol > 0.4 else 'Orta' if realized_vol > 0.25 else 'Düşük',
                    'category_risk': 'Yüksek' if category == 'ENERGY' else 'Orta'
                },
                'confidence': 70.0
            }
            
        except Exception as e:
            print(f"ERROR: Temel commodity analizi hatası: {str(e)}")
            return self._get_default_commodity_response(symbol, current_price)
    
    def _calculate_commodity_score(self, ultra_result) -> float:
        """Genel commodity skoru hesaplama"""
        try:
            scores = []
            
            # Ultra commodity score (%50)
            scores.append(ultra_result.ultra_commodity_score * 0.5)
            
            # Supply-demand balance (%25)
            scores.append(ultra_result.supply_demand.balance_score * 0.25)
            
            # Macro environment (%15)
            macro_score = 50 + (ultra_result.macro_factors.global_gdp_growth - 2.0) * 10
            macro_score = max(0, min(100, macro_score))
            scores.append(macro_score * 0.15)
            
            # Risk adjustment (%10)
            risk_score = 80 if ultra_result.risk_assessment.get('overall_risk') == 'Düşük Risk' else 50 if 'Orta' in ultra_result.risk_assessment.get('overall_risk', '') else 20
            scores.append(risk_score * 0.1)
            
            return sum(scores)
            
        except Exception:
            return 50.0
    
    def _analyze_commodity_cycle(self, ultra_result, historical_data: Optional[pd.DataFrame]) -> Dict:
        """Commodity market cycle analizi"""
        try:
            # Supply-demand cycle
            sd_balance = ultra_result.supply_demand.balance_score
            if sd_balance > 70:
                cycle_phase = "Boom (Yüksek Talep)"
            elif sd_balance > 50:
                cycle_phase = "Büyüme"
            elif sd_balance > 30:
                cycle_phase = "Durgunluk"
            else:
                cycle_phase = "Çöküş (Arz Fazlası)"
            
            # Price cycle
            price_forecast = ultra_result.price_forecast
            price_trend = "Yükseliş" if price_forecast.get('6_months', 100) > price_forecast.get('1_month', 100) else "Düşüş"
            
            return {
                'cycle_phase': cycle_phase,
                'price_trend': price_trend,
                'cycle_strength': 'Güçlü' if abs(sd_balance - 50) > 20 else 'Orta',
                'cycle_duration_estimate': '6-12 ay',
                'next_phase_probability': {
                    'Boom': 20 if cycle_phase == "Büyüme" else 5,
                    'Büyüme': 30 if cycle_phase in ["Durgunluk", "Boom"] else 10,
                    'Durgunluk': 30 if cycle_phase == "Büyüme" else 20,
                    'Çöküş': 15 if cycle_phase == "Durgunluk" else 5
                }
            }
            
        except Exception:
            return {'cycle_phase': 'Belirsiz', 'price_trend': 'Yatay'}
    
    def _analyze_supply_chain(self, ultra_result) -> Dict:
        """Supply chain analizi"""
        try:
            profile = ultra_result.commodity_profile
            supply_demand = ultra_result.supply_demand
            
            # Supply chain risk
            if profile.geopolitical_sensitivity > 0.7:
                supply_chain_risk = "Yüksek"
            elif profile.geopolitical_sensitivity > 0.4:
                supply_chain_risk = "Orta"
            else:
                supply_chain_risk = "Düşük"
            
            # Key supply regions (simulated)
            supply_regions = {
                'energy': ['Middle East', 'Russia', 'US', 'Canada'],
                'precious': ['South Africa', 'Australia', 'Russia', 'Canada'],
                'base': ['Chile', 'China', 'Australia', 'Peru'],
                'agriculture': ['US', 'Brazil', 'Argentina', 'Ukraine']
            }.get(profile.commodity_type.value, ['Global'])
            
            return {
                'supply_chain_risk': supply_chain_risk,
                'key_supply_regions': supply_regions[:3],
                'supply_concentration': 'Yüksek' if len(supply_regions) <= 3 else 'Orta',
                'transportation_risk': 'Yüksek' if profile.commodity_type.value == 'energy' else 'Orta',
                'storage_capacity': 'Yüksek' if profile.is_storable else 'Düşük',
                'supply_elasticity': profile.supply_elasticity,
                'demand_elasticity': abs(profile.demand_elasticity)
            }
            
        except Exception:
            return {'supply_chain_risk': 'Orta'}
    
    def _recommend_commodity_strategies(self, ultra_result, market_cycle: Dict) -> List[Dict]:
        """Commodity investment strategies"""
        try:
            strategies = []
            
            # Trend following
            if ultra_result.ultra_commodity_score > 60:
                strategies.append({
                    'strategy': 'Long Commodity Trend',
                    'description': f'Pozitif trend ve fundamentals ile long pozisyon',
                    'risk_level': 'Orta',
                    'time_horizon': '3-6 ay',
                    'expected_return': '8-15%'
                })
            
            # Contango/Backwardation play
            cycle_phase = market_cycle.get('cycle_phase', '')
            if 'Boom' in cycle_phase or 'Büyüme' in cycle_phase:
                strategies.append({
                    'strategy': 'Backwardation Play',
                    'description': 'Near-month futures long, far-month short',
                    'risk_level': 'Yüksek',
                    'time_horizon': '1-3 ay',
                    'expected_return': '5-12%'
                })
            
            # Seasonal play
            seasonal = ultra_result.seasonal_patterns
            if seasonal.get('current_month_bias') == 'Pozitif':
                strategies.append({
                    'strategy': 'Seasonal Trade',
                    'description': f'Seasonal güçlü dönem trade',
                    'risk_level': 'Düşük',
                    'time_horizon': '1-2 ay',
                    'expected_return': '3-8%'
                })
            
            # Volatility strategy
            vol_regime = ultra_result.volatility_analysis.get('volatility_regime', 'normal')
            if vol_regime in ['high', 'extreme']:
                strategies.append({
                    'strategy': 'Volatility Trading',
                    'description': 'Yüksek volatilitede range/swing trading',
                    'risk_level': 'Yüksek',
                    'time_horizon': '2-4 hafta',
                    'expected_return': '10-20%'
                })
            
            return strategies[:3]  # Top 3 strategies
            
        except Exception:
            return [{
                'strategy': 'Conservative Hold',
                'description': 'Mevcut pozisyonu koru',
                'risk_level': 'Düşük'
            }]
    
    def _generate_commodity_risk_management(self, ultra_result) -> Dict:
        """Commodity risk management"""
        try:
            risk_mgmt = {
                'position_sizing': {},
                'hedging_strategies': [],
                'risk_factors': [],
                'monitoring_points': []
            }
            
            # Position sizing
            overall_risk = ultra_result.risk_assessment.get('overall_risk', 'Orta Risk')
            vol_regime = ultra_result.volatility_analysis.get('volatility_regime', 'normal')
            
            if 'Yüksek' in overall_risk or vol_regime in ['high', 'extreme']:
                position_size = 'Küçük pozisyon (1-3% risk)'
                max_exposure = '5%'
            elif 'Düşük' in overall_risk and vol_regime == 'low':
                position_size = 'Normal pozisyon (3-7% risk)'
                max_exposure = '15%'
            else:
                position_size = 'Orta pozisyon (2-5% risk)'
                max_exposure = '10%'
            
            risk_mgmt['position_sizing'] = {
                'recommended_size': position_size,
                'max_portfolio_exposure': max_exposure,
                'leverage_recommendation': 'Düşük (1:2-1:5)' if 'Yüksek' in overall_risk else 'Orta (1:5-1:10)'
            }
            
            # Hedging strategies
            commodity_type = ultra_result.commodity_profile.commodity_type.value
            
            if commodity_type == 'energy':
                risk_mgmt['hedging_strategies'].append({
                    'type': 'Dollar Hedge',
                    'description': 'USD güçlenmesine karşı hedge',
                    'instruments': 'DXY short, EUR/USD long'
                })
            
            if ultra_result.supply_demand.supply_disruption_risk > 0.3:
                risk_mgmt['hedging_strategies'].append({
                    'type': 'Supply Shock Hedge',
                    'description': 'Arz kesintisi riskine karşı protection',
                    'instruments': 'Call options, related commodities'
                })
            
            # Risk factors
            risk_mgmt['risk_factors'] = [
                f"Jeopolitik risk: {ultra_result.risk_assessment.get('geopolitical_risk', 'Orta')}",
                f"Arz riski: {ultra_result.risk_assessment.get('supply_risk', 'Orta')}",
                f"Talep riski: {ultra_result.risk_assessment.get('demand_risk', 'Orta')}",
                f"Volatilite riski: {ultra_result.risk_assessment.get('volatility_risk', 'Orta')}"
            ]
            
            # Monitoring points
            risk_mgmt['monitoring_points'] = [
                'Supply-demand rapor günleri',
                'Merkez bankası toplantıları (USD impact)',
                'Jeopolitik gelişmeler',
                'Hava durumu (agriculture için)',
                'Çin PMI ve economic data',
                'Stok seviyeleri (inventory reports)'
            ]
            
            return risk_mgmt
            
        except Exception:
            return {
                'position_sizing': {'recommended_size': 'Orta pozisyon'},
                'risk_factors': ['Genel piyasa riski']
            }
    
    def _generate_commodity_summary(self, symbol: str, ultra_result, commodity_score: float) -> str:
        """Commodity analizi özeti"""
        try:
            # Score assessment
            if commodity_score >= 75:
                score_assessment = "mükemmel"
            elif commodity_score >= 65:
                score_assessment = "iyi"
            elif commodity_score >= 50:
                score_assessment = "orta"
            else:
                score_assessment = "zayıf"
            
            commodity_type = ultra_result.commodity_profile.commodity_type.value
            
            summary = f"{symbol} emtia analizi {score_assessment} skorla tamamlandı (%{commodity_score:.1f}). "
            summary += f"{commodity_type.title()} kategorisinde değerlendirme yapıldı. "
            
            # Supply-demand
            sd_balance = ultra_result.supply_demand.balance_score
            if sd_balance > 60:
                summary += "Talep arzdan güçlü, "
            elif sd_balance < 40:
                summary += "Arz fazlası mevcut, "
            else:
                summary += "Arz-talep dengeli, "
            
            # Volatility
            vol_regime = ultra_result.volatility_analysis.get('volatility_regime', 'normal')
            if vol_regime in ['high', 'extreme']:
                summary += "yüksek volatilite nedeniyle dikkatli pozisyon önerisi. "
            elif vol_regime == 'low':
                summary += "düşük volatilite ortamı pozisyon artırmaya uygun. "
            else:
                summary += "normal volatilite seviyesi. "
            
            # Trading recommendation
            recommendation = ultra_result.trading_recommendation
            summary += f"Genel öneri: {recommendation.lower()}."
            
            return summary
            
        except Exception:
            return f"{symbol} için commodity analizi tamamlandı"
    
    def _get_default_commodity_response(self, symbol: str, current_price: float) -> Dict:
        """Varsayılan commodity cevabı"""
        return {
            'commodity_score': 50.0,
            'analysis_summary': f"{symbol} için commodity analizi temel parametrelerle tamamlandı",
            'trading_recommendation': 'BEKLE',
            'basic_metrics': {
                'symbol': symbol,
                'current_price': current_price or 100.0,
                'category': 'GENEL'
            },
            'risk_assessment': {
                'overall_risk': 'Orta Risk'
            },
            'confidence': 70.0
        }
