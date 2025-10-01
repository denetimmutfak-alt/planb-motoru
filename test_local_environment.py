#!/usr/bin/env python3
"""
PlanB Motoru - Local Environment Testing Script
Ultra-Comprehensive System Validation
"""

import requests
import psycopg2
import redis
import time
import json
import os
import sys
from datetime import datetime
import subprocess
import docker
from urllib.parse import urlparse

class EnvironmentTester:
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        
    def log_result(self, test_name, status, message="", details=None):
        """Log test result"""
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        self.results.append(result)
        
        # Color coded output
        color = '\033[92m' if status == 'PASS' else '\033[91m' if status == 'FAIL' else '\033[93m'
        reset = '\033[0m'
        print(f"{color}[{status}]{reset} {test_name}: {message}")
        
    def test_docker_services(self):
        """Test Docker services status"""
        try:
            client = docker.from_env()
            
            # Check if docker-compose.local.yml is running
            containers = client.containers.list()
            
            expected_services = [
                'planb_postgres_test',
                'planb_redis_test', 
                'planb_core_test',
                'planb_dashboard_test'
            ]
            
            running_services = [container.name for container in containers]
            
            for service in expected_services:
                if any(service in name for name in running_services):
                    self.log_result(f"Docker Service: {service}", "PASS", "Container running")
                else:
                    self.log_result(f"Docker Service: {service}", "FAIL", "Container not found")
                    
        except Exception as e:
            self.log_result("Docker Services", "FAIL", f"Docker not accessible: {e}")
    
    def test_database_connection(self):
        """Test PostgreSQL database connection"""
        try:
            # Test connection to local test database
            conn = psycopg2.connect(
                host='localhost',
                port=5433,
                database='planb_test',
                user='planb_user',
                password='planb_secure_pass_2024'
            )
            
            with conn.cursor() as cur:
                # Test basic query
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                
                # Test TimescaleDB extension
                cur.execute("SELECT installed_version FROM pg_available_extensions WHERE name = 'timescaledb';")
                timescale_version = cur.fetchone()
                
                if timescale_version:
                    self.log_result("TimescaleDB Extension", "PASS", f"Version: {timescale_version[0]}")
                else:
                    self.log_result("TimescaleDB Extension", "FAIL", "Extension not installed")
                
                # Test sample tables
                cur.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
                """)
                tables = [row[0] for row in cur.fetchall()]
                
                expected_tables = ['market_data', 'analysis_results', 'signals', 'user_decisions']
                for table in expected_tables:
                    if table in tables:
                        self.log_result(f"Database Table: {table}", "PASS", "Table exists")
                    else:
                        self.log_result(f"Database Table: {table}", "WARN", "Table not found")
            
            conn.close()
            self.log_result("Database Connection", "PASS", f"PostgreSQL: {version[:50]}")
            
        except Exception as e:
            self.log_result("Database Connection", "FAIL", f"Connection failed: {e}")
    
    def test_redis_connection(self):
        """Test Redis connection"""
        try:
            r = redis.Redis(host='localhost', port=6380, db=0, decode_responses=True)
            
            # Test basic operations
            test_key = f"health_check_{int(time.time())}"
            r.set(test_key, "test_value", ex=60)
            value = r.get(test_key)
            
            if value == "test_value":
                self.log_result("Redis Connection", "PASS", "Read/Write operations successful")
                
                # Get Redis info
                info = r.info()
                self.log_result("Redis Info", "PASS", 
                               f"Version: {info.get('redis_version')}, Memory: {info.get('used_memory_human')}")
            else:
                self.log_result("Redis Connection", "FAIL", "Read/Write test failed")
                
        except Exception as e:
            self.log_result("Redis Connection", "FAIL", f"Connection failed: {e}")
    
    def test_api_endpoints(self):
        """Test API endpoints"""
        endpoints = [
            ('Core API Health', 'http://localhost:8001/health'),
            ('Dashboard Health', 'http://localhost:9091/health'),
            ('Core API Root', 'http://localhost:8001/'),
            ('Dashboard Root', 'http://localhost:9091/')
        ]
        
        for name, url in endpoints:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    self.log_result(f"API Endpoint: {name}", "PASS", 
                                   f"Status: {response.status_code}, Response time: {response.elapsed.total_seconds():.2f}s")
                    
                    # Try to parse JSON response for health endpoints
                    if '/health' in url:
                        try:
                            health_data = response.json()
                            self.log_result(f"Health Data: {name}", "PASS", 
                                           f"Status: {health_data.get('status', 'unknown')}")
                        except:
                            pass
                else:
                    self.log_result(f"API Endpoint: {name}", "FAIL", 
                                   f"Status: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                self.log_result(f"API Endpoint: {name}", "FAIL", "Connection refused")
            except Exception as e:
                self.log_result(f"API Endpoint: {name}", "FAIL", f"Error: {e}")
    
    def test_market_data_pipeline(self):
        """Test market data pipeline"""
        try:
            # Test market data API endpoint
            response = requests.get('http://localhost:8001/api/v1/market-data/latest', timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    self.log_result("Market Data Pipeline", "PASS", 
                                   f"Retrieved {len(data)} market data entries")
                    
                    # Analyze first entry
                    first_entry = data[0]
                    required_fields = ['symbol', 'price', 'timestamp', 'market']
                    missing_fields = [field for field in required_fields if field not in first_entry]
                    
                    if not missing_fields:
                        self.log_result("Market Data Structure", "PASS", "All required fields present")
                    else:
                        self.log_result("Market Data Structure", "WARN", 
                                       f"Missing fields: {missing_fields}")
                else:
                    self.log_result("Market Data Pipeline", "WARN", "No data returned")
            else:
                self.log_result("Market Data Pipeline", "FAIL", f"API returned: {response.status_code}")
                
        except Exception as e:
            self.log_result("Market Data Pipeline", "FAIL", f"Error: {e}")
    
    def test_ml_ensemble(self):
        """Test ML Ensemble"""
        try:
            # Test ML prediction endpoint
            test_payload = {
                "symbol": "AAPL",
                "features": {
                    "price": 150.0,
                    "volume": 1000000,
                    "rsi": 65.0,
                    "macd": 0.5
                }
            }
            
            response = requests.post(
                'http://localhost:8001/api/v1/ml/predict',
                json=test_payload,
                timeout=30
            )
            
            if response.status_code == 200:
                prediction = response.json()
                if 'signal' in prediction and 'confidence' in prediction:
                    self.log_result("ML Ensemble", "PASS", 
                                   f"Signal: {prediction['signal']}, Confidence: {prediction['confidence']:.2f}")
                else:
                    self.log_result("ML Ensemble", "WARN", "Unexpected response format")
            else:
                self.log_result("ML Ensemble", "FAIL", f"API returned: {response.status_code}")
                
        except Exception as e:
            self.log_result("ML Ensemble", "FAIL", f"Error: {e}")
    
    def test_telegram_bot(self):
        """Test Telegram bot configuration"""
        try:
            # Check if Telegram bot environment variables are set
            bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
            chat_id = os.getenv('TELEGRAM_CHAT_ID')
            
            if bot_token and chat_id:
                self.log_result("Telegram Config", "PASS", "Bot token and chat ID configured")
                
                # Test bot status endpoint
                response = requests.get('http://localhost:8001/api/v1/telegram/status', timeout=10)
                if response.status_code == 200:
                    status = response.json()
                    self.log_result("Telegram Bot Status", "PASS", f"Status: {status.get('status', 'unknown')}")
                else:
                    self.log_result("Telegram Bot Status", "WARN", f"Status endpoint returned: {response.status_code}")
            else:
                self.log_result("Telegram Config", "WARN", "Bot token or chat ID not configured")
                
        except Exception as e:
            self.log_result("Telegram Bot", "FAIL", f"Error: {e}")
    
    def test_dependencies(self):
        """Test Python dependencies"""
        required_packages = [
            'fastapi', 'uvicorn', 'psycopg2', 'redis', 'pandas', 
            'numpy', 'scikit-learn', 'lightgbm', 'xgboost', 'tensorflow',
            'python-telegram-bot', 'yfinance', 'requests'
        ]
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                self.log_result(f"Package: {package}", "PASS", "Successfully imported")
            except ImportError:
                self.log_result(f"Package: {package}", "FAIL", "Import failed")
    
    def test_file_structure(self):
        """Test required file structure"""
        required_files = [
            'docker-compose.local.yml',
            'requirements.txt',
            'firefox_dashboard_server.py',
            'Dockerfile.dashboard',
            'config/settings.py',
            'src/core/api.py',
            'src/ml/ensemble.py'
        ]
        
        for file_path in required_files:
            full_path = os.path.join(os.getcwd(), file_path)
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                self.log_result(f"File: {file_path}", "PASS", f"Size: {size} bytes")
            else:
                self.log_result(f"File: {file_path}", "FAIL", "File not found")
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print("=" * 80)
        print("🚀 PLANB MOTORU - LOCAL ENVIRONMENT TESTING")
        print("=" * 80)
        print(f"⏰ Test started at: {self.start_time}")
        print()
        
        # Run all test categories
        self.test_file_structure()
        print()
        self.test_dependencies()
        print()
        self.test_docker_services()
        print()
        self.test_database_connection()
        print()
        self.test_redis_connection()
        print()
        self.test_api_endpoints()
        print()
        self.test_market_data_pipeline()
        print()
        self.test_ml_ensemble()
        print()
        self.test_telegram_bot()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.results if r['status'] == 'FAIL'])
        warned_tests = len([r for r in self.results if r['status'] == 'WARN'])
        
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        print(f"⏱️  Duration: {duration.total_seconds():.2f} seconds")
        print(f"📈 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {warned_tests}")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.results:
                if result['status'] == 'FAIL':
                    print(f"   ❌ {result['test']}: {result['message']}")
        
        if warned_tests > 0:
            print("\n⚠️  WARNINGS:")
            for result in self.results:
                if result['status'] == 'WARN':
                    print(f"   ⚠️  {result['test']}: {result['message']}")
        
        # Save detailed results
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'summary': {
                    'start_time': self.start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'duration_seconds': duration.total_seconds(),
                    'total_tests': total_tests,
                    'passed': passed_tests,
                    'failed': failed_tests,
                    'warnings': warned_tests,
                    'success_rate': (passed_tests/total_tests)*100
                },
                'detailed_results': self.results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        print("=" * 80)

if __name__ == "__main__":
    tester = EnvironmentTester()
    tester.run_comprehensive_test()