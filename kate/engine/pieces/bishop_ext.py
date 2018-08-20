from .bishop import cBishop
from .piece import cTouch, cTouchBeyond
from .. import analyze_helper


STEPS = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]

def is_move_stuck(match, srcx, srcy, dstx, dsty):
    cbishop = cBishop(match, srcx, srcy)
    return cbishop.is_move_stuck(dstx, dsty)

  
def disclosures(match, color, excluded_dir, srcx, srcy, discl_attacked, discl_supported):
    for j in range(0, 4, 2):
        first = cTouchBeyond(None, None, None, None, match.PIECES['blk'], 0, 0)
        second = cTouchBeyond(None, None, None, None, match.PIECES['blk'], 0, 0)

        for i in range(0, 2, 1):
            stepx = STEPS[j+i][0]
            stepy = STEPS[j+i][1]
            direction = cBishop.dir_for_move(srcx, srcy, (srcx + stepx), (srcy + stepy))
            if(direction == excluded_dir or direction == match.REVERSE_DIRS[excluded_dir]):
                break
            x1, y1 = match.search(srcx, srcy, stepx, stepy)
            if(x1 != match.UNDEF_X):
                piece = match.readfield(x1, y1)
                if(first.piece == match.PIECES['blk']):
                    first.piece = piece
                    first.fieldx = x1
                    first.fieldy = y1
                    continue
                elif(second.piece == match.PIECES['blk']):
                    second.piece = piece
                    second.fieldx = x1
                    second.fieldy = y1
                    if(match.color_of_piece(first.piece) != match.color_of_piece(second.piece) and 
                       first.piece != match.PIECES['blk'] and second.piece != match.PIECES['blk']):
                        if(match.color_of_piece(first.piece) == color):
                            if(first.piece == match.PIECES['wBp'] or first.piece == match.PIECES['bBp'] or 
                               first.piece == match.PIECES['wQu'] or first.piece == match.PIECES['bQu']):
                                discl_attacked.append(second)
                        else:
                            if(second.piece == match.PIECES['wBp'] or second.piece == match.PIECES['bBp'] or 
                               second.piece == match.PIECES['wQu'] or second.piece == match.PIECES['bQu']):
                                discl_attacked.append(first)
                    elif(match.color_of_piece(first.piece) == match.color_of_piece(second.piece) and 
                         match.color_of_piece(first.piece) == color and
                         first.piece != match.PIECES['blk'] and second.piece != match.PIECES['blk']):
                        if(first.piece == match.PIECES['wBp'] or first.piece == match.PIECES['bBp'] or 
                           first.piece == match.PIECES['wQu'] or first.piece == match.PIECES['bQu']):
                            discl_supported.append(second)
                        elif(second.piece == match.PIECES['wBp'] or second.piece == match.PIECES['bBp'] or 
                             second.piece == match.PIECES['wQu'] or second.piece == match.PIECES['bQu']):
                            discl_supported.append(first)
                    else:
                        break
                else:
                    break


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


def defends_fork_field(match, piece, srcx, srcy, dstx, dsty): #, analyses
    if(is_move_stuck(match, srcx, srcy, dstx, dsty)):
        return False

    color = match.color_of_piece(piece)
    opp_color = match.oppcolor_of_piece(piece)

    direction = cBishop.dir_for_move(srcx, srcy, dstx, dsty)
    if(direction == match.DIRS['north-east'] or direction == match.DIRS['south-west']):
        BP_STEPS = [ [1, 1], [-1, -1] ]
    else:
        BP_STEPS = [ [-1, 1], [1, -1] ]

    for i in range(2):
        stepx = BP_STEPS[i][0]
        stepy = BP_STEPS[i][1]

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

    move_dir = cBishop.dir_for_move(srcx, srcy, dstx, dsty)

    move_opp_dir = match.REVERSE_DIRS[move_dir]
    
    for i in range(4):
        stepx = STEPS[i][0]
        stepy = STEPS[i][1]

        direction = cBishop.dir_for_move(dstx, dsty, dstx + stepx, dsty + stepy)
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

