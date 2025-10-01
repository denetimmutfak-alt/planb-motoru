#!/usr/bin/env python3
"""
PlanB Motoru - Simple Local Test
Basic environment validation
"""

import requests
import json
from datetime import datetime

def test_dashboard():
    """Test dashboard endpoints"""
    print("🧪 Testing Dashboard Endpoints...")
    
    try:
        # Test main dashboard
        response = requests.get('http://localhost:9090', timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard main page: PASS")
        else:
            print(f"❌ Dashboard main page: FAIL ({response.status_code})")
        
        # Test health endpoint
        response = requests.get('http://localhost:9090/health', timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health endpoint: PASS - Status: {health_data.get('status')}")
        else:
            print(f"❌ Health endpoint: FAIL ({response.status_code})")
        
        # Test system test endpoint
        response = requests.get('http://localhost:9090/test', timeout=5)
        if response.status_code == 200:
            test_data = response.json()
            print(f"✅ System test endpoint: PASS - Status: {test_data.get('status')}")
            print(f"   Test Results: {test_data.get('test_results')}")
        else:
            print(f"❌ System test endpoint: FAIL ({response.status_code})")
            
    except requests.exceptions.ConnectionError:
        print("❌ Dashboard not accessible - Connection refused")
    except Exception as e:
        print(f"❌ Test error: {e}")

def test_python_environment():
    """Test Python environment"""
    print("\n🐍 Testing Python Environment...")
    
    required_modules = [
        'flask', 'requests', 'json', 'datetime', 
        'os', 'sys', 'time'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}: Available")
        except ImportError:
            print(f"❌ {module}: Missing")

def main():
    """Main test function"""
    print("=" * 60)
    print("🚀 PLANB MOTORU - SIMPLE LOCAL TEST")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now()}")
    print()
    
    test_python_environment()
    test_dashboard()
    
    print("\n" + "=" * 60)
    print("📊 Basic Environment Test Completed")
    print("=" * 60)

if __name__ == "__main__":
    main()