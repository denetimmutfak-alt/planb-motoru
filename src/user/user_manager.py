"""
PlanB Motoru - User Manager
Kullanıcı hesapları ve tercihleri yönetimi
"""
import json
import os
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from src.security.encryption_manager import encryption_manager
from src.utils.logger import log_info, log_error, log_debug

class UserManager:
    """Kullanıcı yöneticisi"""
    
    def __init__(self):
        self.users_file = "data/users/users.json"
        self.preferences_file = "data/users/preferences.json"
        self.sessions_file = "data/users/sessions.json"
        self._ensure_user_directory()
        self._load_users()
        self._load_preferences()
        self._load_sessions()
    
    def _ensure_user_directory(self):
        """Kullanıcı dizinini oluştur"""
        os.makedirs("data/users", exist_ok=True)
    
    def _load_users(self):
        """Kullanıcıları yükle"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            else:
                self.users = {}
                self._create_default_user()
            log_info(f"{len(self.users)} kullanıcı yüklendi")
        except Exception as e:
            log_error(f"Kullanıcı yükleme hatası: {e}")
            self.users = {}
    
    def _load_preferences(self):
        """Kullanıcı tercihlerini yükle"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    self.preferences = json.load(f)
            else:
                self.preferences = {}
            log_info(f"{len(self.preferences)} kullanıcı tercihi yüklendi")
        except Exception as e:
            log_error(f"Kullanıcı tercihleri yükleme hatası: {e}")
            self.preferences = {}
    
    def _load_sessions(self):
        """Kullanıcı oturumlarını yükle"""
        try:
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    self.sessions = json.load(f)
            else:
                self.sessions = {}
            log_info(f"{len(self.sessions)} kullanıcı oturumu yüklendi")
        except Exception as e:
            log_error(f"Kullanıcı oturumları yükleme hatası: {e}")
            self.sessions = {}
    
    def _create_default_user(self):
        """Varsayılan kullanıcı oluştur"""
        try:
            default_user = {
                'user_id': 'default_user',
                'username': 'PlanB_User',
                'email': 'user@planbmotoru.com',
                'password_hash': self._hash_password('Personal_Access_2024'),
                'role': 'admin',
                'status': 'active',
                'created_at': datetime.now().isoformat(),
                'last_login': None,
                'login_count': 0,
                'preferences': {
                    'theme': 'light',
                    'language': 'tr',
                    'timezone': 'Europe/Istanbul',
                    'notifications': {
                        'email': True,
                        'push': True,
                        'sms': False
                    },
                    'dashboard': {
                        'default_market': 'bist',
                        'auto_refresh': True,
                        'refresh_interval': 30,
                        'show_advanced_analysis': True
                    },
                    'analysis': {
                        'default_timeframe': '1d',
                        'show_technical_indicators': True,
                        'show_astrology_analysis': True,
                        'show_sentiment_analysis': True,
                        'confidence_threshold': 0.7
                    },
                    'portfolio': {
                        'default_currency': 'TRY',
                        'show_pnl_percentage': True,
                        'show_daily_change': True,
                        'auto_update_prices': True
                    },
                    'alerts': {
                        'price_alerts': True,
                        'analysis_alerts': True,
                        'sentiment_alerts': True,
                        'email_alerts': True
                    }
                }
            }
            
            self.users['default_user'] = default_user
            self._save_users()
            log_info("Varsayılan kullanıcı oluşturuldu")
            
        except Exception as e:
            log_error(f"Varsayılan kullanıcı oluşturma hatası: {e}")
    
    def create_user(self, username: str, email: str, password: str, role: str = 'user') -> bool:
        """Yeni kullanıcı oluştur"""
        try:
            # Kullanıcı adı kontrolü
            if self._username_exists(username):
                log_error(f"Kullanıcı adı zaten mevcut: {username}")
                return False
            
            # Email kontrolü
            if self._email_exists(email):
                log_error(f"Email zaten mevcut: {email}")
                return False
            
            # Kullanıcı ID oluştur
            user_id = self._generate_user_id(username)
            
            # Yeni kullanıcı
            new_user = {
                'user_id': user_id,
                'username': username,
                'email': email,
                'password_hash': self._hash_password(password),
                'role': role,
                'status': 'active',
                'created_at': datetime.now().isoformat(),
                'last_login': None,
                'login_count': 0,
                'preferences': self._get_default_preferences()
            }
            
            self.users[user_id] = new_user
            self._save_users()
            
            log_info(f"Yeni kullanıcı oluşturuldu: {username}")
            return True
            
        except Exception as e:
            log_error(f"Kullanıcı oluşturma hatası: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Kullanıcı kimlik doğrulama"""
        try:
            # Kullanıcıyı bul
            user = self._find_user_by_username(username)
            if not user:
                log_error(f"Kullanıcı bulunamadı: {username}")
                return None
            
            # Şifre kontrolü
            if not self._verify_password(password, user['password_hash']):
                log_error(f"Geçersiz şifre: {username}")
                return None
            
            # Kullanıcı durumu kontrolü
            if user['status'] != 'active':
                log_error(f"Kullanıcı aktif değil: {username}")
                return None
            
            # Giriş bilgilerini güncelle
            user['last_login'] = datetime.now().isoformat()
            user['login_count'] = user.get('login_count', 0) + 1
            
            self._save_users()
            
            # Oturum oluştur
            session_id = self._create_session(user['user_id'])
            
            log_info(f"Kullanıcı giriş yaptı: {username}")
            
            return {
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'session_id': session_id,
                'preferences': user['preferences']
            }
            
        except Exception as e:
            log_error(f"Kullanıcı kimlik doğrulama hatası: {e}")
            return None
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Kullanıcı bilgilerini getir"""
        try:
            return self.users.get(user_id)
        except Exception as e:
            log_error(f"Kullanıcı bilgisi alma hatası: {e}")
            return None
    
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """Kullanıcı bilgilerini güncelle"""
        try:
            if user_id not in self.users:
                log_error(f"Kullanıcı bulunamadı: {user_id}")
                return False
            
            # Güncellenebilir alanlar
            allowed_fields = ['email', 'role', 'status']
            
            for field, value in update_data.items():
                if field in allowed_fields:
                    self.users[user_id][field] = value
            
            self.users[user_id]['updated_at'] = datetime.now().isoformat()
            self._save_users()
            
            log_info(f"Kullanıcı güncellendi: {user_id}")
            return True
            
        except Exception as e:
            log_error(f"Kullanıcı güncelleme hatası: {e}")
            return False
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """Şifre değiştir"""
        try:
            if user_id not in self.users:
                log_error(f"Kullanıcı bulunamadı: {user_id}")
                return False
            
            user = self.users[user_id]
            
            # Eski şifre kontrolü
            if not self._verify_password(old_password, user['password_hash']):
                log_error(f"Eski şifre yanlış: {user_id}")
                return False
            
            # Yeni şifre hash'le
            user['password_hash'] = self._hash_password(new_password)
            user['password_changed_at'] = datetime.now().isoformat()
            
            self._save_users()
            
            log_info(f"Şifre değiştirildi: {user_id}")
            return True
            
        except Exception as e:
            log_error(f"Şifre değiştirme hatası: {e}")
            return False
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Kullanıcı tercihlerini getir"""
        try:
            if user_id in self.users:
                return self.users[user_id].get('preferences', self._get_default_preferences())
            else:
                return self._get_default_preferences()
        except Exception as e:
            log_error(f"Kullanıcı tercihleri alma hatası: {e}")
            return self._get_default_preferences()
    
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Kullanıcı tercihlerini güncelle"""
        try:
            if user_id not in self.users:
                log_error(f"Kullanıcı bulunamadı: {user_id}")
                return False
            
            # Mevcut tercihleri al
            current_preferences = self.users[user_id].get('preferences', {})
            
            # Yeni tercihleri birleştir
            updated_preferences = self._merge_preferences(current_preferences, preferences)
            
            # Tercihleri güncelle
            self.users[user_id]['preferences'] = updated_preferences
            self.users[user_id]['preferences_updated_at'] = datetime.now().isoformat()
            
            self._save_users()
            
            log_info(f"Kullanıcı tercihleri güncellendi: {user_id}")
            return True
            
        except Exception as e:
            log_error(f"Kullanıcı tercihleri güncelleme hatası: {e}")
            return False
    
    def create_session(self, user_id: str) -> str:
        """Kullanıcı oturumu oluştur"""
        try:
            session_id = self._generate_session_id()
            
            session_data = {
                'session_id': session_id,
                'user_id': user_id,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
                'last_activity': datetime.now().isoformat(),
                'ip_address': '127.0.0.1',  # Local access
                'user_agent': 'PlanB_Motoru_Client'
            }
            
            self.sessions[session_id] = session_data
            self._save_sessions()
            
            log_info(f"Oturum oluşturuldu: {session_id}")
            return session_id
            
        except Exception as e:
            log_error(f"Oturum oluşturma hatası: {e}")
            return ""
    
    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Oturum doğrulama"""
        try:
            if session_id not in self.sessions:
                return None
            
            session = self.sessions[session_id]
            
            # Süre kontrolü
            expires_at = datetime.fromisoformat(session['expires_at'])
            if datetime.now() > expires_at:
                self._delete_session(session_id)
                return None
            
            # Son aktiviteyi güncelle
            session['last_activity'] = datetime.now().isoformat()
            self._save_sessions()
            
            # Kullanıcı bilgilerini getir
            user = self.get_user(session['user_id'])
            if not user:
                self._delete_session(session_id)
                return None
            
            return {
                'user_id': user['user_id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'session_id': session_id,
                'preferences': user['preferences']
            }
            
        except Exception as e:
            log_error(f"Oturum doğrulama hatası: {e}")
            return None
    
    def delete_session(self, session_id: str) -> bool:
        """Oturumu sil"""
        try:
            return self._delete_session(session_id)
        except Exception as e:
            log_error(f"Oturum silme hatası: {e}")
            return False
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Tüm kullanıcıları getir"""
        try:
            users_list = []
            for user_id, user_data in self.users.items():
                # Hassas bilgileri çıkar
                safe_user_data = {
                    'user_id': user_data['user_id'],
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'role': user_data['role'],
                    'status': user_data['status'],
                    'created_at': user_data['created_at'],
                    'last_login': user_data.get('last_login'),
                    'login_count': user_data.get('login_count', 0)
                }
                users_list.append(safe_user_data)
            
            return users_list
            
        except Exception as e:
            log_error(f"Kullanıcı listesi alma hatası: {e}")
            return []
    
    def delete_user(self, user_id: str) -> bool:
        """Kullanıcıyı sil"""
        try:
            if user_id not in self.users:
                log_error(f"Kullanıcı bulunamadı: {user_id}")
                return False
            
            # Kullanıcının oturumlarını sil
            sessions_to_delete = [sid for sid, session in self.sessions.items() if session['user_id'] == user_id]
            for session_id in sessions_to_delete:
                self._delete_session(session_id)
            
            # Kullanıcıyı sil
            del self.users[user_id]
            self._save_users()
            
            log_info(f"Kullanıcı silindi: {user_id}")
            return True
            
        except Exception as e:
            log_error(f"Kullanıcı silme hatası: {e}")
            return False
    
    def _username_exists(self, username: str) -> bool:
        """Kullanıcı adı var mı kontrol et"""
        for user in self.users.values():
            if user['username'] == username:
                return True
        return False
    
    def _email_exists(self, email: str) -> bool:
        """Email var mı kontrol et"""
        for user in self.users.values():
            if user['email'] == email:
                return True
        return False
    
    def _find_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Kullanıcı adına göre kullanıcı bul"""
        for user in self.users.values():
            if user['username'] == username:
                return user
        return None
    
    def _generate_user_id(self, username: str) -> str:
        """Kullanıcı ID oluştur"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{username.lower()}_{timestamp}"
    
    def _generate_session_id(self) -> str:
        """Oturum ID oluştur"""
        import secrets
        return secrets.token_urlsafe(32)
    
    def _hash_password(self, password: str) -> str:
        """Şifre hash'le"""
        salt = "PlanB_Motoru_Salt_2024"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Şifre doğrula"""
        return self._hash_password(password) == password_hash
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Varsayılan tercihler"""
        return {
            'theme': 'light',
            'language': 'tr',
            'timezone': 'Europe/Istanbul',
            'notifications': {
                'email': True,
                'push': True,
                'sms': False
            },
            'dashboard': {
                'default_market': 'bist',
                'auto_refresh': True,
                'refresh_interval': 30,
                'show_advanced_analysis': True
            },
            'analysis': {
                'default_timeframe': '1d',
                'show_technical_indicators': True,
                'show_astrology_analysis': True,
                'show_sentiment_analysis': True,
                'confidence_threshold': 0.7
            },
            'portfolio': {
                'default_currency': 'TRY',
                'show_pnl_percentage': True,
                'show_daily_change': True,
                'auto_update_prices': True
            },
            'alerts': {
                'price_alerts': True,
                'analysis_alerts': True,
                'sentiment_alerts': True,
                'email_alerts': True
            }
        }
    
    def _merge_preferences(self, current: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Tercihleri birleştir"""
        try:
            merged = current.copy()
            
            for key, value in new.items():
                if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                    merged[key] = self._merge_preferences(merged[key], value)
                else:
                    merged[key] = value
            
            return merged
            
        except Exception as e:
            log_error(f"Tercih birleştirme hatası: {e}")
            return current
    
    def _create_session(self, user_id: str) -> str:
        """Oturum oluştur (internal)"""
        return self.create_session(user_id)
    
    def _delete_session(self, session_id: str) -> bool:
        """Oturumu sil (internal)"""
        try:
            if session_id in self.sessions:
                del self.sessions[session_id]
                self._save_sessions()
                log_info(f"Oturum silindi: {session_id}")
                return True
            return False
        except Exception as e:
            log_error(f"Oturum silme hatası: {e}")
            return False
    
    def _save_users(self):
        """Kullanıcıları kaydet"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Kullanıcı kaydetme hatası: {e}")
    
    def _save_preferences(self):
        """Tercihleri kaydet"""
        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Tercih kaydetme hatası: {e}")
    
    def _save_sessions(self):
        """Oturumları kaydet"""
        try:
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(self.sessions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Oturum kaydetme hatası: {e}")
    
    def cleanup_expired_sessions(self):
        """Süresi dolmuş oturumları temizle"""
        try:
            current_time = datetime.now()
            expired_sessions = []
            
            for session_id, session_data in self.sessions.items():
                expires_at = datetime.fromisoformat(session_data['expires_at'])
                if current_time > expires_at:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                self._delete_session(session_id)
            
            if expired_sessions:
                log_info(f"{len(expired_sessions)} süresi dolmuş oturum temizlendi")
            
        except Exception as e:
            log_error(f"Oturum temizleme hatası: {e}")
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """Kullanıcı istatistikleri"""
        try:
            total_users = len(self.users)
            active_users = len([u for u in self.users.values() if u['status'] == 'active'])
            total_sessions = len(self.sessions)
            
            # Son 24 saatte giriş yapan kullanıcılar
            last_24h = datetime.now() - timedelta(hours=24)
            recent_logins = len([
                u for u in self.users.values() 
                if u.get('last_login') and datetime.fromisoformat(u['last_login']) > last_24h
            ])
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': total_users - active_users,
                'total_sessions': total_sessions,
                'recent_logins_24h': recent_logins,
                'user_roles': {
                    role: len([u for u in self.users.values() if u['role'] == role])
                    for role in set(u['role'] for u in self.users.values())
                }
            }
            
        except Exception as e:
            log_error(f"Kullanıcı istatistikleri alma hatası: {e}")
            return {}

# Global user manager instance
user_manager = UserManager()

