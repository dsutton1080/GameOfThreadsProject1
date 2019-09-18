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

class BoardSquare(pygame.sprite.Sprite):
    def __init__(self,
                 grid_coord,
                 window_coord,
                 width,
                 height,
                 color=colors['GREY']):
        super(BoardSquare, self).__init__()
        self.grid_coord = grid_coord
        self.window_coord = window_coord
        self.color = color
        self.rect = Rect(self.window_coord[0], self.window_coord[1], width, height)
        self.surface = pygame.Surface((width, height))
        self.surface.fill(self.color)

    def update_color(self, color):
        self.color = color


class Board:
    def __init__(self,
                 window_location,
                 width,
                 height):
        super(Board, self).__init__()
        self.window_location = window_location
        self.width = width
        self.height = height
        self.offset = SCREEN_HEIGHT / 400
        self.squareWidth = (self.width / 9) - self.offset
        self.squareHeight = (self.height / 9) - self.offset

        # stores a list of BoardSquare objects
        self.squares = self.create_board_squares()

        # stores the TextBox objects for the row labels
        self.rowLabels = self.create_row_labels()

        # stores the TextBox objects for the column labels
        self.colLabels = self.create_col_labels()

    def create_board_squares(self):
        x, y = self.window_location
        squares = []
        offsetY = 0
        for rowY in [(y + (self.squareHeight * i)) for i in range(1, 9)]:
            row = 1
            offsetX = 0
            for colX in [(x + (self.squareWidth * i)) for i in range(1, 9)]:
                col = 1
                squares = squares + [
                    BoardSquare((row, col), (colX + offsetX, rowY + offsetY), self.squareWidth, self.squareHeight)]
                col += 1
                offsetX += self.offset
            row += 1
            offsetY += self.offset
        return squares

    def create_row_labels(self):
        x, y = self.window_location
        fontSize = floor(min(self.squareHeight, self.squareWidth))

        def create_label(index):
            return TextBox("{}".format(chr(index + 64)), (x, y + (index * self.offset) + (self.squareHeight * index)),
                           fontsize=fontSize)

        return reduce(lambda others, i: others + [create_label(i)], range(1, 9), [])

    def create_col_labels(self):
        x, y = self.window_location
        fontSize = floor(min(self.squareHeight, self.squareWidth))

        def create_label(index):
            return TextBox("{}".format(index), (x + (index * self.offset) + (self.squareWidth * index), y), fontsize=fontSize)

        return reduce(lambda others, i: others + [create_label(i)], range(1, 9), [])


def blit_objects(surface, objlist):
    for obj in objlist:
        surface.blit(obj.surface, obj.rect)


class TextBox(pygame.sprite.Sprite):
    def __init__(self,
                 message,
                 window_coord=(0, 0),
                 textcolor=colors['WHITE'],
                 backgroundcolor=colors['BLACK'],
                 fontsize=48,
                 font=None):
        super(TextBox, self).__init__()
        self.message = message
        self.window_coord = window_coord
        self.textcolor = textcolor
        self.backgroundcolor = backgroundcolor
        self.fontsize = fontsize
        self.font = font
        font = pygame.font.SysFont(self.font, self.fontsize)
        self.surface = font.render(message, True, self.textcolor, self.backgroundcolor)
        self.rect = pygame.Rect(self.window_coord[0], self.window_coord[1], self.surface.get_width(), self.surface.get_height())
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()


class Ship(pygame.sprite.Sprite):
    def __init__(self,
                 length,
                 squareWidth,
                 squareHeight,
                 window_coord):
        super(Ship, self).__init__()
        self.length = length
        self.squareWidth = squareWidth
        self.squareHeight = squareHeight
        self.window_coord = window_coord
        self.grid_coord = (0, 0)
        self.offset = SCREEN_HEIGHT / 400
        self.rect = Rect(self.window_coord[0], self.window_coord[1], self.squareWidth, self.squareHeight * self.length)
        self.surface = pygame.Surface((self.rect.w, self.rect.h))
        self.surface.fill(colors['BLUE'])


def quit_actions():
    pygame.quit()
    sys.exit()


def is_quit_case(event):
    return event == pygame.QUIT


# background = pygame.image.load('battleship.jpg').convert()
# screen.blit(background, (0, 0))
#
# battleshipTextBox = TextBox("Battleship!", (250, 100), fontsize=96)
# screen.blit(battleshipTextBox.surface, battleshipTextBox.rect)
#
# instructionsTextBox = TextBox("Press the SPACE bar to play", (200, 300), fontsize=48)
# screen.blit(instructionsTextBox.surface, instructionsTextBox.rect)

def run_start():
    screen.blit(imageBattleshipSurface, (0, 0))

    battleshipTextBox = TextBox("Battleship!", (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 4), fontsize=96)
    screen.blit(battleshipTextBox.surface, battleshipTextBox.rect)

    instructionsTextBox = TextBox("Press the SPACE bar to play", (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2), fontsize=48)
    screen.blit(instructionsTextBox.surface, instructionsTextBox.rect)

    pygame.display.update()

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


def run_place_ships(numShips):

    # define the board to place on
    placeBoard = Board(((SCREEN_WIDTH / 3), (SCREEN_HEIGHT / 6)), (SCREEN_WIDTH / 2), (SCREEN_HEIGHT * (2 / 3)))

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


    # define instructions box
    instructionsTextBox1 = TextBox("Drag and Drop a ship from the left to a location in the grid on the right.", (48, 48))
    instructionsTextBox2 = TextBox("Once placed, rotate the ship by using the up and down arrow keys.", (48, 96))

    pygame.display.flip()
    screen.blit(blackBackground, blackBackground.get_rect())
    blit_objects(screen, placeBoard.squares + placeBoard.rowLabels + placeBoard.colLabels)
    blit_objects(screen, shipQueue)
    screen.blit(instructionsTextBox1.surface, instructionsTextBox1.rect)
    screen.blit(instructionsTextBox2.surface, instructionsTextBox2.rect)


    # define instructions box
    # draw initial state

    # event loop

run_start()
num = run_get_number_ships()
run_place_ships(num)

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.time.delay(200)