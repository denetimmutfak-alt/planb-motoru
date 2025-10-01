#!/usr/bin/env python3
"""
PlanB Motoru - Ultra Market Data Pipeline
Real-time Data Collection & Feature Engineering
"""

import asyncio
import aiohttp
import sqlite3
import json
import time
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List
import random

class UltraMarketDataPipeline:
    def __init__(self):
        self.db_path = "data/planb_ultra.db"
        self.symbols = {
            'BIST': ['THYAO.IS', 'AKBNK.IS', 'ISCTR.IS', 'TCELL.IS', 'SAHOL.IS'],
            'NASDAQ': ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'AMZN'],
            'CRYPTO': ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD'],
            'FOREX': ['EURUSD=X', 'GBPUSD=X', 'USDJPY=X']
        }
        
    def get_db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        return conn
    
    async def fetch_real_data(self, symbol: str) -> Dict:
        """Fetch real market data for symbol"""
        try:
            # Use yfinance for real data
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d", interval="1m")
            
            if hist.empty:
                return None
            
            latest = hist.iloc[-1]
            
            # Calculate technical indicators
            rsi = self.calculate_rsi(hist['Close'].values)
            macd = self.calculate_macd(hist['Close'].values)
            
            return {
                'symbol': symbol.replace('.IS', '').replace('-USD', '').replace('=X', ''),
                'price': float(latest['Close']),
                'volume': int(latest['Volume']) if not pd.isna(latest['Volume']) else 0,
                'change_percent': float((latest['Close'] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2] * 100) if len(hist) > 1 else 0,
                'rsi': rsi,
                'macd': macd,
                'timestamp': datetime.now(),
                'market': self.get_market_for_symbol(symbol)
            }
            
        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")
            return None
    
    def calculate_rsi(self, prices: np.array, period: int = 14) -> float:
        """Calculate RSI indicator"""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return round(float(rsi), 2)
    
    def calculate_macd(self, prices: np.array) -> float:
        """Calculate MACD indicator"""
        if len(prices) < 26:
            return 0.0
        
        exp1 = pd.Series(prices).ewm(span=12).mean()
        exp2 = pd.Series(prices).ewm(span=26).mean()
        macd = exp1 - exp2
        
        return round(float(macd.iloc[-1]), 4)
    
    def get_market_for_symbol(self, symbol: str) -> str:
        """Determine market for symbol"""
        if '.IS' in symbol:
            return 'BIST'
        elif any(crypto in symbol for crypto in ['BTC', 'ETH', 'SOL', 'ADA']):
            return 'CRYPTO'
        elif '=X' in symbol:
            return 'FOREX'
        else:
            return 'NASDAQ'
    
    def store_market_data(self, data: Dict):
        """Store market data in database"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO market_data 
                (symbol, price, volume, market, timestamp, change_percent, rsi, macd)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['symbol'], data['price'], data['volume'], data['market'],
                data['timestamp'], data['change_percent'], data['rsi'], data['macd']
            ))
            
            conn.commit()
            print(f"✅ Stored: {data['symbol']} @ ${data['price']:.2f}")
            
        except Exception as e:
            print(f"❌ Store error for {data['symbol']}: {e}")
        finally:
            conn.close()
    
    async def run_ml_analysis(self, symbol: str, market_data: Dict):
        """Run ML analysis and generate signals"""
        try:
            # Prepare features for ML model
            features = {
                'rsi': market_data['rsi'],
                'macd': market_data['macd'],
                'price': market_data['price'],
                'volume': market_data['volume'],
                'price_change': market_data['change_percent']
            }
            
            # Call ML prediction API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'http://localhost:8001/api/v1/ml/predict',
                    json={'symbol': symbol, 'features': features},
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    if response.status == 200:
                        prediction = await response.json()
                        print(f"🤖 ML Prediction for {symbol}: {prediction['signal']} ({prediction['confidence']:.1%})")
                        
                        # If high confidence, trigger Telegram notification
                        if prediction['confidence'] > 0.75:
                            await self.send_high_confidence_alert(prediction)
                    else:
                        print(f"❌ ML API error for {symbol}: {response.status}")
                        
        except Exception as e:
            print(f"❌ ML Analysis error for {symbol}: {e}")
    
    async def send_high_confidence_alert(self, prediction: Dict):
        """Send high confidence signal alert"""
        # This would integrate with Telegram bot
        print(f"🚨 HIGH CONFIDENCE ALERT: {prediction['symbol']} - {prediction['signal']} ({prediction['confidence']:.1%})")
    
    async def collect_data_for_market(self, market: str):
        """Collect data for all symbols in a market"""
        symbols = self.symbols.get(market, [])
        
        print(f"📊 Collecting {market} data for {len(symbols)} symbols...")
        
        tasks = []
        for symbol in symbols:
            task = self.fetch_real_data(symbol)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results = [r for r in results if r is not None and not isinstance(r, Exception)]
        
        # Store valid results
        for data in valid_results:
            self.store_market_data(data)
            # Run ML analysis
            await self.run_ml_analysis(data['symbol'], data)
        
        print(f"✅ {market}: {len(valid_results)}/{len(symbols)} symbols processed")
        return len(valid_results)
    
    async def run_continuous_pipeline(self):
        """Run continuous data collection pipeline"""
        print("🚀 Starting Ultra Market Data Pipeline...")
        print("🔄 Continuous mode: Every 60 seconds")
        
        cycle_count = 0
        
        while True:
            try:
                cycle_count += 1
                start_time = time.time()
                
                print(f"\n🔄 Pipeline Cycle #{cycle_count} - {datetime.now().strftime('%H:%M:%S')}")
                
                # Collect data for all markets
                total_processed = 0
                for market in self.symbols.keys():
                    processed = await self.collect_data_for_market(market)
                    total_processed += processed
                    await asyncio.sleep(2)  # Rate limiting
                
                # Update system metrics
                self.update_system_metrics(total_processed, time.time() - start_time)
                
                print(f"✅ Cycle #{cycle_count} completed: {total_processed} symbols in {time.time() - start_time:.1f}s")
                
                # Wait for next cycle
                await asyncio.sleep(60)
                
            except KeyboardInterrupt:
                print("\n🛑 Pipeline stopped by user")
                break
            except Exception as e:
                print(f"❌ Pipeline error: {e}")
                await asyncio.sleep(30)  # Wait before retry
    
    def update_system_metrics(self, symbols_processed: int, cycle_time: float):
        """Update system performance metrics"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        try:
            metrics = [
                ('symbols_processed_per_cycle', symbols_processed),
                ('cycle_time_seconds', cycle_time),
                ('data_collection_rate', symbols_processed / cycle_time if cycle_time > 0 else 0)
            ]
            
            for metric_name, value in metrics:
                cursor.execute("""
                    INSERT INTO system_metrics (metric_name, metric_value, timestamp)
                    VALUES (?, ?, ?)
                """, (metric_name, value, datetime.now()))
            
            conn.commit()
            
        except Exception as e:
            print(f"❌ Metrics update error: {e}")
        finally:
            conn.close()
    
    async def run_single_cycle(self):
        """Run single data collection cycle for testing"""
        print("🧪 Running single test cycle...")
        
        total_processed = 0
        for market in self.symbols.keys():
            processed = await self.collect_data_for_market(market)
            total_processed += processed
        
        print(f"✅ Test cycle completed: {total_processed} symbols processed")
        return total_processed

if __name__ == "__main__":
    pipeline = UltraMarketDataPipeline()
    
    # Check if running single test or continuous
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        asyncio.run(pipeline.run_single_cycle())
    else:
        asyncio.run(pipeline.run_continuous_pipeline())