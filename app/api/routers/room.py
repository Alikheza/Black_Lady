from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..connection import RoomConnectionManager

room_endpoint = APIRouter()

room_List: dict[int : RoomConnectionManager] = {}

@room_endpoint.websocket("/ws/game/")
async def game_websocket_endpoint(websocket: WebSocket, room_id: str = None):
    await websocket.accept()

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

    await room.connect(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            match data.get("action"):
                case "send_message":
                    await room.broadcast(f"Client {websocket} says: {data.get('message')}")
                case "start_game":
                    
                    await room.broadcast(f"Game started")

                case "validate_move":
                    await room.broadcast(f"Move validated")
    except WebSocketDisconnect:
        print(f"Client disconnected from room {room_id}")

