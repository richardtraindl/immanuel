from .. values import *
from .piece import *


class cPawn(cPiece):
    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    def is_trapped(self):
        return False # pawn cannot be trapped

################
    def do_move(self, dstx, dsty, prom_piece=PIECES['blk']):
        board = self.match.board
        dstpiece = board.readfield(dstx, dsty)
        move = super().do_move(dstx, dsty, prom_piece)

        if(prom_piece != PIECES['blk']):
            move.move_type = cMove.TYPES['promotion']
            board.writefield(dstx, dsty, prom_piece)
            self.match.score -= (SCORES[prom_piece] - SCORES[self.piece])
        elif(dstpiece == PIECES['blk'] and self.xpos != dstx):
            move.move_type = cMove.TYPES['en_passant']
            move.e_p_fieldx = self.xpos
            move.e_p_fieldy = dsty
            move.captured_piece = board.readfield(move.e_p_fieldx, move.e_p_fieldy)
            board.writefield(move.e_p_fieldx, move.e_p_fieldy, PIECES['blk'])
            self.match.score += SCORES[move.captured_piece]

        return move
################

################
    def undo_move(self, move):
        board = self.match.board
        super().undo_move(move)

        if(move.move_type == move.TYPES['promotion']):
            if(self.color == COLORS['white']):
                origin = PIECES['wPw']
            else:
                origin = PIECES['bPw']
            board.writefield(move.srcx, move.srcy, origin)
            board.writefield(move.dstx, move.dsty, move.captured_piece)
            self.match.score += (SCORES[move.prom_piece] - SCORES[origin])
        elif(move.move_type == move.TYPES['en_passant']):
            board.writefield(move.dstx, move.dsty, PIECES['blk'])
            board.writefield(move.e_p_fieldx, move.e_p_fieldy, move.captured_piece)

        return move
################

    def move_controles_file(self, dstx, dsty):
        return False

    def is_running(self):
        if(self.color == COLORS['white']):
            stepx = 0
            stepy = 1
            opp_pawn = PIECES['bPw']
        else:
            stepx = 0
            stepy = -1
            opp_pawn = PIECES['wPw']
        for i in range(-1, 2, 1):
            x1 = self.xpos + i
            y1 = self.ypos
            while(True):
                x1, y1 = self.match.board.search(x1, y1, stepx, stepy)
                if(x1 is not None):
                    piece = self.match.board.readfield(x1, y1)
                    if(piece == opp_pawn):
                        return False
                else:
                    break
        return True

    def is_weak(self):
        friends, enemies = list_all_field_touches(self.match, self.xpos, self.ypos, self.color)
        if(len(friends) >= len(enemies)):
            return False
        if(self.color == COLORS['white']):
            stepy = -1
        else:
            stepy = 1
        for i in range(2):
            if(i == 0):
                newx = self.xpos + 1
            else:
                newx = self.xpos - 1
            if(self.match.is_inbounds(newx, self.ypos)):
                x1, y1 = self.match.board.search(newx, self.ypos, newx, stepy)
                if(x1 is not None):
                    piece = self.match.board.readfield(x1, y1)
                    if((piece == PIECES['wPw'] or piece == PIECES['bPw']) and
                       self.color == self.match.color_of_piece(piece)):
                        return False
        return True

# class end

