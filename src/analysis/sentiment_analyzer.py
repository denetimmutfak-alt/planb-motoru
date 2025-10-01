"""
PlanB Motoru - Sentiment & News Analyzer
Sosyal medya, haber ve gündem analizi modülü
"""
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import re
from urllib.parse import quote
import time
from src.api.twitter_api import twitter_api
from src.api.news_api import news_api
from src.api.reddit_api import reddit_api
from src.utils.logger import log_info, log_error

class SentimentAnalyzer:
    """Sentiment ve haber analizi yapan sınıf"""
    
    def __init__(self):
        self.positive_keywords = [
            'bullish', 'buy', 'strong', 'growth', 'profit', 'gain', 'rise', 'up', 'positive',
            'excellent', 'great', 'amazing', 'fantastic', 'outstanding', 'breakthrough',
            'partnership', 'acquisition', 'expansion', 'innovation', 'breakthrough',
            'yükseliş', 'alış', 'güçlü', 'büyüme', 'kar', 'kazanç', 'artış', 'pozitif',
            'mükemmel', 'harika', 'muhteşem', 'başarılı', 'atılım', 'ortaklık', 'satın alma'
        ]
        
        self.negative_keywords = [
            'bearish', 'sell', 'weak', 'decline', 'loss', 'fall', 'down', 'negative',
            'terrible', 'awful', 'disaster', 'crash', 'bankruptcy', 'scandal',
            'lawsuit', 'investigation', 'regulatory', 'fine', 'penalty', 'crisis',
            'düşüş', 'satış', 'zayıf', 'kayıp', 'düşme', 'negatif', 'kötü', 'felaket',
            'çöküş', 'iflas', 'skandal', 'dava', 'soruşturma', 'kriz'
        ]
        
        self.neutral_keywords = [
            'hold', 'stable', 'neutral', 'maintain', 'unchanged', 'flat',
            'bekle', 'kararlı', 'nötr', 'sabit', 'değişmez'
        ]
    
    def analyze_twitter_sentiment(self, symbol: str, count: int = 100) -> Dict[str, Any]:
        """Twitter sentiment analizi (gerçek API)"""
        try:
            # Gerçek Twitter API kullan
            if twitter_api.bearer_token:
                log_info(f"Twitter API ile {symbol} sentiment analizi başlatılıyor")
                
                # Sembol tipine göre analiz yap
                if symbol.endswith('.IS') or symbol in ['BTC', 'ETH', 'ADA', 'DOT']:
                    # Kripto para için
                    result = twitter_api.get_crypto_sentiment(symbol.replace('.IS', ''))
                else:
                    # Hisse senedi için
                    result = twitter_api.get_stock_sentiment(symbol)
                
                return {
                    'score': result.get('sentiment_score', 50),
                    'sentiment': result.get('sentiment', 'neutral'),
                    'confidence': result.get('confidence', 0.5),
                    'source': 'Twitter API',
                    'total_tweets': result.get('total_tweets', 0),
                    'positive_tweets': result.get('positive_tweets', 0),
                    'negative_tweets': result.get('negative_tweets', 0),
                    'neutral_tweets': result.get('neutral_tweets', 0)
                }
            else:
                log_info(f"Twitter API token yok, simüle edilmiş veri kullanılıyor: {symbol}")
                # Fallback: Simüle edilmiş veri
                simulated_tweets = [
                    f"{symbol} looking strong today! #bullish",
                    f"Great earnings report from {symbol}",
                    f"{symbol} breaking resistance levels",
                f"Market sentiment positive for {symbol}",
                f"{symbol} showing good momentum"
            ]
            
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            
            for tweet in simulated_tweets:
                sentiment = self._analyze_text_sentiment(tweet)
                if sentiment == 'positive':
                    positive_count += 1
                elif sentiment == 'negative':
                    negative_count += 1
                else:
                    neutral_count += 1
            
            total = positive_count + negative_count + neutral_count
            if total == 0:
                return {"score": 50, "sentiment": "neutral", "confidence": 0}
            
            positive_ratio = positive_count / total
            negative_ratio = negative_count / total
            
            # Sentiment skoru hesapla (0-100)
            score = (positive_ratio * 100) - (negative_ratio * 50) + 50
            score = max(0, min(100, score))
            
            if positive_ratio > negative_ratio:
                sentiment = "positive"
                confidence = positive_ratio
            elif negative_ratio > positive_ratio:
                sentiment = "negative"
                confidence = negative_ratio
            else:
                sentiment = "neutral"
                confidence = 0.5
            
            return {
                "score": round(score, 2),
                "sentiment": sentiment,
                "confidence": round(confidence, 2),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "neutral_count": neutral_count,
                "total_tweets": total
            }
            
        except Exception as e:
            return {"score": 50, "sentiment": "neutral", "confidence": 0, "error": str(e)}
    
    def analyze_news_sentiment(self, symbol: str, days: int = 7) -> Dict[str, Any]:
        """Haber sentiment analizi (gerçek API)"""
        try:
            # Gerçek NewsAPI kullan
            if news_api.api_key:
                log_info(f"NewsAPI ile {symbol} haber sentiment analizi başlatılıyor")
                
                # Sembol tipine göre haber al
                if symbol.endswith('.IS') or symbol in ['BTC', 'ETH', 'ADA', 'DOT']:
                    # Kripto para için
                    market_news = news_api.get_market_news('crypto')
                else:
                    # Hisse senedi için
                    market_news = news_api.get_market_news('stocks')
                
                sentiment_analysis = market_news.get('sentiment_analysis', {})
                
                return {
                    'score': sentiment_analysis.get('sentiment_score', 50),
                    'sentiment': sentiment_analysis.get('sentiment', 'neutral'),
                    'confidence': sentiment_analysis.get('confidence', 0.5),
                    'source': 'NewsAPI',
                    'total_articles': sentiment_analysis.get('total_articles', 0),
                    'positive_articles': sentiment_analysis.get('positive_articles', 0),
                    'negative_articles': sentiment_analysis.get('negative_articles', 0),
                    'neutral_articles': sentiment_analysis.get('neutral_articles', 0)
                }
            else:
                log_info(f"NewsAPI anahtarı yok, simüle edilmiş veri kullanılıyor: {symbol}")
                # Fallback: Simüle edilmiş veri
                simulated_news = [
                    f"{symbol} reports strong quarterly earnings",
                    f"{symbol} announces new product launch",
                    f"{symbol} forms strategic partnership",
                f"{symbol} beats market expectations",
                f"{symbol} shows robust growth metrics"
            ]
            
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            
            for news in simulated_news:
                sentiment = self._analyze_text_sentiment(news)
                if sentiment == 'positive':
                    positive_count += 1
                elif sentiment == 'negative':
                    negative_count += 1
                else:
                    neutral_count += 1
            
            total = positive_count + negative_count + neutral_count
            if total == 0:
                return {"score": 50, "sentiment": "neutral", "confidence": 0}
            
            positive_ratio = positive_count / total
            negative_ratio = negative_count / total
            
            # Haber sentiment skoru (0-100)
            score = (positive_ratio * 100) - (negative_ratio * 50) + 50
            score = max(0, min(100, score))
            
            if positive_ratio > negative_ratio:
                sentiment = "positive"
                confidence = positive_ratio
            elif negative_ratio > positive_ratio:
                sentiment = "negative"
                confidence = negative_ratio
            else:
                sentiment = "neutral"
                confidence = 0.5
            
            return {
                "score": round(score, 2),
                "sentiment": sentiment,
                "confidence": round(confidence, 2),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "neutral_count": neutral_count,
                "total_news": total,
                "timeframe_days": days
            }
            
        except Exception as e:
            return {"score": 50, "sentiment": "neutral", "confidence": 0, "error": str(e)}
    
    def analyze_reddit_sentiment(self, symbol: str, subreddits: List[str] = None) -> Dict[str, Any]:
        """Reddit sentiment analizi (gerçek API)"""
        try:
            # Gerçek Reddit API kullan
            if reddit_api.client_id:
                log_info(f"Reddit API ile {symbol} sentiment analizi başlatılıyor")
                
                # Sembol tipine göre post al
                if symbol.endswith('.IS') or symbol in ['BTC', 'ETH', 'ADA', 'DOT']:
                    # Kripto para için
                    market_sentiment = reddit_api.get_market_sentiment('crypto')
                else:
                    # Hisse senedi için
                    market_sentiment = reddit_api.get_market_sentiment('stocks')
                
                sentiment_analysis = market_sentiment.get('sentiment_analysis', {})
                
                return {
                    'score': sentiment_analysis.get('sentiment_score', 50),
                    'sentiment': sentiment_analysis.get('sentiment', 'neutral'),
                    'confidence': sentiment_analysis.get('confidence', 0.5),
                    'source': 'Reddit API',
                    'total_posts': sentiment_analysis.get('total_posts', 0),
                    'positive_posts': sentiment_analysis.get('positive_posts', 0),
                    'negative_posts': sentiment_analysis.get('negative_posts', 0),
                    'neutral_posts': sentiment_analysis.get('neutral_posts', 0)
                }
            else:
                log_info(f"Reddit API credentials yok, simüle edilmiş veri kullanılıyor: {symbol}")
                # Fallback: Simüle edilmiş veri
                if subreddits is None:
                    subreddits = ['investing', 'stocks', 'SecurityAnalysis', 'ValueInvesting']
                
                simulated_posts = [
                    f"DD: {symbol} undervalued with strong fundamentals",
                    f"{symbol} technical analysis shows bullish pattern",
                    f"Long term holder of {symbol}, very optimistic",
                f"{symbol} earnings call was impressive",
                f"Added more {symbol} to my portfolio"
            ]
            
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            
            for post in simulated_posts:
                sentiment = self._analyze_text_sentiment(post)
                if sentiment == 'positive':
                    positive_count += 1
                elif sentiment == 'negative':
                    negative_count += 1
                else:
                    neutral_count += 1
            
            total = positive_count + negative_count + neutral_count
            if total == 0:
                return {"score": 50, "sentiment": "neutral", "confidence": 0}
            
            positive_ratio = positive_count / total
            negative_ratio = negative_count / total
            
            # Reddit sentiment skoru (0-100)
            score = (positive_ratio * 100) - (negative_ratio * 50) + 50
            score = max(0, min(100, score))
            
            if positive_ratio > negative_ratio:
                sentiment = "positive"
                confidence = positive_ratio
            elif negative_ratio > positive_ratio:
                sentiment = "negative"
                confidence = negative_ratio
            else:
                sentiment = "neutral"
                confidence = 0.5
            
            return {
                "score": round(score, 2),
                "sentiment": sentiment,
                "confidence": round(confidence, 2),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "neutral_count": neutral_count,
                "total_posts": total,
                "subreddits": subreddits
            }
            
        except Exception as e:
            return {"score": 50, "sentiment": "neutral", "confidence": 0, "error": str(e)}
    
    def analyze_company_news(self, symbol: str) -> Dict[str, Any]:
        """Şirket gündemi analizi (simüle edilmiş)"""
        try:
            # Simüle edilmiş şirket gündemi
            company_events = [
                "Q3 earnings beat expectations",
                "New product launch announced",
                "Strategic partnership signed",
                "Management guidance raised",
                "Market expansion plans revealed"
            ]
            
            # Her olay için sentiment analizi
            positive_events = 0
            negative_events = 0
            neutral_events = 0
            
            for event in company_events:
                sentiment = self._analyze_text_sentiment(event)
                if sentiment == 'positive':
                    positive_events += 1
                elif sentiment == 'negative':
                    negative_events += 1
                else:
                    neutral_events += 1
            
            total_events = positive_events + negative_events + neutral_events
            if total_events == 0:
                return {"score": 50, "sentiment": "neutral", "confidence": 0}
            
            positive_ratio = positive_events / total_events
            negative_ratio = negative_events / total_events
            
            # Şirket gündemi skoru (0-100)
            score = (positive_ratio * 100) - (negative_ratio * 50) + 50
            score = max(0, min(100, score))
            
            if positive_ratio > negative_ratio:
                sentiment = "positive"
                confidence = positive_ratio
            elif negative_ratio > positive_ratio:
                sentiment = "negative"
                confidence = negative_ratio
            else:
                sentiment = "neutral"
                confidence = 0.5
            
            return {
                "score": round(score, 2),
                "sentiment": sentiment,
                "confidence": round(confidence, 2),
                "positive_events": positive_events,
                "negative_events": negative_events,
                "neutral_events": neutral_events,
                "total_events": total_events,
                "recent_events": company_events[:3]  # Son 3 olay
            }
            
        except Exception as e:
            return {"score": 50, "sentiment": "neutral", "confidence": 0, "error": str(e)}
    
    def _analyze_text_sentiment(self, text: str) -> str:
        """Metin sentiment analizi"""
        text_lower = text.lower()
        
        positive_score = sum(1 for keyword in self.positive_keywords if keyword in text_lower)
        negative_score = sum(1 for keyword in self.negative_keywords if keyword in text_lower)
        neutral_score = sum(1 for keyword in self.neutral_keywords if keyword in text_lower)
        
        if positive_score > negative_score:
            return "positive"
        elif negative_score > positive_score:
            return "negative"
        else:
            return "neutral"
    
    def calculate_sentiment_score(self, symbol: str) -> float:
        """Genel sentiment skoru hesapla (0-100)"""
        try:
            # Tüm sentiment kaynaklarını analiz et
            twitter_sentiment = self.analyze_twitter_sentiment(symbol)
            news_sentiment = self.analyze_news_sentiment(symbol)
            reddit_sentiment = self.analyze_reddit_sentiment(symbol)
            company_news = self.analyze_company_news(symbol)
            
            # Ağırlıklı ortalama hesapla
            weights = {
                'twitter': 0.25,
                'news': 0.35,
                'reddit': 0.25,
                'company': 0.15
            }
            
            total_score = (
                twitter_sentiment['score'] * weights['twitter'] +
                news_sentiment['score'] * weights['news'] +
                reddit_sentiment['score'] * weights['reddit'] +
                company_news['score'] * weights['company']
            )
            
            return round(total_score, 2)
            
        except Exception as e:
            return 50.0  # Varsayılan nötr skor
    
    def get_sentiment_analysis(self, symbol: str) -> Dict[str, Any]:
        """Tam sentiment analizi"""
        try:
            twitter_sentiment = self.analyze_twitter_sentiment(symbol)
            news_sentiment = self.analyze_news_sentiment(symbol)
            reddit_sentiment = self.analyze_reddit_sentiment(symbol)
            company_news = self.analyze_company_news(symbol)
            
            overall_score = self.calculate_sentiment_score(symbol)
            
            # Genel sentiment belirleme
            if overall_score >= 60:
                overall_sentiment = "positive"
            elif overall_score <= 40:
                overall_sentiment = "negative"
            else:
                overall_sentiment = "neutral"
            
            return {
                "score": overall_score,
                "sentiment": overall_sentiment,
                "twitter": twitter_sentiment,
                "news": news_sentiment,
                "reddit": reddit_sentiment,
                "company_news": company_news,
                "analysis_date": datetime.now().isoformat(),
                "description": f"Genel sentiment: {overall_sentiment} ({overall_score}/100)"
            }
            
        except Exception as e:
            return {
                "score": 50,
                "sentiment": "neutral",
                "error": str(e),
                "analysis_date": datetime.now().isoformat()
            }

# Global instance
sentiment_analyzer = SentimentAnalyzer()

