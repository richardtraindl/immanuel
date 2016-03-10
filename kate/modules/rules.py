from kate.models import Match
from kate.modules import values, pawn, rook, knight, bishop, queen, king


ERROR_CODES = {
    'none' : 0,
    'general-error' : 1,
    'pawn-error' : 2,
    'rook-error' : 3,
    'knight-error' : 4,
    'bishop-error' : 5,
    'queen-error' : 6,
    'king-error' : 7,
}

ERROR_MSGS = {
    ERROR_CODES['none'] : "Zug ist OK.",
    ERROR_CODES['general-error'] : "Allgemeiner Fehler",
    ERROR_CODES['pawn-error'] : "Bauernzug Fehler",
    ERROR_CODES['rook-error'] : "Turmzug Fehler",
    ERROR_CODES['knight-error'] : "Springerzug Fehler",
    ERROR_CODES['bishop-error'] : "Läuferzug Fehler",
    ERROR_CODES['queen-error'] : "Damenzug Fehler",
    ERROR_CODES['king-error'] : "Königzug Fehler",
}


DIRS = {
    'north' : 1,
    'south' : 2,
    'east' : 3,
    'west' : 4,
    'north-east' : 5,
    'south-west' : 6,
    'north-west' : 7,
    'south-east' : 8,
    '2north' : 9,
    '2south' : 10,
    'sh-castling' : 11,
    'lg-castling' : 12:
    'valid' : 13,
    'undefined' : 14 
}


REVERSE_DIRS = {
    DIRS['north'] : DIRS['south'],
    DIRS['south'] : DIRS['north'],
    DIRS['east'] : DIRS['west'],
    DIRS['west'] : DIRS['east'],
    DIRS['north-east'] : DIRS['south-west'],
    DIRS['south-west'] : DIRS['north-east'],
    DIRS['north-west'] : DIRS['south-east'],
    DIRS['south-east'] : DIRS['north-west'],
    DIRS['2north'] : DIRS['2south'],
    DIRS['2south'] : DIRS['2north'],
    DIRS['sh-castling'] : DIRS['undefined'],
    DIRS['lg-castling'] : DIRS['undefined'],
    DIRS['valid'] : DIRS['valid'],
    DIRS['undefined'] : DIRS['undefined'] 
}

UNDEF_X = 8
UNDEF_Y = 8


def is_move_color_ok_OLD(piece, count):
    color = Match.color_of_piece(piece)
    if(count % 2 == 0 and color == Match.COLORS['white']):
        return True
    elif(count % 2 == 1 and color == Match.COLORS['black']):
        return True
    else:
        return False


def is_inbounds(x, y):
    if(x < 0 or x > 7 or y < 0 or y > 7):
        return False
    else:
        return True


def is_move_inbounds(srcx, srcy, dstx, dsty):
    if(srcx < 0 or srcx > 7 or srcy < 0 or srcy > 7 or
       dstx < 0 or dstx > 7 or dsty < 0 or dsty > 7):
        return False
    else:
        return True


def search(match, srcx, srcy, stepx, stepy):
    x = srcx + stepx
    y = srcy + stepy
    while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
        field = match.readfield(x, y)
        if(field != Match.PIECES['blk']):
            return x, y

        x += stepx
        y += stepy
    return UNDEF_X, UNDEF_Y


def pin_dir(match, scrx, srcy):
    piece = match.readfield(scrx, srcy)
    color = Match.color_of_piece(piece)
    if(color == Match.COLORS['white']):
        kgx = match.wKg_x
        kgy = match.wKg_y
    else:
        kgx = match.bKg_x
        kgy = match.bKg_y

    direction, stepx, stepy = rook.rk_step(None, scrx, srcy, kgx, kgy)
    if(direction != DIRS['undefined']):
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        if(dstx != UNDEF_X):
            piece = match.readfield(dstx, dsty)
            if( (color == Match.COLORS['white'] and piece == Match.PIECES['wKg']) or
                (color == Match.COLORS['black'] and piece == Match.PIECES['bKg']) ):
                reverse_dir = REVERSE_DIRS[direction]
                reverse_dir, stepx, stepy = rook.rk_step(reverse_dir, None, None, None, None)
                dstx, dsty = search(match, scrx, srcy, stepx, stepy)
                if(dstx != UNDEF_X):
                    piece = match.readfield(dstx, dsty)
                    if(color == Match.COLORS['white']):
                        if(piece == Match.PIECES['bQu'] or piece == Match.PIECES['bRk']):
                            return direction
                        else:
                            return DIRS['undefined']
                    else:
                        if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['wRk']):
                            return direction
                        else:
                            return DIRS['undefined']

    direction, stepx, stepy = bishop.bp_step(None, scrx, srcy, kgx, kgy)
    if(direction != DIRS['undefined']):
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        if(dstx != UNDEF_X):
            piece = match.readfield(dstx, dsty)
            if( (color == Match.COLORS['white'] and piece == Match.PIECES['wKg']) or
                (color == Match.COLORS['black'] and piece == Match.PIECES['bKg']) ):
                reverse_dir = REVERSE_DIRS[direction]
                reverse_dir, stepx, stepy = bishop.bp_step(reverse_dir, None, None, None, None)
                dstx, dsty = search(match, scrx, srcy, stepx, stepy)
                if(dstx != UNDEF_X):
                    piece = match.readfield(dstx, dsty)
                    if(color == Match.COLORS['white']):
                        if(piece == Match.PIECES['bQu'] or piece == Match.PIECES['bBp']):
                            return direction
                        else:
                            return DIRS['undefined']
                    else:
                        if(piece == Match.PIECES['wQu'] or piece == Match.PIECES['wBp']):
                            return direction
                        else:
                            return DIRS['undefined']
    return DIRS['undefined']


def attacked(match, scrx, srcy):
    piece = match.readfield(scrx, srcy)

    color = Match.color_of_piece(piece)

    RK_STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    for i in range(4):
        stepx = RK_STEPS[i][0]
        stepy = RK_STEPS[i][1]
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        if(dstx != UNDEF_X):
            piece = match.readfield(dstx, dsty)
            if( (color == Match.COLORS['white'] and (piece == Match.PIECES['bQu'] or piece == Match.PIECES['bRk'])) or
                (color == Match.COLORS['black'] and (piece == Match.PIECES['wQu'] or piece == Match.PIECES['wRk'])) ):
                return True, dstx, dsty

    BP_STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
    for i in range(4):
        stepx = BP_STEPS[i][0]
        stepy = BP_STEPS[i][1]
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        if(dstx != UNDEF_X):
            piece = match.readfield(dstx, dsty)
            if( (color == Match.COLORS['white'] and (piece == Match.PIECES['bQu'] or piece == Match.PIECES['bBp'])) or
                (color == Match.COLORS['black'] and (piece == Match.PIECES['wQu'] or piece == Match.PIECES['wBp'])) ):
                return True, dstx, dsty

    KN_STEPS = [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]
    for i in range(8):
        dstx = scrx + KN_STEPS[i][0]
        dsty = srcy + KN_STEPS[i][1]
        if(is_inbounds(dstx, dsty)):
            piece = match.readfield(dstx, dsty)
            if( (color == Match.COLORS['white'] and piece == Match.PIECES['bKn']) or
                (color == Match.COLORS['black'] and piece == Match.PIECES['wKn']) ):
                return True, dstx, dsty

    KG_STEPS = [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]
    for i in range(8):
        dstx = scrx + KG_STEPS[i][0]
        dsty = srcy + KG_STEPS[i][1]
        if(is_inbounds(dstx, dsty)):
            piece = match.readfield(dstx, dsty)
            if( (color == Match.COLORS['white'] and piece == Match.PIECES['bKg']) or
                (color == Match.COLORS['black'] and piece == Match.PIECES['wKg']) ):
                return True, dstx, dsty

    wPW_STEPS = [ [1, 1], [-1, 1] ]
    for i in range(2):
        dstx = scrx + wPW_STEPS[i][0]
        dsty = srcy + wPW_STEPS[i][1]
        if(is_inbounds(dstx, dsty)):
            piece = match.readfield(dstx, dsty)
            if(color == Match.COLORS['white'] and piece == Match.PIECES['bPw']):
                return True, dstx, dsty

    bPW_STEPS = [ [1, -1], [-1, -1] ]
    for i in range(2):
        dstx = scrx + bPW_STEPS[i][0]
        dsty = srcy + bPW_STEPS[i][1]
        if(is_inbounds(dstx, dsty)):
            piece = match.readfield(dstx, dsty)
            if(color == Match.COLORS['black'] and piece == Match.PIECES['wPw']):
                return True, dstx, dsty

    return False, UNDEF_X, UNDEF_Y


def is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece):
    if(not is_move_inbounds(srcx, srcy, dstx, dsty)):
        return False, ERROR_CODES['out-of-bounds']

    piece = match.readfield(srcx, srcy)

    if(match.next_color() != Match.color_of_piece(piece):
        return False, ERROR_CODES['wrong-color']

    if(piece == Match.PIECES['wPw'] or piece == Match.PIECES['bPw']):
        if(not pawn.is_move_ok(match, srcx, srcy, dstx, dsty, piece, prom_piece)):
            return False, ERROR_CODES['pawn-error']
        else:
            return True, ERROR_CODES['none']
    elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
        if(not rook.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False, ERROR_CODES['rook-error']
        else:
            return True, ERROR_CODES['none']
    elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
        if(not knight.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False, ERROR_CODES['knight-error']
        else:
            return True, ERROR_CODES['none']
    elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
        if(not bishop.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False, ERROR_CODES['bishop-error']
        else:
            return True, ERROR_CODES['none']
    elif(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
        if(not queen.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False, ERROR_CODES['queen-error']
        else:
            return True, ERROR_CODES['none']
    elif(piece == Match.PIECES['wKg'] or piece == Match.PIECES['bKg']):
        if(not king.is_move_ok(match, srcx, srcy, dstx, dsty, piece)):
            return False, ERROR_CODES['king-error']
        else:
            return True, ERROR_CODES['none']
    else:
        return False, ERROR_CODES['general-error']
