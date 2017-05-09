from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from kate.modules import helper
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
        PIECES['bQu'] : COLORS['black']
    }

    PIECES_RANK = {
        PIECES['blk'] : 0,
        PIECES['wPw'] : 1,
        PIECES['bPw'] : 1,
        PIECES['wKn'] : 2,
        PIECES['bKn'] : 2,
        PIECES['wBp'] : 2,
        PIECES['bBp'] : 2,
        PIECES['wRk'] : 4,
        PIECES['bRk'] : 4,
        PIECES['wQu'] : 5,
        PIECES['bQu'] : 5,
        PIECES['wKg'] : 6,
        PIECES['bKg'] : 6
    }

    EXPORT_PIECES = {
        0 : '0',
        1 : '1',
        2 : '2',
        3 : '3',
        4 : '4',
        5 : '5',
        6 : '6',
        9 : '9',
        10 : 'A',
        11 : 'B',
        12 : 'C',
        13 : 'D',
        14 : 'E' 
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
        PIECES['bQu'] : 950
    }

    REVERSED_SCORES = {
        PIECES['blk'] : PIECES['blk'],
        PIECES['wKg'] : PIECES['bKg'],
        PIECES['wPw'] : PIECES['bPw'],
        PIECES['wRk'] : PIECES['bRk'] ,
        PIECES['wKn'] : PIECES['bKn'],
        PIECES['wBp'] : PIECES['bBp'],
        PIECES['wQu'] : PIECES['bQu'],
        PIECES['bKg'] : PIECES['wKg'],
        PIECES['bPw'] : PIECES['wPw'],
        PIECES['bRk'] : PIECES['wRk'],
        PIECES['bKn'] : PIECES['wKn'],
        PIECES['bBp'] : PIECES['wBp'],
        PIECES['bQu'] : PIECES['wQu']
    }

    ATTACKED_SCORES = {
        PIECES['blk'] : 0,
        PIECES['wKg'] : -10,
        PIECES['wPw'] : -1,
        PIECES['wRk'] : -5,
        PIECES['wKn'] : -4,
        PIECES['wBp'] : -4,
        PIECES['wQu'] : -7,
        PIECES['bKg'] : 10,
        PIECES['bPw'] : 1,
        PIECES['bRk'] : 5,
        PIECES['bKn'] : 4,
        PIECES['bBp'] : 4,
        PIECES['bQu'] : 7
    }

    SUPPORTED_SCORES = {
        PIECES['blk'] : 0,
        PIECES['wKg'] : 10,
        PIECES['wPw'] : 1,
        PIECES['wRk'] : 5,
        PIECES['wKn'] : 4,
        PIECES['wBp'] : 4,
        PIECES['wQu'] : 7,
        PIECES['bKg'] : -10,
        PIECES['bPw'] : -1,
        PIECES['bRk'] : -5,
        PIECES['bKn'] : -4,
        PIECES['bBp'] : -4,
        PIECES['bQu'] : -7
    }

    STATUS = {
        'open' : 1,
        'draw' : 2,
        'winner_white' : 3,
        'winner_black' : 4,
        'cancelled' : 5 }

    LEVELS = {
        'blitz' : 0,
        'low' : 1,
        'medium' : 2,
        'high' : 3 }

    status = models.PositiveSmallIntegerField(null=False, default=STATUS['open'])
    count = models.SmallIntegerField(null=False, default=0)
    score = models.IntegerField(null=False, default=0)
    begin = models.DateTimeField(default=timezone.now)
    white_player = models.CharField(max_length=100, blank=False)
    white_player_human = models.BooleanField(null=False, default=True)
    elapsed_time_white = models.IntegerField(null=False, default=0)
    black_player = models.CharField(max_length=100, blank=False)
    black_player_human = models.BooleanField(null=False, default=True)
    elapsed_time_black = models.IntegerField(null=False, default=0)
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
    _immanuels_thread_lock = threading.Lock()
    _immanuels_threads_list = []


    def __init__(self, *args, **kwargs):
        super(Match, self).__init__(*args, **kwargs)
        self.move_list = []


    def setboardbase(self):
        self.board = [ [0 for x in range(8)] for x in range(8) ]
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


    def writefield(self, x, y, value):
        self.board[y][x] = value


    def readfield(self, x, y):
        return self.board[y][x]


    def next_color(self):
        if(self.count % 2 == 0 ):
            return self.COLORS['white']
        else:
            return self.COLORS['black']


    def next_color_human(self):
        if(self.count % 2 == 0 ):
            return self.white_player_human
        else:
            return self.black_player_human


    def is_immanuel(self):
        return (self.white_player_human == False or self.black_player_human == False)


    def is_last_move_capture(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            if(move.captured_piece != self.PIECES['blk']):
                return True

        return False


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


    @staticmethod
    def color_of_piece(piece):
        return Match.PIECES_COLOR[piece]

    @staticmethod
    def oppcolor_of_piece(piece):
        color = Match.PIECES_COLOR[piece]
        return Match.REVERSED_COLORS[color]

    @staticmethod
    def koord_to_index(koord):
        x = ord(koord[0]) - ord('a')
        y = ord(koord[1]) - ord('1')
        return x,y


    @staticmethod
    def index_to_koord(x, y):
        col = chr(x + ord('a'))
        row = chr(y + ord('1'))
        koord = str(col + row)
        return koord


    @classmethod
    def remove_threads(cls, match):
        with cls._immanuels_thread_lock:
            for item in cls._immanuels_threads_list:
                if(item.match.id == match.id and item.is_alive() == False):
                    cls._immanuels_threads_list.remove(item)
                    item.join()


    @classmethod
    def add_thread(cls, thread):
        with cls._immanuels_thread_lock:
            cls._immanuels_threads_list.append(thread)


    @classmethod
    def get_active_thread(cls, match):
        with cls._immanuels_thread_lock:
            for item in cls._immanuels_threads_list:
                if(item.match.id == match.id and item.is_alive()):
                    return item
        return None


    @classmethod
    def does_thread_exist(cls, thread):
        with cls._immanuels_thread_lock:
            for item in cls._immanuels_threads_list:
                if(item is thread and item.is_alive()):
                    return True
            return False


class Move(models.Model):
    TYPES = {
        'standard' : 1,
        'short_castling' : 2,
        'long_castling' : 3,
        'promotion' : 4,
        'en_passant' : 5 }

    match = models.ForeignKey(Match, on_delete=models.CASCADE, null=False)
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


    def __init__(self, *args, **kwargs):
        super(Move, self).__init__(*args, **kwargs)


    class Meta:
        unique_together = (("match", "count"),)


    def format_move(self):
        if(self.move_type == Move.TYPES['standard']):
            if(self.captured_piece == 0):
                hyphen = "-"
            else:
                hyphen = "x"
            fmtmove = Match.index_to_koord(self.srcx, self.srcy) + hyphen + Match.index_to_koord(self.dstx, self.dsty)
            return fmtmove
        elif(self.move_type == Move.TYPES['short_castling']):
            return "0-0"
        elif(self.move_type == Move.TYPES['long_castling']):
            return "0-0-0"
        elif(self.move_type == Move.TYPES['promotion']):
            if(self.captured_piece == 0):
                hyphen = "-"
            else:
                hyphen = "x"
            fmtmove= Match.index_to_koord(self.srcx, self.srcy) + hyphen + Match.index_to_koord(self.dstx, self.dsty) + " " + helper.reverse_lookup(Match.PIECES, self.prom_piece)
            return fmtmove
        else:
            fmtmove= Match.index_to_koord(self.srcx, self.srcy) + "x" + Match.index_to_koord(self.dstx, self.dsty) + " e.p."
            return fmtmove



class Comment(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=500)



class OpeningMove(models.Model):
    previous = models.ForeignKey('OpeningMove', null=True)
    movecnt = models.PositiveSmallIntegerField(null=False)
    src = models.CharField(max_length=2, blank=False)
    dst = models.CharField(max_length=2, blank=False)


    class Meta:
        unique_together = (("previous", "movecnt", "src", "dst"),)

