from .engine import GameEngine
# from .room import Room

class Game(GameEngine):
    def __init__(self, odd_party = False, total_score : int = 200):

        self.game_players : list = None
        super().__init__(odd_party, total_score)

