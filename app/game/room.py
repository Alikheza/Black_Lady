from .game import Game

class Room(Game):
    def __init__(self, creator):

        self.id : int 
        self.players : list = [creator.id]
        self.creator : object = creator

    def add_players (self, invited_player) -> None:
        self.players.append(invited_player)
    # def _accept_invite(self, player_id):
        