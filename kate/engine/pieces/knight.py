from kate.engine import rules, calc_helper
from kate.engine.match import *


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


def list_field_touches(match, color, fieldx, fieldy):
    touches = []

    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and piece == PIECES['wKn']) or
                (color == COLORS['black'] and piece == PIECES['bKn']) ):
                touches.append([piece, x1, y1])

    return touches


def does_attack(match, srcx, srcy, dstx, dsty):
    priority = 5

    knight = match.readfield(srcx, srcy)

    if(knight != PIECES['wKn'] and knight != PIECES['bKn']):
        return False, 0

    color = Match.color_of_piece(knight)
    opp_color = Match.oppcolor_of_piece(knight)

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    return True, 2 # priority
                else:
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        priority = min(priority, 2)
                    else:
                        match.writefield(srcx, srcy, PIECES['blk'])
                        touched = rules.is_field_touched(match, opp_color, dstx, dsty)
                        match.writefield(srcx, srcy, knight)
                        if(touched):
                            priority = min(priority, 3)
                        elif(rules.is_field_touched(match, opp_color, x1, y1)):
                            if(calc_helper.PIECES_RANK[piece] >= calc_helper.PIECES_RANK[knight]):
                                priority = min(priority, 2)
                            else:
                                priority = min(priority, 3)
                        else:
                            priority = min(priority, 2)

    if(priority == 5):
        return False, 0
    else:
        return True, priority


def count_attacks(match, srcx, srcy, dstx, dsty):
    count = 0

    knight = match.readfield(srcx, srcy)

    if(knight != PIECES['wKn'] and knight != PIECES['bKn']):
        return count

    color = Match.color_of_piece(knight)
    opp_color = Match.oppcolor_of_piece(knight)

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                count += 1

    return count


def score_attacks(match, srcx, srcy):
    score = 0

    knight = match.readfield(srcx, srcy)

    if(knight != PIECES['wKn'] and knight != PIECES['bKn']):
        return score

    color = Match.color_of_piece(knight)
    opp_color = Match.oppcolor_of_piece(knight)

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                score += calc_helper.ATTACKED_SCORES[piece]

    return score


def does_support_attacked(match, srcx, srcy, dstx, dsty):
    priority = 5

    knight = match.readfield(srcx, srcy)

    if(knight != PIECES['wKn'] and knight != PIECES['bKn']):
        return False, 0

    color = Match.color_of_piece(knight)
    opp_color = Match.oppcolor_of_piece(knight)

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        return True, 2 # priority
                    else:
                        if(macalc_helpertch.PIECES_RANK[piece] >= calc_helper.PIECES_RANK[knight]):
                            return True, 2 # priority
                        else:
                            priority = min(priority, 3)

    if(priority == 5):
        return False, 0
    else:
        return True, priority



def score_supports_of_attacked(match, srcx, srcy):
    score = 0

    knight = match.readfield(srcx, srcy)

    if(knight != PIECES['wKn'] and knight != PIECES['bKn']):
        return score

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
                    score += calc_helper.SUPPORTED_SCORES[piece]

    return score 


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
