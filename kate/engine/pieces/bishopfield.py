from .piecefield import cPieceField


class cBishopField(cPieceField):
    def __init__(self, match, fieldx, fieldy):
        super().__init__(match, fieldx, fieldy, [match.PIECES['wBp'], match.PIECES['wQu']], [match.PIECES['bBp'], match.PIECES['bQu']], [[1, 1], [-1, -1], [-1, 1], [1, -1]])

# class end

