"""
PlanB Motoru - Kripto Para Veri Sağlayıcısı
Kripto para birimleri veri sağlayıcısı
"""
import requests
from typing import List, Dict, Optional
from .base_provider import BaseProvider
from src.utils.logger import log_info, log_error, log_debug, log_warning

class CryptoProvider(BaseProvider):
    """Kripto para veri sağlayıcısı"""
    
    def __init__(self):
        super().__init__("Crypto")
        self.symbols = []
        self._load_symbols()
    
    def _load_symbols(self):
        """Kripto sembollerini yükle - Tam liste öncelikli"""
        try:
            # Tam listeyi direkt kullan
            self._load_fallback_symbols()
            log_info(f"Crypto: {len(self.symbols)} sembol yüklendi (tam liste)")
            
        except Exception as e:
            log_error(f"Crypto tam liste yüklenirken hata: {e}")
            # CoinGecko API'yi dene
            try:
                self._load_from_coingecko()
            except Exception as e2:
                log_error(f"CoinGecko API hatası: {e2}")
                # Son çare: Basit liste
                self.symbols = ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD"]
                log_warning("Crypto: Minimal sembol listesi kullanılıyor")
    
    def _load_from_coingecko(self):
        """CoinGecko API'den kripto paraları yükle"""
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 50,  # 50 kripto
                "page": 1,
                "sparkline": False
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if not data or len(data) == 0:
                raise ValueError("CoinGecko'dan veri alınamadı")
            
            # Sembolleri formatla
            self.symbols = [f"{coin['symbol'].upper()}-USD" for coin in data]
            
            log_info(f"Crypto: {len(self.symbols)} sembol yüklendi (CoinGecko API)")
            
        except Exception as e:
            raise e
    
    def _load_from_coinmarketcap(self):
        """CoinMarketCap benzeri API'den kripto paraları yükle"""
        try:
            # Basit veri yapısı simülasyonu
            # Gerçek kullanımda CoinMarketCap API key gerekir
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
            
            # Demo için fallback'e geç
            raise ValueError("CoinMarketCap API key gerekli")
            
        except Exception as e:
            raise e
    
    def _load_fallback_symbols(self):
        """Tam listeye göre kripto sembol listesi - 80 sembol"""
        self.symbols = [
            # TAM LİSTEDEN ALINAN KRİPTO SEMBOLLER (80 adet)
            "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", 
            "DOT-USD", "TRX-USD", "LINK-USD", "MATIC-USD", "SHIB-USD", "LTC-USD", "UNI-USD", "ATOM-USD", 
            "XLM-USD", "XMR-USD", "ETC-USD", "ALGO-USD", "BCH-USD", "VET-USD", "FIL-USD", "XTZ-USD", 
            "EOS-USD", "AAVE-USD", "ICP-USD", "THETA-USD", "XDC-USD", "FTM-USD", "EGLD-USD", "NEAR-USD", 
            "GRT-USD", "QNT-USD", "RUNE-USD", "BSV-USD", "NEO-USD", "KLAY-USD", "MIOTA-USD", "BTT-USD", 
            "CAKE-USD", "CHZ-USD", "HBAR-USD", "KSM-USD", "MKR-USD", "ENJ-USD", "STX-USD", "CRV-USD", 
            "COMP-USD", "ZEC-USD", "BAT-USD", "DASH-USD", "WAVES-USD", "MANA-USD", "SAND-USD", "SNX-USD", 
            "YFI-USD", "CELO-USD", "ONE-USD", "GALA-USD", "IMX-USD", "APE-USD", "RNDR-USD", "APT-USD", 
            "ARB-USD", "OP-USD", "SUI-USD", "SEI-USD", "TIA-USD", "INJ-USD", "PYTH-USD", "JUP-USD", 
            "FET-USD", "AGIX-USD", "OCEAN-USD", "RPL-USD", "LDO-USD", "SSV-USD", "MINA-USD", "ROSE-USD"
        ]
        log_warning(f"Crypto: Tam listeye göre güncellenmiş sembol listesi kullanılıyor ({len(self.symbols)} sembol)")
    
    def get_symbols(self) -> List[str]:
        """Kripto sembol listesini getir"""
        return self.symbols.copy()
    
    def get_market_info(self) -> Dict[str, any]:
        """Crypto pazar bilgilerini getir"""
        return {
            'market_name': 'Cryptocurrency',
            'country': 'Global',
            'currency': 'USD',
            'timezone': 'UTC',
            'trading_hours': '24/7',
            'symbol_count': len(self.symbols)
        }
    
    def get_top_symbols(self, limit: int = 20) -> List[str]:
        """En çok işlem gören kripto paraları getir"""
        top_crypto = [
            "BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "SOL-USD",
            "XRP-USD", "DOT-USD", "DOGE-USD", "AVAX-USD", "SHIB-USD",
            "MATIC-USD", "LTC-USD", "UNI-USD", "LINK-USD", "ATOM-USD",
            "ALGO-USD", "VET-USD", "ICP-USD", "FIL-USD", "TRX-USD"
        ]
        
        return top_crypto[:limit]
    
    def get_category_symbols(self, category: str) -> List[str]:
        """Kategoriye göre kripto paraları getir"""
        category_mapping = {
            'bitcoin': ['BTC-USD'],
            'ethereum': ['ETH-USD'],
            'defi': ['UNI-USD', 'AAVE-USD', 'COMP-USD', 'MKR-USD', 'SNX-USD'],
            'layer1': ['ETH-USD', 'ADA-USD', 'SOL-USD', 'DOT-USD', 'AVAX-USD', 'ATOM-USD', 'ALGO-USD'],
            'layer2': ['MATIC-USD', 'OP-USD', 'ARB-USD'],
            'meme': ['DOGE-USD', 'SHIB-USD', 'PEPE-USD'],
            'storage': ['FIL-USD', 'AR-USD', 'SC-USD'],
            'gaming': ['AXS-USD', 'SAND-USD', 'MANA-USD', 'GALA-USD'],
            'ai': ['FET-USD', 'AGIX-USD', 'OCEAN-USD'],
            'privacy': ['XMR-USD', 'ZEC-USD', 'DASH-USD']
        }
        
        return category_mapping.get(category.lower(), [])
    
    def get_market_cap_symbols(self, min_cap: str = "large") -> List[str]:
        """Piyasa değerine göre kripto paraları getir"""
        if min_cap.lower() == "large":
            # Büyük kripto paralar (Top 10)
            return ["BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "SOL-USD", "XRP-USD", "DOT-USD", "DOGE-USD", "AVAX-USD", "SHIB-USD"]
        elif min_cap.lower() == "mid":
            # Orta kripto paralar (11-50)
            return ["MATIC-USD", "LTC-USD", "UNI-USD", "LINK-USD", "ATOM-USD", "ALGO-USD", "VET-USD", "ICP-USD", "FIL-USD", "TRX-USD"]
        else:
            # Küçük kripto paralar (51+)
            return ["XLM-USD", "BCH-USD", "EOS-USD", "XTZ-USD", "NEO-USD", "IOTA-USD", "ZEC-USD", "DASH-USD", "XMR-USD", "ETC-USD"]
    
    def get_stablecoins(self) -> List[str]:
        """Stablecoin'leri getir"""
        return ["USDT-USD", "USDC-USD", "BUSD-USD", "DAI-USD", "TUSD-USD"]
    
    def validate_symbol(self, symbol: str) -> bool:
        """Kripto sembol geçerliliğini kontrol et"""
        return symbol in self.symbols
    
    def get_company_info(self, symbol: str) -> Optional[Dict[str, any]]:
        """Kripto para bilgilerini getir (lansman tarihi)"""
        if not symbol.endswith('-USD'):
            symbol = f"{symbol}-USD"
        
        if symbol not in self.symbols:
            return None
        
        # Kripto para bilgileri (isim + lansman tarihi)
        crypto_info = {
            "BTC-USD": {"name": "Bitcoin", "founding_date": "2009-01-03"},
            "ETH-USD": {"name": "Ethereum", "founding_date": "2015-07-30"},
            "BNB-USD": {"name": "Binance Coin", "founding_date": "2017-07-25"},
            "ADA-USD": {"name": "Cardano", "founding_date": "2017-09-29"},
            "SOL-USD": {"name": "Solana", "founding_date": "2020-03-16"},
            "XRP-USD": {"name": "Ripple", "founding_date": "2012-06-01"},
            "DOT-USD": {"name": "Polkadot", "founding_date": "2020-05-26"},
            "DOGE-USD": {"name": "Dogecoin", "founding_date": "2013-12-06"},
            "AVAX-USD": {"name": "Avalanche", "founding_date": "2020-09-21"},
            "SHIB-USD": {"name": "Shiba Inu", "founding_date": "2020-08-01"},
            "MATIC-USD": {"name": "Polygon", "founding_date": "2019-05-01"},
            "LTC-USD": {"name": "Litecoin", "founding_date": "2011-10-07"},
            "UNI-USD": {"name": "Uniswap", "founding_date": "2020-09-17"},
            "LINK-USD": {"name": "Chainlink", "founding_date": "2017-09-20"},
            "ATOM-USD": {"name": "Cosmos", "founding_date": "2019-03-14"},
            "FTM-USD": {"name": "Fantom", "founding_date": "2018-12-01"},
            "ALGO-USD": {"name": "Algorand", "founding_date": "2019-06-19"},
            "VET-USD": {"name": "VeChain", "founding_date": "2015-08-01"},
            "FIL-USD": {"name": "Filecoin", "founding_date": "2017-08-10"},
            "TRX-USD": {"name": "TRON", "founding_date": "2017-09-01"},
            "ETC-USD": {"name": "Ethereum Classic", "founding_date": "2016-07-20"},
            "XLM-USD": {"name": "Stellar", "founding_date": "2014-07-31"},
            "BCH-USD": {"name": "Bitcoin Cash", "founding_date": "2017-08-01"},
            "EOS-USD": {"name": "EOS", "founding_date": "2017-06-26"},
            "AAVE-USD": {"name": "Aave", "founding_date": "2020-10-01"},
            "SUSHI-USD": {"name": "SushiSwap", "founding_date": "2020-08-28"},
            "COMP-USD": {"name": "Compound", "founding_date": "2020-06-15"},
            "MKR-USD": {"name": "Maker", "founding_date": "2017-12-18"},
            "YFI-USD": {"name": "Yearn Finance", "founding_date": "2020-07-17"},
            "SNX-USD": {"name": "Synthetix", "founding_date": "2018-03-01"},
            "USDT-USD": {"name": "Tether", "founding_date": "2014-10-06"},
            "USDC-USD": {"name": "USD Coin", "founding_date": "2018-09-26"},
            "DAI-USD": {"name": "Dai", "founding_date": "2017-12-18"},
            "BUSD-USD": {"name": "Binance USD", "founding_date": "2019-09-05"},
            "TUSD-USD": {"name": "TrueUSD", "founding_date": "2018-03-06"},
            "WBTC-USD": {"name": "Wrapped Bitcoin", "founding_date": "2019-01-31"},
            "REN-USD": {"name": "Ren", "founding_date": "2017-08-01"},
            "KNC-USD": {"name": "Kyber Network", "founding_date": "2017-09-24"},
            "BAT-USD": {"name": "Basic Attention Token", "founding_date": "2017-05-31"},
            "ZRX-USD": {"name": "0x Protocol", "founding_date": "2017-08-15"},
            "REP-USD": {"name": "Augur", "founding_date": "2015-10-27"},
            "OMG-USD": {"name": "OMG Network", "founding_date": "2017-07-01"},
            "LRC-USD": {"name": "Loopring", "founding_date": "2017-08-01"},
            "ENJ-USD": {"name": "Enjin Coin", "founding_date": "2017-11-01"},
            "MANA-USD": {"name": "Decentraland", "founding_date": "2017-09-17"},
            "SAND-USD": {"name": "The Sandbox", "founding_date": "2020-08-14"},
            "AXS-USD": {"name": "Axie Infinity", "founding_date": "2020-11-04"},
            "CHZ-USD": {"name": "Chiliz", "founding_date": "2018-02-01"},
            "FLOW-USD": {"name": "Flow", "founding_date": "2020-10-01"},
            "ICP-USD": {"name": "Internet Computer", "founding_date": "2021-05-10"},
            "NEAR-USD": {"name": "NEAR Protocol", "founding_date": "2020-10-13"},
            "APT-USD": {"name": "Aptos", "founding_date": "2022-10-17"},
            "SUI-USD": {"name": "Sui", "founding_date": "2023-05-03"},
            "ARB-USD": {"name": "Arbitrum", "founding_date": "2023-03-23"},
            "OP-USD": {"name": "Optimism", "founding_date": "2022-05-31"},
            "INJ-USD": {"name": "Injective", "founding_date": "2020-11-01"},
            "SEI-USD": {"name": "Sei", "founding_date": "2023-08-15"},
            "TIA-USD": {"name": "Celestia", "founding_date": "2023-10-31"},
            "JUP-USD": {"name": "Jupiter", "founding_date": "2024-01-31"},
            "WIF-USD": {"name": "dogwifhat", "founding_date": "2023-11-20"},
            "BONK-USD": {"name": "Bonk", "founding_date": "2022-12-25"},
            "PEPE-USD": {"name": "Pepe", "founding_date": "2023-04-17"},
            "FLOKI-USD": {"name": "Floki", "founding_date": "2021-06-25"}
        }
        
        # Kripto para bilgilerini al
        info = crypto_info.get(symbol, {
            "name": f"{symbol.replace('-USD', '')}",
            "founding_date": "2020-01-01"  # Varsayılan tarih
        })
        
        return {
            "symbol": symbol,
            "name": info["name"],
            "founding_date": info["founding_date"],
            "market": "Crypto",
            "country": "Global",
            "currency": "USD"
        }

