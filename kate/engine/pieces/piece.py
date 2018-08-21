

class cPiece:
    DIRS = { 'valid' : 13, 'undefined' : 14 }
    DIRS_ARY = [DIRS['undefined'], DIRS['undefined'], DIRS['undefined'], DIRS['undefined']]

    REVERSE_DIRS = { DIRS['valid'] : DIRS['valid'], DIRS['undefined'] : DIRS['undefined'] }

    STEPS = []

    UNDEF_X = 8
    UNDEF_Y = 8

    def __init__(self, match, xpos, ypos):
        self.match = match
        self.xpos = xpos
        self.ypos = ypos
        self.piece = match.readfield(xpos, ypos)
        self.color = match.color_of_piece(self.piece)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        return cls.DIRS['undefined']

    @classmethod
    def step_for_dir(cls, direction):
        return cls.UNDEF_X, cls.UNDEF_Y

    def is_piece_trapped(self):
        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                dstpiece = self.match.readfield(x1, y1)
                if(dstpiece == self.match.PIECES['blk']):
                    return False
                elif(self.match.color_of_piece(dstpiece) == self.color):
                    continue
                else:
                    if(self.match.is_field_touched(self.match.oppcolor_of_piece(self.piece), x1, y1, 0)):
                        if(self.match.PIECES_RANK[self.piece] <= self.match.PIECES_RANK[dstpiece]):
                            return False
                    else:
                        return False
        return True

    def is_piece_stuck_new(self):
        pin_dir = self.match.evaluate_pin_dir(self.xpos, self.ypos) # self.color, 
        for piecedir in self.DIRS:
            if(pin_dir == piecedir):
                return False
        return True

    def is_move_stuck(self, dstx, dsty):
        mv_dir = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        pin_dir = self.match.evaluate_pin_dir(self.xpos, self.ypos)
        if(pin_dir == self.DIRS['undefined'] or mv_dir == pin_dir or self.REVERSE_DIRS[mv_dir] == pin_dir):
            return False
        else:
            return True

    # version for rook and bishop - other pieces override function
    def is_move_valid(self, dstx, dsty):
        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == self.DIRS['undefined']):
            return False

        stepx, stepy = self.step_for_dir(direction)
        pin_dir = self.match.evaluate_pin_dir(self.xpos, self.ypos) # self.color, 
        if(direction == self.DIRS_ARY[0] or direction == self.DIRS_ARY[1]):
            if(pin_dir != self.DIRS_ARY[0] and pin_dir != self.DIRS_ARY[1] and pin_dir != self.DIRS['undefined']):
                return False
        elif(direction == self.DIRS_ARY[2] or direction == self.DIRS_ARY[3]):
            if(pin_dir != self.DIRS_ARY[2] and pin_dir != self.DIRS_ARY[3] and pin_dir != self.DIRS['undefined']):
                return False

        x = self.xpos + stepx
        y = self.ypos + stepy
        while(x >= 0 and x <= 7 and y >= 0 and y <= 7):
            field = self.match.readfield(x, y)
            if(x == dstx and y == dsty):
                if(self.match.color_of_piece(field) == self.color):
                    return False
                else:
                    return True
            elif(field != self.match.PIECES['blk']):
                return False

            x += stepx
            y += stepy

        return False

    # version for rook and bishop - other pieces override function
    def find_attacks_and_supports(self, dstx, dsty, attacked, supported):
        from .. analyze_helper import field_touches_beyond

        opp_color = self.match.oppcolor_of_piece(self.color)
        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1, y1 = self.match.search(dstx, dsty, stepx , stepy)
            if(x1 !=  self.match.UNDEF_X):
                if(x1 == self.xpos and y1 == self.ypos):
                    continue

                cpiece = cPiece(self.match, dstx, dsty)
                if(cpiece.is_move_stuck(x1, y1)):
                    continue

                piece = self.match.readfield(x1, y1)
                if(self.match.color_of_piece(piece) == opp_color):
                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    attacked.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
                    field_touches_beyond(self.match, opp_color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###
                else:
                    if(piece == self.match.PIECES['blk'] or piece == self.match.PIECES['wKg'] or piece == self.match.PIECES['bKg']):
                        continue
                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    supported.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
                    field_touches_beyond(self.match, self.color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###

# class end


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

