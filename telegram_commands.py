#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PlanB ULTRA Telegram Bot Commands
Manuel kontrol ve pozisyon yönetimi için ek komutlar.
"""

import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from signal_tracker import SignalTracker, ReminderBot
import pandas as pd

class PlanBBotCommands:
    def __init__(self):
        self.tracker = SignalTracker()
        
    async def holdings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Aktif pozisyonları göster"""
        holdings = self.tracker.get_active_holdings()
        
        if holdings.empty:
            await update.message.reply_text("📊 Şu anda aktif pozisyon yok.")
            return
            
        message = "📊 <b>Aktif Pozisyonlarınız:</b>\n\n"
        
        for _, h in holdings.iterrows():
            days_left = int(h.days_remaining)
            
            if days_left <= 0:
                status = "🔴 SAT ZAMANI!"
            elif days_left <= 2:
                status = f"🟡 {days_left} gün kaldı"
            else:
                status = f"🟢 {days_left} gün kaldı"
                
            message += (
                f"• <b>{h.symbol}</b> - {status}\n"
                f"  📅 AL: {pd.to_datetime(h.signal_date).strftime('%d.%m.%Y')}\n"
                f"  📊 Puan: {h.score:.1f}/100\n"
                f"  💰 Fiyat: ${h.price:.2f}\n"
                f"  ⏰ Süre: {h.holding_period}\n\n"
            )
            
        # İnline butonlar ekle
        keyboard = [
            [InlineKeyboardButton("🔔 Hatırlatmaları Kontrol Et", callback_data="check_reminders")],
            [InlineKeyboardButton("📈 Bugün SAT Zamanı", callback_data="today_sells")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            message, 
            parse_mode="HTML",
            reply_markup=reply_markup
        )
        
    async def mark_sold(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Varlığı satıldı olarak işaretle"""
        if not context.args:
            await update.message.reply_text("❌ Kullanım: /sold THYAO.IS")
            return
            
        symbol = context.args[0].upper()
        
        try:
            self.tracker.mark_sold(symbol)
            await update.message.reply_text(f"✅ {symbol} satıldı olarak işaretlendi!")
        except Exception as e:
            await update.message.reply_text(f"❌ Hata: {e}")
            
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """İnline buton callback'leri"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "check_reminders":
            pending = self.tracker.get_pending_reminders()
            
            if pending.empty:
                message = "📅 Bugün hatırlatılacak varlık yok."
            else:
                message = f"🔔 <b>Bugün {len(pending)} varlık için SAT zamanı:</b>\n\n"
                for _, p in pending.iterrows():
                    message += f"• <b>{p.symbol}</b> (Puan: {p.score:.1f})\n"
                    
            await query.edit_message_text(message, parse_mode="HTML")
            
        elif query.data == "today_sells":
            pending = self.tracker.get_pending_reminders()
            
            if pending.empty:
                message = "📊 Bugün satılacak varlık yok."
            else:
                # Her varlık için SAT butonu oluştur
                keyboard = []
                for _, p in pending.iterrows():
                    keyboard.append([
                        InlineKeyboardButton(
                            f"💰 {p.symbol} SATILDI", 
                            callback_data=f"sold_{p.symbol}"
                        )
                    ])
                    
                reply_markup = InlineKeyboardMarkup(keyboard)
                message = f"💰 <b>Bugün satılacaklar ({len(pending)}):</b>\n\nSattığınız varlıkları işaretleyin:"
                
                await query.edit_message_text(
                    message, 
                    parse_mode="HTML",
                    reply_markup=reply_markup
                )
                
        elif query.data.startswith("sold_"):
            symbol = query.data.replace("sold_", "")
            self.tracker.mark_sold(symbol)
            await query.edit_message_text(f"✅ {symbol} satıldı olarak işaretlendi!")
            
    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """İstatistikler göster"""
        with self.tracker.tracker.sqlite3.connect(self.tracker.db_path) as conn:
            # Toplam sinyal sayısı
            total_signals = pd.read_sql_query(
                "SELECT COUNT(*) as count FROM signals WHERE signal_type='AL'", 
                conn
            ).iloc[0]['count']
            
            # Aktif pozisyon sayısı
            active_count = pd.read_sql_query(
                "SELECT COUNT(*) as count FROM signals WHERE signal_type='AL' AND sold=0", 
                conn
            ).iloc[0]['count']
            
            # Satılan pozisyon sayısı
            sold_count = pd.read_sql_query(
                "SELECT COUNT(*) as count FROM signals WHERE signal_type='AL' AND sold=1", 
                conn
            ).iloc[0]['count']
            
        message = (
            f"📊 <b>PlanB ULTRA İstatistikleri:</b>\n\n"
            f"🎯 Toplam AL sinyali: {total_signals}\n"
            f"📈 Aktif pozisyonlar: {active_count}\n"
            f"💰 Satılan pozisyonlar: {sold_count}\n"
            f"📈 Başarı oranı: {(sold_count/total_signals*100):.1f}%" if total_signals > 0 else "📈 Başarı oranı: 0%"
        )
        
        await update.message.reply_text(message, parse_mode="HTML")


def main():
    """Bot komutlarını başlat"""
    BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN environment variable gerekli!")
        return
        
    app = Application.builder().token(BOT_TOKEN).build()
    commands = PlanBBotCommands()
    
    # Komut handler'ları
    app.add_handler(CommandHandler("holdings", commands.holdings))
    app.add_handler(CommandHandler("sold", commands.mark_sold))
    app.add_handler(CommandHandler("stats", commands.stats))
    app.add_handler(CallbackQueryHandler(commands.button_callback))
    
    print("🤖 PlanB ULTRA Bot komutları aktif!")
    app.run_polling()

if __name__ == "__main__":
    main()