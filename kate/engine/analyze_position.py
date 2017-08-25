from .match import *
from .rules import RETURN_CODES, is_move_valid, game_status
from . import analyze_move
from .pieces.pawn import is_running 
from .cvalues import *


X_F = 5
X_G = 6
X_H = 7
Y_2 = 1
Y_3 = 2
Y_6 = 5
Y_7 = 6


def evaluate_contacts(match):
    supported = 0
    attacked = 0

    color = match.next_color()

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == COLORS['undefined']):
                continue

            supported += analyze_move.score_supports_of_attacked(match, x, y)

            attacked += analyze_move.score_attacks(match, x, y)

    return (supported + attacked)


def evaluate_piece_moves(match, srcx, srcy, excludedpieces):
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
            flag, errcode = is_move_valid(match, srcx, srcy, dstx, dsty, PIECES['blk'])
            if(flag):
                movecnt += 1
            elif(errcode == RETURN_CODES['out-of-bounds']):
                break

    return movecnt


def evaluate_movecnt(match, color, excludedpieces):
    movecnt = 0

    for y1 in range(8):
        for x1 in range(8):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == color):
                count = evaluate_piece_moves(match, x1, y1, excludedpieces)
                movecnt += count

    return movecnt


def evaluate_developments(match):
    developed_whites = 0
    developed_blacks = 0

    if(match.wKg_first_movecnt > 0 and (match.wKg_first_movecnt == match.wRk_a1_first_movecnt or match.wKg_first_movecnt == match.wRk_h1_first_movecnt)):
        if(match.readfield(X_F, Y_2) == PIECES['wPw'] and 
           (match.readfield(X_G, Y_2) == PIECES['wPw'] or match.readfield(X_G, Y_3) == PIECES['wPw']) and
           (match.readfield(X_H, Y_2) == PIECES['wPw'] or match.readfield(X_H, Y_3) == PIECES['wPw'])):
            developed_whites = SCORES[PIECES['bPw']] // 4
    else:
        developed_whites = SCORES[PIECES['wPw']] // 4

    if(match.bKg_first_movecnt > 0 and (match.bKg_first_movecnt == match.bRk_a8_first_movecnt or match.bKg_first_movecnt == match.bRk_h8_first_movecnt)):
        if(match.readfield(X_F, Y_7) == PIECES['bPw'] and 
           (match.readfield(X_G, Y_7) == PIECES['bPw'] or match.readfield(X_G, Y_6) == PIECES['bPw']) and
           (match.readfield(X_H, Y_7) == PIECES['bPw'] or match.readfield(X_H, Y_6) == PIECES['bPw'])):
            developed_blacks = SCORES[PIECES['wPw']] // 4
    else:
        developed_blacks = SCORES[PIECES['bPw']] // 4
        
    excludedpieces = [ PIECES['wKg'], PIECES['bKg'], PIECES['wQu'], PIECES['bQu'] ]
    whitemovecnt = evaluate_movecnt(match, COLORS['white'], excludedpieces)
    whitemovecnt = (whitemovecnt * SCORES[PIECES['bPw']] // 4)
    blackmovecnt = evaluate_movecnt(match, COLORS['black'], excludedpieces)    
    blackmovecnt = (blackmovecnt * SCORES[PIECES['wPw']] // 4)

    return developed_whites + developed_blacks + whitemovecnt + blackmovecnt


def evaluate_endgame(match):
    running = 0

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(piece == PIECES['wPw']):
                if(is_running):
                    running += REVERSED_SCORES[piece] // 2
                    if(y >= 4):
                        running += REVERSED_SCORES[piece]
            elif(piece == PIECES['bPw']):
                if(is_running):
                    running += REVERSED_SCORES[piece] // 2
                    if(y <= 3):
                        running += REVERSED_SCORES[piece]

    return running


def evaluate_position(match, movecnt):
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

        value += evaluate_contacts(match)

        if(match.count < 40):
            value += evaluate_developments(match)

        if(match.count > 50):
            value += evaluate_endgame(match)

        return value

