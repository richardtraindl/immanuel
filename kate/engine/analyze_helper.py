from .match import *
from .cvalues import *
from . import rules
from .pieces import pawn, rook, knight, bishop, queen, king


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


def piece_is_lower_equal_than_captured(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    
    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return True

    captured_piece = match.readfield(gmove.dstx, gmove.dsty)
    if(PIECES_RANK[piece] <= PIECES_RANK[captured_piece]):
        return True
    else:
        return False
  

def dstfield_is_supported(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    
    match.writefield(gmove.srcx, gmove.srcy, PIECES['blk'])    

    is_touched = rules.is_field_touched(match, Match.color_of_piece(piece), gmove.dstx, gmove.dsty, 0)

    match.writefield(gmove.srcx, gmove.srcy, piece)
    
    return is_touched


def dstfield_is_attacked(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    
    match.writefield(gmove.srcx, gmove.srcy, PIECES['blk'])    

    is_touched = rules.is_field_touched(match, Match.oppcolor_of_piece(piece), gmove.dstx, gmove.dsty, 0)

    match.writefield(gmove.srcx, gmove.srcy, piece)
    
    return is_touched


def dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    
    match.writefield(gmove.srcx, gmove.srcy, PIECES['blk'])

    frdlytouches, enmytouches = field_touches(match, Match.color_of_piece(piece), gmove.dstx, gmove.dsty)
    
    match.writefield(gmove.srcx, gmove.srcy, piece)

    return len(frdlytouches) >= len(enmytouches)


def piece_is_lower_equal_than_enemy_on_srcfield(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    enemies = list_field_touches(match, Match.oppcolor_of_piece(piece), gmove.srcx, gmove.srcy)

    for enemy in enemies:
        if(PIECES_RANK[piece] > PIECES_RANK[enemy.piece]):
            return False

    return True


def piece_is_lower_fairy_equal_than_enemy_on_dstfield(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    enemies = list_field_touches(match, Match.oppcolor_of_piece(piece), gmove.dstx, gmove.dsty)

    for enemy in enemies:
        if(PIECES_RANK[piece] > PIECES_RANK[enemy.piece]):
            if(PIECES_RANK[piece] == PIECES_RANK[PIECES['wRk']] and 
               PIECES_RANK[enemy.piece] == PIECES_RANK[PIECES['wBp']]):
                continue
            else:
                return False

    return True


def is_discl_attacked_supported(discl_attacked):
    if(len(discl_attacked) == 0):
        return False

    for ctouch_beyond in discl_attacked:
        if(len(ctouch_beyond.supporter_beyond) > 0):
            return True

    return False


def is_discl_supported_attacked_(discl_supported):
    if(len(discl_supported) == 0):
        return False

    for ctouch_beyond in discl_supported:
        if(len(ctouch_beyond.attacker_beyond) > 0):
            print("disclosed supported is attacked")
            return True

    return False


def srcfield_is_supported(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    return rules.is_field_touched(match, Match.color_of_piece(piece), gmove.srcx, gmove.srcy, 0)


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty): # , forked
    if(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        return queen.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        return rook.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        return bishop.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        return knight.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        return king.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
    elif(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return pawn.defends_fork_field(match, piece, srcx, srcy, dstx, dsty) # , forked
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


def is_piece_attacked(lst, piece1, piece2):
    for ctouch_beyond in lst:
        if(ctouch_beyond.piece == piece1 or ctouch_beyond.piece == piece2):
            return True

    return False


def piece_is_lower_equal_than_enemy_on_dstfield(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    match.writefield(gmove.srcx, gmove.srcy, PIECES['blk'])

    enemies = list_field_touches(match, Match.oppcolor_of_piece(piece), gmove.dstx, gmove.dsty)

    match.writefield(gmove.srcx, gmove.srcy, piece)

    for enemy in enemies:
        if(PIECES_RANK[piece] > PIECES_RANK[enemy.piece]):
            return False

    return True


def is_attacked_supported(attacked):
    if(len(attacked) == 0):
        return False

    for ctouch_beyond in attacked:
        if(len(ctouch_beyond.supporter_beyond) > 0):
            return True

    return False


def is_attacked_pinned(match, attacked):
    if(len(attacked) == 0):
        return False

    for ctouch_beyond in attacked:
        pindir = rules.pin_dir(match, None, ctouch_beyond.fieldx, ctouch_beyond.fieldy)
        if(pindir != rules.DIRS['undefined']):
            return True

    return False


def is_attacked_soft_pinned(match, attacked):
    if(len(attacked) == 0):
        return False

    for ctouch_beyond in attacked:
        if(is_soft_pin(match, ctouch_beyond.fieldx, ctouch_beyond.fieldy)):
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
        return False

    for ctouch_beyond in supported:
        if(len(ctouch_beyond.attacker_beyond) > 0):
            return True

    return False


def is_supported_lower_equal_than_attacker(supported):
    if(len(supported) == 0):
        return False

    for ctouch_beyond in supported:
        for attacker_beyond in ctouch_beyond.attacker_beyond:
            if(PIECES_RANK[ctouch_beyond.piece] > PIECES_RANK[attacker_beyond.piece]):
                return False

    return True


"""def is_supported_add_supported(analyses):
    if(len(analyses.lst_supported) == 0):
        return False

    for ctouch_beyond in analyses.lst_supported:
        if(len(ctouch_beyond.supporter_beyond) > 0):
            return True

    return False


def highest_disclosed_attacked(analyses):
    piece = PIECES['blk']

    for ctouch_beyond in analyses.lst_disclosed_attacked:
        if(PIECES_RANK[ctouch_beyond.piece] > PIECES_RANK[piece]):
            piece = ctouch_beyond.piece

    return piece



def is_attacked_add_attacked(analyses):
    if(len(analyses.lst_attacked) == 0):
        return False

    for ctouch_beyond in analyses.lst_attacked:
        if(len(ctouch_beyond.attacker_beyond) > 0):
            return True

    return False"""
