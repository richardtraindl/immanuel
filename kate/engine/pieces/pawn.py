from .. match import *
from .. import rules
from .. cvalues import *
from .generic_piece import cTouch


WHITE_1N_X = 0
WHITE_1N_Y = 1
WHITE_2N_X = 0
WHITE_2N_Y = 2
WHITE_1N1E_X = 1
WHITE_1N1E_Y = 1
WHITE_1N1W_X = -1
WHITE_1N1W_Y = 1

BLACK_1S_X = 0
BLACK_1S_Y = -1
BLACK_2S_X = 0
BLACK_2S_Y = -2
BLACK_1S1E_X = 1
BLACK_1S1E_Y = -1
BLACK_1S1W_X = -1
BLACK_1S1W_Y = -1

WPW_BACK_STEPS = [ [1, -1], [-1, -1] ]
BPW_BACK_STEPS = [ [1, 1], [-1, 1] ]
WPW_STEPS = [ [1, 1], [-1, 1] ]
BPW_STEPS = [ [1, -1], [-1, -1] ]

blank = PIECES['blk']
GEN_WSTEPS = [ [[0, 1, blank]],
               [[0, 2, blank]],
               [[1, 1, blank]], 
               [[-1, 1, blank]] ]

GEN_WPROM_STEPS = [ [[0, 1, PIECES['wQu']], [1, 1, PIECES['wQu']], [-1, 1, PIECES['wQu']], [0, 1, PIECES['wRk']]],
                    [[1, 1, PIECES['wRk']], [-1, 1, PIECES['wRk']], [0, 1, PIECES['wBp']], [1, 1, PIECES['wBp']]],
                    [[-1, 1, PIECES['wBp']], [0, 1, PIECES['wKn']], [1, 1, PIECES['wKn']], [-1, 1, PIECES['wKn']]] ]

GEN_BSTEPS = [ [[0, -1, blank]],
               [[0, -2, blank]],
               [[-1, -1, blank]], 
               [[1, -1, blank]] ]

GEN_BPROM_STEPS = [ [[0, -1, PIECES['bQu']], [0, -1, PIECES['bRk']], [0, -1, PIECES['bBp']], [0, -1, PIECES['bKn']]],
                    [[1, -1, PIECES['bQu']], [1, -1, PIECES['bRk']], [1, -1, PIECES['bBp']], [1, -1, PIECES['bKn']]],
                    [[-1, -1, PIECES['bQu']], [-1, -1, PIECES['bRk']], [-1, -1, PIECES['bBp']], [-1, -1, PIECES['bKn']]] ]


def is_field_touched(match, color, fieldx, fieldy):
    if(color == COLORS['white']):
        STEPS = WPW_BACK_STEPS
    else:
        STEPS = BPW_BACK_STEPS

    for i in range(2):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( (color == COLORS['white'] and piece == PIECES['wPw']) or
                (color == COLORS['black'] and piece == PIECES['bPw']) ):
                return True

    return False


def field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches):
    PW_BACK_STEPS = [ [1, -1], [-1, -1], [1, 1], [-1, 1] ]
    
    for i in range(4):
        x1 = fieldx + PW_BACK_STEPS[i][0]
        y1 = fieldy + PW_BACK_STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                pin_dir = rules.pin_dir(match, x1, y1)
                direction = pw_dir(x1, y1, fieldx, fieldy, piece)
                if(direction == rules.DIRS['undefined']):
                    continue
                if(pin_dir == direction or pin_dir == rules.REVERSE_DIRS[direction] or 
                   pin_dir == rules.DIRS['undefined']):
                    if(Match.color_of_piece(piece) == color):
                        frdlytouches.append(piece)
                    else:
                        enmytouches.append(piece)


def field_color_touches_beyond(match, color, ctouch):
    PW_BACK_STEPS = [ [1, -1], [-1, -1], [1, 1], [-1, 1] ]
    
    for i in range(4):
        x1 = ctouch.fieldx + PW_BACK_STEPS[i][0]
        y1 = ctouch.fieldy + PW_BACK_STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                pin_dir = rules.pin_dir(match, x1, y1)
                direction = pw_dir(x1, y1, ctouch.fieldx, ctouch.fieldy, piece)
                if(direction == rules.DIRS['undefined']):
                    continue
                if(pin_dir == direction or pin_dir == rules.REVERSE_DIRS[direction] or 
                   pin_dir == rules.DIRS['undefined']):
                    if(Match.color_of_piece(piece) == color):
                        ctouch.supporter_beyond.append([piece, x1, y1])
                    else:
                        ctouch.attacker_beyond.append([piece, x1, y1])


def list_field_touches(match, color, fieldx, fieldy):
    touches = []

    if(color == COLORS['white']):
        STEPS = WPW_BACK_STEPS
    else:
        STEPS = BPW_BACK_STEPS

    for i in range(2):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)

            pin_dir = rules.pin_dir(match, x1, y1)
            direction = pw_dir(x1, y1, fieldx, fieldy, piece)
            if(direction == rules.DIRS['undefined']):
                continue
            if(pin_dir == direction or pin_dir == rules.REVERSE_DIRS[direction] or 
               pin_dir == rules.DIRS['undefined']):
                if( (color == COLORS['white'] and piece == PIECES['wPw']) or
                    (color == COLORS['black'] and piece == PIECES['bPw']) ):
                    touches.append([piece, x1, y1])

    return touches
 
 
def attacks_and_supports(match, srcx, srcy, dstx, dsty, attacked, supported):
    token = 0x0

    pawn = match.readfield(srcx, srcy)

    if(pawn != PIECES['wPw'] and pawn != PIECES['bPw']):
        return token

    color = Match.color_of_piece(pawn)
    opp_color = Match.oppcolor_of_piece(pawn)

    if(color == COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue

            piece = match.readfield(x1, y1)

            if(match.color_of_piece(piece) == opp_color):
                ctouch = cTouch(piece, x1, y1)
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

                rules.field_touches_beyond(match, color, ctouch)

                match.writefield(srcx, srcy, pawn)
                ###
            else:
                if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    continue

                ctouch = cTouch(piece, x1, y1)
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

                rules.field_touches_beyond(match, color, ctouch)

                match.writefield(srcx, srcy, pawn)
                ###

    return token 


def score_attacks(match, srcx, srcy):
    score = 0

    pawn = match.readfield(srcx, srcy)

    if(pawn != PIECES['wPw'] and pawn != PIECES['bPw']):
        return score

    color = Match.color_of_piece(pawn)
    opp_color = Match.oppcolor_of_piece(pawn)

    if(color == COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == opp_color):
                pin_dir = rules.pin_dir(match, srcx, srcy)
                direction = pw_dir(srcx, srcy, x1, y1, piece)
                if(pin_dir == direction or pin_dir == rules.DIRS['undefined']):
                    score += ATTACKED_SCORES[piece]

    return score


def score_supports_of_attacked(match, srcx, srcy):
    score = 0

    pawn = match.readfield(srcx, srcy)

    if(pawn != PIECES['wPw'] and pawn != PIECES['bPw']):
        return score

    color = Match.color_of_piece(pawn)
    opp_color = Match.oppcolor_of_piece(pawn)

    if(color == COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == PIECES['blk'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    score += SUPPORTED_SCORES[piece]

    return score


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty):
    color = Match.color_of_piece(piece)

    if(color == COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(rules.is_fork_field(match, piece, srcx, srcy, x1, y1)):
                return True

    return False


def count_attacks(match, color, fieldx, fieldy):
    count = 0

    if(color == COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == color):
                if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                    count += 1
                elif(rules.is_field_touched(match, color, x1, y1)):
                    continue
                else:
                    count += 1
    return count


def is_running(match, srcx, srcy):
    piece = match.readfield(srcx, srcy)
    if(piece == PIECES['wPw']):
        stepx = 0
        stepy = 1
        opp_pawn = PIECES['bPw']
    elif(piece == PIECES['bPw']):
        stepx = 0
        stepy = -1
        opp_pawn = PIECES['wPw']
    else:
        return False

    STARTS = [0, 1, -1]
    for i in range(3):
        x1 = srcx + STARTS[i]
        y1 = srcy
        while( x1 != rules.UNDEF_X and rules.is_inbounds(x1, y1) ):
            x1, y1 = rules.search(match, x1, y1, stepx , stepy)
            if(x1 != rules.UNDEF_X):
                piece = match.readfield(x1, y1)
                if(piece == opp_pawn):
                    return False

    return True



def pw_dir(srcx, srcy, dstx, dsty, piece):
    DIRS = rules.DIRS
    step_x = dstx - srcx
    step_y = dsty - srcy
    if(piece == PIECES['wPw']):
        if(step_x == WHITE_1N_X and step_y == WHITE_1N_Y):
            return DIRS['north']
        elif(step_x == WHITE_2N_X and step_y == WHITE_2N_Y and srcy == 1):
            return DIRS['2north']
        elif(step_x == WHITE_1N1E_X and step_y == WHITE_1N1E_Y):
            return DIRS['north-east']
        elif(step_x == WHITE_1N1W_X and step_y == WHITE_1N1W_Y):
            return DIRS['north-west']
        else:
            return DIRS['undefined']
    else:
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == BLACK_1S_X and step_y == BLACK_1S_Y):
            return DIRS['south']
        elif(step_x == BLACK_2S_X and step_y == BLACK_2S_Y and srcy == 6):
            return DIRS['2south']
        elif(step_x == BLACK_1S1E_X and step_y == BLACK_1S1E_Y):
            return DIRS['south-east']
        elif(step_x == BLACK_1S1W_X and step_y == BLACK_1S1W_Y):
            return DIRS['south-west']
        else:
            return DIRS['undefined']


def is_white_ep_move_ok(match, srcx, srcy, dstx, dsty):
    if(len(match.move_list) == 0):
        return False
    else:
        move = match.move_list[-1]

    piece = match.readfield(dstx, dsty)
    opp_piece = match.readfield(move.dstx, move.dsty)
    if(piece == PIECES['blk'] and opp_piece == PIECES['bPw'] and 
       move.srcy - move.dsty == 2 and move.dsty == srcy and move.dstx == dstx and 
       move.dsty - dsty == -1):
        return True
    else:
        return False


def is_black_ep_move_ok(match, srcx, srcy, dstx, dsty):
    if(len(match.move_list) == 0):
        return False
    else:
        move = match.move_list[-1]

    piece = match.readfield(dstx, dsty)
    opp_piece = match.readfield(move.dstx, move.dsty)
    if(piece == PIECES['blk'] and opp_piece == PIECES['wPw'] and 
       move.srcy - move.dsty == -2 and move.dsty == srcy and move.dstx == dstx and 
       move.dsty - dsty == 1):
        return True
    else:
        return False


def is_move_valid(match, srcx, srcy, dstx, dsty, piece, prom_piece):
    DIRS = rules.DIRS
    direction = pw_dir(srcx, srcy, dstx, dsty, piece)
    if(direction == DIRS['undefined']):
        return False

    pin_dir = rules.pin_dir(match, srcx, srcy)

    dstpiece = match.readfield(dstx, dsty)

    if(piece == PIECES['wPw']):
        # check pins
        if(direction == DIRS['north'] or direction == DIRS['2north']):
            if(pin_dir != DIRS['north'] and pin_dir != DIRS['south'] and pin_dir != DIRS['undefined']):
                return False
        elif(direction == DIRS['north-west']):
            if(pin_dir != DIRS['north-west'] and pin_dir != DIRS['south-east'] and pin_dir != DIRS['undefined']):
                return False
        elif(direction == DIRS['north-east']):
            if(pin_dir != DIRS['north-east'] and pin_dir != DIRS['south-west'] and pin_dir != DIRS['undefined']):
                return False

        # check fields
        if(direction == DIRS['north'] and dstpiece != PIECES['blk']):
            return False
        elif(direction == DIRS['2north']):
            midpiece = match.readfield(dstx, srcy + WHITE_1N_Y)
            if(midpiece != PIECES['blk'] or dstpiece != PIECES['blk']):
                return False
        elif(direction == DIRS['north-west'] or direction == DIRS['north-east']):
            if(Match.color_of_piece(dstpiece) != COLORS['black']):
                return is_white_ep_move_ok(match, srcx, srcy, dstx, dsty)

        # check promotion
        if(dsty == 7 and prom_piece != PIECES['wQu'] and prom_piece != PIECES['wRk'] and prom_piece != PIECES['wBp'] and prom_piece != PIECES['wKn']):
            return False
    else:
        # check pins
        if(direction == DIRS['south'] or direction == DIRS['2south']):
            if(pin_dir != DIRS['north'] and pin_dir != DIRS['south'] and pin_dir != DIRS['undefined']):
                return False
        elif(direction == DIRS['south-east']):
            if(pin_dir != DIRS['north-west'] and pin_dir != DIRS['south-east'] and pin_dir != DIRS['undefined']):
                return False
        elif(direction == DIRS['south-west']):
            if(pin_dir != DIRS['north-east'] and pin_dir != DIRS['south-west'] and pin_dir != DIRS['undefined']):
                return False
        
        # check fields
        if(direction == DIRS['south'] and dstpiece != PIECES['blk']):
            return False
        elif(direction == DIRS['2south']):
            midpiece = match.readfield(dstx, srcy + BLACK_1S_Y)
            if(midpiece != PIECES['blk'] or dstpiece != PIECES['blk']):
                return False
        elif(direction == DIRS['south-east'] or direction == DIRS['south-west']):
            if(Match.color_of_piece(dstpiece) != COLORS['white']):
                return is_black_ep_move_ok(match, srcx, srcy, dstx, dsty)

        # check promotion
        if(dsty == 0 and prom_piece != PIECES['bQu'] and prom_piece != PIECES['bRk'] and prom_piece != PIECES['bBp'] and prom_piece != PIECES['bKn']):
            return False

    return True

  
