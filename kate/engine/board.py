from .values import *


class cBoard:
    COORD = {
        '1' : 0,
        '2' : 1,
        '3' : 2,
        '4' : 3,
        '5' : 4,
        '6' : 5,
        '7' : 6,
        '8' : 7,
    }

    def __init__(self):
        self.fields = [ [PIECES['wRk'], PIECES['wKn'], PIECES['wBp'], PIECES['wQu'], PIECES['wKg'], PIECES['wBp'], PIECES['wKn'], PIECES['wRk']],
                        [PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw']],
                        [PIECES['bRk'], PIECES['bKn'], PIECES['bBp'], PIECES['bQu'], PIECES['bKg'], PIECES['bBp'], PIECES['bKn'], PIECES['bRk']] ]
        self.wKg_x = self.COORD['5']
        self.wKg_y = self.COORD['1']
        self.bKg_x = self.COORD['5']
        self.bKg_y = self.COORD['8']
        self.fifty_moves_count = 0
        self.white_movecnt_short_castling_lost = 0
        self.white_movecnt_long_castling_lost = 0
        self.black_movecnt_short_castling_lost = 0
        self.black_movecnt_long_castling_lost = 0
        self.wQu_cnt = 1
        self.bQu_cnt = 1
        self.wOfficer_cnt = 6
        self.bOfficer_cnt = 6

    def set_to_base(self):
        self.fields[self.COORD['1']][self.COORD['1']] = PIECES['wRk']
        self.fields[self.COORD['1']][self.COORD['2']] = PIECES['wKn']
        self.fields[self.COORD['1']][self.COORD['3']] = PIECES['wBp']
        self.fields[self.COORD['1']][self.COORD['4']] = PIECES['wQu']
        self.fields[self.COORD['1']][self.COORD['5']] = PIECES['wKg']
        self.fields[self.COORD['1']][self.COORD['6']] = PIECES['wBp']
        self.fields[self.COORD['1']][self.COORD['7']] = PIECES['wKn']
        self.fields[self.COORD['1']][self.COORD['8']] = PIECES['wRk']

        for y in range (self.COORD['2'], (self.COORD['2'] + 1), 1):
            for x in range (self.COORD['1'], (self.COORD['8'] + 1), 1):
                self.fields[y][x] = PIECES['wPw']

        for y in range (self.COORD['3'], (self.COORD['6'] + 1), 1):
            for x in range (self.COORD['1'], (self.COORD['8'] + 1), 1):
                self.fields[y][x] = PIECES['blk']

        for y in range (self.COORD['7'], (self.COORD['7'] + 1), 1):
            for x in range (self.COORD['1'], (self.COORD['8'] + 1), 1):
                self.fields[y][x] = PIECES['bPw']

        self.fields[self.COORD['8']][self.COORD['1']] = PIECES['bRk']
        self.fields[self.COORD['8']][self.COORD['2']] = PIECES['bKn']
        self.fields[self.COORD['8']][self.COORD['3']] = PIECES['bBp']
        self.fields[self.COORD['8']][self.COORD['4']] = PIECES['bQu']
        self.fields[self.COORD['8']][self.COORD['5']] = PIECES['bKg']
        self.fields[self.COORD['8']][self.COORD['6']] = PIECES['bBp']
        self.fields[self.COORD['8']][self.COORD['7']] = PIECES['bKn']
        self.fields[self.COORD['8']][self.COORD['8']] = PIECES['bRk']
        
        self.wKg_x = self.COORD['5']
        self.wKg_y = self.COORD['1']
        self.bKg_x = self.COORD['5']
        self.bKg_y = self.COORD['8']
        self.fifty_moves_count = 0
        self.white_movecnt_short_castling_lost = 0
        self.white_movecnt_long_castling_lost = 0
        self.black_movecnt_short_castling_lost = 0
        self.black_movecnt_long_castling_lost = 0
        self.wQu_cnt = 1
        self.bQu_cnt = 1
        self.wOfficer_cnt = 6
        self.bOfficer_cnt = 6
    # set_to_base() end

    def domove_white_movecnt_short_castling_lost(self, srcx, srcy, movecnt):
        if(self.white_movecnt_short_castling_lost == 0):
            if(srcx == self.COORD['5'] and srcy == self.COORD['1']): 
                self.white_movecnt_short_castling_lost = movecnt
            elif(srcx == self.COORD['8'] and srcy == self.COORD['1']):
                self.white_movecnt_short_castling_lost = movecnt

    def undomove_white_movecnt_short_castling_lost(self, move):
        if(self.white_movecnt_short_castling_lost == move.count):
            self.white_movecnt_short_castling_lost = 0

    def domove_white_movecnt_long_castling_lost(self, srcx, srcy, movecnt):
        if(self.white_movecnt_long_castling_lost == 0):
            if(srcx == self.COORD['5'] and srcy == self.COORD['1']):
                self.white_movecnt_long_castling_lost = movecnt
            elif(srcx == self.COORD['1'] and srcy == self.COORD['1']):
                self.white_movecnt_long_castling_lost = movecnt

    def undomove_white_movecnt_long_castling_lost(self, move):
        if(self.white_movecnt_long_castling_lost == move.count):
            self.white_movecnt_long_castling_lost = 0

    def domove_black_movecnt_short_castling_lost(self, srcx, srcy, movecnt):
        if(self.black_movecnt_short_castling_lost == 0):
            if(srcx == self.COORD['5'] and srcy == self.COORD['8']):
                self.black_movecnt_short_castling_lost = movecnt
            elif(srcx == self.COORD['8'] and srcy == self.COORD['8']):
                self.black_movecnt_short_castling_lost = movecnt

    def undomove_black_movecnt_short_castling_lost(self, move):
        if(self.black_movecnt_short_castling_lost == move.count):
            self.black_movecnt_short_castling_lost = 0

    def domove_black_movecnt_long_castling_lost(self, srcx, srcy, movecnt):
        if(self.black_movecnt_long_castling_lost == 0):
            if(srcx == self.COORD['5'] and srcy == self.COORD['8']):
                self.black_movecnt_long_castling_lost = movecnt
            elif(srcx == self.COORD['1'] and srcy == self.COORD['8']):
                self.black_movecnt_long_castling_lost = movecnt

    def undomove_black_movecnt_long_castling_lost(self, move):
        if(self.black_movecnt_long_castling_lost == move.count):
            self.black_movecnt_long_castling_lost = 0

    def domove_counter(self, dstpiece):
        self.update_counter(dstpiece, -1)

    def undomove_counter(self, move):
        self.update_counter(move.captured_piece, 1)

    def update_counter(self, piece, value):
        if(piece == PIECES['wQu']):
            self.wQu_cnt += value
        elif(piece == PIECES['bQu']):
            self.bQu_cnt += value
        elif(piece == PIECES['wKn'] or piece == PIECES['wBp'] or piece == PIECES['wRk']):
            self.wOfficer_cnt += value
        elif(piece == PIECES['bKn'] or piece == PIECES['bBp'] or piece == PIECES['bRk']):
            self.bOfficer_cnt += value

    def domove_fifty_moves_count(self, srcpiece, dstpiece):
        if(srcpiece == PIECES['wPw'] or srcpiece == PIECES['bPw']):
            self.fifty_moves_count = 0
        elif(dstpiece != PIECES['blk']):
            self.fifty_moves_count = 0
        else:
            self.fifty_moves_count += 1

    def undomove_fifty_moves_count(self, move):
        self.fifty_moves_count = move.fifty_moves_count

    def writefield(self, x, y, value):
        self.fields[y][x] = value

    def readfield(self, x, y):
        return self.fields[y][x]

    def search(self, srcx, srcy, stepx, stepy):
        x = srcx + stepx
        y = srcy + stepy
        while(x >= self.COORD['1'] and x <= self.COORD['8'] and y >= self.COORD['1'] and y <= self.COORD['8']):
            field = self.readfield(x, y)
            if(field != PIECES['blk']):
                return x, y
            x += stepx
            y += stepy
        return None, None

    @classmethod
    def is_inbounds(cls, x, y):
        if(x < cls.COORD['1'] or x > cls.COORD['8'] or y < cls.COORD['1'] or y > cls.COORD['8']):
            return False
        else:
            return True

    @classmethod
    def is_move_inbounds(cls, srcx, srcy, dstx, dsty):
        if(srcx < cls.COORD['1'] or srcx > cls.COORD['8'] or srcy < cls.COORD['1'] or srcy > cls.COORD['8'] or
           dstx < cls.COORD['1'] or dstx > cls.COORD['8'] or dsty < cls.COORD['1'] or dsty > cls.COORD['8']):
            return False
        else:
            return True

# class end
