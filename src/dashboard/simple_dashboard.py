#!/usr/bin/env python3
"""
Basit ve Güvenilir Dashboard
Sadece test modu için optimize edilmiş
"""

from flask import Flask, render_template_string, jsonify, request
import threading
import json
import os
import sys
from datetime import datetime

# Proje kök dizinini path'e ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.analysis_engine import PlanBAnalysisEngine
from src.utils.logger import log_info, log_error, log_success
from src.dashboard.websocket_handler import start_websocket_server, send_analysis_update_sync
from src.portfolio.portfolio_manager import portfolio_manager
# AI Trading Bot import (optional)
try:
    from src.ai.trading_bot import ai_trading_bot
except ImportError:
    ai_trading_bot = None


# Analiz ilerleme durumu için global değişkenler
analysis_progress = {
    'progress': 0.0,
    'eta_seconds': None,
    'status': 'idle',
    'start_time': None,
    'total': 0,
    'completed': 0
}
analysis_progress_lock = threading.Lock()

app = Flask(__name__)

# HTML Template - Basit ve Temiz
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlanB Motoru - Test Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 10px;
        }
        
        /* Mobile First Responsive Design */
        @media (max-width: 768px) {
            body { padding: 5px; }
            .container { margin: 0; border-radius: 10px; }
            .header { padding: 20px; }
            .header h1 { font-size: 1.8em; }
            .header p { font-size: 1em; }
            .content { padding: 15px; }
            .btn { 
                padding: 12px 20px; 
                font-size: 1em; 
                margin: 5px;
                width: 100%;
                max-width: 300px;
            }
            .market-buttons { 
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                gap: 10px;
            }
            .market-btn { 
                width: 100%; 
                max-width: 280px; 
                padding: 15px;
                font-size: 1.1em;
            }
            .results table { 
                font-size: 0.8em; 
                overflow-x: auto;
                display: block;
                white-space: nowrap;
            }
            .results th, .results td { 
                padding: 8px 4px; 
                min-width: 80px;
            }
            .log-content { 
                font-size: 0.9em; 
                max-height: 200px;
            }
        }
        
        @media (max-width: 480px) {
            .header h1 { font-size: 1.5em; }
            .header p { font-size: 0.9em; }
            .content { padding: 10px; }
            .btn { 
                padding: 10px 15px; 
                font-size: 0.9em;
            }
            .market-btn { 
                padding: 12px;
                font-size: 1em;
            }
            .results table { 
                font-size: 0.7em;
            }
            .results th, .results td { 
                padding: 6px 2px; 
                min-width: 70px;
            }
        }
        
        /* Tablet Responsive */
        @media (min-width: 769px) and (max-width: 1024px) {
            .container { max-width: 95%; }
            .market-buttons { 
                display: grid; 
                grid-template-columns: repeat(2, 1fr); 
                gap: 15px;
            }
            .results table { font-size: 0.9em; }
        }
        
        /* Desktop Optimizations */
        @media (min-width: 1025px) {
            .market-buttons { 
                display: grid; 
                grid-template-columns: repeat(3, 1fr); 
                gap: 20px;
            }
        }
        
        /* Mobile Navigation */
        .mobile-nav {
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            border-top: 1px solid #ddd;
            padding: 10px;
            z-index: 1000;
        }
        
        .mobile-nav-btn {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 8px;
            background: none;
            border: none;
            color: #666;
            font-size: 0.8em;
            cursor: pointer;
            flex: 1;
        }
        
        .mobile-nav-btn.active {
            color: #007bff;
        }
        
        .mobile-nav-btn i {
            font-size: 1.2em;
            margin-bottom: 4px;
        }
        
        @media (max-width: 768px) {
            .mobile-nav {
                display: flex;
            }
            body {
                padding-bottom: 80px;
            }
        }
        
        /* Touch-friendly buttons */
        @media (hover: none) and (pointer: coarse) {
            .btn, .market-btn {
                min-height: 44px;
                touch-action: manipulation;
            }
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            padding: 30px; 
            text-align: center; 
            position: relative;
            overflow: hidden;
        }
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="40" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="40" cy="80" r="1.5" fill="rgba(255,255,255,0.1)"/></svg>');
            animation: float 6s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        .header h1 { 
            font-size: 2.5em; 
            margin-bottom: 10px; 
            position: relative; 
            z-index: 1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header p { 
            font-size: 1.2em; 
            opacity: 0.9; 
            position: relative; 
            z-index: 1;
        }
        .content { padding: 30px; }
        .status-card { 
            background: #f8f9fa; 
            border-radius: 10px; 
            padding: 20px; 
            margin-bottom: 20px; 
            border-left: 5px solid #28a745;
        }
        .status-card.error { border-left-color: #dc3545; }
        .status-card.warning { border-left-color: #ffc107; }
        .btn { 
            background: linear-gradient(135deg, #28a745, #20c997); 
            color: white; 
            border: none; 
            padding: 15px 30px; 
            border-radius: 8px; 
            font-size: 1.1em; 
            cursor: pointer; 
            transition: all 0.3s ease;
            margin: 10px;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
            position: relative;
            overflow: hidden;
        }
        .btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        .btn:hover::before {
            left: 100%;
        }
        .btn:hover { 
            transform: translateY(-3px); 
            box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
        }
        .btn:disabled { 
            background: #6c757d; 
            cursor: not-allowed; 
            transform: none; 
            box-shadow: none;
        }
        .market-btn {
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            text-align: center;
        }
        .results { 
            margin-top: 30px; 
            background: #f8f9fa; 
            border-radius: 10px; 
            padding: 20px; 
            min-height: 200px;
        }
        .results-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .results-table th {
            background: #2c3e50;
            color: white;
            padding: 15px 8px;
            text-align: left;
            font-weight: bold;
            font-size: 0.85em;
        }
        .results-table td {
            padding: 10px 8px;
            border-bottom: 1px solid #ecf0f1;
            font-size: 0.8em;
        }
        .results-table tr:hover {
            background: #f8f9fa;
        }
        .symbol-card { 
            background: white; 
            border-radius: 8px; 
            padding: 15px; 
            margin: 10px 0; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #007bff;
        }
        .symbol-name { font-weight: bold; font-size: 1.2em; color: #2c3e50; }
        .symbol-score { font-size: 1.1em; margin: 5px 0; }
        .symbol-signal { 
            padding: 5px 10px; 
            border-radius: 5px; 
            font-weight: bold; 
            display: inline-block;
        }
        .signal-buy { background: #d4edda; color: #155724; }
        .signal-sell { background: #f8d7da; color: #721c24; }
        .signal-hold { background: #fff3cd; color: #856404; }
        .loading { 
            text-align: center; 
            padding: 40px; 
            color: #6c757d; 
        }
        .spinner { 
            border: 4px solid #f3f3f3; 
            border-top: 4px solid #3498db; 
            border-radius: 50%; 
            width: 40px; 
            height: 40px; 
            animation: spin 2s linear infinite; 
            margin: 0 auto 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .log { 
            background: #2c3e50; 
            color: #ecf0f1; 
            padding: 15px; 
            border-radius: 8px; 
            font-family: 'Courier New', monospace; 
            font-size: 0.9em; 
            max-height: 300px; 
            overflow-y: auto; 
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 PlanB Motoru</h1>
            <p>Tam Mod Dashboard - Tüm Semboller</p>
        </div>
        
        <div class="content">
            <div class="status-card" id="statusCard">
                <h3>📊 Sistem Durumu</h3>
                <p id="statusText">Hazır - Analiz başlatmak için butona basın</p>
                <div id="progressBarContainer" style="display:none; margin-top:10px;">
                    <div style="background:#e9ecef; border-radius:8px; height:18px; width:100%;">
                        <div id="progressBar" style="background:linear-gradient(90deg,#28a745,#20c997); height:18px; border-radius:8px; width:0%; transition:width 0.3s;"></div>
                    </div>
                    <div style="margin-top:4px; font-size:0.95em; color:#333;">
                        <span id="progressPercent">0%</span> | Kalan süre: <span id="progressEta">-</span>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <h3>🎯 Analiz Seçenekleri</h3>
                <div style="margin: 20px 0;">
                    <button class="btn" id="analyzeBtn" onclick="startAnalysis('all')">
                        🔍 Tüm Piyasalar (392 Sembol)
                    </button>
                </div>
                
                <div class="market-buttons" style="margin: 20px 0;">
                    <button class="btn market-btn" onclick="startAnalysis('bist')" style="background: linear-gradient(135deg, #e74c3c, #c0392b);">
                        🇹🇷 BIST (300+ Sembol)
                    </button>
                    <button class="btn market-btn" onclick="startAnalysis('nasdaq')" style="background: linear-gradient(135deg, #3498db, #2980b9);">
                        🇺🇸 NASDAQ (110 Sembol)
                    </button>
                    <button class="btn market-btn" onclick="startAnalysis('xetra')" style="background: linear-gradient(135deg, #9b59b6, #8e44ad);">
                        🇩🇪 XETRA (125 Sembol)
                    </button>
                    <button class="btn market-btn" onclick="startAnalysis('crypto')" style="background: linear-gradient(135deg, #f39c12, #e67e22);">
                        ₿ Crypto (50 Sembol)
                    </button>
                    <button class="btn market-btn" onclick="startAnalysis('commodities')" style="background: linear-gradient(135deg, #27ae60, #229954);">
                        🥇 Emtia (28 Sembol)
                    </button>
                </div>
                
                <!-- AI Trading Bot Section -->
                <div class="ai-bot-section" style="margin: 30px 0; padding: 20px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px; color: white;">
                    <h3 style="text-align: center; margin-bottom: 20px;">🤖 AI Trading Bot</h3>
                    <div class="bot-controls" style="display: flex; justify-content: center; gap: 10px; margin-bottom: 20px; flex-wrap: wrap;">
                        <button onclick="startTradingBot('conservative')" class="bot-btn" style="background: #27ae60; color: white; border: none; padding: 10px 15px; border-radius: 8px; cursor: pointer;">Conservative</button>
                        <button onclick="startTradingBot('moderate')" class="bot-btn" style="background: #f39c12; color: white; border: none; padding: 10px 15px; border-radius: 8px; cursor: pointer;">Moderate</button>
                        <button onclick="startTradingBot('aggressive')" class="bot-btn" style="background: #e74c3c; color: white; border: none; padding: 10px 15px; border-radius: 8px; cursor: pointer;">Aggressive</button>
                        <button onclick="stopTradingBot()" class="bot-btn" style="background: #95a5a6; color: white; border: none; padding: 10px 15px; border-radius: 8px; cursor: pointer;">Stop Bot</button>
                    </div>
                    <div id="bot-status" class="bot-status" style="text-align: center;">
                        <p>Bot Status: <span id="bot-status-text" style="font-weight: bold;">Inactive</span></p>
                        <p>Mode: <span id="bot-mode-text" style="font-weight: bold;">-</span></p>
                        <p>Total Trades: <span id="bot-trades-text" style="font-weight: bold;">0</span></p>
                        <p>Win Rate: <span id="bot-winrate-text" style="font-weight: bold;">0%</span></p>
                    </div>
                </div>
                
                <button class="btn" onclick="refreshData()" style="background: linear-gradient(135deg, #6c757d, #5a6268);">
                    🔄 Verileri Yenile
                </button>
            </div>
            
            <div class="results" id="results">
                <h3>📈 Analiz Sonuçları</h3>
                <div id="resultsContent">
                    <div class="loading">
                        <div class="spinner"></div>
                        <p>Analiz sonuçları burada görünecek...</p>
                    </div>
                </div>
            </div>
            
            <div class="log" id="log">
                <strong>📝 Sistem Logları:</strong><br>
                <div id="logContent">Dashboard başlatıldı - Hazır</div>
            </div>
        </div>
    </div>

    <script>
        let isAnalyzing = false;
        let websocket = null;
        
        // WebSocket bağlantısı kur
        function connectWebSocket() {
            try {
                websocket = new WebSocket('ws://localhost:8765');
                
                websocket.onopen = function(event) {
                    console.log('WebSocket bağlantısı kuruldu');
                    addLog('🔗 Real-time güncellemeler aktif');
                };
                
                websocket.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    handleWebSocketMessage(data);
                };
                
                websocket.onclose = function(event) {
                    console.log('WebSocket bağlantısı kapandı');
                    addLog('❌ Real-time güncellemeler durdu');
                    // 5 saniye sonra yeniden bağlanmayı dene
                    setTimeout(connectWebSocket, 5000);
                };
                
                websocket.onerror = function(error) {
                    console.error('WebSocket hatası:', error);
                };
                
            } catch (error) {
                console.error('WebSocket bağlantı hatası:', error);
            }
        }
        
        // WebSocket mesajlarını işle
        function handleWebSocketMessage(data) {
            switch(data.type) {
                case 'welcome':
                    addLog('✅ ' + data.message);
                    break;
                case 'price_update':
                    updatePriceDisplay(data.symbol, data.data);
                    break;
                case 'analysis_update':
                    updateAnalysisDisplay(data.symbol, data.data);
                    break;
                case 'alert':
                    showAlert(data.data);
                    break;
                case 'pong':
                    // Ping-pong için
                    break;
            }
        }
        
        // Fiyat güncellemesini göster
        function updatePriceDisplay(symbol, priceData) {
            addLog(`📈 ${symbol}: ${priceData.price} (${priceData.change}%)`);
        }
        
        // Analiz güncellemesini göster
        function updateAnalysisDisplay(symbol, analysisData) {
            const score = analysisData.total_score || 0;
            const signal = analysisData.signal || 'TUT';
            addLog(`📊 ${symbol}: Skor ${score}/100, Sinyal: ${signal}`);
        }
        
        // Uyarı göster
        function showAlert(alertData) {
            addLog(`🚨 UYARI: ${alertData.message}`);
        }
        
        // Sayfa yüklendiğinde WebSocket bağlantısını kur
        window.addEventListener('load', function() {
            connectWebSocket();
        });
        
        function addLog(message) {
            const logContent = document.getElementById('logContent');
            const timestamp = new Date().toLocaleTimeString();
            logContent.innerHTML += `<br>[${timestamp}] ${message}`;
            logContent.scrollTop = logContent.scrollHeight;
        }
        
        function updateStatus(message, type = 'info') {
            const statusCard = document.getElementById('statusCard');
            const statusText = document.getElementById('statusText');
            
            statusText.textContent = message;
            statusCard.className = 'status-card';
            if (type === 'error') statusCard.classList.add('error');
            if (type === 'warning') statusCard.classList.add('warning');
        }
        
        // Analiz ilerleme çubuğunu güncelle
        function showProgressBar(show) {
            const container = document.getElementById('progressBarContainer');
            if (container) container.style.display = show ? '' : 'none';
        }
        function updateProgressBar(progress, eta, status, completed, total) {
            const bar = document.getElementById('progressBar');
            const percent = document.getElementById('progressPercent');
            const etaSpan = document.getElementById('progressEta');
            const pct = Math.round(progress * 100);
            if (bar) bar.style.width = pct + '%';
            if (percent) percent.textContent = pct + '%';
            if (etaSpan) etaSpan.textContent = eta !== null && eta !== undefined ? formatEta(eta) : '-';
        }
        function formatEta(seconds) {
            if (seconds === 0) return 'Bitti';
            if (!seconds || seconds < 0) return '-';
            const m = Math.floor(seconds / 60);
            const s = seconds % 60;
            return (m > 0 ? m + ' dk ' : '') + s + ' sn';
        }
        let progressInterval = null;
        function startProgressPolling() {
            showProgressBar(true);
            if (progressInterval) clearInterval(progressInterval);
            progressInterval = setInterval(async () => {
                try {
                    const resp = await fetch('/api/analyze/progress');
                    if (resp.ok) {
                        const data = await resp.json();
                        updateProgressBar(data.progress, data.eta_seconds, data.status, data.completed, data.total);
                        if (data.status === 'completed' || data.status === 'error') {
                            clearInterval(progressInterval);
                            setTimeout(() => showProgressBar(false), 2000);
                        }
                    }
                } catch (e) {}
            }, 1000);
        }
        function stopProgressPolling() {
            if (progressInterval) clearInterval(progressInterval);
            showProgressBar(false);
        }
        
        async function startAnalysis(market = 'all') {
            if (isAnalyzing) return;
            
            isAnalyzing = true;
            
            // Tüm butonları devre dışı bırak
            const allBtns = document.querySelectorAll('.btn');
            allBtns.forEach(btn => {
                btn.disabled = true;
                if (btn.onclick && btn.onclick.toString().includes('startAnalysis')) {
                    btn.textContent = '⏳ Analiz Çalışıyor...';
                }
            });
            
            const marketNames = {
                'all': 'Tüm Piyasalar',
                'bist': 'BIST',
                'nasdaq': 'NASDAQ', 
                'xetra': 'XETRA',
                'crypto': 'Crypto',
                'commodities': 'Emtia'
            };
            
            updateStatus(`${marketNames[market]} analizi başlatılıyor...`, 'warning');
            addLog(`${marketNames[market]} analizi başlatıldı`);
            startProgressPolling();
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        test_mode: false,
                        market: market
                    })
                });
                
                if (response.ok) {
                    const result = await response.json();
                    updateStatus(`${marketNames[market]} analizi tamamlandı!`, 'info');
                    addLog(`${marketNames[market]} analizi tamamlandı: ${result.message}`);
                    displayResults(result);
                } else {
                    throw new Error('Analiz başarısız');
                }
            } catch (error) {
                updateStatus('Analiz hatası: ' + error.message, 'error');
                addLog('HATA: ' + error.message);
            } finally {
                isAnalyzing = false;
                stopProgressPolling();
                
                // Tüm butonları tekrar aktif et
                allBtns.forEach(btn => {
                    btn.disabled = false;
                    if (btn.onclick && btn.onclick.toString().includes('startAnalysis')) {
                        const marketType = btn.onclick.toString().match(/startAnalysis\\('(\\w+)'\\)/);
                        if (marketType) {
                            const market = marketType[1];
                            const marketTexts = {
                                'all': '🔍 Tüm Piyasalar (392 Sembol)',
                                'bist': '🇹🇷 BIST (300+ Sembol)',
                                'nasdaq': '🇺🇸 NASDAQ (110 Sembol)',
                                'xetra': '🇩🇪 XETRA (125 Sembol)',
                                'crypto': '₿ Crypto (50 Sembol)',
                                'commodities': '🥇 Emtia (28 Sembol)'
                            };
                            btn.textContent = marketTexts[market] || 'Analiz Başlat';
                        }
                    }
                });
            }
        }
        
        function displayResults(result) {
            const resultsContent = document.getElementById('resultsContent');
            
            if (result.results && result.results.length > 0) {
                let html = '<h4>✅ Başarılı Analizler:</h4>';
                html += `
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>Tarih/Saat</th>
                                <th>Hisse Kodu</th>
                                <th>Güncel Fiyat</th>
                                <th>Toplam Puan</th>
                                <th>Sinyal</th>
                                <th>Pazar</th>
                                <th>AL Ne Zaman</th>
                                <th>TUT Ne Zamana</th>
                            </tr>
                        </thead>
                        <tbody>
                `;
                
                result.results.forEach(item => {
                    const signalClass = item.signal === 'AL' ? 'signal-buy' : 
                                      item.signal === 'SAT' ? 'signal-sell' : 'signal-hold';
                    const score = (item.total_score && !isNaN(item.total_score)) ? item.total_score.toFixed(1) : 'N/A';
                    const currentPrice = (item.current_price && !isNaN(item.current_price)) ? item.current_price.toFixed(2) : 'N/A';
                    const market = getMarketType(item.symbol);
                    const analysisTime = new Date().toLocaleString('tr-TR');
                    const alTime = item.signal === 'AL' ? 'Şimdi' : '-';
                    const tutTime = (item.signal === 'TUT' || item.signal === 'AL') ? 
                        (item.hold_days ? `${item.hold_days} gün` : 'Belirsiz') : '-';
                    
                    
                    html += `
                        <tr>
                            <td>${analysisTime}</td>
                            <td><strong>${item.symbol}</strong></td>
                            <td>$${currentPrice}</td>
                            <td><strong>${score}</strong></td>
                            <td><span class="symbol-signal ${signalClass}">${item.signal || 'TUT'}</span></td>
                            <td>${market}</td>
                            <td>${alTime}</td>
                            <td>${tutTime}</td>
                        </tr>
                    `;
                });
                
                html += '</tbody></table>';
                resultsContent.innerHTML = html;
            } else {
                resultsContent.innerHTML = '<div class="loading"><p>❌ Analiz sonucu bulunamadı</p></div>';
            }
        }
        
        function getMarketType(symbol) {
            if (symbol.endsWith('.IS')) return 'BIST';
            if (symbol.endsWith('.DE')) return 'XETRA';
            if (symbol.endsWith('-USD')) return 'Crypto';
            if (symbol.includes('=F')) return 'Commodity';
            return 'NASDAQ';
        }
        
        async function refreshData() {
            addLog('Veriler yenileniyor...');
            try {
                const response = await fetch('/api/data');
                if (response.ok) {
                    addLog('Veriler başarıyla yenilendi');
                } else {
                    addLog('Veri yenileme hatası');
                }
            } catch (error) {
                addLog('HATA: ' + error.message);
            }
        }
        
        // AI Trading Bot Functions
        function startTradingBot(mode) {
            fetch('/api/trading-bot/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mode: mode })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateBotStatus();
                    addLog(`AI Trading Bot başlatıldı - Mod: ${mode}`, 'success');
                } else {
                    addLog(`Bot başlatma hatası: ${data.message}`, 'error');
                }
            })
            .catch(error => {
                addLog(`Bot başlatma hatası: ${error}`, 'error');
            });
        }
        
        function stopTradingBot() {
            fetch('/api/trading-bot/stop', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateBotStatus();
                    addLog('AI Trading Bot durduruldu', 'success');
                } else {
                    addLog(`Bot durdurma hatası: ${data.message}`, 'error');
                }
            })
            .catch(error => {
                addLog(`Bot durdurma hatası: ${error}`, 'error');
            });
        }
        
        function updateBotStatus() {
            fetch('/api/trading-bot/status')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('bot-status-text').textContent = data.status;
                    document.getElementById('bot-mode-text').textContent = data.mode || '-';
                    document.getElementById('bot-trades-text').textContent = data.total_trades || 0;
                    document.getElementById('bot-winrate-text').textContent = (data.win_rate || 0) + '%';
                }
            })
            .catch(error => {
                console.error('Bot durum güncelleme hatası:', error);
            });
        }
        
        // Bot durumunu periyodik olarak güncelle
        setInterval(updateBotStatus, 5000);
        
        // Mobile Navigation Functions
        function showSection(section) {
            // Mobile nav button states
            document.querySelectorAll('.mobile-nav-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.closest('.mobile-nav-btn').classList.add('active');
            
            // Section switching logic
            switch(section) {
                case 'analysis':
                    addLog('📊 Analiz bölümü aktif');
                    break;
                case 'portfolio':
                    addLog('💼 Portfolio bölümü aktif');
                    loadPortfolios();
                    break;
                case 'alerts':
                    addLog('🔔 Uyarılar bölümü aktif');
                    loadAlerts();
                    break;
                case 'settings':
                    addLog('⚙️ Ayarlar bölümü aktif');
                    break;
            }
        }
        
        // Portfolio functions
        async function loadPortfolios() {
            try {
                const response = await fetch('/api/portfolios');
                const data = await response.json();
                if (data.status === 'success') {
                    addLog(`💼 ${data.portfolios.length} portfolio yüklendi`);
                }
            } catch (error) {
                addLog('❌ Portfolio yüklenemedi: ' + error.message);
            }
        }
        
        // Alert functions
        async function loadAlerts() {
            try {
                addLog('🔔 Uyarılar yükleniyor...');
                // Alert API calls will be added later
            } catch (error) {
                addLog('❌ Uyarılar yüklenemedi: ' + error.message);
            }
        }
        
        // Touch gesture support
        let touchStartX = 0;
        let touchStartY = 0;
        
        document.addEventListener('touchstart', function(e) {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        });
        
        document.addEventListener('touchend', function(e) {
            if (!touchStartX || !touchStartY) return;
            
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            
            const diffX = touchStartX - touchEndX;
            const diffY = touchStartY - touchEndY;
            
            // Horizontal swipe detection
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                if (diffX > 0) {
                    // Swipe left - next section
                    addLog('👈 Sol kaydırma algılandı');
                } else {
                    // Swipe right - previous section
                    addLog('👉 Sağ kaydırma algılandı');
                }
            }
            
            touchStartX = 0;
            touchStartY = 0;
        });
        
        // Sayfa yüklendiğinde
        document.addEventListener('DOMContentLoaded', function() {
            addLog('Dashboard yüklendi');
            refreshData();
            updateMarketCounts();
            
            // Mobile detection
            if (window.innerWidth <= 768) {
                addLog('📱 Mobil cihaz algılandı');
            }
        });

        // Varlık sayılarını güncelle
        async function updateMarketCounts() {
            try {
                const response = await fetch('/api/markets/counts');
                if (response.ok) {
                    const data = await response.json();
                    if (data.status === 'success') {
                        const counts = data.counts;
                        // Buton metinlerini güncelle
                        const buttons = {
                            'all': `🔍 Tüm Piyasalar (${counts.all} Sembol)`,
                            'bist': `🇹🇷 BIST (${counts.bist} Sembol)`,
                            'nasdaq': `🇺🇸 NASDAQ (${counts.nasdaq} Sembol)`,
                            'xetra': `🇩🇪 XETRA (${counts.xetra} Sembol)`,
                            'crypto': `₿ Crypto (${counts.crypto} Sembol)`,
                            'commodities': `🥇 Emtia (${counts.commodities} Sembol)`
                        };
                        
                        document.querySelectorAll('.btn, .market-btn').forEach(btn => {
                            const onclick = btn.getAttribute('onclick');
                            if (onclick && onclick.includes('startAnalysis')) {
                                const market = onclick.match(/startAnalysis\\('([\\w]+)'\\)/);
                                if (market && buttons[market[1]]) {
                                    btn.textContent = buttons[market[1]];
                                }
                            }
                        });
                        
                        addLog(`📊 Varlık sayıları güncellendi: ${counts.all} toplam sembol`);
                    }
                }
            } catch (error) {
                addLog('❌ Varlık sayıları güncellenemedi: ' + error.message);
            }
        }
    </script>
    
    <!-- Mobile Navigation -->
    <div class="mobile-nav">
        <button class="mobile-nav-btn active" onclick="showSection('analysis')">
            <i>📊</i>
            <span>Analiz</span>
        </button>
        <button class="mobile-nav-btn" onclick="showSection('portfolio')">
            <i>💼</i>
            <span>Portfolio</span>
        </button>
        <button class="mobile-nav-btn" onclick="showSection('alerts')">
            <i>🔔</i>
            <span>Uyarılar</span>
        </button>
        <button class="mobile-nav-btn" onclick="showSection('settings')">
            <i>⚙️</i>
            <span>Ayarlar</span>
        </button>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Ana sayfa"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data')
def get_data():
    """Veri durumu"""
    try:
        return jsonify({
            'status': 'success',
            'message': 'Dashboard çalışıyor',
            'timestamp': datetime.now().isoformat(),
            'test_mode': False
        })
    except Exception as e:
        log_error(f"Veri alma hatası: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analiz başlat"""
    try:
        data = request.get_json() or {}
        market_filter = data.get('market', 'all')
        
        log_info(f"Dashboard'dan analiz başlatıldı - Market: {market_filter}")
        

        # Analiz ilerleme durumunu başlat
        with analysis_progress_lock:
            analysis_progress['progress'] = 0.0
            analysis_progress['eta_seconds'] = None
            analysis_progress['status'] = 'running'
            analysis_progress['start_time'] = datetime.now().timestamp()
            analysis_progress['total'] = 0
            analysis_progress['completed'] = 0

        # Analiz motorunu başlat
        engine = PlanBAnalysisEngine()

        # Sembolleri getir ve market filtresi uygula
        symbols = engine.market_data.get_all_symbols(test_mode=False)
        if market_filter != 'all':
            symbols = engine._filter_symbols_by_market(symbols, market_filter)
        total_symbols = len(symbols)
        with analysis_progress_lock:
            analysis_progress['total'] = total_symbols

        import time
        results = []
        start_time = time.time()
        for idx, symbol in enumerate(symbols, 1):
            result = engine.analyze_single_symbol(symbol)
            if result:
                results.append(result)
            # İlerleme ve ETA hesapla
            with analysis_progress_lock:
                analysis_progress['completed'] = idx
                analysis_progress['progress'] = idx / total_symbols if total_symbols else 1.0
                elapsed = time.time() - start_time
                if idx > 0:
                    eta = (elapsed / idx) * (total_symbols - idx)
                    analysis_progress['eta_seconds'] = int(eta)
        
        with analysis_progress_lock:
            analysis_progress['status'] = 'completed'
            analysis_progress['progress'] = 1.0
            analysis_progress['eta_seconds'] = 0

        if results and len(results) > 0:
            log_success("Analiz başarıyla tamamlandı")
            # WebSocket ile real-time güncelleme gönder
            try:
                for analysis_result in results[:5]:  # İlk 5 sonucu gönder
                    symbol = analysis_result.get('symbol', '')
                    if symbol:
                        send_analysis_update_sync(symbol, analysis_result)
            except Exception as e:
                log_error(f"WebSocket güncellemesi gönderilirken hata: {e}")
            # JSON serialization için numpy tiplerini, NaN ve Infinity değerlerini düzelt
            def fix_json_types(obj):
                import math
                if hasattr(obj, 'item'):  # numpy scalar
                    val = obj.item()
                    if isinstance(val, float):
                        if math.isnan(val) or math.isinf(val):
                            return None
                    return val
                elif isinstance(obj, float):
                    if math.isnan(obj) or math.isinf(obj):
                        return None
                elif isinstance(obj, dict):
                    return {k: fix_json_types(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [fix_json_types(item) for item in obj]
                else:
                    return obj
            fixed_result = fix_json_types(results);
            return jsonify({
                'status': 'success',
                'message': 'Analiz tamamlandı',
                'results': fixed_result,
                'total_analyzed': len(results),
                'successful': len([r for r in results if r and r.get('status') == 'success'])
            })
        else:
            log_error("Analiz başarısız")
            return jsonify({
                'status': 'error',
                'message': 'Analiz başarısız',
                'results': []
            }), 500
    except Exception as e:
        log_error(f"Analiz hatası: {e}")
        with analysis_progress_lock:
            analysis_progress['status'] = 'error'
        return jsonify({
            'status': 'error',
            'message': str(e),
            'results': []
        }), 500


# Analiz ilerleme durumunu dönen endpoint
@app.route('/api/analyze/progress', methods=['GET'])
def get_analysis_progress():
    with analysis_progress_lock:
        return jsonify({
            'progress': analysis_progress['progress'],
            'eta_seconds': analysis_progress['eta_seconds'],
            'status': analysis_progress['status'],
            'total': analysis_progress['total'],
            'completed': analysis_progress['completed']
        })

# Varlık sayılarını dönen endpoint
@app.route('/api/markets/counts', methods=['GET'])
def get_market_counts():
    try:
        engine = PlanBAnalysisEngine()
        all_symbols = engine.market_data.get_all_symbols(test_mode=False)
        
        counts = {
            'all': len(all_symbols),
            'bist': len([s for s in all_symbols if s.endswith('.IS')]),
            'nasdaq': len([s for s in all_symbols if not any(s.endswith(suffix) for suffix in ['.IS', '.DE', '-USD', '=F'])]),
            'xetra': len([s for s in all_symbols if s.endswith('.DE')]),
            'crypto': len([s for s in all_symbols if s.endswith('-USD')]),
            'commodities': len([s for s in all_symbols if s.endswith('=F')])
        }
        
        return jsonify({
            'status': 'success',
            'counts': counts
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/portfolios', methods=['GET'])
def get_portfolios():
    """Portfolio listesini getir"""
    try:
        portfolios = portfolio_manager.list_portfolios()
        return jsonify({
            'status': 'success',
            'portfolios': portfolios
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/portfolios/<portfolio_name>', methods=['GET'])
def get_portfolio(portfolio_name):
    """Portfolio detaylarını getir"""
    try:
        summary = portfolio_manager.get_portfolio_summary(portfolio_name)
        positions = portfolio_manager.get_portfolio_positions(portfolio_name)
        transactions = portfolio_manager.get_portfolio_transactions(portfolio_name)
        
        return jsonify({
            'status': 'success',
            'summary': summary,
            'positions': positions,
            'transactions': transactions
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/portfolios', methods=['POST'])
def create_portfolio():
    """Yeni portfolio oluştur"""
    try:
        data = request.get_json() or {}
        name = data.get('name', '')
        initial_cash = data.get('initial_cash', 10000.0)
        
        if not name:
            return jsonify({
                'status': 'error',
                'message': 'Portfolio adı gerekli'
            }), 400
        
        portfolio = portfolio_manager.create_portfolio(name, initial_cash)
        
        return jsonify({
            'status': 'success',
            'message': f'Portfolio oluşturuldu: {name}',
            'portfolio': {
                'name': portfolio.name,
                'cash': portfolio.cash,
                'created_date': portfolio.created_date
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/portfolios/<portfolio_name>/positions', methods=['POST'])
def add_position(portfolio_name):
    """Portfolio'ya pozisyon ekle"""
    try:
        data = request.get_json() or {}
        symbol = data.get('symbol', '')
        quantity = data.get('quantity', 0)
        entry_price = data.get('entry_price', 0)
        current_price = data.get('current_price', entry_price)
        market = data.get('market', 'UNKNOWN')
        notes = data.get('notes', '')
        
        if not symbol or quantity <= 0 or entry_price <= 0:
            return jsonify({
                'status': 'error',
                'message': 'Geçersiz pozisyon verisi'
            }), 400
        
        success = portfolio_manager.add_position(
            portfolio_name, symbol, quantity, entry_price, 
            current_price, market, notes
        )
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Pozisyon eklendi: {symbol}'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Pozisyon eklenemedi'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# AI Trading Bot API Endpoints
@app.route('/api/trading-bot/start', methods=['POST'])
def start_trading_bot():
    try:
        if not ai_trading_bot:
            return jsonify({'success': False, 'message': 'AI Trading Bot modülü yüklenemedi'})
            
        data = request.get_json()
        mode = data.get('mode', 'conservative')
        
        success = ai_trading_bot.start_bot(mode)
        
        if success:
            return jsonify({'success': True, 'message': f'Bot başlatıldı - Mod: {mode}'})
        else:
            return jsonify({'success': False, 'message': 'Bot başlatılamadı'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Hata: {str(e)}'})

@app.route('/api/trading-bot/stop', methods=['POST'])
def stop_trading_bot():
    try:
        if not ai_trading_bot:
            return jsonify({'success': False, 'message': 'AI Trading Bot modülü yüklenemedi'})
            
        success = ai_trading_bot.stop_bot()
        
        if success:
            return jsonify({'success': True, 'message': 'Bot durduruldu'})
        else:
            return jsonify({'success': False, 'message': 'Bot durdurulamadı'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Hata: {str(e)}'})

@app.route('/api/trading-bot/status', methods=['GET'])
def get_trading_bot_status():
    try:
        if not ai_trading_bot:
            return jsonify({
                'success': True,
                'status': 'unavailable',
                'mode': '-',
                'total_trades': 0,
                'win_rate': 0,
                'bot_confidence': 0,
                'current_positions': 0,
                'last_trade_time': None,
                'performance': {}
            })
            
        performance = ai_trading_bot.get_bot_performance()
        
        return jsonify({
            'success': True,
            'status': 'active' if ai_trading_bot.is_active else 'inactive',
            'mode': ai_trading_bot.trading_mode,
            'total_trades': performance.get('total_trades', 0),
            'win_rate': performance.get('win_rate', 0),
            'bot_confidence': performance.get('bot_confidence', 0),
            'current_positions': performance.get('current_positions', 0),
            'last_trade_time': performance.get('last_trade_time'),
            'performance': performance
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Hata: {str(e)}'})

@app.route('/api/trading-bot/run-cycle', methods=['POST'])
def run_trading_cycle():
    try:
        if not ai_trading_bot:
            return jsonify({'success': False, 'message': 'AI Trading Bot modülü yüklenemedi'})
            
        if not ai_trading_bot.is_active:
            return jsonify({'success': False, 'message': 'Bot aktif değil'})
        
        result = ai_trading_bot.run_trading_cycle()
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Hata: {str(e)}'})

@app.route('/api/trading-bot/history', methods=['GET'])
def get_trading_bot_history():
    try:
        if not ai_trading_bot:
            return jsonify({'success': False, 'message': 'AI Trading Bot modülü yüklenemedi'})
            
        limit = request.args.get('limit', 50, type=int)
        history = ai_trading_bot.get_trade_history(limit)
        
        return jsonify({
            'success': True,
            'history': history
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Hata: {str(e)}'})

def run_dashboard(host='0.0.0.0', port=5004, debug=False):
    """Dashboard'ı çalıştır"""
    log_success("🚀 Basit Dashboard başlatılıyor...")
    log_info(f"URL: http://{host}:{port}")
    
    # WebSocket sunucusunu başlat
    try:
        websocket_thread = start_websocket_server()
        log_success("🔗 WebSocket sunucusu başlatıldı (ws://localhost:8765)")
    except Exception as e:
        log_error(f"WebSocket sunucusu başlatılamadı: {e}")
    
    app.run(host=host, port=port, debug=debug, threaded=True)

if __name__ == '__main__':
    run_dashboard()

