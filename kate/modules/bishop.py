  

DIRS = {
    'north-east' : 1,
    'south-west' : 2,
    'north-west' : 3,
    'south-east' : 4,
    'undefined' : 5 }


REVERSE_DIRS = {
    'north-east' : DIRS['south-west'],
    'south-west' : DIRS['north-east'],
    'north-west' : DIRS['south-east'],
    'south-east' : DIRS['north-west'],
    'undefined' : 5 }

NEAST_X = 1
NEAST_Y = 1
SWEST_X = -1
SWEST_Y = -1
NWEST_X = -1
NWEST_Y = 1
SEAST_X = 1
SEAST_Y = -1

def bishop_direction(srcx, srcy, dstx, dsty):
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


def move_step(srcx, srcy, dstx, dsty):
    direction = bishop_direction(srcx, srcy, dstx, dsty)
    if(direction == DIRS['north-east']):
        return NEAST_X, NEAST_Y
    elif(direction == DIRS['south-west']):
        return SWEST_X, SWEST_Y
    elif(direction == DIRS['north-west']):
        return NWEST_X, NWEST_Y
    elif(direction == DIRS['south-east']):
        return SEAST_X, SEAST_Y
    else:
        return 8, 8


def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    direction = bishop_direction(srcx, srcy, dstx, dsty)
    if(direction == DIRS['undefined']):
        return False

    stepx, stepy = move_step(srcx, srcy, dstx, dsty)

    if(match.color_of_piece(piece) == match.COLORS['white']):
        pinned = DIRS['undefined']
        # fesselung = gib_weisse_figur_fesselung(_session->brett, _gzug->start_x, _gzug->start_y, _session->kw_feldnr_x, _session->kw_feldnr_y); \
    else:
        pinned = DIRS['undefined']
        # fesselung = gib_schwarze_figur_fesselung(_session->brett, _gzug->start_x, _gzug->start_y, _session->ks_feldnr_x, _session->ks_feldnr_y); \

    if(direction == DIRS['north-east'] or direction == DIRS['south-west']):
        if(pinned != DIRS['north-east'] and pinned != DIRS['south-west'] and pinned != DIRS['undefined']):
            return False
    elif(direction == DIRS['north-west'] or direction == DIRS['south-east']):
        if(pinned != DIRS['north-west'] and pinned != DIRS['south-east'] and pinned != DIRS['undefined']):
            return False

    x = srcx
    y = srcy
    while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
        x += stepx
        y += stepy
        field = match.readfield(x, y)
        if(x == dstx and y == dsty):
            if(match.color_of_piece(field)== match.color_of_piece(piece)):
                return False
            else:
                return True
        elif(field != match.PIECES['blk']):
            return False

    return False

