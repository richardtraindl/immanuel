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


def prnt_before_calc(match, count, priomove):
    print("\n***********************************************")
    print("match: " + str(match.begin))
    print("count: " + str(count))
    print("calculate: " + priomove.gmove.format_genmove())
    print("tactics: " + priomove.concat_tactics(" | "))
    print("priorities: " + reverse_lookup(priomove.PRIO, priomove.prio) + " | " + reverse_lookup(priomove.PRIO, priomove.prio_sec))

def prnt_after_calc(match, gmove, score, newcandidates, nodecandidates, nodescore):
    print("CURR SEARCH: " + str(score).rjust(8, " ") + \
          " [" + gmove.format_genmove() + "] " + concat_fmt_gmoves(newcandidates))
    print("CANDIDATES:  " + str(nodescore).rjust(8, " ") + concat_fmt_gmoves(nodecandidates))

def concat_fmt_gmoves(gmoves):
    str_gmoves = ""
    for gmove in gmoves:
        if(gmove):
            str_gmoves += " [" + gmove.format_genmove() + "] "
    return str_gmoves

def prnt_priomoves(priomoves):
    for priomove in priomoves:
        print("\n" + priomove.gmove.format_genmove(), end=" ")
        priomove.prnt_tactics()

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
        return max(slimits.first_count, count_up_to_prio(priomoves, PrioMove.PRIO['prio5']))
    elif(depth <= slimits.dpth_stage2):
        return max(slimits.count, count_up_to_prio(priomoves, PrioMove.PRIO['prio5']))
    elif(depth <= slimits.dpth_stage3): # and (last_pmove.is_tactic_stormy() or is_stormy(match))):
        count = 0
        silent_move_cnt = 0

        for priomove in priomoves:
            if(priomove.is_tactic_stormy()):
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
        return min(slimits.count, count)
    elif(last_pmove.is_tactic_urgent()):
        count = 0
        silent_move_cnt = 0

        for priomove in priomoves:
            if(priomove.find_tactic(PrioMove.TACTICS['promotion']) or #defend-check
               priomove.find_tactic(PrioMove.TACTICS['capture-good-deal'])):
                count += 1
                priomove.prio = PrioMove.PRIO['prio2']
                continue
            elif(priomove.find_tactic(PrioMove.TACTICS['capture-bad-deal'])):
                count += 1
                priomove.prio = PrioMove.PRIO['prio3']
                continue
            elif(silent_move_cnt < 1 and priomove.is_tactic_silent()):
                count += 1
                silent_move_cnt += 1
                priomove.prio = PrioMove.PRIO['prio1']
                continue
            else:
                priomove.prio = PrioMove.PRIO['prio10']

        priomoves.sort(key=attrgetter('prio'))
        return min(slimits.count, count)
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

    rank_gmoves(match, priomoves)    
    
    if(depth <= 12):
        maxcnt = select_maxcount(match, priomoves, depth, slimits, last_pmove)
    else:
        nodecandidates.append(None)
        return score_position(match, len(priomoves)), nodecandidates

    if(depth == 1):
        print("************ maxcnt: " + str(maxcnt) + " ******************")
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
            prnt_before_calc(match, count, priomove)

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

                prnt_after_calc(match, gmove, score, newcandidates, nodecandidates, nodescore)

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

                prnt_after_calc(match, gmove, score, newcandidates, nodecandidates, nodescore)

            beta = min(beta, nodescore)
            if(beta <= alpha):
                break # alpha cut-off

        if(depth == 1):
            diff = match.score + nodescore
            diff_limit = abs(match.SCORES[match.PIECES['wPw']]) * 2
            huge_diff = diff > diff_limit
            elapsed_time = time.time() - starttime
            exceeded = elapsed_time > match.seconds_per_move
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
        if(match.level == match.LEVELS['blitz']):
            self.first_count = 12
            self.count = 6
            self.dpth_stage1 = 1
            self.dpth_stage2 = 2
            self.dpth_stage3 = 5
        elif(match.level == match.LEVELS['low']):
            self.first_count = 12
            self.count = 8
            self.dpth_stage1 = 1
            self.dpth_stage2 = 3
            self.dpth_stage3 = 6
        elif(match.level == match.LEVELS['medium']):
            self.first_count = 16
            self.count = 12
            self.dpth_stage1 = 1
            self.dpth_stage2 = 4
            self.dpth_stage3 = 7
        else:
            self.first_count = 20
            self.count = 16
            self.dpth_stage1 = 1
            self.dpth_stage2 = 5
            self.dpth_stage3 = 8


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
    print(msg + concat_fmt_gmoves(candidates))
    prnt_fmttime("\ncalc-time: ", elapsed_time)
    return candidates

