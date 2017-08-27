from .match import *
from .rules import RETURN_CODES, is_move_valid, game_status
from . import analyze_move
from .pieces import pawn, knight, bishop, rook, king 
from .cvalues import *


A1 = [0, 0]
B1 = [1, 0]
C1 = [2, 0]
D1 = [3, 0]
F1 = [5, 0]
G1 = [6, 0]
H1 = [7, 0]
A2 = [0, 1]
A3 = [0, 2]
B2 = [1, 1]
B3 = [1, 2]
C2 = [2, 1]
F2 = [5, 1]
G2 = [6, 1]
G3 = [6, 2]
H2 = [7, 1]
H3 = [7, 2]

A8 = [0, 7]
B8 = [1, 7]
C8 = [2, 7]
D8 = [3, 7]
F8 = [5, 7]
G8 = [6, 7]
H8 = [7, 7]
A7 = [0, 6]
A6 = [0, 5]
B7 = [1, 6]
B6 = [1, 5]
C7 = [2, 6]
F7 = [5, 6]
G7 = [6, 6]
G6 = [6, 5]
H7 = [7, 6]
H6 = [7, 5]


def score_attacks(match, srcx, srcy):
    score = 0

    score += rook.score_attacks(match, srcx, srcy)

    score += knight.score_attacks(match, srcx, srcy)

    score += bishop.score_attacks(match, srcx, srcy)

    score += king.score_attacks(match, srcx, srcy)

    score += pawn.score_attacks(match, srcx, srcy)

    return score


def score_supports_of_attacked(match, srcx, srcy):
    score = 0
    
    score += rook.score_supports_of_attacked(match, srcx, srcy)

    score += bishop.score_supports_of_attacked(match, srcx, srcy)

    score += knight.score_supports_of_attacked(match, srcx, srcy)

    score += king.score_supports_of_attacked(match, srcx, srcy)

    score += pawn.score_supports_of_attacked(match, srcx, srcy)

    return score


def score_contacts(match, color):
    supported = 0
    attacked = 0

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == color):
                supported += score_supports_of_attacked(match, x, y)
                attacked += score_attacks(match, x, y)

    return (supported + attacked)


def count_piece_moves(match, srcx, srcy, excludedpieces):
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

def count_all_moves(match, color, excludedpieces):
    movecnt = 0

    for y1 in range(8):
        for x1 in range(8):
            piece = match.readfield(x1, y1)
            if(Match.color_of_piece(piece) == color):
                count = count_piece_moves(match, x1, y1, excludedpieces)
                movecnt += count

    return movecnt


def score_development(match, color):
    value = 0

    if(color == COLORS['white']):
        if(match.readfield(F1[0], F1[1]) == PIECES['wKg'] or 
           match.readfield(G1[0], G1[1]) == PIECES['wKg'] or 
           match.readfield(H1[0], H1[1]) == PIECES['wKg'] and 
           match.readfield(H1[0], H1[1]) != PIECES['wRk'] and
           match.readfield(G1[0], G1[1]) != PIECES['wRk']):
            if((match.readfield(G2[0], G2[1]) == PIECES['wPw'] or
                match.readfield(G3[0], G3[1]) == PIECES['wPw']) and
               (match.readfield(H2[0], H2[1]) == PIECES['wPw'] or
                match.readfield(H3[0], H3[1]) == PIECES['wPw'])):
                value = SCORES[PIECES['bPw']] // 4

        elif(match.readfield(D1[0], D1[1]) == PIECES['wKg'] or
             match.readfield(C1[0], C1[1]) == PIECES['wKg'] or
             match.readfield(B1[0], B1[1]) == PIECES['wKg'] or
             match.readfield(A1[0], A1[1]) == PIECES['wKg'] and
             match.readfield(A1[0], A1[1]) != PIECES['wRk'] and
             match.readfield(B1[0], B1[1]) != PIECES['wRk'] and
             match.readfield(C1[0], C1[1]) != PIECES['wRk']):
            if(match.readfield(C2[0], C2[1]) == PIECES['wPw'] and 
               (match.readfield(B2[0], B2[1]) == PIECES['wPw'] or
                match.readfield(B3[0], B3[1]) == PIECES['wPw']) and 
               (match.readfield(A2[0], A2[1]) == PIECES['wPw'] or
                match.readfield(A3[0], A3[1]) == PIECES['wPw'])):
                value = SCORES[PIECES['bPw']] // 4

        excludedpieces = [ PIECES['wKg'], PIECES['wQu']]
        movecnt = count_all_moves(match, COLORS['white'], excludedpieces)
        
        value += (movecnt * SCORES[PIECES['bPw']] // 4)

        return value

    else:
        if(match.readfield(F8[0], F8[1]) == PIECES['bKg'] or 
           match.readfield(G8[0], G8[1]) == PIECES['bKg'] or 
           match.readfield(H8[0], H8[1]) == PIECES['bKg'] and 
           match.readfield(H8[0], H8[1]) != PIECES['bRk'] and
           match.readfield(G8[0], G8[1]) != PIECES['bRk']):
            if((match.readfield(G7[0], G7[1]) == PIECES['bPw'] or
                match.readfield(G6[0], G6[1]) == PIECES['bPw']) and
               (match.readfield(H7[0], H7[1]) == PIECES['bPw'] or
                match.readfield(H6[0], H6[1]) == PIECES['bPw'])):
                value = SCORES[PIECES['wPw']] // 4

        elif(match.readfield(D8[0], D8[1]) == PIECES['bKg'] or
             match.readfield(C8[0], C8[1]) == PIECES['bKg'] or
             match.readfield(B8[0], B8[1]) == PIECES['bKg'] or
             match.readfield(A8[0], A8[1]) == PIECES['bKg'] and
             match.readfield(A8[0], A8[1]) != PIECES['bRk'] and
             match.readfield(B8[0], B8[1]) != PIECES['bRk'] and
             match.readfield(C8[0], C8[1]) != PIECES['bRk']):
            if(match.readfield(C7[0], C7[1]) == PIECES['bPw'] and 
               (match.readfield(B7[0], B7[1]) == PIECES['bPw'] or
                match.readfield(B6[0], B6[1]) == PIECES['bPw']) and 
               (match.readfield(A7[0], A7[1]) == PIECES['bPw'] or
                match.readfield(A6[0], A6[1]) == PIECES['bPw'])):
                value = SCORES[PIECES['wPw']] // 4

        excludedpieces = [ PIECES['bKg'], PIECES['bQu'] ]
        movecnt = count_all_moves(match, COLORS['black'], excludedpieces)    
        
        value += (movecnt * SCORES[PIECES['wPw']] // 4)

        return value


def score_endgame(match, color):
    value = 0

    for y in range(0, 8, 1):
        for x in range(0, 8, 1):
            piece = match.readfield(x, y)
            if(Match.color_of_piece(piece) == color and piece == PIECES['wPw']):
                if(is_running(match, x, y)):
                    value += REVERSED_SCORES[piece] // 2
                    if(y >= 4):
                        value += REVERSED_SCORES[piece]
            elif(Match.color_of_piece(piece) == color and piece == PIECES['bPw']):
                if(is_running(match, x, y)):
                    value += REVERSED_SCORES[piece] // 2
                    if(y <= 3):
                        value += REVERSED_SCORES[piece]

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

        value += score_contacts(match, COLORS['white'])
        value += score_contacts(match, COLORS['black'])

        if(match.count < 40):
            value += score_development(match, COLORS['white'])
            value += score_development(match, COLORS['black'])

        if(match.count > 50):
            value += score_endgame(match, COLORS['white'])
            value += score_endgame(match, COLORS['black'])

        return value


