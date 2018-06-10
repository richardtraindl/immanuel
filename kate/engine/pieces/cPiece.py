from .. match import *
from .. cvalues import *


class cPiece:
    ROLE_PAWN = 1
    ROLE_ROOK = 2
    ROLE_KNIGHT = 3
    ROLE_BISHOP = 4
    ROLE_QUEEN = 5
    ROLE_KING = 6

    COLOR_WHITE = 11
    COLOR_BLACK = 12
    
    def __init__(self, piece, fieldx, fieldy):
        self.role = role
        self.color = color
        self.xpos = xpos
        self.ypos = ypos
        self.mvcnt = mvcnt
        self.promoted_pawn = promoted_pawn


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

