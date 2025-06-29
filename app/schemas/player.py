from pydantic import BaseModel, Field
from typing import Annotated

class player_form(BaseModel):

    player_password: Annotated[str, Field(
        min_length=8,
        max_length=50,
        description="Password must be between 8 and 50 characters"
    )]
    player_username: Annotated[
        str, 
        Field(
            min_length=3,max_length=20,pattern=r'^[a-z0-9_]+$',
            description="Username must be 3-20 characters long and contain only" \
            " lowercase letters, numbers, and underscores")
            ]

class player(player_form):
    player_name : Annotated[str, Field(
        min_length=3, max_length=50,
        description="Name must be between 3 and 50 characters"
    )]

class Token(BaseModel):
    access_token: str
    token_type: str
    
class Friends(BaseModel):
    player_id: int 
    friend_id: int
    request_status: str = "requested"