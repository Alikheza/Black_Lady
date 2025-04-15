"""
This module manages the online/offline status of players and whether they are currently in a game. 
It is recommended to use an in-memory database (Redis) for better performance and scalability 
instead of this dictionary-based approach.
"""

from __future__ import annotations
from datetime import datetime, timedelta

# Dictionary to store player status.
# Key: username (str)
# Value: list[online_status (bool), in_game_status (bool), last_heartbeat (datetime), invite_request(room_id:player_username)]
heartBeat: dict[str, list[bool, bool, datetime, dict[str:str]]] = {}


def check_player_online(username: str) -> list[bool, bool, datetime] | None:
    """
    Check if a player is online and return their status.
    
    Args:
        username (str): The username of the player.

    Returns:
        list[bool, bool, datetime] | None: A list containing the player's online status, 
        in-game status, and last heartbeat timestamp, or None if the player is not found.
    """
    player = heartBeat.get(username)
    if not player:
        return None
    if player[0] == False:
        return player
    elif datetime.now() - player[2] > timedelta(seconds=40) and player[1] == False:
        heartBeat[username][0] = False
        player[0] = False

    return player


def update_player_status(username: str, online: bool = True, is_playing: bool = False) -> None:
    """
    Update the online and in-game status of a player. If the player is not already in the 
    heartBeat dictionary, they will be added.

    Args:
        username (str): The username of the player.
        online (bool): Whether the player is online. Defaults to True.
        is_playing (bool): Whether the player is currently in a game. Defaults to False.
    """
    if heartBeat.get(username):
        heartBeat[username][:3] = [online, is_playing, datetime.now()]
    else:
        heartBeat[username] = [online, is_playing, datetime.now(), {}]
        

def add_invitation(username, room_id:str, player_id:str):
    heartBeat[username][3] = {room_id:player_id}