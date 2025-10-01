#!/usr/bin/env python3
"""
Simple Dashboard Server - Test
"""

from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    """Ana dashboard sayfası"""
    dashboard_path = os.path.join(os.path.dirname(__file__), "aktif_dashboard.html")
    if os.path.exists(dashboard_path):
        return send_file(dashboard_path)
    else:
        return "<h1>Dashboard dosyası bulunamadı!</h1>", 404

@app.route("/health")
def health():
    """Sistem durumu"""
    return {"status": "ok", "port": 5003}

if __name__ == "__main__":
    print("🚀 Simple Dashboard Server - Port 5003")
    print("🌐 URL: http://localhost:5003")
    print("📊 Dashboard: Aktif Motor İkonları")
    
    app.run(
        host='127.0.0.1',
        port=5003,
        debug=False,
        use_reloader=False,
        threaded=True
    )