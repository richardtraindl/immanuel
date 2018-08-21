from .rook import cRook
from .piece import cTouch, cTouchBeyond
from .. import analyze_helper


STEPS = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]

def is_move_stuck(match, srcx, srcy, dstx, dsty):
    crook = cRook(match, srcx, srcy)
    return crook.is_move_stuck(dstx, dsty)


def score_attacks(match, srcx, srcy):
    score = 0

    rook = match.readfield(srcx, srcy)

    color = match.color_of_piece(rook)
    opp_color = match.oppcolor_of_piece(rook)

    frdlytouches, enmytouches = field_touches(match, color, srcx, srcy)
    if(len(frdlytouches) < len(enmytouches)):
        return score

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = match.search(srcx, srcy, stepx, stepy)
        if(x1 != match.UNDEF_X):
            if(is_move_stuck(match, x1, y1, srcx, srcy)):
                continue

            frdlytouches, enmytouches = field_touches(match, color, x1, y1)
            #if(len(frdlytouches) < len(enmytouches)):
                #continue
                
            piece = match.readfield(x1, y1)

            if(match.color_of_piece(piece) == opp_color):
                if(len(enmytouches) == 0 or match.PIECES_RANK[rook] <= match.PIECES_RANK[piece]):
                    score += match.ATTACKED_SCORES[piece]

                # extra score if attacked is pinned
                direction = cRook.dir_for_move(srcx, srcy, x1, y1)
                enmy_pin = match.evaluate_pin_dir(x1, y1) #opp_color, 
                if(enmy_pin != match.DIRS['undefined']):
                    if(enmy_pin != direction and enmy_pin != match.REVERSE_DIRS[direction]):
                        score += match.ATTACKED_SCORES[piece]
                    else:
                        if(piece != match.PIECES['wRk'] and piece != match.PIECES['bRk'] and
                           piece != match.PIECES['wPw'] and piece != match.PIECES['bPw']):
                            score += match.ATTACKED_SCORES[piece]

                if(match.is_soft_pin(x1, y1)):
                    score += match.ATTACKED_SCORES[piece]

    return score


def score_supports(match, srcx, srcy):
    score = 0

    rook = match.readfield(srcx, srcy)

    color = Match.color_of_piece(rook)
    opp_color = match.oppcolor_of_piece(rook)

    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]
        x1, y1 = match.search(srcx, srcy, stepx , stepy)
        if(x1 != match.UNDEF_X):
            if(x1 == srcx and y1 == srcy):
                continue

            if(is_move_stuck(match, x1, y1, srcx, srcy)):
                continue

            piece = match.readfield(x1, y1)

            if(Match.color_of_piece(piece) == color):
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
            if(is_move_stuck(match, x1, y1, fieldx, fieldy)):
                continue

            piece = match.readfield(x1, y1)
            if(piece == match.PIECES['blk']):
                continue
            elif(match.color_of_piece(piece) == color):
                if(match.is_field_touched(color, x1, y1, 1) == False):
                    count += 1
                elif(match.PIECES_RANK[piece] > match.PIECES_RANK[match.PIECES['wRk']]):
                    count += 1
            """else:
                count -= 1"""

    return count


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty): #, analyses
    if(is_move_stuck(match, srcx, srcy, dstx, dsty)):
        return False

    color = match.color_of_piece(piece)
    opp_color = match.oppcolor_of_piece(piece)

    direction = cRook.dir_for_move(srcx, srcy, dstx, dsty)
    if(direction == match.DIRS['north'] or direction == match.DIRS['south']):
        RK_STEPS = [ [1, 0], [-1, 0] ]
    else:
        RK_STEPS = [ [0, 1], [0, -1] ]

    for i in range(2):
        stepx = RK_STEPS[i][0]
        stepy = RK_STEPS[i][1]

        x1 = dstx + stepx
        y1 = dsty + stepy
        while(match.is_inbounds(x1, y1)):
            fork_field = match.readfield(x1, y1)

            if(match.color_of_piece(fork_field) == opp_color):
                break

            if(analyze_helper.is_fork_field(match, piece, x1, y1)):
                #cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                #analyses.lst_fork_defended.append(cfork)
                return True

            if(match.color_of_piece(fork_field) == color):
                break

            x1 += stepx
            y1 += stepy

    return False


def controles_file(match, piece, color, srcx, srcy, dstx, dsty):
    cnt = 0

    move_dir = cRook.dir_for_move(srcx, srcy, dstx, dsty)

    move_opp_dir = match.REVERSE_DIRS[move_dir]
    
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]

        direction = cRook.dir_for_move(dstx, dsty, dstx + stepx, dsty + stepy)
        if(direction == move_dir or direction == move_opp_dir):
            continue

        x1 = dstx + stepx
        y1 = dsty + stepy
        while(match.is_inbounds(x1, y1)):
            piece = match.readfield(x1, y1)
            if(match.color_of_piece(piece) == color):
                break
            else:
                cnt += 1
                x1 += stepx
                y1 += stepy

    if(cnt >= 5):
        return True
    else:
        return False

