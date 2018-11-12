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
        piecescnt = 0

        for y in range(0, 8, 1):
            for x in range(0, 8, 1):
                piece = self.match.readfield(x, y)
                if(piece == PIECES['blk'] or color != self.match.color_of_piece(piece)):
                    continue
                else:
                    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                        cpawn = cPawn(self.match, x, y)
                        pawnmoves = cpawn.generate_moves(mode)
                        if(len(pawnmoves) > 0):
                            piecescnt += 1
                            genmoves.extend(pawnmoves)
                    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                        crook = cRook(self.match, x, y)
                        rookmoves = crook.generate_moves(mode)
                        if(len(rookmoves) > 0):
                            piecescnt += 1
                            genmoves.extend(rookmoves)
                    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                        cbishop = cBishop(self.match, x, y)
                        bishopmoves = cbishop.generate_moves(mode)
                        if(len(bishopmoves) > 0):
                            piecescnt += 1
                            genmoves.extend(bishopmoves)
                    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                        cknight = cKnight(self.match, x, y)
                        knightmoves = cknight.generate_moves(mode)
                        if(len(knightmoves) > 0):
                            piecescnt += 1
                            genmoves.extend(knightmoves)
                    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                        cqueen = cQueen(self.match, x, y)
                        queenmoves = cqueen.generate_moves(mode)
                        if(len(queenmoves) > 0):
                            piecescnt += 1
                            genmoves.extend(queenmoves)
                    else:
                        cking = cKing(self.match, x, y)
                        kingmoves = cking.generate_moves(mode)
                        if(len(kingmoves) > 0):
                            piecescnt += 1
                            genmoves.extend(kingmoves)
        return genmoves, piecescnt

# class end


