#!/usr/bin/env python3
"""
Real-Time Market Data Collector
Polygon/Tiingo (stocks) + Binance (crypto) data feeds
15-minute periodic analysis trigger
"""

import asyncio
import logging
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
from dataclasses import dataclass, asdict
import psycopg2
from psycopg2.extras import RealDictCursor
import redis
import aiohttp
import time

# Market data providers
try:
    from polygon import RESTClient as PolygonClient
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False

try:
    from binance.client import Client as BinanceClient
    BINANCE_AVAILABLE = True
except ImportError:
    BINANCE_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class MarketDataPoint:
    """Market data standardized format"""
    timestamp: datetime
    symbol: str
    market: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: Optional[float] = None

class PolygonDataProvider:
    """Polygon.io data provider for stocks"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = PolygonClient(api_key) if POLYGON_AVAILABLE else None
        
    async def get_realtime_data(self, symbols: List[str]) -> List[MarketDataPoint]:
        """Get real-time stock data"""
        data_points = []
        
        if not self.client:
            logger.warning("Polygon client not available")
            return data_points
            
        try:
            for symbol in symbols:
                # Get current day's data
                bars = self.client.get_aggs(
                    ticker=symbol,
                    multiplier=1,
                    timespan="minute",
                    from_=datetime.now().strftime("%Y-%m-%d"),
                    to=datetime.now().strftime("%Y-%m-%d")
                )
                
                for bar in bars:
                    data_point = MarketDataPoint(
                        timestamp=datetime.fromtimestamp(bar.timestamp / 1000),
                        symbol=symbol,
                        market="BIST" if symbol.endswith(".IS") else "NASDAQ",
                        open=bar.open,
                        high=bar.high,
                        low=bar.low,
                        close=bar.close,
                        volume=bar.volume,
                        adjusted_close=bar.close
                    )
                    data_points.append(data_point)
                    
        except Exception as e:
            logger.error(f"Polygon data fetch error: {e}")
            
        return data_points

class BinanceDataProvider:
    """Binance data provider for crypto"""
    
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.client = BinanceClient(api_key, secret_key) if BINANCE_AVAILABLE else None
        
    async def get_realtime_data(self, symbols: List[str]) -> List[MarketDataPoint]:
        """Get real-time crypto data"""
        data_points = []
        
        if not self.client:
            logger.warning("Binance client not available")
            return data_points
            
        try:
            # Get 24hr ticker statistics
            tickers = self.client.get_ticker()
            
            for ticker in tickers:
                if ticker['symbol'] in symbols:
                    # Get recent klines (candlestick data)
                    klines = self.client.get_klines(
                        symbol=ticker['symbol'],
                        interval='1m',
                        limit=1
                    )
                    
                    if klines:
                        kline = klines[0]
                        data_point = MarketDataPoint(
                            timestamp=datetime.fromtimestamp(kline[0] / 1000),
                            symbol=ticker['symbol'],
                            market="CRYPTO",
                            open=float(kline[1]),
                            high=float(kline[2]),
                            low=float(kline[3]),
                            close=float(kline[4]),
                            volume=int(float(kline[5])),
                            adjusted_close=float(kline[4])
                        )
                        data_points.append(data_point)
                        
        except Exception as e:
            logger.error(f"Binance data fetch error: {e}")
            
        return data_points

class DatabaseManager:
    """PostgreSQL/TimescaleDB manager"""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        
    def save_market_data(self, data_points: List[MarketDataPoint]):
        """Save market data to TimescaleDB hypertable"""
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    for point in data_points:
                        cur.execute("""
                            INSERT INTO market_data 
                            (timestamp, symbol, market, open, high, low, close, volume, adjusted_close)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (timestamp, symbol) DO UPDATE SET
                            open = EXCLUDED.open,
                            high = EXCLUDED.high,
                            low = EXCLUDED.low,
                            close = EXCLUDED.close,
                            volume = EXCLUDED.volume,
                            adjusted_close = EXCLUDED.adjusted_close
                        """, (
                            point.timestamp,
                            point.symbol,
                            point.market,
                            point.open,
                            point.high,
                            point.low,
                            point.close,
                            point.volume,
                            point.adjusted_close
                        ))
                    conn.commit()
                    logger.info(f"Saved {len(data_points)} market data points")
                    
        except Exception as e:
            logger.error(f"Database save error: {e}")
    
    def get_symbols_for_analysis(self) -> Dict[str, List[str]]:
        """Get symbols that need analysis"""
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Most active symbols from last 24h
                    cur.execute("""
                        SELECT symbol, market, COUNT(*) as data_points
                        FROM market_data 
                        WHERE timestamp >= NOW() - INTERVAL '24 hours'
                        GROUP BY symbol, market
                        HAVING COUNT(*) >= 10
                        ORDER BY data_points DESC
                        LIMIT 50
                    """)
                    
                    results = cur.fetchall()
                    symbols_by_market = {}
                    
                    for row in results:
                        market = row['market']
                        if market not in symbols_by_market:
                            symbols_by_market[market] = []
                        symbols_by_market[market].append(row['symbol'])
                    
                    return symbols_by_market
                    
        except Exception as e:
            logger.error(f"Get symbols error: {e}")
            return {}

class ParquetArchiver:
    """Raw data archival to Parquet files"""
    
    def __init__(self, data_path: str = "/app/data/raw"):
        self.data_path = data_path
        os.makedirs(data_path, exist_ok=True)
        
    def archive_daily_data(self, date: datetime):
        """Archive day's data to Parquet"""
        try:
            db_url = os.getenv('DATABASE_URL')
            with psycopg2.connect(db_url) as conn:
                # Query day's data
                query = """
                    SELECT * FROM market_data 
                    WHERE DATE(timestamp) = %s
                    ORDER BY timestamp, symbol
                """
                df = pd.read_sql(query, conn, params=[date.date()])
                
                if len(df) > 0:
                    # Save to Parquet
                    filename = f"market_data_{date.strftime('%Y-%m-%d')}.parquet"
                    filepath = os.path.join(self.data_path, filename)
                    df.to_parquet(filepath, compression='snappy', index=False)
                    
                    logger.info(f"Archived {len(df)} records to {filename}")
                    
        except Exception as e:
            logger.error(f"Parquet archive error: {e}")

class RealTimeDataCollector:
    """Main real-time data collection orchestrator"""
    
    def __init__(self):
        # Environment variables
        self.polygon_api_key = os.getenv('POLYGON_API_KEY')
        self.tiingo_api_key = os.getenv('TIINGO_API_KEY')
        self.binance_api_key = os.getenv('BINANCE_API_KEY')
        self.binance_secret = os.getenv('BINANCE_SECRET_KEY')
        self.db_url = os.getenv('DATABASE_URL')
        self.redis_url = os.getenv('REDIS_URL')
        
        # Data providers
        self.polygon_provider = PolygonDataProvider(self.polygon_api_key) if self.polygon_api_key else None
        self.binance_provider = BinanceDataProvider(
            self.binance_api_key, 
            self.binance_secret
        ) if self.binance_api_key and self.binance_secret else None
        
        # Database and cache
        self.db_manager = DatabaseManager(self.db_url) if self.db_url else None
        self.redis_client = redis.from_url(self.redis_url) if self.redis_url else None
        self.parquet_archiver = ParquetArchiver()
        
        # Collection intervals
        self.data_collection_interval = 60  # 1 minute
        self.analysis_trigger_interval = 15 * 60  # 15 minutes
        
        # Symbol lists
        self.stock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']  # Top US stocks
        self.crypto_symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT']  # Top crypto
        
    async def collect_market_data(self):
        """Collect market data from all providers"""
        all_data_points = []
        
        # Collect stock data
        if self.polygon_provider:
            stock_data = await self.polygon_provider.get_realtime_data(self.stock_symbols)
            all_data_points.extend(stock_data)
            
        # Collect crypto data
        if self.binance_provider:
            crypto_data = await self.binance_provider.get_realtime_data(self.crypto_symbols)
            all_data_points.extend(crypto_data)
            
        # Save to database
        if self.db_manager and all_data_points:
            self.db_manager.save_market_data(all_data_points)
            
        # Cache latest data in Redis
        if self.redis_client and all_data_points:
            for point in all_data_points:
                key = f"latest_data:{point.symbol}"
                self.redis_client.setex(
                    key, 
                    300,  # 5 minute TTL
                    json.dumps(asdict(point), default=str)
                )
        
        logger.info(f"Collected {len(all_data_points)} data points")
        return all_data_points
    
    async def trigger_analysis(self):
        """Trigger analysis for collected data"""
        try:
            if not self.db_manager:
                return
                
            # Get symbols that need analysis
            symbols_by_market = self.db_manager.get_symbols_for_analysis()
            
            # Trigger analysis for each symbol via Redis
            if self.redis_client:
                for market, symbols in symbols_by_market.items():
                    for symbol in symbols:
                        analysis_request = {
                            'symbol': symbol,
                            'market': market,
                            'timestamp': datetime.now().isoformat(),
                            'trigger': 'scheduled_analysis'
                        }
                        
                        # Push to analysis queue
                        self.redis_client.lpush(
                            'analysis_queue',
                            json.dumps(analysis_request)
                        )
                        
                logger.info(f"Triggered analysis for {sum(len(symbols) for symbols in symbols_by_market.values())} symbols")
                
        except Exception as e:
            logger.error(f"Analysis trigger error: {e}")
    
    async def health_check(self):
        """Health check endpoint data"""
        status = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'providers': {
                'polygon': self.polygon_provider is not None,
                'binance': self.binance_provider is not None
            },
            'database': self.db_manager is not None,
            'redis': self.redis_client is not None,
            'last_collection': getattr(self, 'last_collection_time', None)
        }
        return status
    
    async def run_collection_cycle(self):
        """Single collection cycle"""
        try:
            start_time = time.time()
            
            # Collect data
            data_points = await self.collect_market_data()
            
            # Update last collection time
            self.last_collection_time = datetime.now().isoformat()
            
            collection_time = time.time() - start_time
            logger.info(f"Collection cycle completed in {collection_time:.2f} seconds")
            
            return len(data_points)
            
        except Exception as e:
            logger.error(f"Collection cycle error: {e}")
            return 0
    
    async def run_analysis_cycle(self):
        """Analysis trigger cycle"""
        try:
            await self.trigger_analysis()
            logger.info("Analysis cycle completed")
        except Exception as e:
            logger.error(f"Analysis cycle error: {e}")
    
    async def run_archive_cycle(self):
        """Daily archival cycle"""
        try:
            yesterday = datetime.now() - timedelta(days=1)
            self.parquet_archiver.archive_daily_data(yesterday)
            logger.info("Archive cycle completed")
        except Exception as e:
            logger.error(f"Archive cycle error: {e}")
    
    async def start_collection_loop(self):
        """Main collection loop"""
        logger.info("Starting real-time data collection loop...")
        
        last_analysis_time = time.time()
        last_archive_time = time.time()
        
        while True:
            try:
                # Data collection (every minute)
                await self.run_collection_cycle()
                
                current_time = time.time()
                
                # Analysis trigger (every 15 minutes)
                if current_time - last_analysis_time >= self.analysis_trigger_interval:
                    await self.run_analysis_cycle()
                    last_analysis_time = current_time
                
                # Archive (once per day at 2 AM)
                hour = datetime.now().hour
                if hour == 2 and current_time - last_archive_time >= 86400:  # 24 hours
                    await self.run_archive_cycle()
                    last_archive_time = current_time
                
                # Wait until next collection
                await asyncio.sleep(self.data_collection_interval)
                
            except Exception as e:
                logger.error(f"Collection loop error: {e}")
                await asyncio.sleep(30)  # Wait 30 seconds on error

# Simple web server for health checks
from aiohttp import web, web_runner
import aiohttp

async def health_handler(request):
    """Health check endpoint"""
    collector = request.app['collector']
    health_data = await collector.health_check()
    return web.json_response(health_data)

async def metrics_handler(request):
    """Metrics endpoint"""
    # Simple metrics
    metrics = {
        'timestamp': datetime.now().isoformat(),
        'uptime_seconds': time.time() - request.app['start_time'],
        'status': 'running'
    }
    return web.json_response(metrics)

async def init_web_server(collector):
    """Initialize web server for health checks"""
    app = web.Application()
    app['collector'] = collector
    app['start_time'] = time.time()
    
    app.router.add_get('/health', health_handler)
    app.router.add_get('/metrics', metrics_handler)
    
    runner = web_runner.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', 8002)
    await site.start()
    
    logger.info("Health check server started on port 8002")

async def main():
    """Main function"""
    collector = RealTimeDataCollector()
    
    # Start health check server
    await init_web_server(collector)
    
    # Start data collection
    await collector.start_collection_loop()

if __name__ == "__main__":
    asyncio.run(main())
