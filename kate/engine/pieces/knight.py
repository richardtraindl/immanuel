from . piece import cPiece


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

# class end

