#!/usr/bin/env python3
"""
PlanB Motoru Dashboard Başlatıcı
Profesyonel Dashboard + Multi-Expert Engine
"""

from flask import Flask, send_file, jsonify
import os
import sys
import logging

# Multi-Expert Engine import
try:
    from multi_expert_complete import MultiExpertEngine
    MULTI_EXPERT_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Multi-Expert Engine yüklenemiyor: {e}")
    MULTI_EXPERT_AVAILABLE = False

app = Flask(__name__)

# Logging'i azalt
logging.getLogger('werkzeug').setLevel(logging.ERROR)

@app.route("/")
def dashboard():
    """Ana dashboard sayfası - Aktif Motor Dashboard"""
    dashboard_path = os.path.join(os.path.dirname(__file__), "aktif_dashboard.html")
    if os.path.exists(dashboard_path):
        return send_file(dashboard_path)
    else:
        return "<h1>Aktif Dashboard dosyası bulunamadı!</h1>", 404

@app.route("/api/analysis")
def api_analysis():
    """Multi-Expert Engine analizi"""
    if not MULTI_EXPERT_AVAILABLE:
        return jsonify({
            "status": "error",
            "error": "Multi-Expert Engine yüklenemedi",
            "timestamp": "2025-09-20 09:55:00"
        })
    
    try:
        # Multi-Expert Engine başlat
        engine = MultiExpertEngine()
        
        # Test verisi
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
        return jsonify({
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
            "timestamp": "2025-09-20 09:55:00"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": "2025-09-20 09:55:00"
        })

@app.route("/health")
def health_check():
    """Sistem durumu kontrolü"""
    return jsonify({
        "status": "healthy",
        "multi_expert": MULTI_EXPERT_AVAILABLE,
        "timestamp": "2025-09-20 09:55:00"
    })

if __name__ == "__main__":
    print("🚀 PlanB Motoru - Aktif Motor Dashboard Başlatılıyor...")
    print("="*50)
    print("🌐 URL: http://localhost:5001")
    print("📊 Dashboard: Aktif Motor İkonları")
    print("🔥 API: Multi-Expert Engine entegre")
    print(f"⚡ Multi-Expert Status: {'✅ Aktif' if MULTI_EXPERT_AVAILABLE else '❌ Deaktif'}")
    print()
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False,
        use_reloader=False
    )