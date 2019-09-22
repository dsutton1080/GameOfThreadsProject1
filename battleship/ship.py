# A ship is represented by a list of lists
# The inner list contains a 2-tuple representing a coordinate and
#    boolean value indicating whether it has been hit at that coordinate


class Ship:
    def __init__(self, size, coords):
        """

        :param size: The length of the ship
        :param coords: List of two-element lists, containing a 2-tuple and a boolean value
        """
        self.size = size        # Size of the ship
        self.coords = coords    # List of tuples of coordinates and boolean values
        self.isSunk = False     # Indicates whether the ship has been sunk
        self.numHits = 0        # Number of time the ship has been hit

    def getCoordIndex(self, position):
        """

        :param position: A 2-tuple representing a grid position
        :return: The index in coords in which position appears. Returns -1 if not found
        """
        for index, coord in enumerate(self.coords):
            if position == coord[0]:
                return index
        return -1

    def getPositions(self):
        """

        :return: A list of grid positions; self.coords except without the boolean values
        """
        positions = []
        for coord in self.coords:
            positions.append(coord[0])
        return positions

    # Changes the boolean value associated with a coordinate to True
    #   If this hit would sink the ship, changes isSunk value to True
    #   Returns True on a success and False if the ship does not occupy the given position
    def hit(self, position):
        """

        :param position: A 2-tuple representing a grid location
        :return: True if the the hit is a success, false otherwise
        """
        index = self.getCoordIndex(position)
        success = False
        if index >= 0:
            if position == self.coords[index][0]:
                self.coords[index][1] = True
                success = True
                self.numHits += 1
            if self.numHits == self.size:
                self.isSunk = True
        return success


# Returns a Ship object given a start coordinate and end coordinate
#   The start and end parameters should be 2-tuples given as (row, column)
def createShip(start, end):
    """

    :param start: A 2-tuple given as (row, column)
    :param end: A 2-tuple given as (row, column)
    :return: A Ship object whose ends are located at the given parameters
    """
    if (start[0] > end[0]) | (start[1] > end[1]):
        temp = start
        start = end
        end = temp
    coords = []
    if start[0] == end[0]:
        size = end[1] - start[1] + 1
        for i in range(start[1], end[1] + 1):
            coords.append([(start[0], i), False])
    elif start[1] == end[1]:
        size = end[0] - start[0] + 1
        for i in range(start[0], end[0] + 1):
            coords.append([(i, start[1]), False])
    newShip = Ship(size, coords)
    return newShip

