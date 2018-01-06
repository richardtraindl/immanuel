from .. match import *
from .. cvalues import *
from .. import rules
from .. import analyze_helper
from .generic_piece import cTouch


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
            if( (color == COLORS['white'] and piece == PIECES['wRk']) or
                (color == COLORS['black'] and piece == PIECES['bRk']) ):
                return True
    return False


def is_move_stuck(match, srcx, srcy, dstx, dsty):
    move_dir = rk_dir(srcx, srcy, dstx, dsty)
    pin_dir = rules.pin_dir(match, srcx, srcy)
    if(pin_dir == rules.DIRS['undefined'] or move_dir == pin_dir):
        return False
    else:
        return True


def field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches):
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(piece == PIECES['wQu'] or piece == PIECES['bQu'] or piece == PIECES['wRk'] or piece == PIECES['bRk']):
                if(is_move_stuck(match, x1, y1, fieldx, fieldy)):
                    continue
                if(Match.color_of_piece(piece) == color):
                    frdlytouches.append(piece)
                else:
                    enmytouches.append(piece)


def field_color_touches_beyond(match, color, ctouch):
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, ctouch.fieldx, ctouch.fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(piece == PIECES['wQu'] or piece == PIECES['bQu'] or piece == PIECES['wRk'] or piece == PIECES['bRk']):
                if(is_move_stuck(match, x1, y1, ctouch.fieldx, ctouch.fieldy)):
                    continue
                if(Match.color_of_piece(piece) == color):
                    ctouch.supporter_beyond.append([piece, x1, y1])
                else:
                    ctouch.attacker_beyond.append([piece, x1, y1])


def list_field_touches(match, color, fieldx, fieldy):
    touches = []
    
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(is_move_stuck(match, x1, y1, fieldx, fieldy)):
                continue

            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and (piece == PIECES['wQu'] or piece == PIECES['wRk'])) or
                (color == COLORS['black'] and (piece == PIECES['bQu'] or piece == PIECES['bRk'])) ):
                touches.append([piece, x1, y1])

    return touches


def attacks_and_supports(match, srcx, srcy, dstx, dsty, attacked, supported):
    token = 0x0

    rook = match.readfield(srcx, srcy)

    color = Match.color_of_piece(rook)
    opp_color = Match.oppcolor_of_piece(rook)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue

            if(is_move_stuck(match, srcx, srcy, x1, y1)):
                continue

            piece = match.readfield(x1, y1)

            if(Match.color_of_piece(piece) == opp_color):
                ctouch = cTouch(srcx, srcy, dstx, dsty, piece, x1, y1)
                attacked.append(ctouch)

                token = token | MV_IS_ATTACK
                if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                    token = token | ATTACKED_IS_PW
                elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                    token = token | ATTACKED_IS_KN
                elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                    token = token | ATTACKED_IS_BP
                elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                    token = token | ATTACKED_IS_RK
                elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                    token = token | ATTACKED_IS_QU
                elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    token = token | ATTACKED_IS_KG

                ###
                match.writefield(srcx, srcy, PIECES['blk'])

                analyze_helper.field_touches_beyond(match, opp_color, ctouch)

                match.writefield(srcx, srcy, rook)
                ###
            else:
                if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    continue

                ctouch = cTouch(srcx, srcy, dstx, dsty, piece, x1, y1)
                supported.append(ctouch)

                token = token | MV_IS_SUPPORT
                if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                    token = token | SUPPORTED_IS_PW
                elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                    token = token | SUPPORTED_IS_KN
                elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                    token = token | SUPPORTED_IS_BP
                elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                    token = token | SUPPORTED_IS_RK
                elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                    token = token | SUPPORTED_IS_QU

                ###
                match.writefield(srcx, srcy, PIECES['blk'])

                analyze_helper.field_touches_beyond(match, color, ctouch)

                match.writefield(srcx, srcy, rook)
                ###

    return token 


def disclosures_field(match, color, excluded_dir, srcx, srcy, disclosed_attacked):
    for j in range(0, 4, 2):
        first = cTouch(None, None, None, None, PIECES['blk'], 0, 0)
        second = cTouch(None, None, None, None, PIECES['blk'], 0, 0)

        for i in range(0, 2, 1):
            stepx = STEPS[j+i][0]
            stepy = STEPS[j+i][1]
            if(excluded_dir == rk_dir(srcx, srcy, (srcx + stepx), (srcy + stepy))):
                break
            x1, y1 = rules.search(match, srcx, srcy, stepx, stepy)
            if(x1 != rules.UNDEF_X):
                piece = match.readfield(x1, y1)
                if(first.piece == PIECES['blk']):
                    first.piece = piece
                    first.fieldx = x1
                    first.fieldy = y1
                    continue
                elif(second.piece == PIECES['blk']):
                    second.piece = piece
                    second.fieldx = x1
                    second.fieldy = y1
                    if(Match.color_of_piece(first.piece) != Match.color_of_piece(second.piece) and 
                       first.piece != PIECES['blk'] and second.piece != PIECES['blk']):
                        if(Match.color_of_piece(first.piece) == color):
                            if(first.piece == PIECES['wRk'] or first.piece == PIECES['bRk'] or 
                               first.piece == PIECES['wQu'] or first.piece == PIECES['bQu']):
                                disclosed_attacked.append(second)
                                return True
                        else:
                            if(second.piece == PIECES['wRk'] or second.piece == PIECES['bRk'] or 
                               second.piece == PIECES['wQu'] or second.piece == PIECES['bQu']):
                                disclosed_attacked.append(first)
                                return True
                    else:
                        break
                else:
                    break

    return False


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
                direction = pin_dir(match, x1, y1)
                if(direction != DIRS['undefined'] and 
                   direction != DIRS['north'] and 
                   direction != DIRS['south'] and 
                   direction != DIRS['east'] and 
                   direction != DIRS['west']):
                    score += ATTACKED_SCORES[piece]

                if(PIECES_RANK[piece] > PIECES_RANK[rook]):
                    score += ATTACKED_SCORES[piece] * 2
                else:
                    score += ATTACKED_SCORES[piece]

    return score


def score_supports(match, srcx, srcy):
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
            if(is_move_stuck(match, srcx, srcy, x1, y1)):
                continue

            piece = match.readfield(x1, y1)
            if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    score += SUPPORTED_SCORES[piece]

    return score 


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked):
    if(is_move_stuck(match, srcx, srcy, dstx, dsty)):
        return False

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(is_move_stuck(match, dstx, dsty, x1, y1)):
                continue

            if(analyze_helper.is_fork_field(match, piece, srcx, srcy, x1, y1)):
                forked.append([srcx, srcy, dstx, dsty,  x1, y1])
                return True
    return False


def count_attacks(match, color, fieldx, fieldy):
    count = 0

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(is_move_stuck(match, fieldx, fieldy, x1, y1)):
                continue

            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == color):
                if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    count += 1
                elif(rules.is_field_touched(match, color, x1, y1)):
                    continue
                else:
                    count += 1
    return count


def controles_file(match, piece, color, srcx, srcy, dstx, dsty):
    cnt = 0

    move_dir = rk_dir(srcx, srcy, dstx, dsty)

    move_opp_dir = rules.REVERSE_DIRS[move_dir]
    
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]

        direction = rk_dir(dstx, dsty, dstx + stepx, dsty + stepy)
        if(direction == move_dir or direction == move_opp_dir):
            continue

        x1 = dstx + stepx
        y1 = dsty + stepy
        while(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == color):
                break
            else:
                cnt += 1
                x1 += stepx
                y1 += stepy

    if(cnt >= 5):
        return True
    else:
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
            if(match.color_of_piece(field) == color):
                return False
            else:
                return True
        elif(field != PIECES['blk']):
            return False

        x += stepx
        y += stepy

    return False

