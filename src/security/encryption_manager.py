"""
PlanB Motoru - Encryption Manager
AES şifreleme ve güvenli veri saklama
"""
import os
import json
import base64
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from src.utils.logger import log_info, log_error, log_debug

class EncryptionManager:
    """AES şifreleme yöneticisi"""
    
    def __init__(self):
        self.master_key = None
        self.fernet = None
        self.key_file = "data/security/master.key"
        self.salt_file = "data/security/salt.key"
        self._ensure_security_dir()
        self._load_or_generate_keys()
    
    def _ensure_security_dir(self):
        """Güvenlik dizinini oluştur"""
        os.makedirs("data/security", exist_ok=True)
        os.makedirs("data/encrypted", exist_ok=True)
    
    def _load_or_generate_keys(self):
        """Anahtar yükle veya oluştur"""
        try:
            # Kişisel kullanım için sabit master password
            master_password = self._get_master_password()
            
            if os.path.exists(self.salt_file):
                # Mevcut salt'ı yükle
                with open(self.salt_file, 'rb') as f:
                    salt = f.read()
            else:
                # Yeni salt oluştur
                salt = os.urandom(16)
                with open(self.salt_file, 'wb') as f:
                    f.write(salt)
            
            # Anahtar türet
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
            
            self.fernet = Fernet(key)
            self.master_key = key
            
            log_info("Şifreleme anahtarları yüklendi")
            
        except Exception as e:
            log_error(f"Anahtar yükleme hatası: {e}")
            self.fernet = None
    
    def _get_master_password(self) -> str:
        """Kişisel master password al"""
        # Kişisel kullanım için sabit password
        # Gerçek uygulamada environment variable veya güvenli input kullanılmalı
        personal_id = "PlanB_Motoru_Personal_2024"
        return personal_id
    
    def encrypt_data(self, data: Any, filename: str = None) -> Optional[str]:
        """Veriyi şifrele"""
        try:
            if not self.fernet:
                log_error("Şifreleme anahtarı yok")
                return None
            
            # Veriyi JSON string'e çevir
            if isinstance(data, (dict, list)):
                json_data = json.dumps(data, ensure_ascii=False, indent=2)
            else:
                json_data = str(data)
            
            # Şifrele
            encrypted_data = self.fernet.encrypt(json_data.encode())
            
            if filename:
                # Dosyaya kaydet
                filepath = f"data/encrypted/{filename}.enc"
                with open(filepath, 'wb') as f:
                    f.write(encrypted_data)
                log_debug(f"Veri şifrelendi ve kaydedildi: {filename}")
                return filepath
            else:
                # Base64 string olarak döndür
                return base64.b64encode(encrypted_data).decode()
            
        except Exception as e:
            log_error(f"Veri şifreleme hatası: {e}")
            return None
    
    def decrypt_data(self, encrypted_data: str = None, filename: str = None) -> Optional[Any]:
        """Veriyi şifresini çöz"""
        try:
            if not self.fernet:
                log_error("Şifreleme anahtarı yok")
                return None
            
            # Veriyi al
            if filename:
                filepath = f"data/encrypted/{filename}.enc"
                if not os.path.exists(filepath):
                    log_error(f"Şifreli dosya bulunamadı: {filename}")
                    return None
                
                with open(filepath, 'rb') as f:
                    encrypted_bytes = f.read()
            else:
                # Base64 string'den bytes'a çevir
                encrypted_bytes = base64.b64decode(encrypted_data.encode())
            
            # Şifresini çöz
            decrypted_data = self.fernet.decrypt(encrypted_bytes)
            json_data = decrypted_data.decode()
            
            # JSON parse et
            try:
                return json.loads(json_data)
            except json.JSONDecodeError:
                return json_data
            
        except Exception as e:
            log_error(f"Veri şifre çözme hatası: {e}")
            return None
    
    def encrypt_sensitive_config(self, config_data: Dict[str, Any]) -> bool:
        """Hassas konfigürasyonu şifrele"""
        try:
            sensitive_keys = ['api_keys', 'passwords', 'tokens', 'secrets']
            encrypted_config = {}
            
            for key, value in config_data.items():
                if any(sensitive in key.lower() for sensitive in sensitive_keys):
                    # Hassas veriyi şifrele
                    encrypted_value = self.encrypt_data(value)
                    encrypted_config[f"{key}_encrypted"] = encrypted_value
                else:
                    encrypted_config[key] = value
            
            # Şifrelenmiş konfigürasyonu kaydet
            return self.encrypt_data(encrypted_config, "sensitive_config") is not None
            
        except Exception as e:
            log_error(f"Hassas konfigürasyon şifreleme hatası: {e}")
            return False
    
    def decrypt_sensitive_config(self) -> Optional[Dict[str, Any]]:
        """Hassas konfigürasyonu şifresini çöz"""
        try:
            encrypted_config = self.decrypt_data(filename="sensitive_config")
            if not encrypted_config:
                return None
            
            decrypted_config = {}
            
            for key, value in encrypted_config.items():
                if key.endswith('_encrypted'):
                    # Şifrelenmiş veriyi çöz
                    original_key = key.replace('_encrypted', '')
                    decrypted_value = self.decrypt_data(value)
                    decrypted_config[original_key] = decrypted_value
                else:
                    decrypted_config[key] = value
            
            return decrypted_config
            
        except Exception as e:
            log_error(f"Hassas konfigürasyon şifre çözme hatası: {e}")
            return None
    
    def encrypt_portfolio_data(self, portfolio_data: Dict[str, Any]) -> bool:
        """Portföy verilerini şifrele"""
        try:
            # Portföy verilerini şifrele
            encrypted_portfolio = {
                'positions': self.encrypt_data(portfolio_data.get('positions', [])),
                'transactions': self.encrypt_data(portfolio_data.get('transactions', [])),
                'metadata': {
                    'name': portfolio_data.get('name', ''),
                    'created_date': portfolio_data.get('created_date', ''),
                    'last_updated': datetime.now().isoformat(),
                    'encrypted': True
                }
            }
            
            return self.encrypt_data(encrypted_portfolio, f"portfolio_{portfolio_data.get('name', 'default')}") is not None
            
        except Exception as e:
            log_error(f"Portföy şifreleme hatası: {e}")
            return False
    
    def decrypt_portfolio_data(self, portfolio_name: str) -> Optional[Dict[str, Any]]:
        """Portföy verilerini şifresini çöz"""
        try:
            encrypted_portfolio = self.decrypt_data(filename=f"portfolio_{portfolio_name}")
            if not encrypted_portfolio:
                return None
            
            # Şifrelenmiş verileri çöz
            decrypted_portfolio = {
                'name': encrypted_portfolio['metadata']['name'],
                'created_date': encrypted_portfolio['metadata']['created_date'],
                'last_updated': encrypted_portfolio['metadata']['last_updated'],
                'positions': self.decrypt_data(encrypted_portfolio['positions']),
                'transactions': self.decrypt_data(encrypted_portfolio['transactions'])
            }
            
            return decrypted_portfolio
            
        except Exception as e:
            log_error(f"Portföy şifre çözme hatası: {e}")
            return None
    
    def encrypt_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Kullanıcı tercihlerini şifrele"""
        try:
            encrypted_prefs = {
                'user_id': user_id,
                'preferences': self.encrypt_data(preferences),
                'encrypted_at': datetime.now().isoformat()
            }
            
            return self.encrypt_data(encrypted_prefs, f"user_prefs_{user_id}") is not None
            
        except Exception as e:
            log_error(f"Kullanıcı tercihleri şifreleme hatası: {e}")
            return False
    
    def decrypt_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Kullanıcı tercihlerini şifresini çöz"""
        try:
            encrypted_prefs = self.decrypt_data(filename=f"user_prefs_{user_id}")
            if not encrypted_prefs:
                return None
            
            return {
                'user_id': encrypted_prefs['user_id'],
                'preferences': self.decrypt_data(encrypted_prefs['preferences']),
                'encrypted_at': encrypted_prefs['encrypted_at']
            }
            
        except Exception as e:
            log_error(f"Kullanıcı tercihleri şifre çözme hatası: {e}")
            return None
    
    def create_secure_hash(self, data: str) -> str:
        """Güvenli hash oluştur"""
        try:
            # Salt ekle
            salt = self._get_master_password()
            salted_data = f"{data}{salt}"
            
            # SHA-256 hash
            hash_object = hashlib.sha256(salted_data.encode())
            return hash_object.hexdigest()
            
        except Exception as e:
            log_error(f"Hash oluşturma hatası: {e}")
            return ""
    
    def verify_data_integrity(self, data: str, expected_hash: str) -> bool:
        """Veri bütünlüğünü doğrula"""
        try:
            actual_hash = self.create_secure_hash(data)
            return actual_hash == expected_hash
            
        except Exception as e:
            log_error(f"Veri bütünlüğü doğrulama hatası: {e}")
            return False
    
    def secure_delete_file(self, filepath: str) -> bool:
        """Dosyayı güvenli şekilde sil"""
        try:
            if os.path.exists(filepath):
                # Dosyayı rastgele veriyle üzerine yaz
                with open(filepath, 'r+b') as f:
                    file_size = os.path.getsize(filepath)
                    f.write(os.urandom(file_size))
                
                # Dosyayı sil
                os.remove(filepath)
                log_debug(f"Dosya güvenli şekilde silindi: {filepath}")
                return True
            
            return False
            
        except Exception as e:
            log_error(f"Güvenli dosya silme hatası: {e}")
            return False
    
    def get_encryption_status(self) -> Dict[str, Any]:
        """Şifreleme durumunu getir"""
        try:
            return {
                'encryption_available': self.fernet is not None,
                'master_key_loaded': self.master_key is not None,
                'security_directory_exists': os.path.exists("data/security"),
                'encrypted_directory_exists': os.path.exists("data/encrypted"),
                'salt_file_exists': os.path.exists(self.salt_file),
                'key_file_exists': os.path.exists(self.key_file)
            }
            
        except Exception as e:
            log_error(f"Şifreleme durumu alınırken hata: {e}")
            return {}

# Global encryption manager instance
encryption_manager = EncryptionManager()

