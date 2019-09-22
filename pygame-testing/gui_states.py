
from utils import colors, SCREEN_WIDTH, SCREEN_HEIGHT
from gui_functions import *
from gui_classes import State, Player, BoardSquare, Board, TextBox, Ship
import sys
import pygame
from pygame.locals import *
from functools import reduce
from math import floor

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
def run_place_ships(numShips, playerName):

    # define the board to place on
    placeBoard = Board(((SCREEN_WIDTH / 3), (SCREEN_HEIGHT / 6)), (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * (2 / 3)))

    instructionsTextBox1 = TextBox("Click a blue ship on the left to select it for placement.", (48, 48))

    instructionsTextBoxEscape = TextBox("Press the ESC button to cancel placing this ship.", (96, 102), fontsize=36)

    instructionsTextBoxClick = TextBox("Click an anchor box on the grid. You will then be able to rotate your ship.",
                                       (48, 48))

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

    # black the screen
    screen.fill(colors['BLACK'])
    pygame.display.flip()
    # blit_objects(screen, placeBoard.squares + placeBoard.rowLabels + placeBoard.colLabels)
    # blit_objects(screen, shipQueue)
    # screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)

    def get_clicked_ship(pos):
        return get_intersect_object_from_list(pos, shipQueue)

    # Display the welcome message
    welcomeBox = TextBox("{}, place your ships!".format(playerName), (130, SCREEN_HEIGHT / 3), fontsize=96, textcolor=colors['GREEN'])
    screen.blit(welcomeBox.surface, welcomeBox.rect)
    pygame.display.update(welcomeBox.rect)
    pygame.time.delay(2000)
    screen.fill(colors['BLACK'])

    # event loop
    shipCoordsList = []

    while True:
        if not shipQueue:
            screen.fill((0, 0, 0))
            pygame.display.flip()
            return list(filter(lambda e: not isinstance(e, tuple), shipCoordsList))
        screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)
        blit_objects(screen, shipQueue)
        blit_board(screen, generate_placement_board(encode_placement_board([], flatten(shipCoordsList))))
        screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clickedShip = get_clicked_ship(event.pos)
                if clickedShip is not None:
                    # highlight ship in the queue
                    highlight(screen, clickedShip, colors['GREEN'])
                    chosenLocation = run_choose_board_location(clickedShip, shipCoordsList)
                    if chosenLocation is None:
                        cover_instructions(screen, instructionsTextBoxEscape)
                        cover_instructions(screen, instructionsTextBoxClick)
                        highlight(screen, clickedShip, colors['BLUE'])
                    else:
                        shipCoordsList += [chosenLocation]
                        shipQueue.remove(clickedShip)
                        highlight(screen, clickedShip, colors['BLACK'])
                        # blit_objects(screen, shipQueue)
        screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)
        pygame.display.flip()
        pygame.time.delay(200)


def run_choose_board_location(ship, otherShipCoords):

    instructionsTextBoxClick = TextBox("Click an anchor box on the grid. You will then be able to rotate your ship.",
                                       (48, 48))
    instructionsTextBoxEscape = TextBox("Press the ESC button to cancel placing this ship.", (96, 102), fontsize=36)

    otherCoordsPairsList = list(map(lambda coord: (coord, 2), otherShipCoords))

    ## display a board with the other placed ships' coordinates filled in
    initialBoard = generate_placement_board(otherCoordsPairsList)


    def escape_placement():
        blit_board(screen, initialBoard)
        pygame.display.flip()


    # highlight the updateBoard squares that correspond to each coordinate in the passed in list of coordinates
    # just display a new board?
    def display_suggestion_placement_board(coordList):
        codePairs = encode_placement_board(coordList, otherCoordsPairsList)
        blit_board(screen, generate_placement_board(codePairs))


    def wait_for_click_display(board, square):
        while True:
            blit_board(screen, board)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and square.rect.collidepoint(event.pos):
                    return True
                elif event.type == pygame.MOUSEMOTION and not square.rect.collidepoint(event.pos):
                    return False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    cover_instructions(screen, instructionsTextBoxEscape)
                    cover_instructions(screen, instructionsTextBoxClick)
                    return None
            pygame.time.delay(100)


    def run_rotate_ship(shipLength, anchorCoord, firstOrientation):
        instructionsTextBoxRotate = TextBox("Use the UP (counter-clockwise) and DOWN (clockwise) arrow keys to rotate your ship.", (96, 10), fontsize=36)
        instructionsTextBoxEnter = TextBox("Press SPACE when you are satisfied with the orientation.", (96, 56), fontsize=36)

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
                        cover_instructions(screen, instructionsTextBoxRotate)
                        cover_instructions(screen, instructionsTextBoxEnter)
                        cover_instructions(screen, instructionsTextBoxEscape)
                        cover_instructions(screen, instructionsTextBoxClick)
                        escape_placement()
                        return None
                    elif event.key == pygame.K_UP and is_possible_orientation(anchorCoord, shipLength, orientation + 1, otherShipCoords):
                        orientation = (orientation + 1) % 4
                    elif event.key == pygame.K_DOWN and is_possible_orientation(anchorCoord, shipLength, orientation - 1, otherShipCoords):
                        orientation = (orientation - 1) % 4
                    elif event.key == pygame.K_SPACE:
                        cover_instructions(screen, instructionsTextBoxRotate)
                        cover_instructions(screen, instructionsTextBoxEnter)
                        cover_instructions(screen, instructionsTextBoxEscape)
                        cover_instructions(screen, instructionsTextBoxClick)
                        escape_placement()
                        pygame.display.flip()
                        return placeList
            placeList = orientation_to_coord_list(anchorCoord, shipLength, orientation)
            blit_board(screen, generate_placement_board(encode_placement_board(placeList, otherShipCoords)))
            pygame.display.flip()
            pygame.time.delay(100)

    blit_board(screen, initialBoard)
    # screen.blit(ship.surface, ship.rect)
    # screen.blit(instructionsTextBoxClick.surface, instructionsTextBoxClick.rect)
    # screen.blit(instructionsTextBoxEscape.surface, instructionsTextBoxEscape.rect)
    pygame.display.flip()

    while True:
        screen.blit(ship.surface, ship.rect)
        screen.blit(instructionsTextBoxClick.surface, instructionsTextBoxClick.rect)
        screen.blit(instructionsTextBoxEscape.surface, instructionsTextBoxEscape.rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None
            elif event.type == MOUSEMOTION:
                hoveredSquare = get_hovered_square(event.pos, initialBoard)
                if hoveredSquare is not None:
                    firstOrientation = first_possible_orientation(hoveredSquare.grid_coord, ship.length, otherShipCoords)
                    if firstOrientation is not None:
                        suggestionCoords = orientation_to_coord_list(hoveredSquare.grid_coord, ship.length, firstOrientation)
                        displayBoard = generate_placement_board(encode_placement_board(suggestionCoords, otherShipCoords))
                        didClick = wait_for_click_display(displayBoard, hoveredSquare)
                        if didClick:
                            placed = run_rotate_ship(ship.length, hoveredSquare.grid_coord, firstOrientation)
                            if placed is not None:
                                otherShipCoords += placed
                                return placed
                            else:
                                escape_placement()
                                cover_instructions(screen, instructionsTextBoxEscape)
                                cover_instructions(screen, instructionsTextBoxClick)
                                return None
                        elif didClick is None:
                            escape_placement()
                            cover_instructions(screen, instructionsTextBoxClick)
                            return None
        pygame.display.flip()
        pygame.time.delay(50)


# the main game loop
# takes 2 args: player1 and player2
def run_game_loop(shipCoords1, shipCoords2):

    switchTurnsInstructionsBox = TextBox("Press the SPACE key to switch turns.", (240, 48))
    switchTurnsInstructionsBox2 = TextBox("Please switch spots with your playing partner. Press SPACE to continue.", (35, SCREEN_HEIGHT / 2), fontsize=44)
    guessBoardLabel = TextBox("Attack Board", (200, SCREEN_HEIGHT / 5), textcolor=colors['RED'])
    myBoardLabel = TextBox("My Board", (SCREEN_WIDTH - 370, SCREEN_HEIGHT / 5), textcolor=colors['GREEN'])
    hitTextBox = TextBox("Hit!", ((SCREEN_WIDTH / 2) - 70, SCREEN_HEIGHT * (8 / 10)), textcolor=colors['GREEN'], fontsize=96)
    missTextBox = TextBox("Miss.", ((SCREEN_WIDTH / 2) - 70, SCREEN_HEIGHT * (8 / 10)), textcolor=colors['RED'], fontsize=96)

    player1 = Player(shipCoords1, "Player 1")
    player2 = Player(shipCoords2, "Player 2")
    state = State(player1, player2)


    def generate_sunk_ship_alert(shipLength):
        return TextBox("You sunk the other player's {}".format(ship_length_to_name(shipLength)), (SCREEN_WIDTH / 4, SCREEN_HEIGHT * (9 / 10)), textcolor=colors['GREEN'])

    def produce_guess_board():
        return generate_guess_board(encode_guess_board(state.player1.guesses, state.player2.ships))

    def produce_guessed_at_board():
        return generate_guessed_at_board(encode_guessed_at_board(state.player2.guesses, state.player1.ships))

    def wait_for_click_guess(square):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and square.rect.collidepoint(event.pos):
                    return square.grid_coord
                elif event.type == pygame.MOUSEMOTION and not square.rect.collidepoint(event.pos):
                    return None
            pygame.time.delay(50)

    def run_switch_turns():
        # display switch turns instruction message
        screen.blit(switchTurnsInstructionsBox.surface, switchTurnsInstructionsBox.rect)
        pygame.display.flip()
        # wait till they hit SPACE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    # black the screen
                    screen.fill((0, 0, 0))
                    # display the instructions to switch turns
                    screen.blit(switchTurnsInstructionsBox2.surface, switchTurnsInstructionsBox2.rect)
                    pygame.display.flip()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == KEYUP and event.key == pygame.K_SPACE:
                                screen.fill(colors['BLACK'])
                                return
            pygame.time.delay(200)

    while True:
        whosTurnTextBox = TextBox("{}'s Turn".format(state.player1.name), (SCREEN_WIDTH * (3 / 8), 40), fontsize=64, textcolor=colors['GREEN'])
        guessInstructionsTextBox = TextBox("Click a coordinate on the Attack Board to fire a missile!", (110, 96))
        initialGuessBoard = produce_guess_board()
        blit_board(screen, initialGuessBoard)
        blit_board(screen, produce_guessed_at_board())
        blit_objects(screen, [guessBoardLabel, myBoardLabel, guessInstructionsTextBox, whosTurnTextBox])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                hoveredSquare = get_hovered_square(event.pos, initialGuessBoard)
                if (hoveredSquare is not None) and (hoveredSquare.grid_coord not in state.player1.guesses):
                    highlight(screen, hoveredSquare, colors['YELLOW'])
                    guess = wait_for_click_guess(hoveredSquare)
                    if guess is not None:
                        pygame.draw.rect(screen, colors['BLACK'], guessInstructionsTextBox.rect)
                        pygame.draw.rect(screen, colors['BLACK'], whosTurnTextBox.rect)
                        if hit(guess, state.player2.ships):
                            highlight(screen, hoveredSquare, colors['GREEN'])
                            screen.blit(hitTextBox.surface, hitTextBox.rect)
                            sunkenShipLength = which_sunk(guess, state.player1.guesses, state.player2.ships)
                            if sunkenShipLength is not None:
                                print(sunkenShipLength)
                                sunkAlertBox = generate_sunk_ship_alert(sunkenShipLength)
                                screen.blit(sunkAlertBox.surface, sunkAlertBox.rect)
                                pygame.display.flip()
                                state.update(guess)
                                if state.is_game_over():
                                    pygame.display.flip()
                                    pygame.time.delay(2000)
                                    screen.fill(colors['BLACK'])
                                    return state.player2.name
                        else:
                            highlight(screen, hoveredSquare, colors['RED'])
                            screen.blit(missTextBox.surface, missTextBox.rect)
                            state.update(guess)
                        pygame.display.flip()
                        pygame.time.delay(1500)
                        run_switch_turns()
                        screen.fill(colors['BLACK'])
        pygame.display.flip()
        pygame.time.delay(50)


# returns a boolean indicating whether or not to play again
def winner_screen_prompt_replay(winnerName):
    screen.fill(colors['BLACK'])
    # display the winner text box
    winnerTextBox = TextBox("{} has won the game!".format(winnerName), (130, 48), fontsize=96, textcolor=colors['GREEN'])
    # display the play again prompt
    playAgainTextBox = TextBox("Would you like to play again? Click either 'YES' or 'NO'.", (90, SCREEN_HEIGHT * (3 / 8)), fontsize=56)
    # display the 'Yes' and 'No' boxes
    yesBox = TextBox("YES", ((SCREEN_WIDTH / 3) - (128 * (2 / 3)), SCREEN_HEIGHT * (3 / 4)), fontsize=128, textcolor=colors['GREEN'])
    noBox = TextBox("NO", ((SCREEN_WIDTH * (2 / 3)) - (128 * (2 / 3)), SCREEN_HEIGHT * (3 / 4)), fontsize=128, textcolor=colors['RED'])
    blit_objects(screen, [winnerTextBox, playAgainTextBox, yesBox, noBox])
    pygame.display.flip()
    # wait for click

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                clickedOnBox = get_intersect_object_from_list(event.pos, [yesBox, noBox])
                if clickedOnBox is not None:
                    screen.fill(colors['BLACK'])
                    pygame.display.flip()
                    if clickedOnBox is yesBox:
                        return True
                    return False
        pygame.time.delay(200)



