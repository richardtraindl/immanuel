from .match import *
from .move import *
from .pieces import pawn, knight, bishop, rook, king
from .cvalues import *
from . import rules
from random import randint


def is_capture(match, move):
    piece = match.readfield(move.srcx, move.srcy)

    dstpiece = match.readfield(move.dstx, move.dsty)

    if(dstpiece != PIECES['blk']):
        if(PIECES_RANK[dstpiece] >= PIECES_RANK[piece]):
            return True, PRIO['prio1']
        else:
            match.writefield(move.srcx, move.srcy, PIECES['blk'])
            enemytouched = rules.is_field_touched(match, Match.color_of_piece(dstpiece), move.dstx, move.dsty)
            match.writefield(move.srcx, move.srcy, piece)        
            if(enemytouched):
                return True, PRIO['prio3']
            else:
                return True, PRIO['prio1']
    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and move.srcx != move.dstx ):
        return True, PRIO['prio1']
    else:
        return False, PRIO['undefined']


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


def is_promotion(match, move):
    if(move.prom_piece == PIECES['blk']):
        return False, PRIO['undefined']
    else:
        return True, PRIO['prio1']


def promotes(match, move):
    token = 0x0

    if(move.prom_piece == PIECES['blk']):
        return token
    else:
        return token | MV_IS_PROMOTION


def is_castling(match, move):
    piece = match.readfield(move.srcx, move.srcy)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(move.srcx - move.dstx == 2 or move.srcx - move.dstx == -2):
            return True, PRIO['prio1']

    return False, PRIO['undefined']


def castles(match, move):
    token = 0x0

    piece = match.readfield(move.srcx, move.srcy)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(move.srcx - move.dstx == 2 or move.srcx - move.dstx == -2):
            return token | MV_IS_CASTLING

    return token


def does_attack(match, move):
    flag, priority = rook.does_attack(match, move.srcx, move.srcy, move.dstx, move.dsty)
    if(flag):
        return True, priority

    flag, priority = bishop.does_attack(match, move.srcx, move.srcy, move.dstx, move.dsty)
    if(flag):
        return True, priority

    flag, priority = knight.does_attack(match, move.srcx, move.srcy, move.dstx, move.dsty)
    if(flag):
        return True, priority

    flag, priority = king.does_attack(match, move.srcx, move.srcy, move.dstx, move.dsty)
    if(flag ):
        return True, priority

    flag, priority = pawn.does_attack(match, move.srcx, move.srcy, move.dstx, move.dsty)
    if(flag):
        return True, priority

    return False, 0


def touches(match, move):
    token = 0x0

    token = token | rook.touches(match, move.srcx, move.srcy, move.dstx, move.dsty)

    token = token | bishop.touches(match, move.srcx, move.srcy, move.dstx, move.dsty)

    token = token | knight.touches(match, move.srcx, move.srcy, move.dstx, move.dsty)

    token = token | king.touches(match, move.srcx, move.srcy, move.dstx, move.dsty)

    token = token | pawn.touches(match, move.srcx, move.srcy, move.dstx, move.dsty)

    return token


def does_support_attacked(match, move):
    flag, priority = rook.does_support_attacked(match, move.srcx, move.srcy, move.dstx, move.dsty)
    if(flag):
        return True, priority

    flag, priority = bishop.does_support_attacked(match, move.srcx, move.srcy, move.dstx, move.dsty)
    if(flag):
        return True, priority

    flag, priority = knight.does_support_attacked(match, move.srcx, move.srcy, move.dstx, move.dsty)
    if(flag):
        return True, priority

    flag, priority = king.does_support_attacked(match, move.srcx, move.srcy, move.dstx, move.dsty)
    if(flag):
        return True, priority

    flag, priority = pawn.does_support_attacked(match, move.srcx, move.srcy, move.dstx, move.dsty)
    if(flag):
        return True, priority

    return False, 0


def supports(match, move, token):
    token = rook.supports(match, move.srcx, move.srcy, move.dstx, move.dsty, token)

    token = bishop.supports(match, move.srcx, move.srcy, move.dstx, move.dsty, token)

    token = knight.supports(match, move.srcx, move.srcy, move.dstx, move.dsty, token)

    token = king.supports(match, move.srcx, move.srcy, move.dstx, move.dsty, token)

    token = pawn.supports(match, move.srcx, move.srcy, move.dstx, move.dsty, token)

    token = touches(match, move, token)

    return token


def count_attacks(match, srcx, srcy, dstx, dsty):
    count = 0

    count += rook.count_attacks(match, srcx, srcy, dstx, dsty)

    count += knight.count_attacks(match, srcx, srcy, dstx, dsty)

    count += bishop.count_attacks(match, srcx, srcy, dstx, dsty)

    count += king.count_attacks(match, srcx, srcy, dstx, dsty)

    count += pawn.count_attacks(match, srcx, srcy, dstx, dsty)

    return count


def score_attacks(match, srcx, srcy):
    score = 0

    score += rook.score_attacks(match, srcx, srcy)

    score += knight.score_attacks(match, srcx, srcy)

    score += bishop.score_attacks(match, srcx, srcy)

    score += king.score_attacks(match, srcx, srcy)

    score += pawn.score_attacks(match, srcx, srcy)

    return score


def score_supports_of_attacked(match, srcx, srcy):
    score = 0
    
    score += rook.score_supports_of_attacked(match, srcx, srcy)

    score += bishop.score_supports_of_attacked(match, srcx, srcy)

    score += knight.score_supports_of_attacked(match, srcx, srcy)

    score += king.score_supports_of_attacked(match, srcx, srcy)

    score += pawn.score_supports_of_attacked(match, srcx, srcy)

    return score


def does_attacked_flee(match, move):
    piece = match.readfield(move.srcx, move.srcy)
    
    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    enemytouches = rules.list_field_touches(match, opp_color, move.srcx, move.srcy)

    if(len(enemytouches) == 0):
        return False, PRIO['undefined']
    else:
        friendlytouches = rules.list_field_touches(match, color, move.srcx, move.srcy)
        
        if(len(friendlytouches) > 0):
            wellsupported = True
            for etouch in enemytouches:
                enemy = etouch[0]
                if(PIECES_RANK[piece] > PIECES_RANK[enemy]):
                    wellsupported = False

            if(wellsupported == True):
                return True, PRIO['prio4']

        match.writefield(move.srcx, move.srcy, PIECES['blk'])
        dstenemytouches = rules.list_field_touches(match, opp_color, move.dstx, move.dsty)
        dstfriendlytouches = rules.list_field_touches(match, color, move.dstx, move.dsty)
        match.writefield(move.srcx, move.srcy, piece)                

        if(len(dstenemytouches) == 0):
            return True, PRIO['prio2']
        else:        
            if(len(dstfriendlytouches) == 0):
                return True, PRIO['prio4']
            else:
                for dstetouch in dstenemytouches:
                    dstenemy = dstetouch[0]
                    if(PIECES_RANK[piece] > PIECES_RANK[dstenemy]):
                        return True, PRIO['prio4']

            return True, PRIO['prio3']


def count_contacts(contacts):
    pawncnt = 0
    officercnt = 0

    for contact in contacts:
        if(contact == PIECES['wPw'] or contact == PIECES['bPw']):
            pawncnt += 1
        else:
            officercnt += 1
    return pawncnt, officercnt


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

        pawncnt, officercnt = count_contacts(fdlycontacts)
        if(pawncnt > 0):
            token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN
        if(officercnt > 0):
            token = token | MV_DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER

        pawncnt, officercnt = count_contacts(enmycontacts)
        if(pawncnt > 0):
            token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN
        if(officercnt > 0):
            token = token | MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER
        ###

        return token


def is_endgame_move(match, move):
    if(match.count > 60):
        if(pawn.is_running(match, move)):
            return True, PRIO['prio3']
        else:
            piece = match.readfield(move.srcx, move.srcy)
            if(piece == PIECES['wPw'] or piece == PIECES['bPw'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                return True, PRIO['prio4']
            else:
                return False, PRIO['undefined']
    else:
        return False, PRIO['undefined']


def progress(match, move):
    token = 0x0

    if(match.count > 60):
        if(pawn.is_running(match, move)):
            return token | MV_IS_PROGRESS
        else:
            piece = match.readfield(move.srcx, move.srcy)
            if(piece == PIECES['wPw'] or piece == PIECES['bPw'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                return token | MV_IS_PROGRESS
            else:
                return token
    else:
        if(randint(0, 5) == 0):
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

def attacker_is_equal_or_lower(token):
    if(token & MV_PIECE_IS_PAWN > 0):
        return True
    elif(token & MV_PIECE_IS_OFFICER > 0 and token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN == 0):
        return True
    elif(token & MV_PIECE_IS_QUEEN and token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN == 0 and token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER > 0):
        return True
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
            elif(token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN == 0 and token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER == 0):
                #count += 1
                pmove[3] = min(PRIO['prio1'], pmove[3])
            # field is NOT touched by enemy-pawn and field is friendly-touched
            elif(token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN == 0 and 
                 (token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN > 0 or token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER > 0)):
                #count += 1
                pmove[3] = min(PRIO['prio1'], pmove[3])
            else:
                count += 1
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_ATTACK > 0):
            # performes a check
            if(token & ATTACKED_IS_KING > 0):
                count += 1
                pmove[3] = min(PRIO['prio2'], pmove[3])
            # attacker is NOT touched by enemy
            elif(token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN == 0 and token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER == 0):
                count += 1
                pmove[3] = min(PRIO['prio3'], pmove[3])
            # attacker is touched by friend
            elif(token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN > 0 or token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER > 0):
                count += 1
                pmove[3] = min(PRIO['prio3'], pmove[3])
            else:
                count += 1
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_SUPPORT > 0):
            # supported is attacked
            if(token & SUPPORTED_IS_ATT_FROM_PAWN > 0 or token & SUPPORTED_IS_ATT_FROM_OFFICER > 0):
                # supporter is NOT touched by enemy
                if(token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN == 0 and token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER == 0):
                    count += 1
                    pmove[3] = min(PRIO['prio3'], pmove[3])
                # supporter is touched by friend
                elif(token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN > 0 or token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER > 0):
                    count += 1
                    pmove[3] = min(PRIO['prio3'], pmove[3])
                else:
                    count += 1
                    pmove[3] = min(PRIO['prio4'], pmove[3])
            else:
                # supported is NOT attacked
                count += 1
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_FLEE > 0):
            # exile-field is NOT attacked
            if(token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN == 0 and token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_OFFICER == 0):
                count += 1
                pmove[3] = min(PRIO['prio3'], pmove[3])
            # exile-field is touched by friend and (refugee is pawn or exile-field is NOT touched by enemy-pawn)
            elif(token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_PAWN > 0 or token & MV_DSTFIELD_IS_FRDLYTOUCHED_BY_OFFICER > 0 and 
                 (token & MV_PIECE_IS_PAWN > 0 or token & MV_DSTFIELD_IS_ENMYTOUCHED_BY_PAWN == 0)):
                count += 1
                pmove[3] = min(PRIO['prio3'], pmove[3])
            else:
                # exile-field is attacked
                pmove[3] = min(PRIO['prio4'], pmove[3])

        if(token & MV_IS_PROGRESS > 0 and pmove[3] > PRIO['prio2']):
            pmove[3] = PRIO['prio2']

        if(count >= 2 and pmove[3] != PRIO['prio1']):
            pmove[3] -= 1
