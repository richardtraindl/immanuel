from .. values import *
from .piece import *


class cRook(cPiece):
    DIRS = { 'north'     : 1,
             'south'     : 2,
             'east'      : 3,
             'west'      : 4,
             'undefined' : 14 }
    DIRS_ARY = [DIRS['north'], DIRS['south'], DIRS['east'], DIRS['west']]
    REVERSE_DIRS = { DIRS['north']     : DIRS['south'],
                     DIRS['south']     : DIRS['north'],
                     DIRS['east']      : DIRS['west'],
                     DIRS['west']      : DIRS['east'],
                     DIRS['undefined'] : DIRS['undefined'] }
    STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    STEP_NORTH_X = 0
    STEP_NORTH_Y = 1
    STEP_SOUTH_X = 0
    STEP_SOUTH_Y = -1
    STEP_EAST_X = 1
    STEP_EAST_Y = 0
    STEP_WEST_X = -1
    STEP_WEST_Y = 0
    GEN_STEPS = [ [[0, 1, PIECES['blk']],   [0, 2,  PIECES['blk']],  [0, 3,  PIECES['blk']],  [0, 4,  PIECES['blk']],  [0, 5,  PIECES['blk']],  [0, 6,  PIECES['blk']],  [0, 7,  PIECES['blk']]],
                  [[0, -1,  PIECES['blk']], [0, -2,  PIECES['blk']], [0, -3,  PIECES['blk']], [0, -4,  PIECES['blk']], [0, -5,  PIECES['blk']], [0, -6,  PIECES['blk']], [0, -7,  PIECES['blk']]],
                  [[1, 0,  PIECES['blk']],  [2, 0,  PIECES['blk']],  [3, 0,  PIECES['blk']],  [4, 0,  PIECES['blk']],  [5, 0,  PIECES['blk']],  [6, 0,  PIECES['blk']],  [7, 0,  PIECES['blk']]],
                  [[-1, 0,  PIECES['blk']], [-2, 0,  PIECES['blk']], [-3, 0,  PIECES['blk']], [-4, 0,  PIECES['blk']], [-5, 0,  PIECES['blk']], [-6, 0,  PIECES['blk']], [-7, 0,  PIECES['blk']]] ]

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        if( (srcx == dstx) and (srcy < dsty) ):
            return cls.DIRS['north']
        elif( (srcx == dstx) and (srcy > dsty) ):
            return cls.DIRS['south']
        elif( (srcx < dstx) and (srcy == dsty) ):
            return cls.DIRS['east']
        elif( (srcx > dstx) and (srcy == dsty) ):
            return cls.DIRS['west']
        else:
            return cls.DIRS['undefined']

    @classmethod
    def step_for_dir(cls, direction):
        if(direction == cls.DIRS['north']):
            return cls.STEP_NORTH_X, cls.STEP_NORTH_Y
        elif(direction == cls.DIRS['south']):
            return cls.STEP_SOUTH_X, cls.STEP_SOUTH_Y
        elif(direction == cls.DIRS['east']):
            return cls.STEP_EAST_X, cls.STEP_EAST_Y
        elif(direction == cls.DIRS['west']):
            return cls.STEP_WEST_X, cls.STEP_WEST_Y
        else:
            return cls.UNDEF_X, cls.UNDEF_Y

    #is_trapped(self)
        # works with inherited class

    #is_piece_stuck(self):
        # works with inherited class

    #is_move_stuck(self, dstx, dsty)
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

