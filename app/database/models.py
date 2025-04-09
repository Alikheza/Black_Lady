# from .connect import Base
from sqlalchemy import String, ForeignKey, Integer , Table , Column
from sqlalchemy.orm import Mapped, mapped_column, relationship , DeclarativeBase 
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models."""
    pass

class Friendship(Base):
    """Association table for friendships ."""

    __tablename__ = "friends_table"

    player_id: Mapped[int] = mapped_column(ForeignKey("players.player_id"), primary_key=True)
    friend_id: Mapped[int] = mapped_column(ForeignKey("players.player_id"), primary_key=True)
    request_status: Mapped[str] = mapped_column(String(20))  # e.g., "accepted", "rejected", "blocked" , "requested"

    player: Mapped["Players"] = relationship("Players", foreign_keys=[player_id], back_populates="friends_with")
    friend: Mapped["Players"] = relationship("Players", foreign_keys=[friend_id], back_populates="friendships")

class Association(Base):
    """Association table for many-to-many relationship between Players and Games."""

    __tablename__ = "games_played"

    player_id: Mapped[int] = mapped_column(ForeignKey("players.player_id"), primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.game_id"), primary_key=True)
    score: Mapped[int] = mapped_column(Integer)

    game: Mapped["Games"] = relationship("Games", back_populates="player_association")
    player: Mapped["Players"] = relationship("Players", back_populates="game_association")

class Players(Base):
    """Players table."""

    __tablename__ = "players"

    player_id: Mapped[int] = mapped_column(primary_key=True)
    player_name: Mapped[str] = mapped_column(String(20))
    player_password: Mapped[str] = mapped_column(String(100))
    player_username: Mapped[str] = mapped_column(String(100))

    friends_with: Mapped[list["Friendship"]] = relationship("Friendship",foreign_keys=[Friendship.player_id], back_populates="player")
    friendships: Mapped[list["Friendship"]] = relationship("Friendship",foreign_keys=[Friendship.friend_id],  back_populates="friend")

    game_association: Mapped[list["Association"]] = relationship("Association", back_populates="player",overlaps="players")


class Games(Base):
    """Games table."""

    __tablename__ = "games"

    game_id: Mapped[int] = mapped_column(primary_key=True)
    winner: Mapped[int] = mapped_column(ForeignKey("players.player_id"))

    player_association: Mapped[list["Association"]] = relationship("Association", back_populates="game",overlaps="games")