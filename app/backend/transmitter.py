import asyncio
import json
import websockets
from threading import Thread

class DataTransmitter:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.connected_clients = set()
        self.loop = None

    async def _handler(self, websocket):
        """Obsługa nowego połączenia od klienta (frontendu)"""
        self.connected_clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            self.connected_clients.remove(websocket)

    async def _broadcast(self, message):
        """Wysyła wiadomość do wszystkich podłączonych klientów"""
        if not self.connected_clients:
            return
        
        # Tworzenie listy tasków wysyłania
        msg_json = json.dumps(message)
        # websockets.broadcast jest dostępne w nowszych wersjach, 
        # ale dla pewności używamy pętli
        for ws in list(self.connected_clients):
            try:
                await ws.send(msg_json)
            except:
                self.connected_clients.remove(ws)

    def start_server(self):
        """Uruchamia serwer w oddzielnym wątku (non-blocking)"""
        new_loop = asyncio.new_event_loop()
        self.loop = new_loop
        
        def run_loop(loop):
            asyncio.set_event_loop(loop)
            start_server = websockets.serve(self._handler, self.host, self.port)
            print(f"Server WebSocket działa na ws://{self.host}:{self.port}")
            loop.run_until_complete(start_server)
            loop.run_forever()

        t = Thread(target=run_loop, args=(new_loop,), daemon=True)
        t.start()

    def send_data(self, data_dict):
        """Publiczna metoda do wywołania z głównego programu"""
        if self.loop:
            asyncio.run_coroutine_threadsafe(self._broadcast(data_dict), self.loop)