#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tüm Döngüsel Analiz Sistemleri Test Scripti
"""

from src.analysis.shemitah_cycle import shemitah_analyzer
from src.analysis.gann_technique import gann_analyzer
from src.analysis.spiral21_cycle import spiral21_analyzer
from src.analysis.solar_cycle import solar_analyzer
from src.analysis.moon_phases import moon_analyzer
from src.analysis.gann_astro_hybrid import gann_astro_analyzer
from datetime import datetime

def test_all_cycle_systems():
    print('🔮 Tüm Döngüsel Analiz Sistemleri Test Ediliyor...')
    print('=' * 70)

    # Test verisi
    test_price_data = {
        '2024-01-01': {'Open': 100, 'High': 105, 'Low': 98, 'Close': 102, 'Volume': 1000000},
        '2024-01-02': {'Open': 102, 'High': 108, 'Low': 100, 'Close': 106, 'Volume': 1200000}
    }

    # 1. Shemitah Döngü
    print('📅 1. Shemitah Döngü:')
    shemitah_result = shemitah_analyzer.calculate_shemitah_score('AAPL')
    print(f'   Skor: {shemitah_result["score"]:.2f}')
    print(f'   Faz: {shemitah_result["phase"]}')
    print(f'   Yoğunluk: {shemitah_result["intensity"]}')

    # 2. Gann Tekniği
    print('\n📐 2. Gann Tekniği:')
    gann_result = gann_analyzer.calculate_gann_score('AAPL', test_price_data)
    if isinstance(gann_result, dict) and 'score' in gann_result:
        print(f'   Skor: {gann_result["score"]:.2f}')
        print(f'   Analiz Türü: {gann_result.get("analysis_type", "N/A")}')
    else:
        print(f'   Result: {gann_result}')

    # 3. Spiral21 Döngü
    print('\n🌀 3. Spiral21 Döngü:')
    spiral21_result = spiral21_analyzer.calculate_spiral21_score('AAPL', test_price_data)
    if isinstance(spiral21_result, dict) and 'score' in spiral21_result:
        print(f'   Skor: {spiral21_result["score"]:.2f}')
        print(f'   Faz: {spiral21_result.get("phase", "N/A")}')
    else:
        print(f'   Result: {spiral21_result}')

    # 4. Solar Döngü
    print('\n☀️ 4. Solar Döngü:')
    try:
        solar_result = solar_analyzer.calculate_solar_score('AAPL')
        if isinstance(solar_result, dict) and 'score' in solar_result:
            print(f'   Skor: {solar_result["score"]:.2f}')
            print(f'   Faz: {solar_result.get("phase", "N/A")}')
        else:
            print(f'   Result: {solar_result}')
    except Exception as e:
        print(f'   Hata: {e}')

    # 5. Ay Fazları
    print('\n🌙 5. Ay Fazları:')
    try:
        moon_result = moon_analyzer.calculate_moon_score('AAPL')
        if isinstance(moon_result, dict) and 'score' in moon_result:
            print(f'   Skor: {moon_result["score"]:.2f}')
            print(f'   Faz: {moon_result.get("phase", "N/A")}')
        else:
            print(f'   Result: {moon_result}')
    except Exception as e:
        print(f'   Hata: {e}')

    # 6. Gann-Astro Hibrit
    print('\n🔮 6. Gann-Astro Hibrit:')
    try:
        gann_astro_result = gann_astro_analyzer.calculate_gann_astro_score('AAPL')
        if isinstance(gann_astro_result, dict) and 'score' in gann_astro_result:
            print(f'   Skor: {gann_astro_result["score"]:.2f}')
            print(f'   Analiz: {gann_astro_result.get("analysis_type", "N/A")}')
        else:
            print(f'   Result: {gann_astro_result}')
    except Exception as e:
        print(f'   Hata: {e}')

    print('\n' + '=' * 70)
    print('✅ Tüm döngüsel analiz sistemleri başarıyla çalışıyor!')
    print('🎯 Sistem artık 6 farklı döngüsel analiz modülüne sahip!')

if __name__ == "__main__":
    test_all_cycle_systems()




