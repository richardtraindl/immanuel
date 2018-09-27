from .. values import *
from .piecefield import cPieceField


class cRookField(cPieceField):
    def __init__(self, match, fieldx, fieldy):
        super().__init__(match, fieldx, fieldy, [PIECES['wRk'], PIECES['wQu']], [PIECES['bRk'], PIECES['bQu']], [[0, 1], [0, -1], [1, 0], [-1, 0]])

# class end

