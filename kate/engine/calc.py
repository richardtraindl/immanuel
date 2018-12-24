import time, copy
from operator import attrgetter
from .values import *
from .match import *
from .move import *
from .openings import retrieve_move
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


class SearchLimits:
    def __init__(self, match):
        if(match.level == match.LEVELS['blitz']):
            self.mvcnt = 6
            self.dpth_stage1 = 2
            self.dpth_stage2 = 5
            self.dpth_max = 8
        elif(match.level == match.LEVELS['low']):
            self.mvcnt = 8
            self.dpth_stage1 = 3
            self.dpth_stage2 = 6
            self.dpth_max = 10
        elif(match.level == match.LEVELS['medium']):
            self.mvcnt = 12
            self.dpth_stage1 = 3
            self.dpth_stage2 = 7
            self.dpth_max = 12
        elif(match.level == match.LEVELS['high']):
            self.mvcnt = 16
            self.dpth_stage1 = 3
            self.dpth_stage2 = 8
            self.dpth_max = 12
        else:                       # level debug
            self.mvcnt = 120
            self.dpth_stage1 = 1
            self.dpth_stage2 = 1
            self.dpth_max = 1

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


def resort_for_stormy_moves(priomoves, new_prio, last_pmove_capture_bad_deal, with_check):
    if(last_pmove_capture_bad_deal == False):
        return
    count_of_stormy = 0
    count_of_bad_captures = 0
    first_silent = None
    for priomove in priomoves:
        if(priomove.is_tactic_stormy(with_check)):
            count_of_stormy += 1
            priomove.prio = min(priomove.prio, new_prio - 2)
        elif(priomove.has_tactic_ext(cTactic(cPrioMove.TACTICS['captures'], cPrioMove.SUB_TACTICS['bad-deal']))):
            count_of_bad_captures += 1
            priomove.upgrade(priomove.TACTICS['captures'])
            priomove.prio = min(priomove.prio, new_prio)
        else:
            if(first_silent is None):
                first_silent = priomove
    if(count_of_bad_captures > 0 and count_of_stormy == 0 and first_silent):
        first_silent.prio = min(first_silent.prio, new_prio - 1)
    priomoves.sort(key=attrgetter('prio'))


def select_maxcount(match, priomoves, depth, slimits, last_pmove):
    if(len(priomoves) == 0 or depth > slimits.dpth_max):
        return 0

    if(priomoves[0].has_domain_tactic(cPrioMove.TACTICS['defends-check'])):
        return len(priomoves)

    if(last_pmove and last_pmove.has_tactic_ext(cTactic(cPrioMove.TACTICS['captures'], cPrioMove.SUB_TACTICS['bad-deal']))):
        last_pmove_capture_bad_deal = True
    else:
        last_pmove_capture_bad_deal = False

    """if(match.next_color() == COLORS['white']):
        cking = cKing(match, match.board.bKg_x, match.board.bKg_y)
    else:
        cking = cKing(match, match.board.wKg_x, match.board.wKg_y)
    with_check = not cking.is_safe()"""
    with_check = False

    if(depth <= slimits.dpth_stage1):
        resort_for_stormy_moves(priomoves, cPrioMove.PRIO['prio1'], last_pmove_capture_bad_deal, with_check)
        count = count_up_to_prio(priomoves, cPrioMove.PRIO['prio2'])
        if(count < slimits.mvcnt):
            return min(slimits.mvcnt, len(priomoves))
        else:
            if(match.level == match.LEVELS['blitz']):
                return slimits.mvcnt
            else:
                return count
    else:
        resort_for_stormy_moves(priomoves, cPrioMove.PRIO['prio1'], last_pmove_capture_bad_deal, with_check)
        return count_up_to_prio(priomoves, cPrioMove.PRIO['prio1'])


def alphabeta(match, depth, slimits, alpha, beta, maximizing, last_pmove):
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
    priomoves, piecescnt = cgenerator.generate_priomoves()
    rank_gmoves(match, priomoves, piecescnt, last_pmove)
    maxcnt = select_maxcount(match, priomoves, depth, slimits, last_pmove)

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
                newscore, newcandidates = alphabeta(match, depth + 1, slimits, maxscore, beta, False, priomove)
            else:
                newscore, newcandidates = alphabeta(match, depth + 1, slimits, alpha, minscore, True, priomove)
            match.undo_move()

        if(depth == 1):
            prnt_search(match, "CURRENT SEARCH: ", newscore, gmove, newcandidates)

        if(maximizing):
            if(newscore > maxscore):
                maxscore = newscore
                if(maxscore >= beta):
                    break # beta cut-off
                else:
                    append_newmove(gmove, candidates, newcandidates)
                    if(depth == 1):
                        prnt_search(match, "CANDIDATE:      ", maxscore, None, candidates)
        else:
            if(newscore < minscore):
                minscore = newscore
                if(minscore <= alpha):
                    break # alpha cut-off
                else:
                    append_newmove(gmove, candidates, newcandidates)
                    if(depth == 1):
                        prnt_search(match, "CANDIDATE:      ", minscore, None, candidates)

        if(depth == 1):
            if(color == COLORS['white']):
                huge_diff = maxscore < match.score + (SCORES[PIECES['wPw']] * 2)
            else:
                huge_diff = minscore > match.score + (SCORES[PIECES['bPw']] * 2)
            #elapsed_time = time.time() - starttime
            #exceeded = elapsed_time > match.seconds_per_move
            exceeded = False
        else:
            huge_diff = False
            exceeded = False
        if(huge_diff and exceeded == False and count < maxcnt + 6):
            continue
        if(count >= maxcnt):
            break

    if(maximizing):
        return maxscore, candidates
    else:
        return minscore, candidates


def calc_move(match):
    if(match.is_opening()):
        msg = "is opening"
    elif(match.is_endgame()):
        msg = "is endgame"
    else:
        msg = "is middlegame"
    print(msg)

    candidates = []
    slimits = SearchLimits(match)
    match.time_start = time.time()
    gmove = None

    if(match.is_opening()):
        gmove = retrieve_move(match)

    if(gmove is not None):
        candidates.append(gmove)
        score = match.score
    else:
        maximizing = match.next_color() == COLORS['white']
        alpha = SCORES[PIECES['wKg']] * 10
        beta = SCORES[PIECES['bKg']] * 10 
        score, candidates = alphabeta(match, 1, slimits, alpha, beta, maximizing, None)

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

