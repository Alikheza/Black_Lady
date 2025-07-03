from fastapi import APIRouter, WebSocket, WebSocketDisconnect , status
from ..room_maneger import RoomManager , room_List  
from ...core.auth_ws import authenticate_ws_player

room_endpoint = APIRouter()


@room_endpoint.websocket("/ws/game/")
async def game_websocket_endpoint(websocket: WebSocket, room_id: str = None):

    user = await authenticate_ws_player(websocket)

    if user is None : return 
    
    if room_id is None : 
        room = RoomManager()
        room_List[room.id] = room
        await websocket.send_json({"room_id": room.id})

    elif room_id not in room_List.keys() :
        await websocket.send_text("Room not found")
        await websocket.close()
        return

    else :
        room = room_List[room_id]
    
    player = room.create_player(user)
    
    await room.connect(player,websocket)
    try:       
        while True:
            data = await room.receive_or_timeout(player)
            if data is None :
                return
            match data.get("action"):

                case "send_message":
                    text = data.get('message')
                    message = {
                        "type" : "message",
                        "payload" : {
                            "from" : player.name ,
                            "text" : text
                        }
                    }
                    await room.broadcast(message=message, exclude_player_id=player.player_id)

                case "selected_card":
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
                    player_username = data.get("player")
                    result = await room.invite_player(target_username=player_username,inviter_id= player.player_id)
                    if result :
                        await room.response(
                            id = player.player_id,
                            message = {
                                "type" : "notification",
                                "payload" : {
                                    "message" : "invitation has been sent" 
                                }  
                            }
                        )

                case "join_room" :
                    room_id = data.get("room_id")
                    room_to_join = room_List.get(room_id)
                    result = await room.join_room(room_to_join=room_to_join, ws=websocket, player=player)
                    if result:
                        room = room_to_join
                
                case _ :
                    await room.broadcast("invalid action")

    except WebSocketDisconnect:
        await room.broadcast(
            exclude_player_id=player.player_id,
            messgae = {
                "type" : "warining",  
                "payloda" : {
                    "messgae" : f"{player.name} disconnected from the room"
                }
            }
        )
# return erro to debuging
    except Exception as e:
        await room.response(
            id=player.player_id,
            message={
                "type" : "error",
                "payload" : {
                    "message" : f"request type invalid, send request in json {e}"
                }
            }
        )
        await room.disconnect(player, status_code=status.WS_1008_POLICY_VIOLATION)
