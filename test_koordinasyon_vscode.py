#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VS Code - Hetzner Koordinasyon Testi
5 Farklı Pazardan 5 Sembol Analizi
"""

print('🔍 VS CODE ANALİZİ - 5 Farklı Pazardan 5 Sembol')
print('='*50)

from telegram_full_trader_with_sentiment import analyze_symbol_fast

# 5 farklı pazardan seçilen semboller
test_symbols = [
    ('THYAO.IS', 'BIST'),      # Türk Hava Yolları - BIST
    ('AAPL', 'NASDAQ'),        # Apple - NASDAQ
    ('BTC-USD', 'CRYPTO'),     # Bitcoin - CRYPTO
    ('GC=F', 'EMTIA'),         # Altın - EMTIA
    ('VOW3.DE', 'XETRA')       # Volkswagen - XETRA
]

results = []
print("📋 ANALİZ BAŞLIYOR...")
print()

for symbol, market in test_symbols:
    print(f'📊 {market} pazarından {symbol} analiz ediliyor...')
    try:
        result = analyze_symbol_fast(symbol)
        if result:
            results.append(result)
            score = result['score']
            signal = result['signal']
            price = result['price']
            print(f'  ✅ Fiyat: {price} - Skor: {score:.1f} - Sinyal: {signal}')
            
            # İşleme şemasını incele
            print(f'  📋 İşleme Detayları:')
            print(f'     • Pazar: {market}')
            print(f'     • Sembol: {symbol}')
            print(f'     • Final Skor: {score:.1f}/100')
            print(f'     • Sinyal Türü: {signal}')
            if 'sentiment_info' in result and result['sentiment_info']:
                print(f'     • Sentiment: {result["sentiment_info"]}')
                
        else:
            print(f'  ❌ Analiz başarısız')
            
    except Exception as e:
        print(f'  ❌ Hata: {e}')
        
    print('-' * 30)

print()
print('📈 VS CODE SONUÇLARI:')
print(f'📊 Toplam Başarılı Analiz: {len(results)}/5')

if results:
    avg_score = sum(r['score'] for r in results) / len(results)
    strong_signals = [r for r in results if r['score'] >= 65]
    moderate_signals = [r for r in results if 50 <= r['score'] < 65]
    weak_signals = [r for r in results if r['score'] < 50]
    
    print(f'📊 Ortalama Skor: {avg_score:.1f}')
    print(f'🎯 Güçlü Sinyal (≥65): {len(strong_signals)} adet')
    print(f'🟡 Orta Sinyal (50-64): {len(moderate_signals)} adet')
    print(f'🔴 Zayıf Sinyal (<50): {len(weak_signals)} adet')
    
    print()
    print('🔍 DETAYLI SONUÇLAR:')
    for i, result in enumerate(results, 1):
        print(f'{i}. {result["symbol"]}: {result["score"]:.1f} - {result["signal"]}')