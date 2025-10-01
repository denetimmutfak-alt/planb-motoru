#!/usr/bin/env python3
"""
Test Resilient Loader - Rate Limit Solution
"""

import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(__file__))

def test_resilient_loader():
    """Test resilient loader functionality"""
    print("🧪 Testing Resilient Loader...")
    
    try:
        from resilient_loader import cached_download, cache_stats, clear_cache
        
        # Test stocks
        test_symbols = ['AAPL', 'THYAO.IS', 'AKBNK.IS']
        
        print("📊 Cache stats before:")
        cache_stats()
        
        for symbol in test_symbols:
            print(f"\n🔍 Testing {symbol}...")
            
            # First download (should hit API)
            start_time = time.time()
            df1 = cached_download(symbol, period="5d", interval="1d", ttl=3600)
            time1 = time.time() - start_time
            
            if not df1.empty:
                print(f"✅ First download: {len(df1)} rows in {time1:.2f}s")
                
                # Second download (should hit cache)
                start_time = time.time() 
                df2 = cached_download(symbol, period="5d", interval="1d", ttl=3600)
                time2 = time.time() - start_time
                
                if not df2.empty:
                    print(f"⚡ Cache hit: {len(df2)} rows in {time2:.2f}s")
                    print(f"🚀 Speed improvement: {time1/time2:.1f}x faster")
                else:
                    print("❌ Cache miss")
            else:
                print(f"❌ No data for {symbol}")
        
        print("\n📊 Cache stats after:")
        cache_stats()
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_integration():
    """Test integration with main system"""
    print("\n🧪 Testing Integration...")
    
    try:
        from telegram_full_trader_with_sentiment import analyze_symbol_fast
        
        # Test with cache system
        print("🔍 Testing THYAO.IS with resilient loader...")
        result = analyze_symbol_fast('THYAO.IS')
        
        if result:
            print(f"✅ Integration success: {result['score']:.1f} - {result['signal']}")
            return True
        else:
            print("❌ Integration failed - no result")
            return False
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Resilient Loader Test Suite")
    print("=" * 50)
    
    tests = [
        ("Resilient Loader", test_resilient_loader),
        ("System Integration", test_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"💥 {test_name} CRASHED: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests PASSED! Rate limit solution ready.")
        return 0
    else:
        print("⚠️  Some tests FAILED. Check implementation.")
        return 1

if __name__ == "__main__":
    exit(main())