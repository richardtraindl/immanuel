from kate.engine.calc_helper import SCORES
from kate.engine.match import *
from kate.engine.move import *


def do_move(match, srcx, srcy, dstx, dsty, prom_piece):
    move = Move(match, 
                match.count + 1, 
                TYPES['standard'],
                srcx, 
                srcy, 
                dstx, 
                dsty, 
                None,
                None,
                PIECES['blk'], 
                prom_piece, 
                match.fifty_moves_count)

    srcpiece = match.readfield(srcx, srcy)
    dstpiece = match.readfield(dstx, dsty)

    if(srcpiece == PIECES['wPw'] or srcpiece == PIECES['bPw']):
        return pawn_do_move(match, move, srcpiece, dstpiece)
    elif(srcpiece == PIECES['wKg'] or srcpiece == PIECES['bKg']):
        return king_do_move(match, move, srcpiece, dstpiece)
    else:
        return generic_do_move(match, move, srcpiece, dstpiece)


def generic_do_move(match, move, srcpiece, dstpiece):
    move.move_type = TYPES['standard']
    move.captured_piece = dstpiece

    match.count += 1            
    match.writefield(move.srcx, move.srcy, PIECES['blk'])
    match.writefield(move.dstx, move.dsty, srcpiece)
    if(dstpiece != PIECES['blk']):
        match.fifty_moves_count = 0
        move.fifty_moves_count = match.fifty_moves_count
    else:
        match.fifty_moves_count += 1
        move.fifty_moves_count = match.fifty_moves_count

    if(srcpiece == PIECES['wKg']):
        match.wKg_x = move.dstx
        match.wKg_y = move.dsty
        if(match.wKg_first_movecnt == 0):
            match.wKg_first_movecnt = match.count
    elif(srcpiece == PIECES['bKg']):
        match.bKg_x = move.dstx
        match.bKg_y = move.dsty
        if(match.bKg_first_movecnt == 0):
            match.bKg_first_movecnt = match.count
    elif(srcpiece == PIECES['wRk']):
        if(move.srcx == 0 and move.srcy == 0 and match.wRk_a1_first_movecnt == 0):
            match.wRk_a1_first_movecnt = match.count
        elif(move.srcx == 7 and move.srcy == 0 and match.wRk_h1_first_movecnt == 0):
            match.wRk_h1_first_movecnt = match.count
    elif(srcpiece == PIECES['bRk']):
        if(move.srcx == 0 and move.srcy == 7 and match.bRk_a8_first_movecnt == 0):
            match.bRk_a8_first_movecnt = match.count
        elif(move.srcx == 7 and move.srcy == 7 and match.bRk_h8_first_movecnt == 0):
            match.bRk_h8_first_movecnt = match.count

    match.score += SCORES[dstpiece]
    match.move_list.append(move)

    return move

    
def pawn_do_move(match, move, srcpiece, dstpiece):
    if(move.prom_piece != PIECES['blk']):
        move.move_type = TYPES['promotion']
        move.captured_piece = dstpiece

        match.count += 1 
        match.writefield(move.srcx, move.srcy, PIECES['blk'])
        match.writefield(move.dstx, move.dsty, move.prom_piece)
        match.fifty_moves_count = 0
        match.score -= (SCORES[move.prom_piece] - SCORES[srcpiece])
        match.score += SCORES[dstpiece]
        match.move_list.append(move)

        return move
    elif(dstpiece == PIECES['blk'] and move.srcx != move.dstx):
        move.move_type = TYPES['en_passant']
        move.e_p_fieldx = move.dstx
        move.e_p_fieldy = move.srcy
        pawn = match.readfield(move.e_p_fieldx, move.e_p_fieldy)
        move.captured_piece = pawn

        match.count += 1 
        match.writefield(move.srcx, move.srcy, PIECES['blk'])
        match.writefield(move.dstx, move.dsty, srcpiece)
        match.fifty_moves_count = 0
        match.writefield(move.e_p_fieldx, move.e_p_fieldy, PIECES['blk'])
        match.score += SCORES[pawn]
        match.move_list.append(move)

        return move
    else:
        return generic_do_move(match, move, srcpiece, dstpiece)


def king_do_move(match, move, srcpiece, dstpiece):
    if(move.dstx - move.srcx == 2):
        move.move_type = TYPES['short_castling']
        move.captured_piece = dstpiece

        match.count += 1   
        match.writefield(move.srcx, move.srcy, PIECES['blk'])
        match.writefield(move.dstx, move.dsty, srcpiece)
        rook = match.readfield(move.srcx + 3, move.srcy)
        match.writefield(move.srcx + 3, move.srcy, PIECES['blk'])
        match.writefield(move.dstx - 1, move.dsty, rook)
        match.fifty_moves_count += 1
        if(srcpiece == PIECES['wKg']):
            match.wKg_x = move.dstx
            match.wKg_y = move.dsty
            if(match.wKg_first_movecnt == 0):
                match.wKg_first_movecnt = match.count
        else:
            match.bKg_x = move.dstx
            match.bKg_y = move.dsty
            if(match.bKg_first_movecnt == 0):
                match.bKg_first_movecnt = match.count
        match.move_list.append(move)

        return move
    elif(move.dstx - move.srcx == -2):
        move.move_type = TYPES['long_castling']
        move.captured_piece = dstpiece

        match.count += 1   
        match.writefield(move.srcx, move.srcy, PIECES['blk'])
        match.writefield(move.dstx, move.dsty, srcpiece)
        rook = match.readfield(move.srcx - 4, move.srcy)
        match.writefield(move.srcx - 4, move.srcy, PIECES['blk'])
        match.writefield(move.dstx + 1, move.dsty, rook)
        match.fifty_moves_count += 1
        if(srcpiece == PIECES['wKg']):
            match.wKg_x = move.dstx
            match.wKg_y = move.dsty
            if(match.wKg_first_movecnt == 0):
                match.wKg_first_movecnt = match.count
        else:
            match.bKg_x = move.dstx
            match.bKg_y = move.dsty
            if(match.bKg_first_movecnt == 0):
                match.bKg_first_movecnt = match.count
        match.move_list.append(move)

        return move
    else:
        return generic_do_move(match, move, srcpiece, dstpiece)


def undo_move(match):
    if(len(match.move_list) > 0):
        move = match.move_list.pop()
    else:
        return None

    if(move.move_type == TYPES['standard']):
        return generic_undo_move(match, move)
    elif(move.move_type == TYPES['short_castling']):
        return king_undo_short_castling(match, move)
    elif(move.move_type == TYPES['long_castling']):
        return king_undo_long_castling(match, move)
    elif(move.move_type == TYPES['promotion']):
        return pawn_undo_promotion(match, move)
    else:
        return pawn_undo_en_passant(match, move)


def generic_undo_move(match, move):
    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count

    piece = match.readfield(move.dstx, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, move.captured_piece)
    match.score -= SCORES[move.captured_piece]
    if(piece == PIECES['wKg']):
        match.wKg_x = move.srcx
        match.wKg_y = move.srcy
        if(match.wKg_first_movecnt == match.count + 1):
            match.wKg_first_movecnt = 0
    elif(piece == PIECES['bKg']):
        match.bKg_x = move.srcx
        match.bKg_y = move.srcy
        if(match.bKg_first_movecnt == match.count + 1):
            match.bKg_first_movecnt = 0
    elif(piece == PIECES['wRk']):
        if(match.wRk_a1_first_movecnt == match.count + 1):
            match.wRk_a1_first_movecnt = 0
        elif(match.wRk_h1_first_movecnt == match.count + 1):
            match.wRk_h1_first_movecnt = 0
    elif(piece == PIECES['bRk']):
        if(match.bRk_a8_first_movecnt == match.count + 1):
            match.bRk_a8_first_movecnt = 0
        elif(match.bRk_h8_first_movecnt == match.count + 1):
            match.bRk_h8_first_movecnt = 0

    return move


def king_undo_short_castling(match, move):
    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count

    piece = match.readfield(move.dstx, move.dsty)
    rook = match.readfield(move.dstx - 1, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, PIECES['blk'])
    match.writefield(move.dstx - 1, move.dsty, PIECES['blk'])
    match.writefield(move.dstx + 1, move.dsty, rook)
    if(piece == PIECES['wKg']):
        match.wKg_x = move.srcx
        match.wKg_y = move.srcy
        match.wKg_first_movecnt = 0
        match.wRk_h1_first_movecnt = 0
    else:
        match.bKg_x = move.srcx
        match.bKg_y = move.srcy
        match.bKg_first_movecnt = 0
        match.bRk_h8_first_movecnt = 0

    return move


def king_undo_long_castling(match, move):
    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count

    piece = match.readfield(move.dstx, move.dsty)
    rook = match.readfield(move.dstx + 1, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, PIECES['blk'])
    match.writefield(move.dstx + 1, move.dsty, PIECES['blk'])
    match.writefield(move.dstx - 2, move.dsty, rook)
    if(piece == PIECES['wKg']):
        match.wKg_x = move.srcx
        match.wKg_y = move.srcy
        match.wKg_first_movecnt = 0
        match.wRk_a1_first_movecnt = 0
    else:
        match.bKg_x = move.srcx
        match.bKg_y = move.srcy
        match.bKg_first_movecnt = 0
        match.bRk_a8_first_movecnt = 0

    return move


def pawn_undo_promotion(match, move):
    if(move.dsty == 7):
        piece = PIECES['wPw']
    else:
        piece = PIECES['bPw']

    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, move.captured_piece)
    match.score += (SCORES[move.prom_piece] - SCORES[piece])
    match.score -= SCORES[move.captured_piece]
    return move


def pawn_undo_en_passant(match, move):
    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count
    piece = match.readfield(move.dstx, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, PIECES['blk'])
    match.writefield(move.e_p_fieldx, move.e_p_fieldy, move.captured_piece)
    match.score -= SCORES[move.captured_piece]
    return move

