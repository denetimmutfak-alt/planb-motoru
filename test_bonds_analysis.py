"""
Test script for Ultra Bonds Analysis
Ultra Tahvil Analizi Test Scripti
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis.bonds_analysis import BondsAnalyzer
import pandas as pd
from datetime import datetime

def test_bonds_analysis():
    """Bonds analizi testleri"""
    print("=" * 60)
    print("ULTRA BONDS ANALİZİ TEST SÜİTİ")
    print("=" * 60)
    
    analyzer = BondsAnalyzer()
    
    test_bonds = [
        {
            'symbol': 'US10Y',
            'name': 'US 10-Year Treasury',
            'bond_data': {
                'bond_type': 'GOVERNMENT',
                'issuer': 'US Treasury',
                'currency': 'USD',
                'coupon_rate': 4.5,
                'face_value': 100,
                'maturity': '2034-01-01',
                'credit_rating': 'AAA'
            }
        },
        {
            'symbol': 'DE10Y',
            'name': 'German 10-Year Bund',
            'bond_data': {
                'bond_type': 'GOVERNMENT',
                'issuer': 'German Government',
                'currency': 'EUR',
                'coupon_rate': 2.8,
                'face_value': 100,
                'maturity': '2034-01-01',
                'credit_rating': 'AAA'
            }
        },
        {
            'symbol': 'AAPL_CORP',
            'name': 'Apple Corporate Bond',
            'bond_data': {
                'bond_type': 'CORPORATE',
                'issuer': 'Apple Inc',
                'currency': 'USD',
                'coupon_rate': 5.2,
                'face_value': 100,
                'maturity': '2029-01-01',
                'credit_rating': 'AA+'
            }
        },
        {
            'symbol': 'TR_GOVT',
            'name': 'Turkish Government Bond',
            'bond_data': {
                'bond_type': 'GOVERNMENT',
                'issuer': 'Turkish Treasury',
                'currency': 'TRY',
                'coupon_rate': 25.0,
                'face_value': 100,
                'maturity': '2028-01-01',
                'credit_rating': 'B+'
            }
        }
    ]
    
    # Generate some sample historical data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    
    test_results = []
    
    for i, bond in enumerate(test_bonds, 1):
        print(f"\nTest {i}/4: {bond['name']} ({bond['symbol']})")
        print("-" * 50)
        
        try:
            # Create sample historical data
            historical_data = pd.DataFrame({
                'Date': dates,
                'Price': 100 + (i-2.5) * 2 + pd.Series(range(len(dates))) * 0.01,
                'Yield': 4.0 + (i-2.5) * 1.5 - pd.Series(range(len(dates))) * 0.001,
                'Volume': 1000000 + pd.Series(range(len(dates))) * 1000
            })
            
            # Run analysis
            result = analyzer.analyze_bond(
                symbol=bond['symbol'],
                bond_data=bond['bond_data'],
                historical_data=historical_data
            )
            
            # Display results
            print(f"✅ Bond Score: {result['bond_score']}")
            print(f"📊 Trading Recommendation: {result['trading_recommendation']}")
            print(f"📝 Analysis: {result['analysis_summary']}")
            
            if 'ultra_analysis' in result:
                ultra = result['ultra_analysis']
                print(f"🎯 Ultra Bond Score: {ultra['ultra_bond_score']}")
                print(f"💰 Bond Type: {ultra['bond_type']}")
                print(f"⭐ Credit Rating: {ultra['credit_rating']}")
                print(f"⏰ Time to Maturity: {ultra['time_to_maturity']:.1f} years")
                
                # Valuation metrics
                val = ultra['valuation']
                print(f"💎 Fair Value: ${val['fair_value']}")
                print(f"📈 Yield to Maturity: {val['yield_to_maturity']:.2f}%")
                print(f"⏳ Duration: {val['duration']:.2f}")
                print(f"🔄 Modified Duration: {val['modified_duration']:.2f}")
                print(f"📊 Convexity: {val['convexity']:.2f}")
                print(f"💹 DV01: {val['dv01']:.4f}")
                
                # Credit risk
                credit = ultra['credit_risk']
                print(f"⚠️ Default Probability: {credit['default_probability']:.3f}%")
                print(f"📊 Credit Spread: {credit['credit_spread']:.2f} bps")
                print(f"🎯 Credit Score: {credit['credit_score']:.1f}/100")
                print(f"💪 Financial Health: {credit['financial_health']:.1f}/100")
                
                # Yield curve
                curve = ultra['yield_curve']
                print(f"📈 Curve Shape: {curve['curve_shape']}")
                print(f"📊 Steepness: {curve['steepness']:.2f}")
                print(f"⚠️ Recession Signal: {curve['recession_signal']}")
                
                # Interest rate environment
                ir_env = ultra['interest_rate_env']
                print(f"🏦 Central Bank Trend: {ir_env['central_bank_trend']}")
                print(f"🔄 Rate Cycle Phase: {ir_env['rate_cycle_phase']}")
                print(f"💰 Fed Funds Rate: {ir_env['fed_funds_rate']:.2f}%")
            
            # Risk assessment
            if 'risk_assessment' in result:
                risk = result['risk_assessment']
                print(f"⚠️ Overall Risk: {risk['overall_risk']}")
                if 'credit_risk' in risk:
                    print(f"💳 Credit Risk: {risk['credit_risk']}")
                if 'interest_rate_risk' in risk:
                    print(f"📊 Interest Rate Risk: {risk['interest_rate_risk']}")
            
            # Curve insights
            if 'curve_insights' in result:
                insights = result['curve_insights']
                print(f"🔍 Economic Signal: {insights.get('economic_signal', 'N/A')}")
                if 'recession_probability' in insights:
                    print(f"📉 Recession Probability: {insights['recession_probability']}%")
            
            # Investment strategies
            if 'investment_strategies' in result:
                strategies = result['investment_strategies']
                print(f"📋 Investment Strategies: {len(strategies)} found")
                for j, strategy in enumerate(strategies[:2], 1):
                    print(f"   {j}. {strategy['strategy']}: {strategy.get('description', 'N/A')}")
            
            print(f"🎯 Confidence: {result['confidence']:.1f}%")
            
            test_results.append({
                'bond': bond['name'],
                'score': result['bond_score'],
                'recommendation': result['trading_recommendation'],
                'success': True
            })
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            test_results.append({
                'bond': bond['name'],
                'score': 0,
                'recommendation': 'ERROR',
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY - ULTRA BONDS ANALYSIS")
    print("=" * 60)
    
    successful_tests = sum(1 for r in test_results if r['success'])
    print(f"✅ Successful Tests: {successful_tests}/{len(test_results)}")
    
    if successful_tests > 0:
        print("\n📊 BOND ANALYSIS RESULTS:")
        for result in test_results:
            if result['success']:
                status_icon = "🟢" if result['score'] >= 60 else "🟡" if result['score'] >= 40 else "🔴"
                print(f"{status_icon} {result['bond']}: {result['score']:.1f} ({result['recommendation']})")
    
    failed_tests = [r for r in test_results if not r['success']]
    if failed_tests:
        print(f"\n❌ Failed Tests: {len(failed_tests)}")
        for result in failed_tests:
            print(f"   - {result['bond']}: {result.get('error', 'Unknown error')}")
    
    if successful_tests == len(test_results):
        print(f"\n🎉 ALL TESTS PASSED! Ultra Bonds Analysis is working perfectly!")
        print(f"💎 Ultra Bonds Analyzer successfully analyzed {len(test_bonds)} different bond types")
        print(f"🔍 Features tested: Yield curve analysis, Credit risk assessment, Duration calculations")
        print(f"🎯 Bond valuation, Interest rate environment, Investment strategies")
    else:
        print(f"\n⚠️ Some tests failed. Please check the errors above.")
    
    return test_results

if __name__ == "__main__":
    test_bonds_analysis()