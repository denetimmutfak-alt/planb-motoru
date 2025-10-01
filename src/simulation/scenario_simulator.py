"""
PlanB Motoru - Scenario Simulator
Portföy etki analizi ve senaryo simülasyonu
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug
from src.portfolio.portfolio_manager import portfolio_manager

class ScenarioSimulator:
    """Senaryo simülatörü"""
    
    def __init__(self):
        self.portfolio_manager = portfolio_manager
        self.scenarios = {
            'market_crash': {
                'name': 'Piyasa Çöküşü',
                'description': 'Genel piyasa %20-50 düşüş',
                'market_impact': -0.3,
                'sector_impacts': {
                    'technology': -0.4,
                    'finance': -0.5,
                    'healthcare': -0.2,
                    'energy': -0.6,
                    'consumer': -0.3,
                    'utilities': -0.1
                }
            },
            'inflation_spike': {
                'name': 'Enflasyon Artışı',
                'description': 'Yüksek enflasyon senaryosu',
                'market_impact': -0.15,
                'sector_impacts': {
                    'technology': -0.3,
                    'finance': -0.2,
                    'healthcare': -0.1,
                    'energy': 0.2,
                    'consumer': -0.25,
                    'utilities': 0.1
                }
            },
            'interest_rate_hike': {
                'name': 'Faiz Artışı',
                'description': 'Merkez bankası faiz artışı',
                'market_impact': -0.2,
                'sector_impacts': {
                    'technology': -0.4,
                    'finance': 0.1,
                    'healthcare': -0.15,
                    'energy': -0.1,
                    'consumer': -0.3,
                    'utilities': -0.2
                }
            },
            'tech_boom': {
                'name': 'Teknoloji Patlaması',
                'description': 'Teknoloji sektörü yükselişi',
                'market_impact': 0.1,
                'sector_impacts': {
                    'technology': 0.4,
                    'finance': 0.05,
                    'healthcare': 0.1,
                    'energy': -0.05,
                    'consumer': 0.15,
                    'utilities': 0.0
                }
            },
            'crypto_crash': {
                'name': 'Kripto Çöküşü',
                'description': 'Kripto para piyasası çöküşü',
                'market_impact': -0.05,
                'sector_impacts': {
                    'technology': -0.1,
                    'finance': -0.05,
                    'healthcare': 0.0,
                    'energy': 0.0,
                    'consumer': 0.0,
                    'utilities': 0.0
                },
                'crypto_impact': -0.7
            },
            'gold_rush': {
                'name': 'Altın Patlaması',
                'description': 'Altın ve değerli metaller yükselişi',
                'market_impact': 0.05,
                'sector_impacts': {
                    'technology': -0.1,
                    'finance': 0.0,
                    'healthcare': 0.0,
                    'energy': 0.0,
                    'consumer': 0.0,
                    'utilities': 0.0
                },
                'commodity_impact': 0.3
            }
        }
    
    def simulate_portfolio_scenario(self, portfolio_name: str, scenario_name: str, 
                                  custom_impacts: Dict[str, float] = None) -> Dict[str, Any]:
        """Portföy senaryo simülasyonu"""
        try:
            portfolio = self.portfolio_manager.get_portfolio(portfolio_name)
            if not portfolio:
                log_error(f"Portföy bulunamadı: {portfolio_name}")
                return {}
            
            scenario = self.scenarios.get(scenario_name)
            if not scenario:
                log_error(f"Senaryo bulunamadı: {scenario_name}")
                return {}
            
            # Mevcut portföy değeri
            current_value = portfolio.cash
            position_impacts = []
            
            for symbol, position in portfolio.positions.items():
                current_price = position['current_price']
                quantity = position['quantity']
                position_value = current_price * quantity
                
                # Sembol etkisini hesapla
                impact = self._calculate_symbol_impact(symbol, scenario, custom_impacts)
                new_price = current_price * (1 + impact)
                new_value = new_price * quantity
                value_change = new_value - position_value
                value_change_pct = (value_change / position_value * 100) if position_value > 0 else 0
                
                position_impacts.append({
                    'symbol': symbol,
                    'current_price': current_price,
                    'new_price': new_price,
                    'current_value': position_value,
                    'new_value': new_value,
                    'value_change': value_change,
                    'value_change_pct': value_change_pct,
                    'impact_factor': impact,
                    'quantity': quantity
                })
                
                current_value += new_value
            
            # Toplam etki
            total_current_value = portfolio.cash + sum(pos['current_value'] for pos in position_impacts)
            total_new_value = current_value
            total_change = total_new_value - total_current_value
            total_change_pct = (total_change / total_current_value * 100) if total_current_value > 0 else 0
            
            # Risk analizi
            risk_analysis = self._analyze_scenario_risk(position_impacts, scenario)
            
            return {
                'scenario_name': scenario['name'],
                'scenario_description': scenario['description'],
                'portfolio_name': portfolio_name,
                'simulation_date': datetime.now().isoformat(),
                'current_portfolio_value': total_current_value,
                'simulated_portfolio_value': total_new_value,
                'total_change': total_change,
                'total_change_pct': total_change_pct,
                'position_impacts': position_impacts,
                'risk_analysis': risk_analysis,
                'scenario_details': scenario
            }
            
        except Exception as e:
            log_error(f"Portföy senaryo simülasyonu hatası: {e}")
            return {}
    
    def simulate_custom_scenario(self, portfolio_name: str, scenario_data: Dict[str, Any]) -> Dict[str, Any]:
        """Özel senaryo simülasyonu"""
        try:
            portfolio = self.portfolio_manager.get_portfolio(portfolio_name)
            if not portfolio:
                log_error(f"Portföy bulunamadı: {portfolio_name}")
                return {}
            
            # Özel senaryo oluştur
            custom_scenario = {
                'name': scenario_data.get('name', 'Özel Senaryo'),
                'description': scenario_data.get('description', 'Kullanıcı tanımlı senaryo'),
                'market_impact': scenario_data.get('market_impact', 0.0),
                'sector_impacts': scenario_data.get('sector_impacts', {}),
                'symbol_impacts': scenario_data.get('symbol_impacts', {}),
                'crypto_impact': scenario_data.get('crypto_impact', 0.0),
                'commodity_impact': scenario_data.get('commodity_impact', 0.0)
            }
            
            # Simülasyonu çalıştır
            return self.simulate_portfolio_scenario(portfolio_name, 'custom', custom_scenario)
            
        except Exception as e:
            log_error(f"Özel senaryo simülasyonu hatası: {e}")
            return {}
    
    def compare_scenarios(self, portfolio_name: str, scenario_names: List[str]) -> Dict[str, Any]:
        """Birden fazla senaryoyu karşılaştır"""
        try:
            results = {}
            
            for scenario_name in scenario_names:
                result = self.simulate_portfolio_scenario(portfolio_name, scenario_name)
                if result:
                    results[scenario_name] = {
                        'scenario_name': result['scenario_name'],
                        'total_change_pct': result['total_change_pct'],
                        'total_change': result['total_change'],
                        'simulated_value': result['simulated_portfolio_value'],
                        'risk_score': result['risk_analysis'].get('overall_risk_score', 0)
                    }
            
            # En iyi ve en kötü senaryolar
            if results:
                best_scenario = max(results.items(), key=lambda x: x[1]['total_change_pct'])
                worst_scenario = min(results.items(), key=lambda x: x[1]['total_change_pct'])
                
                return {
                    'portfolio_name': portfolio_name,
                    'comparison_date': datetime.now().isoformat(),
                    'scenarios': results,
                    'best_scenario': {
                        'name': best_scenario[0],
                        'change_pct': best_scenario[1]['total_change_pct'],
                        'change_value': best_scenario[1]['total_change']
                    },
                    'worst_scenario': {
                        'name': worst_scenario[0],
                        'change_pct': worst_scenario[1]['total_change_pct'],
                        'change_value': worst_scenario[1]['total_change']
                    },
                    'scenario_count': len(results)
                }
            
            return {}
            
        except Exception as e:
            log_error(f"Senaryo karşılaştırma hatası: {e}")
            return {}
    
    def stress_test_portfolio(self, portfolio_name: str) -> Dict[str, Any]:
        """Portföy stres testi"""
        try:
            # Tüm senaryoları test et
            all_scenarios = list(self.scenarios.keys())
            comparison_result = self.compare_scenarios(portfolio_name, all_scenarios)
            
            if not comparison_result:
                return {}
            
            # Stres testi metrikleri
            scenario_changes = [scenario['total_change_pct'] for scenario in comparison_result['scenarios'].values()]
            
            stress_metrics = {
                'max_loss_pct': min(scenario_changes),
                'max_gain_pct': max(scenario_changes),
                'average_change_pct': np.mean(scenario_changes),
                'volatility': np.std(scenario_changes),
                'downside_risk': np.mean([change for change in scenario_changes if change < 0]),
                'upside_potential': np.mean([change for change in scenario_changes if change > 0])
            }
            
            # Risk seviyesi belirleme
            if stress_metrics['max_loss_pct'] < -20:
                risk_level = 'Yüksek Risk'
            elif stress_metrics['max_loss_pct'] < -10:
                risk_level = 'Orta Risk'
            else:
                risk_level = 'Düşük Risk'
            
            return {
                'portfolio_name': portfolio_name,
                'stress_test_date': datetime.now().isoformat(),
                'stress_metrics': stress_metrics,
                'risk_level': risk_level,
                'scenario_results': comparison_result['scenarios'],
                'recommendations': self._generate_stress_test_recommendations(stress_metrics)
            }
            
        except Exception as e:
            log_error(f"Stres testi hatası: {e}")
            return {}
    
    def _calculate_symbol_impact(self, symbol: str, scenario: Dict[str, Any], 
                               custom_impacts: Dict[str, float] = None) -> float:
        """Sembol etkisini hesapla"""
        try:
            # Özel etkiler varsa kullan
            if custom_impacts and symbol in custom_impacts:
                return custom_impacts[symbol]
            
            # Senaryo etkilerini uygula
            base_impact = scenario.get('market_impact', 0.0)
            
            # Sektör etkisi
            sector = self._get_symbol_sector(symbol)
            sector_impact = scenario.get('sector_impacts', {}).get(sector, 0.0)
            
            # Kripto etkisi
            if self._is_crypto_symbol(symbol):
                crypto_impact = scenario.get('crypto_impact', 0.0)
                return crypto_impact
            
            # Emtia etkisi
            if self._is_commodity_symbol(symbol):
                commodity_impact = scenario.get('commodity_impact', 0.0)
                return commodity_impact
            
            # Toplam etki (sektör + genel piyasa)
            total_impact = base_impact + (sector_impact * 0.7)  # Sektör etkisini %70 ağırlıkla
            
            return total_impact
            
        except Exception as e:
            log_error(f"Sembol etki hesaplama hatası: {e}")
            return 0.0
    
    def _get_symbol_sector(self, symbol: str) -> str:
        """Sembol sektörünü belirle"""
        try:
            # Basit sektör eşleştirmesi
            sector_mapping = {
                # Teknoloji
                'AAPL': 'technology', 'MSFT': 'technology', 'GOOGL': 'technology',
                'AMZN': 'technology', 'META': 'technology', 'NVDA': 'technology',
                'TSLA': 'technology', 'NFLX': 'technology',
                
                # Finans
                'JPM': 'finance', 'BAC': 'finance', 'WFC': 'finance',
                'GS': 'finance', 'MS': 'finance',
                
                # Sağlık
                'JNJ': 'healthcare', 'PFE': 'healthcare', 'UNH': 'healthcare',
                'ABBV': 'healthcare', 'LLY': 'healthcare',
                
                # Enerji
                'XOM': 'energy', 'CVX': 'energy', 'SHEL': 'energy', 'BP': 'energy',
                
                # Tüketici
                'WMT': 'consumer', 'HD': 'consumer', 'MCD': 'consumer',
                'NKE': 'consumer', 'KO': 'consumer', 'PEP': 'consumer',
                
                # BIST
                'THYAO.IS': 'technology', 'AKBNK.IS': 'finance', 'GARAN.IS': 'finance',
                'ISCTR.IS': 'finance', 'SAHOL.IS': 'consumer', 'TUPRS.IS': 'energy',
                'KRDMD.IS': 'energy', 'SASA.IS': 'consumer'
            }
            
            return sector_mapping.get(symbol, 'other')
            
        except Exception as e:
            return 'other'
    
    def _is_crypto_symbol(self, symbol: str) -> bool:
        """Kripto sembol mü kontrol et"""
        crypto_symbols = ['BTC', 'ETH', 'ADA', 'DOT', 'SOL', 'AVAX', 'MATIC', 'ATOM', 'XRP']
        return symbol in crypto_symbols
    
    def _is_commodity_symbol(self, symbol: str) -> bool:
        """Emtia sembol mü kontrol et"""
        commodity_symbols = ['GOLD', 'SILVER', 'OIL', 'GAS']
        return symbol in commodity_symbols
    
    def _analyze_scenario_risk(self, position_impacts: List[Dict[str, Any]], 
                             scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Senaryo risk analizi"""
        try:
            if not position_impacts:
                return {}
            
            # Pozisyon etkilerini analiz et
            impacts = [pos['value_change_pct'] for pos in position_impacts]
            values = [pos['current_value'] for pos in position_impacts]
            
            # Risk metrikleri
            max_loss = min(impacts)
            max_gain = max(impacts)
            avg_impact = np.mean(impacts)
            impact_volatility = np.std(impacts)
            
            # Ağırlıklı risk (büyük pozisyonlar daha önemli)
            weighted_impacts = [impact * value for impact, value in zip(impacts, values)]
            total_value = sum(values)
            weighted_avg_impact = sum(weighted_impacts) / total_value if total_value > 0 else 0
            
            # Risk seviyesi
            if max_loss < -20 or impact_volatility > 15:
                risk_level = 'Yüksek'
            elif max_loss < -10 or impact_volatility > 10:
                risk_level = 'Orta'
            else:
                risk_level = 'Düşük'
            
            return {
                'max_loss_pct': max_loss,
                'max_gain_pct': max_gain,
                'average_impact_pct': avg_impact,
                'weighted_avg_impact_pct': weighted_avg_impact,
                'impact_volatility': impact_volatility,
                'risk_level': risk_level,
                'overall_risk_score': abs(weighted_avg_impact) + impact_volatility,
                'scenario_severity': abs(scenario.get('market_impact', 0)) * 100
            }
            
        except Exception as e:
            log_error(f"Risk analizi hatası: {e}")
            return {}
    
    def _generate_stress_test_recommendations(self, stress_metrics: Dict[str, Any]) -> List[str]:
        """Stres testi önerileri oluştur"""
        try:
            recommendations = []
            
            if stress_metrics['max_loss_pct'] < -20:
                recommendations.append("Portföy yüksek risk altında. Çeşitlendirme artırılmalı.")
            
            if stress_metrics['volatility'] > 15:
                recommendations.append("Portföy volatilitesi yüksek. Daha stabil varlıklar eklenmeli.")
            
            if stress_metrics['downside_risk'] < -10:
                recommendations.append("Düşüş riski yüksek. Koruyucu pozisyonlar düşünülmeli.")
            
            if stress_metrics['upside_potential'] > 20:
                recommendations.append("Yükseliş potansiyeli yüksek. Risk toleransına göre pozisyon artırılabilir.")
            
            if not recommendations:
                recommendations.append("Portföy dengeli görünüyor. Mevcut strateji devam ettirilebilir.")
            
            return recommendations
            
        except Exception as e:
            return ["Stres testi önerileri oluşturulamadı."]
    
    def get_available_scenarios(self) -> Dict[str, Dict[str, Any]]:
        """Mevcut senaryoları getir"""
        try:
            return {
                scenario_id: {
                    'id': scenario_id,
                    'name': scenario['name'],
                    'description': scenario['description'],
                    'market_impact': scenario.get('market_impact', 0.0)
                }
                for scenario_id, scenario in self.scenarios.items()
            }
        except Exception as e:
            log_error(f"Senaryo listesi alma hatası: {e}")
            return {}
    
    def create_custom_scenario(self, scenario_data: Dict[str, Any]) -> str:
        """Özel senaryo oluştur"""
        try:
            scenario_id = f"custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            custom_scenario = {
                'name': scenario_data.get('name', 'Özel Senaryo'),
                'description': scenario_data.get('description', 'Kullanıcı tanımlı senaryo'),
                'market_impact': scenario_data.get('market_impact', 0.0),
                'sector_impacts': scenario_data.get('sector_impacts', {}),
                'symbol_impacts': scenario_data.get('symbol_impacts', {}),
                'crypto_impact': scenario_data.get('crypto_impact', 0.0),
                'commodity_impact': scenario_data.get('commodity_impact', 0.0),
                'created_at': datetime.now().isoformat(),
                'is_custom': True
            }
            
            self.scenarios[scenario_id] = custom_scenario
            
            log_info(f"Özel senaryo oluşturuldu: {scenario_id}")
            return scenario_id
            
        except Exception as e:
            log_error(f"Özel senaryo oluşturma hatası: {e}")
            return ""

# Global scenario simulator instance
scenario_simulator = ScenarioSimulator()

