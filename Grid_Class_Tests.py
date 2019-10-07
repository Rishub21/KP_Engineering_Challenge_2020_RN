from Models.Grid_Class import Grid
from Models.Card_Class import Card
import curses


def test_find_closest_perfect_square(num_decks):
    test_grid = Grid(num_decks, False, None)
    closest_perfect_square = test_grid.find_closest_perfect_square()
    return (closest_perfect_square ** 2 <= num_decks * 52 and ((closest_perfect_square + 1) ** 2 > num_decks * 52))

def test_generate_empty_grid(num_decks):
    test_grid = Grid(num_decks, False, None)
    num_cards = 0
    for i in range(len(test_grid.grid)):
        num_cards += len(test_grid.grid[i])
    return ( num_cards == num_decks * 52)


def test_populate_grid(num_decks):
    test_grid = Grid(num_decks, False, None)  
    number_each_card_dict = dict.fromkeys(Card.possible_types, 0)

    for row in test_grid.grid:
        for col in row:
            number_each_card_dict[col.type] += 1
    for key in number_each_card_dict:
        if(number_each_card_dict[key] != num_decks * 4):
            return Faalse
    return True

allClear = True
for i in range(20):
    if(not test_find_closest_perfect_square(i + 1)):
        print ("problem with closest square at " + str(i + 1) + " decks")
        allClear = False
    if(not test_generate_empty_grid(i + 1)):
        print ("problem with empty grid " + str(i + 1) + " decks")
        allClear = False
    if(not test_populate_grid(i + 1)):
        print ("problem with populate grid " + str(i + 1) + " decks")
        allClear = False

if(allClear):
    print("ALL TESTS PASSED")
