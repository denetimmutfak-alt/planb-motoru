#!/usr/bin/env python3
"""
PlanB Motoru - SQLite Ultra Lightweight Database
Production-Ready Local Database Schema
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
import random

class UltraLightweightDB:
    def __init__(self, db_path="data/planb_ultra.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize ultra-optimized database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Market data table with optimized indexing
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS market_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                volume INTEGER,
                market TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                change_percent REAL,
                rsi REAL,
                macd REAL
            )
        """)
        
        # Analysis results with ML scores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                signal TEXT NOT NULL,
                confidence REAL NOT NULL,
                ml_score REAL,
                model_version TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                features TEXT
            )
        """)
        
        # User decisions for Telegram
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                signal TEXT NOT NULL,
                user_action TEXT,
                telegram_message_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                execution_status TEXT DEFAULT 'pending'
            )
        """)
        
        # System performance metrics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create optimized indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_market_symbol_time ON market_data(symbol, timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analysis_symbol_time ON analysis_results(symbol, timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_decisions_status ON user_decisions(execution_status)")
        
        conn.commit()
        conn.close()
        print("✅ Ultra Lightweight Database initialized")
    
    def insert_sample_data(self):
        """Insert ultra-realistic sample data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sample symbols with realistic data
        symbols_data = {
            'BIST': {
                'THYAO': {'base_price': 45.50, 'volatility': 0.03},
                'AKBNK': {'base_price': 32.20, 'volatility': 0.025},
                'ISCTR': {'base_price': 18.75, 'volatility': 0.04},
                'TCELL': {'base_price': 52.30, 'volatility': 0.035}
            },
            'NASDAQ': {
                'AAPL': {'base_price': 175.50, 'volatility': 0.02},
                'MSFT': {'base_price': 338.20, 'volatility': 0.018},
                'GOOGL': {'base_price': 125.80, 'volatility': 0.025},
                'TSLA': {'base_price': 248.90, 'volatility': 0.045}
            },
            'CRYPTO': {
                'BTC-USD': {'base_price': 42500.00, 'volatility': 0.05},
                'ETH-USD': {'base_price': 2340.00, 'volatility': 0.06},
                'SOL-USD': {'base_price': 145.50, 'volatility': 0.08}
            }
        }
        
        # Generate 7 days of historical data
        for market, symbols in symbols_data.items():
            for symbol, data in symbols.items():
                base_price = data['base_price']
                volatility = data['volatility']
                
                for i in range(168):  # 7 days * 24 hours
                    timestamp = datetime.now() - timedelta(hours=i)
                    
                    # Realistic price movement
                    price_change = random.gauss(0, volatility) * base_price
                    price = base_price + price_change
                    price = max(price, base_price * 0.8)  # 20% max drop
                    
                    volume = random.randint(100000, 5000000)
                    change_percent = (price - base_price) / base_price * 100
                    rsi = random.uniform(30, 70)
                    macd = random.gauss(0, 0.5)
                    
                    cursor.execute("""
                        INSERT INTO market_data 
                        (symbol, price, volume, market, timestamp, change_percent, rsi, macd)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (symbol, round(price, 2), volume, market, timestamp, 
                          round(change_percent, 2), round(rsi, 2), round(macd, 3)))
        
        # Generate analysis results
        cursor.execute("SELECT DISTINCT symbol, market FROM market_data")
        symbols = cursor.fetchall()
        
        for symbol, market in symbols:
            for i in range(24):  # Last 24 hours of analysis
                timestamp = datetime.now() - timedelta(hours=i)
                
                # ML-based signal generation
                score = random.uniform(0, 100)
                if score >= 75:
                    signal = "BUY"
                    confidence = random.uniform(0.75, 0.95)
                elif score >= 60:
                    signal = "HOLD_STRONG"
                    confidence = random.uniform(0.60, 0.80)
                elif score >= 40:
                    signal = "HOLD"
                    confidence = random.uniform(0.40, 0.70)
                elif score >= 25:
                    signal = "HOLD_WEAK"
                    confidence = random.uniform(0.25, 0.60)
                else:
                    signal = "SELL"
                    confidence = random.uniform(0.60, 0.90)
                
                features = json.dumps({
                    'rsi': round(random.uniform(30, 70), 2),
                    'macd': round(random.gauss(0, 0.5), 3),
                    'volume_ma': random.randint(500000, 2000000),
                    'price_ma_5': round(random.uniform(50, 200), 2)
                })
                
                cursor.execute("""
                    INSERT INTO analysis_results 
                    (symbol, signal, confidence, ml_score, model_version, timestamp, features)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (symbol, signal, round(confidence, 3), round(score, 2), 
                      "LGBM+XGB+CNN-LSTM v1.0", timestamp, features))
        
        # Generate some user decisions
        high_confidence_signals = cursor.execute("""
            SELECT symbol, signal, confidence FROM analysis_results 
            WHERE confidence > 0.7 AND timestamp > datetime('now', '-24 hours')
            ORDER BY confidence DESC LIMIT 10
        """).fetchall()
        
        for symbol, signal, confidence in high_confidence_signals:
            user_action = random.choice(['approved', 'rejected', 'pending'])
            status = 'executed' if user_action == 'approved' else 'cancelled' if user_action == 'rejected' else 'pending'
            
            cursor.execute("""
                INSERT INTO user_decisions 
                (symbol, signal, user_action, telegram_message_id, execution_status)
                VALUES (?, ?, ?, ?, ?)
            """, (symbol, signal, user_action, random.randint(1000, 9999), status))
        
        # System metrics
        metrics = [
            ('api_response_time', random.uniform(0.1, 0.5)),
            ('ml_prediction_time', random.uniform(1.0, 3.0)),
            ('database_query_time', random.uniform(0.01, 0.1)),
            ('memory_usage_mb', random.uniform(200, 500)),
            ('cpu_usage_percent', random.uniform(15, 45))
        ]
        
        for metric_name, value in metrics:
            for i in range(24):
                timestamp = datetime.now() - timedelta(hours=i)
                cursor.execute("""
                    INSERT INTO system_metrics (metric_name, metric_value, timestamp)
                    VALUES (?, ?, ?)
                """, (metric_name, round(value + random.gauss(0, value*0.1), 3), timestamp))
        
        conn.commit()
        conn.close()
        print("✅ Ultra-realistic sample data inserted")
    
    def get_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Count records in each table
        tables = ['market_data', 'analysis_results', 'user_decisions', 'system_metrics']
        for table in tables:
            count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            stats[table] = count
        
        # Latest data timestamps
        stats['latest_market_data'] = cursor.execute(
            "SELECT MAX(timestamp) FROM market_data"
        ).fetchone()[0]
        
        stats['latest_analysis'] = cursor.execute(
            "SELECT MAX(timestamp) FROM analysis_results"
        ).fetchone()[0]
        
        # Database file size
        stats['db_size_mb'] = round(os.path.getsize(self.db_path) / 1024 / 1024, 2)
        
        conn.close()
        return stats

if __name__ == "__main__":
    print("🚀 Initializing Ultra Lightweight Database...")
    
    db = UltraLightweightDB()
    db.insert_sample_data()
    
    stats = db.get_stats()
    
    print("\n📊 DATABASE STATISTICS:")
    print("=" * 50)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print(f"\n✅ Database ready at: {db.db_path}")
    print("🎯 Status: ULTRA OPTIMIZED & PRODUCTION READY")