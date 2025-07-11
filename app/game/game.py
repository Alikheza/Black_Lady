from .engine import GameEngine 
from .player import Player


class Game(GameEngine):
    
    def __init__(self):
        self.players : list["Player"] = []
        self.game_started : bool = False
        self.turn : int = None
        self.first_move : bool = False
        self.is_heart_broken : bool = False
        self.ground: dict[int, str] = {}  
        self.score_bord : dict[int, int] = {0:0,1:0,2:0,3:0}
        super().__init__()

    def _start_game(self):
        if len(self.players)==3 :
            self.odd_p = True 
            self.score_bord.pop(3)
        else: False
            
        self.game_turn = (self.game_turn + 1 ) % len(self.players)

        self.exchange(self.players)

        self.game_started = True
        
        for num , player in enumerate(self.players):
            for card in player.deck :
                if card == "C_2":
                    self.turn = num
                    return num
                
    def _validate_move(self, move, player_num):
        if not self.is_heart_broken and len(self.ground) > 0 and move.startswith("H_"):
            player = self.players[player_num]
            player_has_no_non_heart_cards = all(player.is_suit_absent_for_player(suit) for suit in self.suits if suit != "H")
            if not player_has_no_non_heart_cards:
                raise ValueError("You cannot play a heart until it is broken.")
        if move.startswith("H_") : self.is_heart_broken = True

        if self.turn != player_num:
            raise ValueError(f"It's not player {player_num}'s turn.")

        if not self.first_move:
            if move != "C_2":
                raise ValueError("The first move must be C_2.")
            self.first_move = True

        if move not in self.players[player_num].deck:
            raise ValueError("Player does not have that card.")
        
        self.players[player_num].deck.remove(move)
        
    def dealer(self) -> None:
        list_card = self._dealer()
        for i, player in enumerate(self.players): 
            player.deck = list_card[i]
    
    def validate_move(self, move, player_num):
        self._validate_move(move, player_num)
        if len(self.ground) == 0 :
            self.ground[player_num] = move
        else:
            suit = move.split("_")[0]
            if not self.ground.values()[0].startwith(suit+"_"):
                player = self.players[player_num]
                if not player.is_suit_absent_for_player(suit):
                    raise ValueError(f"invalid move you have an {suit}")
            self.ground[player_num] = move
            if len(self.ground) == 4 :
                self.handleScore()
        return True

    def handleScore(self):

        suit, max_val = list(self.ground.values())[0].split("_")
        max_val = int(max_val)
        player_with_max_value = list(self.ground.keys())[0]
        negetive_value = 1 if suit == "H" else 0

        for player_id, card_str in self.ground.items():
            card_suit, card_val = card_str.split("_")
            card_val = int(card_val)
            if card_suit != suit:
                if card_suit == "H":
                    negetive_value += 1
                elif card_suit == "S" and card_val == 12:  # Queen of Spades
                    negetive_value += 13 if not self.odd_p else 17
            elif card_val > max_val:
                max_val = card_val
                player_with_max_value = player_id
                if suit == "H" : 
                    negetive_value+=1

        for player in self.players:
            if player.player_number == player_with_max_value:
                player.player_score += negetive_value
                self.score_bord[player_with_max_value] += negetive_value
                

        self.ground.clear()
        self.turn = player_with_max_value            