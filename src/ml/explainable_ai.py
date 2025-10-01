"""
PlanB Motoru - Explainable AI
Tahmin açıklamaları ve model interpretability
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug

class ExplainableAI:
    """Explainable AI - Tahmin açıklamaları"""
    
    def __init__(self):
        self.feature_importance_weights = {
            'technical': 0.3,
            'fundamental': 0.25,
            'sentiment': 0.2,
            'astrology': 0.15,
            'cycles': 0.1
        }
        
        self.explanation_templates = {
            'bullish': [
                "Güçlü teknik göstergeler pozitif momentum gösteriyor",
                "Temel analiz verileri şirketin sağlamlığını destekliyor",
                "Pozitif market sentimenti fiyat artışını destekliyor",
                "Astrolojik döngüler olumlu zamanlama gösteriyor"
            ],
            'bearish': [
                "Teknik göstergeler düşüş sinyali veriyor",
                "Temel analiz zayıflık işaretleri gösteriyor",
                "Negatif market sentimenti satış baskısı yaratıyor",
                "Astrolojik döngüler zorlu dönem işaret ediyor"
            ],
            'neutral': [
                "Teknik göstergeler karışık sinyaller veriyor",
                "Temel analiz dengeli görünüyor",
                "Market sentimenti nötr seviyede",
                "Astrolojik döngüler belirsizlik gösteriyor"
            ]
        }
    
    def explain_prediction(self, symbol: str, prediction_data: Dict[str, Any], 
                          analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tahmin açıklaması oluştur"""
        try:
            # Temel tahmin bilgileri
            predicted_price = prediction_data.get('predicted_price', 0)
            current_price = prediction_data.get('current_price', 0)
            confidence = prediction_data.get('confidence', 0.5)
            
            # Fiyat değişim yüzdesi
            price_change_pct = ((predicted_price - current_price) / current_price * 100) if current_price > 0 else 0
            
            # Tahmin yönü
            prediction_direction = self._get_prediction_direction(price_change_pct)
            
            # Ana faktörleri analiz et
            key_factors = self._analyze_key_factors(analysis_data)
            
            # Açıklama metni oluştur
            explanation_text = self._generate_explanation_text(
                symbol, prediction_direction, price_change_pct, key_factors, confidence
            )
            
            # Risk faktörleri
            risk_factors = self._identify_risk_factors(analysis_data)
            
            # Güven seviyesi açıklaması
            confidence_explanation = self._explain_confidence(confidence, key_factors)
            
            return {
                'symbol': symbol,
                'prediction_direction': prediction_direction,
                'price_change_pct': price_change_pct,
                'confidence': confidence,
                'explanation_text': explanation_text,
                'key_factors': key_factors,
                'risk_factors': risk_factors,
                'confidence_explanation': confidence_explanation,
                'model_insights': self._generate_model_insights(prediction_data),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            log_error(f"Tahmin açıklaması oluşturma hatası: {e}")
            return {}
    
    def _get_prediction_direction(self, price_change_pct: float) -> str:
        """Tahmin yönünü belirle"""
        if price_change_pct > 5:
            return 'strong_bullish'
        elif price_change_pct > 2:
            return 'bullish'
        elif price_change_pct > -2:
            return 'neutral'
        elif price_change_pct > -5:
            return 'bearish'
        else:
            return 'strong_bearish'
    
    def _analyze_key_factors(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Ana faktörleri analiz et"""
        try:
            key_factors = []
            
            # Teknik analiz faktörleri
            technical_score = analysis_data.get('technical_score', 50)
            if technical_score > 60:
                key_factors.append({
                    'category': 'technical',
                    'factor': 'Güçlü Teknik Göstergeler',
                    'impact': 'positive',
                    'weight': 0.3,
                    'description': f'RSI, MACD ve hareketli ortalamalar pozitif sinyal veriyor (Skor: {technical_score})'
                })
            elif technical_score < 40:
                key_factors.append({
                    'category': 'technical',
                    'factor': 'Zayıf Teknik Göstergeler',
                    'impact': 'negative',
                    'weight': 0.3,
                    'description': f'RSI, MACD ve hareketli ortalamalar negatif sinyal veriyor (Skor: {technical_score})'
                })
            
            # Temel analiz faktörleri
            financial_score = analysis_data.get('financial_score', 50)
            if financial_score > 60:
                key_factors.append({
                    'category': 'fundamental',
                    'factor': 'Sağlam Temel Analiz',
                    'impact': 'positive',
                    'weight': 0.25,
                    'description': f'Finansal sağlamlık ve büyüme göstergeleri olumlu (Skor: {financial_score})'
                })
            elif financial_score < 40:
                key_factors.append({
                    'category': 'fundamental',
                    'factor': 'Zayıf Temel Analiz',
                    'impact': 'negative',
                    'weight': 0.25,
                    'description': f'Finansal sağlamlık ve büyüme göstergeleri zayıf (Skor: {financial_score})'
                })
            
            # Sentiment faktörleri
            sentiment_score = analysis_data.get('sentiment_score', 50)
            if sentiment_score > 60:
                key_factors.append({
                    'category': 'sentiment',
                    'factor': 'Pozitif Market Sentimenti',
                    'impact': 'positive',
                    'weight': 0.2,
                    'description': f'Twitter, haberler ve sosyal medya pozitif (Skor: {sentiment_score})'
                })
            elif sentiment_score < 40:
                key_factors.append({
                    'category': 'sentiment',
                    'factor': 'Negatif Market Sentimenti',
                    'impact': 'negative',
                    'weight': 0.2,
                    'description': f'Twitter, haberler ve sosyal medya negatif (Skor: {sentiment_score})'
                })
            
            # Astrolojik faktörler
            astrology_score = analysis_data.get('astrology_score', 50)
            if astrology_score > 60:
                key_factors.append({
                    'category': 'astrology',
                    'factor': 'Olumlu Astrolojik Döngüler',
                    'impact': 'positive',
                    'weight': 0.15,
                    'description': f'Vedik astroloji ve gezegen döngüleri olumlu (Skor: {astrology_score})'
                })
            elif astrology_score < 40:
                key_factors.append({
                    'category': 'astrology',
                    'factor': 'Zorlu Astrolojik Döngüler',
                    'impact': 'negative',
                    'weight': 0.15,
                    'description': f'Vedik astroloji ve gezegen döngüleri zorlu (Skor: {astrology_score})'
                })
            
            # Döngüsel faktörler
            cycle_score = analysis_data.get('shemitah_score', 50)
            if cycle_score > 60:
                key_factors.append({
                    'category': 'cycles',
                    'factor': 'Olumlu Döngüsel Dönem',
                    'impact': 'positive',
                    'weight': 0.1,
                    'description': f'Shemitah ve spiral döngüler olumlu (Skor: {cycle_score})'
                })
            elif cycle_score < 40:
                key_factors.append({
                    'category': 'cycles',
                    'factor': 'Zorlu Döngüsel Dönem',
                    'impact': 'negative',
                    'weight': 0.1,
                    'description': f'Shemitah ve spiral döngüler zorlu (Skor: {cycle_score})'
                })
            
            return key_factors
            
        except Exception as e:
            log_error(f"Ana faktör analizi hatası: {e}")
            return []
    
    def _generate_explanation_text(self, symbol: str, direction: str, 
                                 price_change_pct: float, key_factors: List[Dict[str, Any]], 
                                 confidence: float) -> str:
        """Açıklama metni oluştur"""
        try:
            # Yön bazlı açıklama
            if direction in ['strong_bullish', 'bullish']:
                direction_text = f"{symbol} için %{abs(price_change_pct):.1f} yükseliş tahmini"
                template_key = 'bullish'
            elif direction in ['strong_bearish', 'bearish']:
                direction_text = f"{symbol} için %{abs(price_change_pct):.1f} düşüş tahmini"
                template_key = 'bearish'
            else:
                direction_text = f"{symbol} için nötr tahmin"
                template_key = 'neutral'
            
            # Ana faktörleri özetle
            positive_factors = [f for f in key_factors if f['impact'] == 'positive']
            negative_factors = [f for f in key_factors if f['impact'] == 'negative']
            
            explanation_parts = [direction_text]
            
            if positive_factors:
                explanation_parts.append(f"Destekleyici faktörler: {', '.join([f['factor'] for f in positive_factors[:2]])}")
            
            if negative_factors:
                explanation_parts.append(f"Risk faktörleri: {', '.join([f['factor'] for f in negative_factors[:2]])}")
            
            # Güven seviyesi
            if confidence > 0.8:
                confidence_text = "Yüksek güven seviyesi"
            elif confidence > 0.6:
                confidence_text = "Orta güven seviyesi"
            else:
                confidence_text = "Düşük güven seviyesi"
            
            explanation_parts.append(f"Tahmin güveni: {confidence_text} (%{confidence*100:.0f})")
            
            return ". ".join(explanation_parts) + "."
            
        except Exception as e:
            log_error(f"Açıklama metni oluşturma hatası: {e}")
            return f"{symbol} için tahmin açıklaması oluşturulamadı."
    
    def _identify_risk_factors(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Risk faktörlerini belirle"""
        try:
            risk_factors = []
            
            # Düşük skorlu faktörler
            low_score_factors = [
                ('technical_score', 'Teknik Analiz Zayıflığı'),
                ('financial_score', 'Temel Analiz Zayıflığı'),
                ('sentiment_score', 'Negatif Market Sentimenti'),
                ('astrology_score', 'Zorlu Astrolojik Dönem'),
                ('shemitah_score', 'Zorlu Döngüsel Dönem')
            ]
            
            for score_key, risk_name in low_score_factors:
                score = analysis_data.get(score_key, 50)
                if score < 40:
                    risk_factors.append({
                        'risk_type': risk_name,
                        'severity': 'high' if score < 30 else 'medium',
                        'score': score,
                        'description': f'{risk_name} düşük skor gösteriyor ({score})'
                    })
            
            # Volatilite riski
            volatility = analysis_data.get('volatility', 0)
            if volatility > 0.3:  # %30+ volatilite
                risk_factors.append({
                    'risk_type': 'Yüksek Volatilite',
                    'severity': 'high',
                    'volatility': volatility,
                    'description': f'Yüksek volatilite riski (%{volatility*100:.1f})'
                })
            
            return risk_factors
            
        except Exception as e:
            log_error(f"Risk faktörleri belirleme hatası: {e}")
            return []
    
    def _explain_confidence(self, confidence: float, key_factors: List[Dict[str, Any]]) -> str:
        """Güven seviyesini açıkla"""
        try:
            if confidence > 0.8:
                return "Yüksek güven seviyesi: Tüm ana faktörler tutarlı sinyal veriyor"
            elif confidence > 0.6:
                return "Orta güven seviyesi: Çoğu faktör tutarlı, bazı belirsizlikler var"
            elif confidence > 0.4:
                return "Düşük güven seviyesi: Faktörler karışık sinyal veriyor"
            else:
                return "Çok düşük güven seviyesi: Faktörler çelişkili, dikkatli olun"
                
        except Exception as e:
            return "Güven seviyesi açıklanamadı"
    
    def _generate_model_insights(self, prediction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Model içgörüleri oluştur"""
        try:
            model_predictions = prediction_data.get('model_predictions', {})
            weights = prediction_data.get('weights', {})
            
            insights = {
                'ensemble_models': len(model_predictions),
                'model_agreement': self._calculate_model_agreement(model_predictions),
                'dominant_model': self._find_dominant_model(weights),
                'prediction_consensus': self._assess_prediction_consensus(model_predictions)
            }
            
            return insights
            
        except Exception as e:
            log_error(f"Model içgörüleri oluşturma hatası: {e}")
            return {}
    
    def _calculate_model_agreement(self, model_predictions: Dict[str, float]) -> float:
        """Model uyumunu hesapla"""
        try:
            if not model_predictions:
                return 0.0
            
            predictions = list(model_predictions.values())
            if len(predictions) < 2:
                return 1.0
            
            # Standart sapma ile uyum ölçümü
            std_dev = np.std(predictions)
            mean_pred = np.mean(predictions)
            
            # Düşük standart sapma = yüksek uyum
            agreement = 1.0 - (std_dev / mean_pred) if mean_pred > 0 else 0.0
            return max(0.0, min(1.0, agreement))
            
        except Exception as e:
            return 0.0
    
    def _find_dominant_model(self, weights: Dict[str, float]) -> str:
        """Dominant modeli bul"""
        try:
            if not weights:
                return "Unknown"
            
            return max(weights.items(), key=lambda x: x[1])[0]
            
        except Exception as e:
            return "Unknown"
    
    def _assess_prediction_consensus(self, model_predictions: Dict[str, float]) -> str:
        """Tahmin konsensüsünü değerlendir"""
        try:
            if not model_predictions:
                return "No consensus"
            
            predictions = list(model_predictions.values())
            positive_count = len([p for p in predictions if p > 0])
            total_count = len(predictions)
            
            consensus_ratio = positive_count / total_count
            
            if consensus_ratio > 0.8:
                return "Strong bullish consensus"
            elif consensus_ratio > 0.6:
                return "Moderate bullish consensus"
            elif consensus_ratio < 0.2:
                return "Strong bearish consensus"
            elif consensus_ratio < 0.4:
                return "Moderate bearish consensus"
            else:
                return "Mixed consensus"
                
        except Exception as e:
            return "No consensus"
    
    def generate_feature_importance_explanation(self, feature_importance: Dict[str, float]) -> Dict[str, Any]:
        """Feature importance açıklaması"""
        try:
            if not feature_importance:
                return {}
            
            # En önemli feature'ları sırala
            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
            
            explanations = []
            for feature, importance in sorted_features[:5]:  # Top 5
                if importance > 0.1:
                    explanations.append({
                        'feature': feature,
                        'importance': importance,
                        'description': self._get_feature_description(feature, importance)
                    })
            
            return {
                'top_features': explanations,
                'total_features': len(feature_importance),
                'feature_diversity': len([f for f in feature_importance.values() if f > 0.05])
            }
            
        except Exception as e:
            log_error(f"Feature importance açıklaması hatası: {e}")
            return {}
    
    def _get_feature_description(self, feature: str, importance: float) -> str:
        """Feature açıklaması"""
        feature_descriptions = {
            'rsi': 'RSI göstergesi - aşırı alım/satım sinyalleri',
            'macd': 'MACD göstergesi - momentum değişimleri',
            'sma_20': '20 günlük hareketli ortalama - kısa vadeli trend',
            'sma_50': '50 günlük hareketli ortalama - orta vadeli trend',
            'volume': 'İşlem hacmi - piyasa ilgisi',
            'volatility': 'Volatilite - fiyat dalgalanması',
            'sentiment': 'Market sentimenti - sosyal medya ve haberler',
            'astrology': 'Astrolojik döngüler - gezegen etkileri',
            'cycles': 'Döngüsel analiz - zaman bazlı döngüler'
        }
        
        base_description = feature_descriptions.get(feature, f'{feature} göstergesi')
        
        if importance > 0.3:
            return f"{base_description} - Çok yüksek etki"
        elif importance > 0.2:
            return f"{base_description} - Yüksek etki"
        elif importance > 0.1:
            return f"{base_description} - Orta etki"
        else:
            return f"{base_description} - Düşük etki"

# Global explainable AI instance
explainable_ai = ExplainableAI()

