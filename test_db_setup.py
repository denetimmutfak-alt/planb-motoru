#!/usr/bin/env python3
"""
Database setup test
"""
import sqlite3
from pathlib import Path

def main():
    try:
        print("Database setup test başlıyor...")
        
        # Database path
        database_path = Path("data/planb_motoru.db")
        database_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Database path: {database_path}")
        
        # Connect to database
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        print("✅ Database connection başarılı")
        
        # Drop table if exists
        cursor.execute('DROP TABLE IF EXISTS analizler')
        print("✅ Eski tablo silindi")
        
        # Create table
        cursor.execute('''
            CREATE TABLE analizler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarih TEXT NOT NULL,
                hisse_kodu TEXT NOT NULL,
                finansal_puan REAL,
                teknik_puan REAL,
                trend_puan REAL,
                gann_puan REAL,
                astroloji_puan REAL,
                shemitah_puan REAL,
                cycle21_puan REAL,
                solar_cycle_puan REAL,
                toplam_puan REAL NOT NULL,
                sinyal TEXT NOT NULL,
                pazar TEXT,
                guncel_fiyat REAL,
                bir_ay_sonraki_fiyat REAL,
                momentum_skor REAL,
                breakout_skor REAL,
                volume_skor REAL,
                al_sinyal TEXT,
                al_guven REAL,
                tutma_suresi INTEGER,
                tutma_tipi TEXT,
                hedef_fiyat_1gun REAL,
                hedef_fiyat_1hafta REAL,
                hedef_fiyat_1ay REAL,
                hedef_fiyat_3ay REAL,
                risk_reward_oran REAL,
                volatilite REAL,
                trend_guclu REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Tablo oluşturuldu")
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_hisse_kodu ON analizler(hisse_kodu)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tarih ON analizler(tarih)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sinyal ON analizler(sinyal)')
        print("✅ İndeksler oluşturuldu")
        
        # Commit and close
        conn.commit()
        conn.close()
        
        print("✅ Database setup tamamlandı")
        
        # Verify
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tablolar: {[t[0] for t in tables]}")
        conn.close()
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

