#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _first_token(line):
    """Extract first token from line"""
    parts = line.strip().split(' - ')
    if parts:
        return parts[0].strip()
    return line.strip().split()[0] if line.strip().split() else ""

def load_bist_symbols():
    """Load BIST symbols with fallback hierarchy"""
    # Test new clean list
    try:
        with open("BIST_GUNCEL_TAM_LISTE_NEW.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if lines:
            print(f"[INFO] Yeni BIST listesi kullanılıyor: {len(lines)} sembol")
            symbols = [_first_token(line) + ".IS" for line in lines]
            return symbols
    except FileNotFoundError:
        print("[WARN] Yeni BIST listesi bulunamadı")
    
    return []

if __name__ == "__main__":
    symbols = load_bist_symbols()
    print(f"BIST sembol sayısı: {len(symbols)}")
    print("İlk 5 sembol:", symbols[:5])
    print("Son 5 sembol:", symbols[-5:])
    
    # Test some specific symbols
    test_symbols = ["A1CAP.IS", "AEFES.IS", "AFYON.IS"]
    for sym in test_symbols:
        if sym in symbols:
            print(f"✓ {sym} listede mevcut")
        else:
            print(f"✗ {sym} listede bulunamadı")