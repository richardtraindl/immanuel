from .bishop import cBishop
from .piece import cTouch, cTouchBeyond
from .. import analyze_helper


STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]

def is_move_stuck(match, srcx, srcy, dstx, dsty):
    cbishop = cBishop(match, srcx, srcy)
    return cbishop.is_move_stuck(dstx, dsty)

def score_attacks(match, srcx, srcy):
    score = 0

    bishop = match.readfield(srcx, srcy)

    color = match.color_of_piece(bishop)
    opp_color = match.oppcolor_of_piece(bishop)

    frdlytouches, enmytouches = analyze_helper.field_touches(match, color, srcx, srcy)
    if(len(frdlytouches) < len(enmytouches)):
        return score

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = match.search(srcx, srcy, stepx, stepy)
        if(x1 != match.UNDEF_X):
            if(is_move_stuck(match, srcx, srcy, x1, y1)):
                continue

            frdlytouches, enmytouches = analyze_helper.field_touches(match, color, x1, y1)
            #if(len(frdlytouches) < len(enmytouches)):
                #continue

            piece = match.readfield(x1, y1)

            if(match.color_of_piece(piece) == opp_color):
                if(len(enmytouches) == 0 or match.PIECES_RANK[bishop] <= match.PIECES_RANK[piece]):
                    score += match.ATTACKED_SCORES[piece]

                # score if attacked is pinned
                direction = cBishop.dir_for_move(srcx, srcy, x1, y1)
                enmy_pin = self.match.evaluate_pin_dir(x1, y1) #opp_color, 
                if(enmy_pin != match.DIRS['undefined']):
                    if(enmy_pin != direction and enmy_pin != match.REVERSE_DIRS[direction]):
                        score += match.ATTACKED_SCORES[piece]
                    else:
                        if(piece != match.PIECES['wBp'] and piece != match.PIECES['bBp'] and
                           piece != match.PIECES['wPw'] and piece != match.PIECES['bPw']):
                            score += match.ATTACKED_SCORES[piece]

                if(match.is_soft_pin(x1, y1)):
                    score += match.ATTACKED_SCORES[piece]

    return score


def score_supports(match, srcx, srcy):
    score = 0

    bishop = match.readfield(srcx, srcy)

    color = match.color_of_piece(bishop)
    opp_color = match.oppcolor_of_piece(bishop)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = match.search(srcx, srcy, stepx, stepy)
        if(x1 != match.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue

            if(is_move_stuck(match, srcx, srcy, x1, y1, 1)):
                continue

            piece = match.readfield(x1, y1)

            if(match.color_of_piece(piece) == color):
                if(match.is_field_touched(opp_color, x1, y1, 1)):
                    score += match.SUPPORTED_SCORES[piece]

    return score 


def count_touches(match, color, fieldx, fieldy):
    count = 0

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = match.search(fieldx, fieldy, stepx, stepy)
        if(x1 != match.UNDEF_X):
            if(is_move_stuck(match, fieldx, fieldy, x1, y1)):
                continue

            piece = match.readfield(x1, y1)
            if(piece == match.PIECES['blk']):
                continue
            elif(match.color_of_piece(piece) == color):
                if(match.is_field_touched(color, x1, y1, 1) == False):
                    count += 1
                elif(match.PIECES_RANK[piece] > match.PIECES_RANK[match.PIECES['wBp']]):
                    count += 1
            """else:
                count -= 1"""

    return count

