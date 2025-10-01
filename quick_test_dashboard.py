#!/usr/bin/env python3
"""
PlanB Motoru - Quick Test Dashboard
Port 8080 Test Server
"""

from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Main dashboard"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>PlanB Motoru - Quick Test</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            background: #1e3c72; 
            color: white; 
            text-align: center; 
            padding: 50px; 
        }}
    </style>
</head>
<body>
    <h1>🚀 PlanB Motoru - Quick Test</h1>
    <h2>✅ Status: RUNNING</h2>
    <p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><a href="/health" style="color: #00ff88;">Health Check</a></p>
</body>
</html>
    """

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'quick-test-dashboard'
    })

if __name__ == '__main__':
    print("🚀 Quick Test Dashboard Starting...")
    print("🌐 URL: http://localhost:8080")
    print("🔍 Health: http://localhost:8080/health")
    
    app.run(host='0.0.0.0', port=8080, debug=False)