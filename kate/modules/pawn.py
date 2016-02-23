from kate.models import Match, Move
from kate.modules import values, pawn


def is_move_ok(match, srcx, srcy, dstx, dsty, prom_piece):
    piece = match.readfield(srcx, srcy)
    if(piece == values.PIECES['wPw'] and dsty == 7 and not (prom_piece == values.PIECES['wQu'] or
       prom_piece == values.PIECES['wRk'] or prom_piece == values.PIECES['wBp'] or prom_piece == values.PIECES['wKn'])):
        return False
    elif(piece == values.PIECES['bPw'] and dsty == 0 and not (prom_piece == values.PIECES['bQu'] or 
         prom_piece == values.PIECES['bRk'] or prom_piece == values.PIECES['bBp'] or prom_piece == values.PIECES['bKn'])):
        return False
    return True
