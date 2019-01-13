from .. values import *
from .. match import *
from .pawn import cPawn
from .knight import cKnight
from .bishop import cBishop
from .rook import cRook
from .king import cKing
from .queen import cQueen


def obj_for_piece(match, piece, xpos, ypos):
    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return cPawn(match, xpos, ypos)
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        return cKnight(match, xpos, ypos)
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        return cBishop(match, xpos, ypos)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        return cRook(match, xpos, ypos)
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        return cQueen(match, xpos, ypos)
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        return cKing(match, xpos, ypos)
    else:
        return None
