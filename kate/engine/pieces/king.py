from .. match import *
from .. import rules
from .. cvalues import *
from .generic_piece import contacts_to_token


STEP_1N_X = 0
STEP_1N_Y = 1
STEP_1N1E_X = 1
STEP_1N1E_Y = 1
STEP_1E_X = 1
STEP_1E_Y = 0
STEP_1S1E_X = 1
STEP_1S1E_Y = -1
STEP_1S_X = 0
STEP_1S_Y = -1
STEP_1S1W_X = -1
STEP_1S1W_Y = -1
STEP_1W_X = -1
STEP_1W_Y = 0
STEP_1N1W_X = -1
STEP_1N1W_Y = 1
STEP_SH_CASTLING_X = 2
STEP_SH_CASTLING_Y = 0
STEP_LG_CASTLING_X = -2
STEP_LG_CASTLING_Y = 0

STEPS = [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]

blank = PIECES['blk']
GEN_STEPS = [ [[0, 1, blank]],
              [[1, 1, blank]],
              [[1, 0, blank]], 
              [[1, -1, blank]],
              [[0, -1, blank]], 
              [[-1, -1, blank]],
              [[-1, 0, blank]],
              [[-1, 1, blank]],
              [[2, 0, blank]],
              [[-2, 0, blank]] ]


def is_field_touched(match, color, fieldx, fieldy):
    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and piece == PIECES['wKg']) or
                (color == COLORS['black'] and piece == PIECES['bKg']) ):
                return True
    return False


def field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches):
    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece != PIECES['wKg'] and piece != PIECES['bKg']):
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
            if( (color == COLORS['white'] and piece == PIECES['wKg']) or
                (color == COLORS['black'] and piece == PIECES['bKg']) ):
                touches.append([piece, x1, y1])
                return touches

    return touches


def does_attack(match, srcx, srcy, dstx, dsty):
    priority = PRIO['undefined']

    king = match.readfield(srcx, srcy)

    if(king != PIECES['wKg'] and king != PIECES['bKg']):
        return False, priority

    color = Match.color_of_piece(king) 
    opp_color = Match.oppcolor_of_piece(king)

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == opp_color):
                pin_dir = rules.pin_dir(match, x1, y1)
                if(pin_dir != rules.DIRS['undefined']):
                    return True, PRIO['prio3']
                else:
                    match.writefield(srcx, srcy, PIECES['blk'])
                    enemysupported = rules.is_field_touched(match, opp_color, x1, y1)
                    match.writefield(srcx, srcy, king)
                    if(not enemysupported):
                        priority = min(priority, PRIO['prio3'])
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

    king = match.readfield(srcx, srcy)

    if(king != PIECES['wKg'] and king != PIECES['bKg']):
        return token

    color = Match.color_of_piece(king)
    opp_color = Match.oppcolor_of_piece(king)

    ###
    match.writefield(srcx, srcy, PIECES['blk'])

    frdlycontacts, enmycontacts = rules.field_touches(match, color, dstx, dsty)

    match.writefield(srcx, srcy, king)

    token = token | contacts_to_token(frdlycontacts, enmycontacts, "FIELDTOUCHES")
    ###

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == opp_color):
                token = token | MV_IS_ATTACK

                if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                    token = token | ATTACKED_IS_PAWN
                elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                    token = token | ATTACKED_IS_QUEEN
                else:
                    token = token | ATTACKED_IS_OFFICER

                ###
                match.writefield(srcx, srcy, PIECES['blk'])

                frdlycontacts, enmycontacts = rules.field_touches(match, color, x1, y1)

                match.writefield(srcx, srcy, king)

                token = token | contacts_to_token(frdlycontacts, enmycontacts, "ATTACKTOUCHES")
                ###
            else:
                if(x1 == srcx and y1 == srcy):
                    continue
                piece = match.readfield(x1, y1)

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

                match.writefield(srcx, srcy, king)

                token = token | contacts_to_token(frdlycontacts, enmycontacts, "SUPPORTTOUCHES")
                ###

    return token


def count_attacks(match, srcx, srcy, dstx, dsty):
    count = 0

    king = match.readfield(srcx, srcy)

    if(king != PIECES['wKg'] and king != PIECES['bKg']):
        return count

    color = Match.color_of_piece(king)
    opp_color = Match.oppcolor_of_piece(king)
    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == opp_color):
                count += 1

    return count


def score_attacks(match, srcx, srcy):
    score = 0

    king = match.readfield(srcx, srcy)

    if(king != PIECES['wKg'] and king != PIECES['bKg']):
        return score

    color = Match.color_of_piece(king)
    opp_color = Match.oppcolor_of_piece(king)

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                score += ATTACKED_SCORES[piece]

    return score


def does_support_attacked(match, srcx, srcy, dstx, dsty):
    priority = PRIO['undefined']

    king = match.readfield(srcx, srcy)

    if(king != PIECES['wKg'] and king != PIECES['bKg']):
        return False, priority

    color = Match.color_of_piece(king)
    opp_color = Match.oppcolor_of_piece(king)

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == PIECES['blk']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        return True, PRIO['prio3']
                    else:
                        priority = min(priority, PRIO['prio4'])

    if(priority == PRIO['undefined']):
        return False, priority
    else:
        return True, priority


def score_supports_of_attacked(match, srcx, srcy):
    score = 0

    king = match.readfield(srcx, srcy)

    if(king != PIECES['wKg'] and king != PIECES['bKg']):
        return score

    color = Match.color_of_piece(king)
    opp_color = Match.oppcolor_of_piece(king)

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == PIECES['blk']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    score += SUPPORTED_SCORES[piece]

    return score 


def kg_dir(srcx, srcy, dstx, dsty):
    DIRS = rules.DIRS
    step_x = dstx - srcx
    step_y = dsty - srcy
    if(step_x == STEP_1N_X and step_y == STEP_1N_Y):
        return DIRS['valid']
    elif(step_x == STEP_1N1E_X and step_y == STEP_1N1E_Y):
        return DIRS['valid']
    elif(step_x == STEP_1E_X and step_y == STEP_1E_Y):
        return DIRS['valid']
    elif(step_x == STEP_1S1E_X and step_y == STEP_1S1E_Y):
        return DIRS['valid']
    elif(step_x == STEP_1S_X and step_y == STEP_1S_Y):
        return DIRS['valid']
    elif(step_x == STEP_1S1W_X and step_y == STEP_1S1W_Y):
        return DIRS['valid']
    elif(step_x == STEP_1W_X and step_y == STEP_1W_Y):
        return DIRS['valid']
    elif(step_x == STEP_1N1W_X and step_y == STEP_1N1W_Y):
        return DIRS['valid']
    elif(step_x == STEP_SH_CASTLING_X and step_y == STEP_SH_CASTLING_Y):
        return DIRS['sh-castling']
    elif(step_x == STEP_LG_CASTLING_X and step_y == STEP_LG_CASTLING_Y):
        return DIRS['lg-castling']
    else:
        return DIRS['undefined']


def is_sh_castling_ok(match, srcx, srcy, dstx, dsty, piece):
    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    for i in range(1, 3, 1):
        fieldx = srcx + i
        field = match.readfield(fieldx, srcy)
        if(field != PIECES['blk']):
            return False

    if( rules.is_inbounds(dstx + 1, dsty ) ):
        rook = match.readfield(dstx + 1, dsty)
    else:
        return False

    if(color == COLORS['white']):
        if(match.wKg_first_movecnt != 0 or match.wRk_h1_first_movecnt != 0 or rook != PIECES['wRk']):
            return False
    else:
        if(match.bKg_first_movecnt != 0 or match.bRk_h8_first_movecnt != 0 or rook != PIECES['bRk']):
            return False            

    king = match.readfield(srcx, srcy)
    match.writefield(srcx, srcy, PIECES['blk'])
    for i in range(3):
        castlingx = srcx + i
        attacked = rules.is_field_touched(match, opp_color, castlingx, srcy)
        if(attacked == True):            
            match.writefield(srcx, srcy, king)
            return False

    match.writefield(srcx, srcy, king)
    return True


def is_lg_castling_ok(match, srcx, srcy, dstx, dsty, piece):
    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    for i in range(1, 4, 1):
        fieldx = srcx - i
        field = match.readfield(fieldx, srcy)
        if(field != PIECES['blk']):
            return False

    if( rules.is_inbounds(dstx - 2, dsty) ):
        rook = match.readfield(dstx - 2, dsty)
    else:
        return False

    if(color == COLORS['white']):
        if(match.wKg_first_movecnt != 0 or match.wRk_a1_first_movecnt != 0 or rook != PIECES['wRk']):
            return False
    else:
        if(match.bKg_first_movecnt != 0 or match.bRk_a8_first_movecnt != 0 or rook != PIECES['bRk']):
            return False

    king = match.readfield(srcx, srcy)
    match.writefield(srcx, srcy, PIECES['blk'])
    for i in range(0, -3, -1):
        castlingx = srcx + i
        attacked = rules.is_field_touched(match, opp_color, castlingx, srcy)
        if(attacked == True):
            match.writefield(srcx, srcy, king)
            return False

    match.writefield(srcx, srcy, king)
    return True


def is_move_valid(match, srcx, srcy, dstx, dsty, piece):
    DIRS = rules.DIRS

    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    direction = kg_dir(srcx, srcy, dstx, dsty)
    if(direction == DIRS['sh-castling']):
        return is_sh_castling_ok(match, srcx, srcy, dstx, dsty, piece)
    if(direction == DIRS['lg-castling']):
        return is_lg_castling_ok(match, srcx, srcy, dstx, dsty, piece)
    if(direction == DIRS['undefined']):
        return False

    king = match.readfield(srcx, srcy)
    captured = match.readfield(dstx, dsty)
    match.writefield(srcx, srcy, PIECES['blk'])
    match.writefield(dstx, dsty, king)
    attacked = rules.is_field_touched(match, opp_color, dstx, dsty)
    match.writefield(srcx, srcy, king)
    match.writefield(dstx, dsty, captured)
    if(attacked == True):
        return False

    field = match.readfield(dstx, dsty)
    if(Match.color_of_piece(field) == color):
        return False

    return True

