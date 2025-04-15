import jwt
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from fastapi import WebSocket , status
from .config import Evariable
from .dependency import get_db
from ..database.CRUD import player as player_crud

SECRET_KEY = Evariable.SECRET_KEY
ALGORITHM = Evariable.ALGORITHM


async def decode_ws_token(token: str):
    """
    Decodes a JWT token and returns the associated player object.
    Raises ValueError if the token is invalid or the player does not exist.
    """
    async for db_session in get_db():
        try:
            decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = decoded_payload.get("sub")

            if not username:
                raise InvalidTokenError("Token missing subject (sub).")

            player = await player_crud.read_player(username=username, db=db_session)

            if not player:
                raise InvalidTokenError("No player found for the token.")

            return player

        except ExpiredSignatureError:
            raise ValueError("WebSocket token has expired.")
        except InvalidTokenError :
            raise ValueError(f"invalid WebSocket token ")



async def authenticate_ws_player(websocket: WebSocket):
    """
    Handles initial WebSocket authentication by receiving a token,
    decoding it, and returning the corresponding player object.
    """
    await websocket.accept()
    await websocket.send_text("Please send your token to authenticate.")

    token_data = await websocket.receive()
    token = token_data.get("text")

    try:
        player = await decode_ws_token(token=token)
        return player
    except Exception:
        await websocket.send_text("Authentication failed. Please login again.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None