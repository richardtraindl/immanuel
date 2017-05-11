import threading


STATUS = { 'open' : 1, 'draw' : 2, 'winner_white' : 3, 'winner_black' : 4, 'cancelled' : 5 }

LEVELS = { 'blitz' : 0, 'low' : 1, 'medium' : 2, 'high' : 3 }

COLORS = { 'undefined' : 0, 'white' : 1, 'black' : 9 }

REVERSED_COLORS = { COLORS['undefined'] : COLORS['undefined'],
                    COLORS['white'] : COLORS['black'],
                    COLORS['black'] : COLORS['white'] }

PIECES = { 'blk' : 0, 'wKg' : 1, 'wPw' : 2, 'wRk' : 3, 'wKn' : 4, 'wBp' : 5, 'wQu' : 6, 
                      'bKg' : 9, 'bPw' : 10, 'bRk' : 11, 'bKn' : 12, 'bBp' : 13, 'bQu' : 14 }

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
E8_X = 3
E8_Y = 7

class Match:
    _immanuels_thread_lock = threading.Lock()
    _immanuels_threads_list = []

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
        self.board = [[0 for x in range(8)] for x in range(8)]
        self.fifty_moves_count = 0
        self.wKg_x = E1_X
        self.wKg_y = E1_Y
        self.bKg_x = E8_X
        self.bKg_y = E8_Y
        self.wKg_first_movecnt = 0
        self.bKg_first_movecnt = 0
        self.wRk_a1_first_movecnt = 0
        self.wRk_h1_first_movecnt = 0
        self.bRk_a8_first_movecnt = 0
        self.bRk_h8_first_movecnt = 0
        self.move_list = []

            
    def setboardbase(self):
        self.board[0][0] = PIECES['wRk']
        self.board[0][1] = PIECES['wKn']
        self.board[0][2] = PIECES['wBp']
        self.board[0][3] = PIECES['wQu']
        self.board[0][4] = PIECES['wKg']
        self.board[0][5] = PIECES['wBp']
        self.board[0][6] = PIECES['wKn']
        self.board[0][7] = PIECES['wRk']

        for i in range(0, 8, 1):
            self.board[1][i] = PIECES['wPw']

        for j in range(2, 6, 1):
            for i in range(0, 8, 1):
                self.board[j][i] = PIECES['blk']

        for i in range(0, 8, 1):
            self.board[6][i] = PIECES['bPw']

        self.board[7][0] = PIECES['bRk']
        self.board[7][1] = PIECES['bKn']
        self.board[7][2] = PIECES['bBp']
        self.board[7][3] = PIECES['bQu']
        self.board[7][4] = PIECES['bKg']
        self.board[7][5] = PIECES['bBp']
        self.board[7][6] = PIECES['bKn']
        self.board[7][7] = PIECES['bRk']
        self.fifty_moves_count = 0
        self.wKg_x = E1_X
        self.wKg_y = E1_Y
        self.bKg_x = E8_X
        self.bKg_y = E8_Y
        self.wKg_first_movecnt = 0
        self.bKg_first_movecnt = 0
        self.wRk_a1_first_movecnt = 0
        self.wRk_h1_first_movecnt = 0
        self.bRk_a8_first_movecnt = 0
        self.bRk_h8_first_movecnt = 0
        self.move_list = []


    def writefield(self, x, y, value):
        self.board[y][x] = value


    def readfield(self, x, y):
        return self.board[y][x]


    def next_color(self):
        if(self.count % 2 == 0 ):
            return COLORS['white']
        else:
            return COLORS['black']


    def next_color_human(self):
        if(self.count % 2 == 0 ):
            return self.white_player_human
        else:
            return self.black_player_human


    def is_immanuel(self):
        return (self.white_player_human == False or self.black_player_human == False)


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


    @staticmethod
    def koord_to_index(koord):
        x = ord(koord[0]) - ord('a')
        y = ord(koord[1]) - ord('1')
        return x,y


    @staticmethod
    def index_to_koord(x, y):
        col = chr(x + ord('a'))
        row = chr(y + ord('1'))
        koord = str(col + row)
        return koord

    @classmethod
    def remove_threads(cls, match):
        with cls._immanuels_thread_lock:
            for item in cls._immanuels_threads_list:
                if(item.match.id == match.id and item.is_alive() == False):
                    cls._immanuels_threads_list.remove(item)
                    item.join()


    @classmethod
    def add_thread(cls, thread):
        with cls._immanuels_thread_lock:
            cls._immanuels_threads_list.append(thread)


    @classmethod
    def get_active_thread(cls, match):
        with cls._immanuels_thread_lock:
            for item in cls._immanuels_threads_list:
                if(item.match.id == match.id and item.is_alive()):
                    return item
        return None


    @classmethod
    def does_thread_exist(cls, thread):
        with cls._immanuels_thread_lock:
            for item in cls._immanuels_threads_list:
                if(item is thread and item.is_alive()):
                    return True
            return False
