from kate.models import Match, Move
from kate.modules import values, pawn


def is_move_color_ok(piece, count):
    color = values.color_of_piece(piece)
    if(count % 2 == 0 and color == values.COLORS['white']):
        return True
    elif(count % 2 == 1 and color == values.COLORS['black']):
        return True
    else:
        return False


def is_move_inbounds(srcx, srcy, dstx, dsty):
    if(srcx < 0 or srcx > 7 or srcy < 0 or srcy > 7 or
       dstx < 0 or dstx > 7 or dsty < 0 or dsty > 7):
        return False
    else:
        return True


def is_move_valid(match, srcx, srcy, dstx, dsty, prom_piece):
    piece = match.readfield(srcx, srcy)

    if(not is_move_inbounds(srcx, srcy, dstx, dsty)):
        return False

    if(not is_move_color_ok(piece, match.count)):
        return False

    if(piece == values.PIECES['wPw'] or piece == values.PIECES['bPw']):
        if(not pawn.is_move_ok(match, srcx, srcy, dstx, dsty, prom_piece)):
            return False
        else:
            return True
    elif(piece == values.PIECES['wRk'] or piece == values.PIECES['bRk']):
        if(not rook.is_move_ok(match, srcx, srcy, dstx, dsty)):
            return False
        else:
            return True
    elif(piece == values.PIECES['wKn'] or piece == values.PIECES['bKn']):
        if(not knight.is_move_ok(match, srcx, srcy, dstx, dsty)):
            return False
        else:
            return True
    elif(piece == values.PIECES['wBp'] or piece == values.PIECES['bBp']):
        if(not bishop.is_move_ok(match, srcx, srcy, dstx, dsty)):
            return False
        else:
            return True
    elif(piece == values.PIECES['wQu'] or piece == values.PIECES['bQu']):
        if(not queen.is_move_ok(match, srcx, srcy, dstx, dsty)):
            return False
        else:
            return True
    elif(piece == values.PIECES['wKg'] or piece == values.PIECES['bKg']):
        if(not king.is_move_ok(match, srcx, srcy, dstx, dsty)):
            return False
        else:
            return True
    else:
        return False
