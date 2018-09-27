from .values import *
from .pieces.pawn import cPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen


class cGenerator:
    def __init__(self, match):
        self.match = match

    def generate_moves(self, mode):
        color = self.match.next_color()
        genmoves = []

        for y in range(0, 8, 1):
            for x in range(0, 8, 1):
                piece = self.match.readfield(x, y)
                if(piece == PIECES['blk'] or color != self.match.color_of_piece(piece)):
                    continue
                else:
                    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                        cpawn = cPawn(self.match, x, y)
                        genmoves.extend(cpawn.generate_moves(mode))
                    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                        crook = cRook(self.match, x, y)
                        genmoves.extend(crook.generate_moves(mode))
                    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                        cbishop = cBishop(self.match, x, y)
                        genmoves.extend(cbishop.generate_moves(mode))
                    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                        cknight = cKnight(self.match, x, y)
                        genmoves.extend(cknight.generate_moves(mode))
                    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                        cqueen = cQueen(self.match, x, y)
                        genmoves.extend(cqueen.generate_moves(mode))
                    else:
                        cking = cKing(self.match, x, y)
                        genmoves.extend(cking.generate_moves(mode))
        return genmoves

# class end


