from .. match import *
from .. cvalues import *
from .. import rules
from .. import analyze_helper
from .generic_piece import cTouch


STEP_2N1E_X = 1
STEP_2N1E_Y = 2
STEP_1N2E_X = 2
STEP_1N2E_Y = 1
STEP_1S2E_X = 2
STEP_1S2E_Y = -1
STEP_2S1E_X = 1
STEP_2S1E_Y = -2
STEP_2S1W_X = -1
STEP_2S1W_Y = -2
STEP_1S2W_X = -2
STEP_1S2W_Y = -1
STEP_1N2W_X = -2
STEP_1N2W_Y = 1
STEP_2N1W_X = -1
STEP_2N1W_Y = 2

STEPS = [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]

blank = PIECES['blk']
GEN_STEPS = [ [[1, 2, blank]],
              [[2, 1, blank]],
              [[2, -1, blank]], 
              [[1, -2, blank]],
              [[-1, -2, blank]],
              [[-2, -1, blank]],
              [[-2, 1, blank]],
              [[-1, 2, blank]] ]


def is_field_touched(match, color, fieldx, fieldy):
    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and piece == PIECES['wKn']) or
                (color == COLORS['black'] and piece == PIECES['bKn']) ):
                return True

    return False


def is_stuck(match, fieldx, fieldy):
    pin_dir = rules.pin_dir(match, fieldx, fieldy)
    if(pin_dir == rules.DIRS['undefined']):
        return False
    else:
        return True
                    

def field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches):
    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                if(is_stuck(match, x1, y1)):
                    continue

                if(Match.color_of_piece(piece) == color):
                    frdlytouches.append([piece, x1, y1])
                else:
                    enmytouches.append([piece, x1, y1])


def field_color_touches_beyond(match, color, ctouch):
    for i in range(8):
        x1 = ctouch.fieldx + STEPS[i][0]
        y1 = ctouch.fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                if(is_stuck(match, x1, y1)):
                    continue

                if(Match.color_of_piece(piece) == color):
                    ctouch = cTouch(None, None, None, None, piece, x1, y1)
                    ctouch.supporter_beyond.append([piece, x1, y1])
                else:
                    ctouch = cTouch(None, None, None, None, piece, x1, y1)
                    ctouch.attacker_beyond.append([piece, x1, y1])


def list_field_touches(match, color, fieldx, fieldy):
    touches = []

    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(is_stuck(match, x1, y1)):
                continue

            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and piece == PIECES['wKn']) or
                (color == COLORS['black'] and piece == PIECES['bKn']) ):
                touches.append([piece, x1, y1])

    return touches


def attacks_and_supports(match, srcx, srcy, dstx, dsty, attacked, supported):
    token = 0x0

    if(is_stuck(match, srcx, srcy)):
        return token

    knight = match.readfield(srcx, srcy)

    color = Match.color_of_piece(knight)
    opp_color = Match.oppcolor_of_piece(knight)

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue

            piece = match.readfield(x1, y1)

            if(match.color_of_piece(piece) == opp_color):
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

                match.writefield(srcx, srcy, knight)
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

                match.writefield(srcx, srcy, knight)
                ###

    return token 


def score_attacks(match, srcx, srcy):
    score = 0

    if(is_stuck(match, srcx, srcy)):
        return score

    knight = match.readfield(srcx, srcy)

    color = Match.color_of_piece(knight)
    opp_color = Match.oppcolor_of_piece(knight)

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                score += ATTACKED_SCORES[piece]

                # extra score for pinned attacked
                enmy_pin = rules.pin_dir(match, x1, y1)
                if(enmy_pin != rules.DIRS['undefined']):
                    score += ATTACKED_SCORES[piece]
                    
                # extra score if attacked is higher
                if(PIECES_RANK[piece] > PIECES_RANK[knight]):
                    score += ATTACKED_SCORES[piece] + ATTACKED_SCORES[knight]

    return score


def score_supports(match, srcx, srcy):
    score = 0

    if(is_stuck(match, srcx, srcy)):
        return score

    knight = match.readfield(srcx, srcy)

    color = Match.color_of_piece(knight)
    opp_color = Match.oppcolor_of_piece(knight)

    for i in range(8):
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


def count_attacks(match, color, fieldx, fieldy):
    count = 0

    if(is_stuck(match, fieldx, fieldy)):
        return count

    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == color):
                if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    count += 1
                elif(rules.is_field_touched(match, color, x1, y1)):
                    continue
                else:
                    count += 1
    return count


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked):
    if(is_stuck(match, srcx, srcy)):
        return False

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(analyze_helper.is_fork_field(match, piece, srcx, srcy, x1, y1)):
                forked.append([srcx, srcy, dstx, dsty,  x1, y1])
                return True

    return False


def is_capture_possible(match, srcx, srcy):
    if(is_stuck(match, srcx, srcy)):
        return False

    knight = match.readfield(srcx, srcy)

    opp_color = Match.oppcolor_of_piece(knight)

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(rules.is_soft_pin(match, srcx, srcy)):
                continue

            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                if(PIECES_RANK[knight] <= PIECES_RANK[piece]):
                    return True
                else:
                    match.writefield(srcx, srcy, PIECES['blk'])
                    friends, enemies = analyze_helper.field_touches(match, Match.color_of_piece(knight), x1, y1)
                    match.writefield(srcx, srcy, knight)
                    if(len(friends) >= len(enemies)):
                        return True

    return False


def kn_dir(srcx, srcy, dstx, dsty):
    DIRS = rules.DIRS
    step_x = dstx - srcx
    step_y = dsty - srcy
    if(step_x == STEP_2N1E_X and step_y == STEP_2N1E_Y):
        return DIRS['valid']
    elif(step_x == STEP_1N2E_X and step_y == STEP_1N2E_Y):
        return DIRS['valid']
    elif(step_x == STEP_1S2E_X and step_y == STEP_1S2E_Y):
        return DIRS['valid']
    elif(step_x == STEP_2S1E_X and step_y == STEP_2S1E_Y):
        return DIRS['valid']
    elif(step_x == STEP_2S1W_X and step_y == STEP_2S1W_Y):
        return DIRS['valid']
    elif(step_x == STEP_1S2W_X and step_y == STEP_1S2W_Y):
        return DIRS['valid']
    elif(step_x == STEP_1N2W_X and step_y == STEP_1N2W_Y):
        return DIRS['valid']
    elif(step_x == STEP_2N1W_X and step_y == STEP_2N1W_Y):
        return DIRS['valid']
    else:
        return DIRS['undefined']


def is_move_valid(match, srcx, srcy, dstx, dsty, piece):
    DIRS = rules.DIRS
    direction = kn_dir(srcx, srcy, dstx, dsty)
    if(direction == DIRS['undefined']):
        return False

    color = Match.color_of_piece(piece)

    pin_dir = rules.pin_dir(match, srcx, srcy)

    if(pin_dir != DIRS['undefined']):
        return False

    field = match.readfield(dstx, dsty)
    if(Match.color_of_piece(field) == color):
        return False

    return True
