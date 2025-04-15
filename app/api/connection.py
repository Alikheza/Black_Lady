from fastapi import WebSocket
from ..game.room import Room

class RoomConnectionManager(Room):
    
    def __init__(self,):
        super().__init__()
        self.connections : dict[str : WebSocket] = {}

    async def connect(self, player, websocket):
        self.connections[player.player_id] = websocket
        self.add_players(player)

    async def disconnect(self, id: str):
        connection = self.connections.pop(id)
        await connection.close()

    async def broadcast(self, message):
        for connection in self.connections.values():
            await connection.send_json(message)
    
    async def response(self, id, message):
        connection = self.connections.get(id)
        await connection.send_json(message)
