#!/usr/bin/env python3
"""
PlanB Core API - FastAPI Mikroservis
Mevcut FinancialAnalyzer + Multi-Expert Engine'i REST API'ye dönüştürür
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import logging
from datetime import datetime
import os
import pandas as pd
import json

# Mevcut modülleri import et
import sys
sys.path.append('/app')

try:
    from src.analysis.financial_analysis import FinancialAnalyzer
    from multi_expert_engine import MultiExpertEngine, ExpertModule
    from config.settings import config
except ImportError as e:
    logging.error(f"Module import error: {e}")
    # Fallback için dummy classes
    class FinancialAnalyzer:
        def analyze_symbol(self, symbol, data):
            return {"status": "success", "signal": "TUT", "confidence": 50}
    
    class MultiExpertEngine:
        def analyze_ensemble(self, symbol, data):
            return {"status": "success", "signal": "TUT", "confidence": 50}

# FastAPI app
app = FastAPI(
    title="PlanB Motoru Core API",
    description="Financial Analysis & Multi-Expert Ensemble Engine",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
financial_analyzer = FinancialAnalyzer()
multi_expert_engine = MultiExpertEngine()

# Pydantic models
class AnalysisRequest(BaseModel):
    symbol: str
    market: str = "BIST"
    data: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    symbol: str
    timestamp: datetime
    signal: str
    confidence: float
    reasoning: str
    technical_indicators: Dict[str, Any]
    expert_results: List[Dict[str, Any]]
    ensemble_result: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    uptime_seconds: float
    memory_usage_mb: float
    active_connections: int

# Startup event
@app.on_event("startup")
async def startup_event():
    logging.info("PlanB Core API starting up...")
    # Initialize connections, load models, etc.

# Health endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Sistem sağlık kontrolü"""
    import psutil
    import time
    
    # Memory usage
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="2.0.0",
        uptime_seconds=time.time() - startup_time,
        memory_usage_mb=memory_mb,
        active_connections=0  # TODO: Implement connection tracking
    )

# Main analysis endpoint
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_symbol(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Ana analiz endpoint'i
    Hem FinancialAnalyzer hem de Multi-Expert Engine'i çalıştırır
    """
    try:
        # Market data preparation
        if request.data:
            df = pd.DataFrame(request.data)
        else:
            # Dummy data for testing
            df = pd.DataFrame({
                'Close': [100, 101, 102, 101, 103],
                'Volume': [1000, 1100, 900, 1200, 1050],
                'High': [101, 102, 103, 102, 104],
                'Low': [99, 100, 101, 100, 102]
            })
        
        # Financial analysis
        financial_result = financial_analyzer.analyze_symbol(request.symbol, df)
        
        # Technical indicators
        tech_indicators = financial_analyzer.calculate_technical_indicators(df)
        
        # Multi-expert ensemble
        ensemble_result = multi_expert_engine.analyze_ensemble(request.symbol, df)
        
        # Expert results compilation
        expert_results = []
        if hasattr(multi_expert_engine, 'get_module_results'):
            expert_results = multi_expert_engine.get_module_results()
        
        # Final signal determination
        final_signal = ensemble_result.get('signal', 'TUT')
        confidence = ensemble_result.get('confidence', 50.0)
        
        # Background task: Log to database
        background_tasks.add_task(log_analysis_result, {
            'symbol': request.symbol,
            'signal': final_signal,
            'confidence': confidence,
            'timestamp': datetime.now()
        })
        
        return AnalysisResponse(
            symbol=request.symbol,
            timestamp=datetime.now(),
            signal=final_signal,
            confidence=confidence,
            reasoning=ensemble_result.get('reasoning', 'Multi-expert analysis'),
            technical_indicators=tech_indicators,
            expert_results=expert_results,
            ensemble_result=ensemble_result
        )
        
    except Exception as e:
        logging.error(f"Analysis error for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Batch analysis endpoint
@app.post("/analyze/batch")
async def analyze_batch(symbols: List[str], market: str = "BIST"):
    """Toplu analiz endpoint'i"""
    results = []
    
    for symbol in symbols:
        try:
            request = AnalysisRequest(symbol=symbol, market=market)
            result = await analyze_symbol(request, BackgroundTasks())
            results.append(result)
        except Exception as e:
            results.append({
                "symbol": symbol,
                "error": str(e),
                "timestamp": datetime.now()
            })
    
    return {"results": results, "total_processed": len(symbols)}

# Technical indicators endpoint
@app.get("/indicators/{symbol}")
async def get_technical_indicators(symbol: str, market: str = "BIST"):
    """Sadece teknik göstergeler"""
    try:
        # Dummy data - production'da real data
        df = pd.DataFrame({
            'Close': [100, 101, 102, 101, 103],
            'Volume': [1000, 1100, 900, 1200, 1050],
            'High': [101, 102, 103, 102, 104],
            'Low': [99, 100, 101, 100, 102]
        })
        
        indicators = financial_analyzer.calculate_technical_indicators(df)
        return {
            "symbol": symbol,
            "timestamp": datetime.now(),
            "indicators": indicators
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Expert modules endpoint
@app.get("/experts/modules")
async def get_expert_modules():
    """Mevcut expert modüllerinin listesi"""
    try:
        modules = multi_expert_engine.get_registered_modules()
        return {
            "modules": modules,
            "total_count": len(modules),
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Performance metrics endpoint
@app.get("/metrics")
async def get_performance_metrics():
    """Sistem performans metrikleri"""
    import psutil
    
    # System metrics
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "timestamp": datetime.now(),
        "system": {
            "cpu_usage_percent": cpu_percent,
            "memory_usage_percent": memory.percent,
            "memory_available_gb": memory.available / (1024**3),
            "disk_usage_percent": disk.percent,
            "disk_free_gb": disk.free / (1024**3)
        },
        "application": {
            "version": "2.0.0",
            "uptime_seconds": time.time() - startup_time,
            "total_requests": 0  # TODO: Implement request counter
        }
    }

# Background task functions
async def log_analysis_result(result_data: Dict[str, Any]):
    """Analiz sonucunu veritabanına kaydet"""
    try:
        # TODO: Database logging implementation
        logging.info(f"Logged analysis result: {result_data}")
    except Exception as e:
        logging.error(f"Failed to log result: {e}")

# Global variables
startup_time = 0

@app.on_event("startup")
async def set_startup_time():
    global startup_time
    import time
    startup_time = time.time()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
