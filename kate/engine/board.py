

class cBoard:
    FIRST = 0
    SECOND = 1
    THIRD = 2
    FOURTH = 3
    FIFTH = 4
    SIXTH = 5
    SEVENTH = 6
    EIGHTH = 7
    UNDEF = 8
    MIN_X = 0
    MIN_Y = 0
    MAX_X = 7
    MAX_Y = 7

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

    def __init__(self):
        self.fields = [ [self.PIECES['wRk'], PIECES['wKn'], self.PIECES['wBp'], self.PIECES['wQu'], self.PIECES['wKg'], self.PIECES['wBp'], self.PIECES['wKn'], self.PIECES['wRk']],
                        [self.PIECES['wPw'], PIECES['wPw'], self.PIECES['wPw'], self.PIECES['wPw'], self.PIECES['wPw'], self.PIECES['wPw'], self.PIECES['wPw'], self.PIECES['wPw']],
                        [self.PIECES['blk'], PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk']],
                        [self.PIECES['blk'], PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk']],
                        [self.PIECES['blk'], PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk']],
                        [self.PIECES['blk'], PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk'], self.PIECES['blk']],
                        [self.PIECES['bPw'], PIECES['bPw'], self.PIECES['bPw'], self.PIECES['bPw'], self.PIECES['bPw'], self.PIECES['bPw'], self.PIECES['bPw'], self.PIECES['bPw']],
                        [self.PIECES['bRk'], PIECES['bKn'], self.PIECES['bBp'], self.PIECES['bQu'], self.PIECES['bKg'], self.PIECES['bBp'], self.PIECES['bKn'], self.PIECES['bRk']] ]

    def set_to_base(self):
        self.fields[FIRST][FIRST] = self.PIECES['wRk']
        self.fields[FIRST][SECOND] = self.PIECES['wKn']
        self.fields[FIRST][THIRD] = self.PIECES['wBp']
        self.fields[FIRST][FOURTH] = self.PIECES['wQu']
        self.fields[FIRST][FIFTH] = self.PIECES['wKg']
        self.fields[FIRST][SIXTH] = self.PIECES['wBp']
        self.fields[FIRST][SEVENTH] = self.PIECES['wKn']
        self.fields[FIRST][EIGHTH] = self.PIECES['wRk']

        for y in range (SECOND, (SECOND + 1), 1):
            for x in range (FIRST, (EIGHTH + 1), 1):
                self.fields[y][x] = self.PIECES['wPw']

        for y in range (THIRD, (SIXTH + 1), 1):
            for x in range (FIRST, (EIGHTH + 1), 1):
                self.fields[y][x] = self.PIECES['blk']

        for y in range (SEVENTH, (SEVENTH + 1), 1):
            for x in range (FIRST, (EIGHTH + 1), 1):
                self.fields[y][x] = self.PIECES['bPw']

        self.fields[EIGHTH][FIRST] = self.PIECES['bRk']
        self.fields[EIGHTH][SECOND] = self.PIECES['bKn']
        self.fields[EIGHTH][THIRD] = self.PIECES['bBp']
        self.fields[EIGHTH][FOURTH] = self.PIECES['bQu']
        self.fields[EIGHTH][FIFTH] = self.PIECES['bKg']
        self.fields[EIGHTH][SIXTH] = self.PIECES['bBp']
        self.fields[EIGHTH][SEVENTH] = self.PIECES['bKn']
        self.fields[EIGHTH][EIGHTH] = self.PIECES['bRk']

    def writefield(self, x, y, value):
        self.fields[y][x] = value

    def readfield(self, x, y):
        return self.fields[y][x]

    def search(self, srcx, srcy, stepx, stepy):
        x = srcx + stepx
        y = srcy + stepy
        while(x >= self.FIRST and x <= self.EIGHTH and y >= self.FIRST and y <= self.EIGHTH):
            field = self.readfield(x, y)
            if(field != self.PIECES['blk']):
                return x, y
            x += stepx
            y += stepy
        return self.UNDEF, self.UNDEF

    @classmethod
    def is_inbounds(cls, x, y):
        if(x < cls.FIRST or x > cls.EIGHTH or y < cls.FIRST or y > cls.EIGHTH):
            return False
        else:
            return True

    @classmethod
    def is_move_inbounds(cls, srcx, srcy, dstx, dsty):
        if(srcx < cls.FIRST or srcx > cls.EIGHTH or srcy < cls.FIRST or srcy > cls.EIGHTH or
           dstx < cls.FIRST or dstx > cls.EIGHTH or dsty < cls.FIRST or dsty > cls.EIGHTH):
            return False
        else:
            return True

# class end
