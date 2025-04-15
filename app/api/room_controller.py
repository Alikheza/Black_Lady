from .connection import RoomConnectionManager
from ..core import heartBeat
from ..game.player import Player

async def invite_player(username: str, player_id: str, room: RoomConnectionManager) -> None:
    """
    Handle player invitation to a game room.
    Sends appropriate response based on player's availability.
    """
    player_status = heartBeat.check_player_online(username=username)

    if player_status is None:
        await room.response(id=player_id, message="No such player exists.")
        return

    is_online, is_in_game = player_status[:2]

    if not is_online:
        await room.response(id=player_id, message="Player is offline.")
        return

    if is_in_game:
        await room.response(id=player_id, message="Player is already in a game.")
        return

    heartBeat.add_invitation(username=username, room_id=room.id, player_id=player_id)
    await room.response(id=player_id, message="Invitation has been sent.")

def create_player_object(room: RoomConnectionManager, player) -> Player:
    """
    Create and return a new Player object if room is not full.
    """
    current_player_count = len(room.players)
    if current_player_count >= 4:
        raise ValueError("Room is already full.")

    player_num = current_player_count + 1
    return Player(
        id=str(player.player_id),
        player_num=player_num,
        name=player.player_name,
        username=player.player_username
    )

async def start_game(room: RoomConnectionManager):
    """
    Start the game if the room has exactly 4 players.
    Sends individual decks to each player.
    """
    if len(room.players) != 4:
        await room.broadcast({"message": "Not enough players to start the game."})
        return


    room.dealer()  # Shuffle and distribute cards

    for player in room.players:
        await room.response(id=player.player_id, message={"deck": player.deck})
