from kate.models import Match, Move
from kate.modules import helper, rules, openings, calc_helper, debug
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
             [[1, 1]],
             [[1, 0]], 
             [[1, -1]],
             [[0, -1]], 
             [[-1, -1]],
             [[-1, 0]],
             [[-1, 1]],
             [[2, 0]],
             [[-2, 0]] ]


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


def prnt_move(msg, move):
    print(msg + 
        Match.index_to_koord(move.srcx, move.srcy) + " " +
        Match.index_to_koord(move.dstx, move.dsty) + " " +
        helper.reverse_lookup(Match.PIECES, move.prom_piece), end="")


class GenMove(object):
    def __init__(self, srcx=None, srcy=None, dstx=None, dsty=None, prom_piece=None):
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.prom_piece = prom_piece


class Generator(object):
    def __init__(self, match=None, active=True, steps=None, board_x=0, board_y=0, dir_idx=0, max_dir=0, step_idx=0, max_step=0, opening_cnt=0):
        self.match = match
        self.active = active
        self.steps = steps
        self.board_x = board_x
        self.board_y = board_y
        self.dir_idx = dir_idx
        self.max_dir = max_dir
        self.step_idx = step_idx
        self.max_step = max_step
        self.opening_cnt = opening_cnt

    def read_steps(self):
        stepx = self.steps[self.dir_idx][self.step_idx][0]
        stepy = self.steps[self.dir_idx][self.step_idx][1]
        if( len(self.steps[self.dir_idx][self.step_idx]) == 3):
            prom_piece = self.steps[self.dir_idx][self.step_idx][2]
        else:
            prom_piece = Match.PIECES['blk']
        return stepx, stepy, prom_piece

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
                self.active = False
                return False
        return True

    def generate_move(self):
        gmove = GenMove()
        color = self.match.next_color()

        while(self.active):
            if(self.steps == None):
                piece = self.match.readfield(self.board_x, self.board_y)
                if(piece == Match.PIECES['blk'] or color != Match.color_of_piece(piece)):
                    if(self.rotate_field()):
                        continue
                    else:
                        return False, gmove
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
            if(flag):
                gmove = GenMove(self.board_x, self.board_y, dstx, dsty, prom_piece)
                self.rotate()
                return True, gmove
            else:
                if(errmsg == rules.ERROR_CODES['king-error']):
                    self.rotate()
                else:
                    if(self.rotate_dir() == False):
                        return False, gmove
        return False, gmove


class immanuelsThread(threading.Thread):
    def __init__(self, name, match):
        threading.Thread.__init__(self)
        self.name = name
        self.match = copy.deepcopy(match)
        self.candidate_srcx = None
        self.candidate_srcy = None
        self.candidate_dstx = None
        self.candidate_dsty = None
        self.candidate_prom_piece = None
        Match.remove_outdated_threads(match)
        Match.add_thread(self)

    def run(self):
        print("Starting " + str(self.name))
        move = Move.objects.filter(match_id=self.match.id).order_by("count").last()
        if(move != None):
            self.match.move_list.append(move)

        if(self.match.level == Match.LEVEL['low']):
            maxdepth = 1
        elif(self.match.level == Match.LEVEL['medium']):
            maxdepth = 2
        elif(self.match.level == Match.LEVEL['high']):
            maxdepth = 3
        else:
            # professional
            maxdepth = 4

        gmove = calc_move(self.match, maxdepth)
        if(gmove != None):
            curr_match = Match.objects.get(id=self.match.id)
            if(curr_match.count == self.match.count and Match.does_thread_exist(self)):
                move = self.match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
                move.save()
                self.match.save()
                print("move saved")
            else:
                print("thread outdated - move dropped")

        return gmove

    def populate_candiate(self, gmove):
        if(gmove):
            self.candidate_srcx = gmove.srcx
            self.candidate_srcy = gmove.srcy
            self.candidate_dstx = gmove.dstx
            self.candidate_dsty = gmove.dsty
            self.candidate_prom_piece = gmove.prom_piece


def rate(color, gmove, newgmove, score, newscore):
    if((color == Match.COLORS['white'] and score < newscore) or 
       (color == Match.COLORS['black'] and score > newscore)):
        return newscore, newgmove
    else:
        return score, gmove


def calc_max(match, maxdepth, depth, alpha, beta):
    generator = Generator()
    generator.match = match
    gmove = None
    color = match.next_color()
    newscore = None
    maxscore = -200000
    oldscore = 0
    count = 0

    while(generator.active):
        flag, newgmove = generator.generate_move()
        if(flag):
            count += 1
            oldscore = match.score
            move = match.do_move(newgmove.srcx, newgmove.srcy, newgmove.dstx, newgmove.dsty, newgmove.prom_piece)
            match.move_list.append(move)
            if(depth == 1):
                msg = "\nmatch.id:" + str(match.id) + " calculate "
                prnt_move(msg, newgmove)
                if(gmove):
                    prnt_move(" CANDIDATE ", gmove)
                    print(" score: " + str(newscore))
                    thread = Match.get_active_thread(match)
                    if(thread and newscore):
                        thread.populate_candiate(gmove)

            if(depth <= maxdepth):
                newscore = calc_min(match, maxdepth, depth + 1, maxscore, beta)[0]
            elif(depth <= maxdepth + 2):
                wkg_attacked = rules.attacked(match, match.wKg_x, match.wKg_y, Match.COLORS['black'])
                bkg_attacked = rules.attacked(match, match.bKg_x, match.bKg_y, Match.COLORS['white'])

                white_promotion = match.readfield(newgmove.dstx, newgmove.dsty) == Match.PIECES['wPw'] and newgmove.dsty >= 6
                black_promotion = match.readfield(newgmove.dstx, newgmove.dsty) == Match.PIECES['bPw'] and newgmove.dsty <= 1

                if(oldscore != match.score or wkg_attacked or bkg_attacked or white_promotion or black_promotion):
                    newscore = calc_min(match, maxdepth, depth + 1, maxscore, beta)[0]
                else:
                    newscore = match.score + calc_helper.evaluate_position(match)
            elif(depth <= maxdepth + 4 and oldscore != match.score):
                newscore = calc_min(match, maxdepth, depth + 1, maxscore, beta)[0]
            else:
                newscore = match.score + calc_helper.evaluate_position(match)

            newscore, gmove = rate(color, gmove, newgmove, maxscore, newscore)
            match.undo_move(True)
            if(newscore > maxscore):
                maxscore = newscore
                if(maxscore >= beta):
                    break
        else:
            if(count == 0):
                status = rules.game_status(match)
                if(status == Match.STATUS['winner_black']):
                    newscore = Match.SCORES[Match.PIECES['wKg']]
                elif(status == Match.STATUS['winner_white']):
                    newscore = Match.SCORES[Match.PIECES['bKg']]
                elif(status == Match.STATUS['draw']):
                    newscore = Match.SCORES[Match.PIECES['blk']]
                else:
                    newscore = match.score

                if(depth == 1):
                    msg = "\nmatch.id:" + str(match.id) + " CANDIDATE "
                    prnt_move(msg, gmove)
                    print(" score: " + str(newscore))
                    thread = Match.get_active_thread(match)
                    if(thread):
                        thread.populate_candiate(gmove)
                return newscore, gmove

    return maxscore, gmove


def calc_min(match, maxdepth, depth, alpha, beta):
    generator = Generator()
    generator.match = match
    gmove = None
    color = match.next_color()
    newscore = None
    minscore = 200000
    oldscore = 0
    count = 0

    while(generator.active):
        flag, newgmove = generator.generate_move()

        if(flag):
            count += 1
            oldscore = match.score
            move = match.do_move(newgmove.srcx, newgmove.srcy, newgmove.dstx, newgmove.dsty, newgmove.prom_piece)
            match.move_list.append(move)
            if(depth == 1):
                msg = "\nmatch.id:" + str(match.id) + " calculate "
                prnt_move(msg, newgmove)
                if(gmove):
                    prnt_move(" CANDIDATE ", gmove)
                    print(" score: " + str(newscore))
                    thread = Match.get_active_thread(match)
                    if(thread and newscore):
                        thread.populate_candiate(gmove)

            if(depth <= maxdepth):
                newscore = calc_max(match, maxdepth, depth + 1, alpha, minscore)[0]
            elif(depth <= maxdepth + 2):
                wkg_attacked = rules.attacked(match, match.wKg_x, match.wKg_y, Match.COLORS['black'])
                bkg_attacked = rules.attacked(match, match.bKg_x, match.bKg_y, Match.COLORS['white'])

                white_promotion = match.readfield(newgmove.dstx, newgmove.dsty) == Match.PIECES['wPw'] and newgmove.dsty >= 6
                black_promotion = match.readfield(newgmove.dstx, newgmove.dsty) == Match.PIECES['bPw'] and newgmove.dsty <= 1

                if(oldscore != match.score or wkg_attacked or bkg_attacked or white_promotion or black_promotion):
                    newscore = calc_max(match, maxdepth, depth + 1, alpha, minscore)[0]
                else:
                    newscore = match.score + calc_helper.evaluate_position(match)
            elif(depth <= maxdepth + 4 and oldscore != match.score):
                newscore = calc_max(match, maxdepth, depth + 1, alpha, minscore)[0]
            else:
                newscore = match.score + calc_helper.evaluate_position(match)

            newscore, gmove = rate(color, gmove, newgmove, minscore, newscore)
            match.undo_move(True)
            if(newscore < minscore):
                minscore = newscore
                if(minscore <= alpha):
                    break
        else:
            if(count == 0):
                status = rules.game_status(match)
                if(status == Match.STATUS['winner_black']):
                    newscore = Match.SCORES[Match.PIECES['wKg']]
                elif(status == Match.STATUS['winner_white']):
                    newscore = Match.SCORES[Match.PIECES['bKg']]
                elif(status == Match.STATUS['draw']):
                    newscore = Match.SCORES[Match.PIECES['blk']]
                else:
                    newscore = match.score

                if(depth == 1):
                    msg = "\nmatch.id:" + str(match.id) + " CANDIDATE "
                    prnt_move(msg, gmove)
                    print(" score: " + str(newscore))
                    thread = Match.get_active_thread(match)
                    if(thread):
                        thread.populate_candiate(gmove)
                return newscore, gmove

    return minscore, gmove


def calc_move(match, maxdepth):
    gmove = openings.retrieve_move(match)

    if(gmove):
        score = match.score
    elif(match.next_color() == Match.COLORS['white']):
        score, gmove = calc_max(match, maxdepth, 1, -200000, 200000)
    else:
        score, gmove = calc_min(match, maxdepth, 1, -200000, 200000)

    if(gmove != None):
        msg = "\nresult: " + str(score) + " match.id: " + str(match.id) + " "
        prnt_move(msg, gmove)
        print("")
    else:
        print("no results found!!!" + str(score))
    return gmove


def thread_do_move(match):
    thread = immanuelsThread("immanuel-" + str(random.randint(0, 100000)), match)
    thread.start()


