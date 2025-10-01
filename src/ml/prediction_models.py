"""
PlanB Motoru - AI Destekli Tahmin Modelleri
Makine öğrenmesi ile fiyat tahminleri
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ML Libraries
try:
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.linear_model import LinearRegression, Ridge, Lasso
    from sklearn.svm import SVR
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from src.utils.logger import log_info, log_error, log_debug

class PricePredictionModel:
    """Fiyat tahmin modeli base sınıfı"""
    
    def __init__(self, name: str):
        self.name = name
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance = None
        self.performance_metrics = {}
    
    def prepare_features(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Veri ön işleme ve feature engineering"""
        try:
            # Teknik indikatörler
            features = pd.DataFrame()
            
            # Fiyat verileri
            if 'close' in data.columns:
                features['close'] = data['close']
                features['open'] = data['open'] if 'open' in data.columns else data['close']
                features['high'] = data['high'] if 'high' in data.columns else data['close']
                features['low'] = data['low'] if 'low' in data.columns else data['close']
                features['volume'] = data['volume'] if 'volume' in data.columns else 1
            
            # Fiyat değişimleri
            features['price_change'] = features['close'].pct_change(fill_method=None)
            features['price_change_2'] = features['close'].pct_change(2)
            features['price_change_5'] = features['close'].pct_change(5)
            
            # Hareketli ortalamalar
            features['sma_5'] = features['close'].rolling(5).mean()
            features['sma_10'] = features['close'].rolling(10).mean()
            features['sma_20'] = features['close'].rolling(20).mean()
            features['ema_12'] = features['close'].ewm(span=12).mean()
            features['ema_26'] = features['close'].ewm(span=26).mean()
            
            # RSI
            delta = features['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            features['rsi'] = 100 - (100 / (1 + rs))
            
            # Bollinger Bands
            bb_period = 20
            bb_std = 2
            features['bb_middle'] = features['close'].rolling(bb_period).mean()
            bb_std_val = features['close'].rolling(bb_period).std()
            features['bb_upper'] = features['bb_middle'] + (bb_std_val * bb_std)
            features['bb_lower'] = features['bb_middle'] - (bb_std_val * bb_std)
            features['bb_width'] = (features['bb_upper'] - features['bb_lower']) / features['bb_middle']
            features['bb_position'] = (features['close'] - features['bb_lower']) / (features['bb_upper'] - features['bb_lower'])
            
            # MACD
            features['macd'] = features['ema_12'] - features['ema_26']
            features['macd_signal'] = features['macd'].ewm(span=9).mean()
            features['macd_histogram'] = features['macd'] - features['macd_signal']
            
            # Volatilite
            features['volatility'] = features['close'].rolling(20).std()
            features['volatility_ratio'] = features['volatility'] / features['close'].rolling(20).mean()
            
            # Hacim indikatörleri
            if 'volume' in features.columns:
                features['volume_sma'] = features['volume'].rolling(20).mean()
                features['volume_ratio'] = features['volume'] / features['volume_sma']
            
            # Lag features
            for lag in [1, 2, 3, 5, 10]:
                features[f'close_lag_{lag}'] = features['close'].shift(lag)
                features[f'volume_lag_{lag}'] = features['volume'].shift(lag) if 'volume' in features.columns else 0
            
            # Hedef değişken (gelecek fiyat)
            target = features['close'].shift(-1)  # Bir sonraki günün fiyatı
            
            # NaN değerleri temizle
            features = features.dropna()
            target = target[features.index]
            
            return features.values, target.values
            
        except Exception as e:
            log_error(f"Feature preparation hatası: {e}")
            return np.array([]), np.array([])
    
    def train(self, X: np.ndarray, y: np.ndarray) -> bool:
        """Modeli eğit"""
        try:
            if len(X) == 0 or len(y) == 0:
                log_error("Eğitim verisi boş")
                return False
            
            # Veriyi ölçeklendir
            X_scaled = self.scaler.fit_transform(X)
            
            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, random_state=42
            )
            
            # Modeli eğit
            self.model.fit(X_train, y_train)
            
            # Performans değerlendirmesi
            y_pred = self.model.predict(X_test)
            
            self.performance_metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'mae': mean_absolute_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred),
                'rmse': np.sqrt(mean_squared_error(y_test, y_pred))
            }
            
            # Feature importance
            if hasattr(self.model, 'feature_importances_'):
                self.feature_importance = self.model.feature_importances_
            
            self.is_trained = True
            log_info(f"{self.name} modeli eğitildi - R²: {self.performance_metrics['r2']:.3f}")
            return True
            
        except Exception as e:
            log_error(f"Model eğitimi hatası: {e}")
            return False
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Tahmin yap"""
        try:
            if not self.is_trained:
                log_error("Model eğitilmemiş")
                return np.array([])
            
            X_scaled = self.scaler.transform(X)
            predictions = self.model.predict(X_scaled)
            return predictions
            
        except Exception as e:
            log_error(f"Tahmin hatası: {e}")
            return np.array([])
    
    def get_model_info(self) -> Dict[str, Any]:
        """Model bilgilerini getir"""
        return {
            'name': self.name,
            'is_trained': self.is_trained,
            'performance_metrics': self.performance_metrics,
            'feature_importance': self.feature_importance.tolist() if self.feature_importance is not None else None
        }

class RandomForestPredictor(PricePredictionModel):
    """Random Forest tahmin modeli"""
    
    def __init__(self):
        super().__init__("Random Forest")
        if ML_AVAILABLE:
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )

class GradientBoostingPredictor(PricePredictionModel):
    """Gradient Boosting tahmin modeli"""
    
    def __init__(self):
        super().__init__("Gradient Boosting")
        if ML_AVAILABLE:
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            )

class SVMPredictor(PricePredictionModel):
    """Support Vector Machine tahmin modeli"""
    
    def __init__(self):
        super().__init__("Support Vector Machine")
        if ML_AVAILABLE:
            self.model = SVR(
                kernel='rbf',
                C=1.0,
                gamma='scale'
            )

class LinearRegressionPredictor(PricePredictionModel):
    """Linear Regression tahmin modeli"""
    
    def __init__(self):
        super().__init__("Linear Regression")
        if ML_AVAILABLE:
            self.model = LinearRegression()

class LSTMPredictor(PricePredictionModel):
    """LSTM Neural Network tahmin modeli"""
    
    def __init__(self, sequence_length: int = 60):
        super().__init__("LSTM Neural Network")
        self.sequence_length = sequence_length
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if TORCH_AVAILABLE else None
    
    def prepare_sequences(self, data: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """LSTM için sequence verileri hazırla"""
        try:
            X, y = [], []
            for i in range(self.sequence_length, len(data)):
                X.append(data[i-self.sequence_length:i])
                y.append(target[i])
            return np.array(X), np.array(y)
        except Exception as e:
            log_error(f"Sequence preparation hatası: {e}")
            return np.array([]), np.array([])
    
    def train(self, X: np.ndarray, y: np.ndarray) -> bool:
        """LSTM modelini eğit"""
        try:
            if not TORCH_AVAILABLE:
                log_error("PyTorch yüklü değil")
                return False
            
            # Sequence verileri hazırla
            X_seq, y_seq = self.prepare_sequences(X, y)
            if len(X_seq) == 0:
                return False
            
            # PyTorch tensors
            X_tensor = torch.FloatTensor(X_seq).to(self.device)
            y_tensor = torch.FloatTensor(y_seq).to(self.device)
            
            # LSTM modeli
            class LSTMModel(nn.Module):
                def __init__(self, input_size, hidden_size=50, num_layers=2, output_size=1):
                    super(LSTMModel, self).__init__()
                    self.hidden_size = hidden_size
                    self.num_layers = num_layers
                    self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
                    self.fc = nn.Linear(hidden_size, output_size)
                
                def forward(self, x):
                    h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
                    c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
                    out, _ = self.lstm(x, (h0, c0))
                    out = self.fc(out[:, -1, :])
                    return out
            
            self.model = LSTMModel(X_seq.shape[2]).to(self.device)
            criterion = nn.MSELoss()
            optimizer = optim.Adam(self.model.parameters(), lr=0.001)
            
            # Eğitim
            self.model.train()
            for epoch in range(100):
                optimizer.zero_grad()
                outputs = self.model(X_tensor)
                loss = criterion(outputs.squeeze(), y_tensor)
                loss.backward()
                optimizer.step()
                
                if epoch % 20 == 0:
                    log_debug(f"Epoch {epoch}, Loss: {loss.item():.4f}")
            
            self.is_trained = True
            log_info(f"{self.name} modeli eğitildi")
            return True
            
        except Exception as e:
            log_error(f"LSTM eğitimi hatası: {e}")
            return False
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """LSTM tahmin yap"""
        try:
            if not self.is_trained or not TORCH_AVAILABLE:
                return np.array([])
            
            # Son sequence'i al
            if len(X) >= self.sequence_length:
                X_seq = X[-self.sequence_length:].reshape(1, self.sequence_length, -1)
                X_tensor = torch.FloatTensor(X_seq).to(self.device)
                
                self.model.eval()
                with torch.no_grad():
                    prediction = self.model(X_tensor)
                    return prediction.cpu().numpy().flatten()
            
            return np.array([])
            
        except Exception as e:
            log_error(f"LSTM tahmin hatası: {e}")
            return np.array([])

class EnsemblePredictor:
    """Ensemble tahmin modeli"""
    
    def __init__(self):
        self.models = []
        self.weights = []
        self.is_trained = False
        
        # Mevcut modelleri ekle
        if ML_AVAILABLE:
            self.models.append(RandomForestPredictor())
            self.models.append(GradientBoostingPredictor())
            self.models.append(SVMPredictor())
            self.models.append(LinearRegressionPredictor())
        
        if TORCH_AVAILABLE:
            self.models.append(LSTMPredictor())
    
    def train(self, data: pd.DataFrame) -> bool:
        """Tüm modelleri eğit"""
        try:
            if not self.models:
                log_error("Hiç model yok")
                return False
            
            # Feature preparation
            X, y = self.models[0].prepare_features(data)
            if len(X) == 0:
                log_error("Feature preparation başarısız")
                return False
            
            # Her modeli eğit
            trained_models = []
            model_performances = []
            
            for model in self.models:
                if model.train(X, y):
                    trained_models.append(model)
                    if 'r2' in model.performance_metrics:
                        model_performances.append(model.performance_metrics['r2'])
                    else:
                        model_performances.append(0.5)  # Default weight
            
            if not trained_models:
                log_error("Hiç model eğitilemedi")
                return False
            
            # Model ağırlıklarını hesapla (R² skoruna göre)
            total_performance = sum(model_performances)
            if total_performance > 0:
                self.weights = [perf / total_performance for perf in model_performances]
            else:
                self.weights = [1.0 / len(trained_models)] * len(trained_models)
            
            self.models = trained_models
            self.is_trained = True
            
            log_info(f"Ensemble modeli eğitildi - {len(trained_models)} model")
            return True
            
        except Exception as e:
            log_error(f"Ensemble eğitimi hatası: {e}")
            return False
    
    def predict(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Ensemble tahmin yap"""
        try:
            if not self.is_trained:
                log_error("Ensemble modeli eğitilmemiş")
                return {}
            
            # Feature preparation
            X, _ = self.models[0].prepare_features(data)
            if len(X) == 0:
                return {}
            
            # Her modelden tahmin al
            predictions = []
            model_predictions = {}
            
            for i, model in enumerate(self.models):
                pred = model.predict(X)
                if len(pred) > 0:
                    predictions.append(pred)
                    model_predictions[model.name] = pred[-1] if len(pred) > 0 else 0
            
            if not predictions:
                return {}
            
            # Ağırlıklı ortalama
            ensemble_prediction = np.average(predictions, axis=0, weights=self.weights)
            
            # Tahmin güven aralığı
            prediction_std = np.std(predictions, axis=0)
            confidence = 1.0 / (1.0 + prediction_std)
            
            return {
                'prediction': ensemble_prediction[-1] if len(ensemble_prediction) > 0 else 0,
                'confidence': confidence[-1] if len(confidence) > 0 else 0.5,
                'model_predictions': model_predictions,
                'weights': dict(zip([m.name for m in self.models], self.weights)),
                'prediction_std': prediction_std[-1] if len(prediction_std) > 0 else 0
            }
            
        except Exception as e:
            log_error(f"Ensemble tahmin hatası: {e}")
            return {}
    
    def get_model_performance(self) -> Dict[str, Any]:
        """Model performans bilgilerini getir"""
        try:
            performance = {}
            for model in self.models:
                performance[model.name] = model.get_model_info()
            
            return {
                'ensemble_trained': self.is_trained,
                'model_count': len(self.models),
                'model_performances': performance,
                'weights': dict(zip([m.name for m in self.models], self.weights))
            }
            
        except Exception as e:
            log_error(f"Model performans bilgisi alınırken hata: {e}")
            return {}

# Global ensemble predictor instance
ensemble_predictor = EnsemblePredictor()

