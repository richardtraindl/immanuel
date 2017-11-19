import time
from operator import itemgetter
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
            print(reverse_lookup(PIECES, move.prom_piece), end="")
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
        prnt_move(" ", pmove[0], "")
        print(" piece:" + str(pmove[1]) + " token:" + hex(pmove[2]) + " prio:" + str(pmove[3]))

    for i in range(6):
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
    priocnts = [0] * 6

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
                        token = analyze_move.analyze_move(match, gmove)
                        priomoves.append([gmove, piece, token, PRIO['unrated']])
                    elif(errmsg != rules.RETURN_CODES['king-error']):
                        break

    if(match.next_color() == COLORS['white']):
        kg_attacked = rules.is_field_touched(match, COLORS['black'], match.wKg_x, match.wKg_y)
    else:
        kg_attacked = rules.is_field_touched(match, COLORS['white'], match.bKg_x, match.bKg_y)

    if(kg_attacked):
        for i in range(4):
            priocnts[i]= 0
        priocnts[0] = len(priomoves)

        for pmove in priomoves:
            pmove[3] = PRIO['prio1']
    else:
        rank_moves(priomoves)
        priomoves.sort(key=itemgetter(3))

        for pmove in priomoves:
            priocnts[PRIO_INDICES[pmove[3]]] += 1

    return priomoves, priocnts


def rate(color, newmove, newscore, currcndts, cndtscore, newcndts):
    if( (color == COLORS["white"] and cndtscore > newscore) or (color == COLORS["black"] and cndtscore < newscore) ):
        return cndtscore
    else:
        del currcndts[:]
        currcndts.append(newmove)

        if(len(newcndts) > 0):
            for cand in newcndts[:9]:
                if(cand):
                    currcndts.append(cand)
                else:
                    break

        currcndts.append(None)
        return newscore


def select_maxcnt(match, depth, prio_moves, prio_cnts, lastmv_prio):
    sum_moves = len(prio_moves)

    if(sum_moves <= 10):
        add_dpth = 1
    else:
        add_dpth = 0

    if(match.level == LEVELS['blitz']):
        cnts = 12
        dpth = 3 + add_dpth
    elif(match.level == LEVELS['low']):
        cnts = 16
        dpth = 4 + add_dpth
    elif(match.level == LEVELS['medium']):
        cnts = 20
        dpth = 5 + add_dpth
    else:
        cnts = 24
        dpth = 6 + add_dpth

    if(depth <= dpth):
        return min(cnts, sum_moves)
    elif(lastmv_prio == PRIO['prio1'] and depth <= dpth + 2):
        print(str(depth) + " ", end="")
        return prio_cnts[0]
    else:
        return 0


def calc_max(match, depth, alpha, beta, lastmv_prio, dbginfo):
    color = match.next_color()
    currcndts = []
    maxscore = -200000
    count = 0

    prio_moves, prio_cnts = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, prio_moves, prio_cnts, lastmv_prio)

    #dbgcounts = dbginfo[0]
    #dbgcounts[depth-1] += 1

    if(depth == 1):
        prnt_priorities(prio_moves, prio_cnts)

    if(len(prio_moves) == 0 or maxcnt == 0):
        currcndts.append(None)
        return score_position(match, len(prio_moves)), currcndts

    for pmove in prio_moves[:maxcnt]:
        newmove = pmove[0]

        if(depth == 1):
            count += 1
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, newmove, "")
            print("   prio: " + str(pmove[3]) + "   token: " + hex(pmove[2]) + " " + token_to_text(pmove[2]))

        matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        newscore, newcndts = calc_min(match, depth + 1, maxscore, beta, pmove[3], dbginfo)

        score = rate(color, newmove, newscore, currcndts, maxscore, newcndts)

        if(depth == 1):
            threadmoves = []
            threadmoves.append(newmove)

            if(len(newcndts) > 0):
                for ncand in newcndts: # [:9]
                    if(ncand):
                        threadmoves.append(ncand)
                    else:
                        break

            dbginfo[1].append(threadmoves)

            prnt_move("CURR SEARCH: [", newmove, "]")
            prnt_moves("", newcndts)

            prnt_moves("CANDIDATES: ", currcndts)
            print("newscore: " + str(newscore) + " / score: " + str(score) + " / maxscore: " + str(maxscore))

            print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

        matchmove.undo_move(match)

        if(score > maxscore):
            maxscore = score
            if(maxscore > beta):
                return maxscore, currcndts

    return maxscore, currcndts


def calc_min(match, depth, alpha, beta, lastmv_prio, dbginfo):
    color = match.next_color()
    currcndts = []
    minscore = 200000
    count = 0

    prio_moves, prio_cnts = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, prio_moves, prio_cnts, lastmv_prio)

    #dbgcounts = dbginfo[0]
    #dbgcounts[depth-1] += 1
    
    if(depth == 1):
        prnt_priorities(prio_moves, prio_cnts)

    if(len(prio_moves) == 0 or maxcnt == 0):
        currcndts.append(None)
        return score_position(match, len(prio_moves)), currcndts

    for pmove in prio_moves[:maxcnt]:
        newmove = pmove[0]
        
        if(depth == 1):
            count += 1
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, newmove, "")
            print("   prio: " + str(pmove[3]) + "   token: " + hex(pmove[2]) + " " + token_to_text(pmove[2]))

        matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        newscore, newcndts = calc_max(match, depth + 1, alpha, minscore, pmove[3], dbginfo)

        score = rate(color, newmove, newscore, currcndts, minscore, newcndts)

        matchmove.undo_move(match)

        if(depth == 1):
            threadmoves = []
            threadmoves.append(newmove)

            if(len(newcndts) > 0):
                for ncand in newcndts: # [:9]
                    if(ncand):
                        threadmoves.append(ncand)
                    else:
                        break

            dbginfo[1].append(threadmoves)

            prnt_move("CURR SEARCH: [", newmove, "]")
            prnt_moves("", newcndts)

            prnt_moves("CANDIDATES: ", currcndts)
            print("newscore: " + str(newscore) + " / score: " + str(score) + " / minscore: " + str(minscore))

            print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

        if(score < minscore):
            minscore = score
            if(minscore < alpha):
                return minscore, currcndts

    return minscore, currcndts


def calc_move(match):
    currcndts = []
    dbgcounts = [0] * 20
    dbgcndts = []    
    dbginfo = []
    start = time.time()

    dbginfo.append(dbgcounts)
    dbginfo.append(dbgcndts)

    gmove = retrieve_move(match)
    if(gmove):
        currcndts.append(gmove)
        score = match.score
    elif(match.next_color() == COLORS['white']):
        score, currcndts = calc_max(match, 1, -200000, 200000, None, dbginfo)
    else:
        score, currcndts = calc_min(match, 1, -200000, 200000, None, dbginfo)

    msg = "result: " + str(score) + " match.id: " + str(match.id) + " "
    prnt_moves(msg, currcndts)
    
    #for i in range(20):
    #    print(str(i + 1) + ": " + str(dbgcounts[i]))

    end = time.time()
    prnt_fmttime("\ncalc-time: ", end - start)
    prnt_attributes(match)
    return currcndts, dbginfo

