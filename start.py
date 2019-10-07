from Models.Game_Class import Game
import argparse
import sys
import time
import curses
from curses import wrapper

parser = argparse.ArgumentParser()
parser.add_argument('-cheat', action='store_true')
args = parser.parse_args()
stdscr = curses.initscr()


def graphic():
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    var = """\

  /\/\   ___ _ __ ___   ___  _ __ _   _
 /    \ / _ \ '_ ` _ \ / _ \| '__| | | |
/ /\/\ \  __/ | | | | | (_) | |  | |_| |
\/    \/\___|_| |_| |_|\___/|_|   \__, |
                                  |___/

                    """
    for line in var.splitlines():
        stdscr.addstr(line + "\n",curses.color_pair(1))

    #print(curses.has_colors() )
    stdscr.addstr("Hey guys, lets play a game of Memory! (Please make sure your terminal is expanded to full screen. Otherwise we won't be able to play the game properly!)\n" )
    stdscr.addstr("Rules are simple. Each player guesses two cards and if they are same value, that's a match. The player with the most matches by the time all cards are revealed wins! \n")
    stdscr.addstr("\nTell me how many players you have. You can have as few as 1 or as many as a 100!")
    stdscr.refresh()

def main(stdscr):

    stdscr.clear()
    curses.start_color()

    graphic()

    curses.echo()
    number_players = get_valid_answer()

    game = Game(number_players, args.cheat,stdscr)
    game.run_game()

def get_valid_answer():

    while True:
        valid_answer = (stdscr.getstr())

        try:
            if(int(valid_answer) >  0 and int(valid_answer) <= 100):
                valid_answer = int(valid_answer)
                break
            else:
                try_again()
        except:
            try_again()
    return valid_answer

def try_again():
    stdscr.erase();
    graphic()
    stdscr.addstr("\nSorry,one more time, I need a valid integer between 1 and 100 inclusive \n")
    stdscr.refresh()


if __name__ == "__main__":
    wrapper(main)
