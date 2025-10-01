#!/usr/bin/env python3
"""
PlanB Motoru - Core API Test Server
FastAPI-based Testing API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional
import random
import json

app = FastAPI(
    title="PlanB Motoru Core API",
    description="Ultra-Professional Market Analysis API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class MarketData(BaseModel):
    symbol: str
    price: float
    volume: int
    timestamp: datetime
    market: str
    change_percent: Optional[float] = None

class PredictionRequest(BaseModel):
    symbol: str
    features: Dict[str, float]

class PredictionResponse(BaseModel):
    symbol: str
    signal: str
    confidence: float
    timestamp: datetime
    model_version: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    services: Dict[str, str]

# Sample data storage
sample_market_data = []

def generate_sample_market_data():
    """Generate sample market data"""
    markets = {
        'BIST': ['THYAO', 'AKBNK', 'ISCTR', 'TCELL', 'SAHOL'],
        'NASDAQ': ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA'],
        'CRYPTO': ['BTC-USD', 'ETH-USD', 'ADA-USD', 'SOL-USD'],
        'FOREX': ['EURUSD', 'GBPUSD', 'USDJPY', 'USDTRY']
    }
    
    data = []
    for market, symbols in markets.items():
        for symbol in symbols:
            price = round(random.uniform(10, 500), 2)
            volume = random.randint(100000, 5000000)
            change = round(random.uniform(-5, 5), 2)
            
            data.append(MarketData(
                symbol=symbol,
                price=price,
                volume=volume,
                timestamp=datetime.now(),
                market=market,
                change_percent=change
            ))
    
    return data

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "🚀 PlanB Motoru Core API",
        "status": "operational",
        "timestamp": datetime.now(),
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "market_data": "/api/v1/market-data",
            "predict": "/api/v1/ml/predict",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        services={
            "api": "running",
            "database": "simulated",
            "ml_engine": "ready",
            "cache": "active"
        }
    )

@app.get("/api/v1/market-data", response_model=List[MarketData], tags=["Market Data"])
async def get_market_data(limit: int = 20):
    """Get latest market data"""
    global sample_market_data
    
    # Generate fresh data
    sample_market_data = generate_sample_market_data()
    
    return sample_market_data[:limit]

@app.get("/api/v1/market-data/latest", response_model=List[MarketData], tags=["Market Data"])
async def get_latest_market_data():
    """Get latest market data"""
    return await get_market_data(25)

@app.get("/api/v1/market-data/{symbol}", response_model=MarketData, tags=["Market Data"])
async def get_symbol_data(symbol: str):
    """Get data for specific symbol"""
    global sample_market_data
    
    if not sample_market_data:
        sample_market_data = generate_sample_market_data()
    
    for data in sample_market_data:
        if data.symbol == symbol:
            return data
    
    raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found")

@app.post("/api/v1/ml/predict", response_model=PredictionResponse, tags=["Machine Learning"])
async def predict_signal(request: PredictionRequest):
    """Generate ML prediction for symbol"""
    # Simulate ML prediction logic
    features = request.features
    
    # Calculate mock score based on features
    score = 0
    if 'rsi' in features:
        score += (70 - features['rsi']) * 0.5  # Lower RSI = higher score
    if 'macd' in features:
        score += features['macd'] * 10  # Positive MACD = higher score
    if 'price' in features:
        score += min(features['price'] / 100, 10)  # Price factor
    
    # Normalize score to 0-100
    score = max(0, min(100, score + 50))
    
    # Determine signal based on score
    if score >= 70:
        signal = "BUY"
        confidence = score / 100
    elif score >= 55:
        signal = "HOLD_STRONG"
        confidence = score / 100
    elif score >= 45:
        signal = "HOLD"
        confidence = score / 100
    elif score >= 30:
        signal = "HOLD_WEAK"
        confidence = score / 100
    else:
        signal = "SELL"
        confidence = (100 - score) / 100
    
    return PredictionResponse(
        symbol=request.symbol,
        signal=signal,
        confidence=round(confidence, 3),
        timestamp=datetime.now(),
        model_version="LightGBM+XGBoost+CNN-LSTM v1.0"
    )

@app.get("/api/v1/telegram/status", tags=["Telegram"])
async def telegram_status():
    """Get Telegram bot status"""
    return {
        "status": "active",
        "bot_configured": True,
        "last_message": datetime.now().isoformat(),
        "active_notifications": 3
    }

@app.get("/api/v1/system/stats", tags=["System"])
async def system_stats():
    """Get system statistics"""
    return {
        "uptime": "0:15:32",
        "total_requests": random.randint(100, 1000),
        "active_connections": random.randint(5, 25),
        "memory_usage": "245 MB",
        "cpu_usage": f"{random.randint(10, 60)}%",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 PLANB MOTORU - CORE API SERVER")
    print("=" * 60)
    print("🌐 API URL: http://localhost:8001")
    print("📚 API Docs: http://localhost:8001/docs")
    print("🔍 Health: http://localhost:8001/health")
    print("📊 Market Data: http://localhost:8001/api/v1/market-data")
    print("🤖 ML Predict: http://localhost:8001/api/v1/ml/predict")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")