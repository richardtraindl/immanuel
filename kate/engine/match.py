

STATUS = {
        'open' : 10,
        'draw' : 11,
        'winner_white' : 12,
        'winner_black' : 13,
        'paused' : 14 }


LEVELS = {
        'blitz' : 0,
        'low' : 1,
        'medium' : 2,
        'high' : 3 }


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


COLORS = {
        'undefined' : 0,
        'white' : 1,
        'black' : 9 
    }


REVERSED_COLORS = { COLORS['undefined'] : COLORS['undefined'],
                    COLORS['white'] : COLORS['black'],
                    COLORS['black'] : COLORS['white'] }


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
        PIECES['bQu'] : COLORS['black'] }


E1_X = 3
E1_Y = 0
A1_X = 0
A1_Y = 0
H1_X = 7
H1_Y = 0
E8_X = 3
E8_Y = 7
A8_X = 0
A8_Y = 7
H8_X = 7
H8_Y = 7


class Match:
    def __init__(self):
        self.status = STATUS['open']
        self.count = 0
        self.score = 0
        self.white_player = ""
        self.white_player_human = True
        self.elapsed_time_white = 0
        self.black_player = ""
        self.black_player_human = True
        self.elapsed_time_black = 0
        self.level = LEVELS['blitz']
        #self.board = [[0 for x in range(8)] for x in range(8)]
        self.board = [ [PIECES['wRk'], PIECES['wKn'], PIECES['wBp'], PIECES['wQu'], PIECES['wKg'], PIECES['wBp'], PIECES['wKn'], PIECES['wRk']],
                       [PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw'], PIECES['wPw']],
                       [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                       [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                       [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                       [PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk'], PIECES['blk']],
                       [PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw'], PIECES['bPw']],
                       [PIECES['bRk'], PIECES['bKn'], PIECES['bBp'], PIECES['bQu'], PIECES['bKg'], PIECES['bBp'], PIECES['bKn'], PIECES['bRk']] ]
        self.fifty_moves_count = 0
        self.wKg_x = E1_X
        self.wKg_y = E1_Y
        self.bKg_x = E8_X
        self.bKg_y = E8_Y
        self.white_movecnt_short_castling_lost = -1
        self.white_movecnt_long_castling_lost = -1
        self.black_movecnt_short_castling_lost = -1
        self.black_movecnt_long_castling_lost = -1
        self.wQu_cnt = 1
        self.bQu_cnt = 1
        self.wOfficer_cnt = 6
        self.bOfficer_cnt = 6
        self.move_list = []


    def update_attributes(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            fifty_moves_count = move.fifty_moves_count
        
            for move in self.move_list:
                if(move.count % 2 == 0):
                    if(self.white_movecnt_short_castling_lost == -1):
                        if(move.srcx == E1_X and move.srcy == E1_Y):
                            self.white_movecnt_short_castling_lost = move.count
                            continue
                        elif(move.srcx == A1_X and move.srcy == A1_Y):
                            self.white_movecnt_short_castling_lost = move.count
                            continue
                    if(self.white_movecnt_long_castling_lost == -1):
                        if(move.srcx == E1_X and move.srcy == E1_Y):
                            self.white_movecnt_long_castling_lost = move.count
                            continue
                        elif(move.srcx == H1_X and move.srcy == H1_Y):
                            self.white_movecnt_long_castling_lost = move.count
                            continue
                else:
                    if(self.black_movecnt_short_castling_lost == -1):
                        if(move.srcx == E8_X and move.srcy == E8_Y):
                            self.black_movecnt_short_castling_lost = move.count
                            continue
                        elif(move.srcx == A8_X and move.srcy == A8_Y):
                            self.black_movecnt_short_castling_lost = move.count
                            continue
                    if(self.black_movecnt_long_castling_lost == -1):
                        if(move.srcx == E8_X and move.srcy == E8_Y):
                            self.black_movecnt_long_castling_lost = move.count
                            continue
                        elif(move.srcx == H8_X and move.srcy == H8_Y):
                            self.black_movecnt_long_castling_lost = move.count
                            continue

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
                elif(piece == PIECES['wRk'] or piece == PIECES['wBp'] or piece == PIECES['wPw']):
                    self.wOfficer_cnt += 1
                elif(piece == PIECES['bRk'] or piece == PIECES['bBp'] or piece == PIECES['bPw']):
                    self.bOfficer_cnt + 1


    def writefield(self, x, y, value):
        self.board[y][x] = value


    def readfield(self, x, y):
        return self.board[y][x]


    def next_color(self):
        if(self.count % 2 == 0 ):
            return COLORS['white']
        else:
            return COLORS['black']


    def is_last_move_capture(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            if(move.captured_piece != PIECES['blk']):
                return True

        return False


    def is_last_move_promotion(self):
        if(len(self.move_list) > 0):
            move = self.move_list[-1]
            if(move.prom_piece != PIECES['blk']):
                return True

        return False


    def read_move_list(self, idx):
        if(len(self.move_list) > 0):
            return self.move_list[idx]
        else:
            return None


    @staticmethod
    def color_of_piece(piece):
        return PIECES_COLOR[piece]


    @staticmethod
    def oppcolor_of_piece(piece):
        color = PIECES_COLOR[piece]
        return REVERSED_COLORS[color]



