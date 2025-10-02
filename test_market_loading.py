#!/usr/bin/env python3
"""
Telegram Bot Load Fonksiyonları Test
"""

import sys
sys.path.append('.')

# Test script to verify all markets are loading correctly
from pathlib import Path

BASE_DIR = Path(".")

def _safe_read_lines(path: Path) -> list[str]:
    """Güvenli dosya okuma"""
    try:
        if not path.exists():
            print(f"❌ Dosya bulunamadı: {path}")
            return []
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        
        print(f"✅ {path.name}: {len(lines)} satır okundu")
        return lines
    except Exception as e:
        print(f"❌ {path} okuma hatası: {e}")
        return []

def _first_token(line: str) -> str:
    """Satırdan ilk token'ı al"""
    try:
        if ' - ' in line:
            return line.split(' - ', 1)[0].strip()
        else:
            return line.split()[0].strip() if line.split() else line.strip()
    except Exception:
        return line.strip()

def test_load_nasdaq_symbols() -> list[str]:
    """NASDAQ hisseleri"""
    lines = _safe_read_lines(BASE_DIR / "NASDAQ_TAM_LISTE_NEW.txt")
    symbols = [_first_token(line) for line in lines]
    print(f"🇺🇸 NASDAQ: {len(symbols)} sembolleri - İlk 5: {symbols[:5]}")
    return symbols

def test_load_crypto_symbols() -> list[str]:
    """Kripto listesi"""
    lines = _safe_read_lines(BASE_DIR / "KRIPTO_TAM_LISTE_NEW.txt")
    symbols = [_first_token(line) for line in lines]
    # Kripto için -USD suffix ekle
    crypto_symbols = [f"{symbol}-USD" for symbol in symbols if symbol]
    print(f"💰 CRYPTO: {len(crypto_symbols)} sembolleri - İlk 5: {crypto_symbols[:5]}")
    return crypto_symbols

def test_load_commodity_symbols() -> list[str]:
    """Emtia listesi"""
    lines = _safe_read_lines(BASE_DIR / "EMTIA_TAM_LISTE_NEW.txt")
    symbols = [_first_token(line) for line in lines]
    # Emtia için futures suffix ekle
    result = []
    for symbol in symbols:
        if symbol in ['GC', 'SI', 'CL', 'NG', 'PA', 'PL', 'ZC', 'ZW', 'ZS']:
            result.append(f"{symbol}=F")
        else:
            result.append(symbol)
    print(f"🌾 EMTIA: {len(result)} sembolleri - İlk 5: {result[:5]}")
    return result

def test_load_xetra_symbols() -> list[str]:
    """XETRA (Almanya) listesi"""
    lines = _safe_read_lines(BASE_DIR / "XETRA_TAM_LISTE_NEW.txt")
    symbols = [_first_token(line) for line in lines]
    # XETRA için .DE suffix ekle
    xetra_symbols = [f"{symbol}.DE" for symbol in symbols if symbol]
    print(f"🇩🇪 XETRA: {len(xetra_symbols)} sembolleri - İlk 5: {xetra_symbols[:5]}")
    return xetra_symbols

def test_load_bist_symbols() -> list[str]:
    """BIST listesi"""
    lines = _safe_read_lines(BASE_DIR / "BIST_GUNCEL_TAM_LISTE_NEW.txt")
    symbols = [_first_token(line) for line in lines]
    # BIST için .IS suffix ekle
    bist_symbols = [f"{symbol}.IS" for symbol in symbols if symbol]
    print(f"🇹🇷 BIST: {len(bist_symbols)} sembolleri - İlk 5: {bist_symbols[:5]}")
    return bist_symbols

def main():
    print("🔍 TÜM PİYASA SİMGE LİSTELERİ TEST EDİLİYOR")
    print("="*60)
    
    # Test all markets
    bist = test_load_bist_symbols()
    nasdaq = test_load_nasdaq_symbols()
    crypto = test_load_crypto_symbols()
    emtia = test_load_commodity_symbols()
    xetra = test_load_xetra_symbols()
    
    print(f"\n📊 ÖZET:")
    print(f"🇹🇷 BIST: {len(bist)} hisse")
    print(f"🇺🇸 NASDAQ: {len(nasdaq)} hisse")
    print(f"💰 CRYPTO: {len(crypto)} kripto")
    print(f"🌾 EMTIA: {len(emtia)} emtia")
    print(f"🇩🇪 XETRA: {len(xetra)} hisse")
    print(f"🌐 TOPLAM: {len(bist) + len(nasdaq) + len(crypto) + len(emtia) + len(xetra)} varlık")
    
    # Sorun tespiti
    if len(nasdaq) == 0:
        print("❌ NASDAQ yüklenemedi!")
    if len(crypto) == 0:
        print("❌ CRYPTO yüklenemedi!")
    if len(emtia) == 0:
        print("❌ EMTIA yüklenemedi!")
    if len(xetra) == 0:
        print("❌ XETRA yüklenemedi!")
    
    if all([len(bist) > 0, len(nasdaq) > 0, len(crypto) > 0, len(emtia) > 0, len(xetra) > 0]):
        print("\n✅ TÜM PİYASALAR BAŞARILI! Telegram bot şimdi tüm piyasaları analiz edebilecek.")
    else:
        print("\n❌ BAZI PİYASALAR YÜKLENEMEDİ! Dosya yollarını kontrol edin.")

if __name__ == "__main__":
    main()