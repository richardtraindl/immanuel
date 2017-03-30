from kate.models import Match, Move


def do_move(match, move, srcpiece, dstpiece):
    move.move_type = Move.TYPES['standard']
    move.captured_piece = dstpiece

    match.count += 1            
    match.writefield(move.srcx, move.srcy, Match.PIECES['blk'])
    match.writefield(move.dstx, move.dsty, srcpiece)
    if(dstpiece != Match.PIECES['blk']):
        match.fifty_moves_count = 0
        move.fifty_moves_count = match.fifty_moves_count
    else:
        match.fifty_moves_count += 1
        move.fifty_moves_count = match.fifty_moves_count

    if(srcpiece == Match.PIECES['wKg']):
        match.wKg_x = move.dstx
        match.wKg_y = move.dsty
        if(match.wKg_first_movecnt == 0):
            match.wKg_first_movecnt = match.count
    elif(srcpiece == Match.PIECES['bKg']):
        match.bKg_x = move.dstx
        match.bKg_y = move.dsty
        if(match.bKg_first_movecnt == 0):
            match.bKg_first_movecnt = match.count
    elif(srcpiece == Match.PIECES['wRk']):
        if(move.srcx == 0 and move.srcy == 0 and match.wRk_a1_first_movecnt == 0):
            match.wRk_a1_first_movecnt = match.count
        elif(move.srcx == 7 and move.srcy == 0 and match.wRk_h1_first_movecnt == 0):
            match.wRk_h1_first_movecnt = match.count
    elif(srcpiece == Match.PIECES['bRk']):
        if(move.srcx == 0 and move.srcy == 7 and match.bRk_a8_first_movecnt == 0):
            match.bRk_a8_first_movecnt = match.count
        elif(move.srcx == 7 and move.srcy == 7 and match.bRk_h8_first_movecnt == 0):
            match.bRk_h8_first_movecnt = match.count

    match.score += Match.SCORES[dstpiece]
    match.move_list.append(move)

    return move


def undo_move(match, move):
    match.count -= 1
    match.fifty_moves_count = move.fifty_moves_count

    piece = match.readfield(move.dstx, move.dsty)
    match.writefield(move.srcx, move.srcy, piece)
    match.writefield(move.dstx, move.dsty, move.captured_piece)
    match.score -= Match.SCORES[move.captured_piece]
    if(piece == Match.PIECES['wKg']):
        match.wKg_x = move.srcx
        match.wKg_y = move.srcy
        if(match.wKg_first_movecnt == match.count + 1):
            match.wKg_first_movecnt = 0
    elif(piece == Match.PIECES['bKg']):
        match.bKg_x = move.srcx
        match.bKg_y = move.srcy
        if(match.bKg_first_movecnt == match.count + 1):
            match.bKg_first_movecnt = 0
    elif(piece == Match.PIECES['wRk']):
        if(match.wRk_a1_first_movecnt == match.count + 1):
            match.wRk_a1_first_movecnt = 0
        elif(match.wRk_h1_first_movecnt == match.count + 1):
            match.wRk_h1_first_movecnt = 0
    elif(piece == Match.PIECES['bRk']):
        if(match.bRk_a8_first_movecnt == match.count + 1):
            match.bRk_a8_first_movecnt = 0
        elif(match.bRk_h8_first_movecnt == match.count + 1):
            match.bRk_h8_first_movecnt = 0

    return move

