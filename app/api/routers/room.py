from fastapi import APIRouter, WebSocket, WebSocketDisconnect , status
from ..connection import RoomConnectionManager 
from ...core.auth_ws import authenticate_ws_player
from .. import room_controller 

room_endpoint = APIRouter()

room_List: dict[str : RoomConnectionManager] = {}

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
                case "selecetd_card":
                    player.selected_card = [card for card in data.get("card").split(",")]
                case "play":
                    room.start_game()
                case "move" :
                    card = data.get("card")
                    if card is None : 
                        message = {"message":"you are in a game action is not accepted"}
                        await room.response(message)
                        continue
                    try:
                        room.validate_move(move=card,player_num=player.player_number)
                    except ValueError as err :
                        await room.response(err)

                case "invite_player" :
                    if room.game_started == True :
                        message = {"message":"you are in a gave action is not accepted"}
                        await room.response(message)
                        continue
                    player_username = data.get("player")
                    await room_controller.invite_player(player_username, player.player_id, room)

                case "join_room" :
                    if room.game_started == True :
                        message = {"message":"you are in a game, action is not accepted"}
                        await room.response(message)
                        continue
                    room_id = data.get("room_id")
                    room_to_join = room_List.get(room_id)
                    result = await room_controller.accept_invitation(current_room=room, room_to_join=room_to_join, ws=websocket, player=player)
                    room_controller.delete_room(room.id, room_List)
                    if result:
                        room = room_to_join
                case _ :
                    await room.broadcast("invalid action")

    except WebSocketDisconnect:
        await room.broadcast(
            f"{player.player_number} disconnected from room {room_id}", 
            exclude_player_id=player.player_id
        )
        await room.check_connection(player)
        room_controller.delete_room(room.id, room_List)

    except Exception as e:
        await room.response(
            message=f"request type invalid, send request in json {e}",
            id=player.player_id
        )
        await room.disconnect(player, status_code=status.WS_1008_POLICY_VIOLATION)
        room_controller.delete_room(room.id, room_List)

