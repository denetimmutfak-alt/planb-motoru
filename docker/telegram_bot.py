#!/usr/bin/env python3
"""
PlanB Telegram Bot - Güven Skoru Filtrelemeli Bildirim Sistemi
Onayla/Reddet butonları ile insan onay mekanizması
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import aiohttp
import psycopg2
from psycopg2.extras import RealDictCursor
import redis

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class PlanBTelegramBot:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.db_url = os.getenv('DATABASE_URL')
        self.redis_url = os.getenv('REDIS_URL')
        self.core_api_url = "http://planb_core:8000"
        self.midas_base_url = os.getenv('MIDAS_BASE_URL', 'https://web.getmidas.com/tr/order')
        
        # Redis connection for caching
        self.redis_client = redis.from_url(self.redis_url) if self.redis_url else None
        
        # Confidence threshold (only signals >= 70% sent)
        self.confidence_threshold = float(os.getenv('CONFIDENCE_THRESHOLD', '70'))
        
        # Message cache for auto-deletion
        self.pending_messages = {}
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bot başlatma komutu"""
        welcome_text = """
🚀 *PlanB Motoru Telegram Bot Aktif!*

Bu bot size yüksek güven skorlu AL/SAT/TUT sinyalleri gönderir.

📊 *Özellikler:*
• Güven skoru ≥ %70 olan sinyaller
• Onayla/Reddet hızlı butonları
• Otomatik Midas link oluşturma
• 5 dakika içinde otomatik mesaj silme
• Karar takip sistemi

📈 *Komutlar:*
/start - Bot'u başlat
/status - Sistem durumu
/stats - Günlük istatistikler
/settings - Ayarlar

✅ Bot hazır! Sinyaller gelmeye başlayacak...
        """
        
        await update.message.reply_text(
            welcome_text, 
            parse_mode='Markdown'
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Sistem durumu kontrolü"""
        try:
            # Core API health check
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.core_api_url}/health") as resp:
                    if resp.status == 200:
                        health_data = await resp.json()
                        
                        status_text = f"""
🔋 *Sistem Durumu*

✅ Core API: Çalışıyor
📊 Uptime: {health_data.get('uptime_seconds', 0):.0f} saniye
💾 Memory: {health_data.get('memory_usage_mb', 0):.1f} MB
🔄 Version: {health_data.get('version', 'N/A')}

🎯 *Bot Ayarları*
📈 Güven Eşiği: ≥ %{self.confidence_threshold}
⏰ Mesaj Süresi: 5 dakika
🔔 Bildirimler: Aktif
                        """
                        
                        await update.message.reply_text(
                            status_text,
                            parse_mode='Markdown'
                        )
                    else:
                        await update.message.reply_text("❌ Core API yanıt vermiyor")
                        
        except Exception as e:
            logger.error(f"Status check error: {e}")
            await update.message.reply_text(f"❌ Sistem kontrolü başarısız: {str(e)}")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Günlük istatistikler"""
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    # Bugünün istatistikleri
                    cur.execute("""
                        SELECT 
                            COUNT(*) as total_signals,
                            COUNT(CASE WHEN approval_status = 'APPROVED' THEN 1 END) as approved,
                            COUNT(CASE WHEN approval_status = 'REJECTED' THEN 1 END) as rejected,
                            COUNT(CASE WHEN approval_status = 'EXPIRED' THEN 1 END) as expired,
                            AVG(confidence_score) as avg_confidence
                        FROM signal_notifications 
                        WHERE DATE(timestamp) = CURRENT_DATE
                    """)
                    
                    stats = cur.fetchone()
                    
                    stats_text = f"""
📊 *Bugünün İstatistikleri*

📈 Toplam Sinyal: {stats['total_signals']}
✅ Onaylanan: {stats['approved']}
❌ Reddedilen: {stats['rejected']}
⏰ Süresi Dolan: {stats['expired']}

📊 Ortalama Güven: %{stats['avg_confidence']:.1f if stats['avg_confidence'] else 0}

📈 Onay Oranı: %{(stats['approved'] / max(stats['total_signals'], 1)) * 100:.1f}
                    """
                    
                    await update.message.reply_text(
                        stats_text,
                        parse_mode='Markdown'
                    )
                    
        except Exception as e:
            logger.error(f"Stats error: {e}")
            await update.message.reply_text(f"❌ İstatistik alınamadı: {str(e)}")
    
    async def send_signal_notification(self, signal_data: Dict):
        """Yüksek güven skorlu sinyal bildirimi gönder"""
        try:
            symbol = signal_data['symbol']
            signal = signal_data['signal']
            confidence = signal_data['confidence']
            
            # Güven skoru filtresi
            if confidence < self.confidence_threshold:
                logger.info(f"Signal {symbol} filtered out: confidence {confidence} < {self.confidence_threshold}")
                return
            
            # Sinyal emoji'si
            signal_emoji = {
                'AL': '🟢',
                'SAT': '🔴', 
                'TUT': '🟡'
            }.get(signal, '⚪')
            
            # Midas link oluştur
            midas_link = self.generate_midas_link(symbol, signal)
            
            # Mesaj metni
            message_text = f"""
{signal_emoji} *{symbol}* - *{signal}*

📊 Güven Skoru: *%{confidence:.1f}*
🕐 Zaman: {datetime.now().strftime('%H:%M:%S')}

🔗 [Midas'ta Aç]({midas_link})

⚡ Bu mesaj 5 dakika içinde silinecek
            """
            
            # Butonlar
            keyboard = [
                [
                    InlineKeyboardButton("✅ Onayla", callback_data=f"approve_{symbol}_{signal}"),
                    InlineKeyboardButton("❌ Reddet", callback_data=f"reject_{symbol}_{signal}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Mesajı gönder
            application = Application.builder().token(self.bot_token).build()
            
            message = await application.bot.send_message(
                chat_id=self.chat_id,
                text=message_text,
                parse_mode='Markdown',
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
            
            # Veritabanına kaydet
            await self.save_signal_notification(signal_data, message.message_id, midas_link)
            
            # 5 dakika sonra mesajı sil
            self.pending_messages[message.message_id] = {
                'delete_at': datetime.now() + timedelta(minutes=5),
                'symbol': symbol,
                'signal': signal
            }
            
            logger.info(f"Signal sent: {symbol} {signal} ({confidence:.1f}%)")
            
        except Exception as e:
            logger.error(f"Failed to send signal notification: {e}")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Buton tıklama işleyicisi"""
        query = update.callback_query
        await query.answer()
        
        # Callback data parse et
        callback_data = query.data
        parts = callback_data.split('_')
        
        if len(parts) >= 3:
            action = parts[0]  # approve/reject
            symbol = parts[1]
            signal = parts[2]
            
            # Karar kaydet
            await self.save_user_decision(
                message_id=query.message.message_id,
                symbol=symbol,
                signal=signal,
                decision=action,
                user_id=query.from_user.id
            )
            
            # Mesajı güncelle
            decision_emoji = "✅" if action == "approve" else "❌"
            decision_text = "ONAYLANDI" if action == "approve" else "REDDEDİLDİ"
            
            updated_text = f"""
{decision_emoji} *{symbol}* - *{signal}* - *{decision_text}*

📊 Karar Zamanı: {datetime.now().strftime('%H:%M:%S')}
👤 Karar Veren: {query.from_user.first_name}

Bu sinyal işleme alındı.
            """
            
            await query.edit_message_text(
                text=updated_text,
                parse_mode='Markdown'
            )
            
            # Pending messages'tan kaldır
            if query.message.message_id in self.pending_messages:
                del self.pending_messages[query.message.message_id]
            
            logger.info(f"User decision: {symbol} {signal} {action}")
    
    def generate_midas_link(self, symbol: str, signal: str) -> str:
        """Midas için otomatik link oluştur"""
        action = "alis" if signal == "AL" else "satis" if signal == "SAT" else "alis"
        # Basit link oluşturma - production'da daha gelişmiş olabilir
        return f"{self.midas_base_url}/BIST/{symbol}/{action}/limit"
    
    async def save_signal_notification(self, signal_data: Dict, message_id: int, midas_link: str):
        """Sinyal bildirimini veritabanına kaydet"""
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO signal_notifications 
                        (timestamp, symbol, signal, confidence_score, telegram_message_id, 
                         expires_at, midas_link, approval_status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        datetime.now(),
                        signal_data['symbol'],
                        signal_data['signal'],
                        signal_data['confidence'],
                        message_id,
                        datetime.now() + timedelta(minutes=5),
                        midas_link,
                        'PENDING'
                    ))
                    conn.commit()
        except Exception as e:
            logger.error(f"Failed to save signal notification: {e}")
    
    async def save_user_decision(self, message_id: int, symbol: str, signal: str, decision: str, user_id: int):
        """Kullanıcı kararını kaydet"""
        try:
            with psycopg2.connect(self.db_url) as conn:
                with conn.cursor() as cur:
                    # Signal notification'ı güncelle
                    status = 'APPROVED' if decision == 'approve' else 'REJECTED'
                    cur.execute("""
                        UPDATE signal_notifications 
                        SET approval_status = %s, approved_at = %s
                        WHERE telegram_message_id = %s
                    """, (status, datetime.now(), message_id))
                    
                    # User decision kaydet
                    cur.execute("""
                        INSERT INTO user_decisions 
                        (timestamp, symbol, original_signal, user_decision, decision_time_seconds)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        datetime.now(),
                        symbol,
                        signal,
                        status,
                        0  # TODO: Calculate actual decision time
                    ))
                    
                    conn.commit()
        except Exception as e:
            logger.error(f"Failed to save user decision: {e}")
    
    async def cleanup_expired_messages(self):
        """Süresi dolan mesajları temizle"""
        now = datetime.now()
        expired_messages = []
        
        for message_id, data in self.pending_messages.items():
            if now >= data['delete_at']:
                expired_messages.append(message_id)
        
        # Süresi dolan mesajları sil
        for message_id in expired_messages:
            try:
                application = Application.builder().token(self.bot_token).build()
                await application.bot.delete_message(
                    chat_id=self.chat_id,
                    message_id=message_id
                )
                
                # Veritabanında EXPIRED olarak işaretle
                with psycopg2.connect(self.db_url) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            UPDATE signal_notifications 
                            SET approval_status = 'EXPIRED'
                            WHERE telegram_message_id = %s
                        """, (message_id,))
                        conn.commit()
                
                del self.pending_messages[message_id]
                logger.info(f"Expired message deleted: {message_id}")
                
            except Exception as e:
                logger.error(f"Failed to delete expired message {message_id}: {e}")
    
    async def start_polling(self):
        """Bot'u başlat ve polling'i başlat"""
        try:
            application = Application.builder().token(self.bot_token).build()
            
            # Handlers
            application.add_handler(CommandHandler("start", self.start_command))
            application.add_handler(CommandHandler("status", self.status_command))
            application.add_handler(CommandHandler("stats", self.stats_command))
            application.add_handler(CallbackQueryHandler(self.button_callback))
            
            # Background tasks
            asyncio.create_task(self.signal_listener())
            asyncio.create_task(self.cleanup_scheduler())
            
            # Start polling
            logger.info("Starting Telegram bot polling...")
            await application.run_polling()
            
        except Exception as e:
            logger.error(f"Bot polling error: {e}")
    
    async def signal_listener(self):
        """Core API'den gelen sinyalleri dinle"""
        while True:
            try:
                # Redis'ten yeni sinyalleri kontrol et
                if self.redis_client:
                    signal_data = self.redis_client.blpop('planb_signals', timeout=10)
                    if signal_data:
                        signal = json.loads(signal_data[1])
                        await self.send_signal_notification(signal)
                
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Signal listener error: {e}")
                await asyncio.sleep(5)
    
    async def cleanup_scheduler(self):
        """Mesaj temizleme scheduler'ı"""
        while True:
            try:
                await self.cleanup_expired_messages()
                await asyncio.sleep(30)  # Her 30 saniyede bir kontrol et
            except Exception as e:
                logger.error(f"Cleanup scheduler error: {e}")
                await asyncio.sleep(60)

async def main():
    """Ana fonksiyon"""
    bot = PlanBTelegramBot()
    await bot.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
