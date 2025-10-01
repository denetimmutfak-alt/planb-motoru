#!/usr/bin/env python3
"""
PlanB Motoru - Enhanced Database Initialization Script
Ultra-Comprehensive TimescaleDB Schema with Production Features
"""

import psycopg2
import os
import sys
from datetime import datetime, timedelta
import random
import json

class DatabaseInitializer:
    def __init__(self):
        self.connection_params = {
            'host': 'localhost',
            'port': 5433,
            'database': 'planb_test',
            'user': 'planb_user',
            'password': 'planb_secure_pass_2024'
        }
        
    def connect(self):
        """Connect to database"""
        try:
            return psycopg2.connect(**self.connection_params)
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return None
    
    def create_extensions(self, conn):
        """Create required extensions"""
        try:
            with conn.cursor() as cur:
                # Enable TimescaleDB extension
                cur.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
                
                # Enable additional useful extensions
                cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
                cur.execute("CREATE EXTENSION IF NOT EXISTS \"pg_stat_statements\";")
                
            conn.commit()
            print("✅ Database extensions created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create extensions: {e}")
            return False

import psycopg2
import os
import sys
from datetime import datetime, timedelta
import random
import json

class DatabaseInitializer:
    def __init__(self):
        self.connection_params = {
            'host': 'localhost',
            'port': 5433,
            'database': 'planb_test',
            'user': 'planb_user',
            'password': 'planb_secure_pass_2024'
        }
        
    def connect(self):
        """Connect to database"""
        try:
            return psycopg2.connect(**self.connection_params)
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return None
    
    def create_extensions(self, conn):
        """Create required extensions"""
        try:
            with conn.cursor() as cur:
                # Enable TimescaleDB extension
                cur.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
                
                # Enable additional useful extensions
                cur.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
                cur.execute("CREATE EXTENSION IF NOT EXISTS \"pg_stat_statements\";")
                
            conn.commit()
            print("✅ Database extensions created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create extensions: {e}")
            return False
    
    def create_schema(self, conn):
        """Create database schema"""
        try:
            with conn.cursor() as cur:
                # Market data table with TimescaleDB hypertable
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS market_data (
                        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                        timestamp TIMESTAMPTZ NOT NULL,
                        symbol VARCHAR(20) NOT NULL,
                        market VARCHAR(20) NOT NULL,
                        open_price DECIMAL(15,6),
                        high_price DECIMAL(15,6),
                        low_price DECIMAL(15,6),
                        close_price DECIMAL(15,6),
                        volume BIGINT,
                        vwap DECIMAL(15,6),
                        created_at TIMESTAMPTZ DEFAULT NOW(),
                        CONSTRAINT market_data_symbol_timestamp_key UNIQUE (symbol, timestamp)
                    );
                """)
                
                # Create hypertable
                cur.execute("""
                    SELECT create_hypertable('market_data', 'timestamp', 
                                           chunk_time_interval => INTERVAL '1 day',
                                           if_not_exists => TRUE);
                """)
                
                # Analysis results table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS analysis_results (
                        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                        timestamp TIMESTAMPTZ NOT NULL,
                        symbol VARCHAR(20) NOT NULL,
                        analysis_type VARCHAR(50) NOT NULL,
                        score DECIMAL(5,2),
                        confidence DECIMAL(5,2),
                        signal VARCHAR(20),
                        technical_indicators JSONB,
                        fundamental_data JSONB,
                        ml_predictions JSONB,
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    );
                """)
                
                # Create hypertable for analysis results
                cur.execute("""
                    SELECT create_hypertable('analysis_results', 'timestamp',
                                           chunk_time_interval => INTERVAL '1 day',
                                           if_not_exists => TRUE);
                """)
                
                # Signals table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS signals (
                        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                        timestamp TIMESTAMPTZ NOT NULL,
                        symbol VARCHAR(20) NOT NULL,
                        signal_type VARCHAR(20) NOT NULL,
                        action VARCHAR(10) NOT NULL, -- BUY, SELL, HOLD
                        confidence DECIMAL(5,2),
                        price DECIMAL(15,6),
                        target_price DECIMAL(15,6),
                        stop_loss DECIMAL(15,6),
                        quantity INTEGER,
                        status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED, EXECUTED
                        ml_model_version VARCHAR(50),
                        analysis_details JSONB,
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    );
                """)
                
                # User decisions table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS user_decisions (
                        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                        signal_id UUID REFERENCES signals(id),
                        decision VARCHAR(20) NOT NULL, -- APPROVE, REJECT, MODIFY
                        decision_timestamp TIMESTAMPTZ NOT NULL,
                        user_id VARCHAR(100),
                        notes TEXT,
                        modified_quantity INTEGER,
                        modified_price DECIMAL(15,6),
                        telegram_message_id BIGINT,
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    );
                """)
                
                # Portfolio positions table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS portfolio_positions (
                        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                        symbol VARCHAR(20) NOT NULL,
                        quantity DECIMAL(15,6),
                        average_price DECIMAL(15,6),
                        current_value DECIMAL(15,6),
                        unrealized_pnl DECIMAL(15,6),
                        last_updated TIMESTAMPTZ DEFAULT NOW(),
                        created_at TIMESTAMPTZ DEFAULT NOW(),
                        CONSTRAINT portfolio_positions_symbol_key UNIQUE (symbol)
                    );
                """)
                
                # Trading transactions table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS trading_transactions (
                        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                        timestamp TIMESTAMPTZ NOT NULL,
                        signal_id UUID REFERENCES signals(id),
                        symbol VARCHAR(20) NOT NULL,
                        action VARCHAR(10) NOT NULL, -- BUY, SELL
                        quantity DECIMAL(15,6),
                        price DECIMAL(15,6),
                        total_value DECIMAL(15,6),
                        fees DECIMAL(15,6),
                        broker VARCHAR(50),
                        order_id VARCHAR(100),
                        status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, FILLED, CANCELLED, FAILED
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    );
                """)
                
                # Create hypertable for transactions
                cur.execute("""
                    SELECT create_hypertable('trading_transactions', 'timestamp',
                                           chunk_time_interval => INTERVAL '1 day',
                                           if_not_exists => TRUE);
                """)
                
                # Performance metrics table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS performance_metrics (
                        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                        timestamp TIMESTAMPTZ NOT NULL,
                        metric_type VARCHAR(50) NOT NULL,
                        metric_value DECIMAL(15,6),
                        period VARCHAR(20), -- DAILY, WEEKLY, MONTHLY, YEARLY
                        additional_data JSONB,
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    );
                """)
                
                # Create hypertable for performance metrics
                cur.execute("""
                    SELECT create_hypertable('performance_metrics', 'timestamp',
                                           chunk_time_interval => INTERVAL '1 day',
                                           if_not_exists => TRUE);
                """)
                
            conn.commit()
            print("✅ Database schema created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create schema: {e}")
            return False
    
    def create_indexes(self, conn):
        """Create performance indexes"""
        try:
            with conn.cursor() as cur:
                # Market data indexes
                cur.execute("CREATE INDEX IF NOT EXISTS idx_market_data_symbol ON market_data(symbol);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_market_data_market ON market_data(market);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_market_data_timestamp_symbol ON market_data(timestamp, symbol);")
                
                # Analysis results indexes
                cur.execute("CREATE INDEX IF NOT EXISTS idx_analysis_results_symbol ON analysis_results(symbol);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_analysis_results_timestamp ON analysis_results(timestamp);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_analysis_results_signal ON analysis_results(signal);")
                
                # Signals indexes
                cur.execute("CREATE INDEX IF NOT EXISTS idx_signals_symbol ON signals(symbol);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_signals_status ON signals(status);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_signals_timestamp ON signals(timestamp);")
                
                # Transactions indexes
                cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_symbol ON trading_transactions(symbol);")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON trading_transactions(timestamp);")
                
            conn.commit()
            print("✅ Database indexes created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create indexes: {e}")
            return False
    
    def insert_sample_data(self, conn):
        """Insert sample data for testing"""
        try:
            with conn.cursor() as cur:
                # Sample market data
                symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'ERCB.IS', 'THYAO.IS', 'BTC-USD', 'ETH-USD']
                markets = ['NASDAQ', 'NASDAQ', 'NASDAQ', 'NASDAQ', 'BIST', 'BIST', 'CRYPTO', 'CRYPTO']
                
                base_time = datetime.now() - timedelta(hours=24)
                
                for i in range(100):  # 100 sample records
                    timestamp = base_time + timedelta(minutes=i * 15)  # 15-minute intervals
                    
                    for symbol, market in zip(symbols, markets):
                        # Generate realistic price data
                        base_price = {'AAPL': 150, 'MSFT': 300, 'GOOGL': 2500, 'TSLA': 800, 
                                    'ERCB.IS': 25, 'THYAO.IS': 45, 'BTC-USD': 45000, 'ETH-USD': 3000}[symbol]
                        
                        price_variation = random.uniform(-0.05, 0.05)  # ±5% variation
                        close_price = base_price * (1 + price_variation)
                        open_price = close_price * (1 + random.uniform(-0.02, 0.02))
                        high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.02))
                        low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.02))
                        volume = random.randint(100000, 5000000)
                        
                        cur.execute("""
                            INSERT INTO market_data (timestamp, symbol, market, open_price, high_price, 
                                                   low_price, close_price, volume)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (symbol, timestamp) DO NOTHING
                        """, (timestamp, symbol, market, open_price, high_price, 
                             low_price, close_price, volume))
                
                # Sample analysis results
                for i in range(50):
                    timestamp = base_time + timedelta(minutes=i * 30)
                    symbol = random.choice(symbols)
                    
                    score = random.uniform(30, 95)
                    confidence = random.uniform(60, 95)
                    
                    if score >= 70:
                        signal = 'BUY'
                    elif score >= 50:
                        signal = 'HOLD'
                    else:
                        signal = 'SELL'
                    
                    technical_indicators = {
                        'rsi': random.uniform(20, 80),
                        'macd': random.uniform(-2, 2),
                        'bollinger_position': random.uniform(0, 1),
                        'volume_profile': random.uniform(0.5, 2.0)
                    }
                    
                    ml_predictions = {
                        'lgbm_score': random.uniform(0, 100),
                        'xgb_score': random.uniform(0, 100),
                        'lstm_prediction': random.uniform(-0.1, 0.1),
                        'ensemble_weight': random.uniform(0.7, 1.0)
                    }
                    
                    cur.execute("""
                        INSERT INTO analysis_results (timestamp, symbol, analysis_type, score, 
                                                    confidence, signal, technical_indicators, ml_predictions)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (timestamp, symbol, 'ULTRA_ANALYSIS', score, confidence, signal, 
                         json.dumps(technical_indicators), json.dumps(ml_predictions)))
                
                # Sample signals
                for i in range(20):
                    timestamp = base_time + timedelta(hours=i)
                    symbol = random.choice(symbols)
                    signal_type = random.choice(['BUY', 'SELL'])
                    
                    price = random.uniform(100, 1000)
                    confidence = random.uniform(70, 95)
                    
                    cur.execute("""
                        INSERT INTO signals (timestamp, symbol, signal_type, action, confidence, 
                                           price, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (timestamp, symbol, signal_type, signal_type, confidence, price, 'PENDING'))
                
            conn.commit()
            print("✅ Sample data inserted successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to insert sample data: {e}")
            return False
    
    def create_views(self, conn):
        """Create useful database views"""
        try:
            with conn.cursor() as cur:
                # Latest market data view
                cur.execute("""
                    CREATE OR REPLACE VIEW latest_market_data AS
                    SELECT DISTINCT ON (symbol) 
                        symbol, market, close_price as price, volume, timestamp
                    FROM market_data 
                    ORDER BY symbol, timestamp DESC;
                """)
                
                # Daily performance view
                cur.execute("""
                    CREATE OR REPLACE VIEW daily_performance AS
                    SELECT 
                        symbol,
                        date(timestamp) as date,
                        first(open_price, timestamp) as open_price,
                        max(high_price) as high_price,
                        min(low_price) as low_price,
                        last(close_price, timestamp) as close_price,
                        sum(volume) as total_volume,
                        count(*) as data_points
                    FROM market_data
                    GROUP BY symbol, date(timestamp)
                    ORDER BY symbol, date DESC;
                """)
                
                # Signal performance view
                cur.execute("""
                    CREATE OR REPLACE VIEW signal_performance AS
                    SELECT 
                        s.symbol,
                        s.signal_type,
                        s.confidence,
                        s.price as signal_price,
                        s.timestamp as signal_time,
                        s.status,
                        COALESCE(ud.decision, 'PENDING') as user_decision
                    FROM signals s
                    LEFT JOIN user_decisions ud ON s.id = ud.signal_id
                    ORDER BY s.timestamp DESC;
                """)
                
            conn.commit()
            print("✅ Database views created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create views: {e}")
            return False
    
    def setup_continuous_aggregates(self, conn):
        """Setup TimescaleDB continuous aggregates for performance"""
        try:
            with conn.cursor() as cur:
                # Hourly market data aggregates
                cur.execute("""
                    CREATE MATERIALIZED VIEW IF NOT EXISTS market_data_hourly
                    WITH (timescaledb.continuous) AS
                    SELECT 
                        time_bucket('1 hour', timestamp) AS hour,
                        symbol,
                        market,
                        first(open_price, timestamp) as open_price,
                        max(high_price) as high_price,
                        min(low_price) as low_price,
                        last(close_price, timestamp) as close_price,
                        sum(volume) as volume,
                        avg(close_price) as avg_price
                    FROM market_data
                    GROUP BY hour, symbol, market;
                """)
                
                # Daily analysis summary
                cur.execute("""
                    CREATE MATERIALIZED VIEW IF NOT EXISTS analysis_daily
                    WITH (timescaledb.continuous) AS
                    SELECT 
                        time_bucket('1 day', timestamp) AS day,
                        symbol,
                        avg(score) as avg_score,
                        avg(confidence) as avg_confidence,
                        count(*) as analysis_count,
                        count(CASE WHEN signal = 'BUY' THEN 1 END) as buy_signals,
                        count(CASE WHEN signal = 'SELL' THEN 1 END) as sell_signals,
                        count(CASE WHEN signal = 'HOLD' THEN 1 END) as hold_signals
                    FROM analysis_results
                    GROUP BY day, symbol;
                """)
                
            conn.commit()
            print("✅ Continuous aggregates created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create continuous aggregates: {e}")
            return False
    
    def initialize_database(self):
        """Main initialization function"""
        print("=" * 60)
        print("🚀 PLANB MOTORU - DATABASE INITIALIZATION")
        print("=" * 60)
        
        conn = self.connect()
        if not conn:
            return False
        
        try:
            success = True
            success &= self.create_extensions(conn)
            success &= self.create_schema(conn)
            success &= self.create_indexes(conn)
            success &= self.create_views(conn)
            success &= self.setup_continuous_aggregates(conn)
            success &= self.insert_sample_data(conn)
            
            if success:
                print("\n✅ Database initialization completed successfully!")
                print("📊 Database is ready for testing and development")
                
                # Show some statistics
                with conn.cursor() as cur:
                    cur.execute("SELECT count(*) FROM market_data;")
                    market_data_count = cur.fetchone()[0]
                    
                    cur.execute("SELECT count(*) FROM analysis_results;")
                    analysis_count = cur.fetchone()[0]
                    
                    cur.execute("SELECT count(*) FROM signals;")
                    signals_count = cur.fetchone()[0]
                
                print(f"📈 Sample data loaded:")
                print(f"   - Market data records: {market_data_count}")
                print(f"   - Analysis results: {analysis_count}")
                print(f"   - Signals: {signals_count}")
                
            else:
                print("\n❌ Database initialization failed!")
                
            return success
            
        finally:
            conn.close()

if __name__ == "__main__":
    initializer = DatabaseInitializer()
    initializer.initialize_database()