from collections import namedtuple

# A coordinate is simply a tuple with a row numbered 1-8 and a column with a letter A-H

Coordinate = namedtuple('Coordinate', [
    'row',
    'col'
])

# A Board is an immutable (frozen) set of coordinates

Board = lambda coordIter: frozenset(coordIter)

# validBoard = lamda board:
#     listBoard = sort(list(board), key=.row)

# A Ship is an immutable (frozen) set of coordinates (also)

Ship = Board
