from .. match import *
from .. cvalues import *
from .. import rules
from .. import analyze_helper
from . import rook, bishop
from .generic_piece import cTouch, cFork


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


def is_field_touched(match, color, fieldx, fieldy, mode):
    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and piece == PIECES['wQu']) or
                (color == COLORS['black'] and piece == PIECES['bQu']) ):
                if(mode == 0):
                    return True
                elif(mode == 1):
                    if(is_move_stuck(match, fieldx, fieldy, x1, y1)):
                        continue
                    else:
                        return True
                else: #mode == 2
                    if(is_move_stuck(match, fieldx, fieldy, x1, y1) or analyze_helper.is_soft_pin(match, x1, y1)):
                        continue
                    else:
                        return True

    return False


def is_move_stuck(match, srcx, srcy, dstx, dsty):
    bp_flag = bishop.is_move_stuck(match, srcx, srcy, dstx, dsty)
    rk_flag = rook.is_move_stuck(match, srcx, srcy, dstx, dsty)
    return bp_flag or rk_flag


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked):
    if(is_move_stuck(match, srcx, srcy, dstx, dsty)):
        return False

    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    direction = qu_dir(srcx, srcy, dstx, dsty)

    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]

        x1 = dstx + stepx
        y1 = dsty + stepy

        step_dir = qu_dir(dstx, dsty, x1, y1)
        if(direction == step_dir or direction == rules.REVERSE_DIRS[step_dir]):
            continue

        while(rules.is_inbounds(x1, y1)):
            fork_field = match.readfield(x1, y1)
            
            if(Match.color_of_piece(fork_field) == opp_color):
                break

            if(analyze_helper.is_fork_field(match, piece, x1, y1)):
                cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                forked.append(cfork)
                return True

            if(Match.color_of_piece(fork_field) == color):
                break

            x1 += stepx
            y1 += stepy

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
                if(rules.is_field_touched(match, color, x1, y1, 1) == False):
                    count += 1
                elif(PIECES_RANK[piece] > PIECES_RANK[PIECES['wQu']]):
                    count += 1
            """else:
                count -= 1"""

    return count


def qu_dir(srcx, srcy, dstx, dsty):
    DIRS = rules.DIRS
    if( (srcx == dstx) and (srcy < dsty) ):
        return DIRS['north']
    elif( (srcx == dstx) and (srcy > dsty) ):
        return DIRS['south']
    elif( (srcx < dstx) and (srcy == dsty) ):
        return DIRS['east']
    elif( (srcx > dstx) and (srcy == dsty) ):
        return DIRS['west']
    elif( (srcx - dstx) == (srcy - dsty) and (srcy < dsty) ):
        return DIRS['north-east']
    elif( (srcx - dstx) == (srcy - dsty) and (srcy > dsty) ):
        return DIRS['south-west']
    elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy < dsty) ):
        return DIRS['north-west']
    elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy > dsty) ):
        return DIRS['south-east']
    else:
        return DIRS['undefined']


def is_move_valid(match, srcx, srcy, dstx, dsty, piece):
    if(rook.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
        return True
    else:
        return bishop.is_move_valid(match, srcx, srcy, dstx, dsty, piece)

