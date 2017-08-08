from .. match import *
from .. import rules
from .. cvalues import *


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


def field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches):
    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece != PIECES['wKn'] and piece != PIECES['bKn']):
                continue
            pin_dir = rules.pin_dir(match, x1, y1)
            if(pin_dir != rules.DIRS['undefined']):
                continue
            if(Match.color_of_piece(piece) == color):
                frdlytouches.append(piece)
            else:
                enmytouches.append(piece)


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
    priority = PRIO['undefined']

    knight = match.readfield(srcx, srcy)

    if(knight != PIECES['wKn'] and knight != PIECES['bKn']):
        return False, priority

    color = Match.color_of_piece(knight)
    opp_color = Match.oppcolor_of_piece(knight)

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
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
                        match.writefield(srcx, srcy, knight)
                        if(not attacked):
                            priority = min(priority, PRIO['prio3'])
                        elif(friendlysupported):
                            if(PIECES_RANK[piece] >= PIECES_RANK[knight]):
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

    knight = match.readfield(srcx, srcy)

    if(knight != PIECES['wKn'] and knight != PIECES['bKn']):
        return token

    color = Match.color_of_piece(knight)
    opp_color = Match.oppcolor_of_piece(knight)

    ###
    match.writefield(srcx, srcy, PIECES['blk'])

    frdlycontacts, enmycontacts = rules.field_touches(match, color, dstx, dsty)

    match.writefield(srcx, srcy, knight)

    pawncnt, officercnt = count_contacts(frdlycontacts)
    if(pawncnt > 0):
        token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN
    if(officercnt > 0):
        token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER

    pawncnt, officercnt = count_contacts(enmycontacts)
    if(pawncnt > 0):
        token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN
    if(officercnt > 0):
        token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER
    ###

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == opp_color):
                token = token | MV_IS_ATTACK

                if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    token = token | ATTACKED_IS_KING
                elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                    token = token | ATTACKED_IS_PAWN
                else:
                    token = token | ATTACKED_IS_OFFICER

                ###
                match.writefield(srcx, srcy, PIECES['blk'])

                frdlycontacts, enmycontacts = rules.field_touches(match, color, x1, y1)

                match.writefield(srcx, srcy, knight)

                pawncnt, officercnt = count_contacts(frdlycontacts)
                if(pawncnt > 0):
                    token = token | ATTACKED_IS_ADD_ATT_FROM_PAWN
                if(officercnt > 0):
                    token = token | ATTACKED_IS_ADD_ATT_FROM_OFFICER

                pawncnt, officercnt = count_contacts(enmycontacts)
                if(pawncnt > 0):
                    token = token | ATTACKED_IS_SUPP_BY_PAWN
                if(officercnt > 0):
                    token = token | ATTACKED_IS_SUPP_BY_OFFICER
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
                else:
                    token = token | SUPPORTED_IS_OFFICER

                ###
                match.writefield(srcx, srcy, PIECES['blk'])

                frdlycontacts, enmycontacts = rules.field_touches(match, color, x1, y1)

                match.writefield(srcx, srcy, knight)

                pawncnt, officercnt = count_contacts(frdlycontacts)
                if(pawncnt > 0):
                    token = token | SUPPORTED_IS_ADD_SUPP_BY_PAWN
                if(officercnt > 0):
                    token = token | SUPPORTED_IS_ADD_SUPP_BY_OFFICER

                pawncnt, officercnt = count_contacts(enmycontacts)
                if(pawncnt > 0):
                    token = token | SUPPORTED_IS_ATT_FROM_PAWN
                if(officercnt > 0):
                    token = token | SUPPORTED_IS_ATT_FROM_OFFICER
                ###

    return token


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
                pin_dir = rules.pin_dir(match, srcx, srcy)
                if(pin_dir == rules.DIRS['undefined']):
                    score += ATTACKED_SCORES[piece]

    return score


def does_support_attacked(match, srcx, srcy, dstx, dsty):
    priority = PRIO['undefined']

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
                        return True, PRIO['prio3']
                    else:
                        return True, PRIO['prio4']

    if(priority == PRIO['undefined']):
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
                    score += SUPPORTED_SCORES[piece]

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
