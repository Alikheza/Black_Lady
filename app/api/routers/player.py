from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from ...core import auth , heartBeat
from ...core.dependency import get_db
from ...schemas import player as Player
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
    if current_user.player_username != username : raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this.")

    heartBeat.update_player_status(username)
    #for test
    player_status = heartBeat.check_player_online(username)
    return {"status":f"{player_status}"}

@player_router.post("/friend/request/{username}",status_code=status.HTTP_201_CREATED)
async def send_friends_request(username: str, current_user: Annotated[dict, Depends(auth.get_current_player)],session: AsyncSession = Depends(get_db)):
    if username == current_user.player_username: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot send a friend request to yourself.")
    friend = await p_crud.read_player(db=session , username=username)
    if not friend : raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="player not found")
    result = await p_crud.check_friend(db=session, player_id=current_user.player_id, friend_id=friend.player_id)
    if result :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=f"you alrady request it result:{result.request_status}")
    friend_schema = Player.Friends(player_id=current_user.player_id, friend_id=friend.player_id , request_status= "requested")
    await p_crud.create_friends_relationship(db=session, data = friend_schema)
    return {"message": "Friend request sent"}

@player_router.put("/friend/update/{username}", status_code=status.HTTP_200_OK)
async def update_friend_request(username: str, action_status: str, current_user: Annotated[dict, Depends(auth.get_current_player)], session: AsyncSession = Depends(get_db)):
    requested_player = await p_crud.read_player(db=session , username=username)
    if not requested_player : raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="player not found")
    requested_player_friend_realationship = await p_crud.check_friend(db=session, player_id=requested_player.player_id, friend_id=current_user.player_id)
    if not requested_player_friend_realationship :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{username} has not sent you a friend request.")
    if action_status == "accepted" :
        data = Player.Friends(player_id=current_user.player_id, friend_id=requested_player.player_id , request_status= action_status)
    else: data = None
    await p_crud.update_friends_relationship(db=session, player_id=requested_player.player_id, friend_id=current_user.player_id, data= data, status=action_status)
    return {"message":"friends status updated"}


#for test
@player_router.get("/home/", status_code=status.HTTP_200_OK)
async def home_player(current_user: Annotated[dict, Depends(auth.get_current_player)]):
    return {"message": f"Hello, {current_user.player_name}!"}
#for test
@player_router.get("/friends/", status_code=status.HTTP_200_OK)
async def read_friends(current_user: Annotated[dict, Depends(auth.get_current_player)], session: AsyncSession = Depends(get_db)):
    friends_list = await p_crud.read_player_friends(db=session, id=current_user.player_id)
    friends_list = [{"name":f"{friend[0]}", "username":f"{friend[1]}"} for friend in friends_list]  
    return friends_list