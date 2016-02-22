from named_constants import Constants


class Colors(Constants):
  undefined = 0
  white = 1
  black = 9


class Pieces(Constants):
  blk = Colors.undefined + 0 # 0
  wKg = Colors.white + 0 # 1
  wPw = Colors.white + 1 # 2
  wRk = Colors.white + 2 # 3
  wKn = Colors.white + 3 # 4
  wBp = Colors.white + 4 # 5
  wQu = Colors.white + 5 # 6
  bKg = Colors.black + 0 # 9 
  bPw = Colors.black + 1 # 10
  bRk = Colors.black + 2 # 11
  bKn = Colors.black + 3 # 12
  bBp = Colors.black + 4 # 13
  bQu = Colors.black + 5 # 14


dictPieces = dict()
dictPieces = { Pieces.blk:'blk',
               Pieces.wKg:'wKg',
               Pieces.wPw:'wPw',
               Pieces.wRk:'wRk',
               Pieces.wKn:'wKn',
               Pieces.wBp:'wBp',
               Pieces.wQu:'wQu',
               Pieces.bKg:'bKg',
               Pieces.bPw:'bPw',
               Pieces.bRk:'bRk',
               Pieces.bKn:'bKn',
               Pieces.bBp:'bBp',
               Pieces.bQu:'bQu' }


def reverse_lookup(dic, value):
    for key in dic:
        if dic[key] == value:
            return key
    raiseValueError


def color_of piece(piece):
  if(piece >= Pieces.wKg and piece <= Pieces.wQu):
    return Colors.white
  elif(piece >= Pieces.bKg and piece <= Pieces.bQu):
    return Colors.black
  else:
    return Colors.undefined


class MoveTypes(Constants):
  standard = 1
  short_castling = 2
  long_castling = 3
  promotion = 4 
  en_passant = 5
  

class MatchStatus(Constants):
  open = 1
  draw = 2
  winner_white = 3
  winner_black = 4
  cancelled = 5


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
    if(move.move_type == MoveTypes.standard):
        if(move.captured_piece == 0):
            hyphen = "-"
        else:
            hyphen = "x"
        fmtmove= index_to_koord(move.src) + hyphen + index_to_koord(move.dest)
        return fmtmove
    elif(move.move_type == MoveTypes.short_castling):
        return "0-0"
    elif(move.move_type == MoveTypes.long_castling):
        return "0-0-0"
    elif(move.move_type == MoveTypes.promotion):
        if(move.captured_piece == 0):
            hyphen = "-"
        else:
            hyphen = "x"
        fmtmove= index_to_koord(move.src) + hyphen + index_to_koord(move.dest) + " " + reverse_lookup(dictPieces, move.prom_piece)
        return fmtmove
    else:
        fmtmove= index_to_koord(move.src) + "x" + index_to_koord(move.dest) + " e.p."
        return fmtmove

