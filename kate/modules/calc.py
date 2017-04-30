from kate.models import Match, Move
from kate.modules import helper, rules, pawn, rook, bishop, knight, queen, king, kate, openings, calc_helper, debug
import random, threading, copy, time 
from operator import itemgetter


def prnt_move(msg, move):
    if(move == None):
        print("no move.....")
    else:
        print(msg + 
            Match.index_to_koord(move.srcx, move.srcy) + "-" +
            Match.index_to_koord(move.dstx, move.dsty), end="")
        if(move.prom_piece != Match.PIECES['blk']):
            print(helper.reverse_lookup(Match.PIECES, move.prom_piece), end="")


def prnt_candidates(msg, candidates):
    if(candidates[0] == None):
        print("no move.....")
    else:
        print(msg, end=" ")
        candmsg = "["
        for cand in candidates[:9]:
            prnt_move(candmsg, cand)
            print("] ", end="")


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
    priority = 5
    
    if( calc_helper.is_capture(match, gmove) ):
        piece_moves.append([prio1, gmove])
        return prio1
    
    if( calc_helper.is_promotion(match, gmove) ):
        piece_moves.append([prio1, gmove])
        return prio1
    
    if( calc_helper.is_castling(match, gmove) ):
        piece_moves.append([prio1, gmove])
        return prio1

    attack, prio = calc_helper.does_attack(match, gmove)
    if(attack):
        priority = min(priority, prio)
        if(priority == prio1):
            piece_moves.append([priority, gmove])
            return priority

    support, prio = calc_helper.does_support_attacked(match, gmove)
    if(support):
        priority = min(priority, prio)
        if(priority == prio1):
            piece_moves.append([priority, gmove])
            return priority

    flee, prio = calc_helper.does_attacked_flee(match, gmove)
    if(flee):
        priority = min(priority, prio)
        if(priority == prio1):
            piece_moves.append([priority, gmove])
            return priority

    endgame, prio = calc_helper.is_endgame_move(match, gmove)
    if(endgame):
        priority = min(priority, prio)
        if(priority == prio1):
            piece_moves.append([priority, gmove])
            return priority

    priority = min(priority, prio4)
    piece_moves.append([priority, gmove])
    return priority


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
    priorities = [0] * 4

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
                        priority = sort_move(match, gmove, piece_moves)
                        if(priority == 0):
                            priorities[0] += 1
                        elif(priority == 1):
                            priorities[1] += 1
                        if(priority == 2):
                            priorities[2] += 1
                        else:
                            priorities[3] += 1

                    elif(errmsg != rules.RETURN_CODES['king-error']):
                        break

    if(match.next_color() == Match.COLORS['white']):
        kg_attacked = rules.is_field_attacked(match, Match.COLORS['black'], match.wKg_x, match.wKg_y)
    else:
        kg_attacked = rules.is_field_attacked(match, Match.COLORS['white'], match.bKg_x, match.bKg_y)

    prio_moves.extend(kg_moves)
    prio_moves.extend(rk_moves)
    prio_moves.extend(bp_moves)
    prio_moves.extend(kn_moves)
    prio_moves.extend(pw_moves)
    prio_moves.extend(qu_moves)
    prio_moves.sort(key=itemgetter(0))
    
    for pmove in prio_moves:
        moves.append(pmove[1])

    if(kg_attacked):
        priorities[0]= len(moves)
        priorities[1]= 0
        priorities[2]= 0
        priorities[3]= 0
    return moves, priorities


class immanuelsThread(threading.Thread):
    def __init__(self, name, match):
        threading.Thread.__init__(self)
        self.name = name
        self.running = True
        self.match = copy.deepcopy(match)
        self.search = [None]
        self.candidates = [None] * 10

        Match.remove_outdated_threads(match)
        Match.add_thread(self)
        print("match.id: " + str(match.id))

    def run(self):
        print("Starting " + str(self.name))
        move = Move.objects.filter(match_id=self.match.id).order_by("count").last()
        if(move != None):
            self.match.move_list.append(move)

        gmove = calc_move(self.match)
        if(self.running and gmove != None):
            curr_match = Match.objects.get(id=self.match.id)
            if(curr_match.count == self.match.count and Match.does_thread_exist(self)):
                move = kate.do_move(self.match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
                move.save()
                self.match.save()
                print("move saved")
            else:
                print("thread outdated - move dropped")
        return gmove

    def populate_candiates(self, candiates):
        if(candiates[0]):
            idx = 0
            for cand in candiates:
                if(cand):
                    self.candidates[idx] = cand
                    idx += 1
                else:
                    break

    def populate_search(self, gmove):
        if(gmove):
            self.search = gmove


def rate(color, gmove, gmovescore, candidates, candidatescore, search_candidates):
    if( (color == Match.COLORS["white"] and candidatescore >= gmovescore) or (color == Match.COLORS["black"] and candidatescore <= gmovescore) ):
        return candidatescore
    else:
        candidates[0] = gmove

        if(search_candidates):
            idx = 1
            for cand in search_candidates[:9]:
                if(cand):
                    candidates[idx] = cand
                    idx += 1

        return gmovescore


def select_maxcnt(match, depth, priorities):
    if(match.level == Match.LEVELS['blitz']):
        counts = [16, 16, 16, 16, 8, 4, 0, 0, 0, 0]
        limit = 2
    elif(match.level == Match.LEVELS['low']):
        counts = [32, 16, 16, 16, 8, 4, 4, 0, 0, 0]
        limit = 2
    elif(match.level == Match.LEVELS['medium']):
        counts = [200, 32, 16, 16, 16, 8, 4, 4, 0, 0]
        limit = 3
    else:
        counts = [200, 200, 32, 16, 16, 16, 8, 4, 4, 0]
        limit = 4

    if(depth <= limit):
        return max((priorities[0] + priorities[1] + priorities[2]), counts[(depth - 1)])
    elif(depth <= limit + 2):
        return min((priorities[0] + priorities[1] + priorities[2]), counts[(depth - 1)])
    elif(depth <= limit + 4):
        return min((priorities[0] + priorities[1]), counts[(depth - 1)])
    else:
        return min((priorities[0]), counts[(depth - 1)])


def calc_max(match, depth, alpha, beta):
    color = match.next_color()
    candidates = [None] * 10
    search_candidates = [None] * 10
    score = None
    maxscore = -200000
    count = 0

    gmoves, priorities = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, priorities)

    if(maxcnt == 0):
        return match.score + calc_helper.evaluate_position(match), candidates

    for gmove in gmoves[:maxcnt]:
        move = kate.do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

        score, search_candidates = calc_min(match, depth + 1, maxscore, beta)

        score = rate(color, gmove, score, candidates, maxscore, search_candidates)

        if(depth == 1):
            count += 1

            thread = Match.get_active_thread(match)
            if(thread):
                thread.populate_search(gmove)
                thread.populate_candiates(candidates)

            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, gmove)
            msg = "    CANDIDATES: "
            prnt_candidates(msg, candidates)
            print(" score: " + str(score) + " / maxscore: " + str(maxscore))

        kate.undo_move(match, True)

        if(score > maxscore):
            maxscore = score
            if(maxscore > beta):
                return maxscore, candidates

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
            print("\nmatch.id: " + str(match.id) + "   count: None" + "   calculate: " + str(score))

        return score, candidates

    return maxscore, candidates


def calc_min(match, depth, alpha, beta):
    color = match.next_color()
    candidates = [None] * 10
    search_candidates = [None] * 10
    score = None
    minscore = 200000
    count = 0

    gmoves, priorities = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, priorities)

    if(maxcnt == 0):
        return match.score + calc_helper.evaluate_position(match), candidates

    for gmove in gmoves[:maxcnt]:
        move = kate.do_move(match,gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

        score, search_candidates = calc_max(match, depth + 1, alpha, minscore)

        score = rate(color, gmove, score, candidates, minscore, search_candidates)

        kate.undo_move(match, True)

        if(depth == 1):
            count += 1

            thread = Match.get_active_thread(match)
            if(thread):
                thread.populate_search(gmove)
                thread.populate_candiates(candidates)

            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, gmove)
            msg = "    CANDIDATES: "
            prnt_candidates(msg, candidates)
            print(" score: " + str(score) + " / minscore: " + str(minscore))

        if(score < minscore):
            minscore = score
            if(minscore < alpha):
                return minscore, candidates

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
            print("\nmatch.id: " + str(match.id) + "   count: None" + "   calculate: " + str(score))

        return score, candidates

    return minscore, candidates


def calc_move(match):
    candidates = [None] * 10

    start = time.time()
    
    candidates[0] = openings.retrieve_move(match)

    if(candidates[0]):
        score = match.score
    elif(match.next_color() == Match.COLORS['white']):
        score, candidates = calc_max(match, 1, -200000, 200000)
    else:
        score, candidates = calc_min(match, 1, -200000, 200000)

    msg = "\nresult: " + str(score) + " match.id: " + str(match.id) + " "
    prnt_candidates(msg, candidates)

    end = time.time()
    print( (end - start) / 60 )
    return candidates[0]


def thread_do_move(match):
    thread = immanuelsThread("immanuel-" + str(random.randint(0, 100000)), match)
    thread.start()


