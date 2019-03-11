from .. values import *
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
    GEN_STEPS = [ [[1, 2, PIECES['blk']]],
                  [[2, 1, PIECES['blk']]],
                  [[2, -1, PIECES['blk']]], 
                  [[1, -2, PIECES['blk']]],
                  [[-1, -2, PIECES['blk']]],
                  [[-2, -1, PIECES['blk']]],
                  [[-2, 1, PIECES['blk']]],
                  [[-1, 2, PIECES['blk']]] ]
    MAXCNT = 1

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

    def is_trapped(self):
        return False # knight cannot be trapped

    #is_piece_stuck(self):
        # works with inherited class

    #is_move_stuck(self, dstx, dsty):
        # works with inherited class

    def is_move_valid(self, dstx, dsty, prom_piece=PIECES['blk']):
        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == self.match.DIRS['undefined']):
            return False

        pin_dir = self.match.eval_pin_dir(self.xpos, self.ypos)
        if(pin_dir != self.match.DIRS['undefined']):
            return False

        dstpiece = self.match.readfield(dstx, dsty)
        if(self.match.color_of_piece(dstpiece) == self.color):
            return False

        return True

    #do_move(self, dstx, dsty, prom_piece)
        # works with inherited class

    #undo_move(self, move)
        # works with inherited class

    #find_attacks_and_supports(self, attacked, supported):
        # works with inherited class

    #forks(self):
        # works with inherited class

    #defends_fork(self)
        # works with inherited class

    #move_defends_fork(self, dstx, dsty)
        # works with inherited class

    def move_controles_file(self, dstx, dsty):
        return False

    # list_moves(self):
       # works with inherited class

    # generate_moves(self):
       # works with inherited class

    # generate_priomoves(self):
       # works with inherited class

# class end

