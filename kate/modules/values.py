

PIECES = dict()
PIECES = {'blk': 0, 
                  'wKg': 1, 'wPw': 2, 'wRk': 3, 'wKn': 4, 'wBp': 5, 'wQu': 6, 
                  'bKg': 9, 'bPw': 10, 'bRk': 11, 'bKn': 12, 'bBp': 13, 'bQu': 14 }

COLORS = dict()
COLORS = {'undefined': 0, 'white': 1, 'black': 2 }

def color_of piece(piece):
  value = PIECES[piece]
  if(value >= wKg and value <= wQu):
    return COLORS[white]
  elif(value >= bKg and value <= bQu):
    return COLORS[black]
  else:
    return COLORS[undefined]

def reverse_lookup(dic, value):
    for key in dic:
        if dic[key] == value:
            return key
    raiseValueError


MOVE_TYPES = dict()
MOVE_TYPES = {
    'standard': 1, 
    'short_castling': 2, 
    'long_castling': 3, 
    'promotion': 4, 
    'en_passant': 5 }


MATCH_STATUS = dict()
MATCH_STATUS = {
    'open': 1, 
    'draw': 2, 
    'winner_white': 3, 
    'winner_black': 4, 
    'cancelled': 5 }

def koord_to_index(koord):
    col = koord[0]
    row = koord[1]
    idx = ord(col) - ord('a')
    idx += (ord(row) - ord('1')) *  8
    return idx


def index_to_koord(idx):
    col = chr((idx % 8) + ord('a'))
    row = chr((idx // 8) + ord('1'))
    koord = str(col + row)
    return koord

def is_incol(idx1, idx2):
    return (idx1 % 8) == (idx2 % 8)

def is_inrow(idx1, idx2):
    return (idx1 // 8) == (idx2 // 8)

def format_move(move):
    if(move.move_type == MOVE_TYPES['standard']):
        if(move.captured_piece == 0):
            hyphen = "-"
        else:
            hyphen = "x"
        fmtmove= index_to_koord(move.src) + hyphen + index_to_koord(move.dest)
        return fmtmove
    elif(move.move_type == MOVE_TYPES['short_castling']):
        return "0-0"
    elif(move.move_type == MOVE_TYPES['long_castling']):
        return "0-0-0"
    elif(move.move_type == MOVE_TYPES['promotion']):
        if(move.captured_piece == 0):
            hyphen = "-"
        else:
            hyphen = "x"
        fmtmove= index_to_koord(move.src) + hyphen + index_to_koord(move.dest) + " " + reverse_lookup(PIECES, move.prom_piece)
        return fmtmove
    else:
        fmtmove= index_to_koord(move.src) + "x" + index_to_koord(move.dest) + " e.p."
        return fmtmove



    
