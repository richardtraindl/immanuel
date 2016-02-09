from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.db.models.signals import post_save
from kate.modules import values


class Match(models.Model):
    active = models.PositiveSmallIntegerField(null=False, default=1)
    begin = models.DateTimeField(default=timezone.now)
    white_player = models.CharField(max_length=100, blank=False)
    black_player = models.CharField(max_length=100, blank=False)
    board = models.CharField(max_length=256)

    def writeboard(self, arrboard):
        fields = ''
        for rows in arrboard:
            for col in rows:
                fields += reverse_lookup(PIECES, value)
                fields += ','
        self.board = fields

    def readboard(self):
        arrboard = [[0 for x in range(8)] for x in range(8)]
        row = 0
        col = 0
        fieldsarr = self.board.split(',')
        for field in fieldsarr:
            arrboard[row][col] = values.PIECES[field]
            col += 1
            if col == 8:
                row += 1
                col = 0
        return arrboard

    def readfield(self, idx):
        fields = self.board.split(',')
        return fields[idx]

    def writefield(self, idx, key):
        fields = self.board.split(',')
        fields[idx] = key
        newfields = ''
        for i in range(len(fields)):
            newfields += fields[i]
            newfields += ','
        self.board = newfields[:255]


    def setboardbase(self):
        self.board = ('wRk,wKn,wBp,wQu,wKg,wBp,wKn,wRk,' 
                        'wPw,wPw,wPw,wPw,wPw,wPw,wPw,wPw,'
                        'blk,blk,blk,blk,blk,blk,blk,blk,'
                        'blk,blk,blk,blk,blk,blk,blk,blk,'
                        'blk,blk,blk,blk,blk,blk,blk,blk,'
                        'blk,blk,blk,blk,blk,blk,blk,blk,'
                        'bPw,bPw,bPw,bPw,bPw,bPw,bPw,bPw,'
                        'bRk,bKn,bBp,bQu,bKg,bBp,bKn,bRk')

    def do_move(self, srcidx, destidx, prom_piece):
        prev_move = Move.objects.filter(match_id=self.id).order_by("count").last()
        if(prev_move == None):
            count = 1
        else:
            count = prev_move.count
            count += 1
        move = Move()
        move.match_id = self.id
        move.count = count
        
        srcpiece = self.readfield(srcidx)
        destpiece = self.readfield(destidx)
        if(srcpiece == 'wPw' or srcpiece == 'bPw'):
            if(prom_piece != 'blk'):
                self.writefield(srcidx, 'blk')
                self.writefield(destidx, prom_piece)
                move.move_type = values.MOVE_TYPES['promotion']
                move.src = srcidx
                move.dest = destidx
                move.captured_piece = values.PIECES[destpiece]
                move.prom_piece = values.PIECES[prom_piece]
                return move
            elif(destpiece == 'blk' and not values.is_incol(srcidx, destidx)):
                self.writefield(srcidx, 'blk')
                self.writefield(destidx, srcpiece)
                move.move_type = values.MOVE_TYPES['en_passant']
                move.src = srcidx
                move.dest = destidx
                row = srcidx // 8
                col = destidx % 8
                move.e_p_field = row * 8 + col
                pawn = self.readfield(move.e_p_field)
                self.writefield(move.e_p_field, 'blk')
                move.captured_piece = values.PIECES[pawn]                
                return move 
        elif(srcpiece == 'wKg' or srcpiece == 'bKg'):
            if(srcidx - destidx == -2):
                self.writefield(srcidx, 'blk')
                self.writefield(destidx, srcpiece)
                rook = self.readfield(srcidx + 3)
                self.writefield(srcidx + 3, 'blk')
                self.writefield(destidx - 1, rook)
                move.move_type = values.MOVE_TYPES['short_castling']
                move.src = srcidx
                move.dest = destidx
                move.captured_piece = values.PIECES[destpiece]
                return move
            elif(srcidx - destidx == 2):
                self.writefield(srcidx, 'blk')
                self.writefield(destidx, srcpiece)
                rook = self.readfield(srcidx - 4)
                self.writefield(srcidx - 4, 'blk')
                self.writefield(destidx + 1, rook)
                move.move_type = values.MOVE_TYPES['long_castling']
                move.src = srcidx
                move.dest = destidx
                move.captured_piece = values.PIECES[destpiece]
                return move

        self.writefield(srcidx, 'blk')
        self.writefield(destidx, srcpiece)
        move.move_type = values.MOVE_TYPES['standard']
        move.src = srcidx
        move.dest = destidx
        move.captured_piece = values.PIECES[destpiece]
        return move

    def undo_move(self):
        move = Move.objects.filter(match_id=self.id).order_by("count").last()
        if(move == None):
            return None
        if(move.move_type == values.MOVE_TYPES['standard']):
            piece = self.readfield(move.dest)
            self.writefield(move.src, piece)
            self.writefield(move.dest, values.reverse_lookup(values.PIECES, move.captured_piece))
            return move
        elif(move.move_type == values.MOVE_TYPES['short_castling']):
            piece = self.readfield(move.dest)
            rook = self.readfield(move.dest - 1)
            self.writefield(move.src, piece)
            self.writefield(move.dest, 'blk')
            self.writefield(move.dest - 1, 'blk')
            self.writefield(move.dest + 1, rook)
            return move
        elif(move.move_type == values.MOVE_TYPES['long_castling']):
            piece = self.readfield(move.dest)
            rook = self.readfield(move.dest + 1)
            self.writefield(move.src, piece)
            self.writefield(move.dest, 'blk')
            self.writefield(move.dest + 1, 'blk')
            self.writefield(move.dest - 2, rook)
            return move
        elif(move.move_type == values.MOVE_TYPES['promotion']):
            if((move.dest // 8) == 7):
                piece = 'wPw'
            else:
                piece = 'bPw'
            self.writefield(move.src, piece)
            self.writefield(move.dest, values.reverse_lookup(values.PIECES, move.captured_piece))
            return move
        else:
            piece = self.readfield(move.dest)
            self.writefield(move.src, piece)
            self.writefield(move.dest, 'blk')
            self.writefield(move.e_p_field, values.reverse_lookup(values.PIECES, move.captured_piece))
            return move


class Move(models.Model):
    match= models.ForeignKey(Match)
    count = models.PositiveSmallIntegerField(null=False)
    move_type = models.PositiveSmallIntegerField(null=False, default=1)
    src = models.PositiveSmallIntegerField(null=False)
    dest = models.PositiveSmallIntegerField(null=False)
    e_p_field = models.PositiveSmallIntegerField(null=True)
    captured_piece = models.PositiveSmallIntegerField(null=False, default=0)
    prom_piece = models.PositiveSmallIntegerField(null=False, default=0)



class Comment(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=500)

