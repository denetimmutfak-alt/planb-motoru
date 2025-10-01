"""
PlanB Motoru - Trend Analiz Modülü
Gelişmiş Trend Analizi ve Hareketli Ortalama Sistemleri
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Tuple
from src.utils.logger import log_info, log_error, log_debug, log_warning

class TrendAnalyzer:
    """Trend analiz işlemlerini yöneten sınıf"""
    
    def __init__(self):
        self.ma_periods = {
            'short': [5, 10, 20],
            'medium': [50, 100],
            'long': [200, 300]
        }
        self.ema_periods = [12, 26, 50, 100, 200]
        self.trend_thresholds = {
            'strong_uptrend': 0.05,  # %5 üzeri güçlü yükseliş
            'uptrend': 0.02,        # %2 üzeri yükseliş
            'sideways': 0.02,       # %2 altı yatay
            'downtrend': -0.02,     # %2 altı düşüş
            'strong_downtrend': -0.05  # %5 altı güçlü düşüş
        }
    
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
            for period in [5, 10, 20, 50, 100, 200]:
                if len(df) >= period:
                    sma = df['Close'].rolling(window=period).mean()
                    if not sma.empty:
                        ma_data[f'sma_{period}'] = round(sma.iloc[-1], 2)
                        ma_data[f'sma_{period}_position'] = 'ÜST' if current_price > sma.iloc[-1] else 'ALT'
                        ma_data[f'sma_{period}_distance'] = round(((current_price - sma.iloc[-1]) / sma.iloc[-1]) * 100, 2)
            
            # EMA hesaplama
            for period in self.ema_periods:
                if len(df) >= period:
                    ema = df['Close'].ewm(span=period).mean()
                    if not ema.empty:
                        ma_data[f'ema_{period}'] = round(ema.iloc[-1], 2)
                        ma_data[f'ema_{period}_position'] = 'ÜST' if current_price > ema.iloc[-1] else 'ALT'
                        ma_data[f'ema_{period}_distance'] = round(((current_price - ema.iloc[-1]) / ema.iloc[-1]) * 100, 2)
            
            return ma_data
            
        except Exception as e:
            log_error(f"Hareketli ortalamalar hesaplanırken hata: {e}")
            return {}
    
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
        
        return df

    def analyze_trend_direction(self, df: pd.DataFrame) -> Dict[str, any]:
        """Trend yönünü analiz et"""
        try:
            if df.empty or len(df) < 50:
                return {"trend": "Bilinmiyor", "strength": 0, "confidence": 0}
            
            # Sütun isimlerini normalize et
            df = self._normalize_columns(df)
            
            # Farklı zaman dilimlerinde trend analizi
            short_trend = self._analyze_short_term_trend(df)
            medium_trend = self._analyze_medium_term_trend(df)
            long_trend = self._analyze_long_term_trend(df)
            
            # Trend skorları
            short_score = self._trend_to_score(short_trend)
            medium_score = self._trend_to_score(medium_trend)
            long_score = self._trend_to_score(long_trend)
            
            # Ağırlıklı ortalama
            total_score = (short_score * 0.3) + (medium_score * 0.4) + (long_score * 0.3)
            
            # Trend belirleme
            if total_score >= 70:
                trend = "GÜÇLÜ_YÜKSELİŞ"
                strength = total_score
            elif total_score >= 60:
                trend = "YÜKSELİŞ"
                strength = total_score
            elif total_score >= 40:
                trend = "YATAY"
                strength = 50
            elif total_score >= 30:
                trend = "DÜŞÜŞ"
                strength = total_score
            else:
                trend = "GÜÇLÜ_DÜŞÜŞ"
                strength = total_score
            
            # Güven seviyesi
            confidence = self._calculate_trend_confidence(df, trend)
            
            return {
                "trend": trend,
                "strength": round(strength, 2),
                "confidence": round(confidence, 2),
                "short_term": short_trend,
                "medium_term": medium_trend,
                "long_term": long_trend,
                "score_breakdown": {
                    "short": short_score,
                    "medium": medium_score,
                    "long": long_score,
                    "total": total_score
                }
            }
            
        except Exception as e:
            log_error(f"Trend yönü analizi yapılırken hata: {e}")
            return {"trend": "Hata", "strength": 0, "confidence": 0}
    
    def _analyze_short_term_trend(self, df: pd.DataFrame) -> str:
        """Kısa vadeli trend analizi (5-20 gün)"""
        try:
            if len(df) < 20:
                return "Bilinmiyor"
            
            # Son 20 günlük veri
            recent_data = df.tail(20)
            
            # Fiyat değişimi
            price_change = ((recent_data['Close'].iloc[-1] - recent_data['Close'].iloc[0]) / recent_data['Close'].iloc[0]) * 100
            
            # Hareketli ortalama analizi
            sma_5 = recent_data['Close'].rolling(window=5).mean()
            sma_10 = recent_data['Close'].rolling(window=10).mean()
            sma_20 = recent_data['Close'].rolling(window=20).mean()
            
            current_price = recent_data['Close'].iloc[-1]
            
            # Trend belirleme
            if (current_price > sma_5.iloc[-1] > sma_10.iloc[-1] > sma_20.iloc[-1] and 
                price_change > self.trend_thresholds['uptrend']):
                return "YÜKSELİŞ"
            elif (current_price < sma_5.iloc[-1] < sma_10.iloc[-1] < sma_20.iloc[-1] and 
                  price_change < self.trend_thresholds['downtrend']):
                return "DÜŞÜŞ"
            else:
                return "YATAY"
                
        except Exception as e:
            log_debug(f"Kısa vadeli trend analizi hatası: {e}")
            return "Bilinmiyor"
    
    def _analyze_medium_term_trend(self, df: pd.DataFrame) -> str:
        """Orta vadeli trend analizi (20-100 gün)"""
        try:
            if len(df) < 100:
                return "Bilinmiyor"
            
            # Son 100 günlük veri
            recent_data = df.tail(100)
            
            # Fiyat değişimi
            price_change = ((recent_data['Close'].iloc[-1] - recent_data['Close'].iloc[0]) / recent_data['Close'].iloc[0]) * 100
            
            # Hareketli ortalama analizi
            sma_20 = recent_data['Close'].rolling(window=20).mean()
            sma_50 = recent_data['Close'].rolling(window=50).mean()
            sma_100 = recent_data['Close'].rolling(window=100).mean()
            
            current_price = recent_data['Close'].iloc[-1]
            
            # Trend belirleme
            if (current_price > sma_20.iloc[-1] > sma_50.iloc[-1] > sma_100.iloc[-1] and 
                price_change > self.trend_thresholds['uptrend']):
                return "YÜKSELİŞ"
            elif (current_price < sma_20.iloc[-1] < sma_50.iloc[-1] < sma_100.iloc[-1] and 
                  price_change < self.trend_thresholds['downtrend']):
                return "DÜŞÜŞ"
            else:
                return "YATAY"
                
        except Exception as e:
            log_debug(f"Orta vadeli trend analizi hatası: {e}")
            return "Bilinmiyor"
    
    def _analyze_long_term_trend(self, df: pd.DataFrame) -> str:
        """Uzun vadeli trend analizi (100+ gün)"""
        try:
            if len(df) < 200:
                return "Bilinmiyor"
            
            # Son 200 günlük veri
            recent_data = df.tail(200)
            
            # Fiyat değişimi
            price_change = ((recent_data['Close'].iloc[-1] - recent_data['Close'].iloc[0]) / recent_data['Close'].iloc[0]) * 100
            
            # Hareketli ortalama analizi
            sma_50 = recent_data['Close'].rolling(window=50).mean()
            sma_100 = recent_data['Close'].rolling(window=100).mean()
            sma_200 = recent_data['Close'].rolling(window=200).mean()
            
            current_price = recent_data['Close'].iloc[-1]
            
            # Trend belirleme
            if (current_price > sma_50.iloc[-1] > sma_100.iloc[-1] > sma_200.iloc[-1] and 
                price_change > self.trend_thresholds['strong_uptrend']):
                return "YÜKSELİŞ"
            elif (current_price < sma_50.iloc[-1] < sma_100.iloc[-1] < sma_200.iloc[-1] and 
                  price_change < self.trend_thresholds['strong_downtrend']):
                return "DÜŞÜŞ"
            else:
                return "YATAY"
                
        except Exception as e:
            log_debug(f"Uzun vadeli trend analizi hatası: {e}")
            return "Bilinmiyor"
    
    def _trend_to_score(self, trend: str) -> float:
        """Trend string'ini skora çevir"""
        trend_scores = {
            "YÜKSELİŞ": 80,
            "DÜŞÜŞ": 20,
            "YATAY": 50,
            "Bilinmiyor": 50
        }
        return trend_scores.get(trend, 50)
    
    def _calculate_trend_confidence(self, df: pd.DataFrame, trend: str) -> float:
        """Trend güven seviyesini hesapla"""
        try:
            if len(df) < 50:
                return 0
            
            # Sütun isimlerini normalize et
            df = self._normalize_columns(df)
            
            # Fiyat volatilitesi
            returns = df['Close'].pct_change(fill_method=None).dropna()
            volatility = returns.std() * 100
            
            # Trend tutarlılığı
            consistency_score = 0
            
            # Son 10 günlük trend tutarlılığı
            recent_returns = returns.tail(10)
            if trend in ["YÜKSELİŞ", "GÜÇLÜ_YÜKSELİŞ"]:
                positive_days = (recent_returns > 0).sum()
                consistency_score = (positive_days / 10) * 100
            elif trend in ["DÜŞÜŞ", "GÜÇLÜ_DÜŞÜŞ"]:
                negative_days = (recent_returns < 0).sum()
                consistency_score = (negative_days / 10) * 100
            else:
                consistency_score = 50
            
            # Volatilite düzeltmesi
            if volatility > 5:  # Yüksek volatilite
                confidence = consistency_score * 0.7
            elif volatility < 2:  # Düşük volatilite
                confidence = consistency_score * 1.2
            else:  # Normal volatilite
                confidence = consistency_score
            
            return min(100, max(0, confidence))
            
        except Exception as e:
            log_debug(f"Trend güven seviyesi hesaplanırken hata: {e}")
            return 50
    
    def calculate_trend_score(self, symbol: str, df: pd.DataFrame) -> float:
        """Genel trend skoru hesapla"""
        try:
            if df.empty or len(df) < 50:
                log_warning(f"{symbol}: Trend analizi için yetersiz veri")
                return 50.0
            
            trend_analysis = self.analyze_trend_direction(df)
            trend_score = trend_analysis.get('strength', 50)
            confidence = trend_analysis.get('confidence', 50)
            
            # Güven seviyesi ile ağırlıklandır
            final_score = (trend_score * confidence / 100)
            
            log_info(f"{symbol}: Trend skoru: {final_score:.2f} (Güven: {confidence:.1f}%)")
            return round(max(0, min(100, final_score)), 2)
            
        except Exception as e:
            log_error(f"{symbol} trend skoru hesaplanırken hata: {e}")
            return 50.0
    
    def identify_support_resistance_levels(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """Destek ve direnç seviyelerini belirle"""
        try:
            if df.empty or len(df) < 50:
                return {"support": [], "resistance": []}
            
            # Yüksek ve düşük noktaları bul
            highs = df['High'].rolling(window=5, center=True).max()
            lows = df['Low'].rolling(window=5, center=True).min()
            
            # Yerel maksimum ve minimum noktalar
            resistance_levels = []
            support_levels = []
            
            for i in range(2, len(df) - 2):
                # Direnç seviyeleri (yerel maksimumlar)
                if (df['High'].iloc[i] == highs.iloc[i] and 
                    df['High'].iloc[i] > df['High'].iloc[i-1] and 
                    df['High'].iloc[i] > df['High'].iloc[i+1]):
                    resistance_levels.append(df['High'].iloc[i])
                
                # Destek seviyeleri (yerel minimumlar)
                if (df['Low'].iloc[i] == lows.iloc[i] and 
                    df['Low'].iloc[i] < df['Low'].iloc[i-1] and 
                    df['Low'].iloc[i] < df['Low'].iloc[i+1]):
                    support_levels.append(df['Low'].iloc[i])
            
            # Seviyeleri temizle ve sırala
            resistance_levels = sorted(list(set(resistance_levels)), reverse=True)[:5]
            support_levels = sorted(list(set(support_levels)))[:5]
            
            return {
                "support": support_levels,
                "resistance": resistance_levels
            }
            
        except Exception as e:
            log_error(f"Destek/direnç seviyeleri belirlenirken hata: {e}")
            return {"support": [], "resistance": []}
    
    def get_trend_insights(self, symbol: str, df: pd.DataFrame) -> Dict[str, any]:
        """Trend analizi içgörüleri"""
        try:
            if df.empty:
                return {
                    'symbol': symbol,
                    'trend_score': 50.0,
                    'error': 'Veri bulunamadı'
                }
            
            # Trend analizlerini yap
            trend_analysis = self.analyze_trend_direction(df)
            ma_data = self.calculate_moving_averages(df)
            support_resistance = self.identify_support_resistance_levels(df)
            trend_score = self.calculate_trend_score(symbol, df)
            
            insights = {
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'trend_score': trend_score,
                'trend_analysis': trend_analysis,
                'moving_averages': ma_data,
                'support_resistance': support_resistance
            }
            
            return insights
            
        except Exception as e:
            log_error(f"{symbol} trend içgörüleri oluşturulurken hata: {e}")
            return {
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'symbol': symbol,
                'trend_score': 50.0,
                'error': str(e)
            }
    
    def get_trend_recommendation(self, symbol: str, df: pd.DataFrame) -> str:
        """Trend analizine göre yatırım önerisi"""
        try:
            trend_score = self.calculate_trend_score(symbol, df)
            trend_analysis = self.analyze_trend_direction(df)
            trend = trend_analysis.get('trend', 'YATAY')
            confidence = trend_analysis.get('confidence', 50)
            
            if trend_score >= 70 and confidence >= 70:
                return "AL"  # Güçlü yükseliş trendi
            elif trend_score >= 60 and confidence >= 60:
                return "AL"  # Yükseliş trendi
            elif trend_score >= 40 and trend == "YATAY":
                return "TUT"  # Yatay trend, bekle
            elif trend_score < 40 and confidence >= 60:
                return "SAT"  # Düşüş trendi
            elif trend_score < 30 and confidence >= 70:
                return "SAT"  # Güçlü düşüş trendi
            else:
                return "TUT"  # Belirsiz durum
                
        except Exception as e:
            log_error(f"{symbol} trend önerisi belirlenirken hata: {e}")
            return "TUT"




