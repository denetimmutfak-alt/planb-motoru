"""
PlanB Motoru - Multi-timeframe Charts
Farklı zaman dilimlerinde grafik analizi
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug

class MultiTimeframeCharts:
    """Multi-timeframe chart analizi"""
    
    def __init__(self):
        self.timeframes = {
            '1m': {'period': '1min', 'days': 1, 'description': '1 Dakika'},
            '5m': {'period': '5min', 'days': 1, 'description': '5 Dakika'},
            '15m': {'period': '15min', 'days': 3, 'description': '15 Dakika'},
            '1h': {'period': '1hour', 'days': 7, 'description': '1 Saat'},
            '4h': {'period': '4hour', 'days': 30, 'description': '4 Saat'},
            '1d': {'period': '1day', 'days': 365, 'description': '1 Gün'},
            '1w': {'period': '1week', 'days': 1825, 'description': '1 Hafta'},
            '1M': {'period': '1month', 'days': 3650, 'description': '1 Ay'}
        }
        
        self.technical_indicators = {
            'sma': {'periods': [20, 50, 200], 'name': 'Simple Moving Average'},
            'ema': {'periods': [12, 26, 50], 'name': 'Exponential Moving Average'},
            'rsi': {'period': 14, 'name': 'Relative Strength Index'},
            'macd': {'fast': 12, 'slow': 26, 'signal': 9, 'name': 'MACD'},
            'bollinger': {'period': 20, 'std': 2, 'name': 'Bollinger Bands'},
            'stochastic': {'k_period': 14, 'd_period': 3, 'name': 'Stochastic Oscillator'}
        }
    
    def generate_multi_timeframe_analysis(self, symbol: str, price_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Multi-timeframe analiz oluştur"""
        try:
            analysis_results = {}
            
            for timeframe, config in self.timeframes.items():
                if timeframe in price_data and not price_data[timeframe].empty:
                    df = price_data[timeframe]
                    
                    # Temel analiz
                    basic_analysis = self._analyze_timeframe_basic(df, timeframe)
                    
                    # Teknik göstergeler
                    technical_analysis = self._analyze_timeframe_technical(df, timeframe)
                    
                    # Trend analizi
                    trend_analysis = self._analyze_timeframe_trend(df, timeframe)
                    
                    # Destek/direnç seviyeleri
                    support_resistance = self._find_support_resistance(df, timeframe)
                    
                    analysis_results[timeframe] = {
                        'timeframe': timeframe,
                        'description': config['description'],
                        'data_points': len(df),
                        'date_range': {
                            'start': df.index[0].isoformat() if not df.empty else None,
                            'end': df.index[-1].isoformat() if not df.empty else None
                        },
                        'basic_analysis': basic_analysis,
                        'technical_analysis': technical_analysis,
                        'trend_analysis': trend_analysis,
                        'support_resistance': support_resistance,
                        'last_updated': datetime.now().isoformat()
                    }
            
            # Cross-timeframe analiz
            cross_timeframe_analysis = self._analyze_cross_timeframe(analysis_results)
            
            return {
                'symbol': symbol,
                'timeframe_analyses': analysis_results,
                'cross_timeframe_analysis': cross_timeframe_analysis,
                'generated_at': datetime.now().isoformat(),
                'total_timeframes': len(analysis_results)
            }
            
        except Exception as e:
            log_error(f"Multi-timeframe analiz hatası: {e}")
            return {}
    
    def _analyze_timeframe_basic(self, df: pd.DataFrame, timeframe: str) -> Dict[str, Any]:
        """Temel timeframe analizi"""
        try:
            if df.empty or 'close' not in df.columns:
                return {}
            
            close_prices = df['close']
            high_prices = df['high'] if 'high' in df.columns else close_prices
            low_prices = df['low'] if 'low' in df.columns else close_prices
            volumes = df['volume'] if 'volume' in df.columns else pd.Series()
            
            # Fiyat istatistikleri
            current_price = close_prices.iloc[-1]
            price_change = close_prices.pct_change(fill_method=None).iloc[-1] * 100 if len(close_prices) > 1 else 0
            
            # Volatilite
            volatility = close_prices.pct_change(fill_method=None).std() * 100 if len(close_prices) > 1 else 0
            
            # Hacim analizi
            volume_analysis = {}
            if not volumes.empty:
                avg_volume = volumes.mean()
                current_volume = volumes.iloc[-1]
                volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
                
                volume_analysis = {
                    'current_volume': current_volume,
                    'average_volume': avg_volume,
                    'volume_ratio': volume_ratio,
                    'volume_trend': 'high' if volume_ratio > 1.5 else ('low' if volume_ratio < 0.5 else 'normal')
                }
            
            return {
                'current_price': current_price,
                'price_change_pct': price_change,
                'volatility_pct': volatility,
                'high_52w': high_prices.max() if not high_prices.empty else current_price,
                'low_52w': low_prices.min() if not low_prices.empty else current_price,
                'volume_analysis': volume_analysis,
                'price_position': self._calculate_price_position(current_price, high_prices, low_prices)
            }
            
        except Exception as e:
            log_error(f"Temel timeframe analizi hatası: {e}")
            return {}
    
    def _analyze_timeframe_technical(self, df: pd.DataFrame, timeframe: str) -> Dict[str, Any]:
        """Teknik göstergeler analizi"""
        try:
            if df.empty or 'close' not in df.columns:
                return {}
            
            close_prices = df['close']
            high_prices = df['high'] if 'high' in df.columns else close_prices
            low_prices = df['low'] if 'low' in df.columns else close_prices
            
            technical_signals = {}
            
            # SMA analizi
            sma_20 = close_prices.rolling(20).mean()
            sma_50 = close_prices.rolling(50).mean()
            sma_200 = close_prices.rolling(200).mean()
            
            if not sma_20.empty and not sma_50.empty:
                current_price = close_prices.iloc[-1]
                current_sma_20 = sma_20.iloc[-1]
                current_sma_50 = sma_50.iloc[-1]
                
                technical_signals['sma_signals'] = {
                    'price_vs_sma20': 'above' if current_price > current_sma_20 else 'below',
                    'price_vs_sma50': 'above' if current_price > current_sma_50 else 'below',
                    'sma_cross': 'bullish' if current_sma_20 > current_sma_50 else 'bearish',
                    'sma_20': current_sma_20,
                    'sma_50': current_sma_50
                }
            
            # RSI analizi
            rsi = self._calculate_rsi(close_prices, 14)
            if not rsi.empty:
                current_rsi = rsi.iloc[-1]
                technical_signals['rsi'] = {
                    'value': current_rsi,
                    'signal': 'oversold' if current_rsi < 30 else ('overbought' if current_rsi > 70 else 'neutral'),
                    'trend': 'bullish' if current_rsi > 50 else 'bearish'
                }
            
            # MACD analizi
            macd_data = self._calculate_macd(close_prices)
            if macd_data:
                technical_signals['macd'] = {
                    'macd_line': macd_data['macd'].iloc[-1],
                    'signal_line': macd_data['signal'].iloc[-1],
                    'histogram': macd_data['histogram'].iloc[-1],
                    'signal': 'bullish' if macd_data['macd'].iloc[-1] > macd_data['signal'].iloc[-1] else 'bearish'
                }
            
            # Bollinger Bands
            bb_data = self._calculate_bollinger_bands(close_prices)
            if bb_data:
                current_price = close_prices.iloc[-1]
                technical_signals['bollinger'] = {
                    'upper': bb_data['upper'].iloc[-1],
                    'middle': bb_data['middle'].iloc[-1],
                    'lower': bb_data['lower'].iloc[-1],
                    'position': 'above' if current_price > bb_data['upper'].iloc[-1] else ('below' if current_price < bb_data['lower'].iloc[-1] else 'middle'),
                    'squeeze': 'yes' if (bb_data['upper'].iloc[-1] - bb_data['lower'].iloc[-1]) / bb_data['middle'].iloc[-1] < 0.1 else 'no'
                }
            
            return technical_signals
            
        except Exception as e:
            log_error(f"Teknik analiz hatası: {e}")
            return {}
    
    def _analyze_timeframe_trend(self, df: pd.DataFrame, timeframe: str) -> Dict[str, Any]:
        """Trend analizi"""
        try:
            if df.empty or 'close' not in df.columns:
                return {}
            
            close_prices = df['close']
            
            # Trend yönü
            if len(close_prices) >= 20:
                recent_20 = close_prices.tail(20)
                trend_direction = 'up' if recent_20.iloc[-1] > recent_20.iloc[0] else 'down'
                
                # Trend gücü
                price_change = (recent_20.iloc[-1] - recent_20.iloc[0]) / recent_20.iloc[0] * 100
                trend_strength = 'strong' if abs(price_change) > 10 else ('moderate' if abs(price_change) > 5 else 'weak')
                
                # Trend süresi
                trend_duration = self._calculate_trend_duration(close_prices)
                
                return {
                    'direction': trend_direction,
                    'strength': trend_strength,
                    'duration_days': trend_duration,
                    'price_change_pct': price_change,
                    'trend_consistency': self._calculate_trend_consistency(close_prices)
                }
            
            return {}
            
        except Exception as e:
            log_error(f"Trend analizi hatası: {e}")
            return {}
    
    def _find_support_resistance(self, df: pd.DataFrame, timeframe: str) -> Dict[str, Any]:
        """Destek/direnç seviyeleri bul"""
        try:
            if df.empty or 'high' not in df.columns or 'low' not in df.columns:
                return {}
            
            high_prices = df['high']
            low_prices = df['low']
            close_prices = df['close']
            
            # Basit destek/direnç seviyeleri
            resistance_levels = self._find_pivot_highs(high_prices)
            support_levels = self._find_pivot_lows(low_prices)
            
            current_price = close_prices.iloc[-1]
            
            # En yakın seviyeler
            nearest_resistance = min([r for r in resistance_levels if r > current_price], default=None)
            nearest_support = max([s for s in support_levels if s < current_price], default=None)
            
            return {
                'resistance_levels': resistance_levels[:5],  # Top 5
                'support_levels': support_levels[:5],  # Top 5
                'nearest_resistance': nearest_resistance,
                'nearest_support': nearest_support,
                'resistance_distance': ((nearest_resistance - current_price) / current_price * 100) if nearest_resistance else None,
                'support_distance': ((current_price - nearest_support) / current_price * 100) if nearest_support else None
            }
            
        except Exception as e:
            log_error(f"Destek/direnç analizi hatası: {e}")
            return {}
    
    def _analyze_cross_timeframe(self, timeframe_analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Cross-timeframe analiz"""
        try:
            if not timeframe_analyses:
                return {}
            
            # Trend uyumu
            trend_alignment = self._check_trend_alignment(timeframe_analyses)
            
            # Sinyal uyumu
            signal_alignment = self._check_signal_alignment(timeframe_analyses)
            
            # Zaman dilimi hiyerarşisi
            timeframe_hierarchy = self._analyze_timeframe_hierarchy(timeframe_analyses)
            
            # Genel değerlendirme
            overall_assessment = self._assess_overall_timeframe(timeframe_analyses)
            
            return {
                'trend_alignment': trend_alignment,
                'signal_alignment': signal_alignment,
                'timeframe_hierarchy': timeframe_hierarchy,
                'overall_assessment': overall_assessment,
                'consensus_strength': self._calculate_consensus_strength(timeframe_analyses)
            }
            
        except Exception as e:
            log_error(f"Cross-timeframe analiz hatası: {e}")
            return {}
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """RSI hesapla"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except Exception as e:
            return pd.Series()
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Optional[Dict[str, pd.Series]]:
        """MACD hesapla"""
        try:
            ema_fast = prices.ewm(span=fast).mean()
            ema_slow = prices.ewm(span=slow).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal).mean()
            histogram = macd_line - signal_line
            
            return {
                'macd': macd_line,
                'signal': signal_line,
                'histogram': histogram
            }
        except Exception as e:
            return None
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std: float = 2) -> Optional[Dict[str, pd.Series]]:
        """Bollinger Bands hesapla"""
        try:
            middle = prices.rolling(period).mean()
            std_dev = prices.rolling(period).std()
            upper = middle + (std_dev * std)
            lower = middle - (std_dev * std)
            
            return {
                'upper': upper,
                'middle': middle,
                'lower': lower
            }
        except Exception as e:
            return None
    
    def _calculate_price_position(self, current_price: float, high_prices: pd.Series, low_prices: pd.Series) -> float:
        """Fiyat pozisyonunu hesapla (0-100)"""
        try:
            if high_prices.empty or low_prices.empty:
                return 50
            
            max_high = high_prices.max()
            min_low = low_prices.min()
            
            if max_high == min_low:
                return 50
            
            position = ((current_price - min_low) / (max_high - min_low)) * 100
            return max(0, min(100, position))
            
        except Exception as e:
            return 50
    
    def _find_pivot_highs(self, high_prices: pd.Series, window: int = 5) -> List[float]:
        """Pivot yüksekleri bul"""
        try:
            pivot_highs = []
            for i in range(window, len(high_prices) - window):
                if all(high_prices.iloc[i] > high_prices.iloc[i-j] for j in range(1, window+1)) and \
                   all(high_prices.iloc[i] > high_prices.iloc[i+j] for j in range(1, window+1)):
                    pivot_highs.append(high_prices.iloc[i])
            
            return sorted(pivot_highs, reverse=True)
        except Exception as e:
            return []
    
    def _find_pivot_lows(self, low_prices: pd.Series, window: int = 5) -> List[float]:
        """Pivot düşükleri bul"""
        try:
            pivot_lows = []
            for i in range(window, len(low_prices) - window):
                if all(low_prices.iloc[i] < low_prices.iloc[i-j] for j in range(1, window+1)) and \
                   all(low_prices.iloc[i] < low_prices.iloc[i+j] for j in range(1, window+1)):
                    pivot_lows.append(low_prices.iloc[i])
            
            return sorted(pivot_lows)
        except Exception as e:
            return []
    
    def _calculate_trend_duration(self, prices: pd.Series) -> int:
        """Trend süresini hesapla (gün)"""
        try:
            if len(prices) < 2:
                return 0
            
            current_price = prices.iloc[-1]
            trend_start = 0
            
            for i in range(len(prices) - 2, -1, -1):
                if (current_price > prices.iloc[0] and prices.iloc[i] > prices.iloc[i+1]) or \
                   (current_price < prices.iloc[0] and prices.iloc[i] < prices.iloc[i+1]):
                    trend_start = i
                    break
            
            return len(prices) - 1 - trend_start
            
        except Exception as e:
            return 0
    
    def _calculate_trend_consistency(self, prices: pd.Series) -> float:
        """Trend tutarlılığını hesapla (0-1)"""
        try:
            if len(prices) < 10:
                return 0.5
            
            # Son 10 günün trend tutarlılığı
            recent_prices = prices.tail(10)
            consistent_moves = 0
            
            for i in range(1, len(recent_prices)):
                if (recent_prices.iloc[i] > recent_prices.iloc[i-1] and recent_prices.iloc[-1] > recent_prices.iloc[0]) or \
                   (recent_prices.iloc[i] < recent_prices.iloc[i-1] and recent_prices.iloc[-1] < recent_prices.iloc[0]):
                    consistent_moves += 1
            
            return consistent_moves / (len(recent_prices) - 1)
            
        except Exception as e:
            return 0.5
    
    def _check_trend_alignment(self, timeframe_analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Trend uyumunu kontrol et"""
        try:
            bullish_count = 0
            bearish_count = 0
            total_timeframes = len(timeframe_analyses)
            
            for timeframe, analysis in timeframe_analyses.items():
                trend_analysis = analysis.get('trend_analysis', {})
                direction = trend_analysis.get('direction', 'neutral')
                
                if direction == 'up':
                    bullish_count += 1
                elif direction == 'down':
                    bearish_count += 1
            
            alignment_strength = max(bullish_count, bearish_count) / total_timeframes if total_timeframes > 0 else 0
            
            return {
                'bullish_timeframes': bullish_count,
                'bearish_timeframes': bearish_count,
                'alignment_strength': alignment_strength,
                'consensus': 'bullish' if bullish_count > bearish_count else ('bearish' if bearish_count > bullish_count else 'mixed')
            }
            
        except Exception as e:
            return {}
    
    def _check_signal_alignment(self, timeframe_analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Sinyal uyumunu kontrol et"""
        try:
            bullish_signals = 0
            bearish_signals = 0
            total_signals = 0
            
            for timeframe, analysis in timeframe_analyses.items():
                technical_analysis = analysis.get('technical_analysis', {})
                
                # RSI sinyali
                rsi = technical_analysis.get('rsi', {})
                if rsi.get('signal') == 'oversold':
                    bullish_signals += 1
                    total_signals += 1
                elif rsi.get('signal') == 'overbought':
                    bearish_signals += 1
                    total_signals += 1
                
                # MACD sinyali
                macd = technical_analysis.get('macd', {})
                if macd.get('signal') == 'bullish':
                    bullish_signals += 1
                    total_signals += 1
                elif macd.get('signal') == 'bearish':
                    bearish_signals += 1
                    total_signals += 1
            
            signal_strength = max(bullish_signals, bearish_signals) / total_signals if total_signals > 0 else 0
            
            return {
                'bullish_signals': bullish_signals,
                'bearish_signals': bearish_signals,
                'signal_strength': signal_strength,
                'consensus': 'bullish' if bullish_signals > bearish_signals else ('bearish' if bearish_signals > bullish_signals else 'mixed')
            }
            
        except Exception as e:
            return {}
    
    def _analyze_timeframe_hierarchy(self, timeframe_analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Zaman dilimi hiyerarşisi analizi"""
        try:
            # Uzun vadeli trend (1w, 1M)
            long_term_trends = []
            for tf in ['1w', '1M']:
                if tf in timeframe_analyses:
                    trend = timeframe_analyses[tf].get('trend_analysis', {}).get('direction', 'neutral')
                    long_term_trends.append(trend)
            
            # Orta vadeli trend (1d, 4h)
            medium_term_trends = []
            for tf in ['1d', '4h']:
                if tf in timeframe_analyses:
                    trend = timeframe_analyses[tf].get('trend_analysis', {}).get('direction', 'neutral')
                    medium_term_trends.append(trend)
            
            # Kısa vadeli trend (1h, 15m)
            short_term_trends = []
            for tf in ['1h', '15m']:
                if tf in timeframe_analyses:
                    trend = timeframe_analyses[tf].get('trend_analysis', {}).get('direction', 'neutral')
                    short_term_trends.append(trend)
            
            return {
                'long_term_trends': long_term_trends,
                'medium_term_trends': medium_term_trends,
                'short_term_trends': short_term_trends,
                'hierarchy_alignment': self._check_hierarchy_alignment(long_term_trends, medium_term_trends, short_term_trends)
            }
            
        except Exception as e:
            return {}
    
    def _check_hierarchy_alignment(self, long_term: List[str], medium_term: List[str], short_term: List[str]) -> str:
        """Hiyerarşi uyumunu kontrol et"""
        try:
            # En yaygın trend yönlerini bul
            long_consensus = max(set(long_term), key=long_term.count) if long_term else 'neutral'
            medium_consensus = max(set(medium_term), key=medium_term.count) if medium_term else 'neutral'
            short_consensus = max(set(short_term), key=short_term.count) if short_term else 'neutral'
            
            # Tüm seviyeler aynı yönde mi?
            if long_consensus == medium_consensus == short_consensus:
                return 'perfect_alignment'
            elif long_consensus == medium_consensus or medium_consensus == short_consensus:
                return 'partial_alignment'
            else:
                return 'no_alignment'
                
        except Exception as e:
            return 'no_alignment'
    
    def _assess_overall_timeframe(self, timeframe_analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Genel timeframe değerlendirmesi"""
        try:
            total_score = 0
            total_weight = 0
            
            # Zaman dilimi ağırlıkları
            timeframe_weights = {
                '1M': 0.3, '1w': 0.25, '1d': 0.2, '4h': 0.15, '1h': 0.1
            }
            
            for timeframe, analysis in timeframe_analyses.items():
                weight = timeframe_weights.get(timeframe, 0.05)
                
                # Temel analiz skoru
                basic_analysis = analysis.get('basic_analysis', {})
                price_change = basic_analysis.get('price_change_pct', 0)
                
                # Trend analiz skoru
                trend_analysis = analysis.get('trend_analysis', {})
                direction = trend_analysis.get('direction', 'neutral')
                trend_score = 70 if direction == 'up' else (30 if direction == 'down' else 50)
                
                # Teknik analiz skoru
                technical_analysis = analysis.get('technical_analysis', {})
                technical_score = self._calculate_technical_score(technical_analysis)
                
                # Ortalama skor
                avg_score = (trend_score + technical_score) / 2
                
                total_score += avg_score * weight
                total_weight += weight
            
            overall_score = total_score / total_weight if total_weight > 0 else 50
            
            return {
                'overall_score': overall_score,
                'recommendation': 'buy' if overall_score > 60 else ('sell' if overall_score < 40 else 'hold'),
                'confidence': min(1.0, abs(overall_score - 50) / 50),
                'timeframe_count': len(timeframe_analyses)
            }
            
        except Exception as e:
            return {}
    
    def _calculate_technical_score(self, technical_analysis: Dict[str, Any]) -> float:
        """Teknik analiz skoru hesapla"""
        try:
            score = 50  # Başlangıç skoru
            
            # RSI skoru
            rsi = technical_analysis.get('rsi', {})
            rsi_value = rsi.get('value', 50)
            if rsi_value > 70:
                score -= 10  # Aşırı alım
            elif rsi_value < 30:
                score += 10  # Aşırı satım
            elif 40 < rsi_value < 60:
                score += 5  # Nötr pozitif
            
            # MACD skoru
            macd = technical_analysis.get('macd', {})
            if macd.get('signal') == 'bullish':
                score += 10
            elif macd.get('signal') == 'bearish':
                score -= 10
            
            # SMA skoru
            sma_signals = technical_analysis.get('sma_signals', {})
            if sma_signals.get('price_vs_sma20') == 'above' and sma_signals.get('price_vs_sma50') == 'above':
                score += 10
            elif sma_signals.get('price_vs_sma20') == 'below' and sma_signals.get('price_vs_sma50') == 'below':
                score -= 10
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50
    
    def _calculate_consensus_strength(self, timeframe_analyses: Dict[str, Any]) -> float:
        """Konsensüs gücünü hesapla"""
        try:
            if not timeframe_analyses:
                return 0.0
            
            scores = []
            for analysis in timeframe_analyses.values():
                overall_assessment = analysis.get('overall_assessment', {})
                score = overall_assessment.get('overall_score', 50)
                scores.append(score)
            
            if not scores:
                return 0.0
            
            # Standart sapma ile konsensüs ölçümü
            mean_score = np.mean(scores)
            std_score = np.std(scores)
            
            # Düşük standart sapma = yüksek konsensüs
            consensus = 1.0 - (std_score / 50) if std_score < 50 else 0.0
            return max(0.0, min(1.0, consensus))
            
        except Exception as e:
            return 0.0

# Global multi-timeframe charts instance
multi_timeframe_charts = MultiTimeframeCharts()

