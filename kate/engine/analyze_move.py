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


def is_field_blocking_attacks_on_king(x1, y1, kg_x, kg_y, enemies):
    if(rook.rk_dir(kg_x, kg_y, x1, y1) != rules.DIRS['undefined']):
        enemy = "rook"
    elif(bishop.bp_dir(kg_x, kg_y, x1, y1) != rules.DIRS['undefined']):
        enemy = "bishop"
    else:
        return False

    for ctouch in enemies:
        if(ctouch.piece == PIECES['wQu'] or ctouch.piece == PIECES['bQu']):
            return True
        elif(enemy == "rook" and
             (ctouch.piece == PIECES['wRk'] or ctouch.piece == PIECES['bRk'])):
            return True
        elif(enemy == "bishop" and
             (ctouch.piece == PIECES['wBp'] or ctouch.piece == PIECES['bBp'])):
            return True

    return False

def defends_king_attack2(match, gmove):
    color = match.next_color()
    beforecnt = 0
    aftercnt = 0
    urgent = False

    if(color == COLORS['white']):
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
    else:
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y

    for i in range(8):
        x1, y1 = rules.search(match, Kg_x, Kg_y, king.STEPS[i][0], king.STEPS[i][1])
        if(x1 != rules.UNDEF_X):
            friends, enemies = field_touches(match, color, x1, y1)
            if(is_field_blocking_attacks_on_king(x1, y1, Kg_x, Kg_y, enemies)):
                if(len(friends) < len(enemies)):
                    beforecnt += 1

    do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

    if(Kg_x == gmove.srcx):
        Kg_x = gmove.dstx
        Kg_y = gmove.dsty

    for i in range(8):
        x1 = Kg_x + king.STEPS[i][0]
        y1 = Kg_y + king.STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
            if(rules.is_field_touched(match, REVERSED_COLORS[color], x1, y1, 0) == False):
                urgent = False

            x1, y1 = rules.search(match, Kg_x, Kg_y, king.STEPS[i][0], king.STEPS[i][1])
            if(x1 != rules.UNDEF_X):
                friends, enemies = field_touches(match, color, x1, y1)
                if(is_field_blocking_attacks_on_king(x1, y1, Kg_x, Kg_y, enemies)):
                    if(len(friends) < len(enemies)):
                        aftercnt += 1

    undo_move(match)

    if(beforecnt > aftercnt or urgent):
        return True, urgent
    else:
        return False, urgent


def defends_king_attack(match, gmove):
    color = match.next_color()
    before_cnt = 0
    after_cnt = 0
    urgent = True

    if(color == COLORS['white']):
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
    else:
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y

    for i in range(8):
        x1 = Kg_x + king.STEPS[i][0]
        y1 = Kg_y + king.STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
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
        x1 = Kg_x + king.STEPS[i][0]
        y1 = Kg_y + king.STEPS[i][1]
        if(rules.is_inbounds(x1, y1)):
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

    color = Match.color_of_piece(piece)

    do_move(match, gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)

    excluded_dir = rook.rk_dir(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)
    rook.disclosures(match, color, excluded_dir, gmove.srcx, gmove.srcy, discl_attacked, discl_supported)

    excluded_dir = bishop.bp_dir(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty)
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


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty): # , forked
    if(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        return queen.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        return rook.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        return bishop.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        return knight.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        return king.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return pawn.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    else:
        return False


def blocks(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    return False


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


def is_repetition(match, gmove):
    count = 0
    
    if(match.next_color() == COLORS['white']):
        last_even_srcx = gmove.srcx
        last_even_srcy = gmove.srcy
        last_odd_srcx = None
        last_odd_srcy = None
    else:
        last_even_srcx = None
        last_even_srcy = None
        last_odd_srcx = gmove.srcx
        last_odd_srcy = gmove.srcy

    for move in reversed(match.move_list):
        if(move.count % 2 == 1):
            if(last_even_srcx is None):
                last_even_srcx = move.srcx
                last_even_srcy = move.srcy
            elif(last_even_srcx == move.dstx and last_even_srcy == move.dsty):
                count += 1
                last_even_srcx = move.srcx
                last_even_srcy = move.srcy
            else:
                break
        else:
            if(last_odd_srcx is None):
                last_odd_srcx = move.srcx
                last_odd_srcy = move.srcy
            elif(last_odd_srcx == move.dstx and last_odd_srcy == move.dsty):
                count += 1
                last_odd_srcx = move.srcx
                last_odd_srcy = move.srcy
            else:
                break

    if(count > 7):
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
            priomove.tactics.append(TACTICS['defend-check'])

        defends_king, urgent = defends_king_attack(match, priomove.gmove)
        if(urgent):
            priomove.tactics.append(TACTICS['defend-king-attack-urgent'])
        elif(defends_king and 
             dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove)):
            priomove.tactics.append(TACTICS['defend-king-attack'])

        if(castles(match, priomove.gmove)):
            priomove.tactics.append(TACTICS['castling'])

        if(is_repetition(match, priomove.gmove)):
            priomove.tactics.append(TACTICS['position-repeat'])

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
                if(srcfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, priomove.gmove) or
                   piece_is_lower_equal_than_enemy_on_srcfield(match, priomove.gmove) == False):
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
            if(is_supported_weak(supported)): # is_supported_attacked(supported)
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
            if(is_discl_supported_weak(discl_supported)): # is_discl_supported_attacked(discl_supported)
                priomove.tactics.append(TACTICS['support-good-deal'])
                all_discl_supporting.append(priomove)
            else:
                priomove.tactics.append(TACTICS['support-bad-deal'])

        #if(blocks(match, priomove.gmove)):


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


