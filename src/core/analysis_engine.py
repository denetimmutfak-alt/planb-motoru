"""
PlanB Motoru - Ana Analiz Motoru
"""
import pandas as pd
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from config.settings import config
from src.utils.logger import log_info, log_error, log_warning, log_success
from src.data.market_data import MarketDataProvider
from src.analysis.financial_analysis import FinancialAnalyzer
from src.analysis.economic_cycle import ultra_economic_analyzer

class PlanBAnalysisEngine:
    """PlanB Motoru ana analiz sınıfı"""
    
    def __init__(self):
        self.config = config.load_from_file()
        self.market_data = MarketDataProvider()
        self.financial_analyzer = FinancialAnalyzer()
        self.database_path = config.DATABASE_PATH
        
        # Veritabanını hazırla
        self._setup_database()
    
    def _setup_database(self):
        """Veritabanını kur ve hazırla"""
        try:
            # Veritabanı klasörünü oluştur
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
            
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Eski tabloyu sil ve yenisini oluştur
            cursor.execute('DROP TABLE IF EXISTS analizler')
            
            cursor.execute('''
                CREATE TABLE analizler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tarih TEXT NOT NULL,
                    hisse_kodu TEXT NOT NULL,
                    finansal_puan REAL,
                    teknik_puan REAL,
                    trend_puan REAL,
                    gann_puan REAL,
                    astroloji_puan REAL,
                    shemitah_puan REAL,
                    cycle21_puan REAL,
                    solar_cycle_puan REAL,
                    economic_cycle_puan REAL,
                    toplam_puan REAL NOT NULL,
                    sinyal TEXT NOT NULL,
                    pazar TEXT,
                    guncel_fiyat REAL,
                    bir_ay_sonraki_fiyat REAL,
                    momentum_skor REAL,
                    breakout_skor REAL,
                    volume_skor REAL,
                    al_sinyal TEXT,
                    al_guven REAL,
                    tutma_suresi INTEGER,
                    tutma_tipi TEXT,
                    hedef_fiyat_1gun REAL,
                    hedef_fiyat_1hafta REAL,
                    hedef_fiyat_1ay REAL,
                    hedef_fiyat_3ay REAL,
                    risk_reward_oran REAL,
                    volatilite REAL,
                    trend_guclu REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # İndeksler oluştur
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_hisse_kodu ON analizler(hisse_kodu)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tarih ON analizler(tarih)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sinyal ON analizler(sinyal)')
            
            conn.commit()
            conn.close()
            
            log_success("Veritabanı hazırlandı")
            
        except Exception as e:
            log_error(f"Veritabanı kurulumunda hata: {e}")
    
    def analyze_single_symbol(self, symbol: str) -> Optional[Dict]:
        """Tek bir sembolü analiz et"""
        try:
            log_info(f"{symbol} analiz ediliyor...")
            
            # Hisse senedi verilerini getir
            stock_data = self.market_data.get_stock_data(symbol)
            if stock_data is None:
                log_warning(f"{symbol} için veri bulunamadı")
                return None
            
            # Dict'i DataFrame'e çevir
            if isinstance(stock_data, dict):
                stock_data = pd.DataFrame.from_dict(stock_data, orient='index')
                stock_data.index = pd.to_datetime(stock_data.index)
            
            if stock_data.empty:
                log_warning(f"{symbol} için veri bulunamadı")
                return None
            
            # Hisse senedi bilgilerini getir
            stock_info = self.market_data.get_stock_info(symbol)
            if stock_info is None:
                log_warning(f"{symbol} için bilgi bulunamadı")
                return None
            
            # Finansal sağlamlık puanını hesapla
            financial_score = self.financial_analyzer.calculate_financial_health_score(symbol, stock_info)
            
            # Teknik göstergeleri hesapla
            technical_indicators = self.financial_analyzer.calculate_technical_indicators(stock_data)
            
            # Trend analizi yap
            trend_analysis = self.financial_analyzer.analyze_trend(stock_data)
            
            # Gann analizi yap
            gann_analysis = self.financial_analyzer.calculate_gann_analysis(stock_data)
            
            # Sinyal üret (gelişmiş versiyon)
            signal, total_score, detailed_analysis = self.financial_analyzer.generate_signal(
                financial_score, technical_indicators, trend_analysis, gann_analysis, symbol, stock_data
            )
            
            # Pazar türünü belirle
            market_type = self._determine_market_type(symbol)
            
            # Tutma süresi bilgisini al
            hold_days = detailed_analysis.get('hold_days', 14)
            
            # Vedik analiz bilgisini ekle
            vedic_analysis = "Geleneksel"
            if 'vedic_analysis' in detailed_analysis:
                vedic_analysis = detailed_analysis['vedic_analysis']
            elif 'vedic_score' in detailed_analysis:
                vedic_analysis = "Vedik"
            
            # Sonuçları derle
            result = {
                'symbol': symbol,
                'market': market_type,
                'financial_score': detailed_analysis.get('financial_score', financial_score),
                'technical_score': detailed_analysis.get('technical_score', technical_indicators.get('rsi', 0)),
                'trend_score': detailed_analysis.get('trend_score', trend_analysis.get('strength', 0)),
                'gann_score': detailed_analysis.get('gann_score', gann_analysis.get('gann_score', 0)),
                'astrology_score': detailed_analysis.get('astrology_score', 0),
                'shemitah_score': detailed_analysis.get('shemitah_score', 0),
                'cycle21_score': detailed_analysis.get('cycle21_score', 0),
                'solar_cycle_score': detailed_analysis.get('solar_cycle_score', 0),
                'economic_cycle_score': detailed_analysis.get('economic_cycle_score', 0),
                'total_score': total_score,
                'signal': signal,
                'hold_days': hold_days,
                'trend': trend_analysis.get('trend', 'Bilinmiyor'),
                'rsi': technical_indicators.get('rsi', 0),
                'current_price': stock_data['Close'].iloc[-1],
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'detailed_analysis': detailed_analysis,
                'vedic_analysis': vedic_analysis
            }
            
            # Veritabanına kaydet
            self._save_analysis_to_db(result)
            
            log_success(f"{symbol} analizi tamamlandı - Sinyal: {signal}, Puan: {total_score:.1f}")
            return result
            
        except Exception as e:
            log_error(f"{symbol} analiz edilirken hata: {e}")
            return None
    
    def analyze_multiple_symbols(self, symbols: List[str], max_workers: int = 12) -> List[Dict]:
        """Birden fazla sembolü paralel analiz et - OPTİMİZE EDİLMİŞ"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import threading
        import time
        
        results = []
        total_symbols = len(symbols)
        completed_count = 0
        lock = threading.Lock()
        
        log_info(f"{total_symbols} sembol paralel analiz edilecek (max {max_workers} thread, hızlı mod)...")
        
        def analyze_with_progress(symbol):
            nonlocal completed_count
            try:
                # Hızlı mod - rate limiting azaltıldı
                time.sleep(0.02)
                
                result = self.analyze_single_symbol(symbol)
                with lock:
                    completed_count += 1
                    if completed_count % 25 == 0 or completed_count == total_symbols:
                        log_info(f"İlerleme: {completed_count}/{total_symbols} ({completed_count/total_symbols*100:.1f}%)")
                return result
            except Exception as e:
                with lock:
                    completed_count += 1
                log_error(f"{symbol} analiz edilirken hata: {e}")
                return None
        
        # Paralel analiz - OPTİMİZE EDİLMİŞ
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_symbol = {executor.submit(analyze_with_progress, symbol): symbol for symbol in symbols}
            
            for future in as_completed(future_to_symbol):
                result = future.result()
                if result:
                    results.append(result)
        
        log_success(f"Paralel analiz tamamlandı: {len(results)}/{total_symbols} başarılı")
        return results
    
    def _filter_symbols_by_market(self, symbols: List[str], market_filter: str) -> List[str]:
        """Sembolleri piyasaya göre filtrele"""
        if market_filter == 'all':
            return symbols
        
        filtered_symbols = []
        for symbol in symbols:
            if market_filter == 'bist' and symbol.endswith('.IS'):
                filtered_symbols.append(symbol)
            elif market_filter == 'nasdaq' and not any(symbol.endswith(suffix) for suffix in ['.IS', '.DE', '-USD', '=F']):
                filtered_symbols.append(symbol)
            elif market_filter == 'xetra' and symbol.endswith('.DE'):
                filtered_symbols.append(symbol)
            elif market_filter == 'crypto' and symbol.endswith('-USD'):
                filtered_symbols.append(symbol)
            elif market_filter == 'commodities' and symbol.endswith('=F'):
                filtered_symbols.append(symbol)
        
        return filtered_symbols
    
    def _get_market_name(self, market_filter: str) -> str:
        """Market filter'dan piyasa adını al"""
        market_names = {
            'all': 'Tam mod',
            'bist': 'BIST',
            'nasdaq': 'NASDAQ',
            'xetra': 'XETRA',
            'crypto': 'Crypto',
            'commodities': 'Emtia'
        }
        return market_names.get(market_filter, 'Bilinmeyen piyasa')
    
    def run_full_analysis(self, test_mode: bool = None, market_filter: str = 'all') -> List[Dict]:
        """Tam analiz çalıştır"""
        try:
            if test_mode is None:
                test_mode = config.TEST_MODE
            
            log_info("PlanB Motoru - Tam Analiz Başlatılıyor...")
            
            # Sembolleri getir
            symbols = self.market_data.get_all_symbols(test_mode)
            if not symbols:
                log_error("Analiz edilecek sembol bulunamadı")
                return []
            
            # Market filter uygula
            if market_filter != 'all':
                symbols = self._filter_symbols_by_market(symbols, market_filter)
                if not symbols:
                    log_error(f"{market_filter} piyasası için sembol bulunamadı")
                    return []
            
            # Test modu logla
            if test_mode:
                log_info(f"Test modu aktif - {len(symbols)} sembol analiz edilecek: {symbols}")
            else:
                market_name = self._get_market_name(market_filter)
                log_info(f"{market_name} - {len(symbols)} sembol analiz edilecek")
            
            # Analizi çalıştır
            results = self.analyze_multiple_symbols(symbols)
            
            # Sonuçları sırala
            results.sort(key=lambda x: x['total_score'], reverse=True)
            
            # Özet rapor
            self._generate_summary_report(results)
            
            return results
            
        except Exception as e:
            log_error(f"Tam analiz çalıştırılırken hata: {e}")
            return []
    
    def _determine_market_type(self, symbol: str) -> str:
        """Sembolün pazar türünü belirle"""
        if symbol.endswith('.IS'):
            return 'BIST'
        elif symbol.endswith('-USD'):
            return 'Kripto'
        elif symbol.endswith('=F'):
            return 'Emtia'
        elif '.' in symbol and not symbol.endswith('.IS'):
            return 'NASDAQ'
        else:
            return 'XETRA'
    
    def _save_analysis_to_db(self, result: Dict):
        """Analiz sonucunu veritabanına kaydet"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Detaylı analiz verilerini çıkar
            detailed_analysis = result.get('detailed_analysis', {})
            momentum_breakout = detailed_analysis.get('momentum_breakout_analysis', {})
            holding_analysis = detailed_analysis.get('holding_analysis', {})
            
            # Momentum ve Breakout skorları
            momentum_score = 0
            breakout_score = 0
            volume_score = 0
            al_signal = "TUT"
            al_confidence = 50
            
            if momentum_breakout:
                momentum_analysis = momentum_breakout.get('momentum_analysis', {})
                breakout_analysis = momentum_breakout.get('breakout_analysis', {})
                volume_analysis = momentum_breakout.get('volume_analysis', {})
                al_analysis = momentum_breakout.get('al_analysis', {})
                
                momentum_score = (momentum_analysis.get('rsi_momentum', 50) + 
                                momentum_analysis.get('macd_momentum', 50) + 
                                momentum_analysis.get('stoch_momentum', 50)) / 3
                breakout_score = breakout_analysis.get('breakout_score', 50)
                volume_score = volume_analysis.get('volume_score', 50)
                
                if al_analysis:
                    al_signal = al_analysis.get('signal', 'TUT')
                    al_confidence = al_analysis.get('confidence', 50)
            
            # Tutma süresi analizi
            holding_period = 14
            holding_type = "medium_term"
            target_1day = 0
            target_1week = 0
            target_1month = 0
            target_3months = 0
            risk_reward_ratio = 1.0
            volatility = 0
            trend_strength = 50
            
            if holding_analysis:
                recommended_holding = holding_analysis.get('recommended_holding', {})
                target_prices = holding_analysis.get('target_prices', {})
                risk_reward = holding_analysis.get('risk_reward', {})
                volatility_data = holding_analysis.get('volatility', {})
                trend_data = holding_analysis.get('trend_strength', {})
                
                holding_period = recommended_holding.get('period', 14)
                holding_type = recommended_holding.get('period_type', 'medium_term')
                
                if target_prices:
                    target_1day = target_prices.get('1_day', {}).get('target', 0)
                    target_1week = target_prices.get('1_week', {}).get('target', 0)
                    target_1month = target_prices.get('1_month', {}).get('target', 0)
                    target_3months = target_prices.get('3_months', {}).get('target', 0)
                
                risk_reward_ratio = risk_reward.get('average_ratio', 1.0)
                volatility = volatility_data.get('volatility', 0)
                trend_strength = trend_data.get('strength', 50)
            
            cursor.execute('''
                INSERT INTO analizler 
                (tarih, hisse_kodu, finansal_puan, teknik_puan, trend_puan, gann_puan,
                 astroloji_puan, shemitah_puan, cycle21_puan, solar_cycle_puan, economic_cycle_puan,
                 toplam_puan, sinyal, pazar, guncel_fiyat, momentum_skor, breakout_skor, volume_skor,
                 al_sinyal, al_guven, tutma_suresi, tutma_tipi,
                 hedef_fiyat_1gun, hedef_fiyat_1hafta, hedef_fiyat_1ay, hedef_fiyat_3ay,
                 risk_reward_oran, volatilite, trend_guclu)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                result['analysis_date'],
                result['symbol'],
                result['financial_score'],
                result['technical_score'],
                result['trend_score'],
                result['gann_score'],
                detailed_analysis.get('astrology_score', 0),
                detailed_analysis.get('shemitah_score', 0),
                detailed_analysis.get('cycle21_score', 0),
                detailed_analysis.get('solar_cycle_score', 0),
                detailed_analysis.get('economic_cycle_score', 0),
                result['total_score'],
                result['signal'],
                result['market'],
                result['current_price'],
                momentum_score,
                breakout_score,
                volume_score,
                al_signal,
                al_confidence,
                holding_period,
                holding_type,
                target_1day,
                target_1week,
                target_1month,
                target_3months,
                risk_reward_ratio,
                volatility,
                trend_strength
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            log_error(f"Veritabanına kayıt sırasında hata: {e}")
    
    def _generate_summary_report(self, results: List[Dict]):
        """Özet rapor oluştur"""
        if not results:
            return
        
        total_count = len(results)
        al_count = len([r for r in results if r['signal'] == 'AL'])
        tut_count = len([r for r in results if r['signal'] == 'TUT'])
        sat_count = len([r for r in results if r['signal'] == 'SAT'])
        
        avg_score = sum(r['total_score'] for r in results) / total_count
        
        log_success("=== ANALİZ ÖZET RAPORU ===")
        log_info(f"Toplam analiz edilen: {total_count}")
        log_info(f"AL sinyali: {al_count} ({al_count/total_count*100:.1f}%)")
        log_info(f"TUT sinyali: {tut_count} ({tut_count/total_count*100:.1f}%)")
        log_info(f"SAT sinyali: {sat_count} ({sat_count/total_count*100:.1f}%)")
        log_info(f"Ortalama puan: {avg_score:.1f}")
        
        # En iyi 5 performans
        top_5 = results[:5]
        log_info("En iyi 5 performans:")
        for i, result in enumerate(top_5, 1):
            log_info(f"{i}. {result['symbol']} - {result['signal']} ({result['total_score']:.1f} puan)")
    
    def get_analysis_history(self, symbol: str = None, limit: int = 100) -> List[Dict]:
        """Analiz geçmişini getir"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            if symbol:
                cursor.execute('''
                    SELECT * FROM analizler 
                    WHERE hisse_kodu = ? 
                    ORDER BY tarih DESC 
                    LIMIT ?
                ''', (symbol, limit))
            else:
                cursor.execute('''
                    SELECT * FROM analizler 
                    ORDER BY tarih DESC 
                    LIMIT ?
                ''', (limit,))
            
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            conn.close()
            
            results = [dict(zip(columns, row)) for row in rows]
            return results
            
        except Exception as e:
            log_error(f"Analiz geçmişi getirilirken hata: {e}")
            return []
    
    def clear_analysis_history(self):
        """Analiz geçmişini temizle"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM analizler')
            
            conn.commit()
            conn.close()
            
            log_success("Analiz geçmişi temizlendi")
            
        except Exception as e:
            log_error(f"Analiz geçmişi temizlenirken hata: {e}")
            raise
    
    def clear_duplicate_analysis(self):
        """Tekrarlanan varlıkları temizle (her varlık sadece 1 kez kalacak)"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Her varlık için en son analizi tut, diğerlerini sil
            cursor.execute('''
                DELETE FROM analizler 
                WHERE id NOT IN (
                    SELECT MAX(id) 
                    FROM analizler 
                    GROUP BY hisse_kodu
                )
            ''')
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            log_success(f"Tekrarlanan analizler temizlendi: {deleted_count} kayıt silindi")
            
        except Exception as e:
            log_error(f"Tekrar temizleme hatası: {e}")
            raise

