# from .connect import Base
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship , DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models."""
    pass

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

    # games: Mapped[list["Games"]] = relationship("Games", secondary="games_played", back_populates="players",overlaps="player_association")
    game_association: Mapped[list["Association"]] = relationship("Association", back_populates="player",overlaps="players")

class Games(Base):
    """Games table."""

    __tablename__ = "games"

    game_id: Mapped[int] = mapped_column(primary_key=True)
    winner: Mapped[int] = mapped_column(ForeignKey("players.player_id"))

    # players: Mapped[list["Players"]] = relationship("Players", secondary="games_played", back_populates="games",overlaps="game_association")
    player_association: Mapped[list["Association"]] = relationship("Association", back_populates="game",overlaps="games")
