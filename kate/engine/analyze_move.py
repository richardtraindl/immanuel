from operator import attrgetter
import copy
from .values import *
from .match import *
from .move import *
from .helper import reverse_lookup
from .analyze_helper import *
from .pieces.pawn import cPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .pieces.piece import cTouch
from .pieces.pieces_helper import obj_for_piece
from .generator import cGenerator


def castles(gmove):
    match = gmove.match
    piece = match.readfield(gmove.srcx, gmove.srcy)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(gmove.srcx - gmove.dstx == 2 or gmove.srcx - gmove.dstx == -2):
            return True


def promotes(gmove):
    if(gmove.prom_piece != PIECES['blk']):
        return True


def captures(gmove):
    match = gmove.match
    piece = match.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)
    dstpiece = match.readfield(gmove.dstx, gmove.dsty)
    if(dstpiece != PIECES['blk']):
        return True
    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and gmove.srcx != gmove.dstx ):
        return True
    else:
        return False


def defends_fork(gmove):
    match = gmove.match
    piece = match.readfield(gmove.srcx, gmove.srcy)
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    cpiece = obj_for_piece(match, piece, gmove.dstx, gmove.dsty)
    if(cpiece):
        is_fork_defend = cpiece.defends_fork()
    else:
        is_fork_defend = False
    match.undo_move()
    return is_fork_defend


def threatens_fork(gmove):
    is_fork_threat = False
    match = gmove.match
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    piece = match.readfield(gmove.dstx, gmove.dsty)
    cpiece = obj_for_piece(match, piece, gmove.dstx, gmove.dsty)
    if(cpiece):
        is_fork_threat = cpiece.threatens_fork()
    match.undo_move()
    return is_fork_threat


def flees(gmove):
    match = gmove.match
    lower_enmy_cnt_old = 0
    lower_enmy_cnt_new = 0
    piece = match.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)

    piece = match.readfield(gmove.srcx, gmove.srcy)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        return False

    frdlytouches_old, enmytouches_old = list_all_field_touches(match, color, gmove.srcx, gmove.srcy)
    ###
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    frdlytouches_new, enmytouches_new = list_all_field_touches(match, color, gmove.dstx, gmove.dsty)
    match.undo_move()
    ###

    if(len(enmytouches_old) > 0 and 
       (len(frdlytouches_old) < len(frdlytouches_new))):
        return True

    if(len(enmytouches_old) > len(enmytouches_new)):
        return True

    for enmy in enmytouches_old:
        if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
            lower_enmy_cnt_old += 1
    for enmy in enmytouches_new:
        if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
            lower_enmy_cnt_new += 1
    if(lower_enmy_cnt_old > lower_enmy_cnt_new):
        return True
    else:
        return False


def find_attacks_and_supports_after_move(gmove):
    attacked = []
    supported = []
    match = gmove.match
    piece = match.readfield(gmove.srcx, gmove.srcy)
    ###
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    cpiece = obj_for_piece(match, piece, gmove.dstx, gmove.dsty)
    if(cpiece):
        cpiece.find_attacks_and_supports(attacked, supported)
        
        if(cpiece.piece == PIECES['wKg'] or cpiece.piece == PIECES['bKg']):
            if(gmove.srcx - gmove.dstx == -2):
                crook = cRook(match, gmove.dstx - 1, gmove.dsty)
                crook.find_attacks_and_supports(attacked, supported)
            elif(gmove.srcx - gmove.dstx == 2):
                crook = cRook(match, gmove.dstx + 1, gmove.dsty)
                crook.find_attacks_and_supports(attacked, supported)
    match.undo_move()
    ###
    return attacked, supported


def find_attacks_on_and_supports_of_dstfield_after_move(gmove):
    match = gmove.match
    piece = match.readfield(gmove.srcx, gmove.srcy)
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    frdlytouches, enmytouches = list_all_field_touches(match, match.color_of_piece(piece), gmove.dstx, gmove.dsty)
    match.undo_move()
    return frdlytouches, enmytouches


def does_unpin(gmove):
    match = gmove.match
    piece = match.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)
    pinlines_before = search_lines_of_pin(match, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)
    ###
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    pinlines_after = search_lines_of_pin(match, color, gmove.dstx, gmove.dsty, None, None)
    match.undo_move()
    ###
    if(len(pinlines_after) < len(pinlines_before)):
        return True
    for pbefore in pinlines_before:
        identical = False
        for pafter in pinlines_after:
            if(pbefore[0].fieldx == pafter[0].fieldx and pbefore[0].fieldy == pafter[0].fieldy):
                identical = True
        if(identical == False):
            return True
    return False


def defends_check(match):
    if(match.next_color() == COLORS['white']):
        cking = cKing(match, match.board.wKg_x, match.board.wKg_y)
    else:
        cking = cKing(match, match.board.bKg_x, match.board.bKg_y)
    return cking.is_attacked()


def check_mates(gmove):
    match = gmove.match
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    is_move_available = match.is_move_available()
    match.undo_move()
    return not is_move_available


def find_disclosed_pieces(match, srcx, srcy, dstx, dsty, discl_attacked, discl_supported):
    piece = match.readfield(srcx, srcy)
    color = match.color_of_piece(piece)
    idx = 0
    for step in cQueen.STEPS:
        if(idx % 2 == 0):
            first = cTouch(PIECES['blk'], 0, 0)
            second = cTouch(PIECES['blk'], 0, 0)
        if(idx < 4):
            cpiece = cRook
            excluded_dir = cRook.dir_for_move(srcx, srcy, dstx, dsty)
            faces = [PIECES['wRk'], PIECES['bRk'], PIECES['wQu'], PIECES['bQu']]
        else:
            cpiece = cBishop
            excluded_dir = cBishop.dir_for_move(srcx, srcy, dstx, dsty)
            faces = [PIECES['wBp'], PIECES['bBp'], PIECES['wQu'], PIECES['bQu']]
        idx += 1

        stepx = step[0]
        stepy = step[1]
        direction = cpiece.dir_for_move(srcx, srcy, (srcx + stepx), (srcy + stepy))
        if(direction == excluded_dir or direction == match.REVERSE_DIRS[excluded_dir]):
            break
        x1, y1 = match.search(srcx, srcy, stepx, stepy)
        if(x1 is not None):
            piece = match.readfield(x1, y1)
            if(first.piece == PIECES['blk']):
                first.piece = piece
                first.fieldx = x1
                first.fieldy = y1
                continue
            elif(second.piece == PIECES['blk']):
                second.piece = piece
                second.fieldx = x1
                second.fieldy = y1

            if(first.piece == PIECES['blk'] or second.piece == PIECES['blk']):
                continue
                
            if(match.color_of_piece(first.piece) != match.color_of_piece(second.piece)):
                if(match.color_of_piece(first.piece) == color):
                    for face in faces:
                        if(first.piece == face):
                            discl_attacked.append(second)
                            break
                else:
                    for face in faces:
                        if(second.piece == face):
                            discl_attacked.append(first)
                            break
            elif(match.color_of_piece(first.piece) == match.color_of_piece(second.piece)):
                if(match.color_of_piece(first.piece) == color):
                    for face in faces:
                        if(first.piece == face):
                            discl_supported.append(second)
                            break
                    for face in faces:
                        if(second.piece == face):
                            discl_supported.append(first)
                            break

def find_disclosures(match, gmove):
    discl_attacked = []
    discl_supported = []

    piece = match.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)

    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    find_disclosed_pieces(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, discl_attacked, discl_supported)
    match.undo_move()
    ###
    match.writefield(gmove.srcx, gmove.srcy, PIECES['blk'])

    for ctouch_beyond in discl_attacked:
        list_field_touches_beyond(match, color, ctouch_beyond)

    for ctouch_beyond in discl_supported:
        list_field_touches_beyond(match, color, ctouch_beyond)

    match.writefield(gmove.srcx, gmove.srcy, piece)
    ###
    
    return discl_attacked, discl_supported


def blocks(gmove):
    STEPS = [ [0, 1], [1, 0], [1, 1], [-1, 1] ]
    match = gmove.match
    piece = match.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)
    #frdlytouches_before_count = 0
    enmytouches_before_count = 0
    #frdlytouches_after_count = 0
    enmytouches_after_count = 0

    for step in STEPS:
        stepx = step[0]
        stepy = step[1]
        x1, y1, x2, y2 = match.search_bi_dirs(gmove.dstx, gmove.dsty, stepx, stepy)
        if(x1 is not None):
            if((x1 == gmove.srcx and y1 == gmove.srcy) or
               (x2 == gmove.srcx and y2 == gmove.srcy)):
                    continue
            piece1 = match.readfield(x1, y1)
            piece2 = match.readfield(x2, y2)
            if(match.color_of_piece(piece1) == match.color_of_piece(piece2)):
                continue
            if(match.color_of_piece(piece1) == color):
                frdlytouches, enmytouches = list_all_field_touches(match, color, x1, y1)
            else:
                frdlytouches, enmytouches = list_all_field_touches(match, color, x2, y2)
            enmytouches_before_count += len(enmytouches)

    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

    for step in STEPS:
        stepx = step[0]
        stepy = step[1]
        x1, y1, x2, y2 = match.search_bi_dirs(gmove.dstx, gmove.dsty, stepx, stepy)
        if(x1 is not None):
            if((x1 == gmove.srcx and y1 == gmove.srcy) or
               (x2 == gmove.srcx and y2 == gmove.srcy)):
                    continue
            piece1 = match.readfield(x1, y1)
            piece2 = match.readfield(x2, y2)
            if(match.color_of_piece(piece1) == match.color_of_piece(piece2)):
                continue
            if(match.color_of_piece(piece1) == color):
                frdlytouches, enmytouches = list_all_field_touches(match, color, x1, y1)
            else:
                frdlytouches, enmytouches = list_all_field_touches(match, color, x2, y2)
            enmytouches_after_count += len(enmytouches)

    match.undo_move()

    if(enmytouches_after_count < enmytouches_before_count):
           return True
    else:
        return False


def running_pawn_in_endgame(gmove):
    if(gmove.match.is_endgame()):
        piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
        if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
            cpawn = cPawn(gmove.match, gmove.srcx, gmove.srcy)
            return cpawn.is_running()
    return False


def defends_invasion(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)
    board =  [[0] * 8 for i in range(8)]

    for y in range(8):
        for x in range(8):
            piece = match.readfield(x, y)
            if(match.color_of_piece(piece) == COLORS['white']):
                board[y][x] += 1
            elif(match.color_of_piece(piece) == COLORS['black']):
                board[y][x] -= 1
   
    return False

def controles_file(gmove):
    match = gmove.match
    piece = match.readfield(gmove.srcx, gmove.srcy)

    if(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        cbishop = cBishop(match, gmove.srcx, gmove.srcy)
        return cbishop.move_controles_file(gmove.dstx, gmove.dsty)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        crook = cRook(match, gmove.srcx, gmove.srcy)
        return crook.move_controles_file(gmove.dstx, gmove.dsty)
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        cqueen = cQueen(match, gmove.srcx, gmove.srcy)
        return cqueen.move_controles_file(gmove.dstx, gmove.dsty)
    else:
        return False

def is_tactical_draw(gmove):
    newmatch = copy.deepcopy(gmove.match)
    newmatch.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

    #if(newmatch.board.fifty_moves_count >= 49):
        #return True

    if(len(newmatch.move_list) < 9):
        return False

    boards = []
    for i in range(9):
        str_board = ""
        for y in range(8):
            for x in range(8):
                piece = newmatch.readfield(x, y)
                str_board += reverse_lookup(PIECES, piece)
        boards.append(str_board)
        newmatch.undo_move()

    count = 0
    str_board = boards[0]
    for i in range(1, 9):
        if(boards[i] == str_board):
            count += 1

    return count >= 2


def is_progress(gmove):
    match = gmove.match
    if(match.is_opening()):
        piece = match.readfield(gmove.srcx, gmove.srcy)
        if(piece == PIECES['wPw']):
            if(gmove.srcy == match.board.COORD['2'] and 
               gmove.srcx >= match.board.COORD['3'] and gmove.srcx <= match.board.COORD['6']):
                return True
        elif(piece == PIECES['bPw']):
            if(gmove.srcy == match.board.COORD['7'] and 
               gmove.srcx >= match.board.COORD['3'] and gmove.srcx <= match.board.COORD['6']):
                return True
        elif(piece == PIECES['wKn']):
            if(gmove.srcy == match.board.COORD['1'] and 
               (gmove.srcx == match.board.COORD['2'] or gmove.srcx == match.board.COORD['7'])):
                return True
        elif(piece == PIECES['bKn']):
            if(gmove.srcy == match.board.COORD['8'] and 
               (gmove.srcx == match.board.COORD['2'] or gmove.srcx == match.board.COORD['7'])):
                return True
        elif(piece == PIECES['wBp']):
            if(gmove.srcy == match.board.COORD['1'] and 
               (gmove.srcx == match.board.COORD['3'] or gmove.srcx == match.board.COORD['6'])):
                return True
        elif(piece == PIECES['bBp']):
            if(gmove.srcy == match.board.COORD['8'] and 
               (gmove.srcx == match.board.COORD['3'] or gmove.srcx == match.board.COORD['6'])):
                return True
        return False
    else:
        return False


def rank_gmoves(match, priomoves, piecescnt, last_pmove, dbggmove, dbgprio):
    all_attacking = []
    all_supporting = []
    all_fork_defending = []
    all_discl_attacking = []
    all_discl_supporting = []
    all_fleeing = []
    all_running = []
    excludes = []

    for priomove in priomoves:
        gmove = priomove.gmove
        from_dstfield_attacked, from_dstfield_supported = find_attacks_and_supports_after_move(gmove)
        frdlytouches_on_dstfield, enmytouches_on_dstfield = find_attacks_on_and_supports_of_dstfield_after_move(gmove)
        discl_attacked, discl_supported = find_disclosures(match, gmove)

        if(len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield) and 
           is_piece_lfe_attacker_on_dstfield(gmove, enmytouches_on_dstfield) and 
           match.is_soft_pin(gmove.srcx, gmove.srcy)[0] == False):
            subtactic = priomove.SUB_TACTICS['good-deal']
        else:
            subtactic = priomove.SUB_TACTICS['bad-deal']

        if(defends_check(match)):
            if(subtactic == priomove.SUB_TACTICS['good-deal'] and
               match.is_soft_pin(gmove.srcx, gmove.srcy)[0] == False):
                priomove.tactics.append(cTactic(priomove.TACTICS['defends-check'], priomove.SUB_TACTICS['good-deal']))
            else:
                priomove.tactics.append(cTactic(priomove.TACTICS['defends-check'], priomove.SUB_TACTICS['bad-deal']))

        if(castles(gmove)):
            match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
            cking = cKing(match, gmove.dstx, gmove.dsty)
            is_king_safe = cking.is_safe()
            match.undo_move()
            if(is_king_safe):
                priomove.tactics.append(cTactic(priomove.TACTICS['castles'], priomove.SUB_TACTICS['good-deal']))
            else:
                priomove.tactics.append(cTactic(priomove.TACTICS['castles'], priomove.SUB_TACTICS['bad-deal']))

        if(is_tactical_draw(gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['is-tactical-draw'], priomove.SUB_TACTICS['neutral']))

        if(promotes(gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['promotes'], subtactic))

        if(captures(gmove)):
            if(subtactic == priomove.SUB_TACTICS['good-deal'] or
               is_piece_lfe_captured(gmove)):
                if(is_captured_pinned_or_soft_pinned(gmove)):
                    priomove.tactics.append(cTactic(priomove.TACTICS['captures'], priomove.SUB_TACTICS['stormy']))
                else:
                    priomove.tactics.append(cTactic(priomove.TACTICS['captures'], priomove.SUB_TACTICS['good-deal']))
            else:
                priomove.tactics.append(cTactic(priomove.TACTICS['captures'], subtactic))

        if(does_unpin(gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['unpins'], subtactic))

        if(defends_fork(gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['defends-fork'], subtactic))
            all_fork_defending.append(priomove)

        if(is_fork_move(gmove, from_dstfield_attacked)):
            priomove.tactics.append(cTactic(priomove.TACTICS['forks'], subtactic))

        if(threatens_fork(gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['threatens-fork'], subtactic))

        if(flees(gmove)):
            if(subtactic == priomove.SUB_TACTICS['good-deal']):
                piece = match.readfield(gmove.srcx, gmove.srcy)
                friends, enemies = list_all_field_touches(match, match.color_of_piece(piece), gmove.srcx, gmove.srcy)
                if(len(friends) < len(enemies) or
                   is_piece_le_attacker_on_srcfield(gmove, enemies) == False):
                    priomove.tactics.append(cTactic(priomove.TACTICS['flees'], priomove.SUB_TACTICS['urgent']))
                elif(len(friends) == 0):
                    priomove.tactics.append(cTactic(priomove.TACTICS['flees'], priomove.SUB_TACTICS['neutral']))
            all_fleeing.append(priomove)

        if(len(from_dstfield_attacked) > 0):
            attack_subtactic = subtactic
            if(attack_subtactic == priomove.SUB_TACTICS['bad-deal']):
                if(is_piece_lower_attacker_on_dstfield(gmove, enmytouches_on_dstfield) and 
                   len(frdlytouches_on_dstfield) > 0):
                    attack_subtactic = priomove.SUB_TACTICS['good-deal']

            for attacked in from_dstfield_attacked:
                if(attacked.piece == PIECES['wKg'] or 
                   attacked.piece == PIECES['bKg']):
                    if(check_mates(gmove)):
                        priomove.tactics.append(cTactic(priomove.TACTICS['attacks-king'], priomove.SUB_TACTICS['urgent']))
                    else:
                        priomove.tactics.append(cTactic(priomove.TACTICS['attacks-king'], attack_subtactic))
                elif(subtactic == priomove.SUB_TACTICS['good-deal'] and 
                   is_attacked_soft_pinned(gmove, attacked)):
                    priomove.tactics.append(cTactic(priomove.TACTICS['attacks'], priomove.SUB_TACTICS['stormy']))
                else:
                    priomove.tactics.append(cTactic(priomove.TACTICS['attacks'], attack_subtactic))
            all_attacking.append(priomove)

        if(len(from_dstfield_supported) > 0):
            if(subtactic == priomove.SUB_TACTICS['good-deal'] and 
               is_supported_le_attacker(from_dstfield_supported)):
                support_subtactic = priomove.SUB_TACTICS['good-deal']
            else:
                support_subtactic = priomove.SUB_TACTICS['bad-deal']

            for supported in from_dstfield_supported:
                if(is_supported_running_pawn(match, supported)):
                    support_tactic = priomove.TACTICS['supports-running-pawn']
                elif(len(supported.attacker_beyond) > 0):
                    support_tactic = priomove.TACTICS['supports']
                else:
                    support_tactic = priomove.TACTICS['supports-unattacked']

                if(support_subtactic == priomove.SUB_TACTICS['good-deal'] and 
                   len(supported.attacker_beyond) > 0 and
                   (is_supporter_lower_attacker(gmove, supported) or
                    match.is_soft_pin(supported.fieldx, supported.fieldy)[0])):
                    support_subtactic = priomove.SUB_TACTICS['urgent']

                priomove.tactics.append(cTactic(support_tactic, support_subtactic))
            all_supporting.append(priomove)

        if(len(discl_attacked) > 0):
            if(is_discl_attacked_supported(discl_attacked) == False):
                priomove.tactics.append(cTactic(priomove.TACTICS['attacks'], priomove.SUB_TACTICS['good-deal']))
            else:
                priomove.tactics.append(cTactic(priomove.TACTICS['attacks'], priomove.SUB_TACTICS['bad-deal']))
            all_discl_attacking.append(priomove)

        if(len(discl_supported) > 0):
            if(is_discl_supported_weak(discl_supported)):
                priomove.tactics.append(cTactic(priomove.TACTICS['supports'], priomove.SUB_TACTICS['good-deal']))
            else:
                priomove.tactics.append(cTactic(priomove.TACTICS['supports'], priomove.SUB_TACTICS['bad-deal']))
            all_discl_supporting.append(priomove)

        if(blocks(gmove)):
            block_subtactic = subtactic
            if(block_subtactic == priomove.SUB_TACTICS['bad-deal']):
                if(is_piece_lower_attacker_on_dstfield(gmove, enmytouches_on_dstfield) and 
                   len(frdlytouches_on_dstfield) > 0):
                    block_subtactic = priomove.SUB_TACTICS['good-deal']
            priomove.tactics.append(cTactic(priomove.TACTICS['blocks'], block_subtactic))

        if(running_pawn_in_endgame(gmove)):
            if(len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield)):
                priomove.tactics.append(cTactic(priomove.TACTICS['is-running-pawn'], priomove.SUB_TACTICS['good-deal']))
            else:
                priomove.tactics.append(cTactic(priomove.TACTICS['is-running-pawn'], priomove.SUB_TACTICS['bad-deal']))
            all_running.append(priomove)

        if(controles_file(priomove.gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['controles-file'], subtactic))

        if(is_progress(gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['is-progress'], priomove.SUB_TACTICS['neutral']))

        if(len(priomove.tactics) > 0):
            piece = match.readfield(gmove.srcx, gmove.srcy)
            priomove.evaluate_priorities(piece)

    all_attacking.sort(key=attrgetter('prio'))
    for pmove in all_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(priomove.TACTICS['attacks'])
            piece = match.readfield(pmove.gmove.srcx, pmove.gmove.srcy)
            pmove.evaluate_priorities(piece)

    excludes.clear()
    all_discl_attacking.sort(key=attrgetter('prio'))
    for pmove in all_discl_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['attacks'])
            piece = match.readfield(pmove.gmove.srcx, pmove.gmove.srcy)
            pmove.evaluate_priorities(piece)

    excludes.clear()
    all_supporting.sort(key=attrgetter('prio'))
    for pmove in all_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['supports'])
            piece = match.readfield(pmove.gmove.srcx, pmove.gmove.srcy)
            pmove.evaluate_priorities(piece)

    excludes.clear()
    all_discl_supporting.sort(key=attrgetter('prio'))
    for pmove in all_discl_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['supports'])
            piece = match.readfield(pmove.gmove.srcx, pmove.gmove.srcy)
            pmove.evaluate_priorities(piece)

    excludes.clear()
    all_fork_defending.sort(key=attrgetter('prio'))
    for pmove in all_fork_defending:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['defends-fork'])
            piece = match.readfield(pmove.gmove.srcx, pmove.gmove.srcy)
            pmove.evaluate_priorities(piece)

    excludes.clear()
    all_fleeing.sort(key=attrgetter('prio'))
    for pmove in all_fleeing:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['flees'])
            piece = match.readfield(pmove.gmove.srcx, pmove.gmove.srcy)
            pmove.evaluate_priorities(piece)

    """excludes.clear()
    all_running.sort(key=attrgetter('prio'))
    for pmove in all_running:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(pmove.TACTICS['is-running-pawn'])
            pmove.evaluate_priorities()"""

    if(dbggmove):
        for priomove in priomoves:
            if(priomove.gmove.srcx == dbggmove.srcx and 
               priomove.gmove.srcy == dbggmove.srcy and 
               priomove.gmove.dstx == dbggmove.dstx and 
               priomove.gmove.dsty == dbggmove.dsty):
                priomove.prio = dbgprio
                break
    priomoves.sort(key=attrgetter('prio'))
