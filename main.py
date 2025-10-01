"""
PlanB Motoru - Ana Çalıştırıcı
Hephaistos & Hermes Entegrasyonlu Finansal Analiz Sistemi
"""
import sys
import argparse
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import config
from src.utils.logger import log_info, log_error, log_success, log_warning
from src.core.analysis_engine import PlanBAnalysisEngine
from src.dashboard.simple_dashboard import run_dashboard as run_simple_dashboard

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(
        description="PlanB Motoru - Finansal Analiz ve Dashboard Sistemi",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python main.py dashboard          # Dashboard'u başlat
  python main.py analyze            # Tam analiz çalıştır
  python main.py analyze --test     # Test modunda analiz
  python main.py analyze --symbol AAPL  # Tek sembol analizi
        """
    )
    
    parser.add_argument(
        'command',
        choices=['dashboard', 'analyze', 'test'],
        help='Çalıştırılacak komut'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test modunda çalıştır (sınırlı sembol listesi)'
    )
    
    parser.add_argument(
        '--symbol',
        type=str,
        help='Analiz edilecek belirli sembol (örn: AAPL, ASELS.IS)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        help='Dashboard port numarası'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Dashboard host adresi'
    )
    
    args = parser.parse_args()
    
    try:
        log_success("🚀 PlanB Motoru Başlatılıyor...")
        log_info(f"Komut: {args.command}")
        
        if args.command == 'dashboard':
            run_dashboard(args)
        elif args.command == 'analyze':
            run_analysis(args)
        elif args.command == 'test':
            run_test(args)
            
    except KeyboardInterrupt:
        log_info("Kullanıcı tarafından durduruldu")
    except Exception as e:
        log_error(f"Ana program hatası: {e}")
        sys.exit(1)

def run_dashboard(args):
    """Dashboard'u çalıştır"""
    try:
        log_info("📊 Dashboard başlatılıyor...")
        
        # Yeni basit dashboard'u çalıştır
        run_simple_dashboard(
            host=args.host,
            port=args.port or 5004,
            debug=config.DEBUG
        )
        
    except Exception as e:
        log_error(f"Dashboard başlatılırken hata: {e}")
        raise

def run_analysis(args):
    """Analiz çalıştır"""
    try:
        log_info("🔍 Analiz başlatılıyor...")
        
        engine = PlanBAnalysisEngine()
        
        if args.symbol:
            # Tek sembol analizi
            log_info(f"Tek sembol analizi: {args.symbol}")
            result = engine.analyze_single_symbol(args.symbol)
            
            if result:
                log_success(f"Analiz tamamlandı:")
                log_info(f"  Sembol: {result['symbol']}")
                log_info(f"  Sinyal: {result['signal']}")
                log_info(f"  Puan: {result['total_score']:.1f}")
                log_info(f"  Pazar: {result['market']}")
                log_info(f"  Trend: {result['trend']}")
            else:
                log_error(f"{args.symbol} analiz edilemedi")
        else:
            # Tam analiz
            test_mode = args.test or config.TEST_MODE
            log_info(f"Tam analiz başlatılıyor (Test modu: {test_mode})")
            
            results = engine.run_full_analysis(test_mode)
            
            if results:
                log_success(f"Analiz tamamlandı: {len(results)} sembol analiz edildi")
                
                # En iyi 10 sonucu göster
                top_10 = results[:10]
                log_info("En iyi 10 performans:")
                for i, result in enumerate(top_10, 1):
                    log_info(f"  {i:2d}. {result['symbol']:10s} - {result['signal']:4s} ({result['total_score']:5.1f} puan)")
            else:
                log_warning("Analiz sonucu bulunamadı")
        
    except Exception as e:
        log_error(f"Analiz çalıştırılırken hata: {e}")
        raise

def run_test(args):
    """Test modunu çalıştır"""
    try:
        log_info("🧪 Test modu başlatılıyor...")
        
        # Test sembolleri
        test_symbols = config.TEST_SYMBOLS
        log_info(f"Test sembolleri: {', '.join(test_symbols)}")
        
        engine = PlanBAnalysisEngine()
        results = engine.analyze_multiple_symbols(test_symbols)
        
        if results:
            log_success(f"Test tamamlandı: {len(results)} sembol analiz edildi")
            
            for result in results:
                log_info(f"  {result['symbol']:10s} - {result['signal']:4s} ({result['total_score']:5.1f} puan)")
        else:
            log_warning("Test sonucu bulunamadı")
        
    except Exception as e:
        log_error(f"Test çalıştırılırken hata: {e}")
        raise

def check_dependencies():
    """Bağımlılıkları kontrol et"""
    try:
        import yfinance
        import pandas
        try:
            import pandas_ta
        except ImportError:
            pass
        import flask
        import requests
        log_success("Temel bağımlılıklar yüklü")
        return True
    except ImportError as e:
        log_error(f"Eksik bağımlılık: {e}")
        log_info("Lütfen 'pip install -r requirements.txt' komutunu çalıştırın")
        return False

if __name__ == "__main__":
    # Bağımlılıkları kontrol et
    if not check_dependencies():
        sys.exit(1)
    
    # Ana programı çalıştır
    main()