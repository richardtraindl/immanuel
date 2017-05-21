from .match import *
from .move import *
from . import rules


def is_capture(match, move):
    piece = match.readfield(move.srcx, move.srcy)

    dstpiece = match.readfield(move.dstx, move.dsty)

    if(dstpiece != PIECES['blk']):
        return True
    elif( (piece == PIECES['wPw'] or piece == PIECES['bPw']) and move.srcx != move.dstx ):
        return True
    else:
        return False


def is_promotion(match, move):
    if(move.prom_piece == PIECES['blk']):
        return False
    else:
        return True


STEP_2E_X = 2
STEP_2W_X = -2
def is_castling(match, move):
    piece = match.readfield(move.srcx, move.srcy)

    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        if(move.srcx - move.dstx == STEP_2E_X or move.srcx - move.dstx == STEP_2W_X):
            return True

    return False



ATT_RESULTS = { 'kg' : 0, 'pinned' : 1, 'higher' : 2, , 'equal' : 3, , 'lower' : 4 }

def search_attacked(match, move):
    attacked = []

    piece = match.readfield(move.srcx, move.srcy)
    opp_color = Match.oppcolor_of_piece(piece)

    touched = rules.list_field_touches(match, opp_color, move.dstx, move.dsty)

    for touch in touched:
        opp_piece = touch[0]
        opp_piece_x = touch[1]
        opp_piece_y = touch[2]

        if(opp_piece == PIECES['wKg'] or PIECES['bKg']):
            attacked.append(ATT_RESULTS['kg'])
            continue
            
        pin_dir = rules.pin_dir(match, opp_piece_x, opp_piece_y)
        if(pin_dir != rules.DIRS['undefined']):
            attacked.append(ATT_RESULTS['pinned'])
            continue

        if(calc_helper.PIECES_RANK[opp_piece] > calc_helper.PIECES_RANK[piece]):
            attacked.append(ATT_RESULTS['higher'])
        elif(calc_helper.PIECES_RANK[opp_piece] == calc_helper.PIECES_RANK[piece]):
            attacked.append(ATT_RESULTS['equal'])
        else:
            attacked.append(ATT_RESULTS['lower'])

    return attacked


SUPP_RESULTS = { 'pinned' : 0, 'lower_than_attacker' : 1, 'equal_with_attacker' : 2, 'higher_than_attacker' : 3 }
    
def search_supported(match, move):
    supported = []

    piece = match.readfield(move.srcx, move.srcy)
    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    friendlytouches = rules.list_field_touches(match, color, move.dstx, move.dsty)

    for ftouch in friendlytouches:
        friend = ftouch[0]
        friend_x = ftouch[1]
        friend_y = ftouch[2]
        
        enemytouches = rules.list_field_touches(match, opp_color, friend_x, friend_y)
        for etouch in enemytouches:
            enemy = etouch[0]
            enemy_x = etouch[1]
            enemy_y = etouch[2]

            pin_dir = rules.pin_dir(match, friend_x, friend_y)
            if(pin_dir != rules.DIRS['undefined']):
                supported.append(SUPP_RESULTS['pinned'])
                continue

            if(calc_helper.PIECES_RANK[enemy] > calc_helper.PIECES_RANK[friend]):
                supported.append(SUPP_RESULTS['lower_than_attacker'])
            elif(calc_helper.PIECES_RANK[enemy] == calc_helper.PIECES_RANK[friend]):
                supported.append(SUPP_RESULTS['equal_with_attacker'])
            else:
                supported.append(SUPP_RESULTS['higher_than_attacker'])

    return supported


FLEE_RESULTS = { 'complete' : 0, 'to_higher_attacker' : 1, 'equal_with_attacker' : 2, 'to_lower_attacker' : 3 }

def flees(match, move):
    flees = []

    piece = match.readfield(move.srcx, move.srcy)
    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    enemytouches = rules.list_field_touches(match, opp_color, move.srcx, move.srcy)
    if(len(enemytouches) == 0):
        return flees

    match.writefield(move.srcx, move.srcy, PIECES['blk'])
    dstenemytouches = rules.list_field_touches(match, opp_color, move.dstx, move.dsty)
    dstfriendlytouches = rules.list_field_touches(match, color, move.dstx, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)
    
    if(len(dstenemytouches) == 0):
        flees.append(FLEE_RESULTS['complete'])
        return flees

    if(len(dstfriendlytouches) == 0):
        return flees

    erank = calc_helper.PIECES_RANK[PIECES['bKg']]
    for etouch in enemytouches:
        enemy = etouch[0]
        if(erank > calc_helper.PIECES_RANK[enemy]):
            erank = calc_helper.PIECES_RANK[enemy]

    dsterank = calc_helper.PIECES_RANK[PIECES['bKg']]
    for dstetouch in dstenemytouches:
        dstenemy = dstetouch[0]
        if(dsterank > calc_helper.PIECES_RANK[dstenemy]):
            dsterank = calc_helper.PIECES_RANK[dstenemy]
            
    if(erank < dsterank):
        flees.append(FLEE_RESULTS['to_higher_attacker'])
    elif(erank == dsterank):
        flees.append(FLEE_RESULTS['equal_with_attacker'])
    else:
        flees.append(FLEE_RESULTS['to_lower_attacker'])

    return flees
