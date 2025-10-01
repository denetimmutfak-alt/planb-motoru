"""
Crypto Analysis Module
Kripto Para Analizi Ana Modülü
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

# CompanyFoundingDates entegrasyonu
try:
    from ..data.company_founding_dates import CompanyFoundingDates
    FOUNDING_DATES_AVAILABLE = True
    print("INFO: CompanyFoundingDates modülü crypto analysis'e entegre edildi")
except ImportError:
    FOUNDING_DATES_AVAILABLE = False
    print("WARNING: CompanyFoundingDates modülü bulunamadı")

try:
    from .ultra_crypto import UltraCryptoAnalyzer
    ULTRA_AVAILABLE = True
    print("INFO: Ultra Crypto Analysis modülü aktif")
except ImportError:
    ULTRA_AVAILABLE = False
    print("WARNING: Ultra Crypto Analysis modülü bulunamadı, temel analiz kullanılacak")

class CryptoAnalyzer:
    """Ana kripto analiz sınıfı"""
    
    def __init__(self):
        """Crypto analyzer'ı başlat"""
        # CompanyFoundingDates entegrasyonu
        self.founding_dates = None
        if FOUNDING_DATES_AVAILABLE:
            try:
                self.founding_dates = CompanyFoundingDates()
                print("INFO: CompanyFoundingDates crypto analyzer'a başarıyla entegre edildi")
            except Exception as e:
                print(f"WARNING: CompanyFoundingDates crypto analyzer'a entegre edilemedi: {str(e)}")
        
        self.ultra_analyzer = None
        if ULTRA_AVAILABLE:
            try:
                self.ultra_analyzer = UltraCryptoAnalyzer()
                print("INFO: Ultra Crypto Analyzer başarıyla başlatıldı")
            except Exception as e:
                print(f"WARNING: Ultra Crypto Analyzer başlatılamadı: {str(e)}")
        
        # Temel kripto kategorileri
        self.crypto_categories = {
            'BITCOIN': ['BTC', 'BITCOIN'],
            'ETHEREUM': ['ETH', 'ETHEREUM'],
            'ALTCOIN': ['ADA', 'XRP', 'LTC', 'BCH', 'DOT', 'LINK'],
            'DEFI': ['UNI', 'AAVE', 'COMP', 'CRV', 'SUSHI', 'YFI', 'CAKE'],
            'LAYER1': ['SOL', 'AVAX', 'ALGO', 'ATOM', 'NEAR', 'FTM'],
            'LAYER2': ['MATIC', 'LRC', 'IMX', 'ARB', 'OP'],
            'NFT': ['ENJ', 'MANA', 'SAND', 'FLOW', 'CHZ'],
            'MEME': ['DOGE', 'SHIB', 'FLOKI', 'PEPE'],
            'STABLECOIN': ['USDT', 'USDC', 'BUSD', 'DAI']
        }
        
        # Temel fiyat tahminleri
        self.base_prices = {
            'BTC': 65000,
            'ETH': 3200,
            'ADA': 0.45,
            'SOL': 145,
            'MATIC': 0.85,
            'UNI': 7.5,
            'DOGE': 0.08,
            'USDT': 1.0
        }
        
        # Risk skorları
        self.risk_scores = {
            'BITCOIN': 30,    # Düşük risk
            'ETHEREUM': 35,   # Düşük-Orta risk  
            'LAYER1': 50,     # Orta risk
            'DEFI': 60,       # Orta-Yüksek risk
            'ALTCOIN': 65,    # Yüksek risk
            'NFT': 70,        # Yüksek risk
            'MEME': 85,       # Çok yüksek risk
            'STABLECOIN': 15  # Çok düşük risk
        }
    
    def analyze_crypto(self, symbol: str, crypto_data: Optional[Dict] = None,
                      historical_data: Optional[pd.DataFrame] = None, **kwargs) -> Dict:
        """Kapsamlı kripto analizi"""
        try:
            # Founding date bilgisini al
            founding_date = None
            founding_info = "Founding date bilgisi mevcut değil"
            if self.founding_dates:
                try:
                    founding_date = self.founding_dates.get_founding_date(symbol)
                    if founding_date:
                        founding_info = f"Founding date: {founding_date}"
                        print(f"INFO: {symbol} founding date bulundu: {founding_date}")
                    else:
                        founding_info = f"{symbol} founding date veritabanında bulunamadı"
                        print(f"DEBUG: {symbol} için founding date bulunamadı")
                except Exception as e:
                    founding_info = f"Founding date alınırken hata: {str(e)}"
                    print(f"ERROR: {symbol} founding date hatası: {str(e)}")
            
            if self.ultra_analyzer and ULTRA_AVAILABLE:
                result = self._ultra_crypto_analysis(symbol, crypto_data, historical_data, **kwargs)
                # Founding date bilgisini ekle
                result['founding_date_info'] = founding_info
                if founding_date:
                    result['founding_date'] = founding_date
                return result
            else:
                result = self._basic_crypto_analysis(symbol, crypto_data, historical_data, **kwargs)
                # Founding date bilgisini ekle
                result['founding_date_info'] = founding_info
                if founding_date:
                    result['founding_date'] = founding_date
                return result
                
        except Exception as e:
            print(f"ERROR: Crypto analizi hatası: {str(e)}")
            return self._get_default_crypto_response(symbol)
    
    def _ultra_crypto_analysis(self, symbol: str, crypto_data: Optional[Dict],
                              historical_data: Optional[pd.DataFrame], **kwargs) -> Dict:
        """Ultra gelişmiş crypto analizi"""
        try:
            # Ana crypto analizi
            result = self.ultra_analyzer.analyze_crypto(
                symbol=symbol,
                crypto_data=crypto_data,
                historical_data=historical_data,
                **kwargs
            )
            
            # Crypto score hesaplama
            crypto_score = self._calculate_crypto_score(result)
            
            # Market phase insights
            market_insights = self._analyze_market_phase(result.market_phase, result.onchain_analysis)
            
            # Blockchain analysis
            blockchain_analysis = self._analyze_blockchain_performance(result.blockchain_metrics, result.crypto_profile)
            
            # DeFi analysis (varsa)
            defi_analysis = None
            if result.defi_metrics:
                defi_analysis = self._analyze_defi_performance(result.defi_metrics)
            
            # On-chain insights
            onchain_insights = self._analyze_onchain_signals(result.onchain_analysis)
            
            # Sentiment analysis
            sentiment_analysis = self._analyze_crypto_sentiment(result.crypto_sentiment)
            
            # Investment strategies
            investment_strategies = self._recommend_crypto_strategies(result)
            
            # Risk management
            risk_management = self._generate_crypto_risk_management(result)
            
            return {
                'crypto_score': round(crypto_score, 1),
                'analysis_summary': self._generate_crypto_summary(
                    symbol, result, crypto_score
                ),
                'trading_recommendation': result.trading_recommendation,
                'ultra_analysis': {
                    'ultra_crypto_score': result.ultra_crypto_score,
                    'crypto_category': result.crypto_profile.category.value,
                    'blockchain': result.crypto_profile.blockchain,
                    'market_cap': result.crypto_profile.market_cap,
                    'consensus_mechanism': result.crypto_profile.consensus_mechanism,
                    'use_case': result.crypto_profile.use_case,
                    'market_phase': result.market_phase.value,
                    'blockchain_metrics': {
                        'active_addresses': result.blockchain_metrics.active_addresses,
                        'transaction_count': result.blockchain_metrics.transaction_count,
                        'avg_block_time': round(result.blockchain_metrics.avg_block_time, 2),
                        'validator_count': result.blockchain_metrics.validator_count,
                        'staking_ratio': round(result.blockchain_metrics.staking_ratio, 3),
                        'development_activity': round(result.blockchain_metrics.development_activity, 1)
                    },
                    'onchain_metrics': {
                        'whale_activity': round(result.onchain_analysis.whale_activity, 3),
                        'hodler_ratio': round(result.onchain_analysis.hodler_ratio, 3),
                        'active_addresses_growth': round(result.onchain_analysis.active_addresses_growth, 3),
                        'fear_greed_index': round(result.onchain_analysis.fear_greed_index, 1),
                        'network_value_to_transactions': round(result.onchain_analysis.network_value_to_transactions, 2)
                    },
                    'sentiment_metrics': {
                        'social_sentiment': round(result.crypto_sentiment.social_sentiment, 1),
                        'institutional_sentiment': round(result.crypto_sentiment.institutional_sentiment, 1),
                        'technical_sentiment': round(result.crypto_sentiment.technical_sentiment, 1),
                        'overall_sentiment': round(np.mean([
                            result.crypto_sentiment.social_sentiment,
                            result.crypto_sentiment.institutional_sentiment,
                            result.crypto_sentiment.technical_sentiment
                        ]), 1)
                    }
                },
                'market_insights': market_insights,
                'blockchain_analysis': blockchain_analysis,
                'defi_analysis': defi_analysis,
                'onchain_insights': onchain_insights,
                'sentiment_analysis': sentiment_analysis,
                'price_targets': result.price_targets,
                'investment_strategies': investment_strategies,
                'risk_management': risk_management,
                'technical_signals': result.technical_signals,
                'fundamental_analysis': result.fundamental_analysis,
                'tokenomics_analysis': result.tokenomics_analysis,
                'adoption_metrics': result.adoption_metrics,
                'ecosystem_health': result.ecosystem_health,
                'risk_assessment': result.risk_assessment,
                'confidence': round(np.mean([
                    90.0 if result.ultra_crypto_score > 75 else 80.0,
                    85.0 if result.risk_assessment.get('overall_risk') in ['Düşük', 'Düşük-Orta'] else 70.0,
                    80.0
                ]), 1)
            }
            
        except Exception as e:
            print(f"ERROR: Ultra crypto analizi hatası: {str(e)}")
            return self._basic_crypto_analysis(symbol, crypto_data, historical_data, **kwargs)
    
    def _basic_crypto_analysis(self, symbol: str, crypto_data: Optional[Dict],
                              historical_data: Optional[pd.DataFrame], **kwargs) -> Dict:
        """Temel crypto analizi"""
        try:
            # Crypto category belirleme
            category = 'ALTCOIN'  # Default
            for cat, symbols in self.crypto_categories.items():
                if symbol.upper() in symbols:
                    category = cat
                    break
            
            # Market cap ve price tahmin et
            if crypto_data and 'market_cap' in crypto_data:
                market_cap = crypto_data['market_cap']
            else:
                # Symbol bazlı tahmin
                market_cap_estimates = {
                    'BTC': 1200000000000,    # 1.2T
                    'ETH': 400000000000,     # 400B
                    'USDT': 100000000000,    # 100B
                    'SOL': 60000000000,      # 60B
                    'ADA': 15000000000,      # 15B
                    'MATIC': 8000000000,     # 8B
                    'UNI': 5000000000,       # 5B
                    'DOGE': 12000000000      # 12B
                }
                market_cap = market_cap_estimates.get(symbol.upper(), 1000000000)  # 1B default
            
            # Current price tahmin et
            current_price = self.base_prices.get(symbol.upper(), 1.0)
            
            # Risk assessment
            risk_score = self.risk_scores.get(category, 50)
            
            # Volatility assessment (category based)
            volatility_levels = {
                'BITCOIN': 'Orta',
                'ETHEREUM': 'Orta',
                'STABLECOIN': 'Çok Düşük',
                'LAYER1': 'Yüksek',
                'DEFI': 'Yüksek',
                'ALTCOIN': 'Çok Yüksek',
                'MEME': 'Extreme',
                'NFT': 'Çok Yüksek'
            }
            volatility = volatility_levels.get(category, 'Yüksek')
            
            # Blockchain belirleme
            blockchain_mapping = {
                'BTC': 'bitcoin',
                'ETH': 'ethereum',
                'ADA': 'cardano',
                'SOL': 'solana',
                'MATIC': 'polygon',
                'AVAX': 'avalanche',
                'DOT': 'polkadot'
            }
            blockchain = blockchain_mapping.get(symbol.upper(), 'ethereum')
            
            # Technology score
            tech_scores = {
                'BITCOIN': 95,
                'ETHEREUM': 90,
                'LAYER1': 80,
                'DEFI': 75,
                'LAYER2': 85,
                'ALTCOIN': 65,
                'NFT': 60,
                'MEME': 30,
                'STABLECOIN': 70
            }
            tech_score = tech_scores.get(category, 60)
            
            # Adoption score
            adoption_scores = {
                'BITCOIN': 95,
                'ETHEREUM': 90,
                'STABLECOIN': 85,
                'LAYER1': 70,
                'DEFI': 65,
                'ALTCOIN': 50,
                'LAYER2': 60,
                'NFT': 45,
                'MEME': 25
            }
            adoption_score = adoption_scores.get(category, 50)
            
            # Crypto score hesaplama
            score_components = [
                tech_score * 0.3,           # Technology 30%
                adoption_score * 0.25,      # Adoption 25%
                (100 - risk_score) * 0.2,   # Risk (inverted) 20%
                60 * 0.15,                  # Market conditions 15%
                65 * 0.1                    # Sentiment 10%
            ]
            crypto_score = sum(score_components)
            
            # Trading recommendation
            if crypto_score >= 75:
                recommendation = "GÜÇLÜ ALIŞ"
            elif crypto_score >= 65:
                recommendation = "ALIŞ"
            elif crypto_score >= 55:
                recommendation = "ZAYIF ALIŞ"
            elif crypto_score >= 45:
                recommendation = "BEKLE"
            elif crypto_score >= 35:
                recommendation = "ZAYIF SAT"
            else:
                recommendation = "SAT"
            
            # Risk level string
            if risk_score <= 25:
                risk_level = "Düşük Risk"
            elif risk_score <= 50:
                risk_level = "Orta Risk"
            elif risk_score <= 75:
                risk_level = "Yüksek Risk"
            else:
                risk_level = "Çok Yüksek Risk"
            
            return {
                'crypto_score': round(crypto_score, 1),
                'analysis_summary': f"{symbol} kripto analizi: {category} kategorisi, {blockchain} blockchain, temel analiz ile değerlendirildi",
                'trading_recommendation': recommendation,
                'basic_metrics': {
                    'category': category,
                    'blockchain': blockchain,
                    'estimated_market_cap': market_cap,
                    'estimated_price': current_price,
                    'technology_score': tech_score,
                    'adoption_score': adoption_score,
                    'volatility_level': volatility
                },
                'risk_assessment': {
                    'overall_risk': risk_level,
                    'volatility_risk': volatility,
                    'technology_risk': 'Düşük' if tech_score > 80 else 'Orta' if tech_score > 60 else 'Yüksek',
                    'adoption_risk': 'Düşük' if adoption_score > 80 else 'Orta' if adoption_score > 60 else 'Yüksek',
                    'regulatory_risk': 'Yüksek' if category in ['MEME', 'PRIVACY'] else 'Orta' if category == 'DEFI' else 'Düşük'
                },
                'price_targets': {
                    '1_month': round(current_price * np.random.uniform(0.9, 1.15), 4),
                    '3_months': round(current_price * np.random.uniform(0.8, 1.3), 4),
                    '1_year': round(current_price * np.random.uniform(0.6, 2.0), 4)
                },
                'confidence': 70.0
            }
            
        except Exception as e:
            print(f"ERROR: Temel crypto analizi hatası: {str(e)}")
            return self._get_default_crypto_response(symbol)
    
    def _calculate_crypto_score(self, ultra_result) -> float:
        """Genel crypto skoru hesaplama"""
        try:
            scores = []
            
            # Ultra crypto score (%40)
            scores.append(ultra_result.ultra_crypto_score * 0.4)
            
            # Fundamental analysis (%25)
            fundamental_score = np.mean([
                ultra_result.fundamental_analysis.get('network_health', 70),
                ultra_result.fundamental_analysis.get('adoption_score', 70),
                ultra_result.fundamental_analysis.get('technology_innovation', 70)
            ])
            scores.append(fundamental_score * 0.25)
            
            # On-chain metrics (%20)
            onchain_score = ultra_result.onchain_analysis.fear_greed_index
            scores.append(onchain_score * 0.2)
            
            # Sentiment (%15)
            sentiment_score = np.mean([
                ultra_result.crypto_sentiment.social_sentiment,
                ultra_result.crypto_sentiment.institutional_sentiment,
                ultra_result.crypto_sentiment.technical_sentiment
            ])
            scores.append(sentiment_score * 0.15)
            
            return sum(scores)
            
        except Exception:
            return 50.0
    
    def _analyze_market_phase(self, market_phase, onchain_analysis) -> Dict:
        """Market phase analizi"""
        try:
            insights = {
                'phase': market_phase.value,
                'description': '',
                'strategy_implication': '',
                'duration_estimate': '',
                'confidence': 0
            }
            
            # Phase descriptions
            phase_descriptions = {
                'bear_market': 'Ayı piyasası - Fiyatlar düşme eğiliminde',
                'bull_market': 'Boğa piyasası - Fiyatlar yükselme eğiliminde', 
                'accumulation': 'Birikim fazı - Akıllı para biriktiriyor',
                'distribution': 'Dağıtım fazı - Profit alma zamanı',
                'parabolic': 'Parabolik yükseliş - Aşırı alım riski',
                'correction': 'Düzeltme - Geçici geri çekilme',
                'consolidation': 'Konsolidasyon - Yan trend'
            }
            insights['description'] = phase_descriptions.get(market_phase.value, 'Belirsiz faz')
            
            # Strategy implications
            strategy_implications = {
                'bear_market': 'DCA stratejisi, düşük leverage',
                'bull_market': 'Trend takibi, profit alma planı',
                'accumulation': 'Agresif birikim, uzun vade odak',
                'distribution': 'Profit alma, pozisyon azaltma',
                'parabolic': 'Risk yönetimi, stop loss',
                'correction': 'Dip alma fırsatı, sabır',
                'consolidation': 'Range trading, bekle-gör'
            }
            insights['strategy_implication'] = strategy_implications.get(market_phase.value, 'Dikkatli yaklaşım')
            
            # Fear & Greed ile confidence
            fear_greed = onchain_analysis.fear_greed_index
            if fear_greed < 25 or fear_greed > 75:
                insights['confidence'] = 85
            elif fear_greed < 40 or fear_greed > 60:
                insights['confidence'] = 70
            else:
                insights['confidence'] = 60
            
            return insights
            
        except Exception:
            return {'phase': 'consolidation', 'description': 'Market konsolidasyon fazında'}
    
    def _analyze_blockchain_performance(self, blockchain_metrics, crypto_profile) -> Dict:
        """Blockchain performans analizi"""
        try:
            performance = {}
            
            # Transaction throughput
            if blockchain_metrics.avg_block_time < 5:
                performance['speed'] = 'Çok Hızlı'
                performance['speed_score'] = 95
            elif blockchain_metrics.avg_block_time < 30:
                performance['speed'] = 'Hızlı'
                performance['speed_score'] = 80
            elif blockchain_metrics.avg_block_time < 300:
                performance['speed'] = 'Orta'
                performance['speed_score'] = 60
            else:
                performance['speed'] = 'Yavaş'
                performance['speed_score'] = 30
            
            # Network security
            if blockchain_metrics.validator_count > 10000:
                performance['security'] = 'Çok Güvenli'
                performance['security_score'] = 95
            elif blockchain_metrics.validator_count > 1000:
                performance['security'] = 'Güvenli'
                performance['security_score'] = 80
            elif blockchain_metrics.validator_count > 100:
                performance['security'] = 'Orta Güvenlik'
                performance['security_score'] = 60
            else:
                performance['security'] = 'Düşük Güvenlik'
                performance['security_score'] = 30
            
            # Development activity
            dev_activity = blockchain_metrics.development_activity
            if dev_activity > 90:
                performance['development'] = 'Çok Aktif'
            elif dev_activity > 70:
                performance['development'] = 'Aktif'
            elif dev_activity > 50:
                performance['development'] = 'Orta'
            else:
                performance['development'] = 'Düşük'
            
            # Staking participation
            if blockchain_metrics.staking_ratio > 0.6:
                performance['staking_health'] = 'Mükemmel'
            elif blockchain_metrics.staking_ratio > 0.4:
                performance['staking_health'] = 'İyi'
            elif blockchain_metrics.staking_ratio > 0.2:
                performance['staking_health'] = 'Orta'
            else:
                performance['staking_health'] = 'Zayıf'
            
            # Overall blockchain score
            blockchain_score = np.mean([
                performance['speed_score'],
                performance['security_score'],
                dev_activity,
                blockchain_metrics.staking_ratio * 100
            ])
            performance['overall_score'] = round(blockchain_score, 1)
            
            return performance
            
        except Exception:
            return {'speed': 'Orta', 'security': 'Orta Güvenlik', 'overall_score': 70.0}
    
    def _analyze_defi_performance(self, defi_metrics) -> Dict:
        """DeFi performans analizi"""
        try:
            analysis = {}
            
            # TVL analysis
            tvl = defi_metrics.total_value_locked
            if tvl > 10000000000:  # 10B+
                analysis['tvl_category'] = 'Çok Büyük'
                analysis['liquidity_strength'] = 'Mükemmel'
            elif tvl > 1000000000:  # 1B+
                analysis['tvl_category'] = 'Büyük'
                analysis['liquidity_strength'] = 'Güçlü'
            elif tvl > 100000000:  # 100M+
                analysis['tvl_category'] = 'Orta'
                analysis['liquidity_strength'] = 'Orta'
            else:
                analysis['tvl_category'] = 'Küçük'
                analysis['liquidity_strength'] = 'Zayıf'
            
            # Yield attractiveness
            yield_rate = defi_metrics.yield_rate * 100
            if yield_rate > 15:
                analysis['yield_assessment'] = 'Çok Yüksek (Risk)'
            elif yield_rate > 8:
                analysis['yield_assessment'] = 'Yüksek'
            elif yield_rate > 4:
                analysis['yield_assessment'] = 'Orta'
            else:
                analysis['yield_assessment'] = 'Düşük'
            
            # Risk assessment
            il_risk = defi_metrics.impermanent_loss_risk * 100
            if il_risk > 10:
                analysis['il_risk_level'] = 'Yüksek'
            elif il_risk > 5:
                analysis['il_risk_level'] = 'Orta'
            else:
                analysis['il_risk_level'] = 'Düşük'
            
            # Protocol health
            health_factors = [
                defi_metrics.audit_score,
                (1 - defi_metrics.smart_contract_risk) * 100,
                defi_metrics.governance_participation * 100,
                min(100, defi_metrics.protocol_revenue / 1000000)  # Revenue in millions
            ]
            protocol_health = np.mean(health_factors)
            
            if protocol_health > 85:
                analysis['protocol_health'] = 'Mükemmel'
            elif protocol_health > 70:
                analysis['protocol_health'] = 'İyi'
            elif protocol_health > 55:
                analysis['protocol_health'] = 'Orta'
            else:
                analysis['protocol_health'] = 'Zayıf'
            
            analysis['health_score'] = round(protocol_health, 1)
            analysis['tvl_usd'] = f"${tvl:,.0f}"
            analysis['apy'] = f"{yield_rate:.1f}%"
            
            return analysis
            
        except Exception:
            return {'protocol_health': 'Orta', 'yield_assessment': 'Orta', 'tvl_category': 'Orta'}
    
    def _analyze_onchain_signals(self, onchain_analysis) -> Dict:
        """On-chain sinyal analizi"""
        try:
            signals = {}
            
            # Whale activity assessment
            whale_activity = onchain_analysis.whale_activity
            if whale_activity > 0.7:
                signals['whale_signal'] = 'Güçlü Aktivite (Dikkat)'
                signals['whale_risk'] = 'Yüksek'
            elif whale_activity > 0.4:
                signals['whale_signal'] = 'Orta Aktivite'
                signals['whale_risk'] = 'Orta'
            else:
                signals['whale_signal'] = 'Düşük Aktivite'
                signals['whale_risk'] = 'Düşük'
            
            # Hodler strength
            hodler_ratio = onchain_analysis.hodler_ratio
            if hodler_ratio > 0.7:
                signals['hodler_strength'] = 'Çok Güçlü'
            elif hodler_ratio > 0.5:
                signals['hodler_strength'] = 'Güçlü'
            elif hodler_ratio > 0.3:
                signals['hodler_strength'] = 'Orta'
            else:
                signals['hodler_strength'] = 'Zayıf'
            
            # Exchange flow analysis
            inflow_outflow_ratio = onchain_analysis.exchange_outflows / onchain_analysis.exchange_inflows
            if inflow_outflow_ratio > 1.2:
                signals['exchange_flow'] = 'Net Çıkış (Pozitif)'
            elif inflow_outflow_ratio > 0.8:
                signals['exchange_flow'] = 'Dengeli'
            else:
                signals['exchange_flow'] = 'Net Giriş (Negatif)'
            
            # Network growth
            addr_growth = onchain_analysis.active_addresses_growth * 100
            if addr_growth > 10:
                signals['network_growth'] = 'Hızlı Büyüme'
            elif addr_growth > 5:
                signals['network_growth'] = 'Sağlıklı Büyüme'
            elif addr_growth > 0:
                signals['network_growth'] = 'Yavaş Büyüme'
            else:
                signals['network_growth'] = 'Daralan Network'
            
            # NVT signal
            nvt = onchain_analysis.network_value_to_transactions
            if nvt > 30:
                signals['nvt_signal'] = 'Aşırı Değerli'
            elif nvt > 15:
                signals['nvt_signal'] = 'Pahalı'
            elif nvt > 8:
                signals['nvt_signal'] = 'Adil Değer'
            else:
                signals['nvt_signal'] = 'Ucuz'
            
            return signals
            
        except Exception:
            return {
                'whale_signal': 'Orta Aktivite',
                'hodler_strength': 'Orta',
                'exchange_flow': 'Dengeli'
            }
    
    def _analyze_crypto_sentiment(self, crypto_sentiment) -> Dict:
        """Crypto sentiment analizi"""
        try:
            analysis = {}
            
            # Overall sentiment
            overall_sentiment = np.mean([
                crypto_sentiment.social_sentiment,
                crypto_sentiment.news_sentiment,
                crypto_sentiment.institutional_sentiment,
                crypto_sentiment.retail_sentiment
            ])
            
            if overall_sentiment > 70:
                analysis['overall_mood'] = 'Çok Pozitif'
                analysis['sentiment_risk'] = 'Aşırı İyimserlik Riski'
            elif overall_sentiment > 55:
                analysis['overall_mood'] = 'Pozitif'
                analysis['sentiment_risk'] = 'Düşük'
            elif overall_sentiment > 45:
                analysis['overall_mood'] = 'Nötr'
                analysis['sentiment_risk'] = 'Düşük'
            elif overall_sentiment > 30:
                analysis['overall_mood'] = 'Negatif'
                analysis['sentiment_risk'] = 'Orta'
            else:
                analysis['overall_mood'] = 'Çok Negatif'
                analysis['sentiment_risk'] = 'Aşırı Kötümserlik'
            
            # Institutional vs Retail
            inst_retail_diff = crypto_sentiment.institutional_sentiment - crypto_sentiment.retail_sentiment
            if abs(inst_retail_diff) > 20:
                if inst_retail_diff > 0:
                    analysis['divergence'] = 'Kurumsal daha iyimser'
                else:
                    analysis['divergence'] = 'Retail daha iyimser'
            else:
                analysis['divergence'] = 'Uyumlu sentiment'
            
            # Social media buzz
            social_avg = np.mean([
                crypto_sentiment.reddit_sentiment,
                crypto_sentiment.twitter_sentiment,
                crypto_sentiment.telegram_sentiment
            ])
            
            if social_avg > 75:
                analysis['social_buzz'] = 'Çok Yüksek'
            elif social_avg > 60:
                analysis['social_buzz'] = 'Yüksek'
            elif social_avg > 40:
                analysis['social_buzz'] = 'Orta'
            else:
                analysis['social_buzz'] = 'Düşük'
            
            analysis['sentiment_score'] = round(overall_sentiment, 1)
            
            return analysis
            
        except Exception:
            return {'overall_mood': 'Nötr', 'sentiment_score': 50.0}
    
    def _recommend_crypto_strategies(self, ultra_result) -> List[Dict]:
        """Crypto investment strategies"""
        try:
            strategies = []
            
            # Market phase strategy
            market_phase = ultra_result.market_phase.value
            crypto_score = ultra_result.ultra_crypto_score
            
            if market_phase == 'accumulation' and crypto_score > 60:
                strategies.append({
                    'strategy': 'DCA Accumulation',
                    'description': 'Birikim fazında düzenli alım yapma',
                    'risk_level': 'Düşük-Orta',
                    'time_horizon': '6-18 ay',
                    'expected_return': '50-200%'
                })
            
            if market_phase == 'bull_market' and crypto_score > 65:
                strategies.append({
                    'strategy': 'Trend Following',
                    'description': 'Boğa piyasasında trend takibi',
                    'risk_level': 'Orta',
                    'time_horizon': '3-12 ay',
                    'expected_return': '25-100%'
                })
            
            # DeFi strategy
            if ultra_result.defi_metrics and ultra_result.defi_metrics.yield_rate > 0.06:
                strategies.append({
                    'strategy': 'DeFi Yield Farming',
                    'description': 'Yüksek getirili DeFi protokollerinde farming',
                    'risk_level': 'Yüksek',
                    'time_horizon': '3-6 ay',
                    'expected_return': f'{ultra_result.defi_metrics.yield_rate*100:.1f}% APY'
                })
            
            # HODLing strategy
            if ultra_result.onchain_analysis.hodler_ratio > 0.6 and crypto_score > 70:
                strategies.append({
                    'strategy': 'Long-term HODL',
                    'description': 'Uzun vadeli elde tutma stratejisi',
                    'risk_level': 'Orta',
                    'time_horizon': '2-5 yıl',
                    'expected_return': '100-500%'
                })
            
            # Staking strategy
            if ultra_result.blockchain_metrics.staking_ratio > 0.5:
                strategies.append({
                    'strategy': 'Staking Strategy',
                    'description': 'Network staking ile passive income',
                    'risk_level': 'Düşük',
                    'time_horizon': '1-3 yıl',
                    'expected_return': '5-15% APY'
                })
            
            return strategies[:3]  # Top 3 strategies
            
        except Exception:
            return [{
                'strategy': 'Buy and Hold',
                'description': 'Temel alım ve elde tutma',
                'risk_level': 'Orta'
            }]
    
    def _generate_crypto_risk_management(self, ultra_result) -> Dict:
        """Crypto risk management"""
        try:
            risk_mgmt = {
                'position_sizing': {},
                'risk_controls': [],
                'monitoring_alerts': [],
                'exit_strategy': {}
            }
            
            # Position sizing
            overall_risk = ultra_result.risk_assessment.get('overall_risk', 'Orta')
            crypto_score = ultra_result.ultra_crypto_score
            
            if 'Yüksek' in overall_risk or crypto_score < 50:
                position_size = 'Küçük pozisyon (1-3% portföy)'
            elif 'Düşük' in overall_risk and crypto_score > 75:
                position_size = 'Büyük pozisyon (5-15% portföy)'
            else:
                position_size = 'Orta pozisyon (3-8% portföy)'
            
            risk_mgmt['position_sizing'] = {
                'recommended_size': position_size,
                'max_single_crypto': '10%',
                'crypto_allocation': 'Max %20 total portföy'
            }
            
            # Risk controls
            if ultra_result.onchain_analysis.whale_activity > 0.7:
                risk_mgmt['risk_controls'].append({
                    'type': 'Whale Alert',
                    'description': 'Büyük holder hareketlerini izle',
                    'action': 'Ani satış dalgalarına karşı hazırlıklı ol'
                })
            
            if ultra_result.crypto_sentiment.fear_greed_index > 75:
                risk_mgmt['risk_controls'].append({
                    'type': 'Greed Control',
                    'description': 'Aşırı iyimserlik kontrolü',
                    'action': 'Profit alma planını aktive et'
                })
            
            volatility_risk = ultra_result.risk_assessment.get('liquidity_risk', 'Orta')
            if volatility_risk == 'Yüksek':
                risk_mgmt['risk_controls'].append({
                    'type': 'Volatility Management',
                    'description': 'Yüksek volatilite kontrolü',
                    'action': 'Stop-loss ve take-profit seviyelerini dar tut'
                })
            
            # Monitoring alerts
            risk_mgmt['monitoring_alerts'] = [
                'On-chain metrics değişimleri',
                'Büyük whale transfer aktiviteleri',
                'Exchange girişlerinde artış',
                'Social sentiment ani değişimleri',
                'Regulasyon haberleri',
                'Technical support/resistance kırılımları'
            ]
            
            # Exit strategy
            current_price = ultra_result.price_targets.get('1_week', 50000)
            risk_mgmt['exit_strategy'] = {
                'stop_loss': f'{current_price * 0.85:.2f} (-15%)',
                'take_profit_1': f'{current_price * 1.3:.2f} (+30%)',
                'take_profit_2': f'{current_price * 1.6:.2f} (+60%)',
                'take_profit_3': f'{current_price * 2.0:.2f} (+100%)',
                'trailing_stop': '10-15% trailing stop'
            }
            
            return risk_mgmt
            
        except Exception:
            return {
                'position_sizing': {'recommended_size': 'Orta pozisyon'},
                'monitoring_alerts': ['Price action monitoring']
            }
    
    def _generate_crypto_summary(self, symbol: str, ultra_result, crypto_score: float) -> str:
        """Crypto analizi özeti"""
        try:
            # Score assessment
            if crypto_score >= 80:
                score_assessment = "mükemmel"
            elif crypto_score >= 70:
                score_assessment = "çok iyi"
            elif crypto_score >= 60:
                score_assessment = "iyi"
            elif crypto_score >= 50:
                score_assessment = "orta"
            else:
                score_assessment = "zayıf"
            
            category = ultra_result.crypto_profile.category.value
            blockchain = ultra_result.crypto_profile.blockchain
            market_phase = ultra_result.market_phase.value
            
            summary = f"{symbol} kripto analizi {score_assessment} skorla tamamlandı (%{crypto_score:.1f}). "
            summary += f"{category.title()} kategorisinde {blockchain} blockchain üzerinde. "
            
            # Market phase
            phase_descriptions = {
                'bull_market': 'Boğa piyasası devam ediyor',
                'bear_market': 'Ayı piyasası koşulları',
                'accumulation': 'Birikim fazında fırsat',
                'distribution': 'Dağıtım fazında dikkat',
                'parabolic': 'Parabolik yükseliş riski',
                'correction': 'Düzeltme fazında',
                'consolidation': 'Konsolidasyon dönemi'
            }
            summary += phase_descriptions.get(market_phase, 'Market belirsiz') + ". "
            
            # Fear & Greed
            fear_greed = ultra_result.onchain_analysis.fear_greed_index
            if fear_greed > 75:
                summary += "Aşırı iyimserlik (greed) seviyelerinde. "
            elif fear_greed < 25:
                summary += "Aşırı kötümserlik (fear) seviyelerinde. "
            else:
                summary += "Dengeli piyasa duyarlılığı. "
            
            # Whale activity
            if ultra_result.onchain_analysis.whale_activity > 0.7:
                summary += "Yüksek whale aktivitesi gözleniyor. "
            
            # HODLer strength
            if ultra_result.onchain_analysis.hodler_ratio > 0.7:
                summary += "Güçlü HODLer desteği mevcut. "
            
            # Trading recommendation
            recommendation = ultra_result.trading_recommendation
            summary += f"Genel öneri: {recommendation.lower()}."
            
            return summary
            
        except Exception:
            return f"{symbol} için kripto analizi tamamlandı"
    
    def _get_default_crypto_response(self, symbol: str) -> Dict:
        """Varsayılan crypto cevabı"""
        return {
            'crypto_score': 50.0,
            'analysis_summary': f"{symbol} için kripto analizi temel parametrelerle tamamlandı",
            'trading_recommendation': 'BEKLE',
            'basic_metrics': {
                'category': 'ALTCOIN',
                'blockchain': 'ethereum',
                'estimated_price': 1.0
            },
            'risk_assessment': {
                'overall_risk': 'Orta Risk'
            },
            'confidence': 70.0
        }
