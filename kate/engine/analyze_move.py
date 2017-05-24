from .match import *
from .move import *
from .pieces import pawn, knight, bishop, rook, king
from .cvalues import *
from . import rules


def is_capture(match, move):
    piece = match.readfield(move.srcx, move.srcy)

    dstpiece = match.readfield(move.dstx, move.dsty)

    if(dstpiece != PIECES['blk']):
        if(PIECES_RANK[dstpiece] >= PIECES_RANK[piece]):
            return True, PRIO['prio1']
        else:
            match.writefield(move.srcx, move.srcy, PIECES['blk'])
            touched = rules.is_field_touched(match, Match.color_of_piece(dstpiece), move.dstx, move.dsty)
            match.writefield(move.srcx, move.srcy, piece)        
            if(touched):
                return True, PRIO['prio2']
            else:
                return True, PRIO['prio1']
    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and move.srcx != move.dstx ):
        return True, PRIO['prio1']
    else:
        return False, PRIO['undefinded']


def is_promotion(match, move):
    if(move.prom_piece == PIECES['blk']):
        return False, PRIO['undefinded']
    else:
        return True, PRIO['prio1']


def is_castling(match, move):
    piece = match.readfield(move.srcx, move.srcy)
    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(move.srcx - move.dstx == 2 or move.srcx - move.dstx == -2):
            return True, PRIO['prio1']

    return False, PRIO['undefinded']


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
        return False, PRIO['undefinded']
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
            return True, PRIO['prio3']
        else:        
            if(len(dstfriendlytouches) == 0):
                return True, PRIO['prio4']
            else:
                for dstetouch in dstenemytouches:
                    dstenemy = dstetouch[0]
                    if(PIECES_RANK[piece] > PIECES_RANK[dstenemy]):
                        return True, PRIO['prio4']

            return True, PRIO['prio3']


def is_endgame_move(match, move):
    if(match.count > 60):
        if(pawn.is_running(match, move)):
            return True, PRIO['prio3']
        else:
            piece = match.readfield(move.srcx, move.srcy)
            if(piece == PIECES['wPw'] or piece == PIECES['bPw'] or piece == PIECES['wKg'] or piece == PIECES['bKg']):
                return True, PRIO['prio4']
            else:
                return False, PRIO['undefinded']
    else:
        return False, PRIO['undefinded']

