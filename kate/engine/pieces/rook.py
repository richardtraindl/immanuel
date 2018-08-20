from .piece import *


class cRook(cPiece):
    DIRS = { 'north'     : 1,
             'south'     : 2,
             'east'      : 3,
             'west'      : 4,
             'undefined' : 14 }

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

    #is_piece_trapped(self)
        # works with inherited class

    #is_piece_stuck_new(self):
        # works with inherited class

    #is_move_stuck(self, dstx, dsty)
        # works with inherited class

    #is_move_valid(self, dstx, dsty)
        # works with inherited class

# class end

