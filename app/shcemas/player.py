from pydantic import BaseModel ,EmailStr

class player_in(BaseModel):
    pass    
class player(player_in):
    player_id : int

class player_form(BaseModel):
    player_name: str
    player_password: str 
    player_username: EmailStr