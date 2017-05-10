from kate.engine.match.pieces import rook, bishop
from kate.engine.match import *


blank = PIECES['blk']
GEN_STEPS = [ [[0, 1, blank], [0, 2, blank], [0, 3, blank], [0, 4, blank], [0, 5, blank], [0, 6, blank], [0, 7, blank]],
              [[0, -1, blank], [0, -2, blank], [0, -3, blank], [0, -4, blank], [0, -5, blank], [0, -6, blank], [0, -7, blank]],
              [[1, 0, blank], [2, 0, blank], [3, 0, blank], [4, 0, blank], [5, 0, blank], [6, 0, blank], [7, 0, blank]],
              [[-1, 0, blank], [-2, 0, blank], [-3, 0, blank], [-4, 0, blank], [-5, 0, blank], [-6, 0, blank], [-7, 0, blank]],
              [[1, 1, blank], [2, 2, blank], [3, 3, blank], [4, 4, blank], [5, 5, blank], [6, 6, blank], [7, 7, blank]],
              [[-1, -1, blank], [-2, -2, blank], [-3, -3, blank], [-4, -4, blank], [-5, -5, blank], [-6, -6, blank], [-7, -7, blank]],
              [[1, -1, blank], [2, -2, blank], [3, -3, blank], [4, -4, blank], [5, -5, blank], [6, -6, blank], [7, -7, blank]],
              [[-1, 1, blank], [-2, 2, blank], [-3, 3, blank], [-4, 4, blank], [-5, 5, blank], [-6, 6, blank], [-7, 7, blank]] ]


def is_move_valid(match, srcx, srcy, dstx, dsty, piece):
    if(rook.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
        return True
    else:
        return bishop.is_move_valid(match, srcx, srcy, dstx, dsty, piece)

