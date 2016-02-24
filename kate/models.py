from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.db.models.signals import post_save
from kate.modules import values


class Match(models.Model):
    COLORS = {
        'undefined' : 0,
        'white' : 1,
        'black' : 9 }

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
        'bQu' : 14 }

    STATUS = {
        'open' : 1,
        'draw' : 2,
        'winner_white' : 3,
        'winner_black' : 4,
        'cancelled' : 5 }

    status = models.PositiveSmallIntegerField(null=False, default=STATUS['open'])
    score = models.SmallIntegerField(null=False, default=0)
    begin = models.DateTimeField(default=timezone.now)
    white_player = models.CharField(max_length=100, blank=False)
    black_player = models.CharField(max_length=100, blank=False)
    board = ArrayField(ArrayField(models.PositiveSmallIntegerField(null=False, blank=False, default=PIECES['blk']), size=8), size=8)

    def writefield(self, x, y, value):
        self.board[y][x] = value


    def readfield(self, x, y):
        return self.board[y][x]


    def setboardbase(self):
        self.board = [ [0  for x in range(8)] for x in range(8) ]
        self.board[0][0] = PIECES['wRk']
        self.board[0][1] = PIECES['wKn']
        self.board[0][2] = PIECES['wBp']
        self.board[0][3] = PIECES['wQu']
        self.board[0][4] = PIECES['wKg']
        self.board[0][5] = PIECES['wBp']
        self.board[0][6] = PIECES['wKn']
        self.board[0][7] = PIECES['wRk']
        for i in range(0, 8, 1):
            self.board[1][i] = PIECES['wPw']
        for j in range(2, 6, 1):
            for i in range(0, 8, 1):
                self.board[j][i] = PIECES['blk']
        for i in range(0, 8, 1):
            self.board[6][i] = PIECES['bPw']
        self.board[7][0] = PIECES['bRk']
        self.board[7][1] = PIECES['bKn']
        self.board[7][2] = PIECES['bBp']
        self.board[7][3] = PIECES['bQu']
        self.board[7][4] = PIECES['bKg']
        self.board[7][5] = PIECES['bBp']
        self.board[7][6] = PIECES['bKn']
        self.board[7][7] = PIECES['bRk']


    def do_move(self, srcx, srcy, dstx, dsty, prom_piece):
        prev_move = Move.objects.filter(match_id=self.id).order_by("count").last()
        if(prev_move == None):
            count = 1
        else:
            count = prev_move.count + 1

        self.count = count
        move = Move()
        move.match_id = self.id
        move.count = count

        srcpiece = self.readfield(srcx, srcy)
        dstpiece = self.readfield(dstx, dsty)
        if(srcpiece == PIECES['wPw'] or srcpiece == PIECES['bPw']):
            if(prom_piece != PIECES['blk']):
                self.writefield(srcx, srcy, PIECES['blk']) 
                self.writefield(dstx, dsty, prom_piece)
                move.move_type = move.TYPES['promotion']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.captured_piece = dstpiece
                move.prom_piece = prom_piece
                return move
            elif(dstpiece == PIECES['blk'] and srcx != dstx):
                self.writefield(srcx, srcy, PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                move.move_type = move.TYPES['en_passant']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.e_p_fieldx = dstx
                move.e_p_fieldy = srcy
                pawn = self.readfield(move.e_p_fieldx, move.e_p_fieldy)
                self.writefield(move.e_p_fieldx, move.e_p_fieldy, PIECES['blk'])
                move.captured_piece = pawn
                return move 
        elif(srcpiece == PIECES['wKg'] or srcpiece == PIECES['bKg']):
            if(srcidx - dstidx == -2):
                self.writefield(srcx, srcy, PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                rook = self.readfield(srcidx + 3, srcy)
                self.writefield(srcx + 3, srcy, PIECES['blk'])
                self.writefield(dstx - 1, dsty, rook)
                move.move_type = move.TYPES['short_castling']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.captured_piece = destpiece
                return move
            elif(srcx - dstx == 2):
                self.writefield(srcx, srcy, PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                rook = self.readfield(srcx - 4, srcy)
                self.writefield(srcx - 4, srcy, PIECES['blk'])
                self.writefield(dstx + 1, dsty, rook)
                move.move_type = move.TYPES['long_castling']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.captured_piece = destpiece
                return move
        self.writefield(srcx, srcy, PIECES['blk'])
        self.writefield(dstx, dsty, srcpiece)
        move.move_type = move.TYPES['standard']
        move.srcx = srcx
        move.srcy = srcy
        move.dstx = dstx
        move.dsty = dsty
        move.captured_piece = dstpiece
        return move


    def undo_move(self):
        move = Move.objects.filter(match_id=self.id).order_by("count").last()
        if(move == None):
            return None
        if(move.move_type == move.TYPES['standard']):
            piece = self.readfield(move.dstx, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, move.captured_piece)
            return move
        elif(move.move_type == move.TYPES['short_castling']):
            piece = self.readfield(move.dstx, move.dsty)
            rook = self.readfield(move.dstx - 1, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, values.PIECES['blk'])
            self.writefield(move.dstx - 1, move.dsty, values.PIECES['blk'])
            self.writefield(move.dstx + 1, move.dsty, rook)
            return move
        elif(move.move_type == move.TYPES['long_castling']):
            piece = self.readfield(move.dstx, move.dsty)
            rook = self.readfield(move.dstx + 1, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, PIECES['blk'])
            self.writefield(move.dstx + 1, move.dsty, PIECES['blk'])
            self.writefield(move.dstx - 2, move.dsty, rook)
            return move
        elif(move.move_type == move.TYPES['promotion']):
            if(move.desty == 7):
                piece = PIECES['wPw']
            else:
                piece = PIECES['bPw']
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, move.captured_piece)
            return move
        else:
            piece = self.readfield(move.dstx, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, PIECES['blk'])
            self.writefield(move.e_p_fieldx, move.e_p_fieldy, move.captured_piece)
            return move

    @staticmethod
    def color_of_piece(piece):
      if(piece >= PIECES['wKg'] and piece <= PIECES['wQu']):
        return COLORS['white']
      elif(piece >= PIECES['bKg'] and piece <= PIECES['bQu']):
        return COLORS['black']
      else:
        return COLORS['undefined']


class Move(models.Model):
    TYPES = {
        'standard' : 1,
        'short_castling' : 2,
        'long_castling' : 3,
        'promotion' : 4,
        'en_passant' : 5 }

    match= models.ForeignKey(Match, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(null=False)
    move_type = models.PositiveSmallIntegerField(null=False, TYPES['standard'])
    srcx = models.PositiveSmallIntegerField(null=False)
    srcy = models.PositiveSmallIntegerField(null=False)
    dstx = models.PositiveSmallIntegerField(null=False)
    dsty = models.PositiveSmallIntegerField(null=False)
    e_p_fieldx = models.PositiveSmallIntegerField(null=True)
    e_p_fieldy = models.PositiveSmallIntegerField(null=True)
    captured_piece = models.PositiveSmallIntegerField(null=False, default=PIECES['blk'])
    prom_piece = models.PositiveSmallIntegerField(null=False, default=PIECES['blk'])

    def format_move(move):
        if(move.move_type == TYPES['standard']):
            if(move.captured_piece == 0):
                hyphen = "-"
            else:
                hyphen = "x"
            fmtmove= index_to_koord(move.srcx, move.srcy) + hyphen + index_to_koord(move.dstx, move.dsty)
            return fmtmove
        elif(move.move_type == TYPES['short_castling']):
            return "0-0"
        elif(move.move_type == TYPES['long_castling']):
            return "0-0-0"
        elif(move.move_type == TYPES['promotion']):
            if(move.captured_piece == 0):
                hyphen = "-"
            else:
                hyphen = "x"
            fmtmove= index_to_koord(move.srcx, move.srcy) + hyphen + index_to_koord(move.dstx, move.dsty) + " " + reverse_lookup(PIECES, move.prom_piece)
            return fmtmove
        else:
            fmtmove= index_to_koord(move.srcx, move.srcy) + "x" + index_to_koord(move.dstx, move.dsty) + " e.p."
            return fmtmove



class Comment(models.Model):
    match= models.ForeignKey(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=500)


