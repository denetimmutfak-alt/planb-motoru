"""
Ultra Crypto Analysis Module
Ultra Kripto Para Analizi Modülü - DeFi, NFT, ve Blockchain Analytics
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json

class CryptoCategory(Enum):
    """Kripto kategorileri"""
    BITCOIN = "bitcoin"
    ETHEREUM = "ethereum"
    ALTCOIN = "altcoin"
    DEFI = "defi"
    NFT = "nft"
    GAMEFI = "gamefi"
    METAVERSE = "metaverse"
    LAYER1 = "layer1"
    LAYER2 = "layer2"
    MEME = "meme"
    STABLECOIN = "stablecoin"
    PRIVACY = "privacy"
    ORACLE = "oracle"
    EXCHANGE = "exchange"

class MarketPhase(Enum):
    """Kripto piyasa dönemleri"""
    BEAR_MARKET = "bear_market"
    BULL_MARKET = "bull_market"
    ACCUMULATION = "accumulation"
    DISTRIBUTION = "distribution"
    PARABOLIC = "parabolic"
    CORRECTION = "correction"
    CONSOLIDATION = "consolidation"

class DeFiProtocolType(Enum):
    """DeFi protokol türleri"""
    DEX = "dex"  # Decentralized Exchange
    LENDING = "lending"  # Lending Protocol
    YIELD_FARMING = "yield_farming"
    LIQUIDITY_MINING = "liquidity_mining"
    INSURANCE = "insurance"
    DERIVATIVES = "derivatives"
    BRIDGE = "bridge"
    GOVERNANCE = "governance"

@dataclass
class BlockchainMetrics:
    """Blockchain temel metrikleri"""
    network_hash_rate: float
    active_addresses: int
    transaction_count: int
    transaction_volume: float
    avg_block_time: float
    network_difficulty: float
    validator_count: int
    staking_ratio: float
    gas_price: float
    block_size: float
    mempool_size: int
    development_activity: float  # GitHub commits, contributions

@dataclass
class DeFiMetrics:
    """DeFi protokol metrikleri"""
    total_value_locked: float  # TVL
    trading_volume_24h: float
    liquidity_ratio: float
    yield_rate: float
    impermanent_loss_risk: float
    protocol_revenue: float
    governance_participation: float
    token_distribution: Dict[str, float]
    smart_contract_risk: float
    audit_score: float

@dataclass
class CryptoProfile:
    """Kripto para profili"""
    symbol: str
    name: str
    category: CryptoCategory
    market_cap: float
    circulating_supply: float
    total_supply: float
    max_supply: Optional[float]
    launch_date: datetime
    blockchain: str
    consensus_mechanism: str
    use_case: str
    team_score: float
    community_score: float
    technology_score: float

@dataclass
class OnChainAnalysis:
    """On-chain analiz metrikleri"""
    whale_activity: float  # Large holder activity
    exchange_inflows: float
    exchange_outflows: float
    hodler_ratio: float  # Long-term holders
    active_addresses_growth: float
    transaction_velocity: float
    network_value_to_transactions: float
    realized_cap: float
    market_value_to_realized_value: float
    fear_greed_index: float

@dataclass
class CryptoSentiment:
    """Kripto piyasa duyarlılığı"""
    social_sentiment: float
    news_sentiment: float
    reddit_sentiment: float
    twitter_sentiment: float
    telegram_sentiment: float
    google_trends: float
    institutional_sentiment: float
    retail_sentiment: float
    influencer_sentiment: float
    technical_sentiment: float

@dataclass
class UltraCryptoResult:
    """Ultra kripto analizi sonucu"""
    ultra_crypto_score: float
    crypto_profile: CryptoProfile
    blockchain_metrics: BlockchainMetrics
    defi_metrics: Optional[DeFiMetrics]
    onchain_analysis: OnChainAnalysis
    crypto_sentiment: CryptoSentiment
    market_phase: MarketPhase
    trading_recommendation: str
    price_targets: Dict[str, float]
    risk_assessment: Dict[str, str]
    technical_signals: Dict[str, Union[str, float]]
    fundamental_analysis: Dict[str, Union[str, float]]
    tokenomics_analysis: Dict[str, Union[str, float]]
    adoption_metrics: Dict[str, Union[str, float]]
    ecosystem_health: Dict[str, Union[str, float]]

class UltraCryptoAnalyzer:
    """Ultra gelişmiş kripto para analizi"""
    
    def __init__(self):
        """Ultra crypto analyzer'ı başlat"""
        print("INFO: Ultra Crypto Analyzer gelişmiş blockchain analytics ile başlatıldı")
        
        # Kripto kategorileri ve ağırlıkları
        self.category_weights = {
            CryptoCategory.BITCOIN: 1.2,
            CryptoCategory.ETHEREUM: 1.15,
            CryptoCategory.LAYER1: 1.1,
            CryptoCategory.DEFI: 1.05,
            CryptoCategory.LAYER2: 1.0,
            CryptoCategory.ALTCOIN: 0.95,
            CryptoCategory.NFT: 0.9,
            CryptoCategory.GAMEFI: 0.85,
            CryptoCategory.MEME: 0.7,
            CryptoCategory.STABLECOIN: 0.8
        }
        
        # Market cycle indicators
        self.cycle_indicators = {
            'bitcoin_dominance': 0.0,
            'alt_season_index': 0.0,
            'total_market_cap': 0.0,
            'fear_greed_index': 0.0
        }
        
        # DeFi protocol scores
        self.defi_protocol_scores = {
            'uniswap': 95,
            'aave': 92,
            'compound': 90,
            'curve': 88,
            'sushiswap': 85,
            'yearn': 83,
            'pancakeswap': 82
        }
        
        # Blockchain benchmarks
        self.blockchain_benchmarks = {
            'ethereum': {'tps': 15, 'finality': 360, 'decentralization': 95},
            'bitcoin': {'tps': 7, 'finality': 3600, 'decentralization': 100},
            'solana': {'tps': 3000, 'finality': 2, 'decentralization': 70},
            'polygon': {'tps': 7000, 'finality': 128, 'decentralization': 75},
            'avalanche': {'tps': 4500, 'finality': 1, 'decentralization': 80}
        }
    
    def analyze_crypto(self, symbol: str, crypto_data: Optional[Dict] = None,
                      historical_data: Optional[pd.DataFrame] = None,
                      blockchain_data: Optional[Dict] = None,
                      defi_data: Optional[Dict] = None, **kwargs) -> UltraCryptoResult:
        """Kapsamlı kripto analizi"""
        try:
            # 1. Crypto profile oluştur
            crypto_profile = self._create_crypto_profile(symbol, crypto_data)
            
            # 2. Blockchain metrics analizi
            blockchain_metrics = self._analyze_blockchain_metrics(
                crypto_profile.blockchain, blockchain_data
            )
            
            # 3. DeFi metrics (varsa)
            defi_metrics = None
            if crypto_profile.category in [CryptoCategory.DEFI, CryptoCategory.ETHEREUM]:
                defi_metrics = self._analyze_defi_metrics(symbol, defi_data)
            
            # 4. On-chain analizi
            onchain_analysis = self._perform_onchain_analysis(
                symbol, historical_data, blockchain_data
            )
            
            # 5. Crypto sentiment analizi
            crypto_sentiment = self._analyze_crypto_sentiment(symbol, **kwargs)
            
            # 6. Market phase belirleme
            market_phase = self._determine_market_phase(
                symbol, historical_data, onchain_analysis
            )
            
            # 7. Technical signals
            technical_signals = self._generate_technical_signals(
                historical_data, onchain_analysis
            )
            
            # 8. Fundamental analysis
            fundamental_analysis = self._perform_fundamental_analysis(
                crypto_profile, blockchain_metrics, defi_metrics
            )
            
            # 9. Tokenomics analysis
            tokenomics_analysis = self._analyze_tokenomics(crypto_profile)
            
            # 10. Adoption metrics
            adoption_metrics = self._calculate_adoption_metrics(
                crypto_profile, blockchain_metrics, onchain_analysis
            )
            
            # 11. Ecosystem health
            ecosystem_health = self._assess_ecosystem_health(
                crypto_profile, blockchain_metrics, onchain_analysis
            )
            
            # 12. Ultra crypto score hesaplama
            ultra_crypto_score = self._calculate_ultra_crypto_score(
                crypto_profile, blockchain_metrics, defi_metrics,
                onchain_analysis, crypto_sentiment, fundamental_analysis,
                tokenomics_analysis, adoption_metrics, ecosystem_health
            )
            
            # 13. Price targets
            price_targets = self._calculate_price_targets(
                symbol, historical_data, ultra_crypto_score, market_phase
            )
            
            # 14. Risk assessment
            risk_assessment = self._assess_crypto_risks(
                crypto_profile, blockchain_metrics, defi_metrics, onchain_analysis
            )
            
            # 15. Trading recommendation
            trading_recommendation = self._generate_trading_recommendation(
                ultra_crypto_score, market_phase, risk_assessment, technical_signals
            )
            
            return UltraCryptoResult(
                ultra_crypto_score=ultra_crypto_score,
                crypto_profile=crypto_profile,
                blockchain_metrics=blockchain_metrics,
                defi_metrics=defi_metrics,
                onchain_analysis=onchain_analysis,
                crypto_sentiment=crypto_sentiment,
                market_phase=market_phase,
                trading_recommendation=trading_recommendation,
                price_targets=price_targets,
                risk_assessment=risk_assessment,
                technical_signals=technical_signals,
                fundamental_analysis=fundamental_analysis,
                tokenomics_analysis=tokenomics_analysis,
                adoption_metrics=adoption_metrics,
                ecosystem_health=ecosystem_health
            )
            
        except Exception as e:
            print(f"ERROR: Ultra crypto analysis error: {str(e)}")
            return self._get_default_crypto_result(symbol)
    
    def _create_crypto_profile(self, symbol: str, crypto_data: Optional[Dict]) -> CryptoProfile:
        """Crypto profile oluştur"""
        try:
            # Kategori belirleme
            category = self._determine_crypto_category(symbol)
            
            # Default values
            default_data = {
                'name': symbol,
                'market_cap': 1000000000,  # 1B default
                'circulating_supply': 100000000,
                'total_supply': 100000000,
                'max_supply': None,
                'launch_date': datetime(2021, 1, 1),
                'blockchain': 'ethereum',
                'consensus_mechanism': 'proof_of_stake',
                'use_case': 'utility',
                'team_score': 75.0,
                'community_score': 70.0,
                'technology_score': 80.0
            }
            
            # Crypto data ile merge
            if crypto_data:
                default_data.update(crypto_data)
            
            return CryptoProfile(
                symbol=symbol,
                name=default_data['name'],
                category=category,
                market_cap=default_data['market_cap'],
                circulating_supply=default_data['circulating_supply'],
                total_supply=default_data['total_supply'],
                max_supply=default_data.get('max_supply'),
                launch_date=default_data['launch_date'] if isinstance(default_data['launch_date'], datetime) 
                           else datetime.strptime(default_data['launch_date'], '%Y-%m-%d'),
                blockchain=default_data['blockchain'],
                consensus_mechanism=default_data['consensus_mechanism'],
                use_case=default_data['use_case'],
                team_score=default_data['team_score'],
                community_score=default_data['community_score'],
                technology_score=default_data['technology_score']
            )
            
        except Exception as e:
            print(f"WARNING: Crypto profile oluşturma hatası: {str(e)}")
            return CryptoProfile(
                symbol=symbol,
                name=symbol,
                category=CryptoCategory.ALTCOIN,
                market_cap=1000000000,
                circulating_supply=100000000,
                total_supply=100000000,
                max_supply=None,
                launch_date=datetime(2021, 1, 1),
                blockchain='ethereum',
                consensus_mechanism='proof_of_stake',
                use_case='utility',
                team_score=70.0,
                community_score=65.0,
                technology_score=75.0
            )
    
    def _determine_crypto_category(self, symbol: str) -> CryptoCategory:
        """Crypto kategorisi belirleme"""
        symbol_upper = symbol.upper()
        
        # Bitcoin
        if symbol_upper in ['BTC', 'BITCOIN']:
            return CryptoCategory.BITCOIN
        
        # Ethereum
        elif symbol_upper in ['ETH', 'ETHEREUM']:
            return CryptoCategory.ETHEREUM
        
        # Stablecoins
        elif symbol_upper in ['USDT', 'USDC', 'BUSD', 'DAI', 'TUSD', 'USTC']:
            return CryptoCategory.STABLECOIN
        
        # DeFi
        elif symbol_upper in ['UNI', 'AAVE', 'COMP', 'CRV', 'SUSHI', 'YFI', '1INCH', 'CAKE']:
            return CryptoCategory.DEFI
        
        # Layer 1
        elif symbol_upper in ['ADA', 'SOL', 'AVAX', 'DOT', 'ALGO', 'ATOM', 'NEAR', 'FTM', 'LUNA']:
            return CryptoCategory.LAYER1
        
        # Layer 2
        elif symbol_upper in ['MATIC', 'LRC', 'IMX', 'ARB', 'OP']:
            return CryptoCategory.LAYER2
        
        # NFT/Gaming
        elif symbol_upper in ['ENJ', 'MANA', 'SAND', 'AXS', 'CHZ', 'FLOW', 'WAX']:
            return CryptoCategory.NFT
        
        # GameFi
        elif symbol_upper in ['AXS', 'SLP', 'GALA', 'ILV', 'ALICE', 'TLM']:
            return CryptoCategory.GAMEFI
        
        # Meme coins
        elif symbol_upper in ['DOGE', 'SHIB', 'FLOKI', 'PEPE', 'BONK']:
            return CryptoCategory.MEME
        
        # Privacy
        elif symbol_upper in ['XMR', 'ZEC', 'DASH', 'SCRT']:
            return CryptoCategory.PRIVACY
        
        # Oracle
        elif symbol_upper in ['LINK', 'BAND', 'TRB']:
            return CryptoCategory.ORACLE
        
        # Exchange tokens
        elif symbol_upper in ['BNB', 'FTT', 'KCS', 'HT', 'LEO']:
            return CryptoCategory.EXCHANGE
        
        else:
            return CryptoCategory.ALTCOIN
    
    def _analyze_blockchain_metrics(self, blockchain: str, blockchain_data: Optional[Dict]) -> BlockchainMetrics:
        """Blockchain metrikleri analizi"""
        try:
            # Default blockchain metrics
            default_metrics = {
                'network_hash_rate': 100e18,  # 100 EH/s
                'active_addresses': 1000000,
                'transaction_count': 1000000,
                'transaction_volume': 10000000000,  # 10B
                'avg_block_time': 15.0,
                'network_difficulty': 1e15,
                'validator_count': 1000,
                'staking_ratio': 0.6,
                'gas_price': 20.0,
                'block_size': 2.0,
                'mempool_size': 50000,
                'development_activity': 85.0
            }
            
            # Blockchain-specific adjustments
            if blockchain.lower() == 'bitcoin':
                default_metrics.update({
                    'avg_block_time': 600.0,  # 10 minutes
                    'validator_count': 15000,  # Mining nodes
                    'staking_ratio': 0.0,  # No staking
                    'gas_price': 0.0  # No gas concept
                })
            elif blockchain.lower() == 'ethereum':
                default_metrics.update({
                    'avg_block_time': 12.0,
                    'validator_count': 500000,
                    'staking_ratio': 0.22,
                    'gas_price': 25.0
                })
            elif blockchain.lower() == 'solana':
                default_metrics.update({
                    'avg_block_time': 0.4,
                    'validator_count': 1500,
                    'staking_ratio': 0.75,
                    'gas_price': 0.000005
                })
            
            # Apply blockchain_data if provided
            if blockchain_data:
                default_metrics.update(blockchain_data)
            
            return BlockchainMetrics(**default_metrics)
            
        except Exception as e:
            print(f"WARNING: Blockchain metrics analizi hatası: {str(e)}")
            return BlockchainMetrics(
                network_hash_rate=100e18,
                active_addresses=1000000,
                transaction_count=1000000,
                transaction_volume=10000000000,
                avg_block_time=15.0,
                network_difficulty=1e15,
                validator_count=1000,
                staking_ratio=0.6,
                gas_price=20.0,
                block_size=2.0,
                mempool_size=50000,
                development_activity=80.0
            )
    
    def _analyze_defi_metrics(self, symbol: str, defi_data: Optional[Dict]) -> DeFiMetrics:
        """DeFi protokol metrikleri"""
        try:
            default_defi = {
                'total_value_locked': 1000000000,  # 1B TVL
                'trading_volume_24h': 100000000,  # 100M
                'liquidity_ratio': 0.15,
                'yield_rate': 0.08,  # 8% APY
                'impermanent_loss_risk': 0.05,  # 5%
                'protocol_revenue': 50000000,  # 50M
                'governance_participation': 0.25,
                'token_distribution': {
                    'team': 0.20,
                    'community': 0.40,
                    'investors': 0.25,
                    'treasury': 0.15
                },
                'smart_contract_risk': 0.02,  # 2% risk
                'audit_score': 95.0
            }
            
            # Symbol-specific DeFi adjustments
            symbol_upper = symbol.upper()
            if symbol_upper == 'UNI':
                default_defi.update({
                    'total_value_locked': 5000000000,
                    'trading_volume_24h': 800000000,
                    'audit_score': 98.0
                })
            elif symbol_upper == 'AAVE':
                default_defi.update({
                    'total_value_locked': 7000000000,
                    'yield_rate': 0.06,
                    'audit_score': 97.0
                })
            
            if defi_data:
                default_defi.update(defi_data)
            
            return DeFiMetrics(**default_defi)
            
        except Exception as e:
            print(f"WARNING: DeFi metrics analizi hatası: {str(e)}")
            return DeFiMetrics(
                total_value_locked=1000000000,
                trading_volume_24h=100000000,
                liquidity_ratio=0.15,
                yield_rate=0.08,
                impermanent_loss_risk=0.05,
                protocol_revenue=50000000,
                governance_participation=0.25,
                token_distribution={'team': 0.20, 'community': 0.40, 'investors': 0.25, 'treasury': 0.15},
                smart_contract_risk=0.02,
                audit_score=90.0
            )
    
    def _perform_onchain_analysis(self, symbol: str, historical_data: Optional[pd.DataFrame],
                                 blockchain_data: Optional[Dict]) -> OnChainAnalysis:
        """On-chain analiz"""
        try:
            # Simulate on-chain metrics
            np.random.seed(hash(symbol) % 2**32)
            
            base_metrics = {
                'whale_activity': np.random.uniform(0.3, 0.8),
                'exchange_inflows': np.random.uniform(1000000, 50000000),
                'exchange_outflows': np.random.uniform(1500000, 45000000),
                'hodler_ratio': np.random.uniform(0.4, 0.8),
                'active_addresses_growth': np.random.uniform(-0.1, 0.3),
                'transaction_velocity': np.random.uniform(0.1, 2.0),
                'network_value_to_transactions': np.random.uniform(5, 50),
                'realized_cap': np.random.uniform(500000000, 50000000000),
                'market_value_to_realized_value': np.random.uniform(0.8, 3.0),
                'fear_greed_index': np.random.uniform(20, 80)
            }
            
            # Symbol-specific adjustments
            symbol_upper = symbol.upper()
            if symbol_upper == 'BTC':
                base_metrics.update({
                    'whale_activity': 0.6,
                    'hodler_ratio': 0.75,
                    'fear_greed_index': 45
                })
            elif symbol_upper == 'ETH':
                base_metrics.update({
                    'whale_activity': 0.55,
                    'hodler_ratio': 0.68,
                    'fear_greed_index': 50
                })
            
            return OnChainAnalysis(**base_metrics)
            
        except Exception as e:
            print(f"WARNING: On-chain analiz hatası: {str(e)}")
            return OnChainAnalysis(
                whale_activity=0.5,
                exchange_inflows=10000000,
                exchange_outflows=12000000,
                hodler_ratio=0.6,
                active_addresses_growth=0.1,
                transaction_velocity=1.0,
                network_value_to_transactions=20,
                realized_cap=5000000000,
                market_value_to_realized_value=1.5,
                fear_greed_index=50
            )
    
    def _analyze_crypto_sentiment(self, symbol: str, **kwargs) -> CryptoSentiment:
        """Kripto sentiment analizi"""
        try:
            # Simulate sentiment data
            np.random.seed(hash(symbol) % 2**32)
            
            sentiment_scores = {
                'social_sentiment': np.random.uniform(30, 80),
                'news_sentiment': np.random.uniform(25, 85),
                'reddit_sentiment': np.random.uniform(20, 90),
                'twitter_sentiment': np.random.uniform(30, 85),
                'telegram_sentiment': np.random.uniform(35, 80),
                'google_trends': np.random.uniform(40, 95),
                'institutional_sentiment': np.random.uniform(45, 75),
                'retail_sentiment': np.random.uniform(25, 85),
                'influencer_sentiment': np.random.uniform(30, 90),
                'technical_sentiment': np.random.uniform(35, 80)
            }
            
            # Market phase adjustments
            current_hour = datetime.now().hour
            if current_hour < 12:  # Morning boost
                for key in sentiment_scores:
                    sentiment_scores[key] += 5
            
            # Ensure bounds
            for key in sentiment_scores:
                sentiment_scores[key] = max(0, min(100, sentiment_scores[key]))
            
            return CryptoSentiment(**sentiment_scores)
            
        except Exception as e:
            print(f"WARNING: Crypto sentiment analizi hatası: {str(e)}")
            return CryptoSentiment(
                social_sentiment=50,
                news_sentiment=50,
                reddit_sentiment=50,
                twitter_sentiment=50,
                telegram_sentiment=50,
                google_trends=50,
                institutional_sentiment=50,
                retail_sentiment=50,
                influencer_sentiment=50,
                technical_sentiment=50
            )
    
    def _determine_market_phase(self, symbol: str, historical_data: Optional[pd.DataFrame],
                               onchain_analysis: OnChainAnalysis) -> MarketPhase:
        """Market phase belirleme"""
        try:
            # Fear & Greed Index'e göre phase belirleme
            fear_greed = onchain_analysis.fear_greed_index
            
            # Whale activity ve hodler ratio
            whale_activity = onchain_analysis.whale_activity
            hodler_ratio = onchain_analysis.hodler_ratio
            
            # Phase logic
            if fear_greed < 25:
                if hodler_ratio > 0.7:
                    return MarketPhase.ACCUMULATION
                else:
                    return MarketPhase.BEAR_MARKET
            elif fear_greed < 40:
                return MarketPhase.ACCUMULATION if whale_activity < 0.5 else MarketPhase.BEAR_MARKET
            elif fear_greed > 75:
                if whale_activity > 0.7:
                    return MarketPhase.DISTRIBUTION
                else:
                    return MarketPhase.PARABOLIC
            elif fear_greed > 60:
                return MarketPhase.BULL_MARKET
            else:
                return MarketPhase.CONSOLIDATION
                
        except Exception:
            return MarketPhase.CONSOLIDATION
    
    def _generate_technical_signals(self, historical_data: Optional[pd.DataFrame],
                                   onchain_analysis: OnChainAnalysis) -> Dict[str, Union[str, float]]:
        """Technical signals"""
        try:
            signals = {}
            
            # Price momentum (simulated)
            momentum_score = 50 + (onchain_analysis.fear_greed_index - 50) * 0.8
            signals['momentum_score'] = round(momentum_score, 1)
            
            # Volume profile
            if onchain_analysis.transaction_velocity > 1.5:
                signals['volume_profile'] = 'Yüksek Aktivite'
            elif onchain_analysis.transaction_velocity > 0.8:
                signals['volume_profile'] = 'Normal Aktivite'
            else:
                signals['volume_profile'] = 'Düşük Aktivite'
            
            # Support/Resistance levels (simulated)
            base_price = 50000  # Base BTC price
            signals['support_level'] = round(base_price * 0.92, 2)
            signals['resistance_level'] = round(base_price * 1.08, 2)
            
            # RSI (simulated)
            rsi_value = 30 + (onchain_analysis.fear_greed_index * 0.8)
            signals['rsi'] = round(rsi_value, 1)
            
            if rsi_value < 30:
                signals['rsi_signal'] = 'Aşırı Satım'
            elif rsi_value > 70:
                signals['rsi_signal'] = 'Aşırı Alım'
            else:
                signals['rsi_signal'] = 'Nötr'
            
            # MACD signal
            macd_histogram = (onchain_analysis.fear_greed_index - 50) / 10
            signals['macd_histogram'] = round(macd_histogram, 2)
            signals['macd_signal'] = 'Pozitif' if macd_histogram > 0 else 'Negatif'
            
            return signals
            
        except Exception as e:
            print(f"WARNING: Technical signals hatası: {str(e)}")
            return {
                'momentum_score': 50.0,
                'volume_profile': 'Normal Aktivite',
                'rsi': 50.0,
                'rsi_signal': 'Nötr'
            }
    
    def _perform_fundamental_analysis(self, crypto_profile: CryptoProfile,
                                     blockchain_metrics: BlockchainMetrics,
                                     defi_metrics: Optional[DeFiMetrics]) -> Dict[str, Union[str, float]]:
        """Fundamental analiz"""
        try:
            analysis = {}
            
            # Network fundamentals
            analysis['network_health'] = min(100, blockchain_metrics.development_activity)
            analysis['adoption_score'] = min(100, blockchain_metrics.active_addresses / 10000)
            analysis['decentralization_score'] = min(100, blockchain_metrics.validator_count / 10)
            
            # Token economics
            if crypto_profile.max_supply:
                scarcity_ratio = crypto_profile.circulating_supply / crypto_profile.max_supply
                analysis['scarcity_score'] = round((1 - scarcity_ratio) * 100, 1)
            else:
                analysis['scarcity_score'] = 50.0  # Neutral for unlimited supply
            
            # Team & Technology
            analysis['team_quality'] = crypto_profile.team_score
            analysis['technology_innovation'] = crypto_profile.technology_score
            analysis['community_strength'] = crypto_profile.community_score
            
            # DeFi fundamentals
            if defi_metrics:
                analysis['protocol_efficiency'] = min(100, defi_metrics.total_value_locked / 1000000)  # TVL in millions
                analysis['yield_attractiveness'] = min(100, defi_metrics.yield_rate * 1000)
                analysis['security_score'] = defi_metrics.audit_score
            
            # Use case assessment
            use_case_scores = {
                'store_of_value': 90,
                'medium_of_exchange': 80,
                'smart_contracts': 85,
                'defi': 88,
                'nft': 75,
                'gaming': 70,
                'utility': 65
            }
            analysis['utility_score'] = use_case_scores.get(crypto_profile.use_case, 60)
            
            return analysis
            
        except Exception as e:
            print(f"WARNING: Fundamental analiz hatası: {str(e)}")
            return {
                'network_health': 75.0,
                'adoption_score': 70.0,
                'team_quality': 75.0,
                'utility_score': 70.0
            }
    
    def _analyze_tokenomics(self, crypto_profile: CryptoProfile) -> Dict[str, Union[str, float]]:
        """Tokenomics analizi"""
        try:
            analysis = {}
            
            # Supply metrics
            if crypto_profile.max_supply:
                inflation_rate = ((crypto_profile.total_supply - crypto_profile.circulating_supply) / 
                                crypto_profile.circulating_supply) * 100
                analysis['potential_inflation'] = round(inflation_rate, 2)
                
                # Scarcity
                scarcity_ratio = crypto_profile.circulating_supply / crypto_profile.max_supply
                if scarcity_ratio > 0.9:
                    analysis['scarcity_level'] = 'Çok Yüksek'
                elif scarcity_ratio > 0.7:
                    analysis['scarcity_level'] = 'Yüksek'
                elif scarcity_ratio > 0.5:
                    analysis['scarcity_level'] = 'Orta'
                else:
                    analysis['scarcity_level'] = 'Düşük'
            else:
                analysis['potential_inflation'] = 'Sınırsız Arz'
                analysis['scarcity_level'] = 'Düşük'
            
            # Market cap assessment
            if crypto_profile.market_cap > 100000000000:  # 100B+
                analysis['market_cap_category'] = 'Large Cap'
                analysis['growth_potential'] = 'Düşük-Orta'
            elif crypto_profile.market_cap > 10000000000:  # 10B+
                analysis['market_cap_category'] = 'Mid Cap'
                analysis['growth_potential'] = 'Orta-Yüksek'
            elif crypto_profile.market_cap > 1000000000:  # 1B+
                analysis['market_cap_category'] = 'Small Cap'
                analysis['growth_potential'] = 'Yüksek'
            else:
                analysis['market_cap_category'] = 'Micro Cap'
                analysis['growth_potential'] = 'Çok Yüksek (Riskli)'
            
            # Age analysis
            age_days = (datetime.now() - crypto_profile.launch_date).days
            if age_days > 1460:  # 4+ years
                analysis['maturity_level'] = 'Olgun'
                analysis['track_record'] = 'Güçlü'
            elif age_days > 730:  # 2+ years
                analysis['maturity_level'] = 'Gelişmekte'
                analysis['track_record'] = 'Orta'
            else:
                analysis['maturity_level'] = 'Genç'
                analysis['track_record'] = 'Sınırlı'
            
            return analysis
            
        except Exception as e:
            print(f"WARNING: Tokenomics analizi hatası: {str(e)}")
            return {
                'scarcity_level': 'Orta',
                'market_cap_category': 'Mid Cap',
                'maturity_level': 'Gelişmekte'
            }
    
    def _calculate_adoption_metrics(self, crypto_profile: CryptoProfile,
                                   blockchain_metrics: BlockchainMetrics,
                                   onchain_analysis: OnChainAnalysis) -> Dict[str, Union[str, float]]:
        """Adoption metrikleri"""
        try:
            metrics = {}
            
            # Network adoption
            metrics['daily_active_users'] = blockchain_metrics.active_addresses
            metrics['transaction_growth'] = onchain_analysis.active_addresses_growth * 100
            
            # Hodler behavior
            if onchain_analysis.hodler_ratio > 0.7:
                metrics['hodling_strength'] = 'Çok Güçlü'
            elif onchain_analysis.hodler_ratio > 0.5:
                metrics['hodling_strength'] = 'Güçlü'
            elif onchain_analysis.hodler_ratio > 0.3:
                metrics['hodling_strength'] = 'Orta'
            else:
                metrics['hodling_strength'] = 'Zayıf'
            
            # Institutional adoption (simulated)
            institutional_score = (crypto_profile.team_score + crypto_profile.technology_score) / 2
            if institutional_score > 85:
                metrics['institutional_interest'] = 'Yüksek'
            elif institutional_score > 70:
                metrics['institutional_interest'] = 'Orta'
            else:
                metrics['institutional_interest'] = 'Düşük'
            
            # Developer activity
            if blockchain_metrics.development_activity > 90:
                metrics['developer_activity'] = 'Çok Aktif'
            elif blockchain_metrics.development_activity > 70:
                metrics['developer_activity'] = 'Aktif'
            elif blockchain_metrics.development_activity > 50:
                metrics['developer_activity'] = 'Orta'
            else:
                metrics['developer_activity'] = 'Düşük'
            
            # Real-world utility
            utility_categories = {
                CryptoCategory.BITCOIN: 85,
                CryptoCategory.ETHEREUM: 90,
                CryptoCategory.DEFI: 80,
                CryptoCategory.LAYER1: 75,
                CryptoCategory.STABLECOIN: 95,
                CryptoCategory.LAYER2: 70,
                CryptoCategory.NFT: 60,
                CryptoCategory.MEME: 20
            }
            utility_score = utility_categories.get(crypto_profile.category, 50)
            metrics['utility_score'] = utility_score
            
            return metrics
            
        except Exception as e:
            print(f"WARNING: Adoption metrics hatası: {str(e)}")
            return {
                'hodling_strength': 'Orta',
                'institutional_interest': 'Orta',
                'developer_activity': 'Aktif',
                'utility_score': 70
            }
    
    def _assess_ecosystem_health(self, crypto_profile: CryptoProfile,
                                blockchain_metrics: BlockchainMetrics,
                                onchain_analysis: OnChainAnalysis) -> Dict[str, Union[str, float]]:
        """Ecosystem sağlık değerlendirmesi"""
        try:
            health = {}
            
            # Network security
            if crypto_profile.blockchain.lower() == 'bitcoin':
                security_score = 100  # Gold standard
            elif crypto_profile.blockchain.lower() == 'ethereum':
                security_score = 95
            else:
                # Based on validator count and staking ratio
                security_score = min(100, (blockchain_metrics.validator_count / 1000) * 50 + 
                                   blockchain_metrics.staking_ratio * 50)
            
            health['network_security'] = round(security_score, 1)
            
            # Decentralization level
            if blockchain_metrics.validator_count > 10000:
                health['decentralization'] = 'Çok Yüksek'
            elif blockchain_metrics.validator_count > 1000:
                health['decentralization'] = 'Yüksek'
            elif blockchain_metrics.validator_count > 100:
                health['decentralization'] = 'Orta'
            else:
                health['decentralization'] = 'Düşük'
            
            # Transaction throughput
            if blockchain_metrics.avg_block_time < 5:
                health['transaction_speed'] = 'Çok Hızlı'
            elif blockchain_metrics.avg_block_time < 30:
                health['transaction_speed'] = 'Hızlı'
            elif blockchain_metrics.avg_block_time < 300:
                health['transaction_speed'] = 'Orta'
            else:
                health['transaction_speed'] = 'Yavaş'
            
            # Ecosystem diversity
            category_diversity = {
                CryptoCategory.ETHEREUM: 95,  # Most diverse ecosystem
                CryptoCategory.LAYER1: 80,
                CryptoCategory.DEFI: 75,
                CryptoCategory.BITCOIN: 70,  # Limited but strong
                CryptoCategory.LAYER2: 65,
                CryptoCategory.ALTCOIN: 50
            }
            health['ecosystem_diversity'] = category_diversity.get(crypto_profile.category, 40)
            
            # Community strength
            community_strength = crypto_profile.community_score
            if community_strength > 85:
                health['community_health'] = 'Çok Güçlü'
            elif community_strength > 70:
                health['community_health'] = 'Güçlü'
            elif community_strength > 55:
                health['community_health'] = 'Orta'
            else:
                health['community_health'] = 'Zayıf'
            
            return health
            
        except Exception as e:
            print(f"WARNING: Ecosystem health değerlendirme hatası: {str(e)}")
            return {
                'network_security': 75.0,
                'decentralization': 'Orta',
                'transaction_speed': 'Orta',
                'community_health': 'Güçlü'
            }
    
    def _calculate_ultra_crypto_score(self, crypto_profile: CryptoProfile,
                                     blockchain_metrics: BlockchainMetrics,
                                     defi_metrics: Optional[DeFiMetrics],
                                     onchain_analysis: OnChainAnalysis,
                                     crypto_sentiment: CryptoSentiment,
                                     fundamental_analysis: Dict,
                                     tokenomics_analysis: Dict,
                                     adoption_metrics: Dict,
                                     ecosystem_health: Dict) -> float:
        """Ultra crypto score hesaplama"""
        try:
            scores = []
            weights = []
            
            # 1. Fundamental Score (25%)
            fundamental_score = np.mean([
                fundamental_analysis.get('network_health', 70),
                fundamental_analysis.get('adoption_score', 70),
                fundamental_analysis.get('team_quality', 70),
                fundamental_analysis.get('technology_innovation', 70),
                fundamental_analysis.get('utility_score', 70)
            ])
            scores.append(fundamental_score)
            weights.append(0.25)
            
            # 2. Technical/On-chain Score (20%)
            onchain_score = np.mean([
                onchain_analysis.fear_greed_index,
                (1 - onchain_analysis.whale_activity) * 100,  # Lower whale activity = better
                onchain_analysis.hodler_ratio * 100,
                (onchain_analysis.active_addresses_growth + 0.1) * 250  # Growth adjusted
            ])
            scores.append(max(0, min(100, onchain_score)))
            weights.append(0.20)
            
            # 3. Sentiment Score (15%)
            sentiment_score = np.mean([
                crypto_sentiment.social_sentiment,
                crypto_sentiment.institutional_sentiment,
                crypto_sentiment.technical_sentiment,
                crypto_sentiment.news_sentiment
            ])
            scores.append(sentiment_score)
            weights.append(0.15)
            
            # 4. Tokenomics Score (15%)
            tokenomics_score = 70  # Base score
            if tokenomics_analysis.get('scarcity_level') == 'Çok Yüksek':
                tokenomics_score += 20
            elif tokenomics_analysis.get('scarcity_level') == 'Yüksek':
                tokenomics_score += 10
            
            # Market cap factor
            if tokenomics_analysis.get('market_cap_category') == 'Large Cap':
                tokenomics_score += 5  # Stability
            elif tokenomics_analysis.get('market_cap_category') == 'Small Cap':
                tokenomics_score += 15  # Growth potential
            
            scores.append(min(100, tokenomics_score))
            weights.append(0.15)
            
            # 5. Adoption Score (10%)
            adoption_score = adoption_metrics.get('utility_score', 70)
            scores.append(adoption_score)
            weights.append(0.10)
            
            # 6. Ecosystem Health Score (10%)
            ecosystem_score = ecosystem_health.get('network_security', 75)
            scores.append(ecosystem_score)
            weights.append(0.10)
            
            # 7. Category Bonus (5%)
            category_weight = self.category_weights.get(crypto_profile.category, 1.0)
            category_score = 50 * category_weight
            scores.append(min(100, category_score))
            weights.append(0.05)
            
            # Calculate weighted average
            weighted_score = sum(score * weight for score, weight in zip(scores, weights))
            
            # Apply blockchain bonus
            blockchain_bonus = {
                'bitcoin': 5,
                'ethereum': 3,
                'solana': 2,
                'polygon': 1,
                'avalanche': 1
            }
            bonus = blockchain_bonus.get(crypto_profile.blockchain.lower(), 0)
            
            final_score = min(100, weighted_score + bonus)
            
            return round(final_score, 2)
            
        except Exception as e:
            print(f"WARNING: Ultra crypto score hesaplama hatası: {str(e)}")
            return 50.0
    
    def _calculate_price_targets(self, symbol: str, historical_data: Optional[pd.DataFrame],
                                ultra_crypto_score: float, market_phase: MarketPhase) -> Dict[str, float]:
        """Price target hesaplama"""
        try:
            # Base price (simulated current price)
            base_price = 50000 if symbol.upper() == 'BTC' else 3000 if symbol.upper() == 'ETH' else 1.0
            
            # Score-based multipliers
            if ultra_crypto_score >= 80:
                bullish_multiplier = 1.5
                bearish_multiplier = 0.9
            elif ultra_crypto_score >= 60:
                bullish_multiplier = 1.3
                bearish_multiplier = 0.85
            elif ultra_crypto_score >= 40:
                bullish_multiplier = 1.15
                bearish_multiplier = 0.8
            else:
                bullish_multiplier = 1.05
                bearish_multiplier = 0.75
            
            # Market phase adjustments
            if market_phase in [MarketPhase.BULL_MARKET, MarketPhase.PARABOLIC]:
                bullish_multiplier *= 1.2
            elif market_phase in [MarketPhase.BEAR_MARKET, MarketPhase.CORRECTION]:
                bearish_multiplier *= 0.8
            
            targets = {
                '1_week': round(base_price * np.random.uniform(0.95, 1.05), 2),
                '1_month': round(base_price * np.random.uniform(0.9, 1.15), 2),
                '3_months': round(base_price * np.random.uniform(0.8, bullish_multiplier), 2),
                '6_months': round(base_price * np.random.uniform(bearish_multiplier, bullish_multiplier * 1.1), 2),
                '1_year': round(base_price * np.random.uniform(bearish_multiplier * 0.8, bullish_multiplier * 1.3), 2),
                'bull_target': round(base_price * bullish_multiplier * 1.5, 2),
                'bear_target': round(base_price * bearish_multiplier * 0.7, 2)
            }
            
            return targets
            
        except Exception as e:
            print(f"WARNING: Price targets hesaplama hatası: {str(e)}")
            return {
                '1_month': 50000,
                '3_months': 52000,
                '1_year': 55000
            }
    
    def _assess_crypto_risks(self, crypto_profile: CryptoProfile,
                            blockchain_metrics: BlockchainMetrics,
                            defi_metrics: Optional[DeFiMetrics],
                            onchain_analysis: OnChainAnalysis) -> Dict[str, str]:
        """Crypto risk değerlendirmesi"""
        try:
            risks = {}
            
            # Overall risk
            risk_factors = []
            
            # Volatility risk
            if crypto_profile.category in [CryptoCategory.MEME, CryptoCategory.ALTCOIN]:
                risk_factors.append('Yüksek')
            elif crypto_profile.category in [CryptoCategory.DEFI, CryptoCategory.NFT]:
                risk_factors.append('Orta-Yüksek')
            elif crypto_profile.category in [CryptoCategory.BITCOIN, CryptoCategory.ETHEREUM]:
                risk_factors.append('Orta')
            else:
                risk_factors.append('Orta-Yüksek')
            
            overall_risk = max(risk_factors, key=risk_factors.count) if risk_factors else 'Orta'
            risks['overall_risk'] = overall_risk
            
            # Liquidity risk
            if crypto_profile.market_cap > 10000000000:  # 10B+
                risks['liquidity_risk'] = 'Düşük'
            elif crypto_profile.market_cap > 1000000000:  # 1B+
                risks['liquidity_risk'] = 'Orta'
            else:
                risks['liquidity_risk'] = 'Yüksek'
            
            # Technology risk
            age_days = (datetime.now() - crypto_profile.launch_date).days
            if age_days > 1460 and crypto_profile.technology_score > 80:
                risks['technology_risk'] = 'Düşük'
            elif age_days > 730 and crypto_profile.technology_score > 60:
                risks['technology_risk'] = 'Orta'
            else:
                risks['technology_risk'] = 'Yüksek'
            
            # Regulatory risk
            if crypto_profile.category == CryptoCategory.STABLECOIN:
                risks['regulatory_risk'] = 'Yüksek'
            elif crypto_profile.category in [CryptoCategory.PRIVACY, CryptoCategory.MEME]:
                risks['regulatory_risk'] = 'Yüksek'
            elif crypto_profile.category in [CryptoCategory.BITCOIN, CryptoCategory.ETHEREUM]:
                risks['regulatory_risk'] = 'Düşük-Orta'
            else:
                risks['regulatory_risk'] = 'Orta'
            
            # Smart contract risk (for DeFi)
            if defi_metrics:
                if defi_metrics.audit_score > 95:
                    risks['smart_contract_risk'] = 'Düşük'
                elif defi_metrics.audit_score > 85:
                    risks['smart_contract_risk'] = 'Orta'
                else:
                    risks['smart_contract_risk'] = 'Yüksek'
            
            # Centralization risk
            if blockchain_metrics.validator_count > 5000:
                risks['centralization_risk'] = 'Düşük'
            elif blockchain_metrics.validator_count > 1000:
                risks['centralization_risk'] = 'Orta'
            else:
                risks['centralization_risk'] = 'Yüksek'
            
            return risks
            
        except Exception as e:
            print(f"WARNING: Risk değerlendirme hatası: {str(e)}")
            return {
                'overall_risk': 'Orta Risk',
                'liquidity_risk': 'Orta',
                'technology_risk': 'Orta'
            }
    
    def _generate_trading_recommendation(self, ultra_crypto_score: float,
                                        market_phase: MarketPhase,
                                        risk_assessment: Dict[str, str],
                                        technical_signals: Dict) -> str:
        """Trading recommendation üretme"""
        try:
            # Score-based recommendation
            if ultra_crypto_score >= 75:
                base_rec = "GÜÇLÜ ALIŞ"
            elif ultra_crypto_score >= 65:
                base_rec = "ALIŞ"
            elif ultra_crypto_score >= 55:
                base_rec = "ZAYIF ALIŞ"
            elif ultra_crypto_score >= 45:
                base_rec = "BEKLE"
            elif ultra_crypto_score >= 35:
                base_rec = "ZAYIF SAT"
            else:
                base_rec = "SAT"
            
            # Market phase adjustments
            if market_phase == MarketPhase.PARABOLIC and ultra_crypto_score < 70:
                return "DİKKATLİ ALIŞ"  # Parabolic phase risk
            elif market_phase == MarketPhase.BEAR_MARKET and ultra_crypto_score > 60:
                return "BEKLE"  # Wait for better entry
            elif market_phase == MarketPhase.ACCUMULATION and ultra_crypto_score > 50:
                return "ALIŞ"  # Good accumulation opportunity
            
            # Risk adjustments
            overall_risk = risk_assessment.get('overall_risk', 'Orta')
            if 'Yüksek' in overall_risk and 'ALIŞ' in base_rec:
                return f"DİKKATLİ {base_rec}"
            
            return base_rec
            
        except Exception:
            return "BEKLE"
    
    def _get_default_crypto_result(self, symbol: str) -> UltraCryptoResult:
        """Varsayılan crypto sonucu"""
        return UltraCryptoResult(
            ultra_crypto_score=50.0,
            crypto_profile=CryptoProfile(
                symbol=symbol,
                name=symbol,
                category=CryptoCategory.ALTCOIN,
                market_cap=1000000000,
                circulating_supply=100000000,
                total_supply=100000000,
                max_supply=None,
                launch_date=datetime(2021, 1, 1),
                blockchain='ethereum',
                consensus_mechanism='proof_of_stake',
                use_case='utility',
                team_score=70.0,
                community_score=65.0,
                technology_score=75.0
            ),
            blockchain_metrics=BlockchainMetrics(
                network_hash_rate=100e18,
                active_addresses=1000000,
                transaction_count=1000000,
                transaction_volume=10000000000,
                avg_block_time=15.0,
                network_difficulty=1e15,
                validator_count=1000,
                staking_ratio=0.6,
                gas_price=20.0,
                block_size=2.0,
                mempool_size=50000,
                development_activity=75.0
            ),
            defi_metrics=None,
            onchain_analysis=OnChainAnalysis(
                whale_activity=0.5,
                exchange_inflows=10000000,
                exchange_outflows=12000000,
                hodler_ratio=0.6,
                active_addresses_growth=0.1,
                transaction_velocity=1.0,
                network_value_to_transactions=20,
                realized_cap=5000000000,
                market_value_to_realized_value=1.5,
                fear_greed_index=50
            ),
            crypto_sentiment=CryptoSentiment(
                social_sentiment=50,
                news_sentiment=50,
                reddit_sentiment=50,
                twitter_sentiment=50,
                telegram_sentiment=50,
                google_trends=50,
                institutional_sentiment=50,
                retail_sentiment=50,
                influencer_sentiment=50,
                technical_sentiment=50
            ),
            market_phase=MarketPhase.CONSOLIDATION,
            trading_recommendation="BEKLE",
            price_targets={'1_month': 50000, '3_months': 52000},
            risk_assessment={'overall_risk': 'Orta Risk'},
            technical_signals={'momentum_score': 50.0},
            fundamental_analysis={'network_health': 75.0},
            tokenomics_analysis={'scarcity_level': 'Orta'},
            adoption_metrics={'utility_score': 70},
            ecosystem_health={'network_security': 75.0}
        )
