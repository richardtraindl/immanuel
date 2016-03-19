from kate.models import Match, Move
from kate.modules import values, rules
import random


RK_STEPS = [ [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
          [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
          [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
          [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]] ]


BP_STEPS = [ [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
             [[-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]],
             [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
             [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]] ]


QU_STEPS = [ [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7]],
             [[0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]],
             [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0]],
             [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0]],
             [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]],
             [[-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]],
             [[1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7]],
             [[-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7]] ]


KN_STEPS = [ [[1, 2]],
             [[2, 1]],
             [[2, -1]], 
             [[1, -2]],
             [[-1, -2]],
             [[-2, -1]],
             [[-2, 1]],
             [[-1, 2]] ]


KG_STEPS = [ [[0, 1]],
             [[0, 2]],
             [[0, 3]], 
             [[0, 4]],
             [[0, 5]], 
             [[0, 6]],
             [[0, 6]],
             [[0, 6]],
             [[0, 6]],
             [[0, 7]] ]


WPW_STEPS = [ [[0, 1]],
              [[0, 2]],
              [[1, 1]], 
              [[-1, 1]] ]

WPROM_STEPS = [ [[0, 1, Match.PIECES['wQu']], [1, 1, Match.PIECES['wQu']], [-1, 1, Match.PIECES['wQu']], [0, 1, Match.PIECES['wRk']]],
                [[1, 1, Match.PIECES['wRk']], [-1, 1, Match.PIECES['wRk']], [0, 1, Match.PIECES['wBp']], [1, 1, Match.PIECES['wBp']]],
                [[-1, 1, Match.PIECES['wBp']], [0, 1, Match.PIECES['wKn']], [1, 1, Match.PIECES['wKn']], [-1, 1, Match.PIECES['wKn']]] ]


BPW_STEPS = [ [[0, -1]],
              [[0, -2]],
              [[-1, -1]], 
              [[1, -1]] ]

BPROM_STEPS = [ [[0, -1, Match.PIECES['bQu']], [0, -1, Match.PIECES['bRk']], [0, -1, Match.PIECES['bBp']], [0, -1, Match.PIECES['bKn']]],
                [[1, -1, Match.PIECES['bQu']], [1, -1, Match.PIECES['bRk']], [1, -1, Match.PIECES['bBp']], [1, -1, Match.PIECES['bKn']]],
                [[-1, -1, Match.PIECES['bQu']], [-1, -1, Match.PIECES['bRk']], [-1, -1, Match.PIECES['bBp']], [-1, -1, Match.PIECES['bKn']]] ]


class genmove(object):
    def __init__(self, srcx=None, srcy=None, dstx=None, dsty=None, prom_piece=None):
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.prom_piece = prom_piece


class Generator(object):
    def __init__(self, match=None, steps=None, board_x=0, board_y=0, dir_idx=0, max_dir=0, step_idx=0, max_step=0):
        self.match = match
        self.steps = steps
        self.board_x = board_x
        self.board_y = board_y
        self.dir_idx = dir_idx
        self.max_dir = max_dir
        self.step_idx = step_idx
        self.max_step = max_step

    def read_steps(self):
        stepx = self.steps[self.dir_idx][self.step_idx][0]
        stepy = self.steps[self.dir_idx][self.step_idx][1]
        if( len(self.steps[self.dir_idx][self.step_idx]) == 3):
            print("llllllllll")
            prom_piece = self.steps[self.dir_idx][self.step_idx][2]
        else:
            prom_piece = Match.PIECES['blk']
        return stepx, stepy, prom_piece


    def rotate_field(self):
        self.steps = None

        if(self.board_x < 7):
            self.board_x += 1
        else:
            self.board_x = 0

            if(self.board_y < 7):
                self.board_y += 1
            else:
                self.board_y = 0
                return False
        return True


    def rotate(self):
        if(self.step_idx + 1 < self.max_step):
            self.step_idx += 1
        else:
            self.step_idx = 0

            if(self.dir_idx + 1 < self.max_dir):
                self.dir_idx += 1
            else:
                self.dir_idx = 0
                return self.rotate_field()
        return True


    def rotate_dir(self):
            self.step_idx = 0

            if(self.dir_idx + 1 < self.max_dir):
                self.dir_idx += 1
                return True
            else:
                self.dir_idx = 0
                return self.rotate_field()


    def generate_move(self):
        gmove = genmove()
        color = self.match.next_color()
        
        while(True):
            if(self.steps == None):
                piece = self.match.readfield(self.board_x, self.board_y)
                if(piece == Match.PIECES['blk'] or color != Match.color_of_piece(piece)):
                    if(self.rotate_field()):
                        continue
                    else:
                        break
                else:
                    if(piece == Match.PIECES['wPw']):
                        if(self.board_y < 6):
                            self.steps = WPW_STEPS
                            self.dir_idx = 0
                            self.max_dir = 4
                            self.step_idx = 0
                            self.max_step = 1
                        else:
                            self.steps = WPROM_STEPS
                            self.dir_idx = 0
                            self.max_dir = 3
                            self.step_idx = 0
                            self.max_step = 4
                    elif(piece == Match.PIECES['bPw']):
                        if(self.board_y > 1):
                            self.steps = BPW_STEPS
                            self.dir_idx = 0
                            self.max_dir = 4
                            self.step_idx = 0
                            self.max_step = 1
                        else:
                            self.steps = BPROM_STEPS
                            self.dir_idx = 0
                            self.max_dir = 3
                            self.step_idx = 0
                            self.max_step = 4
                    elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
                        self.steps = RK_STEPS
                        self.dir_idx = 0
                        self.max_dir = 4
                        self.step_idx = 0
                        self.max_step = 7
                    elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
                        self.steps = BP_STEPS
                        self.dir_idx = 0
                        self.max_dir = 4
                        self.step_idx = 0
                        self.max_step = 7
                    elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
                        self.steps = KN_STEPS
                        self.dir_idx = 0
                        self.max_dir = 8
                        self.step_idx = 0
                        self.max_step = 1
                    elif(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
                        self.steps = QU_STEPS
                        self.dir_idx = 0
                        self.max_dir = 8
                        self.step_idx = 0
                        self.max_step = 7
                    else:
                        self.steps = KG_STEPS
                        self.dir_idx = 0
                        self.max_dir = 10
                        self.step_idx = 0
                        self.max_step = 1

            stepx, stepy, prom_piece = self.read_steps()
            dstx = self.board_x + stepx
            dsty = self.board_y + stepy
            flag, errmsg = rules.is_move_valid(self.match, self.board_x, self.board_y, dstx, dsty, prom_piece)
            if(flag == True):
                # print("OK: " + str(self.board_x) + " " + str(self.board_y) + " " + str(dstx) + " " + str(dsty))
                gmove = genmove(self.board_x, self.board_y, dstx, dsty, prom_piece)
                self.rotate()
                return True, gmove
            else:
                # print("NOK: " + str(self.board_x) + " " + str(self.board_y) + " " + str(dstx) + " " + str(dsty))
                # print(rules.ERROR_MSGS[errmsg])
                if(self.rotate_dir() == False):
                    break

        return False, gmove


def random_move(match):
    generator = Generator()
    generator.match = match
    # gmove = genmove()
    flag, gmove = generator.generate_move()
    rand_flag = False
    count = random.randint(0, 9)
    for i in range(count):
        rand_flag, rand_gmove = generator.generate_move()
    if(rand_flag):
        return rand_flag, rand_gmove
    elif(flag):
        return flag, gmove
    else:
        return False, gmove
