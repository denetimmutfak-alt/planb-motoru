"""
PlanB Motoru - WebSocket Handler
Real-time dashboard updates için WebSocket desteği
"""
import asyncio
import websockets
import json
import threading
import time
from datetime import datetime
from typing import Dict, Set, Any
from src.utils.logger import log_info, log_error, log_debug

class WebSocketHandler:
    """WebSocket bağlantılarını yöneten sınıf"""
    
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.running = False
        self.server = None
        
    async def register_client(self, websocket, path=None):
        """Yeni istemci kaydet"""
        self.clients.add(websocket)
        log_info(f"WebSocket istemci bağlandı: {websocket.remote_address}")
        
        try:
            # Hoş geldin mesajı gönder
            welcome_msg = {
                "type": "welcome",
                "message": "PlanB Motoru WebSocket bağlantısı kuruldu",
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(welcome_msg))
            
            # İstemci bağlantısını dinle
            async for message in websocket:
                await self.handle_client_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            log_info(f"WebSocket istemci bağlantısı kapandı: {websocket.remote_address}")
        finally:
            self.clients.remove(websocket)
    
    async def handle_client_message(self, websocket, message):
        """İstemci mesajlarını işle"""
        try:
            data = json.loads(message)
            msg_type = data.get('type', 'unknown')
            
            if msg_type == 'subscribe':
                # Belirli bir sembol için güncellemeleri dinle
                symbol = data.get('symbol', '')
                log_info(f"İstemci {symbol} için güncellemeleri dinlemeye başladı")
                
                # Abonelik onayı gönder
                response = {
                    "type": "subscription_confirmed",
                    "symbol": symbol,
                    "message": f"{symbol} için güncellemeler aktif",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(response))
                
            elif msg_type == 'ping':
                # Ping-pong için
                pong_response = {
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(pong_response))
                
        except json.JSONDecodeError:
            log_error("Geçersiz JSON mesajı alındı")
        except Exception as e:
            log_error(f"İstemci mesajı işlenirken hata: {e}")
    
    async def broadcast_update(self, update_data: Dict[str, Any]):
        """Tüm bağlı istemcilere güncelleme gönder"""
        if not self.clients:
            return
            
        message = json.dumps(update_data)
        disconnected_clients = set()
        
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                log_error(f"İstemciye mesaj gönderilirken hata: {e}")
                disconnected_clients.add(client)
        
        # Bağlantısı kopan istemcileri temizle
        self.clients -= disconnected_clients
    
    async def send_price_update(self, symbol: str, price_data: Dict[str, Any]):
        """Fiyat güncellemesi gönder"""
        update = {
            "type": "price_update",
            "symbol": symbol,
            "data": price_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast_update(update)
    
    async def send_analysis_update(self, symbol: str, analysis_data: Dict[str, Any]):
        """Analiz güncellemesi gönder"""
        update = {
            "type": "analysis_update",
            "symbol": symbol,
            "data": analysis_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast_update(update)
    
    async def send_alert(self, alert_data: Dict[str, Any]):
        """Uyarı mesajı gönder"""
        update = {
            "type": "alert",
            "data": alert_data,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast_update(update)
    
    async def start_server(self):
        """WebSocket sunucusunu başlat"""
        try:
            self.server = await websockets.serve(
                self.register_client,
                self.host,
                self.port
            )
            self.running = True
            log_info(f"WebSocket sunucusu başlatıldı: ws://{self.host}:{self.port}")
            
            # Sunucuyu çalıştır
            await self.server.wait_closed()
            
        except Exception as e:
            log_error(f"WebSocket sunucusu başlatılırken hata: {e}")
    
    def stop_server(self):
        """WebSocket sunucusunu durdur"""
        self.running = False
        if self.server:
            self.server.close()
        log_info("WebSocket sunucusu durduruldu")

# Global WebSocket handler instance
websocket_handler = WebSocketHandler()

def start_websocket_server():
    """WebSocket sunucusunu ayrı thread'de başlat"""
    def run_server():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websocket_handler.start_server())
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    log_info("WebSocket sunucusu thread'de başlatıldı")
    return thread

def send_price_update_sync(symbol: str, price_data: Dict[str, Any]):
    """Senkron fiyat güncellemesi gönder"""
    if websocket_handler.running and websocket_handler.clients:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websocket_handler.send_price_update(symbol, price_data))
        loop.close()

def send_analysis_update_sync(symbol: str, analysis_data: Dict[str, Any]):
    """Senkron analiz güncellemesi gönder"""
    if websocket_handler.running and websocket_handler.clients:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websocket_handler.send_analysis_update(symbol, analysis_data))
        loop.close()

def send_alert_sync(alert_data: Dict[str, Any]):
    """Senkron uyarı gönder"""
    if websocket_handler.running and websocket_handler.clients:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(websocket_handler.send_alert(alert_data))
        loop.close()

