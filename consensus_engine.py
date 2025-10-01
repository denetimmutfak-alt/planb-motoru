#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CONSENSUS ENGINE - UNCERTAINTY-AWARE ENSEMBLE SYSTEM
Arkadaş fikirlerinin kalbi - tüm expert modülleri birleştiren sistem
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging
from dataclasses import dataclass
import json
from collections import defaultdict
import statistics

from multi_expert_engine import ExpertModule, ModuleResult, ModuleRegistry, get_registry

logger = logging.getLogger(__name__)

@dataclass
class EnsembleResult:
    """Ensemble sonuç formatı"""
    final_score: float  # 0-100 nihai skor
    signal: str  # "BUY", "HOLD", "SELL"
    confidence: float  # 0-1 genel güven seviyesi
    explanation: str  # Ana açıklama
    timestamp: str  # Analiz zamanı
    
    # Detay bilgiler
    module_contributions: Dict[str, float]  # Her modülün nihai skora katkısı
    module_results: Dict[str, Dict[str, Any]]  # Her modülün detay sonucu
    top_drivers: List[Dict[str, Any]]  # En etkili 3-5 modül
    risk_factors: List[str]  # Tespit edilen risk faktörleri
    opportunity_factors: List[str]  # Tespit edilen fırsat faktörleri
    
    # Meta bilgiler
    total_modules_used: int  # Kullanılan modül sayısı
    average_uncertainty: float  # Ortalama belirsizlik
    consensus_strength: float  # Konsensüs gücü (0-1)
    conflicting_signals: List[str]  # Çelişkili sinyaller

class ConsensusEngine:
    """
    Uncertainty-Aware Ensemble System
    Arkadaşın önerdiği weighted uncertainty scoring yaklaşımı
    """
    
    def __init__(self, base_weights: Dict[str, float] = None):
        self.registry = get_registry()
        
        # Base weights - her modül için temel ağırlık
        self.base_weights = base_weights or {}
        
        # Dynamic weight faktörleri
        self.uncertainty_penalty = 0.8  # Uncertainty'nin ağırlığa etkisi
        self.performance_factor = 0.2  # Geçmiş performansın etkisi
        self.confidence_threshold = 0.7  # Güven eşiği
        
        # Signal thresholds
        self.buy_threshold = 65.0
        self.sell_threshold = 35.0
        
        # İstatistikler
        self.prediction_history = []
        self.performance_metrics = {}
        
        logger.info("ConsensusEngine initialized")
    
    def calculate_dynamic_weights(self, module_results: Dict[str, ModuleResult]) -> Dict[str, float]:
        """
        Her modül için dinamik ağırlık hesapla
        Arkadaşın uncertainty-aware ağırlıklandırma algoritması
        """
        weights = {}
        total_weight = 0.0
        
        for module_name, result in module_results.items():
            # Base weight (varsayılan veya yapılandırılmış)
            base_weight = self.base_weights.get(module_name, 1.0)
            
            # Uncertainty penalty
            uncertainty_factor = 1.0 - (result.uncertainty * self.uncertainty_penalty)
            
            # Confidence bonus
            confidence_bonus = 1.0
            if result.confidence_level == "HIGH":
                confidence_bonus = 1.2
            elif result.confidence_level == "MEDIUM":
                confidence_bonus = 1.0
            else:  # LOW
                confidence_bonus = 0.7
            
            # Performance factor (geçmiş başarı oranı)
            performance_factor = self.get_module_performance(module_name)
            
            # Final weight calculation
            final_weight = base_weight * uncertainty_factor * confidence_bonus * performance_factor
            
            # Minimum weight guarantee (arkadaşın zorunlu katkı prensibi)
            final_weight = max(final_weight, 0.02)  # En az %2 ağırlık
            
            weights[module_name] = final_weight
            total_weight += final_weight
        
        # Normalize weights
        if total_weight > 0:
            weights = {k: v / total_weight for k, v in weights.items()}
        
        return weights
    
    def get_module_performance(self, module_name: str) -> float:
        """Modülün geçmiş performans faktörü"""
        # Bu gerçek uygulamada geçmiş tahmin başarı oranları ile hesaplanacak
        # Şimdilik varsayılan değer döndürüyoruz
        default_performance = {
            "Ultra Astrology Analysis": 0.85,
            "Ultra Technical Analysis": 0.92,
            "Ultra Sentiment Analysis": 0.78,
            "Ultra Financial Analysis": 0.88,
            "Ultra Risk Assessment": 0.90,
            "Quantum Ultra Analysis": 0.75,  # Yeni modül
            "Consciousness Ultra Analysis": 0.70,  # Yeni modül
            "Energy Ultra Analysis": 0.72  # Yeni modül
        }
        return default_performance.get(module_name, 0.80)
    
    def analyze_consensus_strength(self, module_results: Dict[str, ModuleResult]) -> float:
        """Modüller arası konsensüs gücünü analiz et"""
        scores = [result.score for result in module_results.values()]
        
        if len(scores) < 2:
            return 1.0
        
        # Standard deviation - düşük olursa yüksek konsensüs
        score_std = np.std(scores)
        max_possible_std = 50.0  # 0-100 aralığında max std
        
        # Konsensüs gücü (1 - normalize edilmiş std)
        consensus = 1.0 - min(score_std / max_possible_std, 1.0)
        
        return consensus
    
    def identify_conflicting_signals(self, module_results: Dict[str, ModuleResult]) -> List[str]:
        """Çelişkili sinyalleri tespit et"""
        conflicts = []
        
        bull_modules = []
        bear_modules = []
        neutral_modules = []
        
        for name, result in module_results.items():
            if result.score > 65:
                bull_modules.append(name)
            elif result.score < 35:
                bear_modules.append(name)
            else:
                neutral_modules.append(name)
        
        # Çelişki analizi
        if len(bull_modules) > 0 and len(bear_modules) > 0:
            conflicts.append(f"Directional conflict: {len(bull_modules)} bullish vs {len(bear_modules)} bearish modules")
        
        # High uncertainty modules
        high_uncertainty = [name for name, result in module_results.items() if result.uncertainty > 0.7]
        if len(high_uncertainty) > len(module_results) * 0.3:
            conflicts.append(f"High uncertainty in {len(high_uncertainty)} modules: {high_uncertainty}")
        
        return conflicts
    
    def extract_risk_and_opportunities(self, module_results: Dict[str, ModuleResult]) -> Tuple[List[str], List[str]]:
        """Risk faktörleri ve fırsatları çıkar"""
        risks = []
        opportunities = []
        
        for name, result in module_results.items():
            for signal_type in result.type:
                # Risk patterns
                if any(risk_word in signal_type.lower() for risk_word in 
                      ['risk', 'warning', 'danger', 'negative', 'bearish', 'decline', 'crash']):
                    risks.append(f"{name}: {signal_type}")
                
                # Opportunity patterns
                elif any(opp_word in signal_type.lower() for opp_word in 
                        ['opportunity', 'bullish', 'positive', 'growth', 'breakthrough', 'surge']):
                    opportunities.append(f"{name}: {signal_type}")
        
        return risks, opportunities
    
    def generate_explanation(self, ensemble_result: EnsembleResult, weights: Dict[str, float]) -> str:
        """Detaylı açıklama üret (XAI)"""
        explanation_parts = []
        
        # Ana sinyal
        explanation_parts.append(f"Final Signal: {ensemble_result.signal} (Score: {ensemble_result.final_score:.1f}/100)")
        
        # Top 3 contributors
        top_contributors = sorted(ensemble_result.module_contributions.items(), 
                                key=lambda x: abs(x[1]), reverse=True)[:3]
        
        explanation_parts.append("Top Contributors:")
        for module, contribution in top_contributors:
            module_result = ensemble_result.module_results[module]
            explanation_parts.append(f"  • {module}: {contribution:+.1f} points ({module_result['explanation']})")
        
        # Consensus info
        explanation_parts.append(f"Consensus Strength: {ensemble_result.consensus_strength:.1%}")
        explanation_parts.append(f"Average Uncertainty: {ensemble_result.average_uncertainty:.1%}")
        
        # Risks and opportunities
        if ensemble_result.risk_factors:
            explanation_parts.append(f"Key Risks: {'; '.join(ensemble_result.risk_factors[:2])}")
        
        if ensemble_result.opportunity_factors:
            explanation_parts.append(f"Key Opportunities: {'; '.join(ensemble_result.opportunity_factors[:2])}")
        
        return " | ".join(explanation_parts)
    
    def run_ensemble_analysis(self, raw_data: Dict[str, Any]) -> EnsembleResult:
        """
        Ana ensemble analizi - tüm modülleri çalıştırıp birleştirir
        Arkadaşın Multi-Expert Engine yaklaşımının uygulanması
        """
        logger.info(f"Starting ensemble analysis for {raw_data.get('symbol', 'Unknown')}")
        
        # 1. Tüm modülleri çalıştır
        module_results = {}
        for module_name, module in self.registry.modules.items():
            try:
                result = module.run_safe_inference(raw_data)
                module_results[module_name] = result
                logger.debug(f"{module_name}: Score={result.score:.2f}, Uncertainty={result.uncertainty:.3f}")
            except Exception as e:
                logger.error(f"Error running module {module_name}: {str(e)}")
                # Fallback result oluştur
                fallback = ModuleResult(
                    score=50.0, uncertainty=1.0, type=["error"], 
                    explanation=f"Module error: {str(e)}", timestamp="", 
                    confidence_level="LOW", contributing_factors={}
                )
                module_results[module_name] = fallback
        
        # 2. Dynamic weights hesapla
        weights = self.calculate_dynamic_weights(module_results)
        
        # 3. Weighted average score hesapla
        total_weighted_score = 0.0
        total_contribution = 0.0
        module_contributions = {}
        
        for module_name, result in module_results.items():
            weight = weights[module_name]
            contribution = result.score * weight
            total_weighted_score += contribution
            total_contribution += weight
            module_contributions[module_name] = contribution
        
        final_score = total_weighted_score / total_contribution if total_contribution > 0 else 50.0
        
        # 4. Signal belirleme
        if final_score >= self.buy_threshold:
            signal = "BUY"
        elif final_score <= self.sell_threshold:
            signal = "SELL"
        else:
            signal = "HOLD"
        
        # 5. Meta analizler
        consensus_strength = self.analyze_consensus_strength(module_results)
        conflicting_signals = self.identify_conflicting_signals(module_results)
        risks, opportunities = self.extract_risk_and_opportunities(module_results)
        
        # 6. İstatistikler
        uncertainties = [result.uncertainty for result in module_results.values()]
        average_uncertainty = np.mean(uncertainties)
        confidence = 1.0 - average_uncertainty  # Genel güven seviyesi
        
        # 7. Top drivers
        top_drivers = []
        sorted_contributions = sorted(module_contributions.items(), 
                                    key=lambda x: abs(x[1]), reverse=True)
        
        for module_name, contribution in sorted_contributions[:5]:
            result = module_results[module_name]
            top_drivers.append({
                "module": module_name,
                "contribution": contribution,
                "score": result.score,
                "uncertainty": result.uncertainty,
                "explanation": result.explanation
            })
        
        # 8. Final result
        ensemble_result = EnsembleResult(
            final_score=round(final_score, 2),
            signal=signal,
            confidence=round(confidence, 3),
            explanation="",  # Aşağıda doldurulacak
            timestamp=datetime.now().isoformat(),
            module_contributions=module_contributions,
            module_results={name: result.to_dict() for name, result in module_results.items()},
            top_drivers=top_drivers,
            risk_factors=risks,
            opportunity_factors=opportunities,
            total_modules_used=len(module_results),
            average_uncertainty=round(average_uncertainty, 3),
            consensus_strength=round(consensus_strength, 3),
            conflicting_signals=conflicting_signals
        )
        
        # 9. Açıklama üret
        ensemble_result.explanation = self.generate_explanation(ensemble_result, weights)
        
        # 10. Geçmişe kaydet
        self.prediction_history.append({
            "timestamp": ensemble_result.timestamp,
            "symbol": raw_data.get("symbol"),
            "final_score": final_score,
            "signal": signal,
            "confidence": confidence
        })
        
        logger.info(f"Ensemble analysis completed: {signal} ({final_score:.2f}) with {confidence:.1%} confidence")
        
        return ensemble_result
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Ensemble performans özeti"""
        if not self.prediction_history:
            return {"status": "No predictions yet"}
        
        recent_predictions = self.prediction_history[-100:]  # Son 100 tahmin
        
        signals = [p["signal"] for p in recent_predictions]
        confidences = [p["confidence"] for p in recent_predictions]
        
        return {
            "total_predictions": len(self.prediction_history),
            "recent_predictions": len(recent_predictions),
            "signal_distribution": {
                "BUY": signals.count("BUY"),
                "HOLD": signals.count("HOLD"), 
                "SELL": signals.count("SELL")
            },
            "average_confidence": round(np.mean(confidences), 3),
            "high_confidence_ratio": len([c for c in confidences if c > 0.7]) / len(confidences),
            "registered_modules": len(self.registry.modules)
        }

def create_consensus_engine(config: Dict[str, Any] = None) -> ConsensusEngine:
    """Consensus Engine factory"""
    config = config or {}
    
    # Default weights (arkadaşın önerisine göre ayarlanabilir)
    default_weights = {
        "Ultra Technical Analysis": 1.2,  # Teknik analiz güçlü
        "Ultra Financial Analysis": 1.1,  # Temel analiz önemli
        "Ultra Sentiment Analysis": 0.9,  # Duygu analizi destekleyici
        "Ultra Astrology Analysis": 0.8,  # Astroloji alternatif görüş
        "Ultra Risk Assessment": 1.3,     # Risk analizi kritik
        "Quantum Ultra Analysis": 0.7,    # Yeni, deneysel
        "Consciousness Ultra Analysis": 0.6,  # Çok yeni
        "Energy Ultra Analysis": 0.6      # Çok yeni
    }
    
    base_weights = config.get("base_weights", default_weights)
    
    engine = ConsensusEngine(base_weights)
    
    # Konfigürasyon ayarları
    if "buy_threshold" in config:
        engine.buy_threshold = config["buy_threshold"]
    if "sell_threshold" in config:
        engine.sell_threshold = config["sell_threshold"]
    if "uncertainty_penalty" in config:
        engine.uncertainty_penalty = config["uncertainty_penalty"]
    
    return engine

if __name__ == "__main__":
    print("⚖️ CONSENSUS ENGINE - UNCERTAINTY-AWARE ENSEMBLE")
    print("="*60)
    
    # Test consensus engine
    engine = create_consensus_engine()
    
    print(f"✅ ConsensusEngine created")
    print(f"✅ Dynamic weight calculation implemented")
    print(f"✅ Uncertainty-aware ensemble ready")
    print(f"✅ Conflict detection system active")
    print(f"✅ XAI explanation generation ready")
    
    print(f"\n🎯 Buy Threshold: {engine.buy_threshold}")
    print(f"🎯 Sell Threshold: {engine.sell_threshold}")
    print(f"📊 Registered modules: {len(engine.registry.modules)}")
    
    print(f"\n🚀 Ready for multi-expert ensemble analysis!")