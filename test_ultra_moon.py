#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test Ultra Moon Phases Analysis"""

from src.analysis.moon_phases import ultra_moon_analyzer
import datetime

def test_ultra_moon_analysis():
    """Test ultra moon analysis functionality"""
    try:
        print("=== Testing Ultra Moon Phases Analysis ===\n")
        
        # Test with AAPL (technology sector)
        result = ultra_moon_analyzer.calculate_ultra_moon_score('AAPL')
        
        print("Ultra Moon Analysis Results:")
        print(f"Score: {result['ultra_moon_score']:.2f}")
        print(f"Moon Phase: {result['lunar_data']['moon_phase']['name']}")
        print(f"Power: {result['lunar_data']['moon_phase']['power']:.2f}")
        print(f"Energy: {result['lunar_data']['moon_phase']['energy']}")
        print(f"Lunar Mansion: {result['lunar_data']['lunar_mansion']['name']}")
        print(f"Sector: {result['lunar_data']['lunar_mansion']['sector']}")
        print(f"Volatility: {result['lunar_data']['lunar_mansion']['volatility']}")
        print(f"Moon Sign: {result['lunar_data']['moon_sign']['sign']}")
        print(f"VOC Status: {result['lunar_data']['void_of_course']['is_void']}")
        print(f"Eclipse Proximity: {result['lunar_data']['eclipse_proximity']['in_orb']}")
        print(f"Market Timing Quality: {result['lunar_data']['market_correlation']['market_timing_quality']}")
        
        print("\nScore Components:")
        for component, value in result['components'].items():
            print(f"{component}: {value:.2f}")
        
        print("\nAnalysis:")
        print(f"Recommendation: {result['analysis']['score_interpretation']}")
        print(f"Key Insights: {', '.join(result['analysis']['key_insights'])}")
        print(f"Volatility Expectation: {result['analysis']['volatility_expectation']}")
        print(f"Sector Preference: {result['analysis']['sector_preference']}")
        
        # Test with different symbols
        print("\n" + "="*50)
        print("Testing Different Symbols:")
        
        symbols = ['GLD', 'CORN', 'BTC-USD', 'JPM']
        for symbol in symbols:
            try:
                sym_result = ultra_moon_analyzer.calculate_ultra_moon_score(symbol)
                print(f"\n{symbol}: Score {sym_result['ultra_moon_score']:.2f} - {sym_result['analysis']['score_interpretation']}")
            except Exception as e:
                print(f"{symbol}: Error - {e}")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ultra_moon_analysis()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")