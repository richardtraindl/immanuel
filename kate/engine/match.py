from datetime import datetime
from .board import cBoard
from .player import cPlayer
from .pieces.pawn import cPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .pieces import pawnfield, knightfield, rookfield, bishopfield, kingfield
from .validator import cValidator


class cMatch:
    STATUS = {
            'open' : 10,
            'draw' : 11,
            'winner_white' : 12,
            'winner_black' : 13,
            'paused' : 14 }

    LEVELS = {
            'blitz' : 0,
            'low' : 1,
            'medium' : 2,
            'high' : 3 }

    SECONDS_PER_MOVE = {
            LEVELS['blitz'] : 30,
            LEVELS['low'] : 60,
            LEVELS['medium'] : 90,
            LEVELS['high'] : 120 }

    PIECES = {
            'blk' : 0,
            'wKg' : 1,
            'wPw' : 2,
            'wRk' : 3,
            'wKn' : 4,
            'wBp' : 5,
            'wQu' : 6,
            'bKg' : 9,
            'bPw' : 10,
            'bRk' : 11,
            'bKn' : 12,
            'bBp' : 13,
            'bQu' : 14 
        }

    COLORS = {
            'undefined' : 0,
            'white' : 1,
            'black' : 9 
        }

    REVERSED_COLORS = { COLORS['undefined'] : COLORS['undefined'],
                        COLORS['white'] : COLORS['black'],
                        COLORS['black'] : COLORS['white'] }

    PIECES_COLOR = {
            PIECES['blk'] : COLORS['undefined'],
            PIECES['wKg'] : COLORS['white'],
            PIECES['wPw'] : COLORS['white'],
            PIECES['wRk'] : COLORS['white'],
            PIECES['wKn'] : COLORS['white'],
            PIECES['wBp'] : COLORS['white'],
            PIECES['wQu'] : COLORS['white'],
            PIECES['bKg'] : COLORS['black'],
            PIECES['bPw'] : COLORS['black'],
            PIECES['bRk'] : COLORS['black'],
            PIECES['bKn'] : COLORS['black'],
            PIECES['bBp'] : COLORS['black'],
            PIECES['bQu'] : COLORS['black'] }

    PIECES_RANK = {
            PIECES['blk'] : 0,
            PIECES['wPw'] : 2,
            PIECES['bPw'] : 2,
            PIECES['wKn'] : 4,
            PIECES['bKn'] : 4,
            PIECES['wBp'] : 4,
            PIECES['bBp'] : 4,
            PIECES['wRk'] : 5,
            PIECES['bRk'] : 5,
            PIECES['wQu'] : 7,
            PIECES['bQu'] : 7,
            PIECES['wKg'] : 9,
            PIECES['bKg'] : 9 }

    DIRS = {
        'north' : 1,
        'south' : 2,
        'east' : 3,
        'west' : 4,
        'north-east' : 5,
        'south-west' : 6,
        'north-west' : 7,
        'south-east' : 8,
        '2north' : 9,
        '2south' : 10,
        'sh-castling' : 11,
        'lg-castling' : 12,
        'valid' : 13,
        'undefined' : 14 
    }

    REVERSE_DIRS = {
        DIRS['north'] : DIRS['south'],
        DIRS['south'] : DIRS['north'],
        DIRS['east'] : DIRS['west'],
        DIRS['west'] : DIRS['east'],
        DIRS['north-east'] : DIRS['south-west'],
        DIRS['south-west'] : DIRS['north-east'],
        DIRS['north-west'] : DIRS['south-east'],
        DIRS['south-east'] : DIRS['north-west'],
        DIRS['2north'] : DIRS['2south'],
        DIRS['2south'] : DIRS['2north'],
        DIRS['sh-castling'] : DIRS['undefined'],
        DIRS['lg-castling'] : DIRS['undefined'],
        DIRS['valid'] : DIRS['valid'],
        DIRS['undefined'] : DIRS['undefined'] 
    }

    SCORES = { 
            PIECES['blk'] : 0,
            PIECES['wKg'] : -20000,
            PIECES['wPw'] : -100,
            PIECES['wRk'] : -500,
            PIECES['wKn'] : -336,
            PIECES['wBp'] : -340,
            PIECES['wQu'] : -950,
            PIECES['bKg'] : 20000,
            PIECES['bPw'] : 100,
            PIECES['bRk'] : 500,
            PIECES['bKn'] : 336,
            PIECES['bBp'] : 340,
            PIECES['bQu'] : 950 }

    SUPPORTED_SCORES = {
            PIECES['blk'] : 0,
            PIECES['wKg'] : 0,
            PIECES['wPw'] : 4,
            PIECES['wRk'] : 10,
            PIECES['wKn'] : 8,
            PIECES['wBp'] : 8,
            PIECES['wQu'] : 16,
            PIECES['bKg'] : 0,
            PIECES['bPw'] : -4,
            PIECES['bRk'] : -10,
            PIECES['bKn'] : -8,
            PIECES['bBp'] : -8,
            PIECES['bQu'] : -16 }

    ATTACKED_SCORES = {
            PIECES['blk'] : 0,
            PIECES['wKg'] : 0,
            PIECES['wPw'] : -4,
            PIECES['wRk'] : -10,
            PIECES['wKn'] : -8,
            PIECES['wBp'] : -8,
            PIECES['wQu'] : -16,
            PIECES['bKg'] : 0,
            PIECES['bPw'] : 4,
            PIECES['bRk'] : 10,
            PIECES['bKn'] : 8,
            PIECES['bBp'] : 8,
            PIECES['bQu'] : 16 }

    E1_X = 4
    E1_Y = 0
    A1_X = 0
    A1_Y = 0
    H1_X = 7
    H1_Y = 0
    E8_X = 4
    E8_Y = 7
    A8_X = 0
    A8_Y = 7
    H8_X = 7
    H8_Y = 7
    A2_Y = 1
    A7_Y = 6

    UNDEF_X = 8
    UNDEF_Y = 8

    def __init__(self):
        self.status = self.STATUS['open']
        self.movecnt = 0
        self.score = 0
        self.level = self.LEVELS['blitz']
        self.seconds_per_move = self.SECONDS_PER_MOVE[self.level]
        self.begin = datetime.now()
        self.time_start = 0
        self.white_player = cPlayer(self.COLORS['white'], "", True, 0)
        self.black_player = cPlayer(self.COLORS['black'], "", True, 0)
        self.board = cBoard(self.PIECES)
        self.fifty_moves_count = 0
        self.white_movecnt_short_castling_lost = 0
        self.white_movecnt_long_castling_lost = 0
        self.black_movecnt_short_castling_lost = 0
        self.black_movecnt_long_castling_lost = 0
        self.wKg_x = self.E1_X
        self.wKg_y = self.E1_Y
        self.bKg_x = self.E8_X
        self.bKg_y = self.E8_Y
        self.wQu_cnt = 1
        self.bQu_cnt = 1
        self.wOfficer_cnt = 6
        self.bOfficer_cnt = 6
        self.move_list = []

    def update_attributes(self):
        self.seconds_per_move = self.SECONDS_PER_MOVE[self.level]

        self.movecnt = len(self.move_list)
        if(self.movecnt > 0):
            move = self.move_list[-1]
            self.fifty_moves_count = move.fifty_moves_count

            for move in self.move_list:
                if(move.count % 2 == 1):
                    if(self.white_movecnt_short_castling_lost == 0):
                        if(move.srcx == self.E1_X and move.srcy == self.E1_Y):
                            self.white_movecnt_short_castling_lost = move.count
                        elif(move.srcx == self.H1_X and move.srcy == self.H1_Y):
                            self.white_movecnt_short_castling_lost = move.count
                            continue
                    if(self.white_movecnt_long_castling_lost == 0):
                        if(move.srcx == self.E1_X and move.srcy == self.E1_Y):
                            self.white_movecnt_long_castling_lost = move.count
                        elif(move.srcx == self.A1_X and move.srcy == self.A1_Y):
                            self.white_movecnt_long_castling_lost = move.count
                            continue
                else:
                    if(self.black_movecnt_short_castling_lost == 0):
                        if(move.srcx == self.E8_X and move.srcy == self.E8_Y):
                            self.black_movecnt_short_castling_lost = move.count
                        elif(move.srcx == self.H8_X and move.srcy == self.H8_Y):
                            self.black_movecnt_short_castling_lost = move.count
                            continue
                    if(self.black_movecnt_long_castling_lost == 0):
                        if(move.srcx == self.E8_X and move.srcy == self.E8_Y):
                            self.black_movecnt_long_castling_lost = move.count
                        elif(move.srcx == self.A8_X and move.srcy == self.A8_Y):
                            self.black_movecnt_long_castling_lost = move.count
                            continue

        self.score = 0
        self.wQu_cnt = 0
        self.bQu_cnt = 0
        self.wOfficer_cnt = 0
        self.bOfficer_cnt = 0
        for y in range(8):
            for x in range(8):
                piece = self.readfield(x, y)

                if(piece == self.PIECES['blk']):
                    continue
                else:
                    self.score -= self.SCORES[piece]

                if(piece == self.PIECES['wKg']):
                    self.wKg_x = x
                    self.wKg_y = y
                elif(piece == self.PIECES['bKg']):
                    self.bKg_x = x
                    self.bKg_y = y
                elif(piece == self.PIECES['wQu']):
                    self.wQu_cnt += 1
                elif(piece == self.PIECES['bQu']):
                    self.bQu_cnt += 1        
                elif(piece == self.PIECES['wRk'] or piece == self.PIECES['wBp'] or piece == self.PIECES['wKn']):
                    self.wOfficer_cnt += 1
                elif(piece == self.PIECES['bRk'] or piece == self.PIECES['bBp'] or piece == self.PIECES['bKn']):
                    self.bOfficer_cnt += 1

    def writefield(self, x, y, value):
        self.board.writefield(x, y, value)

    def readfield(self, x, y):
        return self.board.readfield(x, y)

    def search(self, srcx, srcy, stepx, stepy):
        return self.board.search(srcx, srcy, stepx, stepy)

    def is_next_color_human(self):
        if(self.movecnt % 2 == 0 ):
            return self.white_player.is_human
        else:
            return self.black_player.is_human

    def next_color(self):
        if(self.movecnt % 2 == 0 ):
            return self.COLORS['white']
        else:
            return self.COLORS['black']

    def is_last_move_capture(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            if(move.captured_piece != self.PIECES['blk']):
                return True

        return False

    def is_king_attacked(self, x1, y1):
        king = self.readfield(x1, y1)
        if(king != self.PIECES['wKg'] and king != self.PIECES['bKg']):
            return False
        color = self.color_of_piece(king)
        return self.is_field_touched(self.REVERSED_COLORS[color], x1, y1, 0)

    def is_last_move_promotion(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            if(move.prom_piece != self.PIECES['blk']):
                return True

        return False

    def read_move_list(self, idx):
        if(len(self.move_list) > 0):
            return self.move_list[idx]
        else:
            return None

    @classmethod
    def color_of_piece(cls, piece):
        return cls.PIECES_COLOR[piece]

    @classmethod
    def oppcolor_of_piece(cls, piece):
        color = cls.PIECES_COLOR[piece]
        return cls.REVERSED_COLORS[color]

    def is_inbounds(self, x, y):
        return self.board.is_inbounds(x, y)

    def is_move_inbounds(self, srcx, srcy, dstx, dsty):
        return self.board.is_move_inbounds(srcx, srcy, dstx, dsty)

    def is_move_valid(self, srcx, srcy, dstx, dsty, prom_piece):
        if(not self.is_move_inbounds(srcx, srcy, dstx, dsty)):
            return False, cValidator.RETURN_CODES['out-of-bounds']

        piece = self.readfield(srcx, srcy)

        if(self.next_color() != self.color_of_piece(piece)):
            return False, cValidator.RETURN_CODES['wrong-color']

        if(piece != self.PIECES['wKg'] and piece != self.PIECES['bKg']):
            if(self.is_king_after_move_attacked(srcx, srcy, dstx, dsty)):
                return False, cValidator.RETURN_CODES['king-error']

        if(piece == self.PIECES['wPw'] or piece == self.PIECES['bPw']):
            cpawn = cPawn(self, srcx, srcy)
            if(cpawn.is_move_valid(dstx, dsty, prom_piece)):
                return True, cValidator.RETURN_CODES['ok']
            else:
                return False, cValidator.RETURN_CODES['pawn-error']
        elif(piece == self.PIECES['wRk'] or piece == self.PIECES['bRk']):
            crook =  cRook(self, srcx, srcy)
            if(crook.is_move_valid(dstx, dsty)):
                return True, cValidator.RETURN_CODES['ok']
            else:
                return False, cValidator.RETURN_CODES['rook-error']
        elif(piece == self.PIECES['wKn'] or piece == self.PIECES['bKn']):
            cknight = cKnight(self, srcx, srcy)
            if(cknight.is_move_valid(dstx, dsty)):
                return True, cValidator.RETURN_CODES['ok']
            else:
                return False, cValidator.RETURN_CODES['knight-error']
        elif(piece == self.PIECES['wBp'] or piece == self.PIECES['bBp']):
            cbishop = cBishop(self, srcx, srcy)
            if(cbishop.is_move_valid(dstx, dsty)):
                return True, cValidator.RETURN_CODES['ok']
            else:
                return False, cValidator.RETURN_CODES['bishop-error']
        elif(piece == self.PIECES['wQu'] or piece == self.PIECES['bQu']):
            cqueen = cQueen(self, srcx, srcy)
            if(cqueen.is_move_valid(dstx, dsty)):
                return True, cValidator.RETURN_CODES['ok']
            else:
                return False, cValidator.RETURN_CODES['queen-error']
        elif(piece == self.PIECES['wKg'] or piece == self.PIECES['bKg']):
            cking = cKing(self, srcx, srcy)
            if(cking.is_move_valid(dstx, dsty)):
                return True, cValidator.RETURN_CODES['ok']
            else:
                return False, cValidator.RETURN_CODES['king-error']
        else:
            return False, cValidator.RETURN_CODES['general-error']

    def do_move(self, srcx, srcy, dstx, dsty, prom_piece):
        piece = self.readfield(srcx, srcy)

        if(piece == self.PIECES['wPw'] or piece == self.PIECES['bPw']):
            cpawn = cPawn(self, srcx, srcy)
            return cpawn.do_move(dstx, dsty, prom_piece)
        elif(piece == self.PIECES['wRk'] or piece == self.PIECES['bRk']):
            crook =  cRook(self, srcx, srcy)
            return crook.do_move(dstx, dsty, prom_piece)
        elif(piece == self.PIECES['wKn'] or piece == self.PIECES['bKn']):
            cknight = cKnight(self, srcx, srcy)
            return cknight.do_move(dstx, dsty, prom_piece)
        elif(piece == self.PIECES['wBp'] or piece == self.PIECES['bBp']):
            cbishop = cBishop(self, srcx, srcy)
            return cbishop.do_move(dstx, dsty, prom_piece)
        elif(piece == self.PIECES['wQu'] or piece == self.PIECES['bQu']):
            cqueen = cQueen(self, srcx, srcy)
            return cqueen.do_move(dstx, dsty, prom_piece)
        elif(piece == self.PIECES['wKg'] or piece == self.PIECES['bKg']):
            cking = cKing(self, srcx, srcy)
            return cking.do_move(dstx, dsty, prom_piece)

    def undo_move(self):
        if(len(self.move_list) > 0):
            move = self.move_list.pop()
        else:
            return None

        piece = self.readfield(move.dstx, move.dsty)

        if(move.move_type == move.TYPES['promotion'] or piece == self.PIECES['wPw'] or piece == self.PIECES['bPw']):
            cpawn = cPawn(self, move.dstx, move.dsty)
            return cpawn.undo_move(move)
        elif(piece == self.PIECES['wRk'] or piece == self.PIECES['bRk']):
            crook =  cRook(self, move.dstx, move.dsty)
            return crook.undo_move(move)
        elif(piece == self.PIECES['wKn'] or piece == self.PIECES['bKn']):
            cknight = cKnight(self, move.dstx, move.dsty)
            return cknight.undo_move(move)
        elif(piece == self.PIECES['wBp'] or piece == self.PIECES['bBp']):
            cbishop = cBishop(self, move.dstx, move.dsty)
            return cbishop.undo_move(move)
        elif(piece == self.PIECES['wQu'] or piece == self.PIECES['bQu']):
            cqueen = cQueen(self, move.dstx, move.dsty)
            return cqueen.undo_move(move)
        elif(piece == self.PIECES['wKg'] or piece == self.PIECES['bKg']):
            cking = cKing(self, move.dstx, move.dsty)
            return cking.undo_move(move)

    def is_king_after_move_attacked(self, srcx, srcy, dstx, dsty):
        piece = self.readfield(srcx, srcy)

        pawnenmy = None
        if(piece == self.PIECES['wPw']):
            cpawn = cPawn(self, srcx, srcy)
            if(cpawn.is_white_ep_move_ok(dstx, dsty)):
                pawnenmy = self.readfield(dstx, srcy)
                self.writefield(dstx, srcy, self.PIECES['blk'])
        elif(piece == self.PIECES['bPw']):
            cpawn = cPawn(self, srcx, srcy)
            if(cpawn.is_black_ep_move_ok(dstx, dsty)):
                pawnenmy = self.readfield(dstx, srcy)
                self.writefield(dstx, srcy, self.PIECES['blk'])

        self.writefield(srcx, srcy, self.PIECES['blk'])
        dstpiece = self.readfield(dstx, dsty)
        self.writefield(dstx, dsty, piece)

        if(self.color_of_piece(piece) == self.COLORS['white']):
            flag = self.is_field_touched(self.COLORS['black'], self.wKg_x, self.wKg_y, 0)
        else:
            flag = self.is_field_touched(self.COLORS['white'], self.bKg_x, self.bKg_y, 0)

        self.writefield(dstx, dsty, dstpiece)
        self.writefield(srcx, srcy, piece)
        if(pawnenmy):
            self.writefield(dstx, srcy, pawnenmy)

        return flag

    def is_field_touched(self, color, srcx, srcy, mode):
        crookfield = rookfield.cRookField(self, srcx, srcy)
        if(crookfield.is_field_touched(color, mode)):
            return True
        cbishopfield = bishopfield.cBishopField(self, srcx, srcy)
        if(cbishopfield.is_field_touched(color, mode)):
            return True
        cknightfield = knightfield.cKnightField(self, srcx, srcy)
        if(cknightfield.is_field_touched(color, mode)):
            return True
        ckingfield = kingfield.cKingField(self, srcx, srcy)
        if(ckingfield.is_field_touched(color)):
            return True
        cpawnfield = pawnfield.cPawnField(self, srcx, srcy)
        if(cpawnfield.is_field_touched(color, mode)):
            return True
        return False

    def is_move_available(self):
        color = self.next_color()
        for y1 in range(8):
            for x1 in range(8):
                piece = self.readfield(x1, y1)
                if(color == self.color_of_piece(piece)):
                    if(piece == self.PIECES['wPw'] and y1 == self.A7_Y):
                        prom_piece = self.PIECES['wQu']
                    elif(piece == self.PIECES['bPw'] and y1 == self.A2_Y):
                        prom_piece = self.PIECES['bQu']
                    else:
                        prom_piece = self.PIECES['blk']
                    for y2 in range(8):
                        for x2 in range(8):
                            flag = self.is_move_valid(x1, y1, x2, y2, prom_piece)[0]
                            if(flag):
                                return True
        return False

    def evaluate_status(self):
        if(self.is_move_available()):
            return self.STATUS['open']
        else:
            if(self.next_color() == self.COLORS['white']):
                if(self.is_field_touched(self.COLORS['black'], self.wKg_x, self.wKg_y, 0)):
                    return self.STATUS['winner_black']
            else:
                if(self.is_field_touched(self.COLORS['white'], self.bKg_x, self.bKg_y, 0)):
                    return self.STATUS['winner_white']
        return self.STATUS['draw']

    def evaluate_pin_dir(self, srcx, srcy):
        cpieces = [cRook, cBishop]
        white_faces = [self.PIECES['wRk'], self.PIECES['wBp']]
        black_faces = [self.PIECES['bRk'], self.PIECES['bBp']]

        for idx in range(2):
            piece = self.readfield(srcx, srcy)
            color = self.color_of_piece(piece)
            if(color == self.COLORS['white']):
                kgx = self.wKg_x
                kgy = self.wKg_y
            else:
                kgx = self.bKg_x
                kgy = self.bKg_y
            direction = cpieces[idx].dir_for_move(srcx, srcy, kgx, kgy)
            if(direction != self.DIRS['undefined']):
                stepx, stepy = cpieces[idx].step_for_dir(direction)
                dstx, dsty = self.search(srcx, srcy, stepx, stepy)
                if(dstx is not None):
                    piece = self.readfield(dstx, dsty)
                    if( (color == self.COLORS['white'] and piece == self.PIECES['wKg']) or
                        (color == self.COLORS['black'] and piece == self.PIECES['bKg']) ):
                        reverse_dir = self.REVERSE_DIRS[direction]
                        stepx, stepy = cpieces[idx].step_for_dir(reverse_dir)
                        dstx, dsty = self.search(srcx, srcy, stepx, stepy)
                        if(dstx is not None):
                            piece = self.readfield(dstx, dsty)
                            if(color == self.COLORS['white']):
                                if(piece == self.PIECES['bQu'] or piece == black_faces[idx]):
                                    return direction
                                else:
                                    return self.DIRS['undefined']
                            else:
                                if(piece == self.PIECES['wQu'] or piece == white_faces[idx]):
                                    return direction
                                else:
                                    return self.DIRS['undefined']
        return self.DIRS['undefined']

    def is_pinned(self, x, y):
        piece = self.readfield(x, y)
        direction = self.evaluate_pin_dir(x, y)
        return direction != self.DIRS['undefined']

    def is_soft_pin(self, srcx, srcy):
        piece = self.readfield(srcx, srcy)
        color = self.color_of_piece(piece)
        opp_color = self.oppcolor_of_piece(piece)
        crookfield = rookfield.cRookField(self, srcx, srcy)
        enemies = crookfield.list_field_touches(opp_color)        
        for enemy in enemies:
            enemy_dir = cRook.dir_for_move(srcx, srcy, enemy.fieldx, enemy.fieldy)
            stepx, stepy = cRook.step_for_dir(self.REVERSE_DIRS[enemy_dir])
            x1, y1 = self.search(srcx, srcy, stepx, stepy)
            if(x1 is not None):
                friend = self.readfield(x1, y1)
                if(self.color_of_piece(friend) == color and 
                   self.PIECES_RANK[friend] > self.PIECES_RANK[piece] and 
                   self.PIECES_RANK[friend] > self.PIECES_RANK[enemy.piece]):
                    return True

        enemies.clear()
        cbishopfield = bishopfield.cBishopField(self, srcx, srcy)
        enemies = cbishopfield.list_field_touches(opp_color) 
        for enemy in enemies:
            enemy_dir = cBishop.dir_for_move(srcx, srcy, enemy.fieldx, enemy.fieldy)
            stepx, stepy = cBishop.step_for_dir(self.REVERSE_DIRS[enemy_dir])
            x1, y1 = self.search(srcx, srcy, stepx, stepy)
            if(x1 is not None):
                friend = self.readfield(x1, y1)
                if(self.color_of_piece(friend) == color and 
                   self.PIECES_RANK[friend] > self.PIECES_RANK[piece] and 
                   self.PIECES_RANK[friend] > self.PIECES_RANK[enemy.piece]):
                    return True
        return False

# class end
