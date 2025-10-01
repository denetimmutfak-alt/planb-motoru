#!/usr/bin/env python3
"""
🚨 EMERGENCY THRESHOLD FIX
=========================
65 puan threshold çok yüksek!
45 puana düşüreceğiz.
"""

# Original script'i oku
with open("telegram_full_trader.py", "r", encoding="utf-8") as f:
    content = f.read()

# Threshold'u 65'ten 45'e düşür
content = content.replace(
    'STRONG_THRESHOLD = float(os.getenv("STRONG_THRESHOLD", "65"))',
    'STRONG_THRESHOLD = float(os.getenv("STRONG_THRESHOLD", "45"))'
)

# Yeni dosyayı yaz
with open("telegram_full_trader_FIXED.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ EMERGENCY FIX HAZIR!")
print("📁 Yeni dosya: telegram_full_trader_FIXED.py")
print("🎯 Threshold: 65 → 45 puan")
print("⚡ Artık daha fazla sinyal alacaksınız!")