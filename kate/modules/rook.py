

DIRS = {
    'north' : 1,
    'south' : 2,
    'east' : 3,
    'west' : 4,
    'undefined' : 5 }

REVERSE_DIRS = {
    'north' : DIRS['south'],
    'south' : DIRS['north'],
    'east' : DIRS['west'],
    'west' : DIRS['east'],
    'undefined' : 5 }

NORTH_X = 0
NORTH_Y = 1
SOUTH_X = 0
SOUTH_Y = -1
EAST_X = 1
EAST_Y = 0
WEST_X = -1
WEST_Y = 0

def rook_direction(srcx, srcy, dstx, dsty):
    if( (srcx == dstx) and (srcy < dsty) ):
        return DIRS['north']
    elif( (srcx == dstx) and (srcy > dsty) ):
        return DIRS['south']
    elif( (srcx < dstx) and (srcy == dsty) ):
        return DIRS['east']
    elif( (srcx > dstx) and (srcy == dsty) ):
        return DIRS['west']
    else:
        return DIRS['undefined']


def move_step(srcx, srcy, dstx, dsty):
    direction = rook_direction(srcx, srcy, dstx, dsty)
    if(direction == DIRS['north']):
        return NORTH_X, NORTH_Y
    elif(direction == DIRS['south']):
        return SOUTH_X, SOUTH_Y
    elif(direction == DIRS['east']):
        return EAST_X, EAST_Y
    elif(direction == DIRS['west']):
        return WEST_X, WEST_Y
    else:
        return 8, 8


def is_move_ok(match, srcx, srcy, dstx, dsty, piece):
    direction = rook_direction(srcx, srcy, dstx, dsty)
    if(direction == DIRS['undefined']):
        return False

    stepx, stepy = move_step(srcx, srcy, dstx, dsty)

    if(match.color_of_piece(piece) == match.COLORS['white']):
        pinned = DIRS['undefined']
        # fesselung = gib_weisse_figur_fesselung(_session->brett, _gzug->start_x, _gzug->start_y, _session->kw_feldnr_x, _session->kw_feldnr_y); \
    else:
        pinned = DIRS['undefined']
        # fesselung = gib_schwarze_figur_fesselung(_session->brett, _gzug->start_x, _gzug->start_y, _session->ks_feldnr_x, _session->ks_feldnr_y); \

    if(direction == DIRS['north'] or direction == DIRS['south']):
        if(pinned != DIRS['north'] and pinned != DIRS['south'] and pinned != DIRS['undefined']):
            return False
    elif(direction == DIRS['east'] or direction == DIRS['west']):
        if(pinned != DIRS['east'] and pinned != DIRS['west'] and pinned != DIRS['undefined']):
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






