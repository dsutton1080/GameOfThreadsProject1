
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

    :param coordCodePairList: 
    :param encodingContext:
    :param window_location:
    :param width:
    :param height:
    :return:
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
    return Board(window_location, width, height, squares=generate_color_squares(coordCodePairList, encodingContext, window_location, width, height))


# context is either "placement", "guess", or "guessedat"
# 0 should be the default grey value
def code_to_color(context, code):

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
    return get_intersect_object_from_list(pos, board.squares)


def cover_instructions(surface, textbox):
    surface.blit(textbox.surface, textbox.surface.fill(colors['BLACK']).move(textbox.window_coord))


def blit_board(surface, board):
    return blit_objects(surface, board.squares + board.rowLabels + board.colLabels)


def blit_objects(surface, objlist):
    for obj in objlist:
        surface.blit(obj.surface, obj.rect)


def highlight(surface, obj, color):
    obj.surface.fill(color)
    obj.rect = obj.surface.get_rect(x=obj.window_coord[0], y=obj.window_coord[1])
    surface.blit(obj.surface, obj.rect)
    pygame.display.update(obj)


def quit_actions():
    pygame.quit()
    sys.exit()


def is_quit_case(event):
    return event == pygame.QUIT


def get_intersect_object_from_list(pos, ls):
    for obj in ls:
        if obj.rect.collidepoint(pos):
            return obj
    return None


def next_orientation(currentOrientation):
    return (currentOrientation + 1) % 4


def orientation_to_ship_end_coord(anchor, shipLength, orientation):
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
    x, y = coord
    if (x > 0) and (x < 9) and (y > 0) and (y < 9):
        return True
    return False


def is_coord_conflict(coordList1, coordList2):
    for coord in coordList1:
        if coord in coordList2:
            return True
    return False


def is_possible_orientation(anchor, shipLength, orientation, otherFilledCoords):
    return (is_on_board(orientation_to_ship_end_coord(anchor, shipLength, orientation))) and (
        not is_coord_conflict(orientation_to_coord_list(anchor, shipLength, orientation), otherFilledCoords))


def orientation_to_coord_list(anchor, shipLength, orientation):

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
    for i in [0, 1, 2, 3]:
        if is_possible_orientation(anchor, shipLength, i, otherFilledCoords):
            return i
    return None


def coord_to_board_square(board):
    print(board.squares)
    return lambda coord: (filter(lambda s: s.grid_coord == coord, board.squares))[0]
