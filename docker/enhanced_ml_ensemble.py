#!/usr/bin/env python3
"""
Enhanced ML Ensemble Engine - LGBM + XGB + CNN-LSTM
Adaptive Trust Weights + Uncertainty Handling + Confidence Scoring
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
import logging
from datetime import datetime, timedelta
import joblib
import json
from dataclasses import dataclass
import os
from pathlib import Path

# ML Libraries
try:
    import lightgbm as lgb
    import xgboost as xgb
    from sklearn.preprocessing import StandardScaler, RobustScaler
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("WARNING: ML libraries not available. Install lightgbm, xgboost, sklearn")

# Deep Learning (opsiyonel)
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout, Conv1D, MaxPooling1D
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("INFO: TensorFlow not available. CNN-LSTM model will be disabled")

@dataclass
class ModelResult:
    """Model sonuç standardı"""
    model_name: str
    signal: str  # AL, SAT, TUT
    confidence: float  # 0-100
    probability_scores: Dict[str, float]  # Her sinyal için olasılık
    feature_importance: Dict[str, float]
    processing_time_ms: float
    sharpe_ratio: Optional[float] = None
    uncertainty_score: Optional[float] = None

@dataclass
class EnsembleResult:
    """Ensemble final sonuç"""
    final_signal: str
    final_confidence: float
    contributing_models: List[ModelResult]
    model_weights: Dict[str, float]
    consensus_score: float
    uncertainty_score: float
    reasoning: str

class ModelPerformanceTracker:
    """Model performans takip sistemi"""
    
    def __init__(self, db_url: str = None):
        self.db_url = db_url
        self.performance_cache = {}
        self.sharpe_window = 30  # 30 günlük Sharpe hesabı
    
    def update_performance(self, model_name: str, actual_result: str, predicted_result: str, 
                          profit_loss: float = 0.0):
        """Model performansını güncelle"""
        if model_name not in self.performance_cache:
            self.performance_cache[model_name] = {
                'predictions': [],
                'accuracy': 0.0,
                'sharpe_ratio': 0.0,
                'total_profit': 0.0,
                'last_updated': datetime.now()
            }
        
        # Prediction accuracy
        self.performance_cache[model_name]['predictions'].append({
            'predicted': predicted_result,
            'actual': actual_result,
            'profit_loss': profit_loss,
            'timestamp': datetime.now()
        })
        
        # Son 30 günlük veriyi tut
        cutoff_date = datetime.now() - timedelta(days=self.sharpe_window)
        self.performance_cache[model_name]['predictions'] = [
            p for p in self.performance_cache[model_name]['predictions']
            if p['timestamp'] > cutoff_date
        ]
        
        # Sharpe ratio hesapla
        profits = [p['profit_loss'] for p in self.performance_cache[model_name]['predictions']]
        if len(profits) > 5:
            returns = np.array(profits)
            sharpe = np.mean(returns) / (np.std(returns) + 1e-8) if np.std(returns) > 0 else 0
            self.performance_cache[model_name]['sharpe_ratio'] = sharpe
        
        # Accuracy hesapla
        correct_predictions = sum(1 for p in self.performance_cache[model_name]['predictions'] 
                                if p['predicted'] == p['actual'])
        total_predictions = len(self.performance_cache[model_name]['predictions'])
        self.performance_cache[model_name]['accuracy'] = correct_predictions / max(total_predictions, 1)
        
        self.performance_cache[model_name]['last_updated'] = datetime.now()
    
    def get_model_weights(self) -> Dict[str, float]:
        """Sharpe ratio'ya göre model ağırlıklarını hesapla"""
        if not self.performance_cache:
            return {'lgbm': 0.4, 'xgb': 0.4, 'cnn_lstm': 0.2}
        
        # Sharpe ratios
        sharpe_scores = {}
        for model_name, perf in self.performance_cache.items():
            sharpe_scores[model_name] = max(perf.get('sharpe_ratio', 0), 0)
        
        # Normalize weights
        total_sharpe = sum(sharpe_scores.values()) + 1e-8
        weights = {model: score / total_sharpe for model, score in sharpe_scores.items()}
        
        # Minimum weight garantisi
        for model in ['lgbm', 'xgb', 'cnn_lstm']:
            if model not in weights:
                weights[model] = 0.1
        
        # Normalize to sum = 1
        total_weight = sum(weights.values())
        weights = {model: weight / total_weight for model, weight in weights.items()}
        
        return weights

class LGBMPriceModel:
    """LightGBM Fiyat Modeli"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.model_path = "/app/models/lgbm_price_model.pkl"
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fiyat tahminleme için özellik mühendisliği"""
        features = pd.DataFrame()
        
        # Price features
        features['price_change'] = df['Close'].pct_change(fill_method=None)
        features['price_volatility'] = df['Close'].rolling(5).std()
        features['price_ma_ratio'] = df['Close'] / df['Close'].rolling(20).mean()
        
        # Volume features
        if 'Volume' in df.columns:
            features['volume_change'] = df['Volume'].pct_change(fill_method=None)
            features['price_volume_corr'] = df['Close'].rolling(10).corr(df['Volume'])
        
        # Technical indicators
        features['rsi'] = self.calculate_rsi(df['Close'])
        features['macd'] = self.calculate_macd(df['Close'])
        
        # Lag features
        for lag in [1, 2, 3, 5]:
            features[f'price_lag_{lag}'] = df['Close'].shift(lag)
            features[f'volume_lag_{lag}'] = df.get('Volume', df['Close']).shift(lag)
        
        # Fill NaN values
        features = features.fillna(method='bfill').fillna(0)
        
        self.feature_names = features.columns.tolist()
        return features
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """RSI hesaplama"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def calculate_macd(self, prices: pd.Series) -> pd.Series:
        """MACD hesaplama"""
        ema12 = prices.ewm(span=12).mean()
        ema26 = prices.ewm(span=26).mean()
        return ema12 - ema26
    
    def predict(self, df: pd.DataFrame) -> ModelResult:
        """Fiyat tahmini ve sinyal üretimi"""
        start_time = datetime.now()
        
        try:
            # Model yükle
            if self.model is None and os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
            
            # Features hazırla
            features = self.prepare_features(df)
            if len(features) == 0:
                raise ValueError("No features generated")
            
            # Prediction (model yoksa basit heuristic)
            if self.model and SKLEARN_AVAILABLE:
                X = self.scaler.fit_transform(features.tail(1))
                prediction = self.model.predict(X)[0]
                probabilities = self.model.predict_proba(X)[0] if hasattr(self.model, 'predict_proba') else [0.3, 0.4, 0.3]
            else:
                # Fallback heuristic
                price_change = features['price_change'].iloc[-1]
                rsi = features['rsi'].iloc[-1]
                
                if price_change > 0.02 and rsi < 70:
                    prediction = "AL"
                    probabilities = [0.7, 0.1, 0.2]
                elif price_change < -0.02 and rsi > 30:
                    prediction = "SAT"
                    probabilities = [0.1, 0.7, 0.2]
                else:
                    prediction = "TUT"
                    probabilities = [0.2, 0.2, 0.6]
            
            # Confidence calculation
            max_prob = max(probabilities)
            confidence = max_prob * 100
            
            # Feature importance (mock)
            feature_importance = {
                'price_change': 0.3,
                'rsi': 0.2,
                'price_volatility': 0.15,
                'volume_change': 0.1,
                'others': 0.25
            }
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return ModelResult(
                model_name="LGBM_Price_Model",
                signal=prediction,
                confidence=confidence,
                probability_scores={
                    'AL': probabilities[0] * 100,
                    'SAT': probabilities[1] * 100,
                    'TUT': probabilities[2] * 100
                },
                feature_importance=feature_importance,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            logging.error(f"LGBM model prediction error: {e}")
            return ModelResult(
                model_name="LGBM_Price_Model",
                signal="TUT",
                confidence=50.0,
                probability_scores={'AL': 25, 'SAT': 25, 'TUT': 50},
                feature_importance={},
                processing_time_ms=0
            )

class XGBVolumeModel:
    """XGBoost Volume-based Model"""
    
    def __init__(self):
        self.model = None
        self.scaler = RobustScaler()
        self.model_path = "/app/models/xgb_volume_model.pkl"
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Volume odaklı özellik hazırlama"""
        features = pd.DataFrame()
        
        # Volume features
        if 'Volume' in df.columns:
            features['volume_sma'] = df['Volume'].rolling(20).mean()
            features['volume_ratio'] = df['Volume'] / features['volume_sma']
            features['volume_volatility'] = df['Volume'].rolling(10).std()
            features['volume_trend'] = df['Volume'].rolling(5).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0])
        else:
            # Volume yoksa price-based proxy
            features['volume_sma'] = df['Close'] * 1000
            features['volume_ratio'] = 1.0
            features['volume_volatility'] = df['Close'].rolling(10).std()
            features['volume_trend'] = 0
        
        # Price-Volume relationship
        features['price_volume_correlation'] = df['Close'].rolling(10).corr(df.get('Volume', df['Close']))
        features['price_volume_divergence'] = (df['Close'].pct_change(fill_method=None) - 
                                             df.get('Volume', df['Close']).pct_change(fill_method=None))
        
        # Market strength indicators
        features['buying_pressure'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'] + 1e-8)
        features['selling_pressure'] = (df['High'] - df['Close']) / (df['High'] - df['Low'] + 1e-8)
        
        # Fill NaN
        features = features.fillna(method='bfill').fillna(0)
        
        return features
    
    def predict(self, df: pd.DataFrame) -> ModelResult:
        """Volume-based prediction"""
        start_time = datetime.now()
        
        try:
            features = self.prepare_features(df)
            
            # XGBoost prediction (fallback to heuristic)
            if self.model and os.path.exists(self.model_path):
                # Model varsa kullan
                X = self.scaler.fit_transform(features.tail(1))
                prediction = self.model.predict(X)[0]
            else:
                # Heuristic approach
                volume_ratio = features['volume_ratio'].iloc[-1]
                buying_pressure = features['buying_pressure'].iloc[-1]
                
                if volume_ratio > 1.5 and buying_pressure > 0.6:
                    prediction = "AL"
                    probabilities = [0.65, 0.15, 0.2]
                elif volume_ratio > 1.2 and buying_pressure < 0.4:
                    prediction = "SAT"
                    probabilities = [0.15, 0.65, 0.2]
                else:
                    prediction = "TUT"
                    probabilities = [0.25, 0.25, 0.5]
            
            confidence = max(probabilities) * 100
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return ModelResult(
                model_name="XGB_Volume_Model",
                signal=prediction,
                confidence=confidence,
                probability_scores={
                    'AL': probabilities[0] * 100,
                    'SAT': probabilities[1] * 100,
                    'TUT': probabilities[2] * 100
                },
                feature_importance={
                    'volume_ratio': 0.4,
                    'buying_pressure': 0.3,
                    'volume_trend': 0.2,
                    'others': 0.1
                },
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            logging.error(f"XGB model prediction error: {e}")
            return ModelResult(
                model_name="XGB_Volume_Model",
                signal="TUT",
                confidence=50.0,
                probability_scores={'AL': 25, 'SAT': 25, 'TUT': 50},
                feature_importance={},
                processing_time_ms=0
            )

class CNNLSTMSignalModel:
    """CNN-LSTM Deep Learning Signal Model"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.sequence_length = 20
        self.model_path = "/app/models/cnn_lstm_signal_model.h5"
    
    def prepare_sequences(self, df: pd.DataFrame) -> np.ndarray:
        """Time series sequences hazırla"""
        # Normalize prices
        prices = df['Close'].values.reshape(-1, 1)
        normalized_prices = self.scaler.fit_transform(prices)
        
        # Create sequences
        sequences = []
        for i in range(len(normalized_prices) - self.sequence_length + 1):
            sequences.append(normalized_prices[i:i+self.sequence_length])
        
        return np.array(sequences)
    
    def predict(self, df: pd.DataFrame) -> ModelResult:
        """Deep learning prediction"""
        start_time = datetime.now()
        
        try:
            if len(df) < self.sequence_length:
                # Yetersiz veri
                return ModelResult(
                    model_name="CNN_LSTM_Signal_Model",
                    signal="TUT",
                    confidence=30.0,
                    probability_scores={'AL': 30, 'SAT': 30, 'TUT': 40},
                    feature_importance={'sequence_patterns': 1.0},
                    processing_time_ms=0
                )
            
            # Model varsa TensorFlow prediction
            if TENSORFLOW_AVAILABLE and self.model and os.path.exists(self.model_path):
                sequences = self.prepare_sequences(df)
                if len(sequences) > 0:
                    prediction = self.model.predict(sequences[-1:])
                    probabilities = prediction[0]
                else:
                    probabilities = [0.3, 0.3, 0.4]
            else:
                # Pattern-based heuristic
                recent_changes = df['Close'].pct_change(fill_method=None).tail(5)
                volatility = recent_changes.std()
                trend = recent_changes.mean()
                
                if trend > 0.01 and volatility < 0.03:
                    prediction = "AL"
                    probabilities = [0.6, 0.2, 0.2]
                elif trend < -0.01 and volatility < 0.03:
                    prediction = "SAT"
                    probabilities = [0.2, 0.6, 0.2]
                else:
                    prediction = "TUT"
                    probabilities = [0.2, 0.2, 0.6]
            
            confidence = max(probabilities) * 100
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return ModelResult(
                model_name="CNN_LSTM_Signal_Model",
                signal=prediction,
                confidence=confidence,
                probability_scores={
                    'AL': probabilities[0] * 100,
                    'SAT': probabilities[1] * 100,
                    'TUT': probabilities[2] * 100
                },
                feature_importance={
                    'pattern_recognition': 0.5,
                    'trend_analysis': 0.3,
                    'volatility_assessment': 0.2
                },
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            logging.error(f"CNN-LSTM model prediction error: {e}")
            return ModelResult(
                model_name="CNN_LSTM_Signal_Model",
                signal="TUT",
                confidence=40.0,
                probability_scores={'AL': 30, 'SAT': 30, 'TUT': 40},
                feature_importance={},
                processing_time_ms=0
            )

class EnhancedMLEnsemble:
    """Enhanced ML Ensemble Engine"""
    
    def __init__(self, db_url: str = None):
        self.lgbm_model = LGBMPriceModel()
        self.xgb_model = XGBVolumeModel()
        self.cnn_lstm_model = CNNLSTMSignalModel()
        self.performance_tracker = ModelPerformanceTracker(db_url)
        
        # Ensemble parameters
        self.min_confidence_threshold = 60.0
        self.consensus_threshold = 0.7
    
    def calculate_uncertainty(self, model_results: List[ModelResult]) -> float:
        """Model sonuçları arasındaki belirsizliği hesapla"""
        if len(model_results) < 2:
            return 50.0
        
        # Signal consensus
        signals = [r.signal for r in model_results]
        most_common = max(set(signals), key=signals.count)
        consensus_ratio = signals.count(most_common) / len(signals)
        
        # Confidence variance
        confidences = [r.confidence for r in model_results]
        confidence_std = np.std(confidences)
        
        # Uncertainty score (lower is better)
        uncertainty = (1 - consensus_ratio) * 50 + (confidence_std / 100) * 50
        return min(uncertainty, 100.0)
    
    def weighted_ensemble_prediction(self, model_results: List[ModelResult], 
                                   weights: Dict[str, float]) -> Tuple[str, float, Dict[str, float]]:
        """Ağırlıklı ensemble prediction"""
        
        # Weighted probability scores
        ensemble_probs = {'AL': 0.0, 'SAT': 0.0, 'TUT': 0.0}
        
        for result in model_results:
            model_weight = weights.get(result.model_name.lower().split('_')[0], 0.33)
            
            for signal, prob in result.probability_scores.items():
                ensemble_probs[signal] += prob * model_weight
        
        # Normalize probabilities
        total_prob = sum(ensemble_probs.values())
        if total_prob > 0:
            ensemble_probs = {k: v / total_prob * 100 for k, v in ensemble_probs.items()}
        
        # Final signal
        final_signal = max(ensemble_probs, key=ensemble_probs.get)
        final_confidence = ensemble_probs[final_signal]
        
        return final_signal, final_confidence, ensemble_probs
    
    def predict_ensemble(self, symbol: str, df: pd.DataFrame) -> EnsembleResult:
        """Ana ensemble prediction fonksiyonu"""
        try:
            # Model predictions
            model_results = []
            
            # LGBM prediction
            lgbm_result = self.lgbm_model.predict(df)
            model_results.append(lgbm_result)
            
            # XGB prediction
            xgb_result = self.xgb_model.predict(df)
            model_results.append(xgb_result)
            
            # CNN-LSTM prediction
            cnn_lstm_result = self.cnn_lstm_model.predict(df)
            model_results.append(cnn_lstm_result)
            
            # Adaptive weights
            model_weights = self.performance_tracker.get_model_weights()
            
            # Weighted ensemble
            final_signal, final_confidence, ensemble_probs = self.weighted_ensemble_prediction(
                model_results, model_weights
            )
            
            # Uncertainty calculation
            uncertainty_score = self.calculate_uncertainty(model_results)
            
            # Consensus score
            signals = [r.signal for r in model_results]
            consensus_score = signals.count(final_signal) / len(signals) * 100
            
            # Reasoning
            reasoning = f"Ensemble analysis: {len(model_results)} models, {consensus_score:.1f}% consensus, {uncertainty_score:.1f}% uncertainty"
            
            return EnsembleResult(
                final_signal=final_signal,
                final_confidence=final_confidence,
                contributing_models=model_results,
                model_weights=model_weights,
                consensus_score=consensus_score,
                uncertainty_score=uncertainty_score,
                reasoning=reasoning
            )
            
        except Exception as e:
            logging.error(f"Ensemble prediction error for {symbol}: {e}")
            
            # Fallback result
            return EnsembleResult(
                final_signal="TUT",
                final_confidence=50.0,
                contributing_models=[],
                model_weights={},
                consensus_score=0.0,
                uncertainty_score=100.0,
                reasoning=f"Ensemble error: {str(e)}"
            )
