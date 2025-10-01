#!/usr/bin/env python3
"""
VS Code Ortamında PlanB ULTRA Analiz Testi
5 farklı pazardan birer sembol analizi
"""

print('🔍 VS CODE ANALİZİ - 5 Farklı Pazardan 5 Sembol')
print('='*50)

# Ultra_v3 modülünü test et
try:
    from ultra_v3 import compute_ultra_v3
    print('✅ ultra_v3 modülü başarıyla yüklendi')
    
    import numpy as np
    test_data = np.random.random(25) * 0.02  # 25 elemanlı test verisi
    result = compute_ultra_v3(test_data)
    print(f'✅ ULTRA V3 test sonucu: {result:.2f}')
except Exception as e:
    print(f'❌ ULTRA V3 modülü hatası: {e}')

print()

from telegram_full_trader_with_sentiment import analyze_symbol_fast

# 5 farklı pazardan seçilen semboller
test_symbols = [
    ('ASELS.IS', 'BIST'),      # Aselsan - BIST
    ('MSFT', 'NASDAQ'),        # Microsoft - NASDAQ
    ('ETH-USD', 'CRYPTO'),     # Ethereum - CRYPTO
    ('CL=F', 'EMTIA'),         # Ham Petrol - EMTIA
    ('SAP.DE', 'XETRA')        # SAP - XETRA
]

results = []
print('📋 VS CODE ANALİZ BAŞLIYOR...')
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
    print(f'📊 Ortalama Skor: {avg_score:.1f}')
    print('📋 Detaylı Sonuçlar:')
    for r in results:
        print(f'  • {r["symbol"]} - {r["score"]:.1f} - {r["signal"]}')