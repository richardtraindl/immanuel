from kate.models import Match

DIRS = {
    'north-east' : 5,
    'south-west' : 6,
    'north-west' : 7,
    'south-east' : 8,
    'undefined' : 10 }

REVERSE_DIRS = {
    'north-east' : DIRS['south-west'],
    'south-west' : DIRS['north-east'],
    'north-west' : DIRS['south-east'],
    'south-east' : DIRS['north-west'],
    'undefined' : 10 }

NEAST_X = 1
NEAST_Y = 1
SWEST_X = -1
SWEST_Y = -1
NWEST_X = -1
NWEST_Y = 1
SEAST_X = 1
SEAST_Y = -1


def direction(srcx, srcy, dstx, dsty):
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

def step(bishop_direction=None, srcx=None, srcy=None, dstx=None, dsty=None):
    if(bishop_direction == None):
        bishop_direction = direction(srcx, srcy, dstx, dsty)

    if(bishop_direction == DIRS['north-east']):
        return NEAST_X, NEAST_Y
    elif(bishop_direction == DIRS['south-west']):
        return SWEST_X, SWEST_Y
    elif(bishop_direction == DIRS['north-west']):
        return NWEST_X, NWEST_Y
    elif(bishop_direction == DIRS['south-east']):
        return SEAST_X, SEAST_Y
    else:
        return 8, 8


def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    bishop_direction = direction(srcx, srcy, dstx, dsty)
    if(bishop_direction == DIRS['undefined']):
        return False

    stepx, stepy = step(None, srcx, srcy, dstx, dsty)

    if(match.color_of_piece(piece) == match.COLORS['white']):
        pinned = DIRS['undefined']
        # fesselung = gib_weisse_figur_fesselung(_session->brett, _gzug->start_x, _gzug->start_y, _session->kw_feldnr_x, _session->kw_feldnr_y); \
    else:
        pinned = DIRS['undefined']
        # fesselung = gib_schwarze_figur_fesselung(_session->brett, _gzug->start_x, _gzug->start_y, _session->ks_feldnr_x, _session->ks_feldnr_y); \

    if(bishop_direction == DIRS['north-east'] or bishop_direction == DIRS['south-west']):
        if(pinned != DIRS['north-east'] and pinned != DIRS['south-west'] and pinned != DIRS['undefined']):
            return False
    elif(bishop_direction == DIRS['north-west'] or bishop_direction == DIRS['south-east']):
        if(pinned != DIRS['north-west'] and pinned != DIRS['south-east'] and pinned != DIRS['undefined']):
            return False

    x = srcx + stepx
    y = srcy + stepy
    while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
        field = match.readfield(x, y)
        if(x == dstx and y == dsty):
            if(match.color_of_piece(field)== match.color_of_piece(piece)):
                return False
            else:
                return True
        elif(field != match.PIECES['blk']):
            return False

        x += stepx
        y += stepy

    return False

