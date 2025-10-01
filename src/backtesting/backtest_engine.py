"""
PlanB Motoru - Backtesting Engine
Geçmiş performans testi ve strateji değerlendirme
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from src.utils.logger import log_info, log_error, log_debug

class BacktestEngine:
    """Backtesting motoru"""
    
    def __init__(self):
        self.initial_capital = 100000  # Başlangıç sermayesi
        self.commission_rate = 0.001  # Komisyon oranı (%0.1)
        self.slippage_rate = 0.0005  # Slippage oranı (%0.05)
        self.results = {}
        
    def run_backtest(self, price_data: pd.DataFrame, signals: pd.Series,
                    strategy_name: str = "Test Strategy") -> Dict[str, Any]:
        """Backtest çalıştır"""
        try:
            if price_data.empty or signals.empty:
                log_error("Boş veri")
                return {}
            
            # Veri hazırlığı
            backtest_data = self._prepare_backtest_data(price_data, signals)
            
            # Backtest simülasyonu
            portfolio_values, trades = self._simulate_trading(backtest_data)
            
            # Performans metrikleri hesapla
            performance_metrics = self._calculate_performance_metrics(
                portfolio_values, trades, backtest_data
            )
            
            # Sonuçları kaydet
            self.results[strategy_name] = {
                'strategy_name': strategy_name,
                'performance_metrics': performance_metrics,
                'trades': trades,
                'portfolio_values': portfolio_values,
                'backtest_data': backtest_data,
                'created_at': datetime.now().isoformat()
            }
            
            log_info(f"Backtest tamamlandı: {strategy_name}")
            return self.results[strategy_name]
            
        except Exception as e:
            log_error(f"Backtest hatası: {e}")
            return {}
    
    def _prepare_backtest_data(self, price_data: pd.DataFrame, signals: pd.Series) -> pd.DataFrame:
        """Backtest verilerini hazırla"""
        try:
            # Veri birleştirme
            backtest_data = price_data.copy()
            
            # Sinyalleri ekle
            backtest_data['signal'] = signals.reindex(backtest_data.index, method='ffill')
            
            # Fiyat değişimleri
            backtest_data['returns'] = backtest_data['close'].pct_change(fill_method=None)
            
            # Hareketli ortalamalar
            backtest_data['sma_20'] = backtest_data['close'].rolling(20).mean()
            backtest_data['sma_50'] = backtest_data['close'].rolling(50).mean()
            
            # RSI
            delta = backtest_data['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            backtest_data['rsi'] = 100 - (100 / (1 + rs))
            
            # Bollinger Bands
            bb_period = 20
            bb_std = 2
            backtest_data['bb_middle'] = backtest_data['close'].rolling(bb_period).mean()
            bb_std_val = backtest_data['close'].rolling(bb_period).std()
            backtest_data['bb_upper'] = backtest_data['bb_middle'] + (bb_std_val * bb_std)
            backtest_data['bb_lower'] = backtest_data['bb_middle'] - (bb_std_val * bb_std)
            
            # NaN değerleri temizle
            backtest_data = backtest_data.dropna()
            
            return backtest_data
            
        except Exception as e:
            log_error(f"Backtest veri hazırlama hatası: {e}")
            return pd.DataFrame()
    
    def _simulate_trading(self, backtest_data: pd.DataFrame) -> Tuple[pd.Series, List[Dict]]:
        """Trading simülasyonu"""
        try:
            portfolio_value = self.initial_capital
            position = 0  # 0: no position, 1: long, -1: short
            position_size = 0
            entry_price = 0
            trades = []
            
            portfolio_values = pd.Series(index=backtest_data.index, dtype=float)
            
            for i, (date, row) in enumerate(backtest_data.iterrows()):
                current_price = row['close']
                signal = row['signal']
                
                # Sinyal işleme
                if signal == 1 and position != 1:  # AL sinyali
                    if position == -1:  # Short pozisyonu kapat
                        pnl = (entry_price - current_price) * position_size
                        portfolio_value += pnl
                        trades.append({
                            'entry_date': entry_date,
                            'exit_date': date,
                            'entry_price': entry_price,
                            'exit_price': current_price,
                            'position_type': 'short',
                            'position_size': position_size,
                            'pnl': pnl,
                            'pnl_pct': (pnl / (entry_price * position_size)) * 100
                        })
                    
                    # Long pozisyon aç
                    position = 1
                    position_size = portfolio_value * 0.95 / current_price  # %95 sermaye kullan
                    entry_price = current_price
                    entry_date = date
                    
                elif signal == -1 and position != -1:  # SAT sinyali
                    if position == 1:  # Long pozisyonu kapat
                        pnl = (current_price - entry_price) * position_size
                        portfolio_value += pnl
                        trades.append({
                            'entry_date': entry_date,
                            'exit_date': date,
                            'entry_price': entry_price,
                            'exit_price': current_price,
                            'position_type': 'long',
                            'position_size': position_size,
                            'pnl': pnl,
                            'pnl_pct': (pnl / (entry_price * position_size)) * 100
                        })
                    
                    # Short pozisyon aç
                    position = -1
                    position_size = portfolio_value * 0.95 / current_price
                    entry_price = current_price
                    entry_date = date
                
                # Portföy değerini güncelle
                if position == 1:  # Long pozisyon
                    portfolio_values[date] = position_size * current_price + (portfolio_value - position_size * entry_price)
                elif position == -1:  # Short pozisyon
                    portfolio_values[date] = portfolio_value + (entry_price - current_price) * position_size
                else:  # Pozisyon yok
                    portfolio_values[date] = portfolio_value
            
            # Son pozisyonu kapat
            if position != 0:
                last_price = backtest_data['close'].iloc[-1]
                last_date = backtest_data.index[-1]
                
                if position == 1:
                    pnl = (last_price - entry_price) * position_size
                else:
                    pnl = (entry_price - last_price) * position_size
                
                portfolio_value += pnl
                trades.append({
                    'entry_date': entry_date,
                    'exit_date': last_date,
                    'entry_price': entry_price,
                    'exit_price': last_price,
                    'position_type': 'long' if position == 1 else 'short',
                    'position_size': position_size,
                    'pnl': pnl,
                    'pnl_pct': (pnl / (entry_price * position_size)) * 100
                })
            
            return portfolio_values, trades
            
        except Exception as e:
            log_error(f"Trading simülasyonu hatası: {e}")
            return pd.Series(), []
    
    def _calculate_performance_metrics(self, portfolio_values: pd.Series, 
                                     trades: List[Dict], 
                                     backtest_data: pd.DataFrame) -> Dict[str, Any]:
        """Performans metriklerini hesapla"""
        try:
            if portfolio_values.empty:
                return {}
            
            # Temel metrikler
            total_return = (portfolio_values.iloc[-1] - self.initial_capital) / self.initial_capital * 100
            annualized_return = self._calculate_annualized_return(portfolio_values)
            
            # Volatilite
            returns = portfolio_values.pct_change(fill_method=None).dropna()
            volatility = returns.std() * np.sqrt(252) * 100  # Yıllık volatilite
            
            # Sharpe Ratio
            risk_free_rate = 0.02  # %2 risk-free rate
            sharpe_ratio = (annualized_return - risk_free_rate) / (volatility / 100) if volatility > 0 else 0
            
            # Maximum Drawdown
            max_drawdown = self._calculate_max_drawdown(portfolio_values)
            
            # Trade istatistikleri
            trade_stats = self._calculate_trade_statistics(trades)
            
            # Win rate
            winning_trades = [t for t in trades if t['pnl'] > 0]
            win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
            
            # Average win/loss
            avg_win = np.mean([t['pnl'] for t in winning_trades]) if winning_trades else 0
            losing_trades = [t for t in trades if t['pnl'] < 0]
            avg_loss = np.mean([t['pnl'] for t in losing_trades]) if losing_trades else 0
            
            # Profit factor
            total_wins = sum(t['pnl'] for t in winning_trades)
            total_losses = abs(sum(t['pnl'] for t in losing_trades))
            profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
            
            # Calmar Ratio
            calmar_ratio = annualized_return / abs(max_drawdown) if max_drawdown != 0 else 0
            
            # Sortino Ratio
            downside_returns = returns[returns < 0]
            downside_volatility = downside_returns.std() * np.sqrt(252) * 100
            sortino_ratio = (annualized_return - risk_free_rate) / (downside_volatility / 100) if downside_volatility > 0 else 0
            
            metrics = {
                'total_return_pct': total_return,
                'annualized_return_pct': annualized_return,
                'volatility_pct': volatility,
                'sharpe_ratio': sharpe_ratio,
                'sortino_ratio': sortino_ratio,
                'calmar_ratio': calmar_ratio,
                'max_drawdown_pct': max_drawdown,
                'win_rate_pct': win_rate,
                'total_trades': len(trades),
                'winning_trades': len(winning_trades),
                'losing_trades': len(losing_trades),
                'avg_win': avg_win,
                'avg_loss': avg_loss,
                'profit_factor': profit_factor,
                'trade_statistics': trade_stats,
                'final_portfolio_value': portfolio_values.iloc[-1],
                'initial_capital': self.initial_capital
            }
            
            return metrics
            
        except Exception as e:
            log_error(f"Performans metrikleri hesaplama hatası: {e}")
            return {}
    
    def _calculate_annualized_return(self, portfolio_values: pd.Series) -> float:
        """Yıllık getiri hesapla"""
        try:
            if len(portfolio_values) < 2:
                return 0.0
            
            total_return = (portfolio_values.iloc[-1] - portfolio_values.iloc[0]) / portfolio_values.iloc[0]
            
            # Zaman periyodu (yıl cinsinden)
            start_date = portfolio_values.index[0]
            end_date = portfolio_values.index[-1]
            time_period = (end_date - start_date).days / 365.25
            
            if time_period > 0:
                annualized_return = (1 + total_return) ** (1 / time_period) - 1
                return annualized_return * 100
            else:
                return 0.0
                
        except Exception as e:
            log_error(f"Yıllık getiri hesaplama hatası: {e}")
            return 0.0
    
    def _calculate_max_drawdown(self, portfolio_values: pd.Series) -> float:
        """Maximum drawdown hesapla"""
        try:
            if portfolio_values.empty:
                return 0.0
            
            # Running maximum
            running_max = portfolio_values.expanding().max()
            
            # Drawdown
            drawdown = (portfolio_values - running_max) / running_max
            
            # Maximum drawdown
            max_drawdown = drawdown.min() * 100
            
            return max_drawdown
            
        except Exception as e:
            log_error(f"Maximum drawdown hesaplama hatası: {e}")
            return 0.0
    
    def _calculate_trade_statistics(self, trades: List[Dict]) -> Dict[str, Any]:
        """Trade istatistikleri"""
        try:
            if not trades:
                return {}
            
            # Trade süreleri
            trade_durations = []
            for trade in trades:
                duration = (trade['exit_date'] - trade['entry_date']).days
                trade_durations.append(duration)
            
            # PnL dağılımı
            pnls = [trade['pnl'] for trade in trades]
            pnl_pcts = [trade['pnl_pct'] for trade in trades]
            
            stats = {
                'avg_trade_duration_days': np.mean(trade_durations) if trade_durations else 0,
                'max_trade_duration_days': max(trade_durations) if trade_durations else 0,
                'min_trade_duration_days': min(trade_durations) if trade_durations else 0,
                'avg_pnl': np.mean(pnls),
                'max_pnl': max(pnls),
                'min_pnl': min(pnls),
                'avg_pnl_pct': np.mean(pnl_pcts),
                'max_pnl_pct': max(pnl_pcts),
                'min_pnl_pct': min(pnl_pcts),
                'pnl_std': np.std(pnls),
                'consecutive_wins': self._calculate_consecutive_wins(trades),
                'consecutive_losses': self._calculate_consecutive_losses(trades)
            }
            
            return stats
            
        except Exception as e:
            log_error(f"Trade istatistikleri hesaplama hatası: {e}")
            return {}
    
    def _calculate_consecutive_wins(self, trades: List[Dict]) -> int:
        """Ardışık kazanç sayısı"""
        try:
            max_consecutive = 0
            current_consecutive = 0
            
            for trade in trades:
                if trade['pnl'] > 0:
                    current_consecutive += 1
                    max_consecutive = max(max_consecutive, current_consecutive)
                else:
                    current_consecutive = 0
            
            return max_consecutive
            
        except Exception as e:
            return 0
    
    def _calculate_consecutive_losses(self, trades: List[Dict]) -> int:
        """Ardışık kayıp sayısı"""
        try:
            max_consecutive = 0
            current_consecutive = 0
            
            for trade in trades:
                if trade['pnl'] < 0:
                    current_consecutive += 1
                    max_consecutive = max(max_consecutive, current_consecutive)
                else:
                    current_consecutive = 0
            
            return max_consecutive
            
        except Exception as e:
            return 0
    
    def compare_strategies(self, strategy_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Stratejileri karşılaştır"""
        try:
            if not strategy_results:
                return {}
            
            comparison = {
                'strategies': [],
                'best_strategy': None,
                'worst_strategy': None,
                'comparison_metrics': {}
            }
            
            # Her strateji için metrikleri topla
            for result in strategy_results:
                strategy_name = result.get('strategy_name', 'Unknown')
                metrics = result.get('performance_metrics', {})
                
                strategy_info = {
                    'name': strategy_name,
                    'total_return': metrics.get('total_return_pct', 0),
                    'sharpe_ratio': metrics.get('sharpe_ratio', 0),
                    'max_drawdown': metrics.get('max_drawdown_pct', 0),
                    'win_rate': metrics.get('win_rate_pct', 0),
                    'total_trades': metrics.get('total_trades', 0)
                }
                
                comparison['strategies'].append(strategy_info)
            
            # En iyi ve en kötü stratejileri bul
            if comparison['strategies']:
                # Sharpe ratio'ya göre sırala
                sorted_strategies = sorted(comparison['strategies'], 
                                         key=lambda x: x['sharpe_ratio'], reverse=True)
                
                comparison['best_strategy'] = sorted_strategies[0]
                comparison['worst_strategy'] = sorted_strategies[-1]
                
                # Karşılaştırma metrikleri
                comparison['comparison_metrics'] = {
                    'avg_return': np.mean([s['total_return'] for s in comparison['strategies']]),
                    'avg_sharpe': np.mean([s['sharpe_ratio'] for s in comparison['strategies']]),
                    'avg_drawdown': np.mean([s['max_drawdown'] for s in comparison['strategies']]),
                    'avg_win_rate': np.mean([s['win_rate'] for s in comparison['strategies']]),
                    'return_std': np.std([s['total_return'] for s in comparison['strategies']]),
                    'sharpe_std': np.std([s['sharpe_ratio'] for s in comparison['strategies']])
                }
            
            return comparison
            
        except Exception as e:
            log_error(f"Strateji karşılaştırma hatası: {e}")
            return {}
    
    def generate_backtest_report(self, strategy_name: str) -> Dict[str, Any]:
        """Backtest raporu oluştur"""
        try:
            if strategy_name not in self.results:
                return {'error': 'Strateji bulunamadı'}
            
            result = self.results[strategy_name]
            metrics = result.get('performance_metrics', {})
            trades = result.get('trades', [])
            
            # Rapor oluştur
            report = {
                'strategy_name': strategy_name,
                'backtest_period': {
                    'start_date': result['backtest_data'].index[0].isoformat(),
                    'end_date': result['backtest_data'].index[-1].isoformat(),
                    'total_days': (result['backtest_data'].index[-1] - result['backtest_data'].index[0]).days
                },
                'performance_summary': {
                    'total_return_pct': metrics.get('total_return_pct', 0),
                    'annualized_return_pct': metrics.get('annualized_return_pct', 0),
                    'volatility_pct': metrics.get('volatility_pct', 0),
                    'sharpe_ratio': metrics.get('sharpe_ratio', 0),
                    'max_drawdown_pct': metrics.get('max_drawdown_pct', 0),
                    'win_rate_pct': metrics.get('win_rate_pct', 0),
                    'total_trades': metrics.get('total_trades', 0)
                },
                'risk_metrics': {
                    'sortino_ratio': metrics.get('sortino_ratio', 0),
                    'calmar_ratio': metrics.get('calmar_ratio', 0),
                    'profit_factor': metrics.get('profit_factor', 0),
                    'avg_win': metrics.get('avg_win', 0),
                    'avg_loss': metrics.get('avg_loss', 0)
                },
                'trade_analysis': {
                    'winning_trades': metrics.get('winning_trades', 0),
                    'losing_trades': metrics.get('losing_trades', 0),
                    'consecutive_wins': metrics.get('trade_statistics', {}).get('consecutive_wins', 0),
                    'consecutive_losses': metrics.get('trade_statistics', {}).get('consecutive_losses', 0),
                    'avg_trade_duration': metrics.get('trade_statistics', {}).get('avg_trade_duration_days', 0)
                },
                'recommendations': self._generate_recommendations(metrics),
                'created_at': result.get('created_at', ''),
                'report_generated_at': datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            log_error(f"Backtest raporu oluşturma hatası: {e}")
            return {'error': str(e)}
    
    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[str]:
        """Öneriler oluştur"""
        recommendations = []
        
        # Sharpe ratio önerileri
        sharpe = metrics.get('sharpe_ratio', 0)
        if sharpe < 0.5:
            recommendations.append("Düşük Sharpe ratio - risk/ödül dengesini iyileştirin")
        elif sharpe > 2.0:
            recommendations.append("Mükemmel Sharpe ratio - strateji çok iyi performans gösteriyor")
        
        # Drawdown önerileri
        max_dd = metrics.get('max_drawdown_pct', 0)
        if max_dd < -20:
            recommendations.append("Yüksek maximum drawdown - risk yönetimi ekleyin")
        elif max_dd > -5:
            recommendations.append("Düşük drawdown - iyi risk kontrolü")
        
        # Win rate önerileri
        win_rate = metrics.get('win_rate_pct', 0)
        if win_rate < 40:
            recommendations.append("Düşük win rate - giriş kriterlerini iyileştirin")
        elif win_rate > 70:
            recommendations.append("Yüksek win rate - strateji güvenilir")
        
        # Trade sayısı önerileri
        total_trades = metrics.get('total_trades', 0)
        if total_trades < 10:
            recommendations.append("Az trade - daha fazla işlem fırsatı arayın")
        elif total_trades > 100:
            recommendations.append("Çok fazla trade - işlem sıklığını azaltın")
        
        if not recommendations:
            recommendations.append("Strateji dengeli - mevcut parametreleri koruyun")
        
        return recommendations
    
    def get_all_results(self) -> Dict[str, Any]:
        """Tüm backtest sonuçlarını getir"""
        return self.results

# Global backtest engine instance
backtest_engine = BacktestEngine()

