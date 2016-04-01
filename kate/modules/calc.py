from kate.models import Match, Move
from kate.modules import values, rules
import random, threading, copy, time


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


class GenMove(object):
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
        gmove = GenMove()
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
                gmove = GenMove(self.board_x, self.board_y, dstx, dsty, prom_piece)
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
    gmove_list = []

    while(True):
        flag, gmove = generator.generate_move()
        if(flag == True):
            gmove_list.append(gmove)
        else:
            break

    count = len(gmove_list)
    if(count == 0):
        return False, gmove

    count = random.randint(0, count - 1)
    print(values.index_to_koord(gmove_list[count].srcx, gmove_list[count].srcy) + " " + \
          values.index_to_koord(gmove_list[count].dstx, gmove_list[count].dsty) + " " + \
          str(gmove_list[count].prom_piece))
    return True, gmove_list[count]


class immanuelsThread1(threading.Thread):
    def __init__(self, threadID, match, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.match = copy.copy(match)
        print(str(self.match.wKg_x) + " "  + 
              str(self.match.wKg_y) + " "  + 
              str(self.match.wKg_first_movecnt) + " "  + 
              str(self.match.wRk_a1_first_movecnt) + " "  + 
              str(self.match.wRk_h1_first_movecnt))

        move = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(move != None):
            self.match.move_list.append(move)
        self.delay = delay

    def run(self):
        print("Starting " + str(self.threadID))
        time.sleep(self.delay)
        flag, gmove = random_move(self.match)
        if(flag):
            move = self.match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
            move.save()
            self.match.save()


def do_random_move(match, delay):
    thread = immanuelsThread1(2, match, delay)
    thread.start()


class immanuelsThread(threading.Thread):
    def __init__(self, threadID, match, depth, delay):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.match = copy.copy(match)
        move = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(move != None):
            self.match.move_list.append(move)
        self.depth = depth
        self.delay = delay

    def run(self):
        print("Starting " + str(self.threadID))
        print(str(self.match.wKg_x) + " "  + 
              str(self.match.wKg_y) + " "  + 
              str(self.match.wKg_first_movecnt) + " "  + 
              str(self.match.wRk_a1_first_movecnt) + " "  + 
              str(self.match.wRk_h1_first_movecnt))
        time.sleep(self.delay)
        gmove = calc_move(self.match, self.depth)
        if(gmove != None):
            move = self.match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
            move.save()
            self.match.save()
            print("move saved")


def rate(color, gmove, new_gmove, score, new_score):
    if((color == Match.COLORS['white'] and score < new_score) or 
       (color == Match.COLORS['black'] and score > new_score)):
        return new_score, new_gmove
    else:
        return score, gmove


def calc_node(match, depth):
    generator = Generator()
    generator.match = match 
    color = match.next_color()
    gmove = None
    count = 0

    print(str(color) + " -------- ")

    if(color == Match.COLORS['white']):
        score = -20000
    else:
        score = 20000

    while(True):
        flag, new_gmove = generator.generate_move()
        if(flag == True):
            count += 1
            move = match.do_move(new_gmove.srcx, new_gmove.srcy, new_gmove.dstx, new_gmove.dsty, new_gmove.prom_piece)
            match.move_list.append(move)

            if(depth > 1):
                new_score, calc_move = calc_node(match, depth - 1)
            else:
                new_score = match.score

            score, gmove = rate(color, gmove, new_gmove, score, new_score)

            match.undo_move(True)
        else:
            break

    if(count == 0):
        status = rules.game_status(match)
        gmove = None
        if(status == Match.STATUS['winner_black']):
            score = Match.SCORES['wKg']
        elif(status == Match.STATUS['winner_white']):
            score = Match.SCORES['bKg']
        elif(status == Match.STATUS['draw']):
            score = Match.SCORES['blk']
        else:
            score = match.score

    return score, gmove


def calc_move(match, depth):
    #if(match.next_color() == Match.COLORS['white']):
    #    alpha = -20000
    #    beta = 20000
    #else:
    #    alpha = 20000
    #    beta = -20000

    score, gmove = calc_node(match, depth)

    if(gmove != None):
        print("result: " + str(score))
        print(str(gmove.srcx) + " " + str(gmove.srcy)  + " " + str(gmove.dstx)  + " " +  str(gmove.dsty)  + " " + str(gmove.prom_piece))
              #values.index_to_koord(gmove.srcx, gmove.srcy) + " " + 
              # values.index_to_koord(gmove.dstx, gmove.dsty) + " " + "blk")
              # values.reverse_lookup(Match.PIECES, gmove.prom_piece))
    else:
        print("no results found!!!" + str(score))
    
    return gmove


def do_move(match, depth, delay):
    thread = immanuelsThread(1, match, depth, delay)
    thread.start()

