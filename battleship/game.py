import player as P


class Game:
    def __init__(self, numShips):
        self.numShips = numShips;
        self.player1 = P.Player()
        self.player2 = P.Player()
        self.currentPlayer = self.player1

    def nextPlayer(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

    def turn(self, guess):
        self.currentPlayer.removeSunkShips()
        self.currentPlayer.guess(guess)
        self.nextPlayer()







