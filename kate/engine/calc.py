import time
from operator import attrgetter
from .match import *
from .move import *
from . import matchmove
from .openingmove import retrieve_move
from .analyze_move import *
from .analyze_position import *
from .helper import *
from .cvalues import *
from .rules import is_move_valid, RETURN_CODES, is_field_touched
from .pieces import pawn, rook, bishop, knight, queen, king
from .debug import prnt_attributes


def prnt_move(headmsg, move, tailmsg):
    if(move == None):
        print("no move.....")
    else:
        print(headmsg + 
            index_to_coord(move.srcx, move.srcy) + "-" +
            index_to_coord(move.dstx, move.dsty), end="")
        if(move.prom_piece != PIECES['blk']):
            print(" " + reverse_lookup(PIECES, move.prom_piece), end="")
        print(tailmsg, end="")


def prnt_moves(msg, moves):
    print(msg, end=" ")

    if(len(moves) == 0):
        print("no move.....")
    else:
        for move in moves:
            if(move):
                prnt_move("[", move, "] ")
            else:
                break
        print("")


def prnt_tactics(tactics):
    print("tatics: ", end="")

    length = len(tactics)
    i = 1
    for tactic in tactics:
        if(i < length):
            print(reverse_lookup(TACTICS, tactic), end=" | ")
        else:
            print(reverse_lookup(TACTICS, tactic), end="")
        i += 1


def prnt_priomoves(priomoves):
    for priomove in priomoves:
        prnt_move("\n", priomove.gmove, " ")
        prnt_tactics(priomove.tactics)


def prnt_fmttime(msg, seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    print( msg + "%02d:%02d:%02d" % (hour, minute, sec))


class Analyses:
    def __init__(self):
        self.core_token = 0x0
        self.srcfield_token = 0x0
        self.dstfield_token = 0x0
        self.lst_attacked = []
        self.lst_supported = []
        self.lst_disclosed_attacked = []
        self.lst_fork_defended = []

class PrioMove:
    def __init__(self, gmove=None):
        self.gmove = gmove
        self.tactics = []
        self.prio = PRIO['prio10']
        self.prio_sec = PRIO['prio10']

    def downgrade(self, old_tactic, new_tactic):
        self.prio = TACTICS_TO_PRIO[new_tactic]
        for idx in range(len(self.tactics)):
            if(self.tactics[idx] == old_tactic):
                self.tactics[idx] = new_tactic
                return

    def fetch_tactics(self, idx):
        if(len(self.tactics) > idx):
            return self.tactics[idx]
        else:
            return TACTICS['undefined']


def read_steps(steps, dir_idx, step_idx):
    stepx = steps[dir_idx][step_idx][0]
    stepy = steps[dir_idx][step_idx][1]
    prom_piece = steps[dir_idx][step_idx][2]
    return stepx, stepy, prom_piece

def generate_moves(match):
    color = match.next_color()
    priomoves = []

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == PIECES['blk'] or color != Match.color_of_piece(piece)):
                continue
            else:
                dir_idx = 0
                step_idx = 0
                if(piece == PIECES['wPw']):
                    if(y < 6):
                        steps = pawn.GEN_WSTEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = pawn.GEN_WPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == PIECES['bPw']):
                    if(y > 1):
                        steps = pawn.GEN_BSTEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = pawn.GEN_BPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                    steps = rook.GEN_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                    steps = bishop.GEN_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                    steps = knight.GEN_STEPS
                    max_dir = 8
                    max_step = 1
                elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                    steps = queen.GEN_STEPS
                    max_dir = 8
                    max_step = 7
                else:
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
                        priomove = PrioMove(gmove)
                        priomoves.append(priomove)
                    elif(errmsg != rules.RETURN_CODES['king-error']):
                        break

    return priomoves


def rate(color, newscore, newmove, newcandidates, score, candidates):
    if( (color == COLORS["white"] and score >= newscore) or (color == COLORS["black"] and score <= newscore) ):
        return score
    else:
        candidates.clear()
        candidates.append(newmove)

        if(len(newcandidates) > 0):
            for newcandidate in newcandidates:
                if(newcandidate):
                    candidates.append(newcandidate)
                else:
                    break

        candidates.append(None)
        return newscore


def was_last_move_stormy(last_pmove):
    for tactic in last_pmove.tactics:
        if(tactic == TACTICS['promotion'] or
           tactic == TACTICS['capture-good-deal'] or
           tactic == TACTICS['attack-king-good-deal'] or 
           tactic == TACTICS['capture-bad-deal'] or       
           tactic == TACTICS['attack-king-bad-deal'] or
           tactic == TACTICS['attack-stormy']):
            return True

    return False

def select_maxcnt_maxprio(match, depth, priomoves, last_pmove):
    #exceeded = False

    #elapsed_time = time.time() - match.time_start
    #if(elapsed_time > match.seconds_per_move):
        #exceeded = True

    if(last_pmove):
        last_prio = last_pmove.prio
    else:
        last_prio = PRIO['prio10']

    if(match.level == LEVELS['blitz']):
        cnt = 8
        dpth_stage1 = 2
        dpth_stage2 = 5
        dpth_stage3 = 8
    elif(match.level == LEVELS['low']):
        cnt = 10
        dpth_stage1 = 3
        dpth_stage2 = 5
        dpth_stage3 = 8
    elif(match.level == LEVELS['medium']):
        cnt = 12
        dpth_stage1 = 4
        dpth_stage2 = 7
        dpth_stage3 = 12
    else:
        cnt = 16
        dpth_stage1 = 5
        dpth_stage2 = 8
        dpth_stage3 = 12

    if(is_endgame(match)):
        dpth_stage1 += 2

    if(depth <= dpth_stage1):
        #if(exceeded):
            #return cnt, PRIO_MIN
        #else:
        return cnt, PRIO_MAX
    elif(depth <= dpth_stage2 and (was_last_move_stormy(last_pmove) or is_stormy(match))):
        return cnt, PRIO_MID
    elif(depth <= dpth_stage3 and was_last_move_stormy(last_pmove)):
        return cnt, PRIO_MIN
    #elif(depth <= dpth_stage3 and (was_last_move_stormy(last_pmove) or is_stormy(match))):
        #return cnt, PRIO_MIN
    else:
        return 0, PRIO['prio1']


def calc_max(match, depth, alpha, beta, last_pmove):
    color = match.next_color()
    candidates = []
    newcandidates = []
    maxscore = SCORES[PIECES['wKg']] * 2
    count = 0

    priomoves = generate_moves(match)
    
    rank_gmoves(match, priomoves)
    
    maxcnt, maxprio = select_maxcnt_maxprio(match, depth, priomoves, last_pmove)

    if(depth == 1):
        prnt_priomoves(priomoves)
        if(len(priomoves) == 1):
            pmove = priomoves[0]
            candidates.append(pmove.gmove)
            candidates.append(None)
            return score_position(match, len(priomoves)), candidates

    if(len(priomoves) == 0 or maxcnt == 0):
        candidates.append(None)
        return score_position(match, len(priomoves)), candidates

    for priomove in priomoves:
        newmove = priomove.gmove

        count += 1

        if(depth == 1):
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, newmove, " | ")
            prnt_tactics(priomove.tactics)
            print(" | " + reverse_lookup(PRIO, priomove.prio) + " | " + reverse_lookup(PRIO, priomove.prio_sec))

        move = matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        newscore, newcandidates = calc_min(match, depth + 1, maxscore, beta, priomove) # , dbginfo

        ### todo move code to other module
        if(is_opening(match)):
            if(piece_movecnt(match, move) == 3):
                if(color == COLORS['white']):
                    newscore += ATTACKED_SCORES[PIECES['bPw']]
                else:
                    newscore += ATTACKED_SCORES[PIECES['wPw']]
        ###

        score = rate(color, newscore, newmove, newcandidates, maxscore, candidates)

        matchmove.undo_move(match)

        if(depth == 1):
            prnt_move("\nCURR SEARCH: " + str(newscore).rjust(8, " ") + " [", newmove, "]")
            prnt_moves("", newcandidates)

            prnt_moves("CANDIDATES:  " + str(score).rjust(8, " "), candidates)
            print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

        if(score > maxscore):
            maxscore = score
            if(maxscore > beta):
                return maxscore, candidates

        if((count >= maxcnt and priomove.prio > PRIO['prio1']) or priomove.prio > maxprio):
            return maxscore, candidates

    return maxscore, candidates


def calc_min(match, depth, alpha, beta, last_pmove):
    color = match.next_color()
    candidates = []
    newcandidates = []
    minscore = SCORES[PIECES['bKg']] * 2
    count = 0

    priomoves = generate_moves(match)
    
    rank_gmoves(match, priomoves)

    maxcnt, maxprio = select_maxcnt_maxprio(match, depth, priomoves, last_pmove)

    if(depth == 1):
        prnt_priomoves(priomoves)
        if(len(priomoves) == 1):
            pmove = priomoves[0]
            candidates.append(pmove.gmove)
            candidates.append(None)
            return score_position(match, len(priomoves)), candidates

    if(len(priomoves) == 0 or maxcnt == 0):
        candidates.append(None)
        return score_position(match, len(priomoves)), candidates

    for priomove in priomoves:
        newmove = priomove.gmove

        count += 1

        if(depth == 1):
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, newmove, " | ")
            prnt_tactics(priomove.tactics)
            print(" | " + reverse_lookup(PRIO, priomove.prio) + " | " + reverse_lookup(PRIO, priomove.prio_sec))

        move = matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        newscore, newcandidates = calc_max(match, depth + 1, alpha, minscore, priomove) # , dbginfo

        ### todo move code to other module
        if(is_opening(match)):
            if(piece_movecnt(match, move) == 3):
                if(color == COLORS['white']):
                    newscore += ATTACKED_SCORES[PIECES['bPw']]
                else:
                    newscore += ATTACKED_SCORES[PIECES['wPw']]
        ###

        score = rate(color, newscore, newmove, newcandidates, minscore, candidates)

        matchmove.undo_move(match)
        
        if(depth == 1):
            prnt_move("\nCURR SEARCH: " + str(newscore).rjust(8, " ") + " [", newmove, "]")
            prnt_moves("", newcandidates)

            prnt_moves("CANDIDATES:  " + str(score).rjust(8, " "), candidates)
            print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

        if(score < minscore):
            minscore = score
            if(minscore < alpha):
                return minscore, candidates

        if((count >= maxcnt and priomove.prio > PRIO['prio1']) or priomove.prio > maxprio):
            return minscore, candidates

    return minscore, candidates


def calc_move(match):
    print("is opening: " + str(is_opening(match)) + " is endgame: " + str(is_endgame(match)))

    candidates = []

    match.time_start = time.time()

    gmove = retrieve_move(match)
    if(gmove):
        candidates.append(gmove)
        score = match.score
    elif(match.next_color() == COLORS['white']):
        score, candidates = calc_max(match, 1, SCORES[PIECES['bKg']] * 2, SCORES[PIECES['bKg']] * 2, None) # , dbginfo
    else:
        score, candidates = calc_min(match, 1, SCORES[PIECES['wKg']] * 2, SCORES[PIECES['bKg']] * 2, None) # , dbginfo

    ### time
    elapsed_time = time.time() - match.time_start
    if(match.next_color() == COLORS['white']):
        match.white_elapsed_seconds += elapsed_time
    else:
        match.black_elapsed_seconds += elapsed_time

    match.time_start = time.time()
    ###

    msg = "result: " + str(score) + " match.id: " + str(match.id) + " "
    prnt_moves(msg, candidates)
    prnt_fmttime("\ncalc-time: ", elapsed_time)
    prnt_attributes(match, "\n")
    return candidates

