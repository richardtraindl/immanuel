from .. values import *
from .piecefield import cPieceField


class cBishopField(cPieceField):
    def __init__(self, match, fieldx, fieldy):
        super().__init__(match, fieldx, fieldy, [PIECES['wBp'], PIECES['wQu']], [PIECES['bBp'], PIECES['bQu']], [[1, 1], [-1, -1], [-1, 1], [1, -1]])

# class end

