import time, copy
from operator import attrgetter
from .values import *
from .match import *
from .move import *
from .openingmove import retrieve_move
from .analyze_move import *
from . import analyze_position
from .helper import *
from .validator import *
from .generator import cGenerator


def prnt_before_calc(match, count, priomove):
    print("\n***********************************************")
    print("match: " + str(match.begin))
    print("count: " + str(count))
    print("calculate: " + priomove.gmove.format_genmove())
    print("tactics: " + priomove.concat_tactics(" | "))
    print("priority: " + str(priomove.prio))
    print("\n***********************************************")

def prnt_search(match, label, score, gmove, candidates):
    if(gmove):
        str_gmove = " [" + gmove.format_genmove() + "] "
    else:
        str_gmove = ""
    print(label + str(score).rjust(8, " ") + str_gmove + concat_fmt_gmoves(match, candidates))

def concat_fmt_gmoves(match, gmoves):
    str_gmoves = ""
    for gmove in gmoves:
        if(gmove):
            str_gmoves += " [" + gmove.format_genmove() + "] "
    return str_gmoves

def prnt_priomoves(match, priomoves):
    for priomove in priomoves:
        print("\n" + priomove.gmove.format_genmove() + " prio: " + str(priomove.prio), end=" ")
        priomove.prnt_tactics()

def prnt_fmttime(msg, seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    print( msg + "%02d:%02d:%02d" % (hour, minute, sec))

class Msgs:
    def __init__(self):
        self.created_at = time.time()
        self.terminate = False
        self.currentsearch = []
# class end

class SearchLimits:
    def __init__(self, match):
        if(match.level == match.LEVELS['blitz']):
            self.mvcnt = 8
            self.dpth_stage1 = 2
            self.dpth_stage2 = 6
            self.dpth_max = 8
        elif(match.level == match.LEVELS['low']):
            self.mvcnt = 12
            self.dpth_stage1 = 3
            self.dpth_stage2 = 6
            self.dpth_max = 10
        elif(match.level == match.LEVELS['medium']):
            self.mvcnt = 16
            self.dpth_stage1 = 4
            self.dpth_stage2 = 7
            self.dpth_max = 12
        else:
            self.mvcnt = 20
            self.dpth_stage1 = 4
            self.dpth_stage2 = 8
            self.dpth_max = 12

        if(match.is_endgame()):
            self.dpth_stage1 += 1
            self.dpth_stage2 += 1

# class end

def append_newmove(gmove, candidates, newcandidates):
    candidates.clear()
    candidates.append(gmove)

    for newcandidate in newcandidates:
        if(newcandidate):
            candidates.append(newcandidate)
        else:
            break

def count_up_to_prio(priomoves, prio_limit):
    count = 0
    for priomove in priomoves:
        if(priomove.prio <= prio_limit):
            count += 1
    return count

def resort_for_stormy_moves(priomoves, new_prio, last_pmove_capture_bad_deal, cnt_of_checks_in_stage):
    count_of_stormy = 0
    count_of_bad_captures = 0
    first_silent = None
    for priomove in priomoves:
        if(priomove.is_tactic_stormy(cnt_of_checks_in_stage)):
            count_of_stormy += 1
            priomove.prio = min(priomove.prio, new_prio - 2)
        elif(last_pmove_capture_bad_deal):
            if(priomove.has_tactic_ext(cTactic(cPrioMove.TACTICS['captures'], cPrioMove.SUB_TACTICS['bad-deal']))):
                count_of_bad_captures += 1
                priomove.prio = min(priomove.prio, new_prio)
        else:
            if(first_silent is None):
                first_silent = priomove
    if(count_of_bad_captures > 0 and count_of_stormy == 0 and first_silent):
        first_silent.prio = min(first_silent.prio, new_prio - 1)
    priomoves.sort(key=attrgetter('prio'))

def select_maxcount(match, priomoves, depth, slimits, last_pmove, cnt_of_checks_in_stage):
    if(len(priomoves) == 0 or depth > slimits.dpth_max):
        return 0

    if(priomoves[0].has_domain_tactic(cPrioMove.TACTICS['defends-check'])):
        return len(priomoves)

    if(last_pmove and last_pmove.has_tactic_ext(cTactic(cPrioMove.TACTICS['captures'], cPrioMove.SUB_TACTICS['bad-deal']))):
        last_pmove_capture_bad_deal = True
    else:
        last_pmove_capture_bad_deal = False

    if(depth <= slimits.dpth_stage1):
        resort_for_stormy_moves(priomoves, 25, last_pmove_capture_bad_deal, cnt_of_checks_in_stage)
        count = count_up_to_prio(priomoves, 25)
        if(count == 0):
            return min(slimits.mvcnt, len(priomoves))
        else:
            return count
    elif(depth <= slimits.dpth_stage2):
        resort_for_stormy_moves(priomoves, 15, last_pmove_capture_bad_deal, cnt_of_checks_in_stage)
        return count_up_to_prio(priomoves, 15)
    else:
        resort_for_stormy_moves(priomoves, 6, last_pmove_capture_bad_deal, None)
        return count_up_to_prio(priomoves, 6)

def alphabeta(match, depth, slimits, alpha, beta, maximizing, last_pmove, cnt_of_checks_in_stage, msgs):
    color = match.next_color()
    candidates = []
    newcandidates = []
    count = 0
    starttime = time.time()

    if(maximizing):
        maxscore = alpha
    else:
        minscore = beta

    cgenerator = cGenerator(match)
    priomoves, piecescnt = cgenerator.generate_moves(1)
    rank_gmoves(match, priomoves, piecescnt, last_pmove)
    maxcnt = select_maxcount(match, priomoves, depth, slimits, last_pmove, cnt_of_checks_in_stage)

    if(depth == 1):
        print("************ maxcnt: " + str(maxcnt) + " ******************")
        prnt_priomoves(match, priomoves)

        if(len(priomoves) == 1):
            pmove = priomoves[0]
            candidates.append(pmove.gmove)
            candidates.append(None)
            if(pmove.has_domain_tactic(cPrioMove.TACTICS['is-tactical-draw'])):
                return 0, candidates
            else:
                return analyze_position.score_position(match, len(priomoves)), candidates

    if(len(priomoves) == 0 or maxcnt == 0):
        candidates.append(None)
        return analyze_position.score_position(match, len(priomoves)), candidates

    for priomove in priomoves:
        if(depth <= slimits.dpth_stage1):
            cnt_of_checks_in_stage = 0        
        elif(priomove.has_domain_tactic(cPrioMove.TACTICS['attacks-king'])):
            cnt_of_checks_in_stage += 1

        gmove = priomove.gmove
        count += 1

        if(depth == 1):
            prnt_before_calc(match, count, priomove)

        if(priomove.has_domain_tactic(cPrioMove.TACTICS['is-tactical-draw'])):
            newcandidates.clear()
            newcandidates.append(None)
            newscore = 0
        else:
            match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

            if(maximizing):
                newscore, newcandidates = alphabeta(match, depth + 1, slimits, maxscore, beta, False, priomove, cnt_of_checks_in_stage, msgs)
            else:
                newscore, newcandidates = alphabeta(match, depth + 1, slimits, alpha, minscore, True, priomove, cnt_of_checks_in_stage, msgs)

            match.undo_move()

        if(maximizing):
            if(newscore > maxscore):
                maxscore = newscore
                append_newmove(gmove, candidates, newcandidates)
                if(maxscore >= beta):
                    if(depth == 1):
                        prnt_search(match, "CURRENT SEARCH CUTOFF: ", -999, gmove, newcandidates)
                        prnt_search(match, "CANDIDATE:             ", maxscore, None, candidates)
                    break # beta cut-off

            if(depth == 1):
                prnt_search(match, "CURRENT SEARCH: ", newscore, gmove, newcandidates)
                prnt_search(match, "CANDIDATE:      ", maxscore, None, candidates)
                msgs.currentsearch.clear()
                for candidate in candidates:
                    msgs.currentsearch.append(candidate)

        else:
            if(newscore < minscore):
                minscore = newscore
                append_newmove(gmove, candidates, newcandidates)
                if(minscore <= alpha):
                    if(depth == 1):
                        prnt_search(match, "CURRENT SEARCH CUTOFF: ", 999, gmove, newcandidates)
                        prnt_search(match, "CANDIDATE:             ", minscore, None, candidates)
                    break # alpha cut-off

            if(depth == 1):
                prnt_search(match, "CURRENT SEARCH: ", newscore, gmove, newcandidates)
                prnt_search(match, "CANDIDATE:      ", minscore, None, candidates)
                msgs.currentsearch.clear()
                for candidate in candidates:
                    msgs.currentsearch.append(candidate)

        #if(depth == 1):
        #    diff = match.score + newscore
        #    diff_limit = abs(match.SCORES[PIECES['wPw']]) * 2
        #    huge_diff = diff > diff_limit
        #    elapsed_time = time.time() - starttime
        #    exceeded = elapsed_time > match.seconds_per_move
        #else:
        #    huge_diff = False
        #    exceeded = False

        #if(huge_diff and exceeded == False and count <= 24):
            #continue
        if(count >= maxcnt):
            break
        if(msgs.terminate):
            break

    if(maximizing):
        return maxscore, candidates
    else:
        return minscore, candidates

def calc_move(match, msgs):
    print("is opening: " + str(match.is_opening()) + \
          " is endgame: " + str(match.is_endgame()))

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
        score, candidates = alphabeta(match, 1, slimits, alpha, beta, maximizing, None, 0, msgs)

    ### time
    elapsed_time = time.time() - match.time_start
    if(match.next_color() == COLORS['white']):
        match.white_player.elapsed_seconds += elapsed_time
    else:
        match.black_player.elapsed_seconds += elapsed_time

    match.time_start = time.time()
    ###

    msg = "result: " + str(score) + " match: " + str(match.begin) + " "
    print(msg + concat_fmt_gmoves(match, candidates))
    prnt_fmttime("\ncalc-time: ", elapsed_time)
    return candidates

