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
        self.board[0][0] = self.PIECES['wRk']
        self.board[0][1] = self.PIECES['wKn']
        self.board[0][2] = self.PIECES['wBp']
        self.board[0][3] = self.PIECES['wQu']
        self.board[0][4] = self.PIECES['wKg']
        self.board[0][5] = self.PIECES['wBp']
        self.board[0][6] = self.PIECES['wKn']
        self.board[0][7] = self.PIECES['wRk']
        for i in range(0, 8, 1):
            self.board[1][i] = self.PIECES['wPw']
        for j in range(2, 6, 1):
            for i in range(0, 8, 1):
                self.board[j][i] = self.PIECES['blk']
        for i in range(0, 8, 1):
            self.board[6][i] = self.PIECES['bPw']
        self.board[7][0] = self.PIECES['bRk']
        self.board[7][1] = self.PIECES['bKn']
        self.board[7][2] = self.PIECES['bBp']
        self.board[7][3] = self.PIECES['bQu']
        self.board[7][4] = self.PIECES['bKg']
        self.board[7][5] = self.PIECES['bBp']
        self.board[7][6] = self.PIECES['bKn']
        self.board[7][7] = self.PIECES['bRk']


    def do_move(self, srcx, srcy, dstx, dsty, prom_piece):
        prevmove = Move.objects.filter(match_id=self.id).order_by("count").last()
        if(prevmove == None):
            count = 1
        else:
            count = prevmove.count + 1

        self.count = count
        move = Move()
        move.match_id = self.id
        move.count = count

        srcpiece = self.readfield(srcx, srcy)
        dstpiece = self.readfield(dstx, dsty)
        if(srcpiece == Match.PIECES['wPw'] or srcpiece == Match.PIECES['bPw']):
            if(prom_piece != Match.PIECES['blk']):
                self.writefield(srcx, srcy, Match.PIECES['blk']) 
                self.writefield(dstx, dsty, prom_piece)
                move.move_type = move.TYPES['promotion']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.captured_piece = dstpiece
                move.prom_piece = prom_piece
                return move
            elif(dstpiece == Match.PIECES['blk'] and srcx != dstx):
                self.writefield(srcx, srcy, Match.PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                move.move_type = move.TYPES['en_passant']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.e_p_fieldx = dstx
                move.e_p_fieldy = srcy
                pawn = self.readfield(move.e_p_fieldx, move.e_p_fieldy)
                self.writefield(move.e_p_fieldx, move.e_p_fieldy, Match.PIECES['blk'])
                move.captured_piece = pawn
                return move 
        elif(srcpiece == Match.PIECES['wKg'] or srcpiece == Match.PIECES['bKg']):
            if(srcx - dstx == -2):
                self.writefield(srcx, srcy, Match.PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                rook = self.readfield(srcx + 3, srcy)
                self.writefield(srcx + 3, srcy, Match.PIECES['blk'])
                self.writefield(dstx - 1, dsty, rook)
                move.move_type = move.TYPES['short_castling']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.captured_piece = dstpiece
                return move
            elif(srcx - dstx == 2):
                self.writefield(srcx, srcy, Match.PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                rook = self.readfield(srcx - 4, srcy)
                self.writefield(srcx - 4, srcy, Match.PIECES['blk'])
                self.writefield(dstx + 1, dsty, rook)
                move.move_type = move.TYPES['long_castling']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.captured_piece = dstpiece
                return move
        self.writefield(srcx, srcy, Match.PIECES['blk'])
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
            if(move.dsty == 7):
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
      if(piece >= Match.PIECES['wKg'] and piece <= Match.PIECES['wQu']):
        return Match.COLORS['white']
      elif(piece >= Match.PIECES['bKg'] and piece <= Match.PIECES['bQu']):
        return Match.COLORS['black']
      else:
        return Match.COLORS['undefined']


class Move(models.Model):
    TYPES = {
        'standard' : 1,
        'short_castling' : 2,
        'long_castling' : 3,
        'promotion' : 4,
        'en_passant' : 5 }

    match= models.ForeignKey(Match, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(null=False)
    move_type = models.PositiveSmallIntegerField(null=False, default=TYPES['standard'])
    srcx = models.PositiveSmallIntegerField(null=False)
    srcy = models.PositiveSmallIntegerField(null=False)
    dstx = models.PositiveSmallIntegerField(null=False)
    dsty = models.PositiveSmallIntegerField(null=False)
    e_p_fieldx = models.PositiveSmallIntegerField(null=True)
    e_p_fieldy = models.PositiveSmallIntegerField(null=True)
    captured_piece = models.PositiveSmallIntegerField(null=False, default=Match.PIECES['blk'])
    prom_piece = models.PositiveSmallIntegerField(null=False, default=Match.PIECES['blk'])

    def format_move(self):
        if(self.move_type == self.TYPES['standard']):
            if(self.captured_piece == 0):
                hyphen = "-"
            else:
                hyphen = "x"
            fmtmove= values.index_to_koord(self.srcx, self.srcy) + hyphen + values.index_to_koord(self.dstx, self.dsty)
            return fmtmove
        elif(self.move_type == self.TYPES['short_castling']):
            return "0-0"
        elif(self.move_type == self.TYPES['long_castling']):
            return "0-0-0"
        elif(self.move_type == self.TYPES['promotion']):
            if(self.captured_piece == 0):
                hyphen = "-"
            else:
                hyphen = "x"
            fmtmove= values.index_to_koord(self.srcx, self.srcy) + hyphen + values.index_to_koord(self.dstx, self.dsty) + " " + reverse_lookup(PIECES, self.prom_piece)
            return fmtmove
        else:
            fmtmove= values.index_to_koord(self.srcx, self.srcy) + "x" + values.index_to_koord(self.dstx, self.dsty) + " e.p."
            return fmtmove



class Comment(models.Model):
    match= models.ForeignKey(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=500)


