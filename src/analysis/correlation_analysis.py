"""
Ultra Correlation Analysis - Professional Grade
Sofistike korelasyon analizi modülü
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from typing import Dict, List, Optional, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

from src.utils.logger import log_info, log_error, log_debug

class UltraCorrelationAnalyzer:
    """Ultra-advanced correlation analysis for financial markets"""
    
    def __init__(self):
        self.benchmark_symbols = [
            'SPY',     # S&P 500
            'QQQ',     # NASDAQ 100
            'TLT',     # 20+ Year Treasury Bonds
            'GLD',     # Gold
            'VIX',     # Volatility Index
            'DXY',     # US Dollar Index
            'MSCI.IS', # MSCI Turkey (for Turkish stocks)
            'XU100.IS', # BIST 100
            'EURUSD=X', # EUR/USD
            'USDTRY=X'  # USD/TRY
        ]
        
        self.sector_etfs = [
            'XLF',  # Financial Sector
            'XLK',  # Technology Sector
            'XLE',  # Energy Sector
            'XLV',  # Healthcare Sector
            'XLI',  # Industrial Sector
            'XLY',  # Consumer Discretionary
            'XLP',  # Consumer Staples
            'XLRE', # Real Estate
            'XLU',  # Utilities
        ]
        
        self.correlation_windows = [5, 10, 21, 63, 252]  # Days
        self.correlation_cache = {}
        
    def analyze_correlations(self, symbol, stock_data):
        """Comprehensive correlation analysis"""
        try:
            if stock_data is None or len(stock_data) < 21:
                return self._default_score()
                
            # Get returns
            returns = stock_data['Close'].pct_change(fill_method=None).dropna()
            
            if len(returns) < 10:
                return self._default_score()
            
            # Multi-timeframe correlation analysis
            correlations = self._calculate_rolling_correlations(symbol, returns)
            
            # Cross-asset correlation strength
            cross_asset_score = self._analyze_cross_asset_correlations(symbol, returns)
            
            # Correlation regime analysis
            regime_score = self._analyze_correlation_regimes(returns)
            
            # Correlation stability analysis
            stability_score = self._analyze_correlation_stability(correlations)
            
            # Dynamic correlation analysis
            dynamic_score = self._analyze_dynamic_correlations(returns)
            
            # Copula-based tail dependence
            tail_dependence_score = self._analyze_tail_dependence(symbol, returns)
            
            # Rolling correlation variance
            variance_score = self._analyze_correlation_variance(correlations)
            
            # Calculate final correlation score
            final_score = self._calculate_correlation_score(
                cross_asset_score, regime_score, stability_score, 
                dynamic_score, tail_dependence_score, variance_score
            )
            
            return {
                'correlation_score': final_score,
                'cross_asset_strength': cross_asset_score,
                'regime_score': regime_score,
                'stability_score': stability_score,
                'dynamic_score': dynamic_score,
                'tail_dependence': tail_dependence_score,
                'variance_score': variance_score,
                'correlations': correlations
            }
            
        except Exception as e:
            log_error(f"Correlation analysis error for {symbol}: {e}")
            return self._default_score()
    
    def _calculate_rolling_correlations(self, symbol, returns):
        """Calculate rolling correlations with multiple benchmarks"""
        correlations = {}
        
        for benchmark in self.benchmark_symbols:
            try:
                # Check cache first
                cache_key = f"{symbol}_{benchmark}_{len(returns)}"
                if cache_key in self.correlation_cache:
                    correlations[benchmark] = self.correlation_cache[cache_key]
                    continue
                
                # Get benchmark data
                end_date = datetime.now()
                start_date = end_date - timedelta(days=400)
                
                benchmark_data = yf.download(benchmark, start=start_date, end=end_date, progress=False)
                if benchmark_data.empty:
                    continue
                    
                benchmark_returns = benchmark_data['Close'].pct_change(fill_method=None).dropna()
                
                # Align data
                common_dates = returns.index.intersection(benchmark_returns.index)
                if len(common_dates) < 10:
                    continue
                
                stock_aligned = returns.loc[common_dates]
                benchmark_aligned = benchmark_returns.loc[common_dates]
                
                # Calculate correlations for different windows
                window_correlations = {}
                for window in self.correlation_windows:
                    if len(common_dates) >= window:
                        rolling_corr = stock_aligned.rolling(window).corr(benchmark_aligned)
                        if len(rolling_corr.dropna()) > 0:
                            window_correlations[f'{window}d'] = {
                                'current': rolling_corr.iloc[-1] if not pd.isna(rolling_corr.iloc[-1]) else 0,
                                'mean': rolling_corr.mean(),
                                'std': rolling_corr.std(),
                                'min': rolling_corr.min(),
                                'max': rolling_corr.max(),
                                'trend': self._calculate_correlation_trend(rolling_corr)
                            }
                
                correlations[benchmark] = window_correlations
                self.correlation_cache[cache_key] = window_correlations
                
            except Exception as e:
                log_debug(f"Benchmark {benchmark} correlation failed: {e}")
                continue
                
        return correlations
    
    def _calculate_correlation_trend(self, rolling_corr):
        """Calculate correlation trend (increasing/decreasing)"""
        try:
            if len(rolling_corr.dropna()) < 5:
                return 0
            
            recent_values = rolling_corr.dropna().tail(5)
            if len(recent_values) < 2:
                return 0
                
            # Simple linear trend
            x = np.arange(len(recent_values))
            y = recent_values.values
            
            # Calculate slope
            if len(x) > 1:
                slope = np.polyfit(x, y, 1)[0]
                return slope
            return 0
            
        except:
            return 0
    
    def _analyze_cross_asset_correlations(self, symbol, returns):
        """Analyze cross-asset correlation strength"""
        try:
            total_correlation_strength = 0
            valid_correlations = 0
            
            # Major asset class correlations
            major_assets = ['SPY', 'TLT', 'GLD', 'VIX', 'DXY']
            
            for asset in major_assets:
                try:
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=200)
                    
                    asset_data = yf.download(asset, start=start_date, end=end_date, progress=False)
                    if asset_data.empty:
                        continue
                        
                    asset_returns = asset_data['Close'].pct_change(fill_method=None).dropna()
                    
                    # Align data
                    common_dates = returns.index.intersection(asset_returns.index)
                    if len(common_dates) < 21:
                        continue
                    
                    stock_aligned = returns.loc[common_dates]
                    asset_aligned = asset_returns.loc[common_dates]
                    
                    # Calculate multiple correlation measures
                    pearson_corr = stock_aligned.corr(asset_aligned)
                    spearman_corr = stock_aligned.rank().corr(asset_aligned.rank())
                    
                    if pd.isna(pearson_corr):
                        continue
                    
                    # Score based on correlation strength and asset type
                    if asset == 'VIX':
                        # Negative VIX correlation is good for risk management
                        strength_score = abs(pearson_corr) * 100
                        if pearson_corr < -0.3:
                            strength_score *= 1.3  # Bonus for good VIX hedge
                    elif asset == 'TLT':
                        # Treasury correlation analysis
                        strength_score = abs(pearson_corr) * 80
                        if pearson_corr < 0:
                            strength_score *= 1.1  # Flight to quality indicator
                    elif asset == 'GLD':
                        # Gold correlation for inflation hedge
                        strength_score = abs(pearson_corr) * 90
                        if pearson_corr > 0.2:
                            strength_score *= 1.1  # Inflation hedge
                    else:
                        strength_score = abs(pearson_corr) * 100
                    
                    # Add rank correlation component
                    rank_correlation_bonus = abs(spearman_corr) * 20
                    total_score = min(100, strength_score + rank_correlation_bonus)
                    
                    total_correlation_strength += total_score
                    valid_correlations += 1
                        
                except Exception as e:
                    log_debug(f"Asset {asset} correlation failed: {e}")
                    continue
            
            if valid_correlations > 0:
                avg_strength = total_correlation_strength / valid_correlations
                return min(100, avg_strength)
            else:
                return 50
                
        except:
            return 50
    
    def _analyze_correlation_regimes(self, returns):
        """Analyze correlation regime changes with advanced regime detection"""
        try:
            if len(returns) < 63:
                return 50
            
            # Calculate rolling volatility as primary regime indicator
            volatility = returns.rolling(21).std() * np.sqrt(252)
            
            # Calculate rolling skewness as secondary indicator
            skewness = returns.rolling(21).skew()
            
            # Calculate rolling kurtosis as tertiary indicator
            kurtosis = returns.rolling(21).kurt()
            
            # Multi-dimensional regime identification
            vol_threshold_high = volatility.quantile(0.75)
            vol_threshold_low = volatility.quantile(0.25)
            
            skew_threshold = abs(skewness).quantile(0.75)
            kurt_threshold = kurtosis.quantile(0.75)
            
            # Define regimes
            high_vol_regime = volatility > vol_threshold_high
            low_vol_regime = volatility < vol_threshold_low
            high_skew_regime = abs(skewness) > skew_threshold
            high_kurt_regime = kurtosis > kurt_threshold
            
            # Calculate regime-specific statistics
            regime_score = 50
            
            if high_vol_regime.sum() > 10 and low_vol_regime.sum() > 10:
                # High volatility regime analysis
                high_vol_returns = returns[high_vol_regime]
                low_vol_returns = returns[low_vol_regime]
                
                if len(high_vol_returns) > 5 and len(low_vol_returns) > 5:
                    # Regime consistency metrics
                    high_vol_sharpe = (high_vol_returns.mean() * 252) / (high_vol_returns.std() * np.sqrt(252)) if high_vol_returns.std() > 0 else 0
                    low_vol_sharpe = (low_vol_returns.mean() * 252) / (low_vol_returns.std() * np.sqrt(252)) if low_vol_returns.std() > 0 else 0
                    
                    # Regime persistence score
                    regime_transitions = (high_vol_regime != high_vol_regime.shift(1)).sum()
                    persistence_score = max(0, 100 - (regime_transitions / len(returns) * 200))
                    
                    # Regime predictability score
                    sharpe_diff = abs(high_vol_sharpe - low_vol_sharpe)
                    predictability_score = min(100, sharpe_diff * 30 + 50)
                    
                    # Combine regime metrics
                    regime_score = (persistence_score * 0.6 + predictability_score * 0.4)
            
            # Skewness regime bonus
            if high_skew_regime.sum() > 5:
                skew_bonus = min(20, abs(skewness.mean()) * 10)
                regime_score += skew_bonus
            
            # Kurtosis regime bonus (excess kurtosis indicates fat tails)
            if high_kurt_regime.sum() > 5:
                kurt_bonus = min(15, (kurtosis.mean() - 3) * 5)  # Subtract 3 for excess kurtosis
                regime_score += kurt_bonus
            
            return min(100, max(0, regime_score))
            
        except:
            return 50
    
    def _analyze_correlation_stability(self, correlations):
        """Analyze correlation stability across timeframes with advanced metrics"""
        try:
            stability_scores = []
            
            for benchmark, windows in correlations.items():
                if len(windows) < 3:
                    continue
                    
                # Collect correlation values across windows
                current_correlations = []
                mean_correlations = []
                std_correlations = []
                trends = []
                
                for window_key, window_data in windows.items():
                    if isinstance(window_data, dict):
                        if 'current' in window_data and not pd.isna(window_data['current']):
                            current_correlations.append(window_data['current'])
                        if 'mean' in window_data and not pd.isna(window_data['mean']):
                            mean_correlations.append(window_data['mean'])
                        if 'std' in window_data and not pd.isna(window_data['std']):
                            std_correlations.append(window_data['std'])
                        if 'trend' in window_data and not pd.isna(window_data['trend']):
                            trends.append(window_data['trend'])
                
                if len(current_correlations) >= 3:
                    # Current correlation stability
                    current_std = np.std(current_correlations)
                    current_stability = max(0, 100 - (current_std * 300))
                    
                    # Historical mean stability
                    if len(mean_correlations) >= 3:
                        mean_std = np.std(mean_correlations)
                        mean_stability = max(0, 100 - (mean_std * 300))
                    else:
                        mean_stability = current_stability
                    
                    # Volatility of correlations stability
                    if len(std_correlations) >= 3:
                        vol_of_vol = np.std(std_correlations)
                        vol_stability = max(0, 100 - (vol_of_vol * 500))
                    else:
                        vol_stability = 50
                    
                    # Trend consistency
                    if len(trends) >= 3:
                        trend_consistency = 100 - abs(np.std(trends)) * 1000
                        trend_consistency = max(0, min(100, trend_consistency))
                    else:
                        trend_consistency = 50
                    
                    # Weighted stability score
                    benchmark_stability = (
                        current_stability * 0.4 +
                        mean_stability * 0.3 +
                        vol_stability * 0.2 +
                        trend_consistency * 0.1
                    )
                    
                    stability_scores.append(benchmark_stability)
            
            if stability_scores:
                return np.mean(stability_scores)
            else:
                return 50
                
        except:
            return 50
    
    def _analyze_dynamic_correlations(self, returns):
        """Analyze dynamic correlation patterns with DCC-GARCH inspired methodology"""
        try:
            if len(returns) < 63:
                return 50
            
            # Multi-timeframe dynamic correlation analysis
            short_window = 21
            medium_window = 63
            long_window = 126
            
            dynamic_scores = []
            
            # Analyze with multiple market proxies
            market_proxies = ['SPY', 'QQQ', 'VIX']
            
            for proxy in market_proxies:
                try:
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=300)
                    
                    proxy_data = yf.download(proxy, start=start_date, end=end_date, progress=False)
                    if proxy_data.empty:
                        continue
                        
                    proxy_returns = proxy_data['Close'].pct_change(fill_method=None).dropna()
                    
                    # Align data
                    common_dates = returns.index.intersection(proxy_returns.index)
                    if len(common_dates) < long_window:
                        continue
                    
                    stock_aligned = returns.loc[common_dates]
                    proxy_aligned = proxy_returns.loc[common_dates]
                    
                    # Calculate dynamic correlations
                    short_corr = stock_aligned.rolling(short_window).corr(proxy_aligned)
                    medium_corr = stock_aligned.rolling(medium_window).corr(proxy_aligned)
                    long_corr = stock_aligned.rolling(long_window).corr(proxy_aligned)
                    
                    # Remove NaN values
                    short_corr = short_corr.dropna()
                    medium_corr = medium_corr.dropna()
                    long_corr = long_corr.dropna()
                    
                    if len(short_corr) > 0 and len(medium_corr) > 0 and len(long_corr) > 0:
                        # Dynamic correlation metrics
                        recent_short = short_corr.tail(5).mean()
                        recent_medium = medium_corr.tail(5).mean()
                        recent_long = long_corr.tail(5).mean()
                        
                        # Momentum in correlations
                        short_momentum = short_corr.tail(10).mean() - short_corr.tail(20).mean()
                        
                        # Correlation convergence/divergence
                        convergence = abs(recent_short - recent_long)
                        
                        # Score based on correlation dynamics
                        if proxy == 'VIX':
                            # For VIX, negative correlation momentum is positive
                            momentum_score = 50 - (short_momentum * 100)
                            if recent_short < -0.3:  # Good VIX hedge
                                momentum_score += 20
                        else:
                            # For equity indices, positive correlation momentum can be good
                            momentum_score = 50 + (short_momentum * 50)
                        
                        # Convergence score (lower convergence = higher score for stability)
                        convergence_score = max(0, 100 - (convergence * 200))
                        
                        # Trend consistency score
                        trend_score = 50
                        if len(short_corr) >= 10:
                            recent_trend = np.polyfit(range(10), short_corr.tail(10).values, 1)[0]
                            trend_score = 50 + (recent_trend * 100)
                        
                        proxy_dynamic_score = (
                            momentum_score * 0.4 +
                            convergence_score * 0.3 +
                            trend_score * 0.3
                        )
                        
                        dynamic_scores.append(min(100, max(0, proxy_dynamic_score)))
                        
                except Exception as e:
                    log_debug(f"Dynamic correlation failed for {proxy}: {e}")
                    continue
            
            if dynamic_scores:
                return np.mean(dynamic_scores)
            else:
                return 50
            
        except:
            return 50
    
    def _analyze_tail_dependence(self, symbol, returns):
        """Analyze tail dependence using simplified copula concepts"""
        try:
            if len(returns) < 63:
                return 50
            
            # Get market returns for comparison (SPY as default)
            try:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=200)
                
                market_data = yf.download('SPY', start=start_date, end=end_date, progress=False)
                if market_data.empty:
                    return 50
                    
                market_returns = market_data['Close'].pct_change(fill_method=None).dropna()
                
                # Align data
                common_dates = returns.index.intersection(market_returns.index)
                if len(common_dates) < 50:
                    return 50
                
                stock_aligned = returns.loc[common_dates]
                market_aligned = market_returns.loc[common_dates]
                
                # Calculate tail dependence measures
                stock_percentiles = stock_aligned.rank(pct=True)
                market_percentiles = market_aligned.rank(pct=True)
                
                # Upper tail dependence (both in top 10%)
                upper_tail_stock = stock_percentiles > 0.9
                upper_tail_market = market_percentiles > 0.9
                upper_tail_dependence = (upper_tail_stock & upper_tail_market).sum() / upper_tail_market.sum() if upper_tail_market.sum() > 0 else 0
                
                # Lower tail dependence (both in bottom 10%)
                lower_tail_stock = stock_percentiles < 0.1
                lower_tail_market = market_percentiles < 0.1
                lower_tail_dependence = (lower_tail_stock & lower_tail_market).sum() / lower_tail_market.sum() if lower_tail_market.sum() > 0 else 0
                
                # Asymmetric tail dependence
                tail_asymmetry = abs(upper_tail_dependence - lower_tail_dependence)
                
                # Score calculation
                # Lower tail dependence in bear markets is often higher (not always good)
                # Upper tail dependence in bull markets can be good for momentum
                tail_score = 50
                
                if upper_tail_dependence > 0.3:  # Good momentum participation
                    tail_score += 20
                if lower_tail_dependence < 0.5:  # Good downside protection
                    tail_score += 15
                if tail_asymmetry < 0.3:  # Symmetric behavior is often preferred
                    tail_score += 15
                
                return min(100, max(0, tail_score))
                
            except:
                return 50
            
        except:
            return 50
    
    def _analyze_correlation_variance(self, correlations):
        """Analyze variance in correlation patterns"""
        try:
            variance_scores = []
            
            for benchmark, windows in correlations.items():
                window_variances = []
                
                for window_key, window_data in windows.items():
                    if isinstance(window_data, dict) and 'std' in window_data:
                        if not pd.isna(window_data['std']):
                            window_variances.append(window_data['std'])
                
                if len(window_variances) >= 2:
                    # Low correlation variance is generally preferred (more stable)
                    avg_variance = np.mean(window_variances)
                    variance_score = max(0, 100 - (avg_variance * 300))  # Scale appropriately
                    variance_scores.append(variance_score)
            
            if variance_scores:
                return np.mean(variance_scores)
            else:
                return 50
                
        except:
            return 50
    
    def _calculate_correlation_score(self, cross_asset_score, regime_score, stability_score, 
                                   dynamic_score, tail_dependence_score, variance_score):
        """Calculate final correlation score with sophisticated weighting"""
        
        # Ultra-sophisticated weighting based on market conditions and importance
        weights = {
            'cross_asset': 0.25,      # Cross-asset relationships
            'regime': 0.20,           # Regime analysis
            'stability': 0.20,        # Correlation stability
            'dynamic': 0.15,          # Dynamic patterns
            'tail_dependence': 0.12,  # Tail dependence
            'variance': 0.08          # Variance patterns
        }
        
        final_score = (
            cross_asset_score * weights['cross_asset'] +
            regime_score * weights['regime'] +
            stability_score * weights['stability'] +
            dynamic_score * weights['dynamic'] +
            tail_dependence_score * weights['tail_dependence'] +
            variance_score * weights['variance']
        )
        
        # Apply sophisticated non-linear scaling
        if final_score > 85:
            # Compress extreme high scores
            final_score = 85 + (final_score - 85) * 0.3
        elif final_score < 15:
            # Compress extreme low scores
            final_score = 15 + (final_score - 15) * 0.3
        
        # Ensure realistic score distribution
        final_score = min(95, max(5, final_score))
        
        return final_score
    
    def _default_score(self):
        """Return default score when analysis fails"""
        return {
            'correlation_score': 50,
            'cross_asset_strength': 50,
            'regime_score': 50,
            'stability_score': 50,
            'dynamic_score': 50,
            'tail_dependence': 50,
            'variance_score': 50,
            'correlations': {}
        }

# Backward compatibility with existing CorrelationAnalyzer class
class CorrelationAnalyzer:
    """Varlıklar arası korelasyon analizi"""
    
    def __init__(self):
        self.correlation_matrix = None
        self.asset_data = {}
        self.cluster_groups = {}
        self.principal_components = None
        
    def add_asset_data(self, symbol: str, price_data: pd.DataFrame, 
                      analysis_data: Dict[str, Any] = None) -> bool:
        """Varlık verisi ekle"""
        try:
            if price_data is None or price_data.empty:
                log_error(f"Boş veri: {symbol}")
                return False
            
            # Fiyat verilerini hazırla
            asset_info = {
                'symbol': symbol,
                'price_data': price_data.copy(),
                'analysis_data': analysis_data or {},
                'returns': None,
                'volatility': None,
                'volume': None
            }
            
            # Günlük getirileri hesapla
            if 'close' in price_data.columns:
                asset_info['returns'] = price_data['close'].pct_change(fill_method=None).dropna()
                asset_info['volatility'] = asset_info['returns'].rolling(20).std()
            
            # Hacim verisi
            if 'volume' in price_data.columns:
                asset_info['volume'] = price_data['volume']
            
            self.asset_data[symbol] = asset_info
            log_debug(f"Varlık verisi eklendi: {symbol}")
            return True
            
        except Exception as e:
            log_error(f"Varlık verisi ekleme hatası: {e}")
            return False
    
    def calculate_correlation_matrix(self, method: str = 'pearson', 
                                   period: int = 252) -> pd.DataFrame:
        """Korelasyon matrisini hesapla"""
        try:
            if len(self.asset_data) < 2:
                log_error("En az 2 varlık gerekli")
                return pd.DataFrame()
            
            # Getiri verilerini topla
            returns_data = {}
            for symbol, data in self.asset_data.items():
                if data['returns'] is not None and len(data['returns']) >= period:
                    returns_data[symbol] = data['returns'].tail(period)
            
            if len(returns_data) < 2:
                log_error("Yeterli getiri verisi yok")
                return pd.DataFrame()
            
            # DataFrame oluştur
            returns_df = pd.DataFrame(returns_data)
            
            # Korelasyon matrisini hesapla
            if method == 'pearson':
                self.correlation_matrix = returns_df.corr(method='pearson')
            elif method == 'spearman':
                self.correlation_matrix = returns_df.corr(method='spearman')
            else:
                self.correlation_matrix = returns_df.corr()
            
            log_info(f"Korelasyon matrisi hesaplandı: {len(returns_data)} varlık")
            return self.correlation_matrix
            
        except Exception as e:
            log_error(f"Korelasyon matrisi hesaplama hatası: {e}")
            return pd.DataFrame()
    
    def find_highly_correlated_pairs(self, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Yüksek korelasyonlu varlık çiftlerini bul"""
        try:
            if self.correlation_matrix is None:
                self.calculate_correlation_matrix()
            
            if self.correlation_matrix.empty:
                return []
            
            highly_correlated = []
            
            # Üst üçgen matrisi kontrol et
            for i in range(len(self.correlation_matrix.columns)):
                for j in range(i+1, len(self.correlation_matrix.columns)):
                    symbol1 = self.correlation_matrix.columns[i]
                    symbol2 = self.correlation_matrix.columns[j]
                    correlation = self.correlation_matrix.iloc[i, j]
                    
                    if abs(correlation) >= threshold:
                        highly_correlated.append({
                            'symbol1': symbol1,
                            'symbol2': symbol2,
                            'correlation': correlation,
                            'correlation_strength': self._get_correlation_strength(abs(correlation)),
                            'relationship': 'positive' if correlation > 0 else 'negative'
                        })
            
            # Korelasyona göre sırala
            highly_correlated.sort(key=lambda x: abs(x['correlation']), reverse=True)
            
            log_info(f"{threshold} üzeri korelasyonlu {len(highly_correlated)} çift bulundu")
            return highly_correlated
            
        except Exception as e:
            log_error(f"Yüksek korelasyonlu çiftler bulunurken hata: {e}")
            return []
    
    def find_anti_correlated_pairs(self, threshold: float = -0.5) -> List[Dict[str, Any]]:
        """Negatif korelasyonlu varlık çiftlerini bul"""
        try:
            if self.correlation_matrix is None:
                self.calculate_correlation_matrix()
            
            if self.correlation_matrix.empty:
                return []
            
            anti_correlated = []
            
            # Üst üçgen matrisi kontrol et
            for i in range(len(self.correlation_matrix.columns)):
                for j in range(i+1, len(self.correlation_matrix.columns)):
                    symbol1 = self.correlation_matrix.columns[i]
                    symbol2 = self.correlation_matrix.columns[j]
                    correlation = self.correlation_matrix.iloc[i, j]
                    
                    if correlation <= threshold:
                        anti_correlated.append({
                            'symbol1': symbol1,
                            'symbol2': symbol2,
                            'correlation': correlation,
                            'correlation_strength': self._get_correlation_strength(abs(correlation)),
                            'diversification_potential': abs(correlation)
                        })
            
            # Korelasyona göre sırala (en negatif önce)
            anti_correlated.sort(key=lambda x: x['correlation'])
            
            log_info(f"{threshold} altı korelasyonlu {len(anti_correlated)} çift bulundu")
            return anti_correlated
            
        except Exception as e:
            log_error(f"Negatif korelasyonlu çiftler bulunurken hata: {e}")
            return []
    
    def perform_cluster_analysis(self, n_clusters: int = 5) -> Dict[str, Any]:
        """Küme analizi yap"""
        try:
            if not ML_AVAILABLE:
                log_error("Scikit-learn yüklü değil")
                return {}
            
            if self.correlation_matrix is None:
                self.calculate_correlation_matrix()
            
            if self.correlation_matrix.empty:
                return {}
            
            # Korelasyon matrisini distance matrisine çevir
            distance_matrix = 1 - abs(self.correlation_matrix)
            
            # KMeans kümeleme
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(distance_matrix)
            
            # Küme gruplarını oluştur
            clusters = {}
            for i, symbol in enumerate(self.correlation_matrix.columns):
                cluster_id = cluster_labels[i]
                if cluster_id not in clusters:
                    clusters[cluster_id] = []
                clusters[cluster_id].append(symbol)
            
            self.cluster_groups = clusters
            
            # Küme analizi sonuçları
            cluster_analysis = {
                'n_clusters': n_clusters,
                'clusters': clusters,
                'cluster_centers': kmeans.cluster_centers_.tolist(),
                'inertia': kmeans.inertia_,
                'silhouette_score': self._calculate_silhouette_score(distance_matrix, cluster_labels)
            }
            
            log_info(f"Küme analizi tamamlandı: {n_clusters} küme")
            return cluster_analysis
            
        except Exception as e:
            log_error(f"Küme analizi hatası: {e}")
            return {}
    
    def perform_pca_analysis(self, n_components: int = 5) -> Dict[str, Any]:
        """Principal Component Analysis"""
        try:
            if not ML_AVAILABLE:
                log_error("Scikit-learn yüklü değil")
                return {}
            
            if self.correlation_matrix is None:
                self.calculate_correlation_matrix()
            
            if self.correlation_matrix.empty:
                return {}
            
            # PCA uygula
            pca = PCA(n_components=min(n_components, len(self.correlation_matrix.columns)))
            pca_result = pca.fit_transform(self.correlation_matrix)
            
            # Bileşen açıklamaları
            explained_variance_ratio = pca.explained_variance_ratio_
            cumulative_variance = np.cumsum(explained_variance_ratio)
            
            # PCA sonuçları
            pca_analysis = {
                'n_components': pca.n_components_,
                'explained_variance_ratio': explained_variance_ratio.tolist(),
                'cumulative_variance': cumulative_variance.tolist(),
                'components': pca.components_.tolist(),
                'feature_names': self.correlation_matrix.columns.tolist(),
                'pca_result': pca_result.tolist()
            }
            
            self.principal_components = pca_analysis
            
            log_info(f"PCA analizi tamamlandı: {pca.n_components_} bileşen")
            return pca_analysis
            
        except Exception as e:
            log_error(f"PCA analizi hatası: {e}")
            return {}
    
    def calculate_portfolio_correlation(self, portfolio_symbols: List[str]) -> Dict[str, Any]:
        """Portfolio korelasyon analizi"""
        try:
            if len(portfolio_symbols) < 2:
                log_error("En az 2 varlık gerekli")
                return {}
            
            # Portfolio varlıklarının verilerini kontrol et
            missing_symbols = [s for s in portfolio_symbols if s not in self.asset_data]
            if missing_symbols:
                log_error(f"Eksik varlık verileri: {missing_symbols}")
                return {}
            
            # Portfolio korelasyon matrisi
            portfolio_corr = self.correlation_matrix.loc[portfolio_symbols, portfolio_symbols]
            
            # Portfolio istatistikleri
            avg_correlation = portfolio_corr.values[np.triu_indices_from(portfolio_corr.values, k=1)].mean()
            max_correlation = portfolio_corr.values[np.triu_indices_from(portfolio_corr.values, k=1)].max()
            min_correlation = portfolio_corr.values[np.triu_indices_from(portfolio_corr.values, k=1)].min()
            
            # Diversifikasyon skoru (düşük korelasyon = yüksek diversifikasyon)
            diversification_score = 100 * (1 - abs(avg_correlation))
            
            # Risk konsantrasyonu
            risk_concentration = self._calculate_risk_concentration(portfolio_symbols)
            
            portfolio_analysis = {
                'portfolio_symbols': portfolio_symbols,
                'correlation_matrix': portfolio_corr.to_dict(),
                'average_correlation': avg_correlation,
                'max_correlation': max_correlation,
                'min_correlation': min_correlation,
                'diversification_score': diversification_score,
                'risk_concentration': risk_concentration,
                'recommendations': self._get_portfolio_recommendations(avg_correlation, diversification_score)
            }
            
            log_info(f"Portfolio korelasyon analizi: {len(portfolio_symbols)} varlık")
            return portfolio_analysis
            
        except Exception as e:
            log_error(f"Portfolio korelasyon analizi hatası: {e}")
            return {}
    
    def find_diversification_opportunities(self, current_portfolio: List[str] = None) -> List[Dict[str, Any]]:
        """Diversifikasyon fırsatlarını bul"""
        try:
            if self.correlation_matrix is None:
                self.calculate_correlation_matrix()
            
            if self.correlation_matrix.empty:
                return []
            
            opportunities = []
            
            if current_portfolio:
                # Mevcut portfolio ile düşük korelasyonlu varlıklar
                for symbol in self.correlation_matrix.columns:
                    if symbol not in current_portfolio:
                        # Portfolio ile ortalama korelasyon
                        portfolio_correlations = [self.correlation_matrix.loc[symbol, p] for p in current_portfolio]
                        avg_correlation = np.mean(portfolio_correlations)
                        
                        if abs(avg_correlation) < 0.3:  # Düşük korelasyon
                            opportunities.append({
                                'symbol': symbol,
                                'average_correlation': avg_correlation,
                                'diversification_potential': 100 * (1 - abs(avg_correlation)),
                                'recommendation': 'Add to portfolio for diversification'
                            })
            else:
                # Genel diversifikasyon fırsatları
                anti_correlated_pairs = self.find_anti_correlated_pairs(threshold=-0.3)
                for pair in anti_correlated_pairs:
                    opportunities.append({
                        'symbol1': pair['symbol1'],
                        'symbol2': pair['symbol2'],
                        'correlation': pair['correlation'],
                        'diversification_potential': pair['diversification_potential'] * 100,
                        'recommendation': 'Pair for portfolio diversification'
                    })
            
            # Diversifikasyon potansiyeline göre sırala
            opportunities.sort(key=lambda x: x.get('diversification_potential', 0), reverse=True)
            
            log_info(f"{len(opportunities)} diversifikasyon fırsatı bulundu")
            return opportunities
            
        except Exception as e:
            log_error(f"Diversifikasyon fırsatları bulunurken hata: {e}")
            return []
    
    def _get_correlation_strength(self, correlation: float) -> str:
        """Korelasyon gücünü belirle"""
        abs_corr = abs(correlation)
        if abs_corr >= 0.9:
            return "Very Strong"
        elif abs_corr >= 0.7:
            return "Strong"
        elif abs_corr >= 0.5:
            return "Moderate"
        elif abs_corr >= 0.3:
            return "Weak"
        else:
            return "Very Weak"
    
    def _calculate_silhouette_score(self, distance_matrix: np.ndarray, cluster_labels: np.ndarray) -> float:
        """Silhouette skorunu hesapla"""
        try:
            if not ML_AVAILABLE:
                return 0.0
            
            from sklearn.metrics import silhouette_score
            return silhouette_score(distance_matrix, cluster_labels, metric='precomputed')
        except:
            return 0.0
    
    def _calculate_risk_concentration(self, portfolio_symbols: List[str]) -> float:
        """Risk konsantrasyonunu hesapla"""
        try:
            if len(portfolio_symbols) < 2:
                return 100.0
            
            # Portfolio korelasyon matrisi
            portfolio_corr = self.correlation_matrix.loc[portfolio_symbols, portfolio_symbols]
            
            # Ortalama korelasyon
            avg_correlation = portfolio_corr.values[np.triu_indices_from(portfolio_corr.values, k=1)].mean()
            
            # Risk konsantrasyonu (yüksek korelasyon = yüksek konsantrasyon)
            risk_concentration = abs(avg_correlation) * 100
            
            return risk_concentration
            
        except Exception as e:
            log_error(f"Risk konsantrasyonu hesaplama hatası: {e}")
            return 50.0
    
    def _get_portfolio_recommendations(self, avg_correlation: float, diversification_score: float) -> List[str]:
        """Portfolio önerileri"""
        recommendations = []
        
        if avg_correlation > 0.7:
            recommendations.append("Portfolio çok yüksek korelasyonlu - diversifikasyon gerekli")
        elif avg_correlation > 0.5:
            recommendations.append("Portfolio orta seviye korelasyonlu - daha fazla diversifikasyon önerilir")
        
        if diversification_score < 30:
            recommendations.append("Düşük diversifikasyon skoru - farklı sektörlerden varlık ekleyin")
        elif diversification_score > 70:
            recommendations.append("İyi diversifikasyon - mevcut yapıyı koruyun")
        
        if not recommendations:
            recommendations.append("Portfolio dengeli - mevcut yapıyı koruyun")
        
        return recommendations
    
    def get_correlation_summary(self) -> Dict[str, Any]:
        """Korelasyon analizi özeti"""
        try:
            if self.correlation_matrix is None:
                return {}
            
            # Genel istatistikler
            correlations = self.correlation_matrix.values[np.triu_indices_from(self.correlation_matrix.values, k=1)]
            
            summary = {
                'total_assets': len(self.correlation_matrix.columns),
                'total_correlations': len(correlations),
                'average_correlation': float(np.mean(correlations)),
                'max_correlation': float(np.max(correlations)),
                'min_correlation': float(np.min(correlations)),
                'std_correlation': float(np.std(correlations)),
                'high_correlation_pairs': len(self.find_highly_correlated_pairs(0.7)),
                'anti_correlation_pairs': len(self.find_anti_correlated_pairs(-0.5)),
                'correlation_matrix': self.correlation_matrix.to_dict() if not self.correlation_matrix.empty else {},
                'cluster_groups': self.cluster_groups,
                'principal_components': self.principal_components
            }
            
            return summary
            
        except Exception as e:
            log_error(f"Korelasyon özeti hazırlanırken hata: {e}")
            return {}

# Global correlation analyzer instances
correlation_analyzer = CorrelationAnalyzer()
ultra_correlation_analyzer = UltraCorrelationAnalyzer()

def get_correlation_score(symbol, stock_data):
    """
    Get ultra-sophisticated correlation score for a stock
    
    Args:
        symbol: Stock symbol
        stock_data: DataFrame with OHLCV data
        
    Returns:
        float: Correlation score (0-100)
    """
    try:
        result = ultra_correlation_analyzer.analyze_correlations(symbol, stock_data)
        return result['correlation_score']
    except:
        return 50.0

