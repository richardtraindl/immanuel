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

STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]

GEN_STEPS = [ [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
              [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
              [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
              [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]] ]


def is_field_attacked(match, color, fieldx, fieldy):
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == Match.COLORS['white'] and (piece == Match.PIECES['wQu'] or piece == Match.PIECES['wRk'])) or
                (color == Match.COLORS['black'] and (piece == Match.PIECES['bQu'] or piece == Match.PIECES['bRk'])) ):
                return True

    return False


def does_attack(match, srcx, srcy):
    rook = match.readfield(srcx, srcy)

    if(rook != Match.PIECES['wRk'] and rook != Match.PIECES['bRk']):
        return False

    color = Match.color_of_piece(rook)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if( Match.REVERSED_COLORS[color] == Match.color_of_piece(piece) ):
                return True

    return False


def count_attacks(match, srcx, srcy):
    count = 0

    rook = match.readfield(srcx, srcy)

    if(rook != Match.PIECES['wRk'] and rook != Match.PIECES['bRk']):
        return count

        color = Match.color_of_piece(rook)

        for i in range(4):
            stepx = STEPS[i][0]
            stepy = STEPS[i][1]
            x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
            if(x1 != rules.UNDEF_X):
                piece = match.readfield(x1, y1)
                if( Match.REVERSED_COLORS[color] == Match.color_of_piece(piece) ):
                    count += 1

    return count


def score_attacks(match, srcx, srcy):
    score = 0

    rook = match.readfield(srcx, srcy)

    if(rook != Match.PIECES['wRk'] and rook != Match.PIECES['bRk']):
        return score

        color = Match.color_of_piece(rook)

        for i in range(4):
            stepx = STEPS[i][0]
            stepy = STEPS[i][1]
            x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
            if(x1 != rules.UNDEF_X):
                piece = match.readfield(x1, y1)
                if( Match.REVERSED_COLORS[color] == Match.color_of_piece(piece) ):
                    score += Match.SCORES[piece]

    return score


def does_support_attacked(match, srcx, srcy):
    rook = match.readfield(srcx, srcy)

    if(rook != Match.PIECES['wRk'] and rook != Match.PIECES['bRk']):
        return False

    color = Match.color_of_piece(rook)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_attacked(match, Match.REVERSED_COLORS[color], x1, y1)):
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

    
def is_move_valid(match, srcx, srcy, dstx, dsty, piece):
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

