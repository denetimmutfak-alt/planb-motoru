#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GERÇEKTEKİ VARLIK SAYISI ANALİZİ
Tüm provider'lardan gerçek sembol sayılarını al
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.providers.bist_provider import BISTProvider
from src.data.providers.nasdaq_provider import NASDAQProvider  
from src.data.providers.xetra_provider import XETRAProvider
from src.data.providers.crypto_provider import CryptoProvider
from src.data.providers.commodities_provider import CommoditiesProvider

def count_real_assets():
    """Gerçekteki tüm provider'lardan sembol sayılarını al"""
    
    print("🔍 GERÇEKTEKİ VARLIK SAYISI ANALİZİ")
    print("=" * 60)
    print("Tüm provider'lardan canlı veri çekiliyor...")
    
    providers_data = {}
    total_symbols = 0
    
    try:
        # BIST Provider
        print("\n📊 BIST Provider analizi...")
        bist = BISTProvider()
        bist_symbols = bist.get_symbols()
        providers_data["BIST"] = len(bist_symbols)
        total_symbols += len(bist_symbols)
        print(f"✅ BIST: {len(bist_symbols)} sembol")
        
        # NASDAQ Provider  
        print("\n📊 NASDAQ Provider analizi...")
        nasdaq = NASDAQProvider()
        nasdaq_symbols = nasdaq.get_symbols()
        providers_data["NASDAQ"] = len(nasdaq_symbols)
        total_symbols += len(nasdaq_symbols)
        print(f"✅ NASDAQ: {len(nasdaq_symbols)} sembol")
        
        # XETRA Provider
        print("\n📊 XETRA Provider analizi...")
        xetra = XETRAProvider()
        xetra_symbols = xetra.get_symbols()
        providers_data["XETRA"] = len(xetra_symbols)
        total_symbols += len(xetra_symbols)
        print(f"✅ XETRA: {len(xetra_symbols)} sembol")
        
        # Crypto Provider
        print("\n📊 Crypto Provider analizi...")
        crypto = CryptoProvider()
        crypto_symbols = crypto.get_symbols()
        providers_data["Crypto"] = len(crypto_symbols)
        total_symbols += len(crypto_symbols)
        print(f"✅ Crypto: {len(crypto_symbols)} sembol")
        
        # Commodities Provider
        print("\n📊 Commodities Provider analizi...")
        commodities = CommoditiesProvider()
        commodities_symbols = commodities.get_symbols()
        providers_data["Commodities"] = len(commodities_symbols)
        total_symbols += len(commodities_symbols)
        print(f"✅ Commodities: {len(commodities_symbols)} sembol")
        
    except Exception as e:
        print(f"❌ Provider analizi hatası: {e}")
        return None
    
    # Sonuçları göster
    print(f"\n🎯 GERÇEKTEKİ TOPLAM VARLIK SAYILARI:")
    print("=" * 60)
    
    for provider, count in providers_data.items():
        print(f"{provider}: {count:,} sembol")
    
    print(f"\n🎯 GENEL TOPLAM: {total_symbols:,} sembol")
    
    # Detaylı analiz
    print(f"\n📊 DETAYLI ANALİZ:")
    print("-" * 40)
    largest_provider = max(providers_data.items(), key=lambda x: x[1])
    print(f"En büyük provider: {largest_provider[0]} ({largest_provider[1]:,} sembol)")
    
    # Provider çeşitliliği
    print(f"Provider sayısı: {len(providers_data)}")
    print(f"Ortalama sembol/provider: {total_symbols/len(providers_data):.0f}")
    
    # Ultra modül entegrasyonu
    print(f"\n🎯 ULTRA MODÜL ENTEGRASYon KAPASİTESİ:")
    print("-" * 40)
    ultra_modules = [
        "Ultra Finansal Analiz",
        "Ultra Teknik Analiz", 
        "Ultra Trend Analizi",
        "Ultra Volatilite Analizi",
        "Ultra Risk Analizi",
        "Ultra Opsiyon Analizi",
        "Ultra Gann Analizi",
        "Ultra Astroloji Analizi",
        "Ultra Sentiment Analizi",
        "Ultra Ekonomik Analiz",
        "Ultra Shemitah Analizi",
        "Ultra Güneş Analizi",
        "Ultra Ay Analizi",
        "Ultra İstatistiksel Analiz",
        "Ultra Para Birimi Analizi",
        "Ultra Emtia Analizi",
        "Ultra Tahvil Analizi",
        "Ultra Kripto Analizi",
        "Ultra ML Entegrasyonu"
    ]
    
    print(f"✅ {len(ultra_modules)} Ultra Modül aktif")
    print(f"✅ {total_symbols:,} enstrüman analiz kapasitesi")
    print(f"✅ Toplam analiz kombinasyonu: {total_symbols * len(ultra_modules):,}")
    
    # Performans tahmini
    print(f"\n⚡ PERFORMANS TAHMİNİ:")
    print("-" * 40)
    avg_time_per_symbol = 0.05  # 50ms per symbol estimate
    total_time = total_symbols * avg_time_per_symbol
    print(f"Tahmini toplam analiz süresi: {total_time:.1f} saniye")
    print(f"Paralel işlemle: {total_time/4:.1f} saniye (4 core)")
    
    memory_per_symbol = 2  # 2KB per symbol estimate  
    total_memory = total_symbols * memory_per_symbol / 1024  # MB
    print(f"Tahmini bellek kullanımı: {total_memory:.1f} MB")
    
    return {
        "providers": providers_data,
        "total": total_symbols,
        "ultra_modules": len(ultra_modules)
    }

def show_provider_details():
    """Her provider'ın detaylarını göster"""
    
    print(f"\n📋 PROVIDER DETAYLARI:")
    print("=" * 60)
    
    try:
        # BIST detayları
        bist = BISTProvider()
        bist_symbols = bist.get_symbols()
        print(f"\n🇹🇷 BIST Provider:")
        print(f"   Toplam: {len(bist_symbols)} sembol")
        print(f"   Format: *.IS (Türk hisse senetleri)")
        print(f"   Örnekler: {', '.join(bist_symbols[:5])}")
        
        # NASDAQ detayları
        nasdaq = NASDAQProvider()
        nasdaq_symbols = nasdaq.get_symbols()
        print(f"\n🇺🇸 NASDAQ Provider:")
        print(f"   Toplam: {len(nasdaq_symbols)} sembol")
        print(f"   Format: Stock symbols (US tech)")
        print(f"   Örnekler: {', '.join(nasdaq_symbols[:5])}")
        
        # XETRA detayları
        xetra = XETRAProvider()
        xetra_symbols = xetra.get_symbols()
        print(f"\n🇩🇪 XETRA Provider:")
        print(f"   Toplam: {len(xetra_symbols)} sembol")
        print(f"   Format: *.DE (German stocks)")
        print(f"   Örnekler: {', '.join(xetra_symbols[:5])}")
        
        # Crypto detayları
        crypto = CryptoProvider()
        crypto_symbols = crypto.get_symbols()
        print(f"\n₿ Crypto Provider:")
        print(f"   Toplam: {len(crypto_symbols)} sembol")
        print(f"   Format: *-USD (Cryptocurrency)")
        print(f"   Örnekler: {', '.join(crypto_symbols[:5])}")
        
        # Commodities detayları
        commodities = CommoditiesProvider()
        commodities_symbols = commodities.get_symbols()
        print(f"\n🥇 Commodities Provider:")
        print(f"   Toplam: {len(commodities_symbols)} sembol")
        print(f"   Format: *=F (Futures)")
        print(f"   Örnekler: {', '.join(commodities_symbols[:5])}")
        
    except Exception as e:
        print(f"❌ Provider detay hatası: {e}")

if __name__ == "__main__":
    print("🎯 GERÇEK VARLIK SAYISI ANALİZİ BAŞLIYOR...")
    
    # Ana analiz
    results = count_real_assets()
    
    if results:
        # Provider detayları
        show_provider_details()
        
        print(f"\n✅ ANALİZ TAMAMLANDI!")
        print(f"Toplam {results['total']:,} sembol {results['ultra_modules']} ultra modülle hazır!")
    else:
        print("❌ Analiz başarısız oldu.")