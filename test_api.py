import requests
import time

print("🎯 API TEST - Multi-Expert Engine")
print("="*40)

try:
    # Health check
    health = requests.get('http://localhost:5000/health', timeout=5)
    print('✅ Health Status:', health.json()['status'])
    print('🔥 Multi-Expert Engine:', '✅ Aktif' if health.json()['multi_expert'] else '❌ Deaktif')
    
    # Quick analysis test
    print()
    print('📊 Hızlı analiz testi başlatılıyor...')
    start = time.time()
    
    analysis = requests.get('http://localhost:5000/api/analysis', timeout=30)
    elapsed = time.time() - start
    
    if analysis.status_code == 200:
        data = analysis.json()
        print(f'⏱️ Süre: {elapsed:.1f}s')
        print(f'✅ Final Skor: {data["final_score"]}/100')
        print(f'🎯 Sinyal: {data["signal"]}')
        print(f'📊 Konsensüs: {data["consensus_strength"]}%')
        print('🎉 API TAM ÇALIŞIYOR!')
    else:
        print(f'❌ HTTP Error: {analysis.status_code}')
        
except Exception as e:
    print(f'❌ Test hatası: {e}')