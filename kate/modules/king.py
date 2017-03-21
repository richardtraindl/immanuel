from kate.models import Match
from kate.modules import rules


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


def is_field_attacked(match, color, fieldx, fieldy):
    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( (color == Match.COLORS['white'] and piece == Match.PIECES['wKg']) or
                (color == Match.COLORS['black'] and piece == Match.PIECES['bKg']) ):
                return True
    return False


def does_attack(match, srcx, srcy):
    king = match.readfield(srcx, srcy)

    if(king != Match.PIECES['wKg'] and king != Match.PIECES['bKg']):
        return False

    color = Match.color_of_piece(piece) 

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( Match.REVERSED_COLORS[color] == Match.color_of_piece(piece) ):
                return True

    return False


def count_attacks(match, srcx, srcy):
    count = 0

    king = match.readfield(srcx, srcy)

    if(king != Match.PIECES['wKg'] and king != Match.PIECES['bKg']):
        return count

    color = Match.color_of_piece(king)

    if(color == Match.COLORS['white']):
        counter = 1
    else:
        counter = -1

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( Match.REVERSED_COLORS[color] == Match.color_of_piece(piece) ):
                count += counter

    return count


def score_attacks(match, srcx, srcy):
    score = 0

    king = match.readfield(srcx, srcy)

    if(king != Match.PIECES['wKg'] and king != Match.PIECES['bKg']):
        return score

    color = Match.color_of_piece(king)

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( Match.REVERSED_COLORS[color] == Match.color_of_piece(piece) ):
                score += Match.SCORES[piece]

    return score


def does_support_attacked(match, srcx, srcy):
    king = match.readfield(srcx, srcy)

    if(king != Match.PIECES['wKg'] and king != Match.PIECES['bKg']):
        return False

    color = Match.color_of_piece(king)

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_attacked(match, Match.REVERSED_COLORS[color], x1, y1)):
                    return True

    return False


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

    if(color == Match.COLORS['white']):
        if(match.wKg_first_movecnt != 0 or match.wRk_h1_first_movecnt != 0):
            return False
    else:
        if(match.bKg_first_movecnt != 0 or match.bRk_h8_first_movecnt != 0):
            return False            

    king = match.readfield(srcx, srcy)
    match.writefield(srcx, srcy, Match.PIECES['blk'])
    for i in range(3):
        castlingx = srcx + i
        attacked = rules.is_field_attacked(match, opp_color, castlingx, srcy)
        if(attacked == True):            
            match.writefield(srcx, srcy, king)
            return False

    match.writefield(srcx, srcy, king)
    return True


def is_lg_castling_ok(match, srcx, srcy, dstx, dsty, piece):
    color = Match.color_of_piece(piece)

    opp_color = Match.REVERSED_COLORS[color]

    for i in range(1, 3, 1):
        fieldx = srcx - i
        field = match.readfield(fieldx, srcy)
        if(field != Match.PIECES['blk']):
            return False

    if(color == Match.COLORS['white']):
        if(match.wKg_first_movecnt != 0 or match.wRk_a1_first_movecnt != 0):
            return False
    else:
        if(match.bKg_first_movecnt != 0 or match.bRk_a8_first_movecnt != 0):
            return False

    king = match.readfield(srcx, srcy)
    match.writefield(srcx, srcy, Match.PIECES['blk'])
    for i in range(0, -3, -1):
        castlingx = srcx + i
        attacked = rules.is_field_attacked(match, opp_color, castlingx, srcy)
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
    attacked = rules.is_field_attacked(match, opp_color, dstx, dsty)
    match.writefield(srcx, srcy, king)
    match.writefield(dstx, dsty, captured)
    if(attacked == True):
        return False

    field = match.readfield(dstx, dsty)
    if(match.color_of_piece(field) == color):
        return False

    return True

