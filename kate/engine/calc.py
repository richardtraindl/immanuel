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
            self.mvcnt_stage1 = 8
            self.mvcnt_stage2 = 8
            self.dpth_stage1 = 1
            self.dpth_stage2 = 3
            self.dpth_max = 10
        elif(match.level == match.LEVELS['low']):
            self.mvcnt_stage1 = 12
            self.mvcnt_stage2 = 8
            self.dpth_stage1 = 2
            self.dpth_stage2 = 5
            self.dpth_max = 10
        elif(match.level == match.LEVELS['medium']):
            self.mvcnt_stage1 = 16
            self.mvcnt_stage2 = 12
            self.dpth_stage1 = 3
            self.dpth_stage2 = 6
            self.dpth_max = 12
        else:
            self.mvcnt_stage1 = 20
            self.mvcnt_stage2 = 12
            self.dpth_stage1 = 4
            self.dpth_stage2 = 7
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

def resort_if_last_move_is_bad_capture(priomoves, last_pmove, new_prio):
    if(last_pmove and last_pmove.has_tactic(cTactic(cPrioMove.TACTICS['capture'], cPrioMove.SUB_TACTICS['bad-deal']))):
        good_capture_moves = []
        bad_capture_moves = []
        silent_moves = []
        for priomove in priomoves:
            if(priomove.has_domain_tactic(cPrioMove.TACTICS['capture'])):
                if(priomove.has_subtactic('bad-deal')):
                    bad_capture_moves.append(priomove)
                else:
                    good_capture_moves.append(priomove)
            else:
                silent_moves.append(priomove)
        if(len(good_capture_moves) == 0 and len(bad_capture_moves) > 0):
            for bad_capture_move in bad_capture_moves:
                bad_capture_move.prio = min(bad_capture_move.prio, new_prio)
            if(len(silent_moves) > 0):
                silent_moves[0].prio = min(silent_moves[0].prio, new_prio - 1)
            priomoves.sort(key=attrgetter('prio'))

def resort_if_last_move_is_capture(priomoves, last_pmove, new_prio):
    challenge = False
    if(last_pmove and last_pmove.has_domain_tactic(cPrioMove.TACTICS['capture'])):
        good_capture_moves = []
        bad_capture_moves = []
        silent_moves = []
        last_pmove_is_bad_deal = last_pmove.has_subtactic('bad-deal')
        for priomove in priomoves:
            if(priomove.has_domain_tactic(cPrioMove.TACTICS['capture'])):
                if(priomove.has_subtactic('bad-deal')):
                    if(last_pmove_is_bad_deal):
                        priomove.prio = min(priomove.prio, new_prio)
                        bad_capture_moves.append(priomove)
                        challenge = True
                else:
                    priomove.prio = min(priomove.prio, new_prio - 2)
                    good_capture_moves.append(priomove)
                    challenge = True
            else:
                priomove.prio = min(priomove.prio, cPrioMove.PRIO['prio5'])
                silent_moves.append(priomove)
        if(last_pmove_is_bad_deal):
            silent_moves[0].prio = min(silent_moves[0].prio, new_prio - 1)
    return challenge

def select_maxcount(match, priomoves, depth, slimits, last_pmove):
    if(len(priomoves) == 0 or depth > slimits.dpth_max):
        return 0

    if(priomoves[0].has_domain_tactic(cPrioMove.TACTICS['defend-check'])):
        return len(priomoves)

    if(depth <= slimits.dpth_stage1):
        resort_if_last_move_is_bad_capture(priomoves, last_pmove, 25)
        count = count_up_to_prio(priomoves, 25)
        if(count == 0):
            return min(slimits.mvcnt_stage1, len(priomoves))
        else:
            return min(slimits.mvcnt_stage1, count)
    elif(depth <= slimits.dpth_stage2):
        resort_if_last_move_is_bad_capture(priomoves, last_pmove, 20)
        count = count_up_to_prio(priomoves, 20)
        if(count == 0):
            return min(slimits.mvcnt_stage2, len(priomoves))
        else:
            return min(slimits.mvcnt_stage2, count)
    elif(depth <= slimits.dpth_max):
        if(resort_if_last_move_is_capture(priomoves, last_pmove, 15)):
            return count_up_to_prio(priomoves, 15)
        else:
            return 0
    else:
        return 0

def alphabeta(match, depth, slimits, alpha, beta, maximizing, last_pmove, msgs):
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
    priomoves, piececnt = cgenerator.generate_moves(1)
    rank_gmoves(match, priomoves, piececnt)    
    maxcnt = select_maxcount(match, priomoves, depth, slimits, last_pmove)
    priomoves.sort(key=attrgetter('prio'))

    if(depth == 1):
        print("************ maxcnt: " + str(maxcnt) + " ******************")
        prnt_priomoves(match, priomoves)

        if(len(priomoves) == 1):
            pmove = priomoves[0]
            candidates.append(pmove.gmove)
            candidates.append(None)
            if(pmove.has_domain_tactic(cPrioMove.TACTICS['tactical-draw'])):
                return 0, candidates
            else:
                return analyze_position.score_position(match, len(priomoves)), candidates

    if(len(priomoves) == 0 or maxcnt == 0):
        candidates.append(None)
        return analyze_position.score_position(match, len(priomoves)), candidates

    for priomove in priomoves:
        gmove = priomove.gmove

        count += 1

        if(depth == 1):
            prnt_before_calc(match, count, priomove)

        if(priomove.has_domain_tactic(cPrioMove.TACTICS['tactical-draw'])):
            newcandidates.clear()
            newcandidates.append(None)
            newscore = 0
        else:
            match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

            if(maximizing):
                newscore, newcandidates = alphabeta(match, depth + 1, slimits, maxscore, beta, False, priomove, msgs)
            else:
                newscore, newcandidates = alphabeta(match, depth + 1, slimits, alpha, minscore, True, priomove, msgs)

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
        elif(msgs.terminate):
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
        score, candidates = alphabeta(match, 1, slimits, alpha, beta, maximizing, None, msgs)

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

