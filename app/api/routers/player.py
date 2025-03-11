from fastapi import APIRouter , Depends ,  HTTPException ,status
from sqlalchemy.orm import Session
from ..dependency import get_db
from ...shcemas import player
from ...database.CRUD import player as p_crud
player_app = APIRouter()

#for test
@player_app.post("/register_player/")
async def register_player(data: player.player_in, db: Session=Depends(get_db)):
    if p_crud.read_player(db=db, username=data.player_username) :
        raise HTTPException(detail="email address is already in use",status_code=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            p_crud.create_player(db=db,data=data)
        except Exception as e :
            raise HTTPException(detail="somthing went wrong", status_code=status.HTTP_406_NOT_ACCEPTABLE)
        return {"message": "player register "}
