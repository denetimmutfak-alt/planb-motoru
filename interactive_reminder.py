import asyncio
import os
import datetime as dt
import pandas as pd

# Bot configuration - will be imported from main system
bot = None

REMIND_FILE = "data/remind.csv"   # user_id,ticker,buy_date,target_days,sent

def add_reminder(user_id, ticker, target_days=28):
    """Hatırlatma ekle"""
    try:
        # CSV varsa oku, yoksa boş DataFrame oluştur
        if os.path.isfile(REMIND_FILE):
            existing_df = pd.read_csv(REMIND_FILE)
        else:
            existing_df = pd.DataFrame(columns=["user_id", "ticker", "buy_date", "target_days", "sent"])
        
        # Yeni satır ekle
        new_row = pd.DataFrame([[user_id, ticker, dt.date.today().strftime('%Y-%m-%d'), target_days, 0]],
                              columns=["user_id", "ticker", "buy_date", "target_days", "sent"])
        
        # Birleştir ve kaydet
        df = pd.concat([existing_df, new_row], ignore_index=True)
        
        # Data klasörü yoksa oluştur
        os.makedirs("data", exist_ok=True)
        df.to_csv(REMIND_FILE, index=False)
        
        return True
    except Exception as e:
        print(f"Hatırlatma eklenirken hata: {e}")
        return False

async def check_reminders():
    """Vadesi gelen hatırlatmaları kontrol et"""
    try:
        if not os.path.isfile(REMIND_FILE):
            return
            
        today = dt.date.today()
        df = pd.read_csv(REMIND_FILE, parse_dates=["buy_date"])
        
        # Vadesi gelen ve henüz gönderilmemiş hatırlatmalar
        due = df[(df["buy_date"] + pd.to_timedelta(df["target_days"], unit="D")).dt.date <= today]
        due = due[due["sent"] == 0]
        
        for _, r in due.iterrows():
            text = f"⏰ <b>{r['ticker']}</b> için holding süresi doldu. SAT'mayı unutma!"
            try:
                # Telegram mesajı gönder (main sistem üzerinden)
                from telegram_full_trader_with_sentiment import send_telegram_message
                send_telegram_message(text)
                # Gönderildi olarak işaretle
                df.loc[df.index == r.name, "sent"] = 1
            except Exception as e:
                print(f"Mesaj gönderme hatası: {e}")
        
        # Güncellenmiş DataFrame'i kaydet
        if len(due) > 0:
            df.to_csv(REMIND_FILE, index=False)
        
    except Exception as e:
        print(f"Hatırlatma kontrolünde hata: {e}")

def create_reminder_button(ticker):
    """Hatırlatma butonu oluştur"""
    try:
        return {
            "inline_keyboard": [[
                {
                    "text": "⏰ SAT vakti gelince bildir",
                    "callback_data": f"rem_{ticker}"
                }
            ]]
        }
    except:
        return None