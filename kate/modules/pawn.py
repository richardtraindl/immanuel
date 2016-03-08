from kate.models import Match
from kate.modules.rules import DIRS, UNDEF_X, UNDEF_Y, pin_dir


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


def pw_dir(srcx, srcy, dstx, dsty, piece):
    step_x = dstx - srcx
    step_y = dsty - srcy
    if(piece == Match.PIECES['wPw']):
        if(step_x == WHITE_1N_X and step_y == WHITE_1N_Y):
            return DIRS['valid']
        elif(step_x == WHITE_2N_X and step_y == WHITE_2N_Y):
            return DIRS['valid']
        elif(step_x == WHITE_1N1E_X and step_y == WHITE_1N1E_Y):
            return DIRS['valid']
        elif(step_x == WHITE_1N1W_X and step_y == WHITE_1N1W_Y):
            return DIRS['valid']
        else:
            return DIRS['undefined']
    else:
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == BLACK_1S_X and step_y == BLACK_1S_Y):
            return DIRS['valid']
        elif(step_x == BLACK_2S_X and step_y == BLACK_2S_Y):
            return DIRS['valid']
        elif(step_x == BLACK_1S1E_X and step_y == BLACK_1S1E_Y):
            return DIRS['valid']
        elif(step_x == BLACK_1S1W_X and step_y == BLACK_1S1W_Y):
            return DIRS['valid']
        else:
            return DIRS['undefined']

def is_move_ok(match, srcx, srcy, dstx, dsty, piece, prom_piece):
    direction = pw_dir(srcx, srcy, dstx, dsty, piece)
    if(direction == DIRS['undefined']):
        return False

    pin_dir = pin_dir(match, srcx, srcy)

    if(direction == DIRS['north'] or direction == DIRS['south']):
        if(pin_dir != DIRS['north'] and pin_dir != DIRS['south'] and pin_dir != DIRS['undefined']):
            return False
    elif(direction == DIRS['north-west'] or direction == DIRS['south-east']):
        if(pin_dir != DIRS['north-west'] and pin_dir != DIRS['south-east'] and pin_dir != DIRS['undefined']):
            return False
    elif(direction == DIRS['north-east'] or direction == DIRS['south-west']):
        if(pin_dir != DIRS['north-east'] and pin_dir != DIRS['south-west'] and pin_dir != DIRS['undefined']):
            return False

    if(piece == Match.PIECES['wPw'] and dsty == 7 and not (prom_piece == Match.PIECES['wQu'] or
       prom_piece == Match.PIECES['wRk'] or prom_piece == Match.PIECES['wBp'] or prom_piece == Match.PIECES['wKn'])):
        return False
    elif(piece == Match.PIECES['bPw'] and dsty == 0 and not (prom_piece == Match.PIECES['bQu'] or 
         prom_piece == Match.PIECES['bRk'] or prom_piece == Match.PIECES['bBp'] or prom_piece == Match.PIECES['bKn'])):
        return False

    return True
