"""
PlanB Motoru - NASDAQ Veri Sağlayıcısı
NASDAQ veri sağlayıcısı
"""
import pandas as pd
import requests
from typing import List, Dict, Optional
from .base_provider import BaseProvider
from src.utils.logger import log_info, log_error, log_debug, log_warning

class NASDAQProvider(BaseProvider):
    """NASDAQ veri sağlayıcısı"""
    
    def __init__(self):
        super().__init__("NASDAQ")
        self.symbols = []
        self._load_symbols()
    
    def _load_symbols(self):
        """NASDAQ sembollerini yükle - Optimize edilmiş liste (NASDAQ100 + 20 ek)"""
        try:
            # TAM LİSTEYE GÖRE NASDAQ SEMBOLLER (109 adet)
            nasdaq_symbols = [
                "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "AVGO", "COST", "PEP",
                "ADBE", "CSCO", "TMUS", "CMCSA", "QCOM", "AMGN", "HON", "INTC", "INTU", "AMD",
                "SBUX", "GILD", "AMAT", "ADP", "MDLZ", "REGN", "VRTX", "ISRG", "PYPL", "ATVI",
                "MRNA", "ADI", "BKNG", "IDXX", "KDP", "SNPS", "ASML", "CHTR", "MU", "MAR",
                "MNST", "LRCX", "KLAC", "NXPI", "CSX", "AEP", "CTAS", "ORLY", "EXC", "MELI",
                "PAYX", "XEL", "DXCM", "WBA", "ROST", "BIIB", "VRSK", "ILMN", "WDAY", "PCAR",
                "EBAY", "DLTR", "CTSH", "FAST", "CPRT", "ODFL", "SGEN", "SIRI", "ALGN", "ANSS",
                "BIDU", "SWKS", "JD", "VOD", "LCID", "RIVN", "FSLR", "ZS", "CRWD", "DDOG",
                "NET", "ASAN", "PLTR", "SNOW", "OKTA", "MDB", "TWLO", "AFRM", "UPST", "COIN",
                "HOOD", "RBLX", "AI", "PATH", "BLZE", "SDGR", "BEAM", "NTLA", "CRSP", "VERV",
                "NVCR", "TNGX", "SPT", "DOCN", "FIGS", "AVPT", "BLND", "BFLY", "CDNS"
            ]
            
            self.symbols = nasdaq_symbols
            log_info(f"NASDAQ: {len(self.symbols)} sembol yüklendi (tam listeye göre)")
            
        except Exception as e:
            log_error(f"NASDAQ sembolleri tam listeden yüklenirken hata: {e}")
            try:
                # Alternatif: Yahoo Finance'dan NASDAQ hisselerini çek
                self._load_from_yahoo()
            except Exception as e2:
                log_error(f"Yahoo'dan yükleme hatası: {e2}")
                # Son çare: Genişletilmiş fallback liste
                self._load_fallback_symbols()
    
    def _load_from_yahoo(self):
        """Yahoo Finance'dan NASDAQ hisselerini yükle"""
        try:
            # Yahoo Finance screener API
            url = "https://query1.finance.yahoo.com/v1/finance/screener"
            params = {
                "formatted": "true",
                "lang": "en-US",
                "region": "US",
                "scrIds": "most_actives",
                "count": 10000,
                "corsDomain": "finance.yahoo.com"
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            symbols = []
            if 'finance' in data and 'result' in data['finance']:
                for result in data['finance']['result']:
                    if 'quotes' in result:
                        for quote in result['quotes']:
                            if 'symbol' in quote:
                                symbol = quote['symbol']
                                if symbol and len(symbol) <= 5 and symbol.isalpha():
                                    symbols.append(symbol)
            
            if symbols:
                self.symbols = list(set(symbols))
                log_info(f"NASDAQ: {len(self.symbols)} sembol yüklendi (Yahoo'dan)")
            else:
                raise ValueError("Yahoo'dan sembol bulunamadı")
                
        except Exception as e:
            raise e
    
    def _load_fallback_symbols(self):
        """Optimize edilmiş NASDAQ sembol listesi - NASDAQ100 + 100 öneri"""
        self.symbols = [
            # NASDAQ 100 - En büyük teknoloji şirketleri
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "CRM",
            "PYPL", "INTC", "AMD", "CSCO", "ORCL", "IBM", "QCOM", "TXN", "AVGO", "AMAT",
            "MU", "ADI", "LRCX", "KLAC", "MCHP", "SNPS", "CDNS", "ANSS", "FTNT", "PANW",
            "CHTR", "CMCSA", "COST", "CSX", "CTAS", "CTSH", "DDOG", "DXCM", "EA", "EBAY",
            "EXC", "FANG", "FAST", "FISV", "GILD", "GOOG", "HON", "IDXX", "ILMN", "INTU",
            "ISRG", "JD", "KDP", "KHC", "LULU", "MAR", "MDLZ", "MELI", "MNST", "MRNA",
            "MRVL", "MTCH", "NTES", "NXPI", "OKTA", "ORLY", "PAYX", "PCAR", "PDD", "PEP",
            "PTON", "REGN", "ROST", "SBUX", "SGEN", "SIRI", "SPLK", "SWKS", "TEAM", "TMUS",
            "VRSK", "VRSN", "VRTX", "WBA", "WDAY", "XEL", "ZM", "ZS", "ALGN", "AMGN",
            "ASML", "ATVI", "BIDU", "BIIB", "BKNG", "CPRT", "CSGP", "DLTR", "EXPE", "INCY",
            "IP", "IPG", "IQV", "IR", "IRM", "IT", "ITW", "IVZ", "J", "JBHT", "JCI",
            "JKHY", "JNJ", "JNPR", "JPM", "K", "KEY", "KEYS", "KIM", "KMB", "KMI",
            "KMX", "KO", "KR", "KSU", "L", "LB", "LDOS", "LEG", "LEN", "LH",
            "LHX", "LIN", "LKQ", "LLY", "LMT", "LNC", "LNT", "LOW", "LUMN", "LUV",
            "LVS", "LW", "LYB", "LYV", "MA", "MAA", "MAS", "MCD", "MCK", "MCO",
            "MDT", "MET", "MGM", "MHK", "MKC", "MKTX", "MLM", "MMC", "MMM", "MO",
            "MOH", "MRK", "MRO", "MS", "MSCI", "MSI", "MTB", "MTD", "NCLH", "NDAQ",
            "NEE", "NEM", "NI", "NKE", "NLOK", "NOC", "NOV", "NOW", "NRG", "NSC",
            "NTAP", "NTRS", "NUE", "NVR", "NWL", "NWS", "NWSA", "O", "ODFL", "OGN",
            "OKE", "OMC", "OTIS", "OXY", "PAYC", "PBCT", "PEAK", "PEG", "PENN", "PFE",
            "PG", "PGR", "PH", "PHM", "PKG", "PKI", "PLD", "PM", "PNC", "PNR",
            "PNW", "POOL", "PPG", "PPL", "PRU", "PSA", "PSX", "PTC", "PVH", "PWR",
            "PXD", "QRVO", "RCL", "RE", "REG", "RF", "RHI", "RJF", "RL", "RMBS",
            "RMD", "ROK", "ROL", "ROP", "RSG", "RTX", "SBAC", "SCHW", "SEDG", "SEE",
            "SHW", "SIVB", "SJM", "SLB", "SNA", "SO", "SPG", "SPGI", "SRE", "STE",
            "STT", "STX", "STZ", "SWK", "SYF", "SYY", "T", "TAP", "TDG", "TDY",
            "TEL", "TER", "TFC", "TFX", "TGT", "TMO", "TPG", "TROW", "TRV", "TSCO",
            "TSN", "TT", "TTWO", "TWTR", "TXT", "TYL", "UA", "UAA", "UAL", "UDR",
            "UHS", "ULTA", "UNH", "UNM", "UNP", "UPS", "URI", "USB", "V", "VFC",
            "VIAC", "VLO", "VMC", "VTR", "VTRS", "VZ", "WAB", "WAT", "WEC", "WELL",
            "WFC", "WHR", "WLTW", "WM", "WMB", "WMT", "WRB", "WST", "WU", "WY",
            "WYNN", "XLNX", "XOM", "XRAY", "XRX", "XYL", "YUM", "ZBH", "ZBRA", "ZION",
            "ZTS"
        ]
        log_warning(f"NASDAQ: Optimize edilmiş sembol listesi kullanılıyor ({len(self.symbols)} sembol)")
    
    def get_symbols(self) -> List[str]:
        """NASDAQ sembol listesini getir"""
        return self.symbols.copy()
    
    def get_market_info(self) -> Dict[str, any]:
        """NASDAQ pazar bilgilerini getir"""
        return {
            'market_name': 'NASDAQ',
            'country': 'United States',
            'currency': 'USD',
            'timezone': 'America/New_York',
            'trading_hours': '09:30-16:00',
            'symbol_count': len(self.symbols)
        }
    
    def get_market_data(self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """NASDAQ hisse verilerini getir"""
        try:
            # yfinance ile veri çek
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                log_warning(f"NASDAQ {symbol} için veri bulunamadı")
                return None
            
            return data
            
        except Exception as e:
            log_error(f"NASDAQ {symbol} veri çekme hatası: {e}")
            return None
    
    def get_company_info(self, symbol: str) -> Optional[Dict[str, any]]:
        """Şirket bilgilerini getir"""
        if not symbol.endswith('.US'):
            symbol = f"{symbol}.US"
        
        if symbol.replace('.US', '') not in self.symbols:
            return None
        
        # NASDAQ şirket bilgileri (isim + kuruluş tarihi)
        company_info = {
            "AAPL.US": {"name": "Apple Inc.", "founding_date": "1976-04-01"},
            "MSFT.US": {"name": "Microsoft Corporation", "founding_date": "1975-04-04"},
            "GOOGL.US": {"name": "Alphabet Inc. (Google)", "founding_date": "1998-09-04"},
            "GOOG.US": {"name": "Alphabet Inc. (Google)", "founding_date": "1998-09-04"},
            "AMZN.US": {"name": "Amazon.com Inc.", "founding_date": "1994-07-05"},
            "NVDA.US": {"name": "NVIDIA Corporation", "founding_date": "1993-01-01"},
            "META.US": {"name": "Meta Platforms Inc. (Facebook)", "founding_date": "2004-02-04"},
            "TSLA.US": {"name": "Tesla Inc.", "founding_date": "2003-07-01"},
            "NFLX.US": {"name": "Netflix Inc.", "founding_date": "1997-08-29"},
            "ADBE.US": {"name": "Adobe Inc.", "founding_date": "1982-12-01"},
            "CSCO.US": {"name": "Cisco Systems Inc.", "founding_date": "1984-12-10"},
            "INTC.US": {"name": "Intel Corporation", "founding_date": "1968-07-18"},
            "AMD.US": {"name": "Advanced Micro Devices Inc.", "founding_date": "1969-05-01"},
            "PYPL.US": {"name": "PayPal Holdings Inc.", "founding_date": "1998-12-01"},
            "CRM.US": {"name": "Salesforce Inc.", "founding_date": "1999-02-01"},
            "ORCL.US": {"name": "Oracle Corporation", "founding_date": "1977-06-16"},
            "IBM.US": {"name": "International Business Machines Corp.", "founding_date": "1911-06-16"},
            "UBER.US": {"name": "Uber Technologies Inc.", "founding_date": "2009-03-01"},
            "LYFT.US": {"name": "Lyft Inc.", "founding_date": "2012-06-01"},
            "SNAP.US": {"name": "Snap Inc.", "founding_date": "2011-09-01"},
            "TWTR.US": {"name": "Twitter Inc.", "founding_date": "2006-03-21"},
            "SQ.US": {"name": "Block Inc. (Square)", "founding_date": "2009-02-01"},
            "ROKU.US": {"name": "Roku Inc.", "founding_date": "2002-10-01"},
            "ZM.US": {"name": "Zoom Video Communications Inc.", "founding_date": "2011-04-01"},
            "DOCU.US": {"name": "DocuSign Inc.", "founding_date": "2003-01-01"},
            "OKTA.US": {"name": "Okta Inc.", "founding_date": "2009-01-01"},
            "CRWD.US": {"name": "CrowdStrike Holdings Inc.", "founding_date": "2011-01-01"},
            "ZS.US": {"name": "Zscaler Inc.", "founding_date": "2007-01-01"},
            "NET.US": {"name": "Cloudflare Inc.", "founding_date": "2009-07-01"},
            "DDOG.US": {"name": "Datadog Inc.", "founding_date": "2010-01-01"}
        }
        
        # Şirket bilgilerini al
        info = company_info.get(symbol, {
            "name": f"{symbol.replace('.US', '')} Inc.",
            "founding_date": "2000-01-01"  # Varsayılan tarih
        })
        
        return {
            "symbol": symbol,
            "name": info["name"],
            "founding_date": info["founding_date"],
            "market": "NASDAQ",
            "country": "USA",
            "currency": "USD"
        }
