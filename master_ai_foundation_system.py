#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MASTER AI KURULUŞ TARİHİ SİSTEMİ
Tüm AI sistemlerini birleştiren ana kontrol merkezi
"""

import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import os

# AI sistemlerini import et
from intelligent_foundation_system import IntelligentFoundationSystem
from intelligent_symbol_processor import IntelligentSymbolProcessor

class MasterAIFoundationSystem:
    """Ana AI kuruluş tarihi sistemi - Tüm AI yeteneklerini birleştirir"""
    
    def __init__(self):
        print("🤖 MASTER AI SİSTEMİ BAŞLATILIYOR...")
        
        self.foundation_ai = IntelligentFoundationSystem()
        self.symbol_ai = IntelligentSymbolProcessor()
        
        self.auto_mode = True  # Tam otomatik mod
        self.learning_mode = True  # Öğrenme modu
        
        print("✅ Tüm AI sistemleri aktif!")
    
    def fully_automated_processing(self, input_data: List[str]) -> Dict:
        """Tamamen otomatik işleme - manuel müdahale yok!"""
        print("🚀 TAM OTOMATİK MOD BAŞLATILIYOR...")
        print("=" * 60)
        
        results = {
            'processed_symbols': {},
            'new_discoveries': {},
            'confidence_scores': {},
            'market_analysis': {},
            'recommendations': [],
            'learning_insights': []
        }
        
        total_symbols = len(input_data)
        successful = 0
        
        for i, raw_input in enumerate(input_data, 1):
            print(f"\n[{i}/{total_symbols}] İşleniyor: {raw_input}")
            
            # 1. Akıllı sembol tanıma ve normalize etme
            symbol_analysis = self.symbol_ai.smart_symbol_batch_processing([raw_input])
            
            if raw_input in symbol_analysis:
                symbol_data = symbol_analysis[raw_input]
                normalized_symbol = symbol_data['normalized']
                detected_market = symbol_data['detected_market']
                symbol_confidence = symbol_data['confidence']
                
                print(f"   🔧 Normalize: {raw_input} -> {normalized_symbol}")
                print(f"   🏪 Market: {detected_market} (Güven: {symbol_confidence:.2f})")
                
                # 2. Otomatik kuruluş tarihi çekme
                foundation_record = self.foundation_ai.auto_detect_and_fetch(normalized_symbol)
                
                if foundation_record:
                    print(f"   ✅ Başarılı: {foundation_record.company_name}")
                    print(f"   📅 Kuruluş: {foundation_record.foundation_date}")
                    print(f"   🎯 Güven: {foundation_record.confidence_score:.2f}")
                    
                    results['processed_symbols'][raw_input] = {
                        'original': raw_input,
                        'normalized': normalized_symbol,
                        'company_name': foundation_record.company_name,
                        'foundation_date': foundation_record.foundation_date,
                        'market_type': foundation_record.market_type,
                        'symbol_confidence': symbol_confidence,
                        'data_confidence': foundation_record.confidence_score,
                        'data_sources': foundation_record.data_sources,
                        'auto_detected': True
                    }
                    
                    successful += 1
                else:
                    print(f"   ❌ Kuruluş tarihi bulunamadı")
                    results['processed_symbols'][raw_input] = {
                        'original': raw_input,
                        'normalized': normalized_symbol,
                        'status': 'foundation_date_not_found',
                        'symbol_confidence': symbol_confidence
                    }
            else:
                print(f"   ❌ Sembol analiz edilemedi")
        
        # 3. Sonuç analizi ve öneriler
        results['success_rate'] = successful / total_symbols
        results['total_processed'] = total_symbols
        results['successful'] = successful
        
        print(f"\n📊 İŞLEM ÖZETİ:")
        print("=" * 40)
        print(f"Toplam: {total_symbols}")
        print(f"Başarılı: {successful}")
        print(f"Başarı oranı: {results['success_rate']:.1%}")
        
        # 4. Market analizi
        market_distribution = {}
        for symbol_data in results['processed_symbols'].values():
            if 'market_type' in symbol_data:
                market = symbol_data['market_type']
                market_distribution[market] = market_distribution.get(market, 0) + 1
        
        results['market_analysis'] = market_distribution
        
        print("\nMarket Dağılımı:")
        for market, count in market_distribution.items():
            print(f"  {market}: {count} şirket")
        
        # 5. Otomatik öneriler üret
        self._generate_auto_recommendations(results)
        
        return results
    
    def _generate_auto_recommendations(self, results: Dict):
        """Otomatik öneriler üret"""
        recommendations = []
        
        # Düşük güven skorlu kayıtları tespit et
        low_confidence = []
        for symbol, data in results['processed_symbols'].items():
            if 'data_confidence' in data and data['data_confidence'] < 0.7:
                low_confidence.append(symbol)
        
        if low_confidence:
            recommendations.append({
                'type': 'low_confidence_review',
                'symbols': low_confidence,
                'action': 'Manuel doğrulama önerilir'
            })
        
        # Market dengesizliği kontrolü
        if results['market_analysis']:
            dominant_market = max(results['market_analysis'], key=results['market_analysis'].get)
            dominant_ratio = results['market_analysis'][dominant_market] / results['successful']
            
            if dominant_ratio > 0.7:
                recommendations.append({
                    'type': 'market_imbalance',
                    'dominant_market': dominant_market,
                    'ratio': dominant_ratio,
                    'action': 'Diğer market türlerinden veri eklenmesi önerilir'
                })
        
        results['recommendations'] = recommendations
    
    def auto_update_existing_system(self):
        """Mevcut sistemi otomatik güncelle"""
        print("🔄 MEVCUT SİSTEM OTOMATİK GÜNCELLEMESİ")
        print("=" * 50)
        
        # Mevcut veritabanını yükle
        db_path = "data/foundation_dates/foundation_database.json"
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
            print(f"📊 Mevcut veritabanı: {len(existing_data)} kayıt")
            
            # Güven skoru olmayan kayıtları bul
            needs_update = []
            for symbol, data in existing_data.items():
                if 'confidence_score' not in data or data.get('confidence_score', 0) < 0.5:
                    needs_update.append(symbol)
            
            print(f"🔧 Güncelleme gerekiyor: {len(needs_update)} kayıt")
            
            if needs_update[:5]:  # İlk 5'ini test et
                print("🤖 AI ile otomatik güncelleme başlatılıyor...")
                updated_results = self.fully_automated_processing(needs_update[:5])
                
                # Güncellemeleri mevcut veritabanına entegre et
                updated_count = 0
                for symbol, new_data in updated_results['processed_symbols'].items():
                    if 'foundation_date' in new_data:
                        existing_data[symbol].update({
                            'confidence_score': new_data.get('data_confidence', 0.5),
                            'data_sources': new_data.get('data_sources', []),
                            'auto_updated': True,
                            'last_update': datetime.now().isoformat()
                        })
                        updated_count += 1
                
                # Güncellenmiş veritabanını kaydet
                if updated_count > 0:
                    with open(db_path, 'w', encoding='utf-8') as f:
                        json.dump(existing_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"✅ {updated_count} kayıt otomatik güncellendi!")
                else:
                    print("⚠️ Güncellenecek veri bulunamadı")
        else:
            print("❌ Mevcut veritabanı bulunamadı")
    
    def intelligent_discovery_mode(self, market_type: str = None):
        """Akıllı keşif modu - yeni sembolleri otomatik bul"""
        print("🔍 AKILLI KEŞİF MODU AKTİF")
        print("=" * 40)
        
        # Market bazlı popüler sembolleri keşfet
        discovery_symbols = {
            'NASDAQ': ['NVDA', 'META', 'NFLX', 'CRM', 'ZOOM', 'UBER', 'LYFT', 'SPOT'],
            'BIST': ['TUPRS.IS', 'ARCLK.IS', 'KOZAL.IS', 'MGROS.IS', 'PGSUS.IS'],
            'CRYPTO': ['MATIC-USD', 'ATOM-USD', 'ALGO-USD', 'SAND-USD', 'MANA-USD'],
            'XETRA': ['ADYEN.DE', 'ASML.DE', 'NESN.DE', 'NOVN.DE']
        }
        
        if market_type and market_type in discovery_symbols:
            symbols_to_discover = discovery_symbols[market_type]
        else:
            # Tüm marketlerden örnekle
            symbols_to_discover = []
            for symbols in discovery_symbols.values():
                symbols_to_discover.extend(symbols[:3])  # Her marketten 3'er
        
        print(f"🎯 {len(symbols_to_discover)} yeni sembol keşfediliyor...")
        
        discovery_results = self.fully_automated_processing(symbols_to_discover)
        
        print("\n🆕 YENİ KEŞİFLER:")
        successful_discoveries = []
        for symbol, data in discovery_results['processed_symbols'].items():
            if 'foundation_date' in data:
                successful_discoveries.append(data)
                print(f"  ✅ {symbol}: {data['company_name']} ({data['foundation_date']})")
        
        print(f"\n🎉 {len(successful_discoveries)} yeni şirket keşfedildi!")
        return discovery_results

def demo_full_automation():
    """Tam otomasyon demo"""
    print("🎭 TAM OTOMASYON DEMO")
    print("=" * 50)
    
    # Ana AI sistemini başlat
    master_ai = MasterAIFoundationSystem()
    
    # Demo veri - karışık formatlar
    demo_input = [
        "AAPL",           # Temiz NASDAQ
        "msft",           # Küçük harf
        "thyao",          # BIST eksik suffix
        "btc-usd",        # Kripto
        "sap.de",         # XETRA
        "INVALID123",     # Geçersiz
        "tsla"            # Tesla
    ]
    
    print("📥 Demo girdi:")
    for item in demo_input:
        print(f"  - {item}")
    
    # Tam otomatik işleme
    results = master_ai.fully_automated_processing(demo_input)
    
    # Sonuçları göster
    print("\n🎯 FINAL SONUÇLAR:")
    print("=" * 40)
    
    for symbol, data in results['processed_symbols'].items():
        if 'foundation_date' in data:
            print(f"✅ {symbol}:")
            print(f"   📝 {data['company_name']}")
            print(f"   📅 {data['foundation_date']}")
            print(f"   🏪 {data['market_type']}")
            print(f"   🎯 Güven: {data['data_confidence']:.2f}")
        else:
            print(f"❌ {symbol}: İşlenemedi")
    
    # Öneriler
    if results['recommendations']:
        print("\n💡 OTOMATİK ÖNERİLER:")
        for rec in results['recommendations']:
            print(f"  ⚠️ {rec['type']}: {rec['action']}")
    
    print("\n🤖 Tam otomasyon demo tamamlandı!")

if __name__ == "__main__":
    demo_full_automation()