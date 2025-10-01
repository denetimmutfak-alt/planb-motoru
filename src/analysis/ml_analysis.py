"""
Machine Learning Analysis Module
Makine Öğrenmesi Analiz Modülü - Ana entegrasyon sistemi
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Union, List
from datetime import datetime
import traceback

# Ultra ML import
try:
    from .ultra_ml import UltraMLAnalyzer, PredictionHorizon, ModelComplexity
    ULTRA_ML_AVAILABLE = True
except ImportError:
    ULTRA_ML_AVAILABLE = False
    print("WARNING: Ultra ML module not available")

class MLAnalyzer:
    """Ana makine öğrenmesi analiz sistemi"""
    
    def __init__(self):
        """ML Analyzer'ı başlat"""
        print("INFO: ML Analyzer başlatıldı")
        
        self.ultra_available = ULTRA_ML_AVAILABLE
        self.ultra_analyzer = UltraMLAnalyzer() if ULTRA_ML_AVAILABLE else None
        
        # Basic ML konfigürasyonu
        self.basic_weights = {
            'technical_indicators': 0.25,
            'fundamental_metrics': 0.20,
            'market_sentiment': 0.15,
            'volume_analysis': 0.12,
            'volatility_patterns': 0.10,
            'momentum_signals': 0.08,
            'support_resistance': 0.05,
            'correlation_analysis': 0.05
        }
        
        # Performance tracking
        self.analysis_history = []
        self.model_performance = {
            'total_predictions': 0,
            'accuracy_sum': 0.0,
            'average_accuracy': 0.0
        }
    
    def analyze(self, symbol: str, 
                all_analysis_results: Dict,
                analysis_mode: str = 'auto',
                historical_data: Optional[pd.DataFrame] = None,
                prediction_horizon: str = 'medium_term',
                **kwargs) -> Dict[str, Any]:
        """Ana ML analizi"""
        try:
            print(f"INFO: ML analizi başlatıldı - {symbol}")
            
            # Mode selection
            if analysis_mode == 'auto':
                # Analysis complexity'ye göre mode seç
                complexity_score = self._assess_analysis_complexity(all_analysis_results)
                if complexity_score >= 15 and self.ultra_available:
                    analysis_mode = 'ultra'
                else:
                    analysis_mode = 'basic'
            
            # Prediction horizon convert
            horizon_mapping = {
                'intraday': PredictionHorizon.INTRADAY,
                'short_term': PredictionHorizon.SHORT_TERM,
                'medium_term': PredictionHorizon.MEDIUM_TERM,
                'long_term': PredictionHorizon.LONG_TERM,
                'strategic': PredictionHorizon.STRATEGIC
            }
            
            pred_horizon = horizon_mapping.get(prediction_horizon, PredictionHorizon.MEDIUM_TERM)
            
            if analysis_mode == 'ultra' and self.ultra_available:
                return self._ultra_ml_analysis(
                    symbol, all_analysis_results, historical_data, pred_horizon, **kwargs
                )
            else:
                return self._basic_ml_analysis(
                    symbol, all_analysis_results, historical_data, pred_horizon, **kwargs
                )
                
        except Exception as e:
            print(f"ERROR: ML analizi hatası: {str(e)}")
            traceback.print_exc()
            return self._get_default_result(symbol)
    
    def _assess_analysis_complexity(self, all_analysis_results: Dict) -> int:
        """Analiz karmaşıklığını değerlendir"""
        try:
            complexity_score = 0
            
            # Her analiz modülü için +1 puan
            complexity_score += len(all_analysis_results)
            
            # Gelişmiş modüller için bonus puanlar
            advanced_modules = [
                'ultra_analysis', 'volatility_analysis', 'options_analysis',
                'gann_analysis', 'astrology_analysis', 'currency_analysis',
                'commodities_analysis', 'bonds_analysis', 'crypto_analysis'
            ]
            
            for module in advanced_modules:
                if module in all_analysis_results:
                    complexity_score += 2
            
            # Detaylı sonuçlar için bonus
            detailed_results = 0
            for result in all_analysis_results.values():
                if isinstance(result, dict):
                    detailed_results += len(result)
            
            if detailed_results > 50:
                complexity_score += 3
            elif detailed_results > 30:
                complexity_score += 2
            elif detailed_results > 15:
                complexity_score += 1
            
            return complexity_score
            
        except Exception:
            return 10  # Medium complexity default
    
    def _ultra_ml_analysis(self, symbol: str,
                          all_analysis_results: Dict,
                          historical_data: Optional[pd.DataFrame],
                          prediction_horizon: PredictionHorizon,
                          **kwargs) -> Dict[str, Any]:
        """Ultra ML analizi"""
        try:
            print(f"INFO: Ultra ML analizi başlatıldı - {symbol}")
            
            # Ultra ML analyzer kullan
            ultra_result = self.ultra_analyzer.integrate_all_analyses(
                symbol=symbol,
                all_analysis_results=all_analysis_results,
                historical_data=historical_data,
                prediction_horizon=prediction_horizon,
                **kwargs
            )
            
            # Convert to standard format
            ml_result = {
                'ml_score': ultra_result.primary_prediction.prediction_value,
                'confidence': ultra_result.primary_prediction.confidence,
                'analysis_mode': 'ultra',
                'prediction_type': 'advanced_ml_ensemble',
                'model_performance': ultra_result.model_performance,
                'feature_importance': ultra_result.feature_importance,
                'trading_signals': ultra_result.trading_signals,
                'risk_assessment': {
                    'prediction_uncertainty': ultra_result.primary_prediction.uncertainty_range,
                    'risk_factors': ultra_result.primary_prediction.risk_factors,
                    'confidence_metrics': ultra_result.confidence_metrics
                },
                'predictions': {
                    'primary': ultra_result.primary_prediction.prediction_value,
                    'ensemble': ultra_result.ensemble_prediction.weighted_prediction,
                    'risk_adjusted': ultra_result.risk_adjusted_forecasts,
                    'scenarios': ultra_result.scenario_analysis
                },
                'ml_insights': {
                    'prediction_explanations': ultra_result.prediction_explanations,
                    'model_consensus': ultra_result.ensemble_prediction.consensus_strength,
                    'uncertainty_range': ultra_result.primary_prediction.uncertainty_range,
                    'supporting_evidence': ultra_result.primary_prediction.supporting_evidence
                },
                'recommendation': ultra_result.recommendation_summary,
                'details': {
                    'horizon': prediction_horizon.value,
                    'features_used': ultra_result.primary_prediction.features_used,
                    'model_accuracy': ultra_result.primary_prediction.model_accuracy,
                    'ensemble_details': {
                        'individual_predictions': ultra_result.ensemble_prediction.individual_predictions,
                        'model_weights': ultra_result.ensemble_prediction.model_weights,
                        'prediction_variance': ultra_result.ensemble_prediction.prediction_variance
                    }
                }
            }
            
            # Performance tracking
            self._update_performance_tracking(ultra_result.primary_prediction.model_accuracy)
            
            return ml_result
            
        except Exception as e:
            print(f"ERROR: Ultra ML analizi hatası: {str(e)}")
            traceback.print_exc()
            return self._basic_ml_analysis(symbol, all_analysis_results, historical_data, prediction_horizon, **kwargs)
    
    def _basic_ml_analysis(self, symbol: str,
                          all_analysis_results: Dict,
                          historical_data: Optional[pd.DataFrame],
                          prediction_horizon: PredictionHorizon,
                          **kwargs) -> Dict[str, Any]:
        """Basit ML analizi"""
        try:
            print(f"INFO: Basic ML analizi - {symbol}")
            
            # Feature extraction
            features = self._extract_basic_features(all_analysis_results, historical_data)
            
            # Simple prediction model
            ml_score = self._calculate_basic_ml_score(features, all_analysis_results)
            
            # Confidence calculation
            confidence = self._calculate_basic_confidence(features, all_analysis_results)
            
            # Trading signals
            trading_signals = self._generate_basic_trading_signals(ml_score, confidence)
            
            # Risk assessment
            risk_assessment = self._basic_risk_assessment(ml_score, confidence, all_analysis_results)
            
            # Feature importance
            feature_importance = self._calculate_basic_feature_importance(features)
            
            # ML insights
            ml_insights = self._generate_basic_ml_insights(ml_score, confidence, features)
            
            # Predictions
            predictions = self._generate_basic_predictions(ml_score, all_analysis_results)
            
            # Recommendation
            recommendation = self._generate_basic_recommendation(symbol, ml_score, confidence, trading_signals)
            
            ml_result = {
                'ml_score': ml_score,
                'confidence': confidence,
                'analysis_mode': 'basic',
                'prediction_type': 'weighted_ensemble',
                'model_performance': {'basic_model_accuracy': 0.72},
                'feature_importance': feature_importance,
                'trading_signals': trading_signals,
                'risk_assessment': risk_assessment,
                'predictions': predictions,
                'ml_insights': ml_insights,
                'recommendation': recommendation,
                'details': {
                    'horizon': prediction_horizon.value,
                    'features_used': list(features.keys()),
                    'model_type': 'weighted_average',
                    'basic_model_info': 'Rule-based ensemble with weighted scoring'
                }
            }
            
            # Performance tracking
            self._update_performance_tracking(0.72)  # Basic model accuracy
            
            return ml_result
            
        except Exception as e:
            print(f"ERROR: Basic ML analizi hatası: {str(e)}")
            return self._get_default_result(symbol)
    
    def _extract_basic_features(self, all_analysis_results: Dict,
                               historical_data: Optional[pd.DataFrame]) -> Dict[str, float]:
        """Basit özellik çıkarma"""
        try:
            features = {}
            
            # Analysis scores
            for analysis_name, result in all_analysis_results.items():
                if isinstance(result, dict):
                    if 'score' in result:
                        features[f'{analysis_name}_score'] = result['score']
                    elif f'{analysis_name}_score' in result:
                        features[f'{analysis_name}_score'] = result[f'{analysis_name}_score']
                    
                    # Confidence features
                    if 'confidence' in result:
                        features[f'{analysis_name}_confidence'] = result['confidence']
            
            # Technical features from historical data
            if historical_data is not None and not historical_data.empty:
                if 'Close' in historical_data.columns:
                    close_prices = historical_data['Close'].values
                    if len(close_prices) > 10:
                        # Price momentum
                        features['price_momentum_5d'] = (close_prices[-1] / close_prices[-6] - 1) * 100 if len(close_prices) > 5 else 0
                        features['price_momentum_10d'] = (close_prices[-1] / close_prices[-11] - 1) * 100 if len(close_prices) > 10 else 0
                        
                        # Volatility
                        features['recent_volatility'] = np.std(close_prices[-10:]) / np.mean(close_prices[-10:]) * 100
                
                # Volume features
                if 'Volume' in historical_data.columns:
                    volumes = historical_data['Volume'].values
                    if len(volumes) > 5:
                        features['volume_trend'] = (np.mean(volumes[-3:]) / np.mean(volumes[-6:-3]) - 1) * 100
            
            # Sentiment aggregation
            sentiment_scores = []
            for analysis_name, result in all_analysis_results.items():
                if isinstance(result, dict):
                    for key, value in result.items():
                        if 'sentiment' in key.lower() and isinstance(value, (int, float)):
                            sentiment_scores.append(value)
            
            if sentiment_scores:
                features['aggregated_sentiment'] = np.mean(sentiment_scores)
            
            # Risk aggregation
            risk_scores = []
            for analysis_name, result in all_analysis_results.items():
                if isinstance(result, dict) and 'risk_assessment' in result:
                    risk_data = result['risk_assessment']
                    if isinstance(risk_data, dict) and 'overall_risk' in risk_data:
                        risk_text = risk_data['overall_risk']
                        risk_value = self._risk_text_to_numeric(risk_text)
                        risk_scores.append(risk_value)
            
            if risk_scores:
                features['aggregated_risk'] = np.mean(risk_scores)
            
            # Fill missing values
            default_features = {
                'financial_score': 50, 'technical_score': 50, 'trend_score': 50,
                'aggregated_sentiment': 50, 'aggregated_risk': 50,
                'price_momentum_5d': 0, 'recent_volatility': 15
            }
            
            for key, default_value in default_features.items():
                if key not in features:
                    features[key] = default_value
            
            return features
            
        except Exception as e:
            print(f"WARNING: Feature extraction hatası: {str(e)}")
            return {
                'financial_score': 50, 'technical_score': 50,
                'aggregated_sentiment': 50, 'aggregated_risk': 50
            }
    
    def _calculate_basic_ml_score(self, features: Dict[str, float],
                                 all_analysis_results: Dict) -> float:
        """Basit ML skoru hesaplama"""
        try:
            weighted_score = 0.0
            total_weight = 0.0
            
            # Weight mapping for features
            feature_weights = {
                'financial_score': 0.20,
                'technical_score': 0.18,
                'trend_score': 0.15,
                'volatility_score': 0.12,
                'risk_score': 0.10,
                'sentiment_score': 0.08,
                'momentum_score': 0.07,
                'volume_score': 0.05,
                'aggregated_sentiment': 0.03,
                'price_momentum_5d': 0.02
            }
            
            # Calculate weighted average
            for feature_name, feature_value in features.items():
                # Find appropriate weight
                weight = 0.05  # Default weight
                for weight_key, weight_value in feature_weights.items():
                    if weight_key in feature_name:
                        weight = weight_value
                        break
                
                # Normalize feature value to 0-100 scale
                normalized_value = max(0, min(100, feature_value))
                
                weighted_score += normalized_value * weight
                total_weight += weight
            
            # Normalize result
            if total_weight > 0:
                ml_score = weighted_score / total_weight
            else:
                ml_score = 50  # Neutral score
            
            # Apply momentum adjustment
            momentum_adjustment = 0
            if 'price_momentum_5d' in features:
                momentum = features['price_momentum_5d']
                if abs(momentum) > 5:  # Significant momentum
                    momentum_adjustment = np.sign(momentum) * min(5, abs(momentum) / 2)
            
            # Apply volatility adjustment
            volatility_adjustment = 0
            if 'recent_volatility' in features:
                volatility = features['recent_volatility']
                if volatility > 20:  # High volatility penalty
                    volatility_adjustment = -min(3, (volatility - 20) / 5)
            
            # Apply sentiment adjustment
            sentiment_adjustment = 0
            if 'aggregated_sentiment' in features:
                sentiment = features['aggregated_sentiment']
                sentiment_deviation = sentiment - 50
                sentiment_adjustment = sentiment_deviation * 0.1
            
            # Final score
            final_score = ml_score + momentum_adjustment + volatility_adjustment + sentiment_adjustment
            final_score = max(0, min(100, final_score))
            
            return final_score
            
        except Exception as e:
            print(f"WARNING: ML score calculation hatası: {str(e)}")
            return 50.0
    
    def _calculate_basic_confidence(self, features: Dict[str, float],
                                   all_analysis_results: Dict) -> float:
        """Basit güven hesaplama"""
        try:
            confidence_factors = []
            
            # Feature completeness
            expected_features = ['financial_score', 'technical_score', 'aggregated_sentiment']
            feature_completeness = sum(1 for f in expected_features if f in features) / len(expected_features)
            confidence_factors.append(feature_completeness * 100)
            
            # Analysis diversity
            analysis_count = len(all_analysis_results)
            diversity_score = min(100, analysis_count * 5)  # More analyses = higher confidence
            confidence_factors.append(diversity_score)
            
            # Consistency check
            score_features = [v for k, v in features.items() if 'score' in k and isinstance(v, (int, float))]
            if len(score_features) > 1:
                score_std = np.std(score_features)
                consistency_score = max(50, 100 - score_std)  # Lower std = higher consistency
                confidence_factors.append(consistency_score)
            else:
                confidence_factors.append(70)
            
            # Risk factor
            risk_value = features.get('aggregated_risk', 50)
            risk_confidence = 100 - risk_value  # Lower risk = higher confidence
            confidence_factors.append(risk_confidence)
            
            # Average confidence
            avg_confidence = np.mean(confidence_factors)
            
            # Ensure reasonable bounds
            final_confidence = max(40, min(95, avg_confidence))
            
            return final_confidence
            
        except Exception as e:
            print(f"WARNING: Confidence calculation hatası: {str(e)}")
            return 70.0
    
    def _generate_basic_trading_signals(self, ml_score: float, confidence: float) -> Dict[str, Union[str, float]]:
        """Basit trading sinyalleri"""
        try:
            signals = {}
            
            # Primary signal
            if ml_score >= 75 and confidence >= 80:
                signals['primary_signal'] = 'GÜÇLÜ ALIŞ'
                signals['signal_strength'] = 90
            elif ml_score >= 65 and confidence >= 70:
                signals['primary_signal'] = 'ALIŞ'
                signals['signal_strength'] = 75
            elif ml_score >= 55 and confidence >= 60:
                signals['primary_signal'] = 'ZAYIF ALIŞ'
                signals['signal_strength'] = 60
            elif ml_score <= 35 and confidence >= 70:
                signals['primary_signal'] = 'SAT'
                signals['signal_strength'] = 25
            elif ml_score <= 45 and confidence >= 60:
                signals['primary_signal'] = 'ZAYIF SAT'
                signals['signal_strength'] = 40
            else:
                signals['primary_signal'] = 'BEKLE'
                signals['signal_strength'] = 50
            
            # Confidence signal
            if confidence >= 85:
                signals['confidence_signal'] = 'Çok Yüksek Güven'
            elif confidence >= 75:
                signals['confidence_signal'] = 'Yüksek Güven'
            elif confidence >= 65:
                signals['confidence_signal'] = 'Orta Güven'
            else:
                signals['confidence_signal'] = 'Düşük Güven'
            
            # Risk-reward estimates
            signals['estimated_upside'] = max(0, ml_score - 50) * 0.8
            signals['estimated_downside'] = max(0, 50 - ml_score) * 0.6
            
            if signals['estimated_downside'] > 0:
                signals['risk_reward_ratio'] = signals['estimated_upside'] / signals['estimated_downside']
            else:
                signals['risk_reward_ratio'] = 5.0
            
            return signals
            
        except Exception as e:
            print(f"WARNING: Trading signals hatası: {str(e)}")
            return {
                'primary_signal': 'BEKLE',
                'signal_strength': 50,
                'confidence_signal': 'Orta Güven'
            }
    
    def _basic_risk_assessment(self, ml_score: float, confidence: float,
                              all_analysis_results: Dict) -> Dict[str, Any]:
        """Basit risk değerlendirmesi"""
        try:
            risk_assessment = {}
            
            # ML prediction risk
            if ml_score > 80 or ml_score < 20:
                risk_assessment['prediction_risk'] = 'Yüksek'
                risk_assessment['prediction_risk_reason'] = 'Extreme prediction values'
            elif ml_score > 70 or ml_score < 30:
                risk_assessment['prediction_risk'] = 'Orta'
                risk_assessment['prediction_risk_reason'] = 'High prediction values'
            else:
                risk_assessment['prediction_risk'] = 'Düşük'
                risk_assessment['prediction_risk_reason'] = 'Moderate prediction range'
            
            # Confidence risk
            if confidence < 60:
                risk_assessment['confidence_risk'] = 'Yüksek'
            elif confidence < 75:
                risk_assessment['confidence_risk'] = 'Orta'
            else:
                risk_assessment['confidence_risk'] = 'Düşük'
            
            # Model reliability
            model_reliability = min(confidence, 90)
            if model_reliability >= 80:
                risk_assessment['model_reliability'] = 'Yüksek'
            elif model_reliability >= 65:
                risk_assessment['model_reliability'] = 'Orta'
            else:
                risk_assessment['model_reliability'] = 'Düşük'
            
            # Overall risk
            risk_factors = []
            if confidence < 65:
                risk_factors.append('Low prediction confidence')
            if ml_score > 85 or ml_score < 15:
                risk_factors.append('Extreme prediction values')
            
            if len(risk_factors) >= 2:
                risk_assessment['overall_risk'] = 'Yüksek Risk'
            elif len(risk_factors) == 1:
                risk_assessment['overall_risk'] = 'Orta Risk'
            else:
                risk_assessment['overall_risk'] = 'Düşük Risk'
            
            risk_assessment['risk_factors'] = risk_factors
            
            return risk_assessment
            
        except Exception as e:
            print(f"WARNING: Risk assessment hatası: {str(e)}")
            return {
                'overall_risk': 'Orta Risk',
                'model_reliability': 'Orta',
                'risk_factors': []
            }
    
    def _calculate_basic_feature_importance(self, features: Dict[str, float]) -> Dict[str, float]:
        """Basit feature importance"""
        try:
            importance = {}
            
            # Predefined importance weights
            importance_weights = {
                'financial': 0.25,
                'technical': 0.20,
                'sentiment': 0.15,
                'trend': 0.12,
                'volatility': 0.10,
                'momentum': 0.08,
                'risk': 0.05,
                'volume': 0.05
            }
            
            # Assign importance based on feature names
            for feature_name in features.keys():
                assigned_importance = 0.02  # Default
                
                for keyword, weight in importance_weights.items():
                    if keyword in feature_name.lower():
                        assigned_importance = weight
                        break
                
                importance[feature_name] = assigned_importance
            
            # Normalize
            total_importance = sum(importance.values())
            if total_importance > 0:
                for feature_name in importance:
                    importance[feature_name] /= total_importance
            
            return importance
            
        except Exception:
            return {'financial_score': 0.4, 'technical_score': 0.3, 'sentiment': 0.3}
    
    def _generate_basic_ml_insights(self, ml_score: float, confidence: float,
                                   features: Dict[str, float]) -> Dict[str, Any]:
        """Basit ML insights"""
        try:
            insights = {}
            
            # Score interpretation
            if ml_score >= 75:
                insights['score_interpretation'] = 'Güçlü pozitif sinyal - Yüksek kazanç potansiyeli'
            elif ml_score >= 65:
                insights['score_interpretation'] = 'Pozitif sinyal - Orta kazanç beklentisi'
            elif ml_score >= 55:
                insights['score_interpretation'] = 'Zayıf pozitif sinyal - Sınırlı potansiyel'
            elif ml_score >= 45:
                insights['score_interpretation'] = 'Nötr - Belirsiz yönelim'
            elif ml_score >= 35:
                insights['score_interpretation'] = 'Zayıf negatif - Düşüş riski'
            else:
                insights['score_interpretation'] = 'Güçlü negatif - Yüksek düşüş riski'
            
            # Confidence interpretation
            if confidence >= 85:
                insights['confidence_interpretation'] = 'Çok yüksek güven - Güvenilir tahmin'
            elif confidence >= 75:
                insights['confidence_interpretation'] = 'Yüksek güven - İyi tahmin kalitesi'
            elif confidence >= 65:
                insights['confidence_interpretation'] = 'Orta güven - Makul tahmin'
            else:
                insights['confidence_interpretation'] = 'Düşük güven - Dikkatli olun'
            
            # Key driving factors
            driving_factors = []
            for feature_name, feature_value in features.items():
                if 'score' in feature_name and feature_value > 70:
                    driving_factors.append(f"Güçlü {feature_name.replace('_score', '')} performansı")
                elif 'score' in feature_name and feature_value < 30:
                    driving_factors.append(f"Zayıf {feature_name.replace('_score', '')} performansı")
            
            insights['driving_factors'] = driving_factors[:3]  # Top 3
            
            # Prediction reliability
            feature_count = len(features)
            if feature_count >= 8:
                insights['prediction_reliability'] = 'Yüksek - Çok sayıda analiz faktörü'
            elif feature_count >= 5:
                insights['prediction_reliability'] = 'Orta - Yeterli analiz faktörü'
            else:
                insights['prediction_reliability'] = 'Düşük - Sınırlı analiz faktörü'
            
            return insights
            
        except Exception:
            return {
                'score_interpretation': 'Orta seviye tahmin',
                'confidence_interpretation': 'Makul güven seviyesi'
            }
    
    def _generate_basic_predictions(self, ml_score: float,
                                   all_analysis_results: Dict) -> Dict[str, float]:
        """Basit tahminler"""
        try:
            predictions = {}
            
            # Base prediction
            predictions['base_prediction'] = ml_score
            
            # Conservative prediction (reduce by volatility/risk)
            risk_adjustment = 0.85  # 15% haircut for risk
            predictions['conservative'] = ml_score * risk_adjustment
            
            # Optimistic prediction (increase by potential)
            optimistic_adjustment = 1.15  # 15% bonus for upside
            predictions['optimistic'] = min(100, ml_score * optimistic_adjustment)
            
            # Risk-adjusted prediction
            # Get average risk from all analyses
            risk_scores = []
            for result in all_analysis_results.values():
                if isinstance(result, dict) and 'risk_assessment' in result:
                    risk_data = result['risk_assessment']
                    if isinstance(risk_data, dict) and 'overall_risk' in risk_data:
                        risk_text = risk_data['overall_risk']
                        risk_value = self._risk_text_to_numeric(risk_text)
                        risk_scores.append(risk_value)
            
            if risk_scores:
                avg_risk = np.mean(risk_scores)
                risk_factor = (100 - avg_risk) / 100
                predictions['risk_adjusted'] = ml_score * risk_factor
            else:
                predictions['risk_adjusted'] = ml_score * 0.9
            
            # Ensure bounds
            for key in predictions:
                predictions[key] = max(0, min(100, predictions[key]))
            
            return predictions
            
        except Exception:
            return {
                'base_prediction': ml_score,
                'conservative': ml_score * 0.85,
                'optimistic': min(100, ml_score * 1.15)
            }
    
    def _generate_basic_recommendation(self, symbol: str, ml_score: float,
                                     confidence: float, trading_signals: Dict) -> str:
        """Basit recommendation"""
        try:
            signal = trading_signals.get('primary_signal', 'BEKLE')
            confidence_level = trading_signals.get('confidence_signal', 'Orta Güven')
            
            recommendation = f"{symbol} için ML analizi tamamlandı. "
            
            if ml_score >= 70:
                recommendation += f"Pozitif tahmin (%{ml_score:.1f}) "
            elif ml_score >= 50:
                recommendation += f"Nötr tahmin (%{ml_score:.1f}) "
            else:
                recommendation += f"Negatif tahmin (%{ml_score:.1f}) "
            
            recommendation += f"ile {confidence_level.lower()}. "
            recommendation += f"Önerilen işlem: {signal.lower()}."
            
            return recommendation
            
        except Exception:
            return f"{symbol} için ML analizi tamamlandı - makul güven seviyesi ile bekle önerisi"
    
    def _risk_text_to_numeric(self, risk_text: str) -> float:
        """Risk text'ini numeric'e çevir"""
        risk_mapping = {
            'çok düşük risk': 10, 'düşük risk': 25, 'düşük-orta': 35,
            'orta risk': 50, 'orta-yüksek': 65, 'yüksek risk': 75,
            'çok yüksek risk': 90, 'extreme': 95
        }
        
        risk_lower = risk_text.lower()
        for key, value in risk_mapping.items():
            if key in risk_lower:
                return value
        return 50
    
    def _update_performance_tracking(self, accuracy: float):
        """Performans tracking güncelle"""
        try:
            self.model_performance['total_predictions'] += 1
            self.model_performance['accuracy_sum'] += accuracy
            self.model_performance['average_accuracy'] = (
                self.model_performance['accuracy_sum'] / 
                self.model_performance['total_predictions']
            )
        except Exception:
            pass
    
    def _get_default_result(self, symbol: str) -> Dict[str, Any]:
        """Varsayılan sonuç"""
        return {
            'ml_score': 50.0,
            'confidence': 65.0,
            'analysis_mode': 'fallback',
            'prediction_type': 'default',
            'model_performance': {'accuracy': 0.60},
            'feature_importance': {'default': 1.0},
            'trading_signals': {
                'primary_signal': 'BEKLE',
                'signal_strength': 50,
                'confidence_signal': 'Orta Güven'
            },
            'risk_assessment': {
                'overall_risk': 'Orta Risk',
                'model_reliability': 'Orta'
            },
            'predictions': {
                'base_prediction': 50.0,
                'conservative': 45.0,
                'optimistic': 55.0
            },
            'ml_insights': {
                'score_interpretation': 'Nötr seviye tahmin',
                'confidence_interpretation': 'Orta güven seviyesi'
            },
            'recommendation': f"{symbol} için ML analizi - orta güven ile bekle önerisi",
            'details': {
                'horizon': 'medium_term',
                'features_used': ['fallback'],
                'model_type': 'fallback'
            }
        }

# Test fonksiyonu
if __name__ == "__main__":
    analyzer = MLAnalyzer()
    
    # Test data
    test_results = {
        'financial': {'score': 72, 'confidence': 85},
        'technical': {'score': 68, 'confidence': 78},
        'sentiment': {'score': 65, 'confidence': 70}
    }
    
    result = analyzer.analyze('TEST', test_results)
    print("ML Analysis Test Result:")
    print(f"ML Score: {result['ml_score']:.1f}")
    print(f"Confidence: {result['confidence']:.1f}")
    print(f"Signal: {result['trading_signals']['primary_signal']}")
    print(f"Mode: {result['analysis_mode']}")
