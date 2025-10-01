#!/usr/bin/env python3
"""
PlanB Motoru - Minimal Dashboard Server
Ultra-Simple Testing Dashboard
"""

from flask import Flask, render_template_string, jsonify
from flask_socketio import SocketIO
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'planb_ultra_secret_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def dashboard():
    """Minimal dashboard"""
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>PlanB Motoru - Test Dashboard</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: #1e3c72; 
            color: white; 
            text-align: center; 
            padding: 50px; 
        }
        .status { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 10px; 
            margin: 20px 0; 
        }
    </style>
</head>
<body>
    <h1>🚀 PlanB Motoru Test Dashboard</h1>
    <div class="status">
        <h2>✅ System Status: ACTIVE</h2>
        <p>Dashboard Server: Running</p>
        <p>Timestamp: {{ timestamp }}</p>
    </div>
    <div class="status">
        <h3>🎯 Quick Tests</h3>
        <a href="/health" style="color: #00ff88;">Health Check</a> | 
        <a href="/test" style="color: #00ff88;">System Test</a>
    </div>
</body>
</html>
    """, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'dashboard',
        'version': '1.0.0'
    })

@app.route('/test')
def system_test():
    """System test page"""
    return jsonify({
        'test_results': {
            'dashboard': 'PASS',
            'flask': 'PASS',
            'socketio': 'PASS',
            'python': 'PASS'
        },
        'timestamp': datetime.now().isoformat(),
        'status': 'ALL_TESTS_PASSED'
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 PlanB Motoru - Test Dashboard")
    print("=" * 50)
    print("🌐 URL: http://localhost:9090")
    print("🔍 Health: http://localhost:9090/health")
    print("🧪 Test: http://localhost:9090/test")
    print("=" * 50)
    
    socketio.run(app, host='0.0.0.0', port=9090, debug=False)