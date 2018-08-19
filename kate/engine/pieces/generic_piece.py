

class cTouch:
    def __init__(self, piece, fieldx, fieldy):
        self.piece = piece
        self.fieldx = fieldx
        self.fieldy = fieldy


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

