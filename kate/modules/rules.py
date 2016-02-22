from kate.models import Match, Move
from kate.modules import values, pawn


def is_move_color_ok(piece, count):
    color = values.color_of piece(piece)
    if(count % 2 == 0 and reverse_lookup(values.COLORS, color) == values.COLORS['black']):
        return True
    elif(count % 2 == 1 and reverse_lookup(values.COLORS, color) == values.COLORS['white']):
        return True
    else:
        return False


def is_move_inbounds(src, dest):
    if(src < 0 or src > 63 or dest < 0 or dest > 63):
        return False
    else:
        return True

def is_move_valid(match, src, dest, prom_piece):
    piece = match.readfield(src)

    if(not is_move_inbounds(src, dest)):
        return False

    if(not is_move_color_ok(piece, match.count)):
        return False

    if(piece == 'wPw' or piece == 'bPw'):
        if(not pawn.is_move_ok(match, src, dest, prom_piece)):
            return False
        else:
            return True
    elif(piece == 'wRk' or piece == 'bRk'):
        if(not rook.is_move_ok(match, src, dest)):
            return False
        else:
            return True
    elif(piece == 'wKn' or piece == 'bKn'):
        if(not knight.is_move_ok(match, src, dest)):
            return False
        else:
            return True
    elif(piece == 'wBp' or piece == 'bBp'):
        if(not bishop.is_move_ok(match, src, dest)):
            return False
        else:
            return True
    elif(piece == 'wQu' or piece == 'bQu'):
        if(not queen.is_move_ok(match, src, dest)):
            return False
        else:
            return True
    elif(piece == 'wKg' or piece == 'bKg'):
        if(not king.is_move_ok(match, src, dest)):
            return False
        else:
            return True
    else:
        return False
