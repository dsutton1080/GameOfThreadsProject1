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

imageBattleshipSurface = pygame.image.load('battleship-1200x900.jpg').convert()
blackBackground = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


def run_start():
    screen.blit(imageBattleshipSurface, (0, 0))

    battleshipTextBox = TextBox("Battleship!", (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 4), fontsize=96)
    screen.blit(battleshipTextBox.surface, battleshipTextBox.rect)

    instructionsTextBox = TextBox("Press the SPACE bar to play", (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2), fontsize=48)
    screen.blit(instructionsTextBox.surface, instructionsTextBox.rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


# returns the number of ships
def run_get_number_ships():
    # define background, instruction, box for each number of ships
    def create_number_boxes():
        def create_number_box(j):
            x = SCREEN_WIDTH / 5
            y = SCREEN_HEIGHT - (SCREEN_HEIGHT / 3)
            return TextBox("{}".format(j), ((x * j) - 128, y), fontsize=128)
        return reduce(lambda others, j: others + [create_number_box(j)], [1, 2, 3, 4, 5], [])


    instructionsTextBox = TextBox("Click the number of ships to play with:", (SCREEN_WIDTH / 7, SCREEN_HEIGHT / 3), fontsize=64)
    numberBoxes = create_number_boxes()

    # draw background
    screen.blit(imageBattleshipSurface, (0, 0))

    # draw instruction
    screen.blit(instructionsTextBox.surface, instructionsTextBox.rect)

    # draw number boxes
    for box in numberBoxes:
        screen.blit(box.surface, box.rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in [1, 2, 3, 4, 5]:
                    if numberBoxes[i - 1].rect.collidepoint(event.pos):
                        return i


# Returns a list of lists of (row, col) coordinates. Example: [[(1,1), (1,2), (1,3)], [(3,3), (4,3)], [(8,8)]]
def run_place_ships(numShips):

    # define the board to place on
    placeBoard = Board(((SCREEN_WIDTH / 3), (SCREEN_HEIGHT / 6)), (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * (2 / 3)))

    instructionsTextBox1 = TextBox("Click a blue ship on the left to select it for placement.", (48, 48))

    def ship_size_to_coord(size):
        queueWidth = SCREEN_WIDTH / 3
        queueHeight = SCREEN_HEIGHT * (2 / 3)
        queueX = SCREEN_WIDTH / 8
        queueY = SCREEN_HEIGHT / 4

        firstColX = queueX
        firstRowY = queueY

        secondColX = queueX + (queueWidth * (1 / 3))

        switch = {
            1: (firstColX,  firstRowY),
            2: (firstColX,  firstRowY + (placeBoard.squareHeight * 2)),
            3: (firstColX,  firstRowY + (placeBoard.squareHeight * 5)),
            4: (secondColX, firstRowY),
            5: (secondColX, firstRowY + (placeBoard.squareHeight * 5))
        }
        return switch[size]

    # define ship surfaces based on numShips - they sit to the left of the board

    def create_ship_queue(n):
        return reduce(lambda prevs, i: prevs + [Ship(i, placeBoard.squareWidth - 1, placeBoard.squareHeight - 1, ship_size_to_coord(i))], range(1, n+1), [])

    shipQueue = create_ship_queue(numShips)

    # draw initial state
    pygame.display.flip()
    screen.blit(blackBackground, blackBackground.get_rect())
    blit_objects(screen, placeBoard.squares + placeBoard.rowLabels + placeBoard.colLabels)
    blit_objects(screen, shipQueue)
    screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)

    def get_clicked_ship(pos):
        return get_intersect_object_from_list(pos, shipQueue)

    # event loop
    shipCoordsList = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clickedShip = get_clicked_ship(event.pos)
                if not clickedShip == None:
                    # highlight ship in the queue
                    highlight(screen, clickedShip, colors['GREEN'])
                    chosenLocation = run_choose_board_location(clickedShip, shipCoordsList)
                    if chosenLocation == None:
                        screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)
                        highlight(screen, clickedShip, colors['BLUE'])
                    else:
                        shipCoordsList += [chosenLocation]
                        shipQueue.remove(clickedShip)
                        blit_objects(screen, shipQueue)
                        screen.blit(instructionsTextBox1)

        pygame.display.flip()
        pygame.time.delay(200)


def run_choose_board_location(ship, otherShipCoords):

    instructionsTextBoxClick = TextBox("Click an anchor box on the grid. You will then be able to rotate your ship.",
                                       (48, 48))
    instructionsTextBoxEscape = TextBox("Press the ESC button to cancel placing this ship.", (96, 102), fontsize=36)

    otherCoordsPairsList = list(map(lambda coord: (coord, 2), otherShipCoords))

    ## display a board with the other placed ships' coordinates filled in
    initialBoard = generate_placement_board(otherCoordsPairsList)


    def get_hovered_square(pos):
        return get_intersect_object_from_list(pos, initialBoard.squares)

    def escape_placement():
        blit_board(screen, initialBoard)
        pygame.display.flip()

    def cover_instructions(textbox):
        screen.blit(textbox.surface, textbox.surface.fill(colors['BLACK']).move(textbox.window_coord))

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print("Pressed ESC")
                    return None


    def run_rotate_ship(shipLength, anchorCoord, firstOrientation):
        instructionsTextBoxRotate = TextBox("Use the UP (counter-clockwise) and DOWN (clockwise) arrow keys to rotate your ship.", (96, 10), fontsize=36)
        instructionsTextBoxEnter = TextBox("Press ENTER when you are satisfied with the orientation.", (96, 56), fontsize=36)

        screen.blit(instructionsTextBoxClick.surface, instructionsTextBoxClick.surface.fill(colors['BLACK']).move(instructionsTextBoxClick.window_coord))

        blit_objects(screen, [instructionsTextBoxEnter, instructionsTextBoxRotate, instructionsTextBoxEscape])
        pygame.display.flip()

        placeList = orientation_to_coord_list(anchorCoord, shipLength, firstOrientation)
        orientation = firstOrientation

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        cover_instructions(instructionsTextBoxRotate)
                        cover_instructions(instructionsTextBoxEnter)
                        cover_instructions(instructionsTextBoxEscape)
                        cover_instructions(instructionsTextBoxClick)
                        escape_placement()
                        return None
                    elif event.key == pygame.K_UP and is_possible_orientation(anchorCoord, shipLength, orientation + 1, otherShipCoords):
                        orientation = (orientation + 1) % 4
                    elif event.key == pygame.K_DOWN and is_possible_orientation(anchorCoord, shipLength, orientation - 1, otherShipCoords):
                        orientation = (orientation - 1) % 4
            placeList = orientation_to_coord_list(anchorCoord, shipLength, orientation)
            display_suggestion_placement_board(placeList)
            pygame.display.flip()
            pygame.time.delay(100)


    screen.blit(ship.surface, ship.rect)
    screen.blit(instructionsTextBoxClick.surface, instructionsTextBoxClick.rect)
    screen.blit(instructionsTextBoxEscape.surface, instructionsTextBoxEscape.rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Pressed ESC")
                return None
            elif event.type == MOUSEMOTION:
                hoveredSquare = get_hovered_square(event.pos)
                if not hoveredSquare == None:
                    firstOrientation = first_possible_orientation(hoveredSquare.grid_coord, ship.length, otherShipCoords)
                    if not firstOrientation == None:
                        suggestionCoords = orientation_to_coord_list(hoveredSquare.grid_coord, ship.length, firstOrientation)
                        display_suggestion_placement_board(suggestionCoords)
                        pygame.display.flip()
                        didClick = wait_for_click(hoveredSquare)
                        if didClick:
                            return run_rotate_ship(ship.length, hoveredSquare.grid_coord, firstOrientation)
                        else:
                            escape_placement()
                            if didClick == None:
                                cover_instructions(instructionsTextBoxEscape)
                                return None
        pygame.display.flip()
        pygame.time.delay(100)


run_start()
num = run_get_number_ships()
run_place_ships(num)