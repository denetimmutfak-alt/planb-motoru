"""
Risk Analizi Modülü
Gelişmiş risk analizi ile ultra entegrasyon desteği

Bu modül risk analizi sağlar ve ultra risk modülü ile entegrasyon destekler
"""

import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, Optional

# CompanyFoundingDates entegrasyonu
try:
    from ..data.company_founding_dates import CompanyFoundingDates
    FOUNDING_DATES_AVAILABLE = True
    print("INFO: CompanyFoundingDates modülü risk analysis'e entegre edildi")
except ImportError:
    FOUNDING_DATES_AVAILABLE = False
    print("WARNING: CompanyFoundingDates modülü bulunamadı")

try:
    from .ultra_risk import UltraRiskAnalyzer
    ULTRA_AVAILABLE = True
except ImportError:
    ULTRA_AVAILABLE = False


class RiskAnalyzer:
    """Risk analizi sistemi"""
    
    def __init__(self):
        """Analyzer'ı başlat"""
        self.name = "Risk Analyzer"
        
        # CompanyFoundingDates entegrasyonu
        self.founding_dates = None
        if FOUNDING_DATES_AVAILABLE:
            try:
                self.founding_dates = CompanyFoundingDates()
                print("INFO: CompanyFoundingDates risk analyzer'a başarıyla entegre edildi")
            except Exception as e:
                print(f"WARNING: CompanyFoundingDates risk analyzer'a entegre edilemedi: {str(e)}")
        
        # Ultra analyzer'ı yükle (varsa)
        if ULTRA_AVAILABLE:
            try:
                self.ultra_analyzer = UltraRiskAnalyzer()
                self.ultra_mode = True
                self._log_info("Ultra Risk Analyzer başarıyla import edildi")
            except Exception as e:
                self.ultra_mode = False
                self._log_error(f"Ultra Risk Analyzer import hatası: {str(e)}")
        else:
            self.ultra_mode = False
            self._log_info("Risk Analyzer (uyumluluk modu) başlatıldı")
    
    def get_risk_score(self, symbol: str, data: Optional[pd.DataFrame] = None, 
                      portfolio_value: float = 100000) -> float:
        """
        Risk skoru hesapla
        
        Args:
            symbol: Sembol
            data: Fiyat verisi (opsiyonel)
            portfolio_value: Portföy değeri
            
        Returns:
            float: Risk skoru (0-100)
        """
        try:
            # Founding date bilgisini al
            founding_date = None
            if self.founding_dates:
                try:
                    founding_date = self.founding_dates.get_founding_date(symbol)
                    if founding_date:
                        print(f"INFO: {symbol} founding date risk analizinde kullanıldı: {founding_date}")
                    else:
                        print(f"DEBUG: {symbol} için founding date risk analizinde bulunamadı")
                except Exception as e:
                    print(f"ERROR: {symbol} founding date risk analizinde hata: {str(e)}")
            
            # Ultra modu aktifse ultra analiz kullan
            if self.ultra_mode:
                ultra_result = self.ultra_analyzer.analyze_ultra_risk(symbol, portfolio_value)
                # Founding date bilgisini ultra result'a ekle
                if founding_date:
                    ultra_result['founding_date'] = founding_date
                return ultra_result['ultra_risk_score']
            
            # Uyumluluk modu - basit risk analizi
            return self._calculate_basic_risk_score(symbol, data, founding_date)
            
        except Exception as e:
            self._log_error(f"Risk skoru hesaplama hatası: {str(e)}")
            return 50.0
    
    def _calculate_basic_risk_score(self, symbol: str, data: Optional[pd.DataFrame] = None, founding_date: str = None) -> float:
        """Basit risk skoru hesaplama"""
        try:
            # Simülasyon için basit risk skoru
            base_score = 50.0
            
            # Sektör risk ayarlaması
            sector_adjustment = self._get_sector_risk_adjustment(symbol)
            
            # Founding date risk adjustment
            founding_adjustment = 0
            if founding_date:
                # Eski şirketler daha az riskli kabul ediliyor
                try:
                    founding_year = int(founding_date.split('-')[0])
                    current_year = datetime.now().year
                    company_age = current_year - founding_year
                    if company_age > 50:
                        founding_adjustment = 5  # Very established
                    elif company_age > 25:
                        founding_adjustment = 3  # Established
                    elif company_age > 10:
                        founding_adjustment = 1  # Mature
                    else:
                        founding_adjustment = -2  # Young, higher risk
                except:
                    founding_adjustment = 0
            
            # Random risk faktörü (gerçek implementasyonda piyasa verisi kullanılır)
            risk_factor = np.random.uniform(0.8, 1.2)
            
            # Final score
            final_score = base_score + sector_adjustment + founding_adjustment + (risk_factor - 1) * 30
            
            return max(0, min(100, final_score))
            
        except Exception as e:
            self._log_error(f"Basit risk skoru hesaplama hatası: {str(e)}")
            return 50.0
    
    def _get_sector_risk_adjustment(self, symbol: str) -> float:
        """Sektör risk ayarlaması"""
        # Basit sektör belirleme
        tech_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA']
        financial_symbols = ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C']
        energy_symbols = ['XOM', 'CVX', 'COP', 'SLB', 'HAL']
        
        if symbol in energy_symbols:
            return -20  # Enerji en riskli
        elif symbol in financial_symbols:
            return -15  # Finansal yüksek risk
        elif symbol in tech_symbols:
            return -10  # Teknoloji orta risk
        else:
            return 0
    
    def _log_info(self, message: str):
        """Info log"""
        print(f"INFO: {message}")
    
    def _log_error(self, message: str):
        """Error log"""
        print(f"ERROR: {message}")
