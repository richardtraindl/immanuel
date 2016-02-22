from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.db.models.signals import post_save
from kate.modules import values


class Match(models.Model):
    status = models.PositiveSmallIntegerField(null=False, default=1)
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
        self.board[0][i] = Pieces.wRk
        self.board[0][i] = Pieces.wKn
        self.board[0][i] = Pieces.wBp
        self.board[0][i] = Pieces.wQu
        self.board[0][i] = Pieces.wKg
        self.board[0][i] = Pieces.wBp
        self.board[0][i] = Pieces.wKn
        self.board[0][i] = Pieces.wRk
        for i in range(0, 8, 1):
            self.board[1][i] = Pieces.wPw
        for j in range(2, 6, 1):
            for i in range(0, 8, 1):
                self.board[j][i] = Pieces.blk
        for i in range(0, 8, 1):
            self.board[6][i] = Pieces.bPw
        self.board[0][i] = Pieces.bRk
        self.board[0][i] = Pieces.bKn
        self.board[0][i] = Pieces.bBp
        self.board[0][i] = Pieces.bQu
        self.board[0][i] = Pieces.bKg
        self.board[0][i] = Pieces.bBp
        self.board[0][i] = Pieces.bKn
        self.board[0][i] = Pieces.bRk


    def do_move(self, srcx, srcy, destx, desty, prom_piece):
        prev_move = Move.objects.filter(match_id=self.id).order_by("count").last()
        if(prev_move == None):
            count = 1
        else:
            count = prev_move.count
            count += 1
        move = Move()
        move.match_id = self.id
        move.count = count
        
        srcpiece = self.readfield(srcx, srcy)
        destpiece = self.readfield(destx, desty)
        if(srcpiece == Pieces.wPw or srcpiece == Pieces.bPw):
            if(prom_piece != Pieces.blk):
                self.writefield(srcx, srcy, Pieces.blk) 
                self.writefield(destx, desty, prom_piece)
                move.move_type = MoveTypes.promotion
                move.srcx = srcidx
                move.srcy = srcidy
                move.destx = destidx
                move.desty = destidy
                move.captured_piece = destpiece
                move.prom_piece = prom_piece
                return move
            elif(destpiece == Pieces.blk and srcx != destx):
                self.writefield(srcx, srcy, Pieces.blk)
                self.writefield(destx, desty, srcpiece)
                move.move_type = MoveTypes.en_passant
                move.srcx = srcx
                move.srcy = srcy
                move.destx = destx
                move.desty = desty
                move.e_p_fieldx = destx
                move.e_p_fieldy = srcy
                pawn = self.readfield(move.e_p_fieldx, move.e_p_fieldy)
                self.writefield(move.e_p_fieldx, move.e_p_fieldy, Pieces.blk)
                move.captured_piece = pawn
                return move 
        elif(srcpiece == Pieces.wKg or srcpiece == Pieces.bKg):
            if(srcidx - destidx == -2):
                self.writefield(srcx, srcy, Pieces.blk)
                self.writefield(destx, desty, srcpiece)
                rook = self.readfield(srcidx + 3, srcy)
                self.writefield(srcx + 3, srcy, Pieces.blk)
                self.writefield(destx - 1, desty, rook)
                move.move_type = MoveTypes.short_castling
                move.srcx = srcx
                move.srcy = srcy
                move.destx = destx
                move.desty = desty
                move.captured_piece = destpiece
                return move
            elif(srcx - destx == 2):
                self.writefield(srcx, srcy, Pieces.blk)
                self.writefield(destx, desty, srcpiece)
                rook = self.readfield(srcx - 4, srcy)
                self.writefield(srcx - 4, srcy, Pieces.blk)
                self.writefield(destx + 1, desty, rook)
                move.move_type = MoveTypes.long_castling
                move.srcx = srcx
                move.srcy = srcy
                move.desxt = destx
                move.desty = desty
                move.captured_piece = destpiece
                return move
        self.writefield(srcx, srcy, Pieces.blk)
        self.writefield(destx, desty, srcpiece)
        move.move_type = MoveTypes.standard
        move.srcx = srcy
        move.srcy = srcy
        move.destx = destx
        move.desty = desty
        move.captured_piece = destpiece
        return move


    def undo_move(self):
        move = Move.objects.filter(match_id=self.id).order_by("count").last()
        if(move == None):
            return None
        if(move.move_type == MoveTypes.standard):
            piece = self.readfield(move.destx, move.desty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.destx, move.desty, move.captured_piece)
            return move
        elif(move.move_type == MoveTypes.short_castling):
            piece = self.readfield(move.destx, move.desty)
            rook = self.readfield(move.destx - 1, move.desty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.destx, move.desty, Pieces.blk)
            self.writefield(move.destx - 1, move.desty, Pieces.blk)
            self.writefield(move.destx + 1, move.desty, rook)
            return move
        elif(move.move_type == MoveTypes.long_castling):
            piece = self.readfield(move.destx, move.desty)
            rook = self.readfield(move.destx + 1, move.desty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.destx, move.desty, Pieces.blk)
            self.writefield(move.destx + 1, move.desty, Pieces.blk)
            self.writefield(move.destx - 2, move.desty, rook)
            return move
        elif(move.move_type == MoveTypes.promotion):
            if(move.desty == 7):
                piece = Pieces.wPw
            else:
                piece = Pieces.bPw
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.destx, move.desty, move.captured_piece)
            return move
        else:
            piece = self.readfield(move.destx, move.desty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.destx, move.desty, Pieces.blk)
            self.writefield(move.e_p_fieldx, move.e_p_fieldy, move.captured_piece)
            return move


class Move(models.Model):
    match= models.ForeignKey(Match, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(null=False)
    move_type = models.PositiveSmallIntegerField(null=False, default=1)
    srcx = models.PositiveSmallIntegerField(null=False)
    srcy = models.PositiveSmallIntegerField(null=False)
    destx = models.PositiveSmallIntegerField(null=False)
    desty = models.PositiveSmallIntegerField(null=False)
    e_p_fieldx = models.PositiveSmallIntegerField(null=True)
    e_p_fieldy = models.PositiveSmallIntegerField(null=True)
    captured_piece = models.PositiveSmallIntegerField(null=False, default=0)
    prom_piece = models.PositiveSmallIntegerField(null=False, default=0)


class Comment(models.Model):
    match= models.ForeignKey(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=500)


