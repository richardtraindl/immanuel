from .. match import *
from .. import rules
from .. cvalues import *


NORTH_X = 0
NORTH_Y = 1
SOUTH_X = 0
SOUTH_Y = -1
EAST_X = 1
EAST_Y = 0
WEST_X = -1
WEST_Y = 0

STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]

blank = PIECES['blk']
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
            if( (color == COLORS['white'] and (piece == PIECES['wQu'] or piece == PIECES['wRk'])) or
                (color == COLORS['black'] and (piece == PIECES['bQu'] or piece == PIECES['bRk'])) ):
                return True

    return False


def field_touches(match, color, fieldx, fieldy, fdlytouches, enmytouches):
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == color):
                fdlytouches.append(piece)
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
            if( (color == COLORS['white'] and (piece == PIECES['wQu'] or piece == PIECES['wRk'])) or
                (color == COLORS['black'] and (piece == PIECES['bQu'] or piece == PIECES['bRk'])) ):
                touches.append([piece, x1, y1])

    return touches


def does_attack(match, srcx, srcy, dstx, dsty):
    priority = PRIO['undefined']

    rook = match.readfield(srcx, srcy)

    if(rook != PIECES['wRk'] and rook != PIECES['wQu'] and rook != PIECES['bRk'] and rook != PIECES['bQu']):
        return False, priority

    color = Match.color_of_piece(rook)
    opp_color = Match.oppcolor_of_piece(rook)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    return True, PRIO['prio2']
                else:
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        priority = min(priority, PRIO['prio3'])
                    else:
                        match.writefield(srcx, srcy, PIECES['blk'])
                        friendlysupported = rules.is_field_touched(match, color, dstx, dsty)
                        attacked = rules.is_field_touched(match, opp_color, dstx, dsty)
                        match.writefield(srcx, srcy, rook)
                        if(not attacked):
                            priority = min(priority, PRIO['prio3'])
                        elif(friendlysupported):
                            if(PIECES_RANK[piece] >= PIECES_RANK[rook]):
                                priority = min(priority, PRIO['prio3'])
                            else:
                                priority = min(priority, PRIO['prio4'])
                        else:
                            priority = min(priority, PRIO['prio4'])

    if(priority == PRIO['undefined']):
        return False, priority
    else:
        return True, priority


def count_contacts(contacts):
    pawncnt = 0
    officercnt = 0

    for contact in contacts:
        if(contact == PIECES['wPw'] or contact == PIECES['bPw']):
            pawncnt += 1
        else:
            officercnt += 1
    return pawncnt, officercnt

def touches(match, srcx, srcy, dstx, dsty):
    token = 0x0

    rook = match.readfield(srcx, srcy)

    if(rook != PIECES['wRk'] and rook != PIECES['wQu'] and rook != PIECES['bRk'] and rook != PIECES['bQu']):
        return token

    color = Match.color_of_piece(rook)
    opp_color = Match.oppcolor_of_piece(rook)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                token = token | MV_IS_ATTACK

                if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    token = token | ATTACKED_IS_KING
                elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                    token = token | ATTACKED_IS_PAWN
                else:
                    token = token | ATTACKED_IS_OFFICER

                match.writefield(srcx, srcy, PIECES['blk'])

                fdlycontacts, enmycontacts = rules.field_touches(match, color, x1, y1)

                match.writefield(srcx, srcy, piece)
                
                pawncnt, officercnt = count_contacts(fdlycontacts)
                if(pawncnt > 0):
                    token = token | ATT_IS_ADD_ATT_FROM_PAWN
                if(officercnt > 0):
                    token = token | ATT_IS_ADD_ATT_FROM_OFFICER

                pawncnt, officercnt = count_contacts(enmycontacts)
                if(pawncnt > 0):
                    token = token | ATT_IS_SUPP_BY_PAWN
                if(officercnt > 0):
                    token = token | ATT_IS_SUPP_BY_OFFICER

            else:
                if(x1 == srcx and y1 == srcy):
                    continue
                piece = match.readfield(x1, y1)
                if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    continue

                token = token | MV_IS_SUPPORT
                if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                    token = token | SUPPORTED_IS_PAWN
                else:
                    token = token | SUPPORTED_IS_OFFICER

                match.writefield(srcx, srcy, PIECES['blk'])

                fdlycontacts, enmycontacts = rules.field_touches(match, color, x1, y1)

                match.writefield(srcx, srcy, piece)

                pawncnt, officercnt = count_contacts(fdlycontacts)
                if(pawncnt > 0):
                    token = token | SUPPORTED_IS_ADD_SUPP_BY_PAWN
                if(officercnt > 0):
                    token = token | SUPPORTED_IS_ADD_SUPP_BY_OFFICER

                pawncnt, officercnt = count_contacts(enmycontacts)
                if(pawncnt > 0):
                    token = token | SUPPORTED_IS_ATT_FROM_PAWN
                if(officercnt > 0):
                    token = token | SUPPORTED_IS_ATT_FROM_OFFICER

    return token


def count_attacks(match, srcx, srcy, dstx, dsty):
    count = 0

    rook = match.readfield(srcx, srcy)

    if(rook != PIECES['wRk'] and rook != PIECES['wQu'] and rook != PIECES['bRk'] and rook != PIECES['bQu']):
        return count

    color = Match.color_of_piece(rook)
    opp_color = Match.oppcolor_of_piece(rook)

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

    if(rook != PIECES['wRk'] and rook != PIECES['wQu'] and rook != PIECES['bRk'] and rook != PIECES['bQu']):
        return score

    color = Match.color_of_piece(rook)
    opp_color = Match.oppcolor_of_piece(rook)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                score += ATTACKED_SCORES[piece]
                pin_dir = rules.pin_dir(match, x1, y1)
                direction = rk_dir(srcx, srcy, x1, y1)
                if(pin_dir == direction):
                    if(piece == PIECES['wRk'] or piece == PIECES['bRk'] or piece == PIECES['wQu'] or piece == PIECES['bQu']):
                        score += ATTACKED_SCORES[piece] // 4
                    else:
                        score += ATTACKED_SCORES[piece] // 2
    return score


def does_support_attacked(match, srcx, srcy, dstx, dsty):
    priority = PRIO['undefined']

    rook = match.readfield(srcx, srcy)

    if(rook != PIECES['wRk'] and rook != PIECES['wQu'] and rook != PIECES['bRk'] and rook != PIECES['bQu']):
        return False, priority

    color = Match.color_of_piece(rook)
    opp_color = Match.oppcolor_of_piece(rook)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        return True, PRIO['prio3']
                    else:
                        return True, PRIO['prio4']

    if(priority == PRIO['undefined']):
        return False, priority
    else:
        return True, priority


def score_supports_of_attacked(match, srcx, srcy):
    score = 0

    rook = match.readfield(srcx, srcy)

    if(rook != PIECES['wRk'] and rook != PIECES['wQu'] and rook != PIECES['bRk'] and rook != PIECES['bQu']):
        return score

    color = Match.color_of_piece(rook)
    opp_color = Match.oppcolor_of_piece(rook)

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
            if(match.color_of_piece(field) == color):
                return False
            else:
                return True
        elif(field != PIECES['blk']):
            return False

        x += stepx
        y += stepy

    return False

