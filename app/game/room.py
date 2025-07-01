from .game import Game
from .player import Player
from secrets import choice
import string


class Room(Game):
    def __init__(self):
        super().__init__()
        self.id = self._id_generator()
        self.leadr : Player
        self.game_played_count : int = 0 
        self.game_played : dict [self.game_played_count:list[tuple[int,int]]] = {}
        

    def _id_generator(self):
        characters = string.ascii_letters + string.digits
        random_id = ''.join(choice(characters) for _ in range(6))
        return random_id

    def add_players (self, player) -> None:
        if self.players == []:
            self.leadr = player
        self.players.append(player)
    
    def start_game(self):
        super()._start_game()
        for player in self.players :
            player.select_card = None