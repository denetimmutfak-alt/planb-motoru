#!/usr/bin/env python3
"""
🎯 ULTRA PREMIUM THRESHOLD: 55 PUAN
===================================
Bu script telegram_full_trader.py'yi 55 puan threshold'a günceller
"""

# Original script'i oku
with open("telegram_full_trader.py", "r", encoding="utf-8") as f:
    content = f.read()

# Threshold'u 45'ten 55'e çıkar
content = content.replace(
    'STRONG_THRESHOLD = float(os.getenv("STRONG_THRESHOLD", "45"))',
    'STRONG_THRESHOLD = float(os.getenv("STRONG_THRESHOLD", "55"))'
)

# Yeni dosyayı yaz
with open("telegram_full_trader_55PUAN.py", "w", encoding="utf-8") as f:
    f.write(content)

print("🎯 ULTRA PREMIUM THRESHOLD HAZIR!")
print("📁 Yeni dosya: telegram_full_trader_55PUAN.py")
print("⚡ Threshold: 45 → 55 puan")
print("🏆 ULTRA PREMIUM seviye aktif!")
print("📊 Beklenen: Günde 1-3 ultra kaliteli sinyal")