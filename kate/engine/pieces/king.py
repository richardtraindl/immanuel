from .. values import *
from . piece import *
from . rook import cRook
from . bishop import cBishop


class cKing(cPiece):
    DIRS = { 'sh-castling' : 11, 'lg-castling' : 12, 'valid' : 13, 'undefined' : 14 }
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
    GEN_STEPS = [ [[0, 1, PIECES['blk']]],
                  [[1, 1, PIECES['blk']]],
                  [[1, 0, PIECES['blk']]], 
                  [[1, -1, PIECES['blk']]],
                  [[0, -1, PIECES['blk']]], 
                  [[-1, -1, PIECES['blk']]],
                  [[-1, 0, PIECES['blk']]],
                  [[-1, 1, PIECES['blk']]],
                  [[2, 0, PIECES['blk']]],
                  [[-2, 0, PIECES['blk']]] ]
    MAXCNT = 1

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

    def is_trapped(self):
        return False # king cannot be trapped

    def is_piece_stuck(self):
        return False # king cannot stuck

    def is_move_stuck(self, dstx, dsty):
        return False # not used for king

    def is_attacked(self):
        return self.match.is_field_touched(REVERSED_COLORS[self.color], self.xpos, self.ypos, self.match.EVAL_MODES['ignore-pins'])

    def is_move_valid(self, dstx, dsty, prom_piece=PIECES['blk']):
        opp_color = self.match.oppcolor_of_piece(self.piece)

        direction = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(direction == self.DIRS['sh-castling']):
            return self.is_sh_castling_ok(dstx, dsty)
        if(direction == self.DIRS['lg-castling']):
            return self.is_lg_castling_ok(dstx, dsty)
        if(direction == self.DIRS['undefined']):
            return False

        captured = self.match.readfield(dstx, dsty)
        self.match.writefield(self.xpos, self.ypos, PIECES['blk'])
        self.match.writefield(dstx, dsty, self.piece)
        attacked = self.match.is_field_touched(opp_color, dstx, dsty, self.match.EVAL_MODES['ignore-pins'])
        self.match.writefield(self.xpos, self.ypos, self.piece)
        self.match.writefield(dstx, dsty, captured)
        if(attacked == True):
            return False

        dstpiece = self.match.readfield(dstx, dsty)
        if(self.match.color_of_piece(dstpiece) == self.color):
            return False

        return True

    def do_move(self, dstx, dsty, prom_piece):
        move = cMove(self.match, 
                    self.match.movecnt() + 1, 
                    cMove.TYPES['standard'],
                    self.xpos, 
                    self.ypos, 
                    dstx, 
                    dsty, 
                    None,
                    None,
                    PIECES['blk'], 
                    prom_piece, 
                    self.match.board.fifty_moves_count)

        dstpiece = self.match.readfield(move.dstx, move.dsty)

        if(move.dstx - move.srcx == 2):
            move.move_type = cMove.TYPES['short_castling']
            move.captured_piece = dstpiece
            self.match.writefield(move.srcx, move.srcy, PIECES['blk'])
            self.match.writefield(move.dstx, move.dsty, self.piece)
            rook = self.match.readfield(move.srcx + 3, move.srcy)
            self.match.writefield(move.srcx + 3, move.srcy, PIECES['blk'])
            self.match.writefield(move.dstx - 1, move.dsty, rook)
        elif(move.dstx - move.srcx == -2):
            move.move_type = cMove.TYPES['long_castling']
            move.captured_piece = dstpiece
            self.match.writefield(move.srcx, move.srcy, PIECES['blk'])
            self.match.writefield(move.dstx, move.dsty, self.piece)
            rook = self.match.readfield(move.srcx - 4, move.srcy)
            self.match.writefield(move.srcx - 4, move.srcy, PIECES['blk'])
            self.match.writefield(move.dstx + 1, move.dsty, rook)
        else:
            move.captured_piece = dstpiece
            self.match.writefield(move.srcx, move.srcy, PIECES['blk'])
            self.match.writefield(move.dstx, move.dsty, self.piece)

        if(self.piece == PIECES['wKg']):
            self.match.board.wKg_x = move.dstx
            self.match.board.wKg_y = move.dsty
            self.match.board.domove_white_movecnt_short_castling_lost(move.srcx, move.srcy, move.count)
            self.match.board.domove_white_movecnt_long_castling_lost(move.srcx, move.srcy, move.count)
        else:
            self.match.board.bKg_x = move.dstx
            self.match.board.bKg_y = move.dsty
            self.match.board.domove_black_movecnt_short_castling_lost(move.srcx, move.srcy, move.count)
            self.match.board.domove_black_movecnt_long_castling_lost(move.srcx, move.srcy, move.count)

        self.match.board.domove_counter(dstpiece)
        self.match.board.domove_fifty_moves_count(self.piece, dstpiece)

        self.match.score += SCORES[dstpiece]
        self.match.move_list.append(move)
        return move

    def undo_move(self, move):
        self.match.writefield(move.srcx, move.srcy, self.piece)
        self.match.writefield(move.dstx, move.dsty, move.captured_piece)
        self.match.score -= SCORES[move.captured_piece]

        if(move.move_type == move.TYPES['short_castling']):
            rook = self.match.readfield(move.dstx - 1, move.dsty)
            self.match.writefield(move.dstx - 1, move.dsty, PIECES['blk'])
            self.match.writefield(move.dstx + 1, move.dsty, rook)
        elif(move.move_type == move.TYPES['long_castling']):
            rook = self.match.readfield(move.dstx + 1, move.dsty)
            self.match.writefield(move.dstx + 1, move.dsty, PIECES['blk'])
            self.match.writefield(move.dstx - 2, move.dsty, rook)

        if(self.piece == PIECES['wKg']):
            self.match.board.wKg_x = move.srcx
            self.match.board.wKg_y = move.srcy
            self.match.board.undomove_white_movecnt_short_castling_lost(move)
            self.match.board.undomove_white_movecnt_long_castling_lost(move)    
        else:
            self.match.board.bKg_x = move.srcx
            self.match.board.bKg_y = move.srcy
            self.match.board.undomove_black_movecnt_short_castling_lost(move)
            self.match.board.undomove_black_movecnt_long_castling_lost(move)                

        self.match.board.undomove_counter(move)
        self.match.board.undomove_fifty_moves_count(move)
        return move

    def is_sh_castling_ok(self, dstx, dsty):
        opp_color = self.match.oppcolor_of_piece(self.piece)

        for i in range(1, 3, 1):
            fieldx = self.xpos + i
            field = self.match.readfield(fieldx, self.ypos)
            if(field != PIECES['blk']):
                return False

        if( self.match.is_inbounds(dstx + 1, dsty)):
            rook = self.match.readfield(dstx + 1, dsty)
        else:
            return False

        if(self.color == COLORS['white']):
            if(self.match.board.white_movecnt_short_castling_lost > 0 or rook != PIECES['wRk']):
                return False
        else:
            if(self.match.board.black_movecnt_short_castling_lost > 0 or rook != PIECES['bRk']):
                return False            

        self.match.writefield(self.xpos, self.ypos, PIECES['blk'])
        for i in range(3):
            castlingx = self.xpos + i
            attacked = self.match.is_field_touched(opp_color, castlingx, self.ypos, self.match.EVAL_MODES['ignore-pins'])
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
            if(field != PIECES['blk']):
                return False

        if(self.match.is_inbounds(dstx - 2, dsty)):
            rook = self.match.readfield(dstx - 2, dsty)
        else:
            return False

        if(self.color == COLORS['white']):
            if(self.match.board.white_movecnt_long_castling_lost > 0 or rook != PIECES['wRk']):
                return False
        else:
            if(self.match.board.black_movecnt_long_castling_lost > 0 or rook != PIECES['bRk']):
                return False

        self.match.writefield(self.xpos, self.ypos, PIECES['blk'])
        for i in range(0, -3, -1):
            castlingx = self.xpos + i
            attacked = self.match.is_field_touched(opp_color, castlingx, self.ypos, self.match.EVAL_MODES['ignore-pins'])
            if(attacked == True):
                self.match.writefield(self.xpos, self.ypos, self.piece)
                return False

        self.match.writefield(self.xpos, self.ypos, self.piece)
        return True

    #find_attacks_and_supports(self, attacked, supported):
        # works with inherited class

    #forks(self):
        # works with inherited class

    """def move_defends_fork(self, dstx, dsty):
        from .. analyze_helper import list_all_field_touches, is_fork_field
        for step in self.STEPS:
            x1, y1 = self.match.search(dstx, dsty, step[0], step[1], self.MAXCNT)
            if(x1 is not None):
                if(x1 == dstx and y1 == dsty):
                    continue
                piece = self.match.readfield(x1, y1)
                if(piece == PIECES['blk'] or 
                   self.match.color_of_piece(piece) == self.color):
                    frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, x1, y1)
                    if(len(frdlytouches) < len(enmytouches)):
                        if(is_fork_field(self.match, x1, y1, REVERSED_COLORS[self.color])):
                            return True
        return False
    def move_defends_fork(self, dstx, dsty):
        from .. analyze_helper import list_all_field_touches, is_fork_field
        for step in self.STEPS:
            stepx = step[0]
            stepy = step[1]
            x1 = dstx + stepx
            y1 = dsty + stepy
            if(x1 == self.xpos and y1 == self.ypos):
                continue
            if(self.match.is_inbounds(x1, y1)):
                cking = cKing(self.match, x1, y1)
                if(cking.is_attacked()):
                    continue
                piece = self.match.readfield(x1, y1)
                if(piece == PIECES['blk'] or 
                   self.match.color_of_piece(piece) == self.color):
                    frdlytouches, enmytouches = list_all_field_touches(self.match, self.color, x1, y1)
                    if(len(frdlytouches) < len(enmytouches)):
                        if(is_fork_field(self.match, x1, y1, REVERSED_COLORS[self.color])):
                            return True
        return False"""

    def move_controles_file(self, dstx, dsty):
        return False

    def score_touches(self):
        return 0

    # list_moves(self):
       # works with inherited class

    # generate_moves(self):
       # works with inherited class

    # generate_priomoves(self):
       # works with inherited class

    def is_safe(self):
        from .. analyze_helper import list_all_field_touches
        count = 0
        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                friends, enemies = list_all_field_touches(self.match, self.color, x1, y1)
                if(len(friends) < len(enemies)):
                    return False
                if(len(enemies) > 0):
                    count += 1
        if(count > 2):
            return False

        friends.clear()
        enemies.clear()
        friends, enemies = list_all_field_touches(self.match, self.color, self.xpos, self.ypos)
        if(len(enemies) >= 2):
            return False
        for enemy in enemies:
            friends_beyond, enemies_beyond = list_all_field_touches(self.match, self.color, enemy.fieldx, enemy.fieldy)
            if(len(friends_beyond) >= len(enemies_beyond)):
                continue
            direction = cRook.dir_for_move(self.xpos, self.ypos, enemy.fieldx, enemy.fieldy)
            if(direction != self.DIRS['undefined']):
                step_x, step_y = cRook.step_for_dir(direction)
            else:
                direction = cBishop.dir_for_move(self.xpos, self.ypos, enemy.fieldx, enemy.fieldy)
                if(direction != self.DIRS['undefined']):
                    step_x, step_y = cBishop.step_for_dir(direction)
                else:
                    return False

            x1 = self.xpos + step_x
            y1 = self.ypos + step_y
            while(self.match.is_inbounds(x1, y1)):
                blocking_friends, blocking_enemies = list_all_field_touches(self.match, self.color, x1, y1)
                if(len(blocking_friends) > 0):
                    break
        return True

    def is_centered(self):
        if(self.xpos >= 2 and self.xpos <= 5 and self.ypos >= 2 and self.ypos <= 5):
            return True
        else:
            return False

# class end

