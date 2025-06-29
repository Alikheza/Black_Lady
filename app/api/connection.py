import asyncio
from fastapi import WebSocket, WebSocketDisconnect , status
from fastapi.websockets import WebSocketState
from ..game.room import Room

class RoomConnectionManager(Room):
    
    def __init__(self,):
        super().__init__()
        self.connections : dict[str : WebSocket] = {}

    async def connect(self, player, websocket):
        self.connections[player.player_id] = websocket
        self.add_players(player)

    async def disconnect(self, player, status_code:status = status.WS_1000_NORMAL_CLOSURE):
        try:
            connection = self.connections[player.player_id]
            if connection.client_state == WebSocketState.CONNECTED:
                await connection.close(code=status_code)  

        except:
            pass
        finally:
            self.connections.pop(player.player_id, None)
            self.players.remove(player)

    async def check_connection(self, player):
        try:
            await asyncio.wait_for(self.connections[player.player_id].receive_text(), timeout=120)
        except (asyncio.TimeoutError, WebSocketDisconnect):
            await self.disconnect(player)
        return self.connections[player.player_id].client_state == WebSocketState.CONNECTED

    async def broadcast(self, message, exclude_player_id:str ):
        for player, connection in self.connections.items():
            if player == exclude_player_id:
                continue
            else:
                await connection.send_json(message)
    
    async def response(self, id, message):
        connection = self.connections.get(id)
        await connection.send_json(message)
        