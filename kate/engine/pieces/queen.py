from .. match import *
from .. cvalues import *
from .. import rules
from .. import analyze_helper
from . import rook, bishop


STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]

blank = PIECES['blk']
GEN_STEPS = [ [[0, 1, blank], [0, 2, blank], [0, 3, blank], [0, 4, blank], [0, 5, blank], [0, 6, blank], [0, 7, blank]],
              [[0, -1, blank], [0, -2, blank], [0, -3, blank], [0, -4, blank], [0, -5, blank], [0, -6, blank], [0, -7, blank]],
              [[1, 0, blank], [2, 0, blank], [3, 0, blank], [4, 0, blank], [5, 0, blank], [6, 0, blank], [7, 0, blank]],
              [[-1, 0, blank], [-2, 0, blank], [-3, 0, blank], [-4, 0, blank], [-5, 0, blank], [-6, 0, blank], [-7, 0, blank]],
              [[1, 1, blank], [2, 2, blank], [3, 3, blank], [4, 4, blank], [5, 5, blank], [6, 6, blank], [7, 7, blank]],
              [[-1, -1, blank], [-2, -2, blank], [-3, -3, blank], [-4, -4, blank], [-5, -5, blank], [-6, -6, blank], [-7, -7, blank]],
              [[1, -1, blank], [2, -2, blank], [3, -3, blank], [4, -4, blank], [5, -5, blank], [6, -6, blank], [7, -7, blank]],
              [[-1, 1, blank], [-2, 2, blank], [-3, 3, blank], [-4, 4, blank], [-5, 5, blank], [-6, 6, blank], [-7, 7, blank]] ]


def is_field_touched(match, color, fieldx, fieldy):
    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and piece == PIECES['wQu']) or
                (color == COLORS['black'] and piece == PIECES['bQu']) ):
                return True
    return False


def is_move_stuck(match, srcx, srcy, dstx, dsty):
    bp_flag = bishop.is_move_stuck(match, srcx, srcy, dstx, dsty)
    rk_flag = rook.is_move_stuck(match, srcx, srcy, dstx, dsty)
    return bp_flag or rk_flag


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked):
    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(is_move_stuck(match, dstx, dsty, x1, y1)):
                continue

            if(analyze_helper.is_fork_field(match, piece, srcx, srcy, x1, y1)):
                forked.append([srcx, srcy, dstx, dsty,  x1, y1])
                return True
    return False


def count_touches(match, color, fieldx, fieldy):
    count = 0

    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(is_move_stuck(match, fieldx, fieldy, x1, y1)):
                continue

            piece = match.readfield(x1, y1)
            if(piece == PIECES['blk']):
                continue
            elif(match.color_of_piece(piece) == color):
                count += 1
            else:
                count -= 1

    return count


def is_move_valid(match, srcx, srcy, dstx, dsty, piece):
    if(rook.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
        return True
    else:
        return bishop.is_move_valid(match, srcx, srcy, dstx, dsty, piece)

