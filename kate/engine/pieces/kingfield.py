from .piecefield import cPieceField
from .piece import cTouch


class cKingField(cPieceField):
    def __init__(self, match, fieldx, fieldy):
        super().__init__(match, fieldx, fieldy, [match.PIECES['wKg']], [match.PIECES['bKg']], [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]])

    def is_field_touched(self, color):
        for step in self.STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if(color == self.match.COLORS['white'] and piece == self.white_faces[0]):
                    return True
                elif(color == self.match.COLORS['black'] and piece == self.black_faces[0]):
                    return True
        return False

    def list_all_field_touches(self, color, frdlytouches, enmytouches):
        for step in self.STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if(piece == self.white_faces[0] or piece == self.black_faces[0]):
                    if(self.match.color_of_piece(piece) == color):
                        frdlytouches.append(cTouch(piece, x1, y1))
                    else:
                        enmytouches.append(cTouch(piece, x1, y1))

    def list_field_touches(self, color):
        touches = []
        for step in self.STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if(color == self.match.COLORS['white'] and piece == self.white_faces[0]):
                    touches.append(cTouch(piece, x1, y1))
                elif(color == self.match.COLORS['black'] and piece == self.black_faces[0]):
                    touches.append(cTouch(piece, x1, y1))
        return touches

    def count_touches(self, color):
        count = 0
        for step in self.STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)

                if(piece == self.match.PIECES['blk']):
                    continue

                if(self.match.color_of_piece(piece) == color):
                    if(piece == self.match.PIECES['wKg'] or piece == self.match.PIECES['bKg'] or 
                       self.match.is_field_touched(color, x1, y1, 1) == False):
                        count += 1
        return count

# class end

