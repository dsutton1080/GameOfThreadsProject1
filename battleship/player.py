import ship as S


class Player:
    def __init__(self):
        """

        """
        self.numShips = 0   # The number of ships the player currently has
        self.shipList = []  # List of ships the player currently has
        self.guesses = []   # List of coordinates the player has guessed
        
        self.shipGrid = [["~" for i in range(8)] for j in range(8)]
        self.guessGrid = [["~" for i in range(8)] for j in range(8)]
        
    # Creates a ship from a start and end coordinate and adds it to shipList
    def placeShip(self, start, end):
        """

        :param start: A 2-tuple representing a start coordinate
        :param end: A 2-tuple representing an end coordinate
        """
        newShip = S.createShip(start, end)
        for pos in newShip.getPositions():
            self.shipGrid[pos[0]][pos[1]] = "S"
        self.shipList.append(newShip)
        self.numShips += 1

    # Removes ships that are sunk from the players shipList
    #   Should be called for a player at the start of each of their turns
    def removeSunkShips(self):
        """

        """
        self.shipList = [ship for ship in self.shipList if ship.isSunk is False]
        self.numShips = len(self.shipList)

    # Returns True if the guess at a position hits a given player's ship
    #   Otherwise returns False
    def guess(self, position, player):
        self.guesses.append(position)
        for ship in player.shipList:
            if ship.hit(position):
                print("Hit!")
                if ship.isSunk:
                    print(f"You sunk the {ship.size} ship!")
                input("Press Enter to end turn.")
                self.guessGrid[position[0]][position[1]] = "H"
                player.shipGrid[position[0]][position[1]] = "X"
                return True
        self.guessGrid[position[0]][position[1]] = "M"
        print("Miss!")
        input("Press Enter to end turn.")
        return False

    def displayGrids(self):
        """

        """
        print("Your Ships:                     Your Guesses:")
        print("   A  B  C  D  E  F  G  H           A  B  C  D  E  F  G  H")
        for idx, row in enumerate(range(0, 8)):
            print(str(idx + 1), end="  ")
            for col in range(0, 8):
                print(self.shipGrid[row][col], " ", end='')
            print("     ", str(idx + 1), end="  ")
            for col in range(0, 8):
                print(self.guessGrid[row][col], " ", end='')
            print("")
        print("")

