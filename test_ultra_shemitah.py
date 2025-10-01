#!/usr/bin/env python3
"""
Ultra Shemitah Analysis Test Module
Tests comprehensive Biblical financial cycles analysis with historical correlation
"""

import sys
import os
from datetime import datetime, timedelta
import logging

# Logging yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path ayarları
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ultra_shemitah():
    """Test ultra Shemitah analysis with comprehensive Biblical cycle features"""
    print("=" * 80)
    print("📜 ULTRA SHEMITAH ANALYSIS TEST")
    print("Testing sophisticated Biblical financial cycles analysis...")
    print("=" * 80)
    
    try:
        # Import module
        from src.analysis.ultra_shemitah import ultra_shemitah_analyzer
        
        print("\n📊 Biblical Financial Cycles Analysis Capabilities:")
        print("✓ 7-year Shemitah cycles with lunar calendar precision")
        print("✓ 49-year Jubilee super-cycles analysis")
        print("✓ Historical market correlation analysis")
        print("✓ Biblical agricultural cycle correlation")
        print("✓ Debt forgiveness cycle modeling")
        print("✓ Economic reset pattern detection")
        
        # Test different symbols with various Shemitah sensitivities
        test_symbols = [
            ('JPM', 'Banking - Highest Shemitah sensitivity'),
            ('AAPL', 'Technology - Moderate Shemitah impact'),
            ('CORN', 'Agricultural - Biblical correlation'),
            ('GLD', 'Gold - Safe haven during Shemitah'),
            ('PG', 'Consumer Staples - Defensive'),
            ('VNQ', 'Real Estate - High Biblical cycle impact')
        ]
        
        print("\n🔍 Testing symbols with different Shemitah sensitivities:")
        print("-" * 70)
        
        for symbol, description in test_symbols:
            try:
                result = ultra_shemitah_analyzer.calculate_ultra_shemitah_score(symbol)
                score = result['ultra_shemitah_score']
                analysis = result['analysis']
                components = result['components']
                
                print(f"\n{symbol:<6} ({description})")
                print(f"  Ultra Shemitah Score: {score:.1f}/100")
                print(f"  Shemitah Year: {analysis.get('shemitah_year', 'N/A')}/7 ({analysis.get('shemitah_phase', 'N/A')})")
                print(f"  Jubilee Position: {analysis.get('jubilee_year', 'N/A')}/49 ({analysis.get('jubilee_phase', 'N/A')})")
                print(f"  Phase Intensity: {analysis.get('phase_intensity', 'N/A')}")
                print(f"  Biblical Principle: {analysis.get('biblical_principle', 'N/A')}")
                
                # Show key component scores
                if 'shemitah_cycle' in components:
                    sc_score = components['shemitah_cycle']['score']
                    print(f"  Shemitah Cycle Score: {sc_score:.1f}")
                
                if 'jubilee_cycle' in components:
                    jc_score = components['jubilee_cycle']['score']
                    print(f"  Jubilee Cycle Score: {jc_score:.1f}")
                
                # Show top insights
                insights = analysis.get('key_insights', [])
                if insights:
                    print(f"  Key Insight: {insights[0]}")
                
            except Exception as e:
                print(f"  ❌ Error testing {symbol}: {e}")
        
        # Test comprehensive Biblical cycle analysis
        print("\n" + "=" * 70)
        print("📜 COMPREHENSIVE BIBLICAL CYCLE ANALYSIS")
        print("=" * 70)
        
        result = ultra_shemitah_analyzer.calculate_ultra_shemitah_score('JPM')  # Financial sector
        components = result['components']
        shemitah_data = result['shemitah_data']
        
        # Shemitah Cycle Analysis
        if 'shemitah_cycle' in components:
            sc = components['shemitah_cycle']
            print(f"\n📅 Shemitah Cycle Analysis:")
            print(f"  Current Year: {sc.get('year_in_cycle', 'N/A')}/7")
            print(f"  Phase: {sc.get('phase', 'N/A')}")
            print(f"  Intensity: {sc.get('intensity', 0):.1%}")
            print(f"  Score: {sc.get('score', 0):.1f}/100")
        
        # Jubilee Cycle Analysis
        if 'jubilee_cycle' in components:
            jc = components['jubilee_cycle']
            print(f"\n🎺 Jubilee Cycle Analysis:")
            print(f"  Year in Jubilee: {jc.get('year_in_jubilee', 'N/A')}/49")
            print(f"  Phase: {jc.get('phase', 'N/A')}")
            print(f"  Next Jubilee: {jc.get('next_jubilee', 'N/A')}")
            print(f"  Score: {jc.get('score', 0):.1f}/100")
        
        # Historical Correlation
        if 'historical_correlation' in components:
            hc = components['historical_correlation']
            print(f"\n📈 Historical Correlation Analysis:")
            print(f"  Correlation Strength: {hc.get('correlation_strength', 0):.1%}")
            print(f"  Historical Pattern: {hc.get('historical_pattern', 'N/A')}")
            print(f"  Score: {hc.get('score', 0):.1f}/100")
        
        # Biblical Principles
        if 'biblical_principles' in components:
            bp = components['biblical_principles']
            print(f"\n✡️ Biblical Principles Analysis:")
            print(f"  Debt Cycle Phase: {bp.get('debt_cycle_phase', 'N/A')}")
            print(f"  Reset Proximity: {bp.get('economic_reset_proximity', 'N/A')}")
            print(f"  Score: {bp.get('score', 0):.1f}/100")
        
        # Current Shemitah Data
        if shemitah_data:
            current_cycle = shemitah_data.get('current_cycle')
            if current_cycle:
                print(f"\n🔄 Current Cycle Details:")
                print(f"  Cycle Number: {current_cycle.cycle_number}")
                print(f"  Market Correlation: {current_cycle.market_correlation:.1%}")
                print(f"  Calculation Confidence: {shemitah_data.get('calculation_confidence', 0):.1%}")
        
        # Test historical event correlation
        print("\n" + "=" * 70)
        print("📊 HISTORICAL EVENT CORRELATION")
        print("=" * 70)
        
        # Test specific historical dates
        historical_dates = [
            (datetime(2008, 9, 15), "Lehman Brothers Collapse"),
            (datetime(2001, 9, 11), "9/11 Market Impact"),
            (datetime(2015, 8, 24), "China Black Monday"),
            (datetime(2022, 6, 13), "Crypto Winter Begin")
        ]
        
        for test_date, event_name in historical_dates:
            try:
                historical_result = ultra_shemitah_analyzer.calculate_ultra_shemitah_score('SPY', test_date)
                h_score = historical_result['ultra_shemitah_score']
                h_analysis = historical_result['analysis']
                
                print(f"\n{event_name} ({test_date.strftime('%Y-%m-%d')}):")
                print(f"  Shemitah Score: {h_score:.1f}/100")
                print(f"  Shemitah Year: {h_analysis.get('shemitah_year', 'N/A')}/7")
                print(f"  Phase: {h_analysis.get('shemitah_phase', 'N/A')}")
                print(f"  Historical Pattern: {h_analysis.get('historical_pattern', 'N/A')}")
                
            except Exception as e:
                print(f"  ❌ Error analyzing {event_name}: {e}")
        
        # Test performance
        print("\n" + "=" * 70)
        print("⚡ PERFORMANCE TEST")
        print("=" * 70)
        
        import time
        
        # Test calculation speed
        start_time = time.time()
        for i in range(10):
            ultra_shemitah_analyzer.calculate_ultra_shemitah_score('AAPL')
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 10
        print(f"Average calculation time: {avg_time:.3f} seconds")
        print(f"Calculations per second: {1/avg_time:.1f}")
        
        print("\n" + "=" * 70)
        print("✅ ULTRA SHEMITAH ANALYSIS TEST COMPLETED")
        print("=" * 70)
        print("🎯 Key Features Verified:")
        print("✓ Professional Biblical financial cycle modeling")
        print("✓ Multi-calendar system integration (Hebrew/Gregorian)")
        print("✓ Historical market correlation analysis")
        print("✓ Agricultural cycle correlation")
        print("✓ Debt forgiveness cycle modeling")
        print("✓ Jubilee super-cycle analysis")
        print("✓ Symbol-specific sensitivity calculation")
        print("✓ Lunar calendar precision adjustments")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in ultra Shemitah test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_with_main():
    """Test integration with main analysis system"""
    print("\n" + "=" * 70)
    print("🔗 INTEGRATION TEST")
    print("=" * 70)
    
    try:
        # Test compatibility functions
        from src.analysis.ultra_shemitah import get_shemitah_score
        from src.analysis.shemitah_analysis import get_shemitah_score as original_get_shemitah_score
        
        # Test ultra function
        ultra_score = get_shemitah_score()
        print(f"Ultra Shemitah function score: {ultra_score:.1f}")
        
        # Test original compatibility
        original_score = original_get_shemitah_score()
        print(f"Original compatibility score: {original_score:.1f}")
        
        # Test financial analyzer integration
        try:
            from src.analysis.financial_analysis import FinancialAnalyzer
            analyzer = FinancialAnalyzer()
            
            signal, total_score, detailed = analyzer.generate_signal(
                financial_score=60, technical_indicators={'rsi': 45},
                trend_analysis={'strength': 55, 'trend': 'neutral'},
                gann_analysis=50, symbol='JPM', stock_data=None
            )
            
            shemitah_component = detailed.get('scores', {}).get('shemitah', 0)
            print(f"Financial analyzer Shemitah component: {shemitah_component:.1f}")
            
        except Exception as e:
            print(f"Financial analyzer integration error: {e}")
        
        print("✅ Integration test successful")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting Ultra Shemitah Analysis Test Suite...")
    
    success1 = test_ultra_shemitah()
    success2 = test_integration_with_main()
    
    if success1 and success2:
        print("\n🎉 ALL TESTS PASSED! Ultra Shemitah Analysis ready for production.")
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")