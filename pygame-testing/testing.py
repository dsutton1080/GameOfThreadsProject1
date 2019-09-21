
from gui_functions import *
from gui_classes import BoardSquare, Board, TextBox, Ship
import sys
import pygame
from pygame.locals import *
from functools import reduce
from math import floor

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

pygame.init()
pygame.display.set_caption("Battleship")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ship = Ship(3, 0, 0, (0, 0))

otherCoordsPairsList = [((1,1), 2)]

## display a board with the other placed ships' coordinates filled in
initialBoard = generate_placement_board(otherCoordsPairsList)


def get_hovered_square(pos):
    return get_intersect_object_from_list(pos, initialBoard.squares)


# highlight the updateBoard squares that correspond to each coordinate in the passed in list of coordinates
# just display a new board?
def display_suggestion_placement_board(coordList):
    codePairs = encode_placement_board(coordList, otherCoordsPairsList)
    blit_board(screen, generate_placement_board(codePairs))


def wait_for_click(square):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and square.rect.collidepoint(event.pos):
                return True
            elif event.type == pygame.MOUSEMOTION and not square.rect.collidepoint(event.pos):
                return False


def run_rotate_ship(shipLength, anchorCoord, firstOrientation):
    instructionsTextBoxRotate = TextBox("Use the UP and DOWN arrow keys to rotate your ship.", (96, 10), fontsize=36)
    instructionsTextBoxEnter = TextBox("Press ENTER when you are satisfied with the orientation.", (96, 56), fontsize=36)
    instructionsTextBoxEscape = TextBox("Press the ESC button to cancel placing this ship.", (96, 102), fontsize=36)

    screen.blit(instructionsTextBoxClick.surface, instructionsTextBoxClick.surface.fill(colors['BLACK']).move(instructionsTextBoxClick.window_coord))

    blit_objects(screen, [instructionsTextBoxEnter, instructionsTextBoxRotate, instructionsTextBoxEscape])
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

blit_board(screen, initialBoard)
instructionsTextBoxClick = TextBox("Click an anchor box on the grid. You will then be able to rotate your ship.", (48, 48))
screen.blit(instructionsTextBoxClick.surface, instructionsTextBoxClick.rect)
pygame.display.flip()

def main_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                hoveredSquare = get_hovered_square(event.pos)
                if not hoveredSquare == None:
                    firstOrientation = first_possible_orientation(hoveredSquare.grid_coord, ship.length, [(1, 1)])
                    if not firstOrientation == None:
                        print(firstOrientation)
                        print(hoveredSquare.grid_coord)
                        print(ship.length)
                        suggestionCoords = orientation_to_coord_list(hoveredSquare.grid_coord, ship.length, firstOrientation)
                        print(list(suggestionCoords))
                        display_suggestion_placement_board(suggestionCoords)
                        pygame.display.flip()
                        didClick = wait_for_click(hoveredSquare)
                        if didClick:
                            shipCoords = run_rotate_ship(ship.length, hoveredSquare.grid_coord, firstOrientation)
                            if not shipCoords == None:
                                return shipCoords
                        else:
                            blit_board(screen, initialBoard)
        pygame.time.delay(100)

main_loop()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == MOUSEMOTION:
#             hoveredSquare = get_hovered_square(event.pos)
#             if not hoveredSquare == None:
#                 firstOrientation = first_possible_orientation(hoveredSquare.grid_coord, ship.length, [(1, 1), (1, 2), (1, 3), (1, 4)])
#                 if not firstOrientation == None:
#                     suggestionCoords = orientation_to_coord_list(hoveredSquare.grid_coord, ship.length, firstOrientation)
#                     # highlight(screen, hoveredSquare, colors['GREEN'])
#                     display_suggestion_placement_board(suggestionCoords)
#                     pygame.display.flip()
#                     didClick = wait_for_click(hoveredSquare)
#                     if didClick:
#                         shipCoords = run_rotate_ship(ship.length, hoveredSquare.grid_coord, firstOrientation)
#                         if not shipCoords == None:
#                             print("Return")
#                     else:
#                         blit_board(screen, initialBoard)
#     pygame.time.delay(100)

# pairs = [((1,1), 1), ((1,2), 1), ((1,3),1), ((6,4),2), ((6,5),2), ((6,6), 2)]
# testBoard = generate_placement_board(pairs)
#
# display_suggestion_placement_board([(1, 1), (1, 2), (1, 3)])
# pygame.display.flip()
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
