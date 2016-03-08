from kate.models import Match
from kate.modules import values, rules


NORTH_X = 0
NORTH_Y = 1
SOUTH_X = 0
SOUTH_Y = -1
EAST_X = 1
EAST_Y = 0
WEST_X = -1
WEST_Y = 0


def rk_dir(srcx, srcy, dstx, dsty):
    if( (srcx == dstx) and (srcy < dsty) ):
        return rules.DIRS['north']
    elif( (srcx == dstx) and (srcy > dsty) ):
        return rules.DIRS['south']
    elif( (srcx < dstx) and (srcy == dsty) ):
        return rules.DIRS['east']
    elif( (srcx > dstx) and (srcy == dsty) ):
        return rules.DIRS['west']
    else:
        return rules.DIRS['undefined']


def rk_step(direction=None, srcx=None, srcy=None, dstx=None, dsty=None):
    if(direction == None):
        direction = rk_dir(srcx, srcy, dstx, dsty)

    if(direction == rules.DIRS['north']):
        return direction, NORTH_X, NORTH_Y
    elif(direction == rules.DIRS['south']):
        return direction, SOUTH_X, SOUTH_Y
    elif(direction == rules.DIRS['east']):
        return direction, EAST_X, EAST_Y
    elif(direction == rules.DIRS['west']):
        return direction, WEST_X, WEST_Y
    else:
        return direction, UNDEF_X, UNDEF_Y


def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    direction, stepx, stepy = rk_step(None, srcx, srcy, dstx, dsty)
    if(direction == rules.DIRS['undefined']):
        return False

    color = Match.color_of_piece(piece)

    pin_dir = rules.pin_dir(match, srcx, srcy)

    if(direction == rules.DIRS['north'] or direction == rules.DIRS['south']):
        if(pin_dir != rules.DIRS['north'] and pin_dir != rules.DIRS['south'] and pin_dir != rules.DIRS['undefined']):
            return False
    elif(direction == rules.DIRS['east'] or direction == rules.DIRS['west']):
        if(pin_dir != rules.DIRS['east'] and pin_dir != rules.DIRS['west'] and pin_dir != rules.DIRS['undefined']):
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

