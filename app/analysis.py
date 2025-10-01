import pandas as pd
import ta
from multi_expert_complete import MultiExpertEngine
import json

def get_indicator():
    """Eski basit RSI hesaplama (geriye uyumluluk için)"""
    df = pd.DataFrame({
        "close": [100, 102, 105, 107, 110],
        "high": [102, 106, 108, 110, 112],
        "low": [98, 100, 103, 105, 108],
        "open": [99, 101, 104, 106, 109],
        "volume": [1000, 1100, 1200, 1250, 1300]
    })
    rsi = ta.momentum.RSIIndicator(close=df["close"]).rsi()
    return rsi.tolist()

def get_multi_expert_analysis():
    """25 modüllü Multi-Expert Engine analizi"""
    try:
        # Multi-Expert Engine başlat
        engine = MultiExpertEngine()
        
        # Test verisi - gerçek API'den alınacak
        test_data = {
            'symbol': 'BIST100',
            'price': 10000.0,
            'volume': 1000000,
            'market_cap': 5000000000,
            'sector': 'INDEX',
            'currency': 'TRY'
        }
        
        # Analiz yap
        result = engine.analyze(test_data)
        
        # JSON formatında sonuç döndür
        return {
            "status": "success",
            "final_score": round(result.final_score, 2),
            "confidence_level": result.confidence_level,
            "consensus_strength": round(result.consensus_strength * 100, 1),
            "module_count": len(engine.modules),
            "weight_sum": round(sum(engine.module_weights.values()), 3),
            "top_contributors": sorted(
                result.module_contributions.items(), 
                key=lambda x: abs(x[1]), 
                reverse=True
            )[:8] if result.module_contributions else [],
            "signal": "AL" if result.final_score >= 70 else "SAT" if result.final_score <= 30 else "TUT",
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }