from kate.models import Match
from kate.modules import values, rules


STEP_1N_X = 0
STEP_1N_Y = 1
STEP_1N1E_X = 1
STEP_1N1E_Y = 1
STEP_1E_X = 1
STEP_1E_Y = 0
STEP_1S1E_X = 1
STEP_1S1E_Y = -1
STEP_1S_X = 0
STEP_1S_Y = -1
STEP_1S1W_X = -1
STEP_1S1W_Y = -1
STEP_1W_X = -1
STEP_1W_Y = 0
STEP_1N1W_X = -1
STEP_1N1W_Y = 1


def kg_dir(srcx, srcy, dstx, dsty):
    step_x = dstx - srcx
    step_y = dsty - srcy
    if(step_x == STEP_1N_X and step_y == STEP_1N_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1N1E_X and step_y == STEP_1N1E_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1E_X and step_y == STEP_1E_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1S1E_X and step_y == STEP_1S1E_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1S_X and step_y == STEP_1S_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1S1W_X and step_y == STEP_1S1W_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1W_X and step_y == STEP_1W_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1N1W_X and step_y == STEP_1N1W_Y):
        return KING_DIRS['valid']
    else:
        return KING_DIRS['undefined']


def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    direction = kg_dir(srcx, srcy, dstx, dsty)
    if(direction == DIRS['undefined']):
        return False

    color = Match.color_of_piece(piece)

    king = match.readfield(srcx, srcy)
    captured = match.readfield(dstx, dsty)
    match.writefield(srcx, srcy, PIECES['blk'])
    match.writefield(dstx, dsty, king)
    flag = attacked(match, dstx, dsty)
    match.writefield(srcx, srcy, king)
    match.writefield(dstx, dsty, captured)
    if(flag == True):
        return False

    field = match.readfield(dstx, dsty)
    if(match.color_of_piece(field) == color):
        return False

    return True

