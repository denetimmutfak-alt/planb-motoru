"""
PlanB Motoru - Reddit API Integration
Reddit post analizi ve sentiment
"""
import os
import json
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug

class RedditAPI:
    """Reddit API entegrasyonu (PRAW kullanmadan)"""
    
    def __init__(self):
        self.base_url = "https://www.reddit.com"
        self.oauth_url = "https://oauth.reddit.com"
        self.client_id = self._get_client_id()
        self.client_secret = self._get_client_secret()
        self.user_agent = "PlanB_Motoru/1.0"
        self.access_token = None
        self.token_expires = 0
        
    def _get_client_id(self) -> Optional[str]:
        """Reddit Client ID al"""
        try:
            # Environment variable'dan al
            client_id = os.getenv('REDDIT_CLIENT_ID')
            if client_id:
                return client_id
            
            # Config dosyasından al
            try:
                from config.api_keys import get_reddit_client_id
                client_id = get_reddit_client_id()
                if client_id:
                    return client_id
            except ImportError:
                pass
            
            log_error("Reddit Client ID bulunamadı")
            return None
            
        except Exception as e:
            log_error(f"Reddit Client ID alınırken hata: {e}")
            return None
    
    def _get_client_secret(self) -> Optional[str]:
        """Reddit Client Secret al"""
        try:
            # Environment variable'dan al
            client_secret = os.getenv('REDDIT_CLIENT_SECRET')
            if client_secret:
                return client_secret
            
            # Config dosyasından al
            try:
                from config.api_keys import get_reddit_client_secret
                client_secret = get_reddit_client_secret()
                if client_secret:
                    return client_secret
            except ImportError:
                pass
            
            log_error("Reddit Client Secret bulunamadı")
            return None
            
        except Exception as e:
            log_error(f"Reddit Client Secret alınırken hata: {e}")
            return None
    
    def _get_access_token(self) -> bool:
        """Reddit OAuth access token al"""
        try:
            if not self.client_id or not self.client_secret:
                log_error("Reddit API credentials eksik")
                return False
            
            # Token hala geçerli mi kontrol et
            if self.access_token and time.time() < self.token_expires:
                return True
            
            # Yeni token al
            auth_url = "https://www.reddit.com/api/v1/access_token"
            auth_data = {
                'grant_type': 'client_credentials'
            }
            
            auth = (self.client_id, self.client_secret)
            headers = {
                'User-Agent': self.user_agent
            }
            
            response = requests.post(auth_url, data=auth_data, auth=auth, headers=headers)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                self.token_expires = time.time() + token_data['expires_in'] - 60  # 1 dakika erken yenile
                
                log_info("Reddit access token alındı")
                return True
            else:
                log_error(f"Reddit token alınamadı: {response.status_code}")
                return False
                
        except Exception as e:
            log_error(f"Reddit token alma hatası: {e}")
            return False
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Reddit API'ye istek gönder"""
        try:
            # Public API kullan (OAuth gerekmez)
            url = f"{self.base_url}{endpoint}"
            headers = {
                'User-Agent': self.user_agent
            }
            
            response = requests.get(url, headers=headers, params=params or {})
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                log_error("Reddit API rate limit aşıldı")
                time.sleep(60)  # 1 dakika bekle
                return None
            else:
                log_error(f"Reddit API hatası: {response.status_code}")
                return None
                
        except Exception as e:
            log_error(f"Reddit API isteği hatası: {e}")
            return None
    
    def search_posts(self, query: str, subreddit: str = None, limit: int = 100, 
                    sort: str = 'relevance', time_filter: str = 'week') -> List[Dict[str, Any]]:
        """Reddit'te post ara"""
        try:
            endpoint = "/search.json"
            params = {
                'q': query,
                'limit': min(limit, 100),
                'sort': sort,
                't': time_filter
            }
            
            if subreddit:
                endpoint = f"/r/{subreddit}/search.json"
            
            response = self._make_request(endpoint, params)
            if response and 'data' in response and 'children' in response['data']:
                posts = [post['data'] for post in response['data']['children']]
                log_info(f"Reddit'te '{query}' için {len(posts)} post bulundu")
                return posts
            
            return []
            
        except Exception as e:
            log_error(f"Reddit post arama hatası: {e}")
            return []
    
    def get_subreddit_posts(self, subreddit: str, limit: int = 100, 
                           sort: str = 'hot', time_filter: str = 'day') -> List[Dict[str, Any]]:
        """Subreddit'ten post al"""
        try:
            endpoint = f"/r/{subreddit}/{sort}.json"
            params = {
                'limit': min(limit, 100),
                't': time_filter
            }
            
            response = self._make_request(endpoint, params)
            if response and 'data' in response and 'children' in response['data']:
                posts = [post['data'] for post in response['data']['children']]
                log_info(f"r/{subreddit}'den {len(posts)} post alındı")
                return posts
            
            return []
            
        except Exception as e:
            log_error(f"Subreddit post alma hatası: {e}")
            return []
    
    def get_financial_posts(self, symbol: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Finansal subreddit'lerden post al"""
        try:
            financial_subreddits = [
                'investing', 'stocks', 'SecurityAnalysis', 'ValueInvesting',
                'StockMarket', 'dividends', 'options', 'wallstreetbets'
            ]
            
            all_posts = []
            
            if symbol:
                # Belirli sembol için arama
                for subreddit in financial_subreddits:
                    posts = self.search_posts(f"${symbol} OR {symbol}", subreddit, limit=25)
                    all_posts.extend(posts)
                    time.sleep(1)  # Rate limit için bekle
            else:
                # Genel finansal postlar
                for subreddit in financial_subreddits:
                    posts = self.get_subreddit_posts(subreddit, limit=25)
                    all_posts.extend(posts)
                    time.sleep(1)  # Rate limit için bekle
            
            # Duplicate postları kaldır
            unique_posts = []
            seen_ids = set()
            for post in all_posts:
                if post['id'] not in seen_ids:
                    unique_posts.append(post)
                    seen_ids.add(post['id'])
            
            log_info(f"Finansal postlar toplandı: {len(unique_posts)}")
            return unique_posts
            
        except Exception as e:
            log_error(f"Finansal postlar alınırken hata: {e}")
            return []
    
    def get_crypto_posts(self, symbol: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Kripto subreddit'lerden post al"""
        try:
            crypto_subreddits = [
                'cryptocurrency', 'Bitcoin', 'ethereum', 'CryptoCurrency',
                'CryptoMoonShots', 'altcoin', 'defi', 'NFT'
            ]
            
            all_posts = []
            
            if symbol:
                # Belirli kripto para için arama
                for subreddit in crypto_subreddits:
                    posts = self.search_posts(f"{symbol} OR {symbol.lower()}", subreddit, limit=25)
                    all_posts.extend(posts)
                    time.sleep(1)  # Rate limit için bekle
            else:
                # Genel kripto postlar
                for subreddit in crypto_subreddits:
                    posts = self.get_subreddit_posts(subreddit, limit=25)
                    all_posts.extend(posts)
                    time.sleep(1)  # Rate limit için bekle
            
            # Duplicate postları kaldır
            unique_posts = []
            seen_ids = set()
            for post in all_posts:
                if post['id'] not in seen_ids:
                    unique_posts.append(post)
                    seen_ids.add(post['id'])
            
            log_info(f"Kripto postlar toplandı: {len(unique_posts)}")
            return unique_posts
            
        except Exception as e:
            log_error(f"Kripto postlar alınırken hata: {e}")
            return []
    
    def analyze_post_sentiment(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Post sentiment analizi"""
        try:
            if not posts:
                return {
                    'total_posts': 0,
                    'sentiment_score': 50.0,
                    'sentiment': 'neutral',
                    'confidence': 0.0,
                    'positive_posts': 0,
                    'negative_posts': 0,
                    'neutral_posts': 0
                }
            
            positive_keywords = [
                'bullish', 'moon', 'rocket', 'buy', 'long', 'up', 'rise', 'gain', 'profit',
                'strong', 'excellent', 'amazing', 'fantastic', 'breakthrough', 'success',
                'hodl', 'diamond hands', 'to the moon', 'pump', 'bull run'
            ]
            
            negative_keywords = [
                'bearish', 'crash', 'dump', 'sell', 'short', 'down', 'fall', 'loss', 'drop',
                'weak', 'terrible', 'awful', 'disaster', 'scam', 'rug pull', 'bear market',
                'paper hands', 'fud', 'panic sell', 'correction'
            ]
            
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            
            for post in posts:
                title = post.get('title', '').lower()
                selftext = post.get('selftext', '').lower()
                content = f"{title} {selftext}"
                
                positive_score = sum(1 for keyword in positive_keywords if keyword in content)
                negative_score = sum(1 for keyword in negative_keywords if keyword in content)
                
                if positive_score > negative_score:
                    positive_count += 1
                elif negative_score > positive_score:
                    negative_count += 1
                else:
                    neutral_count += 1
            
            total_posts = len(posts)
            sentiment_score = ((positive_count * 100) + (neutral_count * 50)) / total_posts
            
            if sentiment_score > 60:
                sentiment = 'positive'
            elif sentiment_score < 40:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            confidence = abs(sentiment_score - 50) / 50
            
            result = {
                'total_posts': total_posts,
                'sentiment_score': round(sentiment_score, 2),
                'sentiment': sentiment,
                'confidence': round(confidence, 2),
                'positive_posts': positive_count,
                'negative_posts': negative_count,
                'neutral_posts': neutral_count,
                'sample_posts': posts[:5]  # İlk 5 post örneği
            }
            
            log_info(f"Reddit sentiment analizi: {sentiment} ({sentiment_score})")
            return result
            
        except Exception as e:
            log_error(f"Reddit sentiment analizi hatası: {e}")
            return {
                'total_posts': 0,
                'sentiment_score': 50.0,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_market_sentiment(self, market: str = 'general') -> Dict[str, Any]:
        """Piyasa sentiment analizi"""
        try:
            if market == 'crypto':
                posts = self.get_crypto_posts(limit=100)
            elif market == 'stocks':
                posts = self.get_financial_posts(limit=100)
            else:
                # Genel piyasa postları
                posts = self.get_financial_posts(limit=50)
                posts.extend(self.get_crypto_posts(limit=50))
            
            sentiment_analysis = self.analyze_post_sentiment(posts)
            
            return {
                'market': market,
                'posts': posts,
                'sentiment_analysis': sentiment_analysis,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            log_error(f"Piyasa sentiment analizi hatası: {e}")
            return {
                'market': market,
                'posts': [],
                'sentiment_analysis': {
                    'total_posts': 0,
                    'sentiment_score': 50.0,
                    'sentiment': 'neutral',
                    'confidence': 0.0
                },
                'error': str(e)
            }

# Global RedditAPI instance
reddit_api = RedditAPI()

