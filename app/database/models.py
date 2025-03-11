from .connect import Base
from sqlalchemy import String , Table , Column , ForeignKey
from sqlalchemy.orm import Mapped , mapped_column , relationship 


association_table = Table(
    "association_table",
    Base.metadata,
    Column("player_id", ForeignKey("players.player_id"), primary_key=True),
    Column("gamer_id", ForeignKey("games.game_id"), primary_key=True),
)

class Players(Base):

    __tablename__ = "players"

    player_id : Mapped[int] = mapped_column(primary_key=True)
    player_name : Mapped[str] = mapped_column(String(20))
    player_username : Mapped[str] 

    games : Mapped[list["Games"]] = relationship(secondary=association_table, back_populates="players")

class Games(Base):

    __tablename__ = "games"

    game_id : Mapped[int] = mapped_column(primary_key=True)

    players : Mapped[list["Players"]] = relationship(secondary=association_table,back_populates="games")

