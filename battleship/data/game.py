import player as P


class Game:
    def __init__(self, numShips):
        """

        :param numShips:
        """
        self.numShips = numShips;
        self.player1 = P.Player()
        self.player2 = P.Player()
        self.currentPlayer = self.player1

    def nextPlayer(self):
        """

        """
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

    def turn(self, guess):
        """

        :param guess:
        """
        self.currentPlayer.removeSunkShips()
        self.currentPlayer.guess(guess)
        self.nextPlayer()

    def shipPlacement(self, start, end):
        """

        :param start:
        :param end:
        """
        self.currentPlayer.placeShip(start, end)
        if self.currentPlayer.numShips == self.numShips:
            self.nextPlayer()







