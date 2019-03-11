from .. values import *
from . piece import *


class cBishop(cPiece):
    DIRS = { 'north-east' : 5,
             'south-west' : 6,
             'north-west' : 7,
             'south-east' : 8,
             'undefined'  : 14 }
    DIRS_ARY = [DIRS['north-east'], DIRS['south-west'], DIRS['north-west'], DIRS['south-east']]
    REVERSE_DIRS = { DIRS['north-east'] : DIRS['south-west'],
                     DIRS['south-west'] : DIRS['north-east'],
                     DIRS['north-west'] : DIRS['south-east'],
                     DIRS['south-east'] : DIRS['north-west'],
                     DIRS['undefined']  : DIRS['undefined'] }
    STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
    STEP_NEAST_X = 1
    STEP_NEAST_Y = 1
    STEP_SWEST_X = -1
    STEP_SWEST_Y = -1
    STEP_NWEST_X = -1
    STEP_NWEST_Y = 1
    STEP_SEAST_X = 1
    STEP_SEAST_Y = -1
    GEN_STEPS = [ [[1, 1, PIECES['blk']],   [2, 2, PIECES['blk']],   [3, 3, PIECES['blk']],   [4, 4, PIECES['blk']],   [5, 5, PIECES['blk']],   [6, 6, PIECES['blk']],   [7, 7, PIECES['blk']]],
                  [[-1, -1, PIECES['blk']], [-2, -2, PIECES['blk']], [-3, -3, PIECES['blk']], [-4, -4, PIECES['blk']], [-5, -5, PIECES['blk']], [-6, -6, PIECES['blk']], [-7, -7, PIECES['blk']]],
                  [[1, -1, PIECES['blk']],  [2, -2, PIECES['blk']],  [3, -3, PIECES['blk']],  [4, -4, PIECES['blk']],  [5, -5, PIECES['blk']],  [6, -6, PIECES['blk']],  [7, -7, PIECES['blk']]],
                  [[-1, 1, PIECES['blk']],  [-2, 2, PIECES['blk']],  [-3, 3, PIECES['blk']],  [-4, 4, PIECES['blk']],  [-5, 5, PIECES['blk']],  [-6, 6, PIECES['blk']],  [-7, 7, PIECES['blk']]] ]

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        if( (srcx - dstx) == (srcy - dsty) and (srcy < dsty) ):
            return cls.DIRS['north-east']
        elif( (srcx - dstx) == (srcy - dsty) and (srcy > dsty) ):
            return cls.DIRS['south-west']
        elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy < dsty) ):
            return cls.DIRS['north-west']
        elif( (srcx - dstx) == ((srcy - dsty) * -1) and (srcy > dsty) ):
            return cls.DIRS['south-east']
        else:
            return cls.DIRS['undefined']

    @classmethod
    def step_for_dir(cls, direction):
        if(direction == cls.DIRS['north-east']):
            return cls.STEP_NEAST_X, cls.STEP_NEAST_Y
        elif(direction == cls.DIRS['south-west']):
            return cls.STEP_SWEST_X, cls.STEP_SWEST_Y
        elif(direction == cls.DIRS['north-west']):
            return cls.STEP_NWEST_X, cls.STEP_NWEST_Y
        elif(direction == cls.DIRS['south-east']):
            return cls.STEP_SEAST_X, cls.STEP_SEAST_Y
        else:
            return cls.UNDEF_X, cls.UNDEF_Y

    #is_trapped(self)
        # works with inherited class

    #is_piece_stuck(self):
        # works with inherited class
    
    #is_move_stuck(self, srcx, srcy, dstx, dsty)
        # works with inherited class

    #is_move_valid(self, dstx, dsty, prom_piece=PIECES['blk'])
        # works with inherited class

    #do_move(self, dstx, dsty, prom_piece)
        # works with inherited class

    #undo_move(self, move)
        # works with inherited class

    #find_attacks_and_supports(self, attacked, supported):
        # works with inherited class

    #forks(self)
        # works with inherited class

    #defends_fork(self)
        # works with inherited class

    #move_defends_fork(self, dstx, dsty)
        # works with inherited class

    #move_controles_file(self, dstx, dsty)
        # works with inherited class

    #score_touches(self):
        # works with inherited class

    # list_moves(self):
       # works with inherited class

    # generate_moves(self):
       # works with inherited class

    # generate_priomoves(self):
       # works with inherited class

# class end

