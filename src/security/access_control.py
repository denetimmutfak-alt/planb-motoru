"""
PlanB Motoru - Access Control
Kişisel kullanım için erişim kontrolü ve kimlik doğrulama
"""
import os
import json
import hashlib
import secrets
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from src.security.encryption_manager import encryption_manager
from src.utils.logger import log_info, log_error, log_debug

class AccessControl:
    """Kişisel erişim kontrolü"""
    
    def __init__(self):
        self.user_sessions = {}
        self.failed_attempts = {}
        self.max_failed_attempts = 5
        self.session_timeout = 24 * 60 * 60  # 24 saat
        self.personal_device_id = self._get_personal_device_id()
        self.authorized_devices = self._load_authorized_devices()
        
    def _get_personal_device_id(self) -> str:
        """Kişisel cihaz ID'si oluştur"""
        try:
            # Kişisel kullanım için sabit device ID
            personal_info = "PlanB_Motoru_Personal_Device_2024"
            device_hash = hashlib.sha256(personal_info.encode()).hexdigest()[:16]
            return device_hash
            
        except Exception as e:
            log_error(f"Device ID oluşturma hatası: {e}")
            return "default_device"
    
    def _load_authorized_devices(self) -> List[str]:
        """Yetkili cihazları yükle"""
        try:
            # Kişisel kullanım için sadece bu cihaz
            return [self.personal_device_id]
            
        except Exception as e:
            log_error(f"Yetkili cihazlar yükleme hatası: {e}")
            return [self.personal_device_id]
    
    def verify_device_access(self, device_id: str = None) -> bool:
        """Cihaz erişimini doğrula"""
        try:
            if device_id is None:
                device_id = self.personal_device_id
            
            # Kişisel cihaz kontrolü
            if device_id in self.authorized_devices:
                log_info(f"Yetkili cihaz erişimi: {device_id}")
                return True
            else:
                log_error(f"Yetkisiz cihaz erişim denemesi: {device_id}")
                return False
                
        except Exception as e:
            log_error(f"Cihaz doğrulama hatası: {e}")
            return False
    
    def create_personal_session(self, user_credentials: Dict[str, str]) -> Optional[str]:
        """Kişisel oturum oluştur"""
        try:
            # Kişisel kullanım için basit kimlik doğrulama
            expected_username = "PlanB_User"
            expected_password = "Personal_Access_2024"
            
            username = user_credentials.get('username', '')
            password = user_credentials.get('password', '')
            
            # Kimlik doğrulama
            if username == expected_username and password == expected_password:
                # Oturum token'ı oluştur
                session_token = secrets.token_urlsafe(32)
                
                # Oturum bilgilerini kaydet
                session_data = {
                    'user_id': 'personal_user',
                    'username': username,
                    'device_id': self.personal_device_id,
                    'created_at': datetime.now().isoformat(),
                    'expires_at': (datetime.now() + timedelta(seconds=self.session_timeout)).isoformat(),
                    'last_activity': datetime.now().isoformat(),
                    'ip_address': '127.0.0.1',  # Local access
                    'user_agent': 'PlanB_Motoru_Personal'
                }
                
                self.user_sessions[session_token] = session_data
                
                # Şifrelenmiş oturum verilerini kaydet
                encryption_manager.encrypt_data(session_data, f"session_{session_token}")
                
                log_info("Kişisel oturum oluşturuldu")
                return session_token
            else:
                log_error("Geçersiz kimlik bilgileri")
                return None
                
        except Exception as e:
            log_error(f"Oturum oluşturma hatası: {e}")
            return None
    
    def verify_session(self, session_token: str) -> bool:
        """Oturum doğrulama"""
        try:
            if not session_token:
                return False
            
            # Oturum verilerini kontrol et
            if session_token in self.user_sessions:
                session_data = self.user_sessions[session_token]
                
                # Süre kontrolü
                expires_at = datetime.fromisoformat(session_data['expires_at'])
                if datetime.now() > expires_at:
                    # Süresi dolmuş oturum
                    self.invalidate_session(session_token)
                    return False
                
                # Cihaz kontrolü
                if session_data['device_id'] not in self.authorized_devices:
                    log_error("Yetkisiz cihaz oturum erişimi")
                    return False
                
                # Son aktiviteyi güncelle
                session_data['last_activity'] = datetime.now().isoformat()
                
                return True
            else:
                # Şifrelenmiş oturum verilerini kontrol et
                encrypted_session = encryption_manager.decrypt_data(filename=f"session_{session_token}")
                if encrypted_session:
                    # Oturumu memory'ye yükle
                    self.user_sessions[session_token] = encrypted_session
                    return self.verify_session(session_token)
                
                return False
                
        except Exception as e:
            log_error(f"Oturum doğrulama hatası: {e}")
            return False
    
    def invalidate_session(self, session_token: str) -> bool:
        """Oturumu geçersiz kıl"""
        try:
            if session_token in self.user_sessions:
                del self.user_sessions[session_token]
            
            # Şifrelenmiş oturum dosyasını sil
            session_file = f"data/encrypted/session_{session_token}.enc"
            if os.path.exists(session_file):
                os.remove(session_file)
            
            log_info(f"Oturum geçersiz kılındı: {session_token}")
            return True
            
        except Exception as e:
            log_error(f"Oturum geçersiz kılma hatası: {e}")
            return False
    
    def get_session_info(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Oturum bilgilerini getir"""
        try:
            if self.verify_session(session_token):
                return self.user_sessions.get(session_token, {})
            return None
            
        except Exception as e:
            log_error(f"Oturum bilgisi alma hatası: {e}")
            return None
    
    def check_rate_limit(self, client_ip: str, action: str) -> bool:
        """Rate limit kontrolü"""
        try:
            current_time = datetime.now()
            key = f"{client_ip}_{action}"
            
            if key not in self.failed_attempts:
                self.failed_attempts[key] = []
            
            # Eski kayıtları temizle (1 saat öncesi)
            cutoff_time = current_time - timedelta(hours=1)
            self.failed_attempts[key] = [
                attempt_time for attempt_time in self.failed_attempts[key]
                if attempt_time > cutoff_time
            ]
            
            # Rate limit kontrolü
            if len(self.failed_attempts[key]) >= self.max_failed_attempts:
                log_error(f"Rate limit aşıldı: {client_ip} - {action}")
                return False
            
            return True
            
        except Exception as e:
            log_error(f"Rate limit kontrolü hatası: {e}")
            return True
    
    def record_failed_attempt(self, client_ip: str, action: str):
        """Başarısız denemeyi kaydet"""
        try:
            key = f"{client_ip}_{action}"
            if key not in self.failed_attempts:
                self.failed_attempts[key] = []
            
            self.failed_attempts[key].append(datetime.now())
            
        except Exception as e:
            log_error(f"Başarısız deneme kaydetme hatası: {e}")
    
    def create_personal_api_key(self) -> str:
        """Kişisel API anahtarı oluştur"""
        try:
            # Kişisel kullanım için sabit API key
            personal_data = f"PlanB_Motoru_Personal_API_{self.personal_device_id}"
            api_key = hashlib.sha256(personal_data.encode()).hexdigest()
            
            # API key'i şifrele ve kaydet
            api_key_data = {
                'api_key': api_key,
                'created_at': datetime.now().isoformat(),
                'device_id': self.personal_device_id,
                'permissions': ['read', 'write', 'admin'],
                'expires_at': (datetime.now() + timedelta(days=365)).isoformat()
            }
            
            encryption_manager.encrypt_data(api_key_data, "personal_api_key")
            
            log_info("Kişisel API anahtarı oluşturuldu")
            return api_key
            
        except Exception as e:
            log_error(f"API anahtarı oluşturma hatası: {e}")
            return ""
    
    def verify_api_key(self, api_key: str) -> bool:
        """API anahtarını doğrula"""
        try:
            # Şifrelenmiş API key verilerini yükle
            api_key_data = encryption_manager.decrypt_data(filename="personal_api_key")
            if not api_key_data:
                return False
            
            # API key kontrolü
            if api_key == api_key_data['api_key']:
                # Süre kontrolü
                expires_at = datetime.fromisoformat(api_key_data['expires_at'])
                if datetime.now() > expires_at:
                    log_error("API anahtarı süresi dolmuş")
                    return False
                
                # Cihaz kontrolü
                if api_key_data['device_id'] != self.personal_device_id:
                    log_error("API anahtarı yetkisiz cihaz için")
                    return False
                
                return True
            
            return False
            
        except Exception as e:
            log_error(f"API anahtarı doğrulama hatası: {e}")
            return False
    
    def log_access_attempt(self, action: str, success: bool, details: Dict[str, Any] = None):
        """Erişim denemesini logla"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'success': success,
                'device_id': self.personal_device_id,
                'details': details or {}
            }
            
            # Log dosyasına kaydet
            log_file = "data/security/access_log.json"
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            
            # Mevcut logları yükle
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Yeni log ekle
            logs.append(log_entry)
            
            # Son 1000 log'u tut
            if len(logs) > 1000:
                logs = logs[-1000:]
            
            # Log'u şifrele ve kaydet
            encryption_manager.encrypt_data(logs, "access_log")
            
            # Şifrelenmemiş kopya da tut (debug için)
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            log_error(f"Erişim log kaydetme hatası: {e}")
    
    def get_access_statistics(self) -> Dict[str, Any]:
        """Erişim istatistiklerini getir"""
        try:
            # Şifrelenmiş log'ları yükle
            logs = encryption_manager.decrypt_data(filename="access_log") or []
            
            if not logs:
                return {}
            
            # İstatistikleri hesapla
            total_attempts = len(logs)
            successful_attempts = len([log for log in logs if log['success']])
            failed_attempts = total_attempts - successful_attempts
            
            # Son 24 saat
            last_24h = datetime.now() - timedelta(hours=24)
            recent_logs = [log for log in logs if datetime.fromisoformat(log['timestamp']) > last_24h]
            
            # En çok kullanılan aksiyonlar
            action_counts = {}
            for log in logs:
                action = log['action']
                action_counts[action] = action_counts.get(action, 0) + 1
            
            return {
                'total_attempts': total_attempts,
                'successful_attempts': successful_attempts,
                'failed_attempts': failed_attempts,
                'success_rate': (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0,
                'recent_attempts_24h': len(recent_logs),
                'most_used_actions': sorted(action_counts.items(), key=lambda x: x[1], reverse=True)[:5],
                'active_sessions': len(self.user_sessions),
                'authorized_devices': len(self.authorized_devices),
                'last_activity': logs[-1]['timestamp'] if logs else None
            }
            
        except Exception as e:
            log_error(f"Erişim istatistikleri alma hatası: {e}")
            return {}
    
    def cleanup_expired_sessions(self):
        """Süresi dolmuş oturumları temizle"""
        try:
            current_time = datetime.now()
            expired_sessions = []
            
            for session_token, session_data in self.user_sessions.items():
                expires_at = datetime.fromisoformat(session_data['expires_at'])
                if current_time > expires_at:
                    expired_sessions.append(session_token)
            
            # Süresi dolmuş oturumları sil
            for session_token in expired_sessions:
                self.invalidate_session(session_token)
            
            if expired_sessions:
                log_info(f"{len(expired_sessions)} süresi dolmuş oturum temizlendi")
            
        except Exception as e:
            log_error(f"Oturum temizleme hatası: {e}")

# Global access control instance
access_control = AccessControl()

