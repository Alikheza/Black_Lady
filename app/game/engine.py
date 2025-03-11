from random import shuffle

class GameEngine :

    def __init__(self, odd_party, total_score):

        self.suits = ["H","D","S","C"]
        self.ranks = [str(i) for i in range(1,14)]
        self.odd_p = odd_party
        self.card = self._create_deck() 
        self.score = total_score
        self.game_played = -1

    def _create_deck (self) -> list:
        temp_deck = [suits + "_" + ranks for suits in self.suits for ranks in self.ranks]
        
        if self.odd_p :
            temp_deck.remove("D_2")
        
        for _ in range(10):
            shuffle(temp_deck)

        self.game_played +=1

        return temp_deck
    
    # def _game_finished ()
    