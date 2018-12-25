from .. values import *
from .piecefield import cPieceField
from .piece import cTouch
from .knight import cKnight


class cKnightField(cPieceField):
    def __init__(self, match, fieldx, fieldy):
        super().__init__(match, fieldx, fieldy, [PIECES['wKn']], [PIECES['bKn']], [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]])

    def is_field_touched(self, color, mode):
        for step in self.STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if((color == COLORS['white'] and piece == self.white_faces[0]) or
                   (color == COLORS['black'] and piece == self.black_faces[0])):
                    if(mode == 0):
                        return True
                    elif(mode == 1):
                        cknight = cKnight(self.match, x1, y1)
                        if(cknight.is_piece_stuck()):
                            continue
                        else:
                            return True
                    else: #mode == 2
                        cknight = cKnight(self.match, x1, y1)
                        if(cknight.is_piece_stuck() or self.match.is_soft_pin(x1, y1)):
                            continue
                        else:
                            return True
        return False

    def list_all_field_touches(self, color, frdlytouches, enmytouches):
        for step in self.STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if(piece == self.white_faces[0] or piece == self.black_faces[0]):
                    cknight = cKnight(self.match, x1, y1)
                    if(cknight.is_piece_stuck()):
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
                if( (color == COLORS['white'] and piece == self.white_faces[0]) or
                    (color == COLORS['black'] and piece == self.black_faces[0]) ):
                    cknight = cKnight(self.match, x1, y1)
                    if(cknight.is_piece_stuck()):
                        continue
                    else:
                        touches.append(cTouch(piece, x1, y1))
        return touches

    def count_touches(self, color, excludes):
        count = 0
        for step in self.STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                continue_flag = False
                for exclude in excludes:
                    if(exclude[0] == x1 and exclude[1] == y1):
                        continue_flag = True
                        break
                if(continue_flag):
                    continue

                piece = self.match.readfield(x1, y1)

                if(piece == PIECES['blk']):
                    continue

                cpiece = self.obj_for_piece(piece, self.fieldx, self.fieldy)
                if(cpiece.is_move_stuck(x1, y1)):
                    continue

                if(self.match.color_of_piece(piece) == color):
                    if(piece == PIECES['wKg'] or piece == PIECES['bKg'] or 
                       self.match.is_field_touched(color, x1, y1, self.match.EVAL_MODES['only-pins-to-king']) == False):
                        count += 1
        return count

# class end

