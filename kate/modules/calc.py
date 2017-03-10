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
    if(move == None):
        print("no move.....")
    else:
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


def read_steps(steps, dir_idx, step_idx):
    stepx = steps[dir_idx][step_idx][0]
    stepy = steps[dir_idx][step_idx][1]
    if(len(steps[dir_idx][step_idx]) == 3):
        prom_piece = steps[dir_idx][step_idx][2]
    else:
        prom_piece = Match.PIECES['blk']
    return stepx, stepy, prom_piece


def generate_moves(match, gmoves):
    color = match.next_color()
    a_moves = []

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == Match.PIECES['blk'] or color != Match.color_of_piece(piece)):
                continue
            else:
                dir_idx = 0
                step_idx = 0
                if(piece == Match.PIECES['wPw']):
                    if(y < 6):
                        steps = WPW_STEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = WPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == Match.PIECES['bPw']):
                    if(y > 1):
                        steps = BPW_STEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = BPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
                    steps = RK_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
                    steps = BP_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
                    steps = KN_STEPS
                    max_dir = 8
                    max_step = 1
                elif(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
                    steps = QU_STEPS
                    max_dir = 8
                    max_step = 7
                else:
                    steps = KG_STEPS
                    max_dir = 10
                    max_step = 1

            for dir_idx in range(0, max_dir, 1):
                for step_idx in range(0, max_step, 1):
                    stepx, stepy, prom_piece = read_steps(steps, dir_idx, step_idx)
                    dstx = x + stepx
                    dsty = y + stepy
                    flag, errmsg = rules.is_move_valid(match, x, y, dstx, dsty, prom_piece)
                    if(flag):
                        gmove = GenMove(x, y, dstx, dsty, prom_piece)
                        attacked = rules.attacked(match, x, y, Match.REVERSED_COLORS[color])
                        dstpiece = match.readfield(dstx, dsty)
                        if(attacked or dstpiece != Match.PIECES['blk']):
                            gmoves.append(gmove)
                        else:
                            a_moves.append(gmove)
                    elif(errmsg != rules.ERROR_CODES['king-error']):
                        break

    gmoves.extend(a_moves)


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
        print("match.id: " + str(match.id))

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
            maxdepth = 4 # professional

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
    if(color == Match.COLORS["white"] and score < newscore):
        return newscore, newgmove
    elif(color == Match.COLORS["black"] and score > newscore):
        return newscore, newgmove
    else:
        return score, gmove


def calc_max(match, maxdepth, depth, alpha, beta):
    gmove = None
    color = match.next_color()
    newscore = None
    maxscore = -200000
    oldscore = 0
    is_move_capture = False
    is_move_promotion = False
    is_former_move_capture = False
    is_former_move_promotion = False
    gmoves = []

    generate_moves(match, gmoves)
    for newgmove in gmoves:
        oldscore = match.score
        is_former_move_capture = match.is_last_move_capture()
        is_former_move_promotion = match.is_last_move_promotion()

        move = match.do_move(newgmove.srcx, newgmove.srcy, newgmove.dstx, newgmove.dsty, newgmove.prom_piece)

        is_move_capture = match.is_last_move_capture()
        is_move_promotion = match.is_last_move_promotion()

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
        elif(depth <= maxdepth + 1):
            if(match.next_color() == Match.COLORS['white']):
                kg_attacked = rules.attacked(match, match.wKg_x, match.wKg_y, Match.COLORS['black'])
            else:
                kg_attacked = rules.attacked(match, match.bKg_x, match.bKg_y, Match.COLORS['white'])

            if(is_move_capture or is_move_promotion or is_former_move_capture or is_former_move_promotion or kg_attacked):
                newscore = calc_min(match, maxdepth, depth + 1, maxscore, beta)[0]
            else:
                newscore = match.score + calc_helper.evaluate_position(match)
        else:
            if(match.next_color() == Match.COLORS['white']):
                kg_attacked = rules.attacked(match, match.wKg_x, match.wKg_y, Match.COLORS['black'])
            else:
                kg_attacked = rules.attacked(match, match.bKg_x, match.bKg_y, Match.COLORS['white'])

            if(depth <= maxdepth + 4 and (is_move_capture or is_move_promotion or kg_attacked)):
                newscore = calc_min(match, maxdepth, depth + 1, maxscore, beta)[0]
            else:
                newscore = match.score + calc_helper.evaluate_position(match)

        newscore, gmove = rate(color, gmove, newgmove, maxscore, newscore)
        match.undo_move(True)
        if(newscore > maxscore):
            maxscore = newscore
            if(maxscore >= beta):
                break

    if(len(gmoves) == 0):
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
    gmove = None
    color = match.next_color()
    newscore = None
    minscore = 200000
    oldscore = 0
    is_move_capture = False
    is_move_promotion = False
    is_former_move_capture = False
    is_former_move_promotion = False
    gmoves = []

    generate_moves(match, gmoves)
    for newgmove in gmoves:
        oldscore = match.score
        is_former_move_capture = match.is_last_move_capture()
        is_former_move_promotion = match.is_last_move_promotion()

        move = match.do_move(newgmove.srcx, newgmove.srcy, newgmove.dstx, newgmove.dsty, newgmove.prom_piece)

        is_move_capture = match.is_last_move_capture()
        is_move_promotion = match.is_last_move_promotion()

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
        elif(depth <= maxdepth + 1):
            if(match.next_color() == Match.COLORS['white']):
                kg_attacked = rules.attacked(match, match.wKg_x, match.wKg_y, Match.COLORS['black'])
            else:
                kg_attacked = rules.attacked(match, match.bKg_x, match.bKg_y, Match.COLORS['white'])

            if(is_move_capture or is_move_promotion or is_former_move_capture or is_former_move_promotion or kg_attacked):
                newscore = calc_max(match, maxdepth, depth + 1, alpha, minscore)[0]
            else:
                newscore = match.score + calc_helper.evaluate_position(match)
        else:
            if(match.next_color() == Match.COLORS['white']):
                kg_attacked = rules.attacked(match, match.wKg_x, match.wKg_y, Match.COLORS['black'])
            else:
                kg_attacked = rules.attacked(match, match.bKg_x, match.bKg_y, Match.COLORS['white'])

            if(depth <= maxdepth + 4 and (is_move_capture or is_move_promotion or kg_attacked)):
                newscore = calc_max(match, maxdepth, depth + 1, alpha, minscore)[0]
            else:
                newscore = match.score + calc_helper.evaluate_position(match)

        newscore, gmove = rate(color, gmove, newgmove, minscore, newscore)
        match.undo_move(True)
        if(newscore < minscore):
            minscore = newscore
            if(minscore <= alpha):
                break

    if(len(gmoves) == 0):
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


