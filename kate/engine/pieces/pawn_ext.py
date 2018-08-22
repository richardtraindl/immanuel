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

