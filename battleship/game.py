import player as P


class Game:
    def __init__(self, numShips):
        self.win = False
        self.numShips = numShips;
        self.player1 = P.Player()
        self.player2 = P.Player()
        self.currentPlayer = self.player1
        self.nextPlayer = self.player2

    def advancePlayer(self):
        self.nextPlayer = self.currentPlayer
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

    def turn(self, guess):
        self.currentPlayer.guess(guess, self.nextPlayer)
        self.advancePlayer()
        self.currentPlayer.removeSunkShips()
        if self.currentPlayer.numShips == 0:
            self.win = True

    def printWinner(self):
        if self.nextPlayer == self.player1:
            print("Player 1 Wins!")
        else:
            print("Player 2 Wins!")




