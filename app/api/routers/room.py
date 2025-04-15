from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from ..connection import RoomConnectionManager
from ...core.auth_ws import authenticate_ws_player
from .. import room_controller

room_endpoint = APIRouter()

room_List: dict[int : RoomConnectionManager] = {}

@room_endpoint.websocket("/ws/game/")
async def game_websocket_endpoint(websocket: WebSocket, room_id: str = None):

    user = await authenticate_ws_player(websocket)

    if user is None : return 
    

    if room_id not in room_List.keys() and room_id is not None:
        await websocket.send_text("Room not found")
        await websocket.close()
        return
    
    if room_id is None:
        room = RoomConnectionManager()
        room_List[room.id] = room
        await websocket.send_json({"room_id": room.id})
    else :
        room = room_List[room_id]
    
    player = room_controller.create_player_object(room, player=user)

    await room.connect(player,websocket)

    try:
        while True:
            data = await websocket.receive_json()
            match data.get("action"):
                case "send_message":
                    message = {"message":f"{player.name} says: {data.get('message')}"}
                    await room.broadcast(message)
                case "start_game":
                    await room_controller.start_game(room)
                case "invite_player" :
                    player_username = data.get("player")
                    await room_controller.invite_player(player_username, player.player_id, room)
                case _ :
                    await room.broadcast("invalid action")

    except WebSocketDisconnect:
        await room.broadcast(f"{player.player_number} disconnected from room {room_id}")
        await room.disconnect(player.player_id)

    except Exception as e:
        await room.broadcast(f"request type invalid, send request in json {e}")
        await room.disconnect(player.player_id)

