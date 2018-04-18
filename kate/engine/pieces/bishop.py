from .. match import *
from .. cvalues import *
from .. import rules
from .. import analyze_helper
from .generic_piece import cTouch, cTouchBeyond, cFork


NEAST_X = 1
NEAST_Y = 1
SWEST_X = -1
SWEST_Y = -1
NWEST_X = -1
NWEST_Y = 1
SEAST_X = 1
SEAST_Y = -1

STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]

NE_SW_STEPS = [ [1, 1], [-1, -1] ]

NW_SE_STEPS = [ [-1, 1], [1, -1] ]

blank = PIECES['blk']
GEN_STEPS = [ [[1, 1, blank], [2, 2, blank], [3, 3, blank], [4, 4, blank], [5, 5, blank], [6, 6, blank], [7, 7, blank]],
              [[-1, -1, blank], [-2, -2, blank], [-3, -3, blank], [-4, -4, blank], [-5, -5, blank], [-6, -6, blank], [-7, -7, blank]],
              [[1, -1, blank], [2, -2, blank], [3, -3, blank], [4, -4, blank], [5, -5, blank], [6, -6, blank], [7, -7, blank]],
              [[-1, 1, blank], [-2, 2, blank], [-3, 3, blank], [-4, 4, blank], [-5, 5, blank], [-6, 6, blank], [-7, 7, blank]] ]


def is_field_touched(match, color, fieldx, fieldy, mode):
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and piece == PIECES['wBp']) or
                (color == COLORS['black'] and piece == PIECES['bBp']) ):
                if(mode == 0):
                    return True
                elif(mode == 1):
                    if(is_move_stuck(match, fieldx, fieldy, x1, y1)):
                        continue
                    else:
                        return True
                else: #mode == 2
                    if(is_move_stuck(match, fieldx, fieldy, x1, y1) or analyze_helper.is_soft_pin(match, x1, y1)):
                        continue
                    else:
                        return True

    return False


def is_piece_stuck(match, srcx, srcy):
    return False


def is_move_stuck(match, srcx, srcy, dstx, dsty):
    move_dir = bp_dir(srcx, srcy, dstx, dsty)
    pin_dir = rules.pin_dir(match, None, srcx, srcy)
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
            if(piece == PIECES['wQu'] or piece == PIECES['bQu'] or piece == PIECES['wBp'] or piece == PIECES['bBp']):
                if(is_move_stuck(match, x1, y1, fieldx, fieldy)):
                    continue

                if(Match.color_of_piece(piece) == color):
                    frdlytouches.append(cTouch(piece, x1, y1))
                else:
                    enmytouches.append(cTouch(piece, x1, y1))


def field_color_touches_beyond(match, color, ctouch_beyond):
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, ctouch_beyond.fieldx, ctouch_beyond.fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            piece = match.readfield(x1, y1)
            if(piece == PIECES['wQu'] or piece == PIECES['bQu'] or piece == PIECES['wBp'] or piece == PIECES['bBp']):
                if(is_move_stuck(match, x1, y1, ctouch_beyond.fieldx, ctouch_beyond.fieldy)):
                    continue

                if(Match.color_of_piece(piece) == color):
                    ctouch_beyond.supporter_beyond.append(cTouch(piece, x1, y1))
                else:
                    ctouch_beyond.attacker_beyond.append(cTouch(piece, x1, y1))


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
            if( (color == COLORS['white'] and (piece == PIECES['wQu'] or piece == PIECES['wBp'])) or
                (color == COLORS['black'] and (piece == PIECES['bQu'] or piece == PIECES['bBp'])) ):
                touches.append(cTouch(piece, x1, y1))

    return touches

  
def attacks_and_supports(match, srcx, srcy, dstx, dsty, attacked, supported):
    token = 0x0

    bishop = match.readfield(srcx, srcy)

    color = Match.color_of_piece(bishop)
    opp_color = Match.oppcolor_of_piece(bishop)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, dstx, dsty, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue
            
            if(is_move_stuck(match, dstx, dsty, x1, y1)):
                continue

            piece = match.readfield(x1, y1)
            
            if(Match.color_of_piece(piece) == opp_color):
                ctouch_beyond = cTouchBeyond(srcx, srcy, dstx, dsty, piece, x1, y1)
                attacked.append(ctouch_beyond)

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

                # attacked piece behind
                x2, y2 = rules.search(match, x1, y1, stepx, stepy)
                if(x2 != rules.UNDEF_X):
                    piece_behind = match.readfield(x2, y2)
                    if(Match.color_of_piece(piece_behind) == opp_color):
                        if(PIECES_RANK[piece_behind] > PIECES_RANK[bishop]):
                            if(piece_behind == PIECES['wKg'] or piece_behind == PIECES['bKg']):
                                token = token | ATTACK_IS_PIN
                            else:
                                token = token | ATTACK_IS_SOFT_PIN

                ###
                match.writefield(srcx, srcy, PIECES['blk'])

                analyze_helper.field_touches_beyond(match, opp_color, ctouch_beyond)

                match.writefield(srcx, srcy, bishop)
                ###

            else:
                if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    continue

                ctouch_beyond = cTouchBeyond(srcx, srcy, dstx, dsty, piece, x1, y1)
                supported.append(ctouch_beyond)

                if(rules.is_field_touched(match, opp_color, x1, y1, 0)):
                    token = token | MV_IS_SUPPORT
                else:
                    token = token | MV_IS_SUPPORT_UNATTACKED

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

                analyze_helper.field_touches_beyond(match, color, ctouch_beyond)

                match.writefield(srcx, srcy, bishop)
                ###

    return token 


def disclosures_field(match, color, excluded_dir, srcx, srcy, disclosed_attacked):
    for j in range(0, 4, 2):
        first = cTouchBeyond(None, None, None, None, PIECES['blk'], 0, 0)
        second = cTouchBeyond(None, None, None, None, PIECES['blk'], 0, 0)

        for i in range(0, 2, 1):
            stepx = STEPS[j+i][0]
            stepy = STEPS[j+i][1]
            if(excluded_dir == bp_dir(srcx, srcy, (srcx + stepx), (srcy + stepy))):
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
                            if(first.piece == PIECES['wBp'] or first.piece == PIECES['bBp'] or 
                               first.piece == PIECES['wQu'] or first.piece == PIECES['bQu']):
                                disclosed_attacked.append(second)
                                return True
                        else:
                            if(second.piece == PIECES['wBp'] or second.piece == PIECES['bBp'] or 
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

    bishop = match.readfield(srcx, srcy)

    color = Match.color_of_piece(bishop)
    opp_color = Match.oppcolor_of_piece(bishop)

    frdlytouches, enmytouches = analyze_helper.field_touches(match, color, srcx, srcy)
    if(len(frdlytouches) < len(enmytouches)):
        return score

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(is_move_stuck(match, srcx, srcy, x1, y1)):
                continue

            frdlytouches, enmytouches = analyze_helper.field_touches(match, color, x1, y1)
            #if(len(frdlytouches) < len(enmytouches)):
                #continue

            piece = match.readfield(x1, y1)

            if(match.color_of_piece(piece) == opp_color):
                if(len(enmytouches) == 0 or PIECES_RANK[bishop] <= PIECES_RANK[piece]):
                    score += ATTACKED_SCORES[piece]

                # score if attacked is pinned
                direction = bp_dir(srcx, srcy, x1, y1)
                enmy_pin = rules.pin_dir(match, opp_color, x1, y1)
                if(enmy_pin != rules.DIRS['undefined']):
                    if(enmy_pin != direction and enmy_pin != rules.REVERSE_DIRS[direction]):
                        score += ATTACKED_SCORES[piece]
                    else:
                        if(piece != PIECES['wBp'] and piece != PIECES['bBp'] and
                           piece != PIECES['wPw'] and piece != PIECES['bPw']):
                            score += ATTACKED_SCORES[piece]

                if(analyze_helper.is_soft_pin(match, x1, y1)):
                    score += ATTACKED_SCORES[piece]

    return score


def score_supports(match, srcx, srcy):
    score = 0

    bishop = match.readfield(srcx, srcy)

    color = Match.color_of_piece(bishop)
    opp_color = Match.oppcolor_of_piece(bishop)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, srcx, srcy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue

            if(is_move_stuck(match, srcx, srcy, x1, y1, 1)):
                continue

            piece = match.readfield(x1, y1)

            if(Match.color_of_piece(piece) == color):
                if(rules.is_field_touched(match, opp_color, x1, y1, 1)):
                    score += SUPPORTED_SCORES[piece]

    return score 


def count_touches(match, color, fieldx, fieldy):
    count = 0

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = rules.search(match, fieldx, fieldy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            if(is_move_stuck(match, fieldx, fieldy, x1, y1)):
                continue

            piece = match.readfield(x1, y1)
            if(piece == PIECES['blk']):
                continue
            elif(match.color_of_piece(piece) == color):
                if(rules.is_field_touched(match, color, x1, y1, 1) == False):
                    count += 1
                elif(PIECES_RANK[piece] > PIECES_RANK[PIECES['wBp']]):
                    count += 1
            """else:
                count -= 1"""

    return count


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked):
    if(is_move_stuck(match, srcx, srcy, dstx, dsty)):
        return False

    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    direction = bp_dir(srcx, srcy, dstx, dsty)
    if(direction == rules.DIRS['north-east'] or direction == rules.DIRS['south-west']):
        BP_STEPS = NW_SE_STEPS
    else:
        BP_STEPS = NE_SW_STEPS

    for i in range(2):
        stepx = BP_STEPS[i][0]
        stepy = BP_STEPS[i][1]

        x1 = dstx + stepx
        y1 = dsty + stepy
        while(rules.is_inbounds(x1, y1)):
            fork_field = match.readfield(x1, y1)

            if(Match.color_of_piece(fork_field) == opp_color):
                break

            if(analyze_helper.is_fork_field(match, piece, x1, y1)):
                cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                forked.append(cfork)
                return True

            if(Match.color_of_piece(fork_field) == color):
                break

            x1 += stepx
            y1 += stepy

    return False


def controles_file(match, piece, color, srcx, srcy, dstx, dsty):
    cnt = 0

    move_dir = bp_dir(srcx, srcy, dstx, dsty)

    move_opp_dir = rules.REVERSE_DIRS[move_dir]
    
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]

        direction = bp_dir(dstx, dsty, dstx + stepx, dsty + stepy)
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

    pin_dir = rules.pin_dir(match, color, srcx, srcy)

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

