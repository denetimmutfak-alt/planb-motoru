"""
PlanB Motoru - Risk Management
Risk yönetimi ve portföy optimizasyonu
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ML Libraries for risk management
try:
    from sklearn.covariance import LedoitWolf
    from scipy.optimize import minimize
    from scipy.stats import norm
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

from src.utils.logger import log_info, log_error, log_debug

class RiskManager:
    """Risk yönetimi sınıfı"""
    
    def __init__(self):
        self.portfolio_data = {}
        self.risk_metrics = {}
        self.var_confidence_levels = [0.95, 0.99]
        self.max_position_size = 0.1  # Maksimum pozisyon büyüklüğü (%10)
        self.max_portfolio_risk = 0.15  # Maksimum portföy riski (%15)
        
    def add_portfolio_position(self, symbol: str, quantity: float, 
                             current_price: float, entry_price: float = None) -> bool:
        """Portföy pozisyonu ekle"""
        try:
            if entry_price is None:
                entry_price = current_price
            
            position_value = quantity * current_price
            unrealized_pnl = (current_price - entry_price) * quantity
            unrealized_pnl_pct = (current_price - entry_price) / entry_price * 100
            
            self.portfolio_data[symbol] = {
                'symbol': symbol,
                'quantity': quantity,
                'current_price': current_price,
                'entry_price': entry_price,
                'position_value': position_value,
                'unrealized_pnl': unrealized_pnl,
                'unrealized_pnl_pct': unrealized_pnl_pct,
                'weight': 0.0,  # Portföy ağırlığı hesaplanacak
                'last_updated': datetime.now().isoformat()
            }
            
            self._update_portfolio_weights()
            log_debug(f"Pozisyon eklendi: {symbol}")
            return True
            
        except Exception as e:
            log_error(f"Pozisyon ekleme hatası: {e}")
            return False
    
    def update_position_price(self, symbol: str, new_price: float) -> bool:
        """Pozisyon fiyatını güncelle"""
        try:
            if symbol not in self.portfolio_data:
                log_error(f"Pozisyon bulunamadı: {symbol}")
                return False
            
            position = self.portfolio_data[symbol]
            position['current_price'] = new_price
            position['position_value'] = position['quantity'] * new_price
            position['unrealized_pnl'] = (new_price - position['entry_price']) * position['quantity']
            position['unrealized_pnl_pct'] = (new_price - position['entry_price']) / position['entry_price'] * 100
            position['last_updated'] = datetime.now().isoformat()
            
            self._update_portfolio_weights()
            log_debug(f"Fiyat güncellendi: {symbol} -> {new_price}")
            return True
            
        except Exception as e:
            log_error(f"Fiyat güncelleme hatası: {e}")
            return False
    
    def _update_portfolio_weights(self):
        """Portföy ağırlıklarını güncelle"""
        try:
            total_value = sum(pos['position_value'] for pos in self.portfolio_data.values())
            
            if total_value > 0:
                for symbol in self.portfolio_data:
                    self.portfolio_data[symbol]['weight'] = (
                        self.portfolio_data[symbol]['position_value'] / total_value
                    )
            
        except Exception as e:
            log_error(f"Portföy ağırlığı güncelleme hatası: {e}")
    
    def calculate_portfolio_risk(self, returns_data: Dict[str, pd.Series] = None) -> Dict[str, Any]:
        """Portföy risk metriklerini hesapla"""
        try:
            if not self.portfolio_data:
                return {'error': 'Portföy verisi yok'}
            
            # Portföy toplam değeri
            total_value = sum(pos['position_value'] for pos in self.portfolio_data.values())
            
            # Ağırlıklar
            weights = np.array([pos['weight'] for pos in self.portfolio_data.values()])
            symbols = list(self.portfolio_data.keys())
            
            # Risk metrikleri
            risk_metrics = {
                'total_portfolio_value': total_value,
                'position_count': len(self.portfolio_data),
                'weights': dict(zip(symbols, weights)),
                'concentration_risk': self._calculate_concentration_risk(),
                'var_metrics': {},
                'expected_shortfall': {},
                'sharpe_ratio': 0.0,
                'max_drawdown': 0.0,
                'volatility': 0.0
            }
            
            # Returns verisi varsa gelişmiş risk metrikleri hesapla
            if returns_data and len(returns_data) > 0:
                risk_metrics.update(self._calculate_advanced_risk_metrics(returns_data, weights, symbols))
            
            self.risk_metrics = risk_metrics
            return risk_metrics
            
        except Exception as e:
            log_error(f"Portföy risk hesaplama hatası: {e}")
            return {'error': str(e)}
    
    def _calculate_concentration_risk(self) -> Dict[str, Any]:
        """Konsantrasyon riskini hesapla"""
        try:
            if not self.portfolio_data:
                return {}
            
            weights = [pos['weight'] for pos in self.portfolio_data.values()]
            
            # Herfindahl-Hirschman Index (HHI)
            hhi = sum(w**2 for w in weights)
            
            # Maksimum ağırlık
            max_weight = max(weights) if weights else 0
            
            # Top 5 konsantrasyonu
            sorted_weights = sorted(weights, reverse=True)
            top5_concentration = sum(sorted_weights[:5])
            
            # Risk seviyesi
            if hhi > 0.25 or max_weight > 0.3:
                risk_level = "High"
            elif hhi > 0.15 or max_weight > 0.2:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            return {
                'hhi': hhi,
                'max_weight': max_weight,
                'top5_concentration': top5_concentration,
                'risk_level': risk_level,
                'recommendation': self._get_concentration_recommendation(risk_level, max_weight)
            }
            
        except Exception as e:
            log_error(f"Konsantrasyon riski hesaplama hatası: {e}")
            return {}
    
    def _calculate_advanced_risk_metrics(self, returns_data: Dict[str, pd.Series], 
                                       weights: np.ndarray, symbols: List[str]) -> Dict[str, Any]:
        """Gelişmiş risk metrikleri hesapla"""
        try:
            if not ML_AVAILABLE:
                return {}
            
            # Returns matrisi oluştur
            returns_matrix = []
            valid_symbols = []
            
            for symbol in symbols:
                if symbol in returns_data and not returns_data[symbol].empty:
                    returns_matrix.append(returns_data[symbol].values)
                    valid_symbols.append(symbol)
            
            if len(returns_matrix) < 2:
                return {}
            
            returns_df = pd.DataFrame(returns_matrix).T
            returns_df.columns = valid_symbols
            
            # Kovaryans matrisi
            if len(returns_df) > 30:  # Yeterli veri varsa
                cov_matrix = LedoitWolf().fit(returns_df).covariance_
            else:
                cov_matrix = returns_df.cov().values
            
            # Portföy volatilitesi
            portfolio_variance = np.dot(weights[:len(valid_symbols)], np.dot(cov_matrix, weights[:len(valid_symbols)]))
            portfolio_volatility = np.sqrt(portfolio_variance * 252)  # Yıllık volatilite
            
            # VaR hesaplamaları
            portfolio_returns = returns_df.dot(weights[:len(valid_symbols)])
            var_metrics = {}
            expected_shortfall = {}
            
            for confidence in self.var_confidence_levels:
                var_value = np.percentile(portfolio_returns, (1 - confidence) * 100)
                var_metrics[f'var_{int(confidence*100)}'] = var_value
                
                # Expected Shortfall (Conditional VaR)
                es_value = portfolio_returns[portfolio_returns <= var_value].mean()
                expected_shortfall[f'es_{int(confidence*100)}'] = es_value
            
            # Sharpe Ratio (varsayılan risk-free rate %2)
            risk_free_rate = 0.02
            expected_return = portfolio_returns.mean() * 252
            sharpe_ratio = (expected_return - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
            
            # Maximum Drawdown
            cumulative_returns = (1 + portfolio_returns).cumprod()
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            max_drawdown = drawdown.min()
            
            return {
                'volatility': portfolio_volatility,
                'var_metrics': var_metrics,
                'expected_shortfall': expected_shortfall,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'covariance_matrix': cov_matrix.tolist()
            }
            
        except Exception as e:
            log_error(f"Gelişmiş risk metrikleri hesaplama hatası: {e}")
            return {}
    
    def calculate_position_risk(self, symbol: str, price_data: pd.DataFrame = None) -> Dict[str, Any]:
        """Pozisyon riskini hesapla"""
        try:
            if symbol not in self.portfolio_data:
                return {'error': 'Pozisyon bulunamadı'}
            
            position = self.portfolio_data[symbol]
            
            # Temel risk metrikleri
            position_risk = {
                'symbol': symbol,
                'position_value': position['position_value'],
                'weight': position['weight'],
                'unrealized_pnl': position['unrealized_pnl'],
                'unrealized_pnl_pct': position['unrealized_pnl_pct'],
                'risk_level': 'Low',
                'recommendations': []
            }
            
            # Ağırlık riski
            if position['weight'] > self.max_position_size:
                position_risk['risk_level'] = 'High'
                position_risk['recommendations'].append(
                    f"Pozisyon ağırlığı çok yüksek (%{position['weight']*100:.1f}) - azaltın"
                )
            elif position['weight'] > self.max_position_size * 0.8:
                position_risk['risk_level'] = 'Medium'
                position_risk['recommendations'].append(
                    f"Pozisyon ağırlığı yüksek (%{position['weight']*100:.1f}) - izleyin"
                )
            
            # Kar/zarar riski
            if position['unrealized_pnl_pct'] < -20:
                position_risk['risk_level'] = 'High'
                position_risk['recommendations'].append(
                    f"Büyük zarar (%{position['unrealized_pnl_pct']:.1f}%) - stop loss değerlendirin"
                )
            elif position['unrealized_pnl_pct'] < -10:
                position_risk['risk_level'] = 'Medium'
                position_risk['recommendations'].append(
                    f"Orta zarar (%{position['unrealized_pnl_pct']:.1f}%) - risk yönetimi uygulayın"
                )
            
            # Fiyat verisi varsa volatilite riski
            if price_data is not None and not price_data.empty and 'close' in price_data.columns:
                returns = price_data['close'].pct_change(fill_method=None).dropna()
                volatility = returns.std() * np.sqrt(252)  # Yıllık volatilite
                
                position_risk['volatility'] = volatility
                
                if volatility > 0.4:  # %40+ volatilite
                    position_risk['risk_level'] = 'High'
                    position_risk['recommendations'].append(
                        f"Yüksek volatilite (%{volatility*100:.1f}) - pozisyon büyüklüğünü azaltın"
                    )
                elif volatility > 0.25:  # %25+ volatilite
                    if position_risk['risk_level'] == 'Low':
                        position_risk['risk_level'] = 'Medium'
                    position_risk['recommendations'].append(
                        f"Orta volatilite (%{volatility*100:.1f}) - dikkatli izleyin"
                    )
            
            return position_risk
            
        except Exception as e:
            log_error(f"Pozisyon riski hesaplama hatası: {e}")
            return {'error': str(e)}
    
    def optimize_portfolio_weights(self, expected_returns: Dict[str, float] = None,
                                 risk_tolerance: float = 0.1) -> Dict[str, Any]:
        """Portföy ağırlıklarını optimize et"""
        try:
            if not self.portfolio_data:
                return {'error': 'Portföy verisi yok'}
            
            symbols = list(self.portfolio_data.keys())
            n_assets = len(symbols)
            
            if n_assets < 2:
                return {'error': 'En az 2 varlık gerekli'}
            
            # Varsayılan beklenen getiriler
            if expected_returns is None:
                expected_returns = {symbol: 0.08 for symbol in symbols}  # %8 varsayılan getiri
            
            # Beklenen getiri vektörü
            mu = np.array([expected_returns.get(symbol, 0.08) for symbol in symbols])
            
            # Kovaryans matrisi (basit yaklaşım)
            # Gerçek uygulamada historical returns kullanılmalı
            cov_matrix = np.eye(n_assets) * 0.04  # %20 volatilite varsayımı
            
            # Optimizasyon fonksiyonu (Markowitz)
            def portfolio_variance(weights):
                return np.dot(weights.T, np.dot(cov_matrix, weights))
            
            def portfolio_return(weights):
                return np.dot(weights, mu)
            
            # Kısıtlar
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Ağırlıklar toplamı 1
            ]
            
            # Sınırlar (her pozisyon %0-30 arası)
            bounds = tuple((0, 0.3) for _ in range(n_assets))
            
            # Başlangıç değerleri (eşit ağırlık)
            x0 = np.array([1.0 / n_assets] * n_assets)
            
            # Optimizasyon
            result = minimize(
                portfolio_variance,
                x0,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            if result.success:
                optimal_weights = result.x
                optimal_return = portfolio_return(optimal_weights)
                optimal_variance = portfolio_variance(optimal_weights)
                optimal_volatility = np.sqrt(optimal_variance)
                
                # Mevcut ağırlıklarla karşılaştır
                current_weights = np.array([self.portfolio_data[symbol]['weight'] for symbol in symbols])
                current_return = portfolio_return(current_weights)
                current_variance = portfolio_variance(current_weights)
                current_volatility = np.sqrt(current_variance)
                
                optimization_result = {
                    'optimal_weights': dict(zip(symbols, optimal_weights)),
                    'optimal_return': optimal_return,
                    'optimal_volatility': optimal_volatility,
                    'current_weights': dict(zip(symbols, current_weights)),
                    'current_return': current_return,
                    'current_volatility': current_volatility,
                    'improvement_potential': {
                        'return_improvement': optimal_return - current_return,
                        'volatility_reduction': current_volatility - optimal_volatility,
                        'sharpe_improvement': (optimal_return / optimal_volatility) - (current_return / current_volatility)
                    },
                    'recommendations': self._get_optimization_recommendations(
                        optimal_weights, current_weights, symbols
                    )
                }
                
                log_info("Portföy optimizasyonu tamamlandı")
                return optimization_result
            else:
                return {'error': 'Optimizasyon başarısız'}
                
        except Exception as e:
            log_error(f"Portföy optimizasyonu hatası: {e}")
            return {'error': str(e)}
    
    def calculate_stop_loss_levels(self, symbol: str, price_data: pd.DataFrame = None) -> Dict[str, Any]:
        """Stop loss seviyelerini hesapla"""
        try:
            if symbol not in self.portfolio_data:
                return {'error': 'Pozisyon bulunamadı'}
            
            position = self.portfolio_data[symbol]
            current_price = position['current_price']
            entry_price = position['entry_price']
            
            stop_loss_levels = {
                'symbol': symbol,
                'current_price': current_price,
                'entry_price': entry_price,
                'stop_loss_levels': {}
            }
            
            # Farklı stop loss stratejileri
            
            # 1. Sabit yüzde stop loss
            stop_loss_5 = entry_price * 0.95  # %5 stop loss
            stop_loss_10 = entry_price * 0.90  # %10 stop loss
            stop_loss_15 = entry_price * 0.85  # %15 stop loss
            
            stop_loss_levels['stop_loss_levels']['fixed_percentage'] = {
                '5%': stop_loss_5,
                '10%': stop_loss_10,
                '15%': stop_loss_15
            }
            
            # 2. Trailing stop loss
            if current_price > entry_price:
                trailing_5 = current_price * 0.95
                trailing_10 = current_price * 0.90
                stop_loss_levels['stop_loss_levels']['trailing'] = {
                    '5%': trailing_5,
                    '10%': trailing_10
                }
            
            # 3. ATR tabanlı stop loss
            if price_data is not None and not price_data.empty and len(price_data) > 14:
                # ATR hesapla
                high = price_data['high'] if 'high' in price_data.columns else price_data['close']
                low = price_data['low'] if 'low' in price_data.columns else price_data['close']
                close = price_data['close']
                
                tr1 = high - low
                tr2 = abs(high - close.shift(1))
                tr3 = abs(low - close.shift(1))
                tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
                atr = tr.rolling(14).mean().iloc[-1]
                
                atr_stop_1 = current_price - (atr * 1)
                atr_stop_2 = current_price - (atr * 2)
                atr_stop_3 = current_price - (atr * 3)
                
                stop_loss_levels['stop_loss_levels']['atr_based'] = {
                    '1x ATR': atr_stop_1,
                    '2x ATR': atr_stop_2,
                    '3x ATR': atr_stop_3,
                    'ATR': atr
                }
            
            # Önerilen stop loss
            if position['unrealized_pnl_pct'] > 10:  # %10+ kar varsa
                recommended_stop = current_price * 0.95  # %5 trailing stop
                stop_loss_levels['recommended'] = {
                    'type': 'trailing_5%',
                    'level': recommended_stop,
                    'reason': 'Kar koruma için trailing stop'
                }
            elif position['unrealized_pnl_pct'] > 0:  # Kar varsa
                recommended_stop = entry_price * 0.98  # %2 stop loss
                stop_loss_levels['recommended'] = {
                    'type': 'fixed_2%',
                    'level': recommended_stop,
                    'reason': 'Kar koruma için sabit stop'
                }
            else:  # Zararda
                recommended_stop = entry_price * 0.90  # %10 stop loss
                stop_loss_levels['recommended'] = {
                    'type': 'fixed_10%',
                    'level': recommended_stop,
                    'reason': 'Zarar sınırlama için stop loss'
                }
            
            return stop_loss_levels
            
        except Exception as e:
            log_error(f"Stop loss hesaplama hatası: {e}")
            return {'error': str(e)}
    
    def _get_concentration_recommendation(self, risk_level: str, max_weight: float) -> str:
        """Konsantrasyon riski önerisi"""
        if risk_level == "High":
            return f"Yüksek konsantrasyon riski - en büyük pozisyonu %{max_weight*100:.1f} azaltın"
        elif risk_level == "Medium":
            return f"Orta konsantrasyon riski - pozisyon dağılımını iyileştirin"
        else:
            return "Düşük konsantrasyon riski - iyi dağılım"
    
    def _get_optimization_recommendations(self, optimal_weights: np.ndarray, 
                                        current_weights: np.ndarray, 
                                        symbols: List[str]) -> List[str]:
        """Optimizasyon önerileri"""
        recommendations = []
        
        for i, symbol in enumerate(symbols):
            current_w = current_weights[i]
            optimal_w = optimal_weights[i]
            diff = optimal_w - current_w
            
            if abs(diff) > 0.05:  # %5'ten fazla fark varsa
                if diff > 0:
                    recommendations.append(f"{symbol}: Ağırlığı artırın (%{diff*100:.1f})")
                else:
                    recommendations.append(f"{symbol}: Ağırlığı azaltın (%{abs(diff)*100:.1f})")
        
        if not recommendations:
            recommendations.append("Portföy ağırlıkları optimal seviyede")
        
        return recommendations
    
    def get_risk_summary(self) -> Dict[str, Any]:
        """Risk özeti"""
        try:
            if not self.portfolio_data:
                return {'error': 'Portföy verisi yok'}
            
            # Genel risk metrikleri
            total_value = sum(pos['position_value'] for pos in self.portfolio_data.values())
            total_pnl = sum(pos['unrealized_pnl'] for pos in self.portfolio_data.values())
            total_pnl_pct = (total_pnl / (total_value - total_pnl)) * 100 if total_value > total_pnl else 0
            
            # Risk seviyesi
            high_risk_positions = 0
            medium_risk_positions = 0
            
            for symbol in self.portfolio_data:
                position_risk = self.calculate_position_risk(symbol)
                if position_risk.get('risk_level') == 'High':
                    high_risk_positions += 1
                elif position_risk.get('risk_level') == 'Medium':
                    medium_risk_positions += 1
            
            # Genel risk seviyesi
            if high_risk_positions > 0:
                overall_risk = 'High'
            elif medium_risk_positions > len(self.portfolio_data) * 0.5:
                overall_risk = 'Medium'
            else:
                overall_risk = 'Low'
            
            summary = {
                'total_portfolio_value': total_value,
                'total_unrealized_pnl': total_pnl,
                'total_unrealized_pnl_pct': total_pnl_pct,
                'position_count': len(self.portfolio_data),
                'high_risk_positions': high_risk_positions,
                'medium_risk_positions': medium_risk_positions,
                'overall_risk_level': overall_risk,
                'concentration_risk': self._calculate_concentration_risk(),
                'risk_metrics': self.risk_metrics,
                'last_updated': datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            log_error(f"Risk özeti hazırlanırken hata: {e}")
            return {'error': str(e)}

# Global risk manager instance
risk_manager = RiskManager()

