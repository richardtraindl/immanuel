from .match import *
from .pieces import pawn, rook, knight, bishop, queen, king


RETURN_CODES = {
    'ok' : 10,
    'draw' : 11,
    'winner_white' : 12,
    'winner_black' : 13,
    'match-cancelled' : 14,
    'wrong-color' : 15,
    'pawn-error' : 20,
    'rook-error' : 21,
    'knight-error' : 22,
    'bishop-error' : 23,
    'queen-error' : 24,
    'king-error' : 25,
    'format-error' : 30,
    'out-of-bounds' : 31,
    'general-error' : 40,
}

RETURN_MSGS = {
    RETURN_CODES['ok'] : "move okay",
    RETURN_CODES['draw'] : "draw",
    RETURN_CODES['winner_white'] : "winner white",
    RETURN_CODES['winner_black'] : "winner black",
    RETURN_CODES['match-cancelled'] : " match is cancelled",
    RETURN_CODES['wrong-color'] : "wrong color",
    RETURN_CODES['pawn-error'] : "pawn error",
    RETURN_CODES['rook-error'] : "rook error",
    RETURN_CODES['knight-error'] : "knight error",
    RETURN_CODES['bishop-error'] : "bishop error",
    RETURN_CODES['queen-error'] : "queen error",
    RETURN_CODES['king-error'] : "king error",
    RETURN_CODES['format-error'] : "format wrror",
    RETURN_CODES['out-of-bounds'] : "wrong square",
    RETURN_CODES['general-error'] : "general error",
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
    'lg-castling' : 12,
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
        if(field != PIECES['blk']):
            return x, y

        x += stepx
        y += stepy
    return UNDEF_X, UNDEF_Y


def pin_dir(match, scrx, srcy):
    piece = match.readfield(scrx, srcy)
    color = match.color_of_piece(piece)
    if(color == COLORS['white']):
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
            if( (color == COLORS['white'] and piece == PIECES['wKg']) or
                (color == COLORS['black'] and piece == PIECES['bKg']) ):
                reverse_dir = REVERSE_DIRS[direction]
                reverse_dir, stepx, stepy = rook.rk_step(reverse_dir, None, None, None, None)
                dstx, dsty = search(match, scrx, srcy, stepx, stepy)
                if(dstx != UNDEF_X):
                    piece = match.readfield(dstx, dsty)
                    if(color == COLORS['white']):
                        if(piece == PIECES['bQu'] or piece == PIECES['bRk']):
                            return direction
                        else:
                            return DIRS['undefined']
                    else:
                        if(piece == PIECES['wQu'] or piece == PIECES['wRk']):
                            return direction
                        else:
                            return DIRS['undefined']

    direction, stepx, stepy = bishop.bp_step(None, scrx, srcy, kgx, kgy)
    if(direction != DIRS['undefined']):
        dstx, dsty = search(match, scrx, srcy, stepx, stepy)
        if(dstx != UNDEF_X):
            piece = match.readfield(dstx, dsty)
            if( (color == COLORS['white'] and piece == PIECES['wKg']) or
                (color == COLORS['black'] and piece == PIECES['bKg']) ):
                reverse_dir = REVERSE_DIRS[direction]
                reverse_dir, stepx, stepy = bishop.bp_step(reverse_dir, None, None, None, None)
                dstx, dsty = search(match, scrx, srcy, stepx, stepy)
                if(dstx != UNDEF_X):
                    piece = match.readfield(dstx, dsty)
                    if(color == COLORS['white']):
                        if(piece == PIECES['bQu'] or piece == PIECES['bBp']):
                            return direction
                        else:
                            return DIRS['undefined']
                    else:
                        if(piece == PIECES['wQu'] or piece == PIECES['wBp']):
                            return direction
                        else:
                            return DIRS['undefined']
    return DIRS['undefined']


def is_field_touched(match, color, srcx, srcy):
    if(rook.is_field_touched(match, color, srcx, srcy)):
        return True

    if(bishop.is_field_touched(match, color, srcx, srcy)):
        return True

    if(knight.is_field_touched(match, color, srcx, srcy)):
        return True

    if(king.is_field_touched(match, color, srcx, srcy)):
        return True

    if(pawn.is_field_touched(match, color, srcx, srcy)):
        return True

    return False


def list_field_touches(match, color, srcx, srcy):
    touches = []

    newtouches = rook.list_field_touches(match, color, srcx, srcy)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    newtouches = bishop.list_field_touches(match, color, srcx, srcy)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    newtouches = knight.list_field_touches(match, color, srcx, srcy)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    newtouches = king.list_field_touches(match, color, srcx, srcy)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    newtouches = pawn.list_field_touches(match, color, srcx, srcy)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    return touches


def is_king_attacked(match, x1, y1):
    king = match.readfield(x1, y1)

    if(king != PIECES['wKg'] and king != PIECES['bKg']):
        return False

    color = match.color_of_piece(king)

    return is_field_touched(match, match.REVERSED_COLORS[color], x1, y1)


def is_king_after_move_attacked(match, srcx, srcy, dstx, dsty):
    piece = match.readfield(srcx, srcy)
    match.writefield(srcx, srcy, PIECES['blk'])
    dstpiece = match.readfield(dstx, dsty)
    match.writefield(dstx, dsty, piece)

    color = match.color_of_piece(piece)

    if(color == COLORS['white']):
        flag = is_field_touched(match, COLORS['black'], match.wKg_x, match.wKg_y)
    else:
        flag = is_field_touched(match,  COLORS['white'], match.bKg_x, match.bKg_y)
        
    match.writefield(dstx, dsty, dstpiece)
    match.writefield(srcx, srcy, piece)

    return flag


def is_move_available(match):
    color = match.next_color()
    for y1 in range(8):
        for x1 in range(8):
            piece = match.readfield(x1, y1)
            if(color == match.color_of_piece(piece)):
                if(color == COLORS['white']):
                    prom_piece = PIECES['wQu']
                else:
                    prom_piece = PIECES['bQu']

                for y2 in range(8):
                    for x2 in range(8):
                        flag = is_move_valid(match, x1, y1, x2, y2, prom_piece)[0]
                        if(flag):
                            return True
    return False


def game_status(match):
    if(is_move_available(match)):
        return STATUS['open']
    else:
        if(match.next_color() == COLORS['white']):
            if(is_field_touched(match, COLORS['black'], match.wKg_x, match.wKg_y)):
                return STATUS['winner_black']
        else:
            if(is_field_touched(match, COLORS['white'], match.bKg_x, match.bKg_y)):
                return STATUS['winner_white']

    return STATUS['draw']


def is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece):
    #print(" counts " + str(match.wKg_first_movecnt) + " " + str(match.wRk_h1_first_movecnt)  + " " + str(match.wRk_a1_first_movecnt))
    #print(" counts " + str(match.bKg_first_movecnt) + " " + str(match.bRk_h8_first_movecnt)  + " " + str(match.bRk_a8_first_movecnt))
    #print("-------------------------------------------")
    if(not is_move_inbounds(srcx, srcy, dstx, dsty)):
        return False, RETURN_CODES['out-of-bounds']

    piece = match.readfield(srcx, srcy)

    if(match.next_color() != match.color_of_piece(piece)):
        return False, RETURN_CODES['wrong-color']

    if(piece != PIECES['wKg'] and piece != PIECES['bKg']):
        if(is_king_after_move_attacked(match, srcx, srcy, dstx, dsty)):
            return False, RETURN_CODES['king-error']

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        if(pawn.is_move_valid(match, srcx, srcy, dstx, dsty, piece, prom_piece)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['pawn-error']
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        if(rook.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['rook-error']
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        if(knight.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['knight-error']
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        if(bishop.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['bishop-error']
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        if(queen.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['queen-error']
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(king.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['king-error']
    else:
        return False, RETURN_CODES['general-error']
