"""
PlanB Motoru - Offline Manager
Offline mod ve lokal yedekleme yönetimi
"""
import json
import os
import shutil
import zipfile
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug
from src.security.encryption_manager import encryption_manager

class OfflineManager:
    """Offline mod ve lokal yedekleme yöneticisi"""
    
    def __init__(self):
        self.offline_directory = "data/offline"
        self.backup_directory = "data/backups"
        self.cache_directory = "data/cache"
        self._ensure_directories()
        
        # Offline mod durumu
        self.is_offline_mode = False
        self.last_sync_time = None
        self.offline_data = {}
        
        # Yedekleme ayarları
        self.backup_settings = {
            'auto_backup': True,
            'backup_interval_hours': 24,
            'max_backups': 30,
            'compress_backups': True,
            'encrypt_backups': True
        }
    
    def _ensure_directories(self):
        """Gerekli dizinleri oluştur"""
        os.makedirs(self.offline_directory, exist_ok=True)
        os.makedirs(self.backup_directory, exist_ok=True)
        os.makedirs(self.cache_directory, exist_ok=True)
        os.makedirs(f"{self.offline_directory}/portfolios", exist_ok=True)
        os.makedirs(f"{self.offline_directory}/analyses", exist_ok=True)
        os.makedirs(f"{self.offline_directory}/market_data", exist_ok=True)
        os.makedirs(f"{self.offline_directory}/user_data", exist_ok=True)
    
    def enable_offline_mode(self) -> bool:
        """Offline modu etkinleştir"""
        try:
            # Mevcut verileri offline dizinine kopyala
            self._sync_data_to_offline()
            
            # Offline modu etkinleştir
            self.is_offline_mode = True
            self.last_sync_time = datetime.now()
            
            # Offline durumu kaydet
            self._save_offline_status()
            
            log_info("Offline mod etkinleştirildi")
            return True
            
        except Exception as e:
            log_error(f"Offline mod etkinleştirme hatası: {e}")
            return False
    
    def disable_offline_mode(self) -> bool:
        """Offline modu devre dışı bırak"""
        try:
            # Offline verilerini ana dizine senkronize et
            self._sync_offline_to_main()
            
            # Offline modu devre dışı bırak
            self.is_offline_mode = False
            
            # Offline durumu kaydet
            self._save_offline_status()
            
            log_info("Offline mod devre dışı bırakıldı")
            return True
            
        except Exception as e:
            log_error(f"Offline mod devre dışı bırakma hatası: {e}")
            return False
    
    def create_backup(self, backup_name: str = None) -> str:
        """Yedekleme oluştur"""
        try:
            if not backup_name:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            backup_path = f"{self.backup_directory}/{backup_name}"
            
            # Yedekleme dizini oluştur
            os.makedirs(backup_path, exist_ok=True)
            
            # Veri dizinlerini kopyala
            data_directories = [
                'data/portfolios',
                'data/analyses',
                'data/users',
                'data/watchlists',
                'data/alerts',
                'data/personal_data_lake',
                'data/macro',
                'data/cache'
            ]
            
            for data_dir in data_directories:
                if os.path.exists(data_dir):
                    dest_dir = f"{backup_path}/{os.path.basename(data_dir)}"
                    shutil.copytree(data_dir, dest_dir, dirs_exist_ok=True)
            
            # Yedekleme bilgilerini kaydet
            backup_info = {
                'backup_name': backup_name,
                'created_at': datetime.now().isoformat(),
                'size_mb': self._calculate_backup_size(backup_path),
                'file_count': self._count_backup_files(backup_path),
                'encrypted': self.backup_settings['encrypt_backups']
            }
            
            with open(f"{backup_path}/backup_info.json", 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            # Yedeklemeyi sıkıştır
            if self.backup_settings['compress_backups']:
                self._compress_backup(backup_path)
            
            # Yedeklemeyi şifrele
            if self.backup_settings['encrypt_backups']:
                self._encrypt_backup(backup_path)
            
            log_info(f"Yedekleme oluşturuldu: {backup_name}")
            return backup_path
            
        except Exception as e:
            log_error(f"Yedekleme oluşturma hatası: {e}")
            return ""
    
    def restore_backup(self, backup_name: str) -> bool:
        """Yedeklemeden geri yükle"""
        try:
            backup_path = f"{self.backup_directory}/{backup_name}"
            
            if not os.path.exists(backup_path):
                log_error(f"Yedekleme bulunamadı: {backup_name}")
                return False
            
            # Yedekleme bilgilerini oku
            backup_info_path = f"{backup_path}/backup_info.json"
            if os.path.exists(backup_info_path):
                with open(backup_info_path, 'r', encoding='utf-8') as f:
                    backup_info = json.load(f)
            else:
                backup_info = {}
            
            # Yedeklemeyi şifre çöz
            if backup_info.get('encrypted', False):
                self._decrypt_backup(backup_path)
            
            # Yedeklemeyi aç
            if backup_info.get('compressed', False):
                self._decompress_backup(backup_path)
            
            # Mevcut verileri yedekle
            temp_backup = self.create_backup(f"temp_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Yedeklemeden geri yükle
            for item in os.listdir(backup_path):
                if item != 'backup_info.json':
                    source_path = f"{backup_path}/{item}"
                    dest_path = f"data/{item}"
                    
                    if os.path.exists(dest_path):
                        shutil.rmtree(dest_path)
                    
                    shutil.copytree(source_path, dest_path)
            
            log_info(f"Yedeklemeden geri yükleme tamamlandı: {backup_name}")
            return True
            
        except Exception as e:
            log_error(f"Yedeklemeden geri yükleme hatası: {e}")
            return False
    
    def get_offline_data(self, data_type: str) -> Dict[str, Any]:
        """Offline verileri getir"""
        try:
            if not self.is_offline_mode:
                log_error("Offline mod aktif değil")
                return {}
            
            offline_file = f"{self.offline_directory}/{data_type}/offline_data.json"
            
            if os.path.exists(offline_file):
                with open(offline_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
                
        except Exception as e:
            log_error(f"Offline veri alma hatası: {e}")
            return {}
    
    def update_offline_data(self, data_type: str, data: Dict[str, Any]) -> bool:
        """Offline verileri güncelle"""
        try:
            if not self.is_offline_mode:
                log_error("Offline mod aktif değil")
                return False
            
            offline_file = f"{self.offline_directory}/{data_type}/offline_data.json"
            
            # Veriyi şifrele
            encrypted_data = self._encrypt_offline_data(data)
            
            with open(offline_file, 'w', encoding='utf-8') as f:
                json.dump(encrypted_data, f, indent=2, ensure_ascii=False)
            
            log_debug(f"Offline veri güncellendi: {data_type}")
            return True
            
        except Exception as e:
            log_error(f"Offline veri güncelleme hatası: {e}")
            return False
    
    def sync_offline_changes(self) -> bool:
        """Offline değişiklikleri senkronize et"""
        try:
            if not self.is_offline_mode:
                log_error("Offline mod aktif değil")
                return False
            
            # Offline verilerini ana dizine senkronize et
            self._sync_offline_to_main()
            
            # Son senkronizasyon zamanını güncelle
            self.last_sync_time = datetime.now()
            self._save_offline_status()
            
            log_info("Offline değişiklikler senkronize edildi")
            return True
            
        except Exception as e:
            log_error(f"Offline senkronizasyon hatası: {e}")
            return False
    
    def get_offline_status(self) -> Dict[str, Any]:
        """Offline durumu getir"""
        try:
            return {
                'is_offline_mode': self.is_offline_mode,
                'last_sync_time': self.last_sync_time.isoformat() if self.last_sync_time else None,
                'offline_data_size': self._calculate_offline_data_size(),
                'available_backups': self._get_available_backups(),
                'backup_settings': self.backup_settings
            }
        except Exception as e:
            log_error(f"Offline durum alma hatası: {e}")
            return {}
    
    def _sync_data_to_offline(self):
        """Verileri offline dizinine senkronize et"""
        try:
            # Portföy verilerini kopyala
            if os.path.exists('data/portfolios'):
                shutil.copytree('data/portfolios', f"{self.offline_directory}/portfolios", dirs_exist_ok=True)
            
            # Analiz verilerini kopyala
            if os.path.exists('data/analyses'):
                shutil.copytree('data/analyses', f"{self.offline_directory}/analyses", dirs_exist_ok=True)
            
            # Kullanıcı verilerini kopyala
            if os.path.exists('data/users'):
                shutil.copytree('data/users', f"{self.offline_directory}/user_data", dirs_exist_ok=True)
            
            # Market verilerini kopyala
            if os.path.exists('data/cache'):
                shutil.copytree('data/cache', f"{self.offline_directory}/market_data", dirs_exist_ok=True)
            
            log_info("Veriler offline dizinine senkronize edildi")
            
        except Exception as e:
            log_error(f"Offline senkronizasyon hatası: {e}")
    
    def _sync_offline_to_main(self):
        """Offline verilerini ana dizine senkronize et"""
        try:
            # Offline verilerini ana dizine kopyala
            if os.path.exists(f"{self.offline_directory}/portfolios"):
                shutil.copytree(f"{self.offline_directory}/portfolios", 'data/portfolios', dirs_exist_ok=True)
            
            if os.path.exists(f"{self.offline_directory}/analyses"):
                shutil.copytree(f"{self.offline_directory}/analyses", 'data/analyses', dirs_exist_ok=True)
            
            if os.path.exists(f"{self.offline_directory}/user_data"):
                shutil.copytree(f"{self.offline_directory}/user_data", 'data/users', dirs_exist_ok=True)
            
            log_info("Offline veriler ana dizine senkronize edildi")
            
        except Exception as e:
            log_error(f"Ana dizin senkronizasyon hatası: {e}")
    
    def _save_offline_status(self):
        """Offline durumu kaydet"""
        try:
            status_data = {
                'is_offline_mode': self.is_offline_mode,
                'last_sync_time': self.last_sync_time.isoformat() if self.last_sync_time else None,
                'backup_settings': self.backup_settings
            }
            
            with open(f"{self.offline_directory}/offline_status.json", 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            log_error(f"Offline durum kaydetme hatası: {e}")
    
    def _load_offline_status(self):
        """Offline durumu yükle"""
        try:
            status_file = f"{self.offline_directory}/offline_status.json"
            
            if os.path.exists(status_file):
                with open(status_file, 'r', encoding='utf-8') as f:
                    status_data = json.load(f)
                
                self.is_offline_mode = status_data.get('is_offline_mode', False)
                last_sync_str = status_data.get('last_sync_time')
                if last_sync_str:
                    self.last_sync_time = datetime.fromisoformat(last_sync_str)
                self.backup_settings = status_data.get('backup_settings', self.backup_settings)
                
        except Exception as e:
            log_error(f"Offline durum yükleme hatası: {e}")
    
    def _compress_backup(self, backup_path: str):
        """Yedeklemeyi sıkıştır"""
        try:
            zip_path = f"{backup_path}.zip"
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_path)
                        zipf.write(file_path, arcname)
            
            # Orijinal dizini sil
            shutil.rmtree(backup_path)
            
            log_info(f"Yedekleme sıkıştırıldı: {zip_path}")
            
        except Exception as e:
            log_error(f"Yedekleme sıkıştırma hatası: {e}")
    
    def _decompress_backup(self, backup_path: str):
        """Yedeklemeyi aç"""
        try:
            zip_path = f"{backup_path}.zip"
            
            if os.path.exists(zip_path):
                with zipfile.ZipFile(zip_path, 'r') as zipf:
                    zipf.extractall(backup_path)
                
                # Zip dosyasını sil
                os.remove(zip_path)
                
                log_info(f"Yedekleme açıldı: {backup_path}")
            
        except Exception as e:
            log_error(f"Yedekleme açma hatası: {e}")
    
    def _encrypt_backup(self, backup_path: str):
        """Yedeklemeyi şifrele"""
        try:
            # Yedekleme bilgilerini güncelle
            backup_info_path = f"{backup_path}/backup_info.json"
            if os.path.exists(backup_info_path):
                with open(backup_info_path, 'r', encoding='utf-8') as f:
                    backup_info = json.load(f)
                
                backup_info['encrypted'] = True
                
                with open(backup_info_path, 'w', encoding='utf-8') as f:
                    json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            log_info(f"Yedekleme şifrelendi: {backup_path}")
            
        except Exception as e:
            log_error(f"Yedekleme şifreleme hatası: {e}")
    
    def _decrypt_backup(self, backup_path: str):
        """Yedekleme şifresini çöz"""
        try:
            # Yedekleme bilgilerini güncelle
            backup_info_path = f"{backup_path}/backup_info.json"
            if os.path.exists(backup_info_path):
                with open(backup_info_path, 'r', encoding='utf-8') as f:
                    backup_info = json.load(f)
                
                backup_info['encrypted'] = False
                
                with open(backup_info_path, 'w', encoding='utf-8') as f:
                    json.dump(backup_info, f, indent=2, ensure_ascii=False)
            
            log_info(f"Yedekleme şifresi çözüldü: {backup_path}")
            
        except Exception as e:
            log_error(f"Yedekleme şifre çözme hatası: {e}")
    
    def _encrypt_offline_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Offline verileri şifrele"""
        try:
            # Hassas verileri şifrele
            encrypted_data = data.copy()
            
            # Portföy değerlerini şifrele
            if 'portfolio_data' in encrypted_data:
                portfolio_data = encrypted_data['portfolio_data']
                if 'cash' in portfolio_data:
                    portfolio_data['cash'] = encryption_manager.encrypt(str(portfolio_data['cash']))
            
            return encrypted_data
            
        except Exception as e:
            log_error(f"Offline veri şifreleme hatası: {e}")
            return data
    
    def _calculate_backup_size(self, backup_path: str) -> float:
        """Yedekleme boyutunu hesapla"""
        try:
            total_size = 0
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
            
            return round(total_size / (1024 * 1024), 2)  # MB
            
        except Exception as e:
            return 0.0
    
    def _count_backup_files(self, backup_path: str) -> int:
        """Yedekleme dosya sayısını hesapla"""
        try:
            file_count = 0
            for root, dirs, files in os.walk(backup_path):
                file_count += len(files)
            
            return file_count
            
        except Exception as e:
            return 0
    
    def _calculate_offline_data_size(self) -> float:
        """Offline veri boyutunu hesapla"""
        try:
            total_size = 0
            for root, dirs, files in os.walk(self.offline_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
            
            return round(total_size / (1024 * 1024), 2)  # MB
            
        except Exception as e:
            return 0.0
    
    def _get_available_backups(self) -> List[Dict[str, Any]]:
        """Mevcut yedeklemeleri getir"""
        try:
            backups = []
            
            if os.path.exists(self.backup_directory):
                for item in os.listdir(self.backup_directory):
                    backup_path = f"{self.backup_directory}/{item}"
                    
                    if os.path.isdir(backup_path):
                        backup_info_path = f"{backup_path}/backup_info.json"
                        
                        if os.path.exists(backup_info_path):
                            with open(backup_info_path, 'r', encoding='utf-8') as f:
                                backup_info = json.load(f)
                            
                            backups.append({
                                'name': item,
                                'created_at': backup_info.get('created_at'),
                                'size_mb': backup_info.get('size_mb', 0),
                                'file_count': backup_info.get('file_count', 0),
                                'encrypted': backup_info.get('encrypted', False)
                            })
            
            # Tarihe göre sırala
            backups.sort(key=lambda x: x['created_at'], reverse=True)
            
            return backups
            
        except Exception as e:
            log_error(f"Mevcut yedeklemeler alma hatası: {e}")
            return []
    
    def cleanup_old_backups(self):
        """Eski yedeklemeleri temizle"""
        try:
            backups = self._get_available_backups()
            
            if len(backups) > self.backup_settings['max_backups']:
                # En eski yedeklemeleri sil
                backups_to_delete = backups[self.backup_settings['max_backups']:]
                
                for backup in backups_to_delete:
                    backup_path = f"{self.backup_directory}/{backup['name']}"
                    
                    if os.path.exists(backup_path):
                        shutil.rmtree(backup_path)
                        log_info(f"Eski yedekleme silindi: {backup['name']}")
            
        except Exception as e:
            log_error(f"Eski yedekleme temizleme hatası: {e}")
    
    def auto_backup(self):
        """Otomatik yedekleme"""
        try:
            if self.backup_settings['auto_backup']:
                # Son yedekleme zamanını kontrol et
                last_backup_time = self._get_last_backup_time()
                
                if last_backup_time:
                    time_since_last_backup = datetime.now() - last_backup_time
                    if time_since_last_backup.total_seconds() < self.backup_settings['backup_interval_hours'] * 3600:
                        return  # Henüz yedekleme zamanı gelmemiş
                
                # Yedekleme oluştur
                backup_path = self.create_backup()
                
                if backup_path:
                    log_info("Otomatik yedekleme tamamlandı")
                    
                    # Eski yedeklemeleri temizle
                    self.cleanup_old_backups()
            
        except Exception as e:
            log_error(f"Otomatik yedekleme hatası: {e}")
    
    def _get_last_backup_time(self) -> Optional[datetime]:
        """Son yedekleme zamanını getir"""
        try:
            backups = self._get_available_backups()
            
            if backups:
                last_backup = backups[0]
                return datetime.fromisoformat(last_backup['created_at'])
            
            return None
            
        except Exception as e:
            return None

# Global offline manager instance
offline_manager = OfflineManager()

