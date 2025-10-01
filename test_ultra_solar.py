#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test Ultra Solar Cycle Analysis"""

from src.analysis.solar_cycle import ultra_solar_analyzer
import datetime

def test_ultra_solar_analysis():
    """Test ultra solar cycle analysis functionality"""
    try:
        print("=== Testing Ultra Solar Cycle Analysis ===\n")
        
        # Test with AAPL (technology sector - high solar sensitivity)
        result = ultra_solar_analyzer.calculate_ultra_solar_score('AAPL')
        
        print("Ultra Solar Cycle Analysis Results:")
        print(f"Score: {result['ultra_solar_score']:.2f}")
        print(f"Solar Cycle: {result['solar_data']['cycle_number']}")
        print(f"Cycle Position: {result['solar_data']['cycle_position']:.1%}")
        print(f"Solar Phase: {result['solar_data']['solar_phase']['phase']}")
        print(f"Market Influence: {result['solar_data']['solar_phase']['market_influence']}")
        print(f"Estimated Sunspots: {result['solar_data']['estimated_sunspot_number']:.0f}")
        print(f"Geomagnetic Level: {result['solar_data']['geomagnetic_activity']['level']}")
        print(f"Kp Index: {result['solar_data']['geomagnetic_activity']['kp_index']}")
        print(f"Solar Wind Speed: {result['solar_data']['solar_wind']['solar_wind_speed_kms']} km/s")
        print(f"Disruption Potential: {result['solar_data']['solar_wind']['disruption_potential']:.2f}")
        print(f"Infrastructure Vulnerability: {result['solar_data']['magnetic_field_impact']['infrastructure_vulnerability']:.1%}")
        
        print("\nScore Components:")
        for component, value in result['components'].items():
            print(f"{component}: {value:.2f}")
        
        print("\nAnalysis:")
        print(f"Recommendation: {result['analysis']['score_interpretation']}")
        print(f"Key Insights: {', '.join(result['analysis']['key_insights'])}")
        print(f"Technology Risk: {result['analysis']['technology_risk']}")
        print(f"Geomagnetic Level: {result['analysis']['geomagnetic_level']}")
        
        # Test with different symbols
        print("\n" + "="*50)
        print("Testing Different Symbols:")
        
        symbols = ['VZ', 'BA', 'NEE', 'XOM', 'JPM']  # Telecom, Aerospace, Utility, Energy, Financial
        for symbol in symbols:
            try:
                sym_result = ultra_solar_analyzer.calculate_ultra_solar_score(symbol)
                print(f"\n{symbol}: Score {sym_result['ultra_solar_score']:.2f} - {sym_result['analysis']['score_interpretation']}")
                print(f"  Technology Risk: {sym_result['analysis']['technology_risk']}")
            except Exception as e:
                print(f"{symbol}: Error - {e}")
        
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ultra_solar_analysis()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")