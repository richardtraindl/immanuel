from kate.models import Match, Move
from kate.modules import rules, generic


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

blank = Match.PIECES['blk']
GEN_WSTEPS = [ [[0, 1, blank]],
               [[0, 2, blank]],
               [[1, 1, blank]], 
               [[-1, 1, blank]] ]

GEN_WPROM_STEPS = [ [[0, 1, Match.PIECES['wQu']], [1, 1, Match.PIECES['wQu']], [-1, 1, Match.PIECES['wQu']], [0, 1, Match.PIECES['wRk']]],
                    [[1, 1, Match.PIECES['wRk']], [-1, 1, Match.PIECES['wRk']], [0, 1, Match.PIECES['wBp']], [1, 1, Match.PIECES['wBp']]],
                    [[-1, 1, Match.PIECES['wBp']], [0, 1, Match.PIECES['wKn']], [1, 1, Match.PIECES['wKn']], [-1, 1, Match.PIECES['wKn']]] ]

GEN_BSTEPS = [ [[0, -1, blank]],
               [[0, -2, blank]],
               [[-1, -1, blank]], 
               [[1, -1, blank]] ]

GEN_BPROM_STEPS = [ [[0, -1, Match.PIECES['bQu']], [0, -1, Match.PIECES['bRk']], [0, -1, Match.PIECES['bBp']], [0, -1, Match.PIECES['bKn']]],
                    [[1, -1, Match.PIECES['bQu']], [1, -1, Match.PIECES['bRk']], [1, -1, Match.PIECES['bBp']], [1, -1, Match.PIECES['bKn']]],
                    [[-1, -1, Match.PIECES['bQu']], [-1, -1, Match.PIECES['bRk']], [-1, -1, Match.PIECES['bBp']], [-1, -1, Match.PIECES['bKn']]] ]


def is_field_touched(match, color, fieldx, fieldy):
    if(color == Match.COLORS['white']):
        STEPS = WPW_BACK_STEPS
    else:
        STEPS = BPW_BACK_STEPS

    for i in range(2):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( (color == Match.COLORS['white'] and piece == Match.PIECES['wPw']) or
                (color == Match.COLORS['black'] and piece == Match.PIECES['bPw']) ):
                return True

    return False


def does_attack(match, srcx, srcy, dstx, dsty):
    priority = 5

    pawn = match.readfield(srcx, srcy)

    if(pawn != Match.PIECES['wPw'] and pawn != Match.PIECES['bPw']):
        return False, 0

    color = Match.color_of_piece(pawn)
    opp_color = Match.REVERSED_COLORS[color]

    if(color == Match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                if(piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                    return True, 1 # priority
                else:
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        return True, 1 # priority
                    else:
                        priority = min(priority, 2)

    if(priority == 5):
        return False, 0
    else:
        return True, priority 


def count_attacks(match, srcx, srcy, dstx, dsty):
    count = 0

    pawn = match.readfield(srcx, srcy)

    if(pawn != Match.PIECES['wPw'] and pawn != Match.PIECES['bPw']):
        return count

    color = Match.color_of_piece(pawn)
    opp_color = Match.REVERSED_COLORS[color]

    if(color == Match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                count += 1

    return count


def score_attacks(match, srcx, srcy):
    score = 0

    pawn = match.readfield(srcx, srcy)

    if(pawn != Match.PIECES['wPw'] and pawn != Match.PIECES['bPw']):
        return score

    color = Match.color_of_piece(pawn)
    opp_color = Match.REVERSED_COLORS[color]

    if(color == Match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                score += Match.ATTACKED_SCORES[piece]

    return score


def does_support_attacked(match, srcx, srcy, dstx, dsty):
    priority = 5

    pawn = match.readfield(srcx, srcy)

    if(pawn != Match.PIECES['wPw'] and pawn != Match.PIECES['bPw']):
        return False, 0

    color = Match.color_of_piece(pawn)
    opp_color = Match.REVERSED_COLORS[color]

    if(color == Match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    pin_dir = rules.pin_dir(match, x1, y1)
                    if(pin_dir != rules.DIRS['undefined']):
                        return True, 1 # priority
                    else:
                        priority = min(priority, 2)
              
    if(priority == 5):
        return False, 0
    else:
        return True, priority


def score_supports_of_attacked(match, srcx, srcy):
    score = 0

    pawn = match.readfield(srcx, srcy)

    if(pawn != Match.PIECES['wPw'] and pawn != Match.PIECES['bPw']):
        return score

    color = Match.color_of_piece(pawn)
    opp_color = Match.REVERSED_COLORS[color]

    if(color == Match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    score += Match.SUPPORTED_SCORES[piece]

    return score


def is_running(match, move):
    piece = match.readfield(move.srcx, move.srcy)
    if(piece == Match.PIECES['wPw']):
        stepx = 0
        stepy = 1
        opp_pawn = Match.PIECES['bPw']
    elif(piece == Match.PIECES['bPw']):
        stepx = 0
        stepy = -1
        opp_pawn = Match.PIECES['wPw']
    else:
        return False

    STARTS = [0, 1, -1]
    for i in range(3):
        x1 = move.dstx + STARTS[i]
        y1 = move.dsty
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
    if(piece == Match.PIECES['wPw']):
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
        move = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(move == None):
            return False
    else:
        move = match.move_list[-1]

    piece = match.readfield(dstx, dsty)
    opp_piece = match.readfield(move.dstx, move.dsty)
    if(piece == Match.PIECES['blk'] and opp_piece == Match.PIECES['bPw'] and 
       srcy == 4 and move.srcx == move.dstx and move.dstx == dstx and 
       move.srcy - 2 == move.dsty):
        return True
    else:
        return False


def is_black_ep_move_ok(match, srcx, srcy, dstx, dsty):
    if(len(match.move_list) == 0):
        move = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(move == None):
            return False
    else:
        move = match.move_list[-1]

    piece = match.readfield(dstx, dsty)
    opp_piece = match.readfield(move.dstx, move.dsty)
    if(piece == Match.PIECES['blk'] and opp_piece == Match.PIECES['wPw'] and 
       srcy == 3 and move.srcx == move.dstx and move.dstx == dstx and 
       move.srcy + 2 == move.dsty):
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

    if(piece == Match.PIECES['wPw']):
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
        if(direction == DIRS['north'] and dstpiece != Match.PIECES['blk']):
            return False
        elif(direction == DIRS['2north']):
            midpiece = match.readfield(dstx, srcy + WHITE_1N_Y)
            if(midpiece != Match.PIECES['blk'] or dstpiece != Match.PIECES['blk']):
                return False
        elif(direction == DIRS['north-west'] or direction == DIRS['north-east']):
            if(Match.color_of_piece(dstpiece) != Match.COLORS['black']):
                return is_white_ep_move_ok(match, srcx, srcy, dstx, dsty)

        # check promotion
        if(dsty == 7 and prom_piece != Match.PIECES['wQu'] and prom_piece != Match.PIECES['wRk'] and prom_piece != Match.PIECES['wBp'] and prom_piece != Match.PIECES['wKn']):
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
        if(direction == DIRS['south'] and dstpiece != Match.PIECES['blk']):
            return False
        elif(direction == DIRS['2south']):
            midpiece = match.readfield(dstx, srcy + BLACK_1S_Y)
            if(midpiece != Match.PIECES['blk'] or dstpiece != Match.PIECES['blk']):
                return False
        elif(direction == DIRS['south-east'] or direction == DIRS['south-west']):
            if(Match.color_of_piece(dstpiece) != Match.COLORS['white']):
                return is_black_ep_move_ok(match, srcx, srcy, dstx, dsty)

        # check promotion
        if(dsty == 0 and prom_piece != Match.PIECES['bQu'] and prom_piece != Match.PIECES['bRk'] and prom_piece != Match.PIECES['bBp'] and prom_piece != Match.PIECES['bKn']):
            return False

    return True


def do_move(match, move, srcpiece, dstpiece):
    if(move.prom_piece != Match.PIECES['blk']):
        move.move_type = Move.TYPES['promotion']
        move.captured_piece = dstpiece

        match.count += 1 
        match.writefield(move.srcx, move.srcy, Match.PIECES['blk'])
        match.writefield(move.dstx, move.dsty, move.prom_piece)
        match.fifty_moves_count = 0
        match.score -= (Match.SCORES[move.prom_piece] - Match.SCORES[srcpiece])
        match.score += Match.SCORES[dstpiece]
        match.move_list.append(move)

        return move
    elif(dstpiece == Match.PIECES['blk'] and move.srcx != move.dstx):
        move.move_type = Move.TYPES['en_passant']
        move.e_p_fieldx = move.dstx
        move.e_p_fieldy = move.srcy
        pawn = match.readfield(move.e_p_fieldx, move.e_p_fieldy)
        move.captured_piece = pawn

        match.count += 1 
        match.writefield(move.srcx, move.srcy, Match.PIECES['blk'])
        match.writefield(move.dstx, move.dsty, srcpiece)
        match.fifty_moves_count = 0
        match.writefield(move.e_p_fieldx, move.e_p_fieldy, Match.PIECES['blk'])
        match.score += Match.SCORES[pawn]
        match.move_list.append(move)

        return move
    else:
        return generic.do_move(match, move, srcpiece, dstpiece)


def undo_promotion(match, move):
    if(move.dsty == 7):
        piece = Match.PIECES['wPw']
    else:
        piece = Match.PIECES['bPw']

    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, move.captured_piece)
    match.score += (Match.SCORES[move.prom_piece] - Match.SCORES[piece])
    match.score -= Match.SCORES[move.captured_piece]

    return move


def undo_en_passant(match, move):
    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count
    piece = match.readfield(move.dstx, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, Match.PIECES['blk'])
    match.writefield(move.e_p_fieldx, move.e_p_fieldy, move.captured_piece)
    match.score -= Match.SCORES[move.captured_piece]

    return move
