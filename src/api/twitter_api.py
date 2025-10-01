"""
PlanB Motoru - Twitter API Integration
Gerçek Twitter API entegrasyonu
"""
import os
import json
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug

class TwitterAPI:
    """Twitter API v2 entegrasyonu"""
    
    def __init__(self):
        self.base_url = "https://api.twitter.com/2"
        self.bearer_token = self._get_bearer_token()
        self.rate_limit_remaining = 300
        self.rate_limit_reset = 0
        
    def _get_bearer_token(self) -> Optional[str]:
        """Twitter Bearer Token'ı al"""
        try:
            # Environment variable'dan al
            token = os.getenv('TWITTER_BEARER_TOKEN')
            if token:
                return token
            
            # Config dosyasından al
            try:
                from config.api_keys import get_api_key
                token = get_api_key('TWITTER')
                if token:
                    return token
            except ImportError:
                pass
            
            log_error("Twitter Bearer Token bulunamadı")
            return None
            
        except Exception as e:
            log_error(f"Twitter token alınırken hata: {e}")
            return None
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Twitter API'ye istek gönder"""
        try:
            if not self.bearer_token:
                log_error("Twitter Bearer Token yok")
                return None
            
            # Rate limit kontrolü
            if self.rate_limit_remaining <= 0:
                wait_time = self.rate_limit_reset - int(time.time())
                if wait_time > 0:
                    log_info(f"Twitter API rate limit - {wait_time} saniye bekleniyor")
                    time.sleep(wait_time)
            
            headers = {
                'Authorization': f'Bearer {self.bearer_token}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=headers, params=params or {})
            
            # Rate limit bilgilerini güncelle
            if 'x-rate-limit-remaining' in response.headers:
                self.rate_limit_remaining = int(response.headers['x-rate-limit-remaining'])
            if 'x-rate-limit-reset' in response.headers:
                self.rate_limit_reset = int(response.headers['x-rate-limit-reset'])
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                log_error("Twitter API rate limit aşıldı")
                return None
            else:
                log_error(f"Twitter API hatası: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            log_error(f"Twitter API isteği hatası: {e}")
            return None
    
    def search_tweets(self, query: str, max_results: int = 100, 
                     start_time: str = None, end_time: str = None) -> List[Dict[str, Any]]:
        """Tweet arama"""
        try:
            params = {
                'query': query,
                'max_results': min(max_results, 100),
                'tweet.fields': 'created_at,public_metrics,context_annotations,lang',
                'user.fields': 'username,verified,public_metrics',
                'expansions': 'author_id'
            }
            
            if start_time:
                params['start_time'] = start_time
            if end_time:
                params['end_time'] = end_time
            
            response = self._make_request('tweets/search/recent', params)
            if response and 'data' in response:
                tweets = response['data']
                
                # User bilgilerini ekle
                if 'includes' in response and 'users' in response['includes']:
                    users = {user['id']: user for user in response['includes']['users']}
                    for tweet in tweets:
                        if tweet['author_id'] in users:
                            tweet['author'] = users[tweet['author_id']]
                
                log_info(f"Twitter'da {len(tweets)} tweet bulundu: {query}")
                return tweets
            
            return []
            
        except Exception as e:
            log_error(f"Tweet arama hatası: {e}")
            return []
    
    def get_trending_topics(self, woeid: int = 1) -> List[Dict[str, Any]]:
        """Trending konuları al (Twitter API v1.1 gerekli)"""
        try:
            # Bu özellik için Twitter API v1.1 gerekli
            # Şimdilik mock data döndürüyoruz
            trending_topics = [
                {"name": "#Bitcoin", "tweet_volume": 50000},
                {"name": "#Tesla", "tweet_volume": 30000},
                {"name": "#Apple", "tweet_volume": 25000},
                {"name": "#BIST", "tweet_volume": 15000},
                {"name": "#Gold", "tweet_volume": 12000}
            ]
            
            log_info(f"Trending konular alındı: {len(trending_topics)} konu")
            return trending_topics
            
        except Exception as e:
            log_error(f"Trending konular alınırken hata: {e}")
            return []
    
    def get_user_tweets(self, username: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Belirli kullanıcının tweetlerini al"""
        try:
            # Önce kullanıcı ID'sini al
            user_response = self._make_request(f'users/by/username/{username}')
            if not user_response or 'data' not in user_response:
                log_error(f"Kullanıcı bulunamadı: {username}")
                return []
            
            user_id = user_response['data']['id']
            
            # Kullanıcının tweetlerini al
            params = {
                'max_results': min(max_results, 100),
                'tweet.fields': 'created_at,public_metrics,context_annotations,lang'
            }
            
            response = self._make_request(f'users/{user_id}/tweets', params)
            if response and 'data' in response:
                tweets = response['data']
                log_info(f"{username} kullanıcısından {len(tweets)} tweet alındı")
                return tweets
            
            return []
            
        except Exception as e:
            log_error(f"Kullanıcı tweetleri alınırken hata: {e}")
            return []
    
    def analyze_sentiment_tweets(self, symbol: str, max_results: int = 100) -> Dict[str, Any]:
        """Belirli sembol için tweet sentiment analizi"""
        try:
            # Sembol için tweet ara
            query = f"${symbol} OR #{symbol} lang:en"
            tweets = self.search_tweets(query, max_results)
            
            if not tweets:
                return {
                    'symbol': symbol,
                    'total_tweets': 0,
                    'sentiment_score': 50.0,
                    'sentiment': 'neutral',
                    'confidence': 0.0,
                    'positive_tweets': 0,
                    'negative_tweets': 0,
                    'neutral_tweets': 0
                }
            
            # Basit sentiment analizi
            positive_keywords = ['bull', 'bullish', 'moon', 'rocket', 'buy', 'long', 'up', 'rise', 'gain', 'profit']
            negative_keywords = ['bear', 'bearish', 'crash', 'dump', 'sell', 'short', 'down', 'fall', 'loss', 'drop']
            
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            
            for tweet in tweets:
                text = tweet.get('text', '').lower()
                
                positive_score = sum(1 for keyword in positive_keywords if keyword in text)
                negative_score = sum(1 for keyword in negative_keywords if keyword in text)
                
                if positive_score > negative_score:
                    positive_count += 1
                elif negative_score > positive_score:
                    negative_count += 1
                else:
                    neutral_count += 1
            
            total_tweets = len(tweets)
            sentiment_score = ((positive_count * 100) + (neutral_count * 50)) / total_tweets
            
            if sentiment_score > 60:
                sentiment = 'positive'
            elif sentiment_score < 40:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            confidence = abs(sentiment_score - 50) / 50
            
            result = {
                'symbol': symbol,
                'total_tweets': total_tweets,
                'sentiment_score': round(sentiment_score, 2),
                'sentiment': sentiment,
                'confidence': round(confidence, 2),
                'positive_tweets': positive_count,
                'negative_tweets': negative_count,
                'neutral_tweets': neutral_count,
                'sample_tweets': tweets[:5]  # İlk 5 tweet örneği
            }
            
            log_info(f"Twitter sentiment analizi: {symbol} - {sentiment} ({sentiment_score})")
            return result
            
        except Exception as e:
            log_error(f"Twitter sentiment analizi hatası: {e}")
            return {
                'symbol': symbol,
                'total_tweets': 0,
                'sentiment_score': 50.0,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_crypto_sentiment(self, symbol: str = "BTC") -> Dict[str, Any]:
        """Kripto para sentiment analizi"""
        try:
            # Kripto için özel arama terimleri
            crypto_queries = [
                f"${symbol}",
                f"#{symbol}",
                f"{symbol} price",
                f"{symbol} crypto"
            ]
            
            all_tweets = []
            for query in crypto_queries:
                tweets = self.search_tweets(query, max_results=25)
                all_tweets.extend(tweets)
                time.sleep(1)  # Rate limit için bekle
            
            # Duplicate tweetleri kaldır
            unique_tweets = []
            seen_ids = set()
            for tweet in all_tweets:
                if tweet['id'] not in seen_ids:
                    unique_tweets.append(tweet)
                    seen_ids.add(tweet['id'])
            
            return self.analyze_sentiment_tweets(symbol, len(unique_tweets))
            
        except Exception as e:
            log_error(f"Kripto sentiment analizi hatası: {e}")
            return {
                'symbol': symbol,
                'total_tweets': 0,
                'sentiment_score': 50.0,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_stock_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Hisse senedi sentiment analizi"""
        try:
            # Hisse senedi için özel arama terimleri
            stock_queries = [
                f"${symbol}",
                f"#{symbol}",
                f"{symbol} stock",
                f"{symbol} shares"
            ]
            
            all_tweets = []
            for query in stock_queries:
                tweets = self.search_tweets(query, max_results=25)
                all_tweets.extend(tweets)
                time.sleep(1)  # Rate limit için bekle
            
            # Duplicate tweetleri kaldır
            unique_tweets = []
            seen_ids = set()
            for tweet in all_tweets:
                if tweet['id'] not in seen_ids:
                    unique_tweets.append(tweet)
                    seen_ids.add(tweet['id'])
            
            return self.analyze_sentiment_tweets(symbol, len(unique_tweets))
            
        except Exception as e:
            log_error(f"Hisse senedi sentiment analizi hatası: {e}")
            return {
                'symbol': symbol,
                'total_tweets': 0,
                'sentiment_score': 50.0,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Rate limit durumunu kontrol et"""
        return {
            'remaining': self.rate_limit_remaining,
            'reset_time': self.rate_limit_reset,
            'reset_datetime': datetime.fromtimestamp(self.rate_limit_reset).isoformat() if self.rate_limit_reset else None
        }

# Global Twitter API instance
twitter_api = TwitterAPI()

