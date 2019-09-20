# TODO: Replace "empty", "ship", "Hit", and "Miss" to the necessary values to display a color

import ship as S


class Player:
    def __init__(self):
        self.numShips = 0   # The number of ships the player currently has
        self.shipList = []  # List of ships the player currently has
        self.guesses = []   # List of coordinates the player has guessed
        
        self.shipGrid = [["empty" for i in range(8)] for j in range(8)]
        self.guessGrid = [["empty" for i in range(8)] for j in range(8)]
        
    # Creates a ship from a start and end coordinate and adds it to shipList
    def placeShip(self, start, end):
        newShip = S.createShip(start, end)
        for pos in newShip.getPositions():
            self.shipGrid[pos[0]][pos[1]] = "ship"
        self.shipList.append(newShip)
        self.numShips += 1

    # Removes ships that are sunk from the players shipList
    #   Should be called for a player at the start of each of their turns
    def removeSunkShips(self):
        self.shipList = [ship for ship in self.shipList if ship.isSunk is False]
        self.numShips = len(self.shipList)

    # Returns True if the guess at a position hits a given player's ship
    #   Otherwise returns False
    def guess(self, position, player):
        self.guesses.append(position)
        for ship in player.shipList:
            if ship.hit(position):
                self.guessGrid[position[0]][position[1]] = "Hit"
                player.shipGrid[position[0]][position[1]] = "Hit"
                return True
        self.guessGrid[position[0]][position[1]] = "Miss"
        return False

