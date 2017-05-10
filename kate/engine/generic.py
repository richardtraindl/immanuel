from kate.engine import match, move


def do_move(match, nmove, srcpiece, dstpiece):
    nmove.move_type = move.TYPES['standard']
    nmove.captured_piece = dstpiece

    match.count += 1            
    match.writefield(nmove.srcx, nmove.srcy, match.PIECES['blk'])
    match.writefield(nmove.dstx, nmove.dsty, srcpiece)
    if(dstpiece != match.PIECES['blk']):
        match.fifty_nmoves_count = 0
        nmove.fifty_nmoves_count = match.fifty_nmoves_count
    else:
        match.fifty_nmoves_count += 1
        nmove.fifty_nmoves_count = match.fifty_nmoves_count

    if(srcpiece == match.PIECES['wKg']):
        match.wKg_x = nmove.dstx
        match.wKg_y = nmove.dsty
        if(match.wKg_first_nmovecnt == 0):
            match.wKg_first_nmovecnt = match.count
    elif(srcpiece == match.PIECES['bKg']):
        match.bKg_x = nmove.dstx
        match.bKg_y = nmove.dsty
        if(match.bKg_first_nmovecnt == 0):
            match.bKg_first_nmovecnt = match.count
    elif(srcpiece == match.PIECES['wRk']):
        if(nmove.srcx == 0 and nmove.srcy == 0 and match.wRk_a1_first_nmovecnt == 0):
            match.wRk_a1_first_nmovecnt = match.count
        elif(nmove.srcx == 7 and nmove.srcy == 0 and match.wRk_h1_first_nmovecnt == 0):
            match.wRk_h1_first_nmovecnt = match.count
    elif(srcpiece == match.PIECES['bRk']):
        if(nmove.srcx == 0 and nmove.srcy == 7 and match.bRk_a8_first_nmovecnt == 0):
            match.bRk_a8_first_nmovecnt = match.count
        elif(nmove.srcx == 7 and nmove.srcy == 7 and match.bRk_h8_first_nmovecnt == 0):
            match.bRk_h8_first_nmovecnt = match.count

    match.score += match.SCORES[dstpiece]
    match.move_list.append(nmove)

    return nmove


def undo_nmove(match, nmove):
    match.count -= 1
    match.fifty_nmoves_count = nmove.fifty_nmoves_count

    piece = match.readfield(nmove.dstx, nmove.dsty)
    match.writefield(nmove.srcx, nmove.srcy, piece)
    match.writefield(nmove.dstx, nmove.dsty, nmove.captured_piece)
    match.score -= match.SCORES[nmove.captured_piece]
    if(piece == match.PIECES['wKg']):
        match.wKg_x = nmove.srcx
        match.wKg_y = nmove.srcy
        if(match.wKg_first_nmovecnt == match.count + 1):
            match.wKg_first_nmovecnt = 0
    elif(piece == match.PIECES['bKg']):
        match.bKg_x = nmove.srcx
        match.bKg_y = nmove.srcy
        if(match.bKg_first_nmovecnt == match.count + 1):
            match.bKg_first_nmovecnt = 0
    elif(piece == match.PIECES['wRk']):
        if(match.wRk_a1_first_nmovecnt == match.count + 1):
            match.wRk_a1_first_nmovecnt = 0
        elif(match.wRk_h1_first_nmovecnt == match.count + 1):
            match.wRk_h1_first_nmovecnt = 0
    elif(piece == match.PIECES['bRk']):
        if(match.bRk_a8_first_nmovecnt == match.count + 1):
            match.bRk_a8_first_nmovecnt = 0
        elif(match.bRk_h8_first_nmovecnt == match.count + 1):
            match.bRk_h8_first_nmovecnt = 0

    return nmove

