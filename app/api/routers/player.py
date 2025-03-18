from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...core.dependency import get_db
from ...shcemas import player
from ...database.CRUD import player as p_crud

player_router = APIRouter()


player_router = APIRouter()

@player_router.post("/register/")
async def register_player(
    data: player.player_form,
    session: AsyncSession = Depends(get_db),
):
    existing_player = await p_crud.read_player(db=session, username=data.player_username)
    if existing_player:
        raise HTTPException(
            detail="email address is already in use",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        await p_crud.create_player(db=session, data=data)
    except Exception as e:
        raise HTTPException(
            detail=f"Something went wrong: {str(e)}",
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
        )

    return {"message": "Player registered successfully!"}
