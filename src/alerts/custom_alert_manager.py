"""
PlanB Motoru - Custom Alert Manager
Kişiselleştirilmiş uyarılar yönetimi
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug

class CustomAlertManager:
    """Kişiselleştirilmiş uyarı yöneticisi"""
    
    def __init__(self):
        self.alerts_file = "data/alerts/custom_alerts.json"
        self.alert_history_file = "data/alerts/alert_history.json"
        self._ensure_alert_directory()
        self._load_alerts()
        self._load_alert_history()
    
    def _ensure_alert_directory(self):
        """Uyarı dizinini oluştur"""
        os.makedirs("data/alerts", exist_ok=True)
    
    def _load_alerts(self):
        """Uyarıları yükle"""
        try:
            if os.path.exists(self.alerts_file):
                with open(self.alerts_file, 'r', encoding='utf-8') as f:
                    self.alerts = json.load(f)
            else:
                self.alerts = {}
            log_info(f"{len(self.alerts)} özel uyarı yüklendi")
        except Exception as e:
            log_error(f"Uyarı yükleme hatası: {e}")
            self.alerts = {}
    
    def _load_alert_history(self):
        """Uyarı geçmişini yükle"""
        try:
            if os.path.exists(self.alert_history_file):
                with open(self.alert_history_file, 'r', encoding='utf-8') as f:
                    self.alert_history = json.load(f)
            else:
                self.alert_history = []
            log_info(f"{len(self.alert_history)} uyarı geçmişi yüklendi")
        except Exception as e:
            log_error(f"Uyarı geçmişi yükleme hatası: {e}")
            self.alert_history = []
    
    def create_alert(self, alert_data: Dict[str, Any]) -> str:
        """Yeni uyarı oluştur"""
        try:
            # Uyarı ID oluştur
            alert_id = self._generate_alert_id()
            
            # Uyarı türünü doğrula
            alert_type = alert_data.get('type', 'price')
            if alert_type not in ['price', 'analysis', 'sentiment', 'volume', 'technical', 'custom']:
                log_error(f"Geçersiz uyarı türü: {alert_type}")
                return ""
            
            # Yeni uyarı
            new_alert = {
                'alert_id': alert_id,
                'name': alert_data.get('name', f'Uyarı {alert_id}'),
                'description': alert_data.get('description', ''),
                'type': alert_type,
                'symbol': alert_data.get('symbol', ''),
                'market': alert_data.get('market', 'bist'),
                'conditions': alert_data.get('conditions', {}),
                'thresholds': alert_data.get('thresholds', {}),
                'is_active': alert_data.get('is_active', True),
                'is_recurring': alert_data.get('is_recurring', False),
                'cooldown_minutes': alert_data.get('cooldown_minutes', 60),
                'notification_methods': alert_data.get('notification_methods', ['dashboard']),
                'priority': alert_data.get('priority', 'medium'),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'last_triggered': None,
                'trigger_count': 0,
                'user_id': alert_data.get('user_id', 'default_user')
            }
            
            self.alerts[alert_id] = new_alert
            self._save_alerts()
            
            log_info(f"Yeni uyarı oluşturuldu: {alert_id}")
            return alert_id
            
        except Exception as e:
            log_error(f"Uyarı oluşturma hatası: {e}")
            return ""
    
    def get_alert(self, alert_id: str) -> Optional[Dict[str, Any]]:
        """Uyarı getir"""
        try:
            return self.alerts.get(alert_id)
        except Exception as e:
            log_error(f"Uyarı alma hatası: {e}")
            return None
    
    def get_all_alerts(self, user_id: str = None, alert_type: str = None, is_active: bool = None) -> List[Dict[str, Any]]:
        """Tüm uyarıları getir"""
        try:
            alerts_list = []
            
            for alert_id, alert_data in self.alerts.items():
                # Filtreler
                if user_id and alert_data.get('user_id') != user_id:
                    continue
                
                if alert_type and alert_data.get('type') != alert_type:
                    continue
                
                if is_active is not None and alert_data.get('is_active') != is_active:
                    continue
                
                alerts_list.append(alert_data)
            
            return alerts_list
            
        except Exception as e:
            log_error(f"Uyarı listesi alma hatası: {e}")
            return []
    
    def update_alert(self, alert_id: str, update_data: Dict[str, Any]) -> bool:
        """Uyarıyı güncelle"""
        try:
            if alert_id not in self.alerts:
                log_error(f"Uyarı bulunamadı: {alert_id}")
                return False
            
            # Güncellenebilir alanlar
            allowed_fields = [
                'name', 'description', 'conditions', 'thresholds', 'is_active',
                'is_recurring', 'cooldown_minutes', 'notification_methods', 'priority'
            ]
            
            for field, value in update_data.items():
                if field in allowed_fields:
                    self.alerts[alert_id][field] = value
            
            self.alerts[alert_id]['updated_at'] = datetime.now().isoformat()
            self._save_alerts()
            
            log_info(f"Uyarı güncellendi: {alert_id}")
            return True
            
        except Exception as e:
            log_error(f"Uyarı güncelleme hatası: {e}")
            return False
    
    def delete_alert(self, alert_id: str) -> bool:
        """Uyarıyı sil"""
        try:
            if alert_id not in self.alerts:
                log_error(f"Uyarı bulunamadı: {alert_id}")
                return False
            
            # Uyarıyı sil
            del self.alerts[alert_id]
            self._save_alerts()
            
            log_info(f"Uyarı silindi: {alert_id}")
            return True
            
        except Exception as e:
            log_error(f"Uyarı silme hatası: {e}")
            return False
    
    def check_price_alerts(self, symbol: str, current_price: float, market: str = 'bist') -> List[Dict[str, Any]]:
        """Fiyat uyarılarını kontrol et"""
        try:
            triggered_alerts = []
            
            for alert_id, alert_data in self.alerts.items():
                if not alert_data.get('is_active', True):
                    continue
                
                if alert_data.get('type') != 'price':
                    continue
                
                if alert_data.get('symbol') != symbol or alert_data.get('market') != market:
                    continue
                
                # Cooldown kontrolü
                if self._is_in_cooldown(alert_data):
                    continue
                
                # Fiyat koşullarını kontrol et
                if self._check_price_conditions(alert_data, current_price):
                    # Uyarıyı tetikle
                    self._trigger_alert(alert_id, {
                        'symbol': symbol,
                        'current_price': current_price,
                        'market': market,
                        'trigger_type': 'price'
                    })
                    triggered_alerts.append(alert_data)
            
            return triggered_alerts
            
        except Exception as e:
            log_error(f"Fiyat uyarı kontrolü hatası: {e}")
            return []
    
    def check_analysis_alerts(self, symbol: str, analysis_data: Dict[str, Any], market: str = 'bist') -> List[Dict[str, Any]]:
        """Analiz uyarılarını kontrol et"""
        try:
            triggered_alerts = []
            
            for alert_id, alert_data in self.alerts.items():
                if not alert_data.get('is_active', True):
                    continue
                
                if alert_data.get('type') != 'analysis':
                    continue
                
                if alert_data.get('symbol') != symbol or alert_data.get('market') != market:
                    continue
                
                # Cooldown kontrolü
                if self._is_in_cooldown(alert_data):
                    continue
                
                # Analiz koşullarını kontrol et
                if self._check_analysis_conditions(alert_data, analysis_data):
                    # Uyarıyı tetikle
                    self._trigger_alert(alert_id, {
                        'symbol': symbol,
                        'analysis_data': analysis_data,
                        'market': market,
                        'trigger_type': 'analysis'
                    })
                    triggered_alerts.append(alert_data)
            
            return triggered_alerts
            
        except Exception as e:
            log_error(f"Analiz uyarı kontrolü hatası: {e}")
            return []
    
    def check_sentiment_alerts(self, symbol: str, sentiment_data: Dict[str, Any], market: str = 'bist') -> List[Dict[str, Any]]:
        """Sentiment uyarılarını kontrol et"""
        try:
            triggered_alerts = []
            
            for alert_id, alert_data in self.alerts.items():
                if not alert_data.get('is_active', True):
                    continue
                
                if alert_data.get('type') != 'sentiment':
                    continue
                
                if alert_data.get('symbol') != symbol or alert_data.get('market') != market:
                    continue
                
                # Cooldown kontrolü
                if self._is_in_cooldown(alert_data):
                    continue
                
                # Sentiment koşullarını kontrol et
                if self._check_sentiment_conditions(alert_data, sentiment_data):
                    # Uyarıyı tetikle
                    self._trigger_alert(alert_id, {
                        'symbol': symbol,
                        'sentiment_data': sentiment_data,
                        'market': market,
                        'trigger_type': 'sentiment'
                    })
                    triggered_alerts.append(alert_data)
            
            return triggered_alerts
            
        except Exception as e:
            log_error(f"Sentiment uyarı kontrolü hatası: {e}")
            return []
    
    def check_volume_alerts(self, symbol: str, volume_data: Dict[str, Any], market: str = 'bist') -> List[Dict[str, Any]]:
        """Hacim uyarılarını kontrol et"""
        try:
            triggered_alerts = []
            
            for alert_id, alert_data in self.alerts.items():
                if not alert_data.get('is_active', True):
                    continue
                
                if alert_data.get('type') != 'volume':
                    continue
                
                if alert_data.get('symbol') != symbol or alert_data.get('market') != market:
                    continue
                
                # Cooldown kontrolü
                if self._is_in_cooldown(alert_data):
                    continue
                
                # Hacim koşullarını kontrol et
                if self._check_volume_conditions(alert_data, volume_data):
                    # Uyarıyı tetikle
                    self._trigger_alert(alert_id, {
                        'symbol': symbol,
                        'volume_data': volume_data,
                        'market': market,
                        'trigger_type': 'volume'
                    })
                    triggered_alerts.append(alert_data)
            
            return triggered_alerts
            
        except Exception as e:
            log_error(f"Hacim uyarı kontrolü hatası: {e}")
            return []
    
    def check_technical_alerts(self, symbol: str, technical_data: Dict[str, Any], market: str = 'bist') -> List[Dict[str, Any]]:
        """Teknik analiz uyarılarını kontrol et"""
        try:
            triggered_alerts = []
            
            for alert_id, alert_data in self.alerts.items():
                if not alert_data.get('is_active', True):
                    continue
                
                if alert_data.get('type') != 'technical':
                    continue
                
                if alert_data.get('symbol') != symbol or alert_data.get('market') != market:
                    continue
                
                # Cooldown kontrolü
                if self._is_in_cooldown(alert_data):
                    continue
                
                # Teknik analiz koşullarını kontrol et
                if self._check_technical_conditions(alert_data, technical_data):
                    # Uyarıyı tetikle
                    self._trigger_alert(alert_id, {
                        'symbol': symbol,
                        'technical_data': technical_data,
                        'market': market,
                        'trigger_type': 'technical'
                    })
                    triggered_alerts.append(alert_data)
            
            return triggered_alerts
            
        except Exception as e:
            log_error(f"Teknik analiz uyarı kontrolü hatası: {e}")
            return []
    
    def _check_price_conditions(self, alert_data: Dict[str, Any], current_price: float) -> bool:
        """Fiyat koşullarını kontrol et"""
        try:
            conditions = alert_data.get('conditions', {})
            thresholds = alert_data.get('thresholds', {})
            
            # Fiyat koşulları
            if 'price_above' in conditions:
                if current_price <= conditions['price_above']:
                    return False
            
            if 'price_below' in conditions:
                if current_price >= conditions['price_below']:
                    return False
            
            # Yüzde değişim koşulları
            if 'change_above' in conditions:
                # Bu durumda önceki fiyat gerekli
                pass
            
            if 'change_below' in conditions:
                # Bu durumda önceki fiyat gerekli
                pass
            
            return True
            
        except Exception as e:
            log_error(f"Fiyat koşul kontrolü hatası: {e}")
            return False
    
    def _check_analysis_conditions(self, alert_data: Dict[str, Any], analysis_data: Dict[str, Any]) -> bool:
        """Analiz koşullarını kontrol et"""
        try:
            conditions = alert_data.get('conditions', {})
            
            # Toplam skor koşulları
            total_score = analysis_data.get('total_score', 0)
            
            if 'score_above' in conditions:
                if total_score <= conditions['score_above']:
                    return False
            
            if 'score_below' in conditions:
                if total_score >= conditions['score_below']:
                    return False
            
            # Sinyal koşulları
            signal = analysis_data.get('signal', 'HOLD')
            
            if 'signal' in conditions:
                if signal != conditions['signal']:
                    return False
            
            # Güven koşulları
            confidence = analysis_data.get('confidence', 0)
            
            if 'confidence_above' in conditions:
                if confidence <= conditions['confidence_above']:
                    return False
            
            return True
            
        except Exception as e:
            log_error(f"Analiz koşul kontrolü hatası: {e}")
            return False
    
    def _check_sentiment_conditions(self, alert_data: Dict[str, Any], sentiment_data: Dict[str, Any]) -> bool:
        """Sentiment koşullarını kontrol et"""
        try:
            conditions = alert_data.get('conditions', {})
            
            # Sentiment skor koşulları
            sentiment_score = sentiment_data.get('overall_score', 50)
            
            if 'sentiment_above' in conditions:
                if sentiment_score <= conditions['sentiment_above']:
                    return False
            
            if 'sentiment_below' in conditions:
                if sentiment_score >= conditions['sentiment_below']:
                    return False
            
            # Sentiment yön koşulları
            sentiment = sentiment_data.get('sentiment', 'neutral')
            
            if 'sentiment_type' in conditions:
                if sentiment != conditions['sentiment_type']:
                    return False
            
            return True
            
        except Exception as e:
            log_error(f"Sentiment koşul kontrolü hatası: {e}")
            return False
    
    def _check_volume_conditions(self, alert_data: Dict[str, Any], volume_data: Dict[str, Any]) -> bool:
        """Hacim koşullarını kontrol et"""
        try:
            conditions = alert_data.get('conditions', {})
            
            # Hacim koşulları
            current_volume = volume_data.get('current_volume', 0)
            average_volume = volume_data.get('average_volume', 0)
            
            if 'volume_above' in conditions:
                if current_volume <= conditions['volume_above']:
                    return False
            
            if 'volume_ratio_above' in conditions:
                if average_volume > 0:
                    volume_ratio = current_volume / average_volume
                    if volume_ratio <= conditions['volume_ratio_above']:
                        return False
            
            return True
            
        except Exception as e:
            log_error(f"Hacim koşul kontrolü hatası: {e}")
            return False
    
    def _check_technical_conditions(self, alert_data: Dict[str, Any], technical_data: Dict[str, Any]) -> bool:
        """Teknik analiz koşullarını kontrol et"""
        try:
            conditions = alert_data.get('conditions', {})
            
            # RSI koşulları
            rsi = technical_data.get('rsi', {})
            rsi_value = rsi.get('value', 50)
            
            if 'rsi_above' in conditions:
                if rsi_value <= conditions['rsi_above']:
                    return False
            
            if 'rsi_below' in conditions:
                if rsi_value >= conditions['rsi_below']:
                    return False
            
            # MACD koşulları
            macd = technical_data.get('macd', {})
            macd_signal = macd.get('signal', 'neutral')
            
            if 'macd_signal' in conditions:
                if macd_signal != conditions['macd_signal']:
                    return False
            
            # SMA koşulları
            sma_signals = technical_data.get('sma_signals', {})
            price_vs_sma20 = sma_signals.get('price_vs_sma20', 'neutral')
            
            if 'price_vs_sma20' in conditions:
                if price_vs_sma20 != conditions['price_vs_sma20']:
                    return False
            
            return True
            
        except Exception as e:
            log_error(f"Teknik analiz koşul kontrolü hatası: {e}")
            return False
    
    def _is_in_cooldown(self, alert_data: Dict[str, Any]) -> bool:
        """Uyarı cooldown'da mı kontrol et"""
        try:
            last_triggered = alert_data.get('last_triggered')
            if not last_triggered:
                return False
            
            cooldown_minutes = alert_data.get('cooldown_minutes', 60)
            last_triggered_time = datetime.fromisoformat(last_triggered)
            cooldown_end = last_triggered_time + timedelta(minutes=cooldown_minutes)
            
            return datetime.now() < cooldown_end
            
        except Exception as e:
            log_error(f"Cooldown kontrolü hatası: {e}")
            return False
    
    def _trigger_alert(self, alert_id: str, trigger_data: Dict[str, Any]):
        """Uyarıyı tetikle"""
        try:
            alert_data = self.alerts[alert_id]
            
            # Uyarı bilgilerini güncelle
            alert_data['last_triggered'] = datetime.now().isoformat()
            alert_data['trigger_count'] = alert_data.get('trigger_count', 0) + 1
            
            # Uyarı geçmişine ekle
            alert_history_entry = {
                'alert_id': alert_id,
                'alert_name': alert_data['name'],
                'triggered_at': datetime.now().isoformat(),
                'trigger_data': trigger_data,
                'notification_methods': alert_data.get('notification_methods', []),
                'priority': alert_data.get('priority', 'medium')
            }
            
            self.alert_history.append(alert_history_entry)
            
            # Dosyaları kaydet
            self._save_alerts()
            self._save_alert_history()
            
            log_info(f"Uyarı tetiklendi: {alert_id}")
            
        except Exception as e:
            log_error(f"Uyarı tetikleme hatası: {e}")
    
    def get_alert_history(self, alert_id: str = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Uyarı geçmişini getir"""
        try:
            if alert_id:
                # Belirli uyarı için geçmiş
                history = [entry for entry in self.alert_history if entry['alert_id'] == alert_id]
            else:
                # Tüm geçmiş
                history = self.alert_history
            
            # Son N kaydı döndür
            return history[-limit:] if history else []
            
        except Exception as e:
            log_error(f"Uyarı geçmişi alma hatası: {e}")
            return []
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Uyarı istatistikleri"""
        try:
            total_alerts = len(self.alerts)
            active_alerts = len([a for a in self.alerts.values() if a.get('is_active', True)])
            inactive_alerts = total_alerts - active_alerts
            
            # Uyarı türü dağılımı
            type_distribution = {}
            for alert in self.alerts.values():
                alert_type = alert.get('type', 'unknown')
                type_distribution[alert_type] = type_distribution.get(alert_type, 0) + 1
            
            # Toplam tetiklenme sayısı
            total_triggers = sum(alert.get('trigger_count', 0) for alert in self.alerts.values())
            
            # Son 24 saatte tetiklenen uyarılar
            last_24h = datetime.now() - timedelta(hours=24)
            recent_triggers = len([
                entry for entry in self.alert_history
                if datetime.fromisoformat(entry['triggered_at']) > last_24h
            ])
            
            return {
                'total_alerts': total_alerts,
                'active_alerts': active_alerts,
                'inactive_alerts': inactive_alerts,
                'type_distribution': type_distribution,
                'total_triggers': total_triggers,
                'recent_triggers_24h': recent_triggers,
                'total_history_entries': len(self.alert_history)
            }
            
        except Exception as e:
            log_error(f"Uyarı istatistikleri alma hatası: {e}")
            return {}
    
    def _generate_alert_id(self) -> str:
        """Uyarı ID oluştur"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        import secrets
        random_part = secrets.token_hex(4)
        return f"alert_{timestamp}_{random_part}"
    
    def _save_alerts(self):
        """Uyarıları kaydet"""
        try:
            with open(self.alerts_file, 'w', encoding='utf-8') as f:
                json.dump(self.alerts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Uyarı kaydetme hatası: {e}")
    
    def _save_alert_history(self):
        """Uyarı geçmişini kaydet"""
        try:
            with open(self.alert_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.alert_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Uyarı geçmişi kaydetme hatası: {e}")

# Global custom alert manager instance
custom_alert_manager = CustomAlertManager()

