

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

        BLK = self.PIECES['blk']
        wRK = self.PIECES['wRk']
        wKN = self.PIECES['wKn']
        wBP = self.PIECES['wBp']
        wQU = self.PIECES['wQu']
        wKG = self.PIECES['wKg']
        wPW = self.PIECES['wPw']
        bRK = self.PIECES['bRk']
        bKN = self.PIECES['bKn']
        bBP = self.PIECES['bBp']
        bQU = self.PIECES['bQu']
        bKG = self.PIECES['bKg']
        bPW = self.PIECES['bPw']

    def __init__(self):

        self.fields = [ [wRK, wKN, wBP, wQU, wKG, wBP, wKN, wRK],
                        [wPW, wPW, wPW, wPW, wPW, wPW, wPW, wPW],
                        [BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK],
                        [BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK],
                        [BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK],
                        [BLK, BLK, BLK, BLK, BLK, BLK, BLK, BLK],
                        [bPW, bPW, bPW, bPW, bPW, bPW, bPW, bPW],
                        [bRK, bKN, bBP, bQU, bKG, bBP, bKN, bRK] ]

    def set_to_base(self):
        self.fields[self.COORD['1']][self.COORD['1']] = self.wRK
        self.fields[self.COORD['1']][self.COORD['2']] = self.wKN
        self.fields[self.COORD['1']][self.COORD['3']] = self.wBP
        self.fields[self.COORD['1']][self.COORD['4']] = self.wQU
        self.fields[self.COORD['1']][self.COORD['5']] = self.wKG
        self.fields[self.COORD['1']][self.COORD['6']] = self.wBP
        self.fields[self.COORD['1']][self.COORD['7']] = self.wKN
        self.fields[self.COORD['1']][self.COORD['8']] = self.wRK

        for y in range (self.COORD['2'], (self.COORD['2'] + 1), 1):
            for x in range (self.COORD['1'], (self.COORD['8'] + 1), 1):
                self.fields[y][x] = self.wPW

        for y in range (self.COORD['3'], (self.COORD['6'] + 1), 1):
            for x in range (self.COORD['1'], (self.COORD['8'] + 1), 1):
                self.fields[y][x] = self.BLK

        for y in range (self.COORD['7'], (self.COORD['7'] + 1), 1):
            for x in range (self.COORD['1'], (self.COORD['8'] + 1), 1):
                self.fields[y][x] = self.bPW

        self.fields[self.COORD['8']][self.COORD['1']] = self.bRK
        self.fields[self.COORD['8']][self.COORD['2']] = self.bKN
        self.fields[self.COORD['8']][self.COORD['3']] = self.bBP
        self.fields[self.COORD['8']][self.COORD['4']] = self.bQU
        self.fields[self.COORD['8']][self.COORD['5']] = self.bKG
        self.fields[self.COORD['8']][self.COORD['6']] = self.bBP
        self.fields[self.COORD['8']][self.COORD['7']] = self.bKN
        self.fields[self.COORD['8']][self.COORD['8']] = self.bRK

    def writefield(self, x, y, value):
        self.fields[y][x] = value

    def readfield(self, x, y):
        return self.fields[y][x]

    def search(self, srcx, srcy, stepx, stepy):
        x = srcx + stepx
        y = srcy + stepy
        while(x >= self.COORD['1'] and x <= self.COORD['8'] and y >= self.COORD['1'] and y <= self.COORD['8']):
            field = self.readfield(x, y)
            if(field != self.BLK):
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
