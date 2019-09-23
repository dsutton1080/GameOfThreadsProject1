# import data.game as G
# import data.player as P
# import data.ship as S

from utils import flatten, colors, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
from pygame.locals import *
from functools import reduce
from math import floor
from copy import deepcopy


class State:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.iterations = 0

    def update(self, guess):
        self.player1.add_guess(guess)
        self.player2, self.player1 = self.player1, self.player2
        self.iterations += 1

    def is_game_over(self):
        def gameover(guesses, ships):
            return all(map(lambda shipcoord: shipcoord in guesses, flatten(ships)))

        return gameover(self.player2.guesses, self.player1.ships)


class Player:
    def __init__(self, ships, name):
        self.ships = ships
        self.guesses = []
        self.name = name

    def add_guess(self, coord):
        self.guesses.append(coord)


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
                 height,
                 squares=None):
        super(Board, self).__init__()
        self.window_location = window_location
        self.width = width
        self.height = height
        self.offset = SCREEN_HEIGHT / 400
        self.squareWidth = (self.width / 9) - self.offset
        self.squareHeight = (self.height / 9) - self.offset

        # stores a list of BoardSquare objects
        if squares == None:
            self.squares = self.create_board_squares()
        else:
            self.squares = squares

        # stores the TextBox objects for the row labels
        self.rowLabels = self.create_row_labels()

        # stores the TextBox objects for the column labels
        self.colLabels = self.create_col_labels()

    def create_board_squares(self):
        x, y = self.window_location
        squares = []
        offsetY = 0
        row = 1
        for rowY in [(y + (self.squareHeight * i)) for i in range(1, 9)]:
            offsetX = 0
            col = 1
            for colX in [(x + (self.squareWidth * i)) for i in range(1, 9)]:
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
            return TextBox("{}".format(index), (x, y + (index * self.offset) + (self.squareHeight * index)),
                           fontsize=fontSize)

        return reduce(lambda others, i: others + [create_label(i)], range(1, 9), [])

    def create_col_labels(self):
        x, y = self.window_location
        fontSize = floor(min(self.squareHeight, self.squareWidth))

        def create_label(index):
            return TextBox("{}".format(chr(index + 64)), (x + (index * self.offset) + (self.squareWidth * index), y), fontsize=fontSize)

        return reduce(lambda others, i: others + [create_label(i)], range(1, 9), [])


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
                 window_coord,
                 orientation=0,
                 color=colors['BLUE']):
        super(Ship, self).__init__()
        self.length = length
        self.squareWidth = squareWidth
        self.squareHeight = squareHeight
        self.window_coord = window_coord
        self.color = color
        self.anchor_coord = (0, 0)
        self.offset = SCREEN_HEIGHT / 400
        self.surface = pygame.Surface((self.squareWidth, self.squareHeight * self.length))
        self.rect = self.surface.fill(self.color).move(self.window_coord[0], self.window_coord[1])