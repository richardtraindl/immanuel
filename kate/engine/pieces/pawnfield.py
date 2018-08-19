from .piecefield import cPieceField
from .piece import cTouch
from .pawn import cPawn


class cPawnField(cPieceField):
    def __init__(self, match, fieldx, fieldy):
        super().__init__(match, fieldx, fieldy, [match.PIECES['wPw']], [match.PIECES['bPw']])
        self.WHITE_BACK_STEPS = [ [1, -1], [-1, -1] ]
        self.BLACK_BACK_STEPS = [ [1, 1], [-1, 1] ]

    def is_field_touched(self, color, mode):
        if(color == self.match.COLORS['white']):
            steps = self.WHITE_BACK_STEPS
        else:
            steps = self.BLACK_BACK_STEPS
        for step in steps:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if( (color == self.match.COLORS['white'] and piece == self.match.PIECES['wPw']) or
                    (color == self.match.COLORS['black'] and piece == self.match.PIECES['bPw']) ):
                    if(mode == 0):
                        return True
                    elif(mode == 1):
                        cpawn = cPawn(self.match, x1, y1)
                        if(cpawn.is_move_stuck(self.fieldx, self.fieldy)):
                            continue
                        else:
                            return True
                    else: #mode == 2
                        cpawn = cPawn(self.match, x1, y1)
                        if(cpawn.is_move_stuck(self.fieldx, self.fieldy) or self.match.is_soft_pin(x1, y1)):
                            continue
                        else:
                            return True
        return False

    def field_color_touches(self, color, frdlytouches, enmytouches):
        BACK_STEPS = [ [1, -1], [-1, -1], [1, 1], [-1, 1] ]
        for step in BACK_STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if((step[1] == -1 and piece == self.match.PIECES['wPw']) or 
                   (step[1] == 1 and  piece == self.match.PIECES['bPw'])):
                    cpawn = cPawn(self.match, x1, y1)
                    if(cpawn.is_move_stuck(self.fieldx, self.fieldy)):
                        continue
                    
                    if(self.match.color_of_piece(piece) == color):
                        frdlytouches.append(cTouch(piece, x1, y1))
                    else:
                        enmytouches.append(cTouch(piece, x1, y1))

    def list_field_touches(self, color):
        touches = []
        if(color == self.match.COLORS['white']):
            STEPS = self.WHITE_BACK_STEPS
        else:
            STEPS = self.BLACK_BACK_STEPS
        for step in STEPS:
            x1 = self.fieldx + step[0]
            y1 = self.fieldy + step[1]
            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)
                if( (color == self.match.COLORS['white'] and piece == self.match.PIECES['wPw']) or
                    (color == self.match.COLORS['black'] and piece == self.match.PIECES['bPw']) ):
                    cpawn = cPawn(self.match, x1, y1)
                    if(cpawn.is_move_stuck(self.fieldx, self.fieldy)):
                        continue
                    touches.append(cTouch(piece, x1, y1))
        return touches

# class end

