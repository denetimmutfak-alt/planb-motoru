#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerçek varlık listelerinden sembol dizilerini oluştur
"""

def read_bist_symbols():
    """BIST TAM LİSTEsi'nden sembolleri oku"""
    symbols = []
    try:
        with open('bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and '\t' in line:
                    symbol = line.split('\t')[0].strip()
                    if symbol and not symbol.startswith('#'):
                        symbols.append(symbol)
    except Exception as e:
        print(f"BIST okuma hatası: {e}")
    return symbols  # Tüm sembolleri döndür

def read_crypto_symbols():
    """Kripto tam listesinden sembolleri oku"""
    symbols = []
    try:
        with open('kripto tam liste.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and ' - ' in line:
                    symbol = line.split(' - ')[0].strip()
                    if symbol:
                        # Kripto için USD paritesini ekle
                        symbols.append(f"{symbol}-USD")
    except Exception as e:
        print(f"Kripto okuma hatası: {e}")
    return symbols

def read_nasdaq_symbols():
    """NASDAQ tam listesinden sembolleri oku"""
    symbols = []
    try:
        with open('nasdaq tam liste.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and ' - ' in line:
                    symbol = line.split(' - ')[0].strip()
                    if symbol:
                        symbols.append(symbol)
    except Exception as e:
        print(f"NASDAQ okuma hatası: {e}")
    return symbols

def read_commodity_symbols():
    """Emtia tam listesinden sembolleri oku"""
    symbols = []
    try:
        with open('emtia tam liste.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and ' - ' in line:
                    symbol = line.split(' - ')[0].strip()
                    if symbol:
                        # Emtia için futures eki ekle
                        if symbol in ['GC', 'SI', 'CL', 'NG', 'PA', 'PL']:
                            symbols.append(f"{symbol}=F")
                        else:
                            symbols.append(symbol)
    except Exception as e:
        print(f"Emtia okuma hatası: {e}")
    return symbols

def read_xetra_symbols():
    """XETRA tam listesinden sembolleri oku"""
    symbols = []
    try:
        with open('XETRA TAM LİSTE-.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and ' - ' in line:
                    symbol = line.split(' - ')[0].strip()
                    if symbol:
                        # XETRA için .DE eki ekle
                        symbols.append(f"{symbol}.DE")
    except Exception as e:
        print(f"XETRA okuma hatası: {e}")
    return symbols

def generate_javascript_symbols():
    """JavaScript formatında sembol dizileri oluştur"""
    
    print("🔄 Gerçek varlık listelerinden semboller okunuyor...")
    
    bist_symbols = read_bist_symbols()
    crypto_symbols = read_crypto_symbols()
    nasdaq_symbols = read_nasdaq_symbols()
    commodity_symbols = read_commodity_symbols()
    xetra_symbols = read_xetra_symbols()
    
    # Tüm sembolleri birleştir
    all_symbols = bist_symbols[:50] + commodity_symbols[:20] + crypto_symbols[:30] + nasdaq_symbols[:50] + xetra_symbols[:30]
    
    # JavaScript kodu oluştur
    js_code = f"""            const symbols = {{
                'all': {str(all_symbols).replace("'", '"')},
                'bist': {str(bist_symbols).replace("'", '"')},
                'emtia': {str(commodity_symbols).replace("'", '"')},
                'kripto': {str(crypto_symbols).replace("'", '"')},
                'nasdaq': {str(nasdaq_symbols).replace("'", '"')},
                'xetra': {str(xetra_symbols).replace("'", '"')}
            }};"""
    
    print("\n📊 Gerçek varlık sayıları:")
    print(f"🇹🇷 BIST: {len(bist_symbols)} varlık")
    print(f"🥇 Emtia: {len(commodity_symbols)} varlık")
    print(f"₿ Kripto: {len(crypto_symbols)} varlık")
    print(f"🇺🇸 NASDAQ: {len(nasdaq_symbols)} varlık") 
    print(f"🇩🇪 XETRA: {len(xetra_symbols)} varlık")
    print(f"🌐 Toplam: {len(all_symbols)} varlık (dashboard'da kullanılan)")
    
    # Dosyaya yaz
    with open('real_symbols.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print("\n✅ Gerçek semboller 'real_symbols.js' dosyasına yazıldı!")
    return js_code

if __name__ == "__main__":
    generate_javascript_symbols()