import time, copy
from operator import attrgetter
from .values import *
from .match import *
from .move import *
from .openingmove import retrieve_move
from .analyze_move import *
from .analyze_position import score_position
from .helper import *
from .validator import *
from .generator import cGenerator


def prnt_before_calc(match, count, priomove):
    print("\n***********************************************")
    print("match: " + str(match.begin))
    print("count: " + str(count))
    print("calculate: " + priomove.gmove.format_genmove())
    print("tactics: " + priomove.concat_tactics(" | "))
    #print("priorities: " + reverse_lookup(priomove.PRIO, priomove.prio))
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
        print("\n" + priomove.gmove.format_genmove(), end=" ")
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
            self.move_count = 16
            self.dpth_stage1 = 2
            self.dpth_stage2 = 2
            self.dpth_max = 10
        elif(match.level == match.LEVELS['low']):
            self.move_count = 16
            self.dpth_stage1 = 3
            self.dpth_stage2 = 3
            self.dpth_max = 10
        elif(match.level == match.LEVELS['medium']):
            self.move_count = 20
            self.dpth_stage1 = 4
            self.dpth_stage2 = 4
            self.dpth_max = 12
        else:
            self.move_count = 24
            self.dpth_stage1 = 5
            self.dpth_stage2 = 5
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
    silent = True

    for priomove in priomoves:
        if(priomove.prio <= prio_limit):
            count += 1
            if(priomove.has_subtactic(cPrioMove.SUB_TACTICS['bad-deal']) == False):
                silent = False
        if(silent and priomove.has_subtactic(cPrioMove.SUB_TACTICS['bad-deal']) == False):
            count += 1
            silent = False
            priomove.prio = min(priomove.prio, prio_limit)
    priomoves.sort(key=attrgetter('prio'))
    return count

def select_maxcount_new(match, priomoves, depth, slimits, last_pmove):
    if(len(priomoves) == 0):
        return 0
    
    if(priomoves[0].has_tactic(cTactic(cPrioMove.TACTICS['defend-check'], cPrioMove.SUB_TACTICS['undefined']))):
        return len(priomoves)

    if(depth <= slimits.dpth_stage1):
        return max(slimits.move_count, count_up_to_prio(priomoves, cPrioMove.PRIO['prio5']))
        """if(match.level == match.LEVELS['blitz']):
            return min(slimits.move_count, count_up_to_prio(priomoves, cPrioMove.PRIO['prio5']))
        else:
            return max(slimits.move_count, count_up_to_prio(priomoves, cPrioMove.PRIO['prio5']))"""
    elif(depth <= slimits.dpth_stage2):
        return max(slimits.move_count, count_up_to_prio(priomoves, cPrioMove.PRIO['prio4']))
    elif(depth <= slimits.dpth_max):
        promotion = []
        good_captures = []
        bad_captures = []
        silent = None
        eval_movecnt = last_pmove.is_tactic_urgent()

        bad_capture = last_pmove.has_tactic_ext(cTactic(cPrioMove.TACTICS['capture'], cPrioMove.SUB_TACTICS['bad-deal']))

        for priomove in priomoves:
            if(priomove.has_tactic(cTactic(cPrioMove.TACTICS['promotion'], cPrioMove.SUB_TACTICS['undefined']))):
                priomove.prio = min(priomove.prio, cPrioMove.PRIO['prio2'])
                promotion.append(priomove)
                eval_movecnt = True
            elif(priomove.has_tactic_ext(cTactic(cPrioMove.TACTICS['capture'], cPrioMove.SUB_TACTICS['good-deal']))):
                priomove.prio = min(priomove.prio, cPrioMove.PRIO['prio2'])
                good_captures.append(priomove)
                eval_movecnt = True
            elif(priomove.has_tactic_ext(cTactic(cPrioMove.TACTICS['capture'], cPrioMove.SUB_TACTICS['bad-deal']))):
                priomove.prio = min(priomove.prio, cPrioMove.PRIO['prio3'])
                bad_captures.append(priomove)
                eval_movecnt = True
            else:
                priomove.prio = cPrioMove.PRIO['prio5']
                if(silent is None):
                    silent = priomove

        if(eval_movecnt == False):
            return 0
        elif((len(promotion) + len(good_captures)) > 0):
            priomoves.sort(key=attrgetter('prio'))
            return (len(promotion) + len(good_captures))
        else:
            if(bad_capture and len(bad_captures) > 0):
                if(silent):
                    silent.prio = cPrioMove.PRIO['prio1']
                    priomoves.sort(key=attrgetter('prio'))
                    return (len(bad_captures) + 1)
                else:
                    priomoves.sort(key=attrgetter('prio'))
                    return (len(bad_captures))
            else:
                return 0
    else:
        return 0

def select_maxcount(match, priomoves, depth, slimits, last_pmove):
    if(len(priomoves) == 0):
        return 0
    
    if(priomoves[0].has_tactic(cTactic(cPrioMove.TACTICS['defend-check'], cPrioMove.SUB_TACTICS['undefined']))):
        return len(priomoves)

    if(depth <= slimits.dpth_stage1):
        if(match.level == match.LEVELS['blitz']):
            return min(slimits.move_count, count_up_to_prio(priomoves, cPrioMove.PRIO['prio5']))
        else:
            return max(slimits.move_count, count_up_to_prio(priomoves, cPrioMove.PRIO['prio5']))
    elif(depth <= slimits.dpth_stage2):
        return min(slimits.move_count, count_up_to_prio(priomoves, cPrioMove.PRIO['prio4']))
    elif(depth <= slimits.dpth_max and last_pmove.is_tactic_urgent()):
        promotion = []
        good_captures = []
        bad_captures = []
        silent = None

        bad_capture = last_pmove.has_tactic_ext(cTactic(cPrioMove.TACTICS['capture'], cPrioMove.SUB_TACTICS['bad-deal']))

        for priomove in priomoves:
            if(priomove.has_tactic(cTactic(cPrioMove.TACTICS['promotion'], cPrioMove.SUB_TACTICS['undefined']))):
                priomove.prio = min(priomove.prio, cPrioMove.PRIO['prio2'])
                promotion.append(priomove)
            elif(priomove.has_tactic_ext(cTactic(cPrioMove.TACTICS['capture'], cPrioMove.SUB_TACTICS['good-deal']))):
                priomove.prio = min(priomove.prio, cPrioMove.PRIO['prio2'])
                good_captures.append(priomove)
            elif(priomove.has_tactic_ext(cTactic(cPrioMove.TACTICS['capture'], cPrioMove.SUB_TACTICS['bad-deal']))):
                priomove.prio = min(priomove.prio, cPrioMove.PRIO['prio3'])
                bad_captures.append(priomove)
            else:
                priomove.prio = cPrioMove.PRIO['prio5']
                if(silent is None):
                    silent = priomove

        if((len(promotion) + len(good_captures)) > 0):
            priomoves.sort(key=attrgetter('prio'))
            return (len(promotion) + len(good_captures))
        else:
            if(bad_capture and len(bad_captures) > 0):
                if(silent):
                    silent.prio = cPrioMove.PRIO['prio1']
                    priomoves.sort(key=attrgetter('prio'))
                    return (len(bad_captures) + 1)
                else:
                    priomoves.sort(key=attrgetter('prio'))
                    return (len(bad_captures))
            else:
                return 0
    elif(depth <= slimits.dpth_max):
        count = 0
        for priomove in priomoves:
            if(priomove.is_tactic_urgent()): #_v2
                priomove.prio = min(priomove.prio, cPrioMove.PRIO['prio2'])
            else:
                priomove.prio = cPrioMove.PRIO['prio5']
        return count
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
    priomoves, piecescnt = cgenerator.generate_moves(1)

    rank_gmoves(match, priomoves, piecescnt)    
    
    maxcnt = select_maxcount(match, priomoves, depth, slimits, last_pmove)

    if(depth == 1):
        print("************ maxcnt: " + str(maxcnt) + " ******************")
        prnt_priomoves(match, priomoves)

        if(len(priomoves) == 1):
            pmove = priomoves[0]
            candidates.append(pmove.gmove)
            candidates.append(None)
            if(pmove.has_tactic(cTactic(cPrioMove.TACTICS['tactical-draw'], cPrioMove.SUB_TACTICS['undefined']))):
                return 0, candidates
            else:
                return score_position(match, len(priomoves)), candidates

    if(len(priomoves) == 0 or maxcnt == 0):
        candidates.append(None)
        return score_position(match, len(priomoves)), candidates

    for priomove in priomoves:
        gmove = priomove.gmove

        count += 1

        if(depth == 1):
            prnt_before_calc(match, count, priomove)

        if(priomove.has_tactic(cTactic(cPrioMove.TACTICS['tactical-draw'], cPrioMove.SUB_TACTICS['undefined']))):
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

