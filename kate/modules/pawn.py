from kate.models import Match


PAWN_DIRS = {
    'valid' : 9,
    'undefined' : 10 }

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


def direction(srcx, srcy, dstx, dsty, piece):
    step_x = dstx - srcx
    step_y = dsty - srcy
    if(piece == Match.PIECES['wPw']):
        if(step_x == WHITE_1N_X and step_y == WHITE_1N_Y):
            return PAWN_DIRS['valid']
        elif(step_x == WHITE_2N_X and step_y == WHITE_2N_Y):
            return PAWN_DIRS['valid']
        elif(step_x == WHITE_1N1E_X and step_y == WHITE_1N1E_Y):
            return PAWN_DIRS['valid']
        elif(step_x == WHITE_1N1W_X and step_y == WHITE_1N1W_Y):
            return PAWN_DIRS['valid']
        else:
            return PAWN_DIRS['undefined']
    else:
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == BLACK_1S_X and step_y == BLACK_1S_Y):
            return PAWN_DIRS['valid']
        elif(step_x == BLACK_2S_X and step_y == BLACK_2S_Y):
            return PAWN_DIRS['valid']
        elif(step_x == BLACK_1S1E_X and step_y == BLACK_1S1E_Y):
            return PAWN_DIRS['valid']
        elif(step_x == BLACK_1S1W_X and step_y == BLACK_1S1W_Y):
            return PAWN_DIRS['valid']
        else:
            return PAWN_DIRS['undefined']

def is_move_ok(match, srcx, srcy, dstx, dsty, piece, prom_piece):
    pawn_direction = direction(srcx, srcy, dstx, dsty, piece)
    if(direction == PAWN_DIRS['undefined']):
        return False

    # if(piece == match.PIECES['wPw']):
    # pinned = DIRS['undefined']
    # fesselung = gib_weisse_figur_fesselung(_session->brett, _gzug->start_x, _gzug->start_y, _session->kw_feldnr_x, _session->kw_feldnr_y); \

    #if(direction == WHITE_DIRS['1north'] or direction == WHITE_DIRS['2north']):
    #    if(pinned != WHITE_DIRS['north-east'] and pinned != DIRS['south-west'] and pinned != DIRS['undefined']):
    #    return False
    #(fesselung == mSTRECKE_UNDEF || fesselung == mSTRECKE_NORD_SUED) &&
    #_gzug->start_y - _gzug->ziel_y == -1){
    #    mABBRUCH_BEI_BAUER_NORD_ZUG_NOK

    # else if(richtung == mRICHT_NORD && 
    #(fesselung == mSTRECKE_UNDEF || fesselung == mSTRECKE_NORD_SUED) &&
    # _gzug->start_y == 1 && _gzug->start_y - _gzug->ziel_y == -2){
    #mABBRUCH_BEI_BAUER_2NORD_ZUG_NOK

    if(piece == match.PIECES['wPw'] and dsty == 7 and not (prom_piece == match.PIECES['wQu'] or
       prom_piece == match.PIECES['wRk'] or prom_piece == match.PIECES['wBp'] or prom_piece == match.PIECES['wKn'])):
        return False
    elif(piece == match.PIECES['bPw'] and dsty == 0 and not (prom_piece == match.PIECES['bQu'] or 
         prom_piece == match.PIECES['bRk'] or prom_piece == match.PIECES['bBp'] or prom_piece == match.PIECES['bKn'])):
        return False
    return True
