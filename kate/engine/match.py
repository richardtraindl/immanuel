from datetime import datetime
from .values import *
from .board import cBoard
from .player import cPlayer
from .pieces.pawn import cPawn
from .pieces.knight import cKnight
from .pieces.bishop import cBishop
from .pieces.rook import cRook
from .pieces.king import cKing
from .pieces.queen import cQueen
from .pieces.pawnfield import cPawnField
from .pieces.knightfield import cKnightField
from .pieces.rookfield import cRookField
from .pieces.bishopfield import cBishopField
from .pieces.kingfield import cKingField


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

    RETURN_CODES = {
        'ok' : 10,
        'draw' : 11,
        'winner_white' : 12,
        'winner_black' : 13,
        'match-cancelled' : 14,
        'wrong-color' : 15,
        'pawn-error' : 20,
        'rook-error' : 21,
        'knight-error' : 22,
        'bishop-error' : 23,
        'queen-error' : 24,
        'king-error' : 25,
        'format-error' : 30,
        'out-of-bounds' : 31,
        'general-error' : 40,
    }

    RETURN_MSGS = {
        RETURN_CODES['ok'] : "move okay",
        RETURN_CODES['draw'] : "draw",
        RETURN_CODES['winner_white'] : "winner white",
        RETURN_CODES['winner_black'] : "winner black",
        RETURN_CODES['match-cancelled'] : " match is cancelled",
        RETURN_CODES['wrong-color'] : "wrong color",
        RETURN_CODES['pawn-error'] : "pawn error",
        RETURN_CODES['rook-error'] : "rook error",
        RETURN_CODES['knight-error'] : "knight error",
        RETURN_CODES['bishop-error'] : "bishop error",
        RETURN_CODES['queen-error'] : "queen error",
        RETURN_CODES['king-error'] : "king error",
        RETURN_CODES['format-error'] : "format wrror",
        RETURN_CODES['out-of-bounds'] : "wrong square",
        RETURN_CODES['general-error'] : "general error",
    }

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
        self.white_player = cPlayer(COLORS['white'], "", True, 0)
        self.black_player = cPlayer(COLORS['black'], "", True, 0)
        self.board = cBoard()
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

                if(piece == PIECES['blk']):
                    continue
                else:
                    self.score -= SCORES[piece]

                if(piece == PIECES['wKg']):
                    self.wKg_x = x
                    self.wKg_y = y
                elif(piece == PIECES['bKg']):
                    self.bKg_x = x
                    self.bKg_y = y
                elif(piece == PIECES['wQu']):
                    self.wQu_cnt += 1
                elif(piece == PIECES['bQu']):
                    self.bQu_cnt += 1        
                elif(piece == PIECES['wRk'] or piece == PIECES['wBp'] or piece == PIECES['wKn']):
                    self.wOfficer_cnt += 1
                elif(piece == PIECES['bRk'] or piece == PIECES['bBp'] or piece == PIECES['bKn']):
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
            return COLORS['white']
        else:
            return COLORS['black']

    def is_opening(self):
        return self.movecnt <= 30

    def is_endgame(self):
        count = self.wQu_cnt + self.wOfficer_cnt + self.bQu_cnt + self.bOfficer_cnt
        return count <= 6

    def is_last_move_capture(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            if(move.captured_piece != PIECES['blk']):
                return True

        return False

    def is_king_attacked(self, x1, y1):
        king = self.readfield(x1, y1)
        if(king != PIECES['wKg'] and king != PIECES['bKg']):
            return False
        color = self.color_of_piece(king)
        return self.is_field_touched(REVERSED_COLORS[color], x1, y1, 0)

    def is_last_move_promotion(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            if(move.prom_piece != PIECES['blk']):
                return True

        return False

    def read_move_list(self, idx):
        if(len(self.move_list) > 0):
            return self.move_list[idx]
        else:
            return None

    @classmethod
    def color_of_piece(cls, piece):
        return PIECES_COLOR[piece]

    @classmethod
    def oppcolor_of_piece(cls, piece):
        color = PIECES_COLOR[piece]
        return REVERSED_COLORS[color]

    def is_inbounds(self, x, y):
        return self.board.is_inbounds(x, y)

    def is_move_inbounds(self, srcx, srcy, dstx, dsty):
        return self.board.is_move_inbounds(srcx, srcy, dstx, dsty)

    def is_move_valid(self, srcx, srcy, dstx, dsty, prom_piece):
        if(not self.is_move_inbounds(srcx, srcy, dstx, dsty)):
            return False, self.RETURN_CODES['out-of-bounds']

        piece = self.readfield(srcx, srcy)

        if(self.next_color() != self.color_of_piece(piece)):
            return False, self.RETURN_CODES['wrong-color']

        if(piece != PIECES['wKg'] and piece != PIECES['bKg']):
            if(self.is_king_after_move_attacked(srcx, srcy, dstx, dsty)):
                return False, self.RETURN_CODES['king-error']

        if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
            cpawn = cPawn(self, srcx, srcy)
            if(cpawn.is_move_valid(dstx, dsty, prom_piece)):
                return True, self.RETURN_CODES['ok']
            else:
                return False, self.RETURN_CODES['pawn-error']
        elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
            crook = cRook(self, srcx, srcy)
            if(crook.is_move_valid(dstx, dsty)):
                return True, self.RETURN_CODES['ok']
            else:
                return False, self.RETURN_CODES['rook-error']
        elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
            cknight = cKnight(self, srcx, srcy)
            if(cknight.is_move_valid(dstx, dsty)):
                return True, self.RETURN_CODES['ok']
            else:
                return False, self.RETURN_CODES['knight-error']
        elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
            cbishop = cBishop(self, srcx, srcy)
            if(cbishop.is_move_valid(dstx, dsty)):
                return True, self.RETURN_CODES['ok']
            else:
                return False, self.RETURN_CODES['bishop-error']
        elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
            cqueen = cQueen(self, srcx, srcy)
            if(cqueen.is_move_valid(dstx, dsty)):
                return True, self.RETURN_CODES['ok']
            else:
                return False, self.RETURN_CODES['queen-error']
        elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
            cking = cKing(self, srcx, srcy)
            if(cking.is_move_valid(dstx, dsty)):
                return True, self.RETURN_CODES['ok']
            else:
                return False, self.RETURN_CODES['king-error']
        else:
            return False, self.RETURN_CODES['general-error']

    def do_move(self, srcx, srcy, dstx, dsty, prom_piece):
        piece = self.readfield(srcx, srcy)

        if(piece == PIECES['wPw'] or piece == PIECES['bPw']):
            cpawn = cPawn(self, srcx, srcy)
            return cpawn.do_move(dstx, dsty, prom_piece)
        elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
            crook =  cRook(self, srcx, srcy)
            return crook.do_move(dstx, dsty, prom_piece)
        elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
            cknight = cKnight(self, srcx, srcy)
            return cknight.do_move(dstx, dsty, prom_piece)
        elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
            cbishop = cBishop(self, srcx, srcy)
            return cbishop.do_move(dstx, dsty, prom_piece)
        elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
            cqueen = cQueen(self, srcx, srcy)
            return cqueen.do_move(dstx, dsty, prom_piece)
        elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
            cking = cKing(self, srcx, srcy)
            return cking.do_move(dstx, dsty, prom_piece)

    def undo_move(self):
        if(len(self.move_list) > 0):
            move = self.move_list.pop()
        else:
            return None

        piece = self.readfield(move.dstx, move.dsty)

        if(move.move_type == move.TYPES['promotion'] or piece == PIECES['wPw'] or piece == PIECES['bPw']):
            cpawn = cPawn(self, move.dstx, move.dsty)
            return cpawn.undo_move(move)
        elif(piece == PIECES['wRk'] or piece == PIECES['bRk']):
            crook =  cRook(self, move.dstx, move.dsty)
            return crook.undo_move(move)
        elif(piece == PIECES['wKn'] or piece == PIECES['bKn']):
            cknight = cKnight(self, move.dstx, move.dsty)
            return cknight.undo_move(move)
        elif(piece == PIECES['wBp'] or piece == PIECES['bBp']):
            cbishop = cBishop(self, move.dstx, move.dsty)
            return cbishop.undo_move(move)
        elif(piece == PIECES['wQu'] or piece == PIECES['bQu']):
            cqueen = cQueen(self, move.dstx, move.dsty)
            return cqueen.undo_move(move)
        elif(piece == PIECES['wKg'] or piece == PIECES['bKg']):
            cking = cKing(self, move.dstx, move.dsty)
            return cking.undo_move(move)

    def is_king_after_move_attacked(self, srcx, srcy, dstx, dsty):
        piece = self.readfield(srcx, srcy)

        pawnenmy = None
        if(piece == PIECES['wPw']):
            cpawn = cPawn(self, srcx, srcy)
            if(cpawn.is_white_ep_move_ok(dstx, dsty)):
                pawnenmy = self.readfield(dstx, srcy)
                self.writefield(dstx, srcy, PIECES['blk'])
        elif(piece == PIECES['bPw']):
            cpawn = cPawn(self, srcx, srcy)
            if(cpawn.is_black_ep_move_ok(dstx, dsty)):
                pawnenmy = self.readfield(dstx, srcy)
                self.writefield(dstx, srcy, PIECES['blk'])

        self.writefield(srcx, srcy, PIECES['blk'])
        dstpiece = self.readfield(dstx, dsty)
        self.writefield(dstx, dsty, piece)

        if(self.color_of_piece(piece) == COLORS['white']):
            flag = self.is_field_touched(COLORS['black'], self.wKg_x, self.wKg_y, 0)
        else:
            flag = self.is_field_touched(COLORS['white'], self.bKg_x, self.bKg_y, 0)

        self.writefield(dstx, dsty, dstpiece)
        self.writefield(srcx, srcy, piece)
        if(pawnenmy):
            self.writefield(dstx, srcy, pawnenmy)

        return flag

    def is_field_touched(self, color, srcx, srcy, mode):
        crookfield = cRookField(self, srcx, srcy)
        if(crookfield.is_field_touched(color, mode)):
            return True
        cbishopfield = cBishopField(self, srcx, srcy)
        if(cbishopfield.is_field_touched(color, mode)):
            return True
        cknightfield = cKnightField(self, srcx, srcy)
        if(cknightfield.is_field_touched(color, mode)):
            return True
        ckingfield = cKingField(self, srcx, srcy)
        if(ckingfield.is_field_touched(color)):
            return True
        cpawnfield = cPawnField(self, srcx, srcy)
        if(cpawnfield.is_field_touched(color, mode)):
            return True
        return False

    def is_move_available(self):
        color = self.next_color()
        for y1 in range(8):
            for x1 in range(8):
                piece = self.readfield(x1, y1)
                if(color == self.color_of_piece(piece)):
                    if(piece == PIECES['wPw'] and y1 == self.A7_Y):
                        prom_piece = PIECES['wQu']
                    elif(piece == PIECES['bPw'] and y1 == self.A2_Y):
                        prom_piece = PIECES['bQu']
                    else:
                        prom_piece = PIECES['blk']
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
            if(self.next_color() == COLORS['white']):
                if(self.is_field_touched(COLORS['black'], self.wKg_x, self.wKg_y, 0)):
                    return self.STATUS['winner_black']
            else:
                if(self.is_field_touched(COLORS['white'], self.bKg_x, self.bKg_y, 0)):
                    return self.STATUS['winner_white']
        return self.STATUS['draw']

    def evaluate_pin_dir(self, srcx, srcy):
        cpieces = [cRook, cBishop]
        white_faces = [PIECES['wRk'], PIECES['wBp']]
        black_faces = [PIECES['bRk'], PIECES['bBp']]

        for idx in range(2):
            piece = self.readfield(srcx, srcy)
            color = self.color_of_piece(piece)
            if(color == COLORS['white']):
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
                    if( (color == COLORS['white'] and piece == PIECES['wKg']) or
                        (color == COLORS['black'] and piece == PIECES['bKg']) ):
                        reverse_dir = self.REVERSE_DIRS[direction]
                        stepx, stepy = cpieces[idx].step_for_dir(reverse_dir)
                        dstx, dsty = self.search(srcx, srcy, stepx, stepy)
                        if(dstx is not None):
                            piece = self.readfield(dstx, dsty)
                            if(color == COLORS['white']):
                                if(piece == PIECES['bQu'] or piece == black_faces[idx]):
                                    return direction
                                else:
                                    return self.DIRS['undefined']
                            else:
                                if(piece == PIECES['wQu'] or piece == white_faces[idx]):
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
        crookfield = cRookField(self, srcx, srcy)
        enemies = crookfield.list_field_touches(opp_color)        
        for enemy in enemies:
            enemy_dir = cRook.dir_for_move(srcx, srcy, enemy.fieldx, enemy.fieldy)
            stepx, stepy = cRook.step_for_dir(self.REVERSE_DIRS[enemy_dir])
            x1, y1 = self.search(srcx, srcy, stepx, stepy)
            if(x1 is not None):
                friend = self.readfield(x1, y1)
                if(self.color_of_piece(friend) == color and 
                   PIECES_RANK[friend] > PIECES_RANK[piece] and 
                   PIECES_RANK[friend] > PIECES_RANK[enemy.piece]):
                    return True

        enemies.clear()
        cbishopfield = cBishopField(self, srcx, srcy)
        enemies = cbishopfield.list_field_touches(opp_color) 
        for enemy in enemies:
            enemy_dir = cBishop.dir_for_move(srcx, srcy, enemy.fieldx, enemy.fieldy)
            stepx, stepy = cBishop.step_for_dir(self.REVERSE_DIRS[enemy_dir])
            x1, y1 = self.search(srcx, srcy, stepx, stepy)
            if(x1 is not None):
                friend = self.readfield(x1, y1)
                if(self.color_of_piece(friend) == color and 
                   PIECES_RANK[friend] > PIECES_RANK[piece] and 
                   PIECES_RANK[friend] > PIECES_RANK[enemy.piece]):
                    return True
        return False

# class end
