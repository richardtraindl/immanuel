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
from .pieces.piece import cTouchBeyond
from .generator import cGenerator
from .validator import *


def castles(gmove):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(gmove.srcx - gmove.dstx == 2 or gmove.srcx - gmove.dstx == -2):
            return True


def promotes(gmove):
    if(gmove.prom_piece != PIECES['blk']):
        return True


def captures(gmove):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    color = gmove.match.color_of_piece(piece)
    dstpiece = gmove.match.readfield(gmove.dstx, gmove.dsty)
    if(dstpiece != PIECES['blk']):
        return True
    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and gmove.srcx != gmove.dstx ):
        return True
    else:
        return False


def defends_fork(gmove):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    return defends_fork_field(gmove.match, piece, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)


def flees(gmove):
    match = gmove.match
    old_lower_cnt = 0
    old_higher_cnt = 0
    new_lower_cnt = 0
    new_higher_cnt = 0
    piece = match.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)
    opp_color = match.oppcolor_of_piece(piece)
    enmycontacts = list_field_touches(match, opp_color, gmove.srcx, gmove.srcy)
    for enmy in enmycontacts:
        if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
            old_lower_cnt += 1
        else:
            old_higher_cnt += 1
    enmycontacts.clear()
    ###
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    enmycontacts = list_field_touches(match, opp_color, gmove.dstx, gmove.dsty)
    for enmy in enmycontacts:
        if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
            new_lower_cnt += 1
        else:
            new_higher_cnt += 1
    match.undo_move()
    ###
    if((old_lower_cnt + old_higher_cnt) > 0 and 
       (new_lower_cnt < old_lower_cnt or 
        new_lower_cnt + new_higher_cnt < old_lower_cnt + old_higher_cnt)):
        return True
    else:
        return False


def find_attacks_and_supports(match, fieldx, fieldy):
    attacked = []
    supported = []

    piece = match.readfield(fieldx, fieldy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        cpawn = cPawn(match, fieldx, fieldy)
        cpawn.find_attacks_and_supports(fieldx, fieldy, attacked, supported)
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        cknight = cKnight(match, fieldx, fieldy)
        cknight.find_attacks_and_supports(fieldx, fieldy, attacked, supported)
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        cbishop = cBishop(match, fieldx, fieldy)
        cbishop.find_attacks_and_supports(fieldx, fieldy, attacked, supported)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        crook = cRook(match, fieldx, fieldy)
        crook.find_attacks_and_supports(fieldx, fieldy, attacked, supported)
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        cqueen = cQueen(match, fieldx, fieldy)
        cqueen.find_attacks_and_supports(fieldx, fieldy, attacked, supported)
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        cking = cKing(match, fieldx, fieldy)
        cking.find_attacks_and_supports(fieldx, fieldy, attacked, supported)
    return attacked, supported


def find_attacks_and_supports_from_srcfield(gmove):
    return find_attacks_and_supports(gmove.match, gmove.srcx, gmove.srcy)

    
def find_attacks_and_supports_from_dstfield_after_move(gmove):
    match = gmove.match
    piece = match.readfield(gmove.srcx, gmove.srcy)
    match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    attacked, supported = find_attacks_and_supports(gmove.match, gmove.dstx, gmove.dsty)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(gmove.srcx - gmove.dstx == -2):
            crook = cRook(match, gmove.dstx - 1, gmove.dsty)
            crook.find_attacks_and_supports(gmove.dstx - 1, gmove.dsty, attacked, supported)
        elif(gmove.srcx - gmove.dstx == 2):
            crook = cRook(match, gmove.dstx + 1, gmove.dsty)
            crook.find_attacks_and_supports(gmove.dstx + 1, gmove.dsty, attacked, supported)
    match.undo_move()
    return attacked, supported


def find_attacks_on_and_supports_of_srcfield(gmove):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    return list_all_field_touches(gmove.match, gmove.match.color_of_piece(piece), gmove.srcx, gmove.srcy)


def find_attacks_on_and_supports_of_dstfield_after_move(gmove):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    gmove.match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    frdlytouches, enmytouches = list_all_field_touches(gmove.match, gmove.match.color_of_piece(piece), gmove.dstx, gmove.dsty)
    gmove.match.undo_move()
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
    # is king attaked
    if(match.next_color() == COLORS['white']):
        return match.is_king_attacked(match.board.wKg_x, match.board.wKg_y)
    else:
        return match.is_king_attacked(match.board.bKg_x, match.board.bKg_y)


def find_disclosed_pieces(match, srcx, srcy, dstx, dsty, discl_attacked, discl_supported):
    piece = match.readfield(srcx, srcy)
    color = match.color_of_piece(piece)
    idx = 0
    for step in cQueen.STEPS:
        if(idx % 2 == 0):
            first = cTouchBeyond(None, None, None, None, PIECES['blk'], 0, 0)
            second = cTouchBeyond(None, None, None, None, PIECES['blk'], 0, 0)
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


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty): # , forked
    if(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        cqueen = cQueen(match, srcx, srcy)
        return cqueen.move_defends_forked_field(dstx, dsty)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        crook = cRook(match, srcx, srcy)
        return crook.move_defends_forked_field(dstx, dsty)
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        cbishop = cBishop(match, srcx, srcy)
        return cbishop.move_defends_forked_field(dstx, dsty)
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        cknight = cKnight(match, srcx, srcy)
        return cknight.move_defends_forked_field(dstx, dsty)
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        cking = cKing(match, srcx, srcy)
        return cking.move_defends_forked_field(dstx, dsty)
    elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        cpawn = cPawn(match, srcx, srcy)
        return cpawn.move_defends_forked_field(dstx, dsty)
    else:
        return False


def blocks(gmove):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    color = gmove.match.color_of_piece(piece)
    oppenents = search_opposed_pieces(gmove.match, color, gmove.dstx, gmove.dsty, gmove.srcx, gmove.srcy)
    for oppenent in oppenents:
        if(PIECES_RANK[oppenent[0].piece] > PIECES_RANK[oppenent[1].piece] and 
           PIECES_RANK[oppenent[0].piece] > PIECES_RANK[piece]):
            return True
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
    color = match.color_of_piece(piece)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return False
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        return False
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        if(bishop.controles_file(match, piece, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)):
            return True
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        if(rook.controles_file(match, piece, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)):
            return True
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        if(rook.controles_file(match, piece, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)):
            return True
        if(bishop.controles_file(match, piece, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)):
            return True

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
               gmove.srcx >= match.board.COORD['2'] and gmove.srcx <= match.board.COORD['7']):
                return True
        elif(piece == PIECES['bPw']):
            if(gmove.srcy == match.board.COORD['7'] and 
               gmove.srcx >= match.board.COORD['2'] and gmove.srcx <= match.board.COORD['7']):
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


def fetch_first_tactics(priomove):
    return priomove.fetch_tactics(0)

def rank_gmoves(match, priomoves, piecescnt, last_pmove):
    all_attacking = []
    all_supporting = []
    all_fork_defending = []
    all_discl_attacking = []
    all_discl_supporting = []
    all_fleeing = []
    all_running = []
    excludes = []

    for priomove in priomoves:
        from_srcfield_attacked, from_srcfield_supported = find_attacks_and_supports_from_srcfield(priomove.gmove)
        from_dstfield_attacked, from_dstfield_supported = find_attacks_and_supports_from_dstfield_after_move(priomove.gmove)
        frdlytouches_on_srcfield, enmytouches_on_srcfield = find_attacks_on_and_supports_of_srcfield(priomove.gmove)
        frdlytouches_on_dstfield, enmytouches_on_dstfield = find_attacks_on_and_supports_of_dstfield_after_move(priomove.gmove)
        discl_attacked, discl_supported = find_disclosures(match, priomove.gmove)
        is_piece_lfe_attacker_on_dstfield_flag = is_piece_lfe_attacker_on_dstfield(priomove.gmove, enmytouches_on_dstfield)

        if(defends_check(match)):
            if(len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield) and
               is_piece_lfe_attacker_on_dstfield_flag):
                subtactic = priomove.SUB_TACTICS['good-deal']
            else:
                subtactic = priomove.SUB_TACTICS['bad-deal']
            priomove.tactics.append(cTactic(priomove.TACTICS['defends-check'], subtactic))

        if(castles(priomove.gmove)):
            match.do_move(priomove.gmove.srcx, priomove.gmove.srcy, priomove.gmove.dstx, priomove.gmove.dsty, priomove.gmove.prom_piece)
            cking = cKing(match, priomove.gmove.dstx, priomove.gmove.dsty)
            is_king_safe = cking.is_king_safe()
            match.undo_move()
            if(is_king_safe):
                subtactic = priomove.SUB_TACTICS['good-deal']
            else:
                subtactic = priomove.SUB_TACTICS['bad-deal']
            priomove.tactics.append(cTactic(priomove.TACTICS['castles'], subtactic))

        if(is_tactical_draw(priomove.gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['is-tactical-draw'], priomove.SUB_TACTICS['good-deal']))

        if(promotes(priomove.gmove)):
            if(len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield) and 
               is_piece_lfe_attacker_on_dstfield_flag):
                subtactic = priomove.SUB_TACTICS['good-deal']
            else:
                subtactic = priomove.SUB_TACTICS['bad-deal']
            priomove.tactics.append(cTactic(priomove.TACTICS['promotes'], subtactic))

        if(captures(priomove.gmove)):
            if(is_piece_le_captured(priomove.gmove) or
               (len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield) and 
                is_piece_lfe_attacker_on_dstfield_flag) or
                is_captured_pinned_or_soft_pinned(priomove.gmove)):
                if(is_piece_le_attacker_on_srcfield(priomove.gmove, enmytouches_on_srcfield) == False):
                    priomove.tactics.append(cTactic(priomove.TACTICS['captures'], priomove.SUB_TACTICS['urgent']))
                else:
                    priomove.tactics.append(cTactic(priomove.TACTICS['captures'], priomove.SUB_TACTICS['good-deal']))
            else:
                priomove.tactics.append(cTactic(priomove.TACTICS['captures'], priomove.SUB_TACTICS['bad-deal']))

        if(does_unpin(priomove.gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['unpins'], priomove.SUB_TACTICS['good-deal']))

        if(defends_fork(priomove.gmove)):
            if(len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield) and 
               is_piece_lfe_attacker_on_dstfield_flag):
                priomove.tactics.append(cTactic(priomove.TACTICS['defends-fork'], priomove.SUB_TACTICS['good-deal']))
            else:
                priomove.tactics.append(cTactic(priomove.TACTICS['supports'], priomove.SUB_TACTICS['bad-deal']))
            all_fork_defending.append(priomove)

        if(flees(priomove.gmove)):
            if(len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield) and
               is_piece_le_attacker_on_dstfield(priomove.gmove, enmytouches_on_dstfield)):
                if(len(frdlytouches_on_srcfield) < len(enmytouches_on_srcfield) or
                   is_piece_le_attacker_on_srcfield(priomove.gmove, enmytouches_on_srcfield) == False):
                    priomove.tactics.append(cTactic(priomove.TACTICS['flees'], priomove.SUB_TACTICS['urgent']))
                elif(len(frdlytouches_on_srcfield) == 0):
                    priomove.tactics.append(cTactic(priomove.TACTICS['flees'], priomove.SUB_TACTICS['neutral']))
            all_fleeing.append(priomove)

        if(len(from_dstfield_attacked) > 0):
            if(len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield) and 
               is_piece_lfe_attacker_on_dstfield_flag):
                #if(piecescnt > 1 and len(enmytouches_on_srcfield) > 0):
                    #subtactic = priomove.SUB_TACTICS['downgraded']
                #else:
                subtactic = priomove.SUB_TACTICS['good-deal']
            else:
                subtactic = priomove.SUB_TACTICS['bad-deal']

            for attacked in from_dstfield_attacked:
                if(attacked.piece == PIECES['wKg'] or 
                   attacked.piece == PIECES['bKg']):
                    priomove.tactics.append(cTactic(priomove.TACTICS['attacks-king'], subtactic))
                elif(subtactic == priomove.SUB_TACTICS['good-deal'] and 
                   is_attacked_soft_pinned(priomove.gmove, attacked)):
                    priomove.tactics.append(cTactic(priomove.TACTICS['attacks'], priomove.SUB_TACTICS['stormy']))
                else:
                    priomove.tactics.append(cTactic(priomove.TACTICS['attacks'], subtactic))
            all_attacking.append(priomove)

        if(len(from_dstfield_supported) > 0):
            if(is_supported_le_attacker(from_dstfield_supported) and 
               len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield) and 
               is_piece_lfe_attacker_on_dstfield_flag):
                subtactic = priomove.SUB_TACTICS['good-deal']
            else:
                subtactic = priomove.SUB_TACTICS['bad-deal']

            for supported in from_dstfield_supported:
                if(is_supported_running_pawn(match, supported)):
                    priomove.tactics.append(cTactic(priomove.TACTICS['supports-running-pawn'], subtactic))
                elif(is_supported_weak(priomove.gmove, supported)):
                    priomove.tactics.append(cTactic(priomove.TACTICS['supports'], subtactic))
                else:
                    priomove.tactics.append(cTactic(priomove.TACTICS['supports-unattacked'], subtactic))
            all_supporting.append(priomove)

        if(len(discl_attacked) > 0):
            if(is_discl_attacked_supported(discl_attacked) == False):
                priomove.tactics.append(cTactic(priomove.TACTICS['attacks'], priomove.SUB_TACTICS['good-deal']))
            else:
                priomove.tactics.append(cTactic(priomove.TACTICS['attacks'], priomove.SUB_TACTICS['bad-deal']))
            all_discl_attacking.append(priomove)

        if(len(discl_supported) > 0):
            if(is_discl_supported_weak(discl_supported)): # is_discl_supported_attacked(discl_supported)
                priomove.tactics.append(cTactic(priomove.TACTICS['supports'], priomove.SUB_TACTICS['good-deal']))
            else:
                priomove.tactics.append(cTactic(priomove.TACTICS['supports'], priomove.SUB_TACTICS['bad-deal']))
            all_discl_supporting.append(priomove)

        if(blocks(priomove.gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['blocks'], priomove.SUB_TACTICS['good-deal']))

        if(running_pawn_in_endgame(priomove.gmove)):
            if(len(frdlytouches_on_dstfield) >= len(enmytouches_on_dstfield)):
                subtactic = priomove.SUB_TACTICS['good-deal']
            else:
                subtactic = priomove.SUB_TACTICS['bad-deal']
            priomove.tactics.append(cTactic(priomove.TACTICS['is-running-pawn'], subtactic))
            all_running.append(priomove)

        """if(controles_file(priomove.gmove)):
            if(len(supports_of_dstfield) >= len(attacks_on_dstfield) and 
               is_piece_lfe_attacker_on_dstfield_flag):
                priomove.tactics.append(cTactic(priomove.TACTICS['controles-file'], priomove.SUB_TACTICS['good-deal']))"""

        if(is_progress(priomove.gmove)):
            priomove.tactics.append(cTactic(priomove.TACTICS['is-progress'], priomove.SUB_TACTICS['neutral']))

        if(len(priomove.tactics) > 0):
            priomove.evaluate_priorities()

    all_attacking.sort(key=attrgetter('prio'))
    for pmove in all_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(cTactic(priomove.TACTICS['attacks'], priomove.SUB_TACTICS['downgraded']))
            pmove.evaluate_priorities()

    excludes.clear()
    all_discl_attacking.sort(key=attrgetter('prio'))
    for pmove in all_discl_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(cTactic(priomove.TACTICS['attacks-discl'], priomove.SUB_TACTICS['downgraded']))
            pmove.evaluate_priorities()

    excludes.clear()
    all_supporting.sort(key=attrgetter('prio'))
    for pmove in all_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(cTactic(priomove.TACTICS['supports'], priomove.SUB_TACTICS['downgraded']))
            pmove.evaluate_priorities()

    excludes.clear()
    all_discl_supporting.sort(key=attrgetter('prio'))
    for pmove in all_discl_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(cTactic(priomove.TACTICS['supports-discl'], priomove.SUB_TACTICS['downgraded']))
            pmove.evaluate_priorities()

    excludes.clear()
    all_fork_defending.sort(key=attrgetter('prio'))
    for pmove in all_fork_defending:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(cTactic(priomove.TACTICS['defends-fork'], priomove.SUB_TACTICS['downgraded']))
            pmove.evaluate_priorities()

    excludes.clear()
    all_fleeing.sort(key=attrgetter('prio'))
    for pmove in all_fleeing:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(cTactic(priomove.TACTICS['flees'], priomove.SUB_TACTICS['downgraded']))
            pmove.evaluate_priorities()

    excludes.clear()
    all_running.sort(key=attrgetter('prio'))
    for pmove in all_running:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(cTactic(priomove.TACTICS['is-running-pawn'], priomove.SUB_TACTICS['downgraded']))
            pmove.evaluate_priorities()

    priomoves.sort(key=attrgetter('prio'))
