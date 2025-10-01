"""
PlanB Motoru - Macro Data Integration
Makro veri entegrasyonu (iklim, jeopolitik, ekonomik)
"""
import requests
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug

class MacroDataIntegration:
    """Makro veri entegrasyonu"""
    
    def __init__(self):
        self.data_directory = "data/macro"
        self._ensure_directories()
        
        # API endpoints (simüle edilmiş)
        self.api_endpoints = {
            'climate': 'https://api.climate-data.org/v1',
            'geopolitical': 'https://api.geopolitical-risk.org/v1',
            'economic': 'https://api.economic-indicators.org/v1',
            'commodity': 'https://api.commodity-prices.org/v1'
        }
        
        # Veri cache
        self.cache = {}
        self.cache_ttl = {}
    
    def _ensure_directories(self):
        """Gerekli dizinleri oluştur"""
        os.makedirs(self.data_directory, exist_ok=True)
        os.makedirs(f"{self.data_directory}/climate", exist_ok=True)
        os.makedirs(f"{self.data_directory}/geopolitical", exist_ok=True)
        os.makedirs(f"{self.data_directory}/economic", exist_ok=True)
        os.makedirs(f"{self.data_directory}/commodity", exist_ok=True)
    
    def get_climate_data(self, region: str = 'global') -> Dict[str, Any]:
        """İklim verilerini getir"""
        try:
            # Cache kontrolü
            cache_key = f"climate_{region}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            # Simüle edilmiş iklim verileri
            climate_data = {
                'region': region,
                'temperature_anomaly': np.random.uniform(-2, 2),  # °C
                'precipitation_change': np.random.uniform(-20, 20),  # %
                'sea_level_rise': np.random.uniform(0, 5),  # mm/year
                'extreme_weather_events': {
                    'hurricanes': np.random.randint(0, 5),
                    'droughts': np.random.randint(0, 3),
                    'floods': np.random.randint(0, 4),
                    'heatwaves': np.random.randint(0, 6)
                },
                'carbon_emissions': {
                    'total_emissions': np.random.uniform(30, 50),  # Gt CO2/year
                    'emissions_change': np.random.uniform(-5, 5),  # %
                    'renewable_share': np.random.uniform(20, 40)  # %
                },
                'agricultural_impact': {
                    'crop_yield_change': np.random.uniform(-10, 5),  # %
                    'water_stress_index': np.random.uniform(0, 100),
                    'soil_quality_index': np.random.uniform(60, 90)
                },
                'energy_impact': {
                    'renewable_capacity': np.random.uniform(2000, 4000),  # GW
                    'fossil_fuel_demand': np.random.uniform(-5, 2),  # %
                    'energy_efficiency': np.random.uniform(1, 3)  # % improvement
                },
                'updated_at': datetime.now().isoformat()
            }
            
            # Cache'e kaydet
            self._cache_data(cache_key, climate_data, 3600)  # 1 saat
            
            log_info(f"İklim verileri alındı: {region}")
            return climate_data
            
        except Exception as e:
            log_error(f"İklim verisi alma hatası: {e}")
            return {}
    
    def get_geopolitical_data(self, region: str = 'global') -> Dict[str, Any]:
        """Jeopolitik verilerini getir"""
        try:
            # Cache kontrolü
            cache_key = f"geopolitical_{region}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            # Simüle edilmiş jeopolitik veriler
            geopolitical_data = {
                'region': region,
                'political_stability_index': np.random.uniform(0, 100),
                'conflict_risk': np.random.uniform(0, 100),
                'trade_tensions': {
                    'us_china': np.random.uniform(0, 100),
                    'eu_uk': np.random.uniform(0, 100),
                    'middle_east': np.random.uniform(0, 100)
                },
                'sanctions_impact': {
                    'active_sanctions': np.random.randint(0, 10),
                    'economic_impact': np.random.uniform(-5, 0),  # %
                    'affected_sectors': ['energy', 'technology', 'finance']
                },
                'currency_volatility': {
                    'usd_index': np.random.uniform(90, 110),
                    'euro_volatility': np.random.uniform(5, 20),  # %
                    'emerging_markets_volatility': np.random.uniform(10, 30)  # %
                },
                'energy_security': {
                    'oil_supply_risk': np.random.uniform(0, 100),
                    'gas_supply_risk': np.random.uniform(0, 100),
                    'renewable_adoption': np.random.uniform(20, 50)  # %
                },
                'regulatory_changes': {
                    'new_regulations': np.random.randint(0, 5),
                    'compliance_cost': np.random.uniform(0, 10),  # %
                    'affected_industries': ['finance', 'technology', 'energy']
                },
                'updated_at': datetime.now().isoformat()
            }
            
            # Cache'e kaydet
            self._cache_data(cache_key, geopolitical_data, 1800)  # 30 dakika
            
            log_info(f"Jeopolitik veriler alındı: {region}")
            return geopolitical_data
            
        except Exception as e:
            log_error(f"Jeopolitik veri alma hatası: {e}")
            return {}
    
    def get_economic_indicators(self, country: str = 'global') -> Dict[str, Any]:
        """Ekonomik göstergeleri getir"""
        try:
            # Cache kontrolü
            cache_key = f"economic_{country}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            # Simüle edilmiş ekonomik veriler
            economic_data = {
                'country': country,
                'gdp_growth': np.random.uniform(-2, 5),  # %
                'inflation_rate': np.random.uniform(1, 8),  # %
                'unemployment_rate': np.random.uniform(3, 12),  # %
                'interest_rates': {
                    'central_bank_rate': np.random.uniform(0, 6),  # %
                    '10_year_bond': np.random.uniform(1, 8),  # %
                    'mortgage_rate': np.random.uniform(2, 10)  # %
                },
                'fiscal_policy': {
                    'debt_to_gdp': np.random.uniform(30, 120),  # %
                    'budget_deficit': np.random.uniform(-5, 10),  # %
                    'tax_rate': np.random.uniform(20, 40)  # %
                },
                'monetary_policy': {
                    'money_supply_growth': np.random.uniform(2, 15),  # %
                    'credit_growth': np.random.uniform(-5, 20),  # %
                    'liquidity_ratio': np.random.uniform(10, 30)  # %
                },
                'trade_balance': {
                    'exports': np.random.uniform(-10, 20),  # % change
                    'imports': np.random.uniform(-5, 15),  # % change
                    'trade_deficit': np.random.uniform(-100, 100)  # billion
                },
                'consumer_confidence': {
                    'consumer_sentiment': np.random.uniform(50, 120),
                    'retail_sales': np.random.uniform(-5, 10),  # %
                    'housing_starts': np.random.uniform(-20, 30)  # %
                },
                'updated_at': datetime.now().isoformat()
            }
            
            # Cache'e kaydet
            self._cache_data(cache_key, economic_data, 1800)  # 30 dakika
            
            log_info(f"Ekonomik göstergeler alındı: {country}")
            return economic_data
            
        except Exception as e:
            log_error(f"Ekonomik veri alma hatası: {e}")
            return {}
    
    def get_commodity_data(self, commodity_type: str = 'all') -> Dict[str, Any]:
        """Emtia verilerini getir"""
        try:
            # Cache kontrolü
            cache_key = f"commodity_{commodity_type}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                return cached_data
            
            # Simüle edilmiş emtia verileri
            commodity_data = {
                'commodity_type': commodity_type,
                'energy': {
                    'crude_oil': {
                        'price': np.random.uniform(60, 120),  # USD/barrel
                        'change_pct': np.random.uniform(-10, 10),
                        'supply_demand': np.random.uniform(0, 100)
                    },
                    'natural_gas': {
                        'price': np.random.uniform(2, 8),  # USD/MMBtu
                        'change_pct': np.random.uniform(-15, 15),
                        'storage_levels': np.random.uniform(50, 100)
                    },
                    'coal': {
                        'price': np.random.uniform(50, 150),  # USD/ton
                        'change_pct': np.random.uniform(-20, 20),
                        'production': np.random.uniform(80, 120)
                    }
                },
                'metals': {
                    'gold': {
                        'price': np.random.uniform(1600, 2200),  # USD/oz
                        'change_pct': np.random.uniform(-5, 5),
                        'demand': np.random.uniform(80, 120)
                    },
                    'silver': {
                        'price': np.random.uniform(20, 35),  # USD/oz
                        'change_pct': np.random.uniform(-10, 10),
                        'industrial_demand': np.random.uniform(70, 130)
                    },
                    'copper': {
                        'price': np.random.uniform(3, 5),  # USD/lb
                        'change_pct': np.random.uniform(-15, 15),
                        'supply_chain': np.random.uniform(0, 100)
                    }
                },
                'agriculture': {
                    'wheat': {
                        'price': np.random.uniform(200, 400),  # USD/ton
                        'change_pct': np.random.uniform(-20, 20),
                        'yield': np.random.uniform(80, 120)
                    },
                    'corn': {
                        'price': np.random.uniform(150, 300),  # USD/ton
                        'change_pct': np.random.uniform(-25, 25),
                        'ethanol_demand': np.random.uniform(70, 130)
                    },
                    'soybeans': {
                        'price': np.random.uniform(300, 600),  # USD/ton
                        'change_pct': np.random.uniform(-20, 20),
                        'export_demand': np.random.uniform(80, 120)
                    }
                },
                'updated_at': datetime.now().isoformat()
            }
            
            # Cache'e kaydet
            self._cache_data(cache_key, commodity_data, 900)  # 15 dakika
            
            log_info(f"Emtia verileri alındı: {commodity_type}")
            return commodity_data
            
        except Exception as e:
            log_error(f"Emtia veri alma hatası: {e}")
            return {}
    
    def analyze_macro_impact(self, symbol: str, market: str = 'bist') -> Dict[str, Any]:
        """Makro verilerin sembol üzerindeki etkisini analiz et"""
        try:
            # Tüm makro verileri al
            climate_data = self.get_climate_data()
            geopolitical_data = self.get_geopolitical_data()
            economic_data = self.get_economic_indicators()
            commodity_data = self.get_commodity_data()
            
            # Sembol analizi
            impact_analysis = {
                'symbol': symbol,
                'market': market,
                'analysis_date': datetime.now().isoformat(),
                'climate_impact': self._analyze_climate_impact(symbol, climate_data),
                'geopolitical_impact': self._analyze_geopolitical_impact(symbol, geopolitical_data),
                'economic_impact': self._analyze_economic_impact(symbol, economic_data),
                'commodity_impact': self._analyze_commodity_impact(symbol, commodity_data),
                'overall_impact': {}
            }
            
            # Genel etki hesapla
            impact_analysis['overall_impact'] = self._calculate_overall_impact(impact_analysis)
            
            log_info(f"Makro etki analizi tamamlandı: {symbol}")
            return impact_analysis
            
        except Exception as e:
            log_error(f"Makro etki analizi hatası: {e}")
            return {}
    
    def _analyze_climate_impact(self, symbol: str, climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """İklim etkisini analiz et"""
        try:
            impact_score = 0
            impact_factors = []
            
            # Sektör bazlı etki
            sector = self._get_symbol_sector(symbol)
            
            if sector == 'energy':
                # Enerji sektörü için iklim etkisi
                renewable_share = climate_data.get('carbon_emissions', {}).get('renewable_share', 0)
                if renewable_share > 30:
                    impact_score += 10
                    impact_factors.append("Yenilenebilir enerji artışı pozitif etki")
                else:
                    impact_score -= 5
                    impact_factors.append("Fosil yakıt bağımlılığı risk")
            
            elif sector == 'agriculture':
                # Tarım sektörü için iklim etkisi
                crop_yield = climate_data.get('agricultural_impact', {}).get('crop_yield_change', 0)
                if crop_yield < -5:
                    impact_score -= 15
                    impact_factors.append("Mahsul verimi düşüşü negatif etki")
                elif crop_yield > 0:
                    impact_score += 5
                    impact_factors.append("Mahsul verimi artışı pozitif etki")
            
            elif sector == 'technology':
                # Teknoloji sektörü için iklim etkisi
                energy_efficiency = climate_data.get('energy_impact', {}).get('energy_efficiency', 0)
                if energy_efficiency > 2:
                    impact_score += 8
                    impact_factors.append("Enerji verimliliği artışı pozitif etki")
            
            return {
                'impact_score': impact_score,
                'impact_factors': impact_factors,
                'severity': 'high' if abs(impact_score) > 10 else ('medium' if abs(impact_score) > 5 else 'low')
            }
            
        except Exception as e:
            return {'impact_score': 0, 'impact_factors': [], 'severity': 'low'}
    
    def _analyze_geopolitical_impact(self, symbol: str, geopolitical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Jeopolitik etkisini analiz et"""
        try:
            impact_score = 0
            impact_factors = []
            
            # Sektör bazlı etki
            sector = self._get_symbol_sector(symbol)
            
            if sector == 'energy':
                # Enerji sektörü için jeopolitik etki
                oil_supply_risk = geopolitical_data.get('energy_security', {}).get('oil_supply_risk', 0)
                if oil_supply_risk > 70:
                    impact_score += 15
                    impact_factors.append("Petrol arz riski yüksek, fiyat artışı bekleniyor")
                elif oil_supply_risk < 30:
                    impact_score -= 5
                    impact_factors.append("Petrol arz güvenli, fiyat düşüşü riski")
            
            elif sector == 'technology':
                # Teknoloji sektörü için jeopolitik etki
                trade_tensions = geopolitical_data.get('trade_tensions', {}).get('us_china', 0)
                if trade_tensions > 70:
                    impact_score -= 10
                    impact_factors.append("ABD-Çin ticaret gerilimi negatif etki")
                elif trade_tensions < 30:
                    impact_score += 5
                    impact_factors.append("Ticaret gerilimi düşük, pozitif etki")
            
            elif sector == 'finance':
                # Finans sektörü için jeopolitik etki
                political_stability = geopolitical_data.get('political_stability_index', 0)
                if political_stability < 40:
                    impact_score -= 12
                    impact_factors.append("Politik istikrarsızlık finans sektörü için risk")
                elif political_stability > 80:
                    impact_score += 8
                    impact_factors.append("Politik istikrar finans sektörü için pozitif")
            
            return {
                'impact_score': impact_score,
                'impact_factors': impact_factors,
                'severity': 'high' if abs(impact_score) > 10 else ('medium' if abs(impact_score) > 5 else 'low')
            }
            
        except Exception as e:
            return {'impact_score': 0, 'impact_factors': [], 'severity': 'low'}
    
    def _analyze_economic_impact(self, symbol: str, economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ekonomik etkisini analiz et"""
        try:
            impact_score = 0
            impact_factors = []
            
            # Sektör bazlı etki
            sector = self._get_symbol_sector(symbol)
            
            # Genel ekonomik durum
            gdp_growth = economic_data.get('gdp_growth', 0)
            inflation_rate = economic_data.get('inflation_rate', 0)
            interest_rate = economic_data.get('interest_rates', {}).get('central_bank_rate', 0)
            
            if sector == 'finance':
                # Finans sektörü için ekonomik etki
                if interest_rate > 4:
                    impact_score += 10
                    impact_factors.append("Yüksek faiz oranları bankalar için pozitif")
                elif interest_rate < 1:
                    impact_score -= 5
                    impact_factors.append("Düşük faiz oranları bankalar için negatif")
                
                if gdp_growth > 3:
                    impact_score += 8
                    impact_factors.append("Güçlü GDP büyümesi kredi talebini artırır")
            
            elif sector == 'technology':
                # Teknoloji sektörü için ekonomik etki
                if gdp_growth > 2:
                    impact_score += 6
                    impact_factors.append("Ekonomik büyüme teknoloji yatırımlarını artırır")
                
                if inflation_rate > 5:
                    impact_score -= 8
                    impact_factors.append("Yüksek enflasyon teknoloji harcamalarını azaltır")
            
            elif sector == 'consumer':
                # Tüketici sektörü için ekonomik etki
                consumer_sentiment = economic_data.get('consumer_confidence', {}).get('consumer_sentiment', 0)
                if consumer_sentiment > 100:
                    impact_score += 12
                    impact_factors.append("Yüksek tüketici güveni harcamaları artırır")
                elif consumer_sentiment < 70:
                    impact_score -= 10
                    impact_factors.append("Düşük tüketici güveni harcamaları azaltır")
            
            return {
                'impact_score': impact_score,
                'impact_factors': impact_factors,
                'severity': 'high' if abs(impact_score) > 10 else ('medium' if abs(impact_score) > 5 else 'low')
            }
            
        except Exception as e:
            return {'impact_score': 0, 'impact_factors': [], 'severity': 'low'}
    
    def _analyze_commodity_impact(self, symbol: str, commodity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Emtia etkisini analiz et"""
        try:
            impact_score = 0
            impact_factors = []
            
            # Sembol türüne göre etki
            if self._is_energy_symbol(symbol):
                # Enerji sembolleri
                oil_price = commodity_data.get('energy', {}).get('crude_oil', {}).get('price', 0)
                if oil_price > 100:
                    impact_score += 15
                    impact_factors.append("Yüksek petrol fiyatları enerji şirketleri için pozitif")
                elif oil_price < 70:
                    impact_score -= 10
                    impact_factors.append("Düşük petrol fiyatları enerji şirketleri için negatif")
            
            elif self._is_metal_symbol(symbol):
                # Metal sembolleri
                gold_price = commodity_data.get('metals', {}).get('gold', {}).get('price', 0)
                if gold_price > 2000:
                    impact_score += 12
                    impact_factors.append("Yüksek altın fiyatları madencilik şirketleri için pozitif")
                elif gold_price < 1700:
                    impact_score -= 8
                    impact_factors.append("Düşük altın fiyatları madencilik şirketleri için negatif")
            
            elif self._is_agriculture_symbol(symbol):
                # Tarım sembolleri
                wheat_price = commodity_data.get('agriculture', {}).get('wheat', {}).get('price', 0)
                if wheat_price > 350:
                    impact_score += 10
                    impact_factors.append("Yüksek buğday fiyatları tarım şirketleri için pozitif")
                elif wheat_price < 250:
                    impact_score -= 6
                    impact_factors.append("Düşük buğday fiyatları tarım şirketleri için negatif")
            
            return {
                'impact_score': impact_score,
                'impact_factors': impact_factors,
                'severity': 'high' if abs(impact_score) > 10 else ('medium' if abs(impact_score) > 5 else 'low')
            }
            
        except Exception as e:
            return {'impact_score': 0, 'impact_factors': [], 'severity': 'low'}
    
    def _calculate_overall_impact(self, impact_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Genel etkiyi hesapla"""
        try:
            impacts = [
                impact_analysis.get('climate_impact', {}).get('impact_score', 0),
                impact_analysis.get('geopolitical_impact', {}).get('impact_score', 0),
                impact_analysis.get('economic_impact', {}).get('impact_score', 0),
                impact_analysis.get('commodity_impact', {}).get('impact_score', 0)
            ]
            
            overall_score = sum(impacts)
            
            # Risk seviyesi
            if overall_score > 20:
                risk_level = 'Yüksek Pozitif'
            elif overall_score > 10:
                risk_level = 'Orta Pozitif'
            elif overall_score > -10:
                risk_level = 'Nötr'
            elif overall_score > -20:
                risk_level = 'Orta Negatif'
            else:
                risk_level = 'Yüksek Negatif'
            
            return {
                'overall_score': overall_score,
                'risk_level': risk_level,
                'confidence': min(100, max(0, 100 - abs(overall_score))),
                'recommendation': self._generate_macro_recommendation(overall_score)
            }
            
        except Exception as e:
            return {'overall_score': 0, 'risk_level': 'Nötr', 'confidence': 50, 'recommendation': 'Veri yetersiz'}
    
    def _generate_macro_recommendation(self, overall_score: float) -> str:
        """Makro öneri oluştur"""
        if overall_score > 15:
            return "Güçlü pozitif makro faktörler. Pozisyon artırılabilir."
        elif overall_score > 5:
            return "Pozitif makro faktörler. Mevcut pozisyon korunabilir."
        elif overall_score > -5:
            return "Nötr makro faktörler. Dikkatli takip edilmeli."
        elif overall_score > -15:
            return "Negatif makro faktörler. Pozisyon azaltılabilir."
        else:
            return "Güçlü negatif makro faktörler. Pozisyon kapatılabilir."
    
    def _get_symbol_sector(self, symbol: str) -> str:
        """Sembol sektörünü belirle"""
        # Basit sektör eşleştirmesi (daha önce tanımlandı)
        sector_mapping = {
            'AAPL': 'technology', 'MSFT': 'technology', 'GOOGL': 'technology',
            'JPM': 'finance', 'BAC': 'finance', 'WFC': 'finance',
            'XOM': 'energy', 'CVX': 'energy', 'SHEL': 'energy',
            'WMT': 'consumer', 'HD': 'consumer', 'MCD': 'consumer',
            'THYAO.IS': 'technology', 'AKBNK.IS': 'finance', 'GARAN.IS': 'finance'
        }
        return sector_mapping.get(symbol, 'other')
    
    def _is_energy_symbol(self, symbol: str) -> bool:
        """Enerji sembolü mü kontrol et"""
        energy_symbols = ['XOM', 'CVX', 'SHEL', 'BP', 'TUPRS.IS', 'KRDMD.IS']
        return symbol in energy_symbols
    
    def _is_metal_symbol(self, symbol: str) -> bool:
        """Metal sembolü mü kontrol et"""
        metal_symbols = ['GOLD', 'SILVER', 'COPPER', 'NEM', 'FCX']
        return symbol in metal_symbols
    
    def _is_agriculture_symbol(self, symbol: str) -> bool:
        """Tarım sembolü mü kontrol et"""
        agriculture_symbols = ['WHEAT', 'CORN', 'SOY', 'ADM', 'BG']
        return symbol in agriculture_symbols
    
    def _get_cached_data(self, key: str) -> Optional[Dict[str, Any]]:
        """Cache'den veri al"""
        try:
            if key in self.cache:
                if datetime.now() < self.cache_ttl[key]:
                    return self.cache[key]
                else:
                    del self.cache[key]
                    del self.cache_ttl[key]
            return None
        except Exception as e:
            return None
    
    def _cache_data(self, key: str, data: Dict[str, Any], ttl_seconds: int):
        """Veriyi cache'e kaydet"""
        try:
            self.cache[key] = data
            self.cache_ttl[key] = datetime.now() + timedelta(seconds=ttl_seconds)
        except Exception as e:
            log_error(f"Cache kaydetme hatası: {e}")

# Global macro data integration instance
macro_data_integration = MacroDataIntegration()

