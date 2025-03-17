from pydantic import BaseModel ,EmailStr

class player_in(BaseModel):
    pass    
class player(player_in):
    player_id : int

class player_form(BaseModel):
    username : str
    password : str 