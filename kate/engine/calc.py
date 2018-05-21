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


def prnt_move(headmsg, move, tailmsg):
    if(move is None):
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
    print("tactics: ", end="")

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
    
    def find_tactic(self, tactic):
        for tactic_item in self.tactics:
            if(tactic_item == tactic):
                return True
        return False

    def is_tactic_stormy(self):
        for tactic in self.tactics:
            if(tactic == TACTICS['defend-check'] or
               tactic == TACTICS['defend-king-attack-urgent'] or
               tactic == TACTICS['defend-king-attack'] or
               tactic == TACTICS['promotion'] or
               tactic == TACTICS['capture-good-deal'] or
               tactic == TACTICS['attack-king-good-deal'] or 
               tactic == TACTICS['capture-bad-deal'] or 
               tactic == TACTICS['attack-king-bad-deal'] or
               tactic == TACTICS['attack-stormy']):
                return True
        return False

    def is_tactic_urgent(self):
        for tactic in self.tactics:
            if(tactic == TACTICS['defend-king-attack-urgent'] or
               tactic == TACTICS['capture-good-deal'] or
               tactic == TACTICS['capture-bad-deal']):
                return True
        return False


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


def append_newmove(gmove, nodecandidates, newcandidates):
    nodecandidates.clear()
    nodecandidates.append(gmove)

    for newcandidate in newcandidates:
        if(newcandidate):
            nodecandidates.append(newcandidate)
        else:
            break

    #nodecandidates.append(None)

def count_up_to_prio(priomoves, prio_limit):
    count = 0

    for priomove in priomoves:
        if(priomove.prio <= prio_limit):
            count += 1

    return count
    
def select_maxcount(match, priomoves, depth, slimits, last_pmove):
    if(len(priomoves) == 0):
        return 0
    
    if(priomoves[0].find_tactic(TACTICS['defend-check'])):
        return len(priomoves)
    
    if(depth <= slimits.dpth_stage1):
        return max(slimits.count, count_up_to_prio(priomoves, PRIO['prio5']))
    elif(depth <= slimits.dpth_stage2 and 
         (last_pmove.is_tactic_stormy() or is_stormy(match))):
        count = 0
        silent_move_cnt = 0

        for priomove in priomoves:
            if(priomove.find_tactic(TACTICS['defend-king-attack-urgent']) or
               priomove.find_tactic(TACTICS['defend-king-attack']) or
               priomove.find_tactic(TACTICS['attack-king-good-deal']) or 
               priomove.find_tactic(TACTICS['capture-good-deal'])):
                count += 1
                priomove.prio = PRIO['prio1']
                continue
            elif(priomove.find_tactic(TACTICS['attack-king-bad-deal']) or priomove.find_tactic(TACTICS['capture-bad-deal'])):
                count += 1
                priomove.prio = PRIO['prio3']
                continue
            elif(silent_move_cnt < 2):
                count += 1
                silent_move_cnt += 1
                priomove.prio = PRIO['prio2']
                continue
            else:
                priomove.prio = PRIO['prio10']

        priomoves.sort(key=attrgetter('prio'))
        return count
    elif(last_pmove.is_tactic_urgent()):
        count = 0
        silent_move_cnt = 0

        for priomove in priomoves:
            if(priomove.find_tactic(TACTICS['defend-king-attack-urgent']) or
               priomove.find_tactic(TACTICS['capture-good-deal'])):
                count += 1
                priomove.prio = PRIO['prio2']
                continue
            elif(priomove.find_tactic(TACTICS['capture-bad-deal'])):
                count += 1
                priomove.prio = PRIO['prio3']
                continue
            elif(silent_move_cnt < 1):
                count += 1
                silent_move_cnt += 1
                priomove.prio = PRIO['prio1']
                continue
            else:
                priomove.prio = PRIO['prio10']

        priomoves.sort(key=attrgetter('prio'))
        return count
    else:
        return 0


def alphabeta(match, depth, slimits, alpha, beta, maximizing, last_pmove, currentsearch):
    color = match.next_color()
    nodecandidates = []
    newcandidates = []
    count = 0

    if(maximizing):
        nodescore = SCORES[PIECES['wKg']] * 2
    else:
        nodescore = SCORES[PIECES['bKg']] * 2

    priomoves = generate_moves(match)
    
    rank_gmoves(match, priomoves, depth, slimits, last_pmove)    
    
    maxcnt = select_maxcount(match, priomoves, depth, slimits, last_pmove)

    if(depth == 1):
        print("maxcount: " + str(maxcnt))
        prnt_priomoves(priomoves)
        if(len(priomoves) == 1):
            pmove = priomoves[0]
            nodecandidates.append(pmove.gmove)
            nodecandidates.append(None)
            if(pmove.find_tactic(TACTICS['position-repeat'])):
                return 0, nodecandidates
            else:
                return score_position(match, len(priomoves)), nodecandidates

    if(len(priomoves) == 0 or maxcnt == 0):
        nodecandidates.append(None)
        return score_position(match, len(priomoves)), nodecandidates

    for priomove in priomoves:
        gmove = priomove.gmove

        count += 1

        if(depth == 1):
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, gmove, " | ")
            prnt_tactics(priomove.tactics)
            print(" | " + reverse_lookup(PRIO, priomove.prio) + " | " + reverse_lookup(PRIO, priomove.prio_sec))

        if(priomove.find_tactic(TACTICS['position-repeat'])):
            newcandidates.clear()
            newcandidates.append(None)
            score = 0
        else:
            matchmove.do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

            score, newcandidates = alphabeta(match, depth + 1, slimits, alpha, beta, not maximizing, priomove, None)

            #score += score_mupltiple_piece_moves_in_opening(match, color)

            matchmove.undo_move(match)

        if(maximizing):
            if(score > nodescore):
                nodescore = score
                append_newmove(gmove, nodecandidates, newcandidates)

            if(depth == 1):
                currentsearch.clear()
                for candidate in nodecandidates:
                    currentsearch.append(candidate)

                prnt_move("\nCURR SEARCH: " + str(score).rjust(8, " ") + " [", gmove, "]")
                prnt_moves("", newcandidates)
                prnt_moves("CANDIDATES:  " + str(nodescore).rjust(8, " "), nodecandidates)
                print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

            alpha = max(alpha, nodescore)
            if(beta <= alpha):
                break # beta cut-off
        else:
            if(score < nodescore):
                nodescore = score
                append_newmove(gmove, nodecandidates, newcandidates)

            if(depth == 1):
                currentsearch.clear()
                for candidate in nodecandidates:
                    currentsearch.append(candidate)

                prnt_move("\nCURR SEARCH: " + str(score).rjust(8, " ") + " [", gmove, "]")
                prnt_moves("", newcandidates)
                prnt_moves("CANDIDATES:  " + str(nodescore).rjust(8, " "), nodecandidates)
                print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

            beta = min(beta, nodescore)
            if(beta <= alpha):
                break # alpha cut-off

        #elapsed_time = time.time() - match.time_start
        #if(elapsed_time > match.seconds_per_move):
            #exceeded = True
        #else:
            #exceeded = False
        if(count >= maxcnt):
            break

    return nodescore, nodecandidates


class SearchLimits:
    def __init__(self, match):
        self.count = 6
        self.dpth_stage1 = 2
        self.dpth_stage2 = 5

        self.setlimits(match)

    def setlimits(self, match):
        if(match.level == LEVELS['blitz']):
            self.count = 6
            self.dpth_stage1 = 2
            self.dpth_stage2 = 5
        elif(match.level == LEVELS['low']):
            self.count = 8
            self.dpth_stage1 = 3
            self.dpth_stage2 = 6
        elif(match.level == LEVELS['medium']):
            self.count = 12
            self.dpth_stage1 = 4
            self.dpth_stage2 = 7
        else:
            self.count = 16
            self.dpth_stage1 = 5
            self.dpth_stage2 = 8


def calc_move(match, currentsearch):
    print("is opening: " + str(is_opening(match)) + " is endgame: " + str(is_endgame(match)))

    candidates = []
    
    slimits = SearchLimits(match)

    match.time_start = time.time()

    gmove = retrieve_move(match)
    if(gmove is not None):
        candidates.append(gmove)
        score = match.score
    else:
        maximizing = match.next_color() == COLORS['white']
        alpha = SCORES[PIECES['wKg']] * 10
        beta = SCORES[PIECES['bKg']] * 10 
        score, candidates = alphabeta(match, 1, slimits, alpha, beta, maximizing, None, currentsearch)

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
    return candidates

