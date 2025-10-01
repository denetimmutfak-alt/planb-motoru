#!/usr/bin/env python3
"""
Enhanced Sentiment Data Sources for Crypto & Commodities
"""

CRYPTO_SENTIMENT_SOURCES = {
    "news_apis": [
        "https://api.coindesk.com/v1/news",
        "https://cryptonews-api.com/api/v1",
        "https://api.blockchain.info/news",
        "https://api.cointelegraph.com/news"
    ],
    "social_sources": [
        "reddit.com/r/cryptocurrency",
        "reddit.com/r/bitcoin", 
        "reddit.com/r/ethereum",
        "twitter.com/crypto_sentiment",
        "telegram.com/crypto_signals"
    ],
    "on_chain_sources": [
        "https://api.glassnode.com/v1/metrics",
        "https://api.santiment.net/graphql",
        "https://api.messari.io/api/v1/assets",
        "https://api.dune.com/api/v1/query"
    ],
    "developer_activity": [
        "github.com/bitcoin/bitcoin/commits",
        "github.com/ethereum/go-ethereum/commits",
        "github.com/cardano-foundation/cardano-node/commits"
    ]
}

COMMODITY_SENTIMENT_SOURCES = {
    "financial_news": [
        "https://api.bloomberg.com/news/commodities",
        "https://api.reuters.com/commodities", 
        "https://api.wsj.com/market-data/commodities",
        "https://commodities.agriculture.com/api/news"
    ],
    "government_data": [
        "https://api.eia.gov/v2/petroleum",  # Energy Information Administration
        "https://api.usda.gov/grain-market",  # USDA Agricultural data
        "https://www.federalreserve.gov/monetarypolicy/beigebook"
    ],
    "industry_reports": [
        "https://api.lme.com/market-data",  # London Metal Exchange
        "https://api.cme.com/market-data",  # Chicago Mercantile Exchange
        "https://api.ice.com/market-data"   # Intercontinental Exchange
    ],
    "weather_data": [
        "https://api.weather.com/agricultural",
        "https://api.noaa.gov/climate-data",
        "https://api.usda.gov/weather-impact"
    ]
}

def get_enhanced_crypto_sentiment(symbol: str) -> dict:
    """Crypto için gelişmiş sentiment analizi"""
    
    # Symbol mapping
    symbol_map = {
        "BTC-USD": "bitcoin",
        "ETH-USD": "ethereum", 
        "ADA-USD": "cardano",
        "DOGE-USD": "dogecoin"
    }
    
    coin_name = symbol_map.get(symbol, symbol.replace("-USD", "").lower())
    
    sentiment_data = {
        "news_sentiment": get_crypto_news_sentiment(coin_name),
        "social_sentiment": get_crypto_social_sentiment(coin_name),
        "onchain_sentiment": get_crypto_onchain_sentiment(coin_name),
        "dev_sentiment": get_crypto_dev_sentiment(coin_name),
        "fear_greed_index": get_crypto_fear_greed(),
        "final_score": 50.0
    }
    
    # Weighted combination
    weights = {
        "news": 0.25,
        "social": 0.30, 
        "onchain": 0.25,
        "dev": 0.10,
        "fear_greed": 0.10
    }
    
    final_score = (
        sentiment_data["news_sentiment"] * weights["news"] +
        sentiment_data["social_sentiment"] * weights["social"] +
        sentiment_data["onchain_sentiment"] * weights["onchain"] +
        sentiment_data["dev_sentiment"] * weights["dev"] +
        sentiment_data["fear_greed_index"] * weights["fear_greed"]
    )
    
    sentiment_data["final_score"] = final_score
    return sentiment_data

def get_crypto_news_sentiment(coin_name: str) -> float:
    """Crypto news sentiment - Mock implementation"""
    # Bu gerçek API'lerle implement edilecek
    import random
    return random.uniform(30, 80)  # Mock data

def get_crypto_social_sentiment(coin_name: str) -> float:
    """Crypto social media sentiment"""
    import random
    return random.uniform(35, 75)  # Mock data

def get_crypto_onchain_sentiment(coin_name: str) -> float:
    """On-chain metrics sentiment"""
    import random
    return random.uniform(40, 70)  # Mock data

def get_crypto_dev_sentiment(coin_name: str) -> float:
    """Developer activity sentiment"""
    import random
    return random.uniform(45, 65)  # Mock data

def get_crypto_fear_greed() -> float:
    """Crypto Fear & Greed Index"""
    import random
    return random.uniform(20, 80)  # Mock data

def get_enhanced_commodity_sentiment(symbol: str) -> dict:
    """Emtia için gelişmiş sentiment analizi"""
    
    # Symbol mapping
    symbol_map = {
        "GC=F": "gold",
        "SI=F": "silver",
        "CL=F": "crude_oil", 
        "ZW=F": "wheat"
    }
    
    commodity_name = symbol_map.get(symbol, symbol)
    
    sentiment_data = {
        "financial_news": get_commodity_financial_news(commodity_name),
        "government_data": get_commodity_government_sentiment(commodity_name),
        "supply_demand": get_commodity_supply_demand(commodity_name),
        "weather_impact": get_commodity_weather_sentiment(commodity_name),
        "geopolitical": get_commodity_geopolitical_sentiment(commodity_name),
        "final_score": 50.0
    }
    
    # Weighted combination  
    weights = {
        "financial_news": 0.25,
        "government_data": 0.20,
        "supply_demand": 0.25,
        "weather_impact": 0.15,
        "geopolitical": 0.15
    }
    
    final_score = sum(
        sentiment_data[key] * weights[key.replace("_impact", "").replace("_data", "")]
        for key in weights.keys()
    )
    
    sentiment_data["final_score"] = final_score
    return sentiment_data

def get_commodity_financial_news(commodity: str) -> float:
    """Commodity financial news sentiment"""
    import random
    return random.uniform(35, 75)  # Mock data

def get_commodity_government_sentiment(commodity: str) -> float:
    """Government reports sentiment"""
    import random
    return random.uniform(40, 70)  # Mock data

def get_commodity_supply_demand(commodity: str) -> float:
    """Supply/demand balance sentiment"""
    import random
    return random.uniform(30, 80)  # Mock data

def get_commodity_weather_sentiment(commodity: str) -> float:
    """Weather impact sentiment"""
    import random
    return random.uniform(35, 75)  # Mock data

def get_commodity_geopolitical_sentiment(commodity: str) -> float:
    """Geopolitical factors sentiment"""
    import random
    return random.uniform(25, 85)  # Mock data

if __name__ == "__main__":
    # Test
    btc_sentiment = get_enhanced_crypto_sentiment("BTC-USD")
    gold_sentiment = get_enhanced_commodity_sentiment("GC=F")
    
    print(f"BTC Enhanced Sentiment: {btc_sentiment['final_score']:.1f}")
    print(f"Gold Enhanced Sentiment: {gold_sentiment['final_score']:.1f}")