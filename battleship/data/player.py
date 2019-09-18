import ship as S


class Player:
    def __init__(self):
        self.numShips = 0   # The number of ships the player currently has
        self.shipList = []  # List of ships the player currently has
        self.guesses = []   # List of coordinates the player has guessed

    # Creates a ship from a start and end coordinate and adds it to shipList
    def placeShip(self, start, end):
        self.shipList.append(S.createShip(start, end))
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
                return True
        return False

