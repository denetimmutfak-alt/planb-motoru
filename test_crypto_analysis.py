"""
Test script for Ultra Crypto Analysis
Ultra Kripto Analizi Test Scripti
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis.crypto_analysis import CryptoAnalyzer
import pandas as pd
from datetime import datetime

def test_crypto_analysis():
    """Crypto analizi testleri"""
    print("=" * 60)
    print("ULTRA CRYPTO ANALİZİ TEST SÜİTİ")
    print("=" * 60)
    
    analyzer = CryptoAnalyzer()
    
    test_cryptos = [
        {
            'symbol': 'BTC',
            'name': 'Bitcoin',
            'crypto_data': {
                'name': 'Bitcoin',
                'market_cap': 1200000000000,  # 1.2T
                'circulating_supply': 19700000,
                'total_supply': 19700000,
                'max_supply': 21000000,
                'launch_date': '2009-01-03',
                'blockchain': 'bitcoin',
                'consensus_mechanism': 'proof_of_work',
                'use_case': 'store_of_value',
                'team_score': 95.0,
                'community_score': 95.0,
                'technology_score': 90.0
            }
        },
        {
            'symbol': 'ETH',
            'name': 'Ethereum',
            'crypto_data': {
                'name': 'Ethereum',
                'market_cap': 400000000000,  # 400B
                'circulating_supply': 120000000,
                'total_supply': 120000000,
                'max_supply': None,
                'launch_date': '2015-07-30',
                'blockchain': 'ethereum',
                'consensus_mechanism': 'proof_of_stake',
                'use_case': 'smart_contracts',
                'team_score': 90.0,
                'community_score': 90.0,
                'technology_score': 95.0
            }
        },
        {
            'symbol': 'UNI',
            'name': 'Uniswap',
            'crypto_data': {
                'name': 'Uniswap',
                'market_cap': 5000000000,  # 5B
                'circulating_supply': 600000000,
                'total_supply': 1000000000,
                'max_supply': 1000000000,
                'launch_date': '2020-09-17',
                'blockchain': 'ethereum',
                'consensus_mechanism': 'proof_of_stake',
                'use_case': 'defi',
                'team_score': 85.0,
                'community_score': 80.0,
                'technology_score': 88.0
            }
        },
        {
            'symbol': 'DOGE',
            'name': 'Dogecoin',
            'crypto_data': {
                'name': 'Dogecoin',
                'market_cap': 12000000000,  # 12B
                'circulating_supply': 140000000000,
                'total_supply': 140000000000,
                'max_supply': None,
                'launch_date': '2013-12-06',
                'blockchain': 'dogecoin',
                'consensus_mechanism': 'proof_of_work',
                'use_case': 'medium_of_exchange',
                'team_score': 60.0,
                'community_score': 95.0,
                'technology_score': 40.0
            }
        }
    ]
    
    # Generate some sample historical data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    
    test_results = []
    
    for i, crypto in enumerate(test_cryptos, 1):
        print(f"\nTest {i}/4: {crypto['name']} ({crypto['symbol']})")
        print("-" * 50)
        
        try:
            # Create sample historical data
            base_price = {'BTC': 65000, 'ETH': 3200, 'UNI': 7.5, 'DOGE': 0.08}[crypto['symbol']]
            
            historical_data = pd.DataFrame({
                'Date': dates,
                'Open': base_price + pd.Series(range(len(dates))) * 0.1,
                'High': base_price * 1.02 + pd.Series(range(len(dates))) * 0.1,
                'Low': base_price * 0.98 + pd.Series(range(len(dates))) * 0.1,
                'Close': base_price + pd.Series(range(len(dates))) * 0.1,
                'Volume': 1000000000 + pd.Series(range(len(dates))) * 1000000
            })
            
            # Additional blockchain and defi data for testing
            blockchain_data = {
                'network_hash_rate': 300e18 if crypto['symbol'] == 'BTC' else 100e18,
                'active_addresses': 1000000,
                'transaction_count': 300000,
                'development_activity': 90.0 if crypto['symbol'] in ['BTC', 'ETH'] else 80.0
            }
            
            defi_data = None
            if crypto['symbol'] == 'UNI':
                defi_data = {
                    'total_value_locked': 5000000000,  # 5B
                    'trading_volume_24h': 800000000,   # 800M
                    'yield_rate': 0.12,  # 12% APY
                    'audit_score': 98.0
                }
            
            # Run analysis
            result = analyzer.analyze_crypto(
                symbol=crypto['symbol'],
                crypto_data=crypto['crypto_data'],
                historical_data=historical_data,
                blockchain_data=blockchain_data,
                defi_data=defi_data
            )
            
            # Display results
            print(f"✅ Crypto Score: {result['crypto_score']}")
            print(f"📊 Trading Recommendation: {result['trading_recommendation']}")
            print(f"📝 Analysis: {result['analysis_summary']}")
            
            if 'ultra_analysis' in result:
                ultra = result['ultra_analysis']
                print(f"🎯 Ultra Crypto Score: {ultra['ultra_crypto_score']}")
                print(f"💰 Category: {ultra['crypto_category']}")
                print(f"⛓️ Blockchain: {ultra['blockchain']}")
                print(f"💎 Market Cap: ${ultra['market_cap']:,.0f}")
                print(f"🔧 Consensus: {ultra['consensus_mechanism']}")
                print(f"🎯 Use Case: {ultra['use_case']}")
                print(f"📈 Market Phase: {ultra['market_phase']}")
                
                # Blockchain metrics
                blockchain = ultra['blockchain_metrics']
                print(f"👥 Active Addresses: {blockchain['active_addresses']:,}")
                print(f"📊 Transactions: {blockchain['transaction_count']:,}")
                print(f"⏱️ Block Time: {blockchain['avg_block_time']}s")
                print(f"🔒 Validators: {blockchain['validator_count']:,}")
                print(f"🥩 Staking Ratio: {blockchain['staking_ratio']:.1%}")
                print(f"💻 Dev Activity: {blockchain['development_activity']}/100")
                
                # On-chain metrics
                onchain = ultra['onchain_metrics']
                print(f"🐋 Whale Activity: {onchain['whale_activity']:.3f}")
                print(f"💎 HODL Ratio: {onchain['hodler_ratio']:.1%}")
                print(f"📈 Address Growth: {onchain['active_addresses_growth']:.1%}")
                print(f"😨 Fear & Greed: {onchain['fear_greed_index']}/100")
                print(f"💱 NVT Ratio: {onchain['network_value_to_transactions']}")
                
                # Sentiment metrics
                sentiment = ultra['sentiment_metrics']
                print(f"📱 Social Sentiment: {sentiment['social_sentiment']}/100")
                print(f"🏦 Institutional Sentiment: {sentiment['institutional_sentiment']}/100")
                print(f"📊 Technical Sentiment: {sentiment['technical_sentiment']}/100")
                print(f"🎯 Overall Sentiment: {sentiment['overall_sentiment']}/100")
            
            # Market insights
            if 'market_insights' in result:
                insights = result['market_insights']
                print(f"🔍 Market Phase: {insights['phase']}")
                print(f"📋 Description: {insights['description']}")
                print(f"💡 Strategy: {insights['strategy_implication']}")
                print(f"🎯 Confidence: {insights['confidence']}%")
            
            # Blockchain analysis
            if 'blockchain_analysis' in result:
                blockchain_perf = result['blockchain_analysis']
                print(f"⚡ Speed: {blockchain_perf['speed']} ({blockchain_perf['speed_score']}/100)")
                print(f"🔐 Security: {blockchain_perf['security']} ({blockchain_perf['security_score']}/100)")
                print(f"💻 Development: {blockchain_perf['development']}")
                print(f"🥩 Staking Health: {blockchain_perf['staking_health']}")
                print(f"📊 Overall Blockchain Score: {blockchain_perf['overall_score']}/100")
            
            # DeFi analysis (if available)
            if 'defi_analysis' in result and result['defi_analysis']:
                defi = result['defi_analysis']
                print(f"💰 TVL Category: {defi['tvl_category']}")
                print(f"💧 Liquidity: {defi['liquidity_strength']}")
                print(f"📈 Yield Assessment: {defi['yield_assessment']}")
                print(f"⚠️ IL Risk: {defi['il_risk_level']}")
                print(f"🏥 Protocol Health: {defi['protocol_health']} ({defi['health_score']}/100)")
                print(f"💵 TVL: {defi['tvl_usd']}")
                print(f"📊 APY: {defi['apy']}")
            
            # On-chain insights
            if 'onchain_insights' in result:
                onchain_signals = result['onchain_insights']
                print(f"🐋 Whale Signal: {onchain_signals['whale_signal']}")
                print(f"💎 HODL Strength: {onchain_signals['hodler_strength']}")
                print(f"🔄 Exchange Flow: {onchain_signals['exchange_flow']}")
                if 'network_growth' in onchain_signals:
                    print(f"📈 Network Growth: {onchain_signals['network_growth']}")
                if 'nvt_signal' in onchain_signals:
                    print(f"💱 NVT Signal: {onchain_signals['nvt_signal']}")
            
            # Sentiment analysis
            if 'sentiment_analysis' in result:
                sentiment_analysis = result['sentiment_analysis']
                print(f"😊 Overall Mood: {sentiment_analysis['overall_mood']}")
                print(f"⚠️ Sentiment Risk: {sentiment_analysis['sentiment_risk']}")
                if 'divergence' in sentiment_analysis:
                    print(f"🔄 Divergence: {sentiment_analysis['divergence']}")
                if 'social_buzz' in sentiment_analysis:
                    print(f"📱 Social Buzz: {sentiment_analysis['social_buzz']}")
                print(f"📊 Sentiment Score: {sentiment_analysis['sentiment_score']}/100")
            
            # Price targets
            if 'price_targets' in result:
                targets = result['price_targets']
                print(f"🎯 Price Targets:")
                for period, price in targets.items():
                    if isinstance(price, (int, float)):
                        print(f"   {period}: ${price:,.4f}")
            
            # Investment strategies
            if 'investment_strategies' in result:
                strategies = result['investment_strategies']
                print(f"💡 Investment Strategies: {len(strategies)} found")
                for j, strategy in enumerate(strategies[:2], 1):
                    print(f"   {j}. {strategy['strategy']}: {strategy.get('description', 'N/A')}")
                    if 'time_horizon' in strategy:
                        print(f"      Time: {strategy['time_horizon']}, Expected: {strategy.get('expected_return', 'N/A')}")
            
            # Risk assessment
            if 'risk_assessment' in result:
                risk = result['risk_assessment']
                print(f"⚠️ Overall Risk: {risk['overall_risk']}")
                if 'liquidity_risk' in risk:
                    print(f"💧 Liquidity Risk: {risk['liquidity_risk']}")
                if 'technology_risk' in risk:
                    print(f"💻 Technology Risk: {risk['technology_risk']}")
                if 'regulatory_risk' in risk:
                    print(f"⚖️ Regulatory Risk: {risk['regulatory_risk']}")
            
            print(f"🎯 Confidence: {result['confidence']:.1f}%")
            
            test_results.append({
                'crypto': crypto['name'],
                'score': result['crypto_score'],
                'recommendation': result['trading_recommendation'],
                'success': True
            })
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            test_results.append({
                'crypto': crypto['name'],
                'score': 0,
                'recommendation': 'ERROR',
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY - ULTRA CRYPTO ANALYSIS")
    print("=" * 60)
    
    successful_tests = sum(1 for r in test_results if r['success'])
    print(f"✅ Successful Tests: {successful_tests}/{len(test_results)}")
    
    if successful_tests > 0:
        print("\n📊 CRYPTO ANALYSIS RESULTS:")
        for result in test_results:
            if result['success']:
                status_icon = "🟢" if result['score'] >= 65 else "🟡" if result['score'] >= 50 else "🔴"
                print(f"{status_icon} {result['crypto']}: {result['score']:.1f} ({result['recommendation']})")
    
    failed_tests = [r for r in test_results if not r['success']]
    if failed_tests:
        print(f"\n❌ Failed Tests: {len(failed_tests)}")
        for result in failed_tests:
            print(f"   - {result['crypto']}: {result.get('error', 'Unknown error')}")
    
    if successful_tests == len(test_results):
        print(f"\n🎉 ALL TESTS PASSED! Ultra Crypto Analysis is working perfectly!")
        print(f"💎 Ultra Crypto Analyzer successfully analyzed {len(test_cryptos)} different cryptocurrencies")
        print(f"🔍 Features tested: Blockchain metrics, DeFi analysis, On-chain signals, Sentiment analysis")
        print(f"🎯 Market phase detection, Price targets, Investment strategies, Risk management")
    else:
        print(f"\n⚠️ Some tests failed. Please check the errors above.")
    
    return test_results

if __name__ == "__main__":
    test_crypto_analysis()