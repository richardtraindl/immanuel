

COLORS = {
    'undefined' : 0,
    'white' : 1,
    'black' : 9 }


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
    'bQu' : 14 } 


MOVE_TYPES = {
    'standard' : 1,
    'short_castling' : 2,
    'long_castling' : 3,
    'promotion' : 4,
    'en_passant' : 5 }

  

MATCH_STATUS = {
    'open' : 1,
    'draw' : 2,
    'winner_white' : 3,
    'winner_black' : 4,
    'cancelled' : 5 }


def reverse_lookup(dic, value):
    for key in dic:
        if dic[key] == value:
            return key
    raiseValueError


def color_of_piece(piece):
  if(piece >= PIECES['wKg'] and piece <= PIECES['wQu']):
    return COLORS['white']
  elif(piece >= PIECES['bKg'] and piece <= PIECES['bQu']):
    return COLORS['black']
  else:
    return COLORS['undefined']


def koord_to_index(koord):
    x = ord(koord[0]) - ord('a')
    y = ord(koord[1]) - ord('1')
    return x,y


def koord_to_index2(koord):
    col = koord[0]
    row = koord[1]
    idx = ord(col) - ord('a')
    idx += (ord(row) - ord('1')) *  8
    return idx


def index_to_koord(x, y):
    col = chr(x + ord('a'))
    row = chr(y + ord('1'))
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
        fmtmove= index_to_koord(move.srcx, move.srcy) + hyphen + index_to_koord(move.dstx, move.dsty)
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
        fmtmove= index_to_koord(move.srcx, move.srcy) + hyphen + index_to_koord(move.dstx, move.dsty) + " " + reverse_lookup(PIECES, move.prom_piece)
        return fmtmove
    else:
        fmtmove= index_to_koord(move.srcx, move.srcy) + "x" + index_to_koord(move.dstx, move.dsty) + " e.p."
        return fmtmove

