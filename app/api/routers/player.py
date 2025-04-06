from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ...core import auth , heartBeat
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

    heartBeat.update_player_status(username=data.player_username)
    return {"message": "Player registered successfully"}

@player_router.post("/login/", status_code=status.HTTP_202_ACCEPTED)
async def login_player(data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    player_data = await p_crud.read_player(db=session, username=data.username)
    if not player_data or not auth.verify_password(data.password, player_data.player_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    token = auth.create_access_token(data={"sub": data.username})
    heartBeat.update_player_status(data.username)
    return Player.Token(access_token=token, token_type="bearer")

@player_router.put("/presence/{username}",status_code=status.HTTP_200_OK)
async def update_player_presence(username:str ,current_user: Annotated[dict, Depends(auth.get_current_player)]):
    if current_user.player_username != username : raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="cant accese this")
    heartBeat.update_player_status(username)
    #for test:
    player_status = heartBeat.check_player_online(username)
    return {"status":f"{player_status}"}
    
#for test
@player_router.get("/home/", status_code=status.HTTP_200_OK)
async def home_player(current_user: Annotated[dict, Depends(auth.get_current_player)]):
    return {"message": f"Hello, {current_user.player_name}!"}
