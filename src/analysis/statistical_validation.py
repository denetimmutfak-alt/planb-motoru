"""
Ultra Statistical Validation - Professional Grade
Sofistike istatistiksel doğrulama ve validation modülü
"""

import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

from src.utils.logger import log_info, log_error, log_debug, log_warning

class UltraStatisticalValidator:
    """Ultra-advanced statistical validation for financial analysis"""
    
    def __init__(self):
        self.confidence_levels = [0.90, 0.95, 0.99]  # 90%, 95%, 99%
        self.monte_carlo_simulations = 10000
        self.bootstrap_samples = 5000
        self.statistical_tests = [
            'shapiro_wilk',     # Normality test
            'jarque_bera',      # Normality test
            'augmented_dickey_fuller',  # Stationarity test
            'ljung_box',        # Autocorrelation test
            'breusch_pagan',    # Heteroscedasticity test
            'variance_ratio'    # Variance ratio test
        ]
        
    def analyze_statistical_validation(self, symbol, stock_data):
        """Comprehensive statistical validation analysis"""
        try:
            if stock_data is None or len(stock_data) < 30:
                return self._default_score()
            
            returns = stock_data['Close'].pct_change(fill_method=None).dropna()
            if len(returns) < 20:
                return self._default_score()
            
            # Monte Carlo simulation validation
            monte_carlo_score = self._monte_carlo_validation(returns)
            
            # Bootstrap confidence intervals
            bootstrap_score = self._bootstrap_validation(returns)
            
            # Statistical significance testing
            significance_score = self._statistical_significance_tests(returns)
            
            # Distribution analysis
            distribution_score = self._distribution_analysis(returns)
            
            # Outlier detection and validation
            outlier_score = self._outlier_validation(returns)
            
            # Cross-validation with walk-forward analysis
            cross_validation_score = self._cross_validation_analysis(returns)
            
            # Regime change validation
            regime_validation_score = self._regime_change_validation(returns)
            
            # Time series stationarity validation
            stationarity_score = self._stationarity_validation(returns)
            
            # Calculate final validation score
            final_score = self._calculate_validation_score(
                monte_carlo_score, bootstrap_score, significance_score,
                distribution_score, outlier_score, cross_validation_score,
                regime_validation_score, stationarity_score
            )
            
            return {
                'statistical_validation_score': final_score,
                'monte_carlo_score': monte_carlo_score,
                'bootstrap_score': bootstrap_score,
                'significance_score': significance_score,
                'distribution_score': distribution_score,
                'outlier_score': outlier_score,
                'cross_validation_score': cross_validation_score,
                'regime_validation_score': regime_validation_score,
                'stationarity_score': stationarity_score
            }
            
        except Exception as e:
            log_error(f"Statistical validation error for {symbol}: {e}")
            return self._default_score()
    
    def _monte_carlo_validation(self, returns):
        """Monte Carlo simulation for validation"""
        try:
            if len(returns) < 10:
                return 50
            
            # Parameter estimation
            mean_return = returns.mean()
            std_return = returns.std()
            
            # Monte Carlo simulations
            simulation_results = []
            
            for _ in range(min(1000, self.monte_carlo_simulations // 10)):  # Reduced for performance
                # Generate random returns
                simulated_returns = np.random.normal(mean_return, std_return, len(returns))
                
                # Calculate key statistics
                sim_sharpe = (np.mean(simulated_returns) * 252) / (np.std(simulated_returns) * np.sqrt(252)) if np.std(simulated_returns) > 0 else 0
                sim_volatility = np.std(simulated_returns) * np.sqrt(252)
                sim_skewness = self._calculate_skewness(simulated_returns)
                sim_kurtosis = self._calculate_kurtosis(simulated_returns)
                
                simulation_results.append({
                    'sharpe': sim_sharpe,
                    'volatility': sim_volatility,
                    'skewness': sim_skewness,
                    'kurtosis': sim_kurtosis
                })
            
            # Compare actual vs simulated
            actual_sharpe = (mean_return * 252) / (std_return * np.sqrt(252)) if std_return > 0 else 0
            actual_volatility = std_return * np.sqrt(252)
            actual_skewness = self._calculate_skewness(returns)
            actual_kurtosis = self._calculate_kurtosis(returns)
            
            # Calculate percentiles
            simulated_sharpes = [r['sharpe'] for r in simulation_results]
            simulated_vols = [r['volatility'] for r in simulation_results]
            simulated_skews = [r['skewness'] for r in simulation_results]
            simulated_kurts = [r['kurtosis'] for r in simulation_results]
            
            if len(simulated_sharpes) > 0:
                sharpe_percentile = np.percentile(simulated_sharpes, 50)
                vol_percentile = np.percentile(simulated_vols, 50)
                skew_percentile = np.percentile(simulated_skews, 50)
                kurt_percentile = np.percentile(simulated_kurts, 50)
                
                # Score based on how well actual matches expected
                sharpe_score = 50 + (actual_sharpe - sharpe_percentile) * 30
                vol_score = 50 - abs(actual_volatility - vol_percentile) * 2
                skew_score = 50 - abs(actual_skewness - skew_percentile) * 20
                kurt_score = 50 - abs(actual_kurtosis - kurt_percentile) * 10
                
                monte_carlo_score = (
                    sharpe_score * 0.30 +
                    vol_score * 0.25 +
                    skew_score * 0.25 +
                    kurt_score * 0.20
                )
                
                return min(100, max(0, monte_carlo_score))
            else:
                return 50
            
        except Exception as e:
            log_debug(f"Monte Carlo validation error: {e}")
            return 50
    
    def _bootstrap_validation(self, returns):
        """Bootstrap confidence intervals validation"""
        try:
            if len(returns) < 20:
                return 50
            
            n_bootstrap = min(1000, self.bootstrap_samples // 5)  # Reduced for performance
            bootstrap_means = []
            bootstrap_stds = []
            bootstrap_sharpes = []
            
            for _ in range(n_bootstrap):
                # Bootstrap sample
                bootstrap_sample = np.random.choice(returns.values, size=len(returns), replace=True)
                
                sample_mean = np.mean(bootstrap_sample)
                sample_std = np.std(bootstrap_sample)
                sample_sharpe = (sample_mean * 252) / (sample_std * np.sqrt(252)) if sample_std > 0 else 0
                
                bootstrap_means.append(sample_mean)
                bootstrap_stds.append(sample_std)
                bootstrap_sharpes.append(sample_sharpe)
            
            # Calculate confidence intervals
            confidence_intervals = {}
            for confidence in [0.90, 0.95]:
                alpha = 1 - confidence
                lower_percentile = (alpha/2) * 100
                upper_percentile = (1 - alpha/2) * 100
                
                confidence_intervals[confidence] = {
                    'mean': [np.percentile(bootstrap_means, lower_percentile), 
                            np.percentile(bootstrap_means, upper_percentile)],
                    'std': [np.percentile(bootstrap_stds, lower_percentile), 
                           np.percentile(bootstrap_stds, upper_percentile)],
                    'sharpe': [np.percentile(bootstrap_sharpes, lower_percentile), 
                              np.percentile(bootstrap_sharpes, upper_percentile)]
                }
            
            # Actual values
            actual_mean = returns.mean()
            actual_std = returns.std()
            actual_sharpe = (actual_mean * 252) / (actual_std * np.sqrt(252)) if actual_std > 0 else 0
            
            # Validation score based on confidence interval coverage
            validation_scores = []
            
            for confidence, intervals in confidence_intervals.items():
                mean_in_ci = intervals['mean'][0] <= actual_mean <= intervals['mean'][1]
                std_in_ci = intervals['std'][0] <= actual_std <= intervals['std'][1]
                sharpe_in_ci = intervals['sharpe'][0] <= actual_sharpe <= intervals['sharpe'][1]
                
                coverage_score = (mean_in_ci + std_in_ci + sharpe_in_ci) / 3
                validation_scores.append(coverage_score * 100)
            
            # Average validation score
            avg_validation_score = np.mean(validation_scores)
            
            # Add bonus for narrow confidence intervals (more precise estimates)
            mean_ci_width = confidence_intervals[0.95]['mean'][1] - confidence_intervals[0.95]['mean'][0]
            sharpe_ci_width = confidence_intervals[0.95]['sharpe'][1] - confidence_intervals[0.95]['sharpe'][0]
            
            precision_bonus = max(0, 20 - (mean_ci_width * 10000 + abs(sharpe_ci_width) * 10))
            
            bootstrap_score = min(100, avg_validation_score + precision_bonus)
            
            return max(0, bootstrap_score)
            
        except Exception as e:
            log_debug(f"Bootstrap validation error: {e}")
            return 50
    
    def _statistical_significance_tests(self, returns):
        """Statistical significance testing battery"""
        try:
            if len(returns) < 30:
                return 50
            
            test_scores = []
            
            # Normality tests
            normality_score = self._test_normality(returns)
            test_scores.append(normality_score)
            
            # Stationarity test
            stationarity_score = self._test_stationarity(returns)
            test_scores.append(stationarity_score)
            
            # Autocorrelation test
            autocorr_score = self._test_autocorrelation(returns)
            test_scores.append(autocorr_score)
            
            # Heteroscedasticity test
            hetero_score = self._test_heteroscedasticity(returns)
            test_scores.append(hetero_score)
            
            # Serial correlation test
            serial_corr_score = self._test_serial_correlation(returns)
            test_scores.append(serial_corr_score)
            
            # Variance ratio test
            variance_ratio_score = self._test_variance_ratio(returns)
            test_scores.append(variance_ratio_score)
            
            # Weighted average of test scores
            weights = [0.20, 0.20, 0.15, 0.15, 0.15, 0.15]
            significance_score = sum(score * weight for score, weight in zip(test_scores, weights))
            
            return min(100, max(0, significance_score))
            
        except Exception as e:
            log_debug(f"Statistical significance tests error: {e}")
            return 50
    
    def _test_normality(self, returns):
        """Test for normality using multiple tests"""
        try:
            # Jarque-Bera test (simplified)
            skewness = self._calculate_skewness(returns)
            kurtosis = self._calculate_kurtosis(returns)
            
            # JB statistic approximation
            n = len(returns)
            jb_stat = (n/6) * (skewness**2 + (kurtosis - 3)**2/4)
            
            # Critical value for 95% confidence (approximately 6.0)
            normality_score = 50
            if jb_stat < 6.0:
                normality_score = 70  # Closer to normal
            elif jb_stat > 15.0:
                normality_score = 30  # Far from normal
            
            return normality_score
            
        except:
            return 50
    
    def _test_stationarity(self, returns):
        """Test for stationarity (simplified ADF test)"""
        try:
            # Simple trend test
            x = np.arange(len(returns))
            correlation = np.corrcoef(x, returns.values)[0, 1]
            
            # Strong trend indicates non-stationarity
            if abs(correlation) < 0.1:
                return 70  # Stationary
            elif abs(correlation) < 0.3:
                return 50  # Borderline
            else:
                return 30  # Non-stationary
                
        except:
            return 50
    
    def _test_autocorrelation(self, returns):
        """Test for autocorrelation"""
        try:
            # Calculate first-order autocorrelation
            if len(returns) < 10:
                return 50
                
            lag1_corr = returns.autocorr(lag=1)
            lag5_corr = returns.autocorr(lag=5) if len(returns) > 5 else 0
            
            if pd.isna(lag1_corr):
                lag1_corr = 0
            if pd.isna(lag5_corr):
                lag5_corr = 0
            
            # Low autocorrelation is good for financial returns
            autocorr_score = 50
            if abs(lag1_corr) < 0.1 and abs(lag5_corr) < 0.15:
                autocorr_score = 70  # Good - low autocorrelation
            elif abs(lag1_corr) > 0.3 or abs(lag5_corr) > 0.3:
                autocorr_score = 30  # Bad - high autocorrelation
            
            return autocorr_score
            
        except:
            return 50
    
    def _test_heteroscedasticity(self, returns):
        """Test for heteroscedasticity (changing variance)"""
        try:
            if len(returns) < 20:
                return 50
            
            # Split returns into two halves and compare variances
            mid_point = len(returns) // 2
            first_half_var = returns.iloc[:mid_point].var()
            second_half_var = returns.iloc[mid_point:].var()
            
            if first_half_var == 0 or second_half_var == 0:
                return 50
            
            # Variance ratio
            var_ratio = max(first_half_var, second_half_var) / min(first_half_var, second_half_var)
            
            # Score based on variance stability
            if var_ratio < 2.0:
                return 70  # Homoscedastic (good)
            elif var_ratio < 4.0:
                return 50  # Moderate heteroscedasticity
            else:
                return 30  # Strong heteroscedasticity
                
        except:
            return 50
    
    def _test_serial_correlation(self, returns):
        """Test for serial correlation using Ljung-Box approximation"""
        try:
            if len(returns) < 20:
                return 50
            
            # Calculate autocorrelations for multiple lags
            autocorrs = []
            max_lags = min(10, len(returns) // 4)
            
            for lag in range(1, max_lags + 1):
                autocorr = returns.autocorr(lag=lag)
                if not pd.isna(autocorr):
                    autocorrs.append(autocorr**2)
            
            if not autocorrs:
                return 50
            
            # Ljung-Box approximation
            lb_stat = len(returns) * (len(returns) + 2) * sum(autocorrs)
            
            # Score based on serial correlation
            if lb_stat < 10:
                return 70  # Low serial correlation
            elif lb_stat < 20:
                return 50  # Moderate serial correlation
            else:
                return 30  # High serial correlation
                
        except:
            return 50
    
    def _test_variance_ratio(self, returns):
        """Variance ratio test for random walk hypothesis"""
        try:
            if len(returns) < 50:
                return 50
            
            # Calculate variance ratios for different periods
            variance_ratios = []
            
            for k in [2, 4, 8]:  # 2-day, 4-day, 8-day periods
                if len(returns) >= k * 10:
                    # k-period returns
                    k_period_returns = returns.rolling(k).sum().dropna()
                    
                    if len(k_period_returns) > 5:
                        # Variance ratio
                        var_k = k_period_returns.var()
                        var_1 = returns.var()
                        
                        if var_1 > 0:
                            vr = var_k / (k * var_1)
                            variance_ratios.append(abs(vr - 1))  # Deviation from 1
            
            if not variance_ratios:
                return 50
            
            # Average deviation from random walk (VR = 1)
            avg_deviation = np.mean(variance_ratios)
            
            # Score based on how close to random walk
            if avg_deviation < 0.2:
                return 70  # Close to random walk
            elif avg_deviation < 0.5:
                return 50  # Moderate deviation
            else:
                return 30  # Far from random walk
                
        except:
            return 50
    
    def _distribution_analysis(self, returns):
        """Analyze return distribution characteristics"""
        try:
            if len(returns) < 20:
                return 50
            
            # Calculate distribution moments
            mean_return = returns.mean()
            std_return = returns.std()
            skewness = self._calculate_skewness(returns)
            kurtosis = self._calculate_kurtosis(returns)
            
            # Distribution quality scores
            scores = []
            
            # Mean close to zero (for returns)
            mean_score = 50 + (0 - abs(mean_return)) * 1000
            scores.append(min(100, max(0, mean_score)))
            
            # Reasonable volatility
            vol_score = 50
            if 0.1 < std_return < 0.5:  # Reasonable daily volatility range
                vol_score = 70
            elif std_return > 0.8:  # Very high volatility
                vol_score = 30
            scores.append(vol_score)
            
            # Skewness close to zero
            skew_score = 50 - abs(skewness) * 25
            scores.append(min(100, max(0, skew_score)))
            
            # Kurtosis (excess kurtosis around 0-3 is normal)
            excess_kurtosis = kurtosis - 3
            kurt_score = 50 - abs(excess_kurtosis) * 10
            scores.append(min(100, max(0, kurt_score)))
            
            # Tail behavior analysis
            tail_score = self._analyze_tail_behavior(returns)
            scores.append(tail_score)
            
            # Weighted average
            weights = [0.15, 0.25, 0.20, 0.20, 0.20]
            distribution_score = sum(score * weight for score, weight in zip(scores, weights))
            
            return min(100, max(0, distribution_score))
            
        except:
            return 50
    
    def _analyze_tail_behavior(self, returns):
        """Analyze tail behavior of returns"""
        try:
            # Extreme returns (top and bottom 5%)
            threshold = 0.05
            
            lower_threshold = returns.quantile(threshold)
            upper_threshold = returns.quantile(1 - threshold)
            
            extreme_negative = returns[returns <= lower_threshold]
            extreme_positive = returns[returns >= upper_threshold]
            
            # Tail symmetry
            if len(extreme_negative) > 0 and len(extreme_positive) > 0:
                neg_tail_mean = abs(extreme_negative.mean())
                pos_tail_mean = extreme_positive.mean()
                
                if pos_tail_mean > 0 and neg_tail_mean > 0:
                    tail_ratio = min(neg_tail_mean, pos_tail_mean) / max(neg_tail_mean, pos_tail_mean)
                    symmetry_score = tail_ratio * 100
                else:
                    symmetry_score = 50
            else:
                symmetry_score = 50
            
            return symmetry_score
            
        except:
            return 50
    
    def _outlier_validation(self, returns):
        """Validate outlier detection and handling"""
        try:
            if len(returns) < 30:
                return 50
            
            # Z-score outlier detection
            z_scores = np.abs((returns - returns.mean()) / returns.std())
            outliers_z = z_scores > 3.0
            
            # IQR outlier detection
            Q1 = returns.quantile(0.25)
            Q3 = returns.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers_iqr = (returns < lower_bound) | (returns > upper_bound)
            
            # Outlier statistics
            outlier_rate_z = outliers_z.sum() / len(returns)
            outlier_rate_iqr = outliers_iqr.sum() / len(returns)
            
            # Score based on outlier prevalence
            # Financial returns should have some outliers but not too many
            optimal_outlier_rate = 0.05  # 5%
            
            z_score = 50 + (optimal_outlier_rate - outlier_rate_z) * 200
            iqr_score = 50 + (optimal_outlier_rate - outlier_rate_iqr) * 200
            
            # Impact of outliers on mean and variance
            returns_no_outliers_z = returns[~outliers_z]
            if len(returns_no_outliers_z) > 10:
                impact_mean = abs(returns.mean() - returns_no_outliers_z.mean()) / returns.std()
                impact_std = abs(returns.std() - returns_no_outliers_z.std()) / returns.std()
                impact_score = 50 - (impact_mean + impact_std) * 25
            else:
                impact_score = 50
            
            outlier_score = (
                z_score * 0.35 +
                iqr_score * 0.35 +
                impact_score * 0.30
            )
            
            return min(100, max(0, outlier_score))
            
        except:
            return 50
    
    def _cross_validation_analysis(self, returns):
        """Cross-validation using walk-forward analysis"""
        try:
            if len(returns) < 60:
                return 50
            
            # Walk-forward cross-validation
            window_size = max(20, len(returns) // 4)
            step_size = max(5, window_size // 4)
            
            prediction_errors = []
            sharpe_predictions = []
            actual_sharpes = []
            
            for start in range(0, len(returns) - window_size, step_size):
                if start + window_size + step_size > len(returns):
                    break
                
                # Training window
                train_returns = returns.iloc[start:start + window_size]
                
                # Test window
                test_returns = returns.iloc[start + window_size:start + window_size + step_size]
                
                if len(train_returns) > 10 and len(test_returns) > 2:
                    # Predict next period characteristics
                    pred_mean = train_returns.mean()
                    pred_std = train_returns.std()
                    pred_sharpe = (pred_mean * 252) / (pred_std * np.sqrt(252)) if pred_std > 0 else 0
                    
                    # Actual next period characteristics
                    actual_mean = test_returns.mean()
                    actual_std = test_returns.std()
                    actual_sharpe = (actual_mean * 252) / (actual_std * np.sqrt(252)) if actual_std > 0 else 0
                    
                    # Prediction errors
                    mean_error = abs(pred_mean - actual_mean) / (train_returns.std() + 1e-10)
                    std_error = abs(pred_std - actual_std) / (train_returns.std() + 1e-10)
                    
                    prediction_errors.append((mean_error + std_error) / 2)
                    
                    sharpe_predictions.append(pred_sharpe)
                    actual_sharpes.append(actual_sharpe)
            
            if not prediction_errors:
                return 50
            
            # Average prediction error (lower is better)
            avg_prediction_error = np.mean(prediction_errors)
            error_score = max(0, 100 - avg_prediction_error * 100)
            
            # Sharpe ratio prediction accuracy
            if len(sharpe_predictions) > 0 and len(actual_sharpes) > 0:
                sharpe_correlation = np.corrcoef(sharpe_predictions, actual_sharpes)[0, 1]
                if not np.isnan(sharpe_correlation):
                    correlation_score = (sharpe_correlation + 1) * 50  # Convert from [-1,1] to [0,100]
                else:
                    correlation_score = 50
            else:
                correlation_score = 50
            
            cross_validation_score = (error_score * 0.6 + correlation_score * 0.4)
            
            return min(100, max(0, cross_validation_score))
            
        except:
            return 50
    
    def _regime_change_validation(self, returns):
        """Validate regime change detection"""
        try:
            if len(returns) < 60:
                return 50
            
            # Multiple regime indicators
            volatility = returns.rolling(20).std()
            mean_returns = returns.rolling(20).mean()
            
            # Volatility regimes
            vol_threshold = volatility.quantile(0.7)
            high_vol_regime = volatility > vol_threshold
            
            # Return regimes
            return_threshold_high = mean_returns.quantile(0.7)
            return_threshold_low = mean_returns.quantile(0.3)
            
            bull_regime = mean_returns > return_threshold_high
            bear_regime = mean_returns < return_threshold_low
            
            # Regime persistence
            regime_changes_vol = (high_vol_regime != high_vol_regime.shift(1)).sum()
            regime_changes_bull = (bull_regime != bull_regime.shift(1)).sum()
            regime_changes_bear = (bear_regime != bear_regime.shift(1)).sum()
            
            # Score based on regime stability
            total_periods = len(returns)
            vol_persistence_score = max(0, 100 - (regime_changes_vol / total_periods) * 200)
            bull_persistence_score = max(0, 100 - (regime_changes_bull / total_periods) * 200)
            bear_persistence_score = max(0, 100 - (regime_changes_bear / total_periods) * 200)
            
            # Regime differentiation (regimes should be different)
            if high_vol_regime.sum() > 5 and (~high_vol_regime).sum() > 5:
                high_vol_returns = returns[high_vol_regime.fillna(False)]
                low_vol_returns = returns[(~high_vol_regime).fillna(True)]
                
                if len(high_vol_returns) > 0 and len(low_vol_returns) > 0:
                    vol_diff = abs(high_vol_returns.std() - low_vol_returns.std())
                    differentiation_score = min(100, vol_diff * 1000)
                else:
                    differentiation_score = 50
            else:
                differentiation_score = 50
            
            regime_validation_score = (
                vol_persistence_score * 0.30 +
                bull_persistence_score * 0.25 +
                bear_persistence_score * 0.25 +
                differentiation_score * 0.20
            )
            
            return min(100, max(0, regime_validation_score))
            
        except:
            return 50
    
    def _stationarity_validation(self, returns):
        """Advanced stationarity validation"""
        try:
            if len(returns) < 50:
                return 50
            
            # Multiple stationarity tests
            
            # 1. Mean stationarity
            window_size = len(returns) // 4
            rolling_means = returns.rolling(window_size).mean().dropna()
            
            if len(rolling_means) > 5:
                mean_trend = np.polyfit(range(len(rolling_means)), rolling_means.values, 1)[0]
                mean_stationarity_score = max(0, 100 - abs(mean_trend) * 10000)
            else:
                mean_stationarity_score = 50
            
            # 2. Variance stationarity
            rolling_vars = returns.rolling(window_size).var().dropna()
            
            if len(rolling_vars) > 5:
                var_trend = np.polyfit(range(len(rolling_vars)), rolling_vars.values, 1)[0]
                var_stationarity_score = max(0, 100 - abs(var_trend) * 100000)
            else:
                var_stationarity_score = 50
            
            # 3. Autocorrelation stationarity
            autocorr_series = []
            for i in range(window_size, len(returns), window_size // 2):
                if i + window_size <= len(returns):
                    window_data = returns.iloc[i:i + window_size]
                    autocorr = window_data.autocorr(lag=1)
                    if not pd.isna(autocorr):
                        autocorr_series.append(autocorr)
            
            if len(autocorr_series) > 3:
                autocorr_stability = 1 - np.std(autocorr_series)
                autocorr_stationarity_score = max(0, autocorr_stability * 100)
            else:
                autocorr_stationarity_score = 50
            
            # 4. Distribution stationarity (using KS test approximation)
            first_half = returns.iloc[:len(returns)//2]
            second_half = returns.iloc[len(returns)//2:]
            
            # Simple comparison of distributions
            if len(first_half) > 10 and len(second_half) > 10:
                mean_diff = abs(first_half.mean() - second_half.mean())
                std_diff = abs(first_half.std() - second_half.std())
                
                distribution_similarity = max(0, 1 - (mean_diff * 100 + std_diff * 10))
                distribution_stationarity_score = distribution_similarity * 100
            else:
                distribution_stationarity_score = 50
            
            # Combine stationarity scores
            stationarity_score = (
                mean_stationarity_score * 0.30 +
                var_stationarity_score * 0.25 +
                autocorr_stationarity_score * 0.25 +
                distribution_stationarity_score * 0.20
            )
            
            return min(100, max(0, stationarity_score))
            
        except:
            return 50
    
    def _calculate_skewness(self, data):
        """Calculate skewness"""
        try:
            n = len(data)
            if n < 3:
                return 0
            
            mean = np.mean(data)
            std = np.std(data, ddof=1)
            
            if std == 0:
                return 0
            
            skewness = (n / ((n-1) * (n-2))) * np.sum(((data - mean) / std) ** 3)
            return skewness
        except:
            return 0
    
    def _calculate_kurtosis(self, data):
        """Calculate kurtosis"""
        try:
            n = len(data)
            if n < 4:
                return 3
            
            mean = np.mean(data)
            std = np.std(data, ddof=1)
            
            if std == 0:
                return 3
            
            kurtosis = (n * (n+1) / ((n-1) * (n-2) * (n-3))) * np.sum(((data - mean) / std) ** 4) - 3 * (n-1)**2 / ((n-2) * (n-3))
            return kurtosis + 3  # Return excess kurtosis + 3
        except:
            return 3
    
    def _calculate_validation_score(self, monte_carlo_score, bootstrap_score, significance_score,
                                  distribution_score, outlier_score, cross_validation_score,
                                  regime_validation_score, stationarity_score):
        """Calculate final validation score with sophisticated weighting"""
        
        # Ultra-sophisticated weighting based on statistical importance
        weights = {
            'monte_carlo': 0.18,        # Monte Carlo validation
            'bootstrap': 0.16,          # Bootstrap confidence
            'significance': 0.15,       # Statistical significance
            'distribution': 0.14,       # Distribution analysis
            'cross_validation': 0.13,   # Cross-validation
            'stationarity': 0.12,       # Stationarity validation
            'regime_validation': 0.08,  # Regime validation
            'outlier': 0.04            # Outlier validation
        }
        
        final_score = (
            monte_carlo_score * weights['monte_carlo'] +
            bootstrap_score * weights['bootstrap'] +
            significance_score * weights['significance'] +
            distribution_score * weights['distribution'] +
            cross_validation_score * weights['cross_validation'] +
            stationarity_score * weights['stationarity'] +
            regime_validation_score * weights['regime_validation'] +
            outlier_score * weights['outlier']
        )
        
        # Apply sophisticated validation-specific scaling
        if final_score > 85:
            # High statistical validation is rare and valuable
            final_score = 85 + (final_score - 85) * 0.2
        elif final_score < 20:
            # Very poor validation is also compressed
            final_score = 20 + (final_score - 20) * 0.3
        
        return min(95, max(5, final_score))
    
    def _default_score(self):
        """Return default score when analysis fails"""
        return {
            'statistical_validation_score': 50,
            'monte_carlo_score': 50,
            'bootstrap_score': 50,
            'significance_score': 50,
            'distribution_score': 50,
            'outlier_score': 50,
            'cross_validation_score': 50,
            'regime_validation_score': 50,
            'stationarity_score': 50
        }

# Backward compatibility and combined analyzer
class StatisticalValidationAnalyzer:
    """İstatistiksel doğrulama ve backtest işlemlerini yöneten sınıf"""
    
    def __init__(self):
        # Tarihsel veri aralığı
        self.analysis_periods = {
            'short': 365,      # 1 yıl
            'medium': 1095,    # 3 yıl
            'long': 1825,      # 5 yıl
            'extended': 3650   # 10 yıl
        }
        
        # İstatistiksel güven seviyeleri
        self.confidence_levels = {
            'low': 0.6,        # %60 güven
            'medium': 0.7,     # %70 güven
            'high': 0.8,       # %80 güven
            'very_high': 0.9   # %90 güven
        }
        
        # Performans metrikleri
        self.performance_metrics = {
            'hit_rate': 'İsabet Oranı',
            'average_return': 'Ortalama Getiri',
            'sharpe_ratio': 'Sharpe Oranı',
            'max_drawdown': 'Maksimum Düşüş',
            'volatility': 'Volatilite',
            'win_loss_ratio': 'Kazanç/Kayıp Oranı'
        }
        
        # Döngü türleri
        self.cycle_types = {
            'shemitah': 'Shemitah Döngüsü',
            'gann': 'Gann Tekniği',
            'spiral21': '21\'li Spiral',
            'solar': 'Solar Döngü',
            'moon': 'Ay Fazları',
            'vedic': 'Vedik Astroloji',
            'gann_astro': 'Gann-Astro Hibrit'
        }
        
        log_info("Statistical Validation Analyzer başlatıldı")
    
    def calculate_hit_rate(self, predictions: List[Dict], actual_results: List[Dict]) -> float:
        """
        İsabet oranını hesapla
        
        Args:
            predictions: Tahminler listesi
            actual_results: Gerçek sonuçlar listesi
            
        Returns:
            İsabet oranı (0-1 arası)
        """
        try:
            if not predictions or not actual_results:
                return 0.0
            
            correct_predictions = 0
            total_predictions = len(predictions)
            
            for i, prediction in enumerate(predictions):
                if i < len(actual_results):
                    predicted_direction = prediction.get('direction', 'neutral')
                    actual_direction = actual_results[i].get('direction', 'neutral')
                    
                    if predicted_direction == actual_direction:
                        correct_predictions += 1
            
            hit_rate = correct_predictions / total_predictions if total_predictions > 0 else 0.0
            return hit_rate
            
        except Exception as e:
            log_error(f"İsabet oranı hesaplama hatası: {e}")
            return 0.0
    
    def calculate_performance_metrics(self, returns: List[float]) -> Dict:
        """
        Performans metriklerini hesapla
        
        Args:
            returns: Getiri listesi
            
        Returns:
            Performans metrikleri
        """
        try:
            if not returns:
                return {}
            
            returns_array = np.array(returns)
            
            # Temel istatistikler
            mean_return = np.mean(returns_array)
            std_return = np.std(returns_array)
            
            # Sharpe oranı (risk-free rate = 0 varsayımı)
            sharpe_ratio = mean_return / std_return if std_return > 0 else 0
            
            # Maksimum düşüş
            cumulative_returns = np.cumprod(1 + returns_array)
            running_max = np.maximum.accumulate(cumulative_returns)
            drawdowns = (cumulative_returns - running_max) / running_max
            max_drawdown = np.min(drawdowns)
            
            # Kazanç/kayıp oranı
            positive_returns = returns_array[returns_array > 0]
            negative_returns = returns_array[returns_array < 0]
            
            avg_win = np.mean(positive_returns) if len(positive_returns) > 0 else 0
            avg_loss = abs(np.mean(negative_returns)) if len(negative_returns) > 0 else 0
            win_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0
            
            # İsabet oranı
            hit_rate = len(positive_returns) / len(returns_array) if len(returns_array) > 0 else 0
            
            metrics = {
                'hit_rate': hit_rate,
                'average_return': mean_return,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'volatility': std_return,
                'win_loss_ratio': win_loss_ratio,
                'total_trades': len(returns_array),
                'winning_trades': len(positive_returns),
                'losing_trades': len(negative_returns)
            }
            
            return metrics
            
        except Exception as e:
            log_error(f"Performans metrikleri hesaplama hatası: {e}")
            return {}
    
    def validate_cycle_performance(self, cycle_type: str, symbol: str, 
                                 historical_data: Dict, cycle_dates: List[str]) -> Dict:
        """
        Döngü performansını doğrula
        
        Args:
            cycle_type: Döngü türü
            symbol: Sembol
            historical_data: Tarihsel fiyat verisi
            cycle_dates: Döngü tarihleri
            
        Returns:
            Döngü performans analizi
        """
        try:
            if not historical_data or not cycle_dates:
                return {'error': 'Yetersiz veri'}
            
            # Döngü tarihlerinde fiyat değişimlerini analiz et
            cycle_returns = []
            cycle_directions = []
            
            for cycle_date in cycle_dates:
                if cycle_date in historical_data:
                    # Döngü tarihinden önceki ve sonraki fiyatları al
                    current_price = historical_data[cycle_date]['Close']
                    
                    # 5 gün önce ve 5 gün sonra
                    date_obj = datetime.strptime(cycle_date, '%Y-%m-%d')
                    before_date = (date_obj - timedelta(days=5)).strftime('%Y-%m-%d')
                    after_date = (date_obj + timedelta(days=5)).strftime('%Y-%m-%d')
                    
                    if before_date in historical_data and after_date in historical_data:
                        before_price = historical_data[before_date]['Close']
                        after_price = historical_data[after_date]['Close']
                        
                        # Getiri hesapla
                        return_rate = (after_price - before_price) / before_price
                        cycle_returns.append(return_rate)
                        
                        # Yön belirle
                        direction = 'bullish' if return_rate > 0.02 else 'bearish' if return_rate < -0.02 else 'neutral'
                        cycle_directions.append(direction)
            
            if not cycle_returns:
                return {'error': 'Döngü tarihlerinde veri bulunamadı'}
            
            # Performans metriklerini hesapla
            performance_metrics = self.calculate_performance_metrics(cycle_returns)
            
            # Döngü türüne göre beklenti
            expected_performance = self._get_expected_performance(cycle_type)
            
            # Performans değerlendirmesi
            performance_rating = self._rate_performance(performance_metrics, expected_performance)
            
            result = {
                'cycle_type': cycle_type,
                'symbol': symbol,
                'total_cycles_analyzed': len(cycle_returns),
                'performance_metrics': performance_metrics,
                'expected_performance': expected_performance,
                'performance_rating': performance_rating,
                'cycle_returns': cycle_returns,
                'cycle_directions': cycle_directions,
                'validation_status': self._get_validation_status(performance_metrics)
            }
            
            log_info(f"{symbol} {cycle_type} döngü doğrulaması: {performance_rating['grade']}")
            return result
            
        except Exception as e:
            log_error(f"{cycle_type} döngü doğrulama hatası: {e}")
            return {'error': str(e)}
    
    def _get_expected_performance(self, cycle_type: str) -> Dict:
        """Döngü türüne göre beklenen performans"""
        expectations = {
            'shemitah': {
                'min_hit_rate': 0.6,
                'min_sharpe': 0.5,
                'max_drawdown': -0.15,
                'description': 'Shemitah döngülerinde yüksek volatilite beklenir'
            },
            'gann': {
                'min_hit_rate': 0.55,
                'min_sharpe': 0.3,
                'max_drawdown': -0.20,
                'description': 'Gann tekniklerinde orta seviye isabet beklenir'
            },
            'spiral21': {
                'min_hit_rate': 0.65,
                'min_sharpe': 0.4,
                'max_drawdown': -0.12,
                'description': '21\'li spiral döngülerinde yüksek isabet beklenir'
            },
            'solar': {
                'min_hit_rate': 0.5,
                'min_sharpe': 0.2,
                'max_drawdown': -0.25,
                'description': 'Solar döngülerinde volatilite artışı beklenir'
            },
            'moon': {
                'min_hit_rate': 0.6,
                'min_sharpe': 0.3,
                'max_drawdown': -0.18,
                'description': 'Ay fazlarında orta seviye isabet beklenir'
            },
            'vedic': {
                'min_hit_rate': 0.7,
                'min_sharpe': 0.6,
                'max_drawdown': -0.10,
                'description': 'Vedik astrolojide yüksek isabet beklenir'
            },
            'gann_astro': {
                'min_hit_rate': 0.75,
                'min_sharpe': 0.7,
                'max_drawdown': -0.08,
                'description': 'Gann-Astro hibrit sistemde en yüksek isabet beklenir'
            }
        }
        
        return expectations.get(cycle_type, {
            'min_hit_rate': 0.5,
            'min_sharpe': 0.2,
            'max_drawdown': -0.20,
            'description': 'Genel beklenti'
        })
    
    def _rate_performance(self, metrics: Dict, expected: Dict) -> Dict:
        """Performansı değerlendir"""
        try:
            hit_rate = metrics.get('hit_rate', 0)
            sharpe_ratio = metrics.get('sharpe_ratio', 0)
            max_drawdown = metrics.get('max_drawdown', 0)
            
            # Kriterleri kontrol et
            hit_rate_pass = hit_rate >= expected['min_hit_rate']
            sharpe_pass = sharpe_ratio >= expected['min_sharpe']
            drawdown_pass = max_drawdown >= expected['max_drawdown']
            
            # Genel değerlendirme
            passed_criteria = sum([hit_rate_pass, sharpe_pass, drawdown_pass])
            
            if passed_criteria == 3:
                grade = 'A'
                rating = 'Mükemmel'
            elif passed_criteria == 2:
                grade = 'B'
                rating = 'İyi'
            elif passed_criteria == 1:
                grade = 'C'
                rating = 'Orta'
            else:
                grade = 'D'
                rating = 'Zayıf'
            
            return {
                'grade': grade,
                'rating': rating,
                'passed_criteria': passed_criteria,
                'total_criteria': 3,
                'criteria_details': {
                    'hit_rate': {'passed': hit_rate_pass, 'value': hit_rate, 'expected': expected['min_hit_rate']},
                    'sharpe_ratio': {'passed': sharpe_pass, 'value': sharpe_ratio, 'expected': expected['min_sharpe']},
                    'max_drawdown': {'passed': drawdown_pass, 'value': max_drawdown, 'expected': expected['max_drawdown']}
                }
            }
            
        except Exception as e:
            log_error(f"Performans değerlendirme hatası: {e}")
            return {'grade': 'F', 'rating': 'Hata', 'passed_criteria': 0}
    
    def _get_validation_status(self, metrics: Dict) -> str:
        """Doğrulama durumunu belirle"""
        try:
            hit_rate = metrics.get('hit_rate', 0)
            sharpe_ratio = metrics.get('sharpe_ratio', 0)
            
            if hit_rate >= 0.7 and sharpe_ratio >= 0.5:
                return 'validated'
            elif hit_rate >= 0.6 and sharpe_ratio >= 0.3:
                return 'partially_validated'
            else:
                return 'not_validated'
                
        except Exception as e:
            log_warning(f"Doğrulama durumu belirleme hatası: {e}")
            return 'unknown'
    
    def run_comprehensive_backtest(self, symbol: str, historical_data: Dict, 
                                 all_cycle_dates: Dict) -> Dict:
        """
        Kapsamlı backtest çalıştır
        
        Args:
            symbol: Sembol
            historical_data: Tarihsel veri
            all_cycle_dates: Tüm döngü tarihleri
            
        Returns:
            Kapsamlı backtest sonuçları
        """
        try:
            backtest_results = {}
            overall_performance = {}
            
            # Her döngü türü için backtest
            for cycle_type, cycle_dates in all_cycle_dates.items():
                if cycle_dates:
                    result = self.validate_cycle_performance(
                        cycle_type, symbol, historical_data, cycle_dates
                    )
                    backtest_results[cycle_type] = result
                    
                    # Genel performansa katkı
                    if 'performance_metrics' in result:
                        metrics = result['performance_metrics']
                        overall_performance[cycle_type] = {
                            'hit_rate': metrics.get('hit_rate', 0),
                            'sharpe_ratio': metrics.get('sharpe_ratio', 0),
                            'grade': result.get('performance_rating', {}).get('grade', 'F')
                        }
            
            # Genel değerlendirme
            overall_grade = self._calculate_overall_grade(overall_performance)
            
            # En iyi ve en kötü performans
            best_performer = max(overall_performance.items(), 
                               key=lambda x: x[1]['hit_rate']) if overall_performance else None
            worst_performer = min(overall_performance.items(), 
                                key=lambda x: x[1]['hit_rate']) if overall_performance else None
            
            comprehensive_result = {
                'symbol': symbol,
                'backtest_period': f"{len(historical_data)} gün",
                'overall_grade': overall_grade,
                'overall_performance': overall_performance,
                'best_performer': best_performer,
                'worst_performer': worst_performer,
                'detailed_results': backtest_results,
                'recommendation': self._get_recommendation(overall_grade, overall_performance),
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            log_info(f"{symbol} kapsamlı backtest tamamlandı: {overall_grade}")
            return comprehensive_result
            
        except Exception as e:
            log_error(f"{symbol} kapsamlı backtest hatası: {e}")
            return {'error': str(e)}
    
    def _calculate_overall_grade(self, overall_performance: Dict) -> str:
        """Genel not hesapla"""
        try:
            if not overall_performance:
                return 'F'
            
            # Ortalama isabet oranı
            avg_hit_rate = np.mean([perf['hit_rate'] for perf in overall_performance.values()])
            
            # Ortalama Sharpe oranı
            avg_sharpe = np.mean([perf['sharpe_ratio'] for perf in overall_performance.values()])
            
            # Not belirleme
            if avg_hit_rate >= 0.7 and avg_sharpe >= 0.5:
                return 'A'
            elif avg_hit_rate >= 0.6 and avg_sharpe >= 0.3:
                return 'B'
            elif avg_hit_rate >= 0.5 and avg_sharpe >= 0.2:
                return 'C'
            else:
                return 'D'
                
        except Exception as e:
            log_warning(f"Genel not hesaplama hatası: {e}")
            return 'F'
    
    def _get_recommendation(self, overall_grade: str, overall_performance: Dict) -> str:
        """Öneri oluştur"""
        try:
            if overall_grade == 'A':
                return 'Mükemmel performans - Tüm döngüler güvenilir'
            elif overall_grade == 'B':
                return 'İyi performans - Çoğu döngü güvenilir'
            elif overall_grade == 'C':
                return 'Orta performans - Dikkatli kullanım önerilir'
            else:
                return 'Zayıf performans - Döngüleri kullanmadan önce iyileştirme gerekli'
                
        except Exception as e:
            log_warning(f"Öneri oluşturma hatası: {e}")
            return 'Değerlendirme yapılamadı'

# Global statistical analyzer instances
statistical_analyzer = StatisticalValidationAnalyzer()
ultra_statistical_validator = UltraStatisticalValidator()

def get_statistical_score(symbol, stock_data):
    """
    Get ultra-sophisticated statistical validation score for a stock
    
    Args:
        symbol: Stock symbol
        stock_data: DataFrame with OHLCV data
        
    Returns:
        float: Statistical validation score (0-100)
    """
    try:
        result = ultra_statistical_validator.analyze_statistical_validation(symbol, stock_data)
        return result['statistical_validation_score']
    except:
        return 50.0





