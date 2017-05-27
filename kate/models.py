from django.db import models
from django.utils import timezone
from kate.engine.match import STATUS, LEVELS, PIECES
from kate.engine import helper
import threading


class Match(models.Model):
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
    level = models.SmallIntegerField(null=False, default=LEVELS['blitz'])
    board = models.CharField(max_length=256, blank=False, default='wRk;wKn;wBp;wQu;wKg;wBp;wKn;wRk;' \
                                                                  'wPw;wPw;wPw;wPw;wPw;wPw;wPw;wPw;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'bPw;bPw;bPw;bPw;bPw;bPw;bPw;bPw;' \
                                                                  'bRk;bKn;bBp;bQu;bKg;bBp;bKn;bRk;')
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
    _matches_thread_lock = threading.Lock()
    _matches_thread_list = []


    def __init__(self, *args, **kwargs):
        super(Match, self).__init__(*args, **kwargs)


    def writefield(self, x, y, value):
        idx = y*32 + x*4
        str_value = helper.reverse_lookup(PIECES, value)
        self.board = self.board[:idx] + str_value + self.board[(idx+3):]


    def readfield(self, x, y):
        idx = y*32 + x*4
        str_value = self.board[idx:idx+3]
        return PIECES[str_value]


    def readfield_core(self, x, y):
        idx = y*32 + x*4
        return self.board[idx:idx+3]


    @classmethod
    def remove_outdated_threads(cls):
        with cls._matches_thread_lock:
            for item in cls._matches_thread_list:
                if(item.running == False): # item.is_alive() == False or 
                    item.running = False
                    cls._matches_thread_list.remove(item)
                    item.join()


    @classmethod
    def add_thread(cls, thread):
        with cls._matches_thread_lock:
            cls._matches_thread_list.append(thread)


    @classmethod
    def get_active_thread(cls, match):
        with cls._matches_thread_lock:
            for item in cls._matches_thread_list:
                if(item.match.id == match.id and item.running): # and item.is_alive() 
                    return item
            return None


    @classmethod
    def deactivate_threads(cls, match):
        with cls._matches_thread_lock:
            for item in cls._matches_thread_list:
                if(item.match.id == match.id):
                    item.running = False


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
    captured_piece = models.PositiveSmallIntegerField(null=False, default=PIECES['blk'])
    prom_piece = models.PositiveSmallIntegerField(null=False, default=PIECES['blk'])
    fifty_moves_count = models.SmallIntegerField(null=False)


    def __init__(self, *args, **kwargs):
        super(Move, self).__init__(*args, **kwargs)


    class Meta:
        unique_together = (("match", "count"),)


class Comment(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=500)

