from .match import *
from .validator import *
from .move import GenMove, PrioMove


class cGenerator:
    ROOK_GEN_STEPS = [ [[0, 1, cMatch.PIECES['blk']], [0, 2, cMatch.PIECES['blk']], [0, 3, cMatch.PIECES['blk']], [0, 4, cMatch.PIECES['blk']], [0, 5, cMatch.PIECES['blk']], [0, 6, cMatch.PIECES['blk']], [0, 7, cMatch.PIECES['blk']]],
                       [[0, -1, cMatch.PIECES['blk']], [0, -2, cMatch.PIECES['blk']], [0, -3, cMatch.PIECES['blk']], [0, -4, cMatch.PIECES['blk']], [0, -5, cMatch.PIECES['blk']], [0, -6, cMatch.PIECES['blk']], [0, -7, cMatch.PIECES['blk']]],
                       [[1, 0, cMatch.PIECES['blk']], [2, 0, cMatch.PIECES['blk']], [3, 0, cMatch.PIECES['blk']], [4, 0, cMatch.PIECES['blk']], [5, 0, cMatch.PIECES['blk']], [6, 0, cMatch.PIECES['blk']], [7, 0, cMatch.PIECES['blk']]],
                       [[-1, 0, cMatch.PIECES['blk']], [-2, 0, cMatch.PIECES['blk']], [-3, 0, cMatch.PIECES['blk']], [-4, 0, cMatch.PIECES['blk']], [-5, 0, cMatch.PIECES['blk']], [-6, 0, cMatch.PIECES['blk']], [-7, 0, cMatch.PIECES['blk']]] ]

    BISHOP_GEN_STEPS = [ [[1, 1, cMatch.PIECES['blk']], [2, 2, cMatch.PIECES['blk']], [3, 3, cMatch.PIECES['blk']], [4, 4, cMatch.PIECES['blk']], [5, 5, cMatch.PIECES['blk']], [6, 6, cMatch.PIECES['blk']], [7, 7, cMatch.PIECES['blk']]],
                         [[-1, -1, cMatch.PIECES['blk']], [-2, -2, cMatch.PIECES['blk']], [-3, -3, cMatch.PIECES['blk']], [-4, -4, cMatch.PIECES['blk']], [-5, -5, cMatch.PIECES['blk']], [-6, -6, cMatch.PIECES['blk']], [-7, -7, cMatch.PIECES['blk']]],
                         [[1, -1, cMatch.PIECES['blk']], [2, -2, cMatch.PIECES['blk']], [3, -3, cMatch.PIECES['blk']], [4, -4, cMatch.PIECES['blk']], [5, -5, cMatch.PIECES['blk']], [6, -6, cMatch.PIECES['blk']], [7, -7, cMatch.PIECES['blk']]],
                         [[-1, 1, cMatch.PIECES['blk']], [-2, 2, cMatch.PIECES['blk']], [-3, 3, cMatch.PIECES['blk']], [-4, 4, cMatch.PIECES['blk']], [-5, 5, cMatch.PIECES['blk']], [-6, 6, cMatch.PIECES['blk']], [-7, 7, cMatch.PIECES['blk']]] ]

    KING_GEN_STEPS = [ [[0, 1, cMatch.PIECES['blk']]],
                       [[1, 1, cMatch.PIECES['blk']]],
                       [[1, 0, cMatch.PIECES['blk']]], 
                       [[1, -1, cMatch.PIECES['blk']]],
                       [[0, -1, cMatch.PIECES['blk']]], 
                       [[-1, -1, cMatch.PIECES['blk']]],
                       [[-1, 0, cMatch.PIECES['blk']]],
                       [[-1, 1, cMatch.PIECES['blk']]],
                       [[2, 0, cMatch.PIECES['blk']]],
                       [[-2, 0, cMatch.PIECES['blk']]] ]

    KNIGHT_GEN_STEPS = [ [[1, 2, cMatch.PIECES['blk']]],
                         [[2, 1, cMatch.PIECES['blk']]],
                         [[2, -1, cMatch.PIECES['blk']]], 
                         [[1, -2, cMatch.PIECES['blk']]],
                         [[-1, -2, cMatch.PIECES['blk']]],
                         [[-2, -1, cMatch.PIECES['blk']]],
                         [[-2, 1, cMatch.PIECES['blk']]],
                         [[-1, 2, cMatch.PIECES['blk']]] ]

    WPAWN_GEN_STEPS = [ [[0, 1, cMatch.PIECES['blk']]],
                        [[0, 2, cMatch.PIECES['blk']]],
                        [[1, 1, cMatch.PIECES['blk']]], 
                        [[-1, 1, cMatch.PIECES['blk']]] ]

    WPROM_GEN_STEPS = [ [[0, 1, cMatch.PIECES['wQu']], [1, 1, cMatch.PIECES['wQu']], [-1, 1, cMatch.PIECES['wQu']], [0, 1, cMatch.PIECES['wRk']]],
                        [[1, 1, cMatch.PIECES['wRk']], [-1, 1, cMatch.PIECES['wRk']], [0, 1, cMatch.PIECES['wBp']], [1, 1, cMatch.PIECES['wBp']]],
                        [[-1, 1, cMatch.PIECES['wBp']], [0, 1, cMatch.PIECES['wKn']], [1, 1, cMatch.PIECES['wKn']], [-1, 1, cMatch.PIECES['wKn']]] ]

    BPAWN_GEN_STEPS = [ [[0, -1, cMatch.PIECES['blk']]],
                        [[0, -2, cMatch.PIECES['blk']]],
                        [[-1, -1, cMatch.PIECES['blk']]], 
                        [[1, -1, cMatch.PIECES['blk']]] ]

    BPROM_GEN_STEPS = [ [[0, -1, cMatch.PIECES['bQu']], [0, -1, cMatch.PIECES['bRk']], [0, -1, cMatch.PIECES['bBp']], [0, -1, cMatch.PIECES['bKn']]],
                        [[1, -1, cMatch.PIECES['bQu']], [1, -1, cMatch.PIECES['bRk']], [1, -1, cMatch.PIECES['bBp']], [1, -1, cMatch.PIECES['bKn']]],
                        [[-1, -1, cMatch.PIECES['bQu']], [-1, -1, cMatch.PIECES['bRk']], [-1, -1, cMatch.PIECES['bBp']], [-1, -1, cMatch.PIECES['bKn']]] ]

    QUEEN_GEN_STEPS = [ [[0, 1, cMatch.PIECES['blk']], [0, 2, cMatch.PIECES['blk']], [0, 3, cMatch.PIECES['blk']], [0, 4, cMatch.PIECES['blk']], [0, 5, cMatch.PIECES['blk']], [0, 6, cMatch.PIECES['blk']], [0, 7, cMatch.PIECES['blk']]],
                        [[0, -1, cMatch.PIECES['blk']], [0, -2, cMatch.PIECES['blk']], [0, -3, cMatch.PIECES['blk']], [0, -4, cMatch.PIECES['blk']], [0, -5, cMatch.PIECES['blk']], [0, -6, cMatch.PIECES['blk']], [0, -7, cMatch.PIECES['blk']]],
                        [[1, 0, cMatch.PIECES['blk']], [2, 0, cMatch.PIECES['blk']], [3, 0, cMatch.PIECES['blk']], [4, 0, cMatch.PIECES['blk']], [5, 0, cMatch.PIECES['blk']], [6, 0, cMatch.PIECES['blk']], [7, 0, cMatch.PIECES['blk']]],
                        [[-1, 0, cMatch.PIECES['blk']], [-2, 0, cMatch.PIECES['blk']], [-3, 0, cMatch.PIECES['blk']], [-4, 0, cMatch.PIECES['blk']], [-5, 0, cMatch.PIECES['blk']], [-6, 0, cMatch.PIECES['blk']], [-7, 0, cMatch.PIECES['blk']]],
                        [[1, 1, cMatch.PIECES['blk']], [2, 2, cMatch.PIECES['blk']], [3, 3, cMatch.PIECES['blk']], [4, 4, cMatch.PIECES['blk']], [5, 5, cMatch.PIECES['blk']], [6, 6, cMatch.PIECES['blk']], [7, 7, cMatch.PIECES['blk']]],
                        [[-1, -1, cMatch.PIECES['blk']], [-2, -2, cMatch.PIECES['blk']], [-3, -3, cMatch.PIECES['blk']], [-4, -4, cMatch.PIECES['blk']], [-5, -5, cMatch.PIECES['blk']], [-6, -6, cMatch.PIECES['blk']], [-7, -7, cMatch.PIECES['blk']]],
                        [[1, -1, cMatch.PIECES['blk']], [2, -2, cMatch.PIECES['blk']], [3, -3, cMatch.PIECES['blk']], [4, -4, cMatch.PIECES['blk']], [5, -5, cMatch.PIECES['blk']], [6, -6, cMatch.PIECES['blk']], [7, -7, cMatch.PIECES['blk']]],
                        [[-1, 1, cMatch.PIECES['blk']], [-2, 2, cMatch.PIECES['blk']], [-3, 3, cMatch.PIECES['blk']], [-4, 4, cMatch.PIECES['blk']], [-5, 5, cMatch.PIECES['blk']], [-6, 6, cMatch.PIECES['blk']], [-7, 7, cMatch.PIECES['blk']]] ]

    def __init__(self, match):
        self.match = match

    @staticmethod
    def read_steps(steps, dir_idx, step_idx):
        stepx = steps[dir_idx][step_idx][0]
        stepy = steps[dir_idx][step_idx][1]
        prom_piece = steps[dir_idx][step_idx][2]
        return stepx, stepy, prom_piece

    def generate_moves(self):
        color = self.match.next_color()
        priomoves = []

        for y in range(0, 8, 1):
            for x in range(0, 8, 1):
                piece = self.match.readfield(x, y)
                if(piece == self.match.PIECES['blk'] or color != self.match.color_of_piece(piece)):
                    continue
                else:
                    dir_idx = 0
                    step_idx = 0
                    if(piece == self.match.PIECES['wPw']):
                        if(y < 6):
                            steps = self.WPAWN_GEN_STEPS
                            max_dir = 4
                            max_step = 1
                        else:
                            steps = self.WPROM_GEN_STEPS
                            max_dir = 3
                            max_step = 4
                    elif(piece == self.match.PIECES['bPw']):
                        if(y > 1):
                            steps = self.BPAWN_GEN_STEPS
                            max_dir = 4
                            max_step = 1
                        else:
                            steps = self.BPROM_GEN_STEPS
                            max_dir = 3
                            max_step = 4
                    elif(piece == self.match.PIECES['wRk'] or piece == self.match.PIECES['bRk']):
                        steps = self.ROOK_GEN_STEPS
                        max_dir = 4
                        max_step = 7
                    elif(piece == self.match.PIECES['wBp'] or piece == self.match.PIECES['bBp']):
                        steps = self.BISHOP_GEN_STEPS
                        max_dir = 4
                        max_step = 7
                    elif(piece == self.match.PIECES['wKn'] or piece == self.match.PIECES['bKn']):
                        steps = self.KNIGHT_GEN_STEPS
                        max_dir = 8
                        max_step = 1
                    elif(piece == self.match.PIECES['wQu'] or piece == self.match.PIECES['bQu']):
                        steps = self.QUEEN_GEN_STEPS
                        max_dir = 8
                        max_step = 7
                    else:
                        steps = self.KING_GEN_STEPS
                        max_dir = 10
                        max_step = 1

                for dir_idx in range(0, max_dir, 1):
                    for step_idx in range(0, max_step, 1):
                        stepx, stepy, prom_piece = self.read_steps(steps, dir_idx, step_idx)
                        dstx = x + stepx
                        dsty = y + stepy
                        flag, errmsg = self.match.is_move_valid(x, y, dstx, dsty, prom_piece)
                        if(flag):
                            if(self.match.readfield(dstx, dsty) != self.match.PIECES['blk']):
                                captures = True
                            else:
                                captures = False
                            gmove = GenMove(x, y, dstx, dsty, prom_piece, captures)
                            priomove = PrioMove(gmove)
                            priomoves.append(priomove)
                        elif(errmsg != cValidator.RETURN_CODES['king-error']):
                            break

        return priomoves
# class end


