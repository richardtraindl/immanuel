from .piecefield import cPieceField


class cRookField(cPieceField):
    def __init__(self, match, fieldx, fieldy):
        super().__init__(match, fieldx, fieldy, [match.PIECES['wRk'], match.PIECES['wQu']], [match.PIECES['bRk'], match.PIECES['bQu']])
        self.STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]

# class end

