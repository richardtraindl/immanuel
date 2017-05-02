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

blank = Match.PIECES['blk']
GEN_STEPS = [ [[0, 1, blank], [0, 2, blank], [0, 3, blank], [0, 4, blank], [0, 5, blank], [0, 6, blank], [0, 7, blank]],
              [[0, -1, blank], [0, -2, blank], [0, -3, blank], [0, -4, blank], [0, -5, blank], [0, -6, blank], [0, -7, blank]],
              [[1, 0, blank], [2, 0, blank], [3, 0, blank], [4, 0, blank], [5, 0, blank], [6, 0, blank], [7, 0, blank]],
              [[-1, 0, blank], [-2, 0, blank], [-3, 0, blank], [-4, 0, blank], [-5, 0, blank], [-6, 0, blank], [-7, 0, blank]] ]


def is_field_touched(match, color, fieldx, fieldy):
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


def does_attack(match, srcx, srcy, dstx, dsty):
    priority = 5

    rook = match.readfield(srcx, srcy)

    if(rook != Match.PIECES['wRk'] and rook != Match.PIECES['wQu'] and rook != Match.PIECES['bRk'] and rook != Match.PIECES['bQu']):
        return False, 0

    color = Match.color_of_piece(rook)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                if(piece == Match.PIECES['wPw'] or piece == Match.PIECES['bPw']):
                    priority = min(priority, 3)
                elif(piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                    return True, 1 # priority
                else:
                    priority = min(priority, 2)

    if(priority == 5):
        return False, 0
    else:
        return True, priority


def count_attacks(match, srcx, srcy, dstx, dsty):
    count = 0

    rook = match.readfield(srcx, srcy)

    if(rook != Match.PIECES['wRk'] and rook != Match.PIECES['wQu'] and rook != Match.PIECES['bRk'] and rook != Match.PIECES['bQu']):
        return count

    color = Match.color_of_piece(rook)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                count += 1

    return count


def score_attacks(match, srcx, srcy):
    score = 0

    rook = match.readfield(srcx, srcy)

    if(rook != Match.PIECES['wRk'] and rook != Match.PIECES['wQu'] and rook != Match.PIECES['bRk'] and rook != Match.PIECES['bQu']):
        return score

        color = Match.color_of_piece(rook)
        opp_color = Match.REVERSED_COLORS[color]

        for i in range(4):
            stepx = STEPS[i][0]
            stepy = STEPS[i][1]
            x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
            if(x1 != rules.UNDEF_X):
                piece = match.readfield(x1, y1)
                if(Match.color_of_piece(piece) == opp_color):
                    score += Match.ATTACKED_SCORES[piece]
                    pin_dir = rules.pin_dir(match, x1, y1)
                    direction = rk_dir(srcx, srcy, x1, y1)
                    if(pin_dir == direction):
                        if(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk'] or piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
                            score += Match.ATTACKED_SCORES[piece] // 4
                        else:
                            score += Match.ATTACKED_SCORES[piece] // 2
    return score


def does_support_attacked(match, srcx, srcy, dstx, dsty):
    priority = 5

    rook = match.readfield(srcx, srcy)

    if(rook != Match.PIECES['wRk'] and rook != Match.PIECES['wQu'] and rook != Match.PIECES['bRk'] and rook != Match.PIECES['bQu']):
        return False, 0

    color = Match.color_of_piece(rook)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    if(piece == Match.PIECES['wPw'] or piece == Match.PIECES['bPw']):
                        priority = min(priority, 3)
                    else:
                        return True, 2 # priority

    if(priority == 5):
        return False, 0
    else:
        return True, priority


def score_supports_of_attacked(match, srcx, srcy):
    score = 0

    rook = match.readfield(srcx, srcy)

    if(rook != Match.PIECES['wRk'] and rook != Match.PIECES['wQu'] and rook != Match.PIECES['bRk'] and rook != Match.PIECES['bQu']):
        return score

    color = Match.color_of_piece(rook)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    score += Match.SUPPORTED_SCORES[piece]

    return score 

  
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

