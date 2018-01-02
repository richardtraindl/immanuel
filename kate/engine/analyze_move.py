from random import randint
from .match import *
from .matchmove import do_move, undo_move
from .move import *
from .pieces import pawn, knight, bishop, rook, king
from .pieces.generic_piece import contacts_to_token
from .calc import *
from .analyze_helper import *
from .cvalues import *
from . import rules
from .analyze_position import score_contacts, score_opening, score_endgame


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


def defends_fork(match, move, forked):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    if(rules.defends_fork_field(match, piece, move.srcx, move.srcy, move.dstx, move.dsty, forked)):
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
        rules.field_touches_beyond(match, color, ctouch)

    match.writefield(move.srcx, move.srcy, piece)
    ###

    return token


def flees(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    enmycontacts = rules.list_field_touches(match, opp_color, move.srcx, move.srcy)
    old_cnt = len(enmycontacts)
    enmycontacts.clear()

    ###
    do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

    enmycontacts = rules.list_field_touches(match, opp_color, move.dstx, move.dsty)
    new_cnt = len(enmycontacts)

    undo_move(match)
    ###

    if(new_cnt < old_cnt):
        token = token | MV_IS_FLEE

    return token


def progress(match, move):
    token = 0x0
    piece = match.readfield(move.srcx, move.srcy)
    color = Match.color_of_piece(piece)

    value = match.score

    value += score_contacts(match, COLORS['white'])

    value += score_contacts(match, COLORS['black'])

    if((value >= (SCORES[PIECES['bPw']] / 2) and color == COLORS['white']) or 
       (value <= (SCORES[PIECES['wPw']] / 2) and color == COLORS['black'])):
        return token | MV_IS_PROGRESS
    else:
        return token

    ###
    """oldvalue = match.score

    oldvalue += score_contacts(match, COLORS['white'])

    oldvalue += score_contacts(match, COLORS['black'])

    if(match.count < 30):
        oldvalue += score_opening(match)

    if(match.count >= 30):
        oldvalue += score_endgame(match)
    ###

    do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

    newvalue = match.score

    newvalue += score_contacts(match, COLORS['white'])

    newvalue += score_contacts(match, COLORS['black'])

    if(match.count < 30):
        newvalue += score_opening(match)

    if(match.count >= 30):
        newvalue += score_endgame(match)

    undo_move(match)
    ###

    if((newvalue - oldvalue >= (SCORES[PIECES['bPw']] / 2) and color == COLORS['white']) or 
       (newvalue - oldvalue <= (SCORES[PIECES['wPw']] / 2) and color == COLORS['black'])):
        return token | MV_IS_PROGRESS
    else:
        return token"""


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

    frdlycontacts, enmycontacts = rules.field_touches(match, color, move.srcx, move.srcy)

    token = token | contacts_to_token(frdlycontacts, enmycontacts, "SRCFIELDTOUCHES")
    frdlycontacts.clear()
    enmycontacts.clear()

    frdlycontacts, enmycontacts = rules.field_touches(match, color, move.dstx, move.dsty)

    match.writefield(move.srcx, move.srcy, piece)

    token = token | contacts_to_token(frdlycontacts, enmycontacts, "DSTFIELDTOUCHES")
    frdlycontacts.clear()
    enmycontacts.clear()
    ###

    token = token | captures(match, move)

    token = token | promotes(match, move)

    token = token | castles(match, move)

    token = token | attacks_and_supports(match, move, attacked, supported)

    token = token | defends_fork(match, move, forked)
    
    token = token | disclosures(match, move, disclosed_attacked)

    token = token | flees(match, move)

    # token = token | progress(match, move)

    tokens[TOKENS['token']] = token
    tokens[TOKENS['attacked']] = attacked
    tokens[TOKENS['supported']] = supported
    tokens[TOKENS['disclosed_attacked']] = disclosed_attacked
    tokens[TOKENS['forked']] = forked
    return tokens


def rank_moves(priomoves):
    all_attacked = []
    all_supported = []
    all_forked = []
    
    list_attacked = []
    list_supported = []
    list_forked = []
    list_flee = []

    for priomove in priomoves:
        token = priomove.tokens[TOKENS['token']]
        attacked = priomove.tokens[TOKENS['attacked']]
        supported = priomove.tokens[TOKENS['supported']]
        disclosed_attacked = priomove.tokens[TOKENS['disclosed_attacked']]
        forked = priomove.tokens[TOKENS['forked']]

        all_attacked.extend(attacked)
        all_supported.extend(supported)
        all_forked.extend(forked)
        
        excludes = []

        if(token & MV_IS_CASTLING > 0):
            priomove.prio = min(PRIO['prio2a'], priomove.prio)

        if(token & MV_IS_PROMOTION > 0):
            priomove.prio = min(PRIO['prio1a'], priomove.prio)

        if(token & MV_IS_CAPTURE > 0):
            if(piece_is_lower_equal_than_captured(token) or
               dstfield_is_attacked(token) == False or
               (dstfield_is_supported(token) and 
                piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                tmpprio = PRIO['prio1a']
            else:
                tmpprio = PRIO['prio1c']
            
            if(token & MV_PIECE_IS_QU > 0):
                tmpprio += 1

            priomove.prio = min(tmpprio, priomove.prio)

        if(token & MV_IS_ATTACK > 0):
            if(token & ATTACKED_IS_KG > 0):
                if(dstfield_is_attacked(token) == False or 
                   (dstfield_is_supported(token) and 
                    piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                    tmpprio = PRIO['prio1a']
                else:
                    tmpprio = PRIO['prio1c']
            else:
                if(dstfield_is_attacked(token) == False or 
                   (dstfield_is_supported(token) and 
                    piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                    tmpprio = PRIO['prio2a']
                else:
                    tmpprio = PRIO['prio4a']

                if(is_attacked_supported(attacked)):
                    tmpprio += PRIO_HALF_STEP

            if(token & MV_PIECE_IS_QU > 0):
                tmpprio += 1

            list_attacked.append([priomove, min(tmpprio, PRIO['last'])])

        if(token & MV_IS_SUPPORT > 0):
            if(dstfield_is_attacked(token) == False or 
               (dstfield_is_supported(token) and 
                piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                tmpprio = PRIO['prio2a']
            else:
                tmpprio = PRIO['prio4a']

            if(is_supported_attacked(supported) == False):
                tmpprio += PRIO_HALF_STEP

            if(is_supported_lower_equal_than_attacker(supported) == False):
                tmpprio += PRIO_HALF_STEP

            if(token & MV_PIECE_IS_QU > 0):
                tmpprio += 1

            list_supported.append([priomove, min(tmpprio, PRIO['last'])])

        if(token & MV_IS_FORK_DEFENSE > 0):
            if(dstfield_is_attacked(token) == False or 
               (dstfield_is_supported(token) and 
                piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                list_forked.append([priomove, PRIO['prio2a']])
            else:
                list_forked.append([priomove, PRIO['prio3a']])

        if(token & MV_IS_DISCLOSURE > 0):
            if(is_disclosed_attacked_supported(disclosed_attacked) == False):
                priomove.prio = min(PRIO['prio2a'], priomove.prio)
            else:
                priomove.prio = min(PRIO['prio2c'], priomove.prio)

        #if(token & MV_IS_PROGRESS > 0):
        #    priomove.prio = min(PRIO['prio3a'], priomove.prio)

        if(token & MV_IS_FLEE > 0):
            if(dstfield_is_attacked(token) == False or
               (dstfield_is_supported(token) and 
                piece_is_lower_fairy_equal_than_enemy_on_dstfield(token))):
                tmpprio = PRIO['prio2a']
            else:
                tmpprio = PRIO['prio4a']

            if(srcfield_is_supported(token) and 
               piece_is_lower_equal_than_enemy_on_srcfield(token)):
                tmpprio += PRIO_STEP

            if(token & MV_PIECE_IS_QU > 0):
                tmpprio += 1

            list_flee.append([priomove, min(tmpprio, PRIO['last'])])

        #if(dstfield_is_attacked(token) == False or dstfield_is_supported(token)):
        #    priomove.prio = min(PRIO['prio3a'], priomove.prio)

    excludes.clear()
    list_attacked.sort(key=itemgetter(1))
    for attackeditem in list_attacked:
        pmove = attackeditem[0]
        for attack in all_attacked:
            if(pmove.gmove.srcx == attack.agent_srcx and pmove.gmove.srcy == attack.agent_srcy and 
               pmove.gmove.dstx == attack.agent_dstx and pmove.gmove.dsty == attack.agent_dsty):
                if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy and  
                       e[2] == attack.fieldx and e[3] == attack.fieldy for e in excludes) == False):
                    if(pmove.prio > attackeditem[1]):
                        pmove.prio = attackeditem[1]
                        excludes.append([pmove.gmove.srcx, pmove.gmove.srcy, attack.fieldx, attack.fieldy])

    excludes.clear()
    list_supported.sort(key=itemgetter(1))
    for supporteditem in list_supported:
        pmove = supporteditem[0]
        for support in all_supported:
            if(pmove.gmove.srcx == support.agent_srcx and pmove.gmove.srcy == support.agent_srcy and 
               pmove.gmove.dstx == support.agent_dstx and pmove.gmove.dsty == support.agent_dsty):
                if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy and  
                       e[2] == support.fieldx and e[3] == support.fieldy for e in excludes) == False):
                    if(pmove.prio > supporteditem[1]):
                        pmove.prio = supporteditem[1]
                        excludes.append([pmove.gmove.srcx, pmove.gmove.srcy, support.fieldx, support.fieldy])

    excludes.clear()
    list_forked.sort(key=itemgetter(1))
    for forkitem in list_forked:
        pmove = forkitem[0]
        for fork in all_forked:
            if(pmove.gmove.srcx == fork[0] and pmove.gmove.srcy == fork[1] and 
               pmove.gmove.dstx == fork[2] and pmove.gmove.dsty == fork[3]):
                if(any(e[0] == fork[0] and e[1] == fork[1] and
                       e[2] == fork[4] and e[3] == fork[5] for e in excludes) == False):
                    if(pmove.prio > forkitem[1]):
                        pmove.prio = forkitem[1]
                        excludes.append([fork[0], fork[1], fork[4], fork[5]])

    excludes.clear()
    list_flee.sort(key=itemgetter(1))
    for fleeitem in list_flee:
        pmove = fleeitem[0]
        if(any(e[0] == pmove.gmove.srcx and e[1] == pmove.gmove.srcy for e in excludes) == False):
            if(pmove.prio > fleeitem[1]):
                pmove.prio = fleeitem[1]
                excludes.append([pmove.gmove.srcx, pmove.gmove.srcy])

