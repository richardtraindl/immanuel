from kate.models import Match


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


def direction(srcx, srcy, dstx, dsty):
    step_x = dstx - srcx
    step_y = dsty - srcy
    if(step_x == STEP_1N_X and step_y == STEP_1N_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1N1E_X and step_y == STEP_1N1E_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1E_X and step_y == STEP_1E_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1S1E_X and step_y == STEP_1S1E_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1S_X and step_y == STEP_1S_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1S1W_X and step_y == STEP_1S1W_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1W_X and step_y == STEP_1W_Y):
        return KING_DIRS['valid']
    elif(step_x == STEP_1N1W_X and step_y == STEP_1N1W_Y):
        return KING_DIRS['valid']
    else:
        return KING_DIRS['undefined']


def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    king_direction = direction(srcx, srcy, dstx, dsty)
    if(king_direction == KING_DIRS['undefined']):
        return False

    if(match.color_of_piece(piece) == match.COLORS['white']):
        attached = False
        # ge_figur = gib_feld(_session->brett, _gzug->ziel_x, _gzug->ziel_y); \
        # if(gib_farbe(ge_figur) == FARBE){ return mNOK; } \
        # figur = gib_feld(_session->brett, _gzug->start_x, _gzug->start_y); \
        # setze_feld(_session->brett, _gzug->start_x, _gzug->start_y, mLEER); \
        # setze_feld(_session->brett, _gzug->ziel_x, _gzug->ziel_y, figur); \
        # if(ist_feld_bedroht(_session->brett, GEGN_FARBE, _gzug->ziel_x, _gzug->ziel_y)){ \
        # setze_feld(_session->brett, _gzug->start_x, _gzug->start_y, figur); \
        # setze_feld(_session->brett, _gzug->ziel_x, _gzug->ziel_y, ge_figur); \
        # return mNOK; \
    else:
        attached = False

    if(attached == True):
        return False

    field = match.readfield(dstx, dsty)
    if(match.color_of_piece(field)== match.color_of_piece(piece)):
        return False

    return True

