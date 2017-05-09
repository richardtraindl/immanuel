


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

E1_X = 3
E1_Y = 0
E8_X = 3
E8_Y = 7

class Match:
    # static_elem = 123

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
        self.board = [[0 for x in range(8)] for y in range()] 
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

