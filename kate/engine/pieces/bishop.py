from .. match import *
from .. import rules
from .. cvalues import *
from .generic_piece import contacts_to_token


NEAST_X = 1
NEAST_Y = 1
SWEST_X = -1
SWEST_Y = -1
NWEST_X = -1
NWEST_Y = 1
SEAST_X = 1
SEAST_Y = -1

STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]

blank = PIECES['blk']
GEN_STEPS = [ [[1, 1, blank], [2, 2, blank], [3, 3, blank], [4, 4, blank], [5, 5, blank], [6, 6, blank], [7, 7, blank]],
              [[-1, -1, blank], [-2, -2, blank], [-3, -3, blank], [-4, -4, blank], [-5, -5, blank], [-6, -6, blank], [-7, -7, blank]],
              [[1, -1, blank], [2, -2, blank], [3, -3, blank], [4, -4, blank], [5, -5, blank], [6, -6, blank], [7, -7, blank]],
              [[-1, 1, blank], [-2, 2, blank], [-3, 3, blank], [-4, 4, blank], [-5, 5, blank], [-6, 6, blank], [-7, 7, blank]] ]


def is_field_touched(match, color, fieldx, fieldy):
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and (piece == PIECES['wQu'] or piece == PIECES['wBp'])) or
                (color == COLORS['black'] and (piece == PIECES['bQu'] or piece == PIECES['bBp'])) ):
                return True

    return False


def field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches):
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(piece != PIECES['wQu'] and piece != PIECES['bQu'] and piece != PIECES['wBp'] and piece != PIECES['bBp']):
                continue
            pin_dir = rules.pin_dir(match, x1, y1)
            direction = bp_dir(fieldx, fieldy, x1, y1)
            if(pin_dir != direction and pin_dir != rules.DIRS['undefined']):
                continue
            if(Match.color_of_piece(piece) == color):
                frdlytouches.append(piece)
            else:
                enmytouches.append(piece)


def list_field_touches(match, color, fieldx, fieldy):
    touches = []
    
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and (piece == PIECES['wQu'] or piece == PIECES['wBp'])) or
                (color == COLORS['black'] and (piece == PIECES['bQu'] or piece == PIECES['bBp'])) ):
                touches.append([piece, x1, y1])

    return touches

  
def touches(match, srcx, srcy, dstx, dsty):
    token = 0x0

    bishop = match.readfield(srcx, srcy)

    if(bishop != PIECES['wBp'] and bishop != PIECES['wQu'] and bishop != PIECES['bBp'] and bishop != PIECES['bQu']):
        return token

    color = Match.color_of_piece(bishop)
    opp_color = Match.oppcolor_of_piece(bishop)

    ###
    match.writefield(srcx, srcy, PIECES['blk'])

    frdlycontacts, enmycontacts = rules.field_touches(match, color, dstx, dsty)

    match.writefield(srcx, srcy, bishop)

    token = token | contacts_to_token(frdlycontacts, enmycontacts, "FIELDTOUCHES")
    ###

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                token = token | MV_IS_ATTACK

                if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                    token = token | ATTACKED_IS_PAWN
                elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    token = token | ATTACKED_IS_KING
                elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                    token = token | ATTACKED_IS_QUEEN
                else:
                    token = token | ATTACKED_IS_OFFICER
                
                ###
                match.writefield(srcx, srcy, PIECES['blk'])

                frdlycontacts, enmycontacts = rules.field_touches(match, color, x1, y1)

                match.writefield(srcx, srcy, bishop)

                token = token | contacts_to_token(frdlycontacts, enmycontacts, "ATTACKTOUCHES")
                ###
            else:
                if(x1 == srcx and y1 == srcy):
                    continue
                piece = match.readfield(x1, y1)
                if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    continue

                token = token | MV_IS_SUPPORT
                if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                    token = token | SUPPORTED_IS_PAWN
                elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                    token = token | SUPPORTED_IS_QUEEN
                else:
                    token = token | SUPPORTED_IS_OFFICER

                ###
                match.writefield(srcx, srcy, PIECES['blk'])

                frdlycontacts, enmycontacts = rules.field_touches(match, color, x1, y1)

                match.writefield(srcx, srcy, bishop)

                token = token | contacts_to_token(frdlycontacts, enmycontacts, "SUPPORTTOUCHES")
                ###

    return token


def score_attacks(match, srcx, srcy):
    score = 0

    bishop = match.readfield(srcx, srcy)

    if(bishop != PIECES['wBp'] and bishop != PIECES['wQu'] and bishop != PIECES['bBp'] and bishop != PIECES['bQu']):
        return score

    color = Match.color_of_piece(bishop)
    opp_color = Match.oppcolor_of_piece(bishop)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == opp_color):
                pin_dir = rules.pin_dir(match, srcx, srcy)
                direction = bp_dir(srcx, srcy, x1, y1)
                if(pin_dir == direction or pin_dir == rules.DIRS['undefined']):
                    score += ATTACKED_SCORES[piece]

    return score


def score_supports_of_attacked(match, srcx, srcy):
    score = 0

    bishop = match.readfield(srcx, srcy)

    if(bishop != PIECES['wBp'] and bishop != PIECES['wQu'] and bishop != PIECES['bBp'] and bishop != PIECES['bQu']):
        return score

    color = Match.color_of_piece(bishop)
    opp_color = Match.oppcolor_of_piece(bishop)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    score += SUPPORTED_SCORES[piece]

    return score 


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
        elif(field != PIECES['blk']):
            return False

        x += stepx
        y += stepy

    return False

