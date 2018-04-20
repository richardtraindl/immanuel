from operator import attrgetter
from .match import *
from .cvalues import *
from .matchmove import do_move, undo_move
#from .move import *
#from .calc import *
from . import rules
from .analyze_position import score_supports, score_attacks, score_opening, score_endgame, is_endgame
from .analyze_helper import *
from .pieces import pawn, knight, bishop, rook, king


def captures(match, move, analyses):
    piece = match.readfield(move.srcx, move.srcy)

    color = Match.color_of_piece(piece)

    dstpiece = match.readfield(move.dstx, move.dsty)

    if(dstpiece != PIECES['blk']):
        analyses.append(ANALYSES['MV_IS_CAPTURE'])
        if(dstpiece == PIECES['wPw'] or dstpiece == PIECES['bPw']):
            analyses.append('CAPTURED_IS_PW')
        elif(dstpiece == PIECES['wKn'] or dstpiece == PIECES['bKn']):
            analyses.append(ANALYSES['CAPTURED_IS_KN'])
        elif(dstpiece == PIECES['wBp'] or dstpiece == PIECES['bBp']):
            analyses.append(ANALYSES['CAPTURED_IS_BP'])
        elif(dstpiece == PIECES['wRk'] or dstpiece == PIECES['bRk']):
            analyses.append(ANALYSES['CAPTURED_IS_RK'])
        elif(dstpiece == PIECES['wQu'] or dstpiece == PIECES['bQu']):
            analyses.append(ANALYSES['CAPTURED_IS_QU'])

    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and move.srcx != move.dstx ):
        analyses.append(ANALYSES['MV_IS_CAPTURE'])
        analyses.append(ANALYSES['CAPTURED_IS_PW'])


def promotes(match, move, analyses):
    if(move.prom_piece != PIECES['blk']):
        analyses.append(ANALYSES['MV_IS_PROMOTION'])


def castles(match, move, analyses):
    piece = match.readfield(move.srcx, move.srcy)

    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(move.srcx - move.dstx == 2 or move.srcx - move.dstx == -2):
            analyses.append(ANALYSES['MV_IS_CASTLING'])


def attacks_and_supports(match, move, analyses):
    attacked = []
    supported = []

    piece = match.readfield(move.srcx, move.srcy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        pawn.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, analyses, attacked, supported)
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        knight.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, analyses, attacked, supported)
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        bishop.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, analyses, attacked, supported)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        rook.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, analyses, attacked, supported)    
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        rook.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, analyses, attacked, supported)
        bishop.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, analyses, attacked, supported)
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        king.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, analyses, attacked, supported)
        if(move.srcx - move.dstx == -2):
            rook.attacks_and_supports(match, move.dstx + 1, move.srcy, move.dstx - 1, move.dsty, analyses, attacked, supported)
        elif(move.srcx - move.dstx == 2):
            rook.attacks_and_supports(match, move.dstx - 2, move.srcy, move.dstx + 1, move.dsty, analyses, attacked, supported)

    return attacked, supported


def defends_check(match, move, analyses):
    piece = match.readfield(move.srcx, move.srcy)

    color = Match.color_of_piece(piece)

    # is king attaked
    if(color == COLORS['white']):
        kg_x = match.wKg_x
        kg_y = match.wKg_y
    else:
        kg_x = match.bKg_x
        kg_y = match.bKg_y

    if(rules.is_king_attacked(match, kg_x, kg_y)):
        analyses.append(ANALYSES['MV_DEFENDS_CHECK'])


def defends_fork(match, move, analyses):
    fork_defended = []

    piece = match.readfield(move.srcx, move.srcy)

    if(defends_fork_field(match, piece, move.srcx, move.srcy, move.dstx, move.dsty, fork_defended)):
        analyses.append(ANALYSES['MV_IS_FORK_DEFENSE'])

    return fork_defended


def disclosures(match, move, analyses):
    disclosed_attacked = []
    
    piece = match.readfield(move.srcx, move.srcy)

    color = Match.color_of_piece(piece)
    
    excluded_dir = rook.rk_dir(move.srcx, move.srcy, move.dstx, move.dsty)
    if(excluded_dir == rules.DIRS['undefined']):
        excluded_dir = bishop.bp_dir(move.srcx, move.srcy, move.dstx, move.dsty)

    do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

    if(rook.disclosures_field(match, color, excluded_dir, move.srcx, move.srcy, disclosed_attacked)):
        analyses.append(ANALYSES['MV_IS_DISCLOSURE'])

    if(bishop.disclosures_field(match, color, excluded_dir, move.srcx, move.srcy, disclosed_attacked)):
        analyses.append(ANALYSES['MV_IS_DISCLOSURE'])

    undo_move(match)

    ###
    match.writefield(move.srcx, move.srcy, PIECES['blk'])

    for ctouch_beyond in disclosed_attacked:
        field_touches_beyond(match, color, ctouch_beyond)

    match.writefield(move.srcx, move.srcy, piece)
    ###
    
    return disclosed_attacked


def flees(match, move, analyses):
    old_lower_cnt = 0
    old_higher_cnt = 0
    new_lower_cnt = 0
    new_higher_cnt = 0

    piece = match.readfield(move.srcx, move.srcy)

    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    enmycontacts = list_field_touches(match, opp_color, move.srcx, move.srcy)
    for enmy in enmycontacts:
        if(PIECES_RANK[enmy.piece] < PIECES_RANK[piece]):
            old_lower_cnt += 1
        else:
            old_higher_cnt += 1
    enmycontacts.clear()

    ###
    do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

    enmycontacts = list_field_touches(match, opp_color, move.dstx, move.dsty)
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
        analyses.append(ANALYSES['MV_IS_FLEE'])


def progress(match, move, analyses):
    piece = match.readfield(move.srcx, move.srcy)

    if(is_endgame(match)):
        if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
            analyses.append(ANALYSES['MV_IS_RUNNING_PAWN'])
        elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
            analyses.append(ANALYSES['MV_IS_PROGRESS'])

    """color = Match.color_of_piece(piece)

    value = match.score

    value += score_attacks(match, color)

    value += score_supports(match, REVERSED_COLORS[color])

    if((value >= (SCORES[PIECES['bPw']] // 10) and color == COLORS['white']) or 
       (value <= (SCORES[PIECES['wPw']] // 10) and color == COLORS['black'])):
        return token | MV_IS_PROGRESS
    else:
        return token"""


def controles_file(match, move, analyses):
    piece = match.readfield(move.srcx, move.srcy)
    color = Match.color_of_piece(piece)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        return
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        if(bishop.controles_file(match, piece, color, move.srcx, move.srcy, move.dstx, move.dsty)):
            analyses.append(ANALYSES['MV_CONTROLES_FILE'])
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        if(rook.controles_file(match, piece, color, move.srcx, move.srcy, move.dstx, move.dsty)):
            analyses.append(ANALYSES['MV_CONTROLES_FILE'])
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        if(rook.controles_file(match, piece, color, move.srcx, move.srcy, move.dstx, move.dsty)):
            analyses.append(ANALYSES['MV_CONTROLES_FILE'])
        if(bishop.controles_file(match, piece, color, move.srcx, move.srcy, move.dstx, move.dsty)):
            analyses.append(ANALYSES['MV_CONTROLES_FILE'])


def analyze_move(match, move):
    analyses = []

    piece = match.readfield(move.srcx, move.srcy)
    
    color = Match.color_of_piece(piece)

    ###
    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        analyses.append(ANALYSES['MV_PIECE_IS_PW'])
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        analyses.append(ANALYSES['MV_PIECE_IS_KN'])
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        analyses.append(ANALYSES['MV_PIECE_IS_BP'])
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        analyses.append(ANALYSES['MV_PIECE_IS_RK'])
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        analyses.append(ANALYSES['MV_PIECE_IS_QU'])
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        analyses.append(ANALYSES['MV_PIECE_IS_KG'])
    ###

    ###
    match.writefield(move.srcx, move.srcy, PIECES['blk'])

    src_supported, src_attacked = field_touches(match, color, move.srcx, move.srcy)

    analyse_piece_fields(src_supported, src_attacked, "SRCFIELDTOUCHES", analyses)

    dst_supported, dst_attacked = field_touches(match, color, move.dstx, move.dsty)

    analyse_piece_fields(dst_supported, dst_attacked, "DSTFIELDTOUCHES", analyses)

    match.writefield(move.srcx, move.srcy, piece)
    ###

    captures(match, move, analyses)

    promotes(match, move, analyses)

    castles(match, move, analyses)

    attacked, supported = attacks_and_supports(match, move, analyses)
    
    defends_check(match, move, analyses)

    fork_defended = defends_fork(match, move, analyses)
    
    disclosed_attacked = disclosures(match, move, analyses)

    flees(match, move, analyses)

    progress(match, move, analyses)
    
    controles_file(match, move, analyses)

    return analyses, attacked, supported, disclosed_attacked, fork_defended


def downgrade(priomove, old_tactic, new_tactic):
    priomove.prio = TACTICS_TO_PRIO[new_tactic]
    for idx in range(len(priomove.tactics)):
        if(priomove.tactics[idx] == old_tactic):
            priomove.tactics[idx] = new_tactic
            return

def len_tactics(priomove):
    return len(priomove.tactics)

def fetch_tactics(priomove, idx):
    if(len(priomove.tactics) > idx):
        return priomove.tactics[idx]
    else:
        return TACTICS['undefined']

def fetch_first_tactics(priomove):
    return  fetch_tactics(priomove, 0)

def eval_tactics(match, priomoves):
    all_analyses = []
    excludes = []

    for priomove in priomoves:
        if(token & MV_IS_CASTLING > 0):
            priomove.tactics.append(TACTICS['castling'])

        if(token & MV_IS_PROMOTION > 0):
            priomove.tactics.append(TACTICS['promotion'])

        if(token & MV_IS_CAPTURE > 0):
            if(piece_is_lower_equal_than_captured(priomove) or
               dstfield_is_attacked(priomove) == False or
               (dstfield_is_supported(priomove) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(priomove))):
                priomove.tactics.append(TACTICS['capture-good-deal'])
            else:
                priomove.tactics.append(TACTICS['capture-bad-deal'])

        if(token & MV_IS_FORK_DEFENSE > 0):
            if(dstfield_is_attacked(token) == False or 
               (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                priomove.tactics.append(TACTICS['defend-fork'])
                all_fork_defending.append(priomove)
            else:
                priomove.tactics.append(TACTICS['support-bad-deal'])

        if(token & MV_IS_FLEE > 0):
            if(dstfield_is_attacked(token) == False or
                (dstfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_dstfield(token))):
                if(piece_is_lower_equal_than_enemy_on_srcfield(token) == False):
                    priomove.tactics.append(TACTICS['flee-urgent'])
                    all_fleeing.append(priomove)
                elif(srcfield_is_supported(token) == False):
                    priomove.tactics.append(TACTICS['flee'])

        if(token & MV_IS_ATTACK > 0):
            if(token & ATTACKED_IS_KG > 0):
                if(dstfield_is_attacked(token) == False or 
                   (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                    priomove.tactics.append(TACTICS['attack-king-good-deal'])
                else:
                    priomove.tactics.append(TACTICS['attack-king-bad-deal'])
            else:
                if(dstfield_is_attacked(token) == False or 
                   (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                    if(token & ATTACK_IS_PIN > 0 or token & ATTACK_IS_SOFT_PIN > 0 or 
                       is_attacked_pinned(match, attacked) or is_attacked_soft_pinned(match, attacked)):
                        priomove.tactics.append(TACTICS['attack-stormy'])
                        all_attacking.append(priomove)
                    elif(is_attacked_supported(attacked) == False or is_attacked_higher_than_piece(match, attacked)):
                        priomove.tactics.append(TACTICS['attack-good-deal'])
                        all_attacking.append(priomove)
                    else:
                        priomove.tactics.append(TACTICS['attack-bad-deal'])
                else:
                    priomove.tactics.append(TACTICS['attack-bad-deal'])

        if(token & MV_IS_SUPPORT > 0):
            if(is_supported_attacked(supported)):
                if(dstfield_is_attacked(token) == False or 
                   (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                    if(is_supported_lower_equal_than_attacker(supported)):
                        priomove.tactics.append(TACTICS['support-good-deal'])
                        all_supporting.append(priomove)
                    else:
                        priomove.tactics.append(TACTICS['support-bad-deal'])
                else:
                    priomove.tactics.append(TACTICS['support-bad-deal'])

        if(token & MV_IS_SUPPORT_UNATTACKED > 0):
            priomove.tactics.append(TACTICS['support-unattacked'])

        if(token & MV_IS_DISCLOSURE > 0):
            if(is_disclosed_attacked_supported(disclosed_attacked) == False):
                priomove.tactics.append(TACTICS['attack-good-deal'])
                all_disclosed_attacking.append(priomove)
            else:
                priomove.tactics.append(TACTICS['attack-bad-deal'])


        if(token & MV_IS_PROGRESS > 0): #and is_endgame(match)
            priomove.tactics.append(TACTICS['progress'])

        if(token & MV_IS_RUNNING_PAWN > 0):
            priomove.tactics.append(TACTICS['running-pawn-in-endgame'])

        """if(token & MV_CONTROLES_FILE > 0):
            if(dstfield_is_attacked(token) == False or 
               (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
               priomove.tactics.append(TACTICS['controles-file-good-deal'])"""

        if(len(priomove.tactics) > 0):
            priomove.tactics.sort()
            priomove.prio = TACTICS_TO_PRIO[fetch_tactics(priomove, 0)]
            priomove.prio_sec = TACTICS_TO_PRIO[fetch_tactics(priomove, 1)]
        else:
            priomove.tactics.append(TACTICS['undefined'])
            priomove.prio = PRIO['prio10']
            priomove.prio_sec = PRIO['prio10']

    all_attacking.sort(key = fetch_first_tactics)
    for pmove in all_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
             downgrade(pmove, TACTICS['attack-stormy'], TACTICS['attack-downgraded'])
             downgrade(pmove, TACTICS['attack-good-deal'], TACTICS['attack-downgraded'])
             priomove.tactics.sort()
             priomove.prio = TACTICS_TO_PRIO[fetch_tactics(priomove, 0)]
             priomove.prio_sec = TACTICS_TO_PRIO[fetch_tactics(priomove, 1)]

    excludes.clear()
    all_disclosed_attacking.sort(key = fetch_first_tactics)
    for pmove in all_disclosed_attacking:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            downgrade(pmove, TACTICS['disclosed-attack-good-deal'], TACTICS['attack-downgraded'])
            priomove.tactics.sort()
            priomove.prio = TACTICS_TO_PRIO[fetch_tactics(priomove, 0)]
            priomove.prio_sec = TACTICS_TO_PRIO[fetch_tactics(priomove, 1)]

    excludes.clear()
    all_supporting.sort(key = fetch_first_tactics)
    for pmove in all_supporting:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            downgrade(pmove, TACTICS['support-good-deal'], TACTICS['support-downgraded'])
            priomove.tactics.sort()
            priomove.prio = TACTICS_TO_PRIO[fetch_tactics(priomove, 0)]
            priomove.prio_sec = TACTICS_TO_PRIO[fetch_tactics(priomove, 1)]

    excludes.clear()
    all_fork_defending.sort(key = fetch_first_tactics)
    for pmove in all_fork_defending:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            downgrade(pmove, TACTICS['defend-fork'], TACTICS['defend-fork-downgraded'])
            priomove.tactics.sort()
            priomove.prio = TACTICS_TO_PRIO[fetch_tactics(priomove, 0)]
            priomove.prio_sec = TACTICS_TO_PRIO[fetch_tactics(priomove, 1)]

    excludes.clear()
    all_fleeing.sort(key = fetch_first_tactics)
    for pmove in all_fleeing:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            downgrade(pmove, TACTICS['flee-urgent'], TACTICS['flee-downgraded'])
            priomove.tactics.sort()
            priomove.prio = TACTICS_TO_PRIO[fetch_tactics(priomove, 0)]
            priomove.prio_sec = TACTICS_TO_PRIO[fetch_tactics(priomove, 1)]

    for priomove in priomoves:
        if(fetch_tactics(priomove, 0) >= TACTICS['support-good-deal'] and 
           fetch_tactics(priomove, 0) <= TACTICS['support-unattacked']):
            priomove.tactics.append(TACTICS['single-silent-move'])
            priomove.tactics.sort()
            priomove.prio = TACTICS_TO_PRIO[fetch_tactics(priomove, 0)]
            priomove.prio_sec = TACTICS_TO_PRIO[fetch_tactics(priomove, 1)]
            break

