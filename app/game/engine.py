from random import shuffle

class GameEngine :

    def __init__(self):
        self.suits = ["H","D","S","C"]
        self.ranks = [str(i) for i in range(2,15)]
        self.odd_p = False
        self.card = self._create_deck() 
        self.game_turn = -1
        

    def _create_deck (self) -> list:
        temp_deck = [suits + "_" + ranks for suits in self.suits for ranks in self.ranks]
        
        if self.odd_p :
            temp_deck.remove("D_2")
        
        for _ in range(10):
            shuffle(temp_deck)


        return temp_deck
    
    def _dealer(self) -> list:
        if self.odd_p :
            list_card = [self.card[:17] , self.card[17:34], self.card[34:]]  
        else : 
            list_card = [self.card[:13] , self.card[13:26], self.card[26:39],[self.card[39:]]]
        return list_card
    
    def exchange(self, player_list:list):
        if self.odd_p and self.game_turn==2 : return

        elif self.game_turn == 3: return 
        
        for player in player_list :
            if player.selected_card == None :
                raise Exception(f"player {player.name} did not select any card")

        if self.odd_p:
            match self.game_turn:
                case 0:
                    for i in range(3):
                        player_list[i].deck.append(player_list[(i-1)%3].selected_card)
                case 1:
                    for i in range(4):
                        player_list[i].deck.append(player_list[(i+1)%3].selected_card)
        else:
            match self.game_turn:
                case 0:
                    for i in range(4):
                        player_list[i].deck.append(player_list[(i-1)%4].selected_card)
                case 1:
                    for i in range(4):
                        player_list[i].deck.append(player_list[(i+1)%4].selected_card)
                case 2 :
                    for i in range(2):
                        player_list[i].deck.append(player_list[i+2].selected_card)
                        player_list[i+2].deck.append(player_list[i].selected_card)