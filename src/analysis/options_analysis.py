"""
Options Analysis Module
Opsiyon analizi ana modülü

Bu modül ultra opsiyon analyzer ile entegrasyon sağlar ve
temel opsiyon analiz fonksiyonalitesi sunar.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime

try:
    from .ultra_options import UltraOptionsAnalyzer
    ULTRA_AVAILABLE = True
    print("INFO: Ultra Options Analysis modülü aktif")
except ImportError:
    ULTRA_AVAILABLE = False
    print("WARNING: Ultra Options Analysis modülü bulunamadı, temel analiz kullanılacak")

class OptionsAnalyzer:
    """Ana opsiyon analiz sınıfı"""
    
    def __init__(self):
        """Opsiyon analyzer'ı başlat"""
        self.ultra_analyzer = None
        if ULTRA_AVAILABLE:
            try:
                self.ultra_analyzer = UltraOptionsAnalyzer()
                print("INFO: Ultra Options Analyzer başarıyla başlatıldı")
            except Exception as e:
                print(f"WARNING: Ultra Options Analyzer başlatılamadı: {str(e)}")
        
        # Temel opsiyon parametreleri
        self.risk_free_rate = 0.05
        self.default_volatility = 0.25
        self.default_time_to_expiry = 0.25  # 3 ay
    
    def analyze_options(self, symbol: str, current_price: float, 
                       options_data: Optional[Dict] = None, **kwargs) -> Dict:
        """Kapsamlı opsiyon analizi"""
        try:
            if self.ultra_analyzer and ULTRA_AVAILABLE:
                return self._ultra_options_analysis(symbol, current_price, options_data, **kwargs)
            else:
                return self._basic_options_analysis(symbol, current_price, options_data, **kwargs)
                
        except Exception as e:
            print(f"ERROR: Opsiyon analizi hatası: {str(e)}")
            return self._get_default_options_response(symbol, current_price)
    
    def _ultra_options_analysis(self, symbol: str, current_price: float,
                               options_data: Optional[Dict], **kwargs) -> Dict:
        """Ultra gelişmiş opsiyon analizi"""
        try:
            # Opsiyon parametrelerini ayarla
            strike_price = kwargs.get('strike_price', current_price)
            time_to_expiry = kwargs.get('time_to_expiry', self.default_time_to_expiry)
            volatility = kwargs.get('volatility', self.default_volatility)
            option_type = kwargs.get('option_type', 'call')
            
            # Ana opsiyon analizi
            option_analysis = self.ultra_analyzer.analyze_option(
                symbol=symbol,
                spot_price=current_price,
                strike_price=strike_price,
                time_to_expiry=time_to_expiry,
                volatility=volatility,
                option_type=option_type,
                **kwargs
            )
            
            # ATM opsiyon analizi
            atm_analysis = self.ultra_analyzer.analyze_option(
                symbol=symbol,
                spot_price=current_price,
                strike_price=current_price,  # ATM
                time_to_expiry=time_to_expiry,
                volatility=volatility,
                option_type=option_type
            )
            
            # OTM opsiyon analizi
            otm_strike = current_price * 1.05 if option_type == 'call' else current_price * 0.95
            otm_analysis = self.ultra_analyzer.analyze_option(
                symbol=symbol,
                spot_price=current_price,
                strike_price=otm_strike,
                time_to_expiry=time_to_expiry,
                volatility=volatility,
                option_type=option_type
            )
            
            # Volatilite yüzeyi analizi
            vol_surface_analysis = self._analyze_volatility_environment(
                current_price, volatility, time_to_expiry
            )
            
            # Opsiyon stratejileri önerisi
            strategy_recommendations = self._recommend_option_strategies(
                current_price, volatility, time_to_expiry, option_analysis
            )
            
            # Implied volatility analizi
            iv_analysis = self._analyze_implied_volatility(
                current_price, strike_price, time_to_expiry, volatility
            )
            
            # Greeks portfolio analizi
            portfolio_greeks = self._calculate_portfolio_greeks([
                option_analysis, atm_analysis, otm_analysis
            ])
            
            # Risk yönetimi önerileri
            risk_management = self._generate_risk_management_advice(
                option_analysis, portfolio_greeks, vol_surface_analysis
            )
            
            # Opsiyon scoring
            options_score = self._calculate_options_score(
                option_analysis, vol_surface_analysis, iv_analysis, portfolio_greeks
            )
            
            return {
                'options_score': round(options_score, 1),
                'analysis_summary': self._generate_options_summary(
                    symbol, option_analysis, atm_analysis, otm_analysis, options_score
                ),
                'main_option': option_analysis,
                'atm_option': atm_analysis,
                'otm_option': otm_analysis,
                'volatility_environment': vol_surface_analysis,
                'strategy_recommendations': strategy_recommendations,
                'implied_volatility_analysis': iv_analysis,
                'portfolio_greeks': portfolio_greeks,
                'risk_management': risk_management,
                'market_outlook': self._generate_market_outlook(
                    option_analysis, vol_surface_analysis
                ),
                'confidence': round(np.mean([
                    option_analysis.get('confidence', 85),
                    90.0 if volatility > 0.15 else 85.0,
                    95.0 if time_to_expiry > 0.1 else 80.0
                ]), 1)
            }
            
        except Exception as e:
            print(f"ERROR: Ultra opsiyon analizi hatası: {str(e)}")
            return self._basic_options_analysis(symbol, current_price, options_data, **kwargs)
    
    def _basic_options_analysis(self, symbol: str, current_price: float,
                               options_data: Optional[Dict], **kwargs) -> Dict:
        """Temel opsiyon analizi"""
        try:
            strike_price = kwargs.get('strike_price', current_price)
            time_to_expiry = kwargs.get('time_to_expiry', self.default_time_to_expiry)
            volatility = kwargs.get('volatility', self.default_volatility)
            
            # Basit Black-Scholes hesaplaması
            option_price = self._simple_black_scholes(
                current_price, strike_price, time_to_expiry, volatility
            )
            
            # Basit Greeks
            delta = min(1.0, max(0.0, (current_price / strike_price) - 0.5))
            gamma = 0.1 * np.exp(-(current_price - strike_price)**2 / (2 * current_price**2))
            theta = -option_price * 0.1 / 365  # Günlük time decay
            vega = option_price * 0.5
            
            # Moneyness
            moneyness = current_price / strike_price
            if moneyness > 1.05:
                money_status = "ITM (Parada)"
            elif moneyness < 0.95:
                money_status = "OTM (Para Dışında)"
            else:
                money_status = "ATM (Para Başında)"
            
            # Basit opsiyon skoru
            options_score = min(100, max(0, 
                50 + (moneyness - 1) * 100 + volatility * 50 - (1 - time_to_expiry) * 30
            ))
            
            return {
                'options_score': round(options_score, 1),
                'analysis_summary': f"{symbol} opsiyonu {money_status} konumunda, temel analiz ile değerlendirildi",
                'basic_metrics': {
                    'theoretical_value': round(option_price, 2),
                    'delta': round(delta, 4),
                    'gamma': round(gamma, 4),
                    'theta': round(theta, 4),
                    'vega': round(vega, 4),
                    'moneyness': round(moneyness, 4),
                    'money_status': money_status
                },
                'risk_assessment': {
                    'overall_risk': 'Orta' if 0.9 < moneyness < 1.1 else 'Yüksek',
                    'time_risk': 'Yüksek' if time_to_expiry < 0.1 else 'Orta',
                    'volatility_risk': 'Yüksek' if volatility > 0.3 else 'Orta'
                },
                'confidence': 70.0
            }
            
        except Exception as e:
            print(f"ERROR: Temel opsiyon analizi hatası: {str(e)}")
            return self._get_default_options_response(symbol, current_price)
    
    def _simple_black_scholes(self, S: float, K: float, T: float, vol: float) -> float:
        """Basit Black-Scholes formülü"""
        try:
            from scipy.stats import norm
            
            d1 = (np.log(S/K) + (self.risk_free_rate + 0.5*vol**2)*T) / (vol*np.sqrt(T))
            d2 = d1 - vol*np.sqrt(T)
            
            call_price = S*norm.cdf(d1) - K*np.exp(-self.risk_free_rate*T)*norm.cdf(d2)
            return max(0, call_price)
            
        except Exception:
            # Fallback calculation
            intrinsic_value = max(0, S - K)
            time_value = S * 0.02 * np.sqrt(T)  # Rough approximation
            return intrinsic_value + time_value
    
    def _analyze_volatility_environment(self, current_price: float, volatility: float,
                                       time_to_expiry: float) -> Dict:
        """Volatilite ortamı analizi"""
        try:
            # Volatilite sınıflandırması
            if volatility > 0.4:
                vol_regime = "Çok Yüksek Volatilite"
                vol_outlook = "Aşırı volatilite, konsolidasyon beklenir"
            elif volatility > 0.3:
                vol_regime = "Yüksek Volatilite"
                vol_outlook = "Yüksek volatilite, dikkatli pozisyon alınmalı"
            elif volatility > 0.2:
                vol_regime = "Normal Volatilite"
                vol_outlook = "Normal volatilite seviyesi"
            else:
                vol_regime = "Düşük Volatilite"
                vol_outlook = "Düşük volatilite, hareket beklentisi"
            
            # Volatilite skoru
            vol_score = min(100, volatility * 250)  # Annualized basis
            
            # Term structure analizi
            short_term_vol = volatility
            long_term_vol = volatility * 1.1  # Typically higher
            
            term_structure = {
                'backwardation' if short_term_vol > long_term_vol else 'contango': True,
                'short_term': round(short_term_vol, 4),
                'long_term': round(long_term_vol, 4),
                'slope': round(long_term_vol - short_term_vol, 4)
            }
            
            return {
                'volatility_regime': vol_regime,
                'volatility_score': round(vol_score, 1),
                'market_outlook': vol_outlook,
                'term_structure': term_structure,
                'vix_equivalent': round(volatility * 100, 1),  # Convert to VIX-like scale
                'volatility_percentile': min(100, max(0, volatility * 300))  # Rough percentile
            }
            
        except Exception as e:
            print(f"ERROR: Volatilite analizi hatası: {str(e)}")
            return {
                'volatility_regime': 'Normal',
                'volatility_score': 50.0,
                'market_outlook': 'Standart volatilite koşulları'
            }
    
    def _recommend_option_strategies(self, current_price: float, volatility: float,
                                    time_to_expiry: float, main_analysis: Dict) -> List[Dict]:
        """Opsiyon stratejileri önerisi"""
        try:
            recommendations = []
            
            # Volatilite bazlı stratejiler
            if volatility > 0.3:
                # Yüksek volatilite - volatilite satışı
                recommendations.append({
                    'strategy': 'Short Straddle',
                    'description': 'Yüksek volatiliteyi sat, range-bound hareket bekle',
                    'max_profit': f'${current_price * 0.1:.2f} (prim geliri)',
                    'max_loss': 'Sınırsız',
                    'breakeven': f'${current_price * 0.95:.2f} - ${current_price * 1.05:.2f}',
                    'risk_level': 'Yüksek',
                    'market_view': 'Volatilite düşecek, fiyat sabit kalacak'
                })
                
                recommendations.append({
                    'strategy': 'Iron Condor',
                    'description': 'Düşük volatilite ve range-bound hareket stratejisi',
                    'max_profit': f'${current_price * 0.05:.2f}',
                    'max_loss': f'${current_price * 0.15:.2f}',
                    'breakeven': f'İki nokta: ±%5 hareket',
                    'risk_level': 'Orta',
                    'market_view': 'Volatilite düşecek, dar aralıkta hareket'
                })
                
            else:
                # Düşük volatilite - volatilite alışı
                recommendations.append({
                    'strategy': 'Long Straddle',
                    'description': 'Büyük hareket bekle, yön önemli değil',
                    'max_profit': 'Sınırsız',
                    'max_loss': f'${current_price * 0.08:.2f} (ödenen prim)',
                    'breakeven': f'${current_price * 0.92:.2f} - ${current_price * 1.08:.2f}',
                    'risk_level': 'Orta',
                    'market_view': 'Büyük hareket gelecek, yön belirsiz'
                })
                
                recommendations.append({
                    'strategy': 'Long Strangle',
                    'description': 'Geniş hareket bekle, daha ucuz alternatif',
                    'max_profit': 'Sınırsız',
                    'max_loss': f'${current_price * 0.06:.2f}',
                    'breakeven': f'±%8-10 hareket gerekli',
                    'risk_level': 'Orta',
                    'market_view': 'Orta-büyük hareket beklentisi'
                })
            
            # Zaman bazlı stratejiler
            if time_to_expiry < 0.1:  # < 1 ay
                recommendations.append({
                    'strategy': 'Theta Decay Play',
                    'description': 'Kısa vadeli zaman değeri kazanımı',
                    'max_profit': f'${current_price * 0.03:.2f}',
                    'max_loss': f'${current_price * 0.05:.2f}',
                    'breakeven': 'Mevcut fiyat ±%2',
                    'risk_level': 'Düşük-Orta',
                    'market_view': 'Fiyat mevcut seviyelerde kalacak'
                })
            
            # Trend bazlı stratejiler
            greeks = main_analysis.get('greeks_analysis', {})
            delta = greeks.get('score', 50) / 100
            
            if delta > 0.6:
                recommendations.append({
                    'strategy': 'Bull Call Spread',
                    'description': 'Kontrollü yükseliş stratejisi',
                    'max_profit': f'${current_price * 0.1:.2f}',
                    'max_loss': f'${current_price * 0.04:.2f}',
                    'breakeven': f'${current_price * 1.02:.2f}',
                    'risk_level': 'Düşük-Orta',
                    'market_view': 'Orta yükseliş beklentisi'
                })
            
            return recommendations[:3]  # Top 3 recommendations
            
        except Exception as e:
            print(f"ERROR: Strateji önerisi hatası: {str(e)}")
            return [{
                'strategy': 'Covered Call',
                'description': 'Temel gelir getirici strateji',
                'risk_level': 'Düşük'
            }]
    
    def _analyze_implied_volatility(self, current_price: float, strike_price: float,
                                   time_to_expiry: float, volatility: float) -> Dict:
        """Implied volatility analizi"""
        try:
            # IV percentile simulation (gerçek veriler olmadığı için)
            historical_vol = volatility * 0.8  # Assume current IV is elevated
            iv_percentile = min(100, max(0, (volatility / historical_vol - 1) * 200 + 50))
            
            # IV rank
            if iv_percentile > 80:
                iv_rank = "Çok Yüksek"
                iv_advice = "Volatilite satış stratejileri düşünün"
            elif iv_percentile > 60:
                iv_rank = "Yüksek"
                iv_advice = "Net volatilite satışı avantajlı olabilir"
            elif iv_percentile > 40:
                iv_rank = "Normal"
                iv_advice = "Neutral volatilite stratejileri uygun"
            else:
                iv_rank = "Düşük"
                iv_advice = "Volatilite alış stratejileri düşünün"
            
            # IV skew analizi
            atm_iv = volatility
            otm_put_iv = volatility * 1.2  # Typical put skew
            otm_call_iv = volatility * 0.9  # Call wing typically lower
            
            skew_metrics = {
                'put_call_skew': round(otm_put_iv - otm_call_iv, 4),
                'atm_iv': round(atm_iv, 4),
                'otm_put_iv': round(otm_put_iv, 4),
                'otm_call_iv': round(otm_call_iv, 4),
                'skew_direction': 'Put Skew' if otm_put_iv > otm_call_iv else 'Call Skew'
            }
            
            return {
                'current_iv': round(volatility, 4),
                'iv_percentile': round(iv_percentile, 1),
                'iv_rank': iv_rank,
                'trading_advice': iv_advice,
                'skew_analysis': skew_metrics,
                'volatility_forecast': self._forecast_volatility(volatility, time_to_expiry)
            }
            
        except Exception as e:
            print(f"ERROR: IV analizi hatası: {str(e)}")
            return {
                'current_iv': volatility,
                'iv_rank': 'Normal',
                'trading_advice': 'Standard volatilite koşulları'
            }
    
    def _forecast_volatility(self, current_vol: float, time_to_expiry: float) -> Dict:
        """Volatilite tahmini"""
        try:
            # Basit mean reversion modeli
            long_term_vol = 0.25  # Long-term average
            mean_reversion_speed = 2.0  # Annual mean reversion
            
            # Forecast for different horizons
            forecasts = {}
            for days in [7, 30, 90]:
                time_fraction = days / 365
                if time_fraction <= time_to_expiry:
                    # Mean reversion formula
                    forecast = long_term_vol + (current_vol - long_term_vol) * np.exp(-mean_reversion_speed * time_fraction)
                    forecasts[f'{days}d'] = round(forecast, 4)
            
            # Trend determination
            if current_vol > long_term_vol * 1.2:
                trend = "Düşüş Eğilimi"
            elif current_vol < long_term_vol * 0.8:
                trend = "Yükseliş Eğilimi"
            else:
                trend = "Sabit Eğilim"
            
            return {
                'forecasts': forecasts,
                'trend': trend,
                'long_term_average': round(long_term_vol, 4),
                'current_vs_longterm': round((current_vol / long_term_vol - 1) * 100, 1)
            }
            
        except Exception as e:
            print(f"ERROR: Volatilite tahmin hatası: {str(e)}")
            return {'trend': 'Belirsiz', 'forecasts': {}}
    
    def _calculate_portfolio_greeks(self, option_analyses: List[Dict]) -> Dict:
        """Portfolio Greeks hesaplama"""
        try:
            total_delta = 0
            total_gamma = 0
            total_theta = 0
            total_vega = 0
            total_rho = 0
            
            valid_analyses = 0
            
            for analysis in option_analyses:
                bs_data = analysis.get('black_scholes', {})
                if bs_data:
                    total_delta += bs_data.get('delta', 0)
                    total_gamma += bs_data.get('gamma', 0)
                    total_theta += bs_data.get('theta', 0)
                    total_vega += bs_data.get('vega', 0)
                    total_rho += bs_data.get('rho', 0)
                    valid_analyses += 1
            
            if valid_analyses == 0:
                return {'error': 'Portfolio Greeks hesaplanamadı'}
            
            # Risk metrics
            directional_risk = abs(total_delta)
            acceleration_risk = abs(total_gamma)
            time_risk = abs(total_theta)
            volatility_risk = abs(total_vega)
            
            # Risk classification
            risk_levels = {
                'directional': 'Yüksek' if directional_risk > 0.5 else 'Orta' if directional_risk > 0.2 else 'Düşük',
                'acceleration': 'Yüksek' if acceleration_risk > 0.1 else 'Orta' if acceleration_risk > 0.05 else 'Düşük',
                'time_decay': 'Yüksek' if time_risk > 0.1 else 'Orta' if time_risk > 0.05 else 'Düşük',
                'volatility': 'Yüksek' if volatility_risk > 0.2 else 'Orta' if volatility_risk > 0.1 else 'Düşük'
            }
            
            return {
                'portfolio_greeks': {
                    'total_delta': round(total_delta, 4),
                    'total_gamma': round(total_gamma, 4),
                    'total_theta': round(total_theta, 4),
                    'total_vega': round(total_vega, 4),
                    'total_rho': round(total_rho, 4)
                },
                'risk_metrics': {
                    'directional_risk': round(directional_risk, 4),
                    'acceleration_risk': round(acceleration_risk, 4),
                    'time_decay_risk': round(time_risk, 4),
                    'volatility_risk': round(volatility_risk, 4)
                },
                'risk_levels': risk_levels,
                'portfolio_summary': self._summarize_portfolio_risk(risk_levels, total_delta, total_theta)
            }
            
        except Exception as e:
            print(f"ERROR: Portfolio Greeks hesaplama hatası: {str(e)}")
            return {'error': 'Portfolio Greeks hesaplanamadı'}
    
    def _summarize_portfolio_risk(self, risk_levels: Dict, total_delta: float, total_theta: float) -> str:
        """Portfolio risk özeti"""
        try:
            summary = "Portfolio "
            
            if risk_levels['directional'] == 'Yüksek':
                direction = 'yükseliş' if total_delta > 0 else 'düşüş'
                summary += f"güçlü {direction} eğilimi gösteriyor. "
            elif risk_levels['directional'] == 'Orta':
                summary += "orta düzeyde yönlü risk taşıyor. "
            else:
                summary += "düşük yönlü risk profili var. "
            
            if risk_levels['time_decay'] == 'Yüksek':
                if total_theta < 0:
                    summary += "Yüksek zaman değeri kaybı riski mevcut. "
                else:
                    summary += "Pozitif zaman değeri kazanımı potansiyeli var. "
            
            if risk_levels['volatility'] == 'Yüksek':
                summary += "Volatilite değişimlerine çok hassas. "
            
            return summary.strip()
            
        except Exception as e:
            print(f"ERROR: Portfolio özet hatası: {str(e)}")
            return "Portfolio risk profili standart seviyelerde"
    
    def _generate_risk_management_advice(self, option_analysis: Dict, portfolio_greeks: Dict,
                                        vol_analysis: Dict) -> Dict:
        """Risk yönetimi önerileri"""
        try:
            advice = {
                'hedging_recommendations': [],
                'position_sizing': {},
                'monitoring_points': [],
                'exit_strategies': []
            }
            
            # Greeks-based hedging
            greeks = option_analysis.get('black_scholes', {})
            delta = greeks.get('delta', 0)
            gamma = greeks.get('gamma', 0)
            theta = greeks.get('theta', 0)
            vega = greeks.get('vega', 0)
            
            # Delta hedging
            if abs(delta) > 0.5:
                advice['hedging_recommendations'].append({
                    'type': 'Delta Hedging',
                    'action': f"Underlying pozisyonunu {abs(delta)*100:.1f}% hedge et",
                    'priority': 'Yüksek' if abs(delta) > 0.8 else 'Orta'
                })
            
            # Gamma hedging
            if abs(gamma) > 0.1:
                advice['hedging_recommendations'].append({
                    'type': 'Gamma Hedging',
                    'action': 'Ek opsiyon pozisyonları ile gamma nötralize et',
                    'priority': 'Orta'
                })
            
            # Vega hedging
            if abs(vega) > 0.15:
                vol_regime = vol_analysis.get('volatility_regime', 'Normal')
                if 'Yüksek' in vol_regime:
                    advice['hedging_recommendations'].append({
                        'type': 'Vega Hedging',
                        'action': 'Volatilite riskini azalt, net vega sat',
                        'priority': 'Yüksek'
                    })
            
            # Position sizing
            vol_score = vol_analysis.get('volatility_score', 50)
            if vol_score > 70:
                position_size = 'Küçük pozisyon (yüksek volatilite)'
            elif vol_score > 40:
                position_size = 'Normal pozisyon'
            else:
                position_size = 'Büyük pozisyon (düşük volatilite)'
            
            advice['position_sizing'] = {
                'recommended_size': position_size,
                'max_portfolio_weight': '5%' if vol_score > 70 else '10%' if vol_score > 40 else '15%',
                'diversification': 'Çoklu vade ve strike kullan'
            }
            
            # Monitoring points
            advice['monitoring_points'] = [
                'Günlük theta decay kontrolü',
                'IV değişimlerini takip et',
                'Underlying fiyat hareketleri',
                'Volatilite rejim değişiklikleri',
                'Greeks dengesi kontrolü'
            ]
            
            # Exit strategies
            if theta < -0.05:
                advice['exit_strategies'].append({
                    'trigger': 'Zaman değeri hızla eriyor',
                    'action': 'Vade yaklaştıkça pozisyonu kapat',
                    'timeline': 'Son 2 hafta'
                })
            
            if vol_analysis.get('iv_percentile', 50) > 80:
                advice['exit_strategies'].append({
                    'trigger': 'IV çok yüksek',
                    'action': 'Volatilite satış pozisyonları düşün',
                    'timeline': 'Mevcut koşullarda'
                })
            
            return advice
            
        except Exception as e:
            print(f"ERROR: Risk yönetimi önerisi hatası: {str(e)}")
            return {
                'hedging_recommendations': [{'type': 'Standart', 'action': 'Normal risk kontrolü'}],
                'position_sizing': {'recommended_size': 'Normal pozisyon'},
                'monitoring_points': ['Günlük pozisyon kontrolü'],
                'exit_strategies': [{'trigger': 'Kar hedefi', 'action': 'Karlı pozisyonları kapat'}]
            }
    
    def _calculate_options_score(self, option_analysis: Dict, vol_analysis: Dict,
                                iv_analysis: Dict, portfolio_greeks: Dict) -> float:
        """Genel opsiyon skoru hesaplama"""
        try:
            scores = []
            
            # Ana opsiyon skoru (%40)
            main_score = option_analysis.get('ultra_option_score', 50)
            scores.append(main_score * 0.4)
            
            # Volatilite ortamı skoru (%25)
            vol_score = vol_analysis.get('volatility_score', 50)
            scores.append(min(100, vol_score) * 0.25)
            
            # IV analiz skoru (%20)
            iv_percentile = iv_analysis.get('iv_percentile', 50)
            iv_score = 100 - abs(iv_percentile - 50)  # Optimal around 50th percentile
            scores.append(iv_score * 0.2)
            
            # Portfolio risk skoru (%15)
            risk_levels = portfolio_greeks.get('risk_levels', {})
            portfolio_score = 100
            for risk_type, level in risk_levels.items():
                if level == 'Yüksek':
                    portfolio_score -= 20
                elif level == 'Orta':
                    portfolio_score -= 10
            scores.append(max(0, portfolio_score) * 0.15)
            
            total_score = sum(scores)
            return min(100, max(0, total_score))
            
        except Exception as e:
            print(f"ERROR: Opsiyon skoru hesaplama hatası: {str(e)}")
            return 50.0
    
    def _generate_options_summary(self, symbol: str, main_analysis: Dict, atm_analysis: Dict,
                                 otm_analysis: Dict, options_score: float) -> str:
        """Opsiyon analizi özeti"""
        try:
            # Score-based assessment
            if options_score >= 80:
                score_assessment = "mükemmel"
            elif options_score >= 70:
                score_assessment = "iyi"
            elif options_score >= 60:
                score_assessment = "orta"
            else:
                score_assessment = "zayıf"
            
            # Main option moneyness
            main_moneyness = main_analysis.get('moneyness_analysis', {})
            money_status = main_moneyness.get('classification', 'ATM')
            
            # ATM Greeks
            atm_greeks = atm_analysis.get('black_scholes', {})
            atm_delta = atm_greeks.get('delta', 0.5)
            atm_theta = atm_greeks.get('theta', 0)
            
            summary = f"{symbol} opsiyon analizi {score_assessment} skorla tamamlandı (%{options_score:.1f}). "
            
            summary += f"Ana opsiyon {money_status} konumunda, "
            
            if atm_delta > 0.6:
                summary += "güçlü yönlü hassasiyet gösteriyor. "
            elif atm_delta > 0.4:
                summary += "orta düzeyde yönlü hassasiyet mevcut. "
            else:
                summary += "düşük yönlü hassasiyet sergiliyor. "
            
            if abs(atm_theta) > 0.1:
                summary += "Yüksek zaman değeri kaybı nedeniyle acil eylem gerektirir. "
            elif abs(atm_theta) > 0.05:
                summary += "Orta düzeyde zaman değeri kaybı izlenmeli. "
            else:
                summary += "Zaman faktörü kontrol altında. "
            
            # Risk assessment
            risk_profile = main_analysis.get('risk_profile', {})
            overall_risk = risk_profile.get('overall_risk', 'Orta Risk')
            
            if 'Yüksek' in overall_risk:
                summary += "Yüksek risk profili dikkatli yönetim gerektiriyor."
            elif 'Düşük' in overall_risk:
                summary += "Düşük risk profili güvenli pozisyon sunuyor."
            else:
                summary += "Standart risk seviyelerinde işlem yapılabilir."
            
            return summary
            
        except Exception as e:
            print(f"ERROR: Opsiyon özeti hatası: {str(e)}")
            return f"{symbol} için opsiyon analizi tamamlandı"
    
    def _generate_market_outlook(self, option_analysis: Dict, vol_analysis: Dict) -> Dict:
        """Piyasa görünümü analizi"""
        try:
            # Volatilite bazlı outlook
            vol_regime = vol_analysis.get('volatility_regime', 'Normal')
            
            if 'Yüksek' in vol_regime:
                market_sentiment = 'Endişeli/Volatil'
                expected_direction = 'Belirsiz, büyük hareketler'
                timeline = 'Kısa vadeli düzeltme beklentisi'
            elif 'Düşük' in vol_regime:
                market_sentiment = 'Sakin/Kompresyon'
                expected_direction = 'Büyük hareket birikiyor'
                timeline = 'Orta vadede volatilite artışı'
            else:
                market_sentiment = 'Normal/Dengeli'
                expected_direction = 'Trend sürdürülebilir'
                timeline = 'Mevcut koşullar devam edebilir'
            
            # Greeks-based signals
            greeks = option_analysis.get('black_scholes', {})
            delta = greeks.get('delta', 0.5)
            
            if delta > 0.7:
                trend_signal = 'Güçlü Yükseliş Sinyali'
            elif delta > 0.3:
                trend_signal = 'Orta Yükseliş Eğilimi'
            elif delta > -0.3:
                trend_signal = 'Nötr/Belirsiz'
            else:
                trend_signal = 'Düşüş Eğilimi'
            
            # Confidence level
            confidence = option_analysis.get('confidence', 75)
            
            return {
                'market_sentiment': market_sentiment,
                'volatility_outlook': vol_analysis.get('market_outlook', 'Normal koşullar'),
                'trend_signal': trend_signal,
                'expected_direction': expected_direction,
                'timeline': timeline,
                'confidence_level': confidence,
                'key_levels': {
                    'support': f"${option_analysis.get('moneyness_analysis', {}).get('intrinsic_value', 0):.2f}",
                    'resistance': f"${float(option_analysis.get('moneyness_analysis', {}).get('intrinsic_value', 100)) * 1.1:.2f}",
                    'breakeven': option_analysis.get('moneyness_analysis', {}).get('classification', 'ATM')
                }
            }
            
        except Exception as e:
            print(f"ERROR: Piyasa görünümü hatası: {str(e)}")
            return {
                'market_sentiment': 'Belirsiz',
                'trend_signal': 'Nötr',
                'timeline': 'Standart koşullar'
            }
    
    def _get_default_options_response(self, symbol: str, current_price: float) -> Dict:
        """Varsayılan opsiyon cevabı"""
        return {
            'options_score': 50.0,
            'analysis_summary': f"{symbol} için opsiyon analizi temel parametrelerle tamamlandı",
            'basic_metrics': {
                'theoretical_value': round(current_price * 0.05, 2),
                'delta': 0.5,
                'gamma': 0.1,
                'theta': -0.02,
                'vega': 0.15,
                'moneyness': 1.0,
                'money_status': 'ATM'
            },
            'confidence': 70.0
        }
