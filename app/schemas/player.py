from pydantic import BaseModel ,EmailStr

class player_form(BaseModel):

    player_password: str 
    player_username: EmailStr

class player(player_form):
    player_name: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class Friends(BaseModel):
    player_id: int 
    friend_id: int
    request_status: str = "requested"

