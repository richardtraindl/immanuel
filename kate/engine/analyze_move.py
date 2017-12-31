from random import randint
from .match import *
from .matchmove import do_move, undo_move
from .move import *
from .pieces import pawn, knight, bishop, rook, king
from .pieces.generic_piece import contacts_to_token
from .calc import *
from .cvalues import *
from . import rules
from .analyze_position import score_contacts, score_opening, score_endgame


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

    if(rules.defends_fork_field(match, piece, move.srcx, move.srcy, move.dstx, move.dsty)):
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
    tokens = [0] * 4
    token = 0x0
    attacked = []
    supported = []
    disclosed_attacked = []

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
    
    token = token | disclosures(match, move, disclosed_attacked)

    token = token | flees(match, move)

    # token = token | progress(match, move)

    tokens[0] = token
    tokens[1] = attacked
    tokens[2] = supported
    tokens[3] = disclosed_attacked
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
        if((token & DSTFLD_IS_ENM_TOU_BY_KG > 0 or
            token & DSTFLD_IS_ENM_TOU_BY_QU > 0) and 
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

def piece_is_lower_fairy_equal_than_enemy_on_dstfield(token):
    if(token & MV_PIECE_IS_KG > 0):
        return False
    elif(token & MV_PIECE_IS_QU > 0):
        if((token & DSTFLD_IS_ENM_TOU_BY_KG > 0 or
            token & DSTFLD_IS_ENM_TOU_BY_QU > 0) and
           token & DSTFLD_IS_ENM_TOU_BY_RK == 0 and
           token & DSTFLD_IS_ENM_TOU_BY_BP == 0 and
           token & DSTFLD_IS_ENM_TOU_BY_KN == 0 and
           token & DSTFLD_IS_ENM_TOU_BY_PW == 0):
            return True
        else:
            return False
    elif(token & MV_PIECE_IS_RK > 0 or token & MV_PIECE_IS_BP > 0 or token & MV_PIECE_IS_KN > 0):
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

def is_attacked_add_attacked(attacked):
    for ctouch in attacked:
        if(len(ctouch.attacker_beyond) > 0):
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

def is_disclosed_attacked_supported(disclosed_attacked):
    for ctouch in disclosed_attacked:
        if(len(ctouch.supporter_beyond) == 0):
            return False
    return True

def highest_disclosed_attacked(disclosed_attacked):
    piece = PIECES['blk']

    for ctouch in disclosed_attacked:
        if(PIECES_RANK[ctouch.piece] > PIECES_RANK[piece]):
            piece = ctouch.piece
    return piece

class PrioMove:
    def __init__(self, gmove=None, piece=None, tokens=None, prio=None):
        self.gmove = gmove
        self.piece = piece
        self.tokens = tokens
        self.prio = prio

def rank_moves(priomoves):
    fleecnt = 0
    flee_list = []

    for priomove in priomoves:
        token = priomove.tokens[0]
        attacked = priomove.tokens[1]
        supported = priomove.tokens[2]
        disclosed_attacked = priomove.tokens[3]

        if(token & MV_IS_CASTLING > 0):
            priomove.prio = min(PRIO['prio3a'], priomove.prio)

        if(token & MV_IS_PROMOTION > 0):
            priomove.prio = min(PRIO['prio1a'], priomove.prio)

        if(token & MV_IS_CAPTURE > 0):
            if(piece_is_lower_equal_than_captured(token) or 
               dstfield_is_attacked(token) == False or 
               (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token)) ):
                priomove.prio = min(PRIO['prio1a'], priomove.prio)
            elif(dstfield_is_attacked(token) == False or dstfield_is_supported(token)):
                priomove.prio = min(PRIO['prio2a'], priomove.prio)
            else:
                priomove.prio = min(PRIO['prio3a'], priomove.prio)

        if(token & MV_IS_ATTACK > 0):
            if(dstfield_is_attacked(token) == False or 
               (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token)) ):
                if(token & ATTACKED_IS_KG > 0):
                    priomove.prio = min(PRIO['prio1b'], priomove.prio)
                elif(is_attacked_supported(attacked) == False):
                    priomove.prio = min(PRIO['prio2b'], priomove.prio)
                else:
                    priomove.prio = min(PRIO['prio3b'], priomove.prio)
            else:
                if(token & ATTACKED_IS_KG > 0):
                    priomove.prio = min(PRIO['prio2b'], priomove.prio)
                else:
                    priomove.prio = min(PRIO['prio3b'], priomove.prio)

        if(token & MV_IS_SUPPORT > 0):
            if(is_supported_attacked(supported)):
                if(dstfield_is_attacked(token) == False or
                   (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token)) ):
                    if(is_supported_add_supported(supported) == False and 
                       is_supported_lower_equal_than_attacker(supported)):
                        priomove.prio = min(PRIO['prio1c'], priomove.prio)
                    else:
                        priomove.prio = min(PRIO['prio2c'], priomove.prio)
                else:
                    priomove.prio = min(PRIO['prio3c'], priomove.prio)
            else:
                priomove.prio = min(PRIO['prio3c'], priomove.prio)

        if(token & MV_IS_FORK_DEFENSE > 0):
            if(dstfield_is_attacked(token) == False or 
               (dstfield_is_supported(token) and piece_is_lower_fairy_equal_than_enemy_on_dstfield(token)) ):
                priomove.prio = min(PRIO['prio1c'], priomove.prio)
            else:
                priomove.prio = min(PRIO['prio3c'], priomove.prio)

        if(token & MV_IS_DISCLOSURE > 0):
            if(is_disclosed_attacked_supported(disclosed_attacked) == False):
                priomove.prio = min(PRIO['prio1b'], priomove.prio)
            else:
                priomove.prio = min(PRIO['prio2b'], priomove.prio)

        if(token & MV_IS_FLEE > 0):
            if(srcfield_is_supported(token) == False or 
               (srcfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_srcfield(token) == False)):
                if(dstfield_is_attacked(token) == False or
                   (dstfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_dstfield(token)) ):
                    if(priomove.prio != PRIO['prio1b']):
                        flee_list.append([priomove, priomove.prio])
                    priomove.prio = min(PRIO['prio1b'], priomove.prio)
                else:
                    priomove.prio = min(PRIO['prio4b'], priomove.prio)
            else:
                priomove.prio = min(PRIO['last'], priomove.prio)

        if(token & MV_IS_PROGRESS > 0):
            priomove.prio = min(PRIO['prio2b'], priomove.prio)

        if(dstfield_is_attacked(token) == False or dstfield_is_supported(token)):
            priomove.prio = min(PRIO['prio4a'], priomove.prio)

        if(token & MV_PIECE_IS_QU > 0 and priomove.prio != PRIO['prio1c'] and priomove.prio != PRIO['last']):
            priomove.prio += 1

    fleecnt = 0
    for fleemove in flee_list:
        fleecnt += 1
        if(fleecnt > 1):
            priomove = fleemove[0]
            priomove.prio = fleemove[1]

