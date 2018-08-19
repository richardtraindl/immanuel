from .rook import cRook
from .bishop import cBishop
from .. import analyze_helper


MAX_STEP_IDX_FOR_RK = 3

STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]

def is_move_stuck(match, srcx, srcy, dstx, dsty):
    cbishop = cBishop(match, srcx, srcy)
    bp_flag = cbishop.is_move_stuck(dstx, dsty)
    crook = cRook(match, srcx, srcy)
    rk_flag = crook.is_move_stuck(dstx, dsty)
    return bp_flag or rk_flag

def defends_fork_field(match, piece, srcx, srcy, dstx, dsty): # , analyses
    if(is_move_stuck(match, srcx, srcy, dstx, dsty)):
        return False

    color = match.color_of_piece(piece)
    opp_color = match.oppcolor_of_piece(piece)

    direction = qu_dir(srcx, srcy, dstx, dsty)

    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]

        x1 = dstx + stepx
        y1 = dsty + stepy

        step_dir = qu_dir(dstx, dsty, x1, y1)
        if(direction == step_dir or direction == match.REVERSE_DIRS[step_dir]):
            continue

        while(match.is_inbounds(x1, y1)):
            fork_field = match.readfield(x1, y1)
            
            if(match.color_of_piece(fork_field) == opp_color):
                break

            if(analyze_helper.is_fork_field(match, piece, x1, y1)):
                #cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                #analyses.lst_fork_defended.append(cfork)
                return True

            if(match.color_of_piece(fork_field) == color):
                break

            x1 += stepx
            y1 += stepy

    return False


def count_touches(match, color, fieldx, fieldy):
    count = 0

    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = match.search(fieldx, fieldy, stepx, stepy)
        if(x1 != match.UNDEF_X):
            if(is_move_stuck(match, fieldx, fieldy, x1, y1)):
                continue

            piece = match.readfield(x1, y1)
            if(piece == match.PIECES['blk']):
                continue
            elif(match.color_of_piece(piece) == color):
                if(match.is_field_touched(color, x1, y1, 1) == False):
                    count += 1
                elif(match.PIECES_RANK[piece] > match.PIECES_RANK[match.PIECES['wQu']]):
                    count += 1
            """else:
                count -= 1"""

    return count

