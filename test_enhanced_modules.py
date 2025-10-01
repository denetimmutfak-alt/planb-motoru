#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import the enhanced modules
try:
    from crypto_corporate_data import get_crypto_corporate_score
    print("✓ crypto_corporate_data module imported successfully")
except ImportError as e:
    print("✗ Failed to import crypto_corporate_data:", e)

try:
    from commodity_corporate_data import get_commodity_corporate_score
    print("✓ commodity_corporate_data module imported successfully")
except ImportError as e:
    print("✗ Failed to import commodity_corporate_data:", e)

try:
    from enhanced_sentiment_sources import EnhancedSentimentSources
    print("✓ enhanced_sentiment_sources module imported successfully")
except ImportError as e:
    print("✗ Failed to import enhanced_sentiment_sources:", e)

# Test crypto analysis
print("\n=== CRYPTO ANALYSIS TEST ===")
try:
    btc_score = get_crypto_corporate_score("BTC-USD")
    print(f"BTC-USD corporate score: {btc_score}")
    
    eth_score = get_crypto_corporate_score("ETH-USD")
    print(f"ETH-USD corporate score: {eth_score}")
    
    ada_score = get_crypto_corporate_score("ADA-USD")
    print(f"ADA-USD corporate score: {ada_score}")
    
    unknown_score = get_crypto_corporate_score("UNKNOWN-USD")
    print(f"UNKNOWN-USD corporate score: {unknown_score}")
    
except Exception as e:
    print("Error in crypto analysis:", e)

# Test commodity analysis
print("\n=== COMMODITY ANALYSIS TEST ===")
try:
    gold_score = get_commodity_corporate_score("GC=F")
    print(f"GC=F (Gold) corporate score: {gold_score}")
    
    oil_score = get_commodity_corporate_score("CL=F")
    print(f"CL=F (Oil) corporate score: {oil_score}")
    
    silver_score = get_commodity_corporate_score("SI=F")
    print(f"SI=F (Silver) corporate score: {silver_score}")
    
    unknown_score = get_commodity_corporate_score("UNKNOWN=F")
    print(f"UNKNOWN=F corporate score: {unknown_score}")
    
except Exception as e:
    print("Error in commodity analysis:", e)

print("\n=== MODULE TEST COMPLETED ===")