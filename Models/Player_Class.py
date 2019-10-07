class Player : 
    def __init__(self, player_number):
        self.player_number = player_number
        self.score = 0

    def __cmp__(self, other_player):
        if self.score > other_player.score :
            return -1
        elif self.score < other_player.score:
            return 1
        return 0

    def __str__(self):
        return str(self.player_number)
