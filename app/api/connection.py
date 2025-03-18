from fastapi import WebSocket
from ..game.room import Room

class RoomConnectionManager(Room):
    def __init__(self,):
        super().__init__()
        self.connections : list[WebSocket] = []

    async def connect(self, websocket):
        self.connections.append(websocket)

    async def disconnect(self, websocket):
        self.connections.remove(websocket)

    async def broadcast(self, message):
        for connection in self.connections:
            await connection.send_json(message)
    