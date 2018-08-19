from operator import attrgetter
import copy
from .match import *
from .matchmove import do_move, undo_move
from . import analyze_position # score_supports, score_attacks, score_opening, score_endgame, is_endgame
from .helper import reverse_lookup
from .analyze_helper import * #dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker, dstfield_is_attacked, piece_is_lower_fairy_equal_than_enemy_on_dstfield, field_touches, search_lines_of_pin, list_field_touches, field_touches_beyond, is_discl_supported_weak, search_opposed_pieces, is_piece_attacked, is_supported_attacked
from .pieces import pawn, knight, bishop, rook, king, queen
from .pieces import pawn_ext, knight_ext, bishop_ext, rook_ext, king_ext, queen_ext

def castles(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    if(piece == match.PIECES['wKg'] or piece == match.PIECES['bKg']):
        if(gmove.srcx - gmove.dstx == 2 or gmove.srcx - gmove.dstx == -2):
            return True


def promotes(match, gmove):
    if(gmove.prom_piece != match.PIECES['blk']):
        return True


def captures(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    color = match.color_of_piece(piece)

    dstpiece = match.readfield(gmove.dstx, gmove.dsty)

    if(dstpiece != match.PIECES['blk']):
        return True
    elif( (piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']) and gmove.srcx != gmove.dstx ):
        return True
    else:
        return False


def defends_fork(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    return defends_fork_field(match, piece, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)


def flees(match, gmove):
    old_lower_cnt = 0
    old_higher_cnt = 0
    new_lower_cnt = 0
    new_higher_cnt = 0

    piece = match.readfield(gmove.srcx, gmove.srcy)

    color = match.color_of_piece(piece)
    opp_color = match.oppcolor_of_piece(piece)

    enmycontacts = list_field_touches(match, opp_color, gmove.srcx, gmove.srcy)
    for enmy in enmycontacts:
        if(match.PIECES_RANK[enmy.piece] < match.PIECES_RANK[piece]):
            old_lower_cnt += 1
        else:
            old_higher_cnt += 1
    enmycontacts.clear()

    ###
    do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

    enmycontacts = list_field_touches(match, opp_color, gmove.dstx, gmove.dsty)
    for enmy in enmycontacts:
        if(match.PIECES_RANK[enmy.piece] < match.PIECES_RANK[piece]):
            new_lower_cnt += 1
        else:
            new_higher_cnt += 1

    undo_move(match)
    ###

    if((old_lower_cnt + old_higher_cnt) > 0 and 
       (new_lower_cnt < old_lower_cnt or 
        new_lower_cnt + new_higher_cnt < old_lower_cnt + old_higher_cnt)):
        return True
    else:
        return False


def attacks_and_supports(match, gmove):
    attacked = []
    supported = []

    piece = match.readfield(gmove.srcx, gmove.srcy)

    if(piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']):
        pawn_ext.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
    elif(piece == match.PIECES['wKn'] or piece == match.PIECES['bKn']):
        knight_ext.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
    elif(piece == match.PIECES['wBp'] or piece == match.PIECES['bBp']):
        bishop_ext.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
    elif(piece == match.PIECES['wRk'] or piece == match.PIECES['bRk']):
        rook_ext.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
    elif(piece == match.PIECES['wQu'] or piece == match.PIECES['bQu']):
        rook_ext.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
        bishop_ext.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
    elif(piece == match.PIECES['wKg'] or piece == match.PIECES['bKg']):
        king_ext.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
        if(gmove.srcx - gmove.dstx == -2):
            rook_ext.attacks_and_supports(match, gmove.dstx + 1, gmove.srcy, gmove.dstx - 1, gmove.dsty, attacked, supported)
        elif(gmove.srcx - gmove.dstx == 2):
            rook_ext.attacks_and_supports(match, gmove.dstx - 2, gmove.srcy, gmove.dstx + 1, gmove.dsty, attacked, supported)

    return attacked, supported


def does_unpin(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)

    pinlines_before = search_lines_of_pin(match, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)

    ###
    do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    
    pinlines_after = search_lines_of_pin(match, color, gmove.dstx, gmove.dsty, None, None)

    undo_move(match)
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
    if(match.next_color() == match.COLORS['white']):
        kg_x = match.wKg_x
        kg_y = match.wKg_y
    else:
        kg_x = match.bKg_x
        kg_y = match.bKg_y

    if(match.is_king_attacked(kg_x, kg_y)):
        return True


def defends_king_attack(match, gmove):
    color = match.next_color()
    before_cnt = 0
    after_cnt = 0
    urgent = True

    if(color == match.COLORS['white']):
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
    else:
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y

    for i in range(8):
        x1 = Kg_x + king.cKing.STEPS[i][0]
        y1 = Kg_y + king.cKing.STEPS[i][1]
        if(match.is_inbounds(x1, y1)):
            friends, enemies = field_touches(match, color, x1, y1)
            if(len(friends) < len(enemies)):
                before_cnt += 1
            if(len(enemies) == 0):
                urgent = False

    do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

    if(Kg_x == gmove.srcx):
        Kg_x = gmove.dstx
        Kg_y = gmove.dsty

    for i in range(8):
        x1 = Kg_x + king.cKing.STEPS[i][0]
        y1 = Kg_y + king.cKing.STEPS[i][1]
        if(match.is_inbounds(x1, y1)):
            friends, enemies = field_touches(match, color, x1, y1)
            if(len(friends) < len(enemies)):
                after_cnt += 1

    undo_move(match)

    if(before_cnt > after_cnt):
        return True, urgent
    else:
        return False, False


def disclosures(match, gmove):
    discl_attacked = []
    discl_supported = []

    piece = match.readfield(gmove.srcx, gmove.srcy)

    color = match.color_of_piece(piece)

    do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

    excluded_dir = rook.cRook.dir_for_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)
    rook_ext.disclosures(match, color, excluded_dir, gmove.srcx, gmove.srcy, discl_attacked, discl_supported)

    excluded_dir = bishop.cBishop.dir_for_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)
    bishop_ext.disclosures(match, color, excluded_dir, gmove.srcx, gmove.srcy, discl_attacked, discl_supported)

    undo_move(match)

    ###
    match.writefield(gmove.srcx, gmove.srcy, match.PIECES['blk'])

    for ctouch_beyond in discl_attacked:
        field_touches_beyond(match, color, ctouch_beyond)

    for ctouch_beyond in discl_supported:
        field_touches_beyond(match, color, ctouch_beyond)

    match.writefield(gmove.srcx, gmove.srcy, piece)
    ###
    
    return discl_attacked, discl_supported


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty): # , forked
    if(piece == match.PIECES['wQu'] or piece == match.PIECES['bQu']):
        rflag = rook_ext.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
        bflag = bishop_ext.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
        return rflag or bflag
    elif(piece == match.PIECES['wRk'] or piece == match.PIECES['bRk']):
        return rook_ext.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == match.PIECES['wBp'] or piece == match.PIECES['bBp']):
        return bishop_ext.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == match.PIECES['wKn'] or piece == match.PIECES['bKn']):
        return knight_ext.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == match.PIECES['wKg'] or piece == match.PIECES['bKg']):
        return king_ext.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']):
        return pawn_ext.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    else:
        return False


def blocks(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    color = match.color_of_piece(piece)

    oppenents = search_opposed_pieces(match, color, gmove.dstx, gmove.dsty, gmove.srcx, gmove.srcy)

    count = 0
    for oppenent in oppenents:
        if(match.PIECES_RANK[oppenent[0].piece] > match.PIECES_RANK[oppenent[1].piece] or
           match.PIECES_RANK[oppenent[0].piece] >= match.PIECES_RANK[piece]):
            count += 1

    return count > 0


def running_pawn_in_endgame(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    if(analyze_position.is_endgame(match)):
        if(piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']):
            return pawn_ext.is_running(match, gmove.srcx, gmove.srcy)

    return False


def controles_file(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    color = match.color_of_piece(piece)

    if(piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']):
        return False
    elif(piece == match.PIECES['wKn'] or piece == match.PIECES['bKn']):
        return False
    elif(piece == match.PIECES['wBp'] or piece == match.PIECES['bBp']):
        if(bishop.controles_file(match, piece, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)):
            return True
    elif(piece == match.PIECES['wRk'] or piece == PIECES['bRk']):
        if(rook.controles_file(match, piece, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)):
            return True
    elif(piece == PIECES['wQu'] or piece == match.PIECES['bQu']):
        if(rook.controles_file(match, piece, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)):
            return True
        if(bishop.controles_file(match, piece, color, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)):
            return True

    return False


def is_tactical_draw(match, gmove):
    newmatch = copy.deepcopy(match)
    do_move(newmatch, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

    #if(newmatch.fifty_moves_count >= 49):
        #return True

    if(len(newmatch.move_list) < 5):
        return False

    boards = []
    for idx in range(min(len(newmatch.move_list), 10)):
        board = ""
        for y in range(8):
            for x in range(8):
                piece = newmatch.readfield(x, y)
                board += reverse_lookup(match.PIECES, piece)
        boards.append(board)

        undo_move(newmatch)

    idx = 0
    count = 0
    lastboard = boards[-1]
    for board in boards:
        idx += 1
        if(idx > 1 and idx % 2 == 1):
            if(board == lastboard):
                count += 1

    if(count >= 3):
        return True
    else:
        return False


def fetch_first_tactics(priomove):
    return priomove.fetch_tactics(0)

def rank_gmoves(match, priomoves, depth, slimits, last_pmove):
    all_attacking = []
    all_supporting = []
    all_fork_defending = []
    all_discl_attacking = []
    all_discl_supporting = []
    all_fleeing = []
    excludes = []
    
    for priomove in priomoves:
        if(defends_check(match)):
            priomove.tactics.append(priomove.TACTICS['defend-check'])

        attacked, supported = attacks_and_supports(match, priomove.gmove)

        dstfld_cnt_of_supp_is_equ_or_high_than_cnt_of_att = dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove)
        dstflield_is_attacked = dstfield_is_attacked(match, priomove.gmove)
        piece_is_lower_fequal_than_enmy_on_dstflield = piece_is_lower_fairy_equal_than_enemy_on_dstfield(match, priomove.gmove)

        defends_king, urgent = defends_king_attack(match, priomove.gmove)
        if(urgent):
            priomove.tactics.append(priomove.TACTICS['defend-king-attack-urgent'])
        elif(defends_king and 
             dstfld_cnt_of_supp_is_equ_or_high_than_cnt_of_att):
            priomove.tactics.append(priomove.TACTICS['defend-king-attack'])

        if(castles(match, priomove.gmove)):
            priomove.tactics.append(priomove.TACTICS['castling'])

        if(is_tactical_draw(match, priomove.gmove)):
            priomove.tactics.append(priomove.TACTICS['tactical-draw'])

        if(promotes(match, priomove.gmove)):
            priomove.tactics.append(priomove.TACTICS['promotion'])

        if(captures(match, priomove.gmove)):
            if(piece_is_lower_equal_than_captured(match, priomove.gmove) or
               dstflield_is_attacked == False or
               (dstfld_cnt_of_supp_is_equ_or_high_than_cnt_of_att and 
                piece_is_lower_fequal_than_enmy_on_dstflield)):
                priomove.tactics.append(priomove.TACTICS['capture-good-deal'])
            else:
                priomove.tactics.append(priomove.TACTICS['capture-bad-deal'])

        if(does_unpin(match, priomove.gmove)):
            priomove.tactics.append(priomove.TACTICS['does-unpin'])

        if(defends_fork(match, priomove.gmove)):
            if(dstflield_is_attacked == False or 
               (dstfld_cnt_of_supp_is_equ_or_high_than_cnt_of_att and 
                piece_is_lower_fequal_than_enmy_on_dstflield)):
                priomove.tactics.append(priomove.TACTICS['defend-fork'])
                all_fork_defending.append(priomove)
            else:
                priomove.tactics.append(priomove.TACTICS['support-bad-deal'])

        if(flees(match, priomove.gmove)):
            if(dstflield_is_attacked == False or
                (dstfld_cnt_of_supp_is_equ_or_high_than_cnt_of_att 
                 and piece_is_lower_equal_than_enemy_on_dstfield(match, priomove.gmove))):
                if(srcfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove) == False or
                   piece_is_lower_equal_than_enemy_on_srcfield(match, priomove.gmove) == False):
                    priomove.tactics.append(priomove.TACTICS['flee-urgent'])
                    all_fleeing.append(priomove)
                elif(srcfield_is_supported(match, priomove.gmove) == False):
                    priomove.tactics.append(priomove.TACTICS['flee'])

        if(len(attacked) > 0):
            if(is_piece_attacked(attacked, match.PIECES['wKg'], match.PIECES['bKg'])):
                if(dstflield_is_attacked == False or 
                   (dstfld_cnt_of_supp_is_equ_or_high_than_cnt_of_att and 
                    piece_is_lower_fequal_than_enmy_on_dstflield)):
                    priomove.tactics.append(priomove.TACTICS['attack-king-good-deal'])
                else:
                    priomove.tactics.append(priomove.TACTICS['attack-king-bad-deal'])
            else:
                if(dstflield_is_attacked == False or 
                   (dstfld_cnt_of_supp_is_equ_or_high_than_cnt_of_att and 
                    piece_is_lower_fequal_than_enmy_on_dstflield)):
                    if(is_attacked_pinned(match, attacked) or 
                       is_attacked_soft_pinned(match, attacked)):
                        priomove.tactics.append(priomove.TACTICS['attack-stormy'])
                        all_attacking.append(priomove)
                    elif(is_attacked_supported(attacked) == False or 
                         is_attacked_higher_equal_than_piece(match, attacked)):
                        priomove.tactics.append(priomove.TACTICS['attack-good-deal'])
                        all_attacking.append(priomove)
                    else:
                        priomove.tactics.append(priomove.TACTICS['attack-bad-deal'])
                else:
                    priomove.tactics.append(priomove.TACTICS['attack-bad-deal'])

        if(len(supported) > 0):
            if(is_supported_weak(match, supported)): # is_supported_attacked(supported)
                if(dstflield_is_attacked == False or 
                   (dstfld_cnt_of_supp_is_equ_or_high_than_cnt_of_att and 
                    piece_is_lower_fequal_than_enmy_on_dstflield)):
                    if(is_supported_lower_equal_than_attacker(match, supported)):
                        priomove.tactics.append(priomove.TACTICS['support-good-deal'])
                        all_supporting.append(priomove)
                    else:
                        priomove.tactics.append(priomove.TACTICS['support-bad-deal'])
                else:
                    priomove.tactics.append(priomove.TACTICS['support-bad-deal'])
            else:
                if(dstflield_is_attacked == False or 
                   dstfld_cnt_of_supp_is_equ_or_high_than_cnt_of_att):
                    priomove.tactics.append(priomove.TACTICS['support-unattacked'])
                else:
                    priomove.tactics.append(priomove.TACTICS['support-bad-deal'])

        discl_attacked, discl_supported = disclosures(match, priomove.gmove)

        if(len(discl_attacked) > 0):
            if(is_discl_attacked_supported(discl_attacked) == False):
                priomove.tactics.append(priomove.TACTICS['attack-good-deal'])
                all_discl_attacking.append(priomove)
            else:
                priomove.tactics.append(priomove.TACTICS['attack-bad-deal'])

        if(len(discl_supported) > 0):
            if(is_discl_supported_weak(discl_supported)): # is_discl_supported_attacked(discl_supported)
                priomove.tactics.append(priomove.TACTICS['support-good-deal'])
                all_discl_supporting.append(priomove)
            else:
                priomove.tactics.append(priomove.TACTICS['support-bad-deal'])

        if(blocks(match, priomove.gmove)):
            priomove.tactics.append(priomove.TACTICS['block'])

        if(running_pawn_in_endgame(match, priomove.gmove)):
            priomove.tactics.append(priomove.TACTICS['running-pawn-in-endgame'])

        """if(controles_file(match, priomove.gmove)):
            if(dstflield_is_attacked == False or 
               (dstfield_is_supported(match, priomove.gmove) and 
                piece_is_lower_fequal_than_enmy_on_dstflield)):
                priomove.tactics.append(priomove.TACTICS['controles-file-good-deal'])"""

        if(len(priomove.tactics) > 0):
            priomove.tactics.sort()
            priomove.prio = priomove.TACTICS_TO_PRIO[priomove.fetch_tactics(0)]
            priomove.prio_sec = priomove.TACTICS_TO_PRIO[priomove.fetch_tactics(1)]
        else:
            priomove.tactics.append(priomove.TACTICS['undefined'])
            priomove.prio = priomove.PRIO['prio10']
            priomove.prio_sec = priomove.PRIO['prio10']

    all_attacking.sort(key = fetch_first_tactics)
    for pmove in all_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
             pmove.downgrade(priomove.TACTICS['attack-stormy'], priomove.TACTICS['attack-downgraded'])
             pmove.downgrade(priomove.TACTICS['attack-good-deal'], priomove.TACTICS['attack-downgraded'])
             pmove.tactics.sort()
             pmove.prio = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
             pmove.prio_sec = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    excludes.clear()
    all_discl_attacking.sort(key = fetch_first_tactics)
    for pmove in all_discl_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(priomove.TACTICS['discl-attack-good-deal'], priomove.TACTICS['attack-downgraded'])
            pmove.tactics.sort()
            pmove.prio = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
            pmove.prio_sec = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    excludes.clear()
    all_supporting.sort(key = fetch_first_tactics)
    for pmove in all_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(priomove.TACTICS['support-good-deal'], priomove.TACTICS['support-downgraded'])
            pmove.tactics.sort()
            pmove.prio = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
            pmove.prio_sec = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    excludes.clear()
    all_discl_supporting.sort(key = fetch_first_tactics)
    for pmove in all_discl_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(priomove.TACTICS['discl-support-good-deal'], priomove.TACTICS['support-downgraded'])
            pmove.tactics.sort()
            pmove.prio = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
            pmove.prio_sec = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    excludes.clear()
    all_fork_defending.sort(key = fetch_first_tactics)
    for pmove in all_fork_defending:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(priomove.TACTICS['defend-fork'], priomove.TACTICS['defend-fork-downgraded'])
            pmove.tactics.sort()
            pmove.prio = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
            pmove.prio_sec = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    excludes.clear()
    all_fleeing.sort(key = fetch_first_tactics)
    for pmove in all_fleeing:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(priomove.TACTICS['flee-urgent'], priomove.TACTICS['flee-downgraded'])
            pmove.tactics.sort()
            pmove.prio = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
            pmove.prio_sec = priomove.TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    priomoves.sort(key=attrgetter('prio', 'prio_sec'))


