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

    def update_white_movecnt_short_castling_lost(self, srcx, srcy, movecnt):
        if(self.white_movecnt_short_castling_lost > 0):
            return False
        elif(srcx == self.COORD['5'] and srcy == self.COORD['1']): 
            self.white_movecnt_short_castling_lost = movecnt
            return True
        elif(srcx == self.COORD['8'] and srcy == self.COORD['1']):
            self.white_movecnt_short_castling_lost = movecnt
            return True
        else:
            return False

    def update_white_movecnt_long_castling_lost(self, srcx, srcy, movecnt):
        if(self.white_movecnt_long_castling_lost > 0):
            return False
        elif(srcx == self.COORD['5'] and srcy == self.COORD['1']):
            self.white_movecnt_long_castling_lost = movecnt
            return True
        elif(srcx == self.COORD['1'] and srcy == self.COORD['1']):
            self.white_movecnt_long_castling_lost = movecnt
            return True
        else:
            return False

    def update_black_movecnt_short_castling_lost(self, srcx, srcy, movecnt):
        if(self.black_movecnt_short_castling_lost > 0):
            return False
        elif(srcx == self.COORD['5'] and srcy == self.COORD['8']):
            self.black_movecnt_short_castling_lost = movecnt
            return True
        elif(srcx == self.COORD['8'] and srcy == self.COORD['8']):
            self.black_movecnt_short_castling_lost = movecnt
            return True
        else:
            return False

    def update_black_movecnt_long_castling_lost(self, srcx, srcy, movecnt):
        if(self.black_movecnt_long_castling_lost > 0):
            return False
        elif(srcx == self.COORD['5'] and srcy == self.COORD['8']):
            self.black_movecnt_long_castling_lost = movecnt
            return True
        elif(srcx == self.COORD['1'] and srcy == self.COORD['8']):
            self.black_movecnt_long_castling_lost = movecnt
            return True
        else:
            return False

    def update_counter(self):
        self.wQu_cnt = 0
        self.bQu_cnt = 0
        self.wOfficer_cnt = 0
        self.bOfficer_cnt = 0
        for y in range(8):
            for x in range(8):
                piece = self.readfield(x, y)
                if(piece == PIECES['wKg']):
                    self.wKg_x = x
                    self.wKg_y = y
                elif(piece == PIECES['bKg']):
                    self.bKg_x = x
                    self.bKg_y = y
                elif(piece == PIECES['wQu']):
                    self.wQu_cnt += 1
                elif(piece == PIECES['bQu']):
                    self.bQu_cnt += 1        
                elif(piece == PIECES['wRk'] or piece == PIECES['wBp'] or piece == PIECES['wKn']):
                    self.wOfficer_cnt += 1
                elif(piece == PIECES['bRk'] or piece == PIECES['bBp'] or piece == PIECES['bKn']):
                    self.bOfficer_cnt += 1

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
