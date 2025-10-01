from src.data.company_founding_dates import CompanyFoundingDates
cfd = CompanyFoundingDates()
test_symbols = ['SOKE', 'AKSA', 'ASELS', 'AKBNK', 'BIMAS']
print('=== TAM LİSTE KONTROL ===')
for symbol in test_symbols:
    date = cfd.get_founding_date(symbol)
    if date:
        print(f'✅ {symbol}: {date}')
    else:
        print(f'❌ {symbol}: Tarih bulunamadı')
print(f'�� Toplam: {cfd.get_count()}')