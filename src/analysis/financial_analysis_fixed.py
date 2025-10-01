"""
PlanB Motoru - Finansal Analiz Modülü (Düzeltilmiş)
Hephaistos & Hermes Entegrasyonlu
"""
import pandas as pd
import pandas_ta as ta
import numpy as np
from typing import Dict, Optional, Tuple
from src.utils.logger import log_info, log_error, log_debug, log_warning
from config.settings import config
from src.analysis.astrology_analysis import AstrologyAnalyzer
from src.analysis.shemitah_analysis import ShemitahAnalyzer
from src.analysis.cycle21_analysis import Cycle21Analyzer
from src.analysis.technical_analysis import TechnicalAnalyzer
from src.analysis.trend_analysis import TrendAnalyzer
from src.analysis.momentum_breakout_analysis import MomentumBreakoutAnalyzer

class FinancialAnalyzer:
    """Finansal analiz işlemlerini yöneten sınıf"""
    
    def __init__(self):
        self.config = config.load_from_file()
        self.analysis_config = self.config.get('analysis', {})
        
        # Analiz modüllerini başlat
        self.astrology_analyzer = AstrologyAnalyzer()
        self.shemitah_analyzer = ShemitahAnalyzer()
        self.cycle21_analyzer = Cycle21Analyzer()
        self.technical_analyzer = TechnicalAnalyzer()
        self.trend_analyzer = TrendAnalyzer()
        self.momentum_breakout_analyzer = MomentumBreakoutAnalyzer()
    
    def calculate_financial_health_score(self, symbol: str, stock_info: Dict) -> float:
        """Finansal sağlamlık puanını hesapla"""
        try:
            score = 0
            
            # PEG Ratio analizi (0-1.5 arası ideal)
            peg_ratio = stock_info.get('pegRatio')
            if peg_ratio and 0 < peg_ratio < 1.5:
                score += 25
                log_debug(f"{symbol}: PEG Ratio uygun ({peg_ratio:.2f})")
            
            # Operasyonel marj analizi (>%15 ideal)
            operating_margin = stock_info.get('operatingMargins', 0)
            if operating_margin > 0.15:
                score += 25
                log_debug(f"{symbol}: Operasyonel marj güçlü ({operating_margin:.2%})")
            
            # Net marj analizi (>%10 ideal)
            profit_margin = stock_info.get('profitMargins', 0)
            if profit_margin > 0.10:
                score += 25
                log_debug(f"{symbol}: Net marj güçlü ({profit_margin:.2%})")
            
            # ROE analizi (>%15 ideal)
            return_on_equity = stock_info.get('returnOnEquity', 0)
            if return_on_equity > 0.15:
                score += 25
                log_debug(f"{symbol}: ROE güçlü ({return_on_equity:.2%})")
            
            log_info(f"{symbol}: Finansal sağlamlık puanı: {score}/100")
            return score
            
        except Exception as e:
            log_error(f"{symbol} finansal sağlamlık puanı hesaplanırken hata: {e}")
            return 0
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> Dict[str, float]:
        """Teknik göstergeleri hesapla"""
        try:
            if df.empty or len(df) < 20:
                log_warning("Yetersiz veri - teknik analiz yapılamıyor")
                return {}
            
            indicators = {}
            
            # RSI (14 günlük)
            rsi = ta.rsi(df['Close'], length=14)
            indicators['rsi'] = rsi.iloc[-1] if not rsi.empty else 50
            
            # MACD
            macd = ta.macd(df['Close'])
            if not macd.empty:
                indicators['macd'] = macd['MACD_12_26_9'].iloc[-1]
                indicators['macd_signal'] = macd['MACDs_12_26_9'].iloc[-1]
                indicators['macd_histogram'] = macd['MACDh_12_26_9'].iloc[-1]
            
            # Bollinger Bands
            bb = ta.bbands(df['Close'], length=20)
            if not bb.empty:
                indicators['bb_upper'] = bb['BBU_20_2.0'].iloc[-1]
                indicators['bb_middle'] = bb['BBM_20_2.0'].iloc[-1]
                indicators['bb_lower'] = bb['BBL_20_2.0'].iloc[-1]
            
            # Stochastic
            stoch = ta.stoch(df['High'], df['Low'], df['Close'])
            if not stoch.empty:
                indicators['stoch_k'] = stoch['STOCHk_14_3_3'].iloc[-1]
                indicators['stoch_d'] = stoch['STOCHd_14_3_3'].iloc[-1]
            
            return indicators
            
        except Exception as e:
            log_error(f"Teknik göstergeler hesaplanırken hata: {e}")
            return {}
    
    def calculate_trend_analysis(self, df: pd.DataFrame) -> Dict[str, any]:
        """Trend analizi yap"""
        try:
            if df.empty or len(df) < 50:
                log_warning("Trend analizi için yetersiz veri")
                return {"trend": "Bilinmiyor", "strength": 0}
            
            # Hareketli ortalamalar
            ma_20 = df['Close'].rolling(window=20).mean()
            ma_50 = df['Close'].rolling(window=50).mean()
            
            current_price = df['Close'].iloc[-1]
            current_ma_20 = ma_20.iloc[-1]
            current_ma_50 = ma_50.iloc[-1]
            
            # Trend belirleme
            if current_price > current_ma_20 > current_ma_50:
                trend = "Yükseliş"
                strength = min(100, ((current_price - current_ma_50) / current_ma_50) * 100)
            elif current_price < current_ma_20 < current_ma_50:
                trend = "Düşüş"
                strength = min(100, ((current_ma_50 - current_price) / current_ma_50) * 100)
            else:
                trend = "Yatay"
                strength = 30
            
            return {
                "trend": trend,
                "strength": strength,
                "ma_20": current_ma_20,
                "ma_50": current_ma_50,
                "price_vs_ma20": ((current_price - current_ma_20) / current_ma_20) * 100
            }
            
        except Exception as e:
            log_error(f"Trend analizi yapılırken hata: {e}")
            return {"trend": "Hata", "strength": 0}
    
    def generate_signal(self, financial_score: float, technical_indicators: Dict, 
                       trend_analysis: Dict, gann_analysis: Dict, symbol: str, 
                       price_data: pd.DataFrame = None) -> Tuple[str, float, Dict]:
        """Gelişmiş sinyal üret - Hephaistos & Hermes entegrasyonlu"""
        try:
            total_score = 0
            score_breakdown = {}
            
            # 1. Finansal sağlamlık (ağırlık: 0.15)
            financial_weight = 0.15
            total_score += financial_score * financial_weight
            score_breakdown['financial'] = financial_score * financial_weight
            
            # 2. Teknik analiz (ağırlık: 0.15)
            technical_weight = 0.15
            if price_data is not None and not price_data.empty:
                technical_score = self.technical_analyzer.calculate_technical_score(symbol, price_data)
            else:
                # Fallback: basit RSI analizi
                rsi = technical_indicators.get('rsi', 50)
                if rsi < 30:
                    technical_score = 80  # Aşırı satım
                elif rsi > 70:
                    technical_score = 20  # Aşırı alım
                else:
                    technical_score = 50 + (50 - abs(rsi - 50)) * 0.6
            
            total_score += technical_score * technical_weight
            score_breakdown['technical'] = technical_score * technical_weight
            
            # 3. Trend analizi (ağırlık: 0.15)
            trend_weight = 0.15
            if price_data is not None and not price_data.empty:
                trend_score = self.trend_analyzer.calculate_trend_score(symbol, price_data)
            else:
                # Fallback: basit trend analizi
                trend = trend_analysis.get('trend', 'Bilinmiyor')
                if trend == 'Yükseliş':
                    trend_score = 80
                elif trend == 'Düşüş':
                    trend_score = 20
                else:
                    trend_score = 50
            
            total_score += trend_score * trend_weight
            score_breakdown['trend'] = trend_score * trend_weight
            
            # 4. Gann analizi (ağırlık: 0.15) - Varsayılan skor
            gann_weight = 0.15
            gann_score = 50  # Varsayılan skor
            total_score += gann_score * gann_weight
            score_breakdown['gann'] = gann_score * gann_weight
            
            # 5. Astroloji analizi (ağırlık: 0.30) - Ana odak noktası
            astrology_weight = 0.30
            astrology_score = self.astrology_analyzer.calculate_astrology_score(symbol)
            total_score += astrology_score * astrology_weight
            score_breakdown['astrology'] = astrology_score * astrology_weight
            
            # 6. Shemitah analizi (ağırlık: 0.05)
            shemitah_weight = 0.05
            shemitah_score = self.shemitah_analyzer.calculate_shemitah_score(symbol)
            total_score += shemitah_score * shemitah_weight
            score_breakdown['shemitah'] = shemitah_score * shemitah_weight
            
            # 7. Döngü21 analizi (ağırlık: 0.05)
            cycle21_weight = 0.05
            cycle21_score = self.cycle21_analyzer.calculate_cycle_score(symbol)
            total_score += cycle21_score * cycle21_weight
            score_breakdown['cycle21'] = cycle21_score * cycle21_weight
            
            # AL Sinyali ve Tutma Süresi Analizi
            al_signal = "TUT"  # Varsayılan
            holding_analysis = {}
            momentum_breakout_analysis = {}
            
            if price_data is not None and not price_data.empty:
                # Momentum ve Breakout analizi
                momentum_data = self.momentum_breakout_analyzer.calculate_momentum_indicators(price_data)
                breakout_data = self.momentum_breakout_analyzer.detect_breakouts(price_data)
                volume_data = self.momentum_breakout_analyzer.analyze_volume_patterns(price_data)
                
                # Mevcut skorlarla AL sinyali değerlendirmesi
                existing_scores = {
                    'total_score': total_score,
                    'financial_score': financial_score,
                    'technical_score': technical_score,
                    'trend_score': trend_score,
                    'gann_score': gann_score,
                    'astrology_score': astrology_score
                }
                
                # AL sinyali oluştur
                al_signal, al_analysis = self.momentum_breakout_analyzer.generate_al_signal(
                    symbol, price_data, existing_scores
                )
                
                # Tutma süresi analizi (Tüm sinyaller için)
                holding_analysis = self.momentum_breakout_analyzer.calculate_holding_period_analysis(
                    symbol, price_data, momentum_data, breakout_data, volume_data
                )
                
                momentum_breakout_analysis = {
                    'momentum_analysis': momentum_data,
                    'breakout_analysis': breakout_data,
                    'volume_analysis': volume_data,
                    'al_analysis': al_analysis
                }
            
            # Final sinyal belirleme (AL sinyali öncelikli)
            if al_signal == "AL":
                signal = "AL"
            elif total_score >= 70:
                signal = "AL"
            elif total_score >= 40:
                signal = "TUT"
            else:
                signal = "SAT"
            
            # Detaylı analiz sonuçları
            # Tutma süresi bilgisini al
            hold_days = 14  # Varsayılan değer
            if holding_analysis and 'recommended_holding' in holding_analysis:
                hold_days = holding_analysis['recommended_holding'].get('period', 14)
            
            detailed_analysis = {
                'financial_score': financial_score,
                'technical_score': technical_score,
                'trend_score': trend_score,
                'gann_score': gann_score,
                'astrology_score': astrology_score,
                'shemitah_score': shemitah_score,
                'cycle21_score': cycle21_score,
                'total_score': total_score,
                'signal': signal,
                'hold_days': hold_days,
                'score_breakdown': score_breakdown,
                'momentum_breakout_analysis': momentum_breakout_analysis,
                'holding_analysis': holding_analysis
            }
            
            log_info(f"{symbol}: Toplam puan: {total_score:.1f}, Sinyal: {signal}")
            log_debug(f"{symbol}: Puan dağılımı: {score_breakdown}")
            
            return signal, total_score, detailed_analysis
            
        except Exception as e:
            log_error(f"{symbol} sinyal üretilirken hata: {e}")
            return "BEKLE", 0, {'error': str(e)}


