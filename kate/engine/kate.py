from kate.engine import move, rules, calc_helper
from kate.engine.match import *


def do_move(match, srcx, srcy, dstx, dsty, prom_piece):
    nmove = move.Move(match=match, 
                count=match.count+1, 
                move_type=move.TYPES['standard'], 
                srcx=srcx, 
                srcy=srcy, 
                dstx=dstx, 
                dsty=dsty, 
                e_p_fieldx=None,
                e_p_fieldy=None,
                captured_piece=PIECES['blk'], 
                prom_piece=prom_piece, 
                fifty_moves_count=match.fifty_moves_count)

    srcpiece = match.readfield(srcx, srcy)
    dstpiece = match.readfield(dstx, dsty)

    if(srcpiece == PIECES['wPw'] or srcpiece == PIECES['bPw']):
        return pawn_do_move(match, nmove, srcpiece, dstpiece)
    elif(srcpiece == PIECES['wKg'] or srcpiece == PIECES['bKg']):
        return king_do_move(match, nmove, srcpiece, dstpiece)
    else:
        return generic_do_move(match, nmove, srcpiece, dstpiece)


def generic_do_move(match, nmove, srcpiece, dstpiece):
    nmove.move_type = move.TYPES['standard']
    nmove.captured_piece = dstpiece

    match.count += 1            
    match.writefield(nmove.srcx, nmove.srcy, PIECES['blk'])
    match.writefield(nmove.dstx, nmove.dsty, srcpiece)
    if(dstpiece != PIECES['blk']):
        match.fifty_nmoves_count = 0
        nmove.fifty_nmoves_count = match.fifty_nmoves_count
    else:
        match.fifty_nmoves_count += 1
        nmove.fifty_nmoves_count = match.fifty_nmoves_count

    if(srcpiece == PIECES['wKg']):
        match.wKg_x = nmove.dstx
        match.wKg_y = nmove.dsty
        if(match.wKg_first_nmovecnt == 0):
            match.wKg_first_nmovecnt = match.count
    elif(srcpiece == PIECES['bKg']):
        match.bKg_x = nmove.dstx
        match.bKg_y = nmove.dsty
        if(match.bKg_first_nmovecnt == 0):
            match.bKg_first_nmovecnt = match.count
    elif(srcpiece == PIECES['wRk']):
        if(nmove.srcx == 0 and nmove.srcy == 0 and match.wRk_a1_first_nmovecnt == 0):
            match.wRk_a1_first_nmovecnt = match.count
        elif(nmove.srcx == 7 and nmove.srcy == 0 and match.wRk_h1_first_nmovecnt == 0):
            match.wRk_h1_first_nmovecnt = match.count
    elif(srcpiece == PIECES['bRk']):
        if(nmove.srcx == 0 and nmove.srcy == 7 and match.bRk_a8_first_nmovecnt == 0):
            match.bRk_a8_first_nmovecnt = match.count
        elif(nmove.srcx == 7 and nmove.srcy == 7 and match.bRk_h8_first_nmovecnt == 0):
            match.bRk_h8_first_nmovecnt = match.count

    match.score += calc_helper.SCORES[dstpiece]
    match.move_list.append(nmove)

    return nmove

    
def pawn_do_move(match, move, srcpiece, dstpiece):
    if(move.prom_piece != PIECES['blk']):
        move.move_type = Move.TYPES['promotion']
        move.captured_piece = dstpiece

        match.count += 1 
        match.writefield(move.srcx, move.srcy, PIECES['blk'])
        match.writefield(move.dstx, move.dsty, move.prom_piece)
        match.fifty_moves_count = 0
        match.score -= (calc_helpe.SCORES[move.prom_piece] - calc_helpe.SCORES[srcpiece])
        match.score += calc_helpe.SCORES[dstpiece]
        match.move_list.append(move)

        return move
    elif(dstpiece == PIECES['blk'] and move.srcx != move.dstx):
        move.move_type = Move.TYPES['en_passant']
        move.e_p_fieldx = move.dstx
        move.e_p_fieldy = move.srcy
        pawn = match.readfield(move.e_p_fieldx, move.e_p_fieldy)
        move.captured_piece = pawn

        match.count += 1 
        match.writefield(move.srcx, move.srcy, PIECES['blk'])
        match.writefield(move.dstx, move.dsty, srcpiece)
        match.fifty_moves_count = 0
        match.writefield(move.e_p_fieldx, move.e_p_fieldy, PIECES['blk'])
        match.score += calc_helpe.SCORES[pawn]
        match.move_list.append(move)

        return move
    else:
        return generic_do_move(match, move, srcpiece, dstpiece)


def king_do_move(match, move, srcpiece, dstpiece):
    if(move.dstx - move.srcx == 2):
        move.move_type = Move.TYPES['short_castling']
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
        move.move_type = Move.TYPES['long_castling']
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
        return generic.do_move(match, move, srcpiece, dstpiece)


def undo_move(match, calc):
    if(calc == False):
        move = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(move == None):
            return None
    else:
        if(len(match.move_list) > 0):
            move = match.move_list.pop()
        else:
            return None

    if(move.move_type == Move.TYPES['standard']):
        return generic_undo_move(match, move)
    elif(move.move_type == Move.TYPES['short_castling']):
        return king_undo_short_castling(match, move)
    elif(move.move_type == Move.TYPES['long_castling']):
        return king_undo_long_castling(match, move)
    elif(move.move_type == Move.TYPES['promotion']):
        return pawn_undo_promotion(match, move)
    else:
        return pawn_undo_en_passant(match, move)


def generic_undo_nmove(match, nmove):
    match.count -= 1
    match.fifty_nmoves_count = nmove.fifty_nmoves_count

    piece = match.readfield(nmove.dstx, nmove.dsty)
    match.writefield(nmove.srcx, nmove.srcy, piece)
    match.writefield(nmove.dstx, nmove.dsty, nmove.captured_piece)
    match.score -= match.SCORES[nmove.captured_piece]
    if(piece == PIECES['wKg']):
        match.wKg_x = nmove.srcx
        match.wKg_y = nmove.srcy
        if(match.wKg_first_nmovecnt == match.count + 1):
            match.wKg_first_nmovecnt = 0
    elif(piece == PIECES['bKg']):
        match.bKg_x = nmove.srcx
        match.bKg_y = nmove.srcy
        if(match.bKg_first_nmovecnt == match.count + 1):
            match.bKg_first_nmovecnt = 0
    elif(piece == PIECES['wRk']):
        if(match.wRk_a1_first_nmovecnt == match.count + 1):
            match.wRk_a1_first_nmovecnt = 0
        elif(match.wRk_h1_first_nmovecnt == match.count + 1):
            match.wRk_h1_first_nmovecnt = 0
    elif(piece == PIECES['bRk']):
        if(match.bRk_a8_first_nmovecnt == match.count + 1):
            match.bRk_a8_first_nmovecnt = 0
        elif(match.bRk_h8_first_nmovecnt == match.count + 1):
            match.bRk_h8_first_nmovecnt = 0

    return nmove


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
    match.score += (calc_helper.SCORES[move.prom_piece] - calc_helpe.SCORES[piece])
    match.score -= calc_helper.SCORES[move.captured_piece]
    return move


def pawn_undo_en_passant(match, move):
    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count
    piece = match.readfield(move.dstx, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, PIECES['blk'])
    match.writefield(move.e_p_fieldx, move.e_p_fieldy, move.captured_piece)
    match.score -= calc_helper.SCORES[move.captured_piece]
    return move

