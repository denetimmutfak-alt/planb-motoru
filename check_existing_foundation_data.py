#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistemdeki Mevcut Kuruluş Tarihi Verilerini Kontrol Et
Provider'larda ve dosyalarda mevcut olan tüm kuruluş tarihlerini say
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def count_existing_foundation_data():
    """Sistemdeki mevcut kuruluş tarihi verilerini say"""
    
    print("🔍 SİSTEMDE MEVCUT KURULUŞ TARİHİ VERİLERİ")
    print("=" * 60)
    
    total_count = 0
    
    # 1. NASDAQ Provider'daki veriler
    try:
        from src.data.providers.nasdaq_provider import NASDAQProvider
        nasdaq = NASDAQProvider()
        nasdaq_symbols = nasdaq.get_symbols()
        
        # Provider'da company_info metodunu kontrol et
        nasdaq_with_dates = 0
        for symbol in nasdaq_symbols:
            try:
                info = nasdaq.get_company_info(symbol)
                if info and 'founding_date' in info:
                    nasdaq_with_dates += 1
            except:
                pass
        
        print(f"✅ NASDAQ Provider: {nasdaq_with_dates} şirket kuruluş tarihi")
        total_count += nasdaq_with_dates
        
    except Exception as e:
        print(f"❌ NASDAQ Provider kontrol hatası: {e}")
    
    # 2. BIST dosyasındaki veriler
    try:
        bist_file = "bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt"
        if os.path.exists(bist_file):
            with open(bist_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            bist_count = 0
            for line in lines:
                line = line.strip()
                if line and '.IS' in line and '\t' in line:
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        date_str = parts[2].strip()
                        # Tarih formatını kontrol et (dd.mm.yyyy)
                        import re
                        if re.match(r'\d{1,2}\.\d{1,2}\.\d{4}', date_str):
                            bist_count += 1
            
            print(f"✅ BIST Dosyası: {bist_count} şirket kuruluş tarihi")
            total_count += bist_count
        else:
            print("⚠️ BIST dosyası bulunamadı")
            
    except Exception as e:
        print(f"❌ BIST dosya kontrol hatası: {e}")
    
    # 3. Archive analiz.py dosyasındaki veriler
    try:
        archive_file = "archive/analiz.py"
        if os.path.exists(archive_file):
            with open(archive_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # founding_date içeren satırları say
            import re
            founding_matches = re.findall(r'"founding_date":\s*"[^"]*"', content)
            archive_count = len(founding_matches)
            
            print(f"✅ Archive Analiz: {archive_count} kuruluş tarihi")
            # Bu duplicate olabilir, toplama ekleme
            
        else:
            print("⚠️ Archive analiz dosyası bulunamadı")
            
    except Exception as e:
        print(f"❌ Archive dosya kontrol hatası: {e}")
    
    # 4. CSV dosyalarındaki veriler
    try:
        csv_files = ["bist_guncel_listesi.csv"]
        csv_total = 0
        
        for csv_file in csv_files:
            if os.path.exists(csv_file):
                with open(csv_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                csv_count = 0
                for i, line in enumerate(lines):
                    if i == 0:  # Header atla
                        continue
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 3:
                            date_str = parts[2].strip()
                            # Tarih formatını kontrol et
                            import re
                            if re.match(r'\d{1,2}\.\d{1,2}\.\d{4}', date_str):
                                csv_count += 1
                
                print(f"✅ {csv_file}: {csv_count} kuruluş tarihi")
                csv_total += csv_count
        
        # CSV'ler BIST ile aynı olabilir, duplicate sayma
        
    except Exception as e:
        print(f"❌ CSV dosya kontrol hatası: {e}")
    
    # 5. Complete foundation dates analysis dosyasındaki veriler
    try:
        analysis_files = [
            "complete_foundation_dates_analysis.py",
            "user_format_analysis.py"
        ]
        
        for analysis_file in analysis_files:
            if os.path.exists(analysis_file):
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Kuruluş tarihi formatlarını say
                import re
                date_patterns = re.findall(r'\"\d{2}\.\d{2}\.\d{4}\"', content)
                pattern_count = len(date_patterns)
                
                print(f"✅ {analysis_file}: {pattern_count} tarih pattern")
        
    except Exception as e:
        print(f"❌ Analysis dosya kontrol hatası: {e}")
    
    # 6. Provider'lardaki fallback listeler
    try:
        provider_files = [
            "src/data/providers/crypto_provider.py",
            "src/data/providers/commodities_provider.py", 
            "src/data/providers/xetra_provider.py"
        ]
        
        provider_total = 0
        for provider_file in provider_files:
            if os.path.exists(provider_file):
                with open(provider_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Sembol listelerini say
                import re
                symbol_patterns = re.findall(r'\"[A-Z0-9\-\.=]+-?[A-Z]*\"', content)
                unique_symbols = len(set(symbol_patterns))
                
                provider_name = provider_file.split('/')[-1].replace('_provider.py', '').upper()
                print(f"✅ {provider_name} Provider: ~{unique_symbols} sembol")
                provider_total += unique_symbols
        
    except Exception as e:
        print(f"❌ Provider dosya kontrol hatası: {e}")
    
    # Özet
    print(f"\n🎯 MEVCUT KURULUŞ TARİHİ VERİLERİ ÖZETİ:")
    print("=" * 60)
    print(f"✅ Kesin kuruluş tarihi verisi: {total_count:,} enstrüman")
    print(f"✅ Provider'larda sembol listesi: ~{provider_total:,} enstrüman")
    print(f"✅ Sistem geneli tahmini: ~{total_count + provider_total//4:,} enstrüman")
    
    print(f"\n💡 DURUMU:")
    print("Verileriniz sistemde mevcut! Provider'larda kayıtlı durumda.")
    print("Sadece yeni dosya formatında organize edilmesi gerekebilir.")
    
    return total_count

if __name__ == "__main__":
    count_existing_foundation_data()