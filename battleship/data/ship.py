# A ship is represented by a list of lists
# The inner list contains a 2-tuple representing a coordinate and
#    boolean value indicating whether it has been hit there


class Ship:
    def __init__(self, size, coords):
        self.size = size
        self.coords = coords
        self.isSunk = False
        self.numHits = 0

    def hit(self, position):
        for coord in self.coords:
            if position == coord[0]:
                coord[1] = True
                print(f"You hit {coord[0]}!\n")
                self.numHits += 1
                break
        if self.numHits == self.size:
            self.isSunk = True
            print(f"You sunk the {self.size} ship!\n")


# Returns a Ship object given a start coordinate and end coordinate
#   represented by 2-Tuples - (row, column)
def createShip(start, end):
    coords = []
    size = 0
    if start[0] == end[0]:
        size = end[1] - start[1] + 1
        for i in range(start[1], end[1] + 1):
            coords.append([(start[0], i), False])
    elif start[1] == end[1]:
        size = end[0] - start[0] + 1
        for i in range(start[0], end[0] + 1):
            coords.append([(i, start[1]), False])
    newShip = Ship(size, coords)
    print(newShip.coords)
    return newShip


# All code below this is for testing
myShip = createShip((0, 0), (0, 4))

for x in range(0,5):
    myShip.hit((0,x))

print(myShip.coords)
