from .match import *
from .pieces.pawn import cPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .pieces import pawnfield, knightfield, rookfield, bishopfield, queenfield, kingfield
from .pieces.piece import cTouch


class cDirTouch:
    def __init__(self, piece, direction, fieldx, fieldy):
        self.piece = piece
        self.direction = direction
        self.fieldx = fieldx
        self.fieldy = fieldy

def search_dir(match, fieldx, fieldy, direction, exclx, excly):
    srcx = fieldx
    srcy = fieldy
    stepx, stepy = cQueen.step_for_dir(direction)
    dirtouches = []

    for i in range(7):
        x1, y1 = match.search(srcx, srcy, stepx, stepy)
        if(x1 is not None and x1 != exclx and y1 != excly):
            piece = match.readfield(x1, y1)
            dirtouches.append(cDirTouch(piece, direction, x1, y1))
            srcx = x1
            srcy = y1
        else:
            break

    return dirtouches


def search_lines_of_pin(match, color, fieldx, fieldy, exclx, excly):
    pinlines = []

    piece = match.readfield(fieldx, fieldy)

    oppcolor = match.REVERSED_COLORS[color]
    
    DIRS = [match.DIRS['north'], match.DIRS['south'], match.DIRS['east'], match.DIRS['west'], match.DIRS['north-east'], match.DIRS['south-west'], match.DIRS['north-west'], match.DIRS['south-east']]
 
    for i in range(8):
        dirtouches = search_dir(match, fieldx, fieldy, DIRS[i], exclx, excly)

        if(len(dirtouches) < 2):
            continue

        if(match.color_of_piece(dirtouches[0].piece) == color and 
           match.color_of_piece(dirtouches[1].piece) == oppcolor and
           match.PIECES_RANK[piece] > match.PIECES_RANK[dirtouches[0].piece] and 
           match.PIECES_RANK[piece] > match.PIECES_RANK[dirtouches[1].piece]):

            if(dirtouches[1].piece == match.PIECES['wQu'] or dirtouches[1].piece == match.PIECES['bQu']):
                pinlines.append([dirtouches[0], dirtouches[1]])

            elif(i < 4 and (dirtouches[1].piece == match.PIECES['wRk'] or dirtouches[1].piece == match.PIECES['bRk'])): 
                pinlines.append([dirtouches[0], dirtouches[1]])

            elif(i >= 4 and (dirtouches[1].piece == match.PIECES['wBp'] or dirtouches[1].piece == match.PIECES['bBp'])):
                pinlines.append([dirtouches[0], dirtouches[1]])

    return pinlines


def search_opposed_pieces(match, color, fieldx, fieldy, excl_fieldx, excl_fieldy):
    oppenents = []

    MAX_STEP_IDX_FOR_RK = 3
    
    oppcolor = match.REVERSED_COLORS[color]

    for i in range(0, 8, 2):
        touches = [None, None]

        for k in range(2):
            stepx = cQueen.STEPS[i+k][0]
            stepy = cQueen.STEPS[i+k][1]

            x1, y1 = match.search(fieldx, fieldy, stepx, stepy)
            if(x1 is not None and x1 == excl_fieldx and y1 == excl_fieldy):
                break

            if(x1):
                piece = match.readfield(x1, y1)

                if(match.color_of_piece(piece) == color):
                    if(touches[0] is None):
                        touches[0] = cTouch(piece, x1, y1)
                else:
                    if(touches[1] is None):
                        if(piece == match.PIECES['wQu'] or piece == match.PIECES['bQu'] or
                          (i+k <= MAX_STEP_IDX_FOR_RK and (piece == match.PIECES['wRk'] or piece == match.PIECES['bRk'])) or
                          (i+k > MAX_STEP_IDX_FOR_RK and (piece == match.PIECES['wBp'] or piece == match.PIECES['bBp']))):
                            touches[1] = cTouch(piece, x1, y1)

        if(touches[0] and touches[1]):
            oppenents.append(touches)

    return oppenents


def is_piece_stuck_new(match, srcx, srcy):
    piece = match.readfield(srcx, srcy)

    if(piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']):
        cpawn = cPawn(match, srcx, srcy)
        return cpawn.is_piece_stuck_new()
    elif(piece == match.PIECES['wKn'] or piece == match.PIECES['bKn']):
        cknight = cKnight(match, srcx, srcy)
        return cknight.is_piece_stuck_new()
    elif(piece == match.PIECES['wBp'] or piece == match.PIECES['bBp']):
        cbishop = cBishop(match, srcx, srcy)
        return cbishop.is_piece_stuck_new()
    elif(piece == match.PIECES['wRk'] or piece == match.PIECES['bRk']):
        crook = cRook(match, srcx, srcy)
        return crook.is_piece_stuck_new()
    elif(piece == match.PIECES['wQu'] or piece == match.PIECES['bQu']):
        cqueen = cQueen(match, srcx, srcy)
        return cqueen.is_piece_stuck_new()
    else:
        cking = cKing(match, srcx, srcy)
        return cking.is_piece_stuck_new()


def list_all_field_touches(match, color, fieldx, fieldy):
    frdlytouches = []
    enmytouches = []

    crookfield = rookfield.cRookField(match, fieldx, fieldy)
    crookfield.list_all_field_touches(color, frdlytouches, enmytouches)

    cbishopfield = bishopfield.cBishopField(match, fieldx, fieldy)
    cbishopfield.list_all_field_touches(color, frdlytouches, enmytouches)

    cknightfield = knightfield.cKnightField(match, fieldx, fieldy)
    cknightfield.list_all_field_touches(color, frdlytouches, enmytouches)

    ckingfield = kingfield.cKingField(match, fieldx, fieldy)
    ckingfield.list_all_field_touches(color, frdlytouches, enmytouches)

    cpawnfield = pawnfield.cPawnField(match, fieldx, fieldy)
    cpawnfield.list_all_field_touches(color, frdlytouches, enmytouches)

    return frdlytouches, enmytouches


def field_touches_beyond(match, color, ctouch_beyond):
    crookfield = rookfield.cRookField(match, ctouch_beyond.fieldx, ctouch_beyond.fieldy)
    crookfield.list_all_field_touches(color, ctouch_beyond.supporter_beyond, ctouch_beyond.attacker_beyond)

    cbishopfield = bishopfield.cBishopField(match, ctouch_beyond.fieldx, ctouch_beyond.fieldy)
    cbishopfield.list_all_field_touches(color, ctouch_beyond.supporter_beyond, ctouch_beyond.attacker_beyond)

    cknightfield = knightfield.cKnightField(match, ctouch_beyond.fieldx, ctouch_beyond.fieldy)
    cknightfield.list_all_field_touches(color, ctouch_beyond.supporter_beyond, ctouch_beyond.attacker_beyond)

    ckingfield = kingfield.cKingField(match, ctouch_beyond.fieldx, ctouch_beyond.fieldy)
    ckingfield.list_all_field_touches(color, ctouch_beyond.supporter_beyond, ctouch_beyond.attacker_beyond)

    cpawnfield = pawnfield.cPawnField(match, ctouch_beyond.fieldx, ctouch_beyond.fieldy)
    cpawnfield.list_all_field_touches(color, ctouch_beyond.supporter_beyond, ctouch_beyond.attacker_beyond)

    return


def list_field_touches(match, color, fieldx, fieldy):
    touches = []

    crookfield = rookfield.cRookField(match, fieldx, fieldy)
    newtouches = crookfield.list_field_touches(color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    cbishopfield = bishopfield.cBishopField(match, fieldx, fieldy)
    newtouches = cbishopfield.list_field_touches(color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    cknightfield = knightfield.cKnightField(match, fieldx, fieldy)
    newtouches = cknightfield.list_field_touches(color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    ckingfield = kingfield.cKingField(match, fieldx, fieldy)
    newtouches = ckingfield.list_field_touches(color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    cpawnfield = pawnfield.cPawnField(match, fieldx, fieldy)
    newtouches = cpawnfield.list_field_touches(color)
    if(len(newtouches) > 0):
        touches.extend(newtouches)

    return touches


def piece_is_lower_equal_than_captured(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    
    if(piece == match.PIECES['wPw'] or piece == match.PIECES['bPw']):
        return True

    captured_piece = match.readfield(gmove.dstx, gmove.dsty)
    if(match.PIECES_RANK[piece] <= match.PIECES_RANK[captured_piece]):
        return True
    else:
        return False


def srcfield_is_supported(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    return match.is_field_touched(match.color_of_piece(piece), gmove.srcx, gmove.srcy, 0)


def piece_is_lower_equal_than_enemy_on_srcfield(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    enemies = list_field_touches(match, match.oppcolor_of_piece(piece), gmove.srcx, gmove.srcy)

    for enemy in enemies:
        if(match.PIECES_RANK[piece] > match.PIECES_RANK[enemy.piece]):
            return False

    return True
    

def srcfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    
    match.writefield(gmove.srcx, gmove.srcy, match.PIECES['blk'])

    frdlytouches, enmytouches = list_all_field_touches(match, match.color_of_piece(piece), gmove.srcx, gmove.srcy)
    
    match.writefield(gmove.srcx, gmove.srcy, piece)

    return len(frdlytouches) >= len(enmytouches)


def piece_is_lower_equal_than_enemy_on_dstfield(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)

    match.writefield(gmove.srcx, gmove.srcy, match.PIECES['blk'])

    enemies = list_field_touches(match, match.oppcolor_of_piece(piece), gmove.dstx, gmove.dsty)

    match.writefield(gmove.srcx, gmove.srcy, piece)

    for enemy in enemies:
        if(match.PIECES_RANK[piece] > match.PIECES_RANK[enemy.piece]):
            return False

    return True


def piece_is_lower_fairy_equal_than_enemy_on_dstfield(match, gmove):
    flag = True

    piece = match.readfield(gmove.srcx, gmove.srcy)

    match.writefield(gmove.srcx, gmove.srcy, match.PIECES['blk'])

    enemies = list_field_touches(match, match.oppcolor_of_piece(piece), gmove.dstx, gmove.dsty)
    for enemy in enemies:
        if(match.PIECES_RANK[piece] > match.PIECES_RANK[enemy.piece]):
            if(match.PIECES_RANK[enemy.piece] == match.PIECES_RANK[match.PIECES['wPw']]):
                flag = False
                break
            if(match.PIECES_RANK[piece] == match.PIECES_RANK[match.PIECES['wQu']]):
                flag = False
                break

    match.writefield(gmove.srcx, gmove.srcy, piece)

    return flag


def dstfield_is_supported(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    
    match.writefield(gmove.srcx, gmove.srcy, match.PIECES['blk'])    

    is_touched = match.is_field_touched(match.color_of_piece(piece), gmove.dstx, gmove.dsty, 0)

    match.writefield(gmove.srcx, gmove.srcy, piece)
    
    return is_touched


def dstfield_is_attacked(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    
    match.writefield(gmove.srcx, gmove.srcy, match.PIECES['blk'])    

    is_touched = match.is_field_touched( match.oppcolor_of_piece(piece), gmove.dstx, gmove.dsty, 0)

    match.writefield(gmove.srcx, gmove.srcy, piece)

    return is_touched


def dstfield_count_of_supporter_is_equal_or_higher_than_count_of_attacker(match, gmove):
    piece = match.readfield(gmove.srcx, gmove.srcy)
    
    match.writefield(gmove.srcx, gmove.srcy, match.PIECES['blk'])

    frdlytouches, enmytouches = list_all_field_touches(match, match.color_of_piece(piece), gmove.dstx, gmove.dsty)

    match.writefield(gmove.srcx, gmove.srcy, piece)

    return len(frdlytouches) >= len(enmytouches)


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
            return True

    return False


def is_discl_supported_weak(discl_supported):
    if(len(discl_supported) == 0):
        return False

    for ctouch_beyond in discl_supported:
        if(len(ctouch_beyond.attacker_beyond) > len(ctouch_beyond.supporter_beyond)):
            return True

    return False

def is_fork_field(match, color, forkx, forky):
    opp_color = match.REVERSED_COLORS[color]

    frdlytouches, enmytouches = list_all_field_touches(match, color, forkx, forky)
    if(len(frdlytouches) >= len(enmytouches)):
        return False

    #cqueenfield = queenfield.cQueenField(match, forkx, forky)
    #if(cqueenfield.is_field_touched(opp_color, 2)):
        #if(cqueenfield.count_touches(color) > 1):
            #return True

    crookfield = rookfield.cRookField(match, forkx, forky)
    if(crookfield.is_field_touched(opp_color, 2)):
        if(crookfield.count_touches(color) > 1):
            return True

    cbishopfield = bishopfield.cBishopField(match, forkx, forky)
    if(cbishopfield.is_field_touched(opp_color, 2)):
        if(cbishopfield.count_touches(color) > 1):
            return True

    cknightfield = knightfield.cKnightField(match, forkx, forky)
    if(cknightfield.is_field_touched(opp_color, 2)):
        if(cknightfield.count_touches(color) > 1):
            return True

    cpawnfield = pawnfield.cPawnField(match, forkx, forky)
    if(cpawnfield.is_field_touched(opp_color, 2)):
        if(cpawnfield.count_touches(color) > 1):
            return True

    ckingfield = kingfield.cKingField(match, forkx, forky)
    if(ckingfield.is_field_touched(opp_color)):
        if(ckingfield.count_touches(color) > 1):
            return True

    return False


def is_piece_attacked(lst, piece1, piece2):
    for ctouch_beyond in lst:
        if(ctouch_beyond.piece == piece1 or ctouch_beyond.piece == piece2):
            return True

    return False


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
        pindir = match.evaluate_pin_dir(ctouch_beyond.fieldx, ctouch_beyond.fieldy)
        if(pindir != match.DIRS['undefined']):
            return True

    return False


def is_attacked_soft_pinned(match, attacked):
    if(len(attacked) == 0):
        return False

    for ctouch_beyond in attacked:
        if(match.is_soft_pin(ctouch_beyond.fieldx, ctouch_beyond.fieldy)):
            return True

    return False


def is_attacked_higher_than_piece(match, attacked):
    for ctouch_beyond in attacked:
        piece = match.readfield(ctouch_beyond.agent_srcx, ctouch_beyond.agent_srcy)
        if(match.PIECES_RANK[ctouch_beyond.piece] > match.PIECES_RANK[piece]):
            return True

    return False


def is_attacked_higher_equal_than_piece(match, attacked):
    for ctouch_beyond in attacked:
        piece = match.readfield(ctouch_beyond.agent_srcx, ctouch_beyond.agent_srcy)

        if(match.PIECES_RANK[ctouch_beyond.piece] >= match.PIECES_RANK[piece]):
            return True

    return False


def is_supported_weak(match, supported):
    if(len(supported) == 0):
        return False

    for ctouch_beyond in supported:
        if(len(ctouch_beyond.attacker_beyond) > len(ctouch_beyond.supporter_beyond)):
            return True
        elif(match.is_soft_pin(ctouch_beyond.fieldx, ctouch_beyond.fieldy)):
            return True

    return False


def is_supported_attacked(supported):
    if(len(supported) == 0):
        return False

    for ctouch_beyond in supported:
        if(len(ctouch_beyond.attacker_beyond) > 0):
            return True

    return False


def is_supported_lower_equal_than_attacker(match, supported):
    if(len(supported) == 0):
        return False

    for ctouch_beyond in supported:
        for attacker_beyond in ctouch_beyond.attacker_beyond:
            if(match.PIECES_RANK[ctouch_beyond.piece] > match.PIECES_RANK[attacker_beyond.piece]):
                return False

    return True

