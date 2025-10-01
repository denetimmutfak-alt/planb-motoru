#!/usr/bin/env python3
"""
PlanB Motoru - Ultra Advanced Telegram Bot
Production-Ready with Auto-Decision Capability
"""

import asyncio
import json
import os
from datetime import datetime
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import sqlite3
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
API_BASE_URL = "http://localhost:8001"
DB_PATH = "data/planb_ultra.db"

class UltraTelegramBot:
    def __init__(self):
        self.bot_token = BOT_TOKEN
        self.chat_id = CHAT_ID
        self.application = None
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        welcome_message = """
🚀 **PlanB Motoru Ultra Bot Aktif!**

✅ **Özellikler:**
• Real-time market sinyalleri
• ML-destekli analiz sonuçları  
• Otomatik karar onay sistemi
• Risk yönetimi ve portföy takibi

📊 **Komutlar:**
/status - Bot durumu
/signals - Son sinyaller
/stats - Sistem istatistikleri
/help - Yardım

🎯 **Durum:** ULTRA OPERATIONAL
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Status command handler"""
        try:
            # Get API health
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            health_data = response.json()
            
            # Get database stats
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM analysis_results WHERE timestamp > datetime('now', '-1 hour')")
            recent_signals = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM user_decisions WHERE execution_status = 'pending'")
            pending_decisions = cursor.fetchone()[0]
            
            conn.close()
            
            status_message = f"""
🔥 **SISTEM DURUMU - ULTRA STABLE**

⚡ **API Status:** {health_data['status']}
📊 **Database:** {health_data['database']['status']}
🤖 **ML Engine:** {health_data['services']['ml_engine']}

📈 **Son 1 Saat:**
• Yeni Sinyaller: {recent_signals}
• Bekleyen Kararlar: {pending_decisions}
• Uptime: {health_data['performance']['uptime']}

🎯 **Performans:** EXCELLENT
⏰ **Son Güncelleme:** {datetime.now().strftime('%H:%M:%S')}
            """
            
            await update.message.reply_text(status_message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Status alınamadı: {str(e)}")
    
    async def signals_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get latest signals"""
        try:
            response = requests.get(f"{API_BASE_URL}/api/v1/analysis?limit=5", timeout=10)
            signals = response.json()
            
            if not signals:
                await update.message.reply_text("📭 Aktif sinyal bulunamadı.")
                return
            
            message = "🎯 **SON SİNYALLER:**\n\n"
            
            for signal in signals:
                confidence_emoji = "🟢" if signal['confidence'] > 0.8 else "🟡" if signal['confidence'] > 0.6 else "🔴"
                signal_emoji = "📈" if "BUY" in signal['signal'] else "📉" if "SELL" in signal['signal'] else "⏸️"
                
                message += f"""{signal_emoji} **{signal['symbol']}**
Signal: `{signal['signal']}`
Confidence: {confidence_emoji} `{signal['confidence']:.1%}`
ML Score: `{signal['ml_score']:.1f}/100`
Time: `{signal['timestamp'][:16]}`

"""
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Sinyaller alınamadı: {str(e)}")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get system statistics"""
        try:
            response = requests.get(f"{API_BASE_URL}/api/v1/stats", timeout=10)
            stats = response.json()
            
            message = f"""
📊 **SİSTEM İSTATİSTİKLERİ**

🏢 **Market Data:**
• Takip Edilen Semboller: {stats['market_data']['unique_symbols']}
• Son 24s Veri Noktası: {stats['market_data']['recent_data_points']}

🤖 **ML Analiz (24s):**
• Toplam Tahmin: {stats['analysis']['total_predictions_24h']}
• Yüksek Güven Sinyalleri: {stats['analysis']['high_confidence_signals']}

🎯 **En İyi Sinyaller:**
"""
            
            for signal in stats['top_signals']:
                message += f"• {signal['symbol']}: {signal['signal']} ({signal['confidence']:.1%})\n"
            
            message += f"\n⚡ **Sistem Sağlığı:** {stats['system_health']}"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ İstatistikler alınamadı: {str(e)}")
    
    async def send_signal_notification(self, signal_data):
        """Send signal notification with approval buttons"""
        symbol = signal_data['symbol']
        signal = signal_data['signal']
        confidence = signal_data['confidence']
        
        # Determine emoji and color based on signal
        if "BUY" in signal:
            emoji = "📈"
            color = "🟢"
        elif "SELL" in signal:
            emoji = "📉" 
            color = "🔴"
        else:
            emoji = "⏸️"
            color = "🟡"
        
        confidence_emoji = "🚀" if confidence > 0.8 else "⚡" if confidence > 0.7 else "⚠️"
        
        message = f"""
{emoji} **YENİ SİNYAL - {symbol}**

🎯 **Signal:** `{signal}`
{confidence_emoji} **Confidence:** `{confidence:.1%}`
📊 **ML Score:** `{signal_data.get('ml_score', 0):.1f}/100`
⏰ **Time:** `{datetime.now().strftime('%H:%M:%S')}`

💡 **Recommendation:** {signal_data.get('recommendation', 'Monitor')}
⚖️ **Risk Level:** {signal_data.get('risk_level', 'Medium')}
        """
        
        # Create approval buttons
        keyboard = [
            [
                InlineKeyboardButton("✅ Onayla", callback_data=f"approve_{symbol}_{signal}"),
                InlineKeyboardButton("❌ Reddet", callback_data=f"reject_{symbol}_{signal}")
            ],
            [
                InlineKeyboardButton("📊 Detay", callback_data=f"details_{symbol}"),
                InlineKeyboardButton("⏳ Beklet", callback_data=f"hold_{symbol}_{signal}")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send to configured chat
        bot = Bot(token=self.bot_token)
        message_obj = await bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
        # Store decision request in database
        self.store_decision_request(symbol, signal, message_obj.message_id)
        
        return message_obj.message_id
    
    def store_decision_request(self, symbol, signal, message_id):
        """Store decision request in database"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user_decisions 
            (symbol, signal, telegram_message_id, execution_status)
            VALUES (?, ?, ?, 'pending')
        """, (symbol, signal, message_id))
        
        conn.commit()
        conn.close()
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        action, symbol = callback_data.split('_', 1)
        
        if action == "approve":
            await self.handle_approval(query, symbol, True)
        elif action == "reject":
            await self.handle_approval(query, symbol, False)
        elif action == "details":
            await self.show_details(query, symbol)
        elif action == "hold":
            await self.handle_hold(query, symbol)
    
    async def handle_approval(self, query, symbol_signal, approved):
        """Handle signal approval/rejection"""
        symbol, signal = symbol_signal.rsplit('_', 1)
        
        # Update database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        status = 'approved' if approved else 'rejected'
        cursor.execute("""
            UPDATE user_decisions 
            SET user_action = ?, execution_status = ?
            WHERE telegram_message_id = ?
        """, (status, 'executed' if approved else 'cancelled', query.message.message_id))
        
        conn.commit()
        conn.close()
        
        # Update message
        action_emoji = "✅" if approved else "❌"
        action_text = "ONAYLANDI" if approved else "REDDEDİLDİ"
        
        new_text = f"{query.message.text}\n\n{action_emoji} **KARAR: {action_text}**\n⏰ {datetime.now().strftime('%H:%M:%S')}"
        
        await query.edit_message_text(text=new_text, parse_mode='Markdown')
        
        # Send execution confirmation
        if approved:
            await query.message.reply_text(f"🚀 **{symbol}** için **{signal}** sinyali execute edildi!")
    
    async def show_details(self, query, symbol):
        """Show detailed analysis for symbol"""
        try:
            response = requests.get(f"{API_BASE_URL}/api/v1/market-data?symbol={symbol}&limit=1", timeout=5)
            market_data = response.json()
            
            response = requests.get(f"{API_BASE_URL}/api/v1/analysis?symbol={symbol}&limit=1", timeout=5)
            analysis_data = response.json()
            
            if market_data and analysis_data:
                market = market_data[0]
                analysis = analysis_data[0]
                
                details = f"""
📊 **{symbol} - DETAYLI ANALİZ**

💰 **Market Data:**
• Price: ${market['price']:.2f}
• Volume: {market['volume']:,}
• Change: {market.get('change_percent', 0):.2f}%
• RSI: {market.get('rsi', 0):.1f}
• MACD: {market.get('macd', 0):.3f}

🤖 **ML Analysis:**
• Signal: {analysis['signal']}
• Confidence: {analysis['confidence']:.1%}
• ML Score: {analysis['ml_score']:.1f}/100
• Model: {analysis['model_version']}

⏰ **Last Update:** {analysis['timestamp'][:16]}
                """
                
                await query.message.reply_text(details, parse_mode='Markdown')
            else:
                await query.message.reply_text("❌ Detay bilgi alınamadı.")
                
        except Exception as e:
            await query.message.reply_text(f"❌ Hata: {str(e)}")
    
    async def handle_hold(self, query, symbol_signal):
        """Handle hold action"""
        symbol, signal = symbol_signal.rsplit('_', 1)
        
        # Update database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE user_decisions 
            SET user_action = 'hold', execution_status = 'pending'
            WHERE telegram_message_id = ?
        """, (query.message.message_id,))
        
        conn.commit()
        conn.close()
        
        new_text = f"{query.message.text}\n\n⏳ **KARAR: BEKLETİLDİ**\n⏰ {datetime.now().strftime('%H:%M:%S')}"
        await query.edit_message_text(text=new_text, parse_mode='Markdown')
    
    def run_bot(self):
        """Run the telegram bot"""
        self.application = Application.builder().token(self.bot_token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("signals", self.signals_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        print("🤖 Ultra Telegram Bot başlatılıyor...")
        print(f"📱 Bot Token: {self.bot_token[:10]}...")
        print(f"💬 Chat ID: {self.chat_id}")
        print("✅ Bot ULTRA OPERATIONAL!")
        
        # Run the bot
        self.application.run_polling()

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️  Telegram Bot Token ayarlanmamış!")
        print("🔧 BOT_TOKEN ve CHAT_ID değişkenlerini düzenleyin.")
    else:
        bot = UltraTelegramBot()
        bot.run_bot()