"""
Currency Analysis Module
Para birimi analizi ana modülü

Bu modül ultra currency analyzer ile entegrasyon sağlar ve
temel forex analiz fonksiyonalitesi sunar.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# CompanyFoundingDates entegrasyonu
try:
    from ..data.company_founding_dates import CompanyFoundingDates
    FOUNDING_DATES_AVAILABLE = True
    print("INFO: CompanyFoundingDates modülü currency analysis'e entegre edildi")
except ImportError:
    FOUNDING_DATES_AVAILABLE = False
    print("WARNING: CompanyFoundingDates modülü bulunamadı")

try:
    from .ultra_currency import UltraCurrencyAnalyzer
    ULTRA_AVAILABLE = True
    print("INFO: Ultra Currency Analysis modülü aktif")
except ImportError:
    ULTRA_AVAILABLE = False
    print("WARNING: Ultra Currency Analysis modülü bulunamadı, temel analiz kullanılacak")

class CurrencyAnalyzer:
    """Ana currency analiz sınıfı"""
    
    def __init__(self):
        """Currency analyzer'ı başlat"""
        # CompanyFoundingDates entegrasyonu
        self.founding_dates = None
        if FOUNDING_DATES_AVAILABLE:
            try:
                self.founding_dates = CompanyFoundingDates()
                print("INFO: CompanyFoundingDates currency analyzer'a başarıyla entegre edildi")
            except Exception as e:
                print(f"WARNING: CompanyFoundingDates currency analyzer'a entegre edilemedi: {str(e)}")
        
        self.ultra_analyzer = None
        if ULTRA_AVAILABLE:
            try:
                self.ultra_analyzer = UltraCurrencyAnalyzer()
                print("INFO: Ultra Currency Analyzer başarıyla başlatıldı")
            except Exception as e:
                print(f"WARNING: Ultra Currency Analyzer başlatılamadı: {str(e)}")
        
        # Temel forex parametreleri
        self.major_pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'AUDUSD', 'USDCAD', 'NZDUSD']
        self.safe_haven_currencies = ['USD', 'JPY', 'CHF']
        self.risk_currencies = ['AUD', 'NZD', 'CAD']
        
        # Basit interest rate mapping
        self.interest_rates = {
            'USD': 5.25, 'EUR': 4.0, 'GBP': 5.0, 'JPY': 0.1,
            'CHF': 1.25, 'AUD': 4.35, 'CAD': 4.75, 'NZD': 5.5, 'TRY': 50.0
        }
    
    def analyze_currency(self, symbol: str, current_rate: float = None,
                        historical_data: Optional[pd.DataFrame] = None, **kwargs) -> Dict:
        """Kapsamlı currency analizi"""
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
                result = self._ultra_currency_analysis(symbol, current_rate, historical_data, **kwargs)
                # Founding date bilgisini ekle
                result['founding_date_info'] = founding_info
                if founding_date:
                    result['founding_date'] = founding_date
                return result
            else:
                result = self._basic_currency_analysis(symbol, current_rate, historical_data, **kwargs)
                # Founding date bilgisini ekle
                result['founding_date_info'] = founding_info
                if founding_date:
                    result['founding_date'] = founding_date
                return result
                
        except Exception as e:
            print(f"ERROR: Currency analizi hatası: {str(e)}")
            return self._get_default_currency_response(symbol, current_rate)
    
    def _ultra_currency_analysis(self, symbol: str, current_rate: float,
                                historical_data: Optional[pd.DataFrame], **kwargs) -> Dict:
        """Ultra gelişmiş currency analizi"""
        try:
            # Ana currency pair analizi
            result = self.ultra_analyzer.analyze_currency_pair(
                symbol=symbol,
                current_rate=current_rate,
                historical_data=historical_data,
                **kwargs
            )
            
            # Currency basket analizi
            base_currency = symbol[:3] if len(symbol) >= 6 else 'USD'
            quote_currency = symbol[3:] if len(symbol) >= 6 else 'EUR'
            
            basket_currencies = [base_currency, quote_currency, 'USD', 'EUR']
            basket_currencies = list(set(basket_currencies))  # Remove duplicates
            
            basket_analysis = self.ultra_analyzer.analyze_currency_basket(basket_currencies)
            
            # Risk-on/Risk-off analizi
            risk_sentiment = self._analyze_risk_sentiment(result)
            
            # Seasonality analizi
            seasonality_analysis = self._analyze_currency_seasonality(symbol, historical_data)
            
            # Central bank calendar
            cb_calendar = self._get_central_bank_calendar(base_currency, quote_currency)
            
            # Currency score hesaplama
            currency_score = self._calculate_currency_score(result, basket_analysis, risk_sentiment)
            
            # Trading strategy önerileri
            strategy_recommendations = self._recommend_currency_strategies(
                result, risk_sentiment, seasonality_analysis
            )
            
            # Risk management
            risk_management = self._generate_currency_risk_management(
                result, basket_analysis
            )
            
            return {
                'currency_score': round(currency_score, 1),
                'analysis_summary': self._generate_currency_summary(
                    symbol, result, currency_score
                ),
                'trading_recommendation': result.trading_recommendation,
                'ultra_analysis': {
                    'ultra_currency_score': result.ultra_currency_score,
                    'trading_recommendation': result.trading_recommendation,
                    'carry_trade': {
                        'rate_differential': result.carry_trade_analysis.interest_rate_differential,
                        'carry_yield': round(result.carry_trade_analysis.carry_yield * 100, 2),
                        'risk_adjusted_carry': round(result.carry_trade_analysis.risk_adjusted_carry * 100, 2),
                        'sharpe_ratio': round(result.carry_trade_analysis.sharpe_ratio, 2)
                    },
                    'central_bank': {
                        'rate_trajectory': result.central_bank_analysis.rate_trajectory,
                        'policy_divergence': round(result.central_bank_analysis.policy_divergence_score, 1),
                        'next_meeting': result.central_bank_analysis.next_meeting_date
                    },
                    'macro_indicators': {
                        'gdp_growth': result.macro_analysis.gdp_growth,
                        'inflation_rate': result.macro_analysis.inflation_rate,
                        'economic_momentum': result.macro_analysis.economic_momentum_score
                    }
                },
                'volatility_analysis': {
                    'realized_vol': round(result.volatility_model.realized_volatility * 100, 2),
                    'implied_vol': round(result.volatility_model.implied_volatility * 100, 2),
                    'vol_regime': result.volatility_model.vol_regime,
                    'vol_forecast': {k: round(v * 100, 2) for k, v in result.volatility_model.volatility_forecast.items()}
                },
                'risk_assessment': result.risk_assessment,
                'basket_analysis': basket_analysis,
                'risk_sentiment': risk_sentiment,
                'seasonality': seasonality_analysis,
                'central_bank_calendar': cb_calendar,
                'strategy_recommendations': strategy_recommendations,
                'risk_management': risk_management,
                'technical_signals': result.technical_signals,
                'fundamental_signals': result.fundamental_signals,
                'confidence': round(np.mean([
                    85.0 if result.ultra_currency_score > 70 else 75.0,
                    90.0 if result.risk_assessment.get('overall_risk') == 'Düşük Risk' else 70.0,
                    80.0
                ]), 1)
            }
            
        except Exception as e:
            print(f"ERROR: Ultra currency analizi hatası: {str(e)}")
            return self._basic_currency_analysis(symbol, current_rate, historical_data, **kwargs)
    
    def _basic_currency_analysis(self, symbol: str, current_rate: float,
                                historical_data: Optional[pd.DataFrame], **kwargs) -> Dict:
        """Temel currency analizi"""
        try:
            base_currency = symbol[:3] if len(symbol) >= 6 else 'USD'
            quote_currency = symbol[3:] if len(symbol) >= 6 else 'EUR'
            
            # Basit interest rate differential
            base_rate = self.interest_rates.get(base_currency, 2.0)
            quote_rate = self.interest_rates.get(quote_currency, 2.0)
            rate_differential = base_rate - quote_rate
            
            # Basit volatilite hesaplama
            if historical_data is not None and len(historical_data) > 20:
                returns = historical_data['Close'].pct_change(fill_method=None).dropna()
                volatility = returns.std() * np.sqrt(252) * 100  # Annualized %
            else:
                volatility = 12.0  # Default 12%
            
            # Currency type classification
            base_type = 'Safe Haven' if base_currency in self.safe_haven_currencies else 'Risk Currency'
            quote_type = 'Safe Haven' if quote_currency in self.safe_haven_currencies else 'Risk Currency'
            
            # Basit carry trade score
            carry_score = 50 + (rate_differential * 5)  # Simple mapping
            carry_score = max(0, min(100, carry_score))
            
            # Basit currency score
            currency_score = np.mean([
                carry_score,
                50 + (rate_differential * 3),  # Rate advantage
                75 if symbol in self.major_pairs else 60,  # Liquidity
                60 if volatility < 15 else 40  # Volatility penalty
            ])
            
            # Basit trading recommendation
            if rate_differential > 2:
                recommendation = "SATIN AL" if volatility < 20 else "DİKKATLİ AL"
            elif rate_differential < -2:
                recommendation = "SAT" if volatility < 20 else "DİKKATLİ SAT"
            else:
                recommendation = "BEKLE"
            
            return {
                'currency_score': round(currency_score, 1),
                'analysis_summary': f"{symbol} pair analizi: {base_currency} ({base_type}) vs {quote_currency} ({quote_type}), temel analiz ile değerlendirildi",
                'basic_metrics': {
                    'base_currency': base_currency,
                    'quote_currency': quote_currency,
                    'interest_rate_differential': round(rate_differential, 2),
                    'base_rate': base_rate,
                    'quote_rate': quote_rate,
                    'volatility': round(volatility, 2),
                    'currency_types': f"{base_type} vs {quote_type}",
                    'is_major_pair': symbol in self.major_pairs
                },
                'carry_trade': {
                    'annual_carry': round(rate_differential, 2),
                    'carry_score': round(carry_score, 1),
                    'attractiveness': 'Yüksek' if abs(rate_differential) > 3 else 'Orta' if abs(rate_differential) > 1 else 'Düşük'
                },
                'risk_assessment': {
                    'overall_risk': 'Yüksek' if volatility > 20 else 'Orta' if volatility > 12 else 'Düşük',
                    'volatility_risk': 'Yüksek' if volatility > 18 else 'Orta',
                    'liquidity_risk': 'Düşük' if symbol in self.major_pairs else 'Orta'
                },
                'trading_recommendation': recommendation,
                'confidence': 70.0
            }
            
        except Exception as e:
            print(f"ERROR: Temel currency analizi hatası: {str(e)}")
            return self._get_default_currency_response(symbol, current_rate)
    
    def _analyze_risk_sentiment(self, ultra_result) -> Dict:
        """Risk sentiment analizi"""
        try:
            # Safe haven vs risk currency analizi
            base_curr = ultra_result.currency_pair.base_currency
            quote_curr = ultra_result.currency_pair.quote_currency
            
            # Risk-on/Risk-off scoring
            if base_curr in self.safe_haven_currencies and quote_curr in self.risk_currencies:
                pair_bias = "Risk-Off Favors Base"
            elif base_curr in self.risk_currencies and quote_curr in self.safe_haven_currencies:
                pair_bias = "Risk-On Favors Base"
            else:
                pair_bias = "Mixed Sentiment"
            
            # Volatilite bazlı risk sentiment
            vol_regime = ultra_result.volatility_model.vol_regime
            if vol_regime in ['high', 'extreme']:
                market_sentiment = "Risk-Off"
            elif vol_regime == 'low':
                market_sentiment = "Risk-On"
            else:
                market_sentiment = "Neutral"
            
            # Carry trade sentiment
            carry_yield = ultra_result.carry_trade_analysis.carry_yield
            if carry_yield > 0.03:
                carry_sentiment = "Risk-On (Carry Favorable)"
            elif carry_yield < -0.03:
                carry_sentiment = "Risk-Off (Carry Unfavorable)"
            else:
                carry_sentiment = "Neutral"
            
            return {
                'pair_bias': pair_bias,
                'market_sentiment': market_sentiment,
                'carry_sentiment': carry_sentiment,
                'risk_score': self._calculate_risk_score(vol_regime, carry_yield),
                'sentiment_recommendation': self._get_sentiment_recommendation(
                    market_sentiment, carry_sentiment, pair_bias
                )
            }
            
        except Exception as e:
            print(f"ERROR: Risk sentiment analiz hatası: {str(e)}")
            return {
                'market_sentiment': 'Neutral',
                'carry_sentiment': 'Neutral',
                'risk_score': 50
            }
    
    def _calculate_risk_score(self, vol_regime: str, carry_yield: float) -> float:
        """Risk skoru hesaplama"""
        try:
            # Volatilite component
            vol_scores = {'low': 85, 'normal': 65, 'high': 35, 'extreme': 15}
            vol_score = vol_scores.get(vol_regime, 50)
            
            # Carry component
            carry_score = 50 + (carry_yield * 1000)  # Scale carry yield
            carry_score = max(0, min(100, carry_score))
            
            # Combined risk score
            return (vol_score * 0.6 + carry_score * 0.4)
            
        except Exception:
            return 50.0
    
    def _get_sentiment_recommendation(self, market_sentiment: str, carry_sentiment: str, pair_bias: str) -> str:
        """Sentiment bazlı öneri"""
        try:
            if market_sentiment == "Risk-On" and "Risk-On" in carry_sentiment:
                return "Risk varlıkları favor, carry trade pozisyonları artırılabilir"
            elif market_sentiment == "Risk-Off" and "Risk-Off" in carry_sentiment:
                return "Safe haven varlıkları favor, carry pozisyonları azaltılmalı"
            elif market_sentiment == "Risk-On" and "Risk-Off" in carry_sentiment:
                return "Karışık sinyaller, dikkatli pozisyon alınmalı"
            else:
                return "Nötr sentiment, trend takip stratejisi uygun"
                
        except Exception:
            return "Standart risk yönetimi uygulanmalı"
    
    def _analyze_currency_seasonality(self, symbol: str, historical_data: Optional[pd.DataFrame]) -> Dict:
        """Currency seasonality analizi"""
        try:
            if historical_data is None or len(historical_data) < 252:
                return {
                    'monthly_patterns': 'Yetersiz veri',
                    'current_month_bias': 'Belirsiz',
                    'seasonal_strength': 0
                }
            
            # Monthly returns analizi
            data = historical_data.copy()
            data['Date'] = pd.to_datetime(data.index) if 'Date' not in data.columns else pd.to_datetime(data['Date'])
            data['Month'] = data['Date'].dt.month
            data['Returns'] = data['Close'].pct_change(fill_method=None)
            
            # Aylık average return
            monthly_avg = data.groupby('Month')['Returns'].mean()
            
            # Mevcut ay
            current_month = datetime.now().month
            current_month_bias = 'Pozitif' if monthly_avg.get(current_month, 0) > 0 else 'Negatif'
            
            # En güçlü ve zayıf aylar
            best_month = monthly_avg.idxmax()
            worst_month = monthly_avg.idxmin()
            
            # Seasonal strength
            seasonal_strength = (monthly_avg.max() - monthly_avg.min()) * 100  # As percentage
            
            return {
                'monthly_patterns': {
                    'best_month': best_month,
                    'worst_month': worst_month,
                    'best_month_return': round(monthly_avg.max() * 100, 2),
                    'worst_month_return': round(monthly_avg.min() * 100, 2)
                },
                'current_month_bias': current_month_bias,
                'current_month_return': round(monthly_avg.get(current_month, 0) * 100, 2),
                'seasonal_strength': round(seasonal_strength, 2),
                'seasonality_significance': 'Güçlü' if seasonal_strength > 2 else 'Orta' if seasonal_strength > 1 else 'Zayıf'
            }
            
        except Exception as e:
            print(f"ERROR: Seasonality analiz hatası: {str(e)}")
            return {'seasonal_strength': 0, 'current_month_bias': 'Belirsiz'}
    
    def _get_central_bank_calendar(self, base_currency: str, quote_currency: str) -> Dict:
        """Merkez bankası takvimi"""
        try:
            # Basit CB meeting calendar (gerçekte API'den gelir)
            cb_meetings = {
                'USD': {'next_meeting': '2025-01-29', 'meeting_type': 'FOMC', 'expected_action': 'Hold'},
                'EUR': {'next_meeting': '2025-01-23', 'meeting_type': 'ECB', 'expected_action': 'Hold'},
                'GBP': {'next_meeting': '2025-02-06', 'meeting_type': 'BoE', 'expected_action': 'Hold'},
                'JPY': {'next_meeting': '2025-01-24', 'meeting_type': 'BoJ', 'expected_action': 'Hold'},
                'CHF': {'next_meeting': '2025-03-20', 'meeting_type': 'SNB', 'expected_action': 'Hold'},
                'AUD': {'next_meeting': '2025-02-04', 'meeting_type': 'RBA', 'expected_action': 'Cut'},
                'CAD': {'next_meeting': '2025-01-29', 'meeting_type': 'BoC', 'expected_action': 'Cut'},
                'TRY': {'next_meeting': '2025-01-23', 'meeting_type': 'CBRT', 'expected_action': 'Hold'}
            }
            
            base_meeting = cb_meetings.get(base_currency, {})
            quote_meeting = cb_meetings.get(quote_currency, {})
            
            return {
                'base_currency_meeting': {
                    'currency': base_currency,
                    'next_meeting': base_meeting.get('next_meeting', 'TBD'),
                    'meeting_type': base_meeting.get('meeting_type', 'Unknown'),
                    'expected_action': base_meeting.get('expected_action', 'Unknown')
                },
                'quote_currency_meeting': {
                    'currency': quote_currency,
                    'next_meeting': quote_meeting.get('next_meeting', 'TBD'),
                    'meeting_type': quote_meeting.get('meeting_type', 'Unknown'),
                    'expected_action': quote_meeting.get('expected_action', 'Unknown')
                },
                'upcoming_events': [
                    f"{base_currency} {base_meeting.get('meeting_type', 'CB')} - {base_meeting.get('next_meeting', 'TBD')}",
                    f"{quote_currency} {quote_meeting.get('meeting_type', 'CB')} - {quote_meeting.get('next_meeting', 'TBD')}"
                ]
            }
            
        except Exception as e:
            print(f"ERROR: CB takvim hatası: {str(e)}")
            return {'upcoming_events': ['Takvim bilgisi mevcut değil']}
    
    def _calculate_currency_score(self, ultra_result, basket_analysis: Dict, risk_sentiment: Dict) -> float:
        """Genel currency skoru hesaplama"""
        try:
            scores = []
            
            # Ultra currency score (%40)
            scores.append(ultra_result.ultra_currency_score * 0.4)
            
            # Basket score (%20)
            basket_score = basket_analysis.get('basket_score', 50)
            scores.append(basket_score * 0.2)
            
            # Risk sentiment score (%20)
            risk_score = risk_sentiment.get('risk_score', 50)
            scores.append(risk_score * 0.2)
            
            # Volatilite adjustment (%20)
            vol_regime = ultra_result.volatility_model.vol_regime
            vol_scores = {'low': 85, 'normal': 70, 'high': 45, 'extreme': 25}
            vol_score = vol_scores.get(vol_regime, 50)
            scores.append(vol_score * 0.2)
            
            return sum(scores)
            
        except Exception as e:
            print(f"ERROR: Currency skor hesaplama hatası: {str(e)}")
            return 50.0
    
    def _recommend_currency_strategies(self, ultra_result, risk_sentiment: Dict, seasonality: Dict) -> List[Dict]:
        """Currency trading stratejileri önerisi"""
        try:
            strategies = []
            
            # Carry trade strategy
            carry_yield = ultra_result.carry_trade_analysis.risk_adjusted_carry
            if carry_yield > 0.02:
                strategies.append({
                    'strategy': 'Carry Trade',
                    'description': f'Pozitif carry (%{carry_yield*100:.2f}) ile long pozisyon',
                    'risk_level': 'Orta',
                    'expected_return': f'%{carry_yield*100:.1f} annual',
                    'conditions': 'Düşük volatilite ortamında uygun'
                })
            
            # Trend following
            tech_signals = ultra_result.technical_signals
            ma_signal = tech_signals.get('ma_signal', 0)
            if abs(ma_signal) >= 1:
                direction = 'Long' if ma_signal > 0 else 'Short'
                strategies.append({
                    'strategy': 'Trend Following',
                    'description': f'{direction} trend takip stratejisi',
                    'risk_level': 'Orta',
                    'expected_return': 'Trend gücüne bağlı',
                    'conditions': 'Güçlü trend sinyali mevcut'
                })
            
            # Mean reversion
            rsi = tech_signals.get('rsi', 50)
            if rsi > 70 or rsi < 30:
                direction = 'Short' if rsi > 70 else 'Long'
                strategies.append({
                    'strategy': 'Mean Reversion',
                    'description': f'Aşırı {("alım" if rsi > 70 else "satım")} sonrası {direction}',
                    'risk_level': 'Yüksek',
                    'expected_return': 'Kısa vadeli düzeltme',
                    'conditions': 'Range-bound market koşullarında'
                })
            
            # Volatility trading
            vol_regime = ultra_result.volatility_model.vol_regime
            if vol_regime in ['high', 'extreme']:
                strategies.append({
                    'strategy': 'Volatility Trading',
                    'description': 'Yüksek volatilitede range trading',
                    'risk_level': 'Yüksek',
                    'expected_return': 'Volatilite premium',
                    'conditions': 'Aktif risk yönetimi gerekli'
                })
            
            # Seasonal strategy
            seasonal_bias = seasonality.get('current_month_bias')
            if seasonal_bias and seasonal_bias != 'Belirsiz':
                strategies.append({
                    'strategy': 'Seasonal Trading',
                    'description': f'Mevcut ay {seasonal_bias.lower()} seasonal bias',
                    'risk_level': 'Düşük',
                    'expected_return': f'{seasonality.get("current_month_return", 0):.1f}%',
                    'conditions': 'Historical pattern geçerli ise'
                })
            
            return strategies[:4]  # Top 4 strategies
            
        except Exception as e:
            print(f"ERROR: Strateji önerisi hatası: {str(e)}")
            return [{
                'strategy': 'Conservative Hold',
                'description': 'Mevcut pozisyonu koru',
                'risk_level': 'Düşük'
            }]
    
    def _generate_currency_risk_management(self, ultra_result, basket_analysis: Dict) -> Dict:
        """Currency risk yönetimi önerileri"""
        try:
            risk_mgmt = {
                'position_sizing': {},
                'hedging_recommendations': [],
                'stop_loss_levels': {},
                'monitoring_points': []
            }
            
            # Position sizing
            vol_regime = ultra_result.volatility_model.vol_regime
            overall_risk = ultra_result.risk_assessment.get('overall_risk', 'Orta Risk')
            
            if 'Yüksek' in overall_risk or vol_regime in ['high', 'extreme']:
                position_size = 'Küçük pozisyon (1-2% risk)'
            elif 'Düşük' in overall_risk and vol_regime == 'low':
                position_size = 'Normal pozisyon (3-5% risk)'
            else:
                position_size = 'Orta pozisyon (2-3% risk)'
            
            risk_mgmt['position_sizing'] = {
                'recommended_size': position_size,
                'max_portfolio_weight': '10%' if 'Düşük' in overall_risk else '5%',
                'leverage_recommendation': 'Düşük (1:2-1:5)' if 'Yüksek' in overall_risk else 'Orta (1:10-1:20)'
            }
            
            # Hedging recommendations
            if ultra_result.carry_trade_analysis.volatility_cost > 0.05:
                risk_mgmt['hedging_recommendations'].append({
                    'type': 'Volatility Hedge',
                    'action': 'Options ile volatilite hedge et',
                    'priority': 'Yüksek'
                })
            
            diversification_score = basket_analysis.get('diversification_score', 50)
            if diversification_score < 40:
                risk_mgmt['hedging_recommendations'].append({
                    'type': 'Diversification',
                    'action': 'Farklı currency cluster\'larına yayıl',
                    'priority': 'Orta'
                })
            
            # Stop loss levels
            volatility = ultra_result.volatility_model.realized_volatility
            daily_vol = volatility / np.sqrt(252)
            
            risk_mgmt['stop_loss_levels'] = {
                'conservative': f'{daily_vol * 2:.1%} (2x günlük volatilite)',
                'moderate': f'{daily_vol * 3:.1%} (3x günlük volatilite)',
                'aggressive': f'{daily_vol * 5:.1%} (5x günlük volatilite)'
            }
            
            # Monitoring points
            risk_mgmt['monitoring_points'] = [
                'Merkez bankası toplantıları ve açıklamaları',
                'Ekonomik veri yayınları (CPI, GDP, İstihdam)',
                'Risk sentiment değişimleri (VIX, carry trade)',
                'Çapraz kur korelasyon değişimleri',
                'Volatilite rejim değişiklikleri'
            ]
            
            return risk_mgmt
            
        except Exception as e:
            print(f"ERROR: Risk yönetimi önerisi hatası: {str(e)}")
            return {
                'position_sizing': {'recommended_size': 'Normal pozisyon'},
                'hedging_recommendations': [{'type': 'Standard', 'action': 'Normal risk kontrolü'}],
                'monitoring_points': ['Günlük pozisyon kontrolü']
            }
    
    def _generate_currency_summary(self, symbol: str, ultra_result, currency_score: float) -> str:
        """Currency analizi özeti"""
        try:
            # Score-based assessment
            if currency_score >= 80:
                score_assessment = "mükemmel"
            elif currency_score >= 70:
                score_assessment = "iyi"
            elif currency_score >= 60:
                score_assessment = "orta"
            else:
                score_assessment = "zayıf"
            
            # Pair information
            base_curr = ultra_result.currency_pair.base_currency
            quote_curr = ultra_result.currency_pair.quote_currency
            
            # Carry trade info
            carry_yield = ultra_result.carry_trade_analysis.carry_yield
            rate_diff = ultra_result.carry_trade_analysis.interest_rate_differential
            
            summary = f"{symbol} currency pair analizi {score_assessment} skorla tamamlandı (%{currency_score:.1f}). "
            
            # Interest rate differential
            if abs(rate_diff) > 2:
                summary += f"Önemli faiz farkı (%{rate_diff:.1f}) mevcut, "
                if rate_diff > 0:
                    summary += f"{base_curr} favor. "
                else:
                    summary += f"{quote_curr} favor. "
            
            # Carry trade assessment
            if carry_yield > 0.03:
                summary += "Güçlü pozitif carry trade fırsatı. "
            elif carry_yield < -0.03:
                summary += "Negatif carry trade maliyeti mevcut. "
            else:
                summary += "Nötr carry trade profili. "
            
            # Volatility assessment
            vol_regime = ultra_result.volatility_model.vol_regime
            if vol_regime == "high" or vol_regime == "extreme":
                summary += "Yüksek volatilite nedeniyle dikkatli pozisyon alınmalı. "
            elif vol_regime == "low":
                summary += "Düşük volatilite ortamı pozisyon büyütmeye uygun. "
            
            # Trading recommendation
            recommendation = ultra_result.trading_recommendation
            if "GÜÇLÜ" in recommendation:
                summary += f"Güçlü {recommendation.split()[1].lower()} sinyali mevcut."
            elif recommendation == "BEKLE":
                summary += "Mevcut koşullarda bekleme önerisi."
            else:
                summary += f"{recommendation.lower()} sinyali aktif."
            
            return summary
            
        except Exception as e:
            print(f"ERROR: Currency özeti hatası: {str(e)}")
            return f"{symbol} için currency analizi tamamlandı"
    
    def _get_default_currency_response(self, symbol: str, current_rate: float) -> Dict:
        """Varsayılan currency cevabı"""
        return {
            'currency_score': 50.0,
            'analysis_summary': f"{symbol} için currency analizi temel parametrelerle tamamlandı",
            'basic_metrics': {
                'symbol': symbol,
                'current_rate': current_rate or 1.0,
                'volatility': 12.0,
                'is_major_pair': symbol in self.major_pairs
            },
            'risk_assessment': {
                'overall_risk': 'Orta Risk',
                'volatility_risk': 'Orta',
                'liquidity_risk': 'Orta'
            },
            'trading_recommendation': 'BEKLE',
            'confidence': 70.0
        }
