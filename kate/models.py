from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.db.models.signals import post_save
from kate.modules import values
import threading


class Match(models.Model):
    COLORS = {
        'undefined' : 0,
        'white' : 1,
        'black' : 9 
    }

    REVERSED_COLORS = {
        COLORS['undefined'] : COLORS['undefined'],
        COLORS['white'] : COLORS['black'],
        COLORS['black'] : COLORS['white'] 
    }

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

    SCORES = {
        PIECES['blk'] : 0,
        PIECES['wKg'] : -20000,
        PIECES['wPw'] : -100,
        PIECES['wRk'] : -500,
        PIECES['wKn'] : -330,
        PIECES['wBp'] : -350,
        PIECES['wQu'] : -950,
        PIECES['bKg'] : 20000,
        PIECES['bPw'] : 100,
        PIECES['bRk'] : 500,
        PIECES['bKn'] : 330,
        PIECES['bBp'] : 350,
        PIECES['bQu'] : 950
    }

    STATUS = {
        'open' : 1,
        'draw' : 2,
        'winner_white' : 3,
        'winner_black' : 4,
        'cancelled' : 5 }

    LEVEL = {
        'medium' : 1,
        'high' : 2,
        'professional' : 3,
        'blitz' : 4 }

    status = models.PositiveSmallIntegerField(null=False, default=STATUS['open'])
    count = models.SmallIntegerField(null=False, default=0)
    score = models.IntegerField(null=False, default=0)    
    begin = models.DateTimeField(default=timezone.now)
    white_player = models.CharField(max_length=100, blank=False)
    white_player_human = models.BooleanField(null=False, default=True)
    black_player = models.CharField(max_length=100, blank=False)
    black_player_human = models.BooleanField(null=False, default=True)
    level = models.SmallIntegerField(null=False, default=1)
    board = ArrayField(ArrayField(models.PositiveSmallIntegerField(null=False, blank=False, default=PIECES['blk']), size=8), size=8)
    fifty_moves_count = models.SmallIntegerField(null=False, default=0)
    wKg_x = models.SmallIntegerField(null=False, default=0)
    wKg_y = models.SmallIntegerField(null=False, default=0)
    bKg_x = models.SmallIntegerField(null=False, default=0)
    bKg_y = models.SmallIntegerField(null=False, default=0)
    wKg_first_movecnt = models.SmallIntegerField(null=False, default=0)
    bKg_first_movecnt = models.SmallIntegerField(null=False, default=0)
    wRk_a1_first_movecnt = models.SmallIntegerField(null=False, default=0)
    wRk_h1_first_movecnt = models.SmallIntegerField(null=False, default=0)
    bRk_a8_first_movecnt = models.SmallIntegerField(null=False, default=0)
    bRk_h8_first_movecnt = models.SmallIntegerField(null=False, default=0)
    immanuels_thread_lock = threading.Lock()
    immanuels_threads_list = []

    def __init__(self, *args, **kwargs):
        super(Match, self).__init__(*args, **kwargs)
        self.move_list = []

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
        self.fifty_moves_count = 0
        self.wKg_x = 4
        self.wKg_y = 0
        self.bKg_x = 4
        self.bKg_y = 7
        self.wKg_first_movecnt = 0
        self.bKg_first_movecnt = 0
        self.wRk_a1_first_movecnt = 0
        self.wRk_h1_first_movecnt = 0
        self.bRk_a8_first_movecnt = 0
        self.bRk_h8_first_movecnt = 0

    def fill_fmtboard(self, switch):
        fmtboard = [ [ [0  for k in range(2)] for x in range(8)] for x in range(8) ]
        if(switch == 0):
            rowstart = 7
            rowend = -1
            rowstep = -1
            colstart = 0
            colend = 8
            colstep = 1
        else:
            rowstart = 0
            rowend = 8
            rowstep = 1
            colstart = 7
            colend = -1
            colstep = -1
        idx1 = 0
        for i in range(rowstart, rowend, rowstep):
            idx2 = 0
            for j in range(colstart, colend, colstep):
                fmtboard[idx1][idx2][0] = self.board[i][j]
                field = chr(ord('a') + j) + chr(ord('1') + i)
                fmtboard[idx1][idx2][1] = field
                idx2 += 1
            idx1 += 1
        return fmtboard

    def html_board(self, switch, movesrc, movedst):
        fmtboard = self.fill_fmtboard(switch)
        htmldata = "<table id='board' matchid='" + str(self.id) + "' movecnt='" + str(self.count) + "'>"
        htmldata += "<tr id='board-letters1'><td>&nbsp;</td>"
        if(switch == 0):
            for i in range(8):
                htmldata += "<td>" + chr(i + ord('A')) + "</td>"
        else:
            for i in range(8):
                htmldata += "<td>" + chr(ord('H') - i) + "</td>"
        htmldata += "<td>&nbsp;</td></tr>"
        for row in fmtboard:
            htmldata += "<tr><td class='board-label'>" + str(row[0][1])[1] + "</td>"
            for col in row:
                if(col[1] == movesrc or col[1] == movedst):
                    htmldata += "<td id='" + str(col[1]) + "' class='hint' value='" + str(col[0]) + "'>"
                else:
                    htmldata += "<td id='" + str(col[1]) + "' value='" + str(col[0]) + "'>"
    
                if(col[0] == 0):
                    htmldata += "&nbsp;"
                else:
                    piece = values.reverse_lookup(Match.PIECES, col[0])
                    htmldata += "<img src='" + "/static/img/" + piece + ".png'>"
                htmldata += "</td>"
            htmldata += "<td class='board-label'>" + str(row[0][1])[1] + "</td></tr>"
        htmldata += "<tr id='board-letters2'><td>&nbsp;</td>"
        if(switch == 0):
            for i in range(8):
                htmldata += "<td>" + chr(i + ord('A')) + "</td>"
        else:
            for i in range(8):
                htmldata += "<td>" + chr(ord('H') - i) + "</td>"
        htmldata += "<td>&nbsp;</td></tr></table>"
        return htmldata

    def do_move(self, srcx, srcy, dstx, dsty, prom_piece):
        self.count += 1
        move = Move()
        move.match_id = self.id
        move.count = self.count
        move.srcx = srcx
        move.srcy = srcy
        move.dstx = dstx
        move.dsty = dsty
        move.fifty_moves_count = self.fifty_moves_count        
        srcpiece = self.readfield(srcx, srcy)
        dstpiece = self.readfield(dstx, dsty)
        if(srcpiece == Match.PIECES['wPw'] or srcpiece == self.PIECES['bPw']):
            if(prom_piece != Match.PIECES['blk']):
                self.writefield(srcx, srcy, self.PIECES['blk']) 
                self.writefield(dstx, dsty, prom_piece)
                self.fifty_moves_count = 0
                move.move_type = move.TYPES['promotion']
                move.captured_piece = dstpiece
                move.prom_piece = prom_piece
                self.score -= (self.SCORES[prom_piece] - self.SCORES[srcpiece])
                self.score += self.SCORES[dstpiece]
                return move
            elif(dstpiece == Match.PIECES['blk'] and srcx != dstx):
                self.writefield(srcx, srcy, self.PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                self.fifty_moves_count = 0
                move.move_type = move.TYPES['en_passant']
                move.e_p_fieldx = dstx
                move.e_p_fieldy = srcy
                pawn = self.readfield(move.e_p_fieldx, move.e_p_fieldy)
                self.writefield(move.e_p_fieldx, move.e_p_fieldy, self.PIECES['blk'])
                move.captured_piece = pawn
                self.score += self.SCORES[pawn]
                return move 
        elif(srcpiece == Match.PIECES['wKg'] or srcpiece == self.PIECES['bKg']):
            if(srcx - dstx == -2):
                self.writefield(srcx, srcy, self.PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                rook = self.readfield(srcx + 3, srcy)
                self.writefield(srcx + 3, srcy, self.PIECES['blk'])
                self.writefield(dstx - 1, dsty, rook)
                self.fifty_moves_count += 1
                if(srcpiece == Match.PIECES['wKg']):
                    self.wKg_x = dstx
                    self.wKg_y = dsty
                    self.wKg_first_movecnt = self.count
                else:
                    self.bKg_x = dstx
                    self.bKg_y = dsty              
                    self.bKg_first_movecnt = self.count
                
                move.move_type = move.TYPES['short_castling']
                move.captured_piece = dstpiece
                return move
            elif(srcx - dstx == 2):
                self.writefield(srcx, srcy, self.PIECES['blk'])
                self.writefield(dstx, dsty, srcpiece)
                rook = self.readfield(srcx - 4, srcy)
                self.writefield(srcx - 4, srcy, self.PIECES['blk'])
                self.writefield(dstx + 1, dsty, rook)
                self.fifty_moves_count += 1
                if(srcpiece == Match.PIECES['wKg']):
                    self.wKg_x = dstx
                    self.wKg_y = dsty
                    self.wKg_first_movecnt = self.count
                else:
                    self.bKg_x = dstx
                    self.bKg_y = dsty              
                    self.bKg_first_movecnt = self.count
                
                move.move_type = move.TYPES['long_castling']
                move.captured_piece = dstpiece
                return move
        self.writefield(srcx, srcy, self.PIECES['blk'])
        self.writefield(dstx, dsty, srcpiece)
        if(dstpiece != self.PIECES['blk']):
            self.fifty_moves_count = 0
        else:
            self.fifty_moves_count += 1
        if(srcpiece == Match.PIECES['wKg']):
            self.wKg_x = dstx
            self.wKg_y = dsty
            self.wKg_first_movecnt = self.count
        elif(srcpiece == Match.PIECES['bKg']):
            self.bKg_x = dstx
            self.bKg_y = dsty
            self.bKg_first_movecnt = self.count
        if(srcpiece == Match.PIECES['wRk']):
            if(srcx == 0 and srcy == 0 and self.wRk_a1_first_movecnt == 0):
                self.wRk_a1_first_movecnt = self.count
            elif(srcx == 7 and srcy == 0 and self.wRk_h1_first_movecnt == 0):
                self.wRk_h1_first_movecnt = self.count
        elif(srcpiece == Match.PIECES['bRk']):
            if(srcx == 0 and srcy == 7 and self.bRk_a8_first_movecnt == 0):
                self.bRk_a8_first_movecnt = self.count
            elif(srcx == 7 and srcy == 7 and self.bRk_h8_first_movecnt == 0):
                self.bRk_h8_first_movecnt = self.count
        move.fifty_moves_count = self.fifty_moves_count
        move.move_type = move.TYPES['standard']
        move.captured_piece = dstpiece
        self.score += self.SCORES[dstpiece]
        return move

    def undo_move(self, calc):
        if(calc == False):
            move = Move.objects.filter(match_id=self.id).order_by("count").last()
            if(move == None):
                return None
        else:
            if(len(self.move_list) > 0):
                move = self.move_list.pop()
            else:
                return None
        self.count -= 1
        self.fifty_moves_count = move.fifty_moves_count
        if(move.move_type == move.TYPES['standard']):
            piece = self.readfield(move.dstx, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, move.captured_piece)
            self.score -= self.SCORES[move.captured_piece]
            if(piece == Match.PIECES['wKg']):
                self.wKg_x = move.srcx
                self.wKg_y = move.srcy
                if(self.wKg_first_movecnt == self.count + 1):
                    self.wKg_first_movecnt = 0
            elif(piece == Match.PIECES['bKg']):
                self.bKg_x = move.srcx
                self.bKg_y = move.srcy
                if(self.bKg_first_movecnt == self.count + 1):
                    self.bKg_first_movecnt = 0
            elif(piece == Match.PIECES['wRk']):
                if(self.wRk_a1_first_movecnt == self.count + 1):
                    self.wRk_a1_first_movecnt = 0
                elif(self.wRk_h1_first_movecnt == self.count + 1):
                    self.wRk_h1_first_movecnt = 0
            elif(piece == Match.PIECES['bRk']):
                if(self.bRk_a8_first_movecnt == self.count + 1):
                    self.bRk_a8_first_movecnt = 0
                elif(self.bRk_h8_first_movecnt == self.count + 1):
                    self.bRk_h8_first_movecnt = 0
            return move
        elif(move.move_type == move.TYPES['short_castling']):
            piece = self.readfield(move.dstx, move.dsty)
            rook = self.readfield(move.dstx - 1, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, self.PIECES['blk'])
            self.writefield(move.dstx - 1, move.dsty, self.PIECES['blk'])
            self.writefield(move.dstx + 1, move.dsty, rook)
            if(piece == Match.PIECES['wKg']):
                self.wKg_x = move.srcx
                self.wKg_y = move.srcy
                self.wKg_first_movecnt = 0
                self.wRk_h1_first_movecnt = 0
            else:
                self.bKg_x = move.srcx
                self.bKg_y = move.srcy
                self.bKg_first_movecnt = 0
                self.bRk_h8_first_movecnt = 0
            return move
        elif(move.move_type == move.TYPES['long_castling']):
            piece = self.readfield(move.dstx, move.dsty)
            rook = self.readfield(move.dstx + 1, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, self.PIECES['blk'])
            self.writefield(move.dstx + 1, move.dsty, self.PIECES['blk'])
            self.writefield(move.dstx - 2, move.dsty, rook)
            if(piece == Match.PIECES['wKg']):
                self.wKg_x = move.srcx
                self.wKg_y = move.srcy
                self.wKg_first_movecnt = 0
                self.wRk_a1_first_movecnt = 0
            else:
                self.bKg_x = move.srcx
                self.bKg_y = move.srcy
                self.bKg_first_movecnt = 0
                self.bRk_a8_first_movecnt = 0
            return move
        elif(move.move_type == move.TYPES['promotion']):
            if(move.dsty == 7):
                piece = self.PIECES['wPw']
            else:
                piece = self.PIECES['bPw']
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, move.captured_piece)
            self.score += (self.SCORES[move.prom_piece] - self.SCORES[piece])
            self.score -= self.SCORES[move.captured_piece]
            return move
        else:
            piece = self.readfield(move.dstx, move.dsty)
            self.writefield(move.srcx, move.srcy, piece)
            self.writefield(move.dstx, move.dsty, self.PIECES['blk'])
            self.writefield(move.e_p_fieldx, move.e_p_fieldy, move.captured_piece)
            self.score -= self.SCORES[move.captured_piece]
            return move

    def next_color(self):
        if(self.count % 2 == 0 ):
            return Match.COLORS['white']
        else:
            return Match.COLORS['black']

    def next_color_human(self):
        if(self.count % 2 == 0 ):
            return self.white_player_human
        else:
            return self.black_player_human

    @staticmethod
    def color_of_piece(piece):
        if(piece >= Match.PIECES['wKg'] and piece <= Match.PIECES['wQu']):
            return Match.COLORS['white']
        elif(piece >= Match.PIECES['bKg'] and piece <= Match.PIECES['bQu']):
            return Match.COLORS['black']
        else:
            return Match.COLORS['undefined']

    def remove_former_threads(self):
        with self.immanuels_thread_lock:
            for item in self.immanuels_threads_list:
                if(item.match.id == self.id):
                    self.immanuels_threads_list.remove(item)

    def add_thread(self, thread):
        with self.immanuels_thread_lock:
            self.immanuels_threads_list.append(thread)

    def does_thread_exist(self, thread):
        with self.immanuels_thread_lock:
            for item in self.immanuels_threads_list:
                if(item is thread):
                    return True
            return False


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
    fifty_moves_count = models.SmallIntegerField(null=False)

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
            fmtmove= values.index_to_koord(self.srcx, self.srcy) + hyphen + values.index_to_koord(self.dstx, self.dsty) + " " + values.reverse_lookup(Match.PIECES, self.prom_piece)
            return fmtmove
        else:
            fmtmove= values.index_to_koord(self.srcx, self.srcy) + "x" + values.index_to_koord(self.dstx, self.dsty) + " e.p."
            return fmtmove

    @staticmethod
    def fill_fmtmoves(match):
        fmtmoves = []
        currmove = Move.objects.filter(match_id=match.id).order_by("count").last()
        if(currmove == None):
            return fmtmoves
        else:
            if(currmove.count % 2 == 0):
                limit = 42
            else:
                limit = 41
            moves = Move.objects.filter(match_id=match.id).order_by("count").reverse()[:limit]
            for move in reversed(moves):
                if(move.count % 2 == 1 ):
                    fmtmoves.append("<tr><td>" + str( (move.count + 1) // 2) + ".</td>")
                    fmtmoves.append("<td>" + move.format_move() + "&nbsp;</td>")
                else:
                    fmtmoves.append("<td>" + move.format_move() + "</td></tr>")
            if(len(moves) % 2 == 1):
                fmtmoves.append("<td>&nbsp;</td></tr>")
            return fmtmoves

    @staticmethod
    def html_moves(match):
        fmtmoves = []
        fmtmoves = Move.fill_fmtmoves(match)
        htmldata = ""
        for col in fmtmoves:
            htmldata += col
        return htmldata


class Comment(models.Model):
    match= models.ForeignKey(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=500)

