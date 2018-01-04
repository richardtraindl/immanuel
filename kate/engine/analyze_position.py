from .match import *
from .rules import RETURN_CODES, game_status, is_move_inbounds
from .pieces import pawn, knight, bishop, rook, king 
from .cvalues import *


def score_attacks(match, srcx, srcy):
    score = 0

    score += rook.score_attacks(match, srcx, srcy)

    score += knight.score_attacks(match, srcx, srcy)

    score += bishop.score_attacks(match, srcx, srcy)

    score += king.score_attacks(match, srcx, srcy)

    score += pawn.score_attacks(match, srcx, srcy)

    return score


def score_supports(match, srcx, srcy):
    score = 0
    
    score += rook.score_supports(match, srcx, srcy)

    score += bishop.score_supports(match, srcx, srcy)

    score += knight.score_supports(match, srcx, srcy)

    score += king.score_supports(match, srcx, srcy)

    score += pawn.score_supports(match, srcx, srcy)

    return score


def score_supports_and_attacks(match):
    score = 0

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
                score += score_supports(match, x, y)
                score += score_attacks(match, x, y)

    return score


def check_mobility_move(match, srcx, srcy, dstx, dsty, prom_piece):
    if(not is_move_inbounds(srcx, srcy, dstx, dsty)):
        return False

    piece = match.readfield(srcx, srcy)

    if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
        if(pawn.is_move_valid(match, srcx, srcy, dstx, dsty, piece, prom_piece)):
            return True
        else:
            return False
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        if(rook.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True
        else:
            return False
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        if(knight.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True
        else:
            return False
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        if(bishop.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True
        else:
            return False
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        if(queen.is_move_valid(match, srcx, srcy, dstx, dsty, piece)):
            return True
        else:
            return False
    else:
        return False

def count_mobility(match, srcx, srcy, excludedpieces):
    piece = match.readfield(srcx, srcy)
    movecnt = 0

    for expiece in excludedpieces:
        if(piece == expiece):
            return movecnt

    if(piece == PIECES['wKg'] or piece == PIECES['bKg']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 8
        stepcnt = 1
    elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 8
        stepcnt = 7
    elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
        dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
        dircnt = 4
        stepcnt = 7
    elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
        dirs = [ [1, 1], [-1, -1], [-1, 1], [1, -1] ]
        dircnt = 4
        stepcnt = 7
    elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
        dirs =  [ [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2] ]
        dircnt = 8
        stepcnt = 1
    else:
        return movecnt

    for j in range(dircnt):
        stepx = dirs[j][0]
        stepy = dirs[j][1]
        dstx = srcx
        dsty = srcy
        for i in range(stepcnt):
            dstx += stepx
            dsty += stepy
            if(check_mobility_move(match, srcx, srcy, dstx, dsty, PIECES['blk'])):
                movecnt += 1
            else:
                break

    return movecnt

def count_all_moves(match, color, excludedpieces):
    movecnt = 0

    for y1 in range(8):
        for x1 in range(8):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == color):
                count = count_mobility(match, x1, y1, excludedpieces)
                movecnt += count

    return movecnt

def is_king_defended_by_pawns(match, color):
    if(color == COLORS['white']):
        y = 1
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
        pawn = PIECES['wPw']
    else:
        y= 6
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y
        pawn = PIECES['bPw']
    
    count = 0
    for x in range(8):
        if(x == Kg_x or x - 1 == Kg_x or x + 1 == Kg_x):
            if(match.readfield(x, y) == pawn):
                count += 1

    if(count >= 2):
        return True
    else:
        return False

def is_rook_over_king(match, color):
    if(color == COLORS['white']):
        y = 0
        Kg_x = match.wKg_x
        Kg_y = match.wKg_y
        king = PIECES['wKg']
        rook = PIECES['wRk']
    else:
        y= 7
        Kg_x = match.bKg_x
        Kg_y = match.bKg_y
        king = PIECES['bKg']
        rook = PIECES['bRk']

    rleftcnt = 0
    rrightcnt = 0
    pleftcnt = 0
    prightcnt = 0
    if(Kg_x > 0):
        for x in range(0, Kg_x, 1):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            elif(piece == rook):
                rleftcnt += 1
            else:
                pleftcnt += 1

    if(Kg_x < 7):
        for x in range(Kg_x + 1, 8, 1):
            piece = match.readfield(x, y)

            if(piece == PIECES['blk']):
                continue
            elif(piece == rook):
                rrightcnt += 1
            else:
                prightcnt += 1

    if(rleftcnt == 2 or rrightcnt == 2 or 
       ((pleftcnt == 0 or prightcnt == 0) and 
        (Kg_x == 0 or Kg_x == 1 or Kg_x == 2 or Kg_x == 5 or Kg_x == 6 or Kg_x == 7)) ):
        return True
    else:
        return False

def score_opening(match):
    value = 0

    whiterate = ATTACKED_SCORES[PIECES['bPw']] // 2
    
    blackrate = ATTACKED_SCORES[PIECES['wPw']] // 2

    # white position
    y = 0
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == PIECES['wKn'] or piece == PIECES['wBp']):
            value += blackrate

    for y in range(2, 4):
        for x in range(2, 5):
            piece = match.readfield(x, y)
            if(piece == PIECES['wPw']):
                value += whiterate

    piece = match.readfield(1, 2)
    if(piece == PIECES['wPw']):
        value += whiterate
    piece = match.readfield(6, 2)
    if(piece == PIECES['wPw']):
        value += whiterate

    # black position
    y = 7
    for x in range(8):
        piece = match.readfield(x, y)
        if(piece == PIECES['bKn'] or piece == PIECES['bBp']):
            value += whiterate

    for y in range(5, 3, -1):
        for x in range(2, 5):
            piece = match.readfield(x, y)
            if(piece == PIECES['bPw']):
                value += blackrate

    piece = match.readfield(1, 5)
    if(piece == PIECES['bPw']):
        value += blackrate
    piece = match.readfield(6, 5)
    if(piece == PIECES['bPw']):
        value += blackrate


    # white king
    if(is_king_defended_by_pawns(match, COLORS['white'])):
        value += whiterate

    if(is_rook_over_king(match, COLORS['white'])):
        value += whiterate

    # black king
    if(is_king_defended_by_pawns(match, COLORS['black'])):
        value += blackrate

    if(is_rook_over_king(match, COLORS['black'])):
        value += blackrate

    return value


def score_endgame(match):
    value = 0

    whiterate = ATTACKED_SCORES[PIECES['bPw']]
    whitesteprate = whiterate / 2

    blackrate = ATTACKED_SCORES[PIECES['wPw']]
    blacksteprate = blackrate / 2

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == PIECES['wPw']):
                if(pawn.is_running(match, x, y)):
                    value += whiterate
                    value += whitesteprate * y
            elif(piece == PIECES['bPw']):
                if(pawn.is_running(match, x, y)):
                    value += blackrate
                    value += blacksteprate * (7 - y)

    return value


def score_position(match, movecnt):
    status = game_status(match)
    if(movecnt == 0 and status != STATUS['open']):
        if(status == STATUS['winner_black']):
            return ( SCORES[PIECES['wKg']] + match.count )
        elif(status == STATUS['winner_white']):
            return ( SCORES[PIECES['bKg']] - match.count )
        else: # draw
            return SCORES[PIECES['blk']]
    else:
        value = match.score

        value += score_supports_and_attacks(match)

        if(match.count < 30):
            value += score_opening(match)

        if(match.count >= 30):
            value += score_endgame(match)

        return value

