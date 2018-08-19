#from . match import *
#from . cvalues import *
#from .pieces import pawn, rook, knight, bishop, queen, king


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


"""def is_inbounds(x, y):
    if(x < 0 or x > 7 or y < 0 or y > 7):
        return False
    else:
        return True"""


"""def is_move_inbounds(srcx, srcy, dstx, dsty):
    if(srcx < 0 or srcx > 7 or srcy < 0 or srcy > 7 or
       dstx < 0 or dstx > 7 or dsty < 0 or dsty > 7):
        return False
    else:
        return True"""


"""def search(match, srcx, srcy, stepx, stepy):
    x = srcx + stepx
    y = srcy + stepy
    while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
        field = match.readfield(x, y)
        if(field != cMatch.PIECES['blk']):
            return x, y

        x += stepx
        y += stepy
    return UNDEF_X, UNDEF_Y"""







"""def is_field_touched(match, color, srcx, srcy, mode):
    if(queen.is_field_touched(match, color, srcx, srcy, mode)):
        return True

    if(rook.is_field_touched(match, color, srcx, srcy, mode)):
        return True

    if(bishop.is_field_touched(match, color, srcx, srcy, mode)):
        return True

    if(knight.is_field_touched(match, color, srcx, srcy, mode)):
        return True

    if(king.is_field_touched(match, color, srcx, srcy)):
        return True

    if(pawn.is_field_touched(match, color, srcx, srcy, mode)):
        return True

    return False"""


"""def is_king_attacked(match, x1, y1):
    king = match.readfield(x1, y1)

    if(king != cMatch.PIECES['wKg'] and king != cMatch.PIECES['bKg']):
        return False

    color = cMatch.color_of_piece(king)

    return is_field_touched(match, cMatch.REVERSED_COLORS[color], x1, y1, 0)"""


"""def is_king_after_move_attacked(match, srcx, srcy, dstx, dsty):
    piece = match.readfield(srcx, srcy)
    pawnenmy = None

    if(piece == cMatch.PIECES['wPw']):
        cpawn = pawn.cPawn(match, srcx, srcy)
        if(cpawn.is_white_ep_move_ok(dstx, dsty)):
            pawnenmy = match.readfield(dstx, srcy)
            match.writefield(dstx, srcy, cMatch.PIECES['blk'])
    elif(piece == cMatch.PIECES['bPw']):
        cpawn = pawn.cPawn(match, srcx, srcy)
        if(cpawn.is_black_ep_move_ok(dstx, dsty)):
            pawnenmy = match.readfield(dstx, srcy)
            match.writefield(dstx, srcy, cMatch.PIECES['blk'])

    match.writefield(srcx, srcy, cMatch.PIECES['blk'])
    dstpiece = match.readfield(dstx, dsty)
    match.writefield(dstx, dsty, piece)

    color = cMatch.color_of_piece(piece)

    if(color == cMatch.COLORS['white']):
        flag = is_field_touched(match, cMatch.COLORS['black'], match.wKg_x, match.wKg_y, 0)
    else:
        flag = is_field_touched(match,  cMatch.COLORS['white'], match.bKg_x, match.bKg_y, 0)
        
    match.writefield(dstx, dsty, dstpiece)
    match.writefield(srcx, srcy, piece)
    if(pawnenmy):
        match.writefield(dstx, srcy, pawnenmy)

    return flag"""








"""def is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece):
    if(not is_move_inbounds(srcx, srcy, dstx, dsty)):
        return False, RETURN_CODES['out-of-bounds']

    piece = match.readfield(srcx, srcy)

    if(match.next_color() != cMatch.color_of_piece(piece)):
        return False, RETURN_CODES['wrong-color']

    if(piece != cMatch.PIECES['wKg'] and piece != cMatch.PIECES['bKg']):
        if(is_king_after_move_attacked(match, srcx, srcy, dstx, dsty)):
            return False, RETURN_CODES['king-error']

    if(piece == cMatch.PIECES['wPw'] or piece == cMatch.PIECES['bPw']):
        cpawn = pawn.cPawn(match, srcx, srcy)
        if(cpawn.is_move_valid(dstx, dsty, prom_piece)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['pawn-error']
    elif(piece == cMatch.PIECES['wRk'] or piece == cMatch.PIECES['bRk']):
        crook =  rook.cRook(match, srcx, srcy)
        if(crook.is_move_valid(dstx, dsty)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['rook-error']
    elif(piece == cMatch.PIECES['wKn'] or piece == cMatch.PIECES['bKn']):
        cknight = knight.cKnight(match, srcx, srcy)
        if(cknight.is_move_valid(dstx, dsty)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['knight-error']
    elif(piece == cMatch.PIECES['wBp'] or piece == cMatch.PIECES['bBp']):
        cbishop = bishop.cBishop(match, srcx, srcy)
        if(cbishop.is_move_valid(dstx, dsty)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['bishop-error']
    elif(piece == cMatch.PIECES['wQu'] or piece == cMatch.PIECES['bQu']):
        cqueen = queen.cQueen(match, srcx, srcy)
        if(cqueen.is_move_valid(dstx, dsty)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['queen-error']
    elif(piece == cMatch.PIECES['wKg'] or piece == cMatch.PIECES['bKg']):
        cking = king.cKing(match, srcx, srcy)
        if(cking.is_move_valid(dstx, dsty)):
            return True, RETURN_CODES['ok']
        else:
            return False, RETURN_CODES['king-error']
    else:
        return False, RETURN_CODES['general-error']"""

