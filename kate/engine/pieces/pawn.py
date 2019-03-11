from .. values import *
from .piece import *
from .. board import *


class cPawn(cPiece):
    DIRS = { 'north' : 1,
             'south' : 2,
             'north-east' : 5,
             'south-west' : 6,
             'north-west' : 7,
             'south-east' : 8,
             '2north' : 9,
             '2south' : 10,
             'valid' : 13,
             'undefined' : 14 }
    REVERSE_DIRS = { DIRS['north'] : DIRS['south'],
                     DIRS['south'] : DIRS['north'],
                     DIRS['north-east'] : DIRS['south-west'],
                     DIRS['south-west'] : DIRS['north-east'],
                     DIRS['north-west'] : DIRS['south-east'],
                     DIRS['south-east'] : DIRS['north-west'],
                     DIRS['2north'] : DIRS['2south'],
                     DIRS['2south'] : DIRS['2north'],
                     DIRS['valid']  : DIRS['valid'],
                     DIRS['undefined']  : DIRS['undefined'] }
    STEP_1N_X = 0
    STEP_1N_Y = 1
    STEP_2N_X = 0
    STEP_2N_Y = 2
    STEP_1N1E_X = 1
    STEP_1N1E_Y = 1
    STEP_1N1W_X = -1
    STEP_1N1W_Y = 1
    STEP_1S_X = 0
    STEP_1S_Y = -1
    STEP_2S_X = 0
    STEP_2S_Y = -2
    STEP_1S1E_X = 1
    STEP_1S1E_Y = -1
    STEP_1S1W_X = -1
    STEP_1S1W_Y = -1
    blk = 0
    wRk = 3
    wKn = 4
    wBp = 5
    wQu = 6
    bRk = 11
    bKn = 12
    bBp = 13
    bQu = 14 
    MAXCNT = 1

    def __init__(self, match, xpos, ypos):
        super().__init__(match, xpos, ypos)
        if(self.color == COLORS['white']):
            self.STEPS = [ [1, 1], [-1, 1] ]
            self.BACK_STEPS = [ [1, -1], [-1, -1] ]
            if(self.ypos < 6):
                self.GEN_STEPS = [ [[0, 1, PIECES['blk']]], [[0, 2, PIECES['blk']]], [[1, 1, PIECES['blk']]], [[-1, 1, PIECES['blk']]] ]
            else:
                self.GEN_STEPS = [ [[0, 1, PIECES['wQu']],  [0, 1, PIECES['wRk']],  [0, 1, PIECES['wBp']],  [0, 1, PIECES['wKn']]],
                                   [[1, 1, PIECES['wQu']],  [1, 1, PIECES['wRk']],  [1, 1, PIECES['wBp']],  [1, 1, PIECES['wKn']]],
                                   [[-1, 1, PIECES['wQu']], [-1, 1, PIECES['wRk']], [-1, 1, PIECES['wBp']], [-1, 1, PIECES['wKn']]] ]
        else:
            self.STEPS = [ [1, -1], [-1, -1] ]
            self.BACK_STEPS = [ [1, 1], [-1, 1] ]
            if(self.ypos > 1):
                self.GEN_STEPS = [ [[0, -1, PIECES['blk']]], [[0, -2, PIECES['blk']]], [[-1, -1, PIECES['blk']]], [[1, -1, PIECES['blk']]] ]
            else:
                self.GEN_STEPS = [ [[0, -1, PIECES['bQu']],  [0, -1, PIECES['bRk']],  [0, -1, PIECES['bBp']],  [0, -1, PIECES['bKn']]],
                                   [[1, -1, PIECES['bQu']],  [1, -1, PIECES['bRk']],  [1, -1, PIECES['bBp']],  [1, -1, PIECES['bKn']]],
                                   [[-1, -1, PIECES['bQu']], [-1, -1, PIECES['bRk']], [-1, -1, PIECES['bBp']], [-1, -1, PIECES['bKn']]] ]

    @classmethod
    def dir_for_move(cls, srcx, srcy, dstx, dsty):
        step_x = dstx - srcx
        step_y = dsty - srcy
        if(step_x == cls.STEP_1N_X and step_y == cls.STEP_1N_Y):
            return cls.DIRS['north']
        elif(step_x == cls.STEP_2N_X and step_y == cls.STEP_2N_Y and 
             srcy == cBoard.COORD['2']):
            return cls.DIRS['2north']
        elif(step_x == cls.STEP_1N1E_X and step_y == cls.STEP_1N1E_Y):
            return cls.DIRS['north-east']
        elif(step_x == cls.STEP_1N1W_X and step_y == cls.STEP_1N1W_Y):
            return cls.DIRS['north-west']
        elif(step_x == cls.STEP_1S_X and step_y == cls.STEP_1S_Y):
            return cls.DIRS['south']
        elif(step_x == cls.STEP_2S_X and step_y == cls.STEP_2S_Y and 
             srcy == cBoard.COORD['7']):
            return cls.DIRS['2south']
        elif(step_x == cls.STEP_1S1E_X and step_y == cls.STEP_1S1E_Y):
            return cls.DIRS['south-east']
        elif(step_x == cls.STEP_1S1W_X and step_y == cls.STEP_1S1W_Y):
            return cls.DIRS['south-west']
        else:
            return cls.DIRS['undefined']

    #step_for_dir(direction):
        # not used for pawn

    def is_trapped(self):
        return False # pawn cannot be trapped

    #is_piece_stuck(self):
        # works with inherited class

    #is_move_stuck(self, dstx, dsty)
        # works with inherited class

    def is_move_valid(self, dstx, dsty, prom_piece):
        move_dir = self.dir_for_move(self.xpos, self.ypos, dstx, dsty)
        if(move_dir == self.DIRS['undefined']):
            return False

        pin_dir = self.match.eval_pin_dir(self.xpos, self.ypos)

        dstpiece = self.match.readfield(dstx, dsty)

        if(self.color == COLORS['white']):
            # check pins
            if(move_dir == self.DIRS['north'] or move_dir == self.DIRS['2north']):
                if(pin_dir != self.DIRS['north'] and pin_dir != self.DIRS['south'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(move_dir == self.DIRS['north-west']):
                if(pin_dir != self.DIRS['north-west'] and pin_dir != self.DIRS['south-east'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(move_dir == self.DIRS['north-east']):
                if(pin_dir != self.DIRS['north-east'] and pin_dir != self.DIRS['south-west'] and pin_dir != self.DIRS['undefined']):
                    return False
            else:
                return False

            # check fields
            if(move_dir == self.DIRS['north'] and dstpiece != PIECES['blk']):
                return False
            elif(move_dir == self.DIRS['2north']):
                midpiece = self.match.readfield(dstx, self.ypos + self.STEP_1N_Y)
                if(midpiece != PIECES['blk'] or dstpiece != PIECES['blk']):
                    return False
            elif(move_dir == self.DIRS['north-west'] or move_dir == self.DIRS['north-east']):
                if(self.match.color_of_piece(dstpiece) != COLORS['black']):
                    return self.is_white_ep_move_ok(dstx, dsty)

            # check promotion
            if(dsty == 7 and prom_piece != PIECES['wQu'] and 
               prom_piece != PIECES['wRk'] and 
               prom_piece != PIECES['wBp'] and 
               prom_piece != PIECES['wKn']):
                return False
            elif(dsty < 7 and prom_piece != PIECES['blk']):
                return False
        else:
            # check pins
            if(move_dir == self.DIRS['south'] or move_dir == self.DIRS['2south']):
                if(pin_dir != self.DIRS['north'] and pin_dir != self.DIRS['south'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(move_dir == self.DIRS['south-east']):
                if(pin_dir != self.DIRS['north-west'] and pin_dir != self.DIRS['south-east'] and pin_dir != self.DIRS['undefined']):
                    return False
            elif(move_dir == self.DIRS['south-west']):
                if(pin_dir != self.DIRS['north-east'] and pin_dir != self.DIRS['south-west'] and pin_dir != self.DIRS['undefined']):
                    return False
            else:
                return False
            
            # check fields
            if(move_dir == self.DIRS['south'] and dstpiece != PIECES['blk']):
                return False
            elif(move_dir == self.DIRS['2south']):
                midpiece = self.match.readfield(dstx, self.ypos + self.STEP_1S_Y)
                if(midpiece != PIECES['blk'] or dstpiece != PIECES['blk']):
                    return False
            elif(move_dir == self.DIRS['south-east'] or move_dir == self.DIRS['south-west']):
                if(self.match.color_of_piece(dstpiece) != COLORS['white']):
                    return self.is_black_ep_move_ok(dstx, dsty)

            # check promotion
            if(dsty == 0 and prom_piece != PIECES['bQu'] and 
               prom_piece != PIECES['bRk'] and 
               prom_piece != PIECES['bBp'] and 
               prom_piece != PIECES['bKn']):
                return False
            elif(dsty > 0 and prom_piece != PIECES['blk']):
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
        
        if(prom_piece != PIECES['blk']):
            move.move_type = cMove.TYPES['promotion']
            move.captured_piece = dstpiece
            self.match.writefield(self.xpos, self.ypos, PIECES['blk'])
            self.match.writefield(dstx, dsty, prom_piece)
            self.match.score -= (SCORES[prom_piece] - SCORES[self.piece])
            self.match.score += SCORES[dstpiece]
        elif(dstpiece == PIECES['blk'] and self.xpos != dstx):
            move.move_type = cMove.TYPES['en_passant']
            move.e_p_fieldx = dstx
            move.e_p_fieldy = self.ypos
            move.captured_piece = self.match.readfield(move.e_p_fieldx, move.e_p_fieldy)
            self.match.writefield(self.xpos, self.ypos, PIECES['blk'])
            self.match.writefield(dstx, dsty, self.piece)
            self.match.writefield(move.e_p_fieldx, move.e_p_fieldy, PIECES['blk'])
            self.match.score += SCORES[move.captured_piece]
        else:
            move.captured_piece = dstpiece
            self.match.writefield(self.xpos, self.ypos, PIECES['blk'])
            self.match.writefield(dstx, dsty, self.piece)
            self.match.score += SCORES[dstpiece]

        if(self.match.color_of_piece(self.piece) == COLORS['white']):
            self.match.board.domove_white_movecnt_short_castling_lost(move.srcx, move.srcy, move.count)
            self.match.board.domove_white_movecnt_long_castling_lost(move.srcx, move.srcy, move.count)
        else:
            self.match.board.domove_black_movecnt_short_castling_lost(move.srcx, move.srcy, move.count)
            self.match.board.domove_black_movecnt_long_castling_lost(move.srcx, move.srcy, move.count)

        self.match.board.domove_counter(dstpiece)
        self.match.board.domove_fifty_moves_count(self.piece, dstpiece)

        self.match.move_list.append(move)
        return move

    def undo_move(self, move):
        if(move.move_type == move.TYPES['standard']):
            self.match.writefield(move.srcx, move.srcy, self.piece)
            self.match.writefield(move.dstx, move.dsty, move.captured_piece)
            self.match.score -= SCORES[move.captured_piece]
        elif(move.move_type == move.TYPES['promotion']):
            if(self.match.color_of_piece(self.piece) == COLORS['white']):
                origin = PIECES['wPw']
            else:
                origin = PIECES['bPw']
            self.match.writefield(move.srcx, move.srcy, origin)
            self.match.writefield(move.dstx, move.dsty, move.captured_piece)
            self.match.score += (SCORES[move.prom_piece] - SCORES[origin])
            self.match.score -= SCORES[move.captured_piece]
        elif(move.move_type == move.TYPES['en_passant']):
            self.match.writefield(move.srcx, move.srcy, self.piece)
            self.match.writefield(move.dstx, move.dsty, PIECES['blk'])
            self.match.writefield(move.e_p_fieldx, move.e_p_fieldy, move.captured_piece)
            self.match.score -= SCORES[move.captured_piece]

        if(self.match.color_of_piece(self.piece) == COLORS['white']):
            self.match.board.undomove_white_movecnt_short_castling_lost(move)
            self.match.board.undomove_white_movecnt_long_castling_lost(move)
        else:
            self.match.board.undomove_black_movecnt_short_castling_lost(move)
            self.match.board.undomove_black_movecnt_long_castling_lost(move)

        self.match.board.undomove_counter(move)
        self.match.board.undomove_fifty_moves_count(move)
        return move

    def is_white_ep_move_ok(self, dstx, dsty):
        if(len(self.match.move_list) == 0):
            return False
        else:
            lastmove = self.match.move_list[-1]

        dstpiece = self.match.readfield(dstx, dsty)
        enemy = self.match.readfield(lastmove.dstx, lastmove.dsty)
        if(dstpiece == PIECES['blk'] and enemy == PIECES['bPw']):
            if(lastmove.srcy - lastmove.dsty == 2 and 
               lastmove.dsty == self.ypos and 
               lastmove.dstx == dstx and 
               lastmove.dsty - dsty == -1):
                return True
        return False

    def is_black_ep_move_ok(self, dstx, dsty):
        if(len(self.match.move_list) == 0):
            return False
        else:
            lastmove = self.match.move_list[-1]

        dstpiece = self.match.readfield(dstx, dsty)
        enemy = self.match.readfield(lastmove.dstx, lastmove.dsty)
        if(dstpiece == PIECES['blk'] and enemy == PIECES['wPw']):
            if(lastmove.srcy - lastmove.dsty == -2 and 
               lastmove.dsty == self.ypos and 
               lastmove.dstx == dstx and 
               lastmove.dsty - dsty == 1):
                return True
        return False

    #find_attacks_and_supports(self, attacked, supported):
        # works with inherited class

    #forks(self):
        # works with inherited class

    #defends_fork(self)
        # works with inherited class

    #move_defends_fork(self, dstx, dsty)
        # works with inherited class

    def move_controles_file(self, dstx, dsty):
        return False

    #score_touches(self):
        # works with inherited class

    # list_moves(self):
       # works with inherited class

    # generate_moves(self):
       # works with inherited class

    # generate_priomoves(self):
       # works with inherited class

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
                x1, y1 = self.match.search(x1, y1, stepx, stepy)
                if(x1 is not None):
                    piece = self.match.readfield(x1, y1)
                    if(piece == opp_pawn):
                        return False
                else:
                    break
        return True

    def is_weak(self):
        from .. analyze_helper import list_all_field_touches
        friends, enemies = list_all_field_touches(self.match, self.color, self.xpos, self.ypos)
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
                x1, y1 = self.match.search(newx, self.ypos, newx, stepy)
                if(x1 is not None):
                    piece = self.match.readfield(x1, y1)
                    if((piece == PIECES['wPw'] or piece == PIECES['bPw']) and
                       self.color == self.match.color_of_piece(piece)):
                        return False
        return True

# class end

