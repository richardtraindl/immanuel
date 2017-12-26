from .match import *
from .matchmove import do_move, undo_move
from .move import *
from .pieces import pawn, knight, bishop, rook, king
from .pieces.generic_piece import contacts_to_token
from .cvalues import *
from . import rules
from .analyze_position import score_contacts, score_opening, score_endgame
from random import randint


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

    token = token | rook.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)

    token = token | bishop.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)

    token = token | knight.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)

    token = token | king.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)

    token = token | pawn.attacks_and_supports(match, move.srcx, move.srcy, move.dstx, move.dsty, attacked, supported)

    return token


def defends_fork(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    if(rules.defends_forked_field(match, piece, move.srcx, move.srcy, move.dstx, move.dsty)):
        token = token | MV_IS_FORK_DEFENSE

    return token


def disclosures(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)
    color = Match.color_of_piece(piece)

    if(rules.disclosures_field(match, color, move.srcx, move.srcy, move.dstx, move.dsty)):
        token = token | MV_IS_DISCLOSURE

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

    if(match.count > 60):
        if(score_endgame(match) > 0):
            return token | MV_IS_PROGRESS
        else:
            return token
    elif(match.count > 40):
        ###
        oldvalue = score_contacts(match, color)
        ###
        do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

        newvalue = score_contacts(match, color)

        undo_move(match)
        ###
    else:
        ###
        #oldvalue = score_contacts(match, color)
        oldvalue = score_opening(match)
        ###
        do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

        #newvalue = score_contacts(match, color)
        newvalue = score_opening(match)

        undo_move(match)
        ###
        
    if((newvalue - oldvalue >= SUPPORTED_SCORES[PIECES['wQu']] and color == COLORS['white']) or 
       (newvalue - oldvalue <= SUPPORTED_SCORES[PIECES['bQu']] and color == COLORS['black'])):
        return token | MV_IS_PROGRESS
    else:
        return token


def analyze_move(match, move):
    tokens = [0] * 3
    token = 0x0
    attacked = []
    supported = []

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

    token = token | defends_fork(match, move)
    
    token = token | disclosures(match, move)

    token = token | flees(match, move)

    token = token | progress(match, move)

    tokens[0] = token
    tokens[1] = attacked
    tokens[2] = supported
    return tokens


def piece_is_lower_equal_than_captured(token):
    if(token & MV_PIECE_IS_KG > 0):
        return False
    elif(token & MV_PIECE_IS_QU > 0):
        if(token & CAPTURED_IS_QU > 0):
            return True
        else:
            return False
    elif(token & MV_PIECE_IS_RK > 0):
        if(token & CAPTURED_IS_QU > 0 or 
           token & CAPTURED_IS_RK > 0):
            return True
        else:
            return False
    elif(token & MV_PIECE_IS_BP > 0 or token & MV_PIECE_IS_KN > 0):
        if(token & CAPTURED_IS_QU > 0 or 
           token & CAPTURED_IS_RK > 0 or
           token & CAPTURED_IS_BP > 0 or
           token & CAPTURED_IS_KN > 0):
            return True
        else:
            return False
    else: # MV_PIECE_IS_PW
        if(token & CAPTURED_IS_QU > 0 or
           token & CAPTURED_IS_RK > 0 or
           token & CAPTURED_IS_BP > 0 or
           token & CAPTURED_IS_KN > 0 or
           token & CAPTURED_IS_PW > 0):
            return True
        else:
            return False

def piece_is_lower_equal_than_attacked(token):
    if(token & MV_PIECE_IS_KG > 0):
        return False
    elif(token & MV_PIECE_IS_QU > 0):
        if(token & ATTACKED_IS_KG > 0 or 
           token & ATTACKED_IS_QU > 0):
            return True
        else:
            return False
    elif(token & MV_PIECE_IS_RK > 0):
        if(token & ATTACKED_IS_KG > 0 or 
           token & ATTACKED_IS_QU > 0 or
           token & ATTACKED_IS_RK > 0):
            return True
        else:
            return False
    elif(token & MV_PIECE_IS_BP > 0 or token & MV_PIECE_IS_KN > 0):
        if(token & ATTACKED_IS_KG > 0 or 
           token & ATTACKED_IS_QU > 0 or 
           token & ATTACKED_IS_RK > 0 or 
           token & ATTACKED_IS_BP > 0 or 
           token & ATTACKED_IS_KN > 0):
            return True
        else:
            return False
    else: # MV_PIECE_IS_PW
        if(token & ATTACKED_IS_KG > 0 or 
           token & ATTACKED_IS_QU > 0 or
           token & ATTACKED_IS_RK > 0 or
           token & ATTACKED_IS_BP > 0 or
           token & ATTACKED_IS_KN > 0 or
           token & ATTACKED_IS_PW > 0):
            return True
        else:
            return False

def piece_is_lower_equal_than_enemy_on_srcfield(token):
    if(token & MV_PIECE_IS_KG > 0):
        return False
    elif(token & MV_PIECE_IS_QU > 0):
        if(token & SRCFLD_IS_ENM_TOU_BY_QU > 0 and 
           token & SRCFLD_IS_ENM_TOU_BY_RK == 0 and
           token & SRCFLD_IS_ENM_TOU_BY_BP == 0 and
           token & SRCFLD_IS_ENM_TOU_BY_KN == 0 and
           token & SRCFLD_IS_ENM_TOU_BY_PW == 0):
            return True
        else:
            return False
    elif(token & MV_PIECE_IS_RK > 0):
        if((token & SRCFLD_IS_ENM_TOU_BY_KG > 0 or 
            token & SRCFLD_IS_ENM_TOU_BY_QU > 0 or 
            token & SRCFLD_IS_ENM_TOU_BY_RK > 0) and
           token & SRCFLD_IS_ENM_TOU_BY_BP == 0 and
           token & SRCFLD_IS_ENM_TOU_BY_KN == 0 and
           token & SRCFLD_IS_ENM_TOU_BY_PW == 0):
            return True
        else:
            return False
    elif(token & MV_PIECE_IS_BP > 0 or token & MV_PIECE_IS_KN > 0):
        if((token & SRCFLD_IS_ENM_TOU_BY_KG > 0 or 
            token & SRCFLD_IS_ENM_TOU_BY_QU > 0 or 
            token & SRCFLD_IS_ENM_TOU_BY_RK > 0 or
            token & SRCFLD_IS_ENM_TOU_BY_BP > 0 or
            token & SRCFLD_IS_ENM_TOU_BY_KN > 0) and 
           token & SRCFLD_IS_ENM_TOU_BY_PW == 0):
            return True
        else:
            return False
    else: # MV_PIECE_IS_PW
        if(token & SRCFLD_IS_ENM_TOU_BY_KG > 0 or 
           token & SRCFLD_IS_ENM_TOU_BY_QU > 0 or 
           token & SRCFLD_IS_ENM_TOU_BY_RK > 0 or 
           token & SRCFLD_IS_ENM_TOU_BY_BP > 0 or 
           token & SRCFLD_IS_ENM_TOU_BY_KN > 0 or
           token & SRCFLD_IS_ENM_TOU_BY_PW > 0):
            return True
        else:
            return False

def piece_is_lower_equal_than_enemy_on_dstfield(token):
    if(token & MV_PIECE_IS_KG > 0):
        return False
    elif(token & MV_PIECE_IS_QU > 0):
        if(token & DSTFLD_IS_ENM_TOU_BY_QU > 0 and 
           token & DSTFLD_IS_ENM_TOU_BY_RK == 0 and
           token & DSTFLD_IS_ENM_TOU_BY_BP == 0 and
           token & DSTFLD_IS_ENM_TOU_BY_KN == 0 and
           token & DSTFLD_IS_ENM_TOU_BY_PW == 0):
            return True
        else:
            return False
    elif(token & MV_PIECE_IS_RK > 0):
        if((token & DSTFLD_IS_ENM_TOU_BY_KG > 0 or 
            token & DSTFLD_IS_ENM_TOU_BY_QU > 0 or 
            token & DSTFLD_IS_ENM_TOU_BY_RK > 0) and
           token & DSTFLD_IS_ENM_TOU_BY_BP == 0 and
           token & DSTFLD_IS_ENM_TOU_BY_KN == 0 and
           token & DSTFLD_IS_ENM_TOU_BY_PW == 0):
            return True
        else:
            return False
    elif(token & MV_PIECE_IS_BP > 0 or token & MV_PIECE_IS_KN > 0):
        if((token & DSTFLD_IS_ENM_TOU_BY_KG > 0 or 
            token & DSTFLD_IS_ENM_TOU_BY_QU > 0 or 
            token & DSTFLD_IS_ENM_TOU_BY_RK > 0 or
            token & DSTFLD_IS_ENM_TOU_BY_BP > 0 or
            token & DSTFLD_IS_ENM_TOU_BY_KN > 0) and 
           token & DSTFLD_IS_ENM_TOU_BY_PW == 0):
            return True
        else:
            return False
    else: # MV_PIECE_IS_PW
        if(token & DSTFLD_IS_ENM_TOU_BY_KG > 0 or 
           token & DSTFLD_IS_ENM_TOU_BY_QU > 0 or 
           token & DSTFLD_IS_ENM_TOU_BY_RK > 0 or 
           token & DSTFLD_IS_ENM_TOU_BY_BP > 0 or 
           token & DSTFLD_IS_ENM_TOU_BY_KN > 0 or
           token & DSTFLD_IS_ENM_TOU_BY_PW > 0):
            return True
        else:
            return False

def srcfield_is_supported(token):
    if(token & SRCFLD_IS_FRDL_TOU_BY_PW > 0 or 
       token & SRCFLD_IS_FRDL_TOU_BY_KN > 0 or 
       token & SRCFLD_IS_FRDL_TOU_BY_BP > 0 or 
       token & SRCFLD_IS_FRDL_TOU_BY_RK > 0 or 
       token & SRCFLD_IS_FRDL_TOU_BY_QU > 0 or 
       token & SRCFLD_IS_FRDL_TOU_BY_KG > 0):
        return True
    else:
        return False

def dstfield_is_attacked(token):
    if(token & DSTFLD_IS_ENM_TOU_BY_PW > 0 or 
       token & DSTFLD_IS_ENM_TOU_BY_KN > 0 or 
       token & DSTFLD_IS_ENM_TOU_BY_BP > 0 or 
       token & DSTFLD_IS_ENM_TOU_BY_RK > 0 or 
       token & DSTFLD_IS_ENM_TOU_BY_QU > 0 or 
       token & DSTFLD_IS_ENM_TOU_BY_KG > 0):
        return True
    else:
        return False

def dstfield_is_supported(token):
    if(token & DSTFLD_IS_FRDL_TOU_BY_PW > 0 or 
       token & DSTFLD_IS_FRDL_TOU_BY_KN > 0 or 
       token & DSTFLD_IS_FRDL_TOU_BY_BP > 0 or 
       token & DSTFLD_IS_FRDL_TOU_BY_RK > 0 or 
       token & DSTFLD_IS_FRDL_TOU_BY_QU > 0 or 
       token & DSTFLD_IS_FRDL_TOU_BY_KG > 0):
        return True
    else:
        return False

def is_attacked_supported(attacked):
    for ctouch in attacked:
        if(len(ctouch.supporter_beyond) > 0):
            return True
    return False

def is_supported_attacked(supported):
    for ctouch in supported:
        if(len(ctouch.attacker_beyond) > 0):
            return True
    return False

def is_supported_lower_equal_than_attacker(supported):
    for ctouch in supported:
        for attacker_beyond in ctouch.attacker_beyond:
            if(PIECES_RANK[ctouch.piece] <= PIECES_RANK[attacker_beyond[0]]):
                return True
    return False

def is_supported_add_supported(supported):
    for ctouch in supported:
        if(len(ctouch.supporter_beyond) > 1):
            return True
    return False

def rank_moves(priomoves):
    fleecnt = 0

    for pmove in priomoves:
        gmove = pmove[0]
        piece = pmove[1]
        tokens = pmove[2]
        token = tokens[0]
        attacked = tokens[1]
        supported = tokens[2]
        
        flee_list = []

        if(token & MV_IS_CASTLING > 0):
            pmove[3] = min(PRIO['prio3'], pmove[3])

        if(token & MV_IS_PROMOTION > 0):
            pmove[3] = min(PRIO['prio1'], pmove[3])

        if(token & MV_IS_CAPTURE > 0):
            if(piece_is_lower_equal_than_captured(token) or 
               dstfield_is_attacked(token) == False or
               (dstfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_dstfield(token))):
                pmove[3] = min(PRIO['prio1'], pmove[3])
            else:
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_ATTACK > 0):
            if(dstfield_is_attacked(token) == False or 
               (dstfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_dstfield(token)) ):
                if(token & ATTACKED_IS_KG > 0):
                    pmove[3] = min(PRIO['prio1'], pmove[3])
                elif(is_attacked_supported(attacked) == False or piece_is_lower_equal_than_attacked(token)):
                    pmove[3] = min(PRIO['prio2'], pmove[3])
                else:
                    pmove[3] = min(PRIO['prio3'], pmove[3])
            else:
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_SUPPORT > 0):
            if(dstfield_is_attacked(token) == False or 
               (dstfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_dstfield(token)) ):
                if(is_supported_attacked(supported) and is_supported_add_supported(supported) == False and is_supported_lower_equal_than_attacker(supported)):
                    pmove[3] = min(PRIO['prio1'], pmove[3])
                else:
                    pmove[3] = min(PRIO['prio3'], pmove[3])
            else:
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_FORK_DEFENSE > 0):
            pmove[3] = min(PRIO['prio1'], pmove[3])
            
        if(token & MV_IS_DISCLOSURE > 0):
            pmove[3] = min(PRIO['prio2'], pmove[3])

        if(token & MV_IS_FLEE > 0):
            if(srcfield_is_supported(token) == False or 
               (srcfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_srcfield(token) == False)):
                if(dstfield_is_attacked(token) == False or
                   (dstfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_dstfield(token)) ):
                    if(pmove[3] != PRIO['prio1']):
                        flee_list.append(pmove)
                    pmove[3] = min(PRIO['prio1'], pmove[3])
                else:
                    pmove[3] = min(PRIO['prio4'], pmove[3])
            else:
                pmove[3] = min(PRIO['last'], pmove[3])

        if(token & MV_IS_PROGRESS > 0):
            pmove[3] = min(PRIO['prio3'], pmove[3])

        if(dstfield_is_attacked(token) == False or dstfield_is_supported(token)):
            pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_PIECE_IS_QU > 0 and pmove[3] != PRIO['last']):
            pmove[3] += 1

    fleecnt = 0
    for fleemove in flee_list:
        fleecnt += 1
        if(fleecnt > 2):
            fleemove[3] = PRIO['prio3']

