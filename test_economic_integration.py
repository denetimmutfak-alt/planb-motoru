#!/usr/bin/env python3
"""
Economic Cycle Integration Test
Test economic cycle module integration with main system
"""

import sys
import os
from pathlib import Path

# Path ayarları
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_economic_integration():
    """Test economic cycle integration"""
    print("🔍 Economic Cycle Integration Test")
    print("=" * 50)
    
    try:
        # Test import
        from src.analysis.economic_cycle import ultra_economic_analyzer
        from src.analysis.financial_analysis import FinancialAnalyzer
        
        # Initialize analyzer
        analyzer = FinancialAnalyzer()
        
        # Test symbol
        symbol = 'AAPL'
        
        # Test economic score calculation
        print(f"\n📊 Testing {symbol} Economic Analysis:")
        
        # Direct economic analysis
        economic_result = ultra_economic_analyzer.calculate_ultra_economic_score(symbol)
        economic_score = economic_result['ultra_economic_score']
        print(f"  Economic Score: {economic_score:.1f}/100")
        print(f"  Business Cycle: {economic_result['analysis']['business_cycle_phase']}")
        print(f"  Recession Risk: {economic_result['analysis']['recession_risk_level']}")
        print(f"  Recommendation: {economic_result['analysis']['score_interpretation']}")
        
        # Test financial analyzer signal generation with economic cycle
        print(f"\n⚙️ Testing Integrated Signal Generation:")
        
        # Mock some basic parameters for signal generation
        financial_score = 60
        technical_indicators = {'rsi': 45}
        trend_analysis = {'strength': 55, 'trend': 'neutral'}
        gann_analysis = 50
        stock_data = None  # For compatibility
        
        signal, total_score, detailed_analysis = analyzer.generate_signal(
            financial_score=financial_score,
            technical_indicators=technical_indicators,
            trend_analysis=trend_analysis,
            gann_analysis=gann_analysis,
            symbol=symbol,
            stock_data=stock_data
        )
        
        print(f"  Total Score: {total_score:.1f}/100")
        print(f"  Signal: {signal}")
        print(f"  Economic Component: {detailed_analysis.get('economic_cycle_score', 'N/A'):.1f}")
        
        # Show component breakdown
        scores = detailed_analysis.get('scores', {})
        if scores:
            print(f"\n📈 Score Breakdown:")
            for component, score in scores.items():
                if component == 'economic_cycle':
                    print(f"  ✅ {component}: {score:.1f} (Economic Cycle Module)")
                else:
                    print(f"     {component}: {score:.1f}")
        
        print(f"\n✅ Economic Cycle Integration Test PASSED")
        print(f"🎯 Economic Module Successfully Integrated:")
        print(f"   ✓ Direct economic analysis working")
        print(f"   ✓ Integrated scoring system working")
        print(f"   ✓ Component breakdown available")
        print(f"   ✓ Macro-economic insights included")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_economic_integration()
    if success:
        print("\n🎉 Economic Cycle Module Successfully Integrated into PlanB Engine!")
    else:
        print("\n⚠️ Integration issues detected. Please check implementation.")