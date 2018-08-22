from .piecefield import cPieceField
from .piece import cTouch
from .knight import cKnight


class cKnightField(cPieceField):
    def __init__(self, match, fieldx, fieldy):
        super().__init__(match, fieldx, fieldy, [match.PIECES['wKn']], [match.PIECES['bKn']])
        self.STEPS = [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]

    def is_field_touched(self, color, mode):
        for step in self.STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if((color == self.match.COLORS['white'] and piece == self.white_faces[0]) or
                   (color == self.match.COLORS['black'] and piece == self.black_faces[0])):
                    if(mode == 0):
                        return True
                    elif(mode == 1):
                        cknight = cKnight(self.match, x1, y1)
                        if(cknight.is_piece_stuck_new()):
                            continue
                        else:
                            return True
                    else: #mode == 2
                        cknight = cKnight(self.match, x1, y1)
                        if(cknight.is_piece_stuck_new() or self.match.is_soft_pin(x1, y1)):
                            continue
                        else:
                            return True
        return False

    def field_color_touches(self, color, frdlytouches, enmytouches):
        for step in self.STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if(piece == self.white_faces[0] or piece == self.black_faces[0]):
                    cknight = cKnight(self.match, x1, y1)
                    if(cknight.is_piece_stuck_new()):
                        continue
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
                if( (color == self.match.COLORS['white'] and piece == self.white_faces[0]) or
                    (color == self.match.COLORS['black'] and piece == self.black_faces[0]) ):
                    cknight = cKnight(self.match, x1, y1)
                    if(cknight.is_piece_stuck_new()):
                        continue
                    else:
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

                cpiece = self.obj_for_piece(piece, self.fieldx, self.fieldy)
                if(cpiece.is_move_stuck(x1, y1)):
                    continue

                if(self.match.color_of_piece(piece) == color):
                    if(piece == self.match.PIECES['wKg'] or piece == self.match.PIECES['bKg'] or 
                       self.match.is_field_touched(color, x1, y1, 1) == False):
                        count += 1
        return count

# class end

