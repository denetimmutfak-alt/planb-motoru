"""
PlanB Motoru - Personal Data Lake
Kişisel veri gölü ve AI öğrenme sistemi
"""
import json
import os
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug
from src.security.encryption_manager import encryption_manager

class PersonalDataLake:
    """Kişisel veri gölü ve AI öğrenme sistemi"""
    
    def __init__(self):
        self.data_directory = "data/personal_data_lake"
        
        # Veri kategorileri
        self.data_categories = {
            'portfolio_history': 'portfolios',
            'analysis_history': 'analyses',
            'trade_history': 'trades',
            'alert_history': 'alerts',
            'market_data': 'market',
            'sentiment_data': 'sentiment',
            'macro_data': 'macro',
            'user_behavior': 'behavior',
            'ai_insights': 'insights'
        }
        
        self._ensure_directories()
        
        # AI öğrenme modelleri
        self.learning_models = {
            'user_preferences': {},
            'trading_patterns': {},
            'risk_tolerance': {},
            'market_timing': {},
            'sector_preferences': {}
        }
        
        # Veri kalitesi metrikleri
        self.data_quality_metrics = {}
    
    def _ensure_directories(self):
        """Gerekli dizinleri oluştur"""
        os.makedirs(self.data_directory, exist_ok=True)
        for category in self.data_categories.values():
            os.makedirs(f"{self.data_directory}/{category}", exist_ok=True)
    
    def store_portfolio_data(self, portfolio_data: Dict[str, Any]) -> bool:
        """Portföy verilerini sakla"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.data_directory}/portfolios/portfolio_{timestamp}.json"
            
            # Veriyi şifrele
            encrypted_data = self._encrypt_data(portfolio_data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(encrypted_data, f, indent=2, ensure_ascii=False)
            
            # AI öğrenme için veriyi işle
            self._process_portfolio_for_learning(portfolio_data)
            
            log_info(f"Portföy verisi saklandı: {filename}")
            return True
            
        except Exception as e:
            log_error(f"Portföy verisi saklama hatası: {e}")
            return False
    
    def store_analysis_data(self, symbol: str, analysis_data: Dict[str, Any]) -> bool:
        """Analiz verilerini sakla"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.data_directory}/analyses/{symbol}_{timestamp}.json"
            
            # Veriyi zenginleştir
            enriched_data = {
                'symbol': symbol,
                'analysis_data': analysis_data,
                'timestamp': timestamp,
                'market_conditions': self._get_market_conditions(),
                'user_context': self._get_user_context()
            }
            
            # Veriyi şifrele
            encrypted_data = self._encrypt_data(enriched_data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(encrypted_data, f, indent=2, ensure_ascii=False)
            
            # AI öğrenme için veriyi işle
            self._process_analysis_for_learning(symbol, analysis_data)
            
            log_info(f"Analiz verisi saklandı: {filename}")
            return True
            
        except Exception as e:
            log_error(f"Analiz verisi saklama hatası: {e}")
            return False
    
    def store_trade_data(self, trade_data: Dict[str, Any]) -> bool:
        """İşlem verilerini sakla"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.data_directory}/trades/trade_{timestamp}.json"
            
            # Veriyi zenginleştir
            enriched_data = {
                'trade_data': trade_data,
                'timestamp': timestamp,
                'market_conditions': self._get_market_conditions(),
                'analysis_context': self._get_analysis_context(trade_data.get('symbol', ''))
            }
            
            # Veriyi şifrele
            encrypted_data = self._encrypt_data(enriched_data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(encrypted_data, f, indent=2, ensure_ascii=False)
            
            # AI öğrenme için veriyi işle
            self._process_trade_for_learning(trade_data)
            
            log_info(f"İşlem verisi saklandı: {filename}")
            return True
            
        except Exception as e:
            log_error(f"İşlem verisi saklama hatası: {e}")
            return False
    
    def store_user_behavior(self, behavior_data: Dict[str, Any]) -> bool:
        """Kullanıcı davranış verilerini sakla"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.data_directory}/behavior/behavior_{timestamp}.json"
            
            # Veriyi zenginleştir
            enriched_data = {
                'behavior_data': behavior_data,
                'timestamp': timestamp,
                'session_context': self._get_session_context()
            }
            
            # Veriyi şifrele
            encrypted_data = self._encrypt_data(enriched_data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(encrypted_data, f, indent=2, ensure_ascii=False)
            
            # AI öğrenme için veriyi işle
            self._process_behavior_for_learning(behavior_data)
            
            log_info(f"Kullanıcı davranış verisi saklandı: {filename}")
            return True
            
        except Exception as e:
            log_error(f"Kullanıcı davranış verisi saklama hatası: {e}")
            return False
    
    def generate_ai_insights(self) -> Dict[str, Any]:
        """AI öngörüleri oluştur"""
        try:
            insights = {
                'generated_at': datetime.now().isoformat(),
                'user_preferences': self._analyze_user_preferences(),
                'trading_patterns': self._analyze_trading_patterns(),
                'risk_profile': self._analyze_risk_profile(),
                'market_timing': self._analyze_market_timing(),
                'sector_insights': self._analyze_sector_preferences(),
                'recommendations': self._generate_personalized_recommendations(),
                'predictions': self._generate_predictions()
            }
            
            # Öngörüleri sakla
            self._store_ai_insights(insights)
            
            log_info("AI öngörüleri oluşturuldu")
            return insights
            
        except Exception as e:
            log_error(f"AI öngörü oluşturma hatası: {e}")
            return {}
    
    def get_personalized_analysis(self, symbol: str) -> Dict[str, Any]:
        """Kişiselleştirilmiş analiz oluştur"""
        try:
            # Kullanıcı geçmişini analiz et
            user_history = self._get_user_history_for_symbol(symbol)
            
            # Kişiselleştirilmiş analiz
            personalized_analysis = {
                'symbol': symbol,
                'user_specific_insights': self._get_user_specific_insights(symbol, user_history),
                'historical_performance': self._get_historical_performance(symbol, user_history),
                'risk_assessment': self._get_personalized_risk_assessment(symbol, user_history),
                'recommendations': self._get_personalized_recommendations(symbol, user_history),
                'confidence_score': self._calculate_confidence_score(symbol, user_history)
            }
            
            return personalized_analysis
            
        except Exception as e:
            log_error(f"Kişiselleştirilmiş analiz oluşturma hatası: {e}")
            return {}
    
    def learn_from_feedback(self, feedback_data: Dict[str, Any]) -> bool:
        """Kullanıcı geri bildiriminden öğren"""
        try:
            # Geri bildirim verilerini işle
            learning_data = {
                'feedback': feedback_data,
                'timestamp': datetime.now().isoformat(),
                'context': self._get_feedback_context(feedback_data)
            }
            
            # AI modellerini güncelle
            self._update_learning_models(learning_data)
            
            # Öğrenme verilerini sakla
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.data_directory}/learning/feedback_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(learning_data, f, indent=2, ensure_ascii=False)
            
            log_info("Geri bildirimden öğrenme tamamlandı")
            return True
            
        except Exception as e:
            log_error(f"Geri bildirim öğrenme hatası: {e}")
            return False
    
    def _process_portfolio_for_learning(self, portfolio_data: Dict[str, Any]):
        """Portföy verilerini AI öğrenme için işle"""
        try:
            # Portföy performansını analiz et
            performance_metrics = self._calculate_portfolio_performance_metrics(portfolio_data)
            
            # Kullanıcı tercihlerini güncelle
            self._update_user_preferences_from_portfolio(portfolio_data, performance_metrics)
            
            # Risk toleransını güncelle
            self._update_risk_tolerance_from_portfolio(portfolio_data, performance_metrics)
            
        except Exception as e:
            log_error(f"Portföy öğrenme işleme hatası: {e}")
    
    def _process_analysis_for_learning(self, symbol: str, analysis_data: Dict[str, Any]):
        """Analiz verilerini AI öğrenme için işle"""
        try:
            # Analiz doğruluğunu takip et
            analysis_accuracy = self._calculate_analysis_accuracy(symbol, analysis_data)
            
            # Sektör tercihlerini güncelle
            self._update_sector_preferences_from_analysis(symbol, analysis_data, analysis_accuracy)
            
            # Piyasa zamanlamasını güncelle
            self._update_market_timing_from_analysis(symbol, analysis_data, analysis_accuracy)
            
        except Exception as e:
            log_error(f"Analiz öğrenme işleme hatası: {e}")
    
    def _process_trade_for_learning(self, trade_data: Dict[str, Any]):
        """İşlem verilerini AI öğrenme için işle"""
        try:
            # İşlem performansını analiz et
            trade_performance = self._calculate_trade_performance(trade_data)
            
            # İşlem kalıplarını güncelle
            self._update_trading_patterns_from_trade(trade_data, trade_performance)
            
            # Risk yönetimini güncelle
            self._update_risk_management_from_trade(trade_data, trade_performance)
            
        except Exception as e:
            log_error(f"İşlem öğrenme işleme hatası: {e}")
    
    def _process_behavior_for_learning(self, behavior_data: Dict[str, Any]):
        """Davranış verilerini AI öğrenme için işle"""
        try:
            # Kullanıcı davranış kalıplarını analiz et
            behavior_patterns = self._analyze_behavior_patterns(behavior_data)
            
            # Kullanıcı tercihlerini güncelle
            self._update_user_preferences_from_behavior(behavior_data, behavior_patterns)
            
        except Exception as e:
            log_error(f"Davranış öğrenme işleme hatası: {e}")
    
    def _analyze_user_preferences(self) -> Dict[str, Any]:
        """Kullanıcı tercihlerini analiz et"""
        try:
            # Simüle edilmiş kullanıcı tercih analizi
            preferences = {
                'preferred_sectors': ['technology', 'finance', 'healthcare'],
                'preferred_markets': ['bist', 'nasdaq'],
                'preferred_timeframes': ['1d', '1w'],
                'risk_tolerance': 'medium',
                'analysis_depth': 'comprehensive',
                'notification_preferences': ['email', 'dashboard'],
                'confidence_threshold': 0.7
            }
            
            return preferences
            
        except Exception as e:
            return {}
    
    def _analyze_trading_patterns(self) -> Dict[str, Any]:
        """İşlem kalıplarını analiz et"""
        try:
            # Simüle edilmiş işlem kalıp analizi
            patterns = {
                'average_holding_period': 15,  # gün
                'preferred_entry_times': ['09:30', '14:00'],
                'preferred_exit_times': ['15:30', '16:00'],
                'position_sizing_pattern': 'conservative',
                'stop_loss_usage': 0.8,  # %80
                'take_profit_usage': 0.6,  # %60
                'diversification_level': 'high'
            }
            
            return patterns
            
        except Exception as e:
            return {}
    
    def _analyze_risk_profile(self) -> Dict[str, Any]:
        """Risk profili analiz et"""
        try:
            # Simüle edilmiş risk profil analizi
            risk_profile = {
                'risk_tolerance': 'medium',
                'max_drawdown_tolerance': 15,  # %
                'volatility_tolerance': 20,  # %
                'correlation_tolerance': 0.7,
                'concentration_risk_tolerance': 0.3,
                'liquidity_preference': 'high',
                'time_horizon': 'medium_term'
            }
            
            return risk_profile
            
        except Exception as e:
            return {}
    
    def _analyze_market_timing(self) -> Dict[str, Any]:
        """Piyasa zamanlamasını analiz et"""
        try:
            # Simüle edilmiş piyasa zamanlama analizi
            market_timing = {
                'best_performing_hours': ['09:30-11:00', '14:00-15:30'],
                'best_performing_days': ['Tuesday', 'Wednesday', 'Thursday'],
                'seasonal_patterns': {
                    'Q1': 'positive',
                    'Q2': 'neutral',
                    'Q3': 'negative',
                    'Q4': 'positive'
                },
                'volatility_preference': 'moderate',
                'trend_following_tendency': 0.7
            }
            
            return market_timing
            
        except Exception as e:
            return {}
    
    def _analyze_sector_preferences(self) -> Dict[str, Any]:
        """Sektör tercihlerini analiz et"""
        try:
            # Simüle edilmiş sektör tercih analizi
            sector_preferences = {
                'top_performing_sectors': ['technology', 'healthcare', 'finance'],
                'underperforming_sectors': ['energy', 'utilities'],
                'sector_rotation_pattern': 'quarterly',
                'diversification_preference': 'high',
                'growth_vs_value_preference': 'growth'
            }
            
            return sector_preferences
            
        except Exception as e:
            return {}
    
    def _generate_personalized_recommendations(self) -> List[Dict[str, Any]]:
        """Kişiselleştirilmiş öneriler oluştur"""
        try:
            recommendations = [
                {
                    'type': 'portfolio_optimization',
                    'title': 'Portföy Optimizasyonu',
                    'description': 'Teknoloji sektörü ağırlığınızı %15 artırmanız önerilir.',
                    'confidence': 0.8,
                    'expected_impact': 'positive'
                },
                {
                    'type': 'risk_management',
                    'title': 'Risk Yönetimi',
                    'description': 'Stop-loss seviyelerinizi %5 daraltmanız önerilir.',
                    'confidence': 0.7,
                    'expected_impact': 'protective'
                },
                {
                    'type': 'timing',
                    'title': 'Zamanlama',
                    'description': 'İşlemlerinizi 14:00-15:30 saatleri arasında yapmanız önerilir.',
                    'confidence': 0.6,
                    'expected_impact': 'neutral'
                }
            ]
            
            return recommendations
            
        except Exception as e:
            return []
    
    def _generate_predictions(self) -> Dict[str, Any]:
        """Öngörüler oluştur"""
        try:
            predictions = {
                'portfolio_performance': {
                    'next_month': 5.2,  # %
                    'next_quarter': 12.8,  # %
                    'next_year': 18.5  # %
                },
                'risk_forecast': {
                    'volatility': 18.5,  # %
                    'max_drawdown': 12.3,  # %
                    'sharpe_ratio': 1.2
                },
                'sector_rotation': {
                    'outperforming_sectors': ['technology', 'healthcare'],
                    'underperforming_sectors': ['energy', 'utilities'],
                    'rotation_probability': 0.7
                }
            }
            
            return predictions
            
        except Exception as e:
            return {}
    
    def _encrypt_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Veriyi şifrele"""
        try:
            # Hassas verileri şifrele
            encrypted_data = data.copy()
            
            # Portföy değerlerini şifrele
            if 'portfolio_data' in encrypted_data:
                portfolio_data = encrypted_data['portfolio_data']
                if 'cash' in portfolio_data:
                    portfolio_data['cash'] = encryption_manager.encrypt(str(portfolio_data['cash']))
            
            return encrypted_data
            
        except Exception as e:
            log_error(f"Veri şifreleme hatası: {e}")
            return data
    
    def _get_market_conditions(self) -> Dict[str, Any]:
        """Piyasa koşullarını getir"""
        try:
            # Simüle edilmiş piyasa koşulları
            return {
                'market_sentiment': 'neutral',
                'volatility_level': 'moderate',
                'trend_direction': 'sideways',
                'volume_level': 'average'
            }
        except Exception as e:
            return {}
    
    def _get_user_context(self) -> Dict[str, Any]:
        """Kullanıcı bağlamını getir"""
        try:
            # Simüle edilmiş kullanıcı bağlamı
            return {
                'user_id': 'default_user',
                'session_id': 'session_123',
                'device_type': 'desktop',
                'location': 'Turkey'
            }
        except Exception as e:
            return {}
    
    def _get_session_context(self) -> Dict[str, Any]:
        """Oturum bağlamını getir"""
        try:
            # Simüle edilmiş oturum bağlamı
            return {
                'session_duration': 45,  # dakika
                'pages_visited': 12,
                'actions_performed': 25,
                'time_of_day': datetime.now().hour
            }
        except Exception as e:
            return {}
    
    def _store_ai_insights(self, insights: Dict[str, Any]):
        """AI öngörülerini sakla"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.data_directory}/insights/insights_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(insights, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            log_error(f"AI öngörü saklama hatası: {e}")
    
    def get_data_quality_report(self) -> Dict[str, Any]:
        """Veri kalitesi raporu oluştur"""
        try:
            report = {
                'generated_at': datetime.now().isoformat(),
                'total_data_points': self._count_total_data_points(),
                'data_freshness': self._calculate_data_freshness(),
                'data_completeness': self._calculate_data_completeness(),
                'data_accuracy': self._calculate_data_accuracy(),
                'recommendations': self._generate_data_quality_recommendations()
            }
            
            return report
            
        except Exception as e:
            log_error(f"Veri kalitesi raporu oluşturma hatası: {e}")
            return {}
    
    def _count_total_data_points(self) -> int:
        """Toplam veri noktası sayısını hesapla"""
        try:
            total_count = 0
            for category in self.data_categories.values():
                category_path = f"{self.data_directory}/{category}"
                if os.path.exists(category_path):
                    total_count += len([f for f in os.listdir(category_path) if f.endswith('.json')])
            return total_count
        except Exception as e:
            return 0
    
    def _calculate_data_freshness(self) -> float:
        """Veri tazeliğini hesapla"""
        try:
            # Simüle edilmiş veri tazeliği
            return 0.85  # %85 taze
        except Exception as e:
            return 0.0
    
    def _calculate_data_completeness(self) -> float:
        """Veri bütünlüğünü hesapla"""
        try:
            # Simüle edilmiş veri bütünlüğü
            return 0.92  # %92 bütün
        except Exception as e:
            return 0.0
    
    def _calculate_data_accuracy(self) -> float:
        """Veri doğruluğunu hesapla"""
        try:
            # Simüle edilmiş veri doğruluğu
            return 0.88  # %88 doğru
        except Exception as e:
            return 0.0
    
    def _generate_data_quality_recommendations(self) -> List[str]:
        """Veri kalitesi önerileri oluştur"""
        try:
            recommendations = [
                "Veri girişi sırasında daha fazla doğrulama yapın",
                "Eksik veri noktalarını tamamlayın",
                "Eski verileri düzenli olarak güncelleyin",
                "Veri tutarlılığını kontrol edin"
            ]
            
            return recommendations
            
        except Exception as e:
            return []

# Global personal data lake instance
personal_data_lake = PersonalDataLake()

