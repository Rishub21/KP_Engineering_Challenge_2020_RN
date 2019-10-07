

# Overview & Rules

I’ve created a game of ***Memory*** where any number of players between 1 - 100 can try to create card matches. A match is made when two cards of equal face value have been chosen. **Suite for this game is not considered**. When all the cards have been matched, the player with the most successful matches is declared the winner. Ties are allowed.


# Instructions

Before starting, please expand your terminal to **FULL SCREEN** and **DO NOT RESIZE** during game play. (**You can minimize the terminal however whenever you want**) This is for best performance given the graphics library I used, which is called curses. I do think this is a reasonable tradeoff because it allows for a more seamless game experience


Clone the git repository and cd into the folder. The code runs with **python 2.7**. No external libraries need to be installed. To start game play run the following command in terminal

    python2.7 start.py


To make it easier for you to play a game to completion: I created a cheat argument. If you run

    python2.7 start.py -cheat

The game will actually show the real values of all hidden cards from the beginning. This allows the user to quickly make correct pairs.

To quit please enter
```control + z```
The usual control + c may not work to end the application because of the curses library


# Language Choice and Tooling:

I chose python because it's a syntax light OOP language that I am comfortable with, making it ideal given the time constraints of the challenge.

I chose the curses library because it allowed me to elegantly simulate a game state that changes in place. It also allowed me to add some helpful coloring to the game.

In a larger project I might have utilized a test library like pytest. However, because I just needed to run a few unit tests, I conducted the test procedure myself.

# Tests
To run the tests for the Grid Class, simply run python Grid_Class_Tests.py .

# Design Explanation


## Scaling
When I played Memory as a kid, there was always an inherent issue with scaling the game. If more kids wanted to join, that meant less potential card matches for each kid. And if a lot of kids came, we would either need to find more decks or make kids sit out. To solve this problem, the program will scale the grid size and number of decks used so that even with a large number of players, there are plenty of cards to go around. Example: When there are 2 players, a grid composed of one deck will be used. If there are 99 players, a grid composed of 20 decks will be used. At minimum, a 1:5 deck to player ratio is maintained. I do cap the number of players at 100 given screen size limit.

You will also notice that after every player turn there is a brief 1 second pause enacted. This gives players the time to read the game output.

## OOP Approach
I took an OO approach to this game because it allowed me to keep logic readable and modular. Below is a brief description of what each class does.

**1.  Game Class:**  This class is responsible for running the turn by turn game dynamics. It handles card guessing and matching for each player.

**2.  Grid Class:** This class handles the logic of creating a grid that has enough cards, and is as square like as possible. (We don’t want a lopsided board with drastically different dimensions). It then populates the empty grid randomly with all the available Card instances. This class also handles the printing of the game board so players can see the status of the game after every turn.


**3. Card & Player Classes:** These are two very simple classes that represent the basic card object that makes up the grid as well as the basic player object that plays the game.


**4.  Testing:** The Grid class holds the most intricate computations. Thus, unit tests for it are available in Grid_Class_Tests.py., testing on all possible deck numbers (1-20). Only this range of decks needs to be tested because the total number of players is restricted to 100.


1.  Test_find_closest_perfect_square : ensures that we create a grid with length and width as near each other as possible

2.  Test_generate_empty_grid : ensures that our grid’s number of slots equals the number of cards to be placed

3.  Test_populate_grid : Ensures that we have the right number of each type of card
