"""
PlanB Motoru - Watchlist Manager
İzleme listeleri yönetimi
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug

class WatchlistManager:
    """İzleme listesi yöneticisi"""
    
    def __init__(self):
        self.watchlists_file = "data/watchlists/watchlists.json"
        self._ensure_watchlist_directory()
        self._load_watchlists()
    
    def _ensure_watchlist_directory(self):
        """İzleme listesi dizinini oluştur"""
        os.makedirs("data/watchlists", exist_ok=True)
    
    def _load_watchlists(self):
        """İzleme listelerini yükle"""
        try:
            if os.path.exists(self.watchlists_file):
                with open(self.watchlists_file, 'r', encoding='utf-8') as f:
                    self.watchlists = json.load(f)
            else:
                self.watchlists = {}
                self._create_default_watchlists()
            log_info(f"{len(self.watchlists)} izleme listesi yüklendi")
        except Exception as e:
            log_error(f"İzleme listesi yükleme hatası: {e}")
            self.watchlists = {}
    
    def _create_default_watchlists(self):
        """Varsayılan izleme listelerini oluştur"""
        try:
            default_watchlists = {
                'bist_blue_chips': {
                    'name': 'BIST Mavi Çiplar',
                    'description': 'BIST 100\'deki büyük şirketler',
                    'symbols': ['THYAO.IS', 'AKBNK.IS', 'GARAN.IS', 'ISCTR.IS', 'SAHOL.IS', 'TUPRS.IS', 'KRDMD.IS', 'SASA.IS'],
                    'market': 'bist',
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat(),
                    'is_public': True,
                    'tags': ['bist', 'blue-chip', 'large-cap']
                },
                'tech_stocks': {
                    'name': 'Teknoloji Hisseleri',
                    'description': 'Teknoloji sektörü hisseleri',
                    'symbols': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'NFLX'],
                    'market': 'nasdaq',
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat(),
                    'is_public': True,
                    'tags': ['technology', 'nasdaq', 'growth']
                },
                'crypto_majors': {
                    'name': 'Kripto Majörler',
                    'description': 'Büyük kripto para birimleri',
                    'symbols': ['BTC', 'ETH', 'ADA', 'DOT', 'SOL', 'AVAX', 'MATIC', 'ATOM'],
                    'market': 'crypto',
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat(),
                    'is_public': True,
                    'tags': ['crypto', 'major', 'blockchain']
                },
                'dividend_stocks': {
                    'name': 'Temettü Hisseleri',
                    'description': 'Yüksek temettü veren hisseler',
                    'symbols': ['JNJ', 'PG', 'KO', 'PEP', 'WMT', 'HD', 'MCD', 'NKE'],
                    'market': 'nasdaq',
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat(),
                    'is_public': True,
                    'tags': ['dividend', 'income', 'stable']
                }
            }
            
            self.watchlists = default_watchlists
            self._save_watchlists()
            log_info("Varsayılan izleme listeleri oluşturuldu")
            
        except Exception as e:
            log_error(f"Varsayılan izleme listesi oluşturma hatası: {e}")
    
    def create_watchlist(self, name: str, description: str = "", symbols: List[str] = None, 
                        market: str = 'bist', tags: List[str] = None, is_public: bool = True) -> str:
        """Yeni izleme listesi oluştur"""
        try:
            # İzleme listesi ID oluştur
            watchlist_id = self._generate_watchlist_id(name)
            
            # Yeni izleme listesi
            new_watchlist = {
                'watchlist_id': watchlist_id,
                'name': name,
                'description': description,
                'symbols': symbols or [],
                'market': market,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_public': is_public,
                'tags': tags or [],
                'user_id': 'default_user',  # Kişisel kullanım için
                'view_count': 0,
                'favorite_count': 0
            }
            
            self.watchlists[watchlist_id] = new_watchlist
            self._save_watchlists()
            
            log_info(f"Yeni izleme listesi oluşturuldu: {name}")
            return watchlist_id
            
        except Exception as e:
            log_error(f"İzleme listesi oluşturma hatası: {e}")
            return ""
    
    def get_watchlist(self, watchlist_id: str) -> Optional[Dict[str, Any]]:
        """İzleme listesi getir"""
        try:
            return self.watchlists.get(watchlist_id)
        except Exception as e:
            log_error(f"İzleme listesi alma hatası: {e}")
            return None
    
    def get_all_watchlists(self, market: str = None, tags: List[str] = None) -> List[Dict[str, Any]]:
        """Tüm izleme listelerini getir"""
        try:
            watchlists_list = []
            
            for watchlist_id, watchlist_data in self.watchlists.items():
                # Market filtresi
                if market and watchlist_data.get('market') != market:
                    continue
                
                # Tag filtresi
                if tags:
                    watchlist_tags = watchlist_data.get('tags', [])
                    if not any(tag in watchlist_tags for tag in tags):
                        continue
                
                # Güvenli veri döndür
                safe_watchlist = {
                    'watchlist_id': watchlist_data['watchlist_id'],
                    'name': watchlist_data['name'],
                    'description': watchlist_data['description'],
                    'symbols': watchlist_data['symbols'],
                    'market': watchlist_data['market'],
                    'created_at': watchlist_data['created_at'],
                    'updated_at': watchlist_data['updated_at'],
                    'is_public': watchlist_data['is_public'],
                    'tags': watchlist_data['tags'],
                    'symbol_count': len(watchlist_data['symbols']),
                    'view_count': watchlist_data.get('view_count', 0),
                    'favorite_count': watchlist_data.get('favorite_count', 0)
                }
                
                watchlists_list.append(safe_watchlist)
            
            return watchlists_list
            
        except Exception as e:
            log_error(f"İzleme listesi listesi alma hatası: {e}")
            return []
    
    def update_watchlist(self, watchlist_id: str, update_data: Dict[str, Any]) -> bool:
        """İzleme listesini güncelle"""
        try:
            if watchlist_id not in self.watchlists:
                log_error(f"İzleme listesi bulunamadı: {watchlist_id}")
                return False
            
            # Güncellenebilir alanlar
            allowed_fields = ['name', 'description', 'symbols', 'market', 'tags', 'is_public']
            
            for field, value in update_data.items():
                if field in allowed_fields:
                    self.watchlists[watchlist_id][field] = value
            
            self.watchlists[watchlist_id]['updated_at'] = datetime.now().isoformat()
            self._save_watchlists()
            
            log_info(f"İzleme listesi güncellendi: {watchlist_id}")
            return True
            
        except Exception as e:
            log_error(f"İzleme listesi güncelleme hatası: {e}")
            return False
    
    def add_symbol_to_watchlist(self, watchlist_id: str, symbol: str) -> bool:
        """İzleme listesine sembol ekle"""
        try:
            if watchlist_id not in self.watchlists:
                log_error(f"İzleme listesi bulunamadı: {watchlist_id}")
                return False
            
            watchlist = self.watchlists[watchlist_id]
            
            # Sembol zaten var mı kontrol et
            if symbol in watchlist['symbols']:
                log_error(f"Sembol zaten listede: {symbol}")
                return False
            
            # Sembol ekle
            watchlist['symbols'].append(symbol)
            watchlist['updated_at'] = datetime.now().isoformat()
            
            self._save_watchlists()
            
            log_info(f"Sembol eklendi: {symbol} -> {watchlist_id}")
            return True
            
        except Exception as e:
            log_error(f"Sembol ekleme hatası: {e}")
            return False
    
    def remove_symbol_from_watchlist(self, watchlist_id: str, symbol: str) -> bool:
        """İzleme listesinden sembol çıkar"""
        try:
            if watchlist_id not in self.watchlists:
                log_error(f"İzleme listesi bulunamadı: {watchlist_id}")
                return False
            
            watchlist = self.watchlists[watchlist_id]
            
            # Sembol var mı kontrol et
            if symbol not in watchlist['symbols']:
                log_error(f"Sembol listede yok: {symbol}")
                return False
            
            # Sembol çıkar
            watchlist['symbols'].remove(symbol)
            watchlist['updated_at'] = datetime.now().isoformat()
            
            self._save_watchlists()
            
            log_info(f"Sembol çıkarıldı: {symbol} -> {watchlist_id}")
            return True
            
        except Exception as e:
            log_error(f"Sembol çıkarma hatası: {e}")
            return False
    
    def delete_watchlist(self, watchlist_id: str) -> bool:
        """İzleme listesini sil"""
        try:
            if watchlist_id not in self.watchlists:
                log_error(f"İzleme listesi bulunamadı: {watchlist_id}")
                return False
            
            # İzleme listesini sil
            del self.watchlists[watchlist_id]
            self._save_watchlists()
            
            log_info(f"İzleme listesi silindi: {watchlist_id}")
            return True
            
        except Exception as e:
            log_error(f"İzleme listesi silme hatası: {e}")
            return False
    
    def get_watchlist_performance(self, watchlist_id: str) -> Dict[str, Any]:
        """İzleme listesi performansı"""
        try:
            watchlist = self.get_watchlist(watchlist_id)
            if not watchlist:
                return {}
            
            # Simüle edilmiş performans verileri
            symbols = watchlist['symbols']
            performance_data = []
            
            for symbol in symbols:
                # Simüle edilmiş performans
                import numpy as np
                price = np.random.uniform(10, 1000)
                change = np.random.uniform(-10, 10)
                volume = np.random.uniform(1000000, 10000000)
                
                performance_data.append({
                    'symbol': symbol,
                    'price': price,
                    'change': change,
                    'change_pct': change,
                    'volume': volume,
                    'market_cap': price * volume * 0.1
                })
            
            # Toplam performans
            total_change = np.mean([data['change_pct'] for data in performance_data])
            best_performer = max(performance_data, key=lambda x: x['change_pct'])
            worst_performer = min(performance_data, key=lambda x: x['change_pct'])
            
            return {
                'watchlist_id': watchlist_id,
                'watchlist_name': watchlist['name'],
                'total_symbols': len(symbols),
                'average_change': total_change,
                'best_performer': best_performer,
                'worst_performer': worst_performer,
                'performance_data': performance_data,
                'updated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            log_error(f"İzleme listesi performans alma hatası: {e}")
            return {}
    
    def search_watchlists(self, query: str) -> List[Dict[str, Any]]:
        """İzleme listelerinde arama"""
        try:
            query_lower = query.lower()
            matching_watchlists = []
            
            for watchlist_id, watchlist_data in self.watchlists.items():
                # Arama kriterleri
                name_match = query_lower in watchlist_data['name'].lower()
                description_match = query_lower in watchlist_data.get('description', '').lower()
                tag_match = any(query_lower in tag.lower() for tag in watchlist_data.get('tags', []))
                symbol_match = any(query_lower in symbol.lower() for symbol in watchlist_data['symbols'])
                
                if name_match or description_match or tag_match or symbol_match:
                    safe_watchlist = {
                        'watchlist_id': watchlist_data['watchlist_id'],
                        'name': watchlist_data['name'],
                        'description': watchlist_data['description'],
                        'symbols': watchlist_data['symbols'],
                        'market': watchlist_data['market'],
                        'tags': watchlist_data['tags'],
                        'symbol_count': len(watchlist_data['symbols']),
                        'match_type': 'name' if name_match else ('description' if description_match else ('tag' if tag_match else 'symbol'))
                    }
                    matching_watchlists.append(safe_watchlist)
            
            return matching_watchlists
            
        except Exception as e:
            log_error(f"İzleme listesi arama hatası: {e}")
            return []
    
    def get_popular_watchlists(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Popüler izleme listeleri"""
        try:
            # Görüntülenme sayısına göre sırala
            popular_watchlists = sorted(
                self.watchlists.items(),
                key=lambda x: x[1].get('view_count', 0),
                reverse=True
            )[:limit]
            
            result = []
            for watchlist_id, watchlist_data in popular_watchlists:
                safe_watchlist = {
                    'watchlist_id': watchlist_data['watchlist_id'],
                    'name': watchlist_data['name'],
                    'description': watchlist_data['description'],
                    'market': watchlist_data['market'],
                    'tags': watchlist_data['tags'],
                    'symbol_count': len(watchlist_data['symbols']),
                    'view_count': watchlist_data.get('view_count', 0),
                    'favorite_count': watchlist_data.get('favorite_count', 0)
                }
                result.append(safe_watchlist)
            
            return result
            
        except Exception as e:
            log_error(f"Popüler izleme listesi alma hatası: {e}")
            return []
    
    def increment_view_count(self, watchlist_id: str) -> bool:
        """Görüntülenme sayısını artır"""
        try:
            if watchlist_id in self.watchlists:
                self.watchlists[watchlist_id]['view_count'] = self.watchlists[watchlist_id].get('view_count', 0) + 1
                self._save_watchlists()
                return True
            return False
        except Exception as e:
            log_error(f"Görüntülenme sayısı artırma hatası: {e}")
            return False
    
    def get_watchlist_statistics(self) -> Dict[str, Any]:
        """İzleme listesi istatistikleri"""
        try:
            total_watchlists = len(self.watchlists)
            public_watchlists = len([w for w in self.watchlists.values() if w.get('is_public', True)])
            private_watchlists = total_watchlists - public_watchlists
            
            # Market dağılımı
            market_distribution = {}
            for watchlist in self.watchlists.values():
                market = watchlist.get('market', 'unknown')
                market_distribution[market] = market_distribution.get(market, 0) + 1
            
            # Tag dağılımı
            tag_distribution = {}
            for watchlist in self.watchlists.values():
                for tag in watchlist.get('tags', []):
                    tag_distribution[tag] = tag_distribution.get(tag, 0) + 1
            
            # Toplam sembol sayısı
            total_symbols = sum(len(watchlist['symbols']) for watchlist in self.watchlists.values())
            
            # En popüler taglar
            popular_tags = sorted(tag_distribution.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                'total_watchlists': total_watchlists,
                'public_watchlists': public_watchlists,
                'private_watchlists': private_watchlists,
                'total_symbols': total_symbols,
                'average_symbols_per_watchlist': total_symbols / total_watchlists if total_watchlists > 0 else 0,
                'market_distribution': market_distribution,
                'popular_tags': popular_tags,
                'total_views': sum(w.get('view_count', 0) for w in self.watchlists.values()),
                'total_favorites': sum(w.get('favorite_count', 0) for w in self.watchlists.values())
            }
            
        except Exception as e:
            log_error(f"İzleme listesi istatistikleri alma hatası: {e}")
            return {}
    
    def export_watchlist(self, watchlist_id: str, format: str = 'json') -> Optional[str]:
        """İzleme listesini dışa aktar"""
        try:
            watchlist = self.get_watchlist(watchlist_id)
            if not watchlist:
                return None
            
            export_data = {
                'watchlist': watchlist,
                'exported_at': datetime.now().isoformat(),
                'export_format': format,
                'version': '1.0'
            }
            
            if format.lower() == 'json':
                filename = f"data/watchlists/export_{watchlist_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                log_info(f"İzleme listesi dışa aktarıldı: {filename}")
                return filename
            
            return None
            
        except Exception as e:
            log_error(f"İzleme listesi dışa aktarma hatası: {e}")
            return None
    
    def import_watchlist(self, import_data: Dict[str, Any]) -> bool:
        """İzleme listesini içe aktar"""
        try:
            if 'watchlist' not in import_data:
                log_error("Geçersiz import verisi")
                return False
            
            watchlist_data = import_data['watchlist']
            
            # Gerekli alanları kontrol et
            required_fields = ['name', 'symbols', 'market']
            for field in required_fields:
                if field not in watchlist_data:
                    log_error(f"Eksik alan: {field}")
                    return False
            
            # Yeni izleme listesi oluştur
            watchlist_id = self.create_watchlist(
                name=watchlist_data['name'],
                description=watchlist_data.get('description', ''),
                symbols=watchlist_data['symbols'],
                market=watchlist_data['market'],
                tags=watchlist_data.get('tags', []),
                is_public=watchlist_data.get('is_public', True)
            )
            
            if watchlist_id:
                log_info(f"İzleme listesi içe aktarıldı: {watchlist_id}")
                return True
            
            return False
            
        except Exception as e:
            log_error(f"İzleme listesi içe aktarma hatası: {e}")
            return False
    
    def _generate_watchlist_id(self, name: str) -> str:
        """İzleme listesi ID oluştur"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"{name.lower().replace(' ', '_')}_{timestamp}"
    
    def _save_watchlists(self):
        """İzleme listelerini kaydet"""
        try:
            with open(self.watchlists_file, 'w', encoding='utf-8') as f:
                json.dump(self.watchlists, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"İzleme listesi kaydetme hatası: {e}")

# Global watchlist manager instance
watchlist_manager = WatchlistManager()

