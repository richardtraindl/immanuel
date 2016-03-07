from kate.models import Match

DIRS = {
    'valid' : 9,
    'undefined' : 10 }


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


def direction(srcx, srcy, dstx, dsty):
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



def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    knight_direction = direction(srcx, srcy, dstx, dsty)
    if(knight_direction == DIRS['undefined']):
        return False

    if(match.color_of_piece(piece) == match.COLORS['white']):
        pinned = DIRS['undefined']
        # fesselung = gib_weisse_figur_fesselung(_session->brett, _gzug->start_x, _gzug->start_y, _session->kw_feldnr_x, _session->kw_feldnr_y); \
    else:
        pinned = DIRS['undefined']
        # fesselung = gib_schwarze_figur_fesselung(_session->brett, _gzug->start_x, _gzug->start_y, _session->ks_feldnr_x, _session->ks_feldnr_y); \

    if(pinned != DIRS['undefined']):
        return False

    field = match.readfield(dstx, dsty)
    if(match.color_of_piece(field)== match.color_of_piece(piece)):
        return False

    return True
