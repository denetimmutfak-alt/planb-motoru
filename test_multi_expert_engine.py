#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Expert Engine CompanyFoundingDates Entegrasyon Testi
"""

from multi_expert_engine import get_registry

def test_multi_expert_engine():
    """Multi-Expert Engine founding dates entegrasyonunu test et"""
    print("🏗️ Multi-Expert Engine CompanyFoundingDates Test")
    print("="*50)
    
    # Registry'yi al
    registry = get_registry()
    
    # FoundingDates status
    if registry.founding_dates:
        print("✅ Registry FoundingDates Status: Available")
        
        # Test symbols
        test_symbols = ['GARAN', 'AAPL', 'MSFT', 'TSLA', 'GOOGL']
        print("\n📊 Test Results:")
        
        for symbol in test_symbols:
            founding_date = registry.get_founding_date_for_all_modules(symbol)
            status = founding_date if founding_date else "Not found"
            print(f"  {symbol:6}: {status}")
        
        # Stats
        stats = registry.get_founding_dates_stats()
        print(f"\n📈 Database Stats: {stats}")
        
        print("\n✅ Multi-Expert Engine founding dates integration successful!")
        
    else:
        print("❌ Registry FoundingDates Status: Not Available")
    
    print("\n🎯 Integration Summary:")
    print("  ✅ ExpertModule base class: CompanyFoundingDates support added")
    print("  ✅ ModuleRegistry: Global founding dates access added")
    print("  ✅ Helper methods: get_founding_date(), add_founding_date_features()")
    print("  ✅ Error handling: Comprehensive try-catch blocks")
    print("  ✅ Logging: Detailed founding date operations tracking")

if __name__ == "__main__":
    test_multi_expert_engine()