#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKILLI SEMBOL TANIMA VE NORMALİZASYON SİSTEMİ
Machine Learning ile otomatik sembol formatı tanıma
"""

import re
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import json

class IntelligentSymbolProcessor:
    """AI ile akıllı sembol işleme sistemi"""
    
    def __init__(self):
        self.market_patterns = {
            'BIST': {
                'patterns': [r'^[A-Z0-9]{3,6}\.IS$', r'^[A-Z0-9]{3,6}$'],
                'suffixes': ['.IS'],
                'examples': ['THYAO.IS', 'GARAN.IS', 'AKBNK.IS']
            },
            'NASDAQ': {
                'patterns': [r'^[A-Z]{1,5}$', r'^[A-Z]{1,5}\.US$'],
                'suffixes': ['.US', ''],
                'examples': ['AAPL', 'MSFT', 'GOOGL']
            },
            'XETRA': {
                'patterns': [r'^[A-Z0-9]{1,4}\.DE$', r'^[A-Z0-9]{1,4}$'],
                'suffixes': ['.DE', '.F'],
                'examples': ['SAP.DE', 'BAS.DE', 'BMW.DE']
            },
            'CRYPTO': {
                'patterns': [r'^[A-Z]{2,10}-USD$', r'^[A-Z]{2,10}$'],
                'suffixes': ['-USD', ''],
                'examples': ['BTC-USD', 'ETH-USD', 'BTC']
            },
            'COMMODITY': {
                'patterns': [r'^[A-Z]{1,3}$', r'^[A-Z]{1,3}[0-9]?$'],
                'suffixes': [''],
                'examples': ['GC', 'CL', 'NG', 'SI']
            }
        }
        
        self.symbol_ml_model = None
        self.symbol_vectorizer = None
        self._train_symbol_classifier()
    
    def _train_symbol_classifier(self):
        """Sembol sınıflandırma modeli eğit"""
        training_data = []
        training_labels = []
        
        # Eğitim verisi oluştur
        for market, info in self.market_patterns.items():
            for example in info['examples']:
                # Sembol özelliklerini çıkar
                features = self._extract_symbol_features(example)
                training_data.append(' '.join(features))
                training_labels.append(market)
        
        # Daha fazla sentetik veri üret
        for market, info in self.market_patterns.items():
            synthetic_symbols = self._generate_synthetic_symbols(market, info, 20)
            for symbol in synthetic_symbols:
                features = self._extract_symbol_features(symbol)
                training_data.append(' '.join(features))
                training_labels.append(market)
        
        # Model eğitimi
        self.symbol_vectorizer = TfidfVectorizer(max_features=100)
        X = self.symbol_vectorizer.fit_transform(training_data)
        
        self.symbol_ml_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.symbol_ml_model.fit(X, training_labels)
        
        print("✅ Sembol sınıflandırma modeli eğitildi")
    
    def _extract_symbol_features(self, symbol: str) -> List[str]:
        """Sembolden özellik çıkarma"""
        features = []
        
        # Temel özellikler
        features.append(f"length_{len(symbol)}")
        features.append(f"has_dot_{bool('.' in symbol)}")
        features.append(f"has_dash_{bool('-' in symbol)}")
        features.append(f"has_number_{bool(re.search(r'\d', symbol))}")
        
        # Suffix analizi
        if '.' in symbol:
            suffix = symbol.split('.')[-1]
            features.append(f"suffix_{suffix}")
        elif '-' in symbol:
            suffix = symbol.split('-')[-1]
            features.append(f"suffix_{suffix}")
        
        # Karakter analizi
        alpha_count = sum(c.isalpha() for c in symbol)
        digit_count = sum(c.isdigit() for c in symbol)
        features.append(f"alpha_ratio_{alpha_count/len(symbol):.1f}")
        features.append(f"digit_ratio_{digit_count/len(symbol):.1f}")
        
        # Pattern matching
        for market, info in self.market_patterns.items():
            for pattern in info['patterns']:
                if re.match(pattern, symbol):
                    features.append(f"matches_{market}_pattern")
        
        return features
    
    def _generate_synthetic_symbols(self, market: str, info: Dict, count: int) -> List[str]:
        """Sentetik sembol üretimi"""
        import random
        import string
        
        symbols = []
        
        for _ in range(count):
            if market == 'BIST':
                base = ''.join(random.choices(string.ascii_uppercase, k=random.randint(4, 6)))
                symbol = f"{base}.IS"
            
            elif market == 'NASDAQ':
                symbol = ''.join(random.choices(string.ascii_uppercase, k=random.randint(2, 5)))
            
            elif market == 'XETRA':
                base = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(2, 4)))
                symbol = f"{base}.DE"
            
            elif market == 'CRYPTO':
                base = ''.join(random.choices(string.ascii_uppercase, k=random.randint(3, 6)))
                symbol = f"{base}-USD"
            
            elif market == 'COMMODITY':
                symbol = ''.join(random.choices(string.ascii_uppercase, k=random.randint(1, 3)))
            
            symbols.append(symbol)
        
        return symbols
    
    def auto_detect_market(self, symbol: str) -> Tuple[str, float]:
        """Sembol için market türünü otomatik tespit et"""
        # Özellik çıkarma
        features = self._extract_symbol_features(symbol)
        feature_text = ' '.join(features)
        
        # ML tahmin
        X = self.symbol_vectorizer.transform([feature_text])
        prediction = self.symbol_ml_model.predict(X)[0]
        probabilities = self.symbol_ml_model.predict_proba(X)[0]
        confidence = max(probabilities)
        
        # Kural tabanlı doğrulama
        rule_based_market = self._rule_based_detection(symbol)
        
        # ML ve kural tabanlı sonuçları birleştir
        if rule_based_market and rule_based_market == prediction:
            final_confidence = min(confidence + 0.2, 1.0)
        else:
            final_confidence = confidence
        
        final_market = rule_based_market if rule_based_market else prediction
        
        return final_market, final_confidence
    
    def _rule_based_detection(self, symbol: str) -> Optional[str]:
        """Kural tabanlı market tespiti"""
        for market, info in self.market_patterns.items():
            for pattern in info['patterns']:
                if re.match(pattern, symbol):
                    return market
        return None
    
    def normalize_symbol(self, symbol: str, target_market: str = None) -> str:
        """Sembolü normalize et"""
        # Büyük harfe çevir
        symbol = symbol.upper().strip()
        
        # Market tespiti
        if not target_market:
            target_market, _ = self.auto_detect_market(symbol)
        
        # Market özelinde normalize et
        if target_market == 'BIST':
            if not symbol.endswith('.IS'):
                symbol += '.IS'
        
        elif target_market == 'NASDAQ':
            # US suffix'i varsa kaldır
            if symbol.endswith('.US'):
                symbol = symbol[:-3]
        
        elif target_market == 'XETRA':
            if not any(symbol.endswith(suffix) for suffix in ['.DE', '.F']):
                symbol += '.DE'
        
        elif target_market == 'CRYPTO':
            if not symbol.endswith('-USD') and not symbol.endswith('USD'):
                symbol += '-USD'
        
        return symbol
    
    def smart_symbol_batch_processing(self, symbols: List[str]) -> Dict[str, Dict]:
        """Toplu sembol işleme"""
        results = {}
        
        print(f"🤖 {len(symbols)} sembol için akıllı işleme başlatılıyor...")
        
        for symbol in symbols:
            original = symbol
            
            # Market tespiti
            market, confidence = self.auto_detect_market(symbol)
            
            # Normalize et
            normalized = self.normalize_symbol(symbol, market)
            
            results[original] = {
                'original': original,
                'normalized': normalized,
                'detected_market': market,
                'confidence': confidence,
                'needs_normalization': original != normalized
            }
        
        return results
    
    def auto_suggest_missing_symbols(self, existing_symbols: List[str], market: str) -> List[str]:
        """Eksik sembolleri otomatik öner"""
        suggestions = []
        
        # Market bazlı ortak semboller
        common_symbols = {
            'BIST': ['THYAO.IS', 'GARAN.IS', 'AKBNK.IS', 'VAKBN.IS', 'ISCTR.IS'],
            'NASDAQ': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA'],
            'XETRA': ['SAP.DE', 'BAS.DE', 'BMW.DE', 'ALV.DE', 'SIE.DE'],
            'CRYPTO': ['BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD'],
            'COMMODITY': ['GC', 'CL', 'NG', 'SI', 'HG', 'ZC', 'ZW']
        }
        
        if market in common_symbols:
            for symbol in common_symbols[market]:
                if symbol not in existing_symbols:
                    suggestions.append(symbol)
        
        return suggestions[:10]  # İlk 10 öneri
    
    def generate_comprehensive_symbol_report(self, symbols: List[str]) -> Dict:
        """Kapsamlı sembol analiz raporu"""
        report = {
            'total_symbols': len(symbols),
            'market_distribution': {},
            'normalization_needed': [],
            'confidence_scores': [],
            'suggestions': {},
            'anomalies': []
        }
        
        # Toplu işleme
        results = self.smart_symbol_batch_processing(symbols)
        
        # İstatistik toplama
        for symbol, data in results.items():
            market = data['detected_market']
            confidence = data['confidence']
            
            # Market dağılımı
            if market not in report['market_distribution']:
                report['market_distribution'][market] = 0
            report['market_distribution'][market] += 1
            
            # Güven skorları
            report['confidence_scores'].append(confidence)
            
            # Normalize edilmesi gerekenler
            if data['needs_normalization']:
                report['normalization_needed'].append({
                    'original': data['original'],
                    'suggested': data['normalized']
                })
            
            # Düşük güven skorlu anomaliler
            if confidence < 0.7:
                report['anomalies'].append({
                    'symbol': symbol,
                    'confidence': confidence,
                    'detected_market': market
                })
        
        # Market bazlı öneriler
        for market in report['market_distribution'].keys():
            suggestions = self.auto_suggest_missing_symbols(symbols, market)
            if suggestions:
                report['suggestions'][market] = suggestions
        
        # Güven skoru istatistikleri
        if report['confidence_scores']:
            report['avg_confidence'] = np.mean(report['confidence_scores'])
            report['min_confidence'] = min(report['confidence_scores'])
            report['max_confidence'] = max(report['confidence_scores'])
        
        return report

def main():
    """Test fonksiyonu"""
    print("🤖 AKILLI SEMBOL TANIMA SİSTEMİ TEST")
    print("=" * 50)
    
    processor = IntelligentSymbolProcessor()
    
    # Test sembolleri
    test_symbols = [
        "AAPL", "aapl.us", "THYAO", "thyao.is",
        "btc", "BTC-USD", "sap.de", "SAP",
        "gc", "GARAN", "microsoft", "ETH"
    ]
    
    print("🔍 Test sembolleri işleniyor...")
    results = processor.smart_symbol_batch_processing(test_symbols)
    
    print("\n📊 SONUÇLAR:")
    print("-" * 50)
    for original, data in results.items():
        print(f"📝 {original} -> {data['normalized']}")
        print(f"   🏪 Market: {data['detected_market']} (Güven: {data['confidence']:.2f})")
        if data['needs_normalization']:
            print(f"   ⚠️ Normalize edildi")
        print()
    
    # Kapsamlı rapor
    print("📊 KAPSAMLI ANALİZ RAPORU:")
    print("-" * 50)
    report = processor.generate_comprehensive_symbol_report(test_symbols)
    
    print(f"Toplam Sembol: {report['total_symbols']}")
    print(f"Ortalama Güven: {report.get('avg_confidence', 0):.2f}")
    print("\nMarket Dağılımı:")
    for market, count in report['market_distribution'].items():
        print(f"  {market}: {count} sembol")
    
    if report['normalization_needed']:
        print(f"\nNormalize Edilecek: {len(report['normalization_needed'])}")
        for item in report['normalization_needed'][:3]:
            print(f"  {item['original']} -> {item['suggested']}")
    
    print("\n🎉 Akıllı sembol tanıma sistemi test edildi!")

if __name__ == "__main__":
    main()