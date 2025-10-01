"""
PlanB Motoru - Finansal Analiz Modülü (Düzeltilmiş)
Hephaistos ve Hermes Entegrasyonlu
"""
import pandas as pd
try:
    import pandas_ta as ta
except ImportError:
    ta = None
import numpy as np
from typing import Dict, Optional, Tuple
from src.utils.logger import log_info, log_error, log_debug, log_warning
from config.settings import config
from src.analysis.astrology_analysis import AstrologyAnalyzer
from src.analysis.shemitah_cycle import shemitah_analyzer
from src.analysis.gann_technique import GannTechniqueAnalyzer
from src.analysis.economic_cycle import ultra_economic_analyzer
from src.analysis.volatility_analysis import VolatilityAnalyzer
from src.analysis.risk_analysis import RiskAnalyzer
from src.analysis.options_analysis import OptionsAnalyzer
from src.analysis.currency_analysis import CurrencyAnalyzer
from src.analysis.commodities_analysis import CommoditiesAnalyzer
from src.data.company_founding_dates import CompanyFoundingDates

class FinancialAnalyzer:
    def calculate_technical_indicators(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Fiyat verisi DataFrame'i üzerinden profesyonel teknik analiz göstergeleri hesaplar.
        Göstergeler: SMA, EMA, RSI, MACD, Bollinger Bands, ATR, Stochastic, CCI, ADX, OBV, MFI, VWAP, ROC, Williams %R, Parabolic SAR, Ichimoku, Supertrend, vs.
        pandas_ta yüklü ise otomatik olarak daha fazla gösterge ekler.
        """
        results = {}
        try:
            close = df['Close'] if 'Close' in df else df.iloc[:, -1]
            high = df['High'] if 'High' in df else None
            low = df['Low'] if 'Low' in df else None
            volume = df['Volume'] if 'Volume' in df else None

            # SMA, EMA
            results['sma_20'] = close.rolling(window=20).mean().iloc[-1] if len(close) >= 20 else None
            results['ema_20'] = close.ewm(span=20, adjust=False).mean().iloc[-1] if len(close) >= 20 else None

            # RSI
            delta = close.diff()
            up = delta.clip(lower=0)
            down = -1 * delta.clip(upper=0)
            roll_up = up.rolling(14).mean()
            roll_down = down.rolling(14).mean()
            rs = roll_up / roll_down
            results['rsi_14'] = 100.0 - (100.0 / (1.0 + rs.iloc[-1])) if roll_down.iloc[-1] != 0 else 100.0

            # MACD
            ema12 = close.ewm(span=12, adjust=False).mean()
            ema26 = close.ewm(span=26, adjust=False).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9, adjust=False).mean()
            results['macd'] = macd.iloc[-1]
            results['macd_signal'] = signal.iloc[-1]
            results['macd_hist'] = (macd - signal).iloc[-1]

            # Bollinger Bands
            sma20 = close.rolling(window=20).mean()
            std20 = close.rolling(window=20).std()
            results['bb_upper'] = (sma20 + 2 * std20).iloc[-1] if len(close) >= 20 else None
            results['bb_lower'] = (sma20 - 2 * std20).iloc[-1] if len(close) >= 20 else None

            # ATR
            if high is not None and low is not None and close is not None:
                tr1 = high - low
                tr2 = (high - close.shift()).abs()
                tr3 = (low - close.shift()).abs()
                tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
                results['atr_14'] = tr.rolling(14).mean().iloc[-1] if len(tr) >= 14 else None

            # Stochastic Oscillator
            if high is not None and low is not None:
                lowest_low = low.rolling(window=14).min()
                highest_high = high.rolling(window=14).max()
                results['stoch_k'] = 100 * ((close - lowest_low) / (highest_high - lowest_low)).iloc[-1] if (highest_high - lowest_low).iloc[-1] != 0 else None

            # CCI
            if high is not None and low is not None:
                tp = (high + low + close) / 3
                cci = (tp - tp.rolling(20).mean()) / (0.015 * tp.rolling(20).std())
                results['cci_20'] = cci.iloc[-1] if len(cci) >= 20 else None

            # ADX
            if ta is not None and high is not None and low is not None and close is not None:
                adx = ta.adx(high, low, close, length=14)
                results['adx_14'] = adx['ADX_14'].iloc[-1] if 'ADX_14' in adx else None

            # OBV
            if volume is not None:
                obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
                results['obv'] = obv.iloc[-1]

            # MFI
            if ta is not None and high is not None and low is not None and close is not None and volume is not None:
                mfi = ta.mfi(high, low, close, volume, length=14)
                results['mfi_14'] = mfi.iloc[-1] if len(mfi) > 0 else None

            # VWAP
            if high is not None and low is not None and close is not None and volume is not None:
                typical_price = (high + low + close) / 3
                vwap = (typical_price * volume).cumsum() / volume.cumsum()
                results['vwap'] = vwap.iloc[-1]

            # ROC
            results['roc_12'] = ((close - close.shift(12)) / close.shift(12) * 100).iloc[-1] if len(close) >= 12 else None

            # Williams %R
            if high is not None and low is not None:
                highest_high = high.rolling(window=14).max()
                lowest_low = low.rolling(window=14).min()
                results['williams_r'] = -100 * ((highest_high - close) / (highest_high - lowest_low)).iloc[-1] if (highest_high - lowest_low).iloc[-1] != 0 else None

            # Parabolic SAR
            if ta is not None and high is not None and low is not None:
                psar = ta.psar(high, low, close)
                results['psar'] = psar['PSARl_0.02_0.2'].iloc[-1] if 'PSARl_0.02_0.2' in psar else None

            # Ichimoku
            if ta is not None and high is not None and low is not None and close is not None:
                ichi = ta.ichimoku(high, low, close)
                results['ichimoku_base'] = ichi[0]['ISA_9'].iloc[-1] if 'ISA_9' in ichi[0] else None

            # Supertrend
            if ta is not None and high is not None and low is not None and close is not None:
                supertrend = ta.supertrend(high, low, close)
                results['supertrend'] = supertrend['SUPERT_7_3.0'].iloc[-1] if 'SUPERT_7_3.0' in supertrend else None

            # Ekstra: pandas_ta ile otomatik göstergeler
            if ta is not None:
                try:
                    ta_results = ta.strategy("All")
                    # Kullanıcı isterse burada daha fazla gösterge eklenebilir
                except Exception:
                    pass

            return results
        except Exception as e:
            log_error(f"Teknik indikatörler hesaplanırken hata: {e}")
            return {"error": str(e)}
    """Finansal analiz sınıfı"""
    
    def __init__(self):
        self.astrology_analyzer = AstrologyAnalyzer()
        self.gann_analyzer = GannTechniqueAnalyzer()
        self.volatility_analyzer = VolatilityAnalyzer()
        self.risk_analyzer = RiskAnalyzer()
        self.options_analyzer = OptionsAnalyzer()
        self.currency_analyzer = CurrencyAnalyzer()
        self.commodities_analyzer = CommoditiesAnalyzer()
        self.founding_dates = CompanyFoundingDates()
        
        # Bonds analyzer'ı güvenli şekilde yükle
        try:
            from .bonds_analysis import BondsAnalyzer
            self.bonds_analyzer = BondsAnalyzer()
            self.bonds_available = True
        except Exception as e:
            log_error(f"Bonds analyzer yüklenemedi: {e}")
            self.bonds_available = False
            
        # Crypto analyzer'ı güvenli şekilde yükle
        try:
            from .crypto_analysis import CryptoAnalyzer
            self.crypto_analyzer = CryptoAnalyzer()
            self.crypto_available = True
        except Exception as e:
            log_error(f"Crypto analyzer yüklenemedi: {e}")
            self.crypto_analyzer = None
            self.crypto_available = False
        
        # ML Analysis import
        try:
            from .ml_analysis import MLAnalyzer
            self.ml_analyzer = MLAnalyzer()
            print("INFO: ML Analyzer yüklendi")
        except ImportError:
            print("WARNING: ML Analyzer bulunamadı")
            self.ml_analyzer = None
        
        log_info("FinancialAnalyzer başlatıldı")
    
    def generate_signal(self, financial_score=None, technical_indicators=None, trend_analysis=None, gann_analysis=None, symbol=None, stock_data=None) -> Tuple[str, float, Dict]:
        """Tüm analiz modüllerinden kapsamlı sinyal üret"""
        try:
            # Kuruluş tarihi bilgisini al
            founding_date = None
            if symbol:
                founding_date = self.founding_dates.get_founding_date(symbol)
                if founding_date:
                    log_debug(f"Financial Analysis - {symbol} kuruluş tarihi: {founding_date}")
            
            # Tüm analiz skorlarını topla
            scores = {}
            score_weights = {}
            details = {}  # Analysis details
            
            # Kuruluş tarihi bilgisini details'e ekle
            if founding_date:
                details['founding_date'] = founding_date
            
            # 1. Finansal Analiz Skoru (Ağırlık: %20)
            if financial_score and isinstance(financial_score, (int, float)):
                scores['financial'] = max(0, min(100, financial_score))
                score_weights['financial'] = 0.20
            
            # 2. Teknik Analiz Skoru (Ağırlık: %18)
            technical_score = 0
            if technical_indicators:
                rsi = technical_indicators.get('rsi', 50)
                # RSI'den teknik skor hesapla (30-70 arası normal, dışı güçlü sinyaller)
                if rsi < 30:
                    technical_score = 75  # Aşırı satım - alım fırsatı
                elif rsi > 70:
                    technical_score = 25  # Aşırı alım - satım sinyali
                else:
                    technical_score = 50  # Nötr
                
                scores['technical'] = technical_score
                score_weights['technical'] = 0.18
            
            # 3. Trend Analizi Skoru (Ağırlık: %12)
            if trend_analysis:
                trend_strength = trend_analysis.get('strength', 50)
                trend_direction = trend_analysis.get('trend', 'neutral')
                
                trend_score = trend_strength
                if trend_direction == 'yukselen':
                    trend_score += 20
                elif trend_direction == 'dusuk':
                    trend_score -= 20
                    
                scores['trend'] = max(0, min(100, trend_score))
                score_weights['trend'] = 0.12
            
            # 4. Gann Tekniği Skoru (Ağırlık: %12)
            if gann_analysis and isinstance(gann_analysis, (int, float)):
                scores['gann'] = max(0, min(100, gann_analysis))
                score_weights['gann'] = 0.12
            
            # 5. Astroloji Analizi (Ağırlık: %8)
            try:
                from ..analysis.astrology_analysis import get_astrology_score
                astro_score = get_astrology_score(symbol, stock_data)
                if astro_score:
                    scores['astrology'] = max(0, min(100, astro_score))
                    score_weights['astrology'] = 0.08
            except:
                scores['astrology'] = 50  # Varsayılan nötr skor
                score_weights['astrology'] = 0.08
            
            # 6. Anomaly Detection (Ağırlık: %8)
            try:
                from ..analysis.anomaly_detector import get_anomaly_score
                anomaly_score = get_anomaly_score(symbol, stock_data)
                # Anomaly score'u 0-100'e çevir (yüksek anomaly = düşük skor)
                transformed_anomaly_score = max(0, 100 - anomaly_score)
                scores['anomaly'] = transformed_anomaly_score
                score_weights['anomaly'] = 0.08
            except:
                scores['anomaly'] = 50
                score_weights['anomaly'] = 0.08
            
            # 6. Shemitah Döngüsü (Ağırlık: %4)
            try:
                from ..analysis.ultra_shemitah import ultra_shemitah_analyzer
                shemitah_result = ultra_shemitah_analyzer.calculate_ultra_shemitah_score(symbol)
                scores['shemitah'] = max(0, min(100, shemitah_result['ultra_shemitah_score']))
                score_weights['shemitah'] = 0.04
                details['shemitah'] = {
                    'score': shemitah_result['ultra_shemitah_score'],
                    'shemitah_year': shemitah_result['analysis']['shemitah_year'],
                    'phase': shemitah_result['analysis']['shemitah_phase'],
                    'jubilee_year': shemitah_result['analysis']['jubilee_year'],
                    'recommendation': shemitah_result['analysis']['score_interpretation']
                }
            except Exception as e:
                # Fallback to basic shemitah
                try:
                    from ..analysis.shemitah_analysis import get_shemitah_score
                    shemitah_score = get_shemitah_score()
                    scores['shemitah'] = max(0, min(100, shemitah_score))
                    score_weights['shemitah'] = 0.04
                    details['shemitah'] = {'error': str(e)}
                except:
                    scores['shemitah'] = 50
                    score_weights['shemitah'] = 0.04
                    details['shemitah'] = {'error': 'Shemitah analysis unavailable'}
            
            # 7. 21 Yıl Döngüsü (Ağırlık: %4)
            try:
                from ..analysis.cycle21_analysis import get_cycle21_score
                cycle21_score = get_cycle21_score()
                scores['cycle21'] = max(0, min(100, cycle21_score))
                score_weights['cycle21'] = 0.04
            except:
                scores['cycle21'] = 50
                score_weights['cycle21'] = 0.04
            
            # 8. Ultra Solar Cycle Analysis (Ağırlık: %3)
            try:
                from ..analysis.solar_cycle import ultra_solar_analyzer
                solar_result = ultra_solar_analyzer.calculate_ultra_solar_score(symbol)
                scores['solar_cycle'] = max(0, min(100, solar_result['ultra_solar_score']))
                score_weights['solar_cycle'] = 0.03
                details['solar_cycle'] = {
                    'score': solar_result['ultra_solar_score'],
                    'cycle_number': solar_result['solar_data']['cycle_number'],
                    'phase': solar_result['solar_data']['solar_phase']['phase'],
                    'sunspot_estimate': solar_result['solar_data']['estimated_sunspot_number'],
                    'geomagnetic_level': solar_result['solar_data']['geomagnetic_activity']['level'],
                    'recommendation': solar_result['analysis']['score_interpretation']
                }
            except Exception as e:
                scores['solar_cycle'] = 50
                score_weights['solar_cycle'] = 0.03
                details['solar_cycle'] = {'error': str(e)}
            
            # 9. Ultra Economic Cycle Analysis (Ağırlık: %5)
            try:
                economic_result = ultra_economic_analyzer.calculate_ultra_economic_score(symbol)
                scores['economic_cycle'] = max(0, min(100, economic_result['ultra_economic_score']))
                score_weights['economic_cycle'] = 0.05
                details['economic_cycle'] = {
                    'score': economic_result['ultra_economic_score'],
                    'business_cycle_phase': economic_result['analysis']['business_cycle_phase'],
                    'recession_risk': economic_result['analysis']['recession_risk_level'],
                    'yield_curve': economic_result['analysis']['yield_curve_shape'],
                    'recommendation': economic_result['analysis']['score_interpretation']
                }
            except Exception as e:
                scores['economic_cycle'] = 50
                score_weights['economic_cycle'] = 0.05
                details['economic_cycle'] = {'error': str(e)}
                log_error(f"Economic cycle analysis error for {symbol}: {e}")
            
            # 10. Anomaly Detection (Ağırlık: %5)
            try:
                from ..analysis.anomaly_detector import get_anomaly_score
                anomaly_score = get_anomaly_score(symbol, stock_data)
                # Anomaly score'u 0-100'e çevir (yüksek anomaly = düşük skor)
                transformed_anomaly_score = max(0, 100 - anomaly_score)
                scores['anomaly'] = transformed_anomaly_score
                score_weights['anomaly'] = 0.05
            except:
                scores['anomaly'] = 50
                score_weights['anomaly'] = 0.05
            
            # 11. Correlation Analysis (Ağırlık: %5)
            try:
                from ..analysis.correlation_analysis import get_correlation_score
                correlation_score = get_correlation_score(symbol, stock_data)
                scores['correlation'] = max(0, min(100, correlation_score))
                score_weights['correlation'] = 0.05
            except:
                scores['correlation'] = 50
                score_weights['correlation'] = 0.05
            
            # 12. Momentum Breakout Analysis (Ağırlık: %6)
            try:
                from ..analysis.momentum_breakout_analysis import get_momentum_score
                momentum_score = get_momentum_score(symbol, stock_data)
                scores['momentum'] = max(0, min(100, momentum_score))
                score_weights['momentum'] = 0.06
            except:
                scores['momentum'] = 50
                score_weights['momentum'] = 0.06
            
            # 13. Ultra Moon Phases Analysis (Ağırlık: %3)
            try:
                from ..analysis.moon_phases import ultra_moon_analyzer
                moon_result = ultra_moon_analyzer.calculate_ultra_moon_score(symbol)
                scores['moon_phases'] = max(0, min(100, moon_result['ultra_moon_score']))
                score_weights['moon_phases'] = 0.03
                details['moon_phases'] = {
                    'score': moon_result['ultra_moon_score'],
                    'phase': moon_result['lunar_data']['moon_phase']['name'],
                    'mansion': moon_result['lunar_data']['lunar_mansion']['name'],
                    'recommendation': moon_result['analysis']['score_interpretation']
                }
            except Exception as e:
                scores['moon_phases'] = 50
                score_weights['moon_phases'] = 0.03
                details['moon_phases'] = {'error': str(e)}
            
            # 14. Sentiment Analysis (Ağırlık: %7)
            try:
                from ..analysis.sentiment_analyzer import get_sentiment_score
                sentiment_score = get_sentiment_score(symbol, stock_data)
                scores['sentiment'] = max(0, min(100, sentiment_score))
                score_weights['sentiment'] = 0.07
            except:
                scores['sentiment'] = 50
                score_weights['sentiment'] = 0.07
            
            # 14. Statistical Validation (Ağırlık: %4)
            try:
                from ..analysis.statistical_validation import get_statistical_score
                statistical_score = get_statistical_score(symbol, stock_data)
                scores['statistical'] = max(0, min(100, statistical_score))
                score_weights['statistical'] = 0.04
            except:
                scores['statistical'] = 50
                score_weights['statistical'] = 0.04
            
            # 15. Vedic Astrology (Ağırlık: %3)
            try:
                from ..analysis.vedic_astrology import get_vedic_score
                vedic_score = get_vedic_score(symbol, stock_data)
                scores['vedic'] = max(0, min(100, vedic_score))
                score_weights['vedic'] = 0.03
            except:
                scores['vedic'] = 50
                score_weights['vedic'] = 0.03
            
            # 16. Ultra Options Analysis (Ağırlık: %4)
            try:
                current_price = stock_data['Close'].iloc[-1] if 'Close' in stock_data else 100
                options_result = self.options_analyzer.analyze_options(symbol, current_price)
                scores['ultra_options'] = max(0, min(100, options_result.get('options_score', 50)))
                score_weights['ultra_options'] = 0.04
                details['ultra_options'] = {
                    'score': options_result.get('options_score', 50),
                    'analysis_summary': options_result.get('analysis_summary', ''),
                    'volatility_regime': options_result.get('volatility_environment', {}).get('volatility_regime', 'Normal'),
                    'strategy_count': len(options_result.get('strategy_recommendations', [])),
                    'confidence': options_result.get('confidence', 75)
                }
            except Exception as e:
                scores['ultra_options'] = 50
                score_weights['ultra_options'] = 0.04
                details['ultra_options'] = {'error': str(e)}
                log_error(f"Ultra options analysis error for {symbol}: {e}")
            
            # 17. Ultra Currency Analysis (Ağırlık: %4)
            try:
                current_price = stock_data['Close'].iloc[-1] if 'Close' in stock_data else 100
                currency_result = self.currency_analyzer.analyze_currency(
                    symbol=f"{symbol}USD",  # Convert to currency pair format
                    current_rate=current_price,
                    historical_data=stock_data
                )
                scores['ultra_currency'] = max(0, min(100, currency_result.get('currency_score', 50)))
                score_weights['ultra_currency'] = 0.04
                details['ultra_currency'] = {
                    'score': currency_result.get('currency_score', 50),
                    'analysis_summary': currency_result.get('analysis_summary', ''),
                    'trading_recommendation': currency_result.get('trading_recommendation', 'BEKLE'),
                    'risk_assessment': currency_result.get('risk_assessment', {}).get('overall_risk', 'Orta'),
                    'confidence': currency_result.get('confidence', 75)
                }
                if 'ultra_analysis' in currency_result:
                    ultra_curr = currency_result['ultra_analysis']
                    details['ultra_currency'].update({
                        'carry_yield': ultra_curr.get('carry_trade', {}).get('carry_yield', 0),
                        'volatility_regime': currency_result.get('volatility_analysis', {}).get('vol_regime', 'normal'),
                        'policy_divergence': ultra_curr.get('central_bank', {}).get('policy_divergence', 0)
                    })
            except Exception as e:
                scores['ultra_currency'] = 50
                score_weights['ultra_currency'] = 0.04
                details['ultra_currency'] = {'error': str(e)}
                log_error(f"Ultra currency analysis error for {symbol}: {e}")
            
            # 18. Ultra Commodities Analysis (Ağırlık: %4)
            try:
                current_price = stock_data['Close'].iloc[-1] if 'Close' in stock_data else 100
                commodity_result = self.commodities_analyzer.analyze_commodity(
                    symbol=symbol,
                    current_price=current_price,
                    historical_data=stock_data
                )
                scores['ultra_commodities'] = max(0, min(100, commodity_result.get('commodity_score', 50)))
                score_weights['ultra_commodities'] = 0.04
                details['ultra_commodities'] = {
                    'score': commodity_result.get('commodity_score', 50),
                    'analysis_summary': commodity_result.get('analysis_summary', ''),
                    'trading_recommendation': commodity_result.get('trading_recommendation', 'BEKLE'),
                    'risk_assessment': commodity_result.get('risk_assessment', {}).get('overall_risk', 'Orta'),
                    'confidence': commodity_result.get('confidence', 75)
                }
                if 'ultra_analysis' in commodity_result:
                    ultra_comm = commodity_result['ultra_analysis']
                    details['ultra_commodities'].update({
                        'commodity_type': ultra_comm.get('commodity_type', 'unknown'),
                        'supply_demand_balance': ultra_comm.get('supply_demand', {}).get('balance_score', 50),
                        'volatility_regime': commodity_result.get('volatility_analysis', {}).get('volatility_regime', 'normal'),
                        'price_forecast_3m': ultra_comm.get('price_forecast', {}).get('3_months', current_price)
                    })
                if 'market_cycle' in commodity_result:
                    details['ultra_commodities']['market_cycle'] = commodity_result['market_cycle'].get('cycle_phase', 'Unknown')
            except Exception as e:
                scores['ultra_commodities'] = 50
                score_weights['ultra_commodities'] = 0.04
                details['ultra_commodities'] = {'error': str(e)}
                log_error(f"Ultra commodities analysis error for {symbol}: {e}")
            
            # 19. Ultra Bonds Analysis (Ağırlık: %4)
            try:
                if self.bonds_available and hasattr(self, 'bonds_analyzer'):
                    bond_result = self.bonds_analyzer.analyze_bond(
                        symbol=symbol,
                        historical_data=stock_data
                    )
                    scores['ultra_bonds'] = max(0, min(100, bond_result.get('bond_score', 50)))
                    score_weights['ultra_bonds'] = 0.04
                    details['ultra_bonds'] = {
                        'score': bond_result.get('bond_score', 50),
                        'analysis_summary': bond_result.get('analysis_summary', ''),
                        'trading_recommendation': bond_result.get('trading_recommendation', 'BEKLE'),
                        'risk_assessment': bond_result.get('risk_assessment', {}).get('overall_risk', 'Orta'),
                        'confidence': bond_result.get('confidence', 75)
                    }
                    if 'ultra_analysis' in bond_result:
                        ultra_bonds = bond_result['ultra_analysis']
                        details['ultra_bonds'].update({
                            'bond_type': ultra_bonds.get('bond_type', 'government'),
                            'credit_rating': ultra_bonds.get('credit_rating', 'BBB'),
                            'yield_to_maturity': ultra_bonds.get('valuation', {}).get('yield_to_maturity', 4.0),
                            'duration': ultra_bonds.get('valuation', {}).get('duration', 5.0),
                            'credit_score': ultra_bonds.get('credit_risk', {}).get('credit_score', 70),
                            'default_probability': ultra_bonds.get('credit_risk', {}).get('default_probability', 1.0)
                        })
                    if 'curve_insights' in bond_result:
                        details['ultra_bonds']['curve_shape'] = bond_result['curve_insights'].get('curve_shape', 'normal')
                        details['ultra_bonds']['recession_signal'] = bond_result['curve_insights'].get('economic_signal', 'Healthy Growth')
                else:
                    scores['ultra_bonds'] = 50
                    score_weights['ultra_bonds'] = 0.04
                    details['ultra_bonds'] = {'note': 'Bonds analysis not available'}
            except Exception as e:
                scores['ultra_bonds'] = 50
                score_weights['ultra_bonds'] = 0.04
                details['ultra_bonds'] = {'error': str(e)}
                log_error(f"Ultra bonds analysis error for {symbol}: {e}")
            
            # 20. Ultra Crypto Analysis (Ağırlık: %4)
            try:
                if self.crypto_available and hasattr(self, 'crypto_analyzer'):
                    crypto_result = self.crypto_analyzer.analyze_crypto(
                        symbol=symbol,
                        historical_data=stock_data
                    )
                    scores['ultra_crypto'] = max(0, min(100, crypto_result.get('crypto_score', 50)))
                    score_weights['ultra_crypto'] = 0.04
                    details['ultra_crypto'] = {
                        'score': crypto_result.get('crypto_score', 50),
                        'analysis_summary': crypto_result.get('analysis_summary', ''),
                        'trading_recommendation': crypto_result.get('trading_recommendation', 'BEKLE'),
                        'risk_assessment': crypto_result.get('risk_assessment', {}).get('overall_risk', 'Orta'),
                        'confidence': crypto_result.get('confidence', 75)
                    }
                    if 'ultra_analysis' in crypto_result:
                        ultra_crypto = crypto_result['ultra_analysis']
                        details['ultra_crypto'].update({
                            'crypto_category': ultra_crypto.get('crypto_category', 'altcoin'),
                            'blockchain': ultra_crypto.get('blockchain', 'ethereum'),
                            'market_phase': ultra_crypto.get('market_phase', 'consolidation'),
                            'fear_greed_index': ultra_crypto.get('onchain_metrics', {}).get('fear_greed_index', 50),
                            'hodler_ratio': ultra_crypto.get('onchain_metrics', {}).get('hodler_ratio', 0.6),
                            'sentiment_score': ultra_crypto.get('sentiment_metrics', {}).get('overall_sentiment', 50)
                        })
                    if 'market_insights' in crypto_result:
                        details['ultra_crypto']['market_phase_description'] = crypto_result['market_insights'].get('description', 'Market konsolidasyon fazında')
                        details['ultra_crypto']['strategy_implication'] = crypto_result['market_insights'].get('strategy_implication', 'Dikkatli yaklaşım')
                else:
                    scores['ultra_crypto'] = 50
                    score_weights['ultra_crypto'] = 0.04
                    details['ultra_crypto'] = {'note': 'Crypto analysis not available'}
            except Exception as e:
                scores['ultra_crypto'] = 50
                score_weights['ultra_crypto'] = 0.04
                details['ultra_crypto'] = {'error': str(e)}
                log_error(f"Ultra crypto analysis error for {symbol}: {e}")
            
            # 21. Ultra ML Analysis (Final Integration) (Ağırlık: %8)
            try:
                if self.ml_analyzer:
                    # Tüm analiz sonuçlarını ML'e gönder
                    all_analysis_results = {}
                    
                    # Populate analysis results
                    if 'financial_score' in details:
                        all_analysis_results['financial'] = {
                            'score': details['financial_score'],
                            'confidence': details.get('financial_confidence', 75)
                        }
                    
                    if 'technical_score' in details:
                        all_analysis_results['technical'] = {
                            'score': details['technical_score'],
                            'confidence': details.get('technical_confidence', 75)
                        }
                    
                    if 'ultra_score' in details:
                        all_analysis_results['ultra_analysis'] = {
                            'score': details['ultra_score'],
                            'confidence': details.get('ultra_confidence', 75),
                            'volatility_regime': details.get('volatility_regime', 'Normal'),
                            'risk_assessment': {'overall_risk': details.get('ultra_risk', 'Orta Risk')}
                        }
                    
                    if 'sentiment_score' in details:
                        all_analysis_results['sentiment_analysis'] = {
                            'score': details['sentiment_score'],
                            'confidence': details.get('sentiment_confidence', 70)
                        }
                    
                    if 'trend_score' in details:
                        all_analysis_results['trend_analysis'] = {
                            'score': details['trend_score'],
                            'confidence': details.get('trend_confidence', 70)
                        }
                    
                    # Add other analyses if available
                    for key in ['gann', 'astrology', 'volatility', 'options', 'currency', 'commodities', 'bonds', 'crypto']:
                        score_key = f'{key}_score'
                        if score_key in details:
                            all_analysis_results[f'{key}_analysis'] = {
                                'score': details[score_key],
                                'confidence': details.get(f'{key}_confidence', 70),
                                'risk_assessment': {'overall_risk': details.get(f'{key}_risk', 'Orta Risk')}
                            }
                    
                    # Run ML analysis
                    ml_result = self.ml_analyzer.analyze(
                        symbol=symbol,
                        all_analysis_results=all_analysis_results,
                        historical_data=stock_data,
                        analysis_mode='auto',
                        prediction_horizon='medium_term'
                    )
                    
                    if ml_result and 'ml_score' in ml_result:
                        scores['ultra_ml'] = ml_result['ml_score']
                        score_weights['ultra_ml'] = 0.08  # En yüksek ağırlık
                        
                        # ML detayları
                        details['ml_score'] = ml_result['ml_score']
                        details['ml_confidence'] = ml_result.get('confidence', 70)
                        details['ml_mode'] = ml_result.get('analysis_mode', 'basic')
                        details['ml_prediction_type'] = ml_result.get('prediction_type', 'ensemble')
                        
                        # Trading signals
                        trading_signals = ml_result.get('trading_signals', {})
                        details['ml_signal'] = trading_signals.get('primary_signal', 'BEKLE')
                        details['ml_signal_strength'] = trading_signals.get('signal_strength', 50)
                        
                        # Risk assessment
                        risk_assessment = ml_result.get('risk_assessment', {})
                        details['ml_risk'] = risk_assessment.get('overall_risk', 'Orta Risk')
                        details['ml_model_reliability'] = risk_assessment.get('model_reliability', 'Orta')
                        
                        # Predictions
                        predictions = ml_result.get('predictions', {})
                        if isinstance(predictions, dict):
                            details['ml_conservative'] = predictions.get('conservative', ml_result['ml_score'])
                            details['ml_optimistic'] = predictions.get('optimistic', ml_result['ml_score'])
                            if 'risk_adjusted' in predictions:
                                risk_adjusted = predictions['risk_adjusted']
                                if isinstance(risk_adjusted, dict):
                                    details['ml_risk_adjusted'] = risk_adjusted.get('moderate', ml_result['ml_score'])
                        
                        # Model performance
                        model_performance = ml_result.get('model_performance', {})
                        if isinstance(model_performance, dict):
                            details['ml_model_accuracy'] = model_performance.get('ensemble_average', 0.70)
                        
                        # Feature importance (top 3)
                        feature_importance = ml_result.get('feature_importance', {})
                        if isinstance(feature_importance, dict):
                            sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
                            details['ml_top_features'] = [f"{name}: {importance:.3f}" for name, importance in sorted_features]
                        
                        details['ml_recommendation'] = ml_result.get('recommendation', f"{symbol} ML analizi tamamlandı")
                    else:
                        scores['ultra_ml'] = 50
                        score_weights['ultra_ml'] = 0.08
                        details['ultra_ml'] = {'note': 'ML analysis returned no score'}
                else:
                    scores['ultra_ml'] = 50
                    score_weights['ultra_ml'] = 0.08
                    details['ultra_ml'] = {'note': 'ML analyzer not available'}
            except Exception as e:
                scores['ultra_ml'] = 50
                score_weights['ultra_ml'] = 0.08
                details['ultra_ml'] = {'error': str(e)}
                log_error(f"Ultra ML analysis error for {symbol}: {e}")
            
            # Ağırlıklı ortalama hesapla
            total_score = 0
            total_weight = 0
            
            for score_type, score in scores.items():
                weight = score_weights.get(score_type, 0)
                total_score += score * weight
                total_weight += weight
            
            # Eğer toplam ağırlık 1'den az ise normalize et
            if total_weight > 0:
                total_score = total_score / total_weight if total_weight != 1 else total_score
            else:
                total_score = 50  # Varsayılan nötr skor
            
            # Sinyal belirle (optimize edilmiş eşikler)
            if total_score >= 65:
                signal = "AL"
            elif total_score >= 55:
                signal = "TUT_GUCLU"
            elif total_score >= 45:
                signal = "TUT"
            elif total_score >= 35:
                signal = "TUT_ZAYIF"
            elif total_score >= 30:
                signal = "SAT"
            else:
                signal = "SAT"
            
            # Detaylı analiz sonuçları
            detailed_analysis = {
                "status": "ok",
                "total_score": round(total_score, 2),
                "scores": scores,
                "weights": score_weights,
                "financial_score": scores.get('financial', 0),
                "technical_score": scores.get('technical', 0),
                "trend_score": scores.get('trend', 0),
                "gann_score": scores.get('gann', 0),
                "astrology_score": scores.get('astrology', 0),
                "shemitah_score": scores.get('shemitah', 0),
                "cycle21_score": scores.get('cycle21', 0),
                "solar_cycle_score": scores.get('solar_cycle', 0),
                "economic_cycle_score": scores.get('economic_cycle', 0),
                "ultra_options_score": scores.get('ultra_options', 0),
                "signal_explanation": f"Toplam skor {total_score:.1f} - {len(scores)} modül analizi",
                "hold_days": self._calculate_hold_days(total_score, scores),
                "trend": trend_analysis.get('trend', 'neutral') if trend_analysis else 'neutral',
                "details": details
            }
            
            log_info(f"{symbol}: Kapsamlı sinyal üretildi - {signal} (Toplam Puan: {total_score:.1f}, {len(scores)} modül)")
            return signal, total_score, detailed_analysis
            
        except Exception as e:
            log_error(f"{symbol} sinyal üretilirken hata: {e}")
            return "BEKLE", 0, {"error": str(e)}
    
    def _calculate_hold_days(self, total_score, scores):
        """Toplam skorlara göre tutma süresi hesapla"""
        base_days = 14
        
        # Yüksek skor = daha uzun tutma
        if total_score >= 80:
            return base_days + 7  # 21 gün
        elif total_score >= 60:
            return base_days + 3  # 17 gün
        elif total_score <= 30:
            return max(7, base_days - 7)  # 7 gün minimum
        else:
            return base_days
    
    def analyze_trend(self, df: pd.DataFrame) -> Dict[str, any]:
        """Trend analizi"""
        return {"trend": "neutral"}
    
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
    
    def calculate_gann_analysis(self, stock_data):
        """Gann tekniği analizi yap"""
        try:
            if stock_data is None or stock_data.empty:
                return {"error": "Veri yok"}
            
            # Gann analizini yap - stock_data'nın symbol bilgisine ihtiyaç var
            # Geçici olarak basit bir analiz döndür
            result = {
                "gann_score": 50.0,  # Varsayılan orta değer
                "support_levels": [],
                "resistance_levels": [],
                "trend": "neutral"
            }
            return result
            
        except Exception as e:
            log_error(f"Gann analizi hesaplanırken hata: {e}")
            return {"error": str(e)}
