from . piece import *


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

    def do_move(self, dstx, dsty, prom_piece):
        move = cMove(self.match, 
                    self.match.movecnt + 1, 
                    cMove.TYPES['standard'],
                    self.xpos, 
                    self.ypos, 
                    dstx, 
                    dsty, 
                    None,
                    None,
                    self.match.PIECES['blk'], 
                    prom_piece, 
                    self.match.fifty_moves_count)

        srcpiece = self.match.readfield(move.srcx, move.srcy)
        dstpiece = self.match.readfield(move.dstx, move.dsty)

        if(srcpiece == self.match.PIECES['wKg']):
            self.match.wKg_x = move.dstx
            self.match.wKg_y = move.dsty

            if(self.match.white_movecnt_short_castling_lost == 0):
                self.match.white_movecnt_short_castling_lost = self.match.movecnt + 1

            if(self.match.white_movecnt_long_castling_lost == 0):
                self.match.white_movecnt_long_castling_lost = self.match.movecnt + 1
        else:
            self.match.bKg_x = move.dstx
            self.match.bKg_y = move.dsty

            if(self.match.black_movecnt_short_castling_lost == 0):
                self.match.black_movecnt_short_castling_lost = self.match.movecnt + 1

            if(self.match.black_movecnt_long_castling_lost == 0):
                self.match.black_movecnt_long_castling_lost = self.match.movecnt + 1

        if(move.dstx - move.srcx == 2):
            move.move_type = cMove.TYPES['short_castling']
            move.captured_piece = dstpiece
            self.match.movecnt += 1   

            self.match.writefield(move.srcx, move.srcy, self.match.PIECES['blk'])
            self.match.writefield(move.dstx, move.dsty, srcpiece)
            rook = self.match.readfield(move.srcx + 3, move.srcy)
            self.match.writefield(move.srcx + 3, move.srcy, self.match.PIECES['blk'])
            self.match.writefield(move.dstx - 1, move.dsty, rook)
            self.match.fifty_moves_count += 1

            self.match.move_list.append(move)
            return move
        elif(move.dstx - move.srcx == -2):
            move.move_type = cMove.TYPES['long_castling']
            move.captured_piece = dstpiece
            self.match.movecnt += 1   

            self.match.writefield(move.srcx, move.srcy, self.match.PIECES['blk'])
            self.match.writefield(move.dstx, move.dsty, srcpiece)
            rook = self.match.readfield(move.srcx - 4, move.srcy)
            self.match.writefield(move.srcx - 4, move.srcy, self.match.PIECES['blk'])
            self.match.writefield(move.dstx + 1, move.dsty, rook)
            self.match.fifty_moves_count += 1

            self.match.move_list.append(move)
            return move
        else:
            move.captured_piece = dstpiece

            self.match.movecnt += 1
            self.match.writefield(move.srcx, move.srcy, self.match.PIECES['blk'])
            self.match.writefield(move.dstx, move.dsty, srcpiece)
            if(dstpiece != self.match.PIECES['blk']):
                self.match.fifty_moves_count = 0
                move.fifty_moves_count = self.match.fifty_moves_count
            else:
                self.match.fifty_moves_count += 1
                move.fifty_moves_count = self.match.fifty_moves_count

            self.match.score += self.match.SCORES[dstpiece]
            self.match.move_list.append(move)
            return move

    def undo_move(self, move):
        if(move.captured_piece == self.match.PIECES['wQu']):
            self.match.wQu_cnt += 1
        elif(move.captured_piece == self.match.PIECES['bQu']):
            self.match.bQu_cnt += 1
        elif(move.captured_piece == self.match.PIECES['wKn'] or move.captured_piece == self.match.PIECES['wBp'] or move.captured_piece == self.match.PIECES['wRk']):
            self.match.wOfficer_cnt += 1
        elif(move.captured_piece == self.match.PIECES['bKn'] or move.captured_piece == self.match.PIECES['bBp'] or move.captured_piece == self.match.PIECES['bRk']):
            self.match.bOfficer_cnt += 1

        self.match.movecnt -= 1
        self.match.fifty_moves_count = move.fifty_moves_count

        piece = self.match.readfield(move.dstx, move.dsty)
        self.match.writefield(move.srcx, move.srcy, piece)
        self.match.writefield(move.dstx, move.dsty, move.captured_piece)

        self.match.score -= self.match.SCORES[move.captured_piece]

        if(move.move_type == move.TYPES['short_castling']):
            rook = self.match.readfield(move.dstx - 1, move.dsty)
            self.match.writefield(move.dstx - 1, move.dsty, self.match.PIECES['blk'])
            self.match.writefield(move.dstx + 1, move.dsty, rook)

            if(piece == self.match.PIECES['wKg']):
                self.match.wKg_x = move.srcx
                self.match.wKg_y = move.srcy

                self.match.white_movecnt_short_castling_lost = 0
                if(self.match.white_movecnt_long_castling_lost == self.match.movecnt + 1):
                    self.match.white_movecnt_long_castling_lost = 0
            else:
                self.match.bKg_x = move.srcx
                self.match.bKg_y = move.srcy

                self.match.black_movecnt_short_castling_lost = 0
                if(self.match.black_movecnt_long_castling_lost == self.match.movecnt + 1):
                    self.match.black_movecnt_long_castling_lost = 0
        elif(move.move_type == move.TYPES['long_castling']):
            rook = self.match.readfield(move.dstx + 1, move.dsty)
            self.match.writefield(move.dstx + 1, move.dsty, self.match.PIECES['blk'])
            self.match.writefield(move.dstx - 2, move.dsty, rook)
        
            if(piece == self.match.PIECES['wKg']):
                self.match.wKg_x = move.srcx
                self.match.wKg_y = move.srcy

                self.match.white_movecnt_long_castling_lost = 0
                if(self.match.white_movecnt_short_castling_lost == self.match.movecnt + 1):
                    self.match.white_movecnt_short_castling_lost = 0
            else:
                self.match.bKg_x = move.srcx
                self.match.bKg_y = move.srcy

                self.match.black_movecnt_long_castling_lost = 0
                if(self.match.black_movecnt_short_castling_lost == self.match.movecnt + 1):
                    self.match.black_movecnt_short_castling_lost = 0
        else:
            if(piece == self.match.PIECES['wKg']):
                self.match.wKg_x = move.srcx
                self.match.wKg_y = move.srcy
                if(self.match.white_movecnt_short_castling_lost == self.match.movecnt + 1):
                    self.match.white_movecnt_short_castling_lost = 0
                if(self.match.white_movecnt_long_castling_lost == self.match.movecnt + 1):
                    self.match.white_movecnt_long_castling_lost = 0
            else:
                self.match.bKg_x = move.srcx
                self.match.bKg_y = move.srcy
                if(self.match.black_movecnt_short_castling_lost == self.match.movecnt + 1):
                    self.match.black_movecnt_short_castling_lost = 0
                if(self.match.black_movecnt_long_castling_lost == self.match.movecnt + 1):
                    self.match.black_movecnt_long_castling_lost = 0

        return move

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

    def move_defends_forked_field(self, dstx, dsty):
        from .. analyze_helper import is_fork_field

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

                if(piece == self.match.PIECES['blk'] or self.match.color_of_piece(piece) == self.color):
                    if(is_fork_field(self.match, self.color, x1, y1)):
                        #cfork = cFork(srcx, srcy, dstx, dsty, x1, y1)
                        #analyses.lst_fork_defended.append(cfork)
                        return True

        return False

    def move_controles_file(self, dstx, dsty):
        return False

    def score_attacks(self):
        from .. analyze_helper import list_all_field_touches

        score = 0

        opp_color = self.match.oppcolor_of_piece(self.piece)

        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                attacked = self.match.readfield(x1, y1)

                if(self.match.color_of_piece(attacked) == opp_color):
                    score += self.match.ATTACKED_SCORES[attacked]

                    # extra score if attacked is pinned
                    enmy_pin = self.match.evaluate_pin_dir(x1, y1) #opp_color, 
                    if(enmy_pin != self.DIRS['undefined']):
                        score += self.match.ATTACKED_SCORES[attacked]

                    if(self.match.is_soft_pin(x1, y1)):
                        score += self.match.ATTACKED_SCORES[attacked]
        return score

    def score_supports(self):
        score = 0

        opp_color = self.match.oppcolor_of_piece(self.piece)

        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                if(x1 == self.xpos and y1 == self.ypos):
                    continue

                supported = self.match.readfield(x1, y1)

                if(self.match.color_of_piece(supported) == self.color):
                    if(self.match.is_field_touched(opp_color, x1, y1, 1)):
                        score += self.match.SUPPORTED_SCORES[supported]
        return score 

    def is_king_safe(match, color):
        from .. analyze_helper import list_all_field_touches

        for step in self.STEPS:
            x1 = self.xpos + step[0]
            y1 = self.ypos + step[1]
            if(self.match.is_inbounds(x1, y1)):
                friends, enemies = list_all_field_touches(self.match, self.color, x1, y1)
                if(len(friends) < len(enemies)):
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
                direction, step_x, step_y = cRook.step_for_dir(direction)
            else:
                direction = cBishop.dir_for_move(self.xpos, self.ypos, enemy.fieldx, enemy.fieldy)
                if(direction != self.DIRS['undefined']):
                    direction, step_x, step_y = cBishop.step_for_dir(direction)
                else:
                    return False

            x1 = self.xpos + step_x
            y1 = self.ypos + step_y
            while(self.match.is_inbounds(x1, y1)):
                blocking_friends, blocking_enemies = list_all_field_touches(self.match, self.color, x1, y1)
                if(len(blocking_friends) > 0):
                    break
        return True

# class end

