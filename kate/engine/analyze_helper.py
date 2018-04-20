from .match import *
from .cvalues import *
from . import rules
from .pieces import pawn, rook, knight, bishop, queen, king


def piece_movecnt(match, gmove):
    
    if(gmove is None):
        return 0

    cnt = 1
    last_srcx = gmove.srcx
    last_srcy = gmove.srcy

    for move in match.move_list:
        if(last_srcx == move.dstx and last_srcy == move.dsty):
            cnt += 1
            last_srcx = move.srcx
            last_srcy = move.srcy

    return cnt


def is_soft_pin(match, srcx, srcy):
    piece = match.readfield(srcx, srcy)
    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)

    enemies = rook.list_field_touches(match, opp_color, srcx, srcy)
    for enemy in enemies:
        enemy_dir = rook.rk_dir(srcx, srcy, enemy.fieldx, enemy.fieldy)
        stepx, stepy = rook.rk_step(rules.REVERSE_DIRS[enemy_dir], None, None, None, None)[1:]
        x1, y1 = rules.search(match, srcx, srcy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            friend = match.readfield(x1, y1)
            if(match.color_of_piece(friend) == color and 
               PIECES_RANK[friend] > PIECES_RANK[piece] and 
               PIECES_RANK[friend] > PIECES_RANK[enemy.piece]):
                return True

    enemies.clear()
    enemies = bishop.list_field_touches(match, opp_color, srcx, srcy)
    for enemy in enemies:
        enemy_dir = bishop.bp_dir(srcx, srcy, enemy.fieldx, enemy.fieldy)
        stepx, stepy = bishop.bp_step(rules.REVERSE_DIRS[enemy_dir], None, None, None, None)[1:]
        x1, y1 = rules.search(match, srcx, srcy, stepx, stepy)
        if(x1 != rules.UNDEF_X):
            friend = match.readfield(x1, y1)
            if(match.color_of_piece(friend) == color and 
               PIECES_RANK[friend] > PIECES_RANK[piece] and 
               PIECES_RANK[friend] > PIECES_RANK[enemy.piece]):
                return True

    return False


def is_piece_stuck(match, srcx, srcy):
    piece = match.readfield(srcx, srcy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return pawn.is_piece_stuck(match, srcx, srcy)
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        return knight.is_piece_stuck(match, srcx, srcy)
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        return bishop.is_piece_stuck(match, srcx, srcy)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        return rook.is_piece_stuck(match, srcx, srcy)
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        return bishop.is_piece_stuck(match, srcx, srcy) or rook.is_piece_stuck(match, srcx, srcy)
    else:
        return king.is_piece_stuck(match, srcx, srcy)


def field_touches(match, color, fieldx, fieldy):
    frdlytouches = []
    enmytouches = []

    rook.field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches)

    bishop.field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches)

    knight.field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches)

    king.field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches)

    pawn.field_color_touches(match, color, fieldx, fieldy, frdlytouches, enmytouches)

    return frdlytouches, enmytouches


def field_touches_beyond(match, color, ctouch_beyond):
    rook.field_color_touches_beyond(match, color, ctouch_beyond)

    bishop.field_color_touches_beyond(match, color, ctouch_beyond)

    knight.field_color_touches_beyond(match, color, ctouch_beyond)

    king.field_color_touches_beyond(match, color, ctouch_beyond)

    pawn.field_color_touches_beyond(match, color, ctouch_beyond)

    return


def list_field_touches(match, color, fieldx, fieldy):
    touches = []

    newtouches = rook.list_field_touches(match, color, fieldx, fieldy)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    newtouches = bishop.list_field_touches(match, color, fieldx, fieldy)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    newtouches = knight.list_field_touches(match, color, fieldx, fieldy)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    newtouches = king.list_field_touches(match, color, fieldx, fieldy)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    newtouches = pawn.list_field_touches(match, color, fieldx, fieldy)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    return touches


def analyse_piece_fields(frdlycontacts, enmycontacts, mode, analyses):
    if(mode == "SRCFIELDTOUCHES"):
        for friend in frdlycontacts:
            piece = friend.piece
            
            if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                analyses.core.append(ANALYSES['SRCFLD_IS_FRDL_TOU_BY_PW'])
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                analyses.core.append(ANALYSES['SRCFLD_IS_FRDL_TOU_BY_KN'])
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                analyses.core.append(ANALYSES['SRCFLD_IS_FRDL_TOU_BY_BP'])
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                analyses.core.append(ANALYSES['SRCFLD_IS_FRDL_TOU_BY_RK'])
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                analyses.core.append(ANALYSES['SRCFLD_IS_FRDL_TOU_BY_QU'])
            elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                analyses.core.append(ANALYSES['SRCFLD_IS_FRDL_TOU_BY_KG'])
            
        for enmemy in enmycontacts:
            piece = enmemy.piece
            
            if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                analyses.core.append(ANALYSES['SRCFLD_IS_ENM_TOU_BY_PW'])
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                analyses.core.append(ANALYSES['SRCFLD_IS_ENM_TOU_BY_KN'])
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                analyses.core.append(ANALYSES['SRCFLD_IS_ENM_TOU_BY_BP'])
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                analyses.core.append(ANALYSES['SRCFLD_IS_ENM_TOU_BY_RK'])
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                analyses.core.append(ANALYSES['SRCFLD_IS_ENM_TOU_BY_QU'])
            elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                analyses.core.append(ANALYSES['SRCFLD_IS_ENM_TOU_BY_KG'])
    elif(mode == "DSTFIELDTOUCHES"):
        for friend in frdlycontacts:
            piece = friend.piece
            
            if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                analyses.core.append(ANALYSES['DSTFLD_IS_FRDL_TOU_BY_PW'])
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                analyses.core.append(ANALYSES['DSTFLD_IS_FRDL_TOU_BY_KN'])
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                analyses.core.append(ANALYSES['DSTFLD_IS_FRDL_TOU_BY_BP'])
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                analyses.core.append(ANALYSES['DSTFLD_IS_FRDL_TOU_BY_RK'])
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                analyses.core.append(ANALYSES['DSTFLD_IS_FRDL_TOU_BY_QU'])
            elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                analyses.core.append(ANALYSES['DSTFLD_IS_FRDL_TOU_BY_KG'])
            
        for enmemy in enmycontacts:
            piece = enmemy.piece
            
            if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                analyses.core.append(ANALYSES['DSTFLD_IS_ENM_TOU_BY_PW'])
            elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
                analyses.core.append(ANALYSES['DSTFLD_IS_ENM_TOU_BY_KN'])
            elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
                analyses.core.append(ANALYSES['DSTFLD_IS_ENM_TOU_BY_BP'])
            elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
                analyses.core.append(ANALYSES['DSTFLD_IS_ENM_TOU_BY_RK'])
            elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
                analyses.core.append(ANALYSES['DSTFLD_IS_ENM_TOU_BY_QU'])
            elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
                analyses.core.append(ANALYSES['DSTFLD_IS_ENM_TOU_BY_KG'])


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked):
    if(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        return queen.defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked)
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        return rook.defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked)
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        return bishop.defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked)
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        return knight.defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked)
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        return king.defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked)
    elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return pawn.defends_fork_field(match, piece, srcx, srcy, dstx, dsty, forked)
    else:
        return False


def is_fork_field(match, piece, forkx, forky):
    color = Match.color_of_piece(piece)
    opp_color = Match.oppcolor_of_piece(piece)
    
    fork_piece = match.readfield(forkx, forky)
    if(Match.color_of_piece(fork_piece) == opp_color):
        return False

    frdlytouches, enmytouches = field_touches(match, color, forkx, forky)
    if(len(frdlytouches) >= len(enmytouches)):
        return False

    if(queen.is_field_touched(match, opp_color, forkx, forky, 2)):
        if(queen.count_touches(match, color, forkx, forky) > 1):
            return True

    if(rook.is_field_touched(match, opp_color, forkx, forky, 2)):
        if(rook.count_touches(match, color, forkx, forky) > 1):
            return True

    if(bishop.is_field_touched(match, opp_color, forkx, forky, 2)):
        if(bishop.count_touches(match, color, forkx, forky) > 1):
            return True

    if(knight.is_field_touched(match, opp_color, forkx, forky, 2)):
        if(knight.count_touches(match, color, forkx, forky) > 1):
            return True

    if(pawn.is_field_touched(match, opp_color, forkx, forky, 2)):
        if(pawn.count_touches(match, color, forkx, forky) > 1):
            return True

    if(king.is_field_touched(match, opp_color, forkx, forky)):
        if(king.count_touches(match, color, forkx, forky) > 1):
            return True

    return False

def fetch_analyses(analyses, item):
    for analysis in analyses:
        if(analysis == item):
            return item

    return None

def fetch_range_analyses(analyses, start_item, end_item):
    for analysis in analyses:
        if(analysis >= start_item and analysis <= end_item):
            return item

    return None

def piece_is_lower_equal_than_captured(priomove):
    piece = fetch_range_analyses(analyses, ANALYSES['MV_PIECE_IS_PW'], ANALYSES['MV_PIECE_IS_KG'])
    captured_piece = fetch_range_analyses(analyses, ANALYSES['CAPTURED_IS_PW'], ANALYSES['CAPTURED_IS_QU'])

    if(captured_piece in None):
        return False

    if(piece == ANALYSES['MV_PIECE_IS_KG']):
        return False
    elif(piece == ANALYSES['MV_PIECE_IS_QU']):
        if(captured_piece == ANALYSES['CAPTURED_IS_QU']):
            return True
        else:
            return False
    elif(piece == ANALYSES['MV_PIECE_IS_RK']):
        if(captured_piece == ANALYSES['CAPTURED_IS_QU'] or 
           captured_piece == ANALYSES['CAPTURED_IS_RK']):
            return True
        else:
            return False
    elif(piece == ANALYSES['MV_PIECE_IS_BP'] or piece == ANALYSES['MV_PIECE_IS_KN']):
        if(captured_piece == ANALYSES['CAPTURED_IS_QU'] or 
           captured_piece == ANALYSES['CAPTURED_IS_RK'] or
           captured_piece == ANALYSES['CAPTURED_IS_BP'] or
           captured_piece == ANALYSES['CAPTURED_IS_KN']):
            return True
        else:
            return False
    elif(piece == ANALYSES['MV_PIECE_IS_PW']):
        return True

    return False


def piece_is_lower_equal_than_captured2(token):
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


def piece_is_lower_equal_than_enemy_on_srcfield(token):
    if(token & MV_PIECE_IS_KG > 0):
        return False
    elif(token & MV_PIECE_IS_QU > 0):
        if(token & SRCFLD_IS_ENM_TOU_BY_RK > 0 or
           token & SRCFLD_IS_ENM_TOU_BY_BP > 0 or 
           token & SRCFLD_IS_ENM_TOU_BY_KN > 0 or
           token & SRCFLD_IS_ENM_TOU_BY_PW > 0):
            return False
        else:
            return True
    elif(token & MV_PIECE_IS_RK > 0):
        if(token & SRCFLD_IS_ENM_TOU_BY_BP > 0 or 
           token & SRCFLD_IS_ENM_TOU_BY_KN > 0 or 
           token & SRCFLD_IS_ENM_TOU_BY_PW > 0):
            return False
        else:
            return True
    elif(token & MV_PIECE_IS_BP > 0 or token & MV_PIECE_IS_KN > 0):
        if(token & SRCFLD_IS_ENM_TOU_BY_PW > 0):
            return False
        else:
            return True
    else: # MV_PIECE_IS_PW
        return True


def piece_is_lower_equal_than_enemy_on_dstfield(token):
    if(token & MV_PIECE_IS_KG > 0):
        return False
    elif(token & MV_PIECE_IS_QU > 0):
        if(token & DSTFLD_IS_ENM_TOU_BY_RK > 0 or
           token & DSTFLD_IS_ENM_TOU_BY_BP > 0 or
           token & DSTFLD_IS_ENM_TOU_BY_KN > 0 or
           token & DSTFLD_IS_ENM_TOU_BY_PW > 0):
            return False
        else:
            return True
    elif(token & MV_PIECE_IS_RK > 0):
        if(token & DSTFLD_IS_ENM_TOU_BY_BP > 0 or
           token & DSTFLD_IS_ENM_TOU_BY_KN > 0 or
           token & DSTFLD_IS_ENM_TOU_BY_PW > 0):
            return False
        else:
            return True
    elif(token & MV_PIECE_IS_BP > 0 or token & MV_PIECE_IS_KN > 0):
        if(token & DSTFLD_IS_ENM_TOU_BY_PW > 0):
            return False
        else:
            return True
    else: # MV_PIECE_IS_PW
        return True


def piece_is_lower_fairy_equal_than_enemy_on_dstfield(token):
    if(token & MV_PIECE_IS_KG > 0):
        return False
    elif(token & MV_PIECE_IS_QU > 0):
        if(token & DSTFLD_IS_ENM_TOU_BY_RK > 0 or
           token & DSTFLD_IS_ENM_TOU_BY_BP > 0 or
           token & DSTFLD_IS_ENM_TOU_BY_KN > 0 or
           token & DSTFLD_IS_ENM_TOU_BY_PW > 0):
            return False
        else:
            return True
    elif(token & MV_PIECE_IS_RK > 0 or token & MV_PIECE_IS_BP > 0 or token & MV_PIECE_IS_KN > 0):
        if(token & DSTFLD_IS_ENM_TOU_BY_PW > 0):
            return False
        else:
            return True
    else: # MV_PIECE_IS_PW
        return True


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

    for ctouch_beyond in attacked:
        if(len(ctouch_beyond.supporter_beyond) > 0):
            return True

    return False


def is_attacked_pinned(match, attacked):
    if(len(attacked) == 0):
        return None

    for ctouch_beyond in attacked:
        pindir = rules.pin_dir(match, None, ctouch_beyond.fieldx, ctouch_beyond.fieldy)
        if(pindir != rules.DIRS['undefined']):
            return True

    return False


def is_attacked_soft_pinned(match, attacked):
    if(len(attacked) == 0):
        return None

    for ctouch_beyond in attacked:
        if(is_soft_pin(match, ctouch_beyond.fieldx, ctouch_beyond.fieldy)):
            return True

    return False


def is_attacked_add_attacked(attacked):
    if(len(attacked) == 0):
        return None

    for ctouch_beyond in attacked:
        if(len(ctouch_beyond.attacker_beyond) > 0):
            return True

    return False


def is_attacked_higher_than_piece(match, attacked):
    for ctouch_beyond in attacked:
        piece = match.readfield(ctouch_beyond.agent_srcx, ctouch_beyond.agent_srcy)
        if(PIECES_RANK[ctouch_beyond.piece] > PIECES_RANK[piece]):
            return True

    return False


def is_supported_attacked(supported):
    if(len(supported) == 0):
        return None

    for ctouch_beyond in supported:
        if(len(ctouch_beyond.attacker_beyond) > 0):
            return True

    return False


def is_supported_lower_equal_than_attacker(supported):
    if(len(supported) == 0):
        return None

    for ctouch_beyond in supported:
        for attacker_beyond in ctouch_beyond.attacker_beyond:
            if(PIECES_RANK[ctouch_beyond.piece] > PIECES_RANK[attacker_beyond.piece]):
                return False

    return True


def is_supported_add_supported(supported):
    if(len(supported) == 0):
        return None

    for ctouch_beyond in supported:
        if(len(ctouch_beyond.supporter_beyond) > 0):
            return True

    return False


def is_disclosed_attacked_supported(disclosed_attacked):
    if(len(disclosed_attacked) == 0):
        return None

    for ctouch_beyond in disclosed_attacked:
        if(len(ctouch_beyond.supporter_beyond) > 0):
            return True

    return False


def highest_disclosed_attacked(disclosed_attacked):
    piece = PIECES['blk']

    for ctouch_beyond in disclosed_attacked:
        if(PIECES_RANK[ctouch_beyond.piece] > PIECES_RANK[piece]):
            piece = ctouch_beyond.piece

    return piece

