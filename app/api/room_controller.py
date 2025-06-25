from .connection import RoomConnectionManager
from ..core import heartBeat
from ..game.player import Player

async def invite_player(username: str, player_id: str, room: RoomConnectionManager) -> None:
    """
    Handle player invitation to a game room.
    Sends appropriate response based on player's availability.
    """
    if room.game_started == True : 
        await room.response(id=player_id,message={"message":"invalid action (you are in a game)"})
        return

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

async def card_dealer(room: RoomConnectionManager):
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
    
    await room.broadcast(message={"message":"chose your card to exchange"})

async def check_player_seleted_card (room: RoomConnectionManager) :
    Not_selected = []
    for player in room.players:
        if player.selected_card == None :
            await room.response(message={"message":"chose your card to exchange"})
            Not_selected.append(player.name)
    return Not_selected