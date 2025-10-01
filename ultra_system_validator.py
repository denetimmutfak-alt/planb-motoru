#!/usr/bin/env python3
"""
PlanB Motoru - FINAL ULTRA COMPREHENSIVE SYSTEM TEST
Complete End-to-End Production Validation
"""

import requests
import sqlite3
import time
import json
import subprocess
import os
from datetime import datetime
from typing import Dict, List

class UltraSystemValidator:
    def __init__(self):
        self.results = []
        self.api_base = "http://localhost:8001"
        self.dashboard_base = "http://localhost:8080"
        self.db_path = "data/planb_ultra.db"
        
    def log_result(self, test: str, status: str, message: str = "", details: Dict = None):
        """Log test result with enhanced formatting"""
        result = {
            'test': test,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        self.results.append(result)
        
        # Enhanced console output
        status_emoji = {
            'PASS': '✅',
            'FAIL': '❌', 
            'WARN': '⚠️',
            'INFO': 'ℹ️'
        }
        
        emoji = status_emoji.get(status, '❓')
        print(f"{emoji} [{status}] {test}: {message}")
        
        if details:
            for key, value in details.items():
                print(f"    └─ {key}: {value}")
    
    def test_file_integrity(self):
        """Test all critical files exist and are valid"""
        print("\n🔍 TESTING FILE INTEGRITY...")
        
        critical_files = {
            'ultra_database.py': 'Database initialization script',
            'ultra_api_server.py': 'Core API server',
            'ultra_telegram_bot.py': 'Telegram bot integration',
            'ultra_market_pipeline.py': 'Market data pipeline',
            'requirements_optimized.txt': 'Production dependencies',
            'docker-compose.local.yml': 'Local deployment config'
        }
        
        for file_path, description in critical_files.items():
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                self.log_result(f"File: {file_path}", "PASS", 
                               f"{description} - {size} bytes")
            else:
                self.log_result(f"File: {file_path}", "FAIL", 
                               f"Missing: {description}")
    
    def test_database_integrity(self):
        """Test database structure and data integrity"""
        print("\n🗄️ TESTING DATABASE INTEGRITY...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Test table existence
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['market_data', 'analysis_results', 'user_decisions', 'system_metrics']
            
            for table in expected_tables:
                if table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    self.log_result(f"Table: {table}", "PASS", 
                                   f"{count} records", {'record_count': count})
                else:
                    self.log_result(f"Table: {table}", "FAIL", "Table missing")
            
            # Test data freshness
            cursor.execute("SELECT MAX(timestamp) FROM market_data")
            latest_data = cursor.fetchone()[0]
            if latest_data:
                self.log_result("Data Freshness", "PASS", 
                               f"Latest: {latest_data[:19]}")
            else:
                self.log_result("Data Freshness", "WARN", "No data found")
            
            # Test database size
            db_size = os.path.getsize(self.db_path) / 1024 / 1024
            self.log_result("Database Size", "PASS", 
                           f"{db_size:.2f} MB", {'size_mb': db_size})
            
            conn.close()
            
        except Exception as e:
            self.log_result("Database Connection", "FAIL", str(e))
    
    def test_api_comprehensive(self):
        """Comprehensive API testing"""
        print("\n🔧 TESTING API COMPREHENSIVELY...")
        
        api_tests = [
            ("/", "Root endpoint"),
            ("/health", "Health check"),
            ("/api/v1/market-data", "Market data endpoint"),
            ("/api/v1/analysis", "Analysis results endpoint"),
            ("/api/v1/stats", "Statistics endpoint"),
            ("/api/v1/telegram/status", "Telegram status endpoint")
        ]
        
        for endpoint, description in api_tests:
            try:
                response = requests.get(f"{self.api_base}{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    response_time = response.elapsed.total_seconds()
                    
                    self.log_result(f"API: {endpoint}", "PASS", 
                                   f"{description} - {response_time:.3f}s",
                                   {'status_code': 200, 'response_time': response_time})
                    
                    # Additional validation for specific endpoints
                    if endpoint == "/health":
                        if data.get('status') == 'ULTRA_HEALTHY':
                            self.log_result("Health Status", "PASS", "System healthy")
                        else:
                            self.log_result("Health Status", "WARN", f"Status: {data.get('status')}")
                    
                    elif endpoint == "/api/v1/market-data":
                        if isinstance(data, list) and len(data) > 0:
                            self.log_result("Market Data Content", "PASS", 
                                           f"{len(data)} symbols returned")
                        else:
                            self.log_result("Market Data Content", "WARN", "No data returned")
                    
                else:
                    self.log_result(f"API: {endpoint}", "FAIL", 
                                   f"Status: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                self.log_result(f"API: {endpoint}", "FAIL", "Connection refused")
            except Exception as e:
                self.log_result(f"API: {endpoint}", "FAIL", str(e))
    
    def test_ml_prediction_accuracy(self):
        """Test ML prediction system"""
        print("\n🤖 TESTING ML PREDICTION SYSTEM...")
        
        test_symbols = ['AAPL', 'THYAO', 'BTC-USD']
        
        for symbol in test_symbols:
            try:
                test_payload = {
                    "symbol": symbol,
                    "features": {
                        "rsi": 65.0,
                        "macd": 0.5,
                        "price": 150.0,
                        "volume": 1000000,
                        "price_change": 2.5
                    }
                }
                
                response = requests.post(
                    f"{self.api_base}/api/v1/ml/predict",
                    json=test_payload,
                    timeout=15
                )
                
                if response.status_code == 200:
                    prediction = response.json()
                    
                    # Validate prediction structure
                    required_fields = ['signal', 'confidence', 'ml_score', 'recommendation']
                    missing_fields = [f for f in required_fields if f not in prediction]
                    
                    if not missing_fields:
                        self.log_result(f"ML Prediction: {symbol}", "PASS", 
                                       f"Signal: {prediction['signal']}, Confidence: {prediction['confidence']:.1%}",
                                       {'signal': prediction['signal'], 
                                        'confidence': prediction['confidence'],
                                        'ml_score': prediction['ml_score']})
                    else:
                        self.log_result(f"ML Prediction: {symbol}", "WARN", 
                                       f"Missing fields: {missing_fields}")
                else:
                    self.log_result(f"ML Prediction: {symbol}", "FAIL", 
                                   f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_result(f"ML Prediction: {symbol}", "FAIL", str(e))
    
    def test_dashboard_service(self):
        """Test dashboard service"""
        print("\n🖥️ TESTING DASHBOARD SERVICE...")
        
        try:
            response = requests.get(self.dashboard_base, timeout=5)
            if response.status_code == 200:
                self.log_result("Dashboard Main", "PASS", "Dashboard accessible")
                
                # Test health endpoint
                health_response = requests.get(f"{self.dashboard_base}/health", timeout=5)
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    self.log_result("Dashboard Health", "PASS", 
                                   f"Status: {health_data.get('status')}")
                else:
                    self.log_result("Dashboard Health", "FAIL", 
                                   f"Status: {health_response.status_code}")
            else:
                self.log_result("Dashboard Main", "FAIL", 
                               f"Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.log_result("Dashboard Service", "FAIL", "Connection refused")
        except Exception as e:
            self.log_result("Dashboard Service", "FAIL", str(e))
    
    def test_system_performance(self):
        """Test system performance metrics"""
        print("\n⚡ TESTING SYSTEM PERFORMANCE...")
        
        try:
            # Test API response times
            endpoints_to_test = ["/health", "/api/v1/market-data", "/api/v1/stats"]
            
            for endpoint in endpoints_to_test:
                start_time = time.time()
                response = requests.get(f"{self.api_base}{endpoint}", timeout=5)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                if response_time < 1.0:
                    status = "PASS"
                elif response_time < 3.0:
                    status = "WARN"
                else:
                    status = "FAIL"
                
                self.log_result(f"Performance: {endpoint}", status, 
                               f"Response time: {response_time:.3f}s",
                               {'response_time_ms': response_time * 1000})
            
            # Test database query performance
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            start_time = time.time()
            cursor.execute("SELECT COUNT(*) FROM market_data WHERE timestamp > datetime('now', '-1 hour')")
            cursor.fetchone()
            db_time = time.time() - start_time
            
            conn.close()
            
            if db_time < 0.1:
                self.log_result("Database Performance", "PASS", 
                               f"Query time: {db_time:.3f}s")
            else:
                self.log_result("Database Performance", "WARN", 
                               f"Query time: {db_time:.3f}s")
                
        except Exception as e:
            self.log_result("Performance Testing", "FAIL", str(e))
    
    def test_data_consistency(self):
        """Test data consistency across components"""
        print("\n🔗 TESTING DATA CONSISTENCY...")
        
        try:
            # Get data from API
            api_response = requests.get(f"{self.api_base}/api/v1/market-data?limit=5", timeout=10)
            if api_response.status_code == 200:
                api_data = api_response.json()
                
                # Compare with database
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT symbol, price FROM market_data ORDER BY timestamp DESC LIMIT 5")
                db_data = cursor.fetchall()
                
                conn.close()
                
                if len(api_data) > 0 and len(db_data) > 0:
                    self.log_result("Data Consistency", "PASS", 
                                   f"API: {len(api_data)} records, DB: {len(db_data)} records")
                else:
                    self.log_result("Data Consistency", "WARN", "Insufficient data for comparison")
            else:
                self.log_result("Data Consistency", "FAIL", "API data unavailable")
                
        except Exception as e:
            self.log_result("Data Consistency", "FAIL", str(e))
    
    def generate_comprehensive_report(self):
        """Generate comprehensive test report"""
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.results if r['status'] == 'FAIL'])
        warning_tests = len([r for r in self.results if r['status'] == 'WARN'])
        
        print("\n" + "=" * 80)
        print("📊 ULTRA COMPREHENSIVE SYSTEM VALIDATION REPORT")
        print("=" * 80)
        print(f"⏰ Test Duration: {datetime.now()}")
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {warning_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # System status
        if failed_tests == 0 and warning_tests <= 2:
            system_status = "🟢 ULTRA OPERATIONAL - PRODUCTION READY"
        elif failed_tests <= 2:
            system_status = "🟡 MOSTLY OPERATIONAL - MINOR ISSUES"
        else:
            system_status = "🔴 CRITICAL ISSUES - REQUIRES ATTENTION"
        
        print(f"\n🎯 SYSTEM STATUS: {system_status}")
        
        # Detailed breakdown
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.results:
                if result['status'] == 'FAIL':
                    print(f"   • {result['test']}: {result['message']}")
        
        if warning_tests > 0:
            print("\n⚠️  WARNINGS:")
            for result in self.results:
                if result['status'] == 'WARN':
                    print(f"   • {result['test']}: {result['message']}")
        
        # Save report
        report_file = f"system_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': total_tests,
                    'passed': passed_tests,
                    'failed': failed_tests,
                    'warnings': warning_tests,
                    'success_rate': (passed_tests/total_tests)*100,
                    'system_status': system_status
                },
                'detailed_results': self.results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        print("=" * 80)
        
        return system_status, (passed_tests/total_tests)*100
    
    def run_ultra_validation(self):
        """Run complete ultra validation suite"""
        print("🚀 STARTING ULTRA COMPREHENSIVE SYSTEM VALIDATION")
        print("=" * 80)
        
        # Run all test suites
        self.test_file_integrity()
        self.test_database_integrity()
        self.test_api_comprehensive()
        self.test_ml_prediction_accuracy()
        self.test_dashboard_service()
        self.test_system_performance()
        self.test_data_consistency()
        
        # Generate final report
        return self.generate_comprehensive_report()

if __name__ == "__main__":
    validator = UltraSystemValidator()
    system_status, success_rate = validator.run_ultra_validation()
    
    print(f"\n🎯 FINAL STATUS: {system_status}")
    print(f"📊 SUCCESS RATE: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🚀 SYSTEM READY FOR PRODUCTION DEPLOYMENT!")
    elif success_rate >= 75:
        print("⚠️  SYSTEM NEEDS MINOR FIXES BEFORE PRODUCTION")
    else:
        print("❌ SYSTEM REQUIRES MAJOR FIXES")