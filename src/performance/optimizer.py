"""
PlanB Motoru - Performance Optimizer
Performans optimizasyonu ve cache yönetimi
"""
import time
import json
import os
import threading
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from functools import wraps
from src.utils.logger import log_info, log_error, log_debug

class PerformanceOptimizer:
    """Performans optimizasyonu yöneticisi"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = {}
        self.performance_metrics = {}
        self.cache_directory = "data/cache"
        self.metrics_file = "data/performance/metrics.json"
        self._ensure_directories()
        self._load_metrics()
        self.cache_lock = threading.Lock()
    
    def _ensure_directories(self):
        """Gerekli dizinleri oluştur"""
        os.makedirs(self.cache_directory, exist_ok=True)
        os.makedirs("data/performance", exist_ok=True)
    
    def _load_metrics(self):
        """Performans metriklerini yükle"""
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    self.performance_metrics = json.load(f)
            else:
                self.performance_metrics = {}
            log_info("Performans metrikleri yüklendi")
        except Exception as e:
            log_error(f"Performans metrikleri yükleme hatası: {e}")
            self.performance_metrics = {}
    
    def cache_result(self, key: str, value: Any, ttl_seconds: int = 300):
        """Sonucu cache'e kaydet"""
        try:
            with self.cache_lock:
                self.cache[key] = value
                self.cache_ttl[key] = datetime.now() + timedelta(seconds=ttl_seconds)
            
            log_debug(f"Cache'e kaydedildi: {key} (TTL: {ttl_seconds}s)")
            
        except Exception as e:
            log_error(f"Cache kaydetme hatası: {e}")
    
    def get_cached_result(self, key: str) -> Optional[Any]:
        """Cache'den sonuç al"""
        try:
            with self.cache_lock:
                if key in self.cache:
                    # TTL kontrolü
                    if datetime.now() < self.cache_ttl[key]:
                        log_debug(f"Cache'den alındı: {key}")
                        return self.cache[key]
                    else:
                        # Süresi dolmuş, cache'den sil
                        del self.cache[key]
                        del self.cache_ttl[key]
                        log_debug(f"Cache süresi doldu: {key}")
            
            return None
            
        except Exception as e:
            log_error(f"Cache alma hatası: {e}")
            return None
    
    def clear_cache(self, key: str = None):
        """Cache'i temizle"""
        try:
            with self.cache_lock:
                if key:
                    if key in self.cache:
                        del self.cache[key]
                        del self.cache_ttl[key]
                        log_info(f"Cache temizlendi: {key}")
                else:
                    self.cache.clear()
                    self.cache_ttl.clear()
                    log_info("Tüm cache temizlendi")
                    
        except Exception as e:
            log_error(f"Cache temizleme hatası: {e}")
    
    def cached(self, ttl_seconds: int = 300, key_prefix: str = ""):
        """Cache decorator"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Cache key oluştur
                cache_key = f"{key_prefix}{func.__name__}_{hash(str(args) + str(kwargs))}"
                
                # Cache'den kontrol et
                cached_result = self.get_cached_result(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Fonksiyonu çalıştır
                start_time = time.time()
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Sonucu cache'e kaydet
                self.cache_result(cache_key, result, ttl_seconds)
                
                # Performans metriklerini kaydet
                self._record_performance_metric(func.__name__, execution_time)
                
                return result
            
            return wrapper
        return decorator
    
    def measure_performance(self, func_name: str = None):
        """Performans ölçüm decorator"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                name = func_name or func.__name__
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self._record_performance_metric(name, execution_time, success=True)
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self._record_performance_metric(name, execution_time, success=False, error=str(e))
                    raise
            
            return wrapper
        return decorator
    
    def _record_performance_metric(self, func_name: str, execution_time: float, success: bool = True, error: str = None):
        """Performans metriği kaydet"""
        try:
            if func_name not in self.performance_metrics:
                self.performance_metrics[func_name] = {
                    'total_calls': 0,
                    'total_time': 0,
                    'average_time': 0,
                    'min_time': float('inf'),
                    'max_time': 0,
                    'success_count': 0,
                    'error_count': 0,
                    'last_called': None,
                    'errors': []
                }
            
            metric = self.performance_metrics[func_name]
            metric['total_calls'] += 1
            metric['total_time'] += execution_time
            metric['average_time'] = metric['total_time'] / metric['total_calls']
            metric['min_time'] = min(metric['min_time'], execution_time)
            metric['max_time'] = max(metric['max_time'], execution_time)
            metric['last_called'] = datetime.now().isoformat()
            
            if success:
                metric['success_count'] += 1
            else:
                metric['error_count'] += 1
                if error:
                    metric['errors'].append({
                        'error': error,
                        'timestamp': datetime.now().isoformat()
                    })
                    # Son 10 hatayı tut
                    metric['errors'] = metric['errors'][-10:]
            
            # Metrikleri kaydet
            self._save_metrics()
            
        except Exception as e:
            log_error(f"Performans metriği kaydetme hatası: {e}")
    
    def get_performance_metrics(self, func_name: str = None) -> Dict[str, Any]:
        """Performans metriklerini getir"""
        try:
            if func_name:
                return self.performance_metrics.get(func_name, {})
            else:
                return self.performance_metrics
        except Exception as e:
            log_error(f"Performans metrikleri alma hatası: {e}")
            return {}
    
    def get_slowest_functions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """En yavaş fonksiyonları getir"""
        try:
            slowest = []
            
            for func_name, metrics in self.performance_metrics.items():
                if metrics['total_calls'] > 0:
                    slowest.append({
                        'function': func_name,
                        'average_time': metrics['average_time'],
                        'total_calls': metrics['total_calls'],
                        'total_time': metrics['total_time'],
                        'max_time': metrics['max_time'],
                        'success_rate': metrics['success_count'] / metrics['total_calls'] * 100
                    })
            
            # Ortalama süreye göre sırala
            slowest.sort(key=lambda x: x['average_time'], reverse=True)
            
            return slowest[:limit]
            
        except Exception as e:
            log_error(f"En yavaş fonksiyonlar alma hatası: {e}")
            return []
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """Cache istatistikleri"""
        try:
            with self.cache_lock:
                total_entries = len(self.cache)
                expired_entries = 0
                current_time = datetime.now()
                
                for key, expiry_time in self.cache_ttl.items():
                    if current_time >= expiry_time:
                        expired_entries += 1
                
                return {
                    'total_entries': total_entries,
                    'active_entries': total_entries - expired_entries,
                    'expired_entries': expired_entries,
                    'cache_hit_rate': self._calculate_cache_hit_rate(),
                    'memory_usage_estimate': total_entries * 1024  # Basit tahmin
                }
                
        except Exception as e:
            log_error(f"Cache istatistikleri alma hatası: {e}")
            return {}
    
    def _calculate_cache_hit_rate(self) -> float:
        """Cache hit rate hesapla"""
        try:
            # Basit cache hit rate hesaplama
            # Gerçek uygulamada daha detaylı tracking gerekli
            total_requests = sum(metric['total_calls'] for metric in self.performance_metrics.values())
            cache_hits = len(self.cache)
            
            if total_requests > 0:
                return (cache_hits / total_requests) * 100
            return 0.0
            
        except Exception as e:
            return 0.0
    
    def optimize_data_loading(self, data_loader_func: Callable, cache_key: str, ttl_seconds: int = 600) -> Any:
        """Veri yükleme optimizasyonu"""
        try:
            # Cache'den kontrol et
            cached_data = self.get_cached_result(cache_key)
            if cached_data is not None:
                return cached_data
            
            # Veriyi yükle
            start_time = time.time()
            data = data_loader_func()
            loading_time = time.time() - start_time
            
            # Cache'e kaydet
            self.cache_result(cache_key, data, ttl_seconds)
            
            # Performans metriği kaydet
            self._record_performance_metric(f"data_loading_{cache_key}", loading_time)
            
            log_info(f"Veri yüklendi: {cache_key} ({loading_time:.2f}s)")
            return data
            
        except Exception as e:
            log_error(f"Veri yükleme optimizasyonu hatası: {e}")
            return None
    
    def batch_process(self, items: List[Any], process_func: Callable, batch_size: int = 10, 
                     delay_between_batches: float = 0.1) -> List[Any]:
        """Toplu işlem optimizasyonu"""
        try:
            results = []
            total_items = len(items)
            
            for i in range(0, total_items, batch_size):
                batch = items[i:i + batch_size]
                
                # Batch'i işle
                start_time = time.time()
                batch_results = process_func(batch)
                batch_time = time.time() - start_time
                
                results.extend(batch_results)
                
                # Performans metriği kaydet
                self._record_performance_metric(f"batch_process_{process_func.__name__}", batch_time)
                
                log_debug(f"Batch işlendi: {i//batch_size + 1}/{(total_items + batch_size - 1)//batch_size} ({batch_time:.2f}s)")
                
                # Batch'ler arası gecikme
                if i + batch_size < total_items and delay_between_batches > 0:
                    time.sleep(delay_between_batches)
            
            return results
            
        except Exception as e:
            log_error(f"Toplu işlem optimizasyonu hatası: {e}")
            return []
    
    def parallel_process(self, items: List[Any], process_func: Callable, max_workers: int = 4) -> List[Any]:
        """Paralel işlem optimizasyonu"""
        try:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            
            results = []
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Tüm görevleri başlat
                future_to_item = {executor.submit(process_func, item): item for item in items}
                
                # Sonuçları topla
                for future in as_completed(future_to_item):
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        log_error(f"Paralel işlem hatası: {e}")
                        results.append(None)
            
            return results
            
        except Exception as e:
            log_error(f"Paralel işlem optimizasyonu hatası: {e}")
            return []
    
    def memory_optimization(self):
        """Bellek optimizasyonu"""
        try:
            import gc
            
            # Garbage collection
            collected = gc.collect()
            
            # Süresi dolmuş cache'leri temizle
            current_time = datetime.now()
            expired_keys = []
            
            with self.cache_lock:
                for key, expiry_time in self.cache_ttl.items():
                    if current_time >= expiry_time:
                        expired_keys.append(key)
                
                for key in expired_keys:
                    if key in self.cache:
                        del self.cache[key]
                        del self.cache_ttl[key]
            
            log_info(f"Bellek optimizasyonu: {collected} obje temizlendi, {len(expired_keys)} cache girişi silindi")
            
        except Exception as e:
            log_error(f"Bellek optimizasyonu hatası: {e}")
    
    def get_system_performance(self) -> Dict[str, Any]:
        """Sistem performans bilgileri"""
        try:
            import psutil
            
            # CPU kullanımı
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Bellek kullanımı
            memory = psutil.virtual_memory()
            
            # Disk kullanımı
            disk = psutil.disk_usage('/')
            
            # Ağ istatistikleri
            network = psutil.net_io_counters()
            
            return {
                'cpu_percent': cpu_percent,
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used,
                    'percent': memory.percent
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except ImportError:
            log_error("psutil kütüphanesi bulunamadı")
            return {}
        except Exception as e:
            log_error(f"Sistem performans bilgisi alma hatası: {e}")
            return {}
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Performans raporu oluştur"""
        try:
            # Performans metrikleri
            performance_metrics = self.get_performance_metrics()
            
            # En yavaş fonksiyonlar
            slowest_functions = self.get_slowest_functions(10)
            
            # Cache istatistikleri
            cache_stats = self.get_cache_statistics()
            
            # Sistem performansı
            system_performance = self.get_system_performance()
            
            # Genel istatistikler
            total_functions = len(performance_metrics)
            total_calls = sum(metric['total_calls'] for metric in performance_metrics.values())
            total_time = sum(metric['total_time'] for metric in performance_metrics.values())
            total_errors = sum(metric['error_count'] for metric in performance_metrics.values())
            
            return {
                'report_generated_at': datetime.now().isoformat(),
                'summary': {
                    'total_functions': total_functions,
                    'total_calls': total_calls,
                    'total_execution_time': total_time,
                    'average_execution_time': total_time / total_calls if total_calls > 0 else 0,
                    'total_errors': total_errors,
                    'error_rate': (total_errors / total_calls * 100) if total_calls > 0 else 0
                },
                'slowest_functions': slowest_functions,
                'cache_statistics': cache_stats,
                'system_performance': system_performance,
                'recommendations': self._generate_recommendations(performance_metrics, cache_stats)
            }
            
        except Exception as e:
            log_error(f"Performans raporu oluşturma hatası: {e}")
            return {}
    
    def _generate_recommendations(self, performance_metrics: Dict[str, Any], cache_stats: Dict[str, Any]) -> List[str]:
        """Performans önerileri oluştur"""
        try:
            recommendations = []
            
            # Yavaş fonksiyonlar için öneriler
            for func_name, metrics in performance_metrics.items():
                if metrics['average_time'] > 1.0:  # 1 saniyeden yavaş
                    recommendations.append(f"{func_name} fonksiyonu yavaş ({metrics['average_time']:.2f}s). Cache veya optimizasyon gerekli.")
                
                if metrics['error_count'] > 0:
                    error_rate = (metrics['error_count'] / metrics['total_calls']) * 100
                    if error_rate > 10:  # %10'dan fazla hata
                        recommendations.append(f"{func_name} fonksiyonunda yüksek hata oranı (%{error_rate:.1f}). Hata yönetimi iyileştirilmeli.")
            
            # Cache önerileri
            if cache_stats.get('cache_hit_rate', 0) < 50:
                recommendations.append("Cache hit rate düşük (%{:.1f}). Cache stratejisi gözden geçirilmeli.".format(cache_stats.get('cache_hit_rate', 0)))
            
            # Sistem performans önerileri
            system_perf = self.get_system_performance()
            if system_perf.get('cpu_percent', 0) > 80:
                recommendations.append("CPU kullanımı yüksek (%{:.1f}). İşlem yükü azaltılmalı.".format(system_perf.get('cpu_percent', 0)))
            
            if system_perf.get('memory', {}).get('percent', 0) > 80:
                recommendations.append("Bellek kullanımı yüksek (%{:.1f}). Bellek optimizasyonu gerekli.".format(system_perf.get('memory', {}).get('percent', 0)))
            
            return recommendations
            
        except Exception as e:
            log_error(f"Performans önerileri oluşturma hatası: {e}")
            return []
    
    def _save_metrics(self):
        """Metrikleri kaydet"""
        try:
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(self.performance_metrics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Metrik kaydetme hatası: {e}")
    
    def cleanup_old_metrics(self, days: int = 30):
        """Eski metrikleri temizle"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            cleaned_count = 0
            
            for func_name, metrics in list(self.performance_metrics.items()):
                last_called = metrics.get('last_called')
                if last_called:
                    last_called_date = datetime.fromisoformat(last_called)
                    if last_called_date < cutoff_date:
                        del self.performance_metrics[func_name]
                        cleaned_count += 1
            
            if cleaned_count > 0:
                self._save_metrics()
                log_info(f"{cleaned_count} eski metrik temizlendi")
            
        except Exception as e:
            log_error(f"Eski metrik temizleme hatası: {e}")

# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer()

