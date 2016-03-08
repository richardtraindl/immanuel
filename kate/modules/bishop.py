from kate.models import Match
from kate.modules import values, rules


NEAST_X = 1
NEAST_Y = 1
SWEST_X = -1
SWEST_Y = -1
NWEST_X = -1
NWEST_Y = 1
SEAST_X = 1
SEAST_Y = -1


def bp_dir(srcx, srcy, dstx, dsty):
    if( (srcx - dstx) == (srcy - dsty) and (srcy < dsty) ):
        return rules.DIRS['north-east']
    elif( (srcx - dstx) == (srcy - dsty) and (srcy > dsty) ):
        return rules.DIRS['south-west']
    elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy < dsty) ):
        return rules.DIRS['north-west']
    elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy > dsty) ):
        return rules.DIRS['south-east']
    else:
        return rules.DIRS['undefined']


def bp_step(direction=None, srcx=None, srcy=None, dstx=None, dsty=None):
    if(direction == None):
        direction = bp_dir(srcx, srcy, dstx, dsty)

    if(direction == rules.DIRS['north-east']):
        return direction, NEAST_X, NEAST_Y
    elif(direction == rules.DIRS['south-west']):
        return direction, SWEST_X, SWEST_Y
    elif(direction == rules.DIRS['north-west']):
        return direction, NWEST_X, NWEST_Y
    elif(direction == rules.DIRS['south-east']):
        return direction, SEAST_X, SEAST_Y
    else:
        return direction, UNDEF_X, UNDEF_Y


def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    direction, stepx, stepy = rk_step(None, srcx, srcy, dstx, dsty)
    if(direction == rules.DIRS['undefined']):
        return False

    color = Match.color_of_piece(piece)

    pin_dir = rules.pin_dir(match, srcx, srcy)

    if(direction == rules.DIRS['north-east'] or direction == rules.DIRS['south-west']):
        if(pin_dir != rules.DIRS['north-east'] and pin_dir != rules.DIRS['south-west'] and pin_dir != rules.DIRS['undefined']):
            return False
    elif(direction == rules.DIRS['north-west'] or direction == rules.DIRS['south-east']):
        if(pin_dir != rules.DIRS['north-west'] and pin_dir != rules.DIRS['south-east'] and pin_dir != rules.DIRS['undefined']):
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

