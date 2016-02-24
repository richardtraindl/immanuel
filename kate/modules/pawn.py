from kate.models import Match, Move
from kate.modules import values, pawn


def is_move_ok(match, srcx, srcy, dstx, dsty, prom_piece):
    piece = match.readfield(srcx, srcy)
    if(piece == match.PIECES['wPw'] and dsty == 7 and not (prom_piece == match.PIECES['wQu'] or
       prom_piece == match.PIECES['wRk'] or prom_piece == match.PIECES['wBp'] or prom_piece == match.PIECES['wKn'])):
        return False
    elif(piece == match.PIECES['bPw'] and dsty == 0 and not (prom_piece == match.PIECES['bQu'] or 
         prom_piece == match.PIECES['bRk'] or prom_piece == match.PIECES['bBp'] or prom_piece == match.PIECES['bKn'])):
        return False
    return True
