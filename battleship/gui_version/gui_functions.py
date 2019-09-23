
from utils import flatten, colors, SCREEN_WIDTH, SCREEN_HEIGHT
import sys
import pygame
from gui_classes import BoardSquare, Board, TextBox, Ship


def ship_length_to_name(length):
    mapping = {
        1: "submarine",
        2: "destroyer",
        3: "cruiser",
        4: "battleship",
        5: "carrier"
    }
    return mapping[length]


def hit(guess, ships):
    return guess in flatten(ships)


def which_sunk(guess, guesses, ships):
    """
    Returns a list of coordinates for a sunken ship given a guess coordinate and past guesses.
    :param guess: coordinate
    :param guesses: a list of previous guesses
    :param ships: a list of list of coordinates that the guesses are "attacking"
    :return: a list of coordinates (a ship) or None
    """
    targetShip = flatten(list(filter(lambda s: guess in s, ships)))
    if all(map(lambda c: c in [guess] + guesses, targetShip)):
        return len(targetShip)
    return None


def encode_guess_board(guesses, otherShips):
    """
    Pairs a list of guess coordinates with their color-encoding values for displaying a board.
    :param guesses: a list of coordinates
    :param otherShips: a list of lists of coordinates representing the "attacked" ships
    :return: a list of (coordinate, code) pairs
    """
    otherShipCoords = flatten(otherShips)

    def map_func(g):
        if g in otherShipCoords:
            return (g, 2)
        else:
            return (g, 1)
    return list(map(map_func, guesses))


def encode_guessed_at_board(guesses, ships):
    """
    Pairs a list of guessed-at coordinates with their color-encoding values for displaying a board.
    :param guesses: a list of coordinates
    :param ships: a list of lists of coordinates representing the "attacked" ships
    :return: a list of (coordinate, code) pairs
    """
    shipCoords = flatten(ships)
    allCoords = [(row, col) for row in range(1, 9) for col in range(1, 9)]

    def map_func(c):
        if c in guesses:
            if c in shipCoords:
                return (c, 3)
            else:
                return (c, 1)
        elif c in shipCoords:
            return (c, 2)
        else:
            return (c, 0)

    return list(map(map_func, allCoords))


def encode_placement_board(suggestionCoords, otherShipCoords):
    """
    Returns a list of coordinates with color codes used to update the placement board on each placement iteration.
    :param suggestionCoords: a list of the coordinates being targeted
    :param otherShipCoords: a list of the other coordinates already placed
    :return: a list of (coordinate, code) pairs
    """
    return list(map(lambda c: (c, 1), suggestionCoords)) + list(map(lambda c: (c, 2), otherShipCoords))


def generate_placement_board(coordCodePairList):
    """
    Uses a list of encoded coordinate pairs to generate a displayable board object used when placing ships.
    :param coordCodePairList: a list of encoded coordinate pairs
    :return: a Board object with colored squares
    """
    window_location = ((SCREEN_WIDTH / 3), (SCREEN_HEIGHT / 6))
    width = (SCREEN_WIDTH / 2)
    height = (SCREEN_HEIGHT * (2 / 3))
    return board_from_coord_code_pairs(coordCodePairList, "placement", window_location, width, height)


def generate_guess_board(coordCodePairList):
    """
    Uses a list of encoded coordinate pairs to generate a displayable board object used when guessing ships.
    :param coordCodePairList: a list of encoded coordinate pairs
    :return: a Board object with colored squares
    """
    width = (7 / 16) * SCREEN_WIDTH
    height = (1 / 2) * SCREEN_HEIGHT
    window_location = (30, SCREEN_HEIGHT / 4)
    return board_from_coord_code_pairs(coordCodePairList, "guess", window_location, width, height)


def generate_guessed_at_board(coordCodePairList):
    """
    Uses a list of encoded coordinate pairs to generate a displayable board object used to show the other team's attacks
    :param coordCodePairList: a list of encoded coordinate pairs
    :return: a Board object with colored squares
    """
    width = (7 / 16) * SCREEN_WIDTH
    height = (1 / 2) * SCREEN_HEIGHT
    window_location = (SCREEN_WIDTH - 30 - width, SCREEN_HEIGHT / 4)
    return board_from_coord_code_pairs(coordCodePairList, "guessed_at", window_location, width, height)


def generate_color_squares(coordCodePairList, encodingContext, window_location, width, height):
    """
    This function uses multiple parameters to generate squares that will be used to display a board.
    :param coordCodePairList: the list of the coordinate, code pairs that encode the creation of the board squares
    :param encodingContext: The type of board context that indicates the way the board squares are created
    :param window_location: The window coordinates for the future board
    :param width: The board width where the squares will be displayed
    :param height: The board height where the squares will be displayed
    :return: a list of all the squares that will fill a board
    """
    offset = SCREEN_HEIGHT / 400
    squareWidth = (width / 9) - offset
    squareHeight = (height / 9) - offset
    x, y = window_location

    def targetCode(curCoord):
        for coord, code in coordCodePairList:
            if coord == curCoord:
                return code
        return 0

    squares = []
    offsetY = 0
    row = 1
    for rowY in [(y + (squareHeight * i)) for i in range(1, 9)]:
        offsetX = 0
        col = 1
        for colX in [(x + (squareWidth * i)) for i in range(1, 9)]:

            squares = squares + [
                BoardSquare((row, col), (colX + offsetX, rowY + offsetY), squareWidth, squareHeight, color=code_to_color(encodingContext, targetCode((row, col))))]
            col += 1
            offsetX += offset
        row += 1
        offsetY += offset
    return squares


# Takes a list of (coord, colorCode) pairs and a location to draw the board and generates a new board with colored squares
def board_from_coord_code_pairs(coordCodePairList,
                                 encodingContext,
                                 window_location,
                                 width,
                                 height):
    """
    This function uses multiple parameters to generate squares that will display the board. It is essentially a wrapper to
    :param coordCodePairList: the list of the coordinate, code pairs that encode the creation of the board squares
    :param encodingContext: The type of board context that indicates the way the board squares are created
    :param window_location: The window coordinates for the future board
    :param width: The board width
    :param height: The board height
    :return: a board with colored squares
    """
    return Board(window_location, width, height, squares=generate_color_squares(coordCodePairList, encodingContext, window_location, width, height))


# context is either "placement", "guess", or "guessedat"
# 0 should be the default grey value
def code_to_color(context, code):
    """
    Based on the context, it will decode the code into an RGB code
    :param context: a string representing the type of board being displayed
    :param code: a single digit integer
    :return: an RGB value for a color
    """

    mapping = {
       "placement": {
           0: colors['GREY'],     # Default. Not filled or suggested.
           1: colors['GREEN'],    # Suggested placement
           2: colors['BLUE']      # Already filled by another placed ship
       },
        "guess": {
            0: colors['GREY'],  # Not guessed
            1: colors['RED'],   # Missed
            2: colors['GREEN']  # Hit
        },
        "guessed_at": {
            0: colors['GREY'],         # Not guessed
            1: colors['LIGHT-RED'],    # They missed our ship
            2: colors['BLUE'],         # Our ship, not guessed
            3: colors['DARK-RED']      # Our ship, they hit
        }
    }
    return mapping[context][code]


def get_hovered_square(pos, board):
    """
    Returns a BoardSquare object that is being hovered on.
    :param pos: The window position coordinates
    :param board: The Board object where the square resides
    :return: A BoardSquare object
    """
    return get_intersect_object_from_list(pos, board.squares)


def cover_instructions(surface, textbox):
    """
    Draws over a textbox to make it disappear.
    :param surface: The pygame Surface object to draw on.
    :param textbox: The TextBox object to cover.
    :return: void
    """
    surface.blit(textbox.surface, textbox.surface.fill(colors['BLACK']).move(textbox.window_coord))


def blit_board(surface, board):
    """
    Draws a Board object on a pygame Surface object.
    :param surface: a pygame Surface object
    :param board: a Board object
    :return: void
    """
    return blit_objects(surface, board.squares + board.rowLabels + board.colLabels)


def blit_objects(surface, objlist):
    """
    Draws a list of objects on a pygame Surface object
    :param surface: a pygame Surface object
    :param objlist: a list of objects with surface and rect attributes
    :return: void
    """
    for obj in objlist:
        surface.blit(obj.surface, obj.rect)


def highlight(surface, obj, color):
    """
    Colors an object and draws it on a Surface
    :param surface: a pygame Surface object
    :param obj: an object with surface and rect attributes
    :param color: an RGB tuple
    :return: void
    """
    obj.surface.fill(color)
    obj.rect = obj.surface.get_rect(x=obj.window_coord[0], y=obj.window_coord[1])
    surface.blit(obj.surface, obj.rect)
    pygame.display.update(obj)


def get_intersect_object_from_list(pos, ls):
    """
    Scans a list of objects and returns the list of objects that is targeted by a given position.
    :param pos: a window coordinate
    :param ls: a list of displayable objects
    :return: a displayable object or None
    """
    for obj in ls:
        if obj.rect.collidepoint(pos):
            return obj
    return None


def next_orientation(currentOrientation):
    """
    Returns the incremented orientation code (mod 4).
    :param currentOrientation: an integer encoding (1 - 3)
    :return: an integer (1 - 3)
    """
    return (currentOrientation + 1) % 4


def orientation_to_ship_end_coord(anchor, shipLength, orientation):
    """
    Given an orientation encoding and the length of a ship, returns a coordinate at the end of the ship
    :param anchor: The starting coordinate of the ship
    :param shipLength: An integer 1-5
    :param orientation: An integer code 0-3
    :return: A coordinate representing the end of the ship
    """
    orientation = orientation % 4
    row, col = anchor
    mapping = {
        0: (row + shipLength - 1, col),
        1: (row, col + shipLength - 1),
        2: (row - shipLength + 1, col),
        3: (row, col - shipLength + 1)
    }
    return mapping[orientation]


def is_on_board(coord):
    """
    Checks to see whether a coordinate is a valid coordinate for our playing board
    :param coord: a (row, col) coordinate
    :return: boolean
    """
    x, y = coord
    if (x > 0) and (x < 9) and (y > 0) and (y < 9):
        return True
    return False


def is_coord_conflict(coordList1, coordList2):
    """
    Used when placing ships. Returns whether or not there is a coordinate conflict between list of coordinates (ships).
    :param coordList1: A list of coordinates
    :param coordList2: A list of coordinates
    :return: boolean
    """
    for coord in coordList1:
        if coord in coordList2:
            return True
    return False


def is_possible_orientation(anchor, shipLength, orientation, otherFilledCoords):
    """
    Checks whether a ship orientation is valid to place.
    :param anchor: The start coordinate of the ship.
    :param shipLength: An integer 1-5.
    :param orientation: An orientation code integer 0-3
    :param otherFilledCoords: The list of other coordinates to check against
    :return: boolean
    """
    return (is_on_board(orientation_to_ship_end_coord(anchor, shipLength, orientation))) and (
        not is_coord_conflict(orientation_to_coord_list(anchor, shipLength, orientation), otherFilledCoords))


def orientation_to_coord_list(anchor, shipLength, orientation):
    """
    Generates the list of coordinates.
    :param anchor: The start coordinate of the ship.
    :param shipLength: An integer 1-5.
    :param orientation: An orientation code integer 0-3
    :return: a list of coordinates representing a ship
    """
    row, col = anchor
    endRow, endCol = orientation_to_ship_end_coord(anchor, shipLength, orientation)

    l = [anchor]

    if orientation == 0:
        return l + list(map(lambda i: (i, col), range(row + 1, row + shipLength)))
    elif orientation == 1:
        return l + list(map(lambda j: (row, j), range(col + 1, col + shipLength)))
    elif orientation == 2:
        return l + list(map(lambda i: (i, col), range(row - shipLength + 1, row)))
    else:
        return l + list(map(lambda j: (row, j), range(col - shipLength + 1, col)))


# returns an orientation code 0-3, otherwise returns None if not possible
def first_possible_orientation(anchor, shipLength, otherFilledCoords):
    """
    Returns the first possible orientation code for an anchor point.
    :param anchor: The start coordinate for the ship.
    :param shipLength: An integer 1-5.
    :param otherFilledCoords: A list of other coordinates to disallow
    :return: an orientation code 0-3
    """
    for i in [0, 1, 2, 3]:
        if is_possible_orientation(anchor, shipLength, i, otherFilledCoords):
            return i
    return None
