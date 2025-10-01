#!/usr/bin/env python3
"""
PlanB Motoru - Comprehensive System Test
Multi-Service Testing Suite
"""

import requests
import json
import time
from datetime import datetime

class SystemTester:
    def __init__(self):
        self.results = []
        
    def log_result(self, test, status, message=""):
        """Log test result"""
        result = {
            'test': test,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
        
        color = '\033[92m' if status == 'PASS' else '\033[91m' if status == 'FAIL' else '\033[93m'
        reset = '\033[0m'
        print(f"{color}[{status}]{reset} {test}: {message}")
    
    def test_dashboard_service(self):
        """Test Dashboard Service (Port 8080)"""
        print("\n🖥️  Testing Dashboard Service...")
        
        try:
            # Test main dashboard
            response = requests.get('http://localhost:8080', timeout=5)
            if response.status_code == 200:
                self.log_result("Dashboard Main Page", "PASS", "Accessible")
            else:
                self.log_result("Dashboard Main Page", "FAIL", f"Status: {response.status_code}")
            
            # Test health endpoint
            response = requests.get('http://localhost:8080/health', timeout=5)
            if response.status_code == 200:
                health = response.json()
                self.log_result("Dashboard Health", "PASS", f"Status: {health.get('status')}")
            else:
                self.log_result("Dashboard Health", "FAIL", f"Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.log_result("Dashboard Service", "FAIL", "Connection refused")
        except Exception as e:
            self.log_result("Dashboard Service", "FAIL", f"Error: {e}")
    
    def test_core_api_service(self):
        """Test Core API Service (Port 8001)"""
        print("\n🔧 Testing Core API Service...")
        
        try:
            # Test root endpoint
            response = requests.get('http://localhost:8001', timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_result("Core API Root", "PASS", f"Version: {data.get('version')}")
            else:
                self.log_result("Core API Root", "FAIL", f"Status: {response.status_code}")
            
            # Test health endpoint
            response = requests.get('http://localhost:8001/health', timeout=5)
            if response.status_code == 200:
                health = response.json()
                self.log_result("Core API Health", "PASS", f"Status: {health.get('status')}")
            else:
                self.log_result("Core API Health", "FAIL", f"Status: {response.status_code}")
            
            # Test market data endpoint
            response = requests.get('http://localhost:8001/api/v1/market-data', timeout=10)
            if response.status_code == 200:
                market_data = response.json()
                self.log_result("Market Data API", "PASS", f"Retrieved {len(market_data)} symbols")
            else:
                self.log_result("Market Data API", "FAIL", f"Status: {response.status_code}")
            
            # Test ML prediction endpoint
            test_payload = {
                "symbol": "AAPL",
                "features": {
                    "rsi": 65.0,
                    "macd": 0.5,
                    "price": 150.0,
                    "volume": 1000000
                }
            }
            
            response = requests.post(
                'http://localhost:8001/api/v1/ml/predict',
                json=test_payload,
                timeout=15
            )
            
            if response.status_code == 200:
                prediction = response.json()
                self.log_result("ML Prediction API", "PASS", 
                              f"Signal: {prediction.get('signal')}, Confidence: {prediction.get('confidence')}")
            else:
                self.log_result("ML Prediction API", "FAIL", f"Status: {response.status_code}")
            
            # Test Telegram status
            response = requests.get('http://localhost:8001/api/v1/telegram/status', timeout=5)
            if response.status_code == 200:
                telegram = response.json()
                self.log_result("Telegram Bot Status", "PASS", f"Status: {telegram.get('status')}")
            else:
                self.log_result("Telegram Bot Status", "FAIL", f"Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.log_result("Core API Service", "FAIL", "Connection refused")
        except Exception as e:
            self.log_result("Core API Service", "FAIL", f"Error: {e}")
    
    def test_system_integration(self):
        """Test system integration"""
        print("\n🔗 Testing System Integration...")
        
        try:
            # Test data flow between services
            # Get market data from API
            market_response = requests.get('http://localhost:8001/api/v1/market-data/latest', timeout=10)
            
            if market_response.status_code == 200:
                market_data = market_response.json()
                if len(market_data) > 0:
                    # Test prediction for first symbol
                    first_symbol = market_data[0]
                    
                    prediction_payload = {
                        "symbol": first_symbol['symbol'],
                        "features": {
                            "rsi": 60.0,
                            "macd": 0.3,
                            "price": first_symbol['price'],
                            "volume": first_symbol['volume']
                        }
                    }
                    
                    pred_response = requests.post(
                        'http://localhost:8001/api/v1/ml/predict',
                        json=prediction_payload,
                        timeout=15
                    )
                    
                    if pred_response.status_code == 200:
                        prediction = pred_response.json()
                        self.log_result("Data Flow Integration", "PASS", 
                                      f"Market→ML: {first_symbol['symbol']} → {prediction['signal']}")
                    else:
                        self.log_result("Data Flow Integration", "FAIL", "ML prediction failed")
                else:
                    self.log_result("Data Flow Integration", "WARN", "No market data available")
            else:
                self.log_result("Data Flow Integration", "FAIL", "Market data retrieval failed")
                
        except Exception as e:
            self.log_result("System Integration", "FAIL", f"Error: {e}")
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print("=" * 80)
        print("🚀 PLANB MOTORU - COMPREHENSIVE SYSTEM TEST")
        print("=" * 80)
        print(f"⏰ Test started at: {datetime.now()}")
        
        # Run all test suites
        self.test_dashboard_service()
        self.test_core_api_service()
        self.test_system_integration()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        total = len(self.results)
        passed = len([r for r in self.results if r['status'] == 'PASS'])
        failed = len([r for r in self.results if r['status'] == 'FAIL'])
        warnings = len([r for r in self.results if r['status'] == 'WARN'])
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        print(f"📈 Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warnings}")
        print(f"📊 Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.results:
                if result['status'] == 'FAIL':
                    print(f"   ❌ {result['test']}: {result['message']}")
        
        # Service status summary
        print("\n🔄 SERVICE STATUS:")
        dashboard_status = "🟢 ONLINE" if any('Dashboard' in r['test'] and r['status'] == 'PASS' for r in self.results) else "🔴 OFFLINE"
        api_status = "🟢 ONLINE" if any('Core API' in r['test'] and r['status'] == 'PASS' for r in self.results) else "🔴 OFFLINE"
        
        print(f"   Dashboard Service (8080): {dashboard_status}")
        print(f"   Core API Service (8001): {api_status}")
        
        print("\n🎯 RECOMMENDATION:")
        if failed == 0:
            print("   ✅ All systems operational - Ready for production deployment!")
        elif failed <= 2:
            print("   ⚠️  Minor issues detected - Review failed tests before deployment")
        else:
            print("   ❌ Major issues detected - Fix critical failures before proceeding")
        
        print("=" * 80)

if __name__ == "__main__":
    tester = SystemTester()
    tester.run_comprehensive_test()