"""
PlanB Motoru - Portfolio Manager
Portfolio takibi ve yönetimi modülü
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from src.utils.logger import log_info, log_error, log_debug

@dataclass
class Position:
    """Portfolio pozisyonu"""
    symbol: str
    quantity: float
    entry_price: float
    current_price: float
    entry_date: str
    market: str
    notes: str = ""
    
    @property
    def market_value(self) -> float:
        """Güncel piyasa değeri"""
        return self.quantity * self.current_price
    
    @property
    def cost_basis(self) -> float:
        """Maliyet bazı"""
        return self.quantity * self.entry_price
    
    @property
    def unrealized_pnl(self) -> float:
        """Gerçekleşmemiş kar/zarar"""
        return self.market_value - self.cost_basis
    
    @property
    def unrealized_pnl_percent(self) -> float:
        """Gerçekleşmemiş kar/zarar yüzdesi"""
        if self.cost_basis == 0:
            return 0
        return (self.unrealized_pnl / self.cost_basis) * 100

@dataclass
class Transaction:
    """Portfolio işlemi"""
    id: str
    symbol: str
    transaction_type: str  # 'buy', 'sell', 'dividend'
    quantity: float
    price: float
    date: str
    fees: float = 0.0
    notes: str = ""

@dataclass
class Portfolio:
    """Portfolio sınıfı"""
    name: str
    positions: List[Position]
    transactions: List[Transaction]
    cash: float
    created_date: str
    last_updated: str
    
    @property
    def total_market_value(self) -> float:
        """Toplam piyasa değeri"""
        return sum(pos.market_value for pos in self.positions) + self.cash
    
    @property
    def total_cost_basis(self) -> float:
        """Toplam maliyet bazı"""
        return sum(pos.cost_basis for pos in self.positions) + self.cash
    
    @property
    def total_unrealized_pnl(self) -> float:
        """Toplam gerçekleşmemiş kar/zarar"""
        return sum(pos.unrealized_pnl for pos in self.positions)
    
    @property
    def total_unrealized_pnl_percent(self) -> float:
        """Toplam gerçekleşmemiş kar/zarar yüzdesi"""
        if self.total_cost_basis == 0:
            return 0
        return (self.total_unrealized_pnl / self.total_cost_basis) * 100

class PortfolioManager:
    """Portfolio yöneticisi"""
    
    def __init__(self, data_dir: str = "data/portfolios"):
        self.data_dir = data_dir
        self.portfolios: Dict[str, Portfolio] = {}
        self._ensure_data_dir()
        self._load_portfolios()
    
    def _ensure_data_dir(self):
        """Veri dizinini oluştur"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _load_portfolios(self):
        """Portfolio'ları yükle"""
        try:
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    portfolio_name = filename[:-5]  # .json uzantısını kaldır
                    filepath = os.path.join(self.data_dir, filename)
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Portfolio nesnesini oluştur
                    positions = [Position(**pos) for pos in data.get('positions', [])]
                    transactions = [Transaction(**tx) for tx in data.get('transactions', [])]
                    
                    portfolio = Portfolio(
                        name=data['name'],
                        positions=positions,
                        transactions=transactions,
                        cash=data.get('cash', 0.0),
                        created_date=data.get('created_date', ''),
                        last_updated=data.get('last_updated', '')
                    )
                    
                    self.portfolios[portfolio_name] = portfolio
                    log_info(f"Portfolio yüklendi: {portfolio_name}")
            
            log_info(f"Toplam {len(self.portfolios)} portfolio yüklendi")
            
        except Exception as e:
            log_error(f"Portfolio'lar yüklenirken hata: {e}")
    
    def _save_portfolio(self, portfolio: Portfolio):
        """Portfolio'yu kaydet"""
        try:
            filepath = os.path.join(self.data_dir, f"{portfolio.name}.json")
            
            # Portfolio'yu dict'e çevir
            data = {
                'name': portfolio.name,
                'positions': [asdict(pos) for pos in portfolio.positions],
                'transactions': [asdict(tx) for tx in portfolio.transactions],
                'cash': portfolio.cash,
                'created_date': portfolio.created_date,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            log_debug(f"Portfolio kaydedildi: {portfolio.name}")
            
        except Exception as e:
            log_error(f"Portfolio kaydedilirken hata: {e}")
    
    def create_portfolio(self, name: str, initial_cash: float = 10000.0) -> Portfolio:
        """Yeni portfolio oluştur"""
        if name in self.portfolios:
            raise ValueError(f"Portfolio zaten mevcut: {name}")
        
        portfolio = Portfolio(
            name=name,
            positions=[],
            transactions=[],
            cash=initial_cash,
            created_date=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )
        
        self.portfolios[name] = portfolio
        self._save_portfolio(portfolio)
        log_info(f"Yeni portfolio oluşturuldu: {name}")
        
        return portfolio
    
    def get_portfolio(self, name: str) -> Optional[Portfolio]:
        """Portfolio getir"""
        return self.portfolios.get(name)
    
    def list_portfolios(self) -> List[str]:
        """Portfolio listesini getir"""
        return list(self.portfolios.keys())
    
    def add_position(self, portfolio_name: str, symbol: str, quantity: float, 
                    entry_price: float, current_price: float = None, 
                    market: str = "UNKNOWN", notes: str = "") -> bool:
        """Portfolio'ya pozisyon ekle"""
        try:
            portfolio = self.get_portfolio(portfolio_name)
            if not portfolio:
                raise ValueError(f"Portfolio bulunamadı: {portfolio_name}")
            
            if current_price is None:
                current_price = entry_price
            
            position = Position(
                symbol=symbol,
                quantity=quantity,
                entry_price=entry_price,
                current_price=current_price,
                entry_date=datetime.now().isoformat(),
                market=market,
                notes=notes
            )
            
            portfolio.positions.append(position)
            self._save_portfolio(portfolio)
            
            log_info(f"Pozisyon eklendi: {symbol} ({quantity} adet @ {entry_price})")
            return True
            
        except Exception as e:
            log_error(f"Pozisyon eklenirken hata: {e}")
            return False
    
    def update_position_price(self, portfolio_name: str, symbol: str, new_price: float) -> bool:
        """Pozisyon fiyatını güncelle"""
        try:
            portfolio = self.get_portfolio(portfolio_name)
            if not portfolio:
                return False
            
            for position in portfolio.positions:
                if position.symbol == symbol:
                    position.current_price = new_price
                    self._save_portfolio(portfolio)
                    log_debug(f"Fiyat güncellendi: {symbol} -> {new_price}")
                    return True
            
            return False
            
        except Exception as e:
            log_error(f"Fiyat güncellenirken hata: {e}")
            return False
    
    def remove_position(self, portfolio_name: str, symbol: str) -> bool:
        """Pozisyonu kaldır"""
        try:
            portfolio = self.get_portfolio(portfolio_name)
            if not portfolio:
                return False
            
            portfolio.positions = [pos for pos in portfolio.positions if pos.symbol != symbol]
            self._save_portfolio(portfolio)
            
            log_info(f"Pozisyon kaldırıldı: {symbol}")
            return True
            
        except Exception as e:
            log_error(f"Pozisyon kaldırılırken hata: {e}")
            return False
    
    def add_transaction(self, portfolio_name: str, symbol: str, transaction_type: str,
                       quantity: float, price: float, fees: float = 0.0, notes: str = "") -> bool:
        """İşlem ekle"""
        try:
            portfolio = self.get_portfolio(portfolio_name)
            if not portfolio:
                return False
            
            transaction_id = f"{symbol}_{transaction_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            transaction = Transaction(
                id=transaction_id,
                symbol=symbol,
                transaction_type=transaction_type,
                quantity=quantity,
                price=price,
                date=datetime.now().isoformat(),
                fees=fees,
                notes=notes
            )
            
            portfolio.transactions.append(transaction)
            self._save_portfolio(portfolio)
            
            log_info(f"İşlem eklendi: {transaction_type} {quantity} {symbol} @ {price}")
            return True
            
        except Exception as e:
            log_error(f"İşlem eklenirken hata: {e}")
            return False
    
    def get_portfolio_summary(self, portfolio_name: str) -> Dict[str, Any]:
        """Portfolio özeti getir"""
        try:
            portfolio = self.get_portfolio(portfolio_name)
            if not portfolio:
                return {}
            
            # En iyi ve en kötü performans
            best_position = None
            worst_position = None
            
            for position in portfolio.positions:
                if best_position is None or position.unrealized_pnl_percent > best_position.unrealized_pnl_percent:
                    best_position = position
                if worst_position is None or position.unrealized_pnl_percent < worst_position.unrealized_pnl_percent:
                    worst_position = position
            
            # Sektör dağılımı
            sector_distribution = {}
            for position in portfolio.positions:
                market = position.market
                if market not in sector_distribution:
                    sector_distribution[market] = 0
                sector_distribution[market] += position.market_value
            
            return {
                'name': portfolio.name,
                'total_market_value': portfolio.total_market_value,
                'total_cost_basis': portfolio.total_cost_basis,
                'total_unrealized_pnl': portfolio.total_unrealized_pnl,
                'total_unrealized_pnl_percent': portfolio.total_unrealized_pnl_percent,
                'cash': portfolio.cash,
                'position_count': len(portfolio.positions),
                'transaction_count': len(portfolio.transactions),
                'best_position': {
                    'symbol': best_position.symbol,
                    'pnl_percent': best_position.unrealized_pnl_percent
                } if best_position else None,
                'worst_position': {
                    'symbol': worst_position.symbol,
                    'pnl_percent': worst_position.unrealized_pnl_percent
                } if worst_position else None,
                'sector_distribution': sector_distribution,
                'last_updated': portfolio.last_updated
            }
            
        except Exception as e:
            log_error(f"Portfolio özeti alınırken hata: {e}")
            return {}
    
    def get_portfolio_positions(self, portfolio_name: str) -> List[Dict[str, Any]]:
        """Portfolio pozisyonlarını getir"""
        try:
            portfolio = self.get_portfolio(portfolio_name)
            if not portfolio:
                return []
            
            return [asdict(position) for position in portfolio.positions]
            
        except Exception as e:
            log_error(f"Pozisyonlar alınırken hata: {e}")
            return []
    
    def get_portfolio_transactions(self, portfolio_name: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Portfolio işlemlerini getir"""
        try:
            portfolio = self.get_portfolio(portfolio_name)
            if not portfolio:
                return []
            
            # En son işlemlerden başla
            transactions = sorted(portfolio.transactions, key=lambda x: x.date, reverse=True)
            return [asdict(tx) for tx in transactions[:limit]]
            
        except Exception as e:
            log_error(f"İşlemler alınırken hata: {e}")
            return []

# Global portfolio manager instance
portfolio_manager = PortfolioManager()

