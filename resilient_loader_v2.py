import os
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

def is_finnhub_supported(ticker):
    """Check if ticker is supported by Finnhub"""
    # Finnhub primarily supports US stocks and some international
    # BIST (.IS), ASX (.AX), TSX (.TO) not well supported
    unsupported_exchanges = ['.IS', '.TO', '.AX', '.L', '.PA', '.DE', '.HK']
    
    for exchange in unsupported_exchanges:
        if ticker.endswith(exchange):
            return False
    
    # If no exchange suffix or US ticker, likely supported
    return True

def cached_download(ticker, period="10d", interval="1d", ttl=172800):  # 2 gün TTL
    """
    Enhanced resilient data loader v2 with parquet cache
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'THYAO.IS')
        period: Data period (e.g., '10d', '1mo')
        interval: Data interval (e.g., '1d', '1h')
        ttl: Cache time-to-live in seconds (default 2 days = 172800)
    
    Returns:
        pandas.DataFrame with OHLCV data
    """
    
    # Generate cache key
    key = hash_key(ticker, period, interval)
    cache_path = os.path.join(CACHE_DIR, f"{key}.parquet")
    
    # Check parquet cache first (3-4x faster than pickle)
    if os.path.isfile(cache_path):
        mod_time = os.path.getmtime(cache_path)
        if time.time() - mod_time < ttl:
            try:
                cached_df = pd.read_parquet(cache_path)
                if not cached_df.empty:
                    print(f"📦 Parquet cache hit: {ticker}")
                    return cached_df
            except Exception as e:
                print(f"⚠️ Parquet cache read error for {ticker}: {e}")
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
            # Save to parquet cache (faster + smaller)
            try:
                df.to_parquet(cache_path, compression="zstd", engine="pyarrow")
                print(f"✅ Yahoo success: {ticker} ({len(df)} rows) → Parquet cached")
            except Exception as e:
                print(f"⚠️ Parquet cache save error: {e}")
            return df
        else:
            raise ValueError(f"Empty data from Yahoo for {ticker}")
            
    except Exception as e:
        print(f"❌ Yahoo failed for {ticker}: {e}")
        
        # Try Finnhub fallback (only for supported markets)
        if finnhub_client and FINNHUB_AVAILABLE and is_finnhub_supported(ticker):
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
                
                # Clean ticker for Finnhub (remove exchange suffix)
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
                    
                    # Save to parquet cache
                    try:
                        df.to_parquet(cache_path, compression="zstd", engine="pyarrow")
                        print(f"✅ Finnhub success: {ticker} ({len(df)} rows) → Parquet cached")
                    except Exception as e:
                        print(f"⚠️ Parquet cache save error: {e}")
                        
                    return df
                else:
                    raise ValueError(f"Invalid Finnhub response for {clean_ticker}")
                    
            except Exception as e:
                print(f"❌ Finnhub failed for {ticker}: {e}")
    
    # Both sources failed, return empty DataFrame
    print(f"💥 All sources failed for {ticker}")
    return pd.DataFrame()

def download_batch(tickers, period="10d", interval="1d", ttl=172800):
    """
    Download multiple tickers with enhanced parquet caching
    
    Args:
        tickers: List of ticker symbols
        period: Data period
        interval: Data interval  
        ttl: Cache TTL in seconds (2 days default)
        
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
        print(f"✅ Parquet cache cleared: {CACHE_DIR}")
    except Exception as e:
        print(f"❌ Cache clear error: {e}")

def cache_stats():
    """Show enhanced cache statistics"""
    try:
        files = os.listdir(CACHE_DIR)
        total_size = sum(os.path.getsize(os.path.join(CACHE_DIR, f)) for f in files)
        parquet_files = [f for f in files if f.endswith('.parquet')]
        pickle_files = [f for f in files if f.endswith('.pkl')]
        
        print(f"📊 Cache stats: {len(files)} files, {total_size/1024/1024:.1f} MB")
        print(f"  - Parquet: {len(parquet_files)} files (new format)")
        print(f"  - Pickle: {len(pickle_files)} files (legacy)")
        
        return len(files), total_size
    except Exception as e:
        print(f"❌ Cache stats error: {e}")
        return 0, 0

def migrate_cache():
    """Migrate old pickle cache to parquet format"""
    try:
        import pickle
        files = os.listdir(CACHE_DIR)
        pickle_files = [f for f in files if f.endswith('.pkl')]
        
        migrated = 0
        for pkl_file in pickle_files:
            try:
                pkl_path = os.path.join(CACHE_DIR, pkl_file)
                parquet_path = pkl_path.replace('.pkl', '.parquet')
                
                # Load from pickle
                df = pickle.load(open(pkl_path, "rb"))
                
                # Save as parquet
                df.to_parquet(parquet_path, compression="zstd", engine="pyarrow")
                
                # Remove old pickle
                os.remove(pkl_path)
                migrated += 1
                
            except Exception as e:
                print(f"⚠️ Migration failed for {pkl_file}: {e}")
        
        print(f"✅ Migrated {migrated} files from pickle to parquet")
        return migrated
        
    except Exception as e:
        print(f"❌ Cache migration error: {e}")
        return 0