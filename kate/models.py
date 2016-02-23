from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.db.models.signals import post_save
from kate.modules import values


class Match(models.Model):
    status = models.PositiveSmallIntegerField(null=False, default=1)
    count = models.SmallIntegerField(null=False, default=0)
    score = models.SmallIntegerField(null=False, default=0)
    begin = models.DateTimeField(default=timezone.now)
    white_player = models.CharField(max_length=100, blank=False)
    black_player = models.CharField(max_length=100, blank=False)
    board = ArrayField(ArrayField(models.PositiveSmallIntegerField(null=False, blank=False, default=0), size=8), size=8)

    def writefield(self, x, y, value):
        self.board[y][x] = value
    
    
    def readfield(self, x, y):
        return self.board[y][x]


    def setboardbase(self):
        
        self.board = [ [0  for x in range(8)] for x in range(8) ]
        self.board[0][0] = values.PIECES['wRk']
        self.board[0][1] = values.PIECES['wKn']
        self.board[0][2] = values.PIECES['wBp']
        self.board[0][3] = values.PIECES['wQu']
        self.board[0][4] = values.PIECES['wKg']
        self.board[0][5] = values.PIECES['wBp']
        self.board[0][6] = values.PIECES['wKn']
        self.board[0][7] = values.PIECES['wRk']
        for i in range(0, 8, 1):
            self.board[1][i] = values.PIECES['wPw']
        for j in range(2, 6, 1):
            for i in range(0, 8, 1):
                self.board[j][i] = values.PIECES['blk']
        for i in range(0, 8, 1):
            self.board[6][i] = values.PIECES['bPw']
        self.board[7][0] = values.PIECES['bRk']
        self.board[7][1] = values.PIECES['bKn']
        self.board[7][2] = values.PIECES['bBp']
        self.board[7][3] = values.PIECES['bQu']
        self.board[7][4] = values.PIECES['bKg']
        self.board[7][5] = values.PIECES['bBp']
        self.board[7][6] = values.PIECES['bKn']
        self.board[7][7] = values.PIECES['bRk']


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
        if(srcpiece == values.PIECES['wPw'] or srcpiece == values.PIECES['bPw']):
            if(prom_piece != values.PIECES['blk']):
                self.writefield(srcx, srcy, values.PIECES['blk']) 
                self.writefield(dstx, dsty, prom_piece)
                move.move_type = values.MOVE_TYPES['promotion']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.captured_piece = dstpiece
                move.prom_piece = prom_piece
                return move
            elif(dstpiece == values.PIECES['blk'] and srcx != dstx):
                self.writefield(srcx, srcy, values.PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                move.move_type = values.MOVE_TYPES['en_passant']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.e_p_fieldx = dstx
                move.e_p_fieldy = srcy
                pawn = self.readfield(move.e_p_fieldx, move.e_p_fieldy)
                self.writefield(move.e_p_fieldx, move.e_p_fieldy, values.PIECES['blk'])
                move.captured_piece = pawn
                return move 
        elif(srcpiece == values.PIECES['wKg'] or srcpiece == values.PIECES['bKg']):
            if(srcidx - dstidx == -2):
                self.writefield(srcx, srcy, values.PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                rook = self.readfield(srcidx + 3, srcy)
                self.writefield(srcx + 3, srcy, values.PIECES['blk'])
                self.writefield(dstx - 1, dsty, rook)
                move.move_type = values.MOVE_TYPES['short_castling']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.captured_piece = destpiece
                return move
            elif(srcx - dstx == 2):
                self.writefield(srcx, srcy, values.PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                rook = self.readfield(srcx - 4, srcy)
                self.writefield(srcx - 4, srcy, values.PIECES['blk'])
                self.writefield(dstx + 1, dsty, rook)
                move.move_type = values.MOVE_TYPES['long_castling']
                move.srcx = srcx
                move.srcy = srcy
                move.dstx = dstx
                move.dsty = dsty
                move.captured_piece = destpiece
                return move
        self.writefield(srcx, srcy, values.PIECES['blk'])
        self.writefield(dstx, dsty, srcpiece)
        move.move_type = values.MOVE_TYPES['standard']
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
        if(move.move_type == values.MOVE_TYPES['standard']):
            piece = self.readfield(move.dstx, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, move.captured_piece)
            return move
        elif(move.move_type == values.values.MOVE_TYPES['short_castling']):
            piece = self.readfield(move.dstx, move.dsty)
            rook = self.readfield(move.dstx - 1, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, values.PIECES['blk'])
            self.writefield(move.dstx - 1, move.dsty, values.PIECES['blk'])
            self.writefield(move.dstx + 1, move.dsty, rook)
            return move
        elif(move.move_type == values.MOVE_TYPES['long_castling']):
            piece = self.readfield(move.dstx, move.dsty)
            rook = self.readfield(move.dstx + 1, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, values.PIECES['blk'])
            self.writefield(move.dstx + 1, move.dsty, values.PIECES['blk'])
            self.writefield(move.dstx - 2, move.dsty, rook)
            return move
        elif(move.move_type == values.MOVE_TYPES['promotion']):
            if(move.desty == 7):
                piece = values.PIECES['wPw']
            else:
                piece = values.PIECES['bPw']
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, move.captured_piece)
            return move
        else:
            piece = self.readfield(move.dstx, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, PIECES['blk'])
            self.writefield(move.e_p_fieldx, move.e_p_fieldy, move.captured_piece)
            return move


class Move(models.Model):
    match= models.ForeignKey(Match, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(null=False)
    move_type = models.PositiveSmallIntegerField(null=False, default=1)
    srcx = models.PositiveSmallIntegerField(null=False)
    srcy = models.PositiveSmallIntegerField(null=False)
    dstx = models.PositiveSmallIntegerField(null=False)
    dsty = models.PositiveSmallIntegerField(null=False)
    e_p_fieldx = models.PositiveSmallIntegerField(null=True)
    e_p_fieldy = models.PositiveSmallIntegerField(null=True)
    captured_piece = models.PositiveSmallIntegerField(null=False, default=0)
    prom_piece = models.PositiveSmallIntegerField(null=False, default=0)


class Comment(models.Model):
    match= models.ForeignKey(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=500)


