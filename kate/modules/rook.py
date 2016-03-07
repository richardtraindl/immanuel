from kate.models import Match
from kate.modules import values, rules

DIRS = {
    'north' : 1,
    'south' : 2,
    'east' : 3,
    'west' : 4,
    'undefined' : 10 }

REVERSE_DIRS = {
    DIRS['north'] : DIRS['south'],
    DIRS['south'] : DIRS['north'],
    DIRS['east'] : DIRS['west'],
    DIRS['west'] : DIRS['east'],
    DIRS['undefined'] : 10 }

NORTH_X = 0
NORTH_Y = 1
SOUTH_X = 0
SOUTH_Y = -1
EAST_X = 1
EAST_Y = 0
WEST_X = -1
WEST_Y = 0


def direction(srcx, srcy, dstx, dsty):
    if( (srcx == dstx) and (srcy < dsty) ):
        return DIRS['north']
    elif( (srcx == dstx) and (srcy > dsty) ):
        return DIRS['south']
    elif( (srcx < dstx) and (srcy == dsty) ):
        return DIRS['east']
    elif( (srcx > dstx) and (srcy == dsty) ):
        return DIRS['west']
    else:
        return DIRS['undefined']


def step(rook_direction=None, srcx=None, srcy=None, dstx=None, dsty=None):
    if(rook_direction == None):
        rook_direction = direction(srcx, srcy, dstx, dsty)

    if(rook_direction == DIRS['north']):
        return NORTH_X, NORTH_Y
    elif(rook_direction == DIRS['south']):
        return SOUTH_X, SOUTH_Y
    elif(rook_direction == DIRS['east']):
        return EAST_X, EAST_Y
    elif(rook_direction == DIRS['west']):
        return WEST_X, WEST_Y
    else:
        return 8, 8


def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    rook_direction = direction(srcx, srcy, dstx, dsty)
    if(rook_direction == DIRS['undefined']):
        return False

    stepx, stepy = step(None, srcx, srcy, dstx, dsty)
    color = match.color_of_piece(piece)
    if(color == match.COLORS['white']):
        pin_direction = rules.pinned(match, color, srcx, srcy, match.wKg_x, match.wKg_y)
    else:
        pin_direction = rules.pinned(match, color, srcx, srcy, match.bKg_x, match.bKg_y)

    if(rook_direction == DIRS['north'] or rook_direction == DIRS['south']):
        if(pin_direction != DIRS['north'] and pin_direction != DIRS['south'] and pin_direction != DIRS['undefined']):
            return False
    elif(rook_direction == DIRS['east'] or rook_direction == DIRS['west']):
        if(pin_direction != DIRS['east'] and pin_direction != DIRS['west'] and pin_direction != DIRS['undefined']):
            return False

    x = srcx + stepx
    y = srcy + stepy
    while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
        field = match.readfield(x, y)
        if(x == dstx and y == dsty):
            if(match.color_of_piece(field) == match.color_of_piece(piece)):
                return False
            else:
                return True
        elif(field != match.PIECES['blk']):
            return False

        x += stepx
        y += stepy

    return False






