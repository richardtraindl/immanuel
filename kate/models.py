from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from kate.engine import helper



class Match(models.Model):
    COLORS = {
        'undefined' : 0,
        'white' : 1,
        'black' : 9 
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
    board = models.CharField(max_length=256, blank=False, default='wRk;wKn;wBp;wQu;wKg;wBp;wKn;wRk;' \
                                                                  'wPw;wPw;wPw;wPw;wPw;wPw;wPw;wPw;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'blk;blk;blk;blk;blk;blk;blk;blk;' \
                                                                  'bPw;bPw;bPw;bPw;bPw;bPw;bPw;bPw;' \
                                                                  'bRk;bKn;bBp;bQu;bKg;bBp;bKn;bRk;')
    # board = ArrayField(ArrayField(models.PositiveSmallIntegerField(null=False, blank=False, default=PIECES['blk']), size=8), size=8)
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

    def __init__(self, *args, **kwargs):
        super(Match, self).__init__(*args, **kwargs)


    def writefield(self, x, y, value):
        idx = y*32 + x*4
        str_value = helper.reverse_lookup(Match.PIECES, value)
        self.board = self.board[:idx] + str_value + self.board[(idx+3):]


    def readfield(self, x, y):
        idx = y*32 + x*4
        str_value = self.board[idx:idx+3]
        return Match.PIECES[str_value]


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

