#!/usr/bin/env python3
"""
Veritabanını kontrol et
"""
import sqlite3

def main():
    try:
        conn = sqlite3.connect('data/planb_motoru.db')
        cursor = conn.cursor()
        
        # Tabloları listele
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print('Tablolar:', [t[0] for t in tables])
        
        # Analizler tablosunu kontrol et
        if ('analizler',) in tables:
            cursor.execute('SELECT COUNT(*) FROM analizler')
            count = cursor.fetchone()[0]
            print(f'Analizler tablosunda {count} kayıt var')
            
            if count > 0:
                cursor.execute('SELECT * FROM analizler ORDER BY created_at DESC LIMIT 3')
                rows = cursor.fetchall()
                print('Son 3 analiz:')
                for row in rows:
                    print(f"  {row[2]} ({row[1]}): {row[11]} puan - {row[12]}")
        else:
            print('Analizler tablosu bulunamadı')
        
        conn.close()
        
    except Exception as e:
        print(f'Hata: {e}')

if __name__ == "__main__":
    main()

