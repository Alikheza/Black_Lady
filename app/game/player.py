class Player:
    
    def __init__(self, id, player_num, name, username):
        self.player_number : int = player_num 
        self.player_id : str = id
        self.name = name
        self.username = username 
        self.deck : list
        self.selected_card : list = None
        self.player_score : int

    def select_card (self, selected_card: list):
        if selected_card in self.deck :
            for card in selected_card :
                self.deck.remove(card)
        else : 
            raise ValueError("player do NOT have that card")

    def is_suit_absent_for_player(self, suit: str) -> bool:
        return all(not card.startswith(suit + "_") for card in self.deck)
