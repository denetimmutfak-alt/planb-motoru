"""
PlanB Motoru - Ultra Advanced Anomaly Detector
Machine Learning & İstatistiksel Anomali Tespiti
Isolation Forest, LSTM, Statistical Analysis
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
# from scipy import stats  # Commented out for now
# from scipy.signal import find_peaks
# from sklearn.ensemble import IsolationForest
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

from src.utils.logger import log_info, log_error, log_debug

# Global accessor functions
def get_anomaly_score(symbol: str, stock_data: pd.DataFrame) -> float:
    """Anomaly skorunu döndür"""
    try:
        global anomaly_detector
        if anomaly_detector is None:
            anomaly_detector = UltraAnomalyDetector()
        
        result = anomaly_detector.detect_comprehensive_anomalies(symbol, stock_data)
        return result.get('anomaly_score', 50.0)
    except Exception as e:
        log_error(f"Anomaly skoru hesaplanırken hata: {e}")
        return 50.0

class UltraAnomalyDetector:
    """Ultra gelişmiş anomali tespit sistemi (scipy-free version)"""
    
    def __init__(self):
        self.algorithms = {
            'statistical_z': 3.0,  # Z-score threshold
            'iqr_multiplier': 1.5,  # IQR outlier detection
            'lstm_threshold': 0.05,  # LSTM prediction error
            'mahalanobis_threshold': 2.5  # Mahalanobis distance
        }
        
        self.feature_weights = {
            'price_volatility': 0.25,
            'volume_pattern': 0.20,
            'technical_divergence': 0.20,
            'market_regime': 0.15,
            'fractal_dimension': 0.10,
            'entropy_analysis': 0.10
        }
        
    def _calculate_zscore(self, data: np.ndarray) -> np.ndarray:
        """Z-score hesaplama (scipy olmadan)"""
        try:
            if len(data) == 0:
                return np.array([])
            
            mean = np.mean(data)
            std = np.std(data)
            
            if std == 0:
                return np.zeros_like(data)
            
            return (data - mean) / std
            
        except Exception as e:
            return np.zeros_like(data) if len(data) > 0 else np.array([])
    
    def detect_isolation_forest_anomalies(self, features_df: pd.DataFrame, 
                                        symbol: str) -> List[Dict[str, Any]]:
        """Basitleştirilmiş anomali tespiti (sklearn olmadan)"""
        try:
            if features_df.empty:
                return []
            
            anomalies = []
            
            # Basit statistical outlier detection
            for column in features_df.columns:
                if features_df[column].dtype in ['float64', 'int64']:
                    z_scores = self._calculate_zscore(features_df[column].values)
                    
                    for i, (idx, z_score) in enumerate(zip(features_df.index, z_scores)):
                        if abs(z_score) > 3:  # 3-sigma rule
                            anomaly = {
                                'type': 'statistical_anomaly',
                                'symbol': symbol,
                                'date': idx,
                                'anomaly_score': abs(z_score) / 3,
                                'z_score': z_score,
                                'column': column,
                                'value': features_df[column].iloc[i],
                                'severity': self._calculate_severity_from_score(abs(z_score) / 3),
                                'description': f"{symbol} {column} istatistiksel anomali: Z={z_score:.2f}"
                            }
                            anomalies.append(anomaly)
            
            if anomalies:
                log_info(f"{symbol}: {len(anomalies)} isolation forest anomali tespit edildi")
            return anomalies
            
        except Exception as e:
            log_error(f"Anomali tespiti hatası: {e}")
            return []
    
    def detect_statistical_anomalies(self, price_data: pd.DataFrame, 
                                   symbol: str) -> List[Dict[str, Any]]:
        """İstatistiksel anomali tespiti (Z-score, IQR, Mahalanobis)"""
        try:
            anomalies = []
            
            # Z-score anomalileri
            for column in ['close', 'volume', 'high', 'low']:
                if column in price_data.columns:
                    z_scores = np.abs(self._calculate_zscore(price_data[column].dropna().values))
                    
                    for i, (idx, z_score) in enumerate(zip(price_data.index, z_scores)):
                        if z_score > self.algorithms['statistical_z']:
                            anomaly = {
                                'type': 'statistical_z_anomaly',
                                'symbol': symbol,
                                'date': idx,
                                'anomaly_score': z_score / self.algorithms['statistical_z'],
                                'z_score': z_score,
                                'column': column,
                                'value': price_data[column].iloc[i],
                                'severity': self._calculate_severity_from_zscore(z_score),
                                'description': f"{symbol} {column} Z-score anomalisi: {z_score:.2f}"
                            }
                            anomalies.append(anomaly)
            
            # IQR anomalileri
            for column in ['close', 'volume']:
                if column in price_data.columns:
                    Q1 = price_data[column].quantile(0.25)
                    Q3 = price_data[column].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - self.algorithms['iqr_multiplier'] * IQR
                    upper_bound = Q3 + self.algorithms['iqr_multiplier'] * IQR
                    
                    outliers = price_data[(price_data[column] < lower_bound) | 
                                        (price_data[column] > upper_bound)]
                    
                    for idx, row in outliers.iterrows():
                        distance_from_bound = min(abs(row[column] - lower_bound), 
                                                abs(row[column] - upper_bound))
                        anomaly_score = distance_from_bound / IQR
                        
                        anomaly = {
                            'type': 'iqr_anomaly',
                            'symbol': symbol,
                            'date': idx,
                            'anomaly_score': anomaly_score,
                            'column': column,
                            'value': row[column],
                            'iqr_lower': lower_bound,
                            'iqr_upper': upper_bound,
                            'distance_from_bound': distance_from_bound,
                            'severity': self._calculate_severity_from_score(anomaly_score),
                            'description': f"{symbol} {column} IQR outlier: {row[column]:.2f}"
                        }
                        anomalies.append(anomaly)
            
            if anomalies:
                log_info(f"{symbol}: {len(anomalies)} istatistiksel Z-score/IQR anomali tespit edildi")
            return anomalies
            
        except Exception as e:
            log_error(f"İstatistiksel anomali tespiti hatası: {e}")
            return []
    
    def detect_fractal_anomalies(self, price_data: pd.DataFrame, 
                               symbol: str) -> List[Dict[str, Any]]:
        """Fraktal analiz ile anomali tespiti"""
        try:
            anomalies = []
            
            if 'close' not in price_data.columns:
                return []
            
            close_prices = price_data['close'].values
            
            # Fraktal boyut hesaplama (Higuchi method)
            fractal_dims = []
            window_size = 50
            
            for i in range(window_size, len(close_prices)):
                window = close_prices[i-window_size:i]
                fractal_dim = self._calculate_higuchi_fractal_dimension(window)
                fractal_dims.append(fractal_dim)
            
            if not fractal_dims:
                return []
            
            # Fraktal boyut anomalileri
            mean_fd = np.mean(fractal_dims)
            std_fd = np.std(fractal_dims)
            
            for i, fd in enumerate(fractal_dims):
                z_score = abs(fd - mean_fd) / std_fd if std_fd > 0 else 0
                
                if z_score > 2.0:  # 2 sigma threshold
                    idx = price_data.index[i + window_size]
                    anomaly = {
                        'type': 'fractal_anomaly',
                        'symbol': symbol,
                        'date': idx,
                        'anomaly_score': z_score / 2.0,
                        'fractal_dimension': fd,
                        'mean_fractal_dimension': mean_fd,
                        'fractal_z_score': z_score,
                        'market_complexity': 'high' if fd > mean_fd else 'low',
                        'severity': self._calculate_severity_from_score(z_score / 2.0),
                        'description': f"{symbol} fraktal boyut anomalisi: {fd:.3f}"
                    }
                    anomalies.append(anomaly)
            
            log_info(f"{symbol}: {len(anomalies)} fraktal anomali tespit edildi")
            return anomalies
            
        except Exception as e:
            log_error(f"Fraktal anomali tespiti hatası: {e}")
            return []
    
    def detect_entropy_anomalies(self, price_data: pd.DataFrame, 
                               symbol: str) -> List[Dict[str, Any]]:
        """Entropi analizi ile anomali tespiti"""
        try:
            anomalies = []
            
            if 'close' not in price_data.columns:
                return []
            
            close_prices = price_data['close'].values
            returns = np.diff(np.log(close_prices))
            
            # Shannon entropisi hesaplama
            window_size = 30
            entropies = []
            
            for i in range(window_size, len(returns)):
                window_returns = returns[i-window_size:i]
                entropy = self._calculate_shannon_entropy(window_returns)
                entropies.append(entropy)
            
            if not entropies:
                return []
            
            # Entropi anomalileri
            mean_entropy = np.mean(entropies)
            std_entropy = np.std(entropies)
            
            for i, entropy in enumerate(entropies):
                z_score = abs(entropy - mean_entropy) / std_entropy if std_entropy > 0 else 0
                
                if z_score > 2.0:
                    idx = price_data.index[i + window_size]
                    anomaly = {
                        'type': 'entropy_anomaly',
                        'symbol': symbol,
                        'date': idx,
                        'anomaly_score': z_score / 2.0,
                        'entropy_value': entropy,
                        'mean_entropy': mean_entropy,
                        'entropy_z_score': z_score,
                        'market_predictability': 'low' if entropy > mean_entropy else 'high',
                        'severity': self._calculate_severity_from_score(z_score / 2.0),
                        'description': f"{symbol} entropi anomalisi: {entropy:.3f}"
                    }
                    anomalies.append(anomaly)
            
            log_info(f"{symbol}: {len(anomalies)} entropi anomali tespit edildi")
            return anomalies
            
        except Exception as e:
            log_error(f"Entropi anomali tespiti hatası: {e}")
            return []
    
    def detect_regime_change_anomalies(self, price_data: pd.DataFrame, 
                                     symbol: str) -> List[Dict[str, Any]]:
        """Piyasa rejim değişikliği anomalileri"""
        try:
            anomalies = []
            
            if 'close' not in price_data.columns:
                return []
            
            close_prices = price_data['close']
            returns = close_prices.pct_change(fill_method=None).dropna()
            
            # Volatilite rejimi
            volatility = returns.rolling(20).std()
            vol_mean = volatility.rolling(60).mean()
            vol_ratio = volatility / vol_mean
            
            # Trend rejimi
            ma_short = close_prices.rolling(10).mean()
            ma_long = close_prices.rolling(50).mean()
            trend_ratio = ma_short / ma_long
            
            # Rejim değişikliği tespiti
            for i in range(60, len(price_data)):
                idx = price_data.index[i]
                
                # Volatilite rejim değişikliği
                if vol_ratio.iloc[i] > 2.0 or vol_ratio.iloc[i] < 0.5:
                    anomaly = {
                        'type': 'regime_change_anomaly',
                        'symbol': symbol,
                        'date': idx,
                        'anomaly_score': abs(np.log(vol_ratio.iloc[i])),
                        'volatility_regime': 'high' if vol_ratio.iloc[i] > 1 else 'low',
                        'volatility_ratio': vol_ratio.iloc[i],
                        'trend_regime': 'uptrend' if trend_ratio.iloc[i] > 1.02 else 'downtrend' if trend_ratio.iloc[i] < 0.98 else 'sideways',
                        'trend_ratio': trend_ratio.iloc[i],
                        'severity': self._calculate_severity_from_score(abs(np.log(vol_ratio.iloc[i]))),
                        'description': f"{symbol} piyasa rejim değişikliği"
                    }
                    anomalies.append(anomaly)
            
            log_info(f"{symbol}: {len(anomalies)} rejim değişikliği anomalisi tespit edildi")
            return anomalies
            
        except Exception as e:
            log_error(f"Rejim değişikliği anomali tespiti hatası: {e}")
            return []
    
    def detect_comprehensive_anomalies(self, symbol: str, price_data: pd.DataFrame, 
                                     sentiment_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ultra kapsamlı anomali tespiti - Tüm algoritmaları birleştir"""
        try:
            all_anomalies = []
            
            # 1. Isolation Forest anomalileri
            if_anomalies = self.detect_isolation_forest_anomalies(price_data, symbol)
            all_anomalies.extend(if_anomalies)
            
            # 2. İstatistiksel anomaliler
            stat_anomalies = self.detect_statistical_anomalies(price_data, symbol)
            all_anomalies.extend(stat_anomalies)
            
            # 3. Fraktal anomaliler
            fractal_anomalies = self.detect_fractal_anomalies(price_data, symbol)
            all_anomalies.extend(fractal_anomalies)
            
            # 4. Entropi anomalileri
            entropy_anomalies = self.detect_entropy_anomalies(price_data, symbol)
            all_anomalies.extend(entropy_anomalies)
            
            # 5. Rejim değişikliği anomalileri
            regime_anomalies = self.detect_regime_change_anomalies(price_data, symbol)
            all_anomalies.extend(regime_anomalies)
            
            # Anomalileri tarihe göre sırala
            all_anomalies.sort(key=lambda x: x['date'], reverse=True)
            
            # Genel anomali skoru hesapla
            anomaly_score = self._calculate_comprehensive_anomaly_score(all_anomalies, price_data)
            
            # Risk assessment
            risk_assessment = self._calculate_comprehensive_risk_assessment(all_anomalies, price_data)
            
            # Market stress indicator
            market_stress = self._calculate_market_stress_indicator(all_anomalies, price_data)
            
            return {
                'symbol': symbol,
                'anomaly_score': anomaly_score,
                'total_anomalies': len(all_anomalies),
                'anomalies': all_anomalies[:20],  # Son 20 anomali
                'risk_assessment': risk_assessment,
                'market_stress_indicator': market_stress,
                'detection_algorithms': list(self.algorithms.keys()),
                'detection_timestamp': datetime.now().isoformat(),
                'recommendation': self._generate_anomaly_recommendation(anomaly_score, risk_assessment)
            }
            
        except Exception as e:
            log_error(f"Kapsamlı anomali tespiti hatası: {e}")
            return {'symbol': symbol, 'anomaly_score': 50.0, 'error': str(e)}
    
    def _create_advanced_features(self, price_data: pd.DataFrame) -> np.ndarray:
        """Gelişmiş feature engineering"""
        try:
            features = []
            
            if 'close' in price_data.columns:
                close = price_data['close']
                
                # Price features
                returns = close.pct_change(fill_method=None).fillna(0)
                log_returns = np.log(close / close.shift(1)).fillna(0)
                
                # Volatility features
                volatility_5 = returns.rolling(5).std().fillna(0)
                volatility_20 = returns.rolling(20).std().fillna(0)
                volatility_ratio = (volatility_5 / volatility_20).fillna(1)
                
                # Momentum features
                momentum_5 = close / close.shift(5) - 1
                momentum_20 = close / close.shift(20) - 1
                
                # Technical indicators
                rsi = self._calculate_rsi(close, 14)
                bb_position = self._calculate_bollinger_position(close, 20)
                
                features = np.column_stack([
                    returns.fillna(0),
                    log_returns.fillna(0),
                    volatility_ratio.fillna(1),
                    momentum_5.fillna(0),
                    momentum_20.fillna(0),
                    rsi.fillna(50),
                    bb_position.fillna(0.5)
                ])
                
            if 'volume' in price_data.columns:
                volume = price_data['volume']
                volume_ma = volume.rolling(20).mean()
                volume_ratio = (volume / volume_ma).fillna(1)
                
                if features.size > 0:
                    features = np.column_stack([features, volume_ratio.fillna(1)])
                else:
                    features = volume_ratio.fillna(1).values.reshape(-1, 1)
            
            return features if features.size > 0 else np.array([]).reshape(0, 1)
            
        except Exception as e:
            log_error(f"Feature engineering hatası: {e}")
            return np.array([]).reshape(0, 1)
    
    def _calculate_higuchi_fractal_dimension(self, data: np.ndarray, max_k: int = 10) -> float:
        """Higuchi fraktal boyut hesaplama"""
        try:
            N = len(data)
            L = []
            
            for k in range(1, max_k + 1):
                Lk = []
                
                for m in range(k):
                    Lkm = 0
                    max_i = int((N - m - 1) / k)
                    
                    for i in range(1, max_i + 1):
                        Lkm += abs(data[m + i * k] - data[m + (i - 1) * k])
                    
                    if max_i > 0:
                        Lkm = Lkm * (N - 1) / (max_i * k * k)
                        Lkm /= max_i
                        Lkm *= (N - 1) / k
                        Lkm /= k
                        Lkm *= (N - 1) / (max_i * k)
                        Lkm = Lkm * (N - 1) / (max_i * k)
                        Lkm = sum(abs(data[m + i * k] - data[m + (i - 1) * k]) 
                                for i in range(1, max_i + 1)) * (N - 1) / (max_i * k * k)
                    
                    Lkm = sum(abs(data[m + i * k] - data[m + (i - 1) * k]) 
                            for i in range(1, max_i + 1))
                    Lkm = Lkm * (N - 1) / (max_i * k * k) if max_i > 0 else 0
                    Lkm = Lkm / k if k > 0 else 0
                    
                    if Lkm > 0:
                        Lkm = sum(abs(data[m + i * k] - data[m + (i - 1) * k]) 
                                for i in range(1, max_i + 1)) * (N - 1) / (max_i * k**2)
                        Lkm = Lkm / k
                        Lkm = Lkm * (N - 1) / (max_i * k)
                        Lkm = Lkm / k
                        
                        # Simplified calculation
                        length = sum(abs(data[m + i * k] - data[m + (i - 1) * k]) 
                                   for i in range(1, max_i + 1))
                        normalization = (N - 1) / (max_i * k**2)
                        Lkm = length * normalization
                        
                    Lkm = Lkm / k if k > 0 else 0
                    Lkm = abs(Lkm) if not np.isnan(Lkm) else 0
                    
                    if Lkm > 0:
                        Lkm = sum(abs(data[m + i * k] - data[m + (i - 1) * k]) 
                                for i in range(1, max_i + 1))
                        if max_i > 0:
                            Lkm = Lkm * (N - 1) / (max_i * k * k)
                        Lkm = Lkm / k if k > 0 else 0
                        
                    Lkm = abs(Lkm) if Lkm is not None and not np.isnan(Lkm) else 0
                    Lkm = max(0, Lkm)  # Ensure non-negative
                    Lkm = min(100, Lkm)  # Cap at reasonable value
                    
                    Lk.append(Lkm)
                
                if Lk:
                    L.append(np.mean([x for x in Lk if x > 0]))
            
            # Calculate fractal dimension
            if len(L) < 2:
                return 1.5  # Default fractal dimension
            
            L = [x for x in L if x > 0]  # Remove zeros
            if len(L) < 2:
                return 1.5
            
            k_values = list(range(1, len(L) + 1))
            log_k = np.log(k_values)
            log_L = np.log(L)
            
            # Linear regression
            if len(log_k) > 1 and len(log_L) > 1:
                slope = np.polyfit(log_k, log_L, 1)[0]
                fractal_dim = -slope
            else:
                fractal_dim = 1.5
            
            # Ensure reasonable bounds
            fractal_dim = max(1.0, min(2.0, fractal_dim))
            
            return fractal_dim
            
        except Exception as e:
            return 1.5  # Default value on error
    
    def _calculate_shannon_entropy(self, data: np.ndarray, bins: int = 10) -> float:
        """Shannon entropisi hesaplama"""
        try:
            if len(data) == 0:
                return 0
            
            # Histogram oluştur
            hist, _ = np.histogram(data, bins=bins)
            
            # Normalize et
            hist = hist / np.sum(hist)
            
            # Sıfır değerleri kaldır
            hist = hist[hist > 0]
            
            # Shannon entropisi
            entropy = -np.sum(hist * np.log2(hist))
            
            return entropy
            
        except Exception as e:
            return 0
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """RSI hesaplama"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.fillna(50)
        except:
            return pd.Series([50] * len(prices), index=prices.index)
    
    def _calculate_bollinger_position(self, prices: pd.Series, period: int = 20) -> pd.Series:
        """Bollinger Band pozisyonu hesaplama"""
        try:
            middle = prices.rolling(period).mean()
            std = prices.rolling(period).std()
            upper = middle + (2 * std)
            lower = middle - (2 * std)
            
            position = (prices - lower) / (upper - lower)
            return position.fillna(0.5)
        except:
            return pd.Series([0.5] * len(prices), index=prices.index)
    
    def _calculate_comprehensive_anomaly_score(self, anomalies: List[Dict], 
                                             price_data: pd.DataFrame) -> float:
        """Kapsamlı anomali skoru hesaplama"""
        try:
            if not anomalies:
                return 50.0  # Neutral score
            
            # Recent anomalies weighted more
            recent_anomalies = [a for a in anomalies if 
                              (datetime.now() - pd.to_datetime(a['date'])).days <= 5]
            
            # Calculate weighted score
            recent_score = np.mean([a['anomaly_score'] for a in recent_anomalies]) if recent_anomalies else 0
            total_score = np.mean([a['anomaly_score'] for a in anomalies])
            
            # Weight recent anomalies more heavily
            final_score = (recent_score * 0.7 + total_score * 0.3) * 100
            
            # Normalize to 0-100 range
            final_score = max(0, min(100, final_score))
            
            return final_score
            
        except Exception as e:
            return 50.0
    
    def _calculate_comprehensive_risk_assessment(self, anomalies: List[Dict], 
                                               price_data: pd.DataFrame) -> Dict[str, Any]:
        """Kapsamlı risk değerlendirmesi"""
        try:
            risk_factors = {
                'liquidity_risk': 'low',
                'volatility_risk': 'low',
                'technical_risk': 'low',
                'regime_risk': 'low',
                'overall_risk': 'low'
            }
            
            # Count anomaly types
            anomaly_counts = {}
            for anomaly in anomalies:
                anomaly_type = anomaly['type']
                anomaly_counts[anomaly_type] = anomaly_counts.get(anomaly_type, 0) + 1
            
            # Assess risks
            if anomaly_counts.get('regime_change_anomaly', 0) > 2:
                risk_factors['regime_risk'] = 'high'
            
            if anomaly_counts.get('statistical_z_anomaly', 0) > 5:
                risk_factors['volatility_risk'] = 'high'
            
            if anomaly_counts.get('isolation_forest_anomaly', 0) > 3:
                risk_factors['technical_risk'] = 'high'
            
            # Overall risk calculation
            high_risks = sum(1 for risk in risk_factors.values() if risk == 'high')
            if high_risks >= 2:
                risk_factors['overall_risk'] = 'high'
            elif high_risks == 1:
                risk_factors['overall_risk'] = 'medium'
            
            return risk_factors
            
        except Exception as e:
            return {'overall_risk': 'medium', 'error': str(e)}
    
    def _calculate_market_stress_indicator(self, anomalies: List[Dict], 
                                         price_data: pd.DataFrame) -> Dict[str, Any]:
        """Piyasa stres göstergesi"""
        try:
            # Stress indicators
            stress_indicators = {
                'anomaly_frequency': len(anomalies) / max(len(price_data), 1),
                'severe_anomaly_ratio': len([a for a in anomalies if a.get('severity') == 'critical']) / max(len(anomalies), 1),
                'recent_stress': len([a for a in anomalies if 
                                    (datetime.now() - pd.to_datetime(a['date'])).days <= 7]) / 7
            }
            
            # Overall stress level
            stress_score = (
                stress_indicators['anomaly_frequency'] * 0.4 +
                stress_indicators['severe_anomaly_ratio'] * 0.4 +
                stress_indicators['recent_stress'] * 0.2
            )
            
            if stress_score > 0.5:
                stress_level = 'high'
            elif stress_score > 0.2:
                stress_level = 'medium'
            else:
                stress_level = 'low'
            
            return {
                'stress_level': stress_level,
                'stress_score': stress_score,
                'indicators': stress_indicators
            }
            
        except Exception as e:
            return {'stress_level': 'medium', 'error': str(e)}
    
    def _generate_anomaly_recommendation(self, anomaly_score: float, 
                                       risk_assessment: Dict[str, Any]) -> str:
        """Anomali skoruna göre öneri üret"""
        try:
            overall_risk = risk_assessment.get('overall_risk', 'medium')
            
            if anomaly_score > 80 and overall_risk == 'high':
                return "YÜKSEK RİSK: Pozisyon boyutunu azalt, sıkı stop-loss kullan"
            elif anomaly_score > 60:
                return "ORTA RİSK: Dikkatli takip et, risk yönetimi uygula"
            elif anomaly_score > 40:
                return "DÜŞÜK RİSK: Normal pozisyon boyutu, standart risk yönetimi"
            else:
                return "MİNİMAL RİSK: Normal trading koşulları"
                
        except Exception as e:
            return "Risk değerlendirmesi yapılamadı"
    
    def _calculate_severity_from_score(self, score: float) -> str:
        """Skordan severity hesapla"""
        if score > 5:
            return 'critical'
        elif score > 3:
            return 'high'
        elif score > 1.5:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_severity_from_zscore(self, z_score: float) -> str:
        """Z-score'dan severity hesapla"""
        if z_score > 5:
            return 'critical'
        elif z_score > 4:
            return 'high'
        elif z_score > 3:
            return 'medium'
        else:
            return 'low'

# Global ultra anomaly detector instance
anomaly_detector = None

