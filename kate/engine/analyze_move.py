from operator import attrgetter
from .match import *
from .cvalues import *
from .matchmove import do_move, undo_move
#from .move import *
#from .calc import *
from . import rules
from .analyze_position import score_supports, score_attacks, score_opening, score_endgame, is_endgame, is_stormy
from .analyze_helper import *
from .pieces import pawn, knight, bishop, rook, king


def castles(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(gmove.srcx - gmove.dstx == 2 or gmove.srcx - gmove.dstx == -2):
            return True


def promotes(match, gmove):
    if(gmove.prom_piece != PIECES['blk']):
        return True


def captures(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    color = Match.color_of_piece(piece)

    dstpiece = match.readfield(gmove.dstx, gmove.dsty)

    if(dstpiece != PIECES['blk']):
        return True
    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and gmove.srcx != gmove.dstx ):
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

    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    enmycontacts = list_field_touches(match, opp_color, gmove.srcx, gmove.srcy)
    for enmy in enmycontacts:
        if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
            old_lower_cnt += 1
        else:
            old_higher_cnt += 1
    enmycontacts.clear()

    ###
    do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

    enmycontacts = list_field_touches(match, opp_color, gmove.dstx, gmove.dsty)
    for enmy in enmycontacts:
        if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
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

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        pawn.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        knight.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        bishop.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        rook.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        rook.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
        bishop.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        king.attacks_and_supports(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, attacked, supported)
        if(gmove.srcx - gmove.dstx == -2):
            rook.attacks_and_supports(match, gmove.dstx + 1, gmove.srcy, gmove.dstx - 1, gmove.dsty, attacked, supported)
        elif(gmove.srcx - gmove.dstx == 2):
            rook.attacks_and_supports(match, gmove.dstx - 2, gmove.srcy, gmove.dstx + 1, gmove.dsty, attacked, supported)

    return attacked, supported


def defends_check(match):
    # is king attaked
    if(match.next_color() == COLORS['white']):
        kg_x = match.wKg_x
        kg_y = match.wKg_y
    else:
        kg_x = match.bKg_x
        kg_y = match.bKg_y

    if(rules.is_king_attacked(match, kg_x, kg_y)):
        return True


def disclosures(match, gmove):
    discl_attacked = []
    discl_supported = []

    piece = match.readfield(gmove.srcx, gmove.srcy)

    color = Match.color_of_piece(piece)
    
    excluded_dir = rook.rk_dir(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)
    if(excluded_dir == rules.DIRS['undefined']):
        excluded_dir = bishop.bp_dir(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)

    do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

    rook.disclosures(match, color, excluded_dir, gmove.srcx, gmove.srcy, discl_attacked, discl_supported)

    bishop.disclosures(match, color, excluded_dir, gmove.srcx, gmove.srcy, discl_attacked, discl_supported)

    undo_move(match)

    ###
    match.writefield(gmove.srcx, gmove.srcy, PIECES['blk'])

    for ctouch_beyond in discl_attacked:
        field_touches_beyond(match, color, ctouch_beyond)

    for ctouch_beyond in discl_supported:
        field_touches_beyond(match, color, ctouch_beyond)

    match.writefield(gmove.srcx, gmove.srcy, piece)
    ###
    
    return discl_attacked, discl_supported


def running_pawn_in_endgame(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    if(is_endgame(match)):
        if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
            return pawn.is_running(match, gmove.srcx, gmove.srcy)

    return False


def controles_file(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    color = Match.color_of_piece(piece)

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
            priomove.tactics.append(TACTICS['defend-check'])
        
        if(castles(match, priomove.gmove)):
            priomove.tactics.append(TACTICS['castling'])

        if(promotes(match, priomove.gmove)):
            priomove.tactics.append(TACTICS['promotion'])

        if(captures(match, priomove.gmove)):
            if(piece_is_lower_equal_than_captured(match, priomove.gmove) or
               dstfield_is_attacked(match, priomove.gmove) == False or
               (dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove) and 
                piece_is_lower_fairy_equal_than_enemy_on_dstfield(match, priomove.gmove))):
                priomove.tactics.append(TACTICS['capture-good-deal'])
            else:
                priomove.tactics.append(TACTICS['capture-bad-deal'])

        if(defends_fork(match, priomove.gmove)):
            if(dstfield_is_attacked(match, priomove.gmove) == False or 
               (dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove) and 
                piece_is_lower_fairy_equal_than_enemy_on_dstfield(match, priomove.gmove))):
                priomove.tactics.append(TACTICS['defend-fork'])
                all_fork_defending.append(priomove)
            else:
                priomove.tactics.append(TACTICS['support-bad-deal'])

        if(flees(match, priomove.gmove)):
            if(dstfield_is_attacked(match, priomove.gmove) == False or
                (dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove) and 
                 piece_is_lower_equal_than_enemy_on_dstfield(match, priomove.gmove))):
                if(piece_is_lower_equal_than_enemy_on_srcfield(match, priomove.gmove) == False):
                    priomove.tactics.append(TACTICS['flee-urgent'])
                    all_fleeing.append(priomove)
                elif(srcfield_is_supported(match, priomove.gmove) == False):
                    priomove.tactics.append(TACTICS['flee'])

        attacked, supported = attacks_and_supports(match, priomove.gmove)

        if(len(attacked) > 0):
            if(is_piece_attacked(attacked, PIECES['wKg'], PIECES['bKg'])):
                if(dstfield_is_attacked(match, priomove.gmove) == False or 
                   (dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove) and 
                    piece_is_lower_fairy_equal_than_enemy_on_dstfield(match, priomove.gmove))):
                    priomove.tactics.append(TACTICS['attack-king-good-deal'])
                else:
                    priomove.tactics.append(TACTICS['attack-king-bad-deal'])
            else:
                if(dstfield_is_attacked(match, priomove.gmove) == False or 
                   (dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove) and 
                    piece_is_lower_fairy_equal_than_enemy_on_dstfield(match, priomove.gmove))):
                    if(is_attacked_pinned(match, attacked) or 
                       is_attacked_soft_pinned(match, attacked)):
                        priomove.tactics.append(TACTICS['attack-stormy'])
                        all_attacking.append(priomove)
                    elif(is_attacked_supported(attacked) == False or 
                         is_attacked_higher_than_piece(match, attacked)):
                        priomove.tactics.append(TACTICS['attack-good-deal'])
                        all_attacking.append(priomove)
                    else:
                        priomove.tactics.append(TACTICS['attack-bad-deal'])
                else:
                    priomove.tactics.append(TACTICS['attack-bad-deal'])

        if(len(supported) > 0):
            if(is_supported_attacked(supported)):
                if(dstfield_is_attacked(match, priomove.gmove) == False or 
                   (dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove) and 
                    piece_is_lower_fairy_equal_than_enemy_on_dstfield(match, priomove.gmove))):
                    if(is_supported_lower_equal_than_attacker(supported)):
                        priomove.tactics.append(TACTICS['support-good-deal'])
                        all_supporting.append(priomove)
                    else:
                        priomove.tactics.append(TACTICS['support-bad-deal'])
                else:
                    priomove.tactics.append(TACTICS['support-bad-deal'])
            else:
                if(dstfield_is_attacked(match, priomove.gmove) == False or 
                   dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove)):
                    priomove.tactics.append(TACTICS['support-unattacked'])
                else:
                    priomove.tactics.append(TACTICS['support-bad-deal'])

        discl_attacked, discl_supported = disclosures(match, priomove.gmove)
        if(len(discl_attacked) > 0):
            if(is_discl_attacked_supported(discl_attacked) == False):
                priomove.tactics.append(TACTICS['attack-good-deal'])
                all_discl_attacking.append(priomove)
            else:
                priomove.tactics.append(TACTICS['attack-bad-deal'])

        if(len(discl_supported) > 0):
            if(is_discl_supported_attacked_(discl_supported)):
                priomove.tactics.append(TACTICS['support-good-deal'])
                all_discl_supporting.append(priomove)
            else:
                priomove.tactics.append(TACTICS['support-bad-deal'])

        if(running_pawn_in_endgame(match, priomove.gmove)):
            priomove.tactics.append(TACTICS['running-pawn-in-endgame'])

        """if(controles_file(match, priomove.gmove)):
            if(dstfield_is_attacked(match, priomove.gmove) == False or 
               (dstfield_is_supported(match, priomove.gmove) and 
                piece_is_lower_fairy_equal_than_enemy_on_dstfield(match, priomove.gmove))):
                priomove.tactics.append(TACTICS['controles-file-good-deal'])"""

        if(len(priomove.tactics) > 0):
            priomove.tactics.sort()
            priomove.prio = TACTICS_TO_PRIO[priomove.fetch_tactics(0)]
            priomove.prio_sec = TACTICS_TO_PRIO[priomove.fetch_tactics(1)]
        else:
            priomove.tactics.append(TACTICS['undefined'])
            priomove.prio = PRIO['prio10']
            priomove.prio_sec = PRIO['prio10']

    all_attacking.sort(key = fetch_first_tactics)
    for pmove in all_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
             pmove.downgrade(TACTICS['attack-stormy'], TACTICS['attack-downgraded'])
             pmove.downgrade(TACTICS['attack-good-deal'], TACTICS['attack-downgraded'])
             pmove.tactics.sort()
             pmove.prio = TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
             pmove.prio_sec = TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    excludes.clear()
    all_discl_attacking.sort(key = fetch_first_tactics)
    for pmove in all_discl_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(TACTICS['discl-attack-good-deal'], TACTICS['attack-downgraded'])
            pmove.tactics.sort()
            pmove.prio = TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
            pmove.prio_sec = TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    excludes.clear()
    all_supporting.sort(key = fetch_first_tactics)
    for pmove in all_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(TACTICS['support-good-deal'], TACTICS['support-downgraded'])
            pmove.tactics.sort()
            pmove.prio = TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
            pmove.prio_sec = TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    excludes.clear()
    all_discl_supporting.sort(key = fetch_first_tactics)
    for pmove in all_discl_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(TACTICS['discl-support-good-deal'], TACTICS['support-downgraded'])
            pmove.tactics.sort()
            pmove.prio = TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
            pmove.prio_sec = TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    excludes.clear()
    all_fork_defending.sort(key = fetch_first_tactics)
    for pmove in all_fork_defending:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(TACTICS['defend-fork'], TACTICS['defend-fork-downgraded'])
            pmove.tactics.sort()
            pmove.prio = TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
            pmove.prio_sec = TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    excludes.clear()
    all_fleeing.sort(key = fetch_first_tactics)
    for pmove in all_fleeing:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.downgrade(TACTICS['flee-urgent'], TACTICS['flee-downgraded'])
            pmove.tactics.sort()
            pmove.prio = TACTICS_TO_PRIO[pmove.fetch_tactics(0)]
            pmove.prio_sec = TACTICS_TO_PRIO[pmove.fetch_tactics(1)]

    priomoves.sort(key=attrgetter('prio', 'prio_sec'))


