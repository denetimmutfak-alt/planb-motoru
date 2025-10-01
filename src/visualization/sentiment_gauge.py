"""
PlanB Motoru - Sentiment Gauge
Anlık sentiment gauge göstergesi
"""
import numpy as np
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug

class SentimentGauge:
    """Anlık sentiment gauge göstergesi"""
    
    def __init__(self):
        self.sentiment_sources = ['twitter', 'news', 'reddit', 'social_media']
        self.gauge_levels = {
            'very_positive': {'min': 80, 'max': 100, 'color': '#00ff00', 'emoji': '🚀'},
            'positive': {'min': 60, 'max': 80, 'color': '#90ee90', 'emoji': '📈'},
            'neutral': {'min': 40, 'max': 60, 'color': '#ffff00', 'emoji': '➡️'},
            'negative': {'min': 20, 'max': 40, 'color': '#ffa500', 'emoji': '📉'},
            'very_negative': {'min': 0, 'max': 20, 'color': '#ff0000', 'emoji': '💥'}
        }
    
    def generate_sentiment_gauge(self, sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sentiment gauge oluştur"""
        try:
            # Genel sentiment skorunu hesapla
            overall_score = sentiment_data.get('overall_score', 50)
            confidence = sentiment_data.get('confidence', 0.5)
            
            # Gauge seviyesini belirle
            gauge_level = self._get_gauge_level(overall_score)
            
            # Kaynak bazlı sentiment
            source_sentiments = self._process_source_sentiments(sentiment_data)
            
            # Trend analizi
            trend_analysis = self._analyze_sentiment_trend(sentiment_data)
            
            # Gauge görselleştirme verileri
            gauge_data = {
                'overall_score': overall_score,
                'confidence': confidence,
                'gauge_level': gauge_level,
                'color': self.gauge_levels[gauge_level]['color'],
                'emoji': self.gauge_levels[gauge_level]['emoji'],
                'source_sentiments': source_sentiments,
                'trend_analysis': trend_analysis,
                'last_updated': datetime.now().isoformat(),
                'gauge_angle': self._calculate_gauge_angle(overall_score),
                'needle_position': self._calculate_needle_position(overall_score)
            }
            
            return gauge_data
            
        except Exception as e:
            log_error(f"Sentiment gauge oluşturma hatası: {e}")
            return {}
    
    def _get_gauge_level(self, score: float) -> str:
        """Gauge seviyesini belirle"""
        for level, config in self.gauge_levels.items():
            if config['min'] <= score <= config['max']:
                return level
        return 'neutral'
    
    def _process_source_sentiments(self, sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Kaynak bazlı sentiment işle"""
        try:
            source_sentiments = {}
            
            for source in self.sentiment_sources:
                if source in sentiment_data:
                    source_data = sentiment_data[source]
                    score = source_data.get('score', 50)
                    confidence = source_data.get('confidence', 0.5)
                    
                    source_sentiments[source] = {
                        'score': score,
                        'confidence': confidence,
                        'level': self._get_gauge_level(score),
                        'color': self.gauge_levels[self._get_gauge_level(score)]['color'],
                        'emoji': self.gauge_levels[self._get_gauge_level(score)]['emoji']
                    }
            
            return source_sentiments
            
        except Exception as e:
            log_error(f"Kaynak sentiment işleme hatası: {e}")
            return {}
    
    def _analyze_sentiment_trend(self, sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sentiment trend analizi"""
        try:
            current_score = sentiment_data.get('overall_score', 50)
            previous_score = sentiment_data.get('previous_score', current_score)
            
            # Trend yönü
            if current_score > previous_score + 5:
                trend_direction = 'improving'
                trend_strength = 'strong'
            elif current_score > previous_score + 2:
                trend_direction = 'improving'
                trend_strength = 'moderate'
            elif current_score < previous_score - 5:
                trend_direction = 'declining'
                trend_strength = 'strong'
            elif current_score < previous_score - 2:
                trend_direction = 'declining'
                trend_strength = 'moderate'
            else:
                trend_direction = 'stable'
                trend_strength = 'weak'
            
            # Momentum
            momentum = current_score - previous_score
            
            return {
                'trend_direction': trend_direction,
                'trend_strength': trend_strength,
                'momentum': momentum,
                'change_pct': ((current_score - previous_score) / previous_score * 100) if previous_score > 0 else 0
            }
            
        except Exception as e:
            log_error(f"Trend analizi hatası: {e}")
            return {'trend_direction': 'stable', 'trend_strength': 'weak', 'momentum': 0}
    
    def _calculate_gauge_angle(self, score: float) -> float:
        """Gauge açısını hesapla"""
        # 0-100 skorunu 0-180 dereceye çevir
        return (score / 100) * 180
    
    def _calculate_needle_position(self, score: float) -> Dict[str, float]:
        """İğne pozisyonunu hesapla"""
        angle = self._calculate_gauge_angle(score)
        # Dairesel gauge için x,y koordinatları
        import math
        radius = 100
        x = radius * math.cos(math.radians(angle - 90))
        y = radius * math.sin(math.radians(angle - 90))
        
        return {'x': x, 'y': y, 'angle': angle}
    
    def generate_multi_asset_gauge(self, assets_sentiment: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Çoklu varlık sentiment gauge"""
        try:
            multi_gauge_data = {}
            
            for asset, sentiment_data in assets_sentiment.items():
                gauge_data = self.generate_sentiment_gauge(sentiment_data)
                multi_gauge_data[asset] = gauge_data
            
            # Genel piyasa sentiment
            all_scores = [data.get('overall_score', 50) for data in multi_gauge_data.values()]
            market_sentiment = {
                'average_score': np.mean(all_scores),
                'median_score': np.median(all_scores),
                'std_score': np.std(all_scores),
                'positive_assets': len([s for s in all_scores if s > 60]),
                'negative_assets': len([s for s in all_scores if s < 40]),
                'total_assets': len(all_scores)
            }
            
            return {
                'assets': multi_gauge_data,
                'market_sentiment': market_sentiment,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            log_error(f"Çoklu varlık gauge hatası: {e}")
            return {}
    
    def generate_sector_sentiment_gauge(self, sector_sentiments: Dict[str, Any]) -> Dict[str, Any]:
        """Sektör sentiment gauge"""
        try:
            sector_gauges = {}
            
            for sector, sentiment_data in sector_sentiments.items():
                gauge_data = self.generate_sentiment_gauge(sentiment_data)
                sector_gauges[sector] = gauge_data
            
            # Sektör rotasyon analizi
            sector_scores = [(sector, data['overall_score']) for sector, data in sector_gauges.items()]
            sector_scores.sort(key=lambda x: x[1], reverse=True)
            
            rotation_analysis = {
                'top_sectors': sector_scores[:3],
                'bottom_sectors': sector_scores[-3:],
                'sector_dispersion': np.std([score for _, score in sector_scores]),
                'rotation_strength': 'strong' if np.std([score for _, score in sector_scores]) > 15 else 'moderate'
            }
            
            return {
                'sector_gauges': sector_gauges,
                'rotation_analysis': rotation_analysis,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            log_error(f"Sektör sentiment gauge hatası: {e}")
            return {}
    
    def generate_real_time_gauge(self, symbol: str, sentiment_stream: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Real-time sentiment gauge"""
        try:
            if not sentiment_stream:
                return {}
            
            # Son 10 sentiment verisi
            recent_sentiments = sentiment_stream[-10:]
            
            # Trend analizi
            scores = [s.get('score', 50) for s in recent_sentiments]
            timestamps = [s.get('timestamp', '') for s in recent_sentiments]
            
            # Hareketli ortalama
            if len(scores) >= 3:
                moving_avg = np.mean(scores[-3:])
            else:
                moving_avg = np.mean(scores) if scores else 50
            
            # Volatilite
            volatility = np.std(scores) if len(scores) > 1 else 0
            
            # Real-time gauge
            real_time_gauge = {
                'symbol': symbol,
                'current_score': scores[-1] if scores else 50,
                'moving_average': moving_avg,
                'volatility': volatility,
                'trend': 'up' if len(scores) > 1 and scores[-1] > scores[-2] else 'down',
                'data_points': len(scores),
                'last_update': timestamps[-1] if timestamps else datetime.now().isoformat(),
                'gauge_level': self._get_gauge_level(scores[-1] if scores else 50)
            }
            
            return real_time_gauge
            
        except Exception as e:
            log_error(f"Real-time gauge hatası: {e}")
            return {}

# Global sentiment gauge instance
sentiment_gauge = SentimentGauge()

