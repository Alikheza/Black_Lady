"""
This module tracks the online and in-game status of players.

Note:
For production systems, replace this in-memory approach with Redis or another persistent
and scalable store to support concurrent and distributed instances.
"""

from __future__ import annotations

from typing import Optional

# Dictionary to track player presence.
# Key: username (str)
# Value: list containing:
#   [0] - online status (bool)
#   [1] - in-game status (bool)
player_presence: dict[str, list[bool, bool]] = {}

def check_player_online(username: str) -> Optional[list[bool, bool]]:
    """
    Check a player's current presence status.

    Args:
        username (str): The username of the player.

    Returns:
        list[bool, bool] | None: A list containing [is_online, is_in_game],
        or None if the player is not found.
    """
    return player_presence.get(username)

def update_player_status(username: str, online: bool = True, is_playing: bool = False) -> None:
    """
    Update the online and in-game status of a player.

    If the player is not already tracked, they will be added.

    Args:
        username (str): The username of the player.
        online (bool): Whether the player is currently online.
        is_playing (bool): Whether the player is currently in a game.
    """
    player_presence[username] = [online, is_playing]
