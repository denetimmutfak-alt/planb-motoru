"""
ML Analysis Test Suite
ML Analizi Test Paketi
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analysis.ml_analysis import MLAnalyzer
import pandas as pd
import numpy as np

def test_ml_analysis():
    """ML analizi test fonksiyonu"""
    print("=== ML Analysis Test Suite ===\n")
    
    analyzer = MLAnalyzer()
    
    # Test 1: ASELS - Comprehensive analysis
    print("TEST 1: ASELS - Comprehensive ML Analysis")
    print("-" * 50)
    
    asels_data = {
        'financial': {
            'score': 78.5,
            'confidence': 87,
            'pe_ratio': 12.3,
            'roe': 18.5,
            'debt_ratio': 0.25
        },
        'technical': {
            'score': 72.8,
            'confidence': 82,
            'rsi': 65,
            'macd_signal': 'positive',
            'support_level': 45.20
        },
        'ultra_analysis': {
            'volatility_regime': 'Normal',
            'options_signals': {'put_call_ratio': 0.8},
            'risk_assessment': {'overall_risk': 'Orta Risk'}
        },
        'gann_analysis': {
            'score': 69.2,
            'confidence': 75,
            'price_targets': [48.50, 52.30]
        },
        'astrology_analysis': {
            'score': 63.8,
            'confidence': 70,
            'planetary_influence': 'positive'
        },
        'sentiment_analysis': {
            'score': 71.5,
            'social_sentiment': 68,
            'news_sentiment': 74
        },
        'volatility_analysis': {
            'score': 65.3,
            'volatility_regime': 'Normal',
            'risk_assessment': {'overall_risk': 'Düşük-Orta'}
        }
    }
    
    # Create sample historical data
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    np.random.seed(42)
    prices = 46.5 + np.cumsum(np.random.normal(0.1, 0.8, 30))
    volumes = np.random.lognormal(15, 0.3, 30)
    
    historical_data = pd.DataFrame({
        'Date': dates,
        'Close': prices,
        'Volume': volumes
    })
    
    result = analyzer.analyze(
        symbol='ASELS',
        all_analysis_results=asels_data,
        analysis_mode='auto',
        historical_data=historical_data,
        prediction_horizon='medium_term'
    )
    
    print(f"Symbol: ASELS")
    print(f"ML Score: {result['ml_score']:.1f}")
    print(f"Confidence: {result['confidence']:.1f}")
    print(f"Analysis Mode: {result['analysis_mode']}")
    print(f"Primary Signal: {result['trading_signals']['primary_signal']}")
    print(f"Signal Strength: {result['trading_signals']['signal_strength']}")
    overall_risk = result['risk_assessment'].get('overall_risk', 'Orta Risk')
    print(f"Risk Assessment: {overall_risk}")
    print(f"Recommendation: {result['recommendation']}")
    
    if 'feature_importance' in result:
        print("\nTop Features:")
        sorted_features = sorted(result['feature_importance'].items(), 
                               key=lambda x: x[1], reverse=True)[:3]
        for feature, importance in sorted_features:
            print(f"  {feature}: {importance:.3f}")
    
    if 'predictions' in result:
        print(f"\nPredictions:")
        for pred_type, value in result['predictions'].items():
            if isinstance(value, (int, float)):
                print(f"  {pred_type}: {value:.1f}")
            elif isinstance(value, dict):
                print(f"  {pred_type}:")
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (int, float)):
                        print(f"    {sub_key}: {sub_value:.1f}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: THYAO - Simpler analysis
    print("TEST 2: THYAO - Basic ML Analysis")
    print("-" * 50)
    
    thyao_data = {
        'financial': {
            'score': 58.3,
            'confidence': 72,
            'risk_assessment': {'overall_risk': 'Yüksek Risk'}
        },
        'technical': {
            'score': 61.7,
            'confidence': 68
        },
        'sentiment_analysis': {
            'score': 45.2,
            'social_sentiment': 42,
            'news_sentiment': 48
        }
    }
    
    result = analyzer.analyze(
        symbol='THYAO',
        all_analysis_results=thyao_data,
        analysis_mode='basic',
        prediction_horizon='short_term'
    )
    
    print(f"Symbol: THYAO")
    print(f"ML Score: {result['ml_score']:.1f}")
    print(f"Confidence: {result['confidence']:.1f}")
    print(f"Analysis Mode: {result['analysis_mode']}")
    print(f"Primary Signal: {result['trading_signals']['primary_signal']}")
    overall_risk = result['risk_assessment'].get('overall_risk', 'Orta Risk')
    print(f"Risk Assessment: {overall_risk}")
    print(f"Recommendation: {result['recommendation']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: BTCUSDT - Crypto ML Analysis
    print("TEST 3: BTCUSDT - Crypto ML Analysis")
    print("-" * 50)
    
    btc_data = {
        'financial': {
            'score': 82.1,
            'confidence': 89
        },
        'technical': {
            'score': 75.6,
            'confidence': 85
        },
        'crypto_analysis': {
            'score': 73.8,
            'confidence': 80,
            'blockchain_metrics': {
                'network_health': 'strong',
                'on_chain_signals': 'bullish'
            },
            'risk_assessment': {'overall_risk': 'Orta Risk'}
        },
        'sentiment_analysis': {
            'score': 78.2,
            'social_sentiment': 81,
            'news_sentiment': 75
        },
        'volatility_analysis': {
            'score': 55.8,
            'volatility_regime': 'High',
            'risk_assessment': {'overall_risk': 'Yüksek Risk'}
        }
    }
    
    result = analyzer.analyze(
        symbol='BTCUSDT',
        all_analysis_results=btc_data,
        analysis_mode='ultra',
        prediction_horizon='long_term'
    )
    
    print(f"Symbol: BTCUSDT")
    print(f"ML Score: {result['ml_score']:.1f}")
    print(f"Confidence: {result['confidence']:.1f}")
    print(f"Analysis Mode: {result['analysis_mode']}")
    print(f"Primary Signal: {result['trading_signals']['primary_signal']}")
    print(f"Signal Strength: {result['trading_signals']['signal_strength']}")
    overall_risk = result['risk_assessment'].get('overall_risk', 'Orta Risk')
    print(f"Risk Assessment: {overall_risk}")
    print(f"Recommendation: {result['recommendation']}")
    
    if 'ml_insights' in result:
        print(f"\nML Insights:")
        for insight_type, insight_value in result['ml_insights'].items():
            if isinstance(insight_value, str):
                print(f"  {insight_type}: {insight_value}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 4: GOLD - Commodities ML Analysis
    print("TEST 4: GOLD - Commodities ML Analysis")
    print("-" * 50)
    
    gold_data = {
        'financial': {
            'score': 67.4,
            'confidence': 78
        },
        'technical': {
            'score': 69.8,
            'confidence': 82
        },
        'commodities_analysis': {
            'score': 71.2,
            'confidence': 84,
            'commodity_category': 'precious_metals',
            'risk_assessment': {'overall_risk': 'Düşük Risk'}
        },
        'currency_analysis': {
            'score': 58.6,
            'confidence': 72,
            'usd_strength': 'moderate'
        },
        'macro_analysis': {
            'score': 62.3,
            'inflation_hedge': 'strong',
            'economic_uncertainty': 'high'
        }
    }
    
    result = analyzer.analyze(
        symbol='GOLD',
        all_analysis_results=gold_data,
        analysis_mode='auto',
        prediction_horizon='strategic'
    )
    
    print(f"Symbol: GOLD")
    print(f"ML Score: {result['ml_score']:.1f}")
    print(f"Confidence: {result['confidence']:.1f}")
    print(f"Analysis Mode: {result['analysis_mode']}")
    print(f"Primary Signal: {result['trading_signals']['primary_signal']}")
    overall_risk = result['risk_assessment'].get('overall_risk', 'Orta Risk')
    print(f"Risk Assessment: {overall_risk}")
    print(f"Recommendation: {result['recommendation']}")
    
    if 'predictions' in result and 'scenarios' in result.get('predictions', {}):
        print(f"\nScenario Analysis:")
        scenarios = result['predictions']['scenarios']
        if isinstance(scenarios, dict):
            for scenario, value in scenarios.items():
                if isinstance(value, (int, float)):
                    print(f"  {scenario}: {value:.1f}")
    
    print("\n" + "="*50 + "\n")
    
    print("=== ML Analysis Test Suite Completed ===")
    print(f"Total Tests: 4")
    print(f"All tests completed successfully!")
    
    # Performance summary
    print(f"\nAnalyzer Performance:")
    print(f"Ultra ML Available: {analyzer.ultra_available}")
    print(f"Total Predictions: {analyzer.model_performance['total_predictions']}")
    if analyzer.model_performance['total_predictions'] > 0:
        print(f"Average Accuracy: {analyzer.model_performance['average_accuracy']:.3f}")

if __name__ == "__main__":
    test_ml_analysis()