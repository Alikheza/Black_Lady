from ..models import Players
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_player(db: AsyncSession, data) -> None:
    new_player = Players(**data.dict())
    db.add(new_player)
    await db.commit()


async def read_player(db: AsyncSession, username: str) -> Players:
    result = await db.execute(select(Players).filter(Players.player_username == username))
    return result.scalar_one_or_none()
