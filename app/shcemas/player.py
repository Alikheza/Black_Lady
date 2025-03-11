from pydantic import BaseModel ,EmailStr

class player_in (BaseModel):
    player_name : str
    player_username : EmailStr
    
class player(player_in):
    player_id : int
