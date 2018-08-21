from . piece import *


class cKnight(cPiece):
    STEPS = [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]

    STEP_2N1E_X = 1
    STEP_2N1E_Y = 2
    STEP_1N2E_X = 2
    STEP_1N2E_Y = 1
    STEP_1S2E_X = 2
    STEP_1S2E_Y = -1
    STEP_2S1E_X = 1
    STEP_2S1E_Y = -2
    STEP_2S1W_X = -1
    STEP_2S1W_Y = -2
    STEP_1S2W_X = -2
    STEP_1S2W_Y = -1
    STEP_1N2W_X = -2
    STEP_1N2W_Y = 1
    STEP_2N1W_X = -1
    STEP_2N1W_Y = 2

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == cls.STEP_2N1E_X and step_y == cls.STEP_2N1E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1N2E_X and step_y == cls.STEP_1N2E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1S2E_X and step_y == cls.STEP_1S2E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_2S1E_X and step_y == cls.STEP_2S1E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_2S1W_X and step_y == cls.STEP_2S1W_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1S2W_X and step_y == cls.STEP_1S2W_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1N2W_X and step_y == cls.STEP_1N2W_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_2N1W_X and step_y == cls.STEP_2N1W_Y):
            return cls.DIRS['valid']
        else:
            return cls.DIRS['undefined']

    #step_for_dir(direction):
        # not used for knight

    def is_piece_trapped(self):
        return False # knight cannot be trapped

    #is_piece_stuck_new(self):
        # works with inherited class

    def is_move_stuck(self, dstx, dsty):
        return False # not used for knight

    def is_move_valid(self, dstx, dsty):
        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == self.match.DIRS['undefined']):
            return False

        pin_dir = self.match.evaluate_pin_dir(self.xpos, self.ypos) #self.color, 
        if(pin_dir != self.match.DIRS['undefined']):
            return False

        dstpiece = self.match.readfield(dstx, dsty)
        if(self.match.color_of_piece(dstpiece) == self.color):
            return False

        return True

    def find_attacks_and_supports(self, dstx, dsty, attacked, supported):
        from .. analyze_helper import field_touches_beyond

        cknight = cKnight(self.match, dstx, dsty)
        if(cknight.is_piece_stuck_new()):
            return

        opp_color =  self.match.oppcolor_of_piece(self.piece)
        for step in self.STEPS:
            x1 = dstx + step[0]
            y1 = dsty + step[1]
            if(self.match.is_inbounds(x1, y1)):
                if(x1 == self.xpos and y1 == self.ypos):
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

    def move_defends_forked_field(self, dstx, dsty):
        from .. analyze_helper import is_field_forked

        if(self.is_move_stuck(dstx, dsty)):
            return False

        for step in self.STEPS:
            x1 = dstx + step[0]
            y1 = dsty + step[1]

            if(x1 == self.xpos and y1 == self.ypos):
                continue

            if(self.match.is_inbounds(x1, y1)):
                piece = self.match.readfield(x1, y1)

                if(self.match.color_of_piece(piece) == self.color):
                    if(is_field_forked(self.match, piece, x1, y1)):
                        #cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                        #analyses.lst_fork_defended.append(cfork)
                        return True

        return False

    def move_controles_file(self, dstx, dsty):
        return False
    
# class end

