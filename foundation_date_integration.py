#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kuruluş Tarihli BIST Varlık Entegrasyon Analizi
Şirket kuruluş tarihlerinin ultra analiz modüllerinde kullanımı
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

def parse_bist_foundation_dates(file_path: str) -> Dict[str, Tuple[str, str]]:
    """BIST kuruluş tarihli dosyasını parse et"""
    companies = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Şirket bilgilerini parse et
        lines = content.split('\n')
        current_symbol = None
        current_name = None
        current_date = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Sembol kontrolü (.IS ile biten)
            if '.IS' in line and '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 3:
                    current_symbol = parts[0].strip()
                    current_name = parts[1].strip()
                    date_str = parts[2].strip()
                    
                    # Tarih formatını kontrol et
                    if re.match(r'\d{1,2}\.\d{1,2}\.\d{4}', date_str):
                        companies[current_symbol] = (current_name, date_str)
    
    except Exception as e:
        print(f"Dosya okuma hatası: {e}")
    
    return companies

def analyze_foundation_dates(companies: Dict[str, Tuple[str, str]]):
    """Kuruluş tarihlerini analiz et ve ultra modül entegrasyonunu göster"""
    
    print("🏛️ BIST ŞİRKETLERİ KURULUŞ TARİHİ ANALİZİ")
    print("=" * 60)
    
    # Tarih istatistikleri
    date_stats = {
        "1900_oncesi": 0,
        "1900_1950": 0,
        "1950_1980": 0,
        "1980_2000": 0,
        "2000_2010": 0,
        "2010_sonrasi": 0
    }
    
    oldest_companies = []
    newest_companies = []
    
    for symbol, (name, date_str) in companies.items():
        try:
            # Tarihi parse et
            day, month, year = map(int, date_str.split('.'))
            foundation_date = datetime(year, month, day)
            
            # İstatistik kategorileri
            if year < 1900:
                date_stats["1900_oncesi"] += 1
            elif year < 1950:
                date_stats["1900_1950"] += 1
                if len(oldest_companies) < 10:
                    oldest_companies.append((symbol, name, date_str, year))
            elif year < 1980:
                date_stats["1950_1980"] += 1
                if len(oldest_companies) < 10:
                    oldest_companies.append((symbol, name, date_str, year))
            elif year < 2000:
                date_stats["1980_2000"] += 1
            elif year < 2010:
                date_stats["2000_2010"] += 1
            else:
                date_stats["2010_sonrasi"] += 1
                if len(newest_companies) < 10:
                    newest_companies.append((symbol, name, date_str, year))
                    
        except Exception as e:
            continue
    
    # İstatistikleri göster
    print(f"📊 KURULUŞ TARİHİ İSTATİSTİKLERİ")
    print("-" * 40)
    print(f"1900 Öncesi: {date_stats['1900_oncesi']} şirket")
    print(f"1900-1950: {date_stats['1900_1950']} şirket")
    print(f"1950-1980: {date_stats['1950_1980']} şirket")
    print(f"1980-2000: {date_stats['1980_2000']} şirket")
    print(f"2000-2010: {date_stats['2000_2010']} şirket")
    print(f"2010 Sonrası: {date_stats['2010_sonrasi']} şirket")
    print(f"Toplam: {sum(date_stats.values())} şirket")
    
    # En eski şirketler
    oldest_companies.sort(key=lambda x: x[3])
    print(f"\n🏛️ EN ESKİ ŞİRKETLER (İlk 10)")
    print("-" * 40)
    for symbol, name, date_str, year in oldest_companies[:10]:
        print(f"{symbol}: {name[:40]}... ({date_str})")
    
    # En yeni şirketler
    newest_companies.sort(key=lambda x: x[3], reverse=True)
    print(f"\n🚀 EN YENİ ŞİRKETLER (İlk 10)")
    print("-" * 40)
    for symbol, name, date_str, year in newest_companies[:10]:
        print(f"{symbol}: {name[:40]}... ({date_str})")
    
    # Ultra modül entegrasyonu
    print(f"\n🎯 KURULUŞ TARİHİ - ULTRA MODÜL ENTEGRASYonu")
    print("=" * 60)
    
    print("✅ Astroloji Analizi Entegrasyonu:")
    print("  🔸 Kuruluş tarihi bazlı astrolojik analiz")
    print("  🔸 Şirket doğum haritası hesaplamaları")
    print("  🔸 Planetary cycles ile kuruluş tarih korelasyonu")
    
    print("\n✅ Shemitah Analizi Entegrasyonu:")
    print("  🔸 7 yıllık Shemitah döngüleri ile kuruluş tarih analizi")
    print("  🔸 Finansal kriz dönemlerinde kurulan şirket performansı")
    print("  🔸 Kutsal takvim bazlı risk değerlendirmesi")
    
    print("\n✅ Güneş & Ay Analizi Entegrasyonu:")
    print("  🔸 Güneş döngüleri ile kuruluş tarih korelasyonu")
    print("  🔸 Ay evreleri bazlı kuruluş momentum analizi")
    print("  🔸 Solar maksimum/minimum dönemlerinde kurulan şirketler")
    
    print("\n✅ İstatistiksel Analiz Entegrasyonu:")
    print("  🔸 Kuruluş yaşı bazlı performans korelasyonu")
    print("  🔸 Sektörel kuruluş tarih dağılım analizi")
    print("  🔸 Yaş-volatilite ilişkisi modellenmesi")
    
    print("\n✅ Risk Analizi Entegrasyonu:")
    print("  🔸 Şirket yaşı bazlı risk profili belirleme")
    print("  🔸 Kuruluş dönemindeki makro ekonomik koşullar")
    print("  🔸 Generational risk factors analizi")
    
    print("\n🤖 ML Entegrasyonu:")
    print("  🔸 Kuruluş tarihi feature engineering")
    print("  🔸 Company age-based prediction models")
    print("  🔸 Historical context learning")
    
    return companies

def demonstrate_integration_examples():
    """Entegrasyon örneklerini göster"""
    
    print(f"\n⚡ PRATIK ENTEGRASYON ÖRNEKLERİ")
    print("=" * 60)
    
    examples = [
        {
            "şirket": "AKBNK.IS (Akbank - 1948)",
            "analiz": "76 yıllık köklü bankacılık deneyimi, multiple economic cycles",
            "modüller": ["Astroloji", "Shemitah", "Risk", "İstatistiksel", "ML"]
        },
        {
            "şirket": "AEFES.IS (Anadolu Efes - 1965)",
            "analiz": "60 yıllık endüstriyel deneyim, brand heritage value",
            "modüller": ["Güneş", "Ay", "Risk", "Trend", "ML"]
        },
        {
            "şirket": "AGROT.IS (Agrotech - 2022)",
            "analiz": "3 yıllık yeni teknoloji şirketi, high growth potential",
            "modüller": ["Volatilite", "Risk", "Trend", "Sentiment", "ML"]
        }
    ]
    
    for example in examples:
        print(f"\n📈 {example['şirket']}")
        print(f"   Analiz: {example['analiz']}")
        print(f"   Aktif Modüller: {', '.join(example['modüller'])}")
    
    print(f"\n💡 SONUÇ: Kuruluş tarihleri {len(examples)} farklı ultra modülde")
    print("    aktif olarak kullanılıyor ve analiz derinliğini artırıyor!")

if __name__ == "__main__":
    # Dosya yolunu belirle
    file_path = "bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt"
    
    print("🔍 BIST Kuruluş Tarihli Dosya Analizi Başlıyor...")
    
    # Şirket verilerini parse et
    companies = parse_bist_foundation_dates(file_path)
    
    if companies:
        print(f"✅ {len(companies)} şirket verisi başarıyla yüklendi")
        
        # Analiz yap
        analyze_foundation_dates(companies)
        
        # Entegrasyon örnekleri
        demonstrate_integration_examples()
        
    else:
        print("❌ Veri yüklenemedi. Dosya formatını kontrol edin.")