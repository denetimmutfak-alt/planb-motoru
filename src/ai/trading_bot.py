"""
AI Trading Bot - Otomatik Trading Sistemi
"""

import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class TradingMode(Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"

@dataclass
class Trade:
    symbol: str
    action: str  # BUY, SELL, HOLD
    price: float
    quantity: int
    timestamp: datetime
    confidence: float
    reason: str

class AITradingBot:
    def __init__(self):
        self.is_active = False
        self.trading_mode = TradingMode.CONSERVATIVE
        self.trade_history: List[Trade] = []
        self.current_positions: Dict[str, int] = {}
        self.total_trades = 0
        self.winning_trades = 0
        self.start_time = None
        
        # Trading parameters based on mode
        self.mode_params = {
            TradingMode.CONSERVATIVE: {
                'max_position_size': 1000,
                'risk_tolerance': 0.02,
                'confidence_threshold': 0.8,
                'max_daily_trades': 5
            },
            TradingMode.MODERATE: {
                'max_position_size': 2500,
                'risk_tolerance': 0.05,
                'confidence_threshold': 0.7,
                'max_daily_trades': 10
            },
            TradingMode.AGGRESSIVE: {
                'max_position_size': 5000,
                'risk_tolerance': 0.1,
                'confidence_threshold': 0.6,
                'max_daily_trades': 20
            }
        }
    
    def start_bot(self, mode: str) -> bool:
        """Bot'u başlat"""
        try:
            self.trading_mode = TradingMode(mode)
            self.is_active = True
            self.start_time = datetime.now()
            print(f"🤖 AI Trading Bot başlatıldı - Mod: {mode}")
            return True
        except Exception as e:
            print(f"❌ Bot başlatma hatası: {e}")
            return False
    
    def stop_bot(self) -> bool:
        """Bot'u durdur"""
        try:
            self.is_active = False
            print("🛑 AI Trading Bot durduruldu")
            return True
        except Exception as e:
            print(f"❌ Bot durdurma hatası: {e}")
            return False
    
    def run_trading_cycle(self) -> Dict[str, Any]:
        """Trading döngüsünü çalıştır"""
        if not self.is_active:
            return {'success': False, 'message': 'Bot aktif değil'}
        
        try:
            # Simüle edilmiş trading kararları
            symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']
            symbol = random.choice(symbols)
            
            # Piyasa analizi simülasyonu
            market_sentiment = random.uniform(0.3, 0.9)
            technical_score = random.uniform(0.4, 0.8)
            fundamental_score = random.uniform(0.5, 0.9)
            
            # Karar verme
            action = self._make_trading_decision(symbol, market_sentiment, technical_score, fundamental_score)
            
            if action['action'] != 'HOLD':
                trade = Trade(
                    symbol=symbol,
                    action=action['action'],
                    price=action['price'],
                    quantity=action['quantity'],
                    timestamp=datetime.now(),
                    confidence=action['confidence'],
                    reason=action['reason']
                )
                
                self.trade_history.append(trade)
                self.total_trades += 1
                
                # Pozisyon güncelleme
                if action['action'] == 'BUY':
                    self.current_positions[symbol] = self.current_positions.get(symbol, 0) + action['quantity']
                elif action['action'] == 'SELL':
                    self.current_positions[symbol] = self.current_positions.get(symbol, 0) - action['quantity']
                
                print(f"📈 Trade: {action['action']} {action['quantity']} {symbol} @ ${action['price']:.2f}")
            
            return {
                'success': True,
                'action': action,
                'market_sentiment': market_sentiment,
                'technical_score': technical_score,
                'fundamental_score': fundamental_score
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Trading cycle hatası: {e}'}
    
    def _make_trading_decision(self, symbol: str, market_sentiment: float, technical_score: float, fundamental_score: float) -> Dict[str, Any]:
        """Trading kararı ver"""
        params = self.mode_params[self.trading_mode]
        
        # Skor hesaplama
        total_score = (market_sentiment * 0.3 + technical_score * 0.4 + fundamental_score * 0.3)
        
        # Fiyat simülasyonu
        base_price = random.uniform(100, 500)
        price = base_price * (1 + random.uniform(-0.05, 0.05))
        
        # Miktar hesaplama
        max_quantity = int(params['max_position_size'] / price)
        quantity = random.randint(1, max_quantity)
        
        # Karar verme
        if total_score >= params['confidence_threshold'] + 0.1:
            action = 'BUY'
            reason = f"Güçlü sinyal (Skor: {total_score:.2f})"
        elif total_score <= params['confidence_threshold'] - 0.1:
            action = 'SELL'
            reason = f"Zayıf sinyal (Skor: {total_score:.2f})"
        else:
            action = 'HOLD'
            reason = f"Belirsiz sinyal (Skor: {total_score:.2f})"
        
        return {
            'action': action,
            'price': price,
            'quantity': quantity,
            'confidence': total_score,
            'reason': reason
        }
    
    def get_bot_performance(self) -> Dict[str, Any]:
        """Bot performansını getir"""
        if not self.start_time:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'bot_confidence': 0,
                'current_positions': 0,
                'last_trade_time': None,
                'uptime': 0
            }
        
        # Simüle edilmiş performans
        win_rate = random.uniform(0.6, 0.8) if self.total_trades > 0 else 0
        bot_confidence = random.uniform(0.7, 0.9)
        current_positions = len(self.current_positions)
        
        uptime = (datetime.now() - self.start_time).total_seconds() / 3600  # saat cinsinden
        
        last_trade_time = None
        if self.trade_history:
            last_trade_time = self.trade_history[-1].timestamp.isoformat()
        
        return {
            'total_trades': self.total_trades,
            'win_rate': win_rate * 100,
            'bot_confidence': bot_confidence * 100,
            'current_positions': current_positions,
            'last_trade_time': last_trade_time,
            'uptime': uptime,
            'trading_mode': self.trading_mode.value,
            'daily_pnl': random.uniform(-500, 1000),
            'total_pnl': random.uniform(-1000, 5000)
        }
    
    def get_trade_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Trade geçmişini getir"""
        recent_trades = self.trade_history[-limit:] if self.trade_history else []
        
        return [
            {
                'symbol': trade.symbol,
                'action': trade.action,
                'price': trade.price,
                'quantity': trade.quantity,
                'timestamp': trade.timestamp.isoformat(),
                'confidence': trade.confidence,
                'reason': trade.reason
            }
            for trade in recent_trades
        ]

# Global instance
ai_trading_bot = AITradingBot()
