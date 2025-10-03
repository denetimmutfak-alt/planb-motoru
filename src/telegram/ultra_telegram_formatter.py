#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱⚡ TELEGRAM ULTRA META-ENHANCED MESSAGE FORMATTER ⚡📱
27-Module Enhanced System için görsel Telegram mesaj formatları

Features:
- Ultra Meta-Enhanced signal formatting
- Volume explosion special alerts
- Interactive button layouts
- Turkish localized content
- Mobile-optimized design
- Real-time market insights

Created: 2025-10-03
Author: Ultra Telegram Design Team
Version: v27.0 Meta-Enhanced
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import json

logger = logging.getLogger(__name__)

class TelegramUltraFormatter:
    """📱 Ultra Meta-Enhanced Telegram Message Formatter"""
    
    def __init__(self):
        self.name = "Telegram Ultra Formatter"
        self.version = "27.0.0"
        logger.info("📱 Telegram Ultra Meta-Enhanced Formatter initialized!")
        
        # Emoji mappings
        self.market_emojis = {
            'NASDAQ': '🇺🇸',
            'BIST': '🇹🇷', 
            'XETRA': '🇩🇪',
            'CRYPTO': '💰',
            'COMMODITY': '🌾'
        }
        
        self.action_emojis = {
            'AL_ULTIMATE': '🟢 AL_ULTIMATE 🧠🔥',
            'AL_GÜÇLÜ': '🟢 AL_GÜÇLÜ 🧠',
            'AL_ORTA': '🟢 AL_ORTA 🧠',
            'AL': '🟢 AL'
        }
        
        self.risk_emojis = {
            'DÜŞÜK': '🚨 DÜŞÜK',
            'ORTA': '🚨 ORTA', 
            'YÜKSEK': '🚨 YÜKSEK',
            'ULTRA ORTA': '🚨 ULTRA ORTA'
        }

    def format_main_signals(self, signals_data: List[Dict], analysis_summary: Dict) -> str:
        """Ana sinyal mesajını formatla"""
        
        # Header
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
        message = f"""🚀 PlanB ULTRA META-ENHANCELİ SONUÇLAR
⏰ {timestamp}

📊 Toplam Analiz: {analysis_summary.get('total_analyzed', 0):,} sembol
⚡ Ultra Güçlü: {analysis_summary.get('ultra_strong_count', 0)} adet (≥120 Meta Skoru)

"""
        
        # Individual signals
        for signal in signals_data[:6]:  # Top 6 signals
            symbol = signal.get('symbol', 'N/A')
            market = signal.get('market', 'UNKNOWN')
            price = signal.get('price', 0.0)
            classical_score = signal.get('classical_score', 0)
            meta_score = signal.get('meta_score', 0)
            collective_intelligence = signal.get('collective_intelligence', 0)
            quantum_state = signal.get('quantum_state', 'NEUTRAL')
            quantum_confidence = signal.get('quantum_confidence', 0)
            time_horizon = signal.get('time_horizon', '2-4 hafta')
            risk_level = signal.get('risk_level', 'ORTA')
            currency_symbol = '$' if market in ['NASDAQ', 'NYSE'] else ('₺' if market == 'BIST' else '$')
            
            # Determine action type
            if meta_score >= 130:
                action = 'AL_ULTIMATE'
            elif meta_score >= 115:
                action = 'AL_GÜÇLÜ'
            elif meta_score >= 100:
                action = 'AL_ORTA'
            else:
                action = 'AL'
            
            # Format signal
            message += f"""{self.action_emojis[action]} 
{symbol} {self.market_emojis.get(market, '🌍')} | {currency_symbol}{price:.2f}
📈 Klasik: {classical_score}/100 | ⚡ Meta: {meta_score}/100
🧠 KZ: %{collective_intelligence} | 🔮 {quantum_state}: %{quantum_confidence}
⏰ {time_horizon} | {self.risk_emojis.get(risk_level, '🚨 ORTA')}

[📊 Tam Analiz] [🎯 Takip Et] [🚨 Alarm Kur]
[📈 Grafik] [📱 Paylaş] [💰 Hesapla]

"""
        
        # Market summary
        message += """────────────────────────────────

📈 Piyasa Özeti:
"""
        
        market_summary = analysis_summary.get('market_summary', {})
        for market, data in market_summary.items():
            strong_count = data.get('strong_count', 0)
            total_count = data.get('total_count', 0)
            message += f"{market}: {strong_count}/{total_count} ultra güçlü {'🔥' if strong_count > 3 else '⚡' if strong_count > 1 else '🚀'}\n"
        
        # Meta-Intelligence insights
        insights = analysis_summary.get('meta_insights', [])
        if insights:
            message += f"""
🧠 Meta-Zeka İçgörüleri:
"""
            for insight in insights[:4]:
                message += f"• {insight}\n"
        
        # System controls
        message += f"""
🌟 Sistem Kontrolleri:
[⚙️ Ayarlar] [📊 Dashboard] [📈 Piyasa Tarama]
[🎯 Portföy] [🚨 Alarmlar] [📱 Bildirimler]

🔧 Analiz Kontrolleri:
[🔍 Filtrele] [⏰ Zaman Çerçevesi] [🎚️ Risk Ayarı]
[💰 Pozisyon Boyutu] [📊 Sıralama] [🔄 Yenile]

🤖 PlanB ULTIMATE v27.0
⚡ 27 Gelişmiş Modül Aktif
🧠 Meta-Intelligence Engine
🔮 Kuantum Probability System"""

        return message
    
    def format_volume_explosion_signals(self, volume_signals: List[Dict], volume_summary: Dict) -> str:
        """Hacim patlaması mesajını formatla"""
        
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
        message = f"""🔊⚡ HACİM PATLAMASI ULTRA SİNYALLER ⚡🔊
🚀 1-3 Gün İçinde Zirve Potansiyeli
⏰ {timestamp}

⚡ Toplam Tespit: {volume_summary.get('total_explosions', 0)} hacim patlaması
🔥 Ultra Güçlü: {volume_summary.get('ultra_strong_count', 0)} adet (≥65 Meta Skoru)

"""
        
        # Volume explosion signals
        for signal in volume_signals[:4]:  # Top 4 volume signals
            symbol = signal.get('symbol', 'N/A')
            market = signal.get('market', 'UNKNOWN')
            price = signal.get('price', 0.0)
            volume_multiplier = signal.get('volume_multiplier', 1.0)
            classical_score = signal.get('classical_score', 0)
            meta_score = signal.get('meta_score', 0)
            collective_intelligence = signal.get('collective_intelligence', 0)
            quantum_state = signal.get('quantum_state', 'NEUTRAL')
            quantum_confidence = signal.get('quantum_confidence', 0)
            risk_level = 'ULTRA ORTA'  # Volume explosions are always higher risk
            currency_symbol = '$' if market in ['NASDAQ', 'NYSE'] else ('₺' if market == 'BIST' else '$')
            
            # Format volume multiplier
            if volume_multiplier >= 1000000000:  # Billion
                vol_display = f"x{volume_multiplier/1000000000:.1f}B"
            elif volume_multiplier >= 1000000:  # Million
                vol_display = f"x{volume_multiplier/1000000:.1f}M"
            elif volume_multiplier >= 1000:  # Thousand
                vol_display = f"x{volume_multiplier/1000:.1f}K"
            else:
                vol_display = f"x{volume_multiplier:.0f}"
            
            # Determine action and fire intensity
            if meta_score >= 120:
                action = '🟢 AL_ULTRA 🔊💥'
                fire = '🔥🔥🔥'
            elif meta_score >= 110:
                action = '🟢 AL_GÜÇLÜ 🔊💥'
                fire = '🔥🔥'
            else:
                action = '🟢 AL_ORTA 🔊💥'
                fire = '🔥'
            
            message += f"""{action}
{symbol} {self.market_emojis.get(market, '🌍')} | {currency_symbol}{price:.2f}
📊 Hacim Patlaması: {vol_display} {fire}
📈 Klasik: {classical_score}/100 | ⚡ Meta: {meta_score}/100
🧠 KZ: %{collective_intelligence} | 🔮 {quantum_state}: %{quantum_confidence}
⏰ 1-3 gün | 🚨 ULTRA ORTA

[📊 Tam Analiz] [🎯 Takip Et] [🚨 Alarm Kur]
[📈 Grafik] [📱 Paylaş] [💰 Hesapla]

"""
        
        # Volume analysis summary
        message += """────────────────────────────────

🔊 Hacim Analizi:
"""
        
        market_volumes = volume_summary.get('market_volumes', {})
        for market, data in market_volumes.items():
            explosion_count = data.get('explosion_count', 0)
            total_count = data.get('total_count', 0)
            emoji = '💥' if explosion_count > 10 else '🔥' if explosion_count > 5 else '⚡'
            message += f"{market}: {explosion_count}/{total_count} hacim patlaması {emoji}\n"
        
        # Important warnings
        message += f"""
⚠️ Önemli Uyarı:
• Hacim patlamaları yüksek volatilite içerir
• 1-3 gün içinde hızlı kar/zarar potansiyeli
• Sıkı stop-loss kullanılması önerilir
• Pozisyon boyutu dikkatli ayarlanmalı

🧠 Meta-Zeka Hacim İçgörüleri:
"""
        
        volume_insights = volume_summary.get('volume_insights', [])
        for insight in volume_insights[:4]:
            message += f"• {insight}\n"
        
        # Risk management controls
        message += f"""
🚨 Risk Yönetimi:
[⚠️ Stop-Loss Ayarla] [💰 Pozisyon Hesapla] [⏰ Exit Timer]
[📊 Risk/Reward] [🔔 Fiyat Alarmı] [📈 Trailing Stop]

🔧 Hacim Kontrolleri:
[🔍 Hacim Filtresi] [⏰ Timeframe] [📊 Volume Profile]
[💥 Spike Detector] [🎯 Breakout Alert] [🔄 Real-Time]

🤖 PlanB ULTRA Volume Scanner v27.0
🔊 Real-Time Volume Analysis
⚡ Breakout Detection Engine
💥 Momentum Capture System"""

        return message
    
    def format_compact_signal(self, signal_data: Dict) -> str:
        """Tekil sinyal için compact format"""
        
        symbol = signal_data.get('symbol', 'N/A')
        market = signal_data.get('market', 'UNKNOWN')
        price = signal_data.get('price', 0.0)
        meta_score = signal_data.get('meta_score', 0)
        collective_intelligence = signal_data.get('collective_intelligence', 0)
        quantum_state = signal_data.get('quantum_state', 'NEUTRAL')
        quantum_confidence = signal_data.get('quantum_confidence', 0)
        enhancement_multiplier = signal_data.get('enhancement_multiplier', 1.0)
        time_horizon = signal_data.get('time_horizon', '2-4 hafta')
        risk_level = signal_data.get('risk_level', 'ORTA')
        
        currency_symbol = '$' if market in ['NASDAQ', 'NYSE'] else ('₺' if market == 'BIST' else '$')
        
        # Fire intensity based on meta score
        if meta_score >= 130:
            fire = '🔥🔥🔥'
            action = 'AL_ULTIMATE'
        elif meta_score >= 115:
            fire = '🔥🔥'
            action = 'AL_GÜÇLÜ'
        else:
            fire = '🔥'
            action = 'AL_ORTA'
        
        message = f"""🧠⚡ META-ENHANCELİ SİNYAL ⚡🧠

🎯 {symbol} {self.market_emojis.get(market, '🌍')}
💰 Fiyat: {currency_symbol}{price:.2f}
⚡ META Puan: {meta_score}/100 {fire}

🧠 Kolektif Zeka: %{collective_intelligence} 🟢
🔮 Kuantum Durum: {quantum_state} (%{quantum_confidence})
⚡ Güçlendirme: {enhancement_multiplier:.1f}x
🎯 Risk: {self.risk_emojis.get(risk_level, '🚨 ORTA')}

🟢 {action}
⏰ {time_horizon}

[📊 Detaylar] [🎯 Takip] [🚨 Alarm]

🤖 v27.0"""

        return message

# Global formatter instance
telegram_formatter = TelegramUltraFormatter()

def format_telegram_main_message(signals_data: List[Dict], analysis_summary: Dict) -> str:
    """Ana Telegram mesajını formatla"""
    return telegram_formatter.format_main_signals(signals_data, analysis_summary)

def format_telegram_volume_message(volume_signals: List[Dict], volume_summary: Dict) -> str:
    """Hacim patlaması Telegram mesajını formatla"""
    return telegram_formatter.format_volume_explosion_signals(volume_signals, volume_summary)

def format_telegram_compact_message(signal_data: Dict) -> str:
    """Compact Telegram mesajını formatla"""
    return telegram_formatter.format_compact_signal(signal_data)

if __name__ == "__main__":
    print("📱⚡ Telegram Ultra Meta-Enhanced Formatter loaded!")
    print("   ✅ Main signals formatting")
    print("   ✅ Volume explosion formatting") 
    print("   ✅ Compact signal formatting")
    print("   ✅ Interactive button layouts")
    print("   ✅ Turkish localized content")
    print("   ✅ Mobile-optimized design")
    print("🚀 Ready for 27-module enhanced system!")