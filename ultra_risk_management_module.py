#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ ULTRA RISK MANAGEMENT MODULE
Profesyonel Risk Yönetimi - Position Sizing, Stop Loss, Take Profit

Author: Ultra Risk Team
Created: 2025-10-03
Version: 1.0.0
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class RiskProfile:
    """Risk profili"""
    risk_tolerance: str  # "CONSERVATIVE", "MODERATE", "AGGRESSIVE"
    max_position_size: float  # % of portfolio
    max_portfolio_heat: float  # % of portfolio at risk
    win_rate: float  # Historical win rate
    avg_win_loss_ratio: float  # R:R ratio

@dataclass
class TradeSetup:
    """Trade setup detayları"""
    symbol: str
    entry_price: float
    position_size_usd: float
    position_size_pct: float
    stop_loss: float
    stop_loss_pct: float
    take_profit_1: float
    take_profit_1_pct: float
    take_profit_2: float
    take_profit_2_pct: float
    take_profit_3: float
    take_profit_3_pct: float
    risk_reward_ratio: float
    max_loss_usd: float
    expected_profit_usd: float
    holding_period: str
    confidence: float

class UltraRiskManager:
    """🛡️ Ultra Professional Risk Manager"""
    
    def __init__(self, portfolio_value: float = 100000):
        self.portfolio_value = portfolio_value
        
        # Risk profiles
        self.risk_profiles = {
            "CONSERVATIVE": RiskProfile(
                risk_tolerance="CONSERVATIVE",
                max_position_size=0.03,  # 3% per position
                max_portfolio_heat=0.10,  # 10% total risk
                win_rate=0.55,
                avg_win_loss_ratio=2.0
            ),
            "MODERATE": RiskProfile(
                risk_tolerance="MODERATE",
                max_position_size=0.05,  # 5% per position
                max_portfolio_heat=0.15,  # 15% total risk
                win_rate=0.50,
                avg_win_loss_ratio=2.5
            ),
            "AGGRESSIVE": RiskProfile(
                risk_tolerance="AGGRESSIVE",
                max_position_size=0.08,  # 8% per position
                max_portfolio_heat=0.20,  # 20% total risk
                win_rate=0.45,
                avg_win_loss_ratio=3.0
            )
        }
    
    def calculate_position_size(
        self, 
        score: float,
        price: float,
        volatility: float,
        market: str = "BIST",
        risk_profile: str = "MODERATE"
    ) -> Tuple[float, float]:
        """
        Position size hesaplama - Kelly Criterion + Risk-adjusted
        
        Returns:
            (position_size_usd, position_size_pct)
        """
        profile = self.risk_profiles[risk_profile]
        
        # 1) Base position size from score
        if score >= 85:  # Hidden Gem
            base_pct = profile.max_position_size * 1.2  # 20% boost
        elif score >= 75:  # Mega Opportunity
            base_pct = profile.max_position_size * 1.0
        elif score >= 65:  # Ultra Signal
            base_pct = profile.max_position_size * 0.7
        else:
            base_pct = profile.max_position_size * 0.5
        
        # 2) Volatility adjustment
        # High volatility = reduce size
        if volatility > 0.40:  # 40%+ volatility
            vol_adjustment = 0.6
        elif volatility > 0.25:
            vol_adjustment = 0.8
        else:
            vol_adjustment = 1.0
        
        # 3) Market adjustment
        market_multipliers = {
            "BIST": 1.0,
            "NASDAQ": 1.2,  # More stable
            "CRYPTO": 0.6,  # More volatile
            "EMTIA": 0.8,
            "XETRA": 1.1
        }
        market_adj = market_multipliers.get(market, 1.0)
        
        # 4) Final position size
        final_pct = base_pct * vol_adjustment * market_adj
        final_pct = min(final_pct, profile.max_position_size)  # Cap
        
        position_size_usd = self.portfolio_value * final_pct
        
        return position_size_usd, final_pct
    
    def calculate_stop_loss(
        self,
        entry_price: float,
        volatility: float,
        atr: Optional[float] = None,
        score: float = 70.0
    ) -> Tuple[float, float]:
        """
        Stop Loss hesaplama - ATR + Score-adjusted
        
        Returns:
            (stop_loss_price, stop_loss_pct)
        """
        # 1) Base stop loss from score
        if score >= 85:  # Hidden Gem - tighter stop
            base_stop_pct = 0.05  # 5%
        elif score >= 75:  # Mega
            base_stop_pct = 0.07  # 7%
        elif score >= 65:  # Ultra
            base_stop_pct = 0.10  # 10%
        else:
            base_stop_pct = 0.12  # 12%
        
        # 2) Volatility adjustment
        if volatility > 0.40:
            vol_multiplier = 1.5  # Wider stop
        elif volatility > 0.25:
            vol_multiplier = 1.2
        else:
            vol_multiplier = 1.0
        
        # 3) ATR-based stop (if available)
        if atr and atr > 0:
            atr_stop_pct = (atr * 2) / entry_price  # 2x ATR
            # Use whichever is wider (more conservative)
            final_stop_pct = max(base_stop_pct * vol_multiplier, atr_stop_pct)
        else:
            final_stop_pct = base_stop_pct * vol_multiplier
        
        stop_loss_price = entry_price * (1 - final_stop_pct)
        
        return stop_loss_price, final_stop_pct
    
    def calculate_take_profits(
        self,
        entry_price: float,
        score: float,
        volatility: float,
        market: str = "BIST"
    ) -> Dict[str, Tuple[float, float]]:
        """
        Take Profit levels - Triple exit strategy
        
        Returns:
            {
                'tp1': (price, pct),
                'tp2': (price, pct),
                'tp3': (price, pct)
            }
        """
        # 1) Base targets from score
        if score >= 85:  # Hidden Gem
            base_tp1, base_tp2, base_tp3 = 0.10, 0.20, 0.35
        elif score >= 75:  # Mega
            base_tp1, base_tp2, base_tp3 = 0.08, 0.15, 0.25
        elif score >= 65:  # Ultra
            base_tp1, base_tp2, base_tp3 = 0.06, 0.12, 0.20
        else:
            base_tp1, base_tp2, base_tp3 = 0.05, 0.10, 0.15
        
        # 2) Volatility bonus
        if volatility > 0.30:
            vol_bonus = 1.3  # Higher targets for volatile assets
        elif volatility > 0.20:
            vol_bonus = 1.15
        else:
            vol_bonus = 1.0
        
        # 3) Market multiplier
        market_multipliers = {
            "BIST": 1.0,
            "NASDAQ": 0.9,  # More realistic
            "CRYPTO": 1.5,  # Higher potential
            "EMTIA": 1.1,
            "XETRA": 0.95
        }
        market_mult = market_multipliers.get(market, 1.0)
        
        # 4) Final targets
        tp1_pct = base_tp1 * vol_bonus * market_mult
        tp2_pct = base_tp2 * vol_bonus * market_mult
        tp3_pct = base_tp3 * vol_bonus * market_mult
        
        return {
            'tp1': (entry_price * (1 + tp1_pct), tp1_pct),
            'tp2': (entry_price * (1 + tp2_pct), tp2_pct),
            'tp3': (entry_price * (1 + tp3_pct), tp3_pct)
        }
    
    def calculate_holding_period(
        self,
        score: float,
        volatility: float,
        market: str = "BIST"
    ) -> str:
        """Tavsiye edilen tutma süresi"""
        if market == "CRYPTO":
            if score >= 85:
                return "3-7 gün (Hızlı çıkış)"
            elif score >= 75:
                return "1-2 hafta"
            else:
                return "2-3 hafta"
        elif market in ["NASDAQ", "XETRA"]:
            if score >= 85:
                return "2-4 hafta"
            elif score >= 75:
                return "4-8 hafta"
            else:
                return "2-3 ay"
        else:  # BIST, EMTIA
            if score >= 85:
                return "3-6 hafta"
            elif score >= 75:
                return "2-3 ay"
            else:
                return "3-6 ay"
    
    def generate_trade_setup(
        self,
        symbol: str,
        score: float,
        price: float,
        volatility: float,
        atr: Optional[float],
        market: str = "BIST",
        risk_profile: str = "MODERATE"
    ) -> TradeSetup:
        """Complete trade setup generation"""
        
        # 1) Position sizing
        position_size_usd, position_size_pct = self.calculate_position_size(
            score, price, volatility, market, risk_profile
        )
        
        # 2) Stop loss
        stop_loss, stop_loss_pct = self.calculate_stop_loss(
            price, volatility, atr, score
        )
        
        # 3) Take profits
        tps = self.calculate_take_profits(price, score, volatility, market)
        
        # 4) Risk/Reward
        max_loss = position_size_usd * stop_loss_pct
        expected_profit = position_size_usd * tps['tp2'][1]  # Use TP2 as target
        risk_reward = expected_profit / max_loss if max_loss > 0 else 0
        
        # 5) Holding period
        holding_period = self.calculate_holding_period(score, volatility, market)
        
        # 6) Confidence
        confidence = min(0.95, (score / 100) * 1.1)  # Scale to 0-95%
        
        return TradeSetup(
            symbol=symbol,
            entry_price=price,
            position_size_usd=position_size_usd,
            position_size_pct=position_size_pct,
            stop_loss=stop_loss,
            stop_loss_pct=stop_loss_pct,
            take_profit_1=tps['tp1'][0],
            take_profit_1_pct=tps['tp1'][1],
            take_profit_2=tps['tp2'][0],
            take_profit_2_pct=tps['tp2'][1],
            take_profit_3=tps['tp3'][0],
            take_profit_3_pct=tps['tp3'][1],
            risk_reward_ratio=risk_reward,
            max_loss_usd=max_loss,
            expected_profit_usd=expected_profit,
            holding_period=holding_period,
            confidence=confidence
        )
    
    def format_trade_message(self, trade: TradeSetup) -> str:
        """Format trade setup as Telegram message"""
        
        # Signal strength emoji
        if trade.confidence >= 0.85:
            strength_emoji = "💎💎💎"
            strength_text = "HIDDEN GEM"
        elif trade.confidence >= 0.75:
            strength_emoji = "🚀🚀"
            strength_text = "MEGA OPPORTUNITY"
        elif trade.confidence >= 0.65:
            strength_emoji = "⚡"
            strength_text = "ULTRA SIGNAL"
        else:
            strength_emoji = "📊"
            strength_text = "NORMAL SIGNAL"
        
        message = f"""
{strength_emoji} <b>{trade.symbol} - {strength_text}</b> {strength_emoji}

💰 <b>TRADE SETUP:</b>
├─ 📍 Giriş: ${trade.entry_price:.2f}
├─ 💵 Pozisyon: ${trade.position_size_usd:,.0f} ({trade.position_size_pct*100:.1f}% portföy)
└─ 🎯 Confidence: {trade.confidence*100:.0f}%

🛑 <b>RİSK YÖNETİMİ:</b>
├─ Stop Loss: ${trade.stop_loss:.2f} ({trade.stop_loss_pct*100:.1f}%)
├─ Max Loss: ${trade.max_loss_usd:,.0f}
└─ Risk/Reward: 1:{trade.risk_reward_ratio:.1f}

🎯 <b>KAR HEDEFLER:</b>
├─ TP1: ${trade.take_profit_1:.2f} (+{trade.take_profit_1_pct*100:.1f}%) [Sell 33%]
├─ TP2: ${trade.take_profit_2:.2f} (+{trade.take_profit_2_pct*100:.1f}%) [Sell 33%]
└─ TP3: ${trade.take_profit_3:.2f} (+{trade.take_profit_3_pct*100:.1f}%) [Sell 34%]

⏰ <b>TUTMA SÜRESİ:</b> {trade.holding_period}
💰 <b>BEKLENİLEN KAR:</b> ${trade.expected_profit_usd:,.0f}

⚡ <b>STRATEJİ:</b>
1️⃣ Giriş fiyatından al
2️⃣ Stop loss'u kesinlikle koy!
3️⃣ TP1'de %33 sat (masrafları çıkar)
4️⃣ TP2'de %33 sat (kar al)
5️⃣ Kalan %34'ü TP3'e trailing stop ile götür

#RiskManagement #ProfessionalTrading
"""
        return message.strip()

# Global instance
ultra_risk_manager = UltraRiskManager()

if __name__ == "__main__":
    # Test
    print("🛡️ Testing Ultra Risk Management Module...")
    
    # Example: AAPL Hidden Gem
    trade_setup = ultra_risk_manager.generate_trade_setup(
        symbol="AAPL",
        score=88.7,
        price=182.50,
        volatility=0.25,
        atr=3.50,
        market="NASDAQ",
        risk_profile="MODERATE"
    )
    
    print(ultra_risk_manager.format_trade_message(trade_setup))
    print("\n✅ Risk Management Module Ready!")
