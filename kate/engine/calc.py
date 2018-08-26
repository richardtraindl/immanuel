import time
from operator import attrgetter
from .match import *
from .move import *
from .openingmove import retrieve_move
from .analyze_move import *
from .analyze_position import *
from .helper import *
from .validator import *
from .generator import cGenerator


def prnt_move(headmsg, move, tailmsg):
    if(move is None):
        print("no move.....")
    else:
        print(headmsg + 
            index_to_coord(move.srcx, move.srcy) + "-" +
            index_to_coord(move.dstx, move.dsty), end="")
        if(move.prom_piece != cMatch.PIECES['blk']):
            print(" " + reverse_lookup(cMatch.PIECES, move.prom_piece), end="")
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
            print(reverse_lookup(PrioMove.TACTICS, tactic), end=" | ")
        else:
            print(reverse_lookup(PrioMove.TACTICS, tactic), end="")
        i += 1


def prnt_priomoves(priomoves):
    for priomove in priomoves:
        prnt_move("\n", priomove.gmove, " ")
        prnt_tactics(priomove.tactics)


def prnt_fmttime(msg, seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    print( msg + "%02d:%02d:%02d" % (hour, minute, sec))


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
    
    if(priomoves[0].find_tactic(PrioMove.TACTICS['defend-check'])):
        return len(priomoves)
    
    if(depth <= slimits.dpth_stage1):
        return max(slimits.count, count_up_to_prio(priomoves, PrioMove.PRIO['prio5']))
    elif(depth <= slimits.dpth_stage2 and 
         (last_pmove.is_tactic_stormy() or is_stormy(match))):
        count = 0
        silent_move_cnt = 0

        for priomove in priomoves:
            if(priomove.find_tactic(PrioMove.TACTICS['defend-king-attack-urgent']) or
               priomove.find_tactic(PrioMove.TACTICS['defend-king-attack']) or
               priomove.find_tactic(PrioMove.TACTICS['attack-king-good-deal']) or 
               priomove.find_tactic(PrioMove.TACTICS['capture-good-deal'])):
                count += 1
                priomove.prio = PrioMove.PRIO['prio1']
                continue
            elif(priomove.find_tactic(PrioMove.TACTICS['attack-king-bad-deal']) or priomove.find_tactic(PrioMove.TACTICS['capture-bad-deal'])):
                count += 1
                priomove.prio = PrioMove.PRIO['prio3']
                continue
            elif(silent_move_cnt < 2):
                count += 1
                silent_move_cnt += 1
                priomove.prio = PrioMove.PRIO['prio2']
                continue
            else:
                priomove.prio = PrioMove.PRIO['prio10']

        priomoves.sort(key=attrgetter('prio'))
        return count
    elif(last_pmove.is_tactic_urgent()):
        count = 0
        silent_move_cnt = 0

        for priomove in priomoves:
            if(priomove.find_tactic(PrioMove.TACTICS['defend-king-attack-urgent']) or
               priomove.find_tactic(PrioMove.TACTICS['capture-good-deal'])):
                count += 1
                priomove.prio = PrioMove.PRIO['prio2']
                continue
            elif(priomove.find_tactic(PrioMove.TACTICS['capture-bad-deal'])):
                count += 1
                priomove.prio = PrioMove.PRIO['prio3']
                continue
            elif(silent_move_cnt < 1):
                count += 1
                silent_move_cnt += 1
                priomove.prio = PrioMove.PRIO['prio1']
                continue
            else:
                priomove.prio = PrioMove.PRIO['prio10']

        priomoves.sort(key=attrgetter('prio'))
        return count
    else:
        return 0


def alphabeta(match, depth, slimits, alpha, beta, maximizing, last_pmove, msgs):
    color = match.next_color()
    nodecandidates = []
    newcandidates = []
    count = 0
    starttime = time.time()

    if(maximizing):
        nodescore = match.SCORES[match.PIECES['wKg']] * 2
    else:
        nodescore = match.SCORES[match.PIECES['bKg']] * 2

    cgenerator = cGenerator(match)
    priomoves = cgenerator.generate_moves()

    rank_gmoves(match, priomoves, depth, slimits, last_pmove)    
    
    maxcnt = select_maxcount(match, priomoves, depth, slimits, last_pmove)

    if(depth == 1):
        prnt_priomoves(priomoves)
        if(len(priomoves) == 1):
            pmove = priomoves[0]
            nodecandidates.append(pmove.gmove)
            nodecandidates.append(None)
            if(pmove.find_tactic(PrioMove.TACTICS['tactical-draw'])):
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
            msg = "\nmatch: " + str(match.begin) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, gmove, " | ")
            prnt_tactics(priomove.tactics)
            print(" | " + reverse_lookup(priomove.PRIO, priomove.prio) + " | " + reverse_lookup(priomove.PRIO, priomove.prio_sec))

        if(priomove.find_tactic(PrioMove.TACTICS['tactical-draw'])):
            newcandidates.clear()
            newcandidates.append(None)
            score = 0
        else:
            match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

            score, newcandidates = alphabeta(match, depth + 1, slimits, alpha, beta, not maximizing, priomove, msgs)

            match.undo_move()

        if(maximizing):
            if(score > nodescore):
                nodescore = score
                append_newmove(gmove, nodecandidates, newcandidates)

            if(depth == 1):
                msgs.currentsearch.clear()
                for candidate in nodecandidates:
                    msgs.currentsearch.append(candidate)

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
                msgs.currentsearch.clear()
                for candidate in nodecandidates:
                    msgs.currentsearch.append(candidate)

                prnt_move("\nCURR SEARCH: " + str(score).rjust(8, " ") + " [", gmove, "]")
                prnt_moves("", newcandidates)
                prnt_moves("CANDIDATES:  " + str(nodescore).rjust(8, " "), nodecandidates)
                print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

            beta = min(beta, nodescore)
            if(beta <= alpha):
                break # alpha cut-off

        if(depth == 1):
            huge_diff = (abs(match.score) - abs(nodescore)) > abs(match.SCORES[match.PIECES['wPw']]) * 2
            elapsed_time = time.time() - starttime
            if(elapsed_time > (match.seconds_per_move / maxcnt) * count):
                exceeded = True
            else:
                exceeded = False
        else:
            huge_diff = False
            exceeded = False

        if(msgs.terminate):
            break
        elif(huge_diff and exceeded == False and count <= 24):
            continue
        elif(count >= maxcnt):
            break

    return nodescore, nodecandidates


class Msgs:
    def __init__(self):
        self.created_at = time.time()
        self.terminate = False
        self.currentsearch = []


class SearchLimits:
    def __init__(self, match):
        self.count = 6
        self.dpth_stage1 = 2
        self.dpth_stage2 = 5

        self.setlimits(match)

    def setlimits(self, match):
        if(match.level == match.LEVELS['blitz']):
            self.count = 6
            self.dpth_stage1 = 2
            self.dpth_stage2 = 5
        elif(match.level == match.LEVELS['low']):
            self.count = 8
            self.dpth_stage1 = 3
            self.dpth_stage2 = 6
        elif(match.level == match.LEVELS['medium']):
            self.count = 12
            self.dpth_stage1 = 4
            self.dpth_stage2 = 7
        else:
            self.count = 16
            self.dpth_stage1 = 5
            self.dpth_stage2 = 8


def calc_move(match, msgs):
    print("is opening: " + str(is_opening(match)) + " is endgame: " + str(is_endgame(match)))

    candidates = []
    
    slimits = SearchLimits(match)

    match.time_start = time.time()

    gmove = retrieve_move(match)
    if(gmove is not None):
        candidates.append(gmove)
        score = match.score
    else:
        maximizing = match.next_color() == match.COLORS['white']
        alpha = match.SCORES[match.PIECES['wKg']] * 10
        beta = match.SCORES[match.PIECES['bKg']] * 10 
        score, candidates = alphabeta(match, 1, slimits, alpha, beta, maximizing, None, msgs)

    ### time
    elapsed_time = time.time() - match.time_start
    if(match.next_color() == match.COLORS['white']):
        match.white_elapsed_seconds += elapsed_time
    else:
        match.black_elapsed_seconds += elapsed_time

    match.time_start = time.time()
    ###

    msg = "result: " + str(score) + " match: " + str(match.begin) + " "
    prnt_moves(msg, candidates)
    prnt_fmttime("\ncalc-time: ", elapsed_time)
    return candidates

