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


def generic.undo_move(match, move):
    piece = self.readfield(move.dstx, move.dsty)
    self.writefield(move.srcx, move.srcy, piece)
    self.writefield(move.dstx, move.dsty, move.captured_piece)
    self.score -= self.SCORES[move.captured_piece]
    if(piece == Match.PIECES['wKg']):
        self.wKg_x = move.srcx
        self.wKg_y = move.srcy
        if(self.wKg_first_movecnt == self.count + 1):
            self.wKg_first_movecnt = 0
    elif(piece == Match.PIECES['bKg']):
        self.bKg_x = move.srcx
        self.bKg_y = move.srcy
        if(self.bKg_first_movecnt == self.count + 1):
            self.bKg_first_movecnt = 0
    elif(piece == Match.PIECES['wRk']):
        if(self.wRk_a1_first_movecnt == self.count + 1):
            self.wRk_a1_first_movecnt = 0
        elif(self.wRk_h1_first_movecnt == self.count + 1):
            self.wRk_h1_first_movecnt = 0
    elif(piece == Match.PIECES['bRk']):
        if(self.bRk_a8_first_movecnt == self.count + 1):
            self.bRk_a8_first_movecnt = 0
        elif(self.bRk_h8_first_movecnt == self.count + 1):
            self.bRk_h8_first_movecnt = 0

    return move



