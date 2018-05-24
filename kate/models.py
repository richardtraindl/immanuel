from django.db import models
from django.utils import timezone
from kate.engine.match import STATUS, LEVELS, PIECES
from kate.engine import helper
import threading


class Match(models.Model):
    status = models.PositiveSmallIntegerField(null=False, default=STATUS['open'])
    level = models.SmallIntegerField(null=False, default=LEVELS['blitz'])
    begin = models.DateTimeField(default=timezone.now)
    time_start = models.IntegerField(null=False, default=0)
    white_player_name = models.CharField(max_length=100, blank=False)
    white_player_is_human = models.BooleanField(null=False, default=True)
    white_elapsed_seconds = models.IntegerField(null=False, default=0)
    black_player_name = models.CharField(max_length=100, blank=False)
    black_player_is_human = models.BooleanField(null=False, default=True)
    black_elapsed_seconds = models.IntegerField(null=False, default=0)
    board = models.CharField(max_length=256, blank=False, default='wRk;wKn;wBp;wQu;wKg;wBp;wKn;wRk;' \
                                                                  'wPw;wPw;wPw;wPw;wPw;wPw;wPw;wPw;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'bPw;bPw;bPw;bPw;bPw;bPw;bPw;bPw;' \
                                                                  'bRk;bKn;bBp;bQu;bKg;bBp;bKn;bRk;')
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


    def is_immanuel(self):
        return (self.white_player_is_human == False or self.black_player_is_human == False)


    @classmethod
    def add_thread(cls, thread):
        with cls._matches_thread_lock:
            cls._matches_thread_list.append(thread)


    @classmethod
    def get_active_thread(cls, match):
        with cls._matches_thread_lock:
            print("get_active_thread length: " + str(len(cls._matches_thread_list)))
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

    @classmethod
    def remove_outdated_threads(cls):
        with cls._matches_thread_lock:
            for item in cls._matches_thread_list:
                if(item.running == False): # item.is_alive() == False or 
                    item.running = False
                    cls._matches_thread_list.remove(item)
                    item.join(3.0)


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

