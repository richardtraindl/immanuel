from .cvalues import *
from . import rules

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
    if(len(attacked) == 0):
        return None

    for ctouch in attacked:
        if(len(ctouch.supporter_beyond) == 0):
            return False

    return True


def is_attacked_pinned(match, attacked):
    if(len(attacked) == 0):
        return None

    for ctouch in attacked:
        pindir = rules.pin_dir(match, ctouch.fieldx, ctouch.fieldy)
        if(pindir != rules.DIRS['undefined']):
            return True

    return False


def is_attacked_add_attacked(attacked):
    if(len(attacked) == 0):
        return None

    for ctouch in attacked:
        if(len(ctouch.attacker_beyond) == 0):
            return False

    return True


def is_attacked_higher_than_piece(match, attacked):
    for ctouch in attacked:
        piece = match.readfield(ctouch.agent_srcx, ctouch.agent_srcy)
        if(PIECES_RANK[ctouch.piece] > PIECES_RANK[piece]):
            return True

    return False


def is_supported_attacked(supported):
    if(len(supported) == 0):
        return None

    for ctouch in supported:
        if(len(ctouch.attacker_beyond) == 0):
            return False

    return True


def is_supported_lower_equal_than_attacker(supported):
    if(len(supported) == 0):
        return None

    for ctouch in supported:
        for attacker_beyond in ctouch.attacker_beyond:
            if(PIECES_RANK[ctouch.piece] > PIECES_RANK[attacker_beyond[0]]):
                return False

    return True


def is_supported_add_supported(supported):
    if(len(supported) == 0):
        return None

    for ctouch in supported:
        if(len(ctouch.supporter_beyond) == 0):
            return False

    return False


def is_disclosed_attacked_supported(disclosed_attacked):
    if(len(disclosed_attacked) == 0):
        return None

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
