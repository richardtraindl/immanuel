from .values import *
from .match import *
from .pieces.pawn import cPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .pieces import pawnfield, knightfield, rookfield, bishopfield, kingfield
from .pieces.piece import cTouch
from .validator import *


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

    oppcolor = REVERSED_COLORS[color]
    
    DIRS = [match.DIRS['north'], match.DIRS['south'], match.DIRS['east'], match.DIRS['west'], match.DIRS['north-east'], match.DIRS['south-west'], match.DIRS['north-west'], match.DIRS['south-east']]
 
    for i in range(8):
        dirtouches = search_dir(match, fieldx, fieldy, DIRS[i], exclx, excly)

        if(len(dirtouches) < 2):
            continue

        if(match.color_of_piece(dirtouches[0].piece) == color and 
           match.color_of_piece(dirtouches[1].piece) == oppcolor and
           PIECES_RANK[piece] > PIECES_RANK[dirtouches[0].piece] and 
           PIECES_RANK[piece] > PIECES_RANK[dirtouches[1].piece]):

            if(dirtouches[1].piece == PIECES['wQu'] or dirtouches[1].piece == PIECES['bQu']):
                pinlines.append([dirtouches[0], dirtouches[1]])

            elif(i < 4 and (dirtouches[1].piece == PIECES['wRk'] or dirtouches[1].piece == PIECES['bRk'])): 
                pinlines.append([dirtouches[0], dirtouches[1]])

            elif(i >= 4 and (dirtouches[1].piece == PIECES['wBp'] or dirtouches[1].piece == PIECES['bBp'])):
                pinlines.append([dirtouches[0], dirtouches[1]])

    return pinlines


def search_opposed_pieces(match, color, fieldx, fieldy, excl_fieldx, excl_fieldy):
    oppenents = []

    MAX_STEP_IDX_FOR_RK = 3
    
    oppcolor = REVERSED_COLORS[color]

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
                        if(piece == PIECES['wQu'] or piece == PIECES['bQu'] or
                          (i+k <= MAX_STEP_IDX_FOR_RK and (piece == PIECES['wRk'] or piece == PIECES['bRk'])) or
                          (i+k > MAX_STEP_IDX_FOR_RK and (piece == PIECES['wBp'] or piece == PIECES['bBp']))):
                            touches[1] = cTouch(piece, x1, y1)

        if(touches[0] and touches[1]):
            oppenents.append(touches)

    return oppenents


def is_piece_stuck(match, srcx, srcy):
    piece = match.readfield(srcx, srcy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        cpawn = cPawn(match, srcx, srcy)
        return cpawn.is_piece_stuck()
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        cknight = cKnight(match, srcx, srcy)
        return cknight.is_piece_stuck()
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        cbishop = cBishop(match, srcx, srcy)
        return cbishop.is_piece_stuck()
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        crook = cRook(match, srcx, srcy)
        return crook.is_piece_stuck()
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        cqueen = cQueen(match, srcx, srcy)
        return cqueen.is_piece_stuck()
    else:
        cking = cKing(match, srcx, srcy)
        return cking.is_piece_stuck()


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


def list_field_touches_beyond(match, color, ctouch_beyond):
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


def is_fork_field(match, color, forkx, forky, excludes):
    opp_color = REVERSED_COLORS[color]
    crookfield = rookfield.cRookField(match, forkx, forky)
    if(crookfield.is_field_touched(opp_color, 2)):
        if(crookfield.count_touches(color, excludes) > 1):
            return True
    cbishopfield = bishopfield.cBishopField(match, forkx, forky)
    if(cbishopfield.is_field_touched(opp_color, 2)):
        if(cbishopfield.count_touches(color, excludes) > 1):
            return True
    cknightfield = knightfield.cKnightField(match, forkx, forky)
    if(cknightfield.is_field_touched(opp_color, 2)):
        if(cknightfield.count_touches(color, excludes) > 1):
            return True
    cpawnfield = pawnfield.cPawnField(match, forkx, forky)
    if(cpawnfield.is_field_touched(opp_color, 2)):
        if(cpawnfield.count_touches(color, excludes) > 1):
            return True
    ckingfield = kingfield.cKingField(match, forkx, forky)
    if(ckingfield.is_field_touched(opp_color)):
        if(ckingfield.count_touches(color, excludes) > 1):
            return True
    return False


def is_piece_le_attacker_on_srcfield(gmove, enmytouches_on_srcfield):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    for enmy in enmytouches_on_srcfield:
        if(PIECES_RANK[piece] > PIECES_RANK[enmy.piece]):
            return False
    return True


def is_piece_le_attacker_on_dstfield(gmove, enmytouches_on_dstfield):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    for enmy in enmytouches_on_dstfield:
        if(PIECES_RANK[piece] > PIECES_RANK[enmy.piece]):
            return False
    return True


def is_piece_lfe_attacker_on_dstfield(gmove, enmytouches_on_dstfield):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    for enmy in enmytouches_on_dstfield:
        if(PIECES_RANK[piece] > PIECES_RANK[enmy.piece]):
            if(PIECES_RANK[piece] == PIECES_RANK[PIECES['wQu']]):
                return False
            if(PIECES_RANK[enmy.piece] == PIECES_RANK[PIECES['wPw']]):
                return False
    return True


def is_supported_weak(gmove, supported):
    gmove.match.do_move(gmove.srcx, gmove.srcy, gmove.dstx, gmove.dsty, gmove.prom_piece)
    supported_weak = len(supported.attacker_beyond) > len(supported.supporter_beyond) or \
                     gmove.match.is_soft_pin(supported.fieldx, supported.fieldy)
    gmove.match.undo_move()
    return supported_weak


def is_supported_le_attacker(from_dstfield_supported):
    for supported in from_dstfield_supported:
        for attacker_beyond in supported.attacker_beyond:
            if(PIECES_RANK[supported.piece] > PIECES_RANK[attacker_beyond.piece]):
                return False
    return True


def is_discl_supported_weak(discl_supported):
    for ctouch_beyond in discl_supported:
        if(len(ctouch_beyond.attacker_beyond) > len(ctouch_beyond.supporter_beyond)):
            return True
    return False


def is_discl_attacked_supported(discl_attacked):
    for ctouch_beyond in discl_attacked:
        if(len(ctouch_beyond.supporter_beyond) > 0):
            return True
    return False


def is_supported_running_pawn(match, supported):
    if(match.is_endgame() == False):
        return False
    if(supported.piece == PIECES['wPw'] or supported.piece == PIECES['bPw']):
        cpawn = cPawn(match, supported.fieldx, supported.fieldy)
        if(cpawn.is_running()):
            return True
    return False


def is_captured_pinned_or_soft_pinned(gmove):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    if(piece != PIECES['wKg'] and piece != PIECES['bKg']):
        gmove.match.writefield(gmove.srcx, gmove.srcy, PIECES['blk'])
    is_soft_pin, pinning_piece = cValidator.is_soft_pin(gmove.match, gmove.dstx, gmove.dsty)
    gmove.match.writefield(gmove.srcx, gmove.srcy, piece)
    if(is_soft_pin and 
       (pinning_piece.fieldx != gmove.srcx or pinning_piece.fieldy != gmove.srcy)):
        return True
    else:
        return False


def is_attacked_soft_pinned(gmove, attacked):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    if(piece != PIECES['wKg'] and piece != PIECES['bKg']):
        gmove.match.writefield(gmove.srcx, gmove.srcy, PIECES['blk'])
    is_soft_pinned = gmove.match.is_soft_pin(attacked.fieldx, attacked.fieldy)
    gmove.match.writefield(gmove.srcx, gmove.srcy, piece)
    return is_soft_pinned


def is_piece_le_captured(gmove):
    piece = gmove.match.readfield(gmove.srcx, gmove.srcy)
    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        return True
    captured_piece = gmove.match.readfield(gmove.dstx, gmove.dsty)
    if(PIECES_RANK[piece] <= PIECES_RANK[captured_piece]):
        return True
    else:
        return False
