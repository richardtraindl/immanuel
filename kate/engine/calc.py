import time, copy
from operator import attrgetter
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
    print("priorities: " + reverse_lookup(priomove.PRIO, priomove.prio) + " | " + reverse_lookup(priomove.PRIO, priomove.prio_sec))

def prnt_after_calc(match, gmove, score, newcandidates, nodecandidates, nodescore):
    print("CURR SEARCH: " + str(score).rjust(8, " ") + \
          " [" + gmove.format_genmove() + "] " + concat_fmt_gmoves(match, newcandidates))
    print("CANDIDATES:  " + str(nodescore).rjust(8, " ") + concat_fmt_gmoves(match, nodecandidates))

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
            self.move_count = 6
            self.dpth_stage1 = 2
            self.dpth_stage2 = 5
            self.dpth_max = 10
        elif(match.level == match.LEVELS['low']):
            self.move_count = 8
            self.dpth_stage1 = 2
            self.dpth_stage2 = 6
            self.dpth_max = 10
        elif(match.level == match.LEVELS['medium']):
            self.move_count = 12
            self.dpth_stage1 = 3
            self.dpth_stage2 = 7
            self.dpth_max = 12
        else:
            self.move_count = 16
            self.dpth_stage1 = 3
            self.dpth_stage1 = 8
            self.dpth_max = 12
# class end

def append_newmove(gmove, nodecandidates, newcandidates):
    nodecandidates.clear()
    nodecandidates.append(gmove)

    for newcandidate in newcandidates:
        if(newcandidate):
            nodecandidates.append(newcandidate)
        else:
            break

def count_up_to_prio(priomoves, prio_limit):
    count = 0

    for priomove in priomoves:
        if(priomove.prio <= prio_limit):
            count += 1

    return count
    
def select_maxcount(match, priomoves, depth, slimits, last_pmove):
    if(len(priomoves) == 0):
        return 0
    
    if(priomoves[0].has_tactic(cTactic(PrioMove.TACTICS['defend-check'], PrioMove.SUB_TACTICS['undefined']))):
        return len(priomoves)

    #is_position_stormy = analyze_position.is_stormy(match)

    if(depth <= slimits.dpth_stage2 and last_pmove and last_pmove.is_tactic_stormy()):
        count = 0
        silent_move_cnt = 0

        for priomove in priomoves:
            if(priomove.is_tactic_stormy()):
                count += 1
                priomove.prio = min(priomove.prio, PrioMove.PRIO['prio2'])
            elif(silent_move_cnt == 0 and priomove.is_tactic_silent()):
                count += 1
                silent_move_cnt += 1
                priomove.prio = min(priomove.prio, PrioMove.PRIO['prio1'])
            else:
                if(depth <= slimits.dpth_stage1 and priomove.prio <= PrioMove.PRIO['prio5']):
                    count += 1
                elif(depth <= slimits.dpth_stage2 and priomove.prio <= PrioMove.PRIO['prio4']):
                    count += 1

        priomoves.sort(key=attrgetter('prio'))
        return count
    elif(depth <= slimits.dpth_stage1):
        return max(slimits.move_count, count_up_to_prio(priomoves, PrioMove.PRIO['prio5']))
    elif(depth <= slimits.dpth_stage2):
        return max(slimits.move_count, count_up_to_prio(priomoves, PrioMove.PRIO['prio4']))
    elif(depth <= slimits.dpth_max and last_pmove.is_tactic_urgent()):
        count = 0
        silent_move_cnt = 0
        bad_capture = last_pmove.has_tactic_ext(cTactic(PrioMove.TACTICS['capture'], PrioMove.SUB_TACTICS['bad-deal']))

        for priomove in priomoves:
            if(bad_capture):
                if(priomove.has_tactic(cTactic(PrioMove.TACTICS['promotion'], PrioMove.SUB_TACTICS['undefined'])) or
                   priomove.has_tactic(cTactic(PrioMove.TACTICS['capture'], PrioMove.SUB_TACTICS['undefined']))):
                    count += 1
                    priomove.prio = min(priomove.prio, PrioMove.PRIO['prio2'])
                elif(silent_move_cnt < 1 and priomove.is_tactic_silent()):
                    count += 1
                    silent_move_cnt += 1
                    priomove.prio = min(priomove.prio, PrioMove.PRIO['prio1'])
                else:
                    priomove.prio = PrioMove.PRIO['prio10']
            else:
                if(priomove.has_tactic(cTactic(PrioMove.TACTICS['promotion'], PrioMove.SUB_TACTICS['undefined'])) or
                   priomove.has_tactic_ext(cTactic(PrioMove.TACTICS['capture'], PrioMove.SUB_TACTICS['good-deal']))):
                    count += 1
                    priomove.prio = min(priomove.prio, PrioMove.PRIO['prio2'])
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
        nodescore = alpha
    else:
        nodescore = beta

    cgenerator = cGenerator(match)
    priomoves = cgenerator.generate_moves()

    rank_gmoves(match, priomoves)    
    
    maxcnt = select_maxcount(match, priomoves, depth, slimits, last_pmove)

    if(depth == 1):
        print("************ maxcnt: " + str(maxcnt) + " ******************")
        prnt_priomoves(match, priomoves)

        if(len(priomoves) == 1):
            pmove = priomoves[0]
            nodecandidates.append(pmove.gmove)
            nodecandidates.append(None)
            if(pmove.has_tactic(cTactic(PrioMove.TACTICS['tactical-draw'], PrioMove.SUB_TACTICS['undefined']))):
                return 0, nodecandidates
            else:
                return analyze_position.score_position(match, len(priomoves)), nodecandidates

    if(len(priomoves) == 0 or maxcnt == 0):
        nodecandidates.append(None)
        return analyze_position.score_position(match, len(priomoves)), nodecandidates

    for priomove in priomoves:
        gmove = priomove.gmove

        count += 1

        if(depth == 1):
            prnt_before_calc(match, count, priomove)

        if(priomove.has_tactic(cTactic(PrioMove.TACTICS['tactical-draw'], PrioMove.SUB_TACTICS['undefined']))):
            newcandidates.clear()
            newcandidates.append(None)
            score = 0
        else:
            match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

            if(maximizing):
                score, newcandidates = alphabeta(match, depth + 1, slimits, nodescore, beta, False, priomove, msgs)
            else:
                score, newcandidates = alphabeta(match, depth + 1, slimits, alpha, nodescore, True, priomove, msgs)

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

            #alpha = max(alpha, nodescore)
            if(nodescore >= beta): # if(beta <= alpha):
                return score, nodecandidates
                #break # beta cut-off
        else:
            if(score < nodescore):
                nodescore = score
                append_newmove(gmove, nodecandidates, newcandidates)

            if(depth == 1):
                msgs.currentsearch.clear()
                for candidate in nodecandidates:
                    msgs.currentsearch.append(candidate)

                prnt_after_calc(match, gmove, score, newcandidates, nodecandidates, nodescore)

            #beta = min(beta, nodescore)
            if(nodescore <= alpha): #if(beta <= alpha):
                return score, nodecandidates
                #break # alpha cut-off

        """if(depth == 1):
            diff = match.score + nodescore
            diff_limit = abs(match.SCORES[match.PIECES['wPw']]) * 2
            huge_diff = diff > diff_limit
            elapsed_time = time.time() - starttime
            exceeded = elapsed_time > match.seconds_per_move
        else:
            huge_diff = False
            exceeded = False

        if(msgs.terminate):
            break"""
        #elif(huge_diff and exceeded == False and count <= 24):
            #continue
        if(count >= maxcnt): #elif(count >= maxcnt):
            break

    return nodescore, nodecandidates

"""def alphabeta(match, depth, slimits, alpha, beta, maximizing, last_pmove, msgs):
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
        return analyze_position.score_position(match, len(priomoves)), nodecandidates

    if(depth == 1):
        print("************ maxcnt: " + str(maxcnt) + " ******************")
        prnt_priomoves(match, priomoves)

        if(len(priomoves) == 1):
            pmove = priomoves[0]
            nodecandidates.append(pmove.gmove)
            nodecandidates.append(None)
            if(pmove.has_tactic(cTactic(PrioMove.TACTICS['tactical-draw'], PrioMove.SUB_TACTICS['undefined']))):
                return 0, nodecandidates
            else:
                return analyze_position.score_position(match, len(priomoves)), nodecandidates

    if(len(priomoves) == 0 or maxcnt == 0):
        nodecandidates.append(None)
        return analyze_position.score_position(match, len(priomoves)), nodecandidates

    for priomove in priomoves:
        gmove = priomove.gmove

        count += 1

        if(depth == 1):
            prnt_before_calc(match, count, priomove)

        if(priomove.has_tactic(cTactic(PrioMove.TACTICS['tactical-draw'], PrioMove.SUB_TACTICS['undefined']))):
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
        #elif(huge_diff and exceeded == False and count <= 24):
            #continue
        elif(count >= maxcnt):
            break

    return nodescore, nodecandidates"""

def calc_move(match, msgs):
    print("is opening: " + str(analyze_position.is_opening(match)) + \
          " is endgame: " + str(analyze_position.is_endgame(match)))

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
        match.white_player.elapsed_seconds += elapsed_time
    else:
        match.black_player.elapsed_seconds += elapsed_time

    match.time_start = time.time()
    ###

    msg = "result: " + str(score) + " match: " + str(match.begin) + " "
    print(msg + concat_fmt_gmoves(match, candidates))
    prnt_fmttime("\ncalc-time: ", elapsed_time)
    return candidates

