"""
PlanB Motoru - API Anahtarları Konfigürasyonu
Güvenli API anahtarı yönetimi
"""
from typing import Optional

# API Anahtarları (ücretsiz tier'lar)
API_KEYS = {
    # Alpha Vantage - Ücretsiz: 5 istek/dakika, 500 istek/gün
    'ALPHA_VANTAGE': {
        'key': 'NNV6Y2WKLVJ2MSEP',  # https://www.alphavantage.co/support/#api-key adresinden alın
        'rate_limit': 5,  # dakikada 5 istek
        'daily_limit': 500,  # günde 500 istek
        'enabled': True  # API key girilene kadar kapalı
    },
    
    # Financial Modeling Prep - Ücretsiz: 250 istek/gün
    'FINANCIAL_MODELING_PREP': {
        'key': 'PPTbB7kkfPuVbw0R7ons66AE8TeqqbeJ',  # https://financialmodelingprep.com/developer/docs adresinden alın
        'rate_limit': 10,  # dakikada 10 istek
        'daily_limit': 250,  # günde 250 istek
        'enabled': True  # API key girilene kadar kapalı
    },
    
    # Polygon.io - Ücretsiz: 5 istek/dakika, 1000 istek/gün
    'POLYGON': {
        'key': 'pBoNdCxlGlGRFf5Nk3P0zzA_k8fkBRoY',  # https://polygon.io/ adresinden alın
        'rate_limit': 5,  # dakikada 5 istek
        'daily_limit': 1000,  # günde 1000 istek
        'enabled': True  # API key girilene kadar kapalı
    },
    
    # Yahoo Finance - Ücretsiz ama rate limiting var
    'YAHOO_FINANCE': {
        'rate_limit': 5,  # dakikada 5 istek (güvenli)
        'enabled': True  # Varsayılan olarak aktif
    },
    
    # Twitter API v2 - Ücretsiz: 300 istek/15 dakika
    'TWITTER': {
        'bearer_token': 'AAAAAAAAAAAAAAAAAAAAAKjm4AEAAAAAw2XfQcq4f0ffSigKkG5Jubl3uFM%3DEPKoULuNS5n1WxpBSYSgPpWvsYrXX7EJMhCf1FYa9v9pWwAgvS',  # https://developer.twitter.com/en/portal/dashboard adresinden alın
        'rate_limit': 300,  # 15 dakikada 300 istek
        'daily_limit': 10000,  # günde 10,000 istek
        'enabled': True  # Bearer token girilene kadar kapalı
    },
    
    # NewsAPI - Ücretsiz: 1000 istek/gün
    'NEWSAPI': {
        'key': 'fe436bb4bc564f97a624d2652b358b86',  # https://newsapi.org/register adresinden alın
        'rate_limit': 1000,  # günde 1000 istek
        'daily_limit': 1000,  # günde 1000 istek
        'enabled': True  # API key girilene kadar kapalı
    },
    
    # Reddit API - Ücretsiz: 60 istek/dakika
    'REDDIT': {
        'client_id': 'QmiOYEAqbRvkbaArOdEH-Q',  # Reddit App Client ID
        'client_secret': '77sm-QOZtki4OtMH7En38CQgUh5Z-A',  # Reddit App Client Secret
        'rate_limit': 60,  # dakikada 60 istek
        'daily_limit': 10000,  # günde 10,000 istek
        'enabled': True  # API key girilene kadar kapalı
    },
    
}

# API Öncelik Sırası (yukarıdan aşağıya)
API_PRIORITY = [
    'ALPHA_VANTAGE',
    'POLYGON',
    'FINANCIAL_MODELING_PREP', 
    'YAHOO_FINANCE'
]

# Fallback Stratejisi
FALLBACK_STRATEGY = {
    'use_static_data': True,  # API'ler çalışmazsa statik veri kullan
    'cache_duration': 3600,  # 1 saat cache
    'retry_attempts': 3,  # 3 deneme
    'retry_delay': 5  # 5 saniye bekleme
}

def get_api_key(service: str) -> Optional[str]:
    """API anahtarını güvenli şekilde al"""
    if service in API_KEYS:
        # Twitter için bearer_token, diğerleri için key
        if service == 'TWITTER':
            return API_KEYS[service].get('bearer_token')
        else:
            return API_KEYS[service].get('key')
    return None

def get_reddit_client_id() -> Optional[str]:
    """Reddit Client ID al"""
    if 'REDDIT' in API_KEYS:
        return API_KEYS['REDDIT'].get('client_id')
    return None

def get_reddit_client_secret() -> Optional[str]:
    """Reddit Client Secret al"""
    if 'REDDIT' in API_KEYS:
        return API_KEYS['REDDIT'].get('client_secret')
    return None

def is_api_enabled(service: str) -> bool:
    """API'nin aktif olup olmadığını kontrol et"""
    if service in API_KEYS:
        return API_KEYS[service].get('enabled', False)
    return False

def get_rate_limit(service: str) -> int:
    """API'nin rate limit'ini al"""
    if service in API_KEYS:
        return API_KEYS[service].get('rate_limit', 5)
    return 5
