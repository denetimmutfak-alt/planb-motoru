"""
PlanB Motoru - Teknik Analiz Modülü
Gelişmiş Teknik Göstergeler ve Analiz
"""
import pandas as pd
try:
    import pandas_ta as ta
except ImportError:
    ta = None
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Tuple
from src.utils.logger import log_info, log_error, log_debug, log_warning
from src.data.company_founding_dates import CompanyFoundingDates

class TechnicalAnalyzer:
    """Teknik analiz işlemlerini yöneten sınıf"""
    
    def __init__(self):
        self.founding_dates = CompanyFoundingDates()
        self.indicators_config = {
            'rsi_period': 14,
            'macd_fast': 12,
            'macd_slow': 26,
            'macd_signal': 9,
            'bb_period': 20,
            'bb_std': 2,
            'stoch_k': 14,
            'stoch_d': 3,
            'sma_periods': [5, 10, 20, 50, 100, 200],
            'ema_periods': [12, 26, 50],
            'volume_sma_period': 20
        }
    
    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Sütun isimlerini normalize et"""
        df = df.copy()  # Orijinal DataFrame'i değiştirme
        
        # Close sütunu
        if 'Close' not in df.columns:
            if 'close' in df.columns:
                df = df.rename(columns={'close': 'Close'})
            elif 'Adj Close' in df.columns:
                df = df.rename(columns={'Adj Close': 'Close'})
            elif 'adj_close' in df.columns:
                df = df.rename(columns={'adj_close': 'Close'})
            elif 'CLOSE' in df.columns:
                df = df.rename(columns={'CLOSE': 'Close'})
        
        # High sütunu
        if 'High' not in df.columns:
            if 'high' in df.columns:
                df = df.rename(columns={'high': 'High'})
            elif 'HIGH' in df.columns:
                df = df.rename(columns={'HIGH': 'High'})
        
        # Low sütunu
        if 'Low' not in df.columns:
            if 'low' in df.columns:
                df = df.rename(columns={'low': 'Low'})
            elif 'LOW' in df.columns:
                df = df.rename(columns={'LOW': 'Low'})
        
        # Volume sütunu
        if 'Volume' not in df.columns:
            if 'volume' in df.columns:
                df = df.rename(columns={'volume': 'Volume'})
            elif 'VOLUME' in df.columns:
                df = df.rename(columns={'VOLUME': 'Volume'})
        
        return df

    def calculate_rsi(self, df: pd.DataFrame, period: int = None) -> Dict[str, float]:
        """RSI (Relative Strength Index) hesapla"""
        try:
            if df.empty or len(df) < 20:
                return {'rsi': 50.0, 'rsi_signal': 'NÖTR'}
            
            # Sütun isimlerini normalize et
            df = self._normalize_columns(df)
            
            period = period or self.indicators_config['rsi_period']
            rsi = ta.rsi(df['Close'], length=period) if ta else None if ta else None
            
            if rsi is None or rsi.empty:
                return {'rsi': 50.0, 'rsi_signal': 'NÖTR'}
            
            current_rsi = rsi.iloc[-1]
            
            # RSI sinyali
            if current_rsi >= 70:
                signal = 'AŞIRI_ALIM'
            elif current_rsi <= 30:
                signal = 'AŞIRI_SATIM'
            elif current_rsi >= 60:
                signal = 'GÜÇLÜ'
            elif current_rsi <= 40:
                signal = 'ZAYIF'
            else:
                signal = 'NÖTR'
            
            return {
                'rsi': round(current_rsi, 2),
                'rsi_signal': signal,
                'rsi_trend': self._calculate_rsi_trend(rsi)
            }
            
        except Exception as e:
            log_error(f"RSI hesaplanırken hata: {e}")
            return {'rsi': 50.0, 'rsi_signal': 'NÖTR'}
    
    def calculate_macd(self, df: pd.DataFrame) -> Dict[str, float]:
        """MACD (Moving Average Convergence Divergence) hesapla"""
        try:
            if df.empty or len(df) < 30:
                return {'macd': 0.0, 'macd_signal': 0.0, 'macd_histogram': 0.0, 'macd_trend': 'NÖTR'}
            
            # Sütun isimlerini normalize et
            df = self._normalize_columns(df)
            
            macd = ta.macd(
                df['Close'], 
                fast=self.indicators_config['macd_fast'],
                slow=self.indicators_config['macd_slow'],
                signal=self.indicators_config['macd_signal']
            ) if ta else None if ta else None
            
            if macd is None or macd.empty:
                return {'macd': 0.0, 'macd_signal': 0.0, 'macd_histogram': 0.0, 'macd_trend': 'NÖTR'}
            
            current_macd = macd['MACD_12_26_9'].iloc[-1]
            current_signal = macd['MACDs_12_26_9'].iloc[-1]
            current_histogram = macd['MACDh_12_26_9'].iloc[-1]
            
            # MACD trend analizi
            macd_trend = self._calculate_macd_trend(macd)
            
            return {
                'macd': round(current_macd, 4),
                'macd_signal': round(current_signal, 4),
                'macd_histogram': round(current_histogram, 4),
                'macd_trend': macd_trend
            }
            
        except Exception as e:
            log_error(f"MACD hesaplanırken hata: {e}")
            return {'macd': 0.0, 'macd_signal': 0.0, 'macd_histogram': 0.0, 'macd_trend': 'NÖTR'}
    
    def calculate_bollinger_bands(self, df: pd.DataFrame) -> Dict[str, float]:
        """Bollinger Bands hesapla"""
        try:
            if df.empty or len(df) < 25:
                return {'bb_upper': 0.0, 'bb_middle': 0.0, 'bb_lower': 0.0, 'bb_position': 'NÖTR'}
            
            # Sütun isimlerini normalize et
            df = self._normalize_columns(df)
            
            bb = ta.bbands(
                df['Close'],
                length=self.indicators_config['bb_period'],
                std=self.indicators_config['bb_std']
            ) if ta else None
            
            if bb is None or bb.empty:
                return {'bb_upper': 0.0, 'bb_middle': 0.0, 'bb_lower': 0.0, 'bb_position': 'NÖTR'}
            
            current_price = df['Close'].iloc[-1]
            bb_upper = bb['BBU_20_2.0'].iloc[-1]
            bb_middle = bb['BBM_20_2.0'].iloc[-1]
            bb_lower = bb['BBL_20_2.0'].iloc[-1]
            
            # Bollinger Bands pozisyonu
            if current_price >= bb_upper:
                position = 'ÜST_BANT'
            elif current_price <= bb_lower:
                position = 'ALT_BANT'
            elif current_price > bb_middle:
                position = 'ÜST_YARIM'
            else:
                position = 'ALT_YARIM'
            
            # Bollinger Bands genişliği
            bb_width = ((bb_upper - bb_lower) / bb_middle) * 100
            
            return {
                'bb_upper': round(bb_upper, 2),
                'bb_middle': round(bb_middle, 2),
                'bb_lower': round(bb_lower, 2),
                'bb_position': position,
                'bb_width': round(bb_width, 2)
            }
            
        except Exception as e:
            log_error(f"Bollinger Bands hesaplanırken hata: {e}")
            return {'bb_upper': 0.0, 'bb_middle': 0.0, 'bb_lower': 0.0, 'bb_position': 'NÖTR'}
    
    def calculate_stochastic(self, df: pd.DataFrame) -> Dict[str, float]:
        """Stochastic Oscillator hesapla"""
        try:
            if df.empty or len(df) < 20:
                return {'stoch_k': 50.0, 'stoch_d': 50.0, 'stoch_signal': 'NÖTR'}
            
            # Sütun isimlerini normalize et
            df = self._normalize_columns(df)
            
            stoch = ta.stoch(
                df['High'], 
                df['Low'], 
                df['Close'],
                k=self.indicators_config['stoch_k'],
                d=self.indicators_config['stoch_d']
            ) if ta else None
            
            if stoch is None or stoch.empty:
                return {'stoch_k': 50.0, 'stoch_d': 50.0, 'stoch_signal': 'NÖTR'}
            
            current_k = stoch['STOCHk_14_3_3'].iloc[-1]
            current_d = stoch['STOCHd_14_3_3'].iloc[-1]
            
            # Stochastic sinyali
            if current_k >= 80 and current_d >= 80:
                signal = 'AŞIRI_ALIM'
            elif current_k <= 20 and current_d <= 20:
                signal = 'AŞIRI_SATIM'
            elif current_k > current_d:
                signal = 'YÜKSELİŞ'
            elif current_k < current_d:
                signal = 'DÜŞÜŞ'
            else:
                signal = 'NÖTR'
            
            return {
                'stoch_k': round(current_k, 2),
                'stoch_d': round(current_d, 2),
                'stoch_signal': signal
            }
            
        except Exception as e:
            log_error(f"Stochastic hesaplanırken hata: {e}")
            return {'stoch_k': 50.0, 'stoch_d': 50.0, 'stoch_signal': 'NÖTR'}
    
    def calculate_moving_averages(self, df: pd.DataFrame) -> Dict[str, float]:
        """Hareketli ortalamaları hesapla"""
        try:
            if df.empty or len(df) < 200:
                return {}
            
            # Sütun isimlerini normalize et
            df = self._normalize_columns(df)
            
            current_price = df['Close'].iloc[-1]
            ma_data = {}
            
            # SMA hesaplama
            for period in self.indicators_config['sma_periods']:
                if len(df) >= period:
                    sma = ta.sma(df['Close'], length=period) if ta else None
                    if not sma.empty:
                        ma_data[f'sma_{period}'] = round(sma.iloc[-1], 2)
                        ma_data[f'sma_{period}_position'] = 'ÜST' if current_price > sma.iloc[-1] else 'ALT'
            
            # EMA hesaplama
            for period in self.indicators_config['ema_periods']:
                if len(df) >= period:
                    ema = ta.ema(df['Close'], length=period) if ta else None
                    if not ema.empty:
                        ma_data[f'ema_{period}'] = round(ema.iloc[-1], 2)
                        ma_data[f'ema_{period}_position'] = 'ÜST' if current_price > ema.iloc[-1] else 'ALT'
            
            # MA trend analizi
            ma_data['ma_trend'] = self._calculate_ma_trend(df)
            
            return ma_data
            
        except Exception as e:
            log_error(f"Hareketli ortalamalar hesaplanırken hata: {e}")
            return {}
    
    def calculate_volume_indicators(self, df: pd.DataFrame) -> Dict[str, float]:
        """Hacim göstergelerini hesapla"""
        try:
            if df.empty or 'Volume' not in df.columns or len(df) < 20:
                return {'volume_ratio': 1.0, 'volume_trend': 'NÖTR'}
            
            current_volume = df['Volume'].iloc[-1]
            volume_sma = ta.sma(df['Volume'], length=self.indicators_config['volume_sma_period']) if ta else None
            
            if volume_sma is None or volume_sma.empty:
                return {'volume_ratio': 1.0, 'volume_trend': 'NÖTR'}
            
            avg_volume = volume_sma.iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
            
            # Hacim trend analizi
            volume_trend = self._calculate_volume_trend(df)
            
            return {
                'volume_ratio': round(volume_ratio, 2),
                'volume_trend': volume_trend,
                'current_volume': current_volume,
                'avg_volume': round(avg_volume, 0)
            }
            
        except Exception as e:
            log_error(f"Hacim göstergeleri hesaplanırken hata: {e}")
            return {'volume_ratio': 1.0, 'volume_trend': 'NÖTR'}
    
    def calculate_technical_score(self, symbol: str, df: pd.DataFrame) -> float:
        """Genel teknik analiz skoru hesapla"""
        try:
            # Kuruluş tarihi bilgisini al
            founding_date = self.founding_dates.get_founding_date(symbol)
            if founding_date:
                log_debug(f"Technical Analysis - {symbol} kuruluş tarihi: {founding_date}")
            
            if df.empty or len(df) < 50:
                log_warning(f"{symbol}: Teknik analiz için yetersiz veri")
                return 50.0
            
            total_score = 0
            weight_count = 0
            
            # RSI analizi (ağırlık: 0.25)
            rsi_data = self.calculate_rsi(df)
            rsi_score = self._rsi_to_score(rsi_data['rsi'])
            total_score += rsi_score * 0.25
            weight_count += 0.25
            
            # MACD analizi (ağırlık: 0.25)
            macd_data = self.calculate_macd(df)
            macd_score = self._macd_to_score(macd_data)
            total_score += macd_score * 0.25
            weight_count += 0.25
            
            # Bollinger Bands analizi (ağırlık: 0.20)
            bb_data = self.calculate_bollinger_bands(df)
            bb_score = self._bb_to_score(bb_data, df['Close'].iloc[-1])
            total_score += bb_score * 0.20
            weight_count += 0.20
            
            # Stochastic analizi (ağırlık: 0.15)
            stoch_data = self.calculate_stochastic(df)
            stoch_score = self._stoch_to_score(stoch_data)
            total_score += stoch_score * 0.15
            weight_count += 0.15
            
            # Hacim analizi (ağırlık: 0.15)
            volume_data = self.calculate_volume_indicators(df)
            volume_score = self._volume_to_score(volume_data)
            total_score += volume_score * 0.15
            weight_count += 0.15
            
            # Normalize et
            if weight_count > 0:
                final_score = total_score / weight_count
            else:
                final_score = 50.0
            
            log_info(f"{symbol}: Teknik analiz skoru: {final_score:.2f}")
            return round(max(0, min(100, final_score)), 2)
            
        except Exception as e:
            log_error(f"{symbol} teknik analiz skoru hesaplanırken hata: {e}")
            return 50.0
    
    def _rsi_to_score(self, rsi: float) -> float:
        """RSI değerini skora çevir"""
        if rsi >= 70:
            return 20  # Aşırı alım
        elif rsi >= 60:
            return 40  # Güçlü
        elif rsi >= 50:
            return 60  # Pozitif
        elif rsi >= 40:
            return 40  # Zayıf
        elif rsi >= 30:
            return 60  # Aşırı satım (alım fırsatı)
        else:
            return 80  # Çok aşırı satım
    
    def _macd_to_score(self, macd_data: Dict) -> float:
        """MACD verilerini skora çevir"""
        macd = macd_data.get('macd', 0)
        signal = macd_data.get('macd_signal', 0)
        histogram = macd_data.get('macd_histogram', 0)
        
        if macd > signal and histogram > 0:
            return 80  # Güçlü yükseliş
        elif macd > signal:
            return 60  # Yükseliş
        elif macd < signal and histogram < 0:
            return 20  # Güçlü düşüş
        elif macd < signal:
            return 40  # Düşüş
        else:
            return 50  # Nötr
    
    def _bb_to_score(self, bb_data: Dict, current_price: float) -> float:
        """Bollinger Bands verilerini skora çevir"""
        position = bb_data.get('bb_position', 'NÖTR')
        
        if position == 'ALT_BANT':
            return 80  # Aşırı satım, alım fırsatı
        elif position == 'ÜST_BANT':
            return 20  # Aşırı alım, satış fırsatı
        elif position == 'ÜST_YARIM':
            return 60  # Pozitif
        elif position == 'ALT_YARIM':
            return 40  # Negatif
        else:
            return 50  # Nötr
    
    def _stoch_to_score(self, stoch_data: Dict) -> float:
        """Stochastic verilerini skora çevir"""
        signal = stoch_data.get('stoch_signal', 'NÖTR')
        
        if signal == 'AŞIRI_SATIM':
            return 80  # Alım fırsatı
        elif signal == 'AŞIRI_ALIM':
            return 20  # Satış fırsatı
        elif signal == 'YÜKSELİŞ':
            return 70  # Pozitif
        elif signal == 'DÜŞÜŞ':
            return 30  # Negatif
        else:
            return 50  # Nötr
    
    def _volume_to_score(self, volume_data: Dict) -> float:
        """Hacim verilerini skora çevir"""
        volume_ratio = volume_data.get('volume_ratio', 1.0)
        trend = volume_data.get('volume_trend', 'NÖTR')
        
        if volume_ratio >= 2.0 and trend == 'YÜKSELİŞ':
            return 80  # Güçlü hacim artışı
        elif volume_ratio >= 1.5 and trend == 'YÜKSELİŞ':
            return 70  # Hacim artışı
        elif volume_ratio >= 1.0 and trend == 'YÜKSELİŞ':
            return 60  # Normal hacim
        elif volume_ratio < 0.5:
            return 30  # Düşük hacim
        else:
            return 50  # Nötr
    
    def _calculate_rsi_trend(self, rsi_series: pd.Series) -> str:
        """RSI trend analizi"""
        try:
            if len(rsi_series) < 5:
                return 'NÖTR'
            
            recent_rsi = rsi_series.tail(5)
            if recent_rsi.iloc[-1] > recent_rsi.iloc[0]:
                return 'YÜKSELİŞ'
            elif recent_rsi.iloc[-1] < recent_rsi.iloc[0]:
                return 'DÜŞÜŞ'
            else:
                return 'NÖTR'
        except:
            return 'NÖTR'
    
    def _calculate_macd_trend(self, macd_df: pd.DataFrame) -> str:
        """MACD trend analizi"""
        try:
            if len(macd_df) < 5:
                return 'NÖTR'
            
            histogram = macd_df['MACDh_12_26_9'].tail(5)
            if histogram.iloc[-1] > histogram.iloc[0]:
                return 'YÜKSELİŞ'
            elif histogram.iloc[-1] < histogram.iloc[0]:
                return 'DÜŞÜŞ'
            else:
                return 'NÖTR'
        except:
            return 'NÖTR'
    
    def _calculate_ma_trend(self, df: pd.DataFrame) -> str:
        """Hareketli ortalama trend analizi"""
        try:
            if len(df) < 50:
                return 'NÖTR'
            
            # Sütun isimlerini normalize et
            df = self._normalize_columns(df)
            
            sma_20 = ta.sma(df['Close'], length=20) if ta else None
            sma_50 = ta.sma(df['Close'], length=50) if ta else None
            
            if sma_20.empty or sma_50.empty:
                return 'NÖTR'
            
            if sma_20.iloc[-1] > sma_50.iloc[-1]:
                return 'YÜKSELİŞ'
            elif sma_20.iloc[-1] < sma_50.iloc[-1]:
                return 'DÜŞÜŞ'
            else:
                return 'NÖTR'
        except:
            return 'NÖTR'
    
    def _calculate_volume_trend(self, df: pd.DataFrame) -> str:
        """Hacim trend analizi"""
        try:
            if len(df) < 10 or 'Volume' not in df.columns:
                return 'NÖTR'
            
            recent_volume = df['Volume'].tail(10)
            if recent_volume.iloc[-1] > recent_volume.iloc[0]:
                return 'YÜKSELİŞ'
            elif recent_volume.iloc[-1] < recent_volume.iloc[0]:
                return 'DÜŞÜŞ'
            else:
                return 'NÖTR'
        except:
            return 'NÖTR'
    
    def get_technical_insights(self, symbol: str, df: pd.DataFrame) -> Dict[str, any]:
        """Teknik analiz içgörüleri"""
        try:
            if df is None or df.empty:
                return {
                    'symbol': symbol,
                    'technical_score': 50.0,
                    'error': 'Veri bulunamadı'
                }
            
            # Tüm teknik göstergeleri hesapla
            rsi_data = self.calculate_rsi(df)
            macd_data = self.calculate_macd(df)
            bb_data = self.calculate_bollinger_bands(df)
            stoch_data = self.calculate_stochastic(df)
            ma_data = self.calculate_moving_averages(df)
            volume_data = self.calculate_volume_indicators(df)
            technical_score = self.calculate_technical_score(symbol, df)
            
            insights = {
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'technical_score': technical_score,
                'rsi': rsi_data,
                'macd': macd_data,
                'bollinger_bands': bb_data,
                'stochastic': stoch_data,
                'moving_averages': ma_data,
                'volume': volume_data
            }
            
            return insights
            
        except Exception as e:
            log_error(f"{symbol} teknik analiz içgörüleri oluşturulurken hata: {e}")
            return {
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'technical_score': 50.0,
                'error': str(e)
            }
    
    def get_technical_recommendation(self, symbol: str, df: pd.DataFrame) -> str:
        """Teknik analiz önerisi"""
        try:
            technical_score = self.calculate_technical_score(symbol, df)
            
            if technical_score >= 75:
                return "AL"  # Güçlü alım sinyali
            elif technical_score >= 60:
                return "AL"  # Alım sinyali
            elif technical_score >= 40:
                return "TUT"  # Bekle
            else:
                return "SAT"  # Satış sinyali
                
        except Exception as e:
            log_error(f"{symbol} teknik analiz önerisi belirlenirken hata: {e}")
            return "TUT"




