from kate.models import Match, Move
from kate.modules import rules 
            
            
def generic.do_move(match, move, srcpiece, dstpiece):
            self.writefield(srcx, srcy, Match.PIECES['blk'])
            self.writefield(dstx, dsty, srcpiece)
            if(dstpiece != Match.PIECES['blk']):
                self.fifty_moves_count = 0
            else:
                self.fifty_moves_count += 1

            if(srcpiece == Match.PIECES['wRk']):
                if(srcx == 0 and srcy == 0 and self.wRk_a1_first_movecnt == 0):
                    self.wRk_a1_first_movecnt = self.count
                elif(srcx == 7 and srcy == 0 and self.wRk_h1_first_movecnt == 0):
                    self.wRk_h1_first_movecnt = self.count
            elif(srcpiece == Match.PIECES['bRk']):
                if(srcx == 0 and srcy == 7 and self.bRk_a8_first_movecnt == 0):
                    self.bRk_a8_first_movecnt = self.count
                elif(srcx == 7 and srcy == 7 and self.bRk_h8_first_movecnt == 0):
                    self.bRk_h8_first_movecnt = self.count
            move.fifty_moves_count = self.fifty_moves_count
            move.move_type = Move.TYPES['standard']
            move.captured_piece = dstpiece
            self.score += Match.SCORES[dstpiece]
            self.move_list.append(move)
            return move
