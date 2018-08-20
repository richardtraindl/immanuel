from .knight import cKnight
from .piece import cTouchBeyond
from .. import analyze_helper


STEPS = [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]


def is_stuck(match, srcx, srcy):
    cknight = cKnight(match, srcx, srcy)
    return cknight.is_piece_stuck_new()


def score_attacks(match, srcx, srcy):
    score = 0

    if(is_stuck(match, srcx, srcy)):
        return score

    knight = match.readfield(srcx, srcy)

    color = Match.color_of_piece(knight)
    opp_color = match.oppcolor_of_piece(knight)

    frdlytouches, enmytouches = field_touches(match, color, srcx, srcy)
    if(len(frdlytouches) < len(enmytouches)):
        return score

    for i in range(8):
        x1 = srcx + STEPS[i][0]
        y1 = srcy + STEPS[i][1]
        if(match.is_inbounds(x1, y1)):
            frdlytouches, enmytouches = field_touches(match, color, x1, y1)
            #if(len(frdlytouches) < len(enmytouches)):
                #continue

            piece = match.readfield(x1, y1)

            if(match.color_of_piece(piece) == opp_color):
                if(len(enmytouches) == 0 or match.PIECES_RANK[knight] <= match.PIECES_RANK[piece]):
                    score += match.ATTACKED_SCORES[piece]

                # extra score if attacked is pinned
                enmy_pin = match.evaluate_pin_dir(x1, y1) #opp_color, 
                if(enmy_pin != match.DIRS['undefined']):
                    score += match.ATTACKED_SCORES[piece]

                if(match.is_soft_pin(x1, y1)):
                    score += match.ATTACKED_SCORES[piece]

    return score


def score_supports(match, srcx, srcy):
    score = 0

    if(is_stuck(match, srcx, srcy)):
        return score

    knight = match.readfield(srcx, srcy)

    color = match.color_of_piece(knight)
    opp_color = match.oppcolor_of_piece(knight)

    for i in range(8):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = match.search(srcx, srcy, stepx , stepy)
        if(x1 != match.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue

            piece = match.readfield(x1, y1)

            if(piece == match.PIECES['blk']):
                continue

            if(match.color_of_piece(piece) == color):
                if(match.is_field_touched(opp_color, x1, y1, 1)):
                    score += match.SUPPORTED_SCORES[piece]

    return score 


def count_touches(match, color, fieldx, fieldy):
    count = 0

    for i in range(8):
        x1 = fieldx + STEPS[i][0]
        y1 = fieldy + STEPS[i][1]
        if(match.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(piece == match.PIECES['blk']):
                continue
            elif(match.color_of_piece(piece) == color):
                if(match.is_field_touched(color, x1, y1, 1) == False):
                    count += 1
                elif(match.PIECES_RANK[piece] > match.PIECES_RANK[match.PIECES['wKn']]):
                    count += 1
            """else:
                count -= 1"""

    return count


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty): #, analyses
    color = match.color_of_piece(piece)
    opp_color = match.oppcolor_of_piece(piece)
    
    for i in range(8):
        x1 = dstx + STEPS[i][0]
        y1 = dsty + STEPS[i][1]

        if(x1 == srcx and y1 == srcy):
            continue

        if(match.is_inbounds(x1, y1)):
            forkfield = match.readfield(x1, y1)

            if(match.color_of_piece(forkfield) == opp_color):
                continue

            if(analyze_helper.is_fork_field(match, piece, x1, y1)):
                #cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                #analyses.lst_fork_defended.append(cfork)
                return True

    return False


