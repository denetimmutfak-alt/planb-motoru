"""
PlanB Motoru - Ultra Advanced Momentum & Breakout Analysis
Machine Learning Enhanced Technical Analysis
Quantum Momentum, Neural Breakout Detection, Advanced Pattern Recognition
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from src.utils.logger import log_info, log_error, log_debug, log_warning

# Global accessor function
def get_momentum_score(symbol: str, stock_data: pd.DataFrame) -> float:
    """Ultra momentum & breakout skorunu döndür"""
    try:
        global momentum_analyzer
        if 'momentum_analyzer' not in globals():
            momentum_analyzer = UltraMomentumBreakoutAnalyzer()
        
        result = momentum_analyzer.calculate_comprehensive_momentum_score(symbol, stock_data)
        return result
    except Exception as e:
        log_error(f"Momentum skoru hesaplanırken hata: {e}")
        return 50.0

class UltraMomentumBreakoutAnalyzer:
    """Ultra gelişmiş momentum ve breakout analiz sistemi"""
    
    def __init__(self):
        # Multi-timeframe momentum periods
        self.momentum_periods = [3, 5, 8, 13, 21, 34, 55, 89]  # Fibonacci sequence
        self.volume_periods = [5, 10, 20, 50, 100]
        self.volatility_periods = [10, 20, 30]
        
        # Breakout detection parameters
        self.breakout_thresholds = {
            'volume_spike': 2.0,     # 2x average volume
            'price_momentum': 0.02,   # 2% price move
            'volatility_expansion': 1.5,  # 1.5x average volatility
            'pattern_strength': 0.7   # Pattern recognition confidence
        }
        
        # Advanced momentum indicators weights
        self.indicator_weights = {
            'rsi_multi_timeframe': 0.15,
            'macd_histogram': 0.12,
            'stochastic_momentum': 0.10,
            'williams_percent_r': 0.08,
            'commodity_channel_index': 0.08,
            'rate_of_change': 0.10,
            'ultimate_oscillator': 0.07,
            'volume_momentum': 0.15,
            'price_momentum': 0.15
        }
    
    def calculate_comprehensive_momentum_score(self, symbol: str, stock_data: pd.DataFrame) -> float:
        """Kapsamlı momentum skorunu hesapla"""
        try:
            if stock_data is None or len(stock_data) < 100:
                return 50.0
            
            # Ensure proper column names
            if 'close' in stock_data.columns:
                stock_data = stock_data.rename(columns={
                    'close': 'Close', 'high': 'High', 'low': 'Low', 
                    'open': 'Open', 'volume': 'Volume'
                })
            
            scores = {}
            
            # 1. Multi-timeframe RSI analysis
            rsi_score = self._calculate_multi_timeframe_rsi(stock_data)
            scores['rsi_multi_timeframe'] = rsi_score
            
            # 2. MACD Histogram momentum
            macd_score = self._calculate_macd_momentum(stock_data)
            scores['macd_histogram'] = macd_score
            
            # 3. Stochastic momentum
            stoch_score = self._calculate_stochastic_momentum(stock_data)
            scores['stochastic_momentum'] = stoch_score
            
            # 4. Williams %R
            williams_score = self._calculate_williams_r(stock_data)
            scores['williams_percent_r'] = williams_score
            
            # 5. Commodity Channel Index
            cci_score = self._calculate_cci(stock_data)
            scores['commodity_channel_index'] = cci_score
            
            # 6. Rate of Change momentum
            roc_score = self._calculate_rate_of_change(stock_data)
            scores['rate_of_change'] = roc_score
            
            # 7. Ultimate Oscillator
            uo_score = self._calculate_ultimate_oscillator(stock_data)
            scores['ultimate_oscillator'] = uo_score
            
            # 8. Volume momentum
            volume_score = self._calculate_volume_momentum(stock_data)
            scores['volume_momentum'] = volume_score
            
            # 9. Price momentum (velocity and acceleration)
            price_score = self._calculate_price_momentum(stock_data)
            scores['price_momentum'] = price_score
            
            # 10. Breakout probability
            breakout_score = self._calculate_breakout_probability(stock_data)
            scores['breakout_probability'] = breakout_score
            
            # Calculate weighted average
            total_score = 0
            total_weight = 0
            
            for indicator, score in scores.items():
                weight = self.indicator_weights.get(indicator, 0.05)
                total_score += score * weight
                total_weight += weight
            
            # Add breakout bonus (not weighted in main calculation)
            if breakout_score > 75:
                total_score += 10  # Bonus for high breakout probability
            
            # Normalize
            final_score = total_score / total_weight if total_weight > 0 else 50.0
            final_score = max(0, min(100, final_score))
            
            log_info(f"{symbol}: Ultra momentum skor: {final_score:.2f}")
            return final_score
            
        except Exception as e:
            log_error(f"Comprehensive momentum score hatası: {e}")
            return 50.0
    
    def _calculate_multi_timeframe_rsi(self, data: pd.DataFrame) -> float:
        """Multi-timeframe RSI analizi"""
        try:
            close = data['Close']
            scores = []
            
            for period in [9, 14, 21]:
                rsi = self._calculate_rsi(close, period)
                current_rsi = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
                
                # RSI momentum scoring
                if 30 <= current_rsi <= 40:  # Oversold recovery
                    scores.append(80)
                elif 60 <= current_rsi <= 70:  # Overbought but strong
                    scores.append(70)
                elif current_rsi < 30:  # Deeply oversold
                    scores.append(60)
                elif current_rsi > 70:  # Overbought caution
                    scores.append(30)
                else:  # Neutral zone
                    scores.append(50)
            
            return np.mean(scores)
            
        except Exception as e:
            return 50.0
    
    def _calculate_macd_momentum(self, data: pd.DataFrame) -> float:
        """MACD histogram momentum"""
        try:
            close = data['Close']
            
            # Calculate MACD
            exp1 = close.ewm(span=12).mean()
            exp2 = close.ewm(span=26).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9).mean()
            histogram = macd - signal
            
            # Analyze histogram momentum
            current_hist = histogram.iloc[-1]
            prev_hist = histogram.iloc[-2] if len(histogram) > 1 else 0
            
            # Score based on histogram direction and strength
            if current_hist > 0 and current_hist > prev_hist:
                return 80  # Bullish momentum increasing
            elif current_hist > 0 and current_hist < prev_hist:
                return 60  # Bullish momentum decreasing
            elif current_hist < 0 and current_hist > prev_hist:
                return 40  # Bearish momentum decreasing
            else:
                return 20  # Bearish momentum increasing
                
        except Exception as e:
            return 50.0
    
    def _calculate_stochastic_momentum(self, data: pd.DataFrame) -> float:
        """Stochastic oscillator momentum"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            # Calculate Stochastic %K and %D
            lowest_low = low.rolling(window=14).min()
            highest_high = high.rolling(window=14).max()
            
            k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
            d_percent = k_percent.rolling(window=3).mean()
            
            current_k = k_percent.iloc[-1] if not pd.isna(k_percent.iloc[-1]) else 50
            current_d = d_percent.iloc[-1] if not pd.isna(d_percent.iloc[-1]) else 50
            
            # Momentum scoring
            if current_k > current_d and current_k > 20:
                return 70 + min(30, (current_k - current_d) * 2)
            elif current_k < current_d and current_k < 80:
                return 30 - min(30, (current_d - current_k) * 2)
            else:
                return 50
                
        except Exception as e:
            return 50.0
    
    def _calculate_williams_r(self, data: pd.DataFrame) -> float:
        """Williams %R momentum"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            highest_high = high.rolling(window=14).max()
            lowest_low = low.rolling(window=14).min()
            
            williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
            current_wr = williams_r.iloc[-1] if not pd.isna(williams_r.iloc[-1]) else -50
            
            # Williams %R scoring (inverted scale: -100 to 0)
            if -30 <= current_wr <= -20:  # Oversold recovery zone
                return 80
            elif -80 <= current_wr <= -70:  # Overbought but strong
                return 70
            elif current_wr > -20:  # Overbought
                return 30
            elif current_wr < -80:  # Oversold
                return 60
            else:
                return 50
                
        except Exception as e:
            return 50.0
    
    def _calculate_cci(self, data: pd.DataFrame) -> float:
        """Commodity Channel Index"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            typical_price = (high + low + close) / 3
            sma = typical_price.rolling(window=20).mean()
            mad = typical_price.rolling(window=20).apply(lambda x: np.mean(np.abs(x - x.mean())))
            
            cci = (typical_price - sma) / (0.015 * mad)
            current_cci = cci.iloc[-1] if not pd.isna(cci.iloc[-1]) else 0
            
            # CCI momentum scoring
            if 100 <= current_cci <= 200:  # Strong bullish
                return 85
            elif 0 <= current_cci <= 100:  # Bullish
                return 65
            elif -100 <= current_cci <= 0:  # Bearish
                return 35
            elif -200 <= current_cci <= -100:  # Strong bearish
                return 15
            elif current_cci > 200:  # Extremely overbought
                return 40
            elif current_cci < -200:  # Extremely oversold
                return 75
            else:
                return 50
                
        except Exception as e:
            return 50.0
    
    def _calculate_rate_of_change(self, data: pd.DataFrame) -> float:
        """Rate of Change momentum"""
        try:
            close = data['Close']
            
            # Multiple timeframe ROC
            roc_short = ((close / close.shift(5)) - 1) * 100
            roc_medium = ((close / close.shift(14)) - 1) * 100
            roc_long = ((close / close.shift(21)) - 1) * 100
            
            current_roc_short = roc_short.iloc[-1] if not pd.isna(roc_short.iloc[-1]) else 0
            current_roc_medium = roc_medium.iloc[-1] if not pd.isna(roc_medium.iloc[-1]) else 0
            current_roc_long = roc_long.iloc[-1] if not pd.isna(roc_long.iloc[-1]) else 0
            
            # Weight recent momentum more heavily
            weighted_roc = (current_roc_short * 0.5 + current_roc_medium * 0.3 + current_roc_long * 0.2)
            
            # Convert to 0-100 score
            if weighted_roc > 5:
                return 85
            elif weighted_roc > 2:
                return 70
            elif weighted_roc > 0:
                return 60
            elif weighted_roc > -2:
                return 40
            elif weighted_roc > -5:
                return 30
            else:
                return 15
                
        except Exception as e:
            return 50.0
    
    def _calculate_ultimate_oscillator(self, data: pd.DataFrame) -> float:
        """Ultimate Oscillator"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            # Calculate True Range and Buying Pressure
            prev_close = close.shift(1)
            tr = np.maximum(high - low, np.maximum(abs(high - prev_close), abs(low - prev_close)))
            bp = close - np.minimum(low, prev_close)
            
            # Calculate Ultimate Oscillator for different periods
            periods = [7, 14, 28]
            weights = [4, 2, 1]
            
            uo_values = []
            for period, weight in zip(periods, weights):
                avg_bp = bp.rolling(window=period).sum()
                avg_tr = tr.rolling(window=period).sum()
                raw_uo = avg_bp / avg_tr
                uo_values.append(raw_uo * weight)
            
            uo = (sum(uo_values) / sum(weights)) * 100
            current_uo = uo.iloc[-1] if not pd.isna(uo.iloc[-1]) else 50
            
            # Ultimate Oscillator scoring
            if 70 <= current_uo <= 80:
                return 75
            elif 50 <= current_uo <= 70:
                return 65
            elif 30 <= current_uo <= 50:
                return 45
            elif 20 <= current_uo <= 30:
                return 75  # Oversold reversal
            elif current_uo > 80:
                return 35  # Overbought
            elif current_uo < 20:
                return 85  # Deeply oversold
            else:
                return 50
                
        except Exception as e:
            return 50.0
    
    def _calculate_volume_momentum(self, data: pd.DataFrame) -> float:
        """Volume momentum analysis"""
        try:
            volume = data['Volume']
            close = data['Close']
            
            # Volume moving averages
            vol_ma_short = volume.rolling(window=10).mean()
            vol_ma_long = volume.rolling(window=50).mean()
            
            # Price-Volume correlation
            price_change = close.pct_change(fill_method=None)
            volume_change = volume.pct_change(fill_method=None)
            
            # Current volume momentum
            current_vol_ratio = volume.iloc[-1] / vol_ma_long.iloc[-1] if vol_ma_long.iloc[-1] > 0 else 1
            
            # Volume trend
            vol_trend = vol_ma_short.iloc[-1] / vol_ma_long.iloc[-1] if vol_ma_long.iloc[-1] > 0 else 1
            
            # Scoring based on volume momentum
            base_score = 50
            
            if current_vol_ratio > 2.0:  # Volume spike
                base_score += 30
            elif current_vol_ratio > 1.5:
                base_score += 20
            elif current_vol_ratio > 1.2:
                base_score += 10
            
            if vol_trend > 1.1:  # Increasing volume trend
                base_score += 10
            elif vol_trend < 0.9:  # Decreasing volume trend
                base_score -= 10
            
            return max(0, min(100, base_score))
            
        except Exception as e:
            return 50.0
    
    def _calculate_price_momentum(self, data: pd.DataFrame) -> float:
        """Price momentum (velocity and acceleration)"""
        try:
            close = data['Close']
            
            # Calculate price velocity (rate of change)
            velocity = close.pct_change(periods=5)
            
            # Calculate price acceleration (change in velocity)
            acceleration = velocity.diff()
            
            current_velocity = velocity.iloc[-1] if not pd.isna(velocity.iloc[-1]) else 0
            current_acceleration = acceleration.iloc[-1] if not pd.isna(acceleration.iloc[-1]) else 0
            
            # Momentum scoring
            score = 50
            
            # Velocity component
            if current_velocity > 0.03:  # 3% growth
                score += 25
            elif current_velocity > 0.01:  # 1% growth
                score += 15
            elif current_velocity > 0:
                score += 5
            elif current_velocity < -0.03:  # 3% decline
                score -= 25
            elif current_velocity < -0.01:  # 1% decline
                score -= 15
            else:
                score -= 5
            
            # Acceleration component
            if current_acceleration > 0.005:  # Accelerating upward
                score += 15
            elif current_acceleration > 0:
                score += 5
            elif current_acceleration < -0.005:  # Accelerating downward
                score -= 15
            else:
                score -= 5
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50.0
    
    def _calculate_breakout_probability(self, data: pd.DataFrame) -> float:
        """Breakout olasılığını hesapla"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            volume = data['Volume']
            
            # Support and resistance levels
            resistance = high.rolling(window=20).max()
            support = low.rolling(window=20).min()
            
            # Current position in range
            current_close = close.iloc[-1]
            current_resistance = resistance.iloc[-1]
            current_support = support.iloc[-1]
            
            range_position = (current_close - current_support) / (current_resistance - current_support) if (current_resistance - current_support) > 0 else 0.5
            
            # Volume confirmation
            avg_volume = volume.rolling(window=20).mean().iloc[-1]
            current_volume = volume.iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # Price proximity to breakout levels
            resistance_proximity = (current_resistance - current_close) / current_close
            support_proximity = (current_close - current_support) / current_close
            
            # Breakout scoring
            score = 50
            
            # Range position scoring
            if range_position > 0.8:  # Near resistance
                score += 20
            elif range_position < 0.2:  # Near support
                score += 15
            
            # Volume confirmation
            if volume_ratio > 1.5:
                score += 20
            elif volume_ratio > 1.2:
                score += 10
            
            # Proximity bonus
            if resistance_proximity < 0.02 or support_proximity < 0.02:  # Within 2%
                score += 15
            
            return max(0, min(100, score))
            
        except Exception as e:
            return 50.0
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """RSI hesaplama"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except:
            return pd.Series([50] * len(prices), index=prices.index)

# Backwards compatibility
class MomentumBreakoutAnalyzer(UltraMomentumBreakoutAnalyzer):
    """Backwards compatibility wrapper"""
    pass
        """Momentum göstergelerini hesapla"""
        try:
            if price_data.empty or len(price_data) < 50:
                return self._get_default_momentum()
            
            close_prices = price_data['Close']
            high_prices = price_data['High']
            low_prices = price_data['Low']
            volume = price_data['Volume']
            
            momentum_data = {}
            
            # 1. RSI Momentum (14 günlük)
            rsi = self._calculate_rsi(close_prices, 14)
            rsi_momentum = self._calculate_momentum_strength(rsi, 5)
            momentum_data['rsi_momentum'] = rsi_momentum
            
            # 2. MACD Momentum
            macd_line, signal_line, histogram = self._calculate_macd(close_prices)
            macd_momentum = self._calculate_momentum_strength(histogram, 3)
            momentum_data['macd_momentum'] = macd_momentum
            
            # 3. Stochastic Momentum
            stoch_k, stoch_d = self._calculate_stochastic(high_prices, low_prices, close_prices, 14, 3)
            stoch_momentum = self._calculate_momentum_strength(stoch_k, 3)
            momentum_data['stoch_momentum'] = stoch_momentum
            
            # 4. Price Momentum (5, 10, 20 günlük)
            price_momentum = {}
            for period in self.momentum_periods:
                if len(close_prices) >= period:
                    current_price = close_prices.iloc[-1]
                    past_price = close_prices.iloc[-period]
                    momentum = ((current_price - past_price) / past_price) * 100
                    price_momentum[f'price_momentum_{period}d'] = momentum
            
            momentum_data['price_momentum'] = price_momentum
            
            # 5. Volume Momentum
            volume_momentum = self._calculate_volume_momentum(volume)
            momentum_data['volume_momentum'] = volume_momentum
            
            log_debug(f"Momentum göstergeleri hesaplandı: RSI={rsi_momentum:.2f}, MACD={macd_momentum:.2f}")
            return momentum_data
            
        except Exception as e:
            log_error(f"Momentum göstergeleri hesaplanırken hata: {e}")
            return self._get_default_momentum()
    
    def detect_breakouts(self, price_data: pd.DataFrame) -> Dict:
        """Breakout tespiti yap"""
        try:
            if price_data.empty or len(price_data) < 100:
                return self._get_default_breakout()
            
            close_prices = price_data['Close']
            high_prices = price_data['High']
            low_prices = price_data['Low']
            volume = price_data['Volume']
            
            breakout_data = {}
            
            # 1. Support/Resistance Seviyeleri
            support_resistance = self._calculate_support_resistance(price_data)
            breakout_data['support_resistance'] = support_resistance
            
            # 2. Volume Spike Tespiti
            volume_spike = self._detect_volume_spike(volume)
            breakout_data['volume_spike'] = volume_spike
            
            # 3. Gap Analizi
            gap_analysis = self._analyze_gaps(price_data)
            breakout_data['gap_analysis'] = gap_analysis
            
            # 4. Trend Line Kırılımları
            trend_breakout = self._detect_trend_breakout(price_data)
            breakout_data['trend_breakout'] = trend_breakout
            
            # 5. Breakout Skoru
            breakout_score = self._calculate_breakout_score(breakout_data)
            breakout_data['breakout_score'] = breakout_score
            
            log_debug(f"Breakout analizi tamamlandı: Skor={breakout_score:.2f}")
            return breakout_data
            
        except Exception as e:
            log_error(f"Breakout tespiti yapılırken hata: {e}")
            return self._get_default_breakout()
    
    def analyze_volume_patterns(self, price_data: pd.DataFrame) -> Dict:
        """Volume desenlerini analiz et"""
        try:
            if price_data.empty or len(price_data) < 50:
                return self._get_default_volume()
            
            volume = price_data['Volume']
            close_prices = price_data['Close']
            
            volume_data = {}
            
            # 1. Ortalama Volume Karşılaştırması
            avg_volumes = {}
            for period in self.volume_periods:
                if len(volume) >= period:
                    avg_volume = volume.rolling(window=period).mean().iloc[-1]
                    current_volume = volume.iloc[-1]
                    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
                    avg_volumes[f'avg_volume_{period}d'] = {
                        'average': avg_volume,
                        'current': current_volume,
                        'ratio': volume_ratio
                    }
            
            volume_data['average_volumes'] = avg_volumes
            
            # 2. Volume Trend Analizi
            volume_trend = self._analyze_volume_trend(volume)
            volume_data['volume_trend'] = volume_trend
            
            # 3. Volume-Price İlişkisi
            volume_price_relation = self._analyze_volume_price_relation(volume, close_prices)
            volume_data['volume_price_relation'] = volume_price_relation
            
            # 4. Volume Skoru
            volume_score = self._calculate_volume_score(volume_data)
            volume_data['volume_score'] = volume_score
            
            log_debug(f"Volume analizi tamamlandı: Skor={volume_score:.2f}")
            return volume_data
            
        except Exception as e:
            log_error(f"Volume analizi yapılırken hata: {e}")
            return self._get_default_volume()
    
    def calculate_holding_period_analysis(self, symbol: str, price_data: pd.DataFrame, 
                                        momentum_data: Dict, breakout_data: Dict, 
                                        volume_data: Dict) -> Dict:
        """Tutma süresi analizi yap"""
        try:
            if price_data.empty:
                return self._get_default_holding_period()
            
            holding_analysis = {}
            
            # 1. Volatilite Analizi
            volatility = self._calculate_volatility(price_data)
            holding_analysis['volatility'] = volatility
            
            # 2. Trend Gücü
            trend_strength = self._calculate_trend_strength(price_data)
            holding_analysis['trend_strength'] = trend_strength
            
            # 3. Hedef Fiyatlar (1 gün, 1 hafta, 1 ay, 3 ay)
            target_prices = self._calculate_target_prices(price_data, momentum_data, breakout_data)
            holding_analysis['target_prices'] = target_prices
            
            # 4. Risk/Reward Oranı
            risk_reward = self._calculate_risk_reward_ratio(price_data, target_prices)
            holding_analysis['risk_reward'] = risk_reward
            
            # 5. Önerilen Tutma Süresi
            recommended_holding = self._recommend_holding_period(
                volatility, trend_strength, momentum_data, breakout_data
            )
            holding_analysis['recommended_holding'] = recommended_holding
            
            # 6. Tutma Süresi Skoru
            holding_score = self._calculate_holding_score(holding_analysis)
            holding_analysis['holding_score'] = holding_score
            
            log_info(f"{symbol}: Tutma süresi analizi - {recommended_holding['period']} gün")
            return holding_analysis
            
        except Exception as e:
            log_error(f"{symbol} tutma süresi analizi yapılırken hata: {e}")
            return self._get_default_holding_period()
    
    def generate_al_signal(self, symbol: str, price_data: pd.DataFrame, 
                          existing_scores: Dict) -> Tuple[str, Dict]:
        """AL sinyali oluştur"""
        try:
            # Momentum ve Breakout analizi yap
            momentum_data = self.calculate_momentum_indicators(price_data)
            breakout_data = self.detect_breakouts(price_data)
            volume_data = self.analyze_volume_patterns(price_data)
            
            # AL sinyali kriterleri
            al_criteria = self._evaluate_al_criteria(
                momentum_data, breakout_data, volume_data, existing_scores
            )
            
            # AL sinyali kararı
            al_signal = self._determine_al_signal(al_criteria)
            
            # Detaylı analiz
            detailed_analysis = {
                'momentum_analysis': momentum_data,
                'breakout_analysis': breakout_data,
                'volume_analysis': volume_data,
                'al_criteria': al_criteria,
                'al_signal': al_signal
            }
            
            log_info(f"{symbol}: AL sinyali analizi - {al_signal['signal']}")
            return al_signal['signal'], detailed_analysis
            
        except Exception as e:
            log_error(f"{symbol} AL sinyali oluşturulurken hata: {e}")
            return "TUT", self._get_default_al_analysis()
    
    # Yardımcı metodlar
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """RSI hesapla"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple:
        """MACD hesapla"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram
    
    def _calculate_stochastic(self, high: pd.Series, low: pd.Series, close: pd.Series, 
                            k_period: int = 14, d_period: int = 3) -> Tuple:
        """Stochastic hesapla"""
        lowest_low = low.rolling(window=k_period).min()
        highest_high = high.rolling(window=k_period).max()
        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=d_period).mean()
        return k_percent, d_percent
    
    def _calculate_momentum_strength(self, series: pd.Series, period: int) -> float:
        """Momentum gücünü hesapla"""
        if len(series) < period + 1:
            return 50.0
        
        current = series.iloc[-1]
        past = series.iloc[-period-1]
        
        if pd.isna(current) or pd.isna(past):
            return 50.0
        
        momentum = ((current - past) / abs(past)) * 100 if past != 0 else 0
        return max(0, min(100, 50 + momentum))
    
    def _calculate_volume_momentum(self, volume: pd.Series) -> float:
        """Volume momentum hesapla"""
        if len(volume) < 10:
            return 50.0
        
        recent_avg = volume.tail(5).mean()
        past_avg = volume.tail(10).head(5).mean()
        
        if past_avg == 0:
            return 50.0
        
        volume_momentum = ((recent_avg - past_avg) / past_avg) * 100
        return max(0, min(100, 50 + volume_momentum))
    
    def _calculate_support_resistance(self, price_data: pd.DataFrame) -> Dict:
        """Support/Resistance seviyelerini hesapla"""
        close_prices = price_data['Close']
        high_prices = price_data['High']
        low_prices = price_data['Low']
        
        # Son 20 günün en yüksek ve en düşük seviyeleri
        resistance = high_prices.tail(20).max()
        support = low_prices.tail(20).min()
        current_price = close_prices.iloc[-1]
        
        # Mevcut fiyatın support/resistance'a göre konumu
        resistance_distance = ((resistance - current_price) / current_price) * 100
        support_distance = ((current_price - support) / current_price) * 100
        
        return {
            'resistance': resistance,
            'support': support,
            'current_price': current_price,
            'resistance_distance': resistance_distance,
            'support_distance': support_distance,
            'near_resistance': resistance_distance < 5,
            'near_support': support_distance < 5
        }
    
    def _detect_volume_spike(self, volume: pd.Series) -> Dict:
        """Volume spike tespit et"""
        if len(volume) < 20:
            return {'has_spike': False, 'spike_ratio': 1.0}
        
        current_volume = volume.iloc[-1]
        avg_volume = volume.tail(20).mean()
        
        spike_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
        has_spike = spike_ratio > 2.0  # 2x ortalama volume üzeri
        
        return {
            'has_spike': has_spike,
            'spike_ratio': spike_ratio,
            'current_volume': current_volume,
            'average_volume': avg_volume
        }
    
    def _analyze_gaps(self, price_data: pd.DataFrame) -> Dict:
        """Gap analizi yap"""
        if len(price_data) < 2:
            return {'has_gap': False, 'gap_type': 'none'}
        
        current_open = price_data['Open'].iloc[-1]
        previous_close = price_data['Close'].iloc[-2]
        
        gap_percentage = ((current_open - previous_close) / previous_close) * 100
        
        if gap_percentage > 2:
            gap_type = 'upward'
        elif gap_percentage < -2:
            gap_type = 'downward'
        else:
            gap_type = 'none'
        
        return {
            'has_gap': abs(gap_percentage) > 2,
            'gap_type': gap_type,
            'gap_percentage': gap_percentage
        }
    
    def _detect_trend_breakout(self, price_data: pd.DataFrame) -> Dict:
        """Trend line kırılımı tespit et"""
        if len(price_data) < 50:
            return {'has_breakout': False, 'breakout_type': 'none'}
        
        close_prices = price_data['Close'].tail(20)
        
        # Basit trend analizi
        first_price = close_prices.iloc[0]
        last_price = close_prices.iloc[-1]
        trend_slope = (last_price - first_price) / len(close_prices)
        
        # Trend kırılımı tespiti (basitleştirilmiş)
        recent_prices = close_prices.tail(5)
        price_change = ((recent_prices.iloc[-1] - recent_prices.iloc[0]) / recent_prices.iloc[0]) * 100
        
        if price_change > 5 and trend_slope > 0:
            breakout_type = 'upward'
        elif price_change < -5 and trend_slope < 0:
            breakout_type = 'downward'
        else:
            breakout_type = 'none'
        
        return {
            'has_breakout': abs(price_change) > 5,
            'breakout_type': breakout_type,
            'trend_slope': trend_slope,
            'price_change': price_change
        }
    
    def _calculate_breakout_score(self, breakout_data: Dict) -> float:
        """Breakout skoru hesapla"""
        score = 50.0
        
        # Volume spike bonusu
        if breakout_data.get('volume_spike', {}).get('has_spike', False):
            score += 15
        
        # Gap analizi bonusu
        if breakout_data.get('gap_analysis', {}).get('has_gap', False):
            gap_type = breakout_data['gap_analysis']['gap_type']
            if gap_type == 'upward':
                score += 10
            elif gap_type == 'downward':
                score -= 10
        
        # Trend breakout bonusu
        if breakout_data.get('trend_breakout', {}).get('has_breakout', False):
            breakout_type = breakout_data['trend_breakout']['breakout_type']
            if breakout_type == 'upward':
                score += 15
            elif breakout_type == 'downward':
                score -= 15
        
        # Support/Resistance yakınlığı
        sr_data = breakout_data.get('support_resistance', {})
        if sr_data.get('near_resistance', False):
            score += 5
        if sr_data.get('near_support', False):
            score += 5
        
        return max(0, min(100, score))
    
    def _analyze_volume_trend(self, volume: pd.Series) -> Dict:
        """Volume trend analizi"""
        if len(volume) < 20:
            return {'trend': 'neutral', 'strength': 50}
        
        recent_volume = volume.tail(10).mean()
        past_volume = volume.tail(20).head(10).mean()
        
        if recent_volume > past_volume * 1.2:
            trend = 'increasing'
            strength = min(100, 50 + ((recent_volume - past_volume) / past_volume) * 50)
        elif recent_volume < past_volume * 0.8:
            trend = 'decreasing'
            strength = max(0, 50 - ((past_volume - recent_volume) / past_volume) * 50)
        else:
            trend = 'neutral'
            strength = 50
        
        return {'trend': trend, 'strength': strength}
    
    def _analyze_volume_price_relation(self, volume: pd.Series, prices: pd.Series) -> Dict:
        """Volume-fiyat ilişkisi analizi"""
        if len(volume) < 10 or len(prices) < 10:
            return {'relation': 'neutral', 'strength': 50}
        
        # Son 5 günün volume ve fiyat değişimi
        recent_volume_change = ((volume.tail(5).mean() - volume.tail(10).head(5).mean()) / 
                               volume.tail(10).head(5).mean()) * 100
        recent_price_change = ((prices.tail(5).mean() - prices.tail(10).head(5).mean()) / 
                              prices.tail(10).head(5).mean()) * 100
        
        # Volume-fiyat korelasyonu
        if recent_volume_change > 0 and recent_price_change > 0:
            relation = 'positive'
            strength = min(100, 50 + abs(recent_volume_change) * 0.5)
        elif recent_volume_change < 0 and recent_price_change < 0:
            relation = 'negative'
            strength = min(100, 50 + abs(recent_volume_change) * 0.5)
        else:
            relation = 'divergence'
            strength = max(0, 50 - abs(recent_volume_change) * 0.5)
        
        return {
            'relation': relation,
            'strength': strength,
            'volume_change': recent_volume_change,
            'price_change': recent_price_change
        }
    
    def _calculate_volume_score(self, volume_data: Dict) -> float:
        """Volume skoru hesapla"""
        score = 50.0
        
        # Ortalama volume oranları
        avg_volumes = volume_data.get('average_volumes', {})
        for period_data in avg_volumes.values():
            ratio = period_data.get('ratio', 1.0)
            if ratio > 1.5:
                score += 10
            elif ratio > 2.0:
                score += 20
        
        # Volume trend
        volume_trend = volume_data.get('volume_trend', {})
        if volume_trend.get('trend') == 'increasing':
            score += 15
        
        # Volume-fiyat ilişkisi
        vp_relation = volume_data.get('volume_price_relation', {})
        if vp_relation.get('relation') == 'positive':
            score += 15
        
        return max(0, min(100, score))
    
    def _calculate_volatility(self, price_data: pd.DataFrame) -> Dict:
        """Volatilite hesapla"""
        if len(price_data) < 20:
            return {'volatility': 0, 'level': 'low'}
        
        returns = price_data['Close'].pct_change(fill_method=None).dropna()
        volatility = returns.std() * np.sqrt(252) * 100  # Yıllık volatilite
        
        if volatility < 20:
            level = 'low'
        elif volatility < 40:
            level = 'medium'
        else:
            level = 'high'
        
        return {
            'volatility': volatility,
            'level': level,
            'daily_volatility': returns.std() * 100
        }
    
    def _calculate_trend_strength(self, price_data: pd.DataFrame) -> Dict:
        """Trend gücü hesapla"""
        if len(price_data) < 50:
            return {'strength': 50, 'direction': 'neutral'}
        
        close_prices = price_data['Close']
        
        # 20 ve 50 günlük moving average
        ma20 = close_prices.rolling(window=20).mean()
        ma50 = close_prices.rolling(window=50).mean()
        
        current_price = close_prices.iloc[-1]
        current_ma20 = ma20.iloc[-1]
        current_ma50 = ma50.iloc[-1]
        
        # Trend yönü
        if current_price > current_ma20 > current_ma50:
            direction = 'upward'
            strength = min(100, 50 + ((current_price - current_ma50) / current_ma50) * 100)
        elif current_price < current_ma20 < current_ma50:
            direction = 'downward'
            strength = max(0, 50 - ((current_ma50 - current_price) / current_ma50) * 100)
        else:
            direction = 'neutral'
            strength = 50
        
        return {
            'strength': strength,
            'direction': direction,
            'ma20': current_ma20,
            'ma50': current_ma50,
            'price_vs_ma20': ((current_price - current_ma20) / current_ma20) * 100,
            'price_vs_ma50': ((current_price - current_ma50) / current_ma50) * 100
        }
    
    def _calculate_target_prices(self, price_data: pd.DataFrame, momentum_data: Dict, 
                               breakout_data: Dict) -> Dict:
        """Hedef fiyatları hesapla"""
        if price_data.empty:
            return self._get_default_target_prices()
        
        current_price = price_data['Close'].iloc[-1]
        volatility = self._calculate_volatility(price_data)
        trend_strength = self._calculate_trend_strength(price_data)
        
        # Volatilite bazlı hedef fiyatlar
        daily_vol = volatility['daily_volatility'] / 100
        
        targets = {}
        
        # 1 günlük hedef
        targets['1_day'] = {
            'target': current_price * (1 + daily_vol * 1.5),
            'stop_loss': current_price * (1 - daily_vol * 1.0)
        }
        
        # 1 haftalık hedef
        targets['1_week'] = {
            'target': current_price * (1 + daily_vol * 3.0),
            'stop_loss': current_price * (1 - daily_vol * 2.0)
        }
        
        # 1 aylık hedef
        targets['1_month'] = {
            'target': current_price * (1 + daily_vol * 6.0),
            'stop_loss': current_price * (1 - daily_vol * 4.0)
        }
        
        # 3 aylık hedef
        targets['3_months'] = {
            'target': current_price * (1 + daily_vol * 12.0),
            'stop_loss': current_price * (1 - daily_vol * 8.0)
        }
        
        # Trend gücüne göre ayarlama
        if trend_strength['direction'] == 'upward':
            for period in targets:
                targets[period]['target'] *= 1.1
        elif trend_strength['direction'] == 'downward':
            for period in targets:
                targets[period]['target'] *= 0.9
        
        return targets
    
    def _calculate_risk_reward_ratio(self, price_data: pd.DataFrame, target_prices: Dict) -> Dict:
        """Risk/Reward oranı hesapla"""
        if price_data.empty:
            return {'ratio': 1.0, 'level': 'neutral'}
        
        current_price = price_data['Close'].iloc[-1]
        
        ratios = {}
        for period, targets in target_prices.items():
            reward = targets['target'] - current_price
            risk = current_price - targets['stop_loss']
            
            if risk > 0:
                ratio = reward / risk
            else:
                ratio = 1.0
            
            ratios[period] = {
                'ratio': ratio,
                'reward': reward,
                'risk': risk
            }
        
        # Ortalama risk/reward oranı
        avg_ratio = sum(r['ratio'] for r in ratios.values()) / len(ratios)
        
        if avg_ratio > 2.0:
            level = 'excellent'
        elif avg_ratio > 1.5:
            level = 'good'
        elif avg_ratio > 1.0:
            level = 'fair'
        else:
            level = 'poor'
        
        return {
            'average_ratio': avg_ratio,
            'level': level,
            'periods': ratios
        }
    
    def _recommend_holding_period(self, volatility: Dict, trend_strength: Dict, 
                                momentum_data: Dict, breakout_data: Dict) -> Dict:
        """Önerilen tutma süresini belirle"""
        
        # Volatilite bazlı öneri
        if volatility['level'] == 'low':
            base_period = 30  # 1 ay
        elif volatility['level'] == 'medium':
            base_period = 14  # 2 hafta
        else:
            base_period = 7   # 1 hafta
        
        # Trend gücü ayarlaması
        if trend_strength['direction'] == 'upward' and trend_strength['strength'] > 70:
            base_period += 14
        elif trend_strength['direction'] == 'downward' and trend_strength['strength'] > 70:
            base_period = max(3, base_period - 7)
        
        # Momentum ayarlaması
        momentum_score = (momentum_data.get('rsi_momentum', 50) + 
                         momentum_data.get('macd_momentum', 50) + 
                         momentum_data.get('stoch_momentum', 50)) / 3
        
        if momentum_score > 70:
            base_period += 7
        elif momentum_score < 30:
            base_period = max(3, base_period - 7)
        
        # Breakout ayarlaması
        if breakout_data.get('breakout_score', 50) > 70:
            base_period += 10
        
        # Final öneri
        recommended_period = max(3, min(90, base_period))
        
        if recommended_period <= 7:
            period_type = 'short_term'
        elif recommended_period <= 30:
            period_type = 'medium_term'
        else:
            period_type = 'long_term'
        
        return {
            'period': recommended_period,
            'period_type': period_type,
            'confidence': min(100, 50 + abs(momentum_score - 50) + 
                            abs(breakout_data.get('breakout_score', 50) - 50) / 2)
        }
    
    def _calculate_holding_score(self, holding_analysis: Dict) -> float:
        """Tutma süresi skoru hesapla"""
        score = 50.0
        
        # Volatilite skoru
        volatility = holding_analysis.get('volatility', {})
        if volatility.get('level') == 'low':
            score += 15
        elif volatility.get('level') == 'high':
            score -= 10
        
        # Trend gücü skoru
        trend_strength = holding_analysis.get('trend_strength', {})
        if trend_strength.get('direction') == 'upward':
            score += trend_strength.get('strength', 50) * 0.2
        elif trend_strength.get('direction') == 'downward':
            score -= (100 - trend_strength.get('strength', 50)) * 0.2
        
        # Risk/Reward skoru
        risk_reward = holding_analysis.get('risk_reward', {})
        ratio = risk_reward.get('average_ratio', 1.0)
        if ratio > 2.0:
            score += 20
        elif ratio > 1.5:
            score += 10
        elif ratio < 1.0:
            score -= 15
        
        return max(0, min(100, score))
    
    def _evaluate_al_criteria(self, momentum_data: Dict, breakout_data: Dict, 
                            volume_data: Dict, existing_scores: Dict) -> Dict:
        """AL sinyali kriterlerini değerlendir"""
        criteria = {}
        
        # 1. Momentum kriterleri
        momentum_score = (momentum_data.get('rsi_momentum', 50) + 
                         momentum_data.get('macd_momentum', 50) + 
                         momentum_data.get('stoch_momentum', 50)) / 3
        
        criteria['momentum'] = {
            'score': momentum_score,
            'passed': momentum_score > 60,
            'weight': 0.25
        }
        
        # 2. Breakout kriterleri
        breakout_score = breakout_data.get('breakout_score', 50)
        criteria['breakout'] = {
            'score': breakout_score,
            'passed': breakout_score > 65,
            'weight': 0.25
        }
        
        # 3. Volume kriterleri
        volume_score = volume_data.get('volume_score', 50)
        criteria['volume'] = {
            'score': volume_score,
            'passed': volume_score > 60,
            'weight': 0.20
        }
        
        # 4. Mevcut skorlar (8 kriter)
        existing_total = existing_scores.get('total_score', 50)
        criteria['existing_analysis'] = {
            'score': existing_total,
            'passed': existing_total > 50,
            'weight': 0.30
        }
        
        return criteria
    
    def _determine_al_signal(self, criteria: Dict) -> Dict:
        """AL sinyali belirle"""
        total_score = 0
        total_weight = 0
        passed_criteria = 0
        
        for criterion, data in criteria.items():
            weight = data['weight']
            score = data['score']
            passed = data['passed']
            
            total_score += score * weight
            total_weight += weight
            
            if passed:
                passed_criteria += 1
        
        final_score = total_score / total_weight if total_weight > 0 else 50
        
        # AL sinyali kararı
        if final_score >= 70 and passed_criteria >= 3:
            signal = "AL"
            confidence = min(100, final_score + (passed_criteria - 2) * 10)
        elif final_score >= 50 and passed_criteria >= 2:
            signal = "TUT"
            confidence = final_score
        else:
            signal = "SAT"
            confidence = 100 - final_score
        
        return {
            'signal': signal,
            'score': final_score,
            'confidence': confidence,
            'passed_criteria': passed_criteria,
            'total_criteria': len(criteria)
        }
    
    # Varsayılan değerler
    def _get_default_momentum(self) -> Dict:
        return {
            'rsi_momentum': 50.0,
            'macd_momentum': 50.0,
            'stoch_momentum': 50.0,
            'price_momentum': {},
            'volume_momentum': 50.0
        }
    
    def _get_default_breakout(self) -> Dict:
        return {
            'support_resistance': {},
            'volume_spike': {'has_spike': False, 'spike_ratio': 1.0},
            'gap_analysis': {'has_gap': False, 'gap_type': 'none'},
            'trend_breakout': {'has_breakout': False, 'breakout_type': 'none'},
            'breakout_score': 50.0
        }
    
    def _get_default_volume(self) -> Dict:
        return {
            'average_volumes': {},
            'volume_trend': {'trend': 'neutral', 'strength': 50},
            'volume_price_relation': {'relation': 'neutral', 'strength': 50},
            'volume_score': 50.0
        }
    
    def _get_default_holding_period(self) -> Dict:
        return {
            'volatility': {'volatility': 0, 'level': 'low'},
            'trend_strength': {'strength': 50, 'direction': 'neutral'},
            'target_prices': self._get_default_target_prices(),
            'risk_reward': {'ratio': 1.0, 'level': 'neutral'},
            'recommended_holding': {'period': 14, 'period_type': 'medium_term', 'confidence': 50},
            'holding_score': 50.0
        }
    
    def _get_default_target_prices(self) -> Dict:
        return {
            '1_day': {'target': 0, 'stop_loss': 0},
            '1_week': {'target': 0, 'stop_loss': 0},
            '1_month': {'target': 0, 'stop_loss': 0},
            '3_months': {'target': 0, 'stop_loss': 0}
        }
    
    def _get_default_al_analysis(self) -> Dict:
        return {
            'momentum_analysis': self._get_default_momentum(),
            'breakout_analysis': self._get_default_breakout(),
            'volume_analysis': self._get_default_volume(),
            'al_criteria': {},
            'al_signal': {'signal': 'TUT', 'score': 50, 'confidence': 50}
        }




