

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

    def __init__(self, PIECES):
        self.PIECES = PIECES
        self.fields = [ [PIECES['wRk'], PIECES['wKn'], PIECES['wBp'], PIECES['wQu'], PIECES['wKg'], PIECES['wBp'], PIECES['wKn'], PIECES['wRk']],
                        [PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                        [PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw']],
                        [PIECES['bRk'], PIECES['bKn'], PIECES['bBp'], PIECES['bQu'], PIECES['bKg'], PIECES['bBp'], PIECES['bKn'], PIECES['bRk']] ]

    def set_to_base(self):
        self.fields[self.FIRST][self.FIRST] = self.PIECES['wRk']
        self.fields[self.FIRST][self.SECOND] = self.PIECES['wKn']
        self.fields[self.FIRST][self.THIRD] = self.PIECES['wBp']
        self.fields[self.FIRST][self.FOURTH] = self.PIECES['wQu']
        self.fields[self.FIRST][self.FIFTH] = self.PIECES['wKg']
        self.fields[self.FIRST][self.SIXTH] = self.PIECES['wBp']
        self.fields[self.FIRST][self.SEVENTH] = self.PIECES['wKn']
        self.fields[self.FIRST][self.EIGHTH] = self.PIECES['wRk']

        for y in range (self.SECOND, (self.SECOND + 1), 1):
            for x in range (self.FIRST, (self.EIGHTH + 1), 1):
                self.fields[y][x] = self.PIECES['wPw']

        for y in range (self.THIRD, (self.SIXTH + 1), 1):
            for x in range (self.FIRST, (self.EIGHTH + 1), 1):
                self.fields[y][x] = self.PIECES['blk']

        for y in range (self.SEVENTH, (self.SEVENTH + 1), 1):
            for x in range (self.FIRST, (self.EIGHTH + 1), 1):
                self.fields[y][x] = self.PIECES['bPw']

        self.fields[self.EIGHTH][self.FIRST] = self.PIECES['bRk']
        self.fields[self.EIGHTH][self.SECOND] = self.PIECES['bKn']
        self.fields[self.EIGHTH][self.THIRD] = self.PIECES['bBp']
        self.fields[self.EIGHTH][self.FOURTH] = self.PIECES['bQu']
        self.fields[self.EIGHTH][self.FIFTH] = self.PIECES['bKg']
        self.fields[self.EIGHTH][self.SIXTH] = self.PIECES['bBp']
        self.fields[self.EIGHTH][self.SEVENTH] = self.PIECES['bKn']
        self.fields[self.EIGHTH][self.EIGHTH] = self.PIECES['bRk']

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
