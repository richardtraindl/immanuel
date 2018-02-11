from .. match import *
from .. cvalues import *
from .. import rules
from .. import analyze_helper
from .generic_piece import cTouch


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
            if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
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
            if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                if(Match.color_of_piece(piece) == color):
                    ctouch.supporter_beyond.append([piece, x1, y1])
                else:
                    ctouch.attacker_beyond.append([piece, x1, y1])

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


def attacks_and_supports(match, srcx, srcy, dstx, dsty, attacked, supported):
    token = 0x0

    king = match.readfield(srcx, srcy)

    color = Match.color_of_piece(king)
    opp_color = Match.oppcolor_of_piece(king)

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

                ###
                match.writefield(srcx, srcy, PIECES['blk'])

                analyze_helper.field_touches_beyond(match, opp_color, ctouch)

                match.writefield(srcx, srcy, king)
                ###
            else:
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

                match.writefield(srcx, srcy, king)
                ###

    return token 


def score_attacks(match, srcx, srcy):
    score = 0

    king = match.readfield(srcx, srcy)

    color = Match.color_of_piece(king)
    opp_color = Match.oppcolor_of_piece(king)

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

    return score


def score_supports(match, srcx, srcy):
    score = 0

    king = match.readfield(srcx, srcy)

    color = Match.color_of_piece(king)
    opp_color = Match.oppcolor_of_piece(king)

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue

            piece = match.readfield(x1, y1)

            if(Match.color_of_piece(piece) == color):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    score += SUPPORTED_SCORES[piece]

    return score 


def count_touches(match, color, fieldx, fieldy):
    count = 0

    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(piece == PIECES['blk']):
                continue
            elif(match.color_of_piece(piece) == color):
                count += 1
            else:
                count -= 1

    return count


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked):
    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(analyze_helper.is_fork_field(match, piece, srcx, srcy, x1, y1)):
                forked.append([srcx, srcy, dstx, dsty,  x1, y1])
                return True

    return False


def is_king_safe(match, color):
    if(color == COLORS['white']):
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
    else:
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y

    for i in range(8):
        x1 = Kg_x + STEPS[i][0]
        y1 = Kg_y + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            friends, enemies = field_touches(match, color, x1, y1)
            if(len(friends) < len(enemies)):
                return False

    friends.clear()
    enemies.clear()
    friends, enemies = field_touches(match, color, Kg_x, Kg_y)
    if(len(enemies) >= 2):
        return False

    for enemy in enemies:
        friends_beyond, enemies_beyond = field_touches(match, color, enemy[1], enemy[2])
        if(len(friends_beyond) >= len(enemies_beyond)):
            continue

        direction = rook.rk_dir(Kg_x, Kg_y, enemy[1], enemy[2])
        if(direction != DIRS['undefined']):
            direction, step_x, step_y = rook.rk_step(direction, None, None, None, None)
        else:
            direction = bishop.bp_dir(Kg_x, Kg_y, enemy[1], enemy[2])
            if(direction != DIRS['undefined']):
                direction, step_x, step_y = bishop.bp_step(direction, None, None, None, None)
            else:
                return False

        x1 = Kg_x + step_x
        y1 = Kg_y + step_y
        while(rules.is_inbounds(x1, y1)):
            blocking_friends, blocking_enemies = field_touches(match, color, x1, y1)
            if(len(blocking_friends) > 0):
                break

    return True


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

