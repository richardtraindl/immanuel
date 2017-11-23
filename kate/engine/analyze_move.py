from .match import *
from .matchmove import do_move, undo_move
from .move import *
from .pieces import pawn, knight, bishop, rook, king, generic_piece
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
            token = token | MV_IS_CAPTURE | CAPTURED_IS_PAWN
        elif(dstpiece == PIECES['wQu'] or dstpiece == PIECES['bQu']):
            token = token | MV_IS_CAPTURE | CAPTURED_IS_QUEEN
        else:
            token = token | MV_IS_CAPTURE | CAPTURED_IS_OFFICER
    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and move.srcx != move.dstx ):
        token = token | MV_IS_CAPTURE | CAPTURED_IS_PAWN
    else:
        return token

    match.writefield(move.srcx, move.srcy, PIECES['blk'])
    fdlytouches, enmytouches = rules.field_touches(match, color, move.dstx, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)

    for friend in fdlytouches:
        if(friend == PIECES['wPw'] or friend == PIECES['bPw']):
            token = token | DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN
        else:
            token = token | DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER

    for enmy in enmytouches:
        if(enmy == PIECES['wPw'] or enmy == PIECES['bPw']):
            token = token | DSTFIELD_IS_ENMYTOUCHED_BY_PAWN
        else:
            token = token | DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER

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


def touches(match, move):
    token = 0x0

    token = token | rook.touches(match, move.srcx, move.srcy, move.dstx, move.dsty)

    token = token | bishop.touches(match, move.srcx, move.srcy, move.dstx, move.dsty)

    token = token | knight.touches(match, move.srcx, move.srcy, move.dstx, move.dsty)

    token = token | king.touches(match, move.srcx, move.srcy, move.dstx, move.dsty)

    token = token | pawn.touches(match, move.srcx, move.srcy, move.dstx, move.dsty)

    return token


"""def forks(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    enmycontacts = rules.forks(match, piece, move.dstx, move.dsty)

    if(len(enmycontacts) > 1):
        token = token | MV_IS_FORK

    return token
"""


def flees(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    enmycontacts = rules.list_field_touches(match, opp_color, move.srcx, move.srcy)

    if(len(enmycontacts) == 0):
        return token
    else:
        token = token | MV_IS_FLEE

        ###
        match.writefield(move.srcx, move.srcy, PIECES['blk'])

        fdlycontacts, enmycontacts = rules.field_touches(match, color, move.dstx, move.dsty)

        match.writefield(move.srcx, move.srcy, piece)

        pawncnt, officercnt, queencnt, kingcnt = generic_piece.count_contacts(fdlycontacts)
        if(pawncnt > 0):
            token = token | DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN
        if(officercnt + queencnt + kingcnt > 0):
            token = token | DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER

        pawncnt, officercnt, queencnt, kingcnt = generic_piece.count_contacts(enmycontacts)
        if(pawncnt > 0):
            token = token | DSTFIELD_IS_ENMYTOUCHED_BY_PAWN
        if(officercnt + queencnt + kingcnt > 0):
            token = token | DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER
        ###

        return token


def progress(match, move):
    token = 0x0
    piece = match.readfield(move.srcx, move.srcy)
    color = Match.color_of_piece(piece)

    if(match.count > 60):
        if(score_endgame(match, color) > 0):
            return token | MV_IS_PROGRESS
        else:
            return token
    elif(match.count > 40):
        ###
        oldvalue = score_contacts(match, color)
        #oldvalue += score_opening(match, color)
        ###
        do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

        newvalue = score_contacts(match, color)
        #newvalue += score_opening(match, color)

        undo_move(match)
        ###
    else:
        ###
        #oldvalue = score_contacts(match, color)
        oldvalue = score_opening(match, color)
        ###
        do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

        #newvalue = score_contacts(match, color)
        newvalue = score_opening(match, color)

        undo_move(match)
        ###
        
    if((newvalue - oldvalue >= SUPPORTED_SCORES[PIECES['wQu']] and color == COLORS['white']) or 
       (newvalue - oldvalue <= SUPPORTED_SCORES[PIECES['bQu']] and color == COLORS['black'])):
        return token | MV_IS_PROGRESS
    else:
        return token


def analyze_move(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        token = token | PIECE_IS_PAWN
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        token = token | PIECE_IS_QUEEN
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        token = token | PIECE_IS_KING
    else:
        token = token | PIECE_IS_OFFICER

    token = token | captures(match, move)

    token = token | promotes(match, move)

    token = token | castles(match, move)

    token = token | touches(match, move)

    token = token | flees(match, move)

    token = token | progress(match, move)

    return token


def captured_is_lower_than_piece(token):
    if(token & PIECE_IS_KING > 0):
        return True
    elif(token & PIECE_IS_QUEEN > 0):
        if(token & CAPTURED_IS_QUEEN > 0):
            return False
        else:
            return True
    elif(token & PIECE_IS_OFFICER > 0):
        if(token & CAPTURED_IS_PAWN > 0):
            return True
        else:
            return False
    else: # token & PIECE_IS_PAWN > 0
        return False

def attacked_is_lower_than_piece(token):
    if(token & PIECE_IS_KING > 0):
        return True
    elif(token & PIECE_IS_QUEEN > 0):
        if(token & ATTACKED_IS_QUEEN > 0):
            return False
        else:
            return True
    elif(token & PIECE_IS_OFFICER > 0):
        if(token & ATTACKED_IS_PAWN > 0):
            return True
        else:
            return False
    else: # token & PIECE_IS_PAWN > 0
        return False

def piece_is_lower_than_enemy_on_srcfield(token):
    if(token & PIECE_IS_KING > 0):
        return False
    elif(token & PIECE_IS_QUEEN > 0):
        return False
    elif(token & PIECE_IS_OFFICER > 0):
        if(token & SRCFIELD_IS_ENMYTOUCHED_BY_PAWN > 0 or token & SRCFIELD_IS_ENMYTOUCHED_BY_OFFICER > 0):
            return False
        else:
            return True
    else: # token & PIECE_IS_PAWN > 0
        if(token & SRCFIELD_IS_ENMYTOUCHED_BY_PAWN > 0):
            return False
        else:
            return True

def piece_is_lower_equal_than_enemy_on_srcfield(token):
    if(token & PIECE_IS_KING > 0):
        return False
    elif(token & PIECE_IS_QUEEN > 0):
        if(token & SRCFIELD_IS_ENMYTOUCHED_BY_QUEEN > 0):
            return True
        else:
            return False
    elif(token & PIECE_IS_OFFICER > 0):
        if(token & SRCFIELD_IS_ENMYTOUCHED_BY_PAWN > 0):
            return False
        else:
            return True
    else: # token & PIECE_IS_PAWN > 0
        return True

def piece_is_lower_than_enemy_on_dstfield(token):
    if(token & PIECE_IS_KING > 0):
        return False
    elif(token & PIECE_IS_QUEEN > 0):
        return False
    elif(token & PIECE_IS_OFFICER > 0):
        if(token & DSTFIELD_IS_ENMYTOUCHED_BY_PAWN > 0 or token & DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER > 0):
            return False
        else:
            return True
    else: # token & PIECE_IS_PAWN > 0
        if(token & DSTFIELD_IS_ENMYTOUCHED_BY_PAWN > 0):
            return False
        else:
            return True

def piece_is_lower_equal_than_enemy_on_dstfield(token):
    if(token & PIECE_IS_KING > 0):
        return False
    elif(token & PIECE_IS_QUEEN > 0):
        if(token & DSTFIELD_IS_ENMYTOUCHED_BY_QUEEN > 0):
            return True
        else:
            return False
    elif(token & PIECE_IS_OFFICER > 0):
        if(token & DSTFIELD_IS_ENMYTOUCHED_BY_PAWN > 0):
            return False
        else:
            return True
    else: # token & PIECE_IS_PAWN > 0
        return True

"""def attacked_is_supported(token):        
    if(token & ATTACKED_IS_SUPP_BY_PAWN > 0 or 
       token & ATTACKED_IS_SUPP_BY_OFFICER > 0):
        return True
    else:
        return False
"""

def supported_is_attacked(token):
    if(token & SUPPORTED_IS_ATT_FROM_PAWN > 0 or token & SUPPORTED_IS_ATT_FROM_OFFICER > 0):
        return True
    else:
        return False

def supported_is_add_supported(token):
    if(token & SUPPORTED_IS_ADD_SUPP_BY_PAWN > 0 or token & SUPPORTED_IS_ADD_SUPP_BY_OFFICER > 0):
        return True
    else:
        return False

"""def supported_is_attacked_from_lower(token):
    #if(token & SUPPORTED_IS_ATT_FROM_QUEEN > 0):
    #    return False
    if(token & SUPPORTED_IS_ATT_FROM_OFFICER): # > 0 and (token & SUPPORTED_IS_PAWN > 0 or token & SUPPORTED_IS_OFFICER > 0)):
        return False
    elif(token & SUPPORTED_IS_ATT_FROM_PAWN > 0 and token & SUPPORTED_IS_PAWN > 0):
        return False
    else:
        return True
"""

def srcfield_is_supported(token):
    if(token & SRCFIELD_IS_FRDLYTOUCHED_BY_PAWN > 0 or token & SRCFIELD_IS_FRDLYTOUCHED_BY_OFFICER > 0 or token & SRCFIELD_IS_FRDLYTOUCHED_BY_QUEEN > 0 or token & SRCFIELD_IS_FRDLYTOUCHED_BY_KING > 0):
        return True
    else:
        return False

def dstfield_is_attacked(token):
    if(token & DSTFIELD_IS_ENMYTOUCHED_BY_PAWN > 0 or token & DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER > 0 or token & DSTFIELD_IS_ENMYTOUCHED_BY_QUEEN > 0 or token & DSTFIELD_IS_ENMYTOUCHED_BY_KING > 0):
        return True
    else:
        return False

def dstfield_is_supported(token):
    if(token & DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN > 0 or token & DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER > 0 or token & DSTFIELD_IS_FRDLYTOUCHED_BY_QUEEN > 0 or token & DSTFIELD_IS_FRDLYTOUCHED_BY_KING > 0):
        return True
    else:
        return False

def rank_moves(priomoves):
    for pmove in priomoves:
        token = pmove[2]
        piece = pmove[1]

        if(token & MV_IS_CASTLING > 0):
            pmove[3] = min(PRIO['prio2'], pmove[3])

        if(token & MV_IS_PROMOTION > 0):
            pmove[3] = min(PRIO['prio1'], pmove[3])

        if(token & MV_IS_CAPTURE > 0):
            if(captured_is_lower_than_piece(token) == False or dstfield_is_attacked(token) == False):
                pmove[3] = min(PRIO['prio1'], pmove[3])
            else:
                pmove[3] = min(PRIO['prio3'], pmove[3])

        if(token & MV_IS_ATTACK > 0):
            if(token & ATTACKED_IS_KING > 0):
                pmove[3] = min(PRIO['prio1'], pmove[3])
            elif(dstfield_is_supported(token) or dstfield_is_attacked(token) == False or attacked_is_lower_than_piece(token) == False):
                pmove[3] = min(PRIO['prio2'], pmove[3])
            else:
                pmove[3] = min(PRIO['prio3'], pmove[3])

        if(token & MV_IS_SUPPORT > 0):
            if(supported_is_attacked(token)):
                if(supported_is_add_supported(token) == False and (dstfield_is_attacked(token) == False or dstfield_is_supported(token)) ):
                    pmove[3] = min(PRIO['prio1'], pmove[3])
                else:
                    pmove[3] = min(PRIO['prio3'], pmove[3])
            else:
                if(supported_is_add_supported(token) == False and (dstfield_is_attacked(token) == False or dstfield_is_supported(token))):
                    pmove[3] = min(PRIO['prio2'], pmove[3])
                else:
                    pmove[3] = min(PRIO['prio3'], pmove[3])

        if(token & MV_IS_FLEE > 0):
            if(srcfield_is_supported(token) == False or 
               (srcfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_srcfield(token) == False)):
                if(dstfield_is_attacked(token) == False):
                    pmove[3] = min(PRIO['prio1'], pmove[3])
                elif(dstfield_is_supported(token) and piece_is_lower_equal_than_enemy_on_dstfield(token)):
                    pmove[3] = min(PRIO['prio1'], pmove[3])
                else:
                    pmove[3] = min(PRIO['prio3'], pmove[3])
            else:
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_PROGRESS > 0):
            pmove[3] = min(PRIO['prio3'], pmove[3])

