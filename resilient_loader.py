import os
import pickle
import hashlib
import time
import datetime as dt
import pandas as pd
import yfinance as yf

# Finnhub import (optional fallback)
try:
    import finnhub
    FINNHUB_AVAILABLE = True
except ImportError:
    FINNHUB_AVAILABLE = False
    print("⚠️ Finnhub not installed. Install with: pip install finnhub-python")

CACHE_DIR = "data/yf_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Initialize Finnhub client if available
finnhub_client = None
if FINNHUB_AVAILABLE:
    finnhub_key = os.getenv("FINNHUB_KEY")
    if finnhub_key:
        try:
            finnhub_client = finnhub.Client(api_key=finnhub_key)
            print("✅ Finnhub fallback activated")
        except:
            print("⚠️ Finnhub key invalid")

def hash_key(ticker, period, interval):
    """Create cache key hash"""
    return hashlib.md5(f"{ticker}_{period}_{interval}".encode()).hexdigest()

def cached_download(ticker, period="10d", interval="1d", ttl=3600):
    """
    Resilient data loader with cache + Finnhub fallback
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'THYAO.IS')
        period: Data period (e.g., '10d', '1mo')
        interval: Data interval (e.g., '1d', '1h')
        ttl: Cache time-to-live in seconds (default 1 hour)
    
    Returns:
        pandas.DataFrame with OHLCV data
    """
    
    # Generate cache key
    key = hash_key(ticker, period, interval)
    cache_path = os.path.join(CACHE_DIR, f"{key}.pkl")
    
    # Check cache first
    if os.path.isfile(cache_path):
        mod_time = os.path.getmtime(cache_path)
        if time.time() - mod_time < ttl:
            try:
                cached_df = pickle.load(open(cache_path, "rb"))
                if not cached_df.empty:
                    print(f"📦 Cache hit: {ticker}")
                    return cached_df
            except Exception as e:
                print(f"⚠️ Cache read error for {ticker}: {e}")
                # Continue to fresh download
    
    # Try Yahoo Finance first
    try:
        print(f"🌐 Downloading {ticker} from Yahoo...")
        df = yf.download(
            ticker, 
            period=period, 
            interval=interval, 
            progress=False, 
            threads=False,
            timeout=10
        )
        
        if not df.empty and len(df) > 0:
            # Save to cache
            try:
                pickle.dump(df, open(cache_path, "wb"))
                print(f"✅ Yahoo success: {ticker} ({len(df)} rows)")
            except Exception as e:
                print(f"⚠️ Cache save error: {e}")
            return df
        else:
            raise ValueError(f"Empty data from Yahoo for {ticker}")
            
    except Exception as e:
        print(f"❌ Yahoo failed for {ticker}: {e}")
        
        # Try Finnhub fallback
        if finnhub_client and FINNHUB_AVAILABLE:
            try:
                print(f"🔄 Trying Finnhub fallback for {ticker}...")
                
                # Calculate timestamp range
                end = int(dt.datetime.now().timestamp())
                
                # Parse period (e.g., '10d' -> 10 days)
                if period.endswith('d'):
                    days = int(period[:-1])
                elif period.endswith('mo'):
                    days = int(period[:-2]) * 30
                elif period.endswith('y'):
                    days = int(period[:-1]) * 365
                else:
                    days = 10  # default
                
                start = int((dt.datetime.now() - dt.timedelta(days=days)).timestamp())
                
                # Clean ticker for Finnhub (remove .IS, .TO etc)
                clean_ticker = ticker.split('.')[0]
                
                # Get data from Finnhub
                data = finnhub_client.stock_candles(clean_ticker, 'D', start, end)
                
                if data and data.get('s') == 'ok' and data.get('c'):
                    # Convert to DataFrame
                    df = pd.DataFrame({
                        'Open': data['o'],
                        'High': data['h'], 
                        'Low': data['l'],
                        'Close': data['c'],
                        'Volume': data['v']
                    })
                    
                    # Set datetime index
                    df.index = pd.to_datetime(data['t'], unit='s')
                    df.index.name = 'Date'
                    
                    # Ensure proper column naming (yfinance compatible)
                    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    
                    # Save to cache
                    try:
                        pickle.dump(df, open(cache_path, "wb"))
                        print(f"✅ Finnhub success: {ticker} ({len(df)} rows)")
                    except Exception as e:
                        print(f"⚠️ Cache save error: {e}")
                        
                    return df
                else:
                    raise ValueError(f"Invalid Finnhub response for {clean_ticker}")
                    
            except Exception as e:
                print(f"❌ Finnhub failed for {ticker}: {e}")
    
    # Both sources failed, return empty DataFrame
    print(f"💥 All sources failed for {ticker}")
    return pd.DataFrame()

def download_batch(tickers, period="10d", interval="1d", ttl=3600):
    """
    Download multiple tickers with caching
    
    Args:
        tickers: List of ticker symbols
        period: Data period
        interval: Data interval  
        ttl: Cache TTL in seconds
        
    Returns:
        dict: {ticker: DataFrame}
    """
    results = {}
    
    for ticker in tickers:
        try:
            df = cached_download(ticker, period, interval, ttl)
            if not df.empty:
                results[ticker] = df
            else:
                print(f"⚠️ No data for {ticker}")
        except Exception as e:
            print(f"❌ Error downloading {ticker}: {e}")
            
    return results

def clear_cache():
    """Clear all cached data"""
    try:
        import shutil
        shutil.rmtree(CACHE_DIR)
        os.makedirs(CACHE_DIR, exist_ok=True)
        print(f"✅ Cache cleared: {CACHE_DIR}")
    except Exception as e:
        print(f"❌ Cache clear error: {e}")

def cache_stats():
    """Show cache statistics"""
    try:
        files = os.listdir(CACHE_DIR)
        total_size = sum(os.path.getsize(os.path.join(CACHE_DIR, f)) for f in files)
        print(f"📊 Cache stats: {len(files)} files, {total_size/1024/1024:.1f} MB")
        return len(files), total_size
    except Exception as e:
        print(f"❌ Cache stats error: {e}")
        return 0, 0