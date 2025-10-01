"""
PlanB Motoru - Heatmap Generator
Sektör bazlı heatmap görselleştirme
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug

class HeatmapGenerator:
    """Sektör bazlı heatmap oluşturucu"""
    
    def __init__(self):
        self.sector_mapping = {
            'Technology': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA'],
            'Finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'AXP'],
            'Healthcare': ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT'],
            'Energy': ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'PXD', 'MPC'],
            'Consumer': ['PG', 'KO', 'PEP', 'WMT', 'HD', 'MCD', 'NKE'],
            'Industrial': ['BA', 'CAT', 'GE', 'MMM', 'HON', 'UPS', 'FDX'],
            'Materials': ['LIN', 'APD', 'SHW', 'ECL', 'DD', 'PPG', 'NEM'],
            'Utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'XEL'],
            'Real Estate': ['AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'WELL', 'O'],
            'Communication': ['VZ', 'T', 'CMCSA', 'CHTR', 'DIS', 'NFLX', 'TMUS']
        }
        
        self.crypto_sectors = {
            'DeFi': ['UNI', 'AAVE', 'COMP', 'MKR', 'SNX', 'YFI', 'CRV'],
            'Layer1': ['ETH', 'ADA', 'SOL', 'AVAX', 'DOT', 'MATIC', 'ATOM'],
            'Meme': ['DOGE', 'SHIB', 'PEPE', 'FLOKI', 'BONK', 'WIF'],
            'Gaming': ['AXS', 'SAND', 'MANA', 'GALA', 'ENJ', 'ILV'],
            'Storage': ['FIL', 'AR', 'SC', 'STORJ', 'SIA'],
            'Privacy': ['XMR', 'ZEC', 'DASH', 'SCRT', 'BEAM']
        }
    
    def generate_sector_heatmap(self, price_data: Dict[str, pd.DataFrame], 
                              timeframe: str = '1d') -> Dict[str, Any]:
        """Sektör heatmap oluştur"""
        try:
            heatmap_data = {}
            
            for sector, symbols in self.sector_mapping.items():
                sector_returns = []
                sector_volumes = []
                
                for symbol in symbols:
                    if symbol in price_data and not price_data[symbol].empty:
                        df = price_data[symbol]
                        
                        # Getiri hesapla
                        if 'close' in df.columns:
                            returns = df['close'].pct_change(fill_method=None).dropna()
                            if not returns.empty:
                                sector_returns.extend(returns.tolist())
                        
                        # Hacim hesapla
                        if 'volume' in df.columns:
                            volumes = df['volume'].dropna()
                            if not volumes.empty:
                                sector_volumes.extend(volumes.tolist())
                
                if sector_returns:
                    avg_return = np.mean(sector_returns) * 100
                    volatility = np.std(sector_returns) * 100
                    volume_ratio = np.mean(sector_volumes) if sector_volumes else 0
                    
                    heatmap_data[sector] = {
                        'return_pct': round(avg_return, 2),
                        'volatility_pct': round(volatility, 2),
                        'volume_ratio': round(volume_ratio, 0),
                        'symbol_count': len([s for s in symbols if s in price_data]),
                        'color_intensity': self._calculate_color_intensity(avg_return, volatility)
                    }
            
            return {
                'heatmap_data': heatmap_data,
                'timeframe': timeframe,
                'generated_at': datetime.now().isoformat(),
                'total_sectors': len(heatmap_data)
            }
            
        except Exception as e:
            log_error(f"Sektör heatmap oluşturma hatası: {e}")
            return {}
    
    def generate_crypto_heatmap(self, price_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Kripto sektör heatmap oluştur"""
        try:
            heatmap_data = {}
            
            for sector, symbols in self.crypto_sectors.items():
                sector_returns = []
                sector_volumes = []
                
                for symbol in symbols:
                    if symbol in price_data and not price_data[symbol].empty:
                        df = price_data[symbol]
                        
                        if 'close' in df.columns:
                            returns = df['close'].pct_change(fill_method=None).dropna()
                            if not returns.empty:
                                sector_returns.extend(returns.tolist())
                        
                        if 'volume' in df.columns:
                            volumes = df['volume'].dropna()
                            if not volumes.empty:
                                sector_volumes.extend(volumes.tolist())
                
                if sector_returns:
                    avg_return = np.mean(sector_returns) * 100
                    volatility = np.std(sector_returns) * 100
                    volume_ratio = np.mean(sector_volumes) if sector_volumes else 0
                    
                    heatmap_data[sector] = {
                        'return_pct': round(avg_return, 2),
                        'volatility_pct': round(volatility, 2),
                        'volume_ratio': round(volume_ratio, 0),
                        'symbol_count': len([s for s in symbols if s in price_data]),
                        'color_intensity': self._calculate_color_intensity(avg_return, volatility)
                    }
            
            return {
                'heatmap_data': heatmap_data,
                'market_type': 'crypto',
                'generated_at': datetime.now().isoformat(),
                'total_sectors': len(heatmap_data)
            }
            
        except Exception as e:
            log_error(f"Kripto heatmap oluşturma hatası: {e}")
            return {}
    
    def _calculate_color_intensity(self, return_pct: float, volatility: float) -> str:
        """Renk yoğunluğunu hesapla"""
        try:
            # Getiri bazlı renk
            if return_pct > 5:
                return 'very_positive'
            elif return_pct > 2:
                return 'positive'
            elif return_pct > -2:
                return 'neutral'
            elif return_pct > -5:
                return 'negative'
            else:
                return 'very_negative'
                
        except Exception as e:
            return 'neutral'
    
    def generate_rotation_analysis(self, heatmap_data: Dict[str, Any]) -> Dict[str, Any]:
        """Sektör rotasyon analizi"""
        try:
            if not heatmap_data or 'heatmap_data' not in heatmap_data:
                return {}
            
            sectors = heatmap_data['heatmap_data']
            
            # En iyi ve en kötü performans
            sorted_sectors = sorted(sectors.items(), 
                                  key=lambda x: x[1]['return_pct'], reverse=True)
            
            top_performers = sorted_sectors[:3]
            bottom_performers = sorted_sectors[-3:]
            
            # Momentum analizi
            momentum_analysis = {
                'leading_sectors': [{'sector': sector, 'return': data['return_pct']} 
                                  for sector, data in top_performers],
                'lagging_sectors': [{'sector': sector, 'return': data['return_pct']} 
                                  for sector, data in bottom_performers],
                'rotation_strength': self._calculate_rotation_strength(sectors),
                'market_breadth': self._calculate_market_breadth(sectors)
            }
            
            return momentum_analysis
            
        except Exception as e:
            log_error(f"Rotasyon analizi hatası: {e}")
            return {}
    
    def _calculate_rotation_strength(self, sectors: Dict[str, Any]) -> str:
        """Rotasyon gücünü hesapla"""
        try:
            returns = [data['return_pct'] for data in sectors.values()]
            if not returns:
                return 'weak'
            
            std_returns = np.std(returns)
            
            if std_returns > 3:
                return 'strong'
            elif std_returns > 1.5:
                return 'moderate'
            else:
                return 'weak'
                
        except Exception as e:
            return 'weak'
    
    def _calculate_market_breadth(self, sectors: Dict[str, Any]) -> Dict[str, Any]:
        """Piyasa genişliğini hesapla"""
        try:
            positive_sectors = len([data for data in sectors.values() 
                                  if data['return_pct'] > 0])
            total_sectors = len(sectors)
            
            breadth_ratio = positive_sectors / total_sectors if total_sectors > 0 else 0
            
            if breadth_ratio > 0.7:
                breadth_strength = 'strong'
            elif breadth_ratio > 0.5:
                breadth_strength = 'moderate'
            else:
                breadth_strength = 'weak'
            
            return {
                'positive_sectors': positive_sectors,
                'total_sectors': total_sectors,
                'breadth_ratio': round(breadth_ratio, 2),
                'breadth_strength': breadth_strength
            }
            
        except Exception as e:
            return {'breadth_ratio': 0, 'breadth_strength': 'weak'}

# Global heatmap generator instance
heatmap_generator = HeatmapGenerator()

