"""
PlanB Motoru - NewsAPI Integration
Canlı haber akışı ve sentiment analizi
"""
import os
import json
import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug

class NewsAPI:
    """NewsAPI entegrasyonu"""
    
    def __init__(self):
        self.base_url = "https://newsapi.org/v2"
        self.api_key = self._get_api_key()
        self.rate_limit_remaining = 1000
        self.rate_limit_reset = 0
        
    def _get_api_key(self) -> Optional[str]:
        """NewsAPI anahtarını al"""
        try:
            # Environment variable'dan al
            key = os.getenv('NEWS_API_KEY')
            if key:
                return key
            
            # Config dosyasından al
            try:
                from config.api_keys import get_api_key
                key = get_api_key('NEWSAPI')
                if key:
                    return key
            except ImportError:
                pass
            
            log_error("NewsAPI anahtarı bulunamadı")
            return None
            
        except Exception as e:
            log_error(f"NewsAPI anahtarı alınırken hata: {e}")
            return None
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """NewsAPI'ye istek gönder"""
        try:
            if not self.api_key:
                log_error("NewsAPI anahtarı yok")
                return None
            
            # Rate limit kontrolü
            if self.rate_limit_remaining <= 0:
                wait_time = self.rate_limit_reset - int(time.time())
                if wait_time > 0:
                    log_info(f"NewsAPI rate limit - {wait_time} saniye bekleniyor")
                    time.sleep(wait_time)
            
            headers = {
                'X-API-Key': self.api_key
            }
            
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=headers, params=params or {})
            
            # Rate limit bilgilerini güncelle
            if 'X-RateLimit-Remaining' in response.headers:
                self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
            if 'X-RateLimit-Reset' in response.headers:
                self.rate_limit_reset = int(response.headers['X-RateLimit-Reset'])
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                log_error("NewsAPI rate limit aşıldı")
                return None
            else:
                log_error(f"NewsAPI hatası: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            log_error(f"NewsAPI isteği hatası: {e}")
            return None
    
    def get_top_headlines(self, category: str = 'business', country: str = 'us', 
                         page_size: int = 100) -> List[Dict[str, Any]]:
        """En güncel haberleri al"""
        try:
            params = {
                'category': category,
                'country': country,
                'pageSize': min(page_size, 100),
                'sortBy': 'publishedAt'
            }
            
            response = self._make_request('top-headlines', params)
            if response and 'articles' in response:
                articles = response['articles']
                log_info(f"NewsAPI'den {len(articles)} haber alındı")
                return articles
            
            return []
            
        except Exception as e:
            log_error(f"Top headlines alınırken hata: {e}")
            return []
    
    def search_news(self, query: str, language: str = 'en', 
                   from_date: str = None, to_date: str = None,
                   page_size: int = 100) -> List[Dict[str, Any]]:
        """Haber ara"""
        try:
            params = {
                'q': query,
                'language': language,
                'pageSize': min(page_size, 100),
                'sortBy': 'publishedAt'
            }
            
            if from_date:
                params['from'] = from_date
            if to_date:
                params['to'] = to_date
            
            response = self._make_request('everything', params)
            if response and 'articles' in response:
                articles = response['articles']
                log_info(f"NewsAPI'de '{query}' için {len(articles)} haber bulundu")
                return articles
            
            return []
            
        except Exception as e:
            log_error(f"Haber arama hatası: {e}")
            return []
    
    def get_financial_news(self, symbol: str = None, page_size: int = 50) -> List[Dict[str, Any]]:
        """Finansal haberleri al"""
        try:
            if symbol:
                # Belirli sembol için haber ara
                query = f"{symbol} stock OR {symbol} shares OR {symbol} earnings"
                articles = self.search_news(query, page_size=page_size)
            else:
                # Genel finansal haberler
                articles = self.get_top_headlines(category='business', page_size=page_size)
            
            # Finansal haberleri filtrele
            financial_keywords = [
                'stock', 'shares', 'earnings', 'revenue', 'profit', 'loss',
                'market', 'trading', 'investment', 'finance', 'economy',
                'hisse', 'sermaye', 'kar', 'zarar', 'piyasa', 'yatırım'
            ]
            
            filtered_articles = []
            for article in articles:
                title = article.get('title', '').lower()
                description = article.get('description', '').lower()
                content = f"{title} {description}"
                
                if any(keyword in content for keyword in financial_keywords):
                    filtered_articles.append(article)
            
            log_info(f"Finansal haberler filtrelendi: {len(filtered_articles)}/{len(articles)}")
            return filtered_articles
            
        except Exception as e:
            log_error(f"Finansal haberler alınırken hata: {e}")
            return []
    
    def get_crypto_news(self, symbol: str = None, page_size: int = 50) -> List[Dict[str, Any]]:
        """Kripto para haberleri al"""
        try:
            if symbol:
                # Belirli kripto para için haber ara
                query = f"{symbol} cryptocurrency OR {symbol} crypto OR {symbol} bitcoin"
                articles = self.search_news(query, page_size=page_size)
            else:
                # Genel kripto haberleri
                query = "cryptocurrency OR bitcoin OR ethereum OR crypto"
                articles = self.search_news(query, page_size=page_size)
            
            # Kripto haberlerini filtrele
            crypto_keywords = [
                'cryptocurrency', 'bitcoin', 'ethereum', 'crypto', 'blockchain',
                'digital currency', 'altcoin', 'defi', 'nft', 'mining'
            ]
            
            filtered_articles = []
            for article in articles:
                title = article.get('title', '').lower()
                description = article.get('description', '').lower()
                content = f"{title} {description}"
                
                if any(keyword in content for keyword in crypto_keywords):
                    filtered_articles.append(article)
            
            log_info(f"Kripto haberler filtrelendi: {len(filtered_articles)}/{len(articles)}")
            return filtered_articles
            
        except Exception as e:
            log_error(f"Kripto haberler alınırken hata: {e}")
            return []
    
    def analyze_news_sentiment(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Haber sentiment analizi"""
        try:
            if not articles:
                return {
                    'total_articles': 0,
                    'sentiment_score': 50.0,
                    'sentiment': 'neutral',
                    'confidence': 0.0,
                    'positive_articles': 0,
                    'negative_articles': 0,
                    'neutral_articles': 0
                }
            
            positive_keywords = [
                'bullish', 'growth', 'profit', 'gain', 'rise', 'up', 'positive',
                'strong', 'excellent', 'outstanding', 'breakthrough', 'success',
                'büyüme', 'kar', 'kazanç', 'artış', 'pozitif', 'güçlü', 'başarı'
            ]
            
            negative_keywords = [
                'bearish', 'decline', 'loss', 'fall', 'down', 'negative',
                'weak', 'terrible', 'crash', 'crisis', 'scandal', 'lawsuit',
                'düşüş', 'kayıp', 'düşme', 'negatif', 'zayıf', 'kriz', 'skandal'
            ]
            
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            
            for article in articles:
                title = article.get('title', '').lower()
                description = article.get('description', '').lower()
                content = f"{title} {description}"
                
                positive_score = sum(1 for keyword in positive_keywords if keyword in content)
                negative_score = sum(1 for keyword in negative_keywords if keyword in content)
                
                if positive_score > negative_score:
                    positive_count += 1
                elif negative_score > positive_score:
                    negative_count += 1
                else:
                    neutral_count += 1
            
            total_articles = len(articles)
            sentiment_score = ((positive_count * 100) + (neutral_count * 50)) / total_articles
            
            if sentiment_score > 60:
                sentiment = 'positive'
            elif sentiment_score < 40:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            confidence = abs(sentiment_score - 50) / 50
            
            result = {
                'total_articles': total_articles,
                'sentiment_score': round(sentiment_score, 2),
                'sentiment': sentiment,
                'confidence': round(confidence, 2),
                'positive_articles': positive_count,
                'negative_articles': negative_count,
                'neutral_articles': neutral_count,
                'sample_articles': articles[:5]  # İlk 5 haber örneği
            }
            
            log_info(f"News sentiment analizi: {sentiment} ({sentiment_score})")
            return result
            
        except Exception as e:
            log_error(f"News sentiment analizi hatası: {e}")
            return {
                'total_articles': 0,
                'sentiment_score': 50.0,
                'sentiment': 'neutral',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def get_market_news(self, market: str = 'general') -> Dict[str, Any]:
        """Piyasa haberleri ve sentiment analizi"""
        try:
            if market == 'crypto':
                articles = self.get_crypto_news(page_size=50)
            elif market == 'stocks':
                articles = self.get_financial_news(page_size=50)
            else:
                # Genel piyasa haberleri
                articles = self.get_top_headlines(category='business', page_size=50)
            
            sentiment_analysis = self.analyze_news_sentiment(articles)
            
            return {
                'market': market,
                'articles': articles,
                'sentiment_analysis': sentiment_analysis,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            log_error(f"Piyasa haberleri alınırken hata: {e}")
            return {
                'market': market,
                'articles': [],
                'sentiment_analysis': {
                    'total_articles': 0,
                    'sentiment_score': 50.0,
                    'sentiment': 'neutral',
                    'confidence': 0.0
                },
                'error': str(e)
            }
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Rate limit durumunu kontrol et"""
        return {
            'remaining': self.rate_limit_remaining,
            'reset_time': self.rate_limit_reset,
            'reset_datetime': datetime.fromtimestamp(self.rate_limit_reset).isoformat() if self.rate_limit_reset else None
        }

# Global NewsAPI instance
news_api = NewsAPI()

