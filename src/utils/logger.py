"""
PlanB Motoru - Loglama Sistemi
"""
import sys
from pathlib import Path
from loguru import logger
from config.settings import config

class PlanBLogger:
    """PlanB Motoru için özelleştirilmiş logger sınıfı"""
    
    def __init__(self):
        self._setup_logger()
    
    def _setup_logger(self):
        """Logger'ı yapılandır"""
        # Mevcut handler'ları temizle
        logger.remove()
        
        # Konsol çıktısı
        logger.add(
            sys.stdout,
            format=config.LOG_FORMAT,
            level=config.LOG_LEVEL,
            colorize=True,
            backtrace=True,
            diagnose=True
        )
        
        # Dosya çıktısı
        log_file = config.LOGS_DIR / "planb_motoru.log"
        logger.add(
            log_file,
            format=config.LOG_FORMAT,
            level=config.LOG_LEVEL,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            backtrace=True,
            diagnose=True
        )
        
        # Hata logları için ayrı dosya
        error_log_file = config.LOGS_DIR / "errors.log"
        logger.add(
            error_log_file,
            format=config.LOG_FORMAT,
            level="ERROR",
            rotation="5 MB",
            retention="30 days",
            compression="zip",
            backtrace=True,
            diagnose=True
        )
    
    def get_logger(self):
        """Logger instance'ını döndür"""
        return logger

# Global logger instance
planb_logger = PlanBLogger()
log = planb_logger.get_logger()

# Kolay kullanım için fonksiyonlar
def log_info(message: str, **kwargs):
    """Bilgi mesajı logla"""
    log.info(message, **kwargs)

def log_warning(message: str, **kwargs):
    """Uyarı mesajı logla"""
    log.warning(message, **kwargs)

def log_error(message: str, **kwargs):
    """Hata mesajı logla"""
    log.error(message, **kwargs)

def log_debug(message: str, **kwargs):
    """Debug mesajı logla"""
    log.debug(message, **kwargs)

def log_success(message: str, **kwargs):
    """Başarı mesajı logla"""
    log.success(message, **kwargs)

