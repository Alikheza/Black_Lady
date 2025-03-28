import jwt
from typing import Annotated
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status
from passlib.hash import pbkdf2_sha1
from .config import Evariable
from ..database.CRUD import player as player_crud
from .dependency import get_db
from sqlalchemy.ext.asyncio import AsyncSession

custom_hash = pbkdf2_sha1.using(rounds=Evariable.HASH_ROUND)
SECRET_KEY = Evariable.SECRET_KEY
ALGORITHM = Evariable.ALGORITHM
TOKEN_EXPIRE_MINUTES = Evariable.ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/login/', scheme_name="player_login")


def hash_password(password: str) -> str:
    return custom_hash.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return custom_hash.verify(password, hashed)



def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_player(
    token: Annotated[str, Depends(oauth2_scheme)], 
    session: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise InvalidTokenError

        player = await player_crud.read_player(username=username, db=session)
        if not player:
            raise InvalidTokenError

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return player
