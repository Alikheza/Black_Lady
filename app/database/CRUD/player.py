# from sqlalchemy import cr
from ..models import Players

def create_player(db,data):
    db_players = Players(**data.dict())
    db.add(db_players)
    db.commit()
    db.refresh(db_players)

def read_player(db, username:str, id:int = False):
    if id :
        return db.query(Players).filter(Players.player_id==id).first()
    else : 
        return db.query(Players).filter(Players.player_username==username).first()