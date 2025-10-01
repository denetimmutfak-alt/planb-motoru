#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PlanB ULTRA Signal Tracking & Reminder System
Bu modül AL sinyallerini takip eder ve SAT zamanı geldiğinde hatırlatır.
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import os
import asyncio
import telegram

class SignalTracker:
    def __init__(self, db_path="data/planb_signals.db"):
        self.db_path = Path(db_path)
        self.init_database()
        
    def init_database(self):
        """Signal tracking veritabanını başlat"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    signal_type TEXT NOT NULL,  -- 'AL' veya 'SAT'
                    score REAL NOT NULL,
                    price REAL,
                    signal_date TIMESTAMP NOT NULL,
                    holding_period TEXT,  -- '2-4 hafta' gibi
                    holding_days INTEGER,  -- sayısal gün sayısı
                    deadline_date TIMESTAMP,  -- satış tarihi
                    reminded BOOLEAN DEFAULT 0,
                    sold BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_deadline 
                ON signals(deadline_date, reminded, sold)
            """)
            
    def add_signal(self, symbol, signal_type, score, price=None, holding_period=None):
        """Yeni sinyal ekle"""
        signal_date = datetime.now()
        
        # Holding period'dan gün sayısını çıkar
        holding_days = self._parse_holding_period(holding_period)
        deadline_date = signal_date + timedelta(days=holding_days) if holding_days else None
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO signals 
                (symbol, signal_type, score, price, signal_date, holding_period, 
                 holding_days, deadline_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (symbol, signal_type, score, price, signal_date, 
                  holding_period, holding_days, deadline_date))
            
        print(f"✅ Signal kaydedildi: {signal_type} {symbol} (deadline: {deadline_date})")
        
    def _parse_holding_period(self, holding_period):
        """Holding period text'inden gün sayısını çıkar"""
        if not holding_period:
            return 7  # default 1 hafta
            
        try:
            # "2-4 hafta" -> ortalama 21 gün
            # "1-2 hafta" -> ortalama 10.5 gün
            if "hafta" in holding_period.lower():
                parts = holding_period.split("-")
                if len(parts) == 2:
                    min_weeks = float(parts[0])
                    max_weeks = float(parts[1].split()[0])  # "4 hafta"dan 4'ü al
                    avg_weeks = (min_weeks + max_weeks) / 2
                    return int(avg_weeks * 7)
                else:
                    # "3 hafta" gibi
                    weeks = float(parts[0])
                    return int(weeks * 7)
            elif "gün" in holding_period.lower():
                return int(''.join(filter(str.isdigit, holding_period)))
            else:
                return 7
        except:
            return 7
            
    def get_pending_reminders(self):
        """Hatırlatılacak sinyalleri getir"""
        today = datetime.now().date()
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query("""
                SELECT * FROM signals 
                WHERE signal_type = 'AL' 
                AND reminded = 0 
                AND sold = 0 
                AND date(deadline_date) <= date(?)
                ORDER BY deadline_date
            """, conn, params=(today,))
            
        return df
        
    def mark_reminded(self, signal_id):
        """Sinyal hatırlatıldı olarak işaretle"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE signals SET reminded = 1 
                WHERE id = ?
            """, (signal_id,))
            
    def mark_sold(self, symbol):
        """Varlık satıldı olarak işaretle"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE signals SET sold = 1 
                WHERE symbol = ? AND signal_type = 'AL' AND sold = 0
            """, (symbol,))
            
    def get_active_holdings(self):
        """Aktif pozisyonları getir"""
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query("""
                SELECT symbol, signal_date, score, price, holding_period, deadline_date,
                       julianday(deadline_date) - julianday('now') as days_remaining
                FROM signals 
                WHERE signal_type = 'AL' AND sold = 0
                ORDER BY deadline_date
            """, conn)
            
        return df


class ReminderBot:
    def __init__(self, bot_token, chat_id):
        self.bot = telegram.Bot(bot_token)
        self.chat_id = chat_id
        self.tracker = SignalTracker()
        
    async def send_reminders(self):
        """Günlük hatırlatmaları gönder"""
        pending = self.tracker.get_pending_reminders()
        
        if pending.empty:
            print("📅 Bugün hatırlatılacak sinyal yok")
            return
            
        for _, signal in pending.iterrows():
            days_held = (datetime.now() - pd.to_datetime(signal.signal_date)).days
            
            message = (
                f"⏰ <b>SAT ZAMANI GELDİ!</b>\n\n"
                f"🎯 <b>{signal.symbol}</b>\n"
                f"📅 AL tarihi: {pd.to_datetime(signal.signal_date).strftime('%d.%m.%Y')}\n"
                f"📊 AL puanı: {signal.score}/100\n"
                f"💰 AL fiyatı: ${signal.price:.2f}" if signal.price else "" + "\n"
                f"⏱️ Elde tutma: {days_held} gün\n"
                f"🎯 Önerilen: <u>BUGÜN SAT</u>\n\n"
                f"💡 Unutma: Kar/zarar kontrolü yap!"
            )
            
            try:
                await self.bot.send_message(
                    self.chat_id, 
                    message, 
                    parse_mode="HTML"
                )
                self.tracker.mark_reminded(signal.id)
                print(f"✅ Hatırlatma gönderildi: {signal.symbol}")
                
            except Exception as e:
                print(f"❌ Hatırlatma gönderilemedi {signal.symbol}: {e}")
                
    async def send_holdings_summary(self):
        """Aktif pozisyonları özetle"""
        holdings = self.tracker.get_active_holdings()
        
        if holdings.empty:
            message = "📊 Şu anda aktif pozisyon yok."
        else:
            message = "📊 <b>Aktif Pozisyonlar:</b>\n\n"
            
            for _, h in holdings.iterrows():
                days_left = int(h.days_remaining)
                status = "🔴 SAT ZAMANI!" if days_left <= 0 else f"🟡 {days_left} gün kaldı"
                
                message += (
                    f"• <b>{h.symbol}</b> - {status}\n"
                    f"  AL: {pd.to_datetime(h.signal_date).strftime('%d.%m')}, "
                    f"Puan: {h.score}/100\n\n"
                )
                
        try:
            await self.bot.send_message(self.chat_id, message, parse_mode="HTML")
        except Exception as e:
            print(f"❌ Özet gönderilemedi: {e}")


if __name__ == "__main__":
    # Test
    tracker = SignalTracker()
    
    # Örnek sinyal ekle
    tracker.add_signal("THYAO.IS", "AL", 75.2, 45.30, "2-4 hafta")
    
    # Pending reminder'ları kontrol et
    pending = tracker.get_pending_reminders()
    print(f"Hatırlatılacak sinyal sayısı: {len(pending)}")