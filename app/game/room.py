import string
import asyncio
from secrets import choice
from .game import Game
from .player import Player
from ..core import presence_tracker

class Room(Game):
    def __init__(self):
        super().__init__()
        self.id = self._id_generator()
        self.leadr : Player
        self.game_played_count : int = 0 
        self.game_played : dict [self.game_played_count : list[tuple[int,int]]] = {}
        self.game_queue = asyncio.Queue()

    def _id_generator(self):
        characters = string.ascii_letters + string.digits
        random_id = ''.join(choice(characters) for _ in range(6))
        return random_id

    def add_players (self, player) -> None:
        player_count = len(self.players)
        if player_count == 0:
            self.leadr = player
        self.players.append(player)
        player.player_number = player_count + 1
    
    def remove_player(self, player) -> None :

        self.players.remove(player)

        for p in self.players :
            if p.player_number > player.player_number :
                message = {
                    "type" : "room_update",
                    "action" : "update_player_numebr",
                    "payload" : {
                        "update_player_number" : p.player_number - 1 
                    }
                }
                p.player_number -= 1
                presence_tracker.push_notification(username = p.username, message = message)

    
    def start_game(self):
        player_number = super()._start_game() + 1
        for player in self.players :
            player.select_card = None
        return player_number
    
    def game_update (self,) :
        
        # for player

        message = {
            "type" : "game_update",
            "payload" : {
                "score_bord" : {
                    
                } 
            } 
        }
        self.game_queue.put_nowait(message)