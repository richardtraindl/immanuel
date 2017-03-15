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

STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]


def is_field_attacked(match, color, fieldx, fieldy):
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == Match.COLORS['white'] and (piece == Match.PIECES['wQu'] or piece == Match.PIECES['wBp'])) or
                (color == Match.COLORS['black'] and (piece == Match.PIECES['bQu'] or piece == Match.PIECES['bBp'])) ):
                return True

    return False


def does_attack(match, srcx, srcy):
    bishop = match.readfield(srcx, srcy)

    if(bishop != Match.PIECES['wBp'] and bishop != Match.PIECES['bBp']):
        return False

    color = Match.color_of_piece(bishop)

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

    bishop = match.readfield(srcx, srcy)

    if(bishop != Match.PIECES['wBp'] and bishop != Match.PIECES['bBp']):
        return count

    color = Match.color_of_piece(bishop)

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

    bishop = match.readfield(srcx, srcy)

    if(bishop != Match.PIECES['wBp'] and bishop != Match.PIECES['bBp']):
        return score

        color = Match.color_of_piece(bishop)

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
    bishop = match.readfield(srcx, srcy)

    if(bishop != Match.PIECES['wBp'] and bishop != Match.PIECES['bBp']):
        return False

    color = Match.color_of_piece(bishop)

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

    
def is_move_valid(match, srcx, srcy, dstx, dsty, piece):
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

