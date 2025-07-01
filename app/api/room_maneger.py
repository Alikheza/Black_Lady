import asyncio
from fastapi import WebSocket, WebSocketDisconnect, status
from fastapi.websockets import WebSocketState
from ..game.room import Room
from ..game.player import Player
from ..core import presence_tracker 
from ..core.config import Evariable

room_List: dict[str : "RoomManager"] = {}

class RoomManager(Room):
    
    def __init__(self):
        super().__init__()  
        self.connections : dict[str : WebSocket] = {}

    def connect(self, player, websocket):
        self.connections[player.player_id] = websocket
        self.add_players(player)
        presence_tracker.update_player_status(username=player.username)

    def disconnect_from_room(self, player: Player, status_code: int = status.WS_1000_NORMAL_CLOSURE):

        self.connections.pop(player.player_id, None)
        self.players.remove(player)
        if len(self.players) == 0:
            room_List.pop(self.id, None)

    async def disconnect(self, player: Player, status_code: int = status.WS_1000_NORMAL_CLOSURE):
        try:
            connection = self.connections[player.player_id]
            if connection.client_state == WebSocketState.CONNECTED:
                await connection.close(code=status_code)
        except:
            pass
        finally:
            self.connections.pop(player.player_id, None)
            self.players.remove(player)
            if len(self.players) == 0:
                room_List.pop(self.id, None)
                

    async def receive_or_timeout(self, player: Player):
        try:
            data = await asyncio.wait_for(self.connections[player.player_id].receive_json(), timeout=Evariable.WS_EXPIRE_SECOUNDS)
        except (asyncio.TimeoutError, WebSocketDisconnect) :
            await self.disconnect(player, status_code=status.WS_1002_PROTOCOL_ERROR)
            presence_tracker.update_player_status(username=player.username, online=False)
            return None    
        return data

    async def broadcast(self, message: dict, exclude_player_id: str = None):
        for player_id, connection in self.connections.items():
            if player_id != exclude_player_id:
                await connection.send_json(message)

    async def response(self, id: str, message: dict):
        connection = self.connections.get(id)
        if connection :
            await connection.send_json(message)
    
    async def invite_player(self, target_username: str, inviter_id: str):
        if self.game_started:
            await self.response(
                id=inviter_id,
                message={"error": "Cannot invite during game"}
                )
            return False

        player_status = presence_tracker.check_player_online(username=target_username)
        if player_status is None:
            await self.response(
                id=inviter_id,
                message={"error": "Player not found"}
            )
            return False

        is_online, is_in_game = player_status[:2]
        if not is_online or is_in_game:
            await self.response(
                id=inviter_id,
                message={"error": "Player unavailable"}
            )
            return False

        return True
    
    async def join_room(self, player: Player, room_to_join: 'RoomManager', ws: WebSocket):

        conditions = {
        room_to_join.id == self.id: "You are already in this room",
        room_to_join.game_started or self.game_started: "Cannot join while game is in progress",
        len(room_to_join.players) >= 4: "Target room is full"
        }

        for condition, message in conditions.items():
            if condition:
                await self.response(id=player.player_id, message=message)
                return False

        room_to_join.connect(player, ws)
        self.disconnect_from_room(player)
        return True
    
    def create_player(self, user) -> Player:
        if len(self.players) >= 4:
            raise ValueError("Room is full")
            
        player = Player(
            id=str(user.player_id),
            player_num=len(self.players) + 1,
            name=user.player_name,
            username=user.player_username
        )
        return player