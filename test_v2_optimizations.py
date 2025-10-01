#!/usr/bin/env python3
"""
PlanB Motoru v2 Optimizations Test
Test all new enhancements before deployment
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(__file__))

def test_early_v2():
    """Test enhanced early warning system"""
    print("🧪 Testing Early Warning v2...")
    try:
        # Mock talib for Windows testing
        import sys
        if 'talib' not in sys.modules:
            import types
            talib = types.ModuleType('talib')
            talib.RSI = lambda x, p: x * 0 + 50  # Mock RSI returning 50
            talib.EMA = lambda x, p: x  # Mock EMA returning same values
            talib.BBANDS = lambda x, p1, p2, p3: (x*1.1, x, x*0.9)  # Mock Bollinger Bands
            sys.modules['talib'] = talib
        
        from early_v2 import ew_optimized
        
        # Create sample data
        dates = pd.date_range(start='2024-01-01', periods=50, freq='D')
        df = pd.DataFrame({
            'Close': np.random.randn(50).cumsum() + 100,
            'Volume': np.random.randint(100000, 1000000, 50)
        }, index=dates)
        
        score = ew_optimized(df, "BIST")
        print(f"✅ Early Warning v2 score: {score}")
        return score >= 0 and score <= 40
        
    except Exception as e:
        print(f"❌ Early Warning v2 test failed: {e}")
        return False

def test_ultra_v3():
    """Test ULTRA v3 enhanced system"""
    print("🧪 Testing ULTRA v3...")
    try:
        from ultra_v3 import compute_ultra_v3
        
        # Create sample returns
        returns = np.random.randn(25) * 0.02  # 25 daily returns
        
        score = compute_ultra_v3(returns)
        print(f"✅ ULTRA v3 score: {score:.2f}")
        return abs(score) <= 45  # Should be within bounds
        
    except Exception as e:
        print(f"❌ ULTRA v3 test failed: {e}")
        return False

def test_vol_spike():
    """Test volume spike detection"""
    print("🧪 Testing Volume Spike Detection...")
    try:
        from vol_spike import refined_volume_spike, volume_spike_indicator
        
        # Create sample data with volume spike
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        df = pd.DataFrame({
            'Close': np.random.randn(30).cumsum() + 100,
            'Volume': [100000] * 29 + [500000]  # Spike on last day
        }, index=dates)
        
        # Add price movement for last day
        df.loc[df.index[-1], 'Close'] = df['Close'].iloc[-2] * 1.025  # +2.5%
        
        spike = refined_volume_spike(df, factor=2.0)
        info = volume_spike_indicator(df)
        
        print(f"✅ Volume spike detected: {spike}")
        print(f"✅ Volume info: {info}")
        return True
        
    except Exception as e:
        print(f"❌ Volume spike test failed: {e}")
        return False

def test_interactive_reminder():
    """Test interactive reminder system"""
    print("🧪 Testing Interactive Reminder...")
    try:
        from interactive_reminder import add_reminder, create_reminder_button
        
        # Test add reminder
        result = add_reminder("test_user", "AAPL", 28)
        print(f"✅ Add reminder result: {result}")
        
        # Test button creation
        button = create_reminder_button("AAPL")
        print(f"✅ Reminder button created: {button is not None}")
        
        return result and button is not None
        
    except Exception as e:
        print(f"❌ Interactive reminder test failed: {e}")
        return False

def test_integration():
    """Test system integration"""
    print("🧪 Testing System Integration...")
    try:
        # Test all imports work together
        from early_v2 import ew_optimized
        from ultra_v3 import compute_ultra_v3
        from vol_spike import refined_volume_spike
        from interactive_reminder import add_reminder
        
        print("✅ All modules imported successfully")
        
        # Create comprehensive test data
        dates = pd.date_range(start='2024-01-01', periods=50, freq='D')
        df = pd.DataFrame({
            'Close': np.random.randn(50).cumsum() + 100,
            'Volume': np.random.randint(100000, 1000000, 50)
        }, index=dates)
        
        returns = df['Close'].pct_change(fill_method=None).dropna().values
        
        # Test all systems
        early_score = ew_optimized(df, "BIST")
        ultra_score = compute_ultra_v3(returns) if len(returns) >= 19 else 0
        vol_spike = refined_volume_spike(df)
        
        total_score = 50 + early_score + ultra_score  # Base 50 + bonuses
        
        print(f"✅ Integration test - Total score: {total_score:.1f}")
        print(f"  - Early v2: +{early_score}")
        print(f"  - ULTRA v3: +{ultra_score:.1f}")
        print(f"  - Vol Spike: {vol_spike}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 PlanB Motoru v2 Optimizations Test Suite")
    print("=" * 50)
    
    tests = [
        ("Early Warning v2", test_early_v2),
        ("ULTRA v3", test_ultra_v3),
        ("Volume Spike", test_vol_spike),
        ("Interactive Reminder", test_interactive_reminder),
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
        print("🎉 All tests PASSED! Ready for deployment.")
        return 0
    else:
        print("⚠️  Some tests FAILED. Check before deployment.")
        return 1

if __name__ == "__main__":
    exit(main())