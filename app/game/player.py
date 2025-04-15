class Player:
    
    def __init__(self, id, player_num, name, username):
        self.player_number : int = player_num 
        self.player_id : str = id
        self.name = name
        self.username = username 
        self.deck : list
        self.selected_card : list = None

    def select_card (self, selected_card: list):
        if selected_card in self.deck :
            for card in selected_card :
                self.selected_card.remove(card)
        else : 
            raise ValueError("player do NOT have that card")

    