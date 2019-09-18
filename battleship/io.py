from functools import reduce

# returns an int from 1 to 5
def prompt_num_ships():

# returns a valid string for the name of the player
def prompt_player_name():

# returns a list of filled ships (lists of coordinate pairs (row,col))
# Example: [ [(1,'A'),(1,'B'),(1,'C')], [(6,'C'), (7,'C'), (8,'C')], ... ]
def prompt_fill_ships(numShips):
    return(
        reduce(lambda prevShips, shipLength : prevShips + prompt_fill_ship(prevShips, shipLength),
               range(1,numShips),
               [])
    )

# returns a single ship (a single list of coordinate pairs (row, col))
# Must not overlap coordinates with any coordinates in the 'prevShips' list
def prompt_fill_ship(prevShips, shipLength):

def prompt_guess(prevGuessList):
    return display.onclick

def display_state(dictState):

def prompt_replay_game():