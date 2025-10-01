"""
PlanB Motoru - Theme Manager
Dark Mode ve custom themes yönetimi
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from src.utils.logger import log_info, log_error, log_debug

class ThemeManager:
    """Tema yöneticisi"""
    
    def __init__(self):
        self.themes = {
            'light': {
                'name': 'Açık Tema',
                'description': 'Klasik açık tema',
                'colors': {
                    'primary': '#007bff',
                    'secondary': '#6c757d',
                    'success': '#28a745',
                    'danger': '#dc3545',
                    'warning': '#ffc107',
                    'info': '#17a2b8',
                    'light': '#f8f9fa',
                    'dark': '#343a40',
                    'background': '#ffffff',
                    'surface': '#f8f9fa',
                    'text': '#212529',
                    'text_secondary': '#6c757d',
                    'border': '#dee2e6',
                    'shadow': 'rgba(0, 0, 0, 0.1)'
                },
                'fonts': {
                    'primary': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
                    'secondary': 'Roboto, sans-serif',
                    'monospace': 'Fira Code, monospace'
                },
                'spacing': {
                    'xs': '4px',
                    'sm': '8px',
                    'md': '16px',
                    'lg': '24px',
                    'xl': '32px',
                    'xxl': '48px'
                },
                'border_radius': {
                    'sm': '4px',
                    'md': '8px',
                    'lg': '12px',
                    'xl': '16px'
                }
            },
            'dark': {
                'name': 'Koyu Tema',
                'description': 'Göz dostu koyu tema',
                'colors': {
                    'primary': '#0d6efd',
                    'secondary': '#6c757d',
                    'success': '#198754',
                    'danger': '#dc3545',
                    'warning': '#fd7e14',
                    'info': '#0dcaf0',
                    'light': '#f8f9fa',
                    'dark': '#212529',
                    'background': '#0d1117',
                    'surface': '#161b22',
                    'text': '#f0f6fc',
                    'text_secondary': '#8b949e',
                    'border': '#30363d',
                    'shadow': 'rgba(0, 0, 0, 0.3)'
                },
                'fonts': {
                    'primary': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
                    'secondary': 'Roboto, sans-serif',
                    'monospace': 'Fira Code, monospace'
                },
                'spacing': {
                    'xs': '4px',
                    'sm': '8px',
                    'md': '16px',
                    'lg': '24px',
                    'xl': '32px',
                    'xxl': '48px'
                },
                'border_radius': {
                    'sm': '4px',
                    'md': '8px',
                    'lg': '12px',
                    'xl': '16px'
                }
            },
            'blue': {
                'name': 'Mavi Tema',
                'description': 'Profesyonel mavi tema',
                'colors': {
                    'primary': '#1e40af',
                    'secondary': '#64748b',
                    'success': '#059669',
                    'danger': '#dc2626',
                    'warning': '#d97706',
                    'info': '#0891b2',
                    'light': '#f1f5f9',
                    'dark': '#1e293b',
                    'background': '#ffffff',
                    'surface': '#f8fafc',
                    'text': '#1e293b',
                    'text_secondary': '#64748b',
                    'border': '#e2e8f0',
                    'shadow': 'rgba(30, 64, 175, 0.1)'
                },
                'fonts': {
                    'primary': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
                    'secondary': 'Roboto, sans-serif',
                    'monospace': 'Fira Code, monospace'
                },
                'spacing': {
                    'xs': '4px',
                    'sm': '8px',
                    'md': '16px',
                    'lg': '24px',
                    'xl': '32px',
                    'xxl': '48px'
                },
                'border_radius': {
                    'sm': '4px',
                    'md': '8px',
                    'lg': '12px',
                    'xl': '16px'
                }
            },
            'green': {
                'name': 'Yeşil Tema',
                'description': 'Doğa dostu yeşil tema',
                'colors': {
                    'primary': '#16a34a',
                    'secondary': '#6b7280',
                    'success': '#22c55e',
                    'danger': '#ef4444',
                    'warning': '#f59e0b',
                    'info': '#06b6d4',
                    'light': '#f0fdf4',
                    'dark': '#14532d',
                    'background': '#ffffff',
                    'surface': '#f0fdf4',
                    'text': '#14532d',
                    'text_secondary': '#6b7280',
                    'border': '#d1fae5',
                    'shadow': 'rgba(22, 163, 74, 0.1)'
                },
                'fonts': {
                    'primary': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
                    'secondary': 'Roboto, sans-serif',
                    'monospace': 'Fira Code, monospace'
                },
                'spacing': {
                    'xs': '4px',
                    'sm': '8px',
                    'md': '16px',
                    'lg': '24px',
                    'xl': '32px',
                    'xxl': '48px'
                },
                'border_radius': {
                    'sm': '4px',
                    'md': '8px',
                    'lg': '12px',
                    'xl': '16px'
                }
            },
            'purple': {
                'name': 'Mor Tema',
                'description': 'Yaratıcı mor tema',
                'colors': {
                    'primary': '#7c3aed',
                    'secondary': '#6b7280',
                    'success': '#10b981',
                    'danger': '#f43f5e',
                    'warning': '#f59e0b',
                    'info': '#06b6d4',
                    'light': '#faf5ff',
                    'dark': '#581c87',
                    'background': '#ffffff',
                    'surface': '#faf5ff',
                    'text': '#581c87',
                    'text_secondary': '#6b7280',
                    'border': '#e9d5ff',
                    'shadow': 'rgba(124, 58, 237, 0.1)'
                },
                'fonts': {
                    'primary': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
                    'secondary': 'Roboto, sans-serif',
                    'monospace': 'Fira Code, monospace'
                },
                'spacing': {
                    'xs': '4px',
                    'sm': '8px',
                    'md': '16px',
                    'lg': '24px',
                    'xl': '32px',
                    'xxl': '48px'
                },
                'border_radius': {
                    'sm': '4px',
                    'md': '8px',
                    'lg': '12px',
                    'xl': '16px'
                }
            }
        }
        
        self.current_theme = 'light'
        self.theme_file = 'data/themes/user_themes.json'
        self._ensure_theme_directory()
        self._load_user_themes()
    
    def _ensure_theme_directory(self):
        """Tema dizinini oluştur"""
        os.makedirs('data/themes', exist_ok=True)
    
    def _load_user_themes(self):
        """Kullanıcı temalarını yükle"""
        try:
            if os.path.exists(self.theme_file):
                with open(self.theme_file, 'r', encoding='utf-8') as f:
                    user_themes = json.load(f)
                    self.themes.update(user_themes)
                log_info(f"{len(user_themes)} kullanıcı teması yüklendi")
        except Exception as e:
            log_error(f"Kullanıcı temaları yükleme hatası: {e}")
    
    def get_available_themes(self) -> Dict[str, Dict[str, Any]]:
        """Mevcut temaları getir"""
        try:
            return {
                theme_id: {
                    'id': theme_id,
                    'name': theme['name'],
                    'description': theme['description'],
                    'is_custom': theme_id not in ['light', 'dark', 'blue', 'green', 'purple']
                }
                for theme_id, theme in self.themes.items()
            }
        except Exception as e:
            log_error(f"Tema listesi alma hatası: {e}")
            return {}
    
    def get_current_theme(self) -> Dict[str, Any]:
        """Mevcut temayı getir"""
        try:
            return self.themes.get(self.current_theme, self.themes['light'])
        except Exception as e:
            log_error(f"Mevcut tema alma hatası: {e}")
            return self.themes['light']
    
    def set_theme(self, theme_id: str) -> bool:
        """Tema ayarla"""
        try:
            if theme_id in self.themes:
                self.current_theme = theme_id
                self._save_current_theme()
                log_info(f"Tema değiştirildi: {theme_id}")
                return True
            else:
                log_error(f"Bilinmeyen tema: {theme_id}")
                return False
        except Exception as e:
            log_error(f"Tema ayarlama hatası: {e}")
            return False
    
    def _save_current_theme(self):
        """Mevcut temayı kaydet"""
        try:
            theme_data = {
                'current_theme': self.current_theme,
                'last_updated': datetime.now().isoformat()
            }
            
            with open('data/themes/current_theme.json', 'w', encoding='utf-8') as f:
                json.dump(theme_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            log_error(f"Mevcut tema kaydetme hatası: {e}")
    
    def create_custom_theme(self, theme_id: str, theme_data: Dict[str, Any]) -> bool:
        """Özel tema oluştur"""
        try:
            # Tema verilerini doğrula
            if not self._validate_theme_data(theme_data):
                return False
            
            # Tema ID'sini kontrol et
            if theme_id in self.themes:
                log_error(f"Tema zaten mevcut: {theme_id}")
                return False
            
            # Özel tema oluştur
            custom_theme = {
                'name': theme_data.get('name', f'Özel Tema {theme_id}'),
                'description': theme_data.get('description', 'Kullanıcı tarafından oluşturulan tema'),
                'colors': theme_data.get('colors', {}),
                'fonts': theme_data.get('fonts', {}),
                'spacing': theme_data.get('spacing', {}),
                'border_radius': theme_data.get('border_radius', {}),
                'created_at': datetime.now().isoformat(),
                'is_custom': True
            }
            
            # Temayı ekle
            self.themes[theme_id] = custom_theme
            
            # Kullanıcı temalarını kaydet
            self._save_user_themes()
            
            log_info(f"Özel tema oluşturuldu: {theme_id}")
            return True
            
        except Exception as e:
            log_error(f"Özel tema oluşturma hatası: {e}")
            return False
    
    def update_custom_theme(self, theme_id: str, theme_data: Dict[str, Any]) -> bool:
        """Özel temayı güncelle"""
        try:
            if theme_id not in self.themes:
                log_error(f"Tema bulunamadı: {theme_id}")
                return False
            
            if not self.themes[theme_id].get('is_custom', False):
                log_error(f"Sadece özel temalar güncellenebilir: {theme_id}")
                return False
            
            # Tema verilerini doğrula
            if not self._validate_theme_data(theme_data):
                return False
            
            # Temayı güncelle
            self.themes[theme_id].update({
                'name': theme_data.get('name', self.themes[theme_id]['name']),
                'description': theme_data.get('description', self.themes[theme_id]['description']),
                'colors': {**self.themes[theme_id]['colors'], **theme_data.get('colors', {})},
                'fonts': {**self.themes[theme_id]['fonts'], **theme_data.get('fonts', {})},
                'spacing': {**self.themes[theme_id]['spacing'], **theme_data.get('spacing', {})},
                'border_radius': {**self.themes[theme_id]['border_radius'], **theme_data.get('border_radius', {})},
                'updated_at': datetime.now().isoformat()
            })
            
            # Kullanıcı temalarını kaydet
            self._save_user_themes()
            
            log_info(f"Özel tema güncellendi: {theme_id}")
            return True
            
        except Exception as e:
            log_error(f"Özel tema güncelleme hatası: {e}")
            return False
    
    def delete_custom_theme(self, theme_id: str) -> bool:
        """Özel temayı sil"""
        try:
            if theme_id not in self.themes:
                log_error(f"Tema bulunamadı: {theme_id}")
                return False
            
            if not self.themes[theme_id].get('is_custom', False):
                log_error(f"Sadece özel temalar silinebilir: {theme_id}")
                return False
            
            # Temayı sil
            del self.themes[theme_id]
            
            # Eğer silinen tema mevcut temaysa, light temaya geç
            if self.current_theme == theme_id:
                self.current_theme = 'light'
                self._save_current_theme()
            
            # Kullanıcı temalarını kaydet
            self._save_user_themes()
            
            log_info(f"Özel tema silindi: {theme_id}")
            return True
            
        except Exception as e:
            log_error(f"Özel tema silme hatası: {e}")
            return False
    
    def _validate_theme_data(self, theme_data: Dict[str, Any]) -> bool:
        """Tema verilerini doğrula"""
        try:
            required_sections = ['colors', 'fonts', 'spacing', 'border_radius']
            
            for section in required_sections:
                if section not in theme_data:
                    log_error(f"Tema verilerinde eksik bölüm: {section}")
                    return False
            
            # Renk doğrulaması
            required_colors = ['primary', 'background', 'text', 'border']
            for color in required_colors:
                if color not in theme_data['colors']:
                    log_error(f"Tema renklerinde eksik: {color}")
                    return False
            
            return True
            
        except Exception as e:
            log_error(f"Tema doğrulama hatası: {e}")
            return False
    
    def _save_user_themes(self):
        """Kullanıcı temalarını kaydet"""
        try:
            user_themes = {
                theme_id: theme_data
                for theme_id, theme_data in self.themes.items()
                if theme_data.get('is_custom', False)
            }
            
            with open(self.theme_file, 'w', encoding='utf-8') as f:
                json.dump(user_themes, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            log_error(f"Kullanıcı temaları kaydetme hatası: {e}")
    
    def generate_css_variables(self, theme_id: str = None) -> str:
        """CSS değişkenleri oluştur"""
        try:
            if theme_id is None:
                theme_id = self.current_theme
            
            theme = self.themes.get(theme_id, self.themes['light'])
            
            css_variables = []
            css_variables.append(':root {')
            
            # Renk değişkenleri
            for color_name, color_value in theme['colors'].items():
                css_variables.append(f'  --color-{color_name}: {color_value};')
            
            # Font değişkenleri
            for font_name, font_value in theme['fonts'].items():
                css_variables.append(f'  --font-{font_name}: {font_value};')
            
            # Spacing değişkenleri
            for spacing_name, spacing_value in theme['spacing'].items():
                css_variables.append(f'  --spacing-{spacing_name}: {spacing_value};')
            
            # Border radius değişkenleri
            for radius_name, radius_value in theme['border_radius'].items():
                css_variables.append(f'  --border-radius-{radius_name}: {radius_value};')
            
            css_variables.append('}')
            
            return '\n'.join(css_variables)
            
        except Exception as e:
            log_error(f"CSS değişkenleri oluşturma hatası: {e}")
            return ''
    
    def generate_theme_css(self, theme_id: str = None) -> str:
        """Tema CSS'i oluştur"""
        try:
            if theme_id is None:
                theme_id = self.current_theme
            
            theme = self.themes.get(theme_id, self.themes['light'])
            
            css_parts = []
            
            # CSS değişkenleri
            css_parts.append(self.generate_css_variables(theme_id))
            
            # Temel stil kuralları
            css_parts.append(f'''
/* {theme['name']} Tema Stilleri */
body {{
    background-color: var(--color-background);
    color: var(--color-text);
    font-family: var(--font-primary);
}}

.container {{
    background-color: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius-lg);
    box-shadow: 0 2px 8px var(--color-shadow);
}}

.btn {{
    background-color: var(--color-primary);
    color: white;
    border: none;
    border-radius: var(--border-radius-md);
    padding: var(--spacing-sm) var(--spacing-md);
    font-family: var(--font-primary);
    transition: all 0.2s ease;
}}

.btn:hover {{
    opacity: 0.9;
    transform: translateY(-1px);
}}

.btn-success {{
    background-color: var(--color-success);
}}

.btn-danger {{
    background-color: var(--color-danger);
}}

.btn-warning {{
    background-color: var(--color-warning);
}}

.btn-info {{
    background-color: var(--color-info);
}}

.card {{
    background-color: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    margin: var(--spacing-md) 0;
}}

.table {{
    background-color: var(--color-surface);
    color: var(--color-text);
}}

.table th {{
    background-color: var(--color-primary);
    color: white;
}}

.table td {{
    border-color: var(--color-border);
}}

.form-control {{
    background-color: var(--color-surface);
    color: var(--color-text);
    border: 1px solid var(--color-border);
    border-radius: var(--border-radius-sm);
}}

.form-control:focus {{
    border-color: var(--color-primary);
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}}

.alert {{
    border-radius: var(--border-radius-md);
    padding: var(--spacing-md);
    margin: var(--spacing-md) 0;
}}

.alert-success {{
    background-color: var(--color-success);
    color: white;
}}

.alert-danger {{
    background-color: var(--color-danger);
    color: white;
}}

.alert-warning {{
    background-color: var(--color-warning);
    color: white;
}}

.alert-info {{
    background-color: var(--color-info);
    color: white;
}}

/* Dark mode özel stiller */
{theme_id == 'dark' and '''
.dark-mode-specific {{
    background-color: var(--color-surface);
    border-color: var(--color-border);
}}

.dark-mode-specific:hover {{
    background-color: var(--color-background);
}}
''' or ''}
''')
            
            return '\n'.join(css_parts)
            
        except Exception as e:
            log_error(f"Tema CSS oluşturma hatası: {e}")
            return ''
    
    def export_theme(self, theme_id: str) -> Optional[Dict[str, Any]]:
        """Temayı dışa aktar"""
        try:
            if theme_id not in self.themes:
                log_error(f"Tema bulunamadı: {theme_id}")
                return None
            
            theme = self.themes[theme_id].copy()
            theme['exported_at'] = datetime.now().isoformat()
            theme['version'] = '1.0'
            
            return theme
            
        except Exception as e:
            log_error(f"Tema dışa aktarma hatası: {e}")
            return None
    
    def import_theme(self, theme_data: Dict[str, Any]) -> bool:
        """Temayı içe aktar"""
        try:
            # Tema verilerini doğrula
            if not self._validate_theme_data(theme_data):
                return False
            
            # Tema ID'sini oluştur
            theme_name = theme_data.get('name', 'Imported Theme')
            theme_id = theme_name.lower().replace(' ', '_').replace('ı', 'i').replace('ğ', 'g').replace('ü', 'u').replace('ş', 's').replace('ö', 'o').replace('ç', 'c')
            
            # Benzersiz ID oluştur
            original_theme_id = theme_id
            counter = 1
            while theme_id in self.themes:
                theme_id = f"{original_theme_id}_{counter}"
                counter += 1
            
            # Temayı ekle
            imported_theme = {
                'name': theme_name,
                'description': theme_data.get('description', 'İçe aktarılan tema'),
                'colors': theme_data['colors'],
                'fonts': theme_data['fonts'],
                'spacing': theme_data['spacing'],
                'border_radius': theme_data['border_radius'],
                'imported_at': datetime.now().isoformat(),
                'is_custom': True
            }
            
            self.themes[theme_id] = imported_theme
            self._save_user_themes()
            
            log_info(f"Tema içe aktarıldı: {theme_id}")
            return True
            
        except Exception as e:
            log_error(f"Tema içe aktarma hatası: {e}")
            return False
    
    def get_theme_preview(self, theme_id: str) -> Dict[str, Any]:
        """Tema önizlemesi oluştur"""
        try:
            if theme_id not in self.themes:
                return {}
            
            theme = self.themes[theme_id]
            
            return {
                'theme_id': theme_id,
                'name': theme['name'],
                'description': theme['description'],
                'preview_colors': {
                    'primary': theme['colors']['primary'],
                    'background': theme['colors']['background'],
                    'surface': theme['colors']['surface'],
                    'text': theme['colors']['text'],
                    'border': theme['colors']['border']
                },
                'css_variables': self.generate_css_variables(theme_id),
                'is_custom': theme.get('is_custom', False)
            }
            
        except Exception as e:
            log_error(f"Tema önizlemesi oluşturma hatası: {e}")
            return {}

# Global theme manager instance
theme_manager = ThemeManager()

