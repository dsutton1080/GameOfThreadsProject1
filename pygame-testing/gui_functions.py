
import sys
import pygame
from gui_classes import BoardSquare, Board, TextBox, Ship


colors = {
    "GREY": (122, 119, 111),
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "GREEN": (0, 255, 0),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0)
}


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

### GENERAL


def generate_color_squares(coordColorPairList, encodingContext, window_location, width, height):
    offset = SCREEN_HEIGHT / 400
    squareWidth = (width / 9) - offset
    squareHeight = (height / 9) - offset
    x, y = window_location

    def targetCode(curCoord):
        for coord, code in coordColorPairList:
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
                BoardSquare((row, col), (colX + offsetX, rowY + offsetY), squareWidth, squareHeight, color=code_to_color(encodingContext, targetCode(row, col)))]
            col += 1
            offsetX += offset
        row += 1
        offsetY += offset
    return squares


# Takes a list of (coord, colorCode) pairs and a location to draw the board and generates a new board with colored squares
def board_from_coord_color_pairs(coordColorPairList,
                                 encodingContext,
                                 window_location,
                                 width,
                                 height):
    return Board(window_location, width, height, squares=generate_color_squares(coordColorPairList, encodingContext, window_location, width, height))


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
                # code1: colors['GREY']  # Not guessed
                # code2: colors['RED']   # Missed
                # code3: colors['GREEN'] # Hit
            },
            "guessedat": {
                # code1: colors['GREY'] # Not guessed
                # code2: colors['RED']  # Missed
                # code3: colors['BLUE'] # Our ship, not guessed
                # code4: colors['ORANGE'] # Our ship, they hit
            }

        }
        return mapping[context][code]


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
    row, col = anchor
    mapping = {
        0: (row + shipLength, col),
        1: (row, col + shipLength),
        2: (row - shipLength, col),
        3: (row, col - shipLength)
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
    def abs_range(a, b):
        if a > b:
            return range(b, a)
        else:
            return range(a, b)

    row, col = anchor
    endRow, endCol = orientation_to_ship_end_coord(anchor, shipLength, orientation)

    rowRange = abs_range(row, endRow)
    colRange = abs_range(col, endCol)

    if not rowRange:
        return map(lambda c: (row, c), colRange)
    else:
        return map(lambda r: (r, col), rowRange)


# returns an orientation code 0-3, otherwise returns None if not possible
def first_possible_orientation(anchor, shipLength, otherFilledCoords):
    for i in [0, 1, 2, 3]:
        if is_possible_orientation(anchor, shipLength, i, otherFilledCoords):
            return i
    return None


def coord_to_board_square(board):
    print(board.squares)
    return lambda coord: (filter(lambda s: s.grid_coord == coord, board.squares))[0]
