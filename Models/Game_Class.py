from Grid_Class import Grid
from Player_Class import Player
import math
import sys
import time
import curses
from copy import deepcopy


class Game :
    def __init__(self, number_of_players, cheat_mode, stdscr):
        # as a heuristic we are saying that there should be a deck for every 5 people
        self.number_of_players = number_of_players
        self.number_decks_needed = self.__get_number_decks_needed(5)
        self.state = Grid(self.number_decks_needed, cheat_mode,stdscr)
        self.player_list = self.__get_player_list()
        self.screen = stdscr
        self.num_cards_paired = 0

    # runs the logic of the whole game
    def run_game(self):
        game_finished = False
        self.state.print_grid()
        while (not game_finished):
            count_of_player_num = 1
            while count_of_player_num <= self.number_of_players:
                if(self.num_cards_paired == self.state.num_cards):
                    self.__announce_winners()
                    time.sleep(5)
                    game_finished = True
                    break
                else:
                    self.take_turn(count_of_player_num)
                count_of_player_num += 1

    # runs the logic of each turn
    def take_turn(self, count_of_player_num):

        location1 =  self.ask_Card_Guess(count_of_player_num, "first")
        row1, col1 = location1[0], location1[1]

        self.state.grid[row1][col1].temp_revealed = True

        location2 =  self.ask_Card_Guess(count_of_player_num, "second")
        row2, col2 = location2[0], location2[1]

        self.state.grid[row2][col2].temp_revealed = True

        card1 = self.state.grid[row1][col1]
        card2 = self.state.grid[row2][col2]

        self.__compare_cards(card1,card2, count_of_player_num)

        self.__wait_til_enter()

        card1.temp_revealed = False
        card2.temp_revealed = False


    def ask_Card_Guess(self, count_of_player_num, number_guess):
        invalid_guess = True
        equal_to_first_guess = False
        already_matched = False

        while(invalid_guess):
            if(equal_to_first_guess):
                self.__screen_print("\n Hmm... you already chose that card. Press enter and then you will be able to pick a new card")
                equal_to_first_guess = False
                self.__wait_til_enter()

            elif(already_matched):
                self.__screen_print("\n Hmm... that card has already been matched, let's try again.Press enter and then you will be able to pick a new card")
                already_matched = False
                self.__wait_til_enter()

            self.__screen_print("\nPlayer %s , what is your %s card row?" % (count_of_player_num,number_guess))

            guess_row = self.__get_valid_answer("row")

            while((not isinstance(guess_row, int)) or guess_row >= len(self.state.grid) or guess_row < 0):
                    self.__screen_print("\nPlayer %s , Hmm.. That was an invalid row entry, please enter another %s card row?" %(count_of_player_num,number_guess))
                    guess_row = self.__get_valid_answer("row")

            self.__screen_print("\nPlayer %s , what is your %s card column?" %(count_of_player_num,number_guess))
            guess_col = self.__get_valid_answer("column")

            while((not isinstance(guess_col, int)) or guess_col >= len(self.state.grid[guess_row]) or guess_col < 0):
                self.__screen_print("\nPlayer %s , Hmm.. That was an invalid column entry, please enter another %s card column?" %(count_of_player_num,number_guess))
                guess_col = self.__get_valid_answer("column")

            if(self.state.grid[guess_row][guess_col].temp_revealed):
                equal_to_first_guess = True
            elif(self.state.grid[guess_row][guess_col].paired):
                already_matched = True
            else:
                invalid_guess =  False

        return [guess_row, guess_col]

    def __announce_winners(self):
        list.sort(self.player_list)

        best_score = self.player_list[0].score
        best_score_list = []
        pointer = 0

        while(pointer < len(self.player_list) and self.player_list[pointer].score == best_score):
            best_score_list.append(self.player_list[pointer])
            pointer += 1

        if(len(best_score_list) == 1):
            self.__screen_print("Our winner is Player " + str(best_score_list[0]))
        else:
            self.__screen_print("Our winners are:  \n")
            for player in best_score_list:
                self.screen.addstr(" Player " + str(player) + " ")
        self.screen.addstr("\nThanks for playing!")
        self.screen.refresh()

    def __compare_cards(self, card1, card2, count_of_player_num):
        if(card1.type == card2.type ):
            self.player_list[count_of_player_num - 1].score += 1
            self.__screen_print("\n NICE! THAT'S A MATCH! Next Player Up! Please Press Enter to continue ")
            card1.paired = True
            card2.paired = True
            self.num_cards_paired += 2
        else:
            self.__screen_print("\n SORRY, NO MATCH. Next Player Up! Please Press Enter to continue")

    def __get_number_decks_needed(self, number_people_per_deck):
        number_decks_needed = int(math.ceil(float(self.number_of_players) / number_people_per_deck))
        return number_decks_needed

    def __get_player_list(self):
        player_list = []
        for player_num in range(self.number_of_players):
            player_list.append(Player(player_num + 1))
        return player_list

    def __print_player_scores(self):

        self.screen.addstr("\n Top Player Scores \n")
        sorted_players = (deepcopy(self.player_list))
        sorted_players.sort()
        for index, player in enumerate(sorted_players):
            if(index >= 5):
                break
            self.screen.addstr("Player " + str(player.player_number)  + ": ")
            self.screen.addstr(str(player.score), curses.A_UNDERLINE)
            self.screen.addstr(" | ")
        self.screen.addstr('\n')

    def __get_valid_answer(self, str):
        while True:
            try:
                valid_answer = int(self.screen.getstr())
                break
            except :
                self.__screen_print("\n Sorry, please enter a valid integer for " + str)
        return valid_answer

    def __screen_print(self,prompt):
        self.screen.erase()
        self.state.print_grid();

        self.__print_player_scores()
        if( "Next Player Up!" in prompt):
            if("NICE!" in prompt):
                curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_WHITE)
            else:
                curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
            self.screen.addstr(prompt,curses.color_pair(1))

        else:
            self.screen.addstr(prompt)
        self.screen.refresh()
    def __wait_til_enter(self):
        while True:
            c = self.screen.getch()
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                break
