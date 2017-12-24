import time
from operator import itemgetter
import random
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
from .debug import prnt_attributes, token_to_text


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
        for move in moves: # [:9]
            if(move):
                prnt_move("[", move, "] ")
            else:
                break
        print("")


def prnt_priorities(prio_moves, prio_cnts):
    for pmove in prio_moves:
        tokens = pmove[2]
        prnt_move("\n ", pmove[0], "")        
        print("piece:" + str(pmove[1]) + " token:" + hex(tokens[0]) + 
               " " + reverse_lookup(PRIO, pmove[3]) + 
               " \ntoken: " + hex(tokens[0]) + " " + token_to_text(tokens[0]))

    for i in range(len(prio_cnts)):
        print(str(i + 1) + ": " + str(prio_cnts[i]))


def prnt_fmttime(msg, seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    print( msg + "%02d:%02d:%02d" % (hour, minute, sec))


def read_steps(steps, dir_idx, step_idx):
    stepx = steps[dir_idx][step_idx][0]
    stepy = steps[dir_idx][step_idx][1]
    prom_piece = steps[dir_idx][step_idx][2]
    return stepx, stepy, prom_piece


def generate_moves(match):
    color = match.next_color()
    priomoves = []
    priocnts = [0] * len(PRIO)

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
                        tokens = analyze_move(match, gmove)
                        priomoves.append([gmove, piece, tokens, PRIO['last']])
                    elif(errmsg != rules.RETURN_CODES['king-error']):
                        break

    if(match.next_color() == COLORS['white']):
        kg_attacked = rules.is_field_touched(match, COLORS['black'], match.wKg_x, match.wKg_y)
    else:
        kg_attacked = rules.is_field_touched(match, COLORS['white'], match.bKg_x, match.bKg_y)

    if(kg_attacked):
        for i in range(len(PRIO)):
            priocnts[i]= 0
        priocnts[0] = len(priomoves)

        for pmove in priomoves:
            if(pmove[1] == PIECES['wQu'] or pmove[1] == PIECES['bQu']):
                pmove[3] = PRIO['prio1b']
            else:
                pmove[3] = PRIO['prio1']
    else:
        rank_moves(priomoves)
        priomoves.sort(key=itemgetter(3))

        for pmove in priomoves:
            priocnts[PRIO_INDICES[pmove[3]]] += 1

    return priomoves, priocnts


def rate(color, newscore, newmove, newcandidates, score, candidates):
    if( (color == COLORS["white"] and score >= newscore) or (color == COLORS["black"] and score <= newscore) ):
        return score
    else:
        candidates.clear()
        candidates.append(newmove)

        #if(len(newcandidates) > 0):
        for newcandidate in newcandidates[:12]:
            if(newcandidate):
                candidates.append(newcandidate)
            else:
                break

        candidates.append(None)
        return newscore


def select_maxcnt(match, depth, prio_moves, prio_cnts, lastmv_prio):
    mvcnt = len(prio_moves)
    prio1_mvcnt = prio_cnts[PRIO_INDICES[PRIO['prio1']]] + prio_cnts[PRIO_INDICES[PRIO['prio1b']]]
    remaining_mvcnt = mvcnt - prio1_mvcnt

    if(match.level == LEVELS['blitz']):
        cnts = 12
        dpth = 3
    elif(match.level == LEVELS['low']):
        cnts = 16
        dpth = 4
    elif(match.level == LEVELS['medium']):
        cnts = 20
        dpth = 5
    else:
        cnts = 24
        dpth = 6

    if(depth <= dpth):
        return max(cnts, prio1_mvcnt)
    elif((lastmv_prio == PRIO['prio1'] or lastmv_prio == PRIO['prio1b']) and depth <= dpth + 5):
        addcnt = 0
        if(remaining_mvcnt > 1):
            addcnt += 1
            idx = random.randint(prio1_mvcnt, mvcnt - 1)
            prio_moves.insert(0, prio_moves.pop(idx))
        if(remaining_mvcnt > 2):
            addcnt += 1
            idx = random.randint(prio1_mvcnt + 1, mvcnt - 1)
            prio_moves.insert(0, prio_moves.pop(idx))

        return min(8, prio1_mvcnt + addcnt)
    else:
        return 0


def calc_max(match, depth, alpha, beta, lastmv_prio):
    color = match.next_color()
    candidates = []
    maxscore = SCORES[PIECES['wKg']] * 2
    count = 0

    prio_moves, prio_cnts = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, prio_moves, prio_cnts, lastmv_prio)

    if(depth == 1):
        prnt_priorities(prio_moves, prio_cnts)

    if(len(prio_moves) == 0 or maxcnt == 0):
        candidates.append(None)
        return score_position(match, len(prio_moves)), candidates

    if(len(prio_moves) == 1):
        pmove = prio_moves[0]
        candidates.append(pmove[0])
        candidates.append(None)
        return score_position(match, len(prio_moves)), candidates

    for pmove in prio_moves[:maxcnt]:
        newmove = pmove[0]

        if(depth == 1):
            count += 1
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, newmove, "")
            print("   " + reverse_lookup(PRIO, pmove[3]))            
        elif(depth == 2):
            print(".", end="")

        matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        newscore, newcandidates = calc_min(match, depth + 1, maxscore, beta, pmove[3]) # , dbginfo

        score = rate(color, newscore, newmove, newcandidates, maxscore, candidates)

        if(depth == 1):
            prnt_move("\nCURR SEARCH: [", newmove, "]")
            prnt_moves("", newcandidates)

            prnt_moves("CANDIDATES: ", candidates)
            print("newscore: " + str(newscore) + " / score: " + str(score) + " / maxscore: " + str(maxscore))

            print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

        matchmove.undo_move(match)

        if(score > maxscore):
            maxscore = score
            if(maxscore > beta):
                return maxscore, candidates

    return maxscore, candidates


def calc_min(match, depth, alpha, beta, lastmv_prio):
    color = match.next_color()
    candidates = []
    minscore = SCORES[PIECES['bKg']] * 2
    count = 0

    prio_moves, prio_cnts = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, prio_moves, prio_cnts, lastmv_prio)

    if(depth == 1):
        prnt_priorities(prio_moves, prio_cnts)

    if(len(prio_moves) == 0 or maxcnt == 0):
        candidates.append(None)
        return score_position(match, len(prio_moves)), candidates

    if(len(prio_moves) == 1):
        pmove = prio_moves[0]
        candidates.append(pmove[0])
        candidates.append(None)
        return score_position(match, len(prio_moves)), candidates

    for pmove in prio_moves[:maxcnt]:
        newmove = pmove[0]
        
        if(depth == 1):
            count += 1
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, newmove, "")
            print("   " + reverse_lookup(PRIO, pmove[3]))
        elif(depth == 2):
            print(".", end="")

        matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        newscore, newcandidates = calc_max(match, depth + 1, alpha, minscore, pmove[3]) # , dbginfo

        score = rate(color, newscore, newmove, newcandidates, minscore, candidates)

        matchmove.undo_move(match)

        if(depth == 1):
            prnt_move("\nCURR SEARCH: [", newmove, "]")
            prnt_moves("", newcandidates)

            prnt_moves("CANDIDATES: ", candidates)
            print("newscore: " + str(newscore) + " / score: " + str(score) + " / minscore: " + str(minscore))

            print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

        if(score < minscore):
            minscore = score
            if(minscore < alpha):
                return minscore, candidates

    return minscore, candidates


def calc_move(match):
    candidates = []

    start = time.time()

    gmove = retrieve_move(match)
    if(gmove):
        candidates.append(gmove)
        score = match.score
    elif(match.next_color() == COLORS['white']):
        score, candidates = calc_max(match, 1, SCORES[PIECES['bKg']] * 2, SCORES[PIECES['bKg']] * 2, None) # , dbginfo
    else:
        score, candidates = calc_min(match, 1, SCORES[PIECES['wKg']] * 2, SCORES[PIECES['bKg']] * 2, None) # , dbginfo

    msg = "result: " + str(score) + " match.id: " + str(match.id) + " "
    prnt_moves(msg, candidates)
    
    end = time.time()
    prnt_fmttime("\ncalc-time: ", end - start)
    prnt_attributes(match)
    return candidates

