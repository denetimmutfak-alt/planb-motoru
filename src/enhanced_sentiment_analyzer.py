import os, torch, logging#!/usr/bin/env python3

from transformers import pipeline"""

from dotenv import load_dotenvEnhanced Sentiment Analyzer for PlanB Trading System

Integrates News API, Reddit API, and TextBlob for comprehensive sentiment analysis

load_dotenv()"""

logging.basicConfig(level=logging.INFO)import os

logger = logging.getLogger(__name__)import requests

import logging

# Türkçe FinBERT pipeline ----------------------------------------------------import json

MODEL_NAME = "savasy/bert-base-turkish-sentiment-cased"import time

device = 0 if torch.cuda.is_available() else -1from datetime import datetime, timedelta

sent_pipe = pipeline("text-classification",import base64

                     model=MODEL_NAME,from typing import Dict, List, Optional, Tuple

                     tokenizer=MODEL_NAME,

                     device=device)# Configure logging

logging.basicConfig(level=logging.INFO)

def berturk_sentiment(text: str) -> float:logger = logging.getLogger(__name__)

    """

    Return continuous polarity in [-1, 1]try:

    """    from textblob import TextBlob

    try:    import nltk

        res = sent_pipe(text[:512], truncation=True)[0]    # Download required NLTK data

        label, score = res["label"], res["score"]    try:

        if label == "POSITIVE":        nltk.data.find('tokenizers/punkt')

            return score    except LookupError:

        elif label == "NEGATIVE":        nltk.download('punkt')

            return -score    

        else:                      # NEUTRAL    try:

            return 0.0        nltk.data.find('corpora/movie_reviews')

    except Exception as e:    except LookupError:

        logger.exception("BERTurk error")        nltk.download('movie_reviews')

        return 0.0        

    TEXTBLOB_AVAILABLE = True

if __name__ == "__main__":except ImportError as e:

    print(berturk_sentiment("Dolar yeni zirve yaptı, piyasalar korkuyor"))    logger.warning(f"TextBlob not available: {e}")
    TEXTBLOB_AVAILABLE = False


class EnhancedSentimentAnalyzer:
    """
    Enhanced sentiment analyzer combining multiple sources:
    - News API for financial news
    - Reddit API for social sentiment
    - TextBlob for natural language processing
    """
    
    def __init__(self):
        # API Keys from environment
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        
        # Reddit OAuth token
        self.reddit_token = None
        self.reddit_token_expires = None
        
        # Initialize Reddit authentication
        self._authenticate_reddit()
        
    def _authenticate_reddit(self):
        """Authenticate with Reddit API using OAuth"""
        if not self.reddit_client_id or not self.reddit_client_secret:
            logger.warning("Reddit credentials not found in environment variables")
            return False
            
        try:
            # Prepare credentials
            auth = base64.b64encode(f"{self.reddit_client_id}:{self.reddit_client_secret}".encode()).decode()
            
            headers = {
                'Authorization': f'Basic {auth}',
                'User-Agent': 'PlanBTradingBot/1.0'
            }
            
            data = {
                'grant_type': 'client_credentials'
            }
            
            response = requests.post('https://www.reddit.com/api/v1/access_token', 
                                   headers=headers, data=data, timeout=10)
            
            if response.status_code == 200:
                token_data = response.json()
                self.reddit_token = token_data['access_token']
                # Token expires in 1 hour typically
                self.reddit_token_expires = datetime.now() + timedelta(seconds=token_data.get('expires_in', 3600))
                logger.info("Reddit authentication successful")
                return True
            else:
                logger.error(f"Reddit authentication failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Reddit authentication error: {e}")
            return False
    
    def _is_reddit_token_valid(self):
        """Check if Reddit token is still valid"""
        if not self.reddit_token or not self.reddit_token_expires:
            return False
        return datetime.now() < self.reddit_token_expires
    
    def get_news_sentiment(self, symbol: str, days_back: int = 7) -> Dict:
        """Get news sentiment for a symbol using News API"""
        if not self.news_api_key:
            logger.warning("News API key not found")
            return {'score': 0, 'count': 0, 'source': 'news_api_unavailable'}
        
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Prepare search query
            query = f'"{symbol}" OR "{symbol.upper()}" AND (stock OR shares OR trading OR financial OR market)'
            
            params = {
                'q': query,
                'from': start_date.strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d'),
                'sortBy': 'relevancy',
                'language': 'en',
                'pageSize': 50,
                'apiKey': self.news_api_key
            }
            
            response = requests.get('https://newsapi.org/v2/everything', params=params, timeout=15)
            
            if response.status_code != 200:
                logger.error(f"News API error: {response.status_code}")
                return {'score': 0, 'count': 0, 'source': 'news_api_error'}
            
            articles = response.json().get('articles', [])
            
            if not articles:
                return {'score': 0, 'count': 0, 'source': 'news_no_articles'}
            
            # Analyze sentiment of articles
            total_sentiment = 0
            article_count = 0
            
            for article in articles:
                title = article.get('title', '')
                description = article.get('description', '')
                content = f"{title} {description}"
                
                if content and TEXTBLOB_AVAILABLE:
                    try:
                        blob = TextBlob(content)
                        sentiment = blob.sentiment.polarity
                        total_sentiment += sentiment
                        article_count += 1
                    except Exception as e:
                        logger.debug(f"TextBlob error for article: {e}")
                        continue
            
            if article_count == 0:
                return {'score': 0, 'count': 0, 'source': 'news_no_analysis'}
            
            # Calculate average sentiment (-1 to 1) -> (0 to 100)
            avg_sentiment = total_sentiment / article_count
            normalized_score = (avg_sentiment + 1) * 50  # Convert to 0-100 scale
            
            return {
                'score': round(normalized_score, 1),
                'count': article_count,
                'source': 'news_api'
            }
            
        except Exception as e:
            logger.error(f"News sentiment error: {e}")
            return {'score': 0, 'count': 0, 'source': 'news_error'}
    
    def get_reddit_sentiment(self, symbol: str, limit: int = 25) -> Dict:
        """Get Reddit sentiment for a symbol"""
        if not self._is_reddit_token_valid():
            if not self._authenticate_reddit():
                return {'score': 0, 'count': 0, 'source': 'reddit_auth_failed'}
        
        try:
            headers = {
                'Authorization': f'Bearer {self.reddit_token}',
                'User-Agent': 'PlanBTradingBot/1.0'
            }
            
            # Search multiple relevant subreddits
            subreddits = ['stocks', 'investing', 'SecurityAnalysis', 'StockMarket', 'wallstreetbets']
            all_posts = []
            
            for subreddit in subreddits:
                try:
                    # Search for symbol in subreddit
                    url = f'https://oauth.reddit.com/r/{subreddit}/search'
                    params = {
                        'q': symbol,
                        'sort': 'relevance',
                        'limit': 10,
                        'restrict_sr': 1,
                        't': 'week'
                    }
                    
                    response = requests.get(url, headers=headers, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        posts = data.get('data', {}).get('children', [])
                        all_posts.extend(posts)
                    
                    # Rate limiting
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.debug(f"Error searching subreddit {subreddit}: {e}")
                    continue
            
            if not all_posts:
                return {'score': 0, 'count': 0, 'source': 'reddit_no_posts'}
            
            # Analyze sentiment
            total_sentiment = 0
            post_count = 0
            
            for post in all_posts[:limit]:
                try:
                    post_data = post.get('data', {})
                    title = post_data.get('title', '')
                    selftext = post_data.get('selftext', '')
                    content = f"{title} {selftext}"
                    
                    if content and TEXTBLOB_AVAILABLE:
                        blob = TextBlob(content)
                        sentiment = blob.sentiment.polarity
                        total_sentiment += sentiment
                        post_count += 1
                        
                except Exception as e:
                    logger.debug(f"Error analyzing Reddit post: {e}")
                    continue
            
            if post_count == 0:
                return {'score': 0, 'count': 0, 'source': 'reddit_no_analysis'}
            
            # Calculate average sentiment
            avg_sentiment = total_sentiment / post_count
            normalized_score = (avg_sentiment + 1) * 50  # Convert to 0-100 scale
            
            return {
                'score': round(normalized_score, 1),
                'count': post_count,
                'source': 'reddit'
            }
            
        except Exception as e:
            logger.error(f"Reddit sentiment error: {e}")
            return {'score': 0, 'count': 0, 'source': 'reddit_error'}
    
    def get_symbol_sentiment(self, symbol: str) -> float:
        """
        Get comprehensive sentiment score for a symbol (0-100 scale)
        Combines news and Reddit sentiment with weighted average
        """
        try:
            # Get sentiment from multiple sources
            news_sentiment = self.get_news_sentiment(symbol)
            reddit_sentiment = self.get_reddit_sentiment(symbol)
            
            # Default neutral sentiment
            final_score = 50.0
            
            # Weight calculation based on data availability
            total_weight = 0
            weighted_sum = 0
            
            # News sentiment (weight: 0.6)
            if news_sentiment['count'] > 0:
                news_weight = min(0.6, news_sentiment['count'] * 0.1)  # Max 0.6, scales with article count
                weighted_sum += news_sentiment['score'] * news_weight
                total_weight += news_weight
                logger.info(f"News sentiment for {symbol}: {news_sentiment['score']:.1f} (from {news_sentiment['count']} articles)")
            
            # Reddit sentiment (weight: 0.4)
            if reddit_sentiment['count'] > 0:
                reddit_weight = min(0.4, reddit_sentiment['count'] * 0.05)  # Max 0.4, scales with post count
                weighted_sum += reddit_sentiment['score'] * reddit_weight
                total_weight += reddit_weight
                logger.info(f"Reddit sentiment for {symbol}: {reddit_sentiment['score']:.1f} (from {reddit_sentiment['count']} posts)")
            
            # Calculate final weighted score
            if total_weight > 0:
                final_score = weighted_sum / total_weight
            
            logger.info(f"Final sentiment score for {symbol}: {final_score:.1f}/100")
            
            return round(final_score, 1)
            
        except Exception as e:
            logger.error(f"Error calculating sentiment for {symbol}: {e}")
            return 50.0  # Return neutral sentiment on error


def test_sentiment_analyzer():
    """Test the sentiment analyzer"""
    print("Testing Enhanced Sentiment Analyzer...")
    
    analyzer = EnhancedSentimentAnalyzer()
    
    # Test with a popular stock
    test_symbols = ['AAPL', 'TSLA', 'MSFT']
    
    for symbol in test_symbols:
        print(f"\nTesting sentiment for {symbol}:")
        sentiment_score = analyzer.get_symbol_sentiment(symbol)
        print(f"Final sentiment score: {sentiment_score}/100")
        
        if sentiment_score >= 60:
            print("Sentiment: POSITIVE")
        elif sentiment_score <= 40:
            print("Sentiment: NEGATIVE")
        else:
            print("Sentiment: NEUTRAL")


if __name__ == "__main__":
    test_sentiment_analyzer()