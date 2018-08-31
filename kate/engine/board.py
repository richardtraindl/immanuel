from .match import cMatch


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

    def __init__(self):
        self.fields = [ [cMatch.PIECES['wRk'], cMatch.PIECES['wKn'], cMatch.PIECES['wBp'], cMatch.PIECES['wQu'], cMatch.PIECES['wKg'], cMatch.PIECES['wBp'], cMatch.PIECES['wKn'], cMatch.PIECES['wRk']],
                        [cMatch.PIECES['wPw'], cMatch.PIECES['wPw'], cMatch.PIECES['wPw'], cMatch.PIECES['wPw'], cMatch.PIECES['wPw'], cMatch.PIECES['wPw'], cMatch.PIECES['wPw'], cMatch.PIECES['wPw']],
                        [cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk']],
                        [cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk']],
                        [cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk']],
                        [cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk'], cMatch.PIECES['blk']],
                        [cMatch.PIECES['bPw'], cMatch.PIECES['bPw'], cMatch.PIECES['bPw'], cMatch.PIECES['bPw'], cMatch.PIECES['bPw'], cMatch.PIECES['bPw'], cMatch.PIECES['bPw'], cMatch.PIECES['bPw']],
                        [cMatch.PIECES['bRk'], cMatch.PIECES['bKn'], cMatch.PIECES['bBp'], cMatch.PIECES['bQu'], cMatch.PIECES['bKg'], cMatch.PIECES['bBp'], cMatch.PIECES['bKn'], cMatch.PIECES['bRk']] ]

    def set_to_base(self):
        self.fields[FIRST][FIRST] = cMatch.PIECES['wRk']
        self.fields[FIRST][SECOND] = cMatch.PIECES['wKn']
        self.fields[FIRST][THIRD] = cMatch.PIECES['wBp']
        self.fields[FIRST][FOURTH] = cMatch.PIECES['wQu']
        self.fields[FIRST][FIFTH] = cMatch.PIECES['wKg']
        self.fields[FIRST][SIXTH] = cMatch.PIECES['wBp']
        self.fields[FIRST][SEVENTH] = cMatch.PIECES['wKn']
        self.fields[FIRST][EIGHTH] = cMatch.PIECES['wRk']

        for y in range (SECOND, (SECOND + 1), 1):
            for x in range (FIRST, (EIGHTH + 1), 1):
                self.fields[y][x] = cMatch.PIECES['wPw']

        for y in range (THIRD, (SIXTH + 1), 1):
            for x in range (FIRST, (EIGHTH + 1), 1):
                self.fields[y][x] = cMatch.PIECES['blk']

        for y in range (SEVENTH, (SEVENTH + 1), 1):
            for x in range (FIRST, (EIGHTH + 1), 1):
                self.fields[y][x] = cMatch.PIECES['bPw']

        self.fields[EIGHTH][FIRST] = cMatch.PIECES['bRk']
        self.fields[EIGHTH][SECOND] = cMatch.PIECES['bKn']
        self.fields[EIGHTH][THIRD] = cMatch.PIECES['bBp']
        self.fields[EIGHTH][FOURTH] = cMatch.PIECES['bQu']
        self.fields[EIGHTH][FIFTH] = cMatch.PIECES['bKg']
        self.fields[EIGHTH][SIXTH] = cMatch.PIECES['bBp']
        self.fields[EIGHTH][SEVENTH] = cMatch.PIECES['bKn']
        self.fields[EIGHTH][EIGHTH] = cMatch.PIECES['bRk']

    def writefield(self, x, y, value):
        self.fields[y][x] = value

    def readfield(self, x, y):
        return self.fields[y][x]

    def search(self, srcx, srcy, stepx, stepy):
        x = srcx + stepx
        y = srcy + stepy
        while(x >= self.FIRST and x <= self.EIGHTH and y >= self.FIRST and y <= self.EIGHTH):
            field = self.readfield(x, y)
            if(field != cMatch.PIECES['blk']):
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
