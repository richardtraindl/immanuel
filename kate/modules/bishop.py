from kate.models import Match
from kate.modules import rules


NEAST_X = 1
NEAST_Y = 1
SWEST_X = -1
SWEST_Y = -1
NWEST_X = -1
NWEST_Y = 1
SEAST_X = 1
SEAST_Y = -1


def is_field_attacked(match, color, fieldx, fieldy):
    BP_STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
    for i in range(4):
        stepx = BP_STEPS[i][0]
        stepy = BP_STEPS[i][1]
        x1, y1 = search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == Match.COLORS['white'] and (piece == Match.PIECES['wQu'] or piece == Match.PIECES['wBp'])) or
                (color == Match.COLORS['black'] and (piece == Match.PIECES['bQu'] or piece == Match.PIECES['bBp'])) ):
                return True

    return False


def does_attack_opponent(match, opp_color, srcx, srcy):
    BP_STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
    for i in range(4):
        stepx = BP_STEPS[i][0]
        stepy = BP_STEPS[i][1]
        x1, y1 = search(match, srcx, srcy, stepx , stepy)
        if(x1 != UNDEF_X):
            piece = match.readfield(x1, y1)
            if( piece != Match.PIECES['blk'] and opp_color != Match.color_of_piece(piece) ):
                return True

    return False


def bp_dir(srcx, srcy, dstx, dsty):
    DIRS = rules.DIRS
    if( (srcx - dstx) == (srcy - dsty) and (srcy < dsty) ):
        return DIRS['north-east']
    elif( (srcx - dstx) == (srcy - dsty) and (srcy > dsty) ):
        return DIRS['south-west']
    elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy < dsty) ):
        return DIRS['north-west']
    elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy > dsty) ):
        return DIRS['south-east']
    else:
        return DIRS['undefined']


def bp_step(direction=None, srcx=None, srcy=None, dstx=None, dsty=None):
    DIRS = rules.DIRS
    if(direction == None):
        direction = bp_dir(srcx, srcy, dstx, dsty)

    if(direction == DIRS['north-east']):
        return direction, NEAST_X, NEAST_Y
    elif(direction == DIRS['south-west']):
        return direction, SWEST_X, SWEST_Y
    elif(direction == DIRS['north-west']):
        return direction, NWEST_X, NWEST_Y
    elif(direction == DIRS['south-east']):
        return direction, SEAST_X, SEAST_Y
    else:
        return direction, rules.UNDEF_X, rules.UNDEF_Y

    
def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    DIRS = rules.DIRS
    direction, stepx, stepy = bp_step(None, srcx, srcy, dstx, dsty)
    if(direction == DIRS['undefined']):
        return False

    color = Match.color_of_piece(piece)

    pin_dir = rules.pin_dir(match, srcx, srcy)

    if(direction == DIRS['north-east'] or direction == DIRS['south-west']):
        if(pin_dir != DIRS['north-east'] and pin_dir != DIRS['south-west'] and pin_dir != DIRS['undefined']):
            return False
    elif(direction == DIRS['north-west'] or direction == DIRS['south-east']):
        if(pin_dir != DIRS['north-west'] and pin_dir != DIRS['south-east'] and pin_dir != DIRS['undefined']):
            return False

    x = srcx + stepx
    y = srcy + stepy
    while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
        field = match.readfield(x, y)
        if(x == dstx and y == dsty):
            if(Match.color_of_piece(field) == color):
                return False
            else:
                return True
        elif(field != Match.PIECES['blk']):
            return False

        x += stepx
        y += stepy

    return False

