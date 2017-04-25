from kate.models import Match, Move
from kate.modules import helper, rules, pawn, rook, bishop, knight, queen, king, kate, openings, calc_helper, debug
import random, threading, copy, time 
from operator import itemgetter


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
    prom_piece = steps[dir_idx][step_idx][2]
    return stepx, stepy, prom_piece


def sort_move(match, gmove, piece_moves):
    prio1 = 1
    prio2 = 2
    prio3 = 3
    prio4 = 4
    
    if( calc_helper.is_capture(match, gmove) ):
        piece_moves.append([prio1, gmove])
        return
    
    if( calc_helper.is_promotion(match, gmove) ):
        piece_moves.append([prio1, gmove])
        return
    
    if( calc_helper.is_castling(match, gmove) ):
        piece_moves.append([prio1, gmove])
        return

    attack, priority = calc_helper.does_attack(match, gmove)
    if(attack):
        piece_moves.append([priority, gmove])
        return

    support, priority = calc_helper.does_support_attacked(match, gmove)
    if(support):
        piece_moves.append([priority, gmove])
        return

    if( calc_helper.does_attacked_flee(match, gmove) ):
        piece_moves.append([prio2, gmove])
        return

    if( calc_helper.is_endgame_move(match, gmove) ):
        piece_moves.append([prio3, gmove])
        return

    piece_moves.append([prio4, gmove])


def generate_moves(match):
    color = match.next_color()
    moves = []
    prio_moves = []
    piece_moves = None
    pw_moves = []
    kn_moves = []
    bp_moves = []
    rk_moves = []
    qu_moves = []
    kg_moves = []

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == Match.PIECES['blk'] or color != Match.color_of_piece(piece)):
                continue
            else:
                dir_idx = 0
                step_idx = 0
                if(piece == Match.PIECES['wPw']):
                    piece_moves = pw_moves
                    if(y < 6):
                        steps = pawn.GEN_WSTEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = pawn.GEN_WPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == Match.PIECES['bPw']):
                    piece_moves = pw_moves
                    if(y > 1):
                        steps = pawn.GEN_BSTEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = pawn.GEN_BPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == Match.PIECES['wRk'] or piece == Match.PIECES['bRk']):
                    piece_moves = rk_moves
                    steps = rook.GEN_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == Match.PIECES['wBp'] or piece == Match.PIECES['bBp']):
                    piece_moves = bp_moves
                    steps = bishop.GEN_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == Match.PIECES['wKn'] or piece == Match.PIECES['bKn']):
                    piece_moves = kn_moves
                    steps = knight.GEN_STEPS
                    max_dir = 8
                    max_step = 1
                elif(piece == Match.PIECES['wQu'] or piece == Match.PIECES['bQu']):
                    piece_moves = qu_moves
                    steps = queen.GEN_STEPS
                    max_dir = 8
                    max_step = 7
                else:
                    piece_moves = kg_moves
                    steps = king.GEN_STEPS
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
                        sort_move(match, gmove, piece_moves)

                    elif(errmsg != rules.ERROR_CODES['king-error']):
                        break

    if(match.next_color() == Match.COLORS['white']):
        kg_attacked = rules.is_field_attacked(match, Match.COLORS['black'], match.wKg_x, match.wKg_y)
    else:
        kg_attacked = rules.is_field_attacked(match, Match.COLORS['white'], match.bKg_x, match.bKg_y)

    qu_moves.sort(key=itemgetter(0))
    prio_moves.extend(qu_moves[:6])
    prio_moves.extend(kg_moves)
    prio_moves.extend(rk_moves)
    prio_moves.extend(bp_moves)
    prio_moves.extend(kn_moves)
    prio_moves.extend(pw_moves)
    prio_moves.sort(key=itemgetter(0))
    prio_moves.extend(qu_moves[6:])

    topmovecnt = 0
    for pmove in prio_moves:
        moves.append(pmove[1])
        if(pmove[0] <= 2):
            topmovecnt += 1

    if(kg_attacked):
        topmovecnt = len(moves)

    return moves, topmovecnt


class immanuelsThread(threading.Thread):
    def __init__(self, name, match):
        threading.Thread.__init__(self)
        self.name = name
        self.match = copy.deepcopy(match)
        self.search_srcx = None
        self.search_srcy = None
        self.search_dstx = None
        self.search_dsty = None
        self.search_prom_piece = None
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

        gmove = calc_move(self.match)
        if(gmove != None):
            curr_match = Match.objects.get(id=self.match.id)
            if(curr_match.count == self.match.count and Match.does_thread_exist(self)):
                move = kate.do_move(self.match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
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

    def populate_search(self, gmove):
        if(gmove):
            self.search_srcx = gmove.srcx
            self.search_srcy = gmove.srcy
            self.search_dstx = gmove.dstx
            self.search_dsty = gmove.dsty
            self.search_prom_piece = gmove.prom_piece


def rate(color, gmove, gmovescore, candidate, candidatescore):
    if(color == Match.COLORS["white"] and candidatescore > gmovescore):
        return candidatescore, candidate
    elif(color == Match.COLORS["black"] and candidatescore < gmovescore):
        return candidatescore, candidate
    else:
        return gmovescore, gmove


def select_maxcnt(match, depth, topmovecnt):
    if(match.level == Match.LEVELS['blitz']):
        if(match.count < 30):
            counts = [16, 8, 8, 0, 0, 0, 0, 0, 0, 0]
            limit = 2
        else:
            counts = [16, 16, 8, 8, 0, 0, 0, 0, 0, 0]
            limit = 2
    else:
        if(match.level == Match.LEVELS['low']):
            counts = [32, 16, 8, 8, 8, 4, 4, 0, 0, 0]
            limit = 3
        elif(match.level == Match.LEVELS['medium']):
            counts = [200, 32, 16, 8, 8, 8, 4, 4, 0, 0]
            limit = 4
        else:
            counts = [200, 200, 32, 16, 8, 8, 8, 4, 4, 0]
            limit = 5

        if(depth <= limit):
            return max(topmovecnt, counts[(depth - 1)])
        else:
            return min(topmovecnt, counts[(depth - 1)])


def calc_max(match, depth, alpha, beta):
    color = match.next_color()
    candidate = None
    score = None
    maxscore = -200000
    count = 0

    gmoves, topmovecnt = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, topmovecnt)

    if(maxcnt == 0):
        return match.score + calc_helper.evaluate_position(match), None

    for gmove in gmoves[:maxcnt]:
        move = kate.do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
            
        if(depth == 1):
            count += 1
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, gmove)

        score = calc_min(match, depth + 1, maxscore, beta)[0]
        # score = match.score + calc_helper.evaluate_position(match)

        score, candidate = rate(color, gmove, score, candidate, maxscore)

        if(depth == 1):
            thread = Match.get_active_thread(match)
            if(thread):
                thread.populate_search(gmove)
                if(candidate):
                    thread.populate_candiate(candidate)
                    prnt_move(" *** CANDIDATE: ", candidate)
                    print(" --- score: " + str(score) + " / maxscore: " + str(maxscore))

        kate.undo_move(match, True)

        if(score > maxscore):
            maxscore = score
            if(maxscore > beta):
                return maxscore, candidate
                # break

    if(len(gmoves) == 0):
        status = rules.game_status(match)
        if(status == Match.STATUS['winner_black']):
            score = Match.SCORES[Match.PIECES['wKg']] - depth
        elif(status == Match.STATUS['winner_white']):
            score = Match.SCORES[Match.PIECES['bKg']] + depth
        elif(status == Match.STATUS['draw']):
            score = Match.SCORES[Match.PIECES['blk']]
        else:
            score = match.score

        if(depth == 1):
            msg = "\nmatch.id: " + str(match.id) + "   count: None" + "   calculate: "
            prnt_move(msg, gmove)

            thread = Match.get_active_thread(match)
            if(thread):
                thread.populate_search(gmove)
                if(candidate):
                    thread.populate_candiate(candidate)
                    prnt_move(" *** CANDIDATE: ", candidate)
                    print(" --- score: " + str(score) + " / maxscore: " + str(maxscore))

        return score, candidate

    return maxscore, candidate


def calc_min(match, depth, alpha, beta):
    color = match.next_color()
    candidate = None
    score = None
    minscore = 200000

    gmoves, topmovecnt = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, topmovecnt)

    if(maxcnt == 0):
        return match.score + calc_helper.evaluate_position(match), None

    for gmove in gmoves[:maxcnt]:
        move = kate.do_move(match,gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

        if(depth == 1):
            count += 1
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, gmove)

        score = calc_max(match, depth + 1, alpha, minscore)[0]
        # score = match.score + calc_helper.evaluate_position(match)

        score, candidate = rate(color, gmove, score, candidate, minscore)

        kate.undo_move(match, True)

        if(depth == 1):
            thread = Match.get_active_thread(match)
            if(thread):
                thread.populate_search(gmove)
                if(candidate):
                    thread.populate_candiate(candidate)
                    prnt_move(" *** CANDIDATE: ", candidate)
                    print(" --- score: " + str(score) + " / minscore: " + str(minscore))

        if(score < minscore):
            minscore = score
            if(minscore < alpha):
                return minscore, candidate
                # break

    if(len(gmoves) == 0):
        status = rules.game_status(match)
        if(status == Match.STATUS['winner_black']):
            score = Match.SCORES[Match.PIECES['wKg']] - depth
        elif(status == Match.STATUS['winner_white']):
            score = Match.SCORES[Match.PIECES['bKg']] + depth
        elif(status == Match.STATUS['draw']):
            score = Match.SCORES[Match.PIECES['blk']]
        else:
            score = match.score

        if(depth == 1):
            msg = "\nmatch.id: " + str(match.id) + "   count: None" + "   calculate: "
            prnt_move(msg, gmove)

            thread = Match.get_active_thread(match)
            if(thread):
                thread.populate_search(gmove)
                if(candidate):
                    thread.populate_candiate(candidate)
                    prnt_move(" *** CANDIDATE: ", candidate)
                    print(" --- score: " + str(score) + " / minscore: " + str(minscore))

        return score, candidate

    return minscore, candidate


def calc_move(match):
    start = time.time()
    
    gmove = openings.retrieve_move(match)

    if(gmove):
        score = match.score
    elif(match.next_color() == Match.COLORS['white']):
        score, gmove = calc_max(match, 1, -200000, 200000)
    else:
        score, gmove = calc_min(match, 1, -200000, 200000)

    if(gmove != None):
        msg = "\nresult: " + str(score) + " match.id: " + str(match.id) + " "
        prnt_move(msg, gmove)
        print("")
    else:
        print("no results found!!!" + str(score))

    end = time.time()
    print( (end - start) / 60 )
    return gmove


def thread_do_move(match):
    thread = immanuelsThread("immanuel-" + str(random.randint(0, 100000)), match)
    thread.start()


