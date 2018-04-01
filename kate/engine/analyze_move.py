from operator import attrgetter
from .match import *
from .cvalues import *
from .matchmove import do_move, undo_move
#from .move import *
#from .calc import *
from . import rules
from .analyze_position import score_supports, score_attacks, score_opening, score_endgame
from .analyze_helper import *
from .pieces import pawn, knight, bishop, rook, king
from .pieces.generic_piece import contacts_to_token


TOKENS = {
    'token' : 0,
    'attacked' : 1,
    'supported' : 2,
    'disclosed_attacked' : 3,
    'forked' : 4 }


def captures(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    color = Match.color_of_piece(piece)

    dstpiece = match.readfield(move.dstx, move.dsty)

    if(dstpiece != PIECES['blk']):
        if(dstpiece == PIECES['wPw'] or dstpiece == PIECES['bPw']):
            token = token | MV_IS_CAPTURE | CAPTURED_IS_PW
        elif(dstpiece == PIECES['wKn'] or dstpiece == PIECES['bKn']):
            token = token | MV_IS_CAPTURE | CAPTURED_IS_KN
        elif(dstpiece == PIECES['wBp'] or dstpiece == PIECES['bBp']):
            token = token | MV_IS_CAPTURE | CAPTURED_IS_BP
        elif(dstpiece == PIECES['wRk'] or dstpiece == PIECES['bRk']):
            token = token | MV_IS_CAPTURE | CAPTURED_IS_RK
        elif(dstpiece == PIECES['wQu'] or dstpiece == PIECES['bQu']):
            token = token | MV_IS_CAPTURE | CAPTURED_IS_QU

    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and move.srcx != move.dstx ):
        token = token | MV_IS_CAPTURE | CAPTURED_IS_PW

    return token


def promotes(match, move):
    token = 0x0

    if(move.prom_piece == PIECES['blk']):
        return token
    else:
        return token | MV_IS_PROMOTION


def castles(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(move.srcx - move.dstx == 2 or move.srcx - move.dstx == -2):
            return token | MV_IS_CASTLING

    return token


def attacks_and_supports(match, move, attacked, supported):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        token = token | pawn.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        token = token | knight.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        token = token | bishop.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        token = token | rook.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)    
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        token = token | rook.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)
        token = token | bishop.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        token = token | king.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)
        if(move.srcx - move.dstx == -2):
            token = token | rook.attacks_and_supports(match, move.dstx + 1, move.srcy, move.dstx - 1, move.dsty, attacked, supported)
        elif(move.srcx - move.dstx == 2):
            token = token | rook.attacks_and_supports(match, move.dstx - 2, move.srcy, move.dstx + 1, move.dsty, attacked, supported)
    else:
        return token

    return token


def defends_check(match, move):
    token = 0x0

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
        token = token | MV_DEFENDS_CHECK

    return token


def defends_fork(match, move, forked):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    if(defends_fork_field(match, piece, move.srcx, move.srcy, move.dstx, move.dsty, forked)):
        token = token | MV_IS_FORK_DEFENSE

    return token


def disclosures(match, move, disclosed_attacked):
    token = 0x0
    
    piece = match.readfield(move.srcx, move.srcy)

    color = Match.color_of_piece(piece)
    
    excluded_dir = rook.rk_dir(move.srcx, move.srcy, move.dstx, move.dsty)
    if(excluded_dir == rules.DIRS['undefined']):
        excluded_dir = bishop.bp_dir(move.srcx, move.srcy, move.dstx, move.dsty)

    do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

    if(rook.disclosures_field(match, color, excluded_dir, move.srcx, move.srcy, disclosed_attacked)):
        token = token | MV_IS_DISCLOSURE

    if(bishop.disclosures_field(match, color, excluded_dir, move.srcx, move.srcy, disclosed_attacked)):
        token = token | MV_IS_DISCLOSURE

    undo_move(match)

    ###
    match.writefield(move.srcx, move.srcy, PIECES['blk'])

    for ctouch in disclosed_attacked:
        field_touches_beyond(match, color, ctouch)

    match.writefield(move.srcx, move.srcy, piece)
    ###

    return token


def flees(match, move):
    token = 0x0
    old_lower_cnt = 0
    old_higher_cnt = 0
    new_lower_cnt = 0
    new_higher_cnt = 0

    piece = match.readfield(move.srcx, move.srcy)

    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    enmycontacts = list_field_touches(match, opp_color, move.srcx, move.srcy)
    for enmy in enmycontacts:
        if(PIECES_RANK[enmy[0]] < PIECES_RANK[piece]):
            old_lower_cnt += 1
        else:
            old_higher_cnt += 1
    enmycontacts.clear()

    ###
    do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

    enmycontacts = list_field_touches(match, opp_color, move.dstx, move.dsty)
    for enmy in enmycontacts:
        if(PIECES_RANK[enmy[0]] < PIECES_RANK[piece]):
            new_lower_cnt += 1
        else:
            new_higher_cnt += 1

    undo_move(match)
    ###

    if((old_lower_cnt + old_higher_cnt) > 0 and 
       (new_lower_cnt < old_lower_cnt or 
        new_lower_cnt + new_higher_cnt < old_lower_cnt + old_higher_cnt)):
        token = token | MV_IS_FLEE

    return token


def progress(match, move):
    token = 0x0
    piece = match.readfield(move.srcx, move.srcy)
    color = Match.color_of_piece(piece)

    value = match.score

    value += score_attacks(match, color)

    value += score_supports(match, REVERSED_COLORS[color])

    if((value >= (SCORES[PIECES['bPw']] / 10) and color == COLORS['white']) or 
       (value <= (SCORES[PIECES['wPw']] / 10) and color == COLORS['black'])):
        return token | MV_IS_PROGRESS
    else:
        return token


def controles_file(match, move):
    token = 0x0
    piece = match.readfield(move.srcx, move.srcy)
    color = Match.color_of_piece(piece)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return token
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        return token
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        if(bishop.controles_file(match, piece, color, move.srcx, move.srcy, move.dstx, move.dsty)):
            return token | MV_CONTROLES_FILE        
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        if(rook.controles_file(match, piece, color, move.srcx, move.srcy, move.dstx, move.dsty)):
            return token | MV_CONTROLES_FILE
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        if(rook.controles_file(match, piece, color, move.srcx, move.srcy, move.dstx, move.dsty)):
            return token | MV_CONTROLES_FILE
        if(bishop.controles_file(match, piece, color, move.srcx, move.srcy, move.dstx, move.dsty)):
            return token | MV_CONTROLES_FILE
    else:
        return token
    
    return token


def analyze_move(match, move):
    tokens = [0] * len(TOKENS)
    token = 0x0
    attacked = []
    supported = []
    disclosed_attacked = []
    forked = []

    piece = match.readfield(move.srcx, move.srcy)
    
    color = Match.color_of_piece(piece)

    ###
    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        token = token | MV_PIECE_IS_PW
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        token = token | MV_PIECE_IS_KN
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        token = token | MV_PIECE_IS_BP
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        token = token | MV_PIECE_IS_RK
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        token = token | MV_PIECE_IS_QU
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        token = token | MV_PIECE_IS_KG
    ###

    ###
    match.writefield(move.srcx, move.srcy, PIECES['blk'])

    frdlycontacts, enmycontacts = field_touches(match, color, move.srcx, move.srcy)

    token = token | contacts_to_token(frdlycontacts, enmycontacts, "SRCFIELDTOUCHES")
    frdlycontacts.clear()
    enmycontacts.clear()

    frdlycontacts, enmycontacts = field_touches(match, color, move.dstx, move.dsty)

    match.writefield(move.srcx, move.srcy, piece)

    token = token | contacts_to_token(frdlycontacts, enmycontacts, "DSTFIELDTOUCHES")
    frdlycontacts.clear()
    enmycontacts.clear()
    ###

    token = token | captures(match, move)

    token = token | promotes(match, move)

    token = token | castles(match, move)

    token = token | attacks_and_supports(match, move, attacked, supported)
    
    token = token | defends_check(match, move)

    token = token | defends_fork(match, move, forked)
    
    token = token | disclosures(match, move, disclosed_attacked)

    token = token | flees(match, move)

    # token = token | progress(match, move)
    
    token = token | controles_file(match, move)

    tokens[TOKENS['token']] = token
    tokens[TOKENS['attacked']] = attacked
    tokens[TOKENS['supported']] = supported
    tokens[TOKENS['disclosed_attacked']] = disclosed_attacked
    tokens[TOKENS['forked']] = forked
    return tokens


def rank_moves(match, priomoves):
    all_attacked = []
    all_supported = []
    all_forked = []
    
    list_attacked = []
    list_supported = []
    list_forked = []
    list_flee = []

    excludes = []

    for priomove in priomoves:
        token = priomove.tokens[TOKENS['token']]
        attacked = priomove.tokens[TOKENS['attacked']]
        supported = priomove.tokens[TOKENS['supported']]
        disclosed_attacked = priomove.tokens[TOKENS['disclosed_attacked']]
        forked = priomove.tokens[TOKENS['forked']]

        all_attacked.extend(attacked)
        all_supported.extend(supported)
        all_forked.extend(forked)

        
        if(token & MV_IS_CASTLING > 0):
            priomove.prio = min(PRIO['castling'], priomove.prio)


        if(token & MV_IS_PROMOTION > 0):
            priomove.prio = min(PRIO['promotion'], priomove.prio)
            continue


        if(token & MV_IS_CAPTURE > 0):
            if(piece_is_lower_equal_than_captured(token) or
               dstfield_is_attacked(token) == False or
               (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                priomove.prio = min(priomove.prio, PRIO['capture-good-deal'])
                continue
            else:
                priomove.prio = min(priomove.prio, PRIO['capture-bad-deal'])


        if(token & MV_IS_FORK_DEFENSE > 0):
            if(dstfield_is_attacked(token) == False or 
               (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                priomove.prio = min(priomove.prio, PRIO['defend-fork'])
                list_forked.append(priomove)
            else:
                priomove.prio = min(priomove.prio, PRIO['support-bad-deal'])


        if(token & MV_IS_FLEE > 0):
            if(dstfield_is_attacked(token) == False or
                (dstfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_dstfield(token))):
                if(piece_is_lower_equal_than_enemy_on_srcfield(token) == False):
                    priomove.prio = min(priomove.prio, PRIO['flee-urgent'])
                    list_flee.append(priomove)
                elif(srcfield_is_supported(token) == False):
                    priomove.prio = min(priomove.prio, PRIO['flee'])
                    list_flee.append(priomove)
            #else: # srcfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_srcfield(token)
                #priomove.prio = min(priomove.prio, PRIO['prio4'])


        if(token & MV_IS_ATTACK > 0):
            if(token & ATTACKED_IS_KG > 0):
                if(dstfield_is_attacked(token) == False or 
                   (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                    priomove.prio = min(priomove.prio, PRIO['attack-king-good-deal'])
                    continue
                else:
                    priomove.prio = min(priomove.prio, PRIO['attack-king-bad-deal'])
            else:
                if(dstfield_is_attacked(token) == False or 
                   (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                    if(is_attacked_supported(attacked) == False or 
                       is_attacked_higher_than_piece(match, attacked) or 
                       is_attacked_pinned(match, attacked)):
                        priomove.prio = min(priomove.prio, PRIO['attack-good-deal'])
                        list_attacked.append(priomove)
                    else:
                        priomove.prio = min(priomove.prio, PRIO['attack-bad-deal'])
                else:
                    priomove.prio = min(priomove.prio, PRIO['attack-bad-deal'])


        if(token & MV_IS_SUPPORT > 0):
            if(is_supported_attacked(supported)):
                if(dstfield_is_attacked(token) == False or 
                   (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                    if(is_supported_lower_equal_than_attacker(supported)):
                        priomove.prio = min(priomove.prio, PRIO['support-good-deal'])
                        list_supported.append(priomove)
                    else:
                        priomove.prio = min(priomove.prio, PRIO['support-bad-deal'])
                else:
                    priomove.prio = min(priomove.prio, PRIO['support-bad-deal'])
            else:
                priomove.prio = min(priomove.prio, PRIO['support-unattacked'])


        if(token & MV_IS_DISCLOSURE > 0):
            if(is_disclosed_attacked_supported(disclosed_attacked) == False):
                priomove.prio = min(priomove.prio, PRIO['disclosed-attack'])
                list_attacked.append(priomove)
            else:
                priomove.prio = min(priomove.prio, PRIO['attack-bad-deal'])


        #if(token & MV_IS_PROGRESS > 0):
        #    priomove.prio = min(PRIO['prio3a'], priomove.prio)


        if(token & MV_CONTROLES_FILE > 0):
            priomove.prio = min(priomove.prio, PRIO['good'])


    list_attacked.sort(key=attrgetter('prio'))
    for pmove in list_attacked:
        for attack in all_attacked:
            if(pmove.gmove.srcx == attack.agent_srcx and pmove.gmove.srcy == attack.agent_srcy and 
               pmove.gmove.dstx == attack.agent_dstx and pmove.gmove.dsty == attack.agent_dsty):
                if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy and  
                       e[2] == attack.fieldx and e[3] == attack.fieldy for e in excludes) == False):
                    excludes.append([attack.agent_srcx, attack.agent_srcy, attack.fieldx, attack.fieldy])
                else:
                    pmove.prio = PRIO['good-postponed'] # min(pmove.prio, )

    excludes.clear()
    list_supported.sort(key=attrgetter('prio'))
    for pmove in list_supported:
        for support in all_supported:
            if(pmove.gmove.srcx == support.agent_srcx and pmove.gmove.srcy == support.agent_srcy and 
               pmove.gmove.dstx == support.agent_dstx and pmove.gmove.dsty == support.agent_dsty):
                if(any(e[0] == support.agent_srcx and e[1] == support.agent_srcy and  
                       e[2] == support.fieldx and e[3] == support.fieldy for e in excludes) == False):
                    excludes.append([support.agent_srcx, support.agent_srcy, support.fieldx, support.fieldy])
                else:
                    pmove.prio = PRIO['good-postponed'] # min(pmove.prio, 

    excludes.clear()
    list_forked.sort(key=attrgetter('prio'))
    for pmove in list_forked:
        for fork in all_forked:
            if(pmove.gmove.srcx == fork.agent_srcx and pmove.gmove.srcy == fork.agent_srcy and 
               pmove.gmove.dstx == fork.agent_dstx and pmove.gmove.dsty == fork.agent_dsty):
                if(any(e[0] == fork.agent_srcx and e[1] == fork.agent_srcy and
                       e[2] == fork.forkx and e[3] == fork.forky for e in excludes) == False):
                    excludes.append([fork.agent_srcx, fork.agent_srcy, fork.forkx, fork.forky])
                else:
                    pmove.prio = PRIO['good-postponed'] # min(pmove.prio, 

    excludes.clear()
    list_flee.sort(key=attrgetter('prio'))
    for pmove in list_flee:
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])
        else:
            pmove.prio = PRIO['good-postponed'] # min(pmove.prio, 

    priomoves.sort(key=attrgetter('prio'))

    for priomove in reversed(priomoves):
        if(priomove.prio > PRIO['single-silent-move'] and priomove.prio <= PRIO['good-postponed']):
            priomove.prio = PRIO['single-silent-move']
            break

