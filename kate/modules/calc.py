from kate.models import Match, Move
from kate.modules import values, rules


ROOK_GEN = [ [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
             [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
             [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
             [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]] ]

BISHOP_GEN = [ [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
               [[-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]],
               [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
               [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]] ]

QUEEN_GEN = [ [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
              [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
              [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
              [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]] ]
              [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
              [[-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]],
              [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
              [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]] ]

KNIGHT_GEN = [ [[0, 1]],
               [[0, 2]],
               [[0, 3]], 
               [[0, 4]],
               [[0, 5]],
               [[0, 6]],
               [[0, 6]],
               [[0, 7]] ]

KING_GEN = [ [[0, 1]],
             [[0, 2]],
             [[0, 3]], 
             [[0, 4]],
             [[0, 5]], 
             [[0, 6]],
             [[0, 6]],
             [[0, 6]],
             [[0, 6]],
             [[0, 7]] ]

WPAWN_GEN = [ [[0, 1, Match.PIECES['blk']]],
              [[0, 2, Match.PIECES['blk']]],
              [[1, 1, Match.PIECES['blk']]], 
              [[-1, 1, Match.PIECES['blk']]],
              [[0, 1, Match.PIECES['wQu']]],
              [[1, 1, Match.PIECES['wQu']]],
              [[-1, 1, Match.PIECES['wQu']]],
              [[0, 1, Match.PIECES['wRk']]],
              [[1, 1, Match.PIECES['wRk']]],
              [[-1, 1, Match.PIECES['wRk']]],
              [[0, 1, Match.PIECES['wBp']]],
              [[1, 1, Match.PIECES['wBp']]],
              [[-1, 1, Match.PIECES['wBp']]],
              [[0, 1, Match.PIECES['wKn']]],
              [[1, 1, Match.PIECES['wKn']]],
              [[-1, 1, Match.PIECES['wKn']]] ]

BPAWN_GEN = [ [[0, -1, Match.PIECES['blk']]],
              [[0, -2, Match.PIECES['blk']]],
              [[-1, -1, Match.PIECES['blk']]], 
              [[1, -1, Match.PIECES['blk']]],
              [[0, -1, Match.PIECES['bQu']]],
              [[1, -1, Match.PIECES['bQu']]],
              [[-1, -1, Match.PIECES['bQu']]],
              [[0, -1, Match.PIECES['bRk']]],
              [[1, -1, Match.PIECES['bRk']]],
              [[-1, -1, Match.PIECES['bRk']]],
              [[0, -1, Match.PIECES['bBp']]],
              [[1, -1, Match.PIECES['bBp']]],
              [[-1, -1, Match.PIECES['bBp']]],
              [[0, -1, Match.PIECES['bKn']]],
              [[1, -1, Match.PIECES['bKn']]],
              [[-1, -1, Match.PIECES['bKn']]] ]


class Generator(object):
    def __init__(self, board_x=0, board_y=0, direction=0, dir_idx_i=0, dir_idx_j=0, dir_idx_k=0):
        self.board_x = 0
        self.board_y = 0
        self.direction = 0
        self.dir_idx_i = 0
        self.dir_idx_j = 0
        self.dir_idx_k = 0


