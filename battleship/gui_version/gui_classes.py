
from utils import flatten, colors, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
from pygame.locals import *
from functools import reduce
from math import floor
from copy import deepcopy


class State:
    """
    Used in the main game loop to switch the current player. It stores the state of both players.
    """
    def __init__(self, player1, player2):
        """
        Initialization method for the State class
        :param player1: A Player object
        :param player2: A Player object
        """
        self.player1 = player1
        self.player2 = player2
        self.iterations = 0

    def update(self, guess):
        """
        Updates the state based by adding the guess and "flipping" the players.
        :param guess: a coordinate
        :return: void
        """
        self.player1.add_guess(guess)
        self.player2, self.player1 = self.player1, self.player2
        self.iterations += 1

    def is_game_over(self):
        """
        Cross references the guesses versus the other player's ships and checks whether the game is over.
        :return: boolean
        """
        def gameover(guesses, ships):
            return all(map(lambda shipcoord: shipcoord in guesses, flatten(ships)))

        return gameover(self.player2.guesses, self.player1.ships)


class Player:
    """
    Represents the encapsulation of ships, guesses, and name of a player
    """
    def __init__(self, ships, name):
        """
        Creates the player
        :param ships: A list of list of coordinates to populate the player's ships
        :param name: The string representing the player's name
        """
        self.ships = ships
        self.guesses = []
        self.name = name

    def add_guess(self, coord):
        """
        Append a guess coordinate to the player's guesses
        :param coord: The guess coordinate
        :return: void
        """
        self.guesses.append(coord)


class BoardSquare(pygame.sprite.Sprite):
    """
    Encapsulates the displayable idea of a board square with dimensional and color properties
    """
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
        """
        Updates the color of the board square
        :param color: an RGB value
        :return: void
        """
        self.color = color


class Board:
    """
    The logical combination of displayable components to draw a board. Stores dimension data.
    """
    def __init__(self,
                 window_location,
                 width,
                 height,
                 squares=None):
        """
        Creates the board given the dimensions
        :param window_location: The window coordinate of the top left
        :param width: The width of the board
        :param height: The height of the board
        :param squares: An optional list of pre-defined squares to display to the board
        """
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
        """
        Generates a generic list of grey BoardSquare objects
        :return: A list of BoardSquare objects
        """
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
        """
        Generates a list of TextBox objects to be the row labels
        :return: a list of TextBox objects
        """
        x, y = self.window_location
        fontSize = floor(min(self.squareHeight, self.squareWidth))

        def create_label(index):
            return TextBox("{}".format(index), (x, y + (index * self.offset) + (self.squareHeight * index)),
                           fontsize=fontSize)

        return reduce(lambda others, i: others + [create_label(i)], range(1, 9), [])

    def create_col_labels(self):
        """
        Generates a list of TextBox objects to be the column labels
        :return: a list of TextBox objects
        """
        x, y = self.window_location
        fontSize = floor(min(self.squareHeight, self.squareWidth))

        def create_label(index):
            return TextBox("{}".format(chr(index + 64)), (x + (index * self.offset) + (self.squareWidth * index), y), fontsize=fontSize)

        return reduce(lambda others, i: others + [create_label(i)], range(1, 9), [])


class TextBox(pygame.sprite.Sprite):
    """
    An encapsulation of a displayable text box with text
    """
    def __init__(self,
                 message,
                 window_coord=(0, 0),
                 textcolor=colors['WHITE'],
                 backgroundcolor=colors['BLACK'],
                 fontsize=48,
                 font=None):
        """
        Creates the text box.
        :param message: The string to display in the text box
        :param window_coord: The coordinate that represents the window location
        :param textcolor: The RGB text color
        :param backgroundcolor: The RGB background color
        :param fontsize: The integer representing the font size
        :param font: The font style (optional)
        """
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
    """
    Encapsulates a displayable Ship object for the coord placement procedure.
    """
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