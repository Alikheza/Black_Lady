from ..models import Players
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_player(db: AsyncSession, data) -> None:
    new_player = Players(**data.dict())
    db.add(new_player)
    await db.commit()

async def read_player(db: AsyncSession, username: str = None, id: int = None) -> Players:
    if username:
        result = await db.execute(select(Players).filter(Players.player_username == username))
    elif id:
        result = await db.execute(select(Players).filter(Players.player_id == id))
    else:
        raise ValueError("id or username must be set")
    return result.scalar_one_or_none()
