from .pawn import cPawn
from .piece import cTouchBeyond
from .. import analyze_helper


WPW_STEPS = [ [1, 1], [-1, 1] ]
WBACK_STEPS = [ [1, -1], [-1, -1] ]
BPW_STEPS = [ [1, -1], [-1, -1] ]
BBACK_STEPS = [ [1, 1], [-1, 1] ]


def is_move_stuck(match, srcx, srcy, dstx, dsty):
    cpawn = cPawn(match, srcx, srcy)
    return cpawn.is_move_stuck(dstx, dsty)


def attacks_and_supports(match, srcx, srcy, dstx, dsty, attacked, supported):
    pawn = match.readfield(srcx, srcy)

    color = match.color_of_piece(pawn)
    opp_color = match.oppcolor_of_piece(pawn)

    if(color == match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]
        if(match.is_inbounds(x1, y1)):
            if(x1 == srcx and y1 == srcy):
                continue

            piece = match.readfield(x1, y1)
            
            if(piece == match.PIECES['blk']):
                continue

            if(is_move_stuck(match, dstx, dsty, x1, y1)):
                continue

            if(match.color_of_piece(piece) == opp_color):
                ctouch_beyond = cTouchBeyond(srcx, srcy, dstx, dsty, piece, x1, y1)
                attacked.append(ctouch_beyond)

                ###
                match.writefield(srcx, srcy, match.PIECES['blk'])

                analyze_helper.field_touches_beyond(match, opp_color, ctouch_beyond)

                match.writefield(srcx, srcy, pawn)
                ###
            else:
                if(piece == match.PIECES['blk'] or piece == match.PIECES['wKg'] or piece == match.PIECES['bKg']):
                    continue

                ctouch_beyond = cTouchBeyond(srcx, srcy, dstx, dsty, piece, x1, y1)
                supported.append(ctouch_beyond)

                ###
                match.writefield(srcx, srcy, match.PIECES['blk'])

                analyze_helper.field_touches_beyond(match, color, ctouch_beyond)

                match.writefield(srcx, srcy, pawn)
                ###


def score_attacks(match, srcx, srcy):
    score = 0

    pawn = match.readfield(srcx, srcy)

    color = match.color_of_piece(pawn)
    opp_color = match.oppcolor_of_piece(pawn)

    frdlytouches, enmytouches = analyze_helper.field_touches(match, color, srcx, srcy)
    if(len(frdlytouches) < len(enmytouches)):
        return score

    if(color == match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(self.match.is_inbounds(x1, y1)):
            if(is_move_stuck(match, srcx, srcy, x1, y1)):
                continue

            frdlytouches, enmytouches = analyze_helper.field_touches(match, color, x1, y1)
            #if(len(frdlytouches) < len(enmytouches)):
                #continue

            piece = match.readfield(x1, y1)

            if(match.color_of_piece(piece) == opp_color):
                score += ATTACKED_SCORES[piece]

                # extra score if attacked is pinned
                enmy_pin = match.evaluate_pin_dir(x1, y1) #opp_color
                if(enmy_pin != cPawn.DIRS['undefined']):
                    score += ATTACKED_SCORES[piece]

                if(match.is_soft_pin(x1, y1)):
                    score += ATTACKED_SCORES[piece]

    return score


def score_supports(match, srcx, srcy):
    score = 0

    pawn = match.readfield(srcx, srcy)

    color = match.color_of_piece(pawn)
    opp_color = match.oppcolor_of_piece(pawn)

    if(color == match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(self.match.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)

            if(is_move_stuck(match, srcx, srcy, x1, y1)):
                continue

            if(match.color_of_piece(piece) == color):
                if(self.match.is_field_touched(match, opp_color, x1, y1, 1)):
                    score += SUPPORTED_SCORES[piece]

    return score


def count_touches(match, color, fieldx, fieldy):
    count = 0

    if(color == match.COLORS['white']):
        STEPS = WPW_STEPS
        pawn = match.PIECES['wPw']
    else:
        STEPS = BPW_STEPS
        pawn = match.PIECES['bPw']

    for i in range(2):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(match.is_inbounds(x1, y1)):
            if(is_move_stuck(match, fieldx, fieldy, x1, y1)):
                continue

            piece = match.readfield(x1, y1)
            if(piece == match.PIECES['blk']):
                continue
            elif(match.color_of_piece(piece) == color):
                if(match.is_field_touched(color, x1, y1, 1) == False):
                    count += 1
                elif(match.PIECES_RANK[piece] > match.PIECES_RANK[match.PIECES['wPw']]):
                    count += 1
            """else:
                count -= 1"""

    return count


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty): #, analyses
    if(is_move_stuck(match, srcx, srcy, dstx, dsty)):
        return False

    color = match.color_of_piece(piece)
    opp_color = match.oppcolor_of_piece(piece)

    if(color == match.COLORS['white']):
        STEPS = WPW_STEPS
    else:
        STEPS = BPW_STEPS

    for i in range(2):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]

        if(match.is_inbounds(x1, y1)):
            fork_field = match.readfield(x1, y1)

            if(match.color_of_piece(fork_field) == opp_color):
                continue

            if(analyze_helper.is_fork_field(match, piece, x1, y1)):
                #cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                #analyses.lst_fork_defended.append(cfork)
                return True

    return False


def is_running(match, srcx, srcy):
    piece = match.readfield(srcx, srcy)
    if(piece == match.PIECES['wPw']):
        stepx = 0
        stepy = 1
        opp_pawn = match.PIECES['bPw']
    elif(piece == match.PIECES['bPw']):
        stepx = 0
        stepy = -1
        opp_pawn = match.PIECES['wPw']
    else:
        return False

    STARTS = [0, 1, -1]
    for i in range(3):
        x1 = srcx + STARTS[i]
        y1 = srcy
        while( x1 != match.UNDEF_X and match.is_inbounds(x1, y1) ):
            x1, y1 = match.search(x1, y1, stepx, stepy)
            if(x1 != match.UNDEF_X):
                piece = match.readfield(x1, y1)
                if(piece == opp_pawn):
                    return False

    return True

