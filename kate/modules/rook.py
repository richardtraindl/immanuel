from kate.models import Match
from kate.modules import rules


NORTH_X = 0
NORTH_Y = 1
SOUTH_X = 0
SOUTH_Y = -1
EAST_X = 1
EAST_Y = 0
WEST_X = -1
WEST_Y = 0


def is_field_attacked(match, color, fieldx, fieldy)
    RK_STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    for i in range(4):
        stepx = RK_STEPS[i][0]
        stepy = RK_STEPS[i][1]
        x1, y1 = search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == Match.COLORS['white'] and (piece == Match.PIECES['wQu'] or piece == Match.PIECES['wRk'])) or
                (color == Match.COLORS['black'] and (piece == Match.PIECES['bQu'] or piece == Match.PIECES['bRk'])) ):
                return True

    return False


def does_attack(match, opp_color, srcx, srcy):
    RK_STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    for i in range(4):
        stepx = RK_STEPS[i][0]
        stepy = RK_STEPS[i][1]
        x1, y1 = search(match, srcx, srcy, stepx , stepy)
        if(x1 != UNDEF_X):
            piece = match.readfield(x1, y1)
            if( piece != Match.PIECES['blk'] and opp_color != Match.color_of_piece(piece) ):
                return True

    return False


def rk_dir(srcx, srcy, dstx, dsty):
    DIRS = rules.DIRS
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


def rk_step(direction=None, srcx=None, srcy=None, dstx=None, dsty=None):
    DIRS = rules.DIRS
    if(direction == None):
        direction = rk_dir(srcx, srcy, dstx, dsty)

    if(direction == DIRS['north']):
        return direction, NORTH_X, NORTH_Y
    elif(direction == DIRS['south']):
        return direction, SOUTH_X, SOUTH_Y
    elif(direction == DIRS['east']):
        return direction, EAST_X, EAST_Y
    elif(direction == DIRS['west']):
        return direction, WEST_X, WEST_Y
    else:
        return direction, rules.UNDEF_X, rules.UNDEF_Y

    
def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    DIRS = rules.DIRS
    direction, stepx, stepy = rk_step(None, srcx, srcy, dstx, dsty)
    if(direction == DIRS['undefined']):
        return False

    color = Match.color_of_piece(piece)

    pin_dir = rules.pin_dir(match, srcx, srcy)

    if(direction == DIRS['north'] or direction == DIRS['south']):
        if(pin_dir != DIRS['north'] and pin_dir != DIRS['south'] and pin_dir != DIRS['undefined']):
            return False
    elif(direction == DIRS['east'] or direction == DIRS['west']):
        if(pin_dir != DIRS['east'] and pin_dir != DIRS['west'] and pin_dir != DIRS['undefined']):
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

