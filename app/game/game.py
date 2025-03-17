from .engine import GameEngine 


class Game(GameEngine):
    def __init__(self, odd_party = False, total_score : int = 200):

        self.players : list = None
        self.game_started : bool = False
        self.turn : int = None
        super().__init__(odd_party, total_score)

    async def start_game(self , input: any):
        
        self.dealer()

        for player in self.players:
            await player.select_card(input)
        
        self.exchange(self.players)

        
        for num , player in enumerate(self.players):
            for card in player.deck :
                if card == "C_2":
                    self.turn = num

    def _validate_move(self, move, player_num):
        if self.turn != player_num :
            raise ValueError (f"player with player number :{player_num} have to play")
        if not self.game_started : 
            if move !="C_2" : 
                raise ValueError(f"player with player number :{player_num} have to play C_2")
            else : return 
        else:
            for card in self.players[player_num].deck :
                if card == move :
                    self.players[player_num].deck.remove(move)
                    return 
            raise ValueError(f"player do not have that card")


    def dealer(self) -> None:
        list_card = self._dealer()
        for i, player in enumerate(self.players): 
            player.deck = list_card[i]
        