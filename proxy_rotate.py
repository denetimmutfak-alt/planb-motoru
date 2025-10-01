"""
Optional Proxy Rotation System for enhanced Yahoo Finance resilience
Install: pip install free-proxy
"""

import random
import requests
import yfinance as yf

# Global proxy pool - populated on demand
PROXY_LIST = []
PROXY_REFRESH_INTERVAL = 300  # 5 minutes

def get_free_proxies():
    """Fetch fresh proxy list"""
    global PROXY_LIST
    try:
        # Import free-proxy (optional dependency)
        from fp.fp import FreeProxy
        
        print("🔄 Fetching fresh proxy list...")
        PROXY_LIST = []
        
        # Get proxies from different countries
        countries = ["US", "GB", "DE", "NL", "FR"]
        
        for _ in range(5):  # Get 5 proxies
            try:
                proxy = FreeProxy(
                    rand=True, 
                    country_id=countries,
                    timeout=1,
                    https=True
                ).get()
                if proxy and proxy not in PROXY_LIST:
                    PROXY_LIST.append(proxy)
            except:
                continue
        
        print(f"✅ Found {len(PROXY_LIST)} working proxies")
        return len(PROXY_LIST) > 0
        
    except ImportError:
        print("⚠️ free-proxy not installed. Install with: pip install free-proxy")
        return False
    except Exception as e:
        print(f"❌ Proxy fetch failed: {e}")
        return False

def rotate_proxy():
    """Get random proxy from pool"""
    global PROXY_LIST
    
    if not PROXY_LIST:
        if not get_free_proxies():
            return None
    
    if PROXY_LIST:
        return random.choice(PROXY_LIST)
    return None

def yahoo_with_proxy(ticker, period="10d", interval="1d", max_retries=3):
    """
    Download data using rotating proxies
    
    Args:
        ticker: Stock symbol
        period: Data period  
        interval: Data interval
        max_retries: Maximum proxy attempts
        
    Returns:
        pandas.DataFrame or empty DataFrame
    """
    
    for attempt in range(max_retries):
        try:
            proxy = rotate_proxy()
            if not proxy:
                print(f"⚠️ No proxy available for attempt {attempt + 1}")
                continue
            
            print(f"🔄 Trying proxy {attempt + 1}/{max_retries}: {proxy}")
            
            # Create session with proxy
            session = requests.Session()
            session.proxies.update({
                "http": proxy,
                "https": proxy
            })
            
            # Set timeout for proxy requests
            session.timeout = 10
            
            # Create custom yfinance ticker with proxy session
            ticker_obj = yf.Ticker(ticker, session=session)
            
            # Download with proxy
            df = ticker_obj.history(
                period=period,
                interval=interval,
                auto_adjust=False,
                prepost=False,
                threads=False
            )
            
            if not df.empty:
                print(f"✅ Proxy success: {ticker} via {proxy}")
                return df
            else:
                print(f"❌ Empty data via proxy {proxy}")
                
        except Exception as e:
            print(f"❌ Proxy {proxy} failed: {e}")
            # Remove failed proxy from list
            if proxy in PROXY_LIST:
                PROXY_LIST.remove(proxy)
            continue
    
    print(f"💥 All {max_retries} proxy attempts failed for {ticker}")
    return pd.DataFrame()

def enhanced_download_with_fallback(ticker, period="10d", interval="1d", use_proxy=False):
    """
    Enhanced download with multiple fallback options
    
    Priority:
    1. Direct Yahoo Finance
    2. Proxy rotation (if enabled)
    3. Finnhub fallback
    
    Args:
        ticker: Stock symbol
        period: Data period
        interval: Data interval
        use_proxy: Enable proxy fallback
        
    Returns:
        pandas.DataFrame
    """
    
    # Try direct Yahoo first
    try:
        print(f"🌐 Direct Yahoo attempt: {ticker}")
        df = yf.download(
            ticker,
            period=period,
            interval=interval,
            progress=False,
            threads=False,
            timeout=10
        )
        
        if not df.empty:
            print(f"✅ Direct Yahoo success: {ticker}")
            return df
            
    except Exception as e:
        print(f"❌ Direct Yahoo failed: {e}")
    
    # Try proxy rotation if enabled
    if use_proxy:
        try:
            print(f"🔄 Trying proxy fallback: {ticker}")
            df = yahoo_with_proxy(ticker, period, interval)
            if not df.empty:
                return df
        except Exception as e:
            print(f"❌ Proxy fallback failed: {e}")
    
    # Final fallback: return empty (Finnhub handled in main loader)
    print(f"💥 All Yahoo methods failed for {ticker}")
    return pd.DataFrame()

def test_proxy_system():
    """Test proxy system functionality"""
    print("🧪 Testing proxy system...")
    
    try:
        # Test proxy fetching
        if get_free_proxies():
            print(f"✅ Proxy system working: {len(PROXY_LIST)} proxies")
            
            # Test with a simple ticker
            df = yahoo_with_proxy("AAPL", period="5d", max_retries=2)
            if not df.empty:
                print(f"✅ Proxy download test successful: {len(df)} rows")
                return True
            else:
                print("❌ Proxy download test failed")
                return False
        else:
            print("❌ Proxy system not available")
            return False
            
    except Exception as e:
        print(f"❌ Proxy test failed: {e}")
        return False