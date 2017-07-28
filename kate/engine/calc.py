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
from .debug import prnt_attributes


def prnt_move(msg, move):
    if(move == None):
        print("no move.....")
    else:
        print(msg + 
            index_to_coord(move.srcx, move.srcy) + "-" +
            index_to_coord(move.dstx, move.dsty), end="")
        if(move.prom_piece != PIECES['blk']):
            print(reverse_lookup(PIECES, move.prom_piece), end="")


def prnt_moves(msg, moves):
    print(msg, end=" ")

    if(len(moves) == 0):
        print("no move.....", end="")
    else:
        for move in moves: # [:9]
            if(move):
                prnt_move("[", move)
                print("] ", end="")
            else:
                break


def prnt_priorities(prio_moves, prio_cnts):
    for pmove in prio_moves:
        prnt_move(" ", pmove[0])
        print(" prio:" + str(pmove[1]) + "/" + str(pmove[2] + "/" + hex(pmove[3]))


def prnt_fmttime(msg, seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    print( msg + "%02d:%02d:%02d" % (hour, minute, sec))


def read_steps(steps, dir_idx, step_idx):
    stepx = steps[dir_idx][step_idx][0]
    stepy = steps[dir_idx][step_idx][1]
    prom_piece = steps[dir_idx][step_idx][2]
    return stepx, stepy, prom_piece


def rank_move(match, gmove):
    priority = PRIO['priolast']

    capture, prio = is_capture(match, gmove)
    if(capture):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority

    promotion, prio = is_promotion(match, gmove) 
    if(promotion):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority
    
    castling, prio = is_castling(match, gmove)
    if(castling):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority

    attack, prio = analyze_move.does_attack(match, gmove)
    if(attack):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority

    support, prio = analyze_move.does_support_attacked(match, gmove)
    if(support):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority

    flee, prio = does_attacked_flee(match, gmove)
    if(flee):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority

    endgame, prio = is_endgame_move(match, gmove)
    if(endgame):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority
        
    return priority


def generate_moves(match):
    color = match.next_color()
    prio_moves = []
    prio_cnts = [0] * 7
    piece_prio = None

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == PIECES['blk'] or color != Match.color_of_piece(piece)):
                continue
            else:
                dir_idx = 0
                step_idx = 0
                if(piece == PIECES['wPw']):
                    piece_prio = 2
                    if(y < 6):
                        steps = pawn.GEN_WSTEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = pawn.GEN_WPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == PIECES['bPw']):
                    piece_prio = 2
                    if(y > 1):
                        steps = pawn.GEN_BSTEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = pawn.GEN_BPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                    piece_prio = 5
                    steps = rook.GEN_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                    piece_prio = 4
                    steps = bishop.GEN_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                    piece_prio = 3
                    steps = knight.GEN_STEPS
                    max_dir = 8
                    max_step = 1
                elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                    piece_prio = 6
                    steps = queen.GEN_STEPS
                    max_dir = 8
                    max_step = 7
                else:
                    piece_prio = 1
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
                        priority = rank_move(match, gmove)
                        token = analyze_move.touches(match, gmove)
                        prio_moves.append([gmove, priority, piece_prio, token])
                        prio_cnts[priority-1] += 1
                    elif(errmsg != rules.RETURN_CODES['king-error']):
                        break

    if(match.next_color() == COLORS['white']):
        kg_attacked = rules.is_field_touched(match, COLORS['black'], match.wKg_x, match.wKg_y)
    else:
        kg_attacked = rules.is_field_touched(match, COLORS['white'], match.bKg_x, match.bKg_y)

    if(kg_attacked):
        for i in range(7):
            prio_cnts[i]= 0
        prio_cnts[0] = len(prio_moves)

    prio_moves.sort(key=itemgetter(1, 2))

    return prio_moves, prio_cnts


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


def select_maxcnt(match, depth, prio_cnts, lastmv_prio):
    if(match.level == LEVELS['blitz']):
        counts = ([3, 12], [5, 8])
    elif(match.level == LEVELS['low']):
        counts = ([3, 12], [7, 8])
    elif(match.level == LEVELS['medium']):
        counts = ([2, 20], [10, 12])
    else:
        counts = ([2, 200], [10, 12])

    if(depth <= counts[0][0]):
        return counts[0][1]
    elif(depth <= counts[1][0]):
        return min( (prio_cnts[0] + prio_cnts[1]), counts[1][1] )
    else:
        if(lastmv_prio == PRIO['prio1'] and depth <= (counts[1][0] + 4)):
            return prio_cnts[0]
        else:
            return 0


def calc_max(match, depth, alpha, beta, lastmv_prio, dbgcndts):
    color = match.next_color()
    currcndts = []
    maxscore = -200000
    count = 0

    prio_moves, prio_cnts = generate_moves(match)
    if(depth == 1):
        prnt_priorities(prio_moves, prio_cnts)

    maxcnt = select_maxcnt(match, depth, prio_cnts, lastmv_prio)

    if(len(prio_moves) == 0 or maxcnt == 0):
        currcndts.append(None)
        return evaluate_position(match, len(prio_moves)), currcndts

    for pmove in prio_moves[:maxcnt]:
        newmove = pmove[0]

        matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        newscore, newcndts = calc_min(match, depth + 1, maxscore, beta, pmove[1], dbgcndts)

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

            dbgcndts.append(threadmoves)

            count += 1

            print("\n____________________________________________________________")

            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, newmove)
            print(" p:" + str(pmove[1]) + " r:" + str(pmove[2]), end="")

            msg = "\nCURR SEARCH: "
            prnt_moves(msg, newcndts)

            msg = "\nCANDIDATES:  "
            prnt_moves(msg, currcndts)
            print(" newscore: " + str(newscore) + " / score: " + str(score) + " / maxscore: " + str(maxscore))
            
            print("\n––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

        matchmove.undo_move(match)

        if(score > maxscore):
            maxscore = score
            if(maxscore > beta):
                return maxscore, currcndts

    return maxscore, currcndts


def calc_min(match, depth, alpha, beta, lastmv_prio, dbgcndts):
    color = match.next_color()
    currcndts = []
    minscore = 200000
    count = 0

    prio_moves, prio_cnts = generate_moves(match)
    if(depth == 1):
        prnt_priorities(prio_moves, prio_cnts)

    maxcnt = select_maxcnt(match, depth, prio_cnts, lastmv_prio)

    if(len(prio_moves) == 0 or maxcnt == 0):
        currcndts.append(None)
        return evaluate_position(match, len(prio_moves)), currcndts

    for pmove in prio_moves[:maxcnt]:
        newmove = pmove[0]

        matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        newscore, newcndts = calc_max(match, depth + 1, alpha, minscore, pmove[1], dbgcndts)

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

            dbgcndts.append(threadmoves)

            count += 1

            print("\n____________________________________________________________")

            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, newmove)
            print(" p:" + str(pmove[1]) + " r:" + str(pmove[2]), end="")

            msg = "\nCURR SEARCH: "
            prnt_moves(msg, newcndts)

            msg = "\nCANDIDATES:  "
            prnt_moves(msg, currcndts)
            print(" newscore: " + str(newscore) + " / score: " + str(score) + " / minscore: " + str(minscore))

            print("\n––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

        if(score < minscore):
            minscore = score
            if(minscore < alpha):
                return minscore, currcndts

    return minscore, currcndts


def calc_move(match):
    currcndts = []
    dbgcndts = []
    start = time.time()

    gmove = retrieve_move(match)
    if(gmove):
        currcndts.append(gmove)
        score = match.score
    elif(match.next_color() == COLORS['white']):
        score, currcndts = calc_max(match, 1, -200000, 200000, None, dbgcndts)
    else:
        score, currcndts = calc_min(match, 1, -200000, 200000, None, dbgcndts)

    msg = "\nresult: " + str(score) + " match.id: " + str(match.id) + " "
    prnt_moves(msg, currcndts)

    end = time.time()
    prnt_fmttime("\ncalc-time: ", end - start)
    prnt_attributes(match)
    return currcndts, dbgcndts
