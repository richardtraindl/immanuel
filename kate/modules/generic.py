from kate.models import Match, Move
from kate.modules import rules 
            
            
def generic.do_move(match, move, srcpiece, dstpiece):
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

    if(srcpiece == Match.PIECES['wRk']):
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

