from .. import models
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import player


async def create_player(db: AsyncSession, data) -> None:
    new_player = models.Players(**data.model_dump())
    db.add(new_player)
    await db.commit()
    await db.refresh(new_player)

async def read_player(db: AsyncSession, username: str = None, id: int = None) -> models.Players:
    if username is not None:
        result = await db.execute(select(models.Players).filter(models.Players.player_username == username))
    elif id is not None:
        result = await db.execute(select(models.Players).filter(models.Players.player_id == id))
    else:
        raise ValueError("id or username must be set")
    return result.scalar_one_or_none()

async def read_player_friends(db: AsyncSession, id:int): 
    result = await db.execute(select(models.Players.player_name,models.Players.player_username)
        .join(models.Friendship , models.Players.player_id == models.Friendship.friend_id)
        .where(models.Friendship.player_id == id,models.Friendship.request_status == "accepted"))
    return result.all()

async def check_friend(db: AsyncSession, player_id: int, friend_id :int):
    result = await db.execute(select(models.Friendship).filter(models.Friendship.player_id == player_id , models.Friendship.friend_id == friend_id ))
    return result.scalar_one_or_none()

async def create_friends_relationship(db:AsyncSession, data) -> None:
    new_firend = models.Friendship(**data.model_dump())
    db.add(new_firend)
    await db.commit()

async def update_friends_relationship(
    db: AsyncSession,
    player_id: int,
    friend_id: int,
    status: str,
    data: player.Friends = None
) -> None:
    
    result = await db.execute(
        select(models.Friendship).where(
            models.Friendship.player_id == player_id,
            models.Friendship.friend_id == friend_id
        )
    )
    relationship = result.scalar_one_or_none()

    if not relationship:
        return

    match status:
        case "accepted":
            relationship.request_status = "accepted"
            
            if data:
                existing = await db.execute(
                    select(models.Friendship).where(
                        models.Friendship.player_id == friend_id,
                        models.Friendship.friend_id == player_id
                    )
                )
                reverse_relationship = existing.scalar_one_or_none()

                if not reverse_relationship:
                    friend = models.Friendship(**data.model_dump())
                    db.add(friend)


        case "rejected":
            relationship.request_status = "rejected"

        case "blocked":
            relationship.request_status = "blocked"

            result = await db.execute(
                select(models.Friendship).where(
                    models.Friendship.player_id == friend_id,
                    models.Friendship.friend_id == player_id
                )
            )
            friend = result.scalar_one_or_none()
            if friend:
                friend.request_status = "blocked"

        case _:
            return None

    await db.commit()
    await db.refresh(relationship)