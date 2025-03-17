from .game import Game
import string
from secrets import choice

class Room(Game):
    def __init__(self):

        self.id = self._id_generator()
        self.players : list 
        self.creator : object 

    def _id_generator(self):
        characters = string.ascii_letters + string.digits
        random_id = ''.join(choice(characters) for _ in range(6))
        return random_id

    def add_players (self, invited_player) -> None:
        self.players.append(invited_player)
    # def _accept_invite(self, player_id):
        