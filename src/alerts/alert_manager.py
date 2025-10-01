"""
PlanB Motoru - Alert Manager
Fiyat ve analiz uyarıları sistemi
"""
import json
import os
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from src.utils.logger import log_info, log_error, log_debug, log_warning

class AlertType(Enum):
    """Uyarı türleri"""
    PRICE_ABOVE = "price_above"
    PRICE_BELOW = "price_below"
    PRICE_CHANGE = "price_change"
    ANALYSIS_SCORE = "analysis_score"
    VOLUME_SPIKE = "volume_spike"
    TECHNICAL_SIGNAL = "technical_signal"
    SENTIMENT_CHANGE = "sentiment_change"

class AlertStatus(Enum):
    """Uyarı durumları"""
    ACTIVE = "active"
    TRIGGERED = "triggered"
    EXPIRED = "expired"
    DISABLED = "disabled"

@dataclass
class Alert:
    """Uyarı sınıfı"""
    id: str
    symbol: str
    alert_type: AlertType
    condition: str  # JSON string olarak koşul
    threshold: float
    message: str
    status: AlertStatus
    created_date: str
    last_checked: str
    triggered_count: int = 0
    last_triggered: str = ""
    expires_at: str = ""
    is_recurring: bool = False
    cooldown_minutes: int = 60  # Tekrar tetiklenme bekleme süresi

@dataclass
class AlertTrigger:
    """Uyarı tetikleme kaydı"""
    id: str
    alert_id: str
    symbol: str
    triggered_at: str
    trigger_value: float
    message: str
    data: Dict[str, Any]

class AlertManager:
    """Uyarı yöneticisi"""
    
    def __init__(self, data_dir: str = "data/alerts"):
        self.data_dir = data_dir
        self.alerts: Dict[str, Alert] = {}
        self.triggered_alerts: List[AlertTrigger] = []
        self.callbacks: List[Callable] = []
        self.running = False
        self.monitor_thread = None
        self._ensure_data_dir()
        self._load_alerts()
    
    def _ensure_data_dir(self):
        """Veri dizinini oluştur"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _load_alerts(self):
        """Uyarıları yükle"""
        try:
            alerts_file = os.path.join(self.data_dir, "alerts.json")
            if os.path.exists(alerts_file):
                with open(alerts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for alert_data in data.get('alerts', []):
                    alert = Alert(
                        id=alert_data['id'],
                        symbol=alert_data['symbol'],
                        alert_type=AlertType(alert_data['alert_type']),
                        condition=alert_data['condition'],
                        threshold=alert_data['threshold'],
                        message=alert_data['message'],
                        status=AlertStatus(alert_data['status']),
                        created_date=alert_data['created_date'],
                        last_checked=alert_data.get('last_checked', ''),
                        triggered_count=alert_data.get('triggered_count', 0),
                        last_triggered=alert_data.get('last_triggered', ''),
                        expires_at=alert_data.get('expires_at', ''),
                        is_recurring=alert_data.get('is_recurring', False),
                        cooldown_minutes=alert_data.get('cooldown_minutes', 60)
                    )
                    self.alerts[alert.id] = alert
                
                log_info(f"{len(self.alerts)} uyarı yüklendi")
            
        except Exception as e:
            log_error(f"Uyarılar yüklenirken hata: {e}")
    
    def _save_alerts(self):
        """Uyarıları kaydet"""
        try:
            alerts_file = os.path.join(self.data_dir, "alerts.json")
            
            data = {
                'alerts': [asdict(alert) for alert in self.alerts.values()],
                'last_updated': datetime.now().isoformat()
            }
            
            with open(alerts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            log_debug("Uyarılar kaydedildi")
            
        except Exception as e:
            log_error(f"Uyarılar kaydedilirken hata: {e}")
    
    def create_alert(self, symbol: str, alert_type: AlertType, threshold: float, 
                    message: str, condition: str = "", expires_at: str = "",
                    is_recurring: bool = False, cooldown_minutes: int = 60) -> str:
        """Yeni uyarı oluştur"""
        try:
            alert_id = f"{symbol}_{alert_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            alert = Alert(
                id=alert_id,
                symbol=symbol,
                alert_type=alert_type,
                condition=condition,
                threshold=threshold,
                message=message,
                status=AlertStatus.ACTIVE,
                created_date=datetime.now().isoformat(),
                last_checked=datetime.now().isoformat(),
                expires_at=expires_at,
                is_recurring=is_recurring,
                cooldown_minutes=cooldown_minutes
            )
            
            self.alerts[alert_id] = alert
            self._save_alerts()
            
            log_info(f"Uyarı oluşturuldu: {symbol} - {alert_type.value} @ {threshold}")
            return alert_id
            
        except Exception as e:
            log_error(f"Uyarı oluşturulurken hata: {e}")
            return ""
    
    def update_alert(self, alert_id: str, **kwargs) -> bool:
        """Uyarıyı güncelle"""
        try:
            if alert_id not in self.alerts:
                return False
            
            alert = self.alerts[alert_id]
            for key, value in kwargs.items():
                if hasattr(alert, key):
                    setattr(alert, key, value)
            
            self._save_alerts()
            log_debug(f"Uyarı güncellendi: {alert_id}")
            return True
            
        except Exception as e:
            log_error(f"Uyarı güncellenirken hata: {e}")
            return False
    
    def delete_alert(self, alert_id: str) -> bool:
        """Uyarıyı sil"""
        try:
            if alert_id in self.alerts:
                del self.alerts[alert_id]
                self._save_alerts()
                log_info(f"Uyarı silindi: {alert_id}")
                return True
            return False
            
        except Exception as e:
            log_error(f"Uyarı silinirken hata: {e}")
            return False
    
    def get_alerts(self, symbol: str = None, status: AlertStatus = None) -> List[Alert]:
        """Uyarıları getir"""
        alerts = list(self.alerts.values())
        
        if symbol:
            alerts = [alert for alert in alerts if alert.symbol == symbol]
        
        if status:
            alerts = [alert for alert in alerts if alert.status == status]
        
        return alerts
    
    def add_callback(self, callback: Callable):
        """Uyarı tetiklendiğinde çağrılacak fonksiyon ekle"""
        self.callbacks.append(callback)
    
    def _trigger_alert(self, alert: Alert, trigger_value: float, data: Dict[str, Any] = None):
        """Uyarıyı tetikle"""
        try:
            # Cooldown kontrolü
            if alert.last_triggered:
                last_triggered = datetime.fromisoformat(alert.last_triggered)
                cooldown_end = last_triggered + timedelta(minutes=alert.cooldown_minutes)
                if datetime.now() < cooldown_end:
                    return  # Cooldown süresi henüz bitmemiş
            
            # Tetikleme kaydı oluştur
            trigger_id = f"{alert.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            trigger = AlertTrigger(
                id=trigger_id,
                alert_id=alert.id,
                symbol=alert.symbol,
                triggered_at=datetime.now().isoformat(),
                trigger_value=trigger_value,
                message=alert.message,
                data=data or {}
            )
            
            self.triggered_alerts.append(trigger)
            
            # Alert istatistiklerini güncelle
            alert.triggered_count += 1
            alert.last_triggered = datetime.now().isoformat()
            
            # Recurring değilse uyarıyı devre dışı bırak
            if not alert.is_recurring:
                alert.status = AlertStatus.TRIGGERED
            
            self._save_alerts()
            
            # Callback'leri çağır
            for callback in self.callbacks:
                try:
                    callback(trigger)
                except Exception as e:
                    log_error(f"Alert callback hatası: {e}")
            
            log_warning(f"🚨 UYARI TETİKLENDİ: {alert.symbol} - {alert.message}")
            
        except Exception as e:
            log_error(f"Uyarı tetiklenirken hata: {e}")
    
    def check_price_alert(self, symbol: str, current_price: float, price_data: Dict[str, Any] = None):
        """Fiyat uyarılarını kontrol et"""
        try:
            active_alerts = self.get_alerts(symbol, AlertStatus.ACTIVE)
            
            for alert in active_alerts:
                if alert.alert_type not in [AlertType.PRICE_ABOVE, AlertType.PRICE_BELOW, AlertType.PRICE_CHANGE]:
                    continue
                
                # Süre kontrolü
                if alert.expires_at:
                    expires_at = datetime.fromisoformat(alert.expires_at)
                    if datetime.now() > expires_at:
                        alert.status = AlertStatus.EXPIRED
                        continue
                
                # Koşul kontrolü
                should_trigger = False
                
                if alert.alert_type == AlertType.PRICE_ABOVE and current_price >= alert.threshold:
                    should_trigger = True
                elif alert.alert_type == AlertType.PRICE_BELOW and current_price <= alert.threshold:
                    should_trigger = True
                elif alert.alert_type == AlertType.PRICE_CHANGE:
                    # Fiyat değişim yüzdesi kontrolü
                    if price_data and 'previous_price' in price_data:
                        change_percent = ((current_price - price_data['previous_price']) / price_data['previous_price']) * 100
                        if abs(change_percent) >= alert.threshold:
                            should_trigger = True
                
                if should_trigger:
                    self._trigger_alert(alert, current_price, price_data)
                
                # Son kontrol zamanını güncelle
                alert.last_checked = datetime.now().isoformat()
            
        except Exception as e:
            log_error(f"Fiyat uyarıları kontrol edilirken hata: {e}")
    
    def check_analysis_alert(self, symbol: str, analysis_data: Dict[str, Any]):
        """Analiz uyarılarını kontrol et"""
        try:
            active_alerts = self.get_alerts(symbol, AlertStatus.ACTIVE)
            
            for alert in active_alerts:
                if alert.alert_type not in [AlertType.ANALYSIS_SCORE, AlertType.SENTIMENT_CHANGE]:
                    continue
                
                # Süre kontrolü
                if alert.expires_at:
                    expires_at = datetime.fromisoformat(alert.expires_at)
                    if datetime.now() > expires_at:
                        alert.status = AlertStatus.EXPIRED
                        continue
                
                # Koşul kontrolü
                should_trigger = False
                
                if alert.alert_type == AlertType.ANALYSIS_SCORE:
                    total_score = analysis_data.get('total_score', 0)
                    if total_score >= alert.threshold:
                        should_trigger = True
                elif alert.alert_type == AlertType.SENTIMENT_CHANGE:
                    sentiment_score = analysis_data.get('sentiment_score', 50)
                    if abs(sentiment_score - 50) >= alert.threshold:
                        should_trigger = True
                
                if should_trigger:
                    self._trigger_alert(alert, analysis_data.get('total_score', 0), analysis_data)
                
                # Son kontrol zamanını güncelle
                alert.last_checked = datetime.now().isoformat()
            
        except Exception as e:
            log_error(f"Analiz uyarıları kontrol edilirken hata: {e}")
    
    def start_monitoring(self, check_interval: int = 60):
        """Uyarı izlemeyi başlat"""
        if self.running:
            return
        
        self.running = True
        
        def monitor_loop():
            while self.running:
                try:
                    # Süresi dolmuş uyarıları kontrol et
                    now = datetime.now()
                    for alert in self.alerts.values():
                        if alert.expires_at:
                            expires_at = datetime.fromisoformat(alert.expires_at)
                            if now > expires_at and alert.status == AlertStatus.ACTIVE:
                                alert.status = AlertStatus.EXPIRED
                    
                    self._save_alerts()
                    
                    # Bekle
                    time.sleep(check_interval)
                    
                except Exception as e:
                    log_error(f"Uyarı izleme hatası: {e}")
                    time.sleep(check_interval)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        log_info("Uyarı izleme başlatıldı")
    
    def stop_monitoring(self):
        """Uyarı izlemeyi durdur"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        log_info("Uyarı izleme durduruldu")
    
    def get_triggered_alerts(self, limit: int = 50) -> List[AlertTrigger]:
        """Tetiklenen uyarıları getir"""
        return sorted(self.triggered_alerts, key=lambda x: x.triggered_at, reverse=True)[:limit]
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Uyarı istatistiklerini getir"""
        try:
            total_alerts = len(self.alerts)
            active_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.ACTIVE])
            triggered_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.TRIGGERED])
            expired_alerts = len([a for a in self.alerts.values() if a.status == AlertStatus.EXPIRED])
            
            # En çok tetiklenen uyarılar
            most_triggered = sorted(self.alerts.values(), key=lambda x: x.triggered_count, reverse=True)[:5]
            
            return {
                'total_alerts': total_alerts,
                'active_alerts': active_alerts,
                'triggered_alerts': triggered_alerts,
                'expired_alerts': expired_alerts,
                'most_triggered': [
                    {
                        'symbol': alert.symbol,
                        'type': alert.alert_type.value,
                        'triggered_count': alert.triggered_count
                    }
                    for alert in most_triggered
                ],
                'total_triggers': len(self.triggered_alerts)
            }
            
        except Exception as e:
            log_error(f"Uyarı istatistikleri alınırken hata: {e}")
            return {}

# Global alert manager instance
alert_manager = AlertManager()

