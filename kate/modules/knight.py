from kate.models import Match
from kate.modules import rules


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

blank = Match.PIECES['blk']
GEN_STEPS = [ [[1, 2, blank]],
              [[2, 1, blank]],
              [[2, -1, blank]], 
              [[1, -2, blank]],
              [[-1, -2, blank]],
              [[-2, -1, blank]],
              [[-2, 1, blank]],
              [[-1, 2, blank]] ]


def is_field_attacked(match, color, fieldx, fieldy):
    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( (color == Match.COLORS['white'] and piece == Match.PIECES['wKn']) or
                (color == Match.COLORS['black'] and piece == Match.PIECES['bKn']) ):
                return True

    return False


def does_attack(match, srcx, srcy, dstx, dsty):
    knight = match.readfield(srcx, srcy)

    if(knight != Match.PIECES['wKn'] and knight != Match.PIECES['bKn']):
        return False, 0

    color = Match.color_of_piece(knight)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                if(piece == Match.PIECES['wPw'] or piece == Match.PIECES['bPw']):
                    return True, 0 # priority
                elif(piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                    return True, 2 # priority
                else:
                    return True, 1 # priority

    return False, 0


def count_attacks(match, srcx, srcy):
    count = 0
    knight = match.readfield(srcx, srcy)

    if(knight != Match.PIECES['wKn'] and knight != Match.PIECES['bKn']):
        return count

    color = Match.color_of_piece(knight)
    opp_color = Match.REVERSED_COLORS[color]

    if(color == Match.COLORS['white']):
        counter = 1
    else:
        counter = -1

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                count += counter

    return count


def score_attacks(match, srcx, srcy):
    score = 0

    knight = match.readfield(srcx, srcy)

    if(knight != Match.PIECES['wKn'] and knight != Match.PIECES['bKn']):
        return score

    color = Match.color_of_piece(knight)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                score += Match.ATTACKED_SCORES[piece]
                if(Match.SCORES[knight] <= Match.REVERSED_SCORES[piece]):
                    score += (Match.ATTACKED_SCORES[piece] // 2)

    return score


def does_support_attacked(match, srcx, srcy, dstx, dsty):
    knight = match.readfield(srcx, srcy)

    if(knight != Match.PIECES['wKn'] and knight != Match.PIECES['bKn']):
        return False, 0

    color = Match.color_of_piece(knight)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_attacked(match, opp_color, x1, y1)):
                    if(piece == Match.PIECES['wPw'] or piece == Match.PIECES['bPw']):
                        return True, 0 # priority
                    else:
                        return True, 1 # priority

    return False, 0



def score_supports_of_attacked(match, srcx, srcy):
    score = 0

    knight = match.readfield(srcx, srcy)

    if(knight != Match.PIECES['wKn'] and knight != Match.PIECES['bKn']):
        return score

    color = Match.color_of_piece(knight)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx , stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_attacked(match, opp_color, x1, y1)):
                    score += Match.SUPPORTED_SCORES[piece]

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
    if(match.color_of_piece(field) == color):
        return False

    return True
