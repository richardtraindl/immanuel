from kate.engine.move import *
from kate.engine.match import *
from kate.engine.matchmove import *
from kate.engine import helper, rules, openings, calc_helper, debug
from kate.engine.pieces import pawn, rook, bishop, knight, queen, king
import time
from operator import itemgetter


def prnt_move(msg, move):
    if(move == None):
        print("no move.....")
    else:
        print(msg + 
            Match.index_to_koord(move.srcx, move.srcy) + "-" +
            Match.index_to_koord(move.dstx, move.dsty), end="")
        if(move.prom_piece != PIECES['blk']):
            print(helper.reverse_lookup(PIECES, move.prom_piece), end="")


def prnt_moves(msg, moves):
    if(moves[0] == None):
        print("no move.....")
    else:
        print(msg, end=" ")
        for move in moves[:9]:
            if(move):
                prnt_move("[", move)
                print("] ", end="")
            else:
                break


def prnt_fmttime(msg, seconds):
    minute, sec = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    print( msg + "%02d:%02d:%02d" % (hour, minute, sec))


class GenMove(object):
    def __init__(self, srcx=None, srcy=None, dstx=None, dsty=None, prom_piece=None):
        self.srcx = srcx
        self.srcy = srcy
        self.dstx = dstx
        self.dsty = dsty
        self.prom_piece = prom_piece


def read_steps(steps, dir_idx, step_idx):
    stepx = steps[dir_idx][step_idx][0]
    stepy = steps[dir_idx][step_idx][1]
    prom_piece = steps[dir_idx][step_idx][2]
    return stepx, stepy, prom_piece


def rank_move(match, gmove):
    prio1 = 1
    prio2 = 2
    prio3 = 3
    prio4 = 4
    priority = 5

    capture, prio = calc_helper.is_capture(match, gmove)
    if(capture):
        priority = min(priority, prio)
        if(priority == prio1):
            return priority

    promotion, prio = calc_helper.is_promotion(match, gmove) 
    if(promotion):
        priority = min(priority, prio)
        if(priority == prio1):
            return priority
    
    castling, prio = calc_helper.is_castling(match, gmove)
    if(castling):
        priority = min(priority, prio)
        if(priority == prio1):
            return priority

    attack, prio = calc_helper.does_attack(match, gmove)
    if(attack):
        priority = min(priority, prio)
        if(priority == prio1):
            return priority

    support, prio = calc_helper.does_support_attacked(match, gmove)
    if(support):
        priority = min(priority, prio)
        if(priority == prio1):
            return priority

    flee, prio = calc_helper.does_attacked_flee(match, gmove)
    if(flee):
        priority = min(priority, prio)
        if(priority == prio1):
            return priority

    endgame, prio = calc_helper.is_endgame_move(match, gmove)
    if(endgame):
        priority = min(priority, prio)
        if(priority == prio1):
            return priority
        
    priority = min(priority, prio4)
    return priority


def generate_moves(match):
    color = match.next_color()
    prio_moves = []
    priorities = [0] * 4
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
                        prio_moves.append([gmove, priority, piece_prio])
                        priorities[priority-1] += 1
                    elif(errmsg != rules.RETURN_CODES['king-error']):
                        break

    if(match.next_color() == COLORS['white']):
        kg_attacked = rules.is_field_touched(match, COLORS['black'], match.wKg_x, match.wKg_y)
    else:
        kg_attacked = rules.is_field_touched(match, COLORS['white'], match.bKg_x, match.bKg_y)

    if(kg_attacked):
        priorities[0]= len(prio_moves)
        priorities[1]= 0
        priorities[2]= 0
        priorities[3]= 0
        
    prio_moves.sort(key=itemgetter(1, 2))
        
    return prio_moves, priorities


def rate(color, gmove, gmovescore, candidates, candidatescore, search_candidates):
    if( (color == COLORS["white"] and candidatescore >= gmovescore) or (color == COLORS["black"] and candidatescore <= gmovescore) ):
        return candidatescore
    else:
        candidates[0] = gmove

        if(search_candidates[0]):
            idx = 1
            for cand in search_candidates[:9]:
                if(cand):
                    candidates[idx] = cand
                    idx += 1
                else:
                    break
        else:
            candidates[1] = None

        return gmovescore


def select_maxcnt(match, depth, priorities):
    if(match.level == LEVELS['blitz']):
        maxdepth = 5
        counts = [12, 12]
        limit = 2
    elif(match.level == LEVELS['low']):
        maxdepth = 6
        counts = [12, 12]
        limit = 2
    elif(match.level == LEVELS['medium']):
        maxdepth = 8
        counts = [16, 12]
        limit = 2
    else:
        maxdepth = 10
        counts = [200, 16]
        limit = 2

    if(depth > maxdepth or (priorities[0] + priorities[1] + priorities[2] + priorities[3]) == 0):
        return 0
    elif(depth <= limit):
        return min( (priorities[0] + priorities[1] + priorities[2] + priorities[3]), counts[0] )
    else:
        return min( (priorities[0] + priorities[1] + priorities[2] + priorities[3]), counts[1] )


def calc_max(match, depth, alpha, beta):
    color = match.next_color()
    candidates = [None] * 10
    search_candidates = [None] * 10
    score = None
    maxscore = -200000
    count = 0

    prio_moves, priorities = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, priorities)

    if(maxcnt == 0):
        return calc_helper.evaluate_position(match, len(prio_moves)), candidates
        
    for pmove in prio_moves[:maxcnt]:
        gmove = pmove[0]
        move = do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

        score, search_candidates = calc_min(match, depth + 1, maxscore, beta)

        score = rate(color, gmove, score, candidates, maxscore, search_candidates)

        if(depth == 1):
            count += 1

            print("\n____________________________________________________________")
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, gmove)
            print(" p:" + str(pmove[1]) + " r:" + str(pmove[2]), end="")

            msg = "\nCURR SEARCH: "
            prnt_moves(msg, search_candidates)

            msg = "\nCANDIDATES:  "
            prnt_moves(msg, candidates)
            print(" score: " + str(score) + " / maxscore: " + str(maxscore))
            
            print("debuginfo: prio1:" + str(priorities[0]) + " prio2:" + str(priorities[1]) + " prio3:" + str(priorities[2]) + " prio4:" + str(priorities[3]))
            print("\n––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

        undo_move(match)

        if(score > maxscore):
            maxscore = score
            if(maxscore > beta):
                return maxscore, candidates

    return maxscore, candidates


def calc_min(match, depth, alpha, beta):
    color = match.next_color()
    candidates = [None] * 10
    search_candidates = [None] * 10
    score = None
    minscore = 200000
    count = 0

    prio_moves, priorities = generate_moves(match)

    maxcnt = select_maxcnt(match, depth, priorities)

    if(maxcnt == 0):
        return calc_helper.evaluate_position(match, len(prio_moves)), candidates

    for pmove in prio_moves[:maxcnt]:
        gmove = pmove[0]
        move = do_move(match,gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

        score, search_candidates = calc_max(match, depth + 1, alpha, minscore)

        score = rate(color, gmove, score, candidates, minscore, search_candidates)

        undo_move(match)

        if(depth == 1):
            count += 1

            print("\n____________________________________________________________")
            msg = "\nmatch.id: " + str(match.id) + "   count: " + str(count) + "   calculate: "
            prnt_move(msg, gmove)
            print(" p:" + str(pmove[1]) + " r:" + str(pmove[2]), end="")

            msg = "\nCURR SEARCH: "
            prnt_moves(msg, search_candidates)

            msg = "\nCANDIDATES:  "
            prnt_moves(msg, candidates)
            print(" score: " + str(score) + " / minscore: " + str(minscore))

            print("debuginfo: prio1:" + str(priorities[0]) + " prio2:" + str(priorities[1]) + " prio3:" + str(priorities[2]) + " prio4:" + str(priorities[3]))
            print("\n––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

        if(score < minscore):
            minscore = score
            if(minscore < alpha):
                return minscore, candidates

    return minscore, candidates


def calc_move(match):
    candidates = [None] * 10

    start = time.time()
    
    # candidates[0] = openings.retrieve_move(match)

    if(candidates[0]):
        score = match.score
    elif(match.next_color() == COLORS['white']):
        score, candidates = calc_max(match, 1, -200000, 200000)
    else:
        score, candidates = calc_min(match, 1, -200000, 200000)

    msg = "\nresult: " + str(score) + " match.id: " + str(match.id) + " "
    prnt_moves(msg, candidates)

    end = time.time()
    prnt_fmttime("\ncalc-time: ", end - start)
    return candidates[0]
