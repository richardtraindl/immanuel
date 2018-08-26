from .pawn import cPawn
from .knight import cKnight
from .rook import cRook
from .bishop import cBishop
from .queen import cQueen
from .king import cKing
from .piece import cTouch


class cPieceField:
    def __init__(self, match, fieldx, fieldy, white_faces, black_faces):
        self.match = match
        self.fieldx = fieldx
        self.fieldy = fieldy
        self.white_faces = white_faces
        self.black_faces = black_faces
        self.STEPS = []

    def obj_for_piece(self, piece, x1, y1):
        if(piece == self.match.PIECES['wBp'] or piece == self.match.PIECES['bBp']):
            return cBishop(self.match, x1, y1)
        elif(piece == self.match.PIECES['wRk'] or piece == self.match.PIECES['bRk']):
            return cRook(self.match, x1, y1)
        elif(piece == self.match.PIECES['wQu'] or piece == self.match.PIECES['bQu']):
            return cQueen(self.match, x1, y1)
        elif(piece == self.match.PIECES['wKg'] or piece == self.match.PIECES['bKg']):
            return cKing(self.match, x1, y1)
        elif(piece == self.match.PIECES['wKn'] or piece == self.match.PIECES['bKn']):
            return cKnight(self.match, x1, y1)
        elif(piece == self.match.PIECES['wPw'] or piece == self.match.PIECES['bPw']):
            return cPawn(self.match, x1, y1)
        else:
            return None

    def is_field_touched(self, color, mode):
        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(self.fieldx, self.fieldy, stepx, stepy)
            if(x1 != self.match.UNDEF_X):
                piece = self.match.readfield(x1, y1)
                flag = False
                if(color == self.match.COLORS['white']):
                    for face in self.white_faces:
                        if(piece == face):
                            flag = True
                            break
                else:
                    for face in self.black_faces:
                        if(piece == face):
                            flag = True
                            break
                if(flag):
                    if(mode == 0):
                        return True
                    elif(mode == 1):
                        cpiece = self.obj_for_piece(piece, x1, y1)
                        if(cpiece.is_move_stuck(self.fieldx, self.fieldy)):
                            continue
                        else:
                            return True
                    else: #mode == 2
                        cpiece = self.obj_for_piece(piece, x1, y1)
                        if(cpiece.is_move_stuck(self.fieldx, self.fieldy) or self.match.is_soft_pin(x1, y1)):
                            continue
                        else:
                            return True
        return False

    def list_all_field_touches(self, color, frdlytouches, enmytouches):
        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(self.fieldx, self.fieldy, stepx, stepy)
            if(x1 != self.match.UNDEF_X):
                piece = self.match.readfield(x1, y1)
                wflag = False
                for face in self.white_faces:
                    if(piece == face):
                        wflag = True
                        break
                bflag = False
                for face in self.black_faces:
                    if(piece == face):
                        bflag = True
                        break
                if(wflag or bflag):
                    cpiece = self.obj_for_piece(piece, x1, y1)
                    if(cpiece.is_move_stuck(self.fieldx, self.fieldy)):
                        continue
                    if(self.match.color_of_piece(piece) == color):
                        frdlytouches.append(cTouch(piece, x1, y1))
                    else:
                        enmytouches.append(cTouch(piece, x1, y1))

    def list_field_touches(self, color):
        touches = []
        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(self.fieldx, self.fieldy, stepx, stepy)
            if(x1 != self.match.UNDEF_X):
                piece = self.match.readfield(x1, y1)
                cpiece = self.obj_for_piece(piece, x1, y1)
                if(cpiece.is_move_stuck(self.fieldx, self.fieldy)):
                    continue
                flag = False
                if(color == self.match.COLORS['white']):
                    for face in self.white_faces:
                        if(piece == face):
                            flag = True
                            break
                else:
                    for face in self.black_faces:
                        if(piece == face):
                            flag = True
                            break
                if(flag):
                    touches.append(cTouch(piece, x1, y1))
        return touches

    def count_touches(self, color):
        count = 0

        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(self.fieldx, self.fieldy, stepx, stepy)
            if(x1 != self.match.UNDEF_X):
                piece = self.match.readfield(x1, y1)

                cpiece = self.obj_for_piece(piece, self.fieldx, self.fieldy)
                if(cpiece.is_move_stuck(x1, y1)):
                    continue

                if(self.match.color_of_piece(piece) == color):
                    if(piece == self.match.PIECES['wKg'] or piece == self.match.PIECES['bKg'] or 
                       self.match.is_field_touched(color, x1, y1, 1) == False):
                        count += 1
        return count

# class end

class cTouchBeyond:
    def __init__(self, srcx, srcy, dstx, dsty, piece, fieldx, fieldy):
        self.agent_srcx = srcx
        self.agent_srcy = srcy
        self.agent_dstx = dstx
        self.agent_dsty = dsty        
        self.piece = piece
        self.fieldx = fieldx
        self.fieldy = fieldy
        self.attacker_beyond = []
        self.supporter_beyond = []


class cFork:
    def __init__(self, srcx, srcy, dstx, dsty, forkx, forky):
        self.agent_srcx = srcx
        self.agent_srcy = srcy
        self.agent_dstx = dstx
        self.agent_dsty = dsty        
        self.forkx = forkx
        self.forky = forky

