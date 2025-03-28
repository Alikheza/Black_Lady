from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ...core import auth
from ...core.dependency import get_db
from ...shcemas import player as Player
from ...database.CRUD import player as p_crud

player_router = APIRouter()

@player_router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register_player(data: Player.player, session: AsyncSession = Depends(get_db)):
    if await p_crud.read_player(db=session, username=data.player_username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already in use")
    
    data.player_password = auth.hash_password(data.player_password)
    await p_crud.create_player(db=session, data=data)
    return {"message": "Player registered successfully"}

@player_router.post("/login/", status_code=status.HTTP_202_ACCEPTED)
async def login_player(data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    player_data = await p_crud.read_player(db=session, username=data.username)
    if not player_data or not auth.verify_password(data.password, player_data.player_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    token = auth.create_access_token(data={"sub": data.username})
    return Player.Token(access_token=token, token_type="bearer")


#for test
@player_router.get("/home/", status_code=status.HTTP_200_OK)
async def home_player(current_user: Annotated[dict, Depends(auth.get_current_player)]):
    return {"message": f"Hello, {current_user.player_name}!"}
