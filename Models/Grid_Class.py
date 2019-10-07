from Card_Class import Card
from collections import defaultdict
import math
import random
import sys
import curses


class Grid :

    def __init__(self,num_decks, cheat_mode, stdscr):
        self.cheat_mode = cheat_mode
        self.num_decks = num_decks
        self.num_cards = 52 * num_decks
        self.grid = self.populate_grid()
        self.screen = stdscr

    def print_grid(self):
       self.screen.erase()
       self.__print_column_header()
       self.__print_rows()
       self.screen.refresh()

# populates grid with proper number of each card
    def populate_grid(self):
        empty_grid = self.generate_empty_grid()
        card_to_be_placed_dict = defaultdict(Card)
        possible_card_types_available_list = list(Card.possible_types)

        for card_type in possible_card_types_available_list:
            card_to_be_placed_dict[card_type] = 4 * self.num_decks

        for row in empty_grid:
            for col in range(len(row)):
                card_type = self.__generate_random_card_value(possible_card_types_available_list)
                row[col] = Card(card_type, self.cheat_mode)
                card_to_be_placed_dict[card_type] -= 1
                if(card_to_be_placed_dict[card_type] == 0):
                    card_to_be_placed_dict.pop(card_type)
                    possible_card_types_available_list.remove(card_type)
        return empty_grid

    # tries to create as close as perfect square as possible
    def generate_empty_grid(self):
        rows = self.find_closest_perfect_square()
        cols = self.find_closest_perfect_square()

        initial_grid = []

        for i in range(rows):
            new_col_list = [0] * cols
            initial_grid.append(new_col_list)

        left_over_cards = self.num_cards - (self.find_closest_perfect_square() ** 2)
        extra_full_rows = left_over_cards / cols
        left_over_cards = left_over_cards - (extra_full_rows * cols)

        for i in range(extra_full_rows):
            new_col_list = [0] * cols
            initial_grid.append(new_col_list)

        if(left_over_cards > 0):
            new_col_list = [0] * left_over_cards
            initial_grid.append(new_col_list)

        return initial_grid

    def find_closest_perfect_square(self):
        closest_perfect_square = 0
        while( ((closest_perfect_square + 1)** 2) <= self.num_cards):
            closest_perfect_square += 1
        return closest_perfect_square

    def __find_spaces_needed(self,row_number):
        count = 0
        while(row_number >= 10):
            row_number  = row_number / 10
            count += 1
        return count

    def __generate_random_card_value(self, possible_card_val_list):
        random_index =  random.randint(0, len(possible_card_val_list) - 1)
        return possible_card_val_list[random_index]

    def __print_column_header(self):
        max_spaces_needed = self.__find_spaces_needed(len(self.grid)) + 1
        columns_header = []
        divider_header = ["- "] * len(self.grid[0])
        for num in range(len(self.grid[0])):
            if len(str(num)) == 1:
                columns_header.append(str(num) + (1 * " "));
            else:
                columns_header.append(str(num));
        self.screen.addstr(((max_spaces_needed + 2)* " ") + ' '.join(map(str, columns_header)) + '\n')
        self.screen.addstr(((max_spaces_needed + 2)* " ") + ' '.join(map(str, divider_header)) + '\n')

    def __print_rows(self):
        max_spaces_needed = self.__find_spaces_needed(len(self.grid)) + 1
        for row_count, row in enumerate(self.grid):
            spaces_needed = max_spaces_needed - (self.__find_spaces_needed(row_count))
            self.screen.addstr(str(row_count) + (((spaces_needed * " ") + "|")))
            for card in row:
                if(card.temp_revealed):
                    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
                    self.screen.addstr(str(card), curses.color_pair(1))
                    self.screen.addstr(" ")
                else:
                    self.screen.addstr(str(card) + " ")
            self.screen.addstr('\n')
