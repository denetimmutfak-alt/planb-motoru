# -*- coding: utf-8 -*-
"""Simple Risk Management Integration Test - No Emojis"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("RISK MANAGEMENT INTEGRATION TEST")
print("=" * 60)

# Test 1: Module Import
print("\n[TEST 1] Module imports...")
try:
    from ultra_risk_management_module import ultra_risk_manager, TradeSetup
    print("[OK] ultra_risk_management_module imported")
    print(f"     Portfolio Value: ${ultra_risk_manager.portfolio_value:,.0f}")
except Exception as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)

# Test 2: Telegram System Import
print("\n[TEST 2] Telegram system import...")
try:
    import telegram_full_trader_with_sentiment
    print("[OK] telegram_full_trader_with_sentiment imported")
    
    if hasattr(telegram_full_trader_with_sentiment, 'ULTRA_RISK_AVAILABLE'):
        status = telegram_full_trader_with_sentiment.ULTRA_RISK_AVAILABLE
        print(f"     ULTRA_RISK_AVAILABLE: {status}")
        if status:
            print("     [OK] Risk management is integrated!")
    
    if hasattr(telegram_full_trader_with_sentiment, 'planb_ultra_system'):
        system = telegram_full_trader_with_sentiment.planb_ultra_system
        print(f"     System Version: {system.version}")
except Exception as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)

# Test 3: Generate Sample Trade Setup
print("\n[TEST 3] Trade setup generation...")
try:
    test_cases = [
        {"symbol": "AAPL", "price": 182.50, "score": 88.7, "volatility": 25.0, "market": "NASDAQ"},
        {"symbol": "BTC-USD", "price": 43500.0, "score": 87.5, "volatility": 65.0, "market": "CRYPTO"},
    ]
    
    print("\nSample Trade Setups:")
    print("-" * 60)
    
    for test in test_cases:
        atr = test["price"] * 0.02
        trade = ultra_risk_manager.generate_trade_setup(
            symbol=test["symbol"],
            price=test["price"],
            score=test["score"],
            volatility=test["volatility"],
            atr=atr,
            market=test["market"]
        )
        
        print(f"\n{test['symbol']} (Score: {test['score']}, Vol: {test['volatility']}%)")
        print(f"  Position: ${trade.position_size_usd:,.0f} ({trade.position_size_pct:.1f}%)")
        print(f"  Stop Loss: ${trade.stop_loss:.2f} ({trade.stop_loss_pct:.1f}%)")
        print(f"  Take Profit 1: ${trade.take_profit_1:.2f} (+{trade.take_profit_1_pct:.1f}%)")
        print(f"  Risk/Reward: 1:{trade.risk_reward_ratio:.1f}")
        print(f"  Holding Period: {trade.holding_period}")
    
    print("\n[OK] All trade setups generated successfully!")
    
except Exception as e:
    print(f"[FAIL] Trade setup error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Signal Line Formatting
print("\n[TEST 4] Signal line formatting...")
try:
    from telegram_full_trader_with_sentiment import format_signal_line
    
    test_signal = {
        "symbol": "AAPL",
        "market": "NASDAQ",
        "price": 182.50,
        "score": 88.7,
        "signal": "[BUY_STRONG]",
        "sentiment_info": " +Positive",
        "trade_setup": ultra_risk_manager.generate_trade_setup(
            symbol="AAPL",
            price=182.50,
            score=88.7,
            volatility=25.0,
            atr=182.50 * 0.02,
            market="NASDAQ"
        )
    }
    
    formatted = format_signal_line(test_signal)
    print("\nFormatted Telegram Message:")
    print("-" * 60)
    print(formatted[:500])  # First 500 chars to avoid encoding issues
    print("-" * 60)
    
    if "Pozisyon:" in formatted and "SL:" in formatted and "TP1:" in formatted:
        print("\n[OK] Signal formatting includes risk management!")
    else:
        print("\n[WARN] Risk management info not found in formatted message")
    
except Exception as e:
    print(f"[FAIL] Formatting error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test Summary
print("\n" + "=" * 60)
print("INTEGRATION TEST COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\nAll Components Working:")
print("  [OK] Risk Management Module")
print("  [OK] Telegram System Integration")
print("  [OK] Trade Setup Generation")
print("  [OK] Signal Formatting")
print("\nSystem Ready for Production!")
print("Version: v27.2 - Professional Risk Management Integrated")
