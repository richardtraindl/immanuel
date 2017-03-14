from kate.models import Match, Move
from kate.modules import rules


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


def is_field_attacked(match, color, fieldx, fieldy):
    if(color == Match.COLORS['white']):
        STEPS = WPW_BACK_STEPS
    else:
        STEPS = BPW_BACK_STEPS

    for i in range(2):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( (color == Match.COLORS['white'] and piece == Match.PIECES['wPw']) or
                (color == Match.COLORS['black'] and piece == Match.PIECES['bPw']):
                return True
   return True


def does_attack(match, srcx, srcy):
    pawn = match.readfield(srcx, srcy)
    color = Match.color_of_piece(pawn)

    if(color == Match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if( color != Match.color_of_piece(piece) ):
                return True

    return False


def does_support_attacked(match, srcx, srcy):
    pawn = match.readfield(srcx, srcy)
    color = Match.color_of_piece(pawn)

    if(color == Match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == Match.PIECES['blk'] or piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
                continue
            if( color == Match.color_of_piece(piece) ):
                if(rules.is_field_attacked(match, Match.REVERSED_COLORS[color], x1, y1):
                    return True

    return False


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
    if(piece == Match.PIECES['blk'] and opp_piece == Match.PIECES['bPw'] and move.srcx == move.dstx and move.dstx == dstx and move.srcy - 2 == move.dsty):
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
    if(piece == Match.PIECES['blk'] and opp_piece == Match.PIECES['wPw'] and move.srcx == move.dstx and move.dstx == dstx and move.srcy + 2 == move.dsty):
        return True
    else:
        return False


def is_move_ok(match, srcx, srcy, dstx, dsty, piece, prom_piece):
    DIRS = rules.DIRS
    direction = pw_dir(srcx, srcy, dstx, dsty, piece)
    if(direction == DIRS['undefined']):
        return False

    pin_dir = rules.pin_dir(match, srcx, srcy)

    if(direction == DIRS['north'] or direction == DIRS['south'] or direction == DIRS['2north'] 
        or direction == DIRS['2south']):
        if(pin_dir != DIRS['north'] and pin_dir != DIRS['south'] and pin_dir != DIRS['undefined']):
            return False
    elif(direction == DIRS['north-west'] or direction == DIRS['south-east']):
        if(pin_dir != DIRS['north-west'] and pin_dir != DIRS['south-east'] and pin_dir != DIRS['undefined']):
            return False
    elif(direction == DIRS['north-east'] or direction == DIRS['south-west']):
        if(pin_dir != DIRS['north-east'] and pin_dir != DIRS['south-west'] and pin_dir != DIRS['undefined']):
            return False

    dstpiece = match.readfield(dstx, dsty)
    dstcolor = Match.color_of_piece(dstpiece)
    if(direction == DIRS['north'] or direction == DIRS['south']):
        if(dstpiece != Match.PIECES['blk']):
            return False
    elif(direction == DIRS['2north']):
        midpiece = match.readfield(dstx, srcy + 1)
        if(midpiece != Match.PIECES['blk'] or dstpiece != Match.PIECES['blk']):
            return False
    elif(direction == DIRS['2south']):
        midpiece = match.readfield(dstx, srcy - 1)
        if(midpiece != Match.PIECES['blk'] or dstpiece != Match.PIECES['blk']):
            return False
    if(direction == DIRS['north-west'] or direction == DIRS['north-east']):
        if(dstcolor != Match.COLORS['black']):
            return is_white_ep_move_ok(match, srcx, srcy, dstx, dsty)
    elif(direction == DIRS['south-east'] or direction == DIRS['south-west']):
        if(dstcolor != Match.COLORS['white']):
            return is_black_ep_move_ok(match, srcx, srcy, dstx, dsty)

    if(piece == Match.PIECES['wPw'] and dsty == 7 and not (prom_piece == Match.PIECES['wQu'] or
       prom_piece == Match.PIECES['wRk'] or prom_piece == Match.PIECES['wBp'] or prom_piece == Match.PIECES['wKn'])):
        return False
    elif(piece == Match.PIECES['bPw'] and dsty == 0 and not (prom_piece == Match.PIECES['bQu'] or 
         prom_piece == Match.PIECES['bRk'] or prom_piece == Match.PIECES['bBp'] or prom_piece == Match.PIECES['bKn'])):
        return False

    return True
