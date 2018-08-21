from . piece import *


class cKing(cPiece):
    DIRS = { 'sh-castling' : 11, 'lg-castling' : 12, 'valid' : 13, 'undefined' : 14 }
    DIRS_ARY = []
    STEPS = [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]

    STEP_1N_X = 0
    STEP_1N_Y = 1
    STEP_1N1E_X = 1
    STEP_1N1E_Y = 1
    STEP_1E_X = 1
    STEP_1E_Y = 0
    STEP_1S1E_X = 1
    STEP_1S1E_Y = -1
    STEP_1S_X = 0
    STEP_1S_Y = -1
    STEP_1S1W_X = -1
    STEP_1S1W_Y = -1
    STEP_1W_X = -1
    STEP_1W_Y = 0
    STEP_1N1W_X = -1
    STEP_1N1W_Y = 1
    STEP_SH_CASTLING_X = 2
    STEP_SH_CASTLING_Y = 0
    STEP_LG_CASTLING_X = -2
    STEP_LG_CASTLING_Y = 0

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == cls.STEP_1N_X and step_y == cls.STEP_1N_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1N1E_X and step_y == cls.STEP_1N1E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1E_X and step_y == cls.STEP_1E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1S1E_X and step_y == cls.STEP_1S1E_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1S_X and step_y == cls.STEP_1S_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1S1W_X and step_y == cls.STEP_1S1W_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1W_X and step_y == cls.STEP_1W_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_1N1W_X and step_y == cls.STEP_1N1W_Y):
            return cls.DIRS['valid']
        elif(step_x == cls.STEP_SH_CASTLING_X and step_y == cls.STEP_SH_CASTLING_Y):
            return cls.DIRS['sh-castling']
        elif(step_x == cls.STEP_LG_CASTLING_X and step_y == cls.STEP_LG_CASTLING_Y):
            return cls.DIRS['lg-castling']
        else:
            return cls.DIRS['undefined']

    #step_for_dir(direction):
        # not used for king

    def is_piece_trapped(self):
        return False # king cannot be trapped

    def is_piece_stuck_new(self):
        return False # king cannot stuck

    def is_move_stuck(self, dstx, dsty):
        return False # not used for king

    def is_move_valid(self, dstx, dsty):
        opp_color = self.match.oppcolor_of_piece(self.piece)

        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == self.DIRS['sh-castling']):
            return self.is_sh_castling_ok(dstx, dsty)
        if(direction == self.DIRS['lg-castling']):
            return self.is_lg_castling_ok(dstx, dsty)
        if(direction == self.DIRS['undefined']):
            return False

        captured = self.match.readfield(dstx, dsty)
        self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
        self.match.writefield(dstx, dsty, self.piece)
        attacked = self.match.is_field_touched(opp_color, dstx, dsty, 0)
        self.match.writefield(self.xpos, self.ypos, self.piece)
        self.match.writefield(dstx, dsty, captured)
        if(attacked == True):
            return False

        dstpiece = self.match.readfield(dstx, dsty)
        if(self.match.color_of_piece(dstpiece) == self.color):
            return False

        return True

    def is_sh_castling_ok(self, dstx, dsty):
        opp_color = self.match.oppcolor_of_piece(self.piece)

        for i in range(1, 3, 1):
            fieldx = self.xpos + i
            field = self.match.readfield(fieldx, self.ypos)
            if(field != self.match.PIECES['blk']):
                return False

        if( self.match.is_inbounds(dstx + 1, dsty)):
            rook = self.match.readfield(dstx + 1, dsty)
        else:
            return False

        if(self.color == self.match.COLORS['white']):
            if(self.match.white_movecnt_short_castling_lost > 0 or rook != self.match.PIECES['wRk']):
                return False
        else:
            if(self.match.black_movecnt_short_castling_lost > 0 or rook != self.match.PIECES['bRk']):
                return False            

        self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
        for i in range(3):
            castlingx = self.xpos + i
            attacked = self.match.is_field_touched(opp_color, castlingx, self.ypos, 0)
            if(attacked == True):
                self.match.writefield(self.xpos, self.ypos, self.piece)
                return False

        self.match.writefield(self.xpos, self.ypos, self.piece)
        return True

    def is_lg_castling_ok(self, dstx, dsty):
        opp_color = self.match.oppcolor_of_piece(self.piece)

        for i in range(1, 4, 1):
            fieldx = self.xpos - i
            field = self.match.readfield(fieldx, self.ypos)
            if(field != self.match.PIECES['blk']):
                return False

        if(self.match.is_inbounds(dstx - 2, dsty)):
            rook = self.match.readfield(dstx - 2, dsty)
        else:
            return False

        if(self.color == self.match.COLORS['white']):
            if(self.match.white_movecnt_long_castling_lost > 0 or rook != self.match.PIECES['wRk']):
                return False
        else:
            if(self.match.black_movecnt_long_castling_lost > 0 or rook != self.match.PIECES['bRk']):
                return False

        self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
        for i in range(0, -3, -1):
            castlingx = self.xpos + i
            attacked = self.match.is_field_touched(opp_color, castlingx, self.ypos, 0)
            if(attacked == True):
                self.match.writefield(self.xpos, self.ypos, self.piece)
                return False

        self.match.writefield(self.xpos, self.ypos, self.piece)
        return True

    def find_attacks_and_supports(self, dstx, dsty, attacked, supported):
        from .. analyze_helper import field_touches_beyond

        opp_color = self.match.oppcolor_of_piece(self.piece)
        for step in self.STEPS:
            x1 = dstx + step[0]
            y1 = dsty + step[1]
            if(self.match.is_inbounds(x1, y1)):
                if(x1 == self.xpos and y1 == self.ypos):
                    continue
    
                piece = self.match.readfield(x1, y1)
                if(piece == self.match.PIECES['blk']):
                    continue

                if(self.match.color_of_piece(piece) == opp_color):
                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    attacked.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
                    field_touches_beyond(self.match, opp_color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###
                else:
                    ctouch_beyond = cTouchBeyond(self.xpos, self.ypos, dstx, dsty, piece, x1, y1)
                    supported.append(ctouch_beyond)
                    ###
                    self.match.writefield(self.xpos, self.ypos, self.match.PIECES['blk'])
                    field_touches_beyond(self.match, self.color, ctouch_beyond)
                    self.match.writefield(self.xpos, self.ypos, self.piece)
                    ###

    def move_defends_forked_field(self, dstx, dsty)
        from .. analyze_helper import is_field_forked

        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]

            x1 = dstx + stepx
            y1 = dsty + stepy

            if(x1 == self.xpos and y1 == self.ypos):
                continue

            if(self.match.is_inbounds(x1, y1)):
                if(self.match.is_king_attacked(x1, y1)):
                    continue

                piece = self.match.readfield(x1, y1)

                if(self.match.color_of_piece(piece) == self.color):
                    if(is_field_forked(self.match, piece, x1, y1)):
                        #cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                        #analyses.lst_fork_defended.append(cfork)
                        return True

        return False

    def move_controles_file(self, dstx, dsty)
        return False

# class end

