from flask import Blueprint, render_template, send_file, request, jsonify
from .analysis import get_multi_expert_analysis
import os

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    # ULTRA Professional Dashboard'u göster
    return render_template("ultra_professional_dashboard.html")

@main_bp.route("/ultra_dashboard")
def ultra_professional_dashboard():
    """ULTRA_PROFESSIONAL_DASHBOARD - Sabit İsim"""
    return render_template("ultra_professional_dashboard.html")

@main_bp.route("/api/analysis")
def api_analysis():
    # Multi-Expert Engine analizi
    analysis_data = get_multi_expert_analysis()
    return analysis_data

@main_bp.route("/api/start_analysis", methods=["POST"])
def start_analysis():
    """Analiz başlatma endpoint'i"""
    try:
        data = request.get_json()
        analysis_type = data.get("analysis_type", "all")
        
        # Analiz tipine göre işlem yap
        if analysis_type == "all":
            message = "Tüm varlıklar analiz ediliyor..."
        elif analysis_type == "bist":
            message = "BIST hisseleri analiz ediliyor..."
        elif analysis_type == "commodity":
            message = "Emtia analizi başlatılıyor..."
        elif analysis_type == "nasdaq":
            message = "NASDAQ analizi başlatılıyor..."
        elif analysis_type == "xetra":
            message = "XETRA analizi başlatılıyor..."
        elif analysis_type == "crypto":
            message = "Kripto analizi başlatılıyor..."
        else:
            message = "Bilinmeyen analiz tipi"
        
        return jsonify({
            "status": "success",
            "message": message,
            "analysis_type": analysis_type
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500