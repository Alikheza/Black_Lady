
class Player:
    
    def __init__(self , name, username, id):
        self.player_number : int 
        self.name = name
        self.username = username 
        self.id = id
        self.deck : list
        self.selected_card : list = None

    # def _accept_invite (self,)

    def select_card (self, selected_card: list):
        if selected_card in self.deck :
            for card in selected_card :
                self.selected_card.remove(card)
        else : 
            raise ValueError("player do NOT have that card")

    