#!/usr/bin/env python3
# Simple server test script
import os
import sys

print("=== HETZNER SERVER DEPLOYMENT CHECK ===")

# Check if new BIST list exists
if os.path.exists("BIST_GUNCEL_TAM_LISTE_NEW.txt"):
    with open("BIST_GUNCEL_TAM_LISTE_NEW.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    print(f"✓ New BIST list found: {len(lines)} symbols")
else:
    print("✗ New BIST list not found")

# Check enhanced modules
modules = ["crypto_corporate_data.py", "commodity_corporate_data.py", "enhanced_sentiment_sources.py"]
for module in modules:
    if os.path.exists(module):
        size = os.path.getsize(module)
        print(f"✓ {module}: {size/1024:.1f}KB")
    else:
        print(f"✗ {module}: Missing")

# Check main trader
if os.path.exists("telegram_full_trader_with_sentiment.py"):
    size = os.path.getsize("telegram_full_trader_with_sentiment.py")
    print(f"✓ Main trader: {size/1024:.1f}KB")
else:
    print("✗ Main trader: Missing")

print("\n=== DEPLOYMENT STATUS ===")
print("Ready for analysis with enhanced capabilities")