from kate.models import Match, Move
from kate.modules import rules, generic


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

blank = Match.PIECES['blk']
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
            if( (color == Match.COLORS['white'] and piece == Match.PIECES['wKg']) or
                (color == Match.COLORS['black'] and piece == Match.PIECES['bKg']) ):
                return True
    return False


def does_attack(match, srcx, srcy, dstx, dsty):
    priority = 5

    king = match.readfield(srcx, srcy)

    if(king != Match.PIECES['wKg'] and king != Match.PIECES['bKg']):
        return False, 0

    color = Match.color_of_piece(king) 
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                pin_dir = rules.pin_dir(match, x1, y1)
                if(pin_dir != rules.DIRS['undefined']):
                    return True, 1 # priority
                else:
                    if(rules.is_field_touched(match, opp_color, x1, y1)):
                        priority = min(priority, 2)
                    else:
                        return True, 1 # priority

    if(priority == 5):
        return False, 0
    else:
        return True, priority


def count_attacks(match, srcx, srcy, dstx, dsty):
    count = 0

    king = match.readfield(srcx, srcy)

    if(king != Match.PIECES['wKg'] and king != Match.PIECES['bKg']):
        return count

    color = Match.color_of_piece(king)
    opp_color = Match.REVERSED_COLORS[color]

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

    king = match.readfield(srcx, srcy)

    if(king != Match.PIECES['wKg'] and king != Match.PIECES['bKg']):
        return score

    color = Match.color_of_piece(king)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == opp_color):
                score += Match.ATTACKED_SCORES[piece]

    return score


def does_support_attacked(match, srcx, srcy, dstx, dsty):
    priority = 5

    king = match.readfield(srcx, srcy)

    if(king != Match.PIECES['wKg'] and king != Match.PIECES['bKg']):
        return False, 0

    color = Match.color_of_piece(king)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk']):
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

    king = match.readfield(srcx, srcy)

    if(king != Match.PIECES['wKg'] and king != Match.PIECES['bKg']):
        return score

    color = Match.color_of_piece(king)
    opp_color = Match.REVERSED_COLORS[color]

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_touched(match, opp_color, x1, y1)):
                    score += Match.SUPPORTED_SCORES[piece]

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

    opp_color = Match.REVERSED_COLORS[color]

    for i in range(1, 3, 1):
        fieldx = srcx + i
        field = match.readfield(fieldx, srcy)
        if(field != Match.PIECES['blk']):
            return False

    if( rules.is_inbounds(dstx + 1, dsty ) ):
        rook = match.readfield(dstx + 1, dsty)
    else:
        return False

    if(color == Match.COLORS['white']):
        if(match.wKg_first_movecnt != 0 or match.wRk_h1_first_movecnt != 0 or rook != Match.PIECES['wRk']):
            return False
    else:
        if(match.bKg_first_movecnt != 0 or match.bRk_h8_first_movecnt != 0 or rook != Match.PIECES['bRk']):
            return False            

    king = match.readfield(srcx, srcy)
    match.writefield(srcx, srcy, Match.PIECES['blk'])
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

    opp_color = Match.REVERSED_COLORS[color]

    for i in range(1, 4, 1):
        fieldx = srcx - i
        field = match.readfield(fieldx, srcy)
        if(field != Match.PIECES['blk']):
            return False

    if( rules.is_inbounds(dstx - 2, dsty) ):
        rook = match.readfield(dstx - 2, dsty)
    else:
        return False

    if(color == Match.COLORS['white']):
        if(match.wKg_first_movecnt != 0 or match.wRk_a1_first_movecnt != 0 or rook != Match.PIECES['wRk']):
            return False
    else:
        if(match.bKg_first_movecnt != 0 or match.bRk_a8_first_movecnt != 0 or rook != Match.PIECES['bRk']):
            return False

    king = match.readfield(srcx, srcy)
    match.writefield(srcx, srcy, Match.PIECES['blk'])
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

    opp_color = Match.REVERSED_COLORS[color]

    direction = kg_dir(srcx, srcy, dstx, dsty)
    if(direction == DIRS['sh-castling']):
        return is_sh_castling_ok(match, srcx, srcy, dstx, dsty, piece)
    if(direction == DIRS['lg-castling']):
        return is_lg_castling_ok(match, srcx, srcy, dstx, dsty, piece)
    if(direction == DIRS['undefined']):
        return False

    king = match.readfield(srcx, srcy)
    captured = match.readfield(dstx, dsty)
    match.writefield(srcx, srcy, Match.PIECES['blk'])
    match.writefield(dstx, dsty, king)
    attacked = rules.is_field_touched(match, opp_color, dstx, dsty)
    match.writefield(srcx, srcy, king)
    match.writefield(dstx, dsty, captured)
    if(attacked == True):
        return False

    field = match.readfield(dstx, dsty)
    if(match.color_of_piece(field) == color):
        return False

    return True


def do_move(match, move, srcpiece, dstpiece):
    if(move.dstx - move.srcx == 2):
        move.move_type = Move.TYPES['short_castling']
        move.captured_piece = dstpiece

        match.count += 1   
        match.writefield(move.srcx, move.srcy, Match.PIECES['blk'])
        match.writefield(move.dstx, move.dsty, srcpiece)
        rook = match.readfield(move.srcx + 3, move.srcy)
        match.writefield(move.srcx + 3, move.srcy, Match.PIECES['blk'])
        match.writefield(move.dstx - 1, move.dsty, rook)
        match.fifty_moves_count += 1
        if(srcpiece == Match.PIECES['wKg']):
            match.wKg_x = move.dstx
            match.wKg_y = move.dsty
            if(match.wKg_first_movecnt == 0):
                match.wKg_first_movecnt = match.count
        else:
            match.bKg_x = move.dstx
            match.bKg_y = move.dsty
            if(match.bKg_first_movecnt == 0):
                match.bKg_first_movecnt = match.count
        match.move_list.append(move)

        return move
    elif(move.dstx - move.srcx == -2):
        move.move_type = Move.TYPES['long_castling']
        move.captured_piece = dstpiece

        match.count += 1   
        match.writefield(move.srcx, move.srcy, Match.PIECES['blk'])
        match.writefield(move.dstx, move.dsty, srcpiece)
        rook = match.readfield(move.srcx - 4, move.srcy)
        match.writefield(move.srcx - 4, move.srcy, Match.PIECES['blk'])
        match.writefield(move.dstx + 1, move.dsty, rook)
        match.fifty_moves_count += 1
        if(srcpiece == Match.PIECES['wKg']):
            match.wKg_x = move.dstx
            match.wKg_y = move.dsty
            if(match.wKg_first_movecnt == 0):
                match.wKg_first_movecnt = match.count
        else:
            match.bKg_x = move.dstx
            match.bKg_y = move.dsty
            if(match.bKg_first_movecnt == 0):
                match.bKg_first_movecnt = match.count
        match.move_list.append(move)

        return move
    else:
        return generic.do_move(match, move, srcpiece, dstpiece)


def undo_short_castling(match, move):
    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count

    piece = match.readfield(move.dstx, move.dsty)
    rook = match.readfield(move.dstx - 1, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, Match.PIECES['blk'])
    match.writefield(move.dstx - 1, move.dsty, Match.PIECES['blk'])
    match.writefield(move.dstx + 1, move.dsty, rook)
    if(piece == Match.PIECES['wKg']):
        match.wKg_x = move.srcx
        match.wKg_y = move.srcy
        match.wKg_first_movecnt = 0
        match.wRk_h1_first_movecnt = 0
    else:
        match.bKg_x = move.srcx
        match.bKg_y = move.srcy
        match.bKg_first_movecnt = 0
        match.bRk_h8_first_movecnt = 0

    return move


def undo_long_castling(match, move):
    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count

    piece = match.readfield(move.dstx, move.dsty)
    rook = match.readfield(move.dstx + 1, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, Match.PIECES['blk'])
    match.writefield(move.dstx + 1, move.dsty, Match.PIECES['blk'])
    match.writefield(move.dstx - 2, move.dsty, rook)
    if(piece == Match.PIECES['wKg']):
        match.wKg_x = move.srcx
        match.wKg_y = move.srcy
        match.wKg_first_movecnt = 0
        match.wRk_a1_first_movecnt = 0
    else:
        match.bKg_x = move.srcx
        match.bKg_y = move.srcy
        match.bKg_first_movecnt = 0
        match.bRk_a8_first_movecnt = 0

    return move
