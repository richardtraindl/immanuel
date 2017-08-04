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
        print(" piece:" + str(pmove[1]) + " token:" + hex(pmove[2]) + " prio:" + str(pmove[3]))


def prnt_fmttime(msg, seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    print( msg + "%02d:%02d:%02d" % (hour, minute, sec))


def read_steps(steps, dir_idx, step_idx):
    stepx = steps[dir_idx][step_idx][0]
    stepy = steps[dir_idx][step_idx][1]
    prom_piece = steps[dir_idx][step_idx][2]
    return stepx, stepy, prom_piece


def rank_move(match, move):
    priority = PRIO['priolast']

    capture, prio = is_capture(match, move)
    if(capture):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority

    promotion, prio = is_promotion(match, move) 
    if(promotion):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority
    
    castling, prio = is_castling(match, move)
    if(castling):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority

    attack, prio = analyze_move.does_attack(match, move)
    if(attack):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority

    support, prio = analyze_move.does_support_attacked(match, move)
    if(support):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority

    flee, prio = does_attacked_flee(match, move)
    if(flee):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority

    endgame, prio = is_endgame_move(match, move)
    if(endgame):
        priority = min(priority, prio)
        if(priority == PRIO['prio1']):
            return priority
        
    return priority


def prioritize_move(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        token = token | MV_PIECE_IS_PAWN
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        token = token | MV_PIECE_IS_KING
    else:
        token = token | MV_PIECE_IS_OFFICER

    token = token | captures(match, move)

    token = token | promotes(match, move)

    token = token | castles(match, move)

    token = token | touches(match, move)

    token = token | flees(match, move)

    token = token | progress(match, move)

    return token

def rank_by_token(priomoves):
    for pmove in priomoves:
        count = 0
        token = pmove[2]
        piece = pmove[1]

        if(token & MV_IS_CASTLING > 0):
            count += 1
            pmove[3] = min(PRIO['prio2'], pmove[3])

        if(token & MV_IS_PROMOTION > 0):
            count += 1
            pmove[3] = min(PRIO['prio2'], pmove[3])

        if(token & MV_IS_CAPTURE > 0):
            count += 1
            if(token & CAPTURED_IS_SUPP_BY_PAWN == 0 and token & CAPTURED_IS_SUPP_BY_OFFICER == 0):
                pmove[3] = min(PRIO['prio2'], pmove[3])
            elif(token & MV_PIECE_IS_PAWN > 0):
                pmove[3] = min(PRIO['prio2'], pmove[3])
            elif(token & CAPTURED_IS_OFFICER > 0):
                pmove[3] = min(PRIO['prio2'], pmove[3])
            elif(token & CAPTURED_IS_SUPP_BY_PAWN == 0 and 
                 (token & CAPTURED_IS_ADD_ATT_FROM_PAWN > 0 or token & CAPTURED_IS_ADD_ATT_FROM_OFFICER > 0)):
                pmove[3] = min(PRIO['prio2'], pmove[3])
            else:
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_ATTACK > 0):
            count += 1
            if(token & ATTACKED_IS_KING > 0):
                pmove[3] = min(PRIO['prio2'], pmove[3])
            elif(token & ATT_IS_ADD_ATT_FROM_PAWN > 0 or token & ATT_IS_ADD_ATT_FROM_OFFICER > 0):
                pmove[3] = min(PRIO['prio3'], pmove[3])
            elif(token & ATT_IS_SUPP_BY_PAWN == 0 and token & ATT_IS_SUPP_BY_OFFICER == 0):
                pmove[3] = min(PRIO['prio3'], pmove[3])
            else:
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_SUPPORT > 0):
            count += 1
            if(token & SUPPORTED_IS_ATT_FROM_PAWN > 0 or token & SUPPORTED_IS_ATT_FROM_OFFICER > 0):
                pmove[3] = min(PRIO['prio3'], pmove[3])
            else:
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_FLEE > 0):
            if(token & FIELD_IS_ATT_FROM_PAWN == 0 and token & FIELD_IS_ATT_FROM_OFFICER == 0):
                count += 1
                pmove[3] = min(PRIO['prio3'], pmove[3])
            else:
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_PROGRESS > 0 and pmove[3] == PRIO['unrated']):
            pmove[3] = PRIO['progress']

        if(count == 2 and pmove[3] > PRIO['prio1']):
            pmove[3] = pmove[3] - 1
        elif(count > 2):
            pmove[3] = pmove[3] - 1


def generate_moves(match):
    color = match.next_color()
    priomoves = []
    priocnts = [0] * 7
    progressmoves = []
    #piece_prio = None

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == PIECES['blk'] or color != Match.color_of_piece(piece)):
                continue
            else:
                dir_idx = 0
                step_idx = 0
                if(piece == PIECES['wPw']):
                    #piece_prio = 2
                    if(y < 6):
                        steps = pawn.GEN_WSTEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = pawn.GEN_WPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == PIECES['bPw']):
                    #piece_prio = 2
                    if(y > 1):
                        steps = pawn.GEN_BSTEPS
                        max_dir = 4
                        max_step = 1
                    else:
                        steps = pawn.GEN_BPROM_STEPS
                        max_dir = 3
                        max_step = 4
                elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                    #piece_prio = 5
                    steps = rook.GEN_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                    #piece_prio = 4
                    steps = bishop.GEN_STEPS
                    max_dir = 4
                    max_step = 7
                elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                    #piece_prio = 3
                    steps = knight.GEN_STEPS
                    max_dir = 8
                    max_step = 1
                elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                    #piece_prio = 6
                    steps = queen.GEN_STEPS
                    max_dir = 8
                    max_step = 7
                else:
                    #piece_prio = 1
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
                        # priority = rank_move(match, gmove)
                        token = prioritize_move(match, gmove)
                        priomoves.append([gmove, piece, token, PRIO['unrated']])
                        #prio_moves.append([gmove, priority, piece_prio, token])
                        # prio_cnts[priority-1] += 1
                    elif(errmsg != rules.RETURN_CODES['king-error']):
                        break

    if(match.next_color() == COLORS['white']):
        kg_attacked = rules.is_field_touched(match, COLORS['black'], match.wKg_x, match.wKg_y)
    else:
        kg_attacked = rules.is_field_touched(match, COLORS['white'], match.bKg_x, match.bKg_y)

    if(kg_attacked):
        for i in range(7):
            priocnts[i]= 0
        priocnts[0] = len(priomoves)

        for pmove in priomoves:
            pmove[3] = PRIO['prio1']
    else:
        rank_by_token(priomoves)
        priomoves.sort(key=itemgetter(3))
        # prio_moves.sort(key=itemgetter(1, 2))

        for pmove in priomoves:
            if(pmove[3] == PRIO['progress']):
                progressmoves.append(pmove)
                priomoves.remove(pmove)
            else:
                priocnts[pmove[3]-1] += 1

    return priomoves, priocnts, progressmoves


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


def select_maxcnt2(match, depth, prio_cnts, lastmv_prio):
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


def select_maxcnt(match, depth, prio_moves, prio_cnts, progress_moves, lastmv_prio):
    if(len(progress_moves) > 0):
        prio_moves.insert(0, progress_moves[0])
        del progress_moves[0]

    if(match.level == LEVELS['blitz']):
        counts = ([3, 12], [5, 8], [8, 4])
    elif(match.level == LEVELS['low']):
        counts = ([3, 12], [7, 8], [10, 4])
    elif(match.level == LEVELS['medium']):
        counts = ([3, 16], [8, 12], [12, 4])
    else:
        counts = ([2, 200], [10, 12], [12, 4])

    if(depth <= counts[0][0]):
        return counts[0][1]
    elif(depth <= counts[1][0]):
        return min( (prio_cnts[0] + prio_cnts[1] + 1), counts[1][1] )
    else:
        if(lastmv_prio <= PRIO['prio2'] and depth <= (counts[1][0] + 2)):
            return prio_cnts[0] + 1
        else:
            return 0


def calc_max(match, depth, alpha, beta, lastmv_prio, dbgcndts):
    color = match.next_color()
    currcndts = []
    maxscore = -200000
    count = 0

    prio_moves, prio_cnts, progress_moves = generate_moves(match)

    #maxcnt = select_maxcnt(match, depth, prio_cnts, lastmv_prio)
    maxcnt = select_maxcnt(match, depth, prio_moves, prio_cnts, progress_moves, lastmv_prio)

    if(depth == 1):
        prnt_priorities(prio_moves, prio_cnts)

    if(len(prio_moves) == 0 or maxcnt == 0):
        currcndts.append(None)
        return evaluate_position(match, len(prio_moves)), currcndts

    for pmove in prio_moves[:maxcnt]:
        newmove = pmove[0]

        matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        #newscore, newcndts = calc_min(match, depth + 1, maxscore, beta, pmove[1], dbgcndts)
        newscore, newcndts = calc_min(match, depth + 1, maxscore, beta, pmove[3], dbgcndts)

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

    prio_moves, prio_cnts, progress_moves = generate_moves(match)

    #maxcnt = select_maxcnt(match, depth, prio_cnts, lastmv_prio)
    maxcnt = select_maxcnt(match, depth, prio_moves, prio_cnts, progress_moves, lastmv_prio)

    if(depth == 1):
        prnt_priorities(prio_moves, prio_cnts)

    if(len(prio_moves) == 0 or maxcnt == 0):
        currcndts.append(None)
        return evaluate_position(match, len(prio_moves)), currcndts

    for pmove in prio_moves[:maxcnt]:
        newmove = pmove[0]

        matchmove.do_move(match, newmove.srcx, newmove.srcy, newmove.dstx, newmove.dsty, newmove.prom_piece)

        #newscore, newcndts = calc_max(match, depth + 1, alpha, minscore, pmove[1], dbgcndts)
        newscore, newcndts = calc_max(match, depth + 1, alpha, minscore, pmove[3], dbgcndts)

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
