from .match import *
from .matchmove import do_move, undo_move
from .move import *
from .pieces import pawn, knight, bishop, rook, king, generic_piece
from .cvalues import *
from . import rules
from .analyze_position import score_contacts, score_development, score_endgame
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
            token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN
        else:
            token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER

    for enmy in enmytouches:
        if(enmy == PIECES['wPw'] or enmy == PIECES['bPw']):
            token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN
        else:
            token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER

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

        pawncnt, officercnt, queencnt = generic_piece.count_contacts(fdlycontacts)
        if(pawncnt > 0):
            token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN
        if(officercnt + queencnt > 0):
            token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER

        pawncnt, officercnt, queencnt = generic_piece.count_contacts(enmycontacts)
        if(pawncnt > 0):
            token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN
        if(officercnt + queencnt > 0):
            token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER
        ###

        return token


def progress(match, move):
    token = 0x0
    piece = match.readfield(move.srcx, move.srcy)
    color = Match.color_of_piece(piece)

    ###
    oldvalue = score_contacts(match, color)

    if(match.count < 40):
        oldvalue += score_development(match, color)
    elif(match.count > 60):
        oldvalue += score_endgame(match, color)
    ###
    
    ###
    do_move(match, move.srcx, move.srcy, move.dstx, move.dsty, move.prom_piece)

    newvalue = score_contacts(match, color)

    if(match.count < 40):
        newvalue += score_development(match, color)
    elif(match.count > 60):
        newvalue += score_endgame(match, color)

    undo_move(match)
    ###

    if((newvalue - oldvalue >= SUPPORTED_SCORES[PIECES['wRk']] and color == COLORS['white']) or (newvalue - oldvalue <= SUPPORTED_SCORES[PIECES['bRk']] and color == COLORS['black'])):
        return token | MV_IS_PROGRESS
    else:
        return token


def analyze_move(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        token = token | MV_PIECE_IS_PAWN
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        token = token | MV_PIECE_IS_QUEEN
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        token = token | MV_PIECE_IS_KING
    else:
        token = token | MV_PIECE_IS_OFFICER

    token = token | captures(match, move)

    token = token | promotes(match, move)

    token = token | castles(match, move)

    token = token | touches(match, move)

    token = token | flees(match, move)

    token = token | progress(match, move)

    return token


def captured_is_equal_or_higher(token):
    if(token & MV_PIECE_IS_PAWN > 0):
        return True
    elif(token & MV_PIECE_IS_OFFICER > 0 and token & CAPTURED_IS_PAWN == 0):
        return True
    elif(token & MV_PIECE_IS_QUEEN and token & CAPTURED_IS_PAWN == 0 and token & CAPTURED_IS_OFFICER == 0):
        return True
    else:
        return False

def dstfield_is_attacked(token):
    if(token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN > 0 or token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER > 0 or token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_QUEEN > 0): 
        return True
    else:
        return False

def dstfield_is_supported(token):
    if(token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN > 0 or token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER > 0 or token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_QUEEN > 0):
        return True
    else:
        return False

def dstfield_is_attacked_and_supported_by_lower_equal(token):
    if(dstfield_is_attacked(token) and dstfield_is_supported(token)):
        if(token & MV_PIECE_IS_PAWN > 0):
            return True
        elif(token & MV_PIECE_IS_OFFICER > 0 and token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN == 0):
            return True
        elif(token & MV_PIECE_IS_QUEEN and token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN == 0 and token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER > 0):
            return True
        else:
            return False
    else:
        return False

def rank_moves(priomoves):
    for pmove in priomoves:
        count = 0
        token = pmove[2]
        piece = pmove[1]

        if(token & MV_IS_CASTLING > 0):
            count += 1
            pmove[3] = min(PRIO['prio2'], pmove[3])

        if(token & MV_IS_PROMOTION > 0):
            #count += 1
            pmove[3] = min(PRIO['prio1'], pmove[3])

        if(token & MV_IS_CAPTURE > 0):
            # captured is equal or higher
            if(captured_is_equal_or_higher(token)):
                #count += 1
                pmove[3] = min(PRIO['prio1'], pmove[3])
            # field is NOT enemy-touched
            elif(dstfield_is_attacked(token) == False):
                #count += 1
                pmove[3] = min(PRIO['prio1'], pmove[3])
            # field is NOT touched by lower enemy and field is friendly-touched
            elif(dstfield_is_attacked_and_supported_by_lower_equal(token)):
                #count += 1
                pmove[3] = min(PRIO['prio1'], pmove[3])
            else:
                count += 1
                pmove[3] = min(PRIO['prio5'], pmove[3])

        if(token & MV_IS_ATTACK > 0):
            # performes a check
            if(token & ATTACKED_IS_KING > 0):
                #count += 1
                pmove[3] = min(PRIO['prio1'], pmove[3])
            # attacker is NOT touched by enemy
            elif(dstfield_is_attacked(token) == False):
                count += 1
                pmove[3] = min(PRIO['prio3'], pmove[3])
            # attacker is NOT touched by lower enemy and field is friendly-touched
            elif(dstfield_is_attacked_and_supported_by_lower_equal(token)):
                count += 1
                pmove[3] = min(PRIO['prio3'], pmove[3])
            # attacker is NOT save
            else:
                count += 1
                pmove[3] = min(PRIO['prio5'], pmove[3])

        if(token & MV_IS_SUPPORT > 0):
            # supported is attacked
            if(token & SUPPORTED_IS_ATT_FROM_PAWN > 0 or token & SUPPORTED_IS_ATT_FROM_OFFICER > 0):
                # supporter is NOT touched by enemy
                if(dstfield_is_attacked(token) == False):
                    count += 1
                    pmove[3] = min(PRIO['prio3'], pmove[3])
                # supporter is NOT touched by lower enemy and field is friendly-touched
                elif(dstfield_is_attacked_and_supported_by_lower_equal(token)):
                    count += 1
                    pmove[3] = min(PRIO['prio3'], pmove[3])
                # supporter is NOT save
                else:
                    count += 1
                    pmove[3] = min(PRIO['prio5'], pmove[3])
            else:
                # supported is NOT attacked
                count += 1
                pmove[3] = min(PRIO['prio5'], pmove[3])

        if(token & MV_IS_FLEE > 0):
            # exile-field is NOT attacked
            if(dstfield_is_attacked(token) == False):
                count += 1
                pmove[3] = min(PRIO['prio3'], pmove[3])
            # exile-field is NOT touched by lower enemy and field is friendly-touched
            elif(dstfield_is_attacked_and_supported_by_lower_equal(token)):
                count += 1
                pmove[3] = min(PRIO['prio3'], pmove[3])
            else:
                # exile-field is attacked and not properly supported
                pmove[3] = min(PRIO['prio5'], pmove[3])

        if(token & MV_IS_PROGRESS > 0):
            pmove[3] = min(PRIO['prio3'], pmove[3])

        pmove[3] = max((pmove[3] - count * 10), PRIO['prio2'])

