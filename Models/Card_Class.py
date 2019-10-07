class Card :
    possible_types = [2,3,4,5,6,7,8,9,10,"J","K","Q","A"]
    def __init__(self, val, cheat_mode):
        self.type = val
        self.temp_revealed = False
        self.cheat_mode = cheat_mode
        self.paired = False

    def equals(self,second_card):
        if(self.type == second_card.type):
            return True
        else:
            return False

    def __str__(self):
        if(self.paired):
            return("  ")

        elif(self.cheat_mode or self.temp_revealed):
            if(len(str(self.type)) == 1):
                return (str(self.type) + " ")
            else:
                return str(self.type)

        else:
            return str("X" + " ")
